# 10X_STT: instructions for Claude sessions

Project: speech technology for Hindi, Telugu and English for the company, in two workstreams: **STT** (speech-to-text; offline, native-script output, three monolingual models, commercial, open data only, AWS rented, very tight budget) and **TTS** (text-to-speech; started 2026-10-14 after the senior asked for immediate TTS work; STT is paused, not cancelled).

## Folder layout
- `stt/` is the STT workstream: `stt/progress.md` (log and memory), `stt/pipeline_3week_lean.md` (the **newer, likely-to-be-used 3-week low-cost plan**, decision D-022), `stt/pipeline.md` (the older, larger plan, kept unchanged for reference), `stt/reports/`, `stt/research_notes/`, `stt/evidence/`.
- `tts/` is the TTS workstream: `tts/progress.md` (log and memory), `tts/research_notes/` (including `carried_over_from_stt_research.md`), `tts/reports/`, `tts/evidence/`.
- Each workstream has **its own `progress.md`**. Work on STT goes in `stt/`; work on TTS goes in `tts/`. Do not mix them. Findings that affect both are noted in each log with a pointer.

## Memory files (the source of truth)
- **At the start of every session:** read the root context here, then read Sections 1 (context brief) and 2 (status snapshot) of the `progress.md` for the workstream you are working on (`stt/progress.md` or `tts/progress.md`). If unsure which, read both snapshots. Read the relevant part of that workstream's plan before working on it.
- **Before finishing every session** (and whenever something material happens): update that workstream's `progress.md` following its Section 0 rules and session-close checklist:
  - append an activity entry (`A-0NN` in STT, `TA-0NN` in TTS; append-only; never edit or delete old entries, correct them with a new entry);
  - refresh the status snapshot, including "Next actions";
  - update whichever ledgers changed (budget, runs, device benchmarks, data, legal, open questions, unknowns, risks).
- **Plan changes:** log a decision (`D-###` in STT, `TD-###` in TTS; plus a pivot if the direction changes) in the relevant `progress.md` first, then edit the plan and note the change at its top. Never change gate thresholds after seeing results without a logged decision.

## Working rules
- Label evidence the way these files do: [M] measured by a cited source, [V] vendor claim, [E] our estimate, [P] proposal, [U] unverified, [OURS] our own measurement with a run or benchmark ID. Record numbers together with their conditions (device, chunk size, normalizer version, dataset hash, commit).
- Do not present estimates or proposals as facts. Many numbers in the research are unverified, so spot-check before anything leaves the team.
- Spending money (AWS GPU, TTS/LLM synthesis, annotation, recording) or sending anything outward (licence letters, access requests, messages to NVIDIA, AI4Bharat, ARTPARK, Kyutai or any author or dataset owner) needs the user's explicit go-ahead first. Accepting a gated dataset or model agreement is the user's own action, never ours. Log it in the relevant `progress.md` after.
- Data and licences: use the more restrictive reading when labels conflict; capture dated gate text for gated datasets; never use T4 data (see `stt/pipeline.md` Section 6 and `stt/reports/Svanita Kyutai and dataset licence audit.md`). Never train on test-set audio.
- STT: use native script for training targets (English words inside Hindi/Telugu stay in native script, decision D-023). Romanization is an optional post-process, never a training target.
- Machine notes (Windows): pandoc and LibreOffice are not installed; Word is installed; use PowerShell for `npm`. The browser pane can read pages the user is signed into; the user signs in and accepts gates. Details are in `stt/progress.md` Section 1.
