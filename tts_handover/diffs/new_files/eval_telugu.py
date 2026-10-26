#!/usr/bin/env python3
"""Evaluate a Pocket TTS Telugu checkpoint on the CPU (so training keeps the GPUs).

STATUS: written 2026-10-18; syntax-checked only, never run. Run it with:
  cd ~/SageMaker/tts/pocket-tts && source ~/SageMaker/tts/env.sh && \
  uv run python ~/SageMaker/tts/scripts/eval_telugu.py --checkpoint ~/SageMaker/tts/runs/telugu_full/checkpoint_00002500.pt \
      --out ~/SageMaker/tts/runs/telugu_full/eval_2500

What it does
1. Writes a generation config (the English 24-layer config with our tokenizer.json).
2. VALID MODE: takes N clips spread evenly over valid.jsonl (male + female + Rasa), and for each one synthesises its transcript
   with that clip's own audio as the voice prompt (the clip itself was never trained on).
3. SENTENCES MODE (optional, --sentences FILE): synthesises each digit-free sentence with two voice prompts.
4. Reads everything back with a Telugu CTC recogniser (default anuragshas/wav2vec2-large-xlsr-53-telugu) and reports character error
   rate (CER) for the real recordings (baseline) and for our generated audio on the SAME texts, plus the generated/real length ratio.
CER here is only a relative number (the recogniser is weak): compare generated vs real, not against zero.
Generation uses the documented CLI: pocket-tts generate --config --checkpoint --voice --text --output-path (one sentence per call).
"""
import argparse
import json
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HOME = os.path.expanduser("~/SageMaker/tts")
PUNCT = re.compile(r"[,.?!;:\"'()\-]")


def norm(t: str) -> str:
    return re.sub(r"\s+", " ", PUNCT.sub(" ", t)).strip()


def make_gen_config(tokenizer_json: str, out_path: Path) -> str:
    import yaml
    c = yaml.safe_load(open("pocket_tts/config/english_2026-04_24l.yaml"))
    c["flow_lm"]["lookup_table"]["tokenizer_path"] = tokenizer_json
    yaml.safe_dump(c, open(out_path, "w"), sort_keys=False)
    return str(out_path)


def generate(job):
    cfg, ckpt, voice, text, out, device = job
    env = dict(os.environ, OMP_NUM_THREADS="4", MKL_NUM_THREADS="4")
    cmd = ["pocket-tts", "generate", "--config", cfg, "--checkpoint", ckpt, "--voice", voice,
           "--text", text, "--output-path", out, "--device", device, "-q"]
    r = subprocess.run(cmd, capture_output=True, text=True, env=env)
    ok = r.returncode == 0 and Path(out).exists()
    return out, ok, ("" if ok else r.stderr[-300:])


def load_asr(name):
    import torch
    from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
    torch.set_num_threads(8)
    proc = Wav2Vec2Processor.from_pretrained(name)
    model = Wav2Vec2ForCTC.from_pretrained(name).eval()
    return model, proc


def transcribe(model, proc, wav_path):
    import soundfile as sf
    import torch
    import torchaudio
    x, sr = sf.read(wav_path, dtype="float32")
    if x.ndim > 1:
        x = x.mean(axis=1)
    t = torch.from_numpy(x)
    if sr != 16000:
        t = torchaudio.functional.resample(t, sr, 16000)
    inp = proc(t.numpy(), sampling_rate=16000, return_tensors="pt").input_values
    with torch.no_grad():
        ids = model(inp).logits.argmax(-1)
    return proc.batch_decode(ids)[0]


