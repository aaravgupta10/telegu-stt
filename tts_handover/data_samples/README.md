# data_samples: manifest and metadata excerpts (no audio, no datasets)

**What the senior asked for:** "10 sample lines from each manifest/metadata file". **That could not be provided for our own manifests** (UNKNOWN - not found in records): the `train.jsonl`, `valid.jsonl`, `train_aligned.jsonl` and `valid_aligned.jsonl` files of the pilot and the full run exist only on the notebooks (`~/SageMaker/tts/data/pilot/` and `~/SageMaker/tts/data/full*/`); they were never copied to this machine. The command that would produce them is in `PROCESS_REPORT.md` Appendix A. What does exist is below.

| File | What it is | Source |
|---|---|---|
| `syspin_telugu_male_transcripts_first10.json` | **Header and the first 10 entries, verbatim**, of the raw SYSPIN Telugu male metadata file (`MetaData`, `SpeakersMetaData`, `Transcripts` with `Transcript` and `Domain`). The full file has 21,463 entries. | extracted from the SYSPIN archive on 2026-10-17 (scratchpad copy of `IISc_SYSPINProject_Telugu_Male_Spk001_HC_Transcripts.json`) |
| `local_prep_test_4clips_train.jsonl` | **Our manifest format** (`path`, `duration`, `transcript`), 4 lines, written by `prep_syspin.py` in a local test on 4 SYSPIN clips (2026-10-18 about 09:50 IST). The paths are local Windows paths from that test. | scratchpad `mini_out/train.jsonl` |
| `pilot_first_valid_line_as_printed.txt` | One manifest line from the pilot's `valid.jsonl` as printed on notebook `rag` | owner's paste, transcript message #143 |
| `pilot_prep_stats.json` | `stats.json` of the pilot prep: clips in the JSON, kept, rejected by reason, domain counts | owner's paste, transcript message #129 |
| `rasa_telugu_parquet_schema_and_two_rows.txt` | Rasa Telugu Parquet schema (`filename`, `text`, `language`, `gender`, `style`, `duration`, `wav_path`, `audio`), rows in the first shard (489), and the first two rows | owner's paste, transcript message #172 |
| `eval_valid_clips_24.tsv` | The 24 held-out validation clips used by the evaluation: clip name, real duration, text with punctuation removed (the exact original string was not saved) | `logs/eval/results_15000.json` |
| `trainer_sample_sentences_exact.txt` | The 3 sentences the trainer synthesised every 2,500 steps (exact text) | `configs/full_run_args_resolved.yaml` |
| `telugu_test_sentences_30_NOT_PROOFREAD.txt` | The 30 test sentences (20 digit-free ones were used) written by the assistant on 2026-10-17; **no Telugu speaker has proofread them** | `tts/eval/telugu_test_sentences.txt` |
| `raw_vs_model_input_text_examples.md` | Raw transcript versus the cleaned text the model receives (4 recorded pairs), counts and examples of what the text rules reject, and the finding that all 412 digit-containing male transcripts carry a `{digits}{spoken form}` pair | computed by reading the raw male transcripts file |

Not available at all: any raw excerpt of the SYSPIN **female** metadata, and any excerpt of our Rasa manifests.
