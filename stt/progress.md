# 10X_STT: Progress Log (living document)

> **Purpose.** This file is the project's memory. It records every action, plan, decision, pivot, measurement and open question so that no one (human or AI session) ever has to reconstruct context from scratch.
> **The plan lives in `pipeline.md`. What actually happened lives here.**

## 0. How to maintain this file (READ FIRST)

1. **At the start of every session:** read Section 1 (Context-restoration brief) and Section 2 (Status snapshot). Then read the stage you are about to work on in `pipeline.md`.
2. **During work:** when a decision is made, a plan changes, a measurement is taken, a run finishes, or a question opens/closes, update the relevant table **and** add an entry to the Activity Log (Section 14).
3. **At the end of every session:** (a) append an Activity Log entry, (b) refresh the Status snapshot (Section 2), (c) update the ledgers (budget, data, runs, legal, unknowns) that changed, (d) write "Next actions".
4. **Never delete or rewrite old log entries.** Correct a mistake with a *new* dated entry that references the old one (e.g. "Correction to A-012: ...").
5. **Plan changes:** a change to `pipeline.md` (threshold, model, stage, dataset) needs a Decision entry (`D-###`) here *first*, then edit `pipeline.md` and bump its version. A change of direction also gets a Pivot entry (`P-###`).
6. **Always record numbers with their conditions** (device, chunk size, normalizer version, dataset hash, commit, run ID). A number without conditions is useless later.
7. **Label evidence** the same way as `pipeline.md`: **[M]** measured by a cited source, **[V]** vendor claim, **[E]** our estimate, **[P]** proposal, **[U]** unverified. For *our own* measurements use **[OURS]** plus run/benchmark ID.
8. **ID schemes:** `D-###` decisions, `P-###` pivots, `A-###` activity entries, `RUN-####` training/eval runs, `BM-###` device benchmarks, `DS-...-vN` dataset versions, `L-##` legal items, `U-##` unknowns, `Q##` open questions, `R-##` risks.
9. **Dates:** ISO `YYYY-MM-DD`. Time of day optional but useful for long days.

---

## 1. Context-restoration brief (if you read nothing else, read this)

**What the project is.** Build a post-trained, **true-streaming** speech-to-text model for **Hindi, Telugu and English (incl. Hindi-English and Telugu-English code-switching)** that runs faster than real time on **laptop/mini-PC CPUs (x86 and Apple silicon)**. **Commercial product, open data only** (no proprietary audio). Compute: **one AWS A10G (24 GB)**, **few-hundred-dollar budget**. Existing architectures only; **post-training focus**; no pre-training. Output in **native script**; **Romanized output is NOT a must** (reason unconfirmed; optional deterministic post-process only).

**Who/what.** The owner is an engineer at 10X Technologies (per account email) who must (1) find the best lab methodology for this use case, (2) design an end-to-end pipeline, (3) get **senior approval**, (4) then build the STT.

**The plan in one paragraph.** Fine-tune (not distil) **NVIDIA Nemotron-3.5-ASR-Streaming-0.6B** (cache-aware FastConformer-RNNT, Hindi supported, **Telugu NOT supported**) on a T1-licence-only mix (~1,280 h MVP: Hindi 550, Telugu 400, English 280, code-switch 50) with multi-lookahead streaming training; export to int8 ONNX; run with **sherpa-onnx >= 1.13.5**. A 1-2 week **Stage 1 spike** (unmodified-model export + laptop RTF + Telugu tokenizer test + 10-20 h Telugu tracer fine-tune + A10G throughput) decides whether this is viable; otherwise fall back to a ~114M cache-aware NeMo model (Path B). Distillation (pseudo-labelling from IndicConformer/SraVaani teachers; model compression) is production-tier only.

**Facts that must not be forgotten**
- **No existing checkpoint meets every constraint.** Nemotron-3.5: streaming+Hindi, no Telugu. SraVaani-0.5-live: streaming+Telugu but CTC-only, gated, no ONNX. IndicConformer: Hindi+Telugu but offline.
- **Parakeet-TDT-v3 / Canary-v2 = 25 European languages only.** Parakeet v2/110M = English only. Parakeet 1.1B Indic = bn/en/hi/ta (no Telugu). The first AI-generated blueprint wrongly assumed Parakeet knew Indic acoustics.
- **Kyutai STT = English/French only, 1B/2.6B params, GPU-class.** Rejected.
- **Binding constraint = Telugu data**: ~670 h clean commercial-safe [E]; no open Telugu-English code-switch corpus exists; Hindi-English only SLR104 (~90 h, CC BY-SA, lecture style).
- **Dataset licence labels conflict** across official pages for Kathbath, Lahaja, IndicVoices-R, SPRING-INX and others; gated sets' conditions only visible after login. Use the more restrictive reading; capture gate text with date.
- **Nemotron-3.5 licence conflict** (OpenMDW-1.1 on HF card vs "NVIDIA Open Model License" on a Together AI listing); text unread -> legal item L-01.
- **Never use Whisper's normalizer** for Hindi/Telugu. Freeze our own versioned normalizer. Telugu WER/CER ratio ~3.5-3.7x, so report CER.
- **Compute numbers are estimates**: ~150 audio-h/GPU-h (120M) and ~30 audio-h/GPU-h (600M) [E], each possibly 2x off. **No A10G NeMo benchmark exists anywhere**; Stage 1 measures it.
- **sherpa-onnx < 1.13.5 silently mis-decodes NeMo streaming transducers.** Pin runtime and exporter together. Quantize to **uint8** weight-only encoder MatMuls; keep convs/decoder/joiner/caches fp32.
- **MVP cost** (lean) ~275 GPU-h ~ **$370 on-demand / ~$195 spot** [E]; excludes storage, test-set annotation, engineer time, legal.
- **Approval flow:** four senior checkpoints (plan+spike; after Stage 1; after Stage 4; after Stage 7).
- **Terminology:** "post-training" here = fine-tuning an existing checkpoint (plus optional pseudo-label distillation), not RLHF-style post-training.

**Where things are**

