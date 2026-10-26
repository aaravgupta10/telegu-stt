# Config deltas against Kyutai's `training/configs/finetune_language.yaml`

**Important:** the upstream YAML file itself was never saved on this machine (UNKNOWN - not found in records). Its values below come from two recorded readings: the browser-pane read of 2026-10-14 (`PL` TA-006) and the helper-agent report of the repo's `args.py`/`finetune_language.yaml` on 2026-10-18 (transcript). Everything not listed as changed was left at the upstream value (the two resolved configs in `configs/` show the full set of values the trainer actually used).

Our two files were created by scripts (`diffs/new_files/from_transcript/make_pilot_cfg.py`, `make_telugu_full_cfg_handrun.py`) that load the upstream YAML, override only the keys below, and write `training/configs/telugu_pilot.yaml` / `telugu_full.yaml` inside the notebook's checkout.

| Key | Upstream value (source) | Pilot (TRUN-0001) | Full run (TRUN-0002) |
|---|---|---|---|
| `batch_size` | **64** [subagent report of args.py/finetune_language.yaml, transcript 2026-10-18; 'batch_size: 64 and grad_accum_steps: 1'] | `16` | `16` (**changed from upstream in BOTH runs**; per GPU) |
| `ckpt_freq` | 2500 [same] | `200` | `2500` |
| `data.train_jsonl` | a path under data/ (exact value UNKNOWN - upstream file not kept) [PL TA-006] | `/home/ec2-user/SageMaker/tts/data/pilot/train_aligned.jsonl` | `/home/ec2-user/SageMaker/tts/data/full/train_aligned.jsonl` |
| `data.valid_jsonl` | a path under data/ (exact value UNKNOWN) [PL TA-006] | `/home/ec2-user/SageMaker/tts/data/pilot/valid_aligned.jsonl` | `/home/ec2-user/SageMaker/tts/data/full/valid_aligned.jsonl` |
| `grad_accum_steps` | 1 [same] | `4` | `1` |
| `max_steps` | 250000 (comment: WER plateaus by ~15k) [PL TA-006 [M], browser read 2026-10-14] | `200` | `15000` |
| `model_overrides.flow_lm.lookup_table.tokenizer_path` | data/tokenizer.model [PL TA-006 [M]] | `/home/ec2-user/SageMaker/tts/data/pilot/tokenizer.json` | `/home/ec2-user/SageMaker/tts/data/full/tokenizer.json` |
| `num_ckpt_keep` | 3 [same] | `1` | `3` |
| `optim.warmup_steps` | 1000 [PL TA-006 [M]] | `50` | `1000` |
| `run_dir` | runs/finetune_language [same] | `/home/ec2-user/SageMaker/tts/runs/telugu_pilot` | `/home/ec2-user/SageMaker/tts/runs/telugu_full` |
| `sample_freq` | not in the yaml; built-in default 10000 [subagent report of args.py; and the pilot's resolved config shows 10000] | `10000` | `2500` |
| `sample_sentences` | not in the yaml; built-in default = 3 English sentences [pilot resolved config (msg #140)] | `['The quick brown fox jumps over the lazy dog.', 'Training is still running; thi` | `['అలాగే ఆ సీన్ ఓ రూంలో జరుగుతుంటే కెమెరా, టెక్నీషియన్స్ అంతా మరో రూంలో కూర్చొని ` |
| `valid_freq` | 2500 [subagent report, same date] | `100` | `2500` |

**Keys identical in the pilot and the full run** (and therefore equal to upstream unless listed in the table above; note `batch_size` is in the table because it differs from upstream although it is the same in both runs): `compile`, `data.final_punct_dropout`, `data.loader_procs`, `data.max_duration_sec`, `data.max_voice_prompt_sec`, `data.num_bucket_batches`, `data.precompute`, `data.prompt_trim_max_sec`, `data.shuffle`, `distill_cfg_coef`, `distill_teacher_config`, `distill_teacher_overrides`, `distill_teacher_use_ema`, `distill_teacher_weights`, `ema_decay`, `eos_loss_weight`, `flow.kwargs`, `flow.type`, `flow_batch_multiplier`, `freeze_head`, `log_freq`, `model_config`, `num_valid_batches`, `optim.betas`, `optim.eps`, `optim.lr`, `optim.lr_min_ratio`, `optim.max_norm`, `optim.muon_head`, `optim.muon_lr`, `optim.muon_momentum`, `optim.muon_polar_steps`, `optim.muon_rms_match`, `optim.schedule`, `optim.type`, `optim.weight_decay`, `reset_text_embedding`, `seed`, `start_from_pretrained`, `stats_ema_decay`, `stats_ema_steps`, `student_init_from`, `text_dropout`, `voice_dropout`.

**Notes**
- The full run's `sample_sentences` are three Telugu validation transcripts (exact text in `data_samples/trainer_sample_sentences_exact.txt`); the pilot kept the default English sentences (never synthesised: `sample_freq` 10000 > 200 steps).
- Effective batch is `batch_size x grad_accum_steps x number of GPUs` [M, `args.py` comment]: pilot 16 x 4 x 1 = 64; full 16 x 1 x 4 = 64; this equals the upstream default (64 x 1 x 1).
- `warmup_steps` stayed 1000 in the full run (upstream value); the pilot used 50.
- Unchanged key facts: `reset_text_embedding: true`, `start_from_pretrained: true`, lr 2e-4 constant, `ema_decay` 0.999, `max_duration_sec` 30, `model_config: pocket_tts/config/english_2026-04_24l.yaml`.