def seconds(path):
    import soundfile as sf
    return sf.info(path).duration


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--checkpoint", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--valid-jsonl", default=f"{HOME}/data/full/valid.jsonl")
    ap.add_argument("--tokenizer", default=f"{HOME}/data/full/tokenizer.json")
    ap.add_argument("--n-valid", type=int, default=24)
    ap.add_argument("--train-jsonl", default=f"{HOME}/data/full/train.jsonl",
                    help="used to drop validation clips whose exact text also appears in training (about 16% here)")
    ap.add_argument("--include-seen", action="store_true", help="also use validation clips whose text appears in training")
    ap.add_argument("--sentences", default="", help="optional text file, one sentence per line")
    ap.add_argument("--voices", nargs="*", default=[], help="reference wav paths for the sentences (default: one SYSPIN male and one SYSPIN female validation clip)")
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--asr-model", default="anuragshas/wav2vec2-large-xlsr-53-telugu")
    args = ap.parse_args()

    out = Path(os.path.expanduser(args.out))
    out.mkdir(parents=True, exist_ok=True)
    cfg = make_gen_config(os.path.expanduser(args.tokenizer), out / "gen.yaml")
    ckpt = os.path.expanduser(args.checkpoint)

    rows = [json.loads(l) for l in open(os.path.expanduser(args.valid_jsonl), encoding="utf-8")]
    pool = rows
    tj = os.path.expanduser(args.train_jsonl)
    if not args.include_seen and os.path.exists(tj):
        train_texts = {norm(json.loads(l)["transcript"]) for l in open(tj, encoding="utf-8")}
        pool = [r for r in rows if norm(r["transcript"]) not in train_texts]
        print(f"validation clips with text NOT seen in training: {len(pool)} of {len(rows)}", flush=True)
    elif not args.include_seen:
        print("WARNING: train jsonl not found, cannot exclude validation clips whose text was seen in training", flush=True)
    step = max(1, len(pool) // args.n_valid)
    clips = pool[::step][: args.n_valid]

    jobs, meta = [], []
    for i, r in enumerate(clips):
        o = str(out / f"valid_{i:02d}.wav")
        jobs.append((cfg, ckpt, r["path"], r["transcript"], o, args.device))
        meta.append(("valid", o, r["transcript"], r["path"], r["duration"]))
    if args.sentences:
        voices = [os.path.expanduser(v) for v in args.voices]
        if not voices:  # the voices we would most likely ship: a clean SYSPIN studio male and female clip
            for tag in ("_te_m_", "_te_f_"):
                hit = next((r["path"] for r in rows if tag in r["path"]), None)
                if hit:
                    voices.append(hit)
        if not voices:
            voices = [rows[len(rows) // 4]["path"], rows[3 * len(rows) // 4]["path"]]
        print("sentence voices:", voices, flush=True)
        sents = [s.strip() for s in open(os.path.expanduser(args.sentences), encoding="utf-8") if s.strip()]
        sents = [s for s in sents if not re.search(r"[0-9]", s)]
        for j, s in enumerate(sents):
            for v, vp in enumerate(voices):
                o = str(out / f"sent_{j:02d}_v{v}.wav")
                jobs.append((cfg, ckpt, vp, s, o, args.device))
                meta.append(("sentence", o, s, vp, None))

    print(f"generating {len(jobs)} clips on {args.device} with {args.workers} workers ...", flush=True)
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        results = list(ex.map(generate, jobs))
    failed = [(o, err) for o, ok, err in results if not ok]
    print(f"generated {len(jobs) - len(failed)} of {len(jobs)}; failed {len(failed)}", flush=True)
    for o, err in failed[:3]:
        print("FAILED", o, err.replace("\n", " | "), flush=True)

    print("loading recogniser ...", flush=True)
    model, proc = load_asr(args.asr_model)
    import jiwer

    table = []
    for (kind, wav, text, voice_path, real_dur), (_, ok, _e) in zip(meta, results):
        if not ok:
            continue
        hyp_gen = norm(transcribe(model, proc, wav))
        gen_dur = seconds(wav)
        row = {"kind": kind, "wav": wav, "text": norm(text), "hyp_generated": hyp_gen, "gen_seconds": round(gen_dur, 2),
               "cer_generated": jiwer.cer(norm(text), hyp_gen) if hyp_gen else 1.0}
        if kind == "valid":
            hyp_real = norm(transcribe(model, proc, voice_path))
            row.update({"real_seconds": round(real_dur, 2), "length_ratio": round(gen_dur / real_dur, 2),
                        "hyp_real": hyp_real, "cer_real": jiwer.cer(norm(text), hyp_real) if hyp_real else 1.0})
        table.append(row)
        print(f"{kind:8s} CER gen {row['cer_generated']:.2f}"
              + (f" | real {row['cer_real']:.2f} | length ratio {row['length_ratio']}" if kind == "valid" else f" | {row['gen_seconds']} s")
              + f" | {os.path.basename(wav)}", flush=True)

    json.dump(table, open(out / "results.json", "w"), ensure_ascii=False, indent=1)
    v = [r for r in table if r["kind"] == "valid"]
    s = [r for r in table if r["kind"] == "sentence"]
    mean = lambda xs: sum(xs) / len(xs) if xs else float("nan")
    print("\n===== SUMMARY (checkpoint:", os.path.basename(ckpt), ") =====")
    if v:
        print(f"VALID clips ({len(v)}): CER real recordings {mean([r['cer_real'] for r in v]):.3f} | CER generated {mean([r['cer_generated'] for r in v]):.3f}"
              f" | mean length ratio gen/real {mean([r['length_ratio'] for r in v]):.2f}"
              f" | clips under 0.5x length {sum(1 for r in v if r['length_ratio'] < 0.5)}")
    if s:
        print(f"SENTENCES ({len(s)} clips): CER generated {mean([r['cer_generated'] for r in s]):.3f} | mean length {mean([r['gen_seconds'] for r in s]):.1f} s")
    print("wavs and results.json in", out)


if __name__ == "__main__":
    main()
