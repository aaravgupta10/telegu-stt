# PROCESS REPORT: Telugu text-to-speech fine-tune of Kyutai Pocket TTS

**Compiled:** 2026-10-18, evening IST, by Claude Code (the assistant that worked on this project with the owner), at the senior's request.
**How it was compiled:** only from files, logs, pasted terminal output and the Claude Code session transcript. **Nothing was trained, run, benchmarked, downloaded or installed to write this.** Existing logs were only exported to CSV.
**Rules followed:** anything not confirmable from the records is written `UNKNOWN - not found in records`; anything deduced is labelled `INFERRED from <source>`; secrets are redacted (no token, key or signed link appears here; the two chat messages that contained signed SYSPIN links were deliberately not copied).

---

## READ THIS FIRST: how complete is this record?

| # | Section | Completeness | What is missing |
|---|---|---|---|
| 1 | Goal | Complete | Target device and number of voices were never decided (open questions) |
| 2 | Base | Mostly complete | Commit of the pilot notebook; the repo's LICENSE file itself was never opened (licence facts come from GitHub API / HF page captures) |
| 3 | Fine-tune vs pretrain | Complete | |
| 4 | Environment | Partial | GPU driver version, ffmpeg version, kernel, instance type of the training notebook (inferred), pilot package list: UNKNOWN |
| 5 | Code changes | **Mostly UNKNOWN for diffs** | No git checkout of the notebooks' repos exists on this machine, so no `git diff` could be produced. No code change is recorded anywhere (see Section 5 for the evidence and the one caveat) |
| 6 | Text side | Mostly complete | Actual tokenizer vocabulary size, token ids, and cleaned versions of Rasa rows: UNKNOWN |
| 7 | Audio side | Mostly complete | |
| 8 | Data | Partial | **"10 sample lines from each manifest" could not be provided**: the manifests lived only on the notebooks and were never copied; substitutes are in `data_samples/`. Per-source split sizes, full-run reject counts, Rasa style mix: UNKNOWN |
| 9 | Training runs | Complete for the two real runs and two failed starts | Pilot checkpoint backup status UNKNOWN |
| 10 | Commands | Partial | Exact commands exist for most steps (from pasted terminal text); 4 commands exist only as the assistant's advice, and the shell history files of the notebooks were never copied (UNKNOWN) |
| 11 | Problems | Complete as recorded | |
| 12 | Decisions | Complete as recorded | |
| 13 | Current state | Complete | |
| 14 | Existing audio | Complete | |
| 15 | Limitations | Complete as recorded | |
| 16 | Timeline | Complete | |

**Conventions.** Times in the session transcript are **UTC** (`Z`); the project log `tts/progress.md` uses **IST dates** (UTC+5:30), so entries dated 2026-10-15 in that log were written on the evening of 2026-10-14 UTC. `msg #N` = the N-th real user message of the session transcript (numbered in `transcripts_summary.md`); `PL` = `tts/progress.md` (full copy in `source_docs/tts_progress_log_FULL.md`); `TA-nnn`/`TD-nnn` = log entries/decisions in `PL`; `TS` = `logs/terminal_sessions_as_pasted.md`. Evidence labels as in `PL`: [M] read from a cited source, [V] vendor/author claim, [E] our estimate, [P] proposal, [U] unverified, [OURS] our own measurement.

**Documentation problems found while compiling** (so the reviewer is not misled by the original files):
1. `PL` Section 2 (status snapshot) and Section 5 (ledgers) were stale: they still said "nothing downloaded, trained or spent" and "$0 spend". They are being refreshed (see the last entry of `PL`).
2. `PL` Section 3 has no row for TD-009 although TA-029 refers to it (the decision "pilot on ml.g5.2xlarge, training on ml.g5.12xlarge", 2026-10-17).
3. `TD-008` says the plan would follow in "pipeline.md REVISION v1.3"; that revision was never written (only v1.1 and v1.2 exist); the Telugu plan is `tts/telugu_teacher_run_sheet.md`.
4. The `tts` notebook was seen as ml.g5.48xlarge on 2026-10-17 (TA-019, created 2026-10-16 20:24 UTC) but the training run shows 4 GPUs. **Update 2026-10-19:** the console page of notebook `tts` (screenshot 27.png, owner, 2026-10-19) shows **type ml.g5.12xlarge, Amazon Linux 2023 / JupyterLab 4, 400 GB EBS, created 2026-10-17 17:45 UTC**. So the notebook used for training is a newer notebook with the same name `tts` as the 48xlarge one; the replacement of the old notebook is not recorded anywhere else.
5. **The tokenizer file is NOT in this package and NOT in S3 (found 2026-10-19).** The model cannot be used without `tokenizer.json` (and its source `tokenizer.model`): the model's text embedding was trained against exactly that vocabulary, and a re-trained tokenizer would not match. The files exist only on the notebook `tts` disk (`~/SageMaker/tts/data/full/tokenizer.json` and `tokenizer.model`, written 2026-10-18 08:27 UTC). The checkpoint sync loop copied checkpoints, samples and logs but not the data folder, and the optional data backup (`tts_backup/`) is not in the bucket (owner checked S3, 2026-10-19). **Update 2026-10-19 (same day): `tokenizer.json` was copied off the notebook by the owner and is now in this package as `artifacts/tokenizer.json`; whether it has been backed up to S3 is UNKNOWN, and `tokenizer.model` was added the same day (`artifacts/tokenizer.model`, verified to match the JSON: 25 of 25 sentences give identical ids).** Both files are now in this package; they should still be backed up to S3. Also not backed up anywhere off the notebook: the prepared WAVs and the reference voice clips (the raw archives are in S3, so they can be rebuilt).
6. On 2026-10-19 notebook `tts` could not be started (console: "This Notebook Instance type 'ml.g5.12xlarge' is temporarily unavailable"), which makes item 5 urgent; see `source_docs/tts_progress_log_FULL.md`, TA-041.

---

## 1. Goal

