# Telugu teacher fine-tune run sheet (deadline: end of day 2026-10-18), written 2026-10-17

**Status:** PROPOSED; nothing started. **Scope (TD-008):** fine-tune the ~313M 24-layer Pocket TTS teacher on **Telugu only**. **No distillation, no Hindi.** If the Telugu result is good, the goal is met. This sheet replaces `hindi_run_sheet.md` for now (kept for later).
**Labels:** [M] read from a primary source; [E] our estimate; [P] proposal; [U] unverified.

## 0. What changes compared with the Hindi sheet
- Language Telugu; Telugu script, sentences end with `.` (no danda); long agglutinative words; digits become Telugu words.
- Only the teacher stage (`finetune_language.yaml`). The deliverable is the fine-tuned 24-layer checkpoint and its generated audio.
- Compute depends on the notebook type the senior chooses (TA-019): 1x A10G or 8x A10G.

## 1. Data
| Source | Licence | Size | Estimated hours |
|---|---|---|---|
| SYSPIN Telugu female (`TEL_F_SPK001`), from S3 `raw/syspin/` | CC-BY-4.0 per IISc | 24.27 GiB | **~56 h [E, scaled from the male file's 0.46 GB per hour]; exact figure in its readme after extraction** |
| SYSPIN Telugu male (`TEL_M_SPK001`) | CC-BY-4.0 per IISc | 20.87 GiB (22,411,247,515 bytes) | **48 h 20 min 26 s, 21,463 sentences, avg 8.1 s [M, its readme]**; one male speaker aged 63; 48 kHz, 24-bit, mono; domains AGRI, BOCU, BOOK, EDUC, FINA, GENE, HEAL, OTHE, POLI, WEAT |
| Rasa Telugu (`ai4bharat/Rasa`, gate accepted, `10xwath`) | CC-BY-4.0 | female 27.28 h + male 24.98 h | **52.26 h** [M] |
| **Total teacher data** | | | **about 156 h** (SYSPIN ~104 h + Rasa 52.3 h; earlier figure of ~139 h was too low because the SYSPIN hours were underestimated) |
Validation: hold out ~2-3% by speaker session (~3 h). Test: ~30-50 Telugu sentences we write (`tts/eval/telugu_test_sentences.txt`, to be proofread by a Telugu speaker), never used in training. Kyutai's guidance: 100 h minimum, 200 h "speaks", 2,000 h "sounds good" [M].

## 2. Steps (hours are estimates [E])
1. **Notebook ready (senior).** Type chosen by the senior; data under `~/SageMaker` only; run `tts/scripts/setup_instance.sh` (untested): checks GPU(s), installs ffmpeg/sox via conda if missing, installs `uv`, clones `kyutai-labs/pocket-tts`, `uv sync`. Log in to Hugging Face on the notebook yourself (`hf auth login`). ~30-45 min.
2. **Pull the data.** `aws s3 cp s3://aarav-10x/raw/syspin/<archive> ~/SageMaker/data/raw/` for both archives (same region, minutes), extract with `tar -xzf` (use `pigz -dc | tar -x` if `pigz` exists); download Rasa Telugu from Hugging Face. **Look at the layout first** (folders, transcript files, metadata); the scripts depend on it. ~30-60 min.
3. **Count and listen.** Sum clip durations per speaker (exact hours), listen to 20 clips per speaker, read the SYSPIN README. ~15 min.
4. **Pilot (~5-10 h of audio, one archive):** clean, align, train the tokenizer, run ~200 training steps, generate 3 sentences. Finds problems early. ~45-60 min.
5. **Audio cleaning (all clips):** resample to 24 kHz mono; trim only the ends (about -40 dB, keep ~0.25 s); loudness-normalise; drop clips under 1 s, over 30 s, clipped or near-silent. Parallel across CPU cores. ~20-40 min.
6. **Text cleaning:** NFC; remove zero-width characters except as the aligner vocabulary requires [check]; keep `, . ? !`; **digits to Telugu words** (library support for Telugu unverified; otherwise a small converter tested on examples); common abbreviations; **English loanwords stay in Telugu script as in the data**; keep only clips whose characters are in the aligner's vocabulary; log rejected lines. ~30 min to write and test.
7. **Align:** `python -m training.scripts.align_data <in.jsonl> <out.jsonl> --model <Telugu char-level Wav2Vec2ForCTC> --device cuda` [M for the script]. Candidates: AI4Bharat IndicWav2Vec Telugu (MIT; exact Hugging Face name still to be located) or `anuragshas/wav2vec2-large-xlsr-53-telugu` (Apache-2.0, ~45% WER on its own test, trained on OpenSLR SLR66). Spot-check 50 clips; drop unalignable lines. **Riskiest step.** ~1-2 h.
8. **Tokenizer:** the repo's `train_tokenizer.py`, 4k SentencePiece on the Telugu transcripts → `data/tokenizer.model`. ~5 min.
9. **Config:** copy `training/configs/finetune_language.yaml` to `telugu_teacher.yaml`; set `flow_lm.lookup_table.tokenizer_path: data/tokenizer.model`; `train_jsonl`/`valid_jsonl` to our aligned files; `run_dir: runs/telugu_teacher`; keep `lr: 2e-4` constant, `warmup_steps: 1000`, `reset_text_embedding: true`, `start_from_pretrained: true`, `max_duration_sec: 30`; **effective batch 64**: on 1 GPU `batch_size: 16, grad_accum_steps: 4`; on 8 GPUs launch with `torchrun --nproc-per-node 8` and `batch_size: 8` per GPU, `grad_accum_steps: 1` (README: ~12 GiB per GPU at batch 8) [M]; `max_steps: 30000`, checkpoints every 2,500; **`num_ckpt_keep: 3`**. The `finetune_language.yaml` header notes Czech reached 12% WER by 10k steps [M].
10. **Train** inside `tmux`: `uv run training/train.py training/configs/telugu_teacher.yaml` (or `uv run torchrun ... training/train.py ...`). **Time [E, unmeasured]:** 1x H100 does 6.3 steps/s at batch 64 [M]; an A10G is roughly 6-8x slower, so 15-30k steps take about 4-11 h on one A10G; 8x A10G might need about 40-90 min if scaling is good. Run `tts/scripts/sync_to_s3.sh` in a second tmux window to back checkpoints up every 10 minutes. First run precomputes latents (minutes).
11. **Evaluate at 10k, 15k, 20k and the last checkpoint:** generate the test sentences **one sentence at a time** (`uv run pocket-tts generate --config <yaml> --checkpoint <ckpt> --voice <prompt.wav> --text "..."`), with a voice prompt from a held-out SYSPIN or Rasa clip; sweep `--eos-threshold` once on a pinned checkpoint. **Judge:** reads the audio back; use **IndicConformer Telugu** via `ai4bharat/indic-conformer-600m-multilingual` (`transformers` with `trust_remote_code`, MIT tag, the gate must be accepted with `10xwath`) so the AI4Bharat NeMo fork is not needed; compare its character error rate with its error rate on real held-out speech from the same speakers. **Listening:** 3-5 colleagues rate 10-20 sentences 1-5 and compare against Prasad's Telugu model by ear. ~1-2 h.
12. **Pick the checkpoint, back up to S3, write the short report (numbers, audio samples, what failed), and STOP the notebook.** ~1 h.

## 3. Proposed success marks [P] (not agreed with the senior)
Judge CER within ~1.5x of its CER on real speech; mean listening score >= 3.5/5 from the colleagues; at least 90% of test sentences with no skipped or repeated words; numbers and dates read correctly in at least 80% of the sentences that contain them; not obviously worse than Prasad's Telugu model by ear.

## 4. Wall-clock and cost [E]
8x A10G: about 7-9 h in total, about $130-210 (price tracker $16.29 per hour for the EC2 type; SageMaker likely higher [U]). 1x A10G: about 14-22 h in total, about $20-40. Hybrid (small type for data work, big type for training only): about $40-80. Stop the notebook whenever work pauses.

## 5. Risks
1. Telugu aligner quality or its character vocabulary not matching Telugu conjuncts and marks; fall back to the other candidate or to alignment with the IndicConformer judge model [U].
2. SYSPIN layout and transcript format unknown until extraction.
3. Training speed unmeasured; the senior's choice of instance type (TA-019).
4. The judge is itself weak on Telugu (about 26 WER on public sets), so scores are noisy; the listening test carries more weight.
5. Digits and numbers in Telugu text.
6. Voice rights: a shipped voice is a real person from a CC-BY dataset (TL-05); internal demo only.
7. Dead time: notebook left running costs money; scripts untested.
8. The 24-layer teacher is slower on CPU than the planned 6-layer student; speed on laptops is not part of tomorrow's goal.