| Path | What |
|---|---|
| `CLAUDE.md` | Standing instructions for every Claude session (read `progress.md` first; update it before finishing; spending/outward actions need the owner's go-ahead) |
| `pipeline.md` | The full plan (Stages 0-9, specs, gates, budget, risks, pivot tree) |
| `progress.md` | This log |
| `reports/Edge streaming Indic STT pipeline.md` / `.docx` | ~8k-word research report (the evidence base; `.docx` is landscape, 22 pages) |
| `research_notes/Edge streaming Indic STT pipeline/` | 6 raw research notes: `base_models.md`, `lab_methodologies.md`, `datasets_licenses.md`, `post_training.md`, `edge_runtime_output.md`, `evaluation_benchmarks.md` |

**Caveats about the evidence base**
- **Compute assumption caveat (added 2026-10-12).** The "one AWS A10G, few-hundred-dollar budget" constraint (R5) came from the *AI-generated blueprint* the owner pasted on 2026-10-08, not from the owner's own words. It was never explicitly confirmed. On 2026-10-12 the owner's normal-chat notes say **8x A10 (24 GB) on AWS**, and the senior's WhatsApp says **"dgx level setup with 8 A100s"**. Every GPU-hour, cost and throughput figure in `pipeline.md` assumes one A10G and must be re-based once Q17 is answered. Also new: the senior wants **three separate monolingual models** and the target includes **phones**. See A-015, Q17-Q23 and `research_notes/context_from_normal_chats_2026-10-12.md`.
- Research was done by 6 parallel AI researchers on 2026-10-08; each used 34-97 tool calls (more than guideline), and many arXiv papers were read via summarising fetch tools. **Spot-check any number before it goes into a document that leaves the team.**
- Several source conflicts are catalogued in `pipeline.md` Section 17 (U-01 to U-23). Nothing there is resolved yet.
- Gate thresholds, stage GPU-hours, the bake-off decision rule and the data-mix proportions are **our proposals/estimates**, not sourced figures.

**Environment notes (this Windows machine)**
- Working directory: `C:\Users\Aarav Gupta\Downloads\10X_STT`. Shells: PowerShell (primary) and Git Bash.
- **pandoc is not installed.** LibreOffice is not available (the skill's `soffice.py` fails on Windows: `socket.AF_UNIX` missing). **Microsoft Word is installed** (usable via COM for docx->PDF and inspection). `pdftoppm` is not installed; PyMuPDF/pip not available in the default python venv.
- `npm install` in Git Bash failed ("Could not determine Node.js install directory"); **use PowerShell for npm**.
- The `.docx` was produced by a custom Markdown->docx script (npm `docx` + `marked`, landscape, tables sized to page width). The script and packages were temporary and have been removed; rebuild if the `.md` changes.

---

## 2. Status snapshot (UPDATE IN PLACE at the end of every session)

| Field | Value |
|---|---|
| **Last updated** | 2026-10-14 (**STT PAUSED**: the team switched to TTS, see A-032 and D-024; before that 2026-10-13: lean 3-week plan written, senior chose native-script output) |
| **Project phase** | PLANNING. Pipeline drafted, **awaiting senior review/approval (checkpoint 1)** |
| **Current stage** | None started. Stage 0 not started |
| **Primary path** | Path A (Nemotron-3.5-ASR-Streaming-0.6B), *conditional on Stage 1 spike* |
| **Spend so far** | $0 AWS, 0 GPU-hours |
| **Open blockers** | (0, added 2026-10-12; since answered: 8 A100s 40 GB, three monolingual models, offline STT, STT first then TTS) Plan conflicts with new context: compute (1x A10G assumed vs 8x A10 / 8x A100 reported), **three separate monolingual models** requested by the senior, phones in scope, streaming listed as "unknown" in the chat notes, TTS scope unknown; senior is still waiting on the owner's message about Kyutai vs NVIDIA (Q17-Q23, D-pending). (1) Senior approval; (2) legal items L-01..L-06 unfiled; (3) minimum-spec laptops not named (Q9); (4) no AWS GPU quota requested yet |
| **Latest gate result** | n/a |
| **Next actions** | 0. (2026-10-12) Audit done: `reports/Svanita Kyutai and dataset licence audit.md` (A-019). Now: owner answers Q17-Q25; owner does the browser-only checks (report Section 9, most important first); owner approves what to send from the drafted licensor/author questions (report Section 10; nothing sent); then log D-### decisions and re-base `pipeline.md` (per-language models, Telugu data and tokenizer route, compute, TTS scope). 1. Share `pipeline.md` + report with seniors; request checkpoint-1 approval. 2. Decide Q7-Q16 where possible (esp. Q7 scope, Q8 chunk size, Q9 devices, Q10 output policy, Q12 test-set budget). 3. Start Stage 0: repo structure, HF access requests (IndicVoices, Vaani, Kathbath, IndicConformer, SraVaani, Nemotron), capture gate text, send licence letters (NVIDIA, AI4Bharat, ARTPARK), AWS GPU vCPU quota + budget alarm, pin versions, pre-register gates. 4. Begin Stage 1 spike as soon as devices + Nemotron access exist. |

---

## 3. Project charter (condensed)

- **Goal:** edge-deployable streaming STT for hi/te/en incl. code-switching (see Section 1).
- **Hard requirements:** R1 true streaming; R2 laptop CPU target; R3 commercial + open-data-only; R4 hi/te/en + code-switch; R5 one A10G, few hundred dollars; R6 Romanized not required; R7 existing architectures, post-training only; R8 senior approval before build. (`pipeline.md` Section 1.2.)
- **MVP definition:** T1-only mix passes the MVP gates (`pipeline.md` 8.6) on the private test set, streaming, int8, on the named lowest-spec laptop. Telugu within +10% of its gate.
- **Production definition:** passes production gates incl. Telugu, code-switch, telephony.
- **Scope option on the table:** Hindi + English GA, Telugu beta (Q7 open).

---

## 4. Decision log

Status values: **Confirmed** (by the owner), **Proposed** (by us, awaiting seniors), **Superseded**, **Reversed**.

| ID | Date | Decision | Alternatives considered | Rationale / evidence | Status |
|---|---|---|---|---|---|
| D-001 | 2026-10-08 | Discard the first AI-generated blueprint (Parakeet/IndicConformer TDT, frozen encoder, IndicXlit-Romanized targets); replace with the researched pipeline | Keep and patch | Eight flaws (see P-001, `pipeline.md` 2.4). Owner explicitly said "forget the pipeline I sent earlier" | Confirmed |
| D-002 | 2026-10-08 | Requirement: **true streaming** | Utterance-level; batch | Owner's answer to clarifying question | Confirmed |
| D-003 | 2026-10-08 | Target device: **laptop / mini-PC CPU (x86 + Apple silicon)** | Android phone; Raspberry Pi; mixed | Owner's answer; allows ~600M-parameter models | Confirmed |
| D-004 | 2026-10-08 | **Commercial product, open data only** | Proprietary data; internal-only | Owner's answer; forces licence tiering | Confirmed |
| D-005 | 2026-10-08 | **Romanized output is not a must**; train on native script; Romanization = optional deterministic post-process | Train on Romanized targets (original blueprint) | Owner: "not a must and should as of now" (reason unconfirmed -> Q16). Romanized targets are noisy and break WER | Confirmed (requirement); Proposed (design) |
| D-006 | 2026-10-08 | **Primary base model: Nemotron-3.5-ASR-Streaming-0.6B** (Path A), conditional on Stage 1 spike | SraVaani-live (C); 114M NeMo (B); IndicConformer; Whisper; Kyutai; Omnilingual; Qwen3-ASR; Voxtral | Only candidate with native cache-aware streaming, Hindi, public fine-tune recipe, maintained sherpa-onnx loader, commercial-use statement. Telugu missing = main risk | Proposed |
| D-007 | 2026-10-08 | **Method for MVP = full fine-tuning (staged: head warm-up then full FT, multi-lookahead streaming training)**; distillation only in production tier | Distillation first; LoRA (unsupported for Nemotron-3.5); frozen encoder | Fits budget; needs no teacher/unlabeled audio; encoder must learn Telugu sounds | Proposed |
| D-008 | 2026-10-08 | **Runtime: sherpa-onnx >= 1.13.5, int8 (uint8 weight-only encoder MatMuls)** | ORT-direct; whisper.cpp; MLX/CoreML (optional Apple path); OpenVINO | First-class NeMo cache-aware support; Apache-2.0; C++/multi-language bindings | Proposed |
| D-009 | 2026-10-08 | **Reject Kyutai** | Adopt DSM | en/fr only; 1B/2.6B; GPU/CUDA; 2.5M h pretraining on 48 H100 | Proposed |
| D-010 | 2026-10-08 | **MVP data mix ~1,280 h T1-only** (Hi 550, Te 400, En 280, CS 50); production ~4,200 h | Include T2 (Kathbath, Shrutilipi, NPTEL) from the start | Licence risk tiers; Telugu is binding; T2 only under written risk acceptance | Proposed |
| D-011 | 2026-10-08 | Teachers for pseudo-labels: IndicConformer-600M + SraVaani-1.0; **not** Whisper-large-v3 or cloud APIs | Whisper; Omnilingual-7B; Sarvam/Gemini/Deepgram | Whisper Telugu script collapse; Omnilingual evidence contradictory; API ToS risk | Proposed (needs L-02) |
| D-012 | 2026-10-08 | `pipeline.md` (plan) and `progress.md` (log) are the project's source of truth; research report `.md/.docx` is the evidence base | Ad-hoc notes | Prevent context rot | Confirmed |
| D-013 | 2026-10-08 | Project folder = `C:\Users\Aarav Gupta\Downloads\10X_STT` (moved from the session scratch folder) | Keep scratch | Owner moved the session; 8 files copied | Confirmed |

| D-014 | 2026-10-08 | Add a project `CLAUDE.md` that makes every session read and maintain `progress.md`, and requires the owner's explicit go-ahead before spending money or sending anything outward | Rely on the owner reminding each session | Owner wants context rot to never be a problem | Confirmed |
| D-015 | 2026-10-12 | **Compute = 8 A100 GPUs** (owner: "we have 8 a100s"). Replaces the inherited one-A10G assumption (R5) | One A10G; 8x A10 (AWS) | Owner's statement; matches the senior's WhatsApp ("dgx level setup with 8 A100s"). Still unknown: 40 GB or 80 GB, owned vs billed, shared with other teams | Confirmed (details open) |
| D-016 | 2026-10-12 | **Three separate monolingual models** (Hindi, Telugu, English-India), each keeping English words in Latin script inside Hindi/Telugu | One multilingual model with code-switching (earlier plan) | Senior's explicit requirement, confirmed by the owner | Confirmed |
| D-017 | 2026-10-13 | **The STT model must be OFFLINE** (not true streaming). Supersedes D-002 | True streaming; utterance-level | Owner confirmed with the senior. Opens the offline route: IndicConformer (Hindi and Telugu per-language models already exist, MIT per READMEs) and Parakeet-TDT-v3-style fine-tunes (as Svanita did); the Nemotron-3.5 streaming route and the Telugu-tokenizer retraining problem are no longer forced. Streaming becomes an optional later phase | Confirmed (supersedes D-002) |
| D-018 | 2026-10-13 | **Scope: both STT and TTS are wanted; STT first**, TTS afterwards (owner: STT is easier to build) | STT only | Owner's statement. Kyutai Pocket TTS becomes relevant in the TTS phase (training code released Aug 2026) | Confirmed |
| D-019 | 2026-10-13 | **GPUs are A100 40 GB (8 of them)**. Refines D-015 | 80 GB | Owner's answer. Still unknown: owned vs billed, shared with other teams | Confirmed (details open) |
| D-021 | 2026-10-13 | **New constraints: very tight budget and only 3 weeks** (owner). The 6-8 week plan no longer fits; a 3-week cut-down plan is being drawn up (see A-027). Note: A-026 mentioned a "D-020" as a proposed bake-off design, which was never recorded as a decision row | Keep the 6-8 week plan | Owner's statement | Confirmed (constraint); plan Proposed |

| D-022 | 2026-10-13 | **Write the 3-week lean plan as a NEW file, `pipeline_3week_lean.md`; keep `pipeline.md` (the older plan) unchanged** apart from a pointer at its top saying the lean plan is newer and likely to be used | Overwrite `pipeline.md` | Owner's instruction: do not overwrite the older plan | Confirmed (plan itself still Proposed pending senior approval) |

| D-023 | 2026-10-13 | **Output policy chosen by the senior: native script ("v1")**: English words inside Hindi/Telugu stay in native script (e.g. मीटिंग). **No Latin-letter variant, no tokenizer change.** Answers Q10 for English words | Latin-letter English (Variant 2) | Senior's instruction after reading the proposed plan; IndicConformer already outputs native script, so the vocabulary is unchanged and the export and training are simpler | Confirmed |

| D-024 | 2026-10-14 | **STT workstream PAUSED (not cancelled); TTS starts immediately** because of urgent constraints (owner, after the senior's request). Project split into `stt/` and `tts/` folders, each with its own `progress.md`; `CLAUDE.md` stays at the project root | Continue STT first | Senior's priority. The senior had approved the STT direction ("loved our work") and chose native-script output (D-023) | Confirmed |

(Add new rows at the bottom. Never delete a row; mark Superseded/Reversed and reference the new ID.)

---

## 5. Pivot log

| ID | Date | From | To | Trigger and evidence | Impact | Decision ref |
|---|---|---|---|---|---|---|
| P-001 | 2026-10-08 | Original AI-generated blueprint: NeMo Parakeet/IndicConformer "FastConformer-TDT", frozen encoder, IndicXlit-Romanized targets, ~100-200 h MVP, <$35 cost, Kyutai rejected only on A10G grounds | Researched pipeline: Nemotron-3.5 streaming fine-tune, native-script training, T1-licensed data mix, spike-first, bake-off, sherpa-onnx int8 | Verification searches + 6-researcher deep research showed Parakeet is not Indic, Romanized targets are noisy, freezing was unsupported, TDT is offline and speeds decoding not encoder, data/licence gaps, export not guaranteed, $35 was one run | Whole plan replaced | D-001 |

(Template for new pivots is in Section 15.)

---

## 6. Stage tracker

| Stage | Name | Planned weeks | Status | Start | End | Gate result | GPU-h (actual) | Cost (actual) | Notes / link |
|---|---|---|---|---|---|---|---|---|---|
| 0 | Governance and foundations | 0-2 | Not started | | | | 0 | $0 | |
| 1 | De-risking spike | 1-2 | Not started | | | | 0 | $0 | |
| 2 | Eval harness, baselines, test set | 2-4 | Not started | | | | 0 | $0 | |
| 3 | Data build | 3-5 | Not started | | | | 0 | $0 | |
| 4 | Bake-off | 5-7 | Not started | | | | 0 | $0 | |
| 5 | Main post-training | 7-11 | Not started | | | | 0 | $0 | |
| 6 | Compression and export | 10-13 | Not started | | | | 0 | $0 | |
| 7 | Evaluation gate and hardening | 12-15 | Not started | | | | 0 | $0 | |
| 8 | Application layer and packaging | 12-16 | Not started | | | | 0 | $0 | |
| 9 | Production track | 16+ | Not started (needs approval) | | | | 0 | $0 | |

Approval checkpoints: **1** plan+spike (pending) | **2** after Stage 1 | **3** after Stage 4 | **4** after Stage 7. Record date, approver and conditions here when granted:

| # | Date | Approver(s) | Outcome / conditions |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |

---

## 7. Budget ledger

**Planned (lean MVP, `pipeline.md` 13.1) [E]:** ~275 GPU-h; ~$276 on-demand / ~$125 spot; + ~$50 TTS; + ~15% contingency; total ~$370 / ~$195. Full report budget ~$300-450 on-demand. Production-scale extrapolation ~$700-800 on-demand.

**Approved ceiling:** *not yet set* (decide at checkpoint 1; set AWS Budgets alarm at 50/80/100%).

**Actuals (one row per billing event / run):**

| Date | Run/Stage | Instance | On-demand or spot | GPU-hours | Cost ($) | Cumulative GPU-h | Cumulative $ | Note |
|---|---|---|---|---|---|---|---|---|
| | | | | | | 0 | 0 | |

**Unpriced items to track separately:** storage (S3/EBS), in-house test-set recording + annotation, engineer time, legal review, laptop hardware, TTS/LLM synthesis spend, any A100 use.

---

## 8. Run registry (training, export and evaluation runs)

| Run ID | Date | Stage | Arm | Purpose | Base ckpt | Dataset (manifest hash) | Config hash / commit | Instance + pricing | GPU-h | Key metrics | Result / decision |
|---|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | | | |

Each run also gets `runs/RUN-####.md` (template in Section 15).

**Device benchmark registry (`BM-###`)**

| ID | Date | Device (CPU, cores, RAM, OS, power mode) | Model/bundle | Chunk | Threads | RTF (paced/unpaced) | Peak RSS | First-token P50/P90 | Finalization P50/P90 | Runtime versions |
|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | | |

**Baseline registry (our re-runs, Stage 2)**

| Model | Test set | Chunk | Normalizer ver | Strict WER | Multi-ref WER | CER | CS-token WER | Notes |
|---|---|---|---|---|---|---|---|---|
| | | | | | | | | |

---

## 9. Data ledger

| Dataset | Version/hash | Access requested | Access granted | Gate text captured | Licence as stated | Tier | Hours (planned / actual) hi / te / en / cs | Manifest rows | Notes |
|---|---|---|---|---|---|---|---|---|---|
| IndicVoices | | not yet | | | CC BY 4.0 (gated) | T1 | 790 / 480 / 0 [E] | | Recount from manifest |
| Vaani | | not yet | | | CC BY 4.0 (gated) | T1 | 1,004 / 184 / 22 transcribed | | Phone/image-prompted |
| SPRING-INX | | not yet | | | CC BY 4.0 vs "public domain" | T1 | 351 / 0 / 0 | | Wording conflict |
| Common Voice v27 | | not yet | | | CC0 | T1 | 15.7 / 0.94 / 2,827 | | |
| FLEURS | | not yet | | | CC BY 4.0 [U] | T1 | ~7 / ~8 / n/a | | Also eval |
| LibriSpeech, VoxPopuli | | not yet | | | CC BY 4.0 / permissive | T1 | English replay | | |
| IndicVoices-R | | not yet | | | BY (HF) vs BY-ND (AIKosh) | T2 | ~75 / ~136 / 0 | | Overlaps IndicVoices |
| Kathbath | | not yet | | | 3 conflicting labels | T2 | ~100 / ~110 / 0 | | Crawled text upstream |
| SLR104 (MUCS Hi-En) | | not yet | | | CC BY-SA 4.0 | T2 | ~90 CS | | Lecture style |
| Shrutilipi | | not yet | | | CC0 pkg / CC-BY-4.0 | T2 | excluded | | AIR audio; out of base mix |
| Models: Nemotron-3.5 | | not yet | | | OpenMDW-1.1 (conflict) | n/a | | | L-01 |
| Models: IndicConformer, SraVaani | | not yet | | | MIT-tagged, gated | n/a | | | L-02 |

Dataset versions frozen for training are recorded as `DS-<tier>-<mix>-vN` with SHA-256 here: *(none yet)*.

---

## 10. Legal and licence tracker

| ID | Item | Owner | Status | Date filed | Reply / outcome |
|---|---|---|---|---|---|
| L-01 | Read OpenMDW-1.1; resolve Together AI "NVIDIA Open Model License" listing; confirm derivative/commercial/on-device redistribution terms | | Open | | |
| L-02 | Written confirmation from AI4Bharat + ARTPARK: commercial use, fine-tuning, use of outputs as pseudo-labels (IndicConformer, SraVaani) | | Open | | |
| L-03 | Capture gate-condition text (IndicVoices, Vaani, Kathbath) at download; counsel review | | Open | | |
| L-04 | Position on T2 data and on CC BY-SA data touching shipped weights | | Open | | |
| L-05 | CC BY attribution duties for model documentation; Indian TDM/DPIIT status; DPDP implications for voice data in the test set | | Open | | |
| L-06 | Licence compatibility: TEN VAD, Silero VAD, Cadence-Fast, NeMo-text-processing, any TTS/LLM used for synthesis | | Open | | |

Generated artefacts to keep in `legal/`: `licence_manifest.csv`, `gate_texts/`, `questions_sent/`. *(None created yet.)*

---

## 11. Open questions (owner decisions)

| ID | Question | Needed by | Status | Answer / decision ref |
|---|---|---|---|---|
| Q7 | Scope: Hi+Te+En GA, or Hi+En GA with Telugu beta? | Before Stage 4 | Open | |
| Q8 | Default chunk size (suggest 320-560 ms) and first-token P90 target | Stage 1 | Open | |
| Q9 | Name the minimum-spec x86 and Apple laptops | Stage 1 | Open | |
| Q10 | Output policy: Latin for English words, ASCII digits, punctuation/casing in/out for Indic | Stage 0/3 | **English words: answered 2026-10-13, native script (D-023).** Still open: digits and punctuation/casing | D-023 |
| Q11 | Tokenizer strategy (small aggregate vs shared BPE; extend vs replace) | Stage 4 | Open (bake-off decides) | |
| Q12 | Budget + owner for in-house test-set recording/annotation | Stage 2 | Open | |
| Q13 | T1-only vs T1+T2 production target; is a T1-only ablation a release requirement? | Stage 9 | Open | |
| Q14 | On-demand vs spot; A100 for batch decoding | Stage 1 | Open | |
| Q15 | Approve gate thresholds after Stage 2 re-runs | Stage 2 | Open | |
| Q16 | Is Romanized output ever required, and why? | Before Stage 8 | Open (owner: "not a must for now") | D-005 |
| Q17 | **Compute:** one A10G (assumed in `pipeline.md`), 8x A10 24 GB on AWS (owner's chat notes), or "dgx level, 8 A100s" (senior's WhatsApp)? Is it owned or billed? | Before any budget/throughput figure is used | **Answered: 8 A100s, 40 GB each** (2026-10-13). Still to confirm: owned or billed? shared with other teams? | D-015, D-019 |
| Q18 | **Model structure:** three separate monolingual models (senior's explicit requirement) vs one multilingual model with code-switching (our plan)? | Before Stage 4 | **Answered 2026-10-12: three separate monolingual models** | D-016 |
| Q19 | **Streaming:** required or not? The chat notes list it as "still unknown"; this project recorded "true streaming" on 2026-10-08 (D-002). Reconfirm. | Stage 1 | **Answered 2026-10-13: OFFLINE** (supersedes D-002) | D-017 |
| Q20 | **Devices:** phones are in scope per the chat notes (laptops only per D-003). Which phones/laptops (RAM, CPU)? | Stage 1 | Open (conflict) | D-003 |
| Q21 | **TTS scope:** is TTS part of this deliverable or STT only? | Now | Open | |
| Q22 | **Accuracy/latency targets** (WER/CER, time to first word) from the senior | Stage 2 | Open | |
| Q23 | Has the owner sent the draft message to the senior (Kyutai vs NVIDIA)? What did the senior reply? | Now | **Not sent as of 2026-10-12; owner wants more info first** (updated draft given in A-020) | |
| Q24 | Which of the drafted licensor/author questions (report Section 10: NVIDIA, AI4Bharat, ARTPARK-IISc/Vaani, IISc SPIRE/RESPIN, Poseidon/Numo, Mozilla, Gram Vaani, OpenSLR/Microsoft, Kapture CX, Kyutai, Prasad Vittaldev, Agora, Bodhan) may be sent, and by whom? | Before relying on T2 data | Open (owner unsure; assistant recommendation: hold, route through senior/legal) | A-019 |
| Q25 | Owner to capture the browser-only items (report Section 9, in priority order: Vaani + IndicVoices gate screenshots; RESPIN form; IndicConformer/SraVaani gates; Numo gate; IndicVoices raw fields + duration sums; bolAIndia STATS.md; IndicTTS PDF; LinkedIn) | Stage 0 | Open | A-019 |

---

## 12. Unknowns and conflicts register (status; details in `pipeline.md` Section 17)

| ID | Short description | Resolve in | Status |
|---|---|---|---|
| U-01 | Nemotron-3.5 licence text/conflict | Stage 0 | **Resolved 2026-10-12 (A-016/A-019): OpenMDW-1.1 for HF weights; archive a dated copy; written NVIDIA confirmation still advisable** |
| U-02 | Is Telugu among Nemotron-3.5's 8 tokenizer-recognised but un-fine-tuned locales? | Stage 1 | **Resolved 2026-10-12: Telugu not supported; tokenizer has zero Telugu characters; `te-IN` prompt slot reserved (id 40). Stage 1 still tests the extension route** |
| U-03 | Does Nemotron-3.5 have a CTC head? | Stage 1 | **Resolved 2026-10-12: no, RNNT-only per NeMo config** |
| U-04 | Can a modified prompt table/vocab export and load in sherpa-onnx? | Stage 1 | Open |
| U-05 | SraVaani-live card inconsistencies | Stage 2 | Open |
| U-06 | SraVaani-1.0 Hindi WER 12.4 vs 14.0 | Stage 2 | Open |
| U-07 | IndicConformer on Vaani-Benchmark: 13.2 vs 20.0 | Stage 2 | Open |
| U-08 | IndicConformer licence (MIT vs CC-BY-4.0 on a repack) | Stage 0 | Open |
| U-09 | Omnilingual Hindi/Telugu contradictory evidence | n/a (not relied on) | Open |
| U-10 | Dataset licence label conflicts | Stage 0 | Open |
| U-11 | IndicVoices hours | Stage 3 | Open |
| U-12 | Vaani hours | Stage 3 | Open |
| U-13 | sherpa-onnx int8 size discrepancy | Stage 1/6 | Open |
| U-14 | Microsoft vs Softcery RTF | Stage 1 | Open |
| U-15 | Silero VAD licence | Stage 8 | **Resolved 2026-10-12: MIT (CC BY-NC text was stale alt text). TEN VAD non-compete clause still for counsel** |
| U-16 | Cloud prices | Stage 0/1 | Open |
| U-17 | A10G NeMo throughput | Stage 1 | Open |
| U-18 | Laptop RTF for streaming FastConformer | Stage 1 | Open |
| U-19 | int8 vs fp32 on Hindi/Telugu | Stage 6 | Open |
| U-20 | Offline -> streaming conversion recipe (we use NVIDIA's released streaming checkpoint) | n/a | Noted |
| U-21 | Tokenizer advice conflict | Stage 4 | Open |
| U-22 | Vendor claims carried (not used as evidence) | n/a | Noted |
| U-23 | Documents/texts never retrieved (OpenMDW-1.1, Indic Open Model License v1.0, gate texts, Whisper licence, NGC 114M licences, etc.) | Stage 0/1 | Open |

---

## 13. Risk register status (details in `pipeline.md` Section 12)

| ID | Risk | Status | Last reviewed |
|---|---|---|---|
| R-01 | Telugu insufficient (~0.7k T1 h; ~30 WER published streaming) | Open, High/High | 2026-10-08 |
| R-02 | Nemotron tokenizer/prompt cannot take Telugu; modified vocab does not export | Open | 2026-10-08 |
| R-03 | 600M too heavy for target laptops | Open | 2026-10-08 |
| R-04 | Licence blocker | Open, Critical | 2026-10-08 |
| R-05 | Code-switch data quality (no real Te-En corpus) | Open | 2026-10-08 |
| R-06 | Catastrophic forgetting | Open | 2026-10-08 |
| R-07 | Pseudo-label noise / teacher output terms | Open | 2026-10-08 |
| R-08 | Export/runtime drift | Open | 2026-10-08 |
| R-09 | Compute estimate off by 2x | Open | 2026-10-08 |
| R-10 | Hallucination/script confusion | Open | 2026-10-08 |
| R-11 | Normalization/eval artefacts | Open | 2026-10-08 |
| R-12 | Domain mismatch (phone vs laptop mic) | Open | 2026-10-08 |
| R-13 | Unpriced costs (storage etc.) exceed GPU bill | Open | 2026-10-08 |
| R-14 | Spot interruptions | Open | 2026-10-08 |

---

## 14. Activity log (APPEND-ONLY; oldest first)

All entries so far are dated 2026-10-08.

**A-001. Task received.** Owner described the task: build an end-to-end pipeline to create an STT model that runs on edge devices; no budget to train from scratch, so use existing architectures and focus on post-training; proficient in Hindi, English and Telugu; several labs have used various methodologies; the owner's job is to find the best one for the use case, build the pipeline, get seniors' approval, then build the STT. The owner shared an AI-generated blueprint (Parakeet/IndicConformer "FastConformer-TDT"; frozen encoder; Romanized IndicXlit transcripts; ~100-200 h MVP up to 3,000 h; one A10G; < $35; ONNX int8 + sherpa-onnx; Kyutai rejected because it supports only en/fr) and said "do not treat this sacredly". Owner asked what we should do, noting Kyutai Labs' success.

**A-002. First assessment + quick verification (6 web searches).** Findings: IndicConformer = AI4Bharat 22-language hybrid CTC/RNNT (600M multilingual; ~120M per-language), MIT per AIKosh; Kyutai STT = `stt-1b-en_fr` (~1B, 0.5 s delay) and `stt-2.6b-en` (2.6B, 2.5 s), en/fr only, GPU/Rust/MLX; Parakeet-TDT-0.6b-v3 = 25 European languages, no Hindi/Telugu; Parakeet RNNT 1.1B Indic variant lists bn/en/hi/ta; dataset licences conflict (Shrutilipi CC0 packaging vs CC-BY-4.0; Kathbath CC0/BY/BY-SA; MUCS licence not found); Omnilingual ASR CTC-300M Apache-2.0 (325M params). Assistant's critique of the blueprint (Romanization noise; Parakeet not Indic; freezing unsupported; TDT offline and decoder-only speedup; thin data; licences; export; cost) -> became P-001. Assistant recommended a 2-week bake-off and listed the four requirement questions.

**A-003. Owner redirect.** Owner: "forget the pipeline I sent earlier"; asked for a new, proper, researched pipeline considering all options and constraints; invited clarifying questions. (-> D-001)

**A-004. Clarifying questions asked and answered.** Q: streaming? -> **true streaming** (D-002). Q: why Romanized? -> **unconfirmed; "not a must"** (D-005). Q: device? -> **laptop / mini-PC CPU (x86 + Apple silicon)** (D-003). Q: commercial/data? -> **commercial, open data only** (D-004).

**A-005. Deep research (6 parallel researchers).** Topics and note files: (1) candidate streaming base models -> `base_models.md`; (2) lab methodologies -> `lab_methodologies.md`; (3) open datasets and licences -> `datasets_licenses.md`; (4) post-training techniques -> `post_training.md`; (5) edge runtime/export/quantization/Romanization -> `edge_runtime_output.md`; (6) evaluation/benchmarks -> `evaluation_benchmarks.md`. Headline results: no checkpoint meets every constraint; Nemotron-3.5-ASR-Streaming-0.6B (2026-06-04; cache-aware RNNT; 40 locales; Hindi yes, Telugu no; OpenMDW-1.1) and SraVaani-0.5-live (Aug 2026; ~430M CTC; Hi+Te streaming; gated) are the near-misses; IndicConformer offline Hindi 13.8 / Telugu 26.4 WER; Telugu ~2x harder than Hindi; clean commercial-safe Telugu ~670 h; no Telugu-English corpus; sherpa-onnx has maintained Nemotron support (>= 1.13.5); measured int8 Nemotron RTF ~0.06-0.15 at 560-1120 ms on a Ryzen desktop, no laptop numbers; A10G g5.xlarge ~$1.006/h on-demand, ~$0.43-0.52/h spot.

**A-006. Report written.** A report-writer agent synthesised the notes into `reports/Edge streaming Indic STT pipeline.md` (~8-10k words): decision summary, candidate/lab/disqualified tables, data tiers and mixes, Stages 0-8 with gates, evaluation protocol, deployment, Romanization design, risk register, budget, timeline, conflicts register, 15 open questions. Report conclusion: the critical path is a de-risking spike plus a legal workstream.

**A-007. Delivery and Word version.** Report delivered as `.md`; owner asked for a Word file. `pandoc` and LibreOffice unavailable; produced `.docx` with a custom Markdown->docx script (landscape; 22 pages; 13 tables; 76 hyperlinks); verified structure through Word automation (page/table counts and table widths); could not render page images to inspect visually. Temporary npm packages removed from the session folder.

**A-008. Folder change.** Owner moved the session to `C:\Users\Aarav Gupta\Downloads\10X_STT`; the app copied the 8 session files there (report `.md`/`.docx` and 6 notes). (-> D-013)

**A-009. Q&A: summary, cost, data hours.** Gave a summary of the report plus costs and data hours. Numbers quoted: report budget ~340 GPU-h ~ $341 on-demand / ~$153 spot; planning range ~$300-450 / ~$180-280; MVP data 1,280 h (Hi 550, Te 400, En 280, CS 50); production ~4,200 h (Hi ~1,500, Te ~1,000, En ~1,200, CS ~300). Assistant's own extrapolation (not in the report): three passes over the production mix ~420 GPU-h for main training; whole project ~610 GPU-h, ~$700-800 on-demand / ~$350-400 spot; flagged as unmeasured. Highlighted unpriced items (notably storage: IndicVoices 745 GB).

**A-010. Q&A: MVP-only cost.** Defined MVP as the T1-only 1,280 h mix reaching the MVP gate. Lean MVP: ~275 GPU-h (dropped pseudo-label decoding ~40 h, 2-arm bake-off 60 h instead of 90 h, +5 h data-build) -> ~$276 on-demand / ~$125 spot GPU; + ~$50 TTS + 15% contingency -> **~$370 / ~$195**. Risk: if A10G throughput is half the estimate, add ~$150 on-demand (bad case ~$550-600). Noted memory-fit risk of full FT of 600M on 24 GB (unverified), spot interruptions, and unpriced storage.

**A-011. Q&A: fine-tuning vs distillation.** Clarified: **MVP = fine-tuning**; distillation = production tier (pseudo-labelling from teachers; conditional compression to ~65M/114M). Explained the five-step fine-tune (data prep; Telugu representation + head warm-up; main full fine-tune with multi-lookahead, English replay, bf16/checkpointing; averaging + export) and the two risky points (Telugu tokenizer/prompt step; A10G memory fit). (-> D-007)

**A-012. Q&A: brief pipeline and sherpa-onnx.** Gave a stage table (Stages 0-8) with gates and the four approval points; explained sherpa-onnx (k2-fsa runtime; Apache-2.0 per notes; executes exported ONNX models on CPU without PyTorch; C++ core with Python/Swift/Kotlin/C#/JS bindings; NeMo cache-aware transducer support since 1.12.22/1.13.3; pin >= 1.13.5; separate encoder/decoder/joiner; hotwords need transducer).

**A-013. Created `pipeline.md` and `progress.md`.** `pipeline.md` v1.0 (~1,000 lines, 20 sections): project definition, strategy, architecture + repo layout, infrastructure/ops, Stages 0-9 with steps/outputs/gates/branches, data spec, training spec, evaluation spec, export/deployment spec, Romanization design, pivot tree, risk register, budget (lean MVP / full / production), timeline, approvals, open decisions, unknowns register, glossary, sources. `progress.md` (this file) created with context brief, status snapshot, decision/pivot logs, tracker tables and templates. Status: awaiting senior review (checkpoint 1).

**A-014. Added `CLAUDE.md`.** At the owner's request, created `CLAUDE.md` in the project root. It tells every Claude session to read `progress.md` Sections 1-2 at the start, to update `progress.md` (activity log, status snapshot, ledgers) before finishing, to log a decision before changing `pipeline.md`, to get the owner's explicit go-ahead before spending money or sending anything outward, and to follow the data/licence and native-script rules. (-> D-014)

**A-015. New context from the owner's normal Claude chats (2026-10-12).** The owner pasted a handoff summarising chats held while away (sandbox with no general internet). Stored verbatim in `research_notes/context_from_normal_chats_2026-10-12.md`. Key content: (1) problem statement restated: **three separate monolingual models** (en, hi, te), edge on **phones and laptops**, commercial, licences must allow it; pipeline wanted for senior approval; nothing trained or built. (2) **Compute discrepancy**: 8x A10 24 GB on AWS (owner) vs "dgx level setup with 8 A100s" (senior). (3) **Senior's position (WhatsApp, 9 Oct)**: wants Kyutai's architecture; believes Prasad trained on a consumer RTX with ~120 h; believes "swap in Telugu data" gives a PoC in an hour or two on 8 GPUs; believes an STT release exists in pocket-tts. (4) **Findings from Prasad Vittaldev's LinkedIn posts (screenshots, unverified [V])**: his Kyutai work is **Telugu Pocket TTS** (124 h, 3 voices, 316M params int8, 3.39x RT on 2 CPU cores); his **STT, "Svanita"**, is NVIDIA-based (FastConformer + TDT, ~620M, CC-BY-4.0, 3-second turns so not true streaming; v0.1 Telugu+English; v0.2 Hindi+Telugu with 73-74% English-word retention in Latin script, Hindi WER 23.7% vs 15.5% for IndicConformer, no Telugu numbers or training data stated). The senior merged the two projects. (5) Kyutai STT is en/fr only; README-level check found no STT training code (to verify). (6) Chat's chosen direction matches ours: fine-tune Nemotron-3.5-ASR-Streaming-0.6B with new tokenizer/decoder, sherpa-onnx, int8, but **per language**; 8-step pipeline; draft message to senior (not confirmed sent). **Conflicts with this project's files:** compute (1x A10G was our inherited assumption, see Section 1 caveat); one multilingual model (ours) vs three monolingual (senior); phones vs laptop-only (D-003); streaming "unknown" vs D-002; TTS scope. **New leads:** Svanita (possible Telugu-capable starting point or baseline; licence and data provenance unknown), Prasad's Telugu TTS. Nothing was changed in `pipeline.md` yet; reconciliation is pending the owner's answers to Q17-Q23. No money spent. (-> Q17-Q23)

**A-016. Licence/lead audit, interim results (2026-10-12; 3 of 6 researchers done; 3 still running: AI4Bharat datasets, other datasets, dataset discovery).** Notes in `research_notes/Svanita Kyutai and dataset licence audit/`: `svanita_prasad.md`, `kyutai_repos.md`, `models_tools_licences.md`. All read-only; nothing downloaded, nobody contacted. Researcher findings (not independently re-checked by us):
- **Svanita** is real: `huggingface.co/prasadvittaldev/svanita-0.6b` (the lnkd.in link resolves there; v0.2 = `main`, v0.1 = branch). Fine-tune of `nvidia/parakeet-tdt-0.6b-v3`, ~622M, pure TDT, **offline** (no chunking/cache), new 4,097-piece unigram tokenizer. Data: **IndicVoices + Kathbath only, 1,136 h (Te 451 h, Hi 685 h)**, one RTX 5060 Ti 16 GB, 8-bit AdamW, ~40% telephone augmentation. Tag `cc-by-4.0`; no LICENSE/NOTICE file; fp32 safetensors only; author reports int8 raised WER ~30 points and ONNX export was not faithful. Author's own numbers (unverified): IndicVoices Hindi 23.7 vs IndicConformer 15.5; Telugu 37.7 vs 27.4; Kathbath read speech far worse than IndicConformer. Verdict: **baseline to beat, not a base or teacher.** The LinkedIn post claims "no Telugu numbers / data / hardware" are wrong for the HF card.
- **Prasad's Telugu Pocket TTS** page: `prasadvittaldev/pocket-tts-telugu-female-syspin` (MIT per card): ~110M distilled single-voice student (not the 316M, not 3 voices); teacher fine-tuned on 124 h Telugu, then distilled on 53 h of one speaker; data credited: IndicTTS Telugu (~8.7 h) and a third-party SYSPIN re-upload with no licence; 124 h not fully accounted for.
- **Kyutai:** no STT training/fine-tuning code anywhere in the org (34 repos, 45 branches checked); maintainer 2026-03-23: no plans to release it. **Senior's belief that STT code is in pocket-tts is false** (its `training/` is TTS-only). Kyutai STT = 1B/2.6B, CUDA or Apple MLX only, no Android, no real laptop-CPU path. Kyutai guidance for a new STT language: a few thousand hours of word-aligned data. Pocket TTS training code was released Aug 2026 (recipe `finetune_language.yaml` + distillation); community Hindi (932 h, 647 h, ~90 h) and Telugu builds exist; TTS is feasible in days, not hours. Weights CC BY 4.0 (Pocket TTS gated); some voices from non-commercial datasets; Kyutai's own STT fine-tune mix includes SPGISpeech (non-commercial) and TED-LIUM (BY-NC-ND) so the CC BY label does not settle training-data safety.
- **Nemotron-3.5 licence resolved (U-01):** HF weights are **OpenMDW-1.1** (full text read: no field-of-use limits, no share-alike, outputs unrestricted; duty = keep agreement and notices of origin). Launch-day front-matter said NVIDIA Open Model License; fixed 2026-06-05; NIM-served builds on NGC/Together still use NVIDIA Open Model License. Archive a dated copy at download.
- **Nemotron-3.5 facts (U-02, U-03):** Telugu **not** supported; tokenizer = BPE 13,087 tokens with **zero Telugu characters** (Telugu would be `<unk>`); prompt dictionary reserves `te-IN: 40`; **no CTC head** (RNNT-only); LoRA "not supported now"; NVIDIA gives no GPU spec. **NVIDIA documents a new-language route** (Riva tutorial `asr-extend-tokenizer-to-newlang-ft-acoustic-model.ipynb`: train new tokenizer, merge, `++model.tokenizer.update_tokenizer=true`, which retrains the RNNT decoder from scratch and keeps the encoder); NVIDIA's own toy Malay run reached ~60% WER and says a good decoder needs far more data/steps. **No NVIDIA "few hundred hours" figure exists** (earlier notes cited a vendor FAQ); community reference points: Swahili 382 h -> 29.8% FLEURS WER; Slovenian 858 h -> ~22-33%; AI4Bharat Bhili ~200 h (no WER).
- **Other licences:** Parakeet-1.1B Indic is NGC/NIM-only, bn/en/hi/ta, community licence forbids using outputs to improve other models -> disqualified. Indic Open Model License v1.0 (Bodhan Indic-Transcribe): derivatives must carry the same licence + UI attribution; using it as a teacher pulls our model under it -> avoid. IndicConformer MIT (README/LICENSE/HF cards/AIKosh); one template repo and one GGUF repack say CC-BY-4.0; Hindi/Telugu per-language ~120M models exist, none streaming. ARTPARK models (SraVaani, Vaani-FastConformer): `mit` tag + contact-sharing gate only; commercial terms unconfirmed. Silero VAD is MIT (the "CC BY-NC" text is stale alt text) (U-15); TEN VAD = Apache-2.0 + a non-compete clause against Agora (counsel); Aksharamukha is AGPL-3.0 (do not ship); uroman MIT + acknowledgement; NeMo, Lhotse, SentencePiece, sherpa-onnx, icefall, onnxruntime, WeNet, whisper.cpp etc. Apache-2.0/MIT. MMS and SeamlessM4T CC-BY-NC. A new CPU figure: NVIDIA's NeMo-Speech.cpp English Q8_0 model on an i7-11700K, 8 threads: 27 ms per 160 ms chunk (~6x real time).
- **Blocked, needs the owner's login/browser:** LinkedIn (authwall); HF gate texts for IndicVoices, Kathbath, IndicConformer repos, ARTPARK repos, Bhili, `kyutai/pocket-tts`; IndicTTS licence PDF; NGC Terms of Use; NVIDIA exemption PDF for the NIM rule. Licensor questions are drafted in `models_tools_licences.md` and `svanita_prasad.md`; **none sent**.
- **Implications (pending decisions, nothing changed in `pipeline.md` yet):** D-009 (reject Kyutai for STT) strengthened. Svanita becomes a baseline row in Stage 2, not a base. Nemotron path to Telugu = documented tokenizer extension + decoder retraining; hours needed likely hundreds to ~1k+ per language, not "a few hundred" (R-01 stays High). U-01, U-02, U-03, U-15 can be marked resolved after the final report. Svanita's data (IndicVoices+Kathbath, 1,136 h) shows what one person did on a consumer GPU for an offline model, not for streaming.

**A-017. Licence audit, interim results #2 (2026-10-12; 4 of 6 researchers done; still running: AI4Bharat/IIT-M datasets, dataset discovery).** Note: `research_notes/Svanita Kyutai and dataset licence audit/datasets_other.md` (non-AI4Bharat datasets). Read-only; nothing downloaded, no logins, nobody contacted. Researcher findings (not re-checked by us):
- **New and important for Telugu: RESPIN-S1.0 (IISc SPIRE Lab).** Clean hours: paper Table 3 = Hindi 944.93 h, **Telugu 1,303.98 h**; the GitHub release repo lists train_hi_clean 712.61 h and **train_te_clean 1,021.16 h** (paper and repo differ by ~230-280 h, reason unstated). Read speech (agriculture/finance sentences), crowd-recorded on mobile at 16 kHz, many speakers, 4-5 dialect regions per language; **English words were removed from the text** (so no code-switch value). **Only licence statement found: AIKosh says CC BY 4.0**; the GitHub repo and paper state none -> rated **T2** pending written confirmation. If confirmed, the Telugu supply (previously ~670 h T1 [E]) could grow by roughly 1.0-1.3k h [E], easing R-01. Access form: `spiredatasets.ee.iisc.ac.in/respincorpus` (not read).
- **Vaani hours confirmed exactly**: Hindi 14,923.7 h total / 1,003.78 h transcribed; Telugu 2,326.47 / 184.484; English 336.791 / 22.456. Licence cc-by-4.0 (HF YAML, project site, paper); gate = auto-approve with contact fields and a "use for" select (Research/Academic/Commercial/Education); gate text not exposed by the API. Sibling repos (all cc-by-4.0): Vaani-transcription-part (2,122.20 h, updated 2026-10-08), Vaani-Benchmark-V1.0 (Hindi only, ~10.9 h, 3 references), Atypical-Speech, Noise-Event. Third-party copies carry no licence tag. `sorika-labs/vaani-v3-dataset` is unrelated to IISc Vaani (a Kathbath+FLEURS compilation labelled Apache-2.0). Transcripts write English words as native script plus Latin in braces, e.g. "ट्रक {truck}"; no official splits; 16 kHz mono.
- **Common Voice** latest = v27.0 (cut-off 2026-09-11), CC0-1.0 on Mozilla Data Collective; dataset pages forbid speaker re-identification and re-hosting; new Mozilla terms (May 2026) say synthetic data/model outputs generated from a dataset must not contain personal data and must be disclosed as machine-generated (reach over ASR weights unclear -> ask Mozilla). Hours confirmed: Hindi 15.71 validated / 26.74 total; Telugu 0.94 / 3.2; English 2,826.8 / 3,795.9; "indian" accent bucket (India, Pakistan, Sri Lanka) = 153,048 clips (5.9%), ~224 h [E].
- **FLEURS** (CC-BY 4.0, but transcripts derive from FLORES text under CC-BY-SA 4.0): hi 8.71 h, te 10.26 h, en 10.31 h [E]; **eval only**.
- **SLR103** moved T3 -> T2: licence ID resolves (via a secondary source) to Microsoft's Open Use of Data Agreement v1.0 (O-UDA-1.0), which imposes no restriction on use of Data or distribution of Results (AI models trained on the Data are "Results"); still needs written confirmation of the ID mapping; 8 kHz story audio, low priority. **MUCS Telugu/Tamil/Gujarati and Microsoft Speech Corpus stay T4** ("shall not be used for commercial purposes").
- **DEMAND** conflict confirmed (metadata cc-by-4.0 vs description CC BY-SA 3.0): use the restrictive reading (T2). **RIRS_NOISES** is labelled Apache-2.0 but bundles RWCP (research/development only) and Aachen AIR RIRs: use only the simulated RIRs unless owners confirm.
- **Do not use aggregator relabels:** `agarwalayushi/hinglish` (CC BY 4.0 over 14 mixed-provenance sources), `kapturecx/Chaashini` (Apache-2.0 over unnamed sources; Hindi 1,394.84 h / Telugu 116.25 h / English 240.61 h), `kapturecx/bolAIndia` (All India Radio scrape, no licence tag), `kapturecx/Vartalaap` (non-commercial). GigaSpeech gate = non-commercial research and educational use (binds the employer if for-profit); SPGISpeech = academic and internal use only; Gram Vaani SLR118 = academic, commercial by email; Skit-S2I and CS-FLEURS = non-commercial; CMU Wilderness = cannot redistribute.
- **Other:** NPTEL2020 Indian English (~15,700 h, YouTube-CC crawl with subtitle labels, ~14.5% reference WER vs a hand-checked sample; Zenodo says cc-by-4.0, GitHub has no licence file) = T2. `google/svq` (cc-by-4.0; phone-recorded queries under clean/background-speech/traffic/media noise; Hindi, Telugu and English locales; test split only) = useful for noise-robustness **eval**. SPRING-INX Hindi on AIKosh is CC BY 4.0, no Telugu entry. `SPRINGLab/Hindi-1482Hrs` has no card or licence (T3). SLR66 Telugu CC BY-SA 4.0 (>= 2.49 h verified); SLR104 CC BY-SA 4.0 (89.86 h train, 5.18 h test). Text: Samanantar CC BY-NC 4.0 (T4); IndicCorp v2 CC0 on its HF card; Wikipedia CC BY-SA 3.0/GFDL; mC4/C4 ODC-By + Common Crawl terms; FineWeb-2 ODC-By 1.0; OSCAR-2301 gated and suspended.
- **Not verified by the researcher:** IndicTTS licence text (iitm.ac.in unreachable), IIIT-Hyderabad Telugu challenge data, Kaggle sets, FSD50K/AudioSet/WHAM!/DNS noise licences, MLS English hours, YODAS per-language hours, TED-LIUM licence (search summary only), the two Microsoft licence IDs (host dead).
- **Needs the owner's browser/login:** Vaani gate text (dated screenshot at `huggingface.co/datasets/ARTPARK-IISc/Vaani`), Mozilla Data Collective click-through terms, the RESPIN access form, the IIT Madras IndicTTS licence page.
- **Drafted, not sent (need the owner's go-ahead):** questions to Vaani (`vaanicontact@gmail.com`: gate allows commercial model training? phase 2 in the public repo? benchmark speakers disjoint from training?), IISc SPIRE Lab (RESPIN CC BY 4.0 in writing; the 230-280 h gap), Gram Vaani (SLR118 commercial permission), OpenSLR/Microsoft Research Open Data (text behind the two licence IDs), Mozilla (model-outputs clause vs ASR weights), AI4Bharat (NPTEL2020 subtitle/YouTube-CC rights).

**A-018. Licence audit, interim results #3 (2026-10-12; 5 of 6 researchers done; still running: AI4Bharat/IIT-M datasets).** Note: `research_notes/Svanita Kyutai and dataset licence audit/datasets_discovery_inventory.md`. Read-only; nothing downloaded or sent. Researcher findings (not re-checked by us):
- **Telugu is less binding than the 2026-10-08 notes said, for read speech only.** RESPIN-S1.0 (IISc SPIRE; AIKosh lists CC BY 4.0, "Open"): Telugu train ~1,021 h clean (~1,335 h with noisier slabs), Hindi ~713 h clean (~1,290 h). **Caveat:** those per-language hours came from a README copy in another agent's scratch space, not re-fetched from the original URL; re-check against the original README before adopting. Rated T1-lean (provisional) until someone captures the SPIRE download-form terms. (A-017's researcher quoted 1,021.16 h Telugu clean from the GitHub repo and 1,303.98 h from the paper Table 3; the two sources agree on ~1.0k+ h.)
- **Numo Indic Speech** (Poseidon AI, created 2026-10-02): Telugu 1,224 h, Hindi 1,315 h, CC BY 4.0 on the card, explicitly commercial; read scripted speech; card silent on consent/speakers; Poseidon's privacy policy says submitted recordings "may be licensed to third party AI companies" -> **T2**.
- **Clearly commercial-safe transcribed hours (low / best / high):** Hindi ~1.9k / ~3.1k / ~5.0k (not a constraint; ~2k of best is spontaneous); **Telugu ~0.55k / ~1.9k / ~3.4k** (only ~0.7k of the best case is spontaneous); English-India (Indian accent) ~0.05k / ~0.25k / ~0.35k (train on generic T1 English plus this). "Best" = T1 + RESPIN-clean + SYSPIN + Rasa + HiACC; "high" adds Numo and noisier RESPIN slabs; overlapping re-uploads (IndicVoices-R, Nirantar) excluded. Low figures are the old notes' numbers, unverified. **Spontaneous Telugu diversity is still the binding limit**, so pseudo-labelling Vaani Telugu (~2.1k h untranscribed) stays a lever. NPTEL2020 Indian English (15,700 h YouTube-CC lectures with uploaded subtitles; AI4Bharat) = T2 upside for English; transcripts only assumed corrected. SPIRE-SIES (170.8 h Indian English) is by request form only, no corpus licence stated.
- **Code-switch:** still no large clearly-safe real corpus for either pair. Hindi-English: HiACC (5.24 h, CC BY 4.0, Zenodo 15551669) is the only newly found clearly licensed set; SLR104 (89.9 h, BY-SA) remains the only sizeable one. Telugu-English: the 243 h set from Microsoft Research India's 2020 paper (arXiv 2006.00782) is unreleased; the "200 h, 400 speakers" set traces only to a March 2026 forum post with no owner or licence; CoSTA's 2.3 h Telugu eval set is promised under CC-BY-4.0 but no release found.
- **Unlabeled pools:** Vaani untranscribed (~13.9k h Hindi, ~2.1k Telugu, ~0.3k English) stays the best commercial-safe pool. bolAIndia (Kapture CX) is the biggest at 190k h but licence/source credits are behind the HF gate -> T3 until read.
- **TTS (in case it is in scope):** SYSPIN is the best studio single-speaker set: Hindi ~119 h, Telugu ~115 h, one male + one female voice each, CC BY 4.0 on AIKosh; Rasa adds ~51 h Hindi and ~52 h Telugu (CC-BY-4.0, expressive); Indian-English TTS (SYSPIN/LIMMITS English, 80 h) has no stated licence.
- **Paid route (estimates/vendor claims):** SpeechData.ai lists Telugu 500 h and Hindi 2,000 h at $65/h with signed consent (vendor claim); Defined.ai ~EUR 159/h; CoSTA's own annotation rates INR 3,000-3,500/h; researcher's own all-in guess for new Telugu collection $40-120/h (unsourced) -> far outside a few-hundred-dollar budget.
- **Licence-label traps:** InfoBayAI (tagged cc-by-4.0, card says research/educational only); Kapture Chaashini (Apache-2.0 tag over scraped audio with ASR labels); `projectkaira/Pretraining-V1` (CC-BY tag over data incl. the non-commercial Microsoft corpus); Karya sanmati-stories (non-commercial); Spoken Tutorial (BY-SA on its own site, CC BY on AI4Bharat's copy).
- **Needs the owner's browser:** (1) `huggingface.co/datasets/kapturecx/bolAIndia` STATS.md and gate text; (2) `spiredatasets.ee.iisc.ac.in/respincorpus` download-form terms + per-language hours, and the NeurIPS paper's ethics section; (3) `huggingface.co/datasets/psdn-ai/numo-indic-speech` gate conditions and consent; (4) the SPIRE-SIES request form (optional); (5) NPTEL's own content licence.
- **Open gaps (open data):** spontaneous Telugu beyond ~0.7k h; any real Telugu-English speech; Hindi-English beyond ~5 h clearly licensed; laptop-mic speech.

**A-019. Svanita / Kyutai / datasets / licence audit COMPLETE (2026-10-12).** All six researchers finished; a report writer produced `reports/Svanita Kyutai and dataset licence audit.md` (~12,500 words, 12 sections: executive summary; senior's claims vs evidence; Svanita/Prasad; Kyutai; base models/teachers/tools licence matrix + Nemotron-3.5 deep dive; dataset master matrix, per-language inventories, code-switch, unlabeled pools, TTS data; corrections to earlier docs; implications for the plan [P]; blocked items; 25 draft licensor questions; talking points for the senior; sources). Raw notes: six files in `research_notes/Svanita Kyutai and dataset licence audit/`. Process note: the deep-research skill's `researcher.md`/`report-writer.md` reference files no longer exist on this machine, so later researchers worked from their prompts and the report writer from written instructions. Nothing downloaded, no logins, nothing sent, no money spent, `pipeline.md` unchanged.
- **Headline conclusions (researcher-compiled, not independently re-checked):** Svanita = offline Parakeet-v3 fine-tune on 1,136 h IndicVoices+Kathbath (Te 451 h, Hi 685 h), one RTX 5060 Ti; baseline only. The "Kyutai + consumer GPU + 120 h" story is Prasad's TTS (published as a single-voice ~110M student). **Kyutai has no STT training code anywhere; senior's pocket-tts STT claim is false;** Kyutai STT cannot run in real time on laptop CPUs and has no Android path; Pocket TTS is a credible separate option if TTS is in scope. **Nemotron-3.5 = OpenMDW-1.1**, no Telugu tokens, no CTC head, documented new-language route (decoder retrained from scratch), no NVIDIA "few hundred hours" figure. Avoid as teachers/bases: Parakeet-1.1B Indic, Bodhan Indic-Transcribe, MMS, SeamlessM4T, canary-1b. Clearly licensed transcribed hours (low/best/high): Hindi ~1.5-1.9k / ~3.2k / ~5.1k; Telugu ~0.55-0.7k / ~1.9-2.0k / ~3.4-3.5k (spontaneous only ~0.55-0.7k; the rest is read speech: RESPIN, SYSPIN, Numo, T2); English-India ~0.05k / ~0.25k / ~0.35k. No real Telugu-English corpus released; Hindi-English only HiACC 5.24 h and SLR104 89.9 h (BY-SA).
- **Conflict resolutions the report chose (restrictive reading when unresolved):** RESPIN = T2 (only AIKosh states CC BY 4.0), repo hours Hindi 712.6 / Telugu 1,021.2 clean (paper: 944.9 / 1,304.0); IndicVoices hours range Hindi 0.52-0.84k, Telugu 0.39-0.51k (Svanita's clip counts support the upper end, derived by the writer [E]); IndicVoices-R = CC BY-ND (AIKosh) T2; Kathbath = T2 (consent wording said "research purposes"); SPRING-INX Hindi = T2; Shrutilipi = T3 leaning T4 (All India Radio copyright page); NPTEL2020 = T3 for any commitment; Rural Women ASR v2 (Hindi) = T3.
- **Corrections to earlier notes:** AI4Bharat dataset gates show only HF's default contact-sharing text (not unreadable); AIKosh licence fields are blanket labels (low authority); model-repo gates (IndicConformer, SraVaani, Bodhan, Bhili) remain unread. Resolved unknowns: U-01, U-02, U-03, U-15 (see Section 12 table).
- **New item to verify first:** Svanita says its Latin English targets came from IndicVoices' `native [english]` annotation, but the AI4Bharat audit found no Latin script in the cleaned `text` field; whether the raw `unsanitized_verbatim` field keeps those pairs decides how costly Latin-English recovery is (needs the owner's access to the data or a duration/field check after access).
- **Pending decisions (nothing changed in the plan yet):** per-language models vs one model (Q18), compute (Q17), streaming/devices (Q19/Q20), TTS scope (Q21), sending licensor questions (Q24), browser-only checks (Q25). (-> Q17-Q25)

**A-020. Owner's answers and questions (2026-10-12).** Owner: (1) **"we have 8 a100s"** -> D-015; (2) **three separate monolingual models** -> D-016; (3) asked **what the difference is between streaming and offline** (explained in chat; see below); (4) **has not sent the message to the senior yet and wants more info first**; (5) **unsure about Q24** (sending licensor questions); (6) asked for a fresh summary of the whole project because context was getting lost (provided in chat).
- **Streaming vs offline (explanation given):** *Offline* = transcribe after the person stops (whole clip/utterance; model sees past and future audio; best accuracy; text appears after they finish; e.g. Svanita, IndicConformer, Whisper). *Streaming* = text appears while they speak, in small chunks (80 ms to ~1 s) with limited look-ahead, so ~0.3-1 s delay and somewhat higher error (NVIDIA English LibriSpeech test-other WER: 5.0 offline, 7.5 at 520 ms, 6.3 at 1,360 ms [M]; our working expectation for Indic +15-25% relative [E]). *Utterance-level* (middle option) = wait for a pause, then transcribe that sentence offline; feels near-live with ~1-2 s delay. **Planning consequence:** if the product only needs text after each sentence, an offline/utterance-level model is cheaper and more accurate and opens the **IndicConformer** route (Hindi and Telugu per-language ~120M models already exist, MIT per READMEs; no Telugu tokenizer problem); true streaming forces the Nemotron-3.5 route (Telugu tokenizer + decoder retraining). Needs a product answer from the senior (Q19).
- **8 A100s: implications (our estimates, not measured):** compute stops being the binding constraint; data and licences are. 600M full fine-tunes become comfortable (80 GB cards even more so); the three language models and the bake-off arms can be trained in parallel; per-GPU an A100 is roughly 2-3x an A10G [U, general knowledge], so the MVP's ~275 A10G-hours might shrink to hours-to-a-day or two of wall-clock if scaling is decent [E, very rough]. Dollar cost depends on whether the machine is owned or billed (Q17 follow-up). The one-A10G cost tables in `pipeline.md` are now obsolete for budgeting but still useful as a work estimate. `pipeline.md` has NOT been re-based yet.
- **Message to the senior:** not sent; an updated draft (corrected facts: Svanita = 1,136 h, NVIDIA base; Kyutai STT has no training code; TTS is the Kyutai part; 8 A100s) was provided in chat; talking points also in report Section 11.
- **Q24 (licensor questions):** explained what it means; assistant recommendation: hold, send nothing yet; once the senior approves the direction, route the first four (NVIDIA, AI4Bharat, IISc SPIRE/RESPIN, ARTPARK-IISc/Vaani) through the senior or legal so they come from the company. Owner to decide.
- **Next:** owner answers Q19 (streaming need) with the senior, sends/edits the message; then re-base `pipeline.md` (decisions D-017+).

**A-021. Owner's answers (2026-10-13).** (1) **Offline model confirmed** with the senior -> D-017 (supersedes D-002 true streaming). (2) **STT and TTS are both wanted; STT first** since it is easier -> D-018 (Q21 answered). (3) **A100s are 40 GB** -> D-019. (4) Owner asked for all URLs for the browser audit and exactly what is needed; will paste text or take screenshots. A dated evidence folder `evidence/` was created for them (screenshots/pastes named `YYYY-MM-DD_<source>_<what>`); assistant gave a re-prioritised list for an offline STT-first plan (see chat; full table in the audit report Section 9).
- **Implications (proposals, nothing changed in `pipeline.md` yet):** offline removes the cache-aware/streaming constraints, the sherpa-onnx streaming-specific pitfalls and most of the Nemotron-3.5 streaming rationale; the candidate bases become IndicConformer per-language (hi, te; hybrid CTC/RNNT, ~120M, MIT per READMEs; gate text unread), Parakeet-TDT-0.6B-v3 / v2 (CC-BY-4.0; Svanita precedent for Telugu+Hindi with a new tokenizer), Nemotron/other as encoders if useful; English-India needs its own base (Parakeet-TDT English). 40 GB A100s fit 600M full fine-tunes comfortably (3 languages can train in parallel). The pipeline needs a re-base: Stage 1 spike, bake-off arms, export (offline ONNX/int8; 3 s chunks for long audio via VAD), gates (drop streaming latency metrics), budget (A100s), per-language data mixes (report Section 6) and the TTS phase.
- **Open:** Q20 devices (phones vs laptops; still unconfirmed), Q22 targets, Q23 message to the senior (still unsent), Q24 licensor questions (owner unsure; recommend hold), Q25 browser items (in progress by owner).

**A-022. Browser-pane audit, first pass (2026-10-13).** The owner signed in to Hugging Face in the built-in browser pane; pages were read with no gate accepted, nothing clicked, nothing downloaded. Evidence file: `evidence/2026-10-13_hf_pages_captured_via_browser_pane.md`.
- **Gates (answers Q25 items 1, 3, 5 in part):** all AI4Bharat and ARTPARK-IISc model repos read (IndicConformer hi, te, 600M; SraVaani-1.0; Vaani-FastConformer-Telugu) show only HF's default "share your contact information (email and username)" gate; licence tag **mit** on all. Kathbath shows the same default gate (tag cc-by-4.0; body says CC0 packaging, text from crawled IndicCorp). IndicVoices and Vaani showed no gate box in this session (cause unknown). No custom conditions text exists on any repo read.
- **IndicConformer per-language hi/te:** conformer-Large encoder ~120M params, 17 blocks, dim 512, hybrid CTC-RNNT; requires AI4Bharat's NeMo fork (`nemo-v2` branch) to fine-tune. **The 600M card now recommends "Indic-Transcribe" as better** (its Indic Open Model License v1.0 was flagged restrictive in the audit); IndicConformer itself remains MIT.
- **SraVaani-1.0:** ~430M, hybrid TDT-CTC, 65 languages; fine-tuned on ~31,270 h from Vaani **plus "multiple open-source speech datasets" (unnamed)**, so its training-data licence chain is unknown; usage needs a token and `trust_remote_code`. Vaani-FastConformer-Telugu: RNNT BPE NeMo model, trained on Vaani; no size, WER or hours on the card.
- **IndicVoices (answers Q25 item 5 in part):** columns confirmed (`text`, `verbatim`, `normalized`, `unsanitized_verbatim`, `unsanitized_normalized`, plus metadata). In the visible **Assamese** rows, **English words survive as `native [english]` pairs in `unsanitized_normalized`** (and noise tags like `[uhh]`), but not in `text`/`verbatim`/`normalized`. **Hindi and Telugu rows could not be viewed** (viewer timeouts), so this is unconfirmed for our languages; the README shows Hindi 445,160 train + 5,530 valid rows, Telugu ~269k train + ~3.3k valid. Latin-English recovery via `unsanitized_normalized` is plausible, pending a check on Hindi and Telugu rows.
- **Still open:** exact hour totals (viewer does not show them), Numo, bolAIndia, RESPIN form, Mozilla terms, IndicTTS PDF, pocket-tts gate, LinkedIn. Q25 stays open.

**A-023. Browser-pane audit, second pass (2026-10-13).** Same method (read only; nothing accepted, submitted or downloaded). Evidence appended to `evidence/2026-10-13_hf_pages_captured_via_browser_pane.md`.
- **Numo Indic Speech (Poseidon AI):** the gate itself says "free to use under CC BY 4.0, including commercially" (answers part of Q25 item 4). Gate form asks full name, work email, organization, consent to Poseidon's privacy policy. 3,845.5 h read, scripted, single-speaker speech: **Hindi 1,314.6 h, Telugu 1,224.2 h** (also Bengali 745.1, Tamil 561.6). Card says it "retains code-switching and commonly used English terms" in the prompts; **how English is written (Latin vs native script) is unknown**. Privacy notice (updated 2026-08-26): contributors are told "Content you submit may be licensed to third party AI companies" for model training, and are paid via blockchain wallet; this informs contributors but does not prove consent to an open CC BY release. Remains T2.
- **bolAIndia (Kapture CX):** no licence shown; gate is an access *request*; files listable but not readable; README (102 kB), STATS.md, MAP.md exist but are gated; 190k h claimed (Hindi 89.8k h, Telugu 9.0k h, English 10.0k h; transcripts include automated annotations not human-verified). **Source credits and usage conditions still unknown: T3, do not train.**
- **RESPIN page could not be read:** it is a React app whose scripts are blocked inside the pane (`ERR_BLOCKED_BY_CLIENT`), so it renders blank. **Needs the owner to open it in their own browser and paste the text** (terms, licence, per-language hours, form fields); do not submit the form without a decision.
- **Still open (Q25):** RESPIN text (owner), IndicVoices Hindi/Telugu rows (viewer timeouts), Mozilla terms, IndicTTS PDF, pocket-tts gate, LinkedIn.

**A-024. RESPIN README supplied by the owner (2026-10-13).** The owner pasted the README text and a page screenshot from IISc's site (evidence: `evidence/2026-10-13_RESPIN_readme_and_page_pasted_by_owner.md`). Findings (primary source, official site):
- **Licence statement found (resolves the AIKosh-only gap):** "the copyright in the ASR data belongs to Indian Institute of Science, Bengaluru and the said ASR data is released or distributed under CC-BY-4.0". Collected and curated by **Navana Tech**; funded by the Gates Foundation; contact `contact.respin@iisc.ac.in`. Licence tier upgrade proposed: **T1 for the licence** (official README states CC-BY-4.0); **speaker consent/privacy (DPDP) is not addressed in the README** and the original recording-consent wording is still unread.
- **Hours (README table, [M]):** Telugu clean **1,021.16 h**, seminoisy 186.10 h, noisy 127.66 h, small 155.89 h, dev 2.30 h; Hindi clean **712.61 h**, seminoisy 273.27 h, noisy 304.55 h, small 128.47 h, dev 2.21 h. All Telugu slabs sum to 1,490.81 h and all Hindi slabs to 1,418.90 h **if the "small" slab does not overlap the others (unverified)**. This matches the repo figures from earlier research (not the paper's 1,303.98 h Telugu clean).
- **Nature of the data:** read speech, 2 domains (Agriculture and Banking/Finance), 16 kHz 16-bit mono WAV, average 5.18 s, 2,287 Telugu speakers and 2,305 Hindi speakers in the clean slabs, 4-5 dialects per language. **Text diversity is very low:** Telugu clean has ~19,978 unique sentences for 702,883 utterances (each sentence is read ~35 times); Hindi clean ~19,345 sentences for 574,544 utterances. Inference [E]: RESPIN adds acoustic/speaker/dialect diversity but little language diversity; cap repeats per sentence and don't let it dominate the mix. In the Bengali sample, English loanwords are written in native script (Hindi/Telugu convention unverified), so Latin-English output would need a lexicon pass, same as IndicVoices.
- **Size [E, arithmetic]:** 16 kHz 16-bit mono is ~115 MB/hour, so Telugu clean is ~118 GB and the whole 10k h corpus ~1.1 TB.
- **Not captured:** the Download, Dataset Download info (how to get the files, any form) and Dataset Models Info tabs (IISc may list baseline models and their licences). Requested from the owner.
- **Effect on data position:** RESPIN is now a licence-clean source of ~1.0k h Telugu and ~0.7k h Hindi read speech, but with narrow text; spontaneous Telugu is still the shortage.

**A-025. IndicVoices hours/English check: viewer route failed, paper checked instead (2026-10-13).** The owner could not run queries in the HF SQL console and the viewer for the large Hindi/Telugu splits kept timing out (the SQL console's `train` splits appeared unavailable: crossed-circle chips; the `valid` route was not completed). I read the IndicVoices paper (arXiv 2403.01926, HTML) in the pane instead: it uses a **two-level transcription** (Level 1 verbatim as spoken; Level 2 standardised to textbook form), deliberately collects **code-mixed** prompts (e.g. MASSIVE utterances translated with code-mixing; digital-payment prompts), and uses Silero VAD segmentation; **it does not (in the passages found) describe the `native [english]` bracket convention**, which is only evidenced by the Assamese rows seen on the HF viewer. Paper Table 6 (speakers/hours per split) was extracted but its columns are ambiguous (row `hi | 287 | 65 | 63 | 5 | 1`), and it describes an older snapshot (7,348 h), so **no reliable hour totals were obtained**. Working estimate stays [E]: Hindi ~0.8k h and Telugu ~0.5k h (row counts 451k and 273k x ~6.5 s per clip, the clip length implied by Svanita's card). **Decision: do not block on this.** Exact hours, the read/spontaneous split and the Hindi/Telugu bracket check move to Stage 0/3, to be done after the owner is authorised to download (e.g. a small script run in the owner's own terminal after their own `hf auth login`, reading only the duration and `unsanitized_normalized` columns). Q25 item 5 stays open at low priority.

**A-026. Pipeline re-based (interim) before the owner's call with the senior (2026-10-13).** Added a **Revision Notice v1.1** at the top of `pipeline.md` summarising the re-base (offline, three monolingual models, 8x A100 40 GB, STT first then TTS; per-language bake-off arms Parakeet-TDT with a new tokenizer vs IndicConformer-120M with Latin added; RESPIN/Numo/bolAIndia status; offline gates; phases S0-S10). **The body of `pipeline.md` is NOT rewritten and still describes the streaming/Nemotron/A10G v1.0 plan; the notice overrides it.** Proposed (not decided): D-020 = per-language offline bake-off arms as above. A full stage-by-stage rewrite is the next task. Gave the owner a briefing for the call with the senior: proposed pipeline, caveats, why not Kyutai (no STT training code; maintainer statement 2026-03-23; en/fr only; 1B/2.6B CUDA/MLX only; no CPU/Android path), the Prasad/Kyutai mix-up (Kyutai = Prasad's Telugu TTS; Svanita STT = NVIDIA Parakeet-TDT-v3, 1,136 h, offline), and questions to ask the senior (devices, accuracy targets, TTS timing, licence approval and who sends licensor questions, compute ownership/sharing, timeline). Owner has not yet sent the earlier message to the senior (Q23); the call replaces it.

**A-027. New constraints: tight budget, 3 weeks (2026-10-13).** The owner said the budget is very tight and there are only 3 weeks. Proposed 3-week cut-down (not yet agreed): STT only (no TTS); Hindi and Telugu fine-tuned from IndicConformer-120M (no Parakeet bake-off unless time remains); English = off-the-shelf Parakeet-TDT measured on Indian-accent test sets, retrained only if clearly weak; T1-licence data only (IndicVoices, Vaani, RESPIN capped, Common Voice; SPRING-INX if confirmed) and no waiting for licensor replies; no paid data, no pseudo-labelling; a small in-house test set (~1 h per language from colleagues) plus public test sets; Latin-English only if the senior requires it (Q10). Week 1 setup, spike, gates, subset downloads, baselines; week 2 data prep and training; week 3 pick best, sherpa-onnx test, demo, report. Deliverable is an **internal demo/evidence package, not a commercially cleared release** (licence confirmations cannot finish in 3 weeks). Risks: AI4Bharat NeMo fork setup, data download volume (IndicVoices full archives ~150 GB Hindi and ~141 GB Telugu; RESPIN Telugu clean ~118 GB [E]), Telugu accuracy, unconfirmed licences, GPU ownership/sharing unknown.

**A-028. Compute is RENTED on AWS; 3-week plan costed (2026-10-13).** Owner: "the compute is all rented, we are using aws" (corrects the earlier assumption that the 8 A100s are owned; Q17 follow-up answered: billed). Price check (third-party aggregators, not AWS's own page; us-east-1; verify before budgeting): **p4d.24xlarge (8x A100 40 GB) ~ $21.96/h on-demand** (~$2.75 per GPU-hour; running it 24/7 for 3 weeks = ~$11,000), spot roughly $8-16/h but volatile; **g5.2xlarge (1x A10G, 8 vCPU, 32 GiB) $1.212/h; g5.12xlarge (4x A10G) $5.672/h (~$1.42 per GPU-hour); g5.48xlarge (8x A10G) $16.288/h**; g5 spot about half or less. Sources: doit.com/compute/spot/us-east-1/{p4d.24xlarge,g5.2xlarge,g5.12xlarge,g5.48xlarge}, calculator.holori.com. **Plan implication:** the 120M IndicConformer models do not need A100s; rent small GPU instances in bursts, never leave a big instance idle. Estimated cost of the 3-week plan [E, throughput unmeasured, ~2x uncertainty]: core training/eval ~255 A10G-equivalent GPU-hours (~$310-360 on-demand), optional English fine-tune of a 600M model +~80 GPU-hours (~+$100-115), a dev/prep box ~120 h (~$145), storage ~1 TB for 3 weeks (~$60 [U, general AWS pricing]), 25% contingency; **expected total ~$650 (range ~$500-1,000), roughly half that if training runs on spot (with interruption risk)**. AWS GPU vCPU quota requests should be filed on day 1 [U, general knowledge]. Open: region, spot acceptable?, existing company savings plans, who files quota requests.

**A-029. Budget too high; cheaper plan explored (2026-10-13).** Owner: ~$650 will not be approved by the senior; asked if free Colab and CPU could cover Hindi and Telugu. Assessment given (estimates, free-tier limits from general knowledge [U]): CPU-only training is not viable; free Colab T4 (16 GB, no bf16, session limits, ~100 GB disk) is enough for the **spike** (baselines, export test, tracer fine-tune) but too small for the full ~255 GPU-hour plan; Kaggle's free weekly GPU quota may stretch to a reduced plan but is fragile. **Proposed lean plan:** free tier for the spike; then a reduced main run (~300 h per language, ~6 epochs, 2 variants each, ~70 A10G-equivalent GPU-hours) on AWS spot (~$0.43-0.52/h for g5.xlarge per earlier snapshots) or a cheap GPU marketplace, no dev box, shut down when idle: ~$50-150 [E]. Decision pending the owner/senior. Nothing else changed.

**A-030. 3-week lean plan written (2026-10-13).** Created `pipeline_3week_lean.md` (Plan v2): scope (internal demo and evidence package, not commercially cleared), what was cut vs the older plan, models (IndicConformer-120M Hindi and Telugu; English shootout between Parakeet-TDT v2/v3, Whisper small/medium, Moonshine, a ~110M NVIDIA English model, licence unchecked), data (~300 h per language: Hindi = IndicVoices 120 + Vaani 100 + RESPIN 65 + Common Voice 15; Telugu = IndicVoices 130 + Vaani 120 + RESPIN 50; no ambiguous-licence sets), test sets (FLEURS, Vaani-Benchmark, Lahaja, google/svq, Svarah, own ~1 h per language), a day-by-day schedule with Gates A (export parity), B (tracer fine-tune exports), C (beats baseline by >= 10% relative on in-house and noisy sets, <= 5% relative loss on clean FLEURS; proposals), 4 training runs (2 languages x 2 variants), costs (~70 GPU-hours, ~$50-150 [E]), licence handling, risks and fallbacks, and the decisions needed. Added a pointer notice at the top of `pipeline.md` (the older plan is otherwise unchanged). Nothing started; awaiting senior approval and answers to Q10, Q20, Q22, RESPIN Download tab, AWS region/spot, HF account.

**A-031. Owner sent the message; senior chose native-script output (2026-10-13).** The owner sent the refined message (drafted in chat) to the senior (Mani) after the call was missed (Q23 answered: sent). The senior was impressed and said to focus on **"v1": English words also appear in native script** (D-023). Effects (applied to `pipeline_3week_lean.md`): Variant 2 (Latin letters, tokenizer extension, bracket-pair extraction, frozen-encoder warm-up) is dropped; vocabulary unchanged so the model exports like the original (lower export risk); the tracer fine-tune now just proves a fine-tuned checkpoint exports; training is 2 core runs (1 per language) plus 2 optional second runs with a different learning rate or augmentation; **GPU work falls from ~70 to ~37-61 GPU-hours (~$16-32 spot, ~$37-74 on-demand), total ~$35-110, about $100 or less in most cases [E]**; the $100 figure told to the senior still holds. New evaluation caveat: loanword spelling variants in native script (e.g. कंप्यूटर / कम्प्यूटर) inflate WER, so report with and without spelling-variant folding and use the multi-reference Vaani-Benchmark for Hindi. Saved GPU-hours can go to the optional second runs, extra data, or fine-tuning English if the shootout shows it is weak. Still open: digits and punctuation/casing policy, devices, targets, AWS region/spot, HF account, RESPIN Download tab.

**A-032. STT paused; project reorganised into `stt/` and `tts/` (2026-10-14).** The senior needs TTS work immediately, so the STT workstream is **paused at the planning stage**: nothing was trained, no money spent, no licensor message sent, the lean 3-week plan (`pipeline_3week_lean.md`) is written and logged but not started. Verified all 22 project files were on disk, then moved everything STT into `stt/` (21 files: `progress.md`, `pipeline.md`, `pipeline_3week_lean.md`, `reports/`, `research_notes/`, `evidence/`) and left `CLAUDE.md` at the root (rewritten for the two-folder layout). Created `tts/` with its own `progress.md` and a carry-over note of the TTS findings from this STT research. **Paths inside this file and the plans are relative to `stt/`** (for example `reports/...`, `evidence/...`). **Nothing is backed up beyond the local disk and there is no version control** (offered `git init` and a zip backup). **To resume STT:** see the status snapshot above and `pipeline_3week_lean.md` Section 9 (decisions needed: AWS region/spot, digits and punctuation policy, devices, accuracy targets, HF account, RESPIN Download tab) and the Day 1-5 steps (access, export test, baselines, own test set, tracer fine-tune).

*(Append new entries below this line. Format: `A-0NN. <title>.` then what was done, what was observed, what it means, links to run/decision IDs.)*

---

## 15. Templates

**Activity entry**
```
A-0NN. <short title>  (YYYY-MM-DD)
What we did:
What we observed (numbers WITH conditions):
What it means / next:
Links: RUN-####, BM-###, D-###, P-###, U-##, L-##
```

**Decision entry (add a row in Section 4)**
```
D-0NN | date | decision | alternatives | rationale/evidence | status (Confirmed/Proposed/Superseded/Reversed)
```

**Pivot entry (add a row in Section 5)**
```
P-0NN | date | from | to | trigger and evidence (numbers) | impact on plan/budget/timeline | decision ref
```

**Run card (`runs/RUN-####.md`)**
```
RUN-####   Date:   Stage:   Arm:   Purpose:
Base checkpoint (hash):          Dataset manifest (hash):
Config file + hash:              Git commit:
Software: NeMo / PyTorch / CUDA / sherpa-onnx / ORT versions:
Hardware: instance type, on-demand or spot, region, image ID:
Key hyperparameters: LR(enc/head), batch_duration, grad-accum, precision, att_context_size set,
                     sampling temperature, augmentation, epochs/steps, FastEmit/CTC weight:
Throughput (audio-h per GPU-h):   Peak GPU memory:   GPU-hours:   Cost:
Interruptions/resumes:
Dev metrics (per language, fp32 and int8 if applicable, chunk size): WER / CER / CS-token WER
Latency/edge metrics (if applicable): BM-### refs
Observations (what went wrong/right, anomalies):
Decision taken:  (link D-###)
```

**Stage-gate record (paste into Stage tracker notes and Activity log)**
```
Stage N gate, date:
Criterion | target | measured | pass/fail
...
Decision (proceed / pivot / stop), approver:
```

**Session close checklist**
- [ ] Activity entry appended
- [ ] Status snapshot refreshed (including Next actions)
- [ ] Budget ledger updated (GPU-h and $)
- [ ] Run registry / benchmark registry updated
- [ ] Data ledger updated (hashes, gate texts)
- [ ] Legal tracker updated
- [ ] Unknowns/open questions updated
- [ ] `pipeline.md` updated only via a logged decision, with version bump
