# Given to the owner as a heredoc in the chat on 2026-10-18T05:41:38.676Z (assistant message); the owner's terminal paste (transcript message #133, 2026-10-18T05:42) shows its output: 'set: [...]' and 'NOT FOUND: [tokenizer_path]'.
# It wrote training/configs/telugu_pilot.yaml from finetune_language.yaml. The tokenizer path was then set by a separate python -c command (see logs/terminal_sessions_as_pasted.md, paste with 'tokenizer path set').
import os, sys, yaml
home = os.path.expanduser("~/SageMaker/tts")
cfg = yaml.safe_load(open("training/configs/finetune_language.yaml"))
ov = {
    "train_jsonl": f"{home}/data/pilot/train_aligned.jsonl",
    "valid_jsonl": f"{home}/data/pilot/valid_aligned.jsonl",
    "tokenizer_path": f"{home}/data/pilot/tokenizer.model",
    "run_dir": f"{home}/runs/telugu_pilot",
    "batch_size": 16, "grad_accum_steps": 4, "max_steps": 200, "warmup_steps": 50,
    "valid_freq": 100, "ckpt_freq": 200, "num_ckpt_keep": 1,
}
hit = set()
def walk(d):
    for k, v in d.items():
        if k in ov:
            d[k] = ov[k]; hit.add(k)
        elif isinstance(v, dict):
            walk(v)
walk(cfg)
print("set:", sorted(hit)); print("NOT FOUND:", sorted(set(ov) - hit))
yaml.safe_dump(cfg, open("training/configs/telugu_pilot.yaml", "w"), sort_keys=False)
