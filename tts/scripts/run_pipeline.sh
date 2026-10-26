#!/usr/bin/env bash
# Unattended: wait for the Rasa download and the SYSPIN prep, prepare Rasa, combine all three datasets,
# align on 4 GPUs, train the tokenizer, write the training config. STOPS BEFORE TRAINING (that spends money; a human starts it).
# STATUS: written 2026-10-18; only syntax-checked locally (bash -n), never run end to end. Watch ~/SageMaker/tts/logs/pipeline.log.
# Start:  nohup bash ~/SageMaker/tts/scripts/run_pipeline.sh > ~/SageMaker/tts/logs/pipeline.out 2>&1 &
set -uo pipefail
T="$HOME/SageMaker/tts"
D="$T/data/full"
LOG="$T/logs/pipeline.log"
ALIGN_MODEL="anuragshas/wav2vec2-large-xlsr-53-telugu"
say() { echo "$(date -u +%T) $*" | tee -a "$LOG"; }
fail() { say "FAILED at stage: $1. Pipeline stopped. Nothing after this stage ran."; exit 1; }
source "$T/env.sh"
cd "$T/pocket-tts" || fail "cd pocket-tts"
# refuse to run twice at once (two copies write the same files); the lock is removed when the script ends
if ! mkdir "$T/logs/pipeline.lock" 2>/dev/null; then
  echo "Another run_pipeline.sh is active (or crashed: then run  rmdir $T/logs/pipeline.lock ). Not starting."; exit 1
fi
trap 'rmdir "$T/logs/pipeline.lock" 2>/dev/null' EXIT
say "pipeline started"

# ---- stage 0: Rasa prep (skipped when its output already exists; FRESH_RASA=1 deletes it and redoes it)
if [ "${FRESH_RASA:-0}" = "1" ]; then say "FRESH_RASA=1: deleting data/full_Rasa"; rm -rf "$T/data/full_Rasa"; fi
RP=""
if [ -f "$T/data/full_Rasa/train.jsonl" ]; then
  say "Rasa prep already done, skipping"
