# diffs/: changes against the original Kyutai code

## Short answer
**No `git diff` against Kyutai's commit could be produced, and no change to Kyutai's code is recorded anywhere.** Both statements are explained below so a reviewer can decide how far to trust them.

## Why no git diff exists
- Kyutai's repository (https://github.com/kyutai-labs/pocket-tts) was cloned **only on the two SageMaker notebooks** (`rag` for the pilot, `tts` for the full run). No copy of the repo, and no git history of it, exists on the machine this folder was compiled on (checked: no `.git` anywhere in the project folder) - UNKNOWN - not found in records.
- The notebooks were not accessed while compiling (the rules forbid running anything), so `git status` / `git diff` could not be read.
- Commit on the full-run notebook `tts`: `1df6b3da17cb43eff8c4c4e077f785520492adff` (`git rev-parse HEAD`, transcript message #152). The trainer recorded it as **`1df6b3d-dirty`** in `logs/full_run_progress.jsonl`, i.e. the working tree differed from that commit. **Which files differed is UNKNOWN.** Commit on the pilot notebook `rag`: UNKNOWN.

## Why we believe Kyutai's code was not modified (evidence, not proof)
1. None of the 46 pasted notebook sessions (`logs/terminal_sessions_as_pasted.md`) shows an edit, `sed -i`, `patch`, `git apply`, `git checkout`, `git stash` or `git pull` on the repo.
2. The assistant never advised editing Kyutai's Python files (searched all 293 assistant text blocks; the one `sed -i` was a config-file copy, 2026-10-18T04:33Z, superseded by `from_transcript/make_pilot_cfg.py`, and never shown as run).
3. Everything we changed was done through **config values** and **our own scripts** (below).
4. **What probably explains "-dirty"** (INFERRED from 1-3, not checked): the new config files we created inside the checkout: `training/configs/telugu_pilot.yaml` and `training/configs/telugu_full.yaml` (the `-dirty` marker from some tools also counts untracked files).

## What is in this folder
- `config_deltas_vs_finetune_language.md`: every config key we changed relative to Kyutai's `training/configs/finetune_language.yaml`, with the upstream value and where it was recorded.
- `new_files/`: our own code with no upstream counterpart, copied unchanged:
  - `prep_syspin.py`, `prep_rasa.py`, `run_pipeline.sh`, `eval_telugu.py`, `sync_to_s3.sh`: used.
  - `setup_instance.sh`, `download_syspin.sh`: written but **not used** (the notebooks were set up by hand, see `PROCESS_REPORT.md` Section 10).
  - `from_transcript/make_pilot_cfg.py`, `from_transcript/make_telugu_full_cfg_handrun.py`: the two scripts that wrote the pilot and full configs; they exist only in the chat (extracted from the transcript with the dates in their header comments).
  - Note: `eval_telugu.py` and `run_pipeline.sh` were edited several times on 2026-10-18 (fixes listed in `PROCESS_REPORT.md` Section 11); the copies here are the **final** versions as uploaded for the last use. The versions that actually ran at each earlier moment are not preserved separately (UNKNOWN), except where a fix is described in the report.

## How a reviewer can close the gap (read-only commands, NOT run by the compiler)
On the notebook `tts` (and `rag` for the pilot commit):
```bash
cd ~/SageMaker/tts/pocket-tts
git rev-parse HEAD
git status --short
git diff > ~/SageMaker/tts/pocket_tts_repo.diff      # changes to tracked files (empty if none)
git diff --no-index /dev/null training/configs/telugu_full.yaml | head -80   # the untracked config as a diff
```
Then compare the first output with `1df6b3da17cb43eff8c4c4e077f785520492adff`.
