# INDEX of tts_handover/

Start with `PROCESS_REPORT.md`. Every file is listed once, with its size in bytes.

| File | Bytes | What it is |
|---|---:|---|
| `INDEX.md` | (this file) | This file: every file in the folder with a one-line description |
| `PROCESS_REPORT.md` | 54159 | The main document: 16 sections (goal, base, environment, code changes, text, audio, data, every training run, commands, problems, decisions, current state, audio outputs, limitations, timeline) with a completeness table up front and read-only commands to close the gaps |
| `artifacts/README.md` | 1167 | Provenance and inspection of the tokenizer file |
| `artifacts/tokenizer.model` | 92476 | SentencePiece source of the tokenizer (matches tokenizer.json: 4,000 pieces, identical token ids) |
| `artifacts/tokenizer.json` | 277583 | The full run's Telugu tokenizer (Unigram, 4,000 entries); needed to use the model; copied off the notebook on 2026-10-19 |
| `audio_samples/01_pilot_step200_valid_AGRI_02122.txt` | 312 | The exact input text of the clip with the same name |
| `audio_samples/01_pilot_step200_valid_AGRI_02122.wav` | 82604 | An existing generated clip (24 kHz mono 16-bit) |
| `audio_samples/02_trainer_sample_step2500_sentence0.txt` | 242 | The exact input text of the clip with the same name |
| `audio_samples/02_trainer_sample_step2500_sentence0.wav` | 307244 | An existing generated clip (24 kHz mono 16-bit) |
| `audio_samples/03_trainer_sample_step2500_sentence1.txt` | 241 | The exact input text of the clip with the same name |
| `audio_samples/03_trainer_sample_step2500_sentence1.wav` | 307244 | An existing generated clip (24 kHz mono 16-bit) |
| `audio_samples/04_trainer_sample_step2500_sentence2.txt` | 224 | The exact input text of the clip with the same name |
| `audio_samples/04_trainer_sample_step2500_sentence2.wav` | 249644 | An existing generated clip (24 kHz mono 16-bit) |
| `audio_samples/05_trainer_sample_step10000_sentence0.txt` | 242 | The exact input text of the clip with the same name |
| `audio_samples/05_trainer_sample_step10000_sentence0.wav` | 318764 | An existing generated clip (24 kHz mono 16-bit) |
| `audio_samples/06_trainer_sample_step10000_sentence1.txt` | 241 | The exact input text of the clip with the same name |
| `audio_samples/06_trainer_sample_step10000_sentence1.wav` | 341804 | An existing generated clip (24 kHz mono 16-bit) |
| `audio_samples/07_trainer_sample_step10000_sentence2.txt` | 224 | The exact input text of the clip with the same name |
| `audio_samples/07_trainer_sample_step10000_sentence2.wav` | 288044 | An existing generated clip (24 kHz mono 16-bit) |
| `audio_samples/08_trainer_sample_step15000_sentence0.txt` | 242 | The exact input text of the clip with the same name |
| `audio_samples/08_trainer_sample_step15000_sentence0.wav` | 322604 | An existing generated clip (24 kHz mono 16-bit) |
| `audio_samples/09_trainer_sample_step15000_sentence1.txt` | 241 | The exact input text of the clip with the same name |
| `audio_samples/09_trainer_sample_step15000_sentence1.wav` | 334124 | An existing generated clip (24 kHz mono 16-bit) |
| `audio_samples/10_trainer_sample_step15000_sentence2.txt` | 224 | The exact input text of the clip with the same name |
| `audio_samples/10_trainer_sample_step15000_sentence2.wav` | 299564 | An existing generated clip (24 kHz mono 16-bit) |
| `audio_samples/11_eval15000_easy_sent_07_v0.txt` | 38 | The exact input text of the clip with the same name |
| `audio_samples/11_eval15000_easy_sent_07_v0.wav` | 86444 | An existing generated clip (24 kHz mono 16-bit) |
| `audio_samples/12_eval15000_easy_sent_07_v1.txt` | 38 | The exact input text of the clip with the same name |
| `audio_samples/12_eval15000_easy_sent_07_v1.wav` | 86444 | An existing generated clip (24 kHz mono 16-bit) |
| `audio_samples/13_eval15000_hard_sent_02_v0.txt` | 96 | The exact input text of the clip with the same name |
| `audio_samples/13_eval15000_hard_sent_02_v0.wav` | 151724 | An existing generated clip (24 kHz mono 16-bit) |
| `audio_samples/14_eval15000_hard_sent_19_v0.txt` | 75 | The exact input text of the clip with the same name |
| `audio_samples/14_eval15000_hard_sent_19_v0.wav` | 124844 | An existing generated clip (24 kHz mono 16-bit) |
| `audio_samples/15_eval15000_hard_sent_15_v0.txt` | 76 | The exact input text of the clip with the same name |
| `audio_samples/15_eval15000_hard_sent_15_v0.wav` | 117164 | An existing generated clip (24 kHz mono 16-bit) |
| `audio_samples/README.md` | 9434 | Table of the 15 clips with durations, exact input texts and how each was made |
| `configs/eval_gen.yaml` | 1284 | Generation config used for evaluation: Kyutai's english_2026-04_24l.yaml with our tokenizer.json path (identical for 10k and 15k) |
| `configs/full_run_args_resolved.yaml` | 2922 | Resolved configuration of the full run exactly as Kyutai's trainer saved it (args.yaml) |
| `configs/pilot_resolved_config_from_log.yaml` | 1983 | Resolved configuration of the pilot, as printed at the top of its training log (the file itself is on notebook rag) |
| `data_samples/README.md` | 2942 | What the data samples are, and what could not be provided (our manifests) |
| `data_samples/eval_valid_clips_24.tsv` | 8072 | The 24 held-out validation clips used in evaluation (normalised text, real durations) |
| `data_samples/local_prep_test_4clips_train.jsonl` | 2184 | Our manifest format, 4 lines from a local test of the prep script |
| `data_samples/pilot_first_valid_line_as_printed.txt` | 583 | One pilot validation manifest line as printed on the notebook |
| `data_samples/pilot_prep_stats.json` | 496 | Statistics printed by the pilot prep (counts, rejects by reason, domains) |
| `data_samples/rasa_telugu_parquet_schema_and_two_rows.txt` | 1943 | Rasa Telugu Parquet schema and its first two rows |
| `data_samples/raw_vs_model_input_text_examples.md` | 6797 | Raw text versus cleaned text, what the rules reject, and the {digits}{spoken form} finding |
| `data_samples/syspin_telugu_male_transcripts_first10.json` | 4348 | Header and first 10 entries of the raw SYSPIN Telugu male metadata file (verbatim) |
| `data_samples/telugu_test_sentences_30_NOT_PROOFREAD.txt` | 3464 | The 30 test sentences written by the assistant; not proofread by a Telugu speaker |
| `data_samples/trainer_sample_sentences_exact.txt` | 941 | The 3 sentences the trainer synthesised at each checkpoint (exact text) |
| `diffs/README.md` | 3617 | Why no git diff exists, the evidence that Kyutai code was not modified, and how to close the gap |
| `diffs/config_deltas_vs_finetune_language.md` | 4744 | Key-by-key config changes against Kyutai's finetune_language.yaml, with upstream values and their sources |
| `diffs/new_files/download_syspin.sh` | 2378 | Our script, written but NOT used: SYSPIN download and extraction |
| `diffs/new_files/eval_telugu.py` | 9190 | Our script: CPU generation and read-back CER evaluation (final version) |
| `diffs/new_files/from_transcript/make_pilot_cfg.py` | 1315 | Script that wrote the pilot config; text taken from the chat (it was never a file in the project) |
| `diffs/new_files/from_transcript/make_telugu_full_cfg_handrun.py` | 1665 | Script that wrote the full-run config, run by hand; text taken from the owner's paste |
| `diffs/new_files/prep_rasa.py` | 7365 | Our script: the same chain for Rasa Telugu Parquet files |
| `diffs/new_files/prep_syspin.py` | 7361 | Our script: SYSPIN text cleaning, silence trim, loudness normalisation, 24 kHz conversion, manifests and 2% hash split |
| `diffs/new_files/run_pipeline.sh` | 6597 | Our script: unattended Rasa prep, combine, 4-GPU alignment, tokenizer, config (stops before training); final version with the lock and fixes |
| `diffs/new_files/setup_instance.sh` | 3348 | Our script, written but NOT used: notebook set-up |
| `diffs/new_files/sync_to_s3.sh` | 1439 | Our script: copies run checkpoints, logs and samples to S3 every 10 minutes |
| `environment.txt` | 9195 | Hardware, OS, CUDA, Python and all 113 package versions, each with its source; UNKNOWN items marked |
| `logs/eval/results_10000.csv` | 34698 | The same per-clip results as a table |
| `logs/eval/results_10000.json` | 47208 | Per-clip evaluation results for that checkpoint (text, what the recogniser heard, CER, durations) |
| `logs/eval/results_15000.csv` | 34590 | The same per-clip results as a table |
| `logs/eval/results_15000.json` | 47099 | Per-clip evaluation results for that checkpoint (text, what the recogniser heard, CER, durations) |
| `logs/full_run_events.csv` | 590 | Run-start and checkpoint events with UTC times (export of progress.jsonl) |
| `logs/full_run_progress.jsonl` | 94200 | The trainer's own machine-readable log of the full run (run starts, 310 train rows, 6 validation rows, checkpoint events) |
| `logs/full_run_train_loss.csv` | 50382 | Training loss, gradient norm, learning rate and speed every logged step of the full run (export of progress.jsonl) |
| `logs/full_run_valid_loss.csv` | 852 | Validation loss at steps 2500 to 15000 (export of progress.jsonl) |
| `logs/pilot_loss.csv` | 976 | Pilot training and validation values parsed from that pasted log |
| `logs/pilot_train_log_as_pasted.txt` | 8766 | The pilot's training log as the owner pasted it (the first lines include the resolved config) |
| `logs/terminal_sessions_as_pasted.md` | 226657 | All 46 notebook terminal sessions pasted into the chat, with timestamps (closest thing to shell history); host names and the token name redacted |
| `source_docs/CLAUDE.md` | 3777 | Standing instructions given to every Claude session on this project |
| `source_docs/captured_HF_model_page_kyutai_pocket-tts_2026-10-12.md` | 26699 | Copy of the Hugging Face model page of kyutai/pocket-tts fetched 2026-10-12 (licence front matter) |
| `source_docs/captured_kyutai_pocket-tts_README_2026-10-12.md` | 27703 | Copy of Kyutai's Pocket TTS README fetched 2026-10-12 |
| `source_docs/captured_kyutai_pocket-tts_training_README_2026-10-12.md` | 17911 | Copy of Kyutai's training README fetched 2026-10-12 |
| `source_docs/carried_over_from_stt_research.md` | 7503 | TTS-relevant findings carried over from the STT research (Kyutai, Prasad, datasets, licences) |
| `source_docs/evidence_2026-10-14_pages_captured_via_browser_pane.md` | 9407 | Primary-source captures read in the browser pane on 2026-10-14 (Kyutai gate, training README, SYSPIN, Rasa, Prasad) |
| `source_docs/stt_research_kyutai_repos.md` | 50028 | STT-phase research note on Kyutai repos (source of the MIT code licence and the 313M parameter claim) |
| `source_docs/tts_hindi_run_sheet_SUPERSEDED.md` | 16159 | Plan for Hindi (superseded by the Telugu-only scope of 2026-10-17) |
| `source_docs/tts_pipeline.md` | 20242 | The first TTS plan (2026-10-14), with revision notices v1.1 and v1.2 on top |
| `source_docs/tts_progress_log_FULL.md` | 85004 | The complete TTS project log (all decisions TD-, activities TA-, open questions), refreshed at the end of this task (the Hugging Face token's name is redacted in this copy; the live log in tts/progress.md still has it) |
| `source_docs/tts_telugu_teacher_run_sheet.md` | 7835 | The Telugu teacher fine-tune plan written 2026-10-17 (steps, estimates, proposed success marks, risks) |
| `transcripts_summary.md` | 37254 | Dated summary of the Claude Code session (2026-10-08 to 2026-10-18) with quotes of decisions and errors, plus an index of all 222 user messages (the msg #N numbers used in the report) |

**Total: 84 files, 4.83 MB uncompressed.**