- **What:** speech technology for Hindi, Telugu and English for the company; two workstreams, STT (paused) and TTS (started 2026-10-14). The senior's requirement carried over from STT: **separate monolingual models per language**, commercial use (so data and base-model licences must allow it), open data only, very tight budget, compute rented on AWS. Sources: `PL` Section 1; msg #17, #37, #42 (2026-10-12).
- **Why TTS now:** "my senior loved our work, but due to some other urgent constraints we have to immediately start working on tts" (msg #51, 2026-10-14T06:38Z). TD-001.
- **Target language(s):** first **Hindi first, Telugu as a stretch** (TD-006, 2026-10-14; deadline "less than a week", msg #56); then, on **2026-10-17**, the senior changed it: "deadline of tomorrow eod ... for now all we have to do is fine tune the 313M params model and teach it telugu, if it has good results with telugu, then we have met our goal" (msg #81, 2026-10-17T03:34Z; TD-008). **Current target: Telugu only, 24-layer teacher only; no Hindi, no distillation (the ~110M student is dropped).** English was planned to use the pretrained English model unchanged (TD-003).
- **Target voice(s):** UNKNOWN - not found in records. TQ-02 (how many voices, which gender, voice cloning wanted?) is still open (`PL` Section 6). Plan v1 assumed one fixed voice per language (TD-003, assumption not confirmed). What the model actually does: Pocket TTS takes a short **reference audio clip** and speaks in that voice [M, README: "voice cloning from a wav prompt", `source_docs/captured_kyutai_pocket-tts_README_2026-10-12.md`]; our teacher was trained on four speakers (see Section 8), so any of those voices can be prompted.
- **Target device/size:** UNKNOWN - not found in records (TQ-03 open). Plan v1 assumed laptop-first CPU inference with the 6-layer ~110M student (TD-003); after TD-008 the deliverable is the fine-tuned 24-layer teacher, which is slower on CPU (`PL`, `tts/telugu_teacher_run_sheet.md` risk 8).
- **Success definition:** never agreed with the senior. Proposed [P]: read-back character error rate within about 1.5x of the recogniser's error rate on real speech, mean listening score >= 3.5/5 from colleagues, at most a few clips with skipped or repeated words, not worse than Prasad Vittaldev's Telugu model by ear (`tts/telugu_teacher_run_sheet.md` Section 3). Open: TQ-06.
- **Deadline:** end of day 2026-10-18 (TD-008).

## 2. Base

- **Repo:** https://github.com/kyutai-labs/pocket-tts (clone command in msg #152, TS). Package version printed by `uv sync`: `pocket-tts 3.3.0`.
- **Commit:** on notebook `tts` (full run): `1df6b3da17cb43eff8c4c4e077f785520492adff` (output of `git rev-parse HEAD`, msg #152, 2026-10-18T06:25Z); `logs/full_run_progress.jsonl` records it as `1df6b3d-dirty` (see Section 5). On notebook `rag` (pilot): **UNKNOWN - not found in records** (`PL` TRUN-0001: "commit not recorded").
- **Starting checkpoint:** Kyutai's pretrained **English 24-layer** model: Hugging Face repo `kyutai/pocket-tts`, file `languages/english_2026-04_24l/model.safetensors` (1.30 GB, download log in msg #155). The config used is `pocket_tts/config/english_2026-04_24l.yaml` (`logs`/`configs/full_run_args_resolved.yaml`). Pinned revision seen in the **pilot** log: `492522650173a0653b7575cdc25ae09810e5d741` (msg #140). Revision used by the full run: UNKNOWN - not found in records (that log line was not captured). The weights file was accessed under the company HF account `10xwath` after the owner accepted the gate (msg #56, 2026-10-14T07:43Z); a check download of `main` on 2026-10-18 fetched snapshot `79556530b8cef3f7c8f526c5c412b65c2a4c2202` (msg #155), which is not necessarily the revision training used.
- **Parameter count:** three figures exist and are not reconciled in the records: (a) **313M** for the 24-layer teacher, from the CALM paper appendix, quoted in `source_docs/stt_research_kyutai_repos.md` line 82 [secondary, not re-read by us]; the owner uses "313M" (msg #58, #81); (b) **316M** for the teacher in Prasad Vittaldev's LinkedIn claim (same file); (c) our own training log prints **"flow_lm + objective: 316.0M trainable params"** for both runs (msg #140 pilot; msg #183 first full launch) [M]. UNKNOWN why (a) and (c) differ.
- **Licences as stated** (not independently verified by us):
  - Code: **MIT** (GitHub API capture of the Kyutai org, 2026-10-12, recorded in `source_docs/stt_research_kyutai_repos.md` line 25 [M of that capture]). The repo's LICENSE file itself was never opened: UNKNOWN.
  - Weights: **CC BY 4.0, gated**: `license: cc-by-4.0` in the HF model page front matter (`source_docs/captured_HF_model_page_kyutai_pocket-tts_2026-10-12.md` line 2) and in the browser capture of 2026-10-14 (`source_docs/evidence_2026-10-14_pages_captured_via_browser_pane.md`).
  - **Prohibited-use text** (README, section "Prohibited use"; gate text): no illegal, harmful, deceptive, fraudulent or unauthorised use, including **voice impersonation or cloning without explicit and lawful consent** (partial quote; full text in `source_docs/captured_kyutai_pocket-tts_README_2026-10-12.md` near the end).
  - Default voices: a separate page (https://huggingface.co/kyutai/tts-voices) details their licences; two voices come from non-commercial datasets [per `source_docs/carried_over_from_stt_research.md`, [M/U]].
  - Licence of **our derived weights** and whether the senior/legal accept the prohibited-use terms: not decided (TQ-09, TL-05).

## 3. Was the training code full pretraining or fine-tuning only? What did we use?

- **The repo supports both** [M, training README, `source_docs/captured_kyutai_pocket-tts_training_README_2026-10-12.md` line 155 ff.]: `scratch.yaml` (24-layer teacher from scratch), `finetune.yaml`, **`finetune_language.yaml`** (continue from the pretrained English teacher but initialise the text embedding fresh because the tokenizer differs; "on Czech, it reached the same WER as a scratch run about 2.5x sooner"), `depth_distill.yaml` (6-layer student from the teacher). The Kyutai README states the data guidance: about 100 h minimum, 200 h "speaks", 2,000 h "sounds good".
- **We used fine-tuning only, with `finetune_language.yaml`.** Evidence: `configs/full_run_args_resolved.yaml` has `start_from_pretrained: true`, `reset_text_embedding: true`, `model_config: pocket_tts/config/english_2026-04_24l.yaml`, and all `distill_*` keys empty; the training log says "starting the text embedding from scratch: ['conditioner.embed.weight']" (msg #140). No pretraining and no distillation were run (TD-008).
- **Training code:** Kyutai's `training/train.py`, unmodified as far as the records show (Section 5), launched with `uv run training/train.py <config>` (pilot, 1 GPU) and `uv run torchrun --nproc-per-node 4 training/train.py <config>` (full run).

## 4. Environment

Full detail with sources in `environment.txt`. Summary:
- **Cloud:** AWS us-east-1, SageMaker notebook instances, Amazon Linux 2023, JupyterLab 4.
- **Pilot:** notebook `rag` (another project's, shared), ml.g5.2xlarge, 1 x NVIDIA A10G, 40 GB disk (TA-031; msg #122).
- **Full run:** notebook `tts`, **4 x NVIDIA A10G** (22.06 GiB usable each), 48 logical CPUs, 191 GiB RAM, 393 GB disk. Instance type: **ml.g5.12xlarge** [M: console page of 2026-10-19, created 2026-10-17 17:45 UTC; consistent with the 4 GPUs seen during training].
- **Software:** CPython 3.10.22 (uv-managed), uv 0.13.1, **PyTorch 2.14.0 (`+cu130`)**, torchaudio 2.11.0, transformers 5.17.0, jiwer 4.0.0, sentencepiece 0.2.2; Kyutai `pocket-tts` 3.3.0. 113-package list in `environment.txt` (from `uv sync` output, msg #152).
- **Known environment problem:** the notebooks' `LD_LIBRARY_PATH` points at system CUDA 13.2 and breaks cuDNN in the uv environment; every GPU command was run as `env -u LD_LIBRARY_PATH ...` (msg #131).
- **UNKNOWN:** NVIDIA driver version, ffmpeg version, kernel version.

## 5. Code changes

**5.1 Changes to Kyutai's code: none recorded.** Evidence: (a) none of the 46 pasted notebook sessions (`TS`) contains an edit, patch, `sed -i`, `git apply`, `git checkout` or `git pull` on the repo; (b) the assistant's advice never contained such an edit (the only `sed -i` in the advice, at 2026-10-18T04:33Z, edited a copy of a config file, was superseded by `make_pilot_cfg.py` and no paste shows it executed); (c) the trainer's own start-up record `logs/full_run_progress.jsonl` shows commit `1df6b3d-dirty`.
**Caveat:** `-dirty` means the working tree differed from the commit; **which files differed is UNKNOWN - not found in records.** INFERRED from the records that the difference is our new config files `training/configs/telugu_pilot.yaml` / `telugu_full.yaml` (untracked or edited), but this was not checked, and `git status`/`git diff` output from the notebooks was never captured.

**5.2 Why no diffs could be produced:** the Kyutai repo existed only on the two notebooks (cloned there); no copy of it exists on this machine, and the notebooks were not accessible while compiling (rule 1). `diffs/README.md` explains this, and gives the exact read-only commands that would produce the diffs.

**5.3 What `diffs/` does contain:**
- `diffs/config_deltas_vs_finetune_language.md`: key-by-key differences between Kyutai's `finetune_language.yaml` (values as recorded) and our pilot and full configs.
- `diffs/new_files/`: **our own code** (no upstream counterpart), copied as is:

| File | Purpose | Status |
|---|---|---|
| `prep_syspin.py` | text cleaning, silence trimming, loudness normalisation, 24 kHz resampling, manifest + 2% hash split for SYSPIN | **Used** (pilot and full run); 4-clip local test + notebook runs |
| `prep_rasa.py` | same chain for Rasa Telugu Parquet shards (WAV bytes read from the file, piped to ffmpeg) | **Used** (full run); only its text/audio functions were tested locally, the Parquet reading ran first on the notebook |
| `run_pipeline.sh` | unattended: Rasa prep, combine, 4-GPU alignment, tokenizer, config; stops before training | **Used** (ran twice; see Section 11); never run end to end without a failure until the second run |
| `eval_telugu.py` | CPU generation + read-back CER evaluation | **Used** (smoke test + 2 checkpoints) |
| `sync_to_s3.sh` | copies run checkpoints/logs/samples to S3 every 10 min | **Used** for the full run (final files confirmed in S3) |
| `setup_instance.sh`, `download_syspin.sh` | planned set-up and download scripts | **Written but NOT used** (never ran on a notebook, TA-032; downloads were done by PC + S3 upload) |
| `from_transcript/make_pilot_cfg.py` | wrote `telugu_pilot.yaml` from `finetune_language.yaml` | **Used** (output in msg #133); text extracted from the assistant's message of 2026-10-18T05:41:38Z |
| `from_transcript/make_telugu_full_cfg_handrun.py` | wrote `telugu_full.yaml` | **Used** (msg #178, output "written. samples: 3") |

## 6. Text side

- **Tokenizer: replaced (not extended).** A new **SentencePiece unigram** tokenizer was trained with Kyutai's `training/scripts/train_tokenizer.py` on our Telugu transcripts, then converted to the Hugging Face `tokenizers` JSON format with `training/scripts/convert_tokenizer.py` (the trainer loads a JSON tokenizer; the SentencePiece `.model` alone failed: "Loading tokenizers json from data/tokenizer.model ... No such file or directory", msg #133). The model's text embedding was **re-initialised** (`reset_text_embedding: true`; "starting the text embedding from scratch: ['conditioner.embed.weight']", msg #140), so the English embedding is not used.
- **Vocabulary size:** default 4000 per the script, read from GitHub on 2026-10-18 (`PL` TA-030 [M]: "default unigram vocab 4000, normalization off"); the Kyutai config has `n_bins: 4000` (subagent report quoting `english_2026-04.yaml`, transcript 2026-10-18). **The actual number of learned pieces: 4,000** (read from the full-run `tokenizer.json` on 2026-10-19: Unigram, 4,000 entries, 0 unknown tokens on the demo sentences, about 0.29 tokens per character; `artifacts/tokenizer.json`). Pilot file sizes: `tokenizer.model` 93,758 bytes, `tokenizer.vocab` 94,962 bytes (screenshot 20.png, msg #134), `tokenizer.json` 279,227 bytes (msg #140). Full-run `tokenizer.json`: 277,583 bytes (sha256 begins ee49d18766b06db2).
- **Trained on:** pilot: pilot `train_aligned.jsonl` (2,245 clips, SYSPIN male slice, 5.0 h). Full: `data/full/train_aligned.jsonl` (68,402 clips; SYSPIN male + female + Rasa; the validation clips are excluded) (msg #177).
- **Check that the conversion is faithful:** `convert_tokenizer` prints "N texts match sentencepiece exactly": 46 texts (pilot, msg #140), 1,404 texts (full, msg #177).
- **Text normalisation** (`diffs/new_files/prep_syspin.py`, functions `clean_text` and `reject_reason`; the same code is used for Rasa): Unicode NFC; remove zero-width characters (U+200B/C/D, U+2060, U+FEFF); typographic quotes/dashes mapped to ASCII; `:` and `;` become `,`; quotes, brackets and braces removed; `- / \ | _ * # ~ @ ^ < > = + & % $` become spaces; whitespace collapsed; space before punctuation removed; repeated punctuation collapsed; **kept punctuation: `, . ? !`**; a clip is **dropped** if the text has a digit (ASCII or Telugu), any character that is not Telugu, space or `, . ? !`, or fewer than 2 words. `final_punct_dropout: 0.3` is a Kyutai training option (`configs/full_run_args_resolved.yaml`).
- **Numbers and dates:** **not converted.** Clips with digits are dropped (412 of 21,463 male SYSPIN transcripts, 1.9%; 10 more dropped for other characters; `data_samples/pilot_prep_stats.json`). **Finding from reading the raw file (not acted on):** all 412 digit-containing male transcripts have the form `{digits}{spoken Telugu form}`, so they could be recovered by keeping the spoken form (`data_samples/raw_vs_model_input_text_examples.md` part D). User input with digits is therefore **not covered** by the model or by any front-end; 10 of the 30 evaluation sentences contain digits and were skipped.
- **English words inside Telugu:** words written in Telugu script stay as in the data (STT decision D-023, recorded in `CLAUDE.md`; e.g. Rasa row: "ఫ్యాకల్టీ", "గవర్నమెంట్"); sentences containing Latin letters are dropped.
- **Raw text vs what the model receives:** four recorded pairs and rejection examples are in `data_samples/raw_vs_model_input_text_examples.md` (in the four recorded pairs the only change is a stripped leading space). The token ids the model actually receives were never printed: UNKNOWN.
- **Inference-time text handling:** Kyutai/Prasad notes say Pocket TTS locates sentence ends with its own tokenizer, which does not work well for Telugu, so text must be passed **one sentence at a time** or words may be dropped [V, Prasad's model card, `source_docs/evidence_2026-10-14_pages_captured_via_browser_pane.md`]. Our evaluation generated one sentence per call.

## 7. Audio side

- **Representation:** Kyutai's **Mimi** codec, continuous latents at 24 kHz with 80 ms frames (12.5 Hz) [README/CLI docs via the subagent fetch of 2026-10-18; `generate.md`: "each frame is 80 ms", output 24 kHz mono]. Latents are **precomputed once** by Kyutai's script and stored next to the manifest: "wrote .../train_aligned_latents.jsonl and ... .meta.json", "stitch_frames=35 (noise floor 0.0e+00)" (msg #140). Time: about 30 s for 5 h (pilot), about 3 min for 145 h on 4 GPUs (msg #183).
- **Modified or retrained?** Not by us. No change recorded. The trainer reports 316.0M trainable parameters for "flow_lm + objective" (msg #140), so INFERRED that the codec is not trained.
- **Preprocessing** (ffmpeg, `diffs/new_files/prep_syspin.py`, identical for Rasa): `silenceremove` at the start (start_silence 0.25 s, -40 dB), `areverse`, same at the end (0.3 s, -40 dB), `areverse`; `loudnorm=I=-23:LRA=11:TP=-2`; `aresample=24000`; output mono 16-bit PCM WAV; clips shorter than 1 s or longer than 30 s dropped. **No denoising.** Source audio: SYSPIN 48 kHz 24-bit mono studio recordings [M, readme]; Rasa 48 kHz mono [M, HF card], embedded as WAV bytes at about 96 KB/s (INFERRED 16-bit).
- **Known issue:** ffmpeg crashed (segmentation fault + core dump) on roughly 3-4% of clips; those clips were dropped. Cause and affected ids: UNKNOWN (`PL` TA-034).

## 8. Data

| Dataset | Source URL | Licence (as found) | Hours | Speakers | Quality | Used for |
|---|---|---|---|---|---|---|
| **SYSPIN Telugu, male** (`IISc_SYSPINProject_Telugu_Male_Spk001_HC.tar.gz`, 20.87 GiB) | https://vaani.iisc.ac.in/dataset/syspindataset (download by form) | CC-BY-4.0 per IISc [M, `source_docs/evidence_2026-10-14...md`] | readme: **48 h 20 min 26 s**, 21,463 sentences, mean 8.108 s [M, `PL` TA-022]; **kept 44.543 h** [OURS, msg #177] | 1 male speaker, age 63, 25 years' experience [M, readme] | studio, 48 kHz 24-bit mono, validated | pilot + full run |
| **SYSPIN Telugu, female** (`..._Female_Spk001_HC.tar.gz`, 24.27 GiB) | same | same | readme hours UNKNOWN (readme not read; about 56 h [E] from file size); **kept 51.406 h** [OURS]; 20,830 clips passed the text rules (denominator in msg #158-#159) | one female speaker (INFERRED from the name `Spk001`); age etc. UNKNOWN | same | full run |
| **Rasa Telugu** (`ai4bharat/Rasa`, `Telugu/` folder: 56 train + 7 test Parquet files, about 17 GB INFERRED from the file listing) | https://huggingface.co/datasets/ai4bharat/Rasa | CC-BY-4.0 (tag and card "License" section) [M] | card: **52.26 h** (female 27.28 h, 15,404 utterances; male 24.98 h, 15,006); **kept 49.399 h** [OURS] | 2 (1 female, 1 male) [M, card] | studio, 48 kHz; expressive styles incl. WIKI, emotions, commands [M, card] | full run |
| **Total kept** | | | **145.3 h** (pipeline log, msg #177) | 4 voices | | |

- **Gender/accent:** gender as above; accent/dialect: UNKNOWN - not found in records.
- **Filtering and cleaning:** text and audio rules in Sections 6-7. Counts that exist: male SYSPIN: 21,463 transcripts, 412 dropped for digits, 10 for other characters, so 21,041 clips went to audio processing (denominator in msg #158); of the pilot slice's 2,628 candidate clips 85 failed in ffmpeg (`data_samples/pilot_prep_stats.json`). Full-run reject counts per dataset (`stats.json` of each prep): UNKNOWN - not copied from the notebook (they are in `~/SageMaker/tts/data/full_*/stats.json` and, if the owner ran the optional backup, in S3 `tts_backup/data/`).
- **Splits** [OURS]: a clip goes to validation if `md5(clip id) % 50 == 0` (about 2%), otherwise to training (`prep_syspin.py`, `prep_rasa.py`). After combining: **68,402 train + 1,395 valid** (msg #177: "combined: 68402 train, 1395 valid"; all aligned). Per-dataset split sizes: UNKNOWN. Rasa's own train/test Parquet shards were merged and split by our hash. There is **no separate held-out test set from the corpora**; evaluation used 24 validation clips with unseen text and 20 sentences we wrote (Section 13).
- **Total hours actually used in training:** 145.3 h kept in total; INFERRED about **142.4 h train and 2.9 h validation** from the clip-count split of 2.0% (assumes equal clip lengths).
- **Overlap checks** (msg #203, 2026-10-18T14:49Z) [OURS]: **0 clips appear in both train and valid**; 222 of 1,395 validation clips have their **exact** transcript in training; after removing punctuation and extra spaces **979 of 1,395** validation clips have text never seen in training; the evaluation used only those 979. The same speakers appear in train and valid (clip-level, not speaker-level, hold-out).
- **Alignment** (word timings Kyutai needs): `training.scripts.align_data --model anuragshas/wav2vec2-large-xlsr-53-telugu` (Apache-2.0 tag and ~45% WER on its own test set per `PL` TA-005 [not verified against the model card]). Pilot: valid 37/37, train 2,245/2,246 (msg #131). Full: **train 68,402/68,402, valid 1,395/1,395** (msg #177).
- **Sample lines:** see `data_samples/`: header and first 10 entries of the raw SYSPIN male transcripts file (the only complete raw metadata that survives), Rasa schema and two rows, pilot stats and manifest line, the 24 validation texts used in evaluation, the 3 trainer sample sentences. **The first 10 lines of our train/valid manifests for each dataset: UNKNOWN - not found in records.**
- **Voice rights / consent:** UNKNOWN - open (TL-05, TQ-08). The datasets are CC-BY-4.0; whether the speakers consented to being cloned is not known.

## 9. Training runs (every run, including failed ones)

Times UTC. Losses are Kyutai's total training objective (flow-matching based; can be negative; **not** an audio-quality measure). "GPU hours" are INFERRED as wall-clock x GPUs (no billing record exists).

| # | Date, time | Run / name | Config file | Start checkpoint | Steps | Batch (per GPU x accum x GPUs = effective) | LR and schedule | GPU hours | Final train / valid loss | Checkpoint path | Outcome and why it stopped |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | 2026-10-18 05:41:57-05:41:58 | pilot start attempt 1 (notebook `rag`) | `training/configs/telugu_pilot.yaml` (tokenizer path still `data/tokenizer.model`) | english_2026-04_24l | 0 | 16 x 4 x 1 = 64 | 2e-4 constant, warm-up 50 | ~0 | none | none | **Failed at start**: tokenizer file not found; my config script looked for a plain `tokenizer_path` key, but the key is `flow_lm.lookup_table.tokenizer_path` under `model_overrides` (msg #133). Fixed by a `python -c` edit and by converting the tokenizer to JSON (msg #140). |
| B | 2026-10-18 05:43:17-05:50:25 | **TRUN-0001 pilot** (`rag`) | `telugu_pilot.yaml` (resolved copy: `configs/pilot_resolved_config_from_log.yaml`) | english_2026-04_24l, revision 4925226... | **200** | 16 x 4 x 1 = 64 | 2e-4 constant, warm-up 50 | ~0.12 (7 min 8 s wall) | train step 200: 0.3417; valid @200: 0.3776 (valid @100: 0.3864) | `~/SageMaker/tts/runs/telugu_pilot/checkpoint_00000200.pt`, `model.safetensors` (on `rag`); S3 backup: UNKNOWN | **Completed** (reached max_steps 200 by design: measure speed ~1.0 steps/s, peak GPU memory 15.9 GiB). Data: 5.026 h SYSPIN male slice. Sample generated afterwards (Section 14, file 01): 1.72 s for a 9.08 s clip. |
| C | 2026-10-18 08:44:20 launch; 08:47:41 run_start; crash 08:47:48 | **full run, first launch** (`tts`) | `telugu_full.yaml` | english_2026-04_24l | 0 | 16 x 1 x 4 = 64 | 2e-4 constant, warm-up 1000 | ~0.2 (precompute) | none | none | **Failed in DDP set-up**: "NCCL error ... Cuda failure 2 'out of memory'" on rank 3 (msg #183). The latent precompute (about 3 min) had left the GPUs almost full (`free: 16 MB`). The log file was overwritten by the relaunch; only the excerpts in `logs/terminal_sessions_as_pasted.md` survive. Relaunched with the same command; latents were reused. |
| D | 2026-10-18 08:55:25 run_start; first step 08:56:34; step 15000 at 11:27:16; end-of-run checkpoint 11:28:23 | **TRUN-0002 full run** (`tts`, 4 x A10G) | `telugu_full.yaml` (resolved copy: `configs/full_run_args_resolved.yaml`) | english_2026-04_24l (revision UNKNOWN) | **15,000** | 16 x 1 x 4 = 64 | 2e-4 constant, 1,000-step warm-up, EMA 0.999, weight decay 0.1 | ~10.2 (2 h 33 min wall x 4) | train step 15000 (single batch): 0.0324; **valid @15000: -0.2061** (best valid: -0.2138 @10000; series in Section 13) | S3 `s3://aarav-10x/checkpoints/telugu_full/` and notebook `~/SageMaker/tts/runs/telugu_full/` (`checkpoint_00015000.pt` 2.4 GiB, `model.safetensors` 1.3 GiB, `optim_00015000.pt` 2.4 GiB) | **Completed**: reached `max_steps` 15000 (the owner's senior had been asked to watch it; the notebook was stopped by the senior afterwards). Speed: steady 1.70 steps/s (mean over steps 300+), GPU utilisation 81-100%, 17.4-18.8 GiB used per GPU (msg #189). No non-finite gradient; max gradient norm 4.32 (clipped at 1.0). |

**Evaluation runs (not training; CPU, same notebook):**

| Date, time (UTC) | What | Result |
|---|---|---|
| 14:52-15:05 | smoke test, 2 validation clips, checkpoint 15000 | worked end to end; took ~14 min (one-time model loading); CER generated 0.144 vs real 0.112 (2 clips) |
| 15:08 | timing of one generation call | 14 s total; "Generated: 2800 ms of audio in 3273 ms so 0.86x" on CPU (msg #208) |
| ~15:09-15:17 | full evaluation, **checkpoint 15000**: 24 validation clips (unseen text) + 20 sentences x 2 voices | see Section 13 |
| ~15:17-15:26 | full evaluation, **checkpoint 10000** | see Section 13 |

## 10. Exact commands

All commands were run on SageMaker notebook terminals by the owner. "As pasted" = the command text appears in the owner's pasted terminal output (`TS`, transcript message in brackets). "As advised" = the command text exists only in the assistant's message and the owner's paste shows its output but not the command line (the paste began mid-output or was a screenshot). The notebooks' own shell histories were never copied: UNKNOWN.

**Pilot (`rag`, 2026-10-18)**
```bash
# stream the first ~2.8 GB of the male archive straight from S3 into extracted files   [as pasted, msg #123, 04:55Z]
aws s3 cp s3://aarav-10x/raw/syspin/IISc_SYSPINProject_Telugu_Male_Spk001_HC.tar.gz - | head -c 2800000000 | tar -xz -C ~/SageMaker/tts/data/raw
# prep (script prep_syspin.py; the command line is visible in msgs #123-#131)
python3 prep_syspin.py --root ~/SageMaker/tts/data/raw/IISc_SYSPIN_Data/IISc_SYSPINProject_Telugu_Male_Spk001_HC --out ~/SageMaker/tts/data/pilot --limit-hours 10 --workers 8
# align (valid, then train)   [as pasted, msg #131, 05:36Z]
env -u LD_LIBRARY_PATH uv run python -m training.scripts.align_data ~/SageMaker/tts/data/pilot/valid.jsonl ~/SageMaker/tts/data/pilot/valid_aligned.jsonl --model anuragshas/wav2vec2-large-xlsr-53-telugu --device cuda
env -u LD_LIBRARY_PATH uv run python -m training.scripts.align_data ~/SageMaker/tts/data/pilot/train.jsonl ~/SageMaker/tts/data/pilot/train_aligned.jsonl --model anuragshas/wav2vec2-large-xlsr-53-telugu --device cuda
# tokenizer + pilot config + first training attempt   [as advised, 05:41:38Z; output pasted in msg #133]
env -u LD_LIBRARY_PATH uv run python -m training.scripts.train_tokenizer ~/SageMaker/tts/data/pilot/tokenizer ~/SageMaker/tts/data/pilot/train_aligned.jsonl
env -u LD_LIBRARY_PATH uv run python ~/SageMaker/tts/scripts/make_pilot_cfg.py          # see diffs/new_files/from_transcript/
env -u LD_LIBRARY_PATH uv run training/train.py training/configs/telugu_pilot.yaml      # failed: tokenizer path
# convert tokenizer, patch tokenizer path, train (pilot)   [as pasted, msg #140, 05:51Z]
env -u LD_LIBRARY_PATH uv run python -m training.scripts.convert_tokenizer ~/SageMaker/tts/data/pilot/tokenizer.model --texts ~/SageMaker/tts/data/pilot/valid_aligned.jsonl
#   (python -c that sets c['model_overrides']['flow_lm.lookup_table.tokenizer_path'] to .../pilot/tokenizer.json in telugu_pilot.yaml; full text in TS)
env -u LD_LIBRARY_PATH uv run training/train.py training/configs/telugu_pilot.yaml 2>&1 | tee -a ~/SageMaker/tts/logs/pilot_train.log
# generate one test clip from the pilot checkpoint   [as pasted, msg #143, 05:57Z]
env -u LD_LIBRARY_PATH uv run pocket-tts generate --config $R/pilot_gen.yaml --checkpoint $R/checkpoint_00000200.pt --voice "$(sed -n 1p $R/gen_args.txt)" --text "$(sed -n 2p $R/gen_args.txt)" --output-path $R/pilot_test.wav --device cuda
```
**Full run (`tts`, 2026-10-18)**
```bash
# check GPUs, S3 access   [as advised 06:01Z; output in screenshot 22.png]
mkdir -p ~/SageMaker/tts/{scripts,logs,bin,data/raw,runs} && nvidia-smi -L && df -h ~/SageMaker | tail -1 && aws s3 ls s3://aarav-10x/raw/syspin/ --human-readable && echo ok | aws s3 cp - s3://aarav-10x/tts_write_test.txt
# extract both SYSPIN archives from S3 in the background   [as advised 06:19Z; screenshot 23.png and msg #149]
for s in Male Female; do nohup sh -c "aws s3 cp s3://aarav-10x/raw/syspin/IISc_SYSPINProject_Telugu_${s}_Spk001_HC.tar.gz - | tar -xz -C $HOME/SageMaker/tts/data/raw" > ~/SageMaker/tts/logs/extract_$s.log 2>&1 & done
# environment, uv, ffmpeg, repo   [as pasted, msgs #150/#152, 06:23-06:25Z]
cd ~/SageMaker/tts && cat > env.sh <<'EOF'   # (4 export lines, see environment.txt)
source ./env.sh && curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR="$HOME/SageMaker/tts/bin" UV_NO_MODIFY_PATH=1 sh
python3 -m venv venv_tools && venv_tools/bin/pip install -q imageio-ffmpeg && ln -sf "$(venv_tools/bin/python -c 'import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())')" bin/ffmpeg
git clone https://github.com/kyutai-labs/pocket-tts.git && cd pocket-tts && uv sync && git rev-parse HEAD
# Hugging Face login (token pasted at the prompt by the owner; value not recorded)   [as pasted, msg #153]
uv run hf auth login && uv run hf auth whoami          # user: 10xwath
# prepare both SYSPIN speakers (22 workers each, in parallel)   [as pasted, msgs #156-#157, 06:29-06:31Z]
for s in Male Female; do nohup python3 prep_syspin.py --root $R/IISc_SYSPINProject_Telugu_${s}_Spk001_HC --out $HOME/SageMaker/tts/data/full_$s --workers 22 > ~/SageMaker/tts/logs/prep_$s.log 2>&1 & done
# download Rasa Telugu   [as pasted, msg #172, 07:22Z]
uv run hf download ai4bharat/Rasa --repo-type dataset --include "Telugu/*" --local-dir ~/SageMaker/tts/data/rasa
# unattended pipeline: Rasa prep, combine, align on 4 GPUs, tokenizer, config   [as pasted, msgs #173 (07:27Z, started twice by mistake) and #175 (08:06Z, FRESH_RASA=1 rerun)]
FRESH_RASA=1 nohup bash ~/SageMaker/tts/scripts/run_pipeline.sh > ~/SageMaker/tts/logs/pipeline.out 2>&1 &
# the config step of the pipeline failed (sample_freq/sample_sentences); config written by hand   [as pasted, msg #178, 08:43Z; script in diffs/new_files/from_transcript/]
# launch training on 4 GPUs   [as pasted, msg #179 (first, failed) and #184 (relaunch), 08:47Z / 08:57Z]
nohup env -u LD_LIBRARY_PATH uv run torchrun --nproc-per-node 4 training/train.py training/configs/telugu_full.yaml > ~/SageMaker/tts/logs/full_train.log 2>&1 &
# checkpoint backup loop to S3   [as pasted, msg #180, 08:48Z]
BUCKET=aarav-10x RUN_DIR=$HOME/SageMaker/tts/runs/telugu_full RUN_NAME=telugu_full nohup bash ~/SageMaker/tts/scripts/sync_to_s3.sh > ~/SageMaker/tts/logs/sync.log 2>&1 &
```
**Evaluation (`tts` after restart, 2026-10-18 afternoon UTC)**
```bash
# data overlap check   [as pasted, msg #203, 14:49Z]  (python -c; full text in TS)
# smoke test   [as pasted, msg #207, 15:07Z]
uv run python ~/SageMaker/tts/scripts/eval_telugu.py --checkpoint ~/SageMaker/tts/runs/telugu_full/checkpoint_00015000.pt --n-valid 2 --out ~/SageMaker/tts/runs/telugu_full/eval_smoke
# full evaluation of both checkpoints   [as advised 15:08Z; log lines pasted in msgs #210-#219]
nohup sh -c 'for s in 15000 10000; do uv run python $HOME/SageMaker/tts/scripts/eval_telugu.py --checkpoint $HOME/SageMaker/tts/runs/telugu_full/checkpoint_000$s.pt --sentences $HOME/SageMaker/tts/eval/telugu_test_sentences.txt --out $HOME/SageMaker/tts/runs/telugu_full/eval_$s; done' > $HOME/SageMaker/tts/logs/eval_run.log 2>&1 &
```
**Inference command used throughout** (documented form, `pocket-tts generate`; not `serve`):
```bash
uv run pocket-tts generate --config <gen.yaml> --checkpoint <checkpoint_N.pt> --voice <reference.wav> --text "<one sentence>" --output-path <out.wav> --device cpu
```
`gen.yaml` = Kyutai's `english_2026-04_24l.yaml` with `flow_lm.lookup_table.tokenizer_path` set to our `tokenizer.json` (`configs/eval_gen.yaml`).

## 11. Problems and fixes (date order, UTC unless marked)

| Date, time | Problem | Cause (as recorded) | Fix | Source |
|---|---|---|---|---|
| 2026-10-14 | Assistant claimed the run sheet and log were updated; they were not | assistant error | edits made 2026-10-15, correction logged | PL TA-009 |
| 2026-10-14 21:00 | Senior wanted data in S3, owner had proposed not using S3; the senior's cost figure for EBS was wrong | disagreement | S3-first design with checkpoint sync (TD-007) | PL TA-013 |
| 2026-10-17 03:37-03:50 | CloudShell "Unable to create the environment" | IAM user lacks CloudShell permission [U] | owner chose manual download + upload | PL TA-018, TA-020; msg #83, #90 |
| 2026-10-17 | Notebook `tts` was created as ml.g5.48xlarge (about $16/h or more) instead of ml.g5.2xlarge | created by the senior | owner stopped it (cost); owner has no permission to edit its type | PL TA-019; msg #90, #91 |
| 2026-10-17 | Confusion about hours (139 h vs 45 h) and an SYSPIN hours estimate of ~40 h that was really 48.3 h | estimate scaled from the wrong GB-per-hour | corrected from the archive's readme | msg #87; PL TA-022 |
| 2026-10-17 ~07:00 | Chrome restarted the female archive download from zero near the end | unknown [U] | `aria2c -x 8 -s 8 -c` with resume; the assistant first misreported its speed (100 MB/s from file size; real 10-15 MiB/s) | PL TA-026, TA-027; msg #101-#103 |
| 2026-10-18 04:25 | Pilot notebook `rag` has a 40 GB disk and is shared with another project | different notebook than planned | stream only the first 2.8 GB; install under `~/SageMaker/tts`; never touch other files | PL TA-031, TA-032 |
| 2026-10-18 04:37 | `uv` and `ffmpeg` missing; setup script had never run | files uploaded to the wrong folder | isolated installs (uv under `~/SageMaker/tts/bin`, ffmpeg via `imageio-ffmpeg`), no conda/.bashrc changes | PL TA-032; msg #122 |
| 2026-10-18 05:19 | JupyterLab terminal stopped accepting input | unknown | new terminal; deleted the extracted raw folder to free disk | msg #126, #129 |
| 2026-10-18 ~05:28 | Aligner failed: `CUDNN_STATUS_SUBLIBRARY_LOADING_FAILED` | notebook `LD_LIBRARY_PATH` points at CUDA 13.2, conflicts with cuDNN in the venv | prefix every GPU command with `env -u LD_LIBRARY_PATH` | msg #131 |
| 2026-10-18 05:41 | First pilot training start crashed: tokenizer not found | config key is dotted under `model_overrides`; tokenizer must be JSON | python edit of the config + `convert_tokenizer` | msg #133, #140 |
| 2026-10-18 06:17 | Two copies of the extraction ran at once | command run twice | killed all, wiped the half-extracted folder, restarted once | msg #148-#149 |
| 2026-10-18 06:23 | `source env.sh` failed: file not found | terminal shell in POSIX mode | `source ./env.sh` | msg #150 |
| 2026-10-18 06:36-06:43 | SYSPIN prep slow; `systemd-coredump` at 94% CPU | **ffmpeg segmentation faults** (about 3-4% of clips) and the core dumps stalled the workers | `ulimit -c 1` did not stop the dumps (tested); waited it out; crashed clips are dropped; probably also the pilot's 85 ffmpeg rejects (INFERRED) | msg #160, #161; PL TA-034 |
| 2026-10-18 07:27 | `run_pipeline.sh` started twice 5 s apart | command run twice | two Rasa preps wrote the same files; alignment parts 1 and 3 ran out of GPU memory (two aligners per GPU, `Process ... has 13.96 GiB`); script stopped at its 95% check (33,382 of 68,402). Added a lock, skip-if-done, `FRESH_RASA=1`; reran at 08:06 | msg #173, #177; PL TA-035 |
| 2026-10-18 08:27 | Config step failed: `AssertionError: some config keys were not found` | `sample_freq` and `sample_sentences` are not keys in `finetune_language.yaml` (built-in defaults) | set at top level; config written by hand | msg #177, #178 |
| 2026-10-18 08:47 | First 4-GPU launch crashed: NCCL `Cuda failure 2 'out of memory'` in DDP init | latent precompute left every GPU nearly full | relaunched the same command (latents reused) | msg #183, #184 |
| 2026-10-18 08:59 | `nvidia-smi ... -c 5` rejected | assistant error: `-c` is "compute mode" | loop with `sleep` | msg #185, #189 |
| 2026-10-18 14:09 | S3 console: no Download option | folders and multi-selection cannot be downloaded; single files can | download single files | msg #192, #193 |
| 2026-10-18 14:49 | 16% of validation texts also occur in training (exact), 30% after normalisation | the corpora repeat sentences across speakers/datasets [INFERRED] | evaluation restricted to the 979 unseen-text validation clips | msg #203; PL TA-039 |
| 2026-10-18 15:05 | First evaluation call took ~14 min for 2 clips | one-time model loading (a later single call took 14 s) | none needed | msg #205-#208 |
| 2026-10-18 evening | Assistant numeric slips in chat: expected 2 `tar` processes (got 6, `pgrep -f` matches the shell wrappers); predicted ~1,170 unseen-text clips (real 979); said 19 test sentences (real 20) | assistant errors | corrected in chat | transcript 2026-10-18 |

## 12. Decisions (with the stated reason)

| Date | Decision | Reason as stated | Source |
|---|---|---|---|
| 2026-10-14 | Start TTS now, STT paused | senior's urgent constraint | TD-001; msg #51 |
| 2026-10-14 | Two folders and two logs (`stt/`, `tts/`) | owner's instruction | TD-002; msg #51 |
| 2026-10-14 | Use Kyutai Pocket TTS as the base, with the teacher-then-student recipe | released training code, community Telugu precedent, small, CPU-friendly | TD-003; TA-002 |
| 2026-10-14 | Use the company HF account `10xwath` | owner's statement | TD-004; msg #53 |
| 2026-10-14 | Data policy: SYSPIN from IISc's official download, Rasa; not the third-party SYSPIN re-upload; IndicTTS and IndicVoices-R held back | licence clarity (restrictive reading) | TD-005; TA-004 |
| 2026-10-14 | Hindi first, Telugu stretch (later superseded) | better aligners and judge for Hindi | TD-006 |
| 2026-10-15 | S3-first design with checkpoint sync | senior's durability and audit concerns | TD-007; TA-013 |
| 2026-10-17 | **Scope change: Telugu only, 24-layer teacher only, deadline end of day 2026-10-18** | senior's instruction | TD-008; msg #81 |
| 2026-10-17 | Pilot on ml.g5.2xlarge, training on ml.g5.12xlarge (TD-009 in TA-029) | cost vs time; the owner chose the hybrid | PL TA-029; msg #112 |
| 2026-10-17 | Download archives with aria2 and upload to S3 by hand | CloudShell blocked, notebook too expensive to leave running | PL TA-020, TA-026 |
| 2026-10-18 | Pilot of 5 h of audio and 200 steps before the real run | very short on time; measure speed and test the pipeline | msg #115; TA-030 |
| 2026-10-18 | Aligner: `anuragshas/wav2vec2-large-xlsr-53-telugu` | candidate named in the plan; worked on our transcripts (0 skipped on valid, 1 on train) | TA-030; msg #131 |
| 2026-10-18 | Add Rasa Telugu to the training data (SYSPIN-only was about 96 h) | reach about 145 h, above Kyutai's 100 h minimum | owner's question msg #170; PL TA-035 |
| 2026-10-18 | 4 GPUs, per-GPU batch 16, no accumulation (effective 64), 15,000 steps, validation/checkpoint/sample every 2,500 | same effective batch as Kyutai's recipe; Kyutai notes "WER plateaus by ~15k"; pilot memory 15.9 GiB fits | PL TA-036; msg #186 |
| 2026-10-18 | Keep 15k steps; decide on 30k only if samples still improve (not needed: validation loss flat from ~10k) | cost and evidence | msg #186; PL TA-037 |
| 2026-10-18 | Evaluate on CPU, restricted to unseen-text clips; headline = ship voices (SYSPIN male and female clips) on new sentences | avoids GPU contention; avoids optimistic scores; product input is text, voice is chosen by us | PL TA-039; msg #200 |
| 2026-10-18 | 15k is the candidate checkpoint; 10k is a comparison (indistinguishable) | final checkpoint; exported weights are a running average [U] | PL TA-039 |

## 13. Current state

- **Best checkpoint considered:** `checkpoint_00015000.pt` / `model.safetensors` of run TRUN-0002 (step 15,000). 10,000 is statistically indistinguishable (the decision rule and the evidence are in `PL` TA-039). Sizes: checkpoint 2.4 GiB, exported weights 1.3 GiB, optimizer state 2.4 GiB (S3 listing, screenshot 25.png, msg #202; all timestamped 2026-10-18 11:29 UTC). Locations: S3 `s3://aarav-10x/checkpoints/telugu_full/` and notebook `tts` disk. The notebook was **stopped** by the senior; whether the final stop was confirmed after the evaluation: UNKNOWN at the time of writing.
- **To run the model you need, besides the weights:** `tokenizer.json` (**not in S3 and not in this package, see the documentation problems above**) and a reference voice clip. With Kyutai's code the weights file `model.safetensors` can be loaded on its own by pointing `weights_path` in the config at it (read from the installed `pocket-tts` 3.3.0 source on 2026-10-19; not yet run with the real file).
- **How inference is run:** Section 10, last block. Reference clip required (`--voice`); one sentence per call; text must be cleaned the same way as training text; **numbers are not supported** (digits were never trained).
- **Inference speed measured so far** [OURS, two single observations, not benchmarks]: pilot checkpoint on 1 x A10G GPU: 1,520 ms of audio generated in 705 ms (2.16x real time; msg #143); checkpoint 15000 on the notebook CPU: 2,800 ms in 3,273 ms (0.86x real time; msg #208). No quantisation, no student model. **2026-10-19, on a laptop** (Intel Core i5-1340P, 12 cores, 15.6 GB RAM, no GPU, Windows, PyTorch 2.14.1 CPU, 8 threads, fp32): model load 18-30 s; 0.63-1.05 x real time over seven requests (e.g. 5.9 s of audio in 7.4 s; 11.9 s in 11.3 s) using the exported `model.safetensors` and local `tokenizer.json` through Kyutai's Python interface (no Hugging Face access); source `tts/progress.md` TA-044. No quantisation, no student model.
- **Training loss/validation series** (`logs/full_run_valid_loss.csv`): valid loss at 2,500 / 5,000 / 7,500 / 10,000 / 12,500 / 15,000 = +0.092 / -0.108 / -0.194 / **-0.214** / -0.183 / -0.206. Rapid improvement to about 7,500 steps, flat afterwards (differences of about 0.03 are within noise).
- **Evaluation (CPU, 24 held-out validation clips with unseen text + 40 sentence clips; read-back with `anuragshas/wav2vec2-large-xlsr-53-telugu`; CER is relative because the recogniser is weak)** [OURS; `logs/eval/results_*.json/.csv`]:

| | 15,000 steps | 10,000 steps |
|---|---|---|
| CER on real recordings of the validation clips (baseline) | 0.138 | 0.138 |
| CER on our generated audio, same texts | 0.153 | 0.153 |
| Paired gap generated minus real, bootstrap 95% interval | +0.015 [-0.005, +0.035] | +0.015 [0.000, +0.031] |
| Length ratio generated/real (min / median / max) | 0.88 / 1.02 / 1.52 | 0.89 / 1.04 / 1.52 |
| Sentence CER, 40 clips, 95% interval | 0.117 [0.097, 0.138] | 0.102 [0.082, 0.123] |
| Sentence CER male voice / female voice | 0.128 / 0.107 | 0.113 / 0.092 |
| Worst clip CER (any single clip) | 0.30 | 0.24 |

  15k minus 10k over all 64 files: +0.009 [-0.001, +0.020] (no reliable difference). The 1.52 length ratio is a 3-word clip (real 1.13 s, generated 1.72 s), a fixed tail effect, not a failure. No clip under half its real length (the pilot's 200-step clip: ratio 0.19).
- **Human assessment:** the owner's senior (a Telugu speaker) listened to the nine trainer samples and said the results are "very good" (verbal, unquantified, msg #209, 2026-10-18T15:08Z). Which files, scores and any issues: UNKNOWN - not found in records. One informal listener is not a listening test.

## 14. Existing audio outputs

15 clips are copied to `audio_samples/`, each with a `.txt` holding the exact input text; the table is in `audio_samples/README.md`. Full inventory on disk:

| Where | What | Exact input text |
|---|---|---|
| `Downloads/pilot_test.wav` (copied as sample 01) | pilot checkpoint, 1.72 s | transcript of validation clip `IISc_SYSPINProject_te_m_AGRI_02122` (text printed in msg #143) |
| `tts/samples/step0000{2500,10000,15000}_{0,1,2}.wav` (9 files; copied as samples 02-10) | trainer samples from TRUN-0002 | `configs/full_run_args_resolved.yaml` `sample_sentences[0..2]`; also `data_samples/trainer_sample_sentences_exact.txt` |
| `10X_STT/telugu_eval.zip` and the unzipped folder `10X_STT/telugu_eval/` (128 clips: `valid_00..23.wav` and `sent_00..19_v0/v1.wav`, for 10,000 and 15,000) (5 copied as samples 11-15) | evaluation output | sentences: the 20 digit-free lines of `tts/eval/telugu_test_sentences.txt` in file order (index mapping verified: 0 mismatches); validation clips: the validation transcript with punctuation removed is in `results_*.json` (the original string with punctuation was not saved: **exact text UNKNOWN**; normalised text in `data_samples/eval_valid_clips_24.tsv`) |
| notebook `tts`: `~/SageMaker/tts/runs/telugu_full/samples/` (6 sets, 18 clips) | all trainer samples | the same 3 sentences; only 2,500/10,000/15,000 were downloaded |
| notebook `rag` `~/SageMaker/tts/runs/telugu_pilot/pilot_test.wav` | same as Downloads copy | |

## 15. Known limitations and open questions (as recorded)

From `PL` Sections 6-7 and entries TA-037 to TA-039, not new opinions:
- Target devices, number of voices, voice cloning wanted or not, quality bar and who approves licences: **open** (TQ-02, TQ-03, TQ-06, TQ-10).
- **Voice rights and consent** for the shipped voice(s) (TL-05, TR-04); the Kyutai prohibited-use text (no cloning without consent) has not been confirmed acceptable by the senior/legal (TQ-09).
- **Digits and numbers**, English words in Latin script, and long inputs are untested or unsupported; the model must be fed one sentence at a time.
- The evaluation recogniser is weak; CER is only a relative number; samples are small (24 and 40 clips); one informal listener; no naturalness or speaker-similarity measure; no comparison with Prasad's Telugu model.
- Speakers in train and validation are the same (held-out clips, not held-out speakers).
- The 30 test sentences were written by the assistant and **not proofread by a Telugu speaker**; their CER is provisional.
- Rasa is expressive speech (several styles) mixed with SYSPIN's neutral reading; the effect on style is unknown [U]. The Rasa style mix in the training data is UNKNOWN.
- Pass marks have not been agreed with the senior (proposed only).
- Speed on target devices (laptop/phone CPU) of the 24-layer teacher: not measured beyond the single CPU observation in Section 13.
- Prasad Vittaldev's Telugu model: provenance of its 124 h and its quality are unmeasured (TU-01).

## 16. Timeline (day by day)

**UTC dates from the transcript; IST in brackets where it differs.**

- **2026-10-08 (STT context, before TTS):** owner asks for a revised STT pipeline (msg #0, 07:52Z); pipeline and cost discussions; `stt/pipeline.md`, `stt/progress.md` and `CLAUDE.md` created (msg #8-#9). Source: `stt/progress.md`.
- **2026-10-12 (STT context):** browser-pane audits of datasets and models; the owner confirms the model must be offline, one monolingual model per language; budget "very tight", "only 3 weeks" (msg #37); the senior chooses "v1" (English words also in native script) (msg #49, 23:11Z). The research notes on Kyutai and Prasad's TTS that later seeded the TTS work were captured here (`source_docs/stt_research_kyutai_repos.md`; READMEs saved 2026-10-12 21:47-21:50Z).
- **2026-10-14 [IST 14-15 Oct]:** **TTS starts** (msg #51, 06:38Z): STT/TTS folders split, TTS plan written (TA-001..TA-003, `tts/pipeline.md`). Owner accepts the Kyutai gate (07:43Z, msg #56), then the Rasa gate and submits the SYSPIN form (11:33Z, msg #60-#62); Hindi first (TD-006); run sheet for Hindi written (TA-006); first status message to the senior (msg #63); "green flag" for the TTS pipeline (19:43Z, msg #66); compute sizing; S3 versus notebook disk discussed (20:45-21:10Z, msg #67-#79); the owner asks the senior for a notebook (TA-012, TA-013).
- **2026-10-15 and 16:** no work recorded in the transcript. The senior creates the SageMaker notebook `tts` (created 2026-10-16 20:24 UTC, per PL TA-019).
- **2026-10-17 [IST]:** 03:30Z: the senior sets the **deadline end of day 2026-10-18 and the Telugu-only scope** (msg #81, TD-008); S3 bucket `aarav-10x` created; CloudShell blocked; notebook `tts` found to be ml.g5.48xlarge and stopped; manual download and upload of the two Telugu SYSPIN archives (msg #90-#109; Chrome restart, aria2); first archive inspected (48.3 h, layout and readme read, TA-022); GPU and time estimates (TA-023..TA-025); requirements for a new notebook sent (15:28Z, msg #110-#113); Telugu run sheet and 30 test sentences written (TA-021).
- **2026-10-18 [IST]:**
  - 04:21Z: archives in S3; pilot on notebook `rag` (msg #114-#118); streaming extraction (04:55Z); prep; terminal glitch (05:19Z); alignment (cuDNN workaround, 05:36Z); pilot tokenizer; first start fails (05:41Z); **pilot trains 200 steps** (05:43-05:50Z); pilot sample 1.72 s (05:57Z).
  - 06:01Z: notebook `tts` (4 x A10G) checked; archives re-extracted from S3 (06:19Z, started twice, fixed); environment set up (06:23-06:28Z); SYSPIN prep started (06:31Z; ffmpeg crashes found 06:36Z).
  - 07:21Z: Rasa download started; SYSPIN prep finished 07:32Z; `run_pipeline.sh` started twice (07:27Z); Rasa prep + combine (07:41Z); alignment out-of-memory failure (07:50Z).
  - 08:06Z: pipeline rerun once: Rasa prep 08:18Z, alignment of 68,402 train / 1,395 valid clips 08:26Z, tokenizer 08:27Z; config step fails then fixed by hand (08:27-08:43Z); first 4-GPU launch fails (08:47Z); **relaunch and full run: 08:55:25Z to 11:28Z, 15,000 steps** (owner away; the senior watched it).
  - 14:00Z: owner returns; reads S3 (highest checkpoint 15000, last modified 16:59 IST); downloads `progress.jsonl`, `args.yaml`, nine sample WAVs (14:09-14:17Z); loss curve read (TA-037); sample measurements (TA-038).
  - 14:49-15:26Z: overlap check; evaluation script smoke test, timing, full evaluation of 15k and 10k (TA-039); senior's verbal verdict "very good" (15:08Z).
  - 15:29Z: evaluation zip checked and analysed; 16:35Z: the senior's request for this handover folder.

---

## Appendix A. Gaps that read-only commands on the notebooks could close (NOT run)

These would turn several UNKNOWNs into facts. They only read and print; none changes anything. Run on notebook `tts` (and `rag` for the pilot):
```bash
cd ~/SageMaker/tts/pocket-tts && git rev-parse HEAD && git status --short && git diff > ~/SageMaker/tts/pocket_tts_repo.diff     # Section 5: what "-dirty" was; diff of tracked files
git -C ~/SageMaker/tts/pocket-tts log -1 --format=%H%n%cd       # on rag too (pilot commit)
head -n 10 ~/SageMaker/tts/data/full/train_aligned.jsonl ~/SageMaker/tts/data/full/valid_aligned.jsonl ~/SageMaker/tts/data/full_Male/train.jsonl ~/SageMaker/tts/data/full_Female/train.jsonl ~/SageMaker/tts/data/full_Rasa/train.jsonl   # Section 8 sample lines
cat ~/SageMaker/tts/data/full_*/stats.json                      # reject counts and Rasa hours by style
nvidia-smi | head -4; ffmpeg -version | head -1; uname -r; cat /etc/os-release | head -2   # Section 4
cd ~/SageMaker/tts/pocket-tts && uv pip freeze                   # a real pip freeze
cat ~/.bash_history | tail -n 400                                # shell history (check for secrets before copying)
wc -l ~/SageMaker/tts/data/full/tokenizer.vocab; ls -l ~/SageMaker/tts/data/full/tokenizer.*   # real vocabulary size
aws s3 cp ~/SageMaker/tts/data/full/tokenizer.json s3://aarav-10x/checkpoints/telugu_full/tokenizer.json && aws s3 cp ~/SageMaker/tts/data/full/tokenizer.model s3://aarav-10x/checkpoints/telugu_full/tokenizer.model   # MOST IMPORTANT: back up the tokenizer (this one WRITES to S3; the others only read)
cp ~/SageMaker/tts/pocket-tts/training/configs/telugu_pilot.yaml ~/SageMaker/tts/pocket-tts/training/configs/telugu_full.yaml ~/SageMaker/tts/   # the config files themselves
```