else
  while pgrep -f "hf download" > /dev/null; do sleep 15; done
  n=$(ls "$T"/data/rasa/Telugu/*.parquet 2>/dev/null | wc -l)
  say "Rasa download finished, parquet files: $n (expected 63)"
  [ "$n" -ge 63 ] || fail "Rasa download incomplete ($n of 63 parquet files)"
  uv run --with pyarrow python "$T/scripts/prep_rasa.py" --root "$T/data/rasa" --out "$T/data/full_Rasa" --workers 44 > "$T/logs/prep_Rasa.log" 2>&1 &
  RP=$!
  say "Rasa prep started (pid $RP)"
fi

# ---- stage 1: SYSPIN prep must be finished
while pgrep -f prep_syspin.py > /dev/null; do sleep 15; done
for s in Male Female; do [ -f "$T/data/full_$s/train.jsonl" ] || fail "SYSPIN $s prep (no train.jsonl)"; done
say "SYSPIN prep finished"
if [ -n "$RP" ]; then wait "$RP" || fail "Rasa prep (see logs/prep_Rasa.log)"; fi
[ -f "$T/data/full_Rasa/train.jsonl" ] || fail "Rasa prep (no train.jsonl)"
say "Rasa prep finished"

# ---- stage 2: combine
mkdir -p "$D"
for f in train valid; do
  cat "$T/data/full_Male/$f.jsonl" "$T/data/full_Female/$f.jsonl" "$T/data/full_Rasa/$f.jsonl" > "$D/$f.jsonl"
done
say "combined: $(wc -l < "$D/train.jsonl") train, $(wc -l < "$D/valid.jsonl") valid"
python3 - <<'EOF' | tee -a "$LOG"
import json, os
t = 0.0
for s in ("Male", "Female", "Rasa"):
    h = json.load(open(os.path.expanduser(f"~/SageMaker/tts/data/full_{s}/stats.json")))["hours_kept"]
    print(f"hours kept {s}: {h}"); t += h
print(f"hours kept TOTAL: {round(t, 1)}")
EOF

# ---- stage 3: align, train list split in 4 (one GPU each), valid on GPU 0
rm -f "$D"/trpart_* "$D"/train_aligned.jsonl "$D"/valid_aligned.jsonl
split --additional-suffix=.jsonl -n l/4 -d "$D/train.jsonl" "$D/trpart_"
pids=""
for i in 0 1 2 3; do
  PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=$i env -u LD_LIBRARY_PATH uv run python -m training.scripts.align_data "$D/trpart_0$i.jsonl" "$D/trpart_0${i}_aligned.jsonl" --model "$ALIGN_MODEL" --device cuda > "$T/logs/align_$i.log" 2>&1 &
  pids="$pids $!"
done
say "alignment of train started on 4 GPUs"
for p in $pids; do wait "$p" || fail "alignment of a train part (see logs/align_*.log)"; done
PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True CUDA_VISIBLE_DEVICES=0 env -u LD_LIBRARY_PATH uv run python -m training.scripts.align_data "$D/valid.jsonl" "$D/valid_aligned.jsonl" --model "$ALIGN_MODEL" --device cuda > "$T/logs/align_valid.log" 2>&1 || fail "alignment of valid"
cat "$D"/trpart_00_aligned.jsonl "$D"/trpart_01_aligned.jsonl "$D"/trpart_02_aligned.jsonl "$D"/trpart_03_aligned.jsonl > "$D/train_aligned.jsonl"
na=$(wc -l < "$D/train_aligned.jsonl"); nt=$(wc -l < "$D/train.jsonl"); nv=$(wc -l < "$D/valid_aligned.jsonl")
say "aligned: train $na of $nt, valid $nv"
[ $((na * 100)) -ge $((nt * 95)) ] || fail "alignment lost more than 5% of train clips ($na of $nt)"
[ "$nv" -ge 1 ] || fail "no valid clips aligned"

# ---- stage 4: tokenizer
env -u LD_LIBRARY_PATH uv run python -m training.scripts.train_tokenizer "$D/tokenizer" "$D/train_aligned.jsonl" > "$T/logs/tokenizer.log" 2>&1 || fail "train_tokenizer (see logs/tokenizer.log)"
[ -f "$D/tokenizer.model" ] || fail "no tokenizer.model"
env -u LD_LIBRARY_PATH uv run python -m training.scripts.convert_tokenizer "$D/tokenizer.model" --texts "$D/valid_aligned.jsonl" 2>&1 | tail -3 | tee -a "$LOG"
[ -f "$D/tokenizer.json" ] || fail "no tokenizer.json"
say "tokenizer done"

# ---- stage 5: config (4 GPUs: batch 16 per GPU, accum 1 -> effective 64)
env -u LD_LIBRARY_PATH uv run python - <<'EOF' 2>&1 | tee -a "$LOG" || fail "config"
import json, os, yaml
h = os.path.expanduser('~/SageMaker/tts')
c = yaml.safe_load(open('training/configs/finetune_language.yaml'))
samples = []
for line in open(f'{h}/data/full/valid.jsonl', encoding='utf-8'):
    t = json.loads(line)['transcript']
    if 40 <= len(t) <= 90 and not any(ch.isdigit() for ch in t):
        samples.append(t)
    if len(samples) == 3:
        break
ov = {
  'train_jsonl': f'{h}/data/full/train_aligned.jsonl', 'valid_jsonl': f'{h}/data/full/valid_aligned.jsonl',
  'run_dir': f'{h}/runs/telugu_full', 'batch_size': 16, 'grad_accum_steps': 1, 'max_steps': 15000,
  'valid_freq': 2500, 'ckpt_freq': 2500, 'num_ckpt_keep': 3,
}
hit = set()
def walk(d):
    for k, v in d.items():
        if k in ov: d[k] = ov[k]; hit.add(k)
        elif isinstance(v, dict): walk(v)
walk(c)
c['sample_freq'] = 2500            # not in the yaml (built-in defaults), so set at the top level
c['sample_sentences'] = samples
c['model_overrides']['flow_lm.lookup_table.tokenizer_path'] = f'{h}/data/full/tokenizer.json'
print('config keys set:', sorted(hit)); print('NOT FOUND:', sorted(set(ov) - hit)); print('sample sentences:', len(samples))
assert not (set(ov) - hit), 'some config keys were not found'
yaml.safe_dump(c, open('training/configs/telugu_full.yaml', 'w'), sort_keys=False, allow_unicode=True)
EOF
[ -f training/configs/telugu_full.yaml ] || fail "config file not written"
say "READY. Config written: training/configs/telugu_full.yaml. Training has NOT been started (needs a human go-ahead)."
df -h "$T" | tail -1 | tee -a "$LOG"
