# The config script the owner ran by hand for the full run (transcript user message #178, 2026-10-18T08:43:50.407Z); output 'written. samples: 3'. It wrote training/configs/telugu_full.yaml on notebook `tts`. (run_pipeline.sh contains an earlier version of this step that failed on sample_freq/sample_sentences, then was fixed.)
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
assert not (set(ov) - hit), set(ov) - hit
c['sample_freq'] = 2500
c['sample_sentences'] = samples
c['model_overrides']['flow_lm.lookup_table.tokenizer_path'] = f'{h}/data/full/tokenizer.json'
yaml.safe_dump(c, open('training/configs/telugu_full.yaml', 'w'), sort_keys=False, allow_unicode=True)
print('written. samples:', len(samples)); print({k: c[k] for k in ('batch_size','grad_accum_steps','max_steps','valid_freq','ckpt_freq','num_ckpt_keep','sample_freq','run_dir')})
print(c['model_overrides'])
