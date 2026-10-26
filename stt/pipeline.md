# 10X_STT: End-to-End Pipeline for an Edge-Deployable Streaming Hindi / Telugu / English STT

| | |
|---|---|
| **Document** | `pipeline.md` (the PLAN) |
| **Version** | 1.0 |
| **Date** | 2026-10-08 |
| **Status** | PROPOSED. Not yet approved by seniors. No stage has started. |
| **Companion file** | `progress.md` (the LOG: what we actually did, decided, changed) |
| **Evidence base** | `reports/Edge streaming Indic STT pipeline.md` (+ `.docx`) and `research_notes/Edge streaming Indic STT pipeline/*.md` |

> ## NEWER PLAN (2026-10-13): see `pipeline_3week_lean.md`
> A **3-week, low-cost plan** (about $50-150) is written in **`pipeline_3week_lean.md`** and is **likely to be the plan we use**, because the owner confirmed a very tight budget and only 3 weeks (D-021, D-022). **This file is the older, larger plan. It is kept unchanged below for reference and has not been overwritten.**
>
> ## REVISION NOTICE v1.1 (2026-10-13): READ THIS FIRST. It overrides the older text below where they conflict.
> The body of this file (v1.0, written 2026-10-08) still describes ONE multilingual, STREAMING model on ONE A10G, based on Nemotron-3.5. Since then the owner confirmed: **(D-015/D-019) 8x A100 40 GB; (D-016) three separate monolingual models (Hindi, Telugu, English-India); (D-017) the STT is OFFLINE; (D-018) STT first, TTS afterwards.** A full rewrite of the stages is still pending; this notice is the interim re-base (**PROPOSED, not yet approved by seniors**):
> - **Offline replaces streaming.** Drop cache-aware training, multi-lookahead, streaming-latency gates and the Nemotron-3.5 rationale (it is streaming; no Telugu tokens). Long audio is handled by VAD segmentation (utterances of roughly 30 s or less) in the application layer.
> - **Per-language bases (bake-off arms, one set per language):** **Arm A** = NVIDIA Parakeet-TDT-0.6B (v3 or v2; CC-BY-4.0) fine-tuned with a NEW tokenizer holding native script plus Latin pieces (the recipe Svanita used: decoder and joint re-initialised, encoder kept). **Arm B** = AI4Bharat IndicConformer per-language ~120M (Hindi, Telugu; MIT per READMEs; hybrid CTC/RNNT; needs AI4Bharat's NeMo fork) with the tokenizer extended or replaced so it can emit Latin-script English (its per-language vocabularies are native-script only). English-India: Parakeet-TDT English (v2) fine-tuned for Indian accents. Baselines to re-measure: IndicConformer, Svanita. Avoid as bases/teachers: Parakeet-1.1B Indic, Indic-Transcribe, MMS, Kyutai (see audit report).
> - **Compute:** 8x A100 40 GB (owned or billed unknown): full fine-tunes of 120M-600M models are comfortable; language arms and bake-off arms can run in parallel. The one-A10G GPU-hour and dollar tables below are obsolete for budgeting (keep as work estimates). Real critical path = data access and licences, the private test set, Latin-English handling, and evaluation, not GPU time.
> - **Data (per language, see `reports/Svanita Kyutai and dataset licence audit.md` Section 6):** RESPIN licence now confirmed CC-BY-4.0 by IISc's README (Telugu clean 1,021 h, Hindi clean 713 h; read speech with only ~20k unique sentences per slab, so cap repeats). Numo (Telugu 1,224 h, Hindi 1,315 h) says "free to use under CC BY 4.0, including commercially" but contributor consent is unclear (T2). bolAIndia is T3 (no licence shown, conditions locked). IndicVoices Hindi/Telugu hours are still estimates (~0.8k / ~0.5k h [E]) and whether Hindi/Telugu rows keep `native [english]` pairs in `unsanitized_normalized` is unverified (seen only in Assamese). Telugu-English and real Hindi-English code-switch data do not exist openly: mine, splice and synthesise.
> - **Gates:** replace the streaming/latency gates by offline accuracy gates relative to re-measured baselines (proposal: MVP within 1.3x of IndicConformer per language on our private test set, production within 1.15x), plus hallucination, script-fidelity, int8-vs-fp32 and CPU speed/size gates for the target devices (devices still unconfirmed, Q20).
> - **Phases:** S0 governance; S1 spike (days, not weeks: baselines, tokenizer test, export/int8 test, 20 h tracer fine-tune per language, A100 throughput); S2 eval harness and private test set; S3 data build; S4 bake-off per language; S5 main training; S6 export and device tests; S7 eval gate; S8 packaging; S9 production track (pseudo-labelling with permitted teachers, T2 decisions, distillation to a smaller model if devices need it); **S10 TTS phase** (Kyutai Pocket TTS is the leading open starting point, to be assessed after STT).
> - **Open decisions:** Q20 devices, Q22 accuracy targets, Q24 licensor questions, Q25 browser checks, Q23 senior's reply.

**Rules for this document**
1. `pipeline.md` says what we *plan* to do. `progress.md` says what we *did*. Never mix the two.
2. Any change to this plan (a threshold, a model, a stage, a dataset) needs a decision entry in `progress.md` (ID `D-###`) *before* this file is edited, and this file's version number goes up.
3. Every number carries an evidence label. If a number has no label, treat it as unverified.

**Evidence labels used everywhere**

| Label | Meaning |
|---|---|
| **[M]** | Measured and published by a cited source, under *their* setup. Not our result. |
| **[V]** | Vendor or self-reported claim. Unverified. |
| **[E]** | Our estimate or extrapolation. Must be validated (most are validated in Stage 1). |
| **[P]** | Our proposal: a threshold or design choice we are free to change via a logged decision. |
| **[U]** | Unverified / not retrieved / from general knowledge. Must be checked before relying on it. |

---

## 0. TL;DR

- **Goal:** a post-trained, **true-streaming** STT for **Hindi, Telugu and English (incl. Hindi-English and Telugu-English code-switching)** that runs faster than real time on **laptop/mini-PC CPUs** (x86 and Apple silicon), for a **commercial** product, using **open data only**, trained on **one AWS A10G (24 GB)** with a **few-hundred-dollar** budget.
- **Method:** **fine-tuning**, not distillation, for the MVP. Distillation (pseudo-labelling and, conditionally, model compression) is a production-tier add-on.
- **Primary base model:** **NVIDIA Nemotron-3.5-ASR-Streaming-0.6B** (cache-aware FastConformer-RNNT, Hindi supported, Telugu NOT supported, commercial-use statement on card).
- **Fallbacks:** (B) ~114M cache-aware NeMo hybrid FastConformer with a new Hindi/Telugu/English tokenizer; (C) SraVaani-0.5-live continuation (only if ARTPARK grants fine-tune-capable weights and written commercial terms); (D) small icefall Zipformer distilled from the winner.
- **Runtime:** int8 ONNX through **sherpa-onnx >= 1.13.5** on CPU.
- **No existing checkpoint meets every constraint.** This is a real post-training programme with failure risk. A 1-2 week **spike (Stage 1)** decides whether Path A is viable before real money is spent.
- **Binding constraint = data, not compute.** Clean commercial-safe transcribed Telugu is only ~670 h [E]. No open Telugu-English code-switch corpus exists.
- **MVP cost:** ~275 A10G GPU-hours, ~$370 on-demand / ~$195 spot [E], excluding storage, test-set annotation, engineer time, legal.
- **Timeline:** ~16 weeks, Stages 0-8, with four approval checkpoints.

---

## 1. Project definition

### 1.1 Goal
Ship an STT model + runtime bundle that a laptop application can load and use for live dictation/captioning in three languages, transcribing code-switched speech in native script (English words in Latin script), with an optional deterministic Romanization layer.

### 1.2 Requirements (confirmed by the user on 2026-10-08)

| ID | Requirement | Source | Consequence for design |
|---|---|---|---|
| R1 | **True streaming**: text appears while the person is still speaking | User answer | Only cache-aware streaming architectures qualify. Offline models (IndicConformer, Whisper, Omnilingual) are demoted to teachers/baselines. |
| R2 | **Target device: laptop / mini-PC CPU** (x86 and Apple silicon) | User answer | ~600M parameters is feasible; int8 CPU inference; no GPU at runtime. |
| R3 | **Commercial product, open data only** (no proprietary audio) | User answer | Every dataset/model licence must be checked. Tiering T1-T4. No NC / research-only data. |
| R4 | **Languages:** Hindi, Telugu, English (Indian accents), code-switching | Original brief | Telugu is the hardest and least-resourced. |
| R5 | **Compute:** one AWS A10G (24 GB), few hundred dollars | Original brief | No pre-training. Post-training only. Compute estimates must be measured early. |
| R6 | **Romanized output is NOT a must** | User answer (reason unconfirmed) | Train on native script. Romanization = optional deterministic post-process layer, never a training target. |
| R7 | Use existing architectures; focus on post-training | Original brief | Fine-tune a released checkpoint. |
| R8 | Pipeline must be approved by seniors before building | Original brief | Four approval checkpoints (Section 15). |

### 1.3 Explicit non-goals
- Pre-training any model from scratch.
- Training on Romanized transcripts (the original AI-generated blueprint did; we rejected it, see 2.4).
- Using proprietary/in-house audio (none available). In-house audio is used **only** for the private *test* set.
- GPU inference at runtime. Cloud APIs as teachers (ToS risk).
- Mobile/Raspberry-Pi targets (not requested; a smaller model arm exists if this changes).

### 1.4 Success definition
- **MVP:** passes the MVP gates in Section 8.6 on the private test set, streaming, int8, on the named lowest-spec laptop. (Hindi + English slices + hallucination + edge gates must pass; Telugu within +10% of its gate.)
- **Production:** passes the production gates, including Telugu, code-switch and telephony slices.
- **Scope option for seniors:** Hindi + English as GA, Telugu as beta (Telugu streaming floor is ~30 WER [M] and only ~0.7k clean T1 hours exist).

### 1.5 Assumptions NOT yet confirmed (each must be closed by a decision entry)

| ID | Assumption | Needed by |
|---|---|---|
| A1 | Default chunk size 320-560 ms (first-token P90 <= 800 ms for MVP) | Stage 1 |
| A2 | A "lowest-spec target laptop" will be named (one x86 U-series, one Apple M-series) | Stage 1 |
| A3 | Telugu is GA vs beta | Before Stage 4 |
| A4 | Punctuation/casing policy for Indic output | Stage 3 |
| A5 | Latin for English words, native script for Indic words, ASCII digits | Stage 0 |
| A6 | Tokenizer strategy (extend vs replace; small aggregate vs shared BPE) | Stage 4 |
| A7 | Budget and owner for recording/annotating the in-house test set | Stage 2 |
| A8 | On-demand vs spot, A100 for batch decoding | Stage 1 |

---

## 2. Strategy: what we are doing and why

### 2.1 Fine-tuning (MVP) vs distillation (later)
- **Fine-tuning (the MVP method).** Start from Nemotron-3.5 (already knows speech, Hindi, English, and already streams). Continue training on our Hindi/Telugu/English/code-switch data so it adds Telugu and Indian-accent robustness. Needs no teacher and no unlabeled audio.
- **Distillation (production tier only), two forms:**
  1. *Pseudo-labelling / noisy student:* IndicConformer-600M + SraVaani-1.0 transcribe Vaani's unlabeled audio; filtered transcripts become extra training data (~1,200 h in the production mix). This is teacher-labelled self-training, not shrinking a model.
  2. *Compression (conditional):* if the 600M model is too slow on the weakest laptops, distil into a ~65M Zipformer or the 114M NeMo model.

### 2.2 Candidate chain

| Path | Model | Role | Why / risk |
|---|---|---|---|
| **A (primary)** | Nemotron-3.5-ASR-Streaming-0.6B | Base for post-training | Only candidate with native cache-aware streaming (80-1120 ms), Hindi supported, public fine-tune recipe, maintained sherpa-onnx loader, commercial-use statement. **Risk:** Telugu not supported; tokenizer/prompt-table extension undocumented; licence text unread. |
| **B (fallback 1)** | ~114M cache-aware NeMo hybrid FastConformer (EN checkpoint) + new aggregate hi/te/en tokenizer | Arm B in bake-off | ~4-5x cheaper on CPU, ~5x cheaper to train [E]. **Risk:** English-only pretraining; a Thai precedent used ~10k h to retarget it. |
| **C (fallback 2)** | ARTPARK-IISc SraVaani-0.5-live (~430M, CTC-only, Hindi+Telugu streaming) | Continue training only if access + written terms | **Risk:** gated, CTC-only (no hotwords), TorchScript fp16, no ONNX. Also the key streaming Telugu baseline to beat. |
| **D (floor)** | icefall streaming Zipformer ~65M | Last resort / distillation student | Best CPU tooling, no Telugu checkpoint. |
| **Teachers (not deployed)** | IndicConformer-600M, SraVaani-1.0 | Pseudo-labels, offline reference | MIT-tagged but gated; output-use terms unverified. Not Whisper-large-v3 (Telugu script collapse). |

### 2.3 Disqualified (and why)

| Option | Reason |
|---|---|
| MMS-1B-all | CC-BY-NC 4.0; ~1B; not streaming |
| Whisper (any size) as base | Not natively streaming; no Indic streaming benchmark; Telugu script collapse / WER > 100 [M, third party] |
| WhisperRT / CarelessWhisper | CC BY-NC 4.0 |
| Voxtral Mini 4B Realtime | ~4.4B params, GPU/vLLM, no Telugu |
| Qwen3-ASR 0.6B/1.7B | No Telugu; GPU-serving oriented |
| Kyutai stt-1b-en_fr / stt-2.6b-en | English/French only; GPU/CUDA; no new-language training code; trained on 2.5M h with 48 H100 |
| Parakeet-TDT-0.6B-v3 / Canary-1B-v2 | 25 European languages; no Hindi/Telugu |
| Parakeet 1.1B Indic | 1.1B; bn/en/hi/ta only; no Telugu; community licence |
| Indic-Transcribe Core/Flex | 1.2B, offline (<=30 s windows), custom licence unread |
| Omnilingual ASR (as deployed model) | Not streaming; <40 s inputs; fairseq2; contradictory accuracy evidence |
| Moonshine | English-only commercial models; non-English legacy models non-commercial |
| Granite Speech, SenseVoice, FireRed | No Hindi/Telugu evidence |
| Sarvam, Gnani, Krutrim, Gemini, Deepgram | API-only; no weights; ToS risk as teachers |

### 2.4 Why the original AI-generated blueprint was dropped (context for anyone who sees it)

The first plan (Parakeet/IndicConformer "FastConformer-TDT", frozen encoder, Romanized IndicXlit targets, Kyutai rejected) had these problems:
1. **Parakeet is not Indic.** v3 covers 25 European languages; v2/110M are English-only. "Already trained on Indian acoustics" was false for Parakeet. A frozen encoder that never heard Telugu cannot learn it in the decoder.
2. **Romanized training targets are noisy.** No canonical Roman spelling; IndicXlit is probabilistic; English words in Devanagari are mangled; WER becomes meaningless. Fix: native script in training, deterministic Romanization at output.
3. **"Freeze the encoder, -70% memory"** was unsupported; full fine-tune is feasible on 24 GB for 120M-600M models in bf16. We use staged freeze-then-unfreeze.
4. **TDT speeds the decoding loop, not the encoder** (which dominates compute), and Parakeet-TDT is offline. "Low-latency edge" needs a cache-aware streaming model.
5. **100-200 h is thin** for three languages + code-switching; Kathbath is read speech, Shrutilipi is broadcast. IndicVoices/Vaani are the right core.
6. **Licences were not checked** (conflicting labels; underlying scraped audio/text).
7. **Export is not a given.** IndicConformer is a hybrid CTC/RNNT model with no official sherpa-onnx support; exports need decoder/joiner repackaging.
8. **$35 was one run, not a project.**
Kyutai was correctly rejected, but for stronger reasons than the A10G: ~1B/2.6B params, en/fr only, GPU-class.

---

## 3. System architecture

### 3.1 End-to-end flow

```
 OPEN DATA (T1 first)                                  PRIVATE TEST SET (in-house, never trained on)
 IndicVoices | Vaani | SPRING-INX | CommonVoice | FLEURS | LibriSpeech/VoxPopuli
        |                                                        |
        v                                                        |
 [S0 Governance] licence manifest, gate text, normalizer, pins   |
        |                                                        |
        v                                                        |
 [S1 SPIKE] unmodified Nemotron -> int8 sherpa-onnx -> RTF on laptops
            tokenizer/Telugu test, prompt-table test, 10-20h tracer fine-tune,
            A10G throughput.  GATE -> else Path B
        |                                                        v
        v                                              [S2 EVAL HARNESS + BASELINES]
 [S3 DATA BUILD] normalise -> script policy -> splice/TTS/mine code-switch
                 -> manifests (speaker-disjoint) -> de-dup vs tests -> freeze DS-mvp-v1
        |
        v
 [S4 BAKE-OFF] Arm A1 / A2 (Nemotron) vs Arm B (114M) [vs C if access]  -> decision memo
        |
        v
 [S5 MAIN FINE-TUNE] 5a head warm-up -> 5b full FT (multi-lookahead) -> 5c-5d ablations -> 5e average
        |
        v
 [S6 EXPORT] chunk-size ONNX graphs -> int8 (uint8 weight-only) -> parity + RTF
        |
        v
 [S7 EVAL GATE] private set + regression suite -> MVP go/no-go
        |
        v
 [S8 PACKAGING] VAD + endpointing + P&C/ITN + (optional Romanization) + signed bundle
        |
        v
   MVP SHIPS  ---->  [S9 PRODUCTION TRACK] pseudo-labels, T2 (if approved), QAT, distillation, Telugu uplift
```

### 3.2 Components

| Component | Choice |
|---|---|
| Training framework | NVIDIA NeMo (version pinned at Stage 0) on PyTorch, Lhotse dataloading |
| Base model | Nemotron-3.5-ASR-Streaming-0.6B (Path A) |
| Tokenizer | SentencePiece; strategy decided in Stage 4 (Section 7.2) |
| Decoder | RNNT (cache-aware). CTC head only if present (unverified [U]) |
| Evaluation | In-house harness (Section 8) |
| Export | sherpa-onnx NeMo export scripts -> ONNX (encoder / decoder / joiner + metadata + tokens.txt) |
| Runtime | sherpa-onnx >= 1.13.5, ORT CPU, 4-6 threads |
| VAD | Silero VAD (licence to be verified by counsel) |
| Optional | Deterministic Romanization module (Section 10) |

### 3.3 Proposed repository layout [P]

```
10X_STT/
  pipeline.md                 # this plan
  progress.md                 # the log (append-only sections + status snapshot)
  reports/                    # research report (.md/.docx)
  research_notes/             # raw research notes (6 files)
  legal/
    licence_manifest.csv      # one row per dataset/model/tool
    gate_texts/               # dated snapshots of HF gate conditions
    questions_sent/           # letters to NVIDIA / AI4Bharat / ARTPARK + replies
  configs/
    normalizer/               # versioned, hashed normalizer spec
    train/                    # NeMo YAMLs per arm/stage
    eval/                     # eval configs, gates.yaml (pre-registered)
    export/                   # sherpa-onnx export configs per chunk size
  data/
    manifests/                # JSONL manifests ONLY (audio lives in S3/EBS, not git)
    lexicon/                  # English-loanword lexicon, script-policy tables
    synth/                    # code-switch synthesis recipes (not audio)
  scripts/                    # data prep, splice, filter, pseudo-label, export, bench
  eval/                       # harness code, baselines results, bootstrap, reports
  runs/                       # run cards (RUN-0001.md ...) + metric dumps
  exports/                    # model bundles (metadata + hashes; weights in S3)
  bench/                      # laptop RTF/RSS/latency results per device
```
Audio, checkpoints and ONNX bundles live in S3 (and EBS while training). Git holds code, configs, manifests, run cards and hashes.

### 3.4 Naming and versioning [P]
- Runs: `RUN-0001`, `RUN-0002`, ... one run card each (template in `progress.md`).
- Datasets: `DS-<tier>-<mix>-v<N>` (e.g. `DS-mvp-v1`), manifest SHA-256 recorded.
- Models: `MODEL-<arm>-<stage>-<date>` for checkpoints; shipped bundles `stt-hite-<semver>`; bundle version is separate from runtime version.
- Decisions: `D-###`. Pivots: `P-###`. Legal items: `L-##`. Unknowns: `U-##`.
- Every run card records: git commit, config hash, dataset manifest hash, base checkpoint hash, NeMo/PyTorch/CUDA versions, instance type, on-demand vs spot, GPU-hours, cost.

### 3.5 Version pins (filled at Stage 0, enforced afterwards)
`NeMo=?  PyTorch=?  CUDA=?  Lhotse=?  sherpa-onnx>=1.13.5 (exact=?)  onnxruntime=?  Python=?`
Rule: **export tool and runtime are pinned together.** Older sherpa-onnx versions silently mis-decode NeMo streaming transducers (fix landed in 1.13.5).

---

## 4. Infrastructure and operations

### 4.1 AWS setup [P unless noted]
- **Instance:** `g5.xlarge` (1x A10G 24 GB), us-east-1. On-demand ~$1.006/h; spot ~$0.43-0.52/h [E, third-party July-Sept 2026 snapshots; verify on provider pages]. Spot interruption rates >20% in one snapshot.
- **CPU/RAM caution [U, general knowledge]:** g5.xlarge has 4 vCPUs and 16 GiB RAM; audio decoding and dataloading on 4 vCPUs may starve the GPU. Evaluate `g5.2xlarge` (8 vCPU, 32 GiB, higher hourly price) in Stage 1. Do all CPU-heavy prep (resampling, filtering, manifest building, synthesis) on a cheap CPU instance or locally, not on the GPU instance.
- **Quota [U, general knowledge]:** new AWS accounts often have zero vCPU quota for G-family instances. File the quota request in Stage 0.
- **AMI:** an AWS Deep Learning AMI with CUDA/PyTorch, or a pinned container; record the image ID in the run card.
- **Storage:** raw archives and manifests in **S3**; attach **EBS** (gp3) only for the working set during training; use instance NVMe for hot data. IndicVoices archives alone are 745 GB, Vaani is larger; do not keep multi-TB volumes idle (an idle 1 TB EBS volume costs real money, ~$0.08/GB-month [U, general AWS pricing]).
- **Security:** private bucket, least-privilege IAM role on the instance, no public ACLs, encrypted volumes. In-house voice recordings are personal data (see 4.5).

### 4.2 Cost guardrails
- AWS Budgets alarm at 50/80/100% of the approved ceiling (set in Stage 0).
- Tag every resource `project=10X_STT, stage=<n>, run=<RUN-id>`.
- **Auto-stop:** every training launch script ends with a shutdown/stop command; idle-GPU watchdog (stop if GPU util < 5% for 20 min) [P].
- Log GPU-hours and dollars into the `progress.md` budget ledger **at the end of every run**.

### 4.3 Spot policy and checkpoint/resume
- Stages 1, 2, 3 (decoding), 6: on-demand (short, interruption-sensitive).
- Stages 4, 5: spot allowed **only with** checkpointing every 15-30 min to EBS and sync to S3, plus automatic resume from latest checkpoint (NeMo `resume_if_exists`-style behaviour [U, verify option names]).
- Resume test is part of Stage 1: kill a run mid-training, resume, confirm loss continuity.

### 4.4 Experiment tracking
TensorBoard or Weights & Biases [P], one project, run name = run ID. Log dev WER/CER per language at fixed chunk size every N steps, learning rate, throughput (audio-hours/GPU-hour), GPU memory, language mix per batch. Dump final metrics to `runs/RUN-xxxx/metrics.json`.

### 4.5 Data protection (in-house test set)
- Written consent form per speaker covering recording, storage, retention, use for evaluation only.
- Store identifiers separately from audio; speaker IDs pseudonymised; retention period decided with counsel.
- DPDP (India) implications for voice data were **not researched** [U]; legal item L-05.
- The private test set never leaves the controlled bucket and is never used for training or tuning (second hold-back split retained).

---

## 5. Stage-by-stage plan

> Every stage uses the same template: **Objective, Prereqs, Inputs, Steps, Outputs, Cost/time, Exit gate, If the gate fails, Log to progress.md.**
> GPU-hours are [E] (derived from ~150 audio-h per GPU-h for a ~120M model and ~30 for a 600M model, each possibly 2x off). **No A10G NeMo throughput benchmark exists in any source we found.** Stage 1 replaces these with measurements.

---

### Stage 0. Governance and foundations (weeks 0-2, parallel, CPU only)

**Objective.** Make the project legally and methodologically auditable before spending any GPU money.

**Prereqs.** Approval checkpoint 1 (plan + spike) is requested once steps 0.3-0.4 are filed.

**Inputs.** The report, the notes, accounts (AWS, Hugging Face).

**Steps**
- 0.1 **Repo + folders** per Section 3.3; `git init`; `.gitignore` for audio/checkpoints.
- 0.2 **Licence manifest** `legal/licence_manifest.csv`, one row per dataset/model/tool. Columns [P]: `id, name, kind(data|model|tool), version_or_hash, url, licence_as_stated, licence_snapshot_path, gate_terms_snapshot_path, date_captured, tier(T1-T4), attribution_string, commercial_use_confirmed(Y/N/pending), derivative_models_ok, contact, notes`.
- 0.3 **Access requests** (HF gated, log date and screenshot/text of every gate condition): IndicVoices, Vaani, Kathbath, IndicConformer-600M (+ per-language hybrid models), SraVaani-0.5-live and SraVaani-1.0, Nemotron-3.5 (accept terms). Gate text is only visible after login, so capture it at request time [dated].
- 0.4 **Legal questions** (full list in Section 16): OpenMDW-1.1 derivative/commercial terms for an int8 fine-tuned model on end-user devices; written confirmation from AI4Bharat and ARTPARK that MIT-tagged gated models allow commercial use, fine-tuning and use of outputs as pseudo-labels; T2 data position; attribution duties.
- 0.5 **Normalizer + script policy v0.1** (Section 6.5 and 8.1), versioned and hashed in `configs/normalizer/`.
- 0.6 **Version pins** (3.5) frozen in a `requirements`/container file.
- 0.7 **Name the minimum-spec devices** (decision A2): at least one low-power x86 U-series laptop, one mid x86, one base Apple M-series, one recent M-series. Obtain or book access.
- 0.8 **Start speaker recruitment** for the in-house test set; draft consent form (4.5).
- 0.9 **Pre-register gates:** commit `configs/eval/gates.yaml` (the Section 8.6 table) with a hash *before* any model results exist.
- 0.10 **AWS prep:** GPU vCPU quota request, Budgets alarm, S3 bucket, IAM role, tags.

**Outputs.** Licence manifest (initial), gate-text snapshots, legal question list + sent letters, normalizer spec v0.1, version-pin file, pre-registered gates, AWS ready.

**Cost/time.** ~$0 GPU. Storage costs unsourced (IndicVoices 745 GB). Weeks 0-2.

**Exit gate.** No unresolved legal *blocker* on the Nemotron licence; manifest exists; access requests filed.

**If the gate fails.** A licence blocker on Nemotron stops Path A. Escalate to seniors; pivot to Path B/C evaluation (logged as a pivot).

**Log.** Licence manifest status, access-request dates, letters sent, decisions A2/A5.

---

### Stage 1. De-risking spike (weeks 1-2, ~12 GPU-h, ~$12 on-demand / ~$6 spot [E])

**Objective.** Answer the five questions that decide whether Path A is viable, using an *unmodified* checkpoint plus one tracer-bullet fine-tune. Replace every [E] compute number with a measurement.

**Prereqs.** Stage 0 items 0.3, 0.6, 0.7, 0.10 done enough to download Nemotron and use the laptops.

**Inputs.** Unmodified Nemotron-3.5-ASR-Streaming-0.6B; 10-20 h of Telugu (IndicVoices/Vaani subset, access permitting); target laptops; a 1-2 h dev slice.

**Steps**
1. **Export unmodified Nemotron-3.5** with the sherpa-onnx recipe `scripts/nemo/nemotron-3.5-asr-streaming-0.6b` [U, confirm script name in the pinned repo]. Produce fp32 + int8 encoder/decoder/joiner, `tokens.txt`, metadata, at **320 ms and 560 ms**. Pin sherpa-onnx >= 1.13.5. **Parity check:** compare ONNX streaming output to NeMo's `conformer_stream_step` simulation on a fixed clip; logit tolerance < 1e-3 for fp32 [P].
2. **Laptop benchmark** on every named device: RTF, peak RSS, first-token latency, finalization latency; threads = 1/2/4; paced and unpaced; follow the Softcery harness hygiene (load-average gate, thread sweep, greedy decoding, built-in endpointing off to isolate model latency).
3. **Tokenizer and Telugu handling:** tokenise a Telugu text sample with Nemotron's SentencePiece model; record unk rate, tokens per word, character coverage, vocab size, byte-fallback presence. Run **zero-shot Telugu** audio and record exactly what it emits (script collapse? Latin? garbage?).
4. **Prompt mechanism:** read `prompt_dictionary` and `auto_prompt_id` in the export metadata. Test whether a new locale (te, plus code-switch locales) can be added (128-dim one-hot over 40 locales suggests free slots, our inference [U]) and whether sherpa-onnx accepts a modified dictionary/vocabulary.
5. **A10G tracer bullet:**
   a. Run NeMo's OOMptimizer [U, script `scripts/speech_recognition/oomptimizer.py`] to find max `batch_duration` for the 600M model (bf16, activation checkpointing, optionally 8-bit Adam).
   b. Measure full fine-tune **throughput (audio-hours per GPU-hour)** and **peak GPU memory**.
   c. Fine-tune on 10-20 h of Telugu with the chosen Telugu-representation approach (extend tokenizer, or replace decoder/joint).
   d. **Export that fine-tuned model through sherpa-onnx and decode a Telugu clip.** This proves train -> export -> decode works with a changed vocabulary or prompt table, which no source documents.
   e. **Kill-and-resume test** on spot (4.3).
6. **Baselines on a 1-2 h dev slice:** IndicConformer-600M, SraVaani-0.5-live (if access), unmodified Nemotron (Hindi, English).
7. **Check for a CTC head** in Nemotron-3.5 (the card only describes RNNT [U]); if none, plan to use IndicConformer's CTC for forced alignment.
8. **Evaluate `g5.2xlarge` vs `g5.xlarge`** for dataloading throughput (4.1).

**Outputs.** `bench/` RTF table per device; tokenizer report; prompt-table findings; A10G throughput + memory numbers; tracer-bullet pass/fail; baseline mini-table; CTC-head answer; **Stage 1 report** (written into `runs/` and summarised in `progress.md`).

**Exit gate [all P]**
- (a) fp32 ONNX matches NeMo streaming simulation.
- (b) int8, unpaced, 1 thread, **RTF <= 0.5 at 560 ms and peak RSS <= 1.5 GB on the lowest-spec target laptop**.
- (c) A documented way to represent Telugu (extend tokenizer, or replace decoder/joint) **with a passing tracer bullet**.
- (d) Measured A10G throughput **>= ~15 audio-hours per GPU-hour** for the 600M model.

**If the gate fails**
- (b) or (d) fails -> **Path B becomes primary** (114M arm).
- (c) fails for Nemotron -> Path B or C becomes primary.
- Licence blocker discovered -> **stop and escalate.**
- Log as pivot `P-###` with numbers.

**Log.** Every measurement (device, CPU model, RTF, RSS), the exact export commands and versions, throughput, memory, tokenizer stats, what zero-shot Telugu produced, gate result, any pivot.

---

### Stage 2. Evaluation harness, baselines, in-house test set (weeks 2-4, ~8 GPU-h, ~$8 [E])

**Objective.** Freeze the yardstick *before* building the model so no threshold is tuned to the result.

**Prereqs.** Stage 0 pre-registered gates + normalizer; Stage 1 devices/baseline access.

**Inputs.** Normalizer spec; public sanity sets; recruited speakers; baseline models.

**Steps**
1. **Implement the evaluation package** (`eval/`): versioned normalizer (8.1), strict WER, lattice/multi-reference WER (OIWER via `voi-oiwer` for Hindi), CER, code-switch-token vs native-token WER with transliteration-invariant scoring (T-WER/SN-WER style), script-fidelity rate, insertion rate on silence/noise, streaming-latency metrics (8.5), edge metrics, speaker-level bootstrap CIs, paired bootstrap between models.
2. **Build the in-house test set** (Section 8.3): 3-5 h per language, 60-100+ speakers; stratified conditions; native-linguist-corrected ASR-seeded transcripts; double annotation of the gold core and 20% of the rest; at least two Telugu dialect regions.
3. **Public sanity sets** (never headline): Kathbath test, FLEURS hi/te, IndicVoices test/valid, Vaani-Benchmark-V1.0 (Hindi, 3 refs), Svarah, Monsoon en-IN/hi-IN, Lahaja, MUCS Hi-En.
4. **Re-run baselines on identical audio** (not copied from papers): IndicConformer-600M (CTC and RNNT); SraVaani-0.5-live at 80/480/1040 ms; SraVaani-1.0; Nemotron-3.5 zero-shot (Hindi, English) at 320/560 ms; unmodified 114M hybrid; community Hindi/Hinglish and Indian-English Zipformers; Whisper-large-v3 only to document the Telugu failure.
5. **Contamination checks:** audio fingerprint + transcript n-gram de-dup of the future training manifests against every public test set; document known in-domain contamination of baselines.
6. **Reproducibility check:** a second engineer reproduces one baseline within 0.2 absolute WER.
7. **Re-confirm the proposed gate thresholds** against the measured baselines (week 1 of this stage); any change = decision entry.

**Outputs.** Harness repo, versioned normalizer (hash), baseline table, private test set v1 (hashed) + held-back split, contamination report.

**Cost/time.** ~8 GPU-h baseline decoding (~$8). Recording/annotation cost is **not sourced**: budget decision A7.

**Exit gate.** Second-engineer reproduction within 0.2 WER; thresholds re-confirmed.

**If the gate fails.** Fix normalizer/harness inconsistencies; do not proceed to training with an unreproducible yardstick.

**Log.** Normalizer hash, test-set size/speakers/hash, all baseline numbers (with chunk size and normaliser), contamination findings, threshold re-confirmation decision.

---

### Stage 3. Data build (weeks 3-5, ~5 GPU-h for MVP, ~$5 [E])

**Objective.** Produce the MVP training manifest, tokenizer inputs, code-switch data and English replay set.

**Prereqs.** Gate text captured; normalizer + script policy frozen; dataset access granted.

**Steps** (detail in Section 6)
1. Download T1 sets; record version/hash and date in the licence manifest.
2. Convert all audio to **16 kHz mono**; drop clips outside duration bounds (e.g. < 1 s or > ~20 s unless segmented [P]).
3. Apply the **normalizer + script policy** (Latin for English words, native script for Indic, ASCII digits) with the **transliteration-lexicon pass**.
4. **Quality filters:** reference-model CER (flag utterances where a strong teacher disagrees wildly), chars-per-second bounds, language/script-ratio checks, repetition checks.
5. **Code-switch data** (Section 6.6): splicing + TTS-plus-LLM text + mining real mixed segments; flag everything synthetic.
6. **English replay set** (CV en-IN, LibriSpeech, Vaani-En, VoxPopuli).
7. **Speaker-disjoint train/dev split**; de-dup vs all test sets (audio fingerprint + normalised transcript n-grams).
8. **Tokenizer artefacts** per the Stage 4 arms (Section 7.2), but **do not commit** to one until the bake-off.
9. **Freeze `DS-mvp-v1`:** manifest JSONL files with per-source tier, hours, language, synthetic flag; compute SHA-256; write the data card.

**Outputs.** `DS-mvp-v1` manifests + data card (hours by language/source/tier, synthetic %, filter retention), updated licence manifest, lexicon files.

**Cost/time.** ~5 GPU-h for alignment/filter decoding. TTS synthesis ~$50 (one preprint's price for ~22k utterances [M, single preprint]) for the 50 h code-switch slice. (Pseudo-labelling of Vaani, ~40 GPU-h, is **production-tier only**.)

**Exit gate.** Manifest with per-source tier and hours; T1-only variant buildable; **zero overlap with test sets**; data card complete.

**If the gate fails.** Resolve overlaps or filter failures before training. If real Telugu hours fall materially below plan, log the shortfall and revisit scope (A3).

**Log.** Final hours per language/source, filter retention rates, synthetic share, manifest hash, any data dropped and why.

---

### Stage 4. Bake-off (weeks 5-7, ~90 GPU-h for 3 arms, ~$90; lean MVP 2 arms ~60 GPU-h, ~$60 [E])

**Objective.** Choose the base **by measurement, not by card claims.**

**Arms (equal data and equal cost cap [P])**

| Arm | What | Notes |
|---|---|---|
| **A1** | Nemotron-3.5, keep tokenizer + extend for Telugu | Preserves Hindi decoder knowledge; needs custom embedding/joint-extension code (not a documented NeMo feature) |
| **A2** | Nemotron-3.5, replace decoder/joint with a new aggregate tokenizer | Cheap; loses Hindi decoder knowledge |
| **B** | 114M cache-aware hybrid + aggregate hi/te/en tokenizer | CPU-cheap fallback |
| **C** | SraVaani-0.5-live continuation | **Only if** fine-tune weights + written commercial terms granted |
| **D** | icefall Zipformer | Enters only if A fails the CPU gate |

Also include one **tokenizer-strategy comparison** (small per-script aggregate 256-512 each vs shared 5-8k BPE) because the notes conflict (Section 7.2).

**Protocol**
- Identical supervised subset: ~**300 h Telugu, 200 h Hindi, 100 h English-IN** [P], identical normalizer, identical recipe, **<= ~30 GPU-h per arm**, multi-lookahead training over {0,1,3,6,13}.
- Report Telugu/Hindi/Indian-English **WER and CER at 160/320/560 ms**, **RTF on the target laptops**, code-switch slice, memory, and **learning curves** (WER at 25/50/100% of the subset).

**Decision rule [P]**
- Choose **Arm A** if it passes the CPU gate **and** beats Arm B by **>= 10% relative on Telugu at 560 ms**.
- Choose **Arm B** if Arm A fails the CPU gate, **or** the gain is < 10% **and** Arm B is >= 3x faster on CPU.
- **Arm C** wins only with written licence terms and an export path.
- The **learning curve** is the extrapolation tool: if curves are still falling steeply at the subset limit, weight the arm with more headroom.

**Outputs.** Decision memo (numbers, curves, chosen arm, tokenizer choice), run cards for every arm.

**Exit gate.** Winner selected with a written memo. **If no arm reaches within 1.5x of the SraVaani-live Telugu baseline (re-measured) at 560 ms on the equal-budget subset, escalate and reconsider scope** (e.g. Hindi + English GA, Telugu beta; or more data).

**If the gate fails.** See pivot tree (Section 11). **Approval checkpoint 3** (base-model decision memo) happens here.

**Log.** Every arm's run IDs, configs, metrics, GPU-hours, the decision and who approved it.

---

### Stage 5. Main post-training of the winner (weeks 7-11, ~150 GPU-h, ~$150 on-demand / ~$75 spot [E])

**Objective.** Train the production candidate on the full MVP mix.

**Prereqs.** Stage 4 decision; `DS-mvp-v1` frozen; spot resume tested.

**Steps (Path A shown; details and hyperparameters in Section 7)**
- **5a. Head warm-up** (only if vocabulary or prompt table changed): freeze the encoder, train decoder/joint/prompt for **2-5k steps** [E] at a higher head learning rate.
- **5b. Full fine-tune:** unfreeze all; encoder LR 1e-4 to 5e-5, cosine (NeMo guidance 1e-4 to 1e-5; override the default Noam warm-up); SpecAugment; speed perturbation 0.9/1.0/1.1; language sampling p_i proportional to n_i^0.5-0.7 with >= 20-30% English + code-switch; **multi-lookahead** `att_context_size` over `[56,{0,1,3,6,13}]` (Nemotron-3.5 left context 56; the left context used at export sets cache shapes, so fix and document it); FP16 RNNT loss with fused batch splitting for memory; bf16; activation checkpointing; duration-bucketed batching; checkpoint every 15-30 min.
- **5c. Pseudo-label round** at lower LR, ablating filtered vs unfiltered labels: **production tier**, skipped in lean MVP.
- **5d. Code-switch ablation:** with vs without synthetic data; keep real code-mixed data in dev.
- **5e. Checkpoint averaging** (last 5-10); optional WiSE-style interpolation with the original encoder; **English regression must be no worse than 10% relative** [P].
- **Ablation priority:** tokenizer strategy -> multi-lookahead vs single (3-8% relative gain in NVIDIA's paper [M]) -> filtered vs unfiltered pseudo-labels -> with/without code-switch synthesis -> average/WiSE alpha -> PTQ vs QAT.

**Outputs.** Candidate checkpoint(s), run cards, learning curves, ablation table, English-regression report.

**Cost/time.** ~150 GPU-h ≈ 3.5 passes over the 1,280 h MVP mix (~4,500 audio-hours) at the estimated 600M throughput [E]. If measured throughput is half, this doubles.

**Exit gate.** Meets the **MVP slices (Section 8.6) on the private set at 560 ms, fp32**; English regression <= 10% relative; no insertion-rate violation.

**If the gate fails.** Diagnose by slice (Telugu data volume? tokenizer? forgetting? code-switch?), then follow the pivot tree. Never "fix" by tuning thresholds.

**Log.** All runs, hyperparameters, curves, ablations, best checkpoint hash, decisions on what to keep.

---

### Stage 6. Compression and export (weeks 10-13, ~10 GPU-h, ~$10 [E])

**Objective.** A verified int8 sherpa-onnx bundle per chunk size.

**Prereqs.** A Stage 5 candidate that passed the fp32 gate.

**Steps**
1. **Export** at the target chunk sizes with the **same recipe as Stage 1** (checklist in Section 9.2). One export per chunk size; normalization = "NA"; cache support baked in; decoder/joiner split; metadata injected; `tokens.txt` from the SentencePiece model; `prompt_dictionary` / `auto_prompt_id` if applicable.
2. **Parity test:** PyTorch cache-aware simulation vs ONNX streaming output on a fixed clip set; numeric divergence below threshold.
3. **Post-training quantization (PTQ) int8:** **weight-only block quantization on encoder MatMuls** is the best-documented path (8.03 fp32 -> 8.01 WER for ORT int8 k-quant; 8.12 for int4-mixed; **10.14 when ConvInteger/MatMulInteger paths were used** [M, English, 8-dataset average, Microsoft ORT port, arXiv 2604.14493]). **Keep subsampling convs, decoder LSTM, joiner and cache tensors in fp32.** Quantize to **uint8 (QUInt8), not QInt8** (the ORT CPU ConvInteger kernel is uint8-only).
4. **Validate on Indic dev sets** (no public int8-vs-fp32 Hindi/Telugu measurement exists). Compare to fp32 per slice.
5. **QAT only if** int8 degradation exceeds 3-5% relative.
6. **Regress the exporter itself:** the ORT port lost 0.75 absolute WER vs PyTorch at fp32 (7.28 -> 8.03) [M]; our parity test must catch that class of drift.
7. **Benchmark** on every named device with the Stage 1 harness (RTF, RSS, first-token/final latency, cold start).

**Outputs.** Per-chunk-size bundles (encoder/decoder/joiner int8, tokens.txt, metadata), parity report, int8-vs-fp32 table, device benchmark table.

**Exit gate.** Parity test passes in CI; **int8 within 3-5% relative of fp32 on every slice**; edge gates met (RTF, RSS).

**If the gate fails.** QAT; or int4-mixed/fp32 for the runtime that tolerates it; or a smaller arm (distillation, Stage 9). Log as pivot.

**Log.** Export commands, versions, bundle hashes, parity result, int8 deltas per slice, device numbers.

---

### Stage 7. Evaluation gate and hardening (weeks 12-15, ~30 GPU-h reserve, ~$30 [E])

**Objective.** Apply the MVP gate and collect the production-gap list.

**Steps**
1. **Full regression suite:** private set (all slices), public sanity sets, synthetic entity/number set (reported separately), adversarial silence/music/noise clips, long streams > 60 s, edge harness on all devices, English-regression check vs unmodified Nemotron.
2. **Paired bootstrap** against baselines with speaker-level CIs.
3. **Hallucination checks:** insertion rate, output length on silence, script-fidelity rate.
4. **Robustness slices:** 8 kHz telephony (codec-processed), 10 dB SNR, far-field.
5. **Ablate and fix** within the ~30 GPU-h reserve (most likely: data rebalancing, extra epoch, averaging weights).
6. **Production-gap list:** which production gates fail and why.

**Exit gate.** **MVP gate (Section 8.6):** all Hindi and English slices plus hallucination and edge gates; Telugu within +10% of its gate. Decision: ship MVP to design partners, or iterate. **Approval checkpoint 4.**

**If the gate fails.** Iterate (bounded), narrow scope (Hindi + English GA, Telugu beta), or stop. Log as pivot with numbers.

**Log.** The complete gate table (target vs actual per slice), go/no-go decision and approver, gap list.

---

### Stage 8. Application layer, packaging, optional Romanization (weeks 12-16)

**Objective.** A product-grade bundle.

**Steps**
1. **VAD:** Silero VAD (counsel to verify licence; README badge says CC BY-NC 4.0 vs MIT in LICENSE file). TEN VAD is "Apache 2.0 with additional conditions" and needs legal review.
2. **Streaming practicalities:** >= 0.5 s pre-roll after VAD; feed one chunk of **trailing silence** (otherwise final words are lost); cut streams only at utterance ends; partials are **replaced, not appended**; unknown session option keys are silently dropped (validate config).
3. **Endpointing:** rule-based first; measure false-cutoff and miss rates.
4. **Punctuation/ITN:** per policy A4; NeMo-text-processing has Hindi ITN; no Telugu ITN found (gap).
5. **Hotwords:** transducer + `modified_beam_search` only.
6. **Optional Romanization module** (Section 10).
7. **Packaging:** signed, versioned bundle: manifest with SHA-256, pinned runtime version, tokenizer hash, chunk size, quantization recipe; detached signature; semantic version separate from runtime version; **sidecar process isolation** for the runtime.
8. **Notices:** auto-generated attribution/notices file from the licence manifest.
9. **CI:** latency/WER/parity regression on every bundle.

**Exit gate.** CI green on latency/WER/parity; **legal sign-off on bundle contents**; attribution file generated.

**Log.** Bundle version + hashes, CI results, legal sign-off reference, VAD/endpoint settings.

---

### Stage 9. Production track (after MVP; only with approval)

**Objective.** Close the gap from MVP to production gates.

**Work items (each its own decision entry)**
1. **Pseudo-labelling at scale** (distillation form 1; ~40 GPU-h for 1.5-2.5k h with a 600M teacher [E]). Teachers: IndicConformer-600M + SraVaani-1.0. Source: Vaani untranscribed audio (~13.9k h Hindi, ~2.1k h Telugu, ~0.3k h English [E]). Filters (thresholds [E], calibrate on a labelled holdout): inter-teacher CER < ~10-15%; script-ratio vs audio-LID check; repeated-n-gram and chars-per-second filters; CTC forced-alignment score. Granary-style pipelines retain 47.9-74.6% [M]. Target ~1,200 h pseudo-labelled in the production mix (Hindi ~350 h, Telugu ~250 h). **Prerequisite:** written confirmation that teacher *outputs* may be used (L-02).
2. **T2 data under written risk acceptance** (Kathbath ~100/110 h Hi/Te, SLR104 ~90 h Hi-En, optional): <= 20% per language; train a **T1-only ablation** so the product can be rebuilt without T2 if challenged. **Shrutilipi (All India Radio audio) and NPTEL stay out** unless Telugu WER stalls and the risk is accepted in writing.
3. **In-house data collection** (consented, commercial-safe) for Telugu and code-switching, if budget allows (also the strongest fix for Telugu).
4. **QAT** if PTQ int8 degrades > 3-5% relative.
5. **Distillation form 2 (compression):** distil to a ~65M Zipformer or the 114M NeMo model if the 600M model is too slow on the weakest laptops.
6. **Telugu uplift:** morphological splitting of targets cut Whisper-medium Telugu WER 23.31 -> 18.73 [M]; must be reversible and applied identically at evaluation.
7. **Punctuation/casing model** and Telugu ITN.
8. **Production gate** (Section 8.6) and a release-regression policy: > 5% relative regression on any slice between releases, or any train/test overlap = **no-go**.

**Production mix target (~4,200 h; ~3,000 labelled + ~1,200 pseudo-labelled) [P]:** Hindi ~1,500 h, Telugu ~1,000 h, English ~1,200 h, code-switch ~300 h.
**Compute implication (our arithmetic [E]):** at ~30 audio-h/GPU-h for the 600M model, three passes over 4,200 h need ~420 GPU-h for the main training stage alone, giving a whole-project total of ~610 GPU-h (~$615 on-demand / ~$275 spot) plus ~$50 TTS and contingency. Throughput is unmeasured and may be 2x off.

---

## 6. Data specification

### 6.1 Licence tiers
T1 = permissive licence on consent-collected audio. T2 = open licence with a caveat (ShareAlike, scraped upstream audio/text, or conflicting labels). T3 = terms unresolved. T4 = unusable commercially. These are engineering risk tiers, **not legal advice**.

### 6.2 Dataset catalogue

| Tier | Dataset (licence per source) | Hindi h | Telugu h | English-IN h | Warnings |
|---|---|---|---|---|---|
| T1 | **IndicVoices** (CC BY 4.0, gated) | ~790 [E] | ~480 [E] | 0 | Hours are our arithmetic (+/-15%); paper 7.3k h vs later listing 12k h vs HF card 23.7k total / 11.2k transcribed. Gate text login-only. Recount from manifest. |
| T1 | **Vaani** (CC BY 4.0, gated) | 1,004 transcribed (14,924 total) | 184 transcribed (2,326 total) | 22 transcribed (337 total) | Paper's fine-tune subset smaller (594 / 113 h). Phone-recorded, image-prompted speech. Some third-party subsets labelled NC. |
| T1 | **SPRING-INX** (AIKosh: CC BY 4.0; paper: "public domain") | 351 | 0 (not released) | 0 | Wording conflict to resolve; ~10% conversational data code-mixed. |
| T1 | Common Voice v27 (CC0) | 15.7 | 0.94 | 2,827 (~5.9% "indian" accent, ~224 h [E]) | Hindi/Telugu tiny. |
| T1 | FLEURS (CC BY 4.0 [U]) | ~7 | ~8 | n/a | Hours from Vistaar; licence/hours not re-retrieved. Also used as eval. |
| T1 | LibriSpeech, VoxPopuli | | | tens-hundreds | English replay only. |
| T2 | IndicVoices-R (HF: CC BY 4.0; AIKosh: CC BY-ND 4.0) | ~75 | ~136 | 0 | Overlaps IndicVoices. ND conflict -> treat as T2. TTS-oriented. |
| T2 | **Kathbath** (HF: cc-by-4.0; GitHub: CC0 packaging; AIKosh: CC BY-SA) | ~100 | ~110 | 0 | Three conflicting labels; text comes from crawled IndicCorp (AI4Bharat does not own it). |
| T2 | **SLR104 / MUCS 2021 Hi-En** (CC BY-SA 4.0) | ~90 (Hi-En CS) | 0 | | Lecture style; BY-SA; HF re-uploads can silently relicense. |
| T2 | OpenSLR SLR66 Telugu (CC BY-SA 4.0) | | small | | ShareAlike question for weights. |
| T2 | **Shrutilipi** (CC0 packaging / CC-BY-4.0 per another listing) | large | large | | Raw audio is All India Radio, crawled; packager does not own it. Stays out of base mix. |
| T3 | SLR103 (MUCS Hindi/Marathi/Odia) | | | | Links to a Microsoft Open Data licence we could not resolve. |
| T4 | Microsoft Speech Corpus (Telugu etc.), MUCS Telugu, Gram Vaani SLR118, Skit-S2I, CS-FLEURS, GigaSpeech (access terms), SPGISpeech, Emilia (orig.), Samanantar text, CMU Wilderness | | | | NC / research / academic-only / no licence. **Do not use.** |

**Committed T1 supply [E]:** Hindi ~2,150 h (1.9-2.3k), **Telugu ~670 h (0.55-0.75k)**, Indian-accent English ~0.1-0.25k h, dedicated Hindi-English code-switch ~0 h, Telugu-English code-switch **0 h**. Adding all T2: Hindi 4.0-4.5k h, Telugu ~1.4k h. **Telugu is the binding constraint** (below IndicWhisper's 806 h and SraVaani's 2,036 h).

**Licence-conflict rules**
- When labels conflict, **use the more restrictive reading** until resolved.
- A CC-BY wrapper cannot license rights the packager does not hold (All India Radio audio, crawled text).
- Capture dated gate text at download for all gated sets.
- CC BY attribution: we give credit, licence notice and link in model documentation; whether weights count as "adaptations" is **undecided** (CC's guidance does not settle it) -> legal item L-05.
- India DPIIT mandatory-licence proposal (Dec 2025): open for consultation until Feb 2026, no final outcome found.

### 6.3 Recommended data mix [P, not experimentally validated]

**MVP, T1 only, ~1,280 h**

| Language | Hours | Sources |
|---|---|---|
| Hindi | 550 | IndicVoices 250, Vaani (QC-filtered) 200, SPRING-INX 80, CV + FLEURS 20 |
| Telugu | 400 | IndicVoices 280, Vaani 110, CV + FLEURS 10 |
| English (Indian-accent weighted) | 280 | CV en-IN subset 180, LibriSpeech 50, Vaani-En 22, VoxPopuli 28 |
| Code-switch | 50 | Synthetic splices of Hi/Te + En + mined code-mixed T1 segments (LID/script filter) |

**Production, ~4,200 h (~3,000 labelled + ~1,200 pseudo-labelled):** Hindi ~1,500 (incl. ~350 h Vaani pseudo-labels, optionally Kathbath ~100 h T2), Telugu ~1,000 (incl. ~250 h pseudo-labels, optional Kathbath ~110 h), English ~1,200, code-switch ~300 (synthetic/mined ~200 h + SLR104 ~90 h T2). T2 <= 20% per language; T1-only ablation required.

**Other bounds [P]:** spike 10-20 h Telugu; bake-off subset ~300 h Te / 200 h Hi / 100 h En-IN. NVIDIA's "a few hundred hours adds a language" is a **[V]** claim; the only evidence found is a single community Danish fine-tune (10 h took WER ~36% -> ~16%).

### 6.4 Manifest and metadata schema [P]
One JSON object per line (NeMo manifest style): `audio_filepath, duration, text, lang (hi|te|en|cs-hi-en|cs-te-en), target_lang, source (dataset id), tier, speaker_id, is_synthetic, cs_density, snr_est, split (train|dev), orig_text` (pre-normalisation, for audit). Plus a dataset-level `data_card.md`: hours by language/source/tier, synthetic %, filter retention, manifest SHA-256, licence manifest row IDs.

### 6.5 Script policy and normalization [P, decide in Stage 0]
- **Latin for English words, native script for Indic words, ASCII digits.** Enforced by a transliteration-lexicon pass (English loanwords written in Devanagari/Telugu are mapped back to their English spelling using a lexicon mined from our own code-switched transcripts).
- Reason: corpora use no common convention (MUCS training mixes Latin and Devanagari while its blind test uses Latin). The SraVaani card warns Latin-script code-switching can inflate WER against single-script references; our evaluation must score this fairly (8.2).
- This choice also fixes the optional Romanization layer (Section 10).
- **Unicode:** NFC (not NFKC without testing); remove ZWJ/ZWNJ on both reference and hypothesis for scoring; nukta folding and chandrabindu/anusvara canonicalisation are *optional folds applied identically to reference and hypothesis*, results reported with and without. **Never use Whisper's normalizer for Hindi/Telugu** (it strips matras and virama; METEOR similarity original vs normalised: English 0.97, Hindi 0.38 [M]).
- **No source covers Telugu ZWNJ/conjunct normalisation or digit handling** in published benchmarks: test empirically, then freeze (versioned, hashed spec).

### 6.6 Code-switching data recipe (no open Telugu-English corpus exists)
1. **Splicing** (NVIDIA's method, arXiv 2306.08753): concatenate a Hindi/Telugu utterance with an English utterance (short silence, loudness-matched); build the mixed transcript; control code-switch density (<10%, 10-30%, >30% foreign tokens); mark `is_synthetic=true`.
2. **TTS + LLM text:** LLM generates entity-dense code-mixed sentences; TTS synthesises. One preprint: ~22,000 entity-dense utterances for < $50 raised Telugu entity-hit-rate 0.027 -> 0.473 on a synthetic holdout, **but regressed read-speech FLEURS-Te WER by up to +6.6 points and missed every pre-registered target** [M, single preprint]. So: mix with real data; ablate with/without; **never use synthetic data for headline accuracy**; TTS and LLM licences are unchecked (L-06).
3. **Mining:** find naturally code-mixed segments in IndicVoices/Vaani/SPRING-INX with script-mix and LID filters. Real volume in T1 sets is unmeasured.
4. **Eval for CS:** private CS-stratified test slice (Section 8.3); report CS-token WER vs native-token WER.

### 6.7 Punctuation constraint
NVIDIA's Nemotron fine-tune recipe expects **punctuated, cased transcripts and a `target_lang` tag per clip**, but IndicConformer-style corpora mostly lack punctuation. Unpunctuated Indic targets would likely teach the model to drop punctuation for Hindi/Telugu (our inference). Options: (a) LLM punctuation restoration of training text (Granary used Qwen2.5-7B, rejecting changes above 5% CER); (b) ship unpunctuated Indic output + a downstream P&C model (Cadence-Fast, 270M, no ONNX export found). **Decision A4/Q10** is for seniors.

---

## 7. Training specification

### 7.1 Hyperparameter table (starting point; all [P] unless marked)

| Item | Setting | Basis |
|---|---|---|
| Init | `nvidia/nemotron-3.5-asr-streaming-0.6b` | Path A |
| Precision | bf16 autocast (Ampere supports bf16 [U]); fp32 master weights | notes |
| Memory (600M) | AdamW fp32 states ~9-10 GB before activations; fits 24 GB only with modest `batch_duration` (~100-300 s), bf16, activation checkpointing; 8-bit Adam saves ~3.6 GB (unverified) | [E] post_training notes |
| Batching | Lhotse dynamic bucketing by total `batch_duration`; find max with OOMptimizer; `num_buckets`, `num_cuts_for_bins_estimate`; default max_duration 16.7 s | NeMo docs |
| Effective batch | Gradient accumulation to several hundred to ~1,000 s of audio | [P], tune |
| LR (encoder) | 1e-4 to 5e-5, **cosine**; replace NeMo's default Noam warm-up | NeMo fine-tune guide |
| LR (head, 5a) | Higher than encoder (e.g. 5-10x) | [E] |
| 5a steps | 2-5k with encoder frozen | [E] |
| Augmentation | SpecAugment on; speed perturb 0.9/1.0/1.1; noise/RIR (MUSAN, RIRS_NOISES) | notes |
| Language sampling | p_i proportional to n_i^0.5-0.7; >= 20-30% English + code-switch | [E] |
| Streaming | `att_context_size` multi-lookahead `[[56,0],[56,1],[56,3],[56,6],[56,13]]` (chunk = (N+1) x 80 ms: 80/160/320/560/1120 ms) | NVIDIA Stateful Conformer; 3-8% relative gain [M] |
| Loss | RNNT with FP16 loss + fused batch splitting. **If a CTC head exists [U]:** CTC weight 0.3. FastEmit lambda ~0.005 optional (latency) | notes (114M path) |
| Epochs | MVP mix ~3.5 passes (~4,500 audio-hours) ~ 150 GPU-h [E] | |
| Checkpointing | Every 15-30 min; keep top-k by dev WER; resume enabled | 4.3 |
| Averaging | Last 5-10 checkpoints; optional WiSE interpolation with original weights | [M] forgetting evidence |
| Regression cap | English WER <= 10% relative worse than unmodified Nemotron | [P] |

Forgetting evidence: Irish-on-Whisper full fine-tune took English LibriSpeech 3.7 -> 8.8 [M] (EWC cut it to 5.4); averaging original and adapted weights is the best-evidenced ASR forgetting control [M, arXiv 2210.15282]. **LoRA is not supported** for Nemotron-3.5 per its fine-tune blog author, so full fine-tuning is the only supported path.

### 7.2 Tokenizer options (open decision A6; bake-off decides)

| Option | Description | Pros | Cons |
|---|---|---|---|
| **Extend (A1)** | Keep Nemotron tokenizer and rows; add Telugu (and code-switch) pieces/prompt slots | Preserves Hindi decoder knowledge | Custom embedding + joint extension code not documented as a NeMo built-in; sherpa-onnx load of modified vocab unverified |
| **Replace (A2)** | New tokenizer; re-initialise decoder/joint; keep encoder | Simple, cheap | Loses Hindi decoder knowledge; needs warm-up (5a) |
| **Small aggregate** | Per-script SentencePiece unigram, 256-512 pieces each (total ~1-1.5k); NeMo aggregate/concatenated tokenizer; free per-token language ID; small RNNT joint memory; fast CPU decode | NVIDIA supports; cheap | Notes conflict (below) |
| **Shared BPE** | One 5-8k BPE across scripts (SraVaani: 5,000 shared; Canary-v2: unified beat concatenated; 8,192 ~ 16,384, both better than 4,096) | Strong results in recent labs | More joint memory |

The post-training notes recommend small aggregate; the lab-methodology notes point to shared 5-8k BPE. **Unreconciled**: include one arm per option in Stage 4. Replacing the vocabulary requires re-initialising decoder/joint (transducer) but the encoder is retained.

### 7.3 Training procedure checklist (per run)
1. Confirm `DS-mvp-v1` hash; confirm config hash; confirm pins.
2. Start OOMptimizer result -> set `batch_duration`.
3. Launch with auto-stop + checkpoint sync + tags.
4. Watch loss, dev WER per language, throughput, GPU memory, language mix.
5. Stop at dev-WER plateau (patience [P]) or budget cap.
6. Average checkpoints, evaluate fp32 at 160/320/560 ms.
7. Write run card; update budget ledger; update `progress.md`.

### 7.4 Training failure modes and mitigations

| Failure mode | Detection | Mitigation |
|---|---|---|
| Language confusion (Telugu <-> Hindi, script collapse) | Script-fidelity rate; per-language CER | Language-balanced sampling; prompt/LID tags; filter mislabelled data |
| Repetition/hallucination | Insertion rate on silence/noise; output length ratio | Training-data filters; adversarial clips; structurally lower risk than seq2seq (our inference) |
| English-word mangling in code-switch | CS-token WER vs native-token WER | Script policy + lexicon; CS data; do not train on romanised targets |
| Telugu agglutination inflating WER | WER/CER ratio (observed 3.5-3.7x) | Headline CER next to WER; optional reversible morphological splitting |
| Catastrophic forgetting (English/Hindi) | English regression gate | English replay >= 20-30%; averaging/WiSE; EWC if needed |
| Streaming degradation | WER vs chunk-size curve | Multi-lookahead training; chunk-aware evaluation |
| Pseudo-label noise bounding quality | Filtered-vs-unfiltered ablation | Two-teacher agreement; drop pseudo-labels if teacher licence fails |
| Domain mismatch (phone/image-prompted Vaani vs laptop mic) | In-house laptop-mic test slice | Noise/RIR augmentation; in-house data |

---

## 8. Evaluation specification

### 8.1 Normalization protocol [P]
NFC; remove ZWJ/ZWNJ both sides; strip punctuation but keep combining marks; lowercase Latin; collapse whitespace; remove annotator tags/disfluency markers; map digits to ASCII via fixed table; optional nukta/chandrabindu/anusvara folds applied identically to reference and hypothesis and reported with/without. **Versioned, hashed spec; every baseline re-run through the same code; never mix differently normalised numbers.**

### 8.2 Metrics (report four numbers per slice, plus diagnostics)
1. **Strict WER** (minimal normalization).
2. **Lattice / multi-reference WER:** OIWER (`voi-oiwer`) for Hindi; 2-3 references on a gold core for Telugu. Multi-reference materially changes results (mean WER 24.80 with 1 ref -> 17.76 with 3 refs on Vaani-Benchmark-V1.0 [M]).
3. **CER** (headline beside WER for Telugu).
4. **Code-switch-token vs native-token WER** with transliteration-invariant scoring (T-WER/SN-WER style). MER does not fix the Devanagari-vs-Latin problem.
- Diagnostics: **script-fidelity rate**, **insertion rate on silence/noise clips** (hallucination signature), speaker-level bootstrap CIs (about 2-3x wider than naive word-level [E]).

### 8.3 In-house test set (private, hashed, never trained on) [P]
- **Size:** 3-5 h per language, 60-100+ speakers (precedents 1.3-12.5 h: Monsoon hi-IN 1.33 h, Svarah 9.6 h, Lahaja 12.5 h, Vaani V1.0 10.9 h).
- **Composition:** ~40% spontaneous/conversational on own phones; ~20% telephony 8 kHz (codec-processed); ~15% read named-entity/number prompts; ~15% code-switch stratified by density; ~10% noisy/far-field.
- **Dialects:** at least two Telugu regions (Telangana, Andhra/Rayalaseema); Hindi L1-Telugu/Tamil/Bengali speakers.
- **Annotation:** ASR-seeded then native-linguist corrected (Monsoon process); double annotation of the 1-1.5 h gold core and 20% of the rest; inter-annotator WER <= 5% read, <= 10% spontaneous [P].
- **Splits:** dev (retirable) + second held-back split. Synthetic TTS audio is for entity/number/lexicon stress tests only, reported separately.
- **Public sanity sets (never headline):** Kathbath test, FLEURS hi/te, IndicVoices test/valid, Vaani-Benchmark-V1.0, Svarah, Monsoon, Lahaja, MUCS Hi-En. Known contamination: IndicWhisper trained on Vistaar splits; Nemotron-3.5's training includes FLEURS and Common Voice; SraVaani uses Vaani and RESPIN for both fine-tuning and evaluation. **The in-house set is the trust anchor.**

### 8.4 Baselines the team re-runs (not copied)
IndicConformer-600M (CTC + RNNT); SraVaani-0.5-live (80/480/1040 ms) and SraVaani-1.0; Nemotron-3.5 zero-shot (Hindi, English) at 320/560 ms; unmodified 114M hybrid; community Hindi/Hinglish and Indian-English Zipformers; Whisper-large-v3 (Telugu failure only). Published numbers are **not comparable across vendors** (Nemotron Hindi 6.8 on FLEURS vs 20.2 on Vaani; IndicConformer 8.2 telephony OIWER vs 13.8 mixed-set mean vs 20.0 single-reference Vaani [M]).

**Published reference points [M, their setup]:** IndicConformer-600M Hindi 13.8 / Telugu 26.4 mean WER; SraVaani-1.0 14.0 / 25.1; IndicWhisper 13.6 / 28.8 (Vistaar); SraVaani-live streaming Telugu 34.6/33.6/31.4/30.3 and Hindi 22.1/21.3/19.3/18.0 WER at 0/80/480/1040 ms; Nemotron-3.5 Hindi FLEURS 8.13 (80 ms) -> 6.81 (1.12 s); Whisper large-v3 Hindi ~30-33, Telugu >100.

### 8.5 Streaming and edge metrics [P]
Per model and per chunk size: WER/CER at 160/320/640/1280 ms and offline (the WER-vs-latency curve); **first-token emission delay** (speech onset to first non-blank token, P50/P90, against forced-alignment boundaries, because chunk-model token timestamps equal chunk end); **finalization latency** (end of speech to final transcript, P50/P90); endpoint delay + false-cutoff and miss rates; partial-hypothesis revision rate (no source defines it, so define and publish it); **RTF** paced and unpaced at 1/2/4 threads on a named CPU/OS/power mode; peak and steady-state RSS; model size on disk fp32/int8; cold-start load time; CPU utilisation. Disable built-in endpointing and use greedy decoding when isolating model latency.

### 8.6 Gates (all [P]; pre-registered in Stage 0, reconfirmed in Stage 2)
Scored on the private set, streaming at <= 640 ms, int8, on a stated laptop CPU.

| Slice | MVP gate | Production gate | Anchor evidence |
|---|---|---|---|
| Hindi clean/read | <= 18 WER | <= 12 | IndicConformer 13.8 mean offline; Nemotron 6.8-8.1 (in-domain); SraVaani-live 18-22 |
| Hindi spontaneous | <= 28 strict (<= 20 multi-ref) | <= 20 (<= 14) | IndicConformer 20.0/13.1 on Vaani V1.0; Nemotron 20.2; Zipformer 25.7 |
| Telugu clean/read | <= 32 WER (<= 10 CER) | <= 24 (<= 7 CER) | IndicWhisper 25.0-25.4; IndicConformer 26.4; SraVaani-live 30-35 |
| Telugu spontaneous/telephony | <= 40 strict | <= 28 | IndicConformer 23.7 OIWER on Voice of India; best agricultural 33.2 |
| English-IN (Svarah/Monsoon) | <= 15 | <= 9 | Whisper large 7.2 Svarah; small streaming 20.7-28 |
| Code-switch | within +8 abs of same model's monolingual spontaneous WER | within +4 abs; CS-token WER <= 1.6x native | Vaani V1.0: CS-token penalty +2.6 to +15.6 abs; no Telugu-English baseline exists |
| Relative | <= 1.3x IndicConformer-600M offline; <= 1.15x best open streaming baseline | <= 1.15x offline | Expected streaming penalty +15-25% relative [E] |
| Robustness | 8 kHz <= 1.6x clean; 10 dB SNR <= 1.5x | <= 1.3x; <= 1.25x | GSM codec and competing speech are the worst degradations [M] |
| Hallucination | insertion <= 3%; no output > 1.2x reference length on silence; script fidelity >= 0.98 | insertion <= 1.5%; SFR >= 0.995 | Whisper Indic failure modes |
| Edge | RTF <= 0.5 (unpaced, 1 thread); RSS <= 1.5 GB; first-token P90 <= 800 ms | RTF <= 0.3; RSS <= 1 GB; first-token P90 <= 500 ms; finalization P90 <= 300 ms | No published Indic laptop numbers |

**Go/no-go rule [P].** MVP requires **all Hindi and English slices plus hallucination and edge gates, with Telugu within +10% of its gate.** Production adds Telugu, code-switch and telephony. **> 5% relative regression on any slice between releases, or any training/test overlap, is a no-go.**

**Expectation check.** Gates are anchored on small streaming models (Hindi ~18-25, Telugu ~30-40 on mixed public sets). The best offline open models are Hindi 13-14 / Telugu 25-26 [M]; a commercial API scores Telugu OIWER 18.2 on a benchmark run by an interested party [M]. **Telugu production gates are the least likely to be met with 0.7k T1 hours.**

---

## 9. Export and deployment specification

### 9.1 Stack

| Layer | Choice | Notes and caveats |
|---|---|---|
| Runtime | **sherpa-onnx >= 1.13.5**, ORT CPU EP, 4-6 threads, `session.intra_op.spin_duration_us=200` | Apache-2.0. First-class NeMo cache-aware transducer support since 1.12.22 (English Nemotron) / 1.13.3 (multilingual 3.5); the greedy-search fix for NeMo streaming landed in **1.13.5**. Older versions decoded Nemotron badly **without any error** -> pin runtime and exporter together. |
| Apple silicon | Baseline: same ONNX bundle on CPU. Optional: MLX 8-bit or CoreML INT8 | MLX 8-bit 733 MB disk / 992 MB peak; 5-bit 539/800 MB (avg FLEURS WER 11.53 vs 11.01 for 8-bit) [M, community]; CoreML INT8 612 MB / 1,238 MB (M5 Pro). **No RTF published for any Apple path.** Community ports cover the stock vocabulary; a modified vocabulary needs re-conversion (our inference). |
| Intel alternatives | OpenVINO IR (FluidInference), GGUF (cstr: F16 1.3 GB, Q4_K 458 MB), ORT-direct three-session runtime | Community artefacts; no laptop RTF. |
| VAD | Silero VAD | Licence conflict (MIT in LICENSE vs CC BY-NC badge) -> counsel. TEN VAD needs legal review. |
| P&C / ITN | Train P&C in if transcripts allow; NeMo-text-processing Hindi ITN; Telugu ITN not found | Cadence-Fast (270M, Hi/Te) has no ONNX export found. |
| Hotwords | Transducer + modified beam search only | Not available for CTC-only models (rules out SraVaani-live as-is). |

### 9.2 Export pitfalls checklist (use in Stage 1 and Stage 6)
1. **Normalization must be "NA" at export** in both the preprocessor object and config; otherwise the graph expects per-utterance normalization.
2. **Cache support is baked per chunk size.** Export through `forward_for_export` with `export_cache_support`; inputs include `cache_last_channel`, `cache_last_time`, `cache_last_channel_len`; outputs return next caches. Left context differs between models ([70,x] Nemotron-EN, [56,x] 3.5) -> fix and document it for the post-trained model. **No official NeMo page documents cache-aware ONNX export**; evidence is a community recipe plus sherpa's scripts.
3. **sherpa needs separate encoder, decoder and joiner sessions plus metadata** (`model_type, vocab_size, subsampling_factor, normalize_type, pred_rnn_layers, pred_hidden, feat_dim`). NeMo emits a combined decoder-joint that must be split. Missing metadata -> "No model_type in the metadata!".
4. **Nemotron-3.5 specifics:** `tokens.txt` from the SentencePiece model; `prompt_dictionary` and `auto_prompt_id` in the encoder metadata; one export per chunk size. Whether a modified prompt dictionary/vocabulary loads is **undocumented** -> Stage 1 tracer bullet.
5. **Quantization:** ConvInteger CPU kernel is uint8-only (QInt8 exports fail with "Could not find an implementation for ConvInteger(10)") -> re-quantize to **QUInt8**. Integer-activation conv paths degraded WER 8.20 -> 10.14 [M]. Use weight-only block quantization on encoder MatMuls; keep convs, decoder, joiner and caches fp32. ORT docs flag U8S8 saturation on non-VNNI x86.
6. **Front-end parity:** replicate NeMo's mel front end exactly (128 mel for Nemotron, 80 for IndicConformer; 0.97 pre-emphasis, Slaney mels). Upstream exports often omit `mel_filters.json` / `hanning_window.json`.
7. **Streaming practicalities:** trailing-silence flush chunk; >= 0.5 s pre-roll after VAD; cut streams only at utterance ends; partials replaced not appended; unknown session option keys silently dropped.
8. **Reduced left context lowers accuracy** (WER 7.28 -> 8.51 when left context dropped from 10 chunks to 2 [M]); mind the memory budget when tuning.
9. **CoreML paths** from IndicConformer use a fixed 1024-frame encoder input (non-streaming); `.mlmodelc` must be compiled on the target Mac.
10. **CI:** regress PyTorch cache-aware simulation vs ONNX streaming output on a fixed clip; fail on WER regression > 0.3 absolute [P], RTF above budget, or numerical divergence beyond threshold.

### 9.3 Measured RTF and size numbers (not interchangeable)

| Setup | Result | Source and caveats |
|---|---|---|
| sherpa-onnx 1.13.8, ORT 1.28.2, int8 Nemotron-3.5 multilingual, **Ryzen 7500F 6C desktop (AVX512)**, 4 threads, greedy, 16.7 s clip | Processing per audio second at 1120/560/320/160/80 ms chunks = 61.3/96.7/145.4/274.6/645.6 ms (**RTF ~0.06/0.10/0.15/0.27/0.65**); test-clip WER 7.91/7.99/8.27/8.88/9.43; finalization 45-75 ms; RAM ~1.0-1.1 GB | [M, Softcery Sept 2026]. Desktop CPU, not a laptop. |
| Same, Mac M2, 1120 ms | 0.176 core-seconds per audio second (2 threads), final p50 85 ms; 4 threads 0.364 core-seconds | [M]. Wall RTF up to ~0.09 if saturated is our inference. |
| Microsoft ORT port of Nemotron-0.6B, AMD EPYC 7V12 (AVX2), 32 cores, batch 1, 0.56 s delay | RTFx 6.7-7.3 (RTF ~0.14-0.15); at 0.16 s delay RTFx 2.87 | [M, arXiv 2604.14493]. Different CPU/ISA/runtime/chunking; do not mix with Softcery. |
| Streaming Zipformer 66M (Indian English), 4-thread Xeon | int8 RTF 0.035; fp32 0.183; int8 ~68 MB | [M, community]. English-fine-tuned. |
| IndicConformer-120M Hindi Q8_0 GGUF | RTF 0.06 (~16x real time), 225 MB, ~140 MB RAM | [M, community, CPU unspecified, offline]. |

**Not known:** RTF on i5/i7 U-series laptops or any M1/M3 for a streaming FastConformer; official sherpa-onnx RTF tables; int8-vs-fp32 WER on Hindi/Telugu. **Planning inference [E]:** a 600M streaming FastConformer int8 should run at RTF ~0.06-0.15 at 560-1120 ms on a 6-8-core AVX2/AVX512 laptop (unproven on 15 W parts); 160-320 ms chunks are the Pareto point on desktop; a 120M model should be 4-5x cheaper per audio second. User-perceived latency ~ half the lookahead window + finalization (45-75 ms) + VAD/endpoint delay.

### 9.4 Bundle format and CI
- Bundle: `encoder.int8.onnx, decoder.onnx (fp32), joiner.onnx (fp32), tokens.txt, metadata, manifest.json` (SHA-256 per file, runtime pin, tokenizer hash, chunk size, quantization recipe, training run ID, dataset manifest hash, normalizer hash) + detached signature (e.g. Sigstore/cosign or minisign), verified at load.
- CI per bundle: parity test, WER regression on a frozen mini-set per slice, RTF/RSS on reference hardware, notices file present.

---

## 10. Optional Romanization layer (never a training target)

Romanization is a **post-process on native-script output**. Romanized training targets are rejected (2.4).

**Design [P]**
1. Tokenise ASR output by script; pass Latin tokens through unchanged (script or token-ID range gives free language ID).
2. Look up Devanagari/Telugu-script English loanwords in a lexicon mined from our own code-switched transcripts; emit the English spelling.
3. Otherwise apply scheme-based transliteration with a **Hindi schwa-deletion pass** (Choudhury-style rules by default); Telugu keeps inherent vowels (background linguistics, not from the sources).
4. Version all tables so output is reproducible.
- **Two modes:** *scholarly* (ISO 15919, round-trip reversible) and *natural* (Hunterian-like, schwa-deleted, loanwords restored, not reversible).

**Tools and licences**
- `indic_transliteration`: MIT; README mentions no ISO 15919/Hunterian and no schwa deletion.
- **Aksharamukha: appears GPL-3.0 -> do not ship in a closed binary.**
- IndicXlit: MIT code and models, but a learned model with stochastic beam output -> comparison baseline only, **not** in the deterministic path.
- uroman: licence unresolved (Apache-2.0 on the Rust port vs MIT-like original).
- Dakshina romanisation dataset: CC BY-SA 4.0 (unconfirmed) -> evaluation use only.
- Known weak points: schwa deletion unsolved by plain mappings (Arora et al., ACL 2020); inconsistent Hindi loanword spellings (डॉलर vs डालर); Telugu lacks a nukta in Unicode (Unicode L2/19-401).

**Evaluation:** round-trip CER on all code points for the strict scheme; token-level agreement with attested romanizations from Dakshina for the natural mode; loanword recovery rate on the code-switch set; schwa-deletion accuracy against a lexicon; small human preference panel. **No published quantitative baselines exist.**

**Status:** Romanization is optional; seniors have not confirmed a requirement (R6). Build only after MVP unless a downstream need appears.

---

## 11. Decision rules and pivot tree

Every pivot gets a `P-###` entry in `progress.md` with the numbers that triggered it.

| # | Trigger | Action | Decided by |
|---|---|---|---|
| 1 | Nemotron licence text (OpenMDW-1.1) blocks commercial derivative or on-device redistribution | Stop Path A. Evaluate B/C. Escalate. | Seniors + counsel |
| 2 | Stage 1 gate (b) fails: RTF > 0.5 or RSS > 1.5 GB at 560 ms on lowest-spec laptop | **Path B (114M) becomes primary**; or raise the min-spec if product allows | Engineering lead + seniors |
| 3 | Stage 1 gate (c) fails: no way to represent Telugu in Nemotron with a working export | Path B primary, or Path C if access + terms | Engineering lead |
| 4 | Stage 1 gate (d) fails: measured throughput < 15 audio-h/GPU-h on 600M | Path B primary; or revise budget upward; or consider A100 | Engineering lead + seniors |
| 5 | Stage 4: Arm A fails CPU gate, or gain < 10% relative and Arm B >= 3x faster | Choose Arm B | Per decision rule |
| 6 | Stage 4: no arm within 1.5x of SraVaani-live Telugu baseline at 560 ms | Escalate: narrow scope (Hi+En GA, Te beta), add data, or revisit plan | Seniors |
| 7 | Stage 5: Telugu dev WER stalls | Add T2 data under written risk acceptance; start pseudo-labelling (Stage 9) earlier; consider in-house data | Seniors |
| 8 | Stage 5: English regression > 10% relative | Raise English replay; weight averaging/WiSE; lower LR; EWC | Engineering lead |
| 9 | Stage 6: int8 degrades > 3-5% relative | QAT; int4-mixed or fp32; or smaller model | Engineering lead |
| 10 | Stage 7: Telugu > +10% over gate, but Hi/En/hallucination/edge pass | Ship Hi+En GA, Telugu beta; continue Stage 9 | Seniors |
| 11 | Teacher-output licence not confirmed | Drop pseudo-labels; rely on T1 + in-house data | Counsel |
| 12 | Synthetic code-switch data regresses real read speech | Reduce synthetic share; report separately; rely on mined/real CS data | Engineering lead |
| 13 | Compute estimate off by 2x | Re-baseline budget; spot + checkpointing; shrink subsets; Path B | Engineering lead + seniors |
| 14 | Any train/test overlap discovered | Rebuild manifests; invalidate affected results; re-run | Engineering lead |

**Stop conditions:** unresolved licence blocker; irreproducible evaluation; gate thresholds modified after seeing results without a logged decision.

---

## 12. Risk register (likelihood / impact are our proposals)

| # | Risk | L / I | Mitigation |
|---|---|---|---|
| 1 | **Telugu insufficient:** ~0.7k T1 hours; published streaming Telugu ~30 WER | High / High | Pseudo-label Vaani Telugu (~2.1k h); phase scope (Hi+En GA, Te beta); decide on T2 under written risk acceptance; in-house data |
| 2 | **Nemotron tokenizer/prompt cannot take Telugu**; modified vocab does not export/load in sherpa-onnx | Medium / High | Stage 1 tracer bullet; Arm B fallback; custom vocab-extension code |
| 3 | **600M too heavy for target laptops** (no laptop RTF exists) | Medium / High | Stage 1 gate; 320-560 ms chunks; thread tuning; Arm B/D; distillation |
| 4 | **Licence blocker** (Nemotron OpenMDW-1.1 vs NVIDIA Open Model License; gated MIT cards; data conflicts; teacher output terms) | Medium / Critical | Written confirmations; T1-only rebuildable model; attribution manifest; counsel review of OpenMDW-1.1 text (unread) |
| 5 | **Code-switch data quality:** no real Telugu-English corpus; synthetic data can regress read speech (+6.6 WER in one preprint) | High / Medium | Mix synthetic with real; in-house CS test set; ablate; report separately |
| 6 | **Catastrophic forgetting** after Telugu full FT | Medium / Medium | English replay >= 20-30%; EWC or WiSE; regression gate |
| 7 | **Pseudo-label noise** bounds student quality; teacher output terms unverified | High / Medium | Two-teacher agreement; script/LID/repetition filters; ablation; drop if licence fails |
| 8 | **Export/runtime drift:** silent mis-decoding on old sherpa; ONNX port loses ~0.75 abs WER | Medium / High | Version-pinned bundles; parity CI; sidecar isolation |
| 9 | **Compute estimate off by 2x** (no A10G benchmark exists) | Medium / Medium | Stage 1 measurement; reserve; spot + checkpointing; A100 for batch decoding |
| 10 | **Hallucination/repetition and script confusion** | Medium / Medium | Insertion-rate and script-fidelity gates; data filters |
| 11 | **Normalization/evaluation artefacts** mislead decisions | Medium / Medium | Frozen normalizer; CER + WER; multi-reference gold core; transliteration-invariant CS scoring |
| 12 | **Domain mismatch:** Vaani is phone/image-prompted; test is laptop mic | Medium / Medium | Noise/RIR augmentation; in-house laptop-mic test set |
| 13 | **Storage/other unpriced costs** exceed the GPU bill | Medium / Medium | S3 + ephemeral EBS; budget alarm; explicit line items for annotation/legal/storage |
| 14 | **Spot interruptions** (>20% in one snapshot) lose progress | Medium / Low | Checkpoint 15-30 min; resume tested in Stage 1 |

---

## 13. Budget

### 13.1 Lean MVP (this is the number to quote) [E]
Assumptions: on-demand $1.006/h; spot ~$0.45/h; only the T1-only MVP mix; no pseudo-labelling; 2-arm bake-off.

| Stage | GPU-hours | On-demand | Spot |
|---|---|---|---|
| 0 Governance | 0 | $0 | $0 |
| 1 Spike | 12 | $12 | $5 |
| 2 Harness + baselines | 8 | $8 | $4 |
| 3 Data build (alignment/filter only) | ~5 | $5 | $2 |
| 4 Bake-off (2 arms x 30) | 60 | $60 | $27 |
| 5 Main post-training | 150 | $151 | $68 |
| 6 Compression/export | 10 | $10 | $5 |
| 7 Eval + hardening | 30 | $30 | $14 |
| **GPU total** | **~275** | **~$276** | **~$125** |
| Synthetic TTS (single-preprint figure) | | ~$50 | ~$50 |
| Contingency (15% of GPU) | | ~$40 | ~$20 |
| **MVP total** | | **~$370** | **~$195** |

### 13.2 Full report budget (3-arm bake-off, pseudo-label decoding included)
~340 GPU-h -> ~$341 on-demand / ~$153 spot; plus ~$50 TTS and 15% contingency -> **planning range ~$300-450 on-demand / ~$180-280 spot.**

### 13.3 Production-scale extrapolation (our arithmetic [E])
~610 GPU-h -> ~$615 on-demand / ~$275 spot + ~$50 TTS + contingency -> **~$700-800 on-demand / ~$350-400 spot.** All depends on unmeasured throughput.

### 13.4 NOT included in any figure
Storage (IndicVoices 745 GB; Vaani larger), recording and annotating the in-house test set (Indic transcription cost per hour not found), engineer time, legal review, laptop hardware, any A100 batch decoding.

**Cost-control rules:** run Stage 1 first and re-issue this table with measured throughput; shut instances down when idle; keep data on S3; log every run's GPU-hours and dollars in the `progress.md` ledger.

---

## 14. Timeline (about 16 weeks [E]; 1-2 engineers + part-time legal)

| Weeks | Activity |
|---|---|
| 0-2 | Stage 0 governance; **Stage 1 spike**; start speaker recruitment |
| 2-4 | Stage 2 harness, baselines, in-house recording and annotation |
| 3-5 | Stage 3 data build, code-switch synthesis |
| 5-7 | **Stage 4 bake-off**; **checkpoint 3: base-model decision memo** |
| 7-11 | Stage 5 main post-training + ablations |
| 10-13 | Stage 6 compression and export |
| 12-15 | Stage 7 evaluation gate and hardening; **MVP go/no-go (checkpoint 4)** |
| 12-16 | Stage 8 application layer, packaging, (optional) Romanization, legal sign-off |
| 16+ | Stage 9 production track (only with approval) |

## 15. Approval checkpoints

| # | When | What seniors approve |
|---|---|---|
| 1 | After Stage 0 steps 0.3-0.4 are filed | Plan + spike + budget ceiling |
| 2 | After the Stage 1 gate | Continue with Path A or switch to B/C; revised budget with measured throughput |
| 3 | After Stage 4 | Base-model decision memo; tokenizer strategy; scope (A3) |
| 4 | After Stage 7 | MVP go/no-go; production track budget |

---

## 16. Open decisions and legal items (owner and status tracked in `progress.md`)

### 16.1 Legal review items
- **L-01** Read OpenMDW-1.1 in full (and resolve the Together AI "NVIDIA Open Model License" listing); confirm derivative-model, attribution and commercial-redistribution terms for a fine-tuned, int8-converted model shipped on end-user devices.
- **L-02** Written confirmation from AI4Bharat and ARTPARK-IISc that MIT-tagged gated models (IndicConformer, SraVaani) permit commercial use, fine-tuning, and use of their outputs as pseudo-labels.
- **L-03** Capture gate-condition text for IndicVoices, Vaani, Kathbath at download time; counsel reviews.
- **L-04** Position on T2 data (Kathbath prompts from crawled text, Shrutilipi/AIR, NPTEL, BY-SA sets), and whether CC BY-SA data may touch shipped weights.
- **L-05** Attribution obligations for CC BY datasets in model documentation; confirm no Indian TDM exception or DPIIT licensing outcome affects the plan; DPDP implications for voice data in the in-house test set (consent, storage, retention).
- **L-06** Licence compatibility for TEN VAD, Silero VAD, Cadence-Fast, NeMo-text-processing, and any TTS/LLM used for synthesis.

### 16.2 Engineering/product decisions
- **Q7** Scope: Hi + Te + En GA, or Hi + En GA with Telugu beta.
- **Q8** Default chunk size (suggest 320-560 ms) and acceptable first-token P90.
- **Q9** Name the minimum-spec x86 and Apple laptops.
- **Q10** Output policy: Latin for English words, ASCII digits, punctuation/casing in or out for Indic output.
- **Q11** Tokenizer strategy: small per-script aggregate vs shared 5-8k BPE; extend vs replace for Nemotron.
- **Q12** Budget and owner for the in-house test set (3-5 h per language) and ownership of the private split.
- **Q13** T1-only vs T1+T2 production target; is a T1-only ablation a release requirement?
- **Q14** On-demand vs spot with checkpointing; allow an A100 for batch pseudo-label decoding.
- **Q15** Approve Section 8.6 gate thresholds after Stage 2 re-runs baselines.
- **Q16** Is Romanized output ever required? (The user said it is not a must; the reason was unconfirmed.)

---

## 17. Unknowns and conflicts register (resolve in Stage 0/1; track in `progress.md`)

| ID | Topic | Conflict or gap | Handling |
|---|---|---|---|
| U-01 | Nemotron-3.5 licence | HF card: OpenMDW-1.1; Together AI listing: NVIDIA Open Model License; text unread | Counsel; ask NVIDIA |
| U-02 | Nemotron-3.5 Telugu | No source confirms whether Telugu is among the 8 "tokenizer-recognised but un-fine-tuned" locales | Stage 1 tokenizer test |
| U-03 | Nemotron-3.5 CTC head | Card describes RNNT; hybrid CTC unverified | Stage 1 check |
| U-04 | Prompt table / modified vocab in sherpa-onnx | Undocumented | Stage 1 tracer bullet |
| U-05 | SraVaani-0.5-live card | Says streaming WER "Hindi only" yet tabulates Telugu; "real-time-safe" CPU claim w/o numbers | Re-measure |
| U-06 | SraVaani-1.0 Hindi WER | 12.4 (card) vs 14.0 (paper) | Use re-run baseline |
| U-07 | IndicConformer on Vaani-Benchmark-V1.0 | 13.2 (card) vs 20.0/16.8/13.1 by approach (paper) | Own multi-reference scoring |
| U-08 | IndicConformer licence | MIT on AI4Bharat cards; community GGUF repack says CC-BY-4.0; training-data licences unstated | Written confirmation (L-02) |
| U-09 | Omnilingual Hindi/Telugu | Meta CSV: Hindi CER 3.6 / Telugu 6.5; third party: Hindi CER 46.0; Voice of India Telugu OIWER 50.7 | Unresolved; do not rely as teacher |
| U-10 | Kathbath, Lahaja, IndicVoices-R, SPRING-INX, GigaSpeech, Emilia licences | Conflicting labels | More restrictive reading |
| U-11 | IndicVoices hours | Paper 7.3k; listing 12k; HF 23.7k total / 11.2k transcribed | Recount from manifest |
| U-12 | Vaani hours | HF 31,278 h / 2,122 transcribed vs paper 31,255 / 2,043; fine-tune subset 594/113 h | Recount |
| U-13 | sherpa-onnx int8 sizes | 464 MB (Softcery) vs ~632-650 MB (OpenWhispr) | Measure ours |
| U-14 | Microsoft vs Softcery RTF | RTFx ~7 (EPYC 32 cores) vs ~16 (Ryzen 4 threads) | Measure ours |
| U-15 | Silero VAD licence | MIT in LICENSE; "CC BY-NC 4.0" badge in README | Counsel (L-06) |
| U-16 | Cloud prices | Modal A100 $2.50 vs $3.72; Lambda A10 $0.86-1.29; spot varies daily | Verify provider pages |
| U-17 | A10G NeMo throughput | No benchmark found anywhere | Stage 1 |
| U-18 | Laptop RTF for any Indic streaming model | None published | Stage 1 |
| U-19 | int8-vs-fp32 on Hindi/Telugu | None published | Stage 6 |
| U-20 | Fine-tune offline -> streaming | No published recipe (we use NVIDIA's released streaming checkpoint instead) | n/a |
| U-21 | Tokenizer advice | Small aggregate (256-512/script) vs shared 5-8k BPE | Stage 4 arms |
| U-22 | Vendor claims carried | NVIDIA "few hundred hours" [V]; Saaras <150 ms TTFT [V]; Voice of India run by an interested party; Danish 10 h anecdote; Bhili ~200 h model unreleased | Not used as evidence |
| U-23 | Not retrieved at all | OpenMDW-1.1 text; Indic Open Model License v1.0 text; gate texts; Whisper licence; NGC 114M streaming-model licences; unified-RNNT paper numbers; full Nemotron fine-tune blog beyond excerpts; Telugu ZWNJ/ITN guidance; TDT cache-aware export to sherpa-onnx | Stage 0/1 |

---

## 18. Glossary

| Term | Meaning |
|---|---|
| **STT/ASR** | Speech-to-text / automatic speech recognition |
| **Streaming** | Emits text while audio is still arriving, in small chunks |
| **Cache-aware streaming** | Encoder keeps cached left context so each new chunk is processed once; trained with limited look-ahead |
| **FastConformer** | NVIDIA's efficient Conformer encoder (8x subsampling) |
| **RNNT / transducer** | Decoder type with an encoder, prediction network and joiner; native to streaming |
| **TDT** | Token-and-Duration Transducer; speeds the decoding loop, not the encoder |
| **CTC** | Simpler alignment-free loss/decoder; no hotwords in sherpa-onnx |
| **Chunk / look-ahead** | Audio window processed at once; `att_context_size=[left,right]` frames of context (80 ms per frame) |
| **WER / CER** | Word / character error rate |
| **OIWER** | Orthographic-variant-tolerant WER (accepts valid spelling variants) |
| **MER / T-WER / SN-WER** | Mixed error rate / transliteration-invariant / script-normalised WER for code-switching |
| **RTF / RTFx** | Real-time factor (processing time / audio time; lower is better) / its inverse |
| **int8 / PTQ / QAT** | 8-bit weights / post-training quantization / quantization-aware training |
| **Pseudo-labelling** | A teacher model transcribes unlabeled audio to make training data |
| **Noisy student** | Train on teacher-labelled data, optionally iterate |
| **Distillation** | Training a (usually smaller) model to mimic a teacher |
| **WiSE-FT / averaging** | Interpolating or averaging weights to limit forgetting |
| **T1-T4** | Our data licence risk tiers |
| **ONNX / sherpa-onnx** | Portable model format / the CPU runtime that executes it |
| **Code-switching (CS)** | Mixing languages within an utterance (Hinglish, Tenglish) |
| **Path A-D, Arm A-D** | Candidate chain (Section 2.2) / bake-off arms (Stage 4) |

---

## 19. Key sources (full list in `reports/` and `research_notes/`)

- Nemotron-3.5 card: https://huggingface.co/nvidia/nemotron-3.5-asr-streaming-0.6b ; fine-tune blog: https://huggingface.co/blog/nvidia/fine-tuning-nemotron-35-asr
- Stateful (cache-aware) Conformer: https://arxiv.org/html/2312.17279v3 ; Canary-v2/Parakeet-v3: https://arxiv.org/html/2509.14128v2
- NeMo fine-tuning docs: https://docs.nvidia.com/nemo/speech/latest/asr/fine_tuning.html ; dataloaders: https://docs.nvidia.com/nemo/speech/latest/dataloaders.html
- Multilingual/code-switched NeMo (concatenated tokenizer): https://arxiv.org/abs/2306.08753 ; https://developer.nvidia.com/blog/multilingual-and-code-switched-automatic-speech-recognition-with-nvidia-nemo/
- IndicConformer: https://huggingface.co/ai4bharat/indic-conformer-600m-multilingual ; SraVaani: https://huggingface.co/ARTPARK-IISc/SraVaani-0.5-live ; SraVaani paper: https://arxiv.org/html/2608.08235
- Datasets: IndicVoices https://huggingface.co/datasets/ai4bharat/IndicVoices ; Vaani https://huggingface.co/datasets/ARTPARK-IISc/Vaani ; Kathbath https://huggingface.co/datasets/ai4bharat/Kathbath ; SPRING-INX https://ar5iv.labs.arxiv.org/html/2310.14654
- CC guidance on AI training: https://creativecommons.org/using-cc-licensed-works-for-ai-training-2/
- sherpa-onnx: https://github.com/k2-fsa/sherpa-onnx ; hotwords: https://k2-fsa.github.io/sherpa/onnx/hotwords/index.html ; Nemotron export scripts: https://github.com/k2-fsa/sherpa-onnx/tree/master/scripts/nemo/nemotron-3.5-asr-streaming-0.6b
- CPU benchmark (Softcery): https://softcery.com/lab/hosting-nemotron-asr-streaming-on-a-cpu.md ; ORT quantization study: https://arxiv.org/html/2604.14493
- Evaluation: Whisper normalizer problem https://arxiv.org/html/2409.02449v4 ; Vaani-Benchmark multi-ref https://arxiv.org/html/2606.21408 ; Voice of India https://arxiv.org/html/2604.19151 ; Vistaar https://arxiv.org/html/2305.15386
- Synthetic code-switch / Telugu entities: https://arxiv.org/abs/2605.03073 ; CoSTA: https://arxiv.org/pdf/2406.10993
- Forgetting/averaging: https://arxiv.org/pdf/2210.15282 ; Irish-on-Whisper: https://arxiv.org/html/2407.06800v1
- Kyutai DSM: https://arxiv.org/html/2509.08753v2 ; Kyutai STT: https://kyutai.org/stt
- Cloud pricing snapshots (verify): https://compute.doit.com/spot/us-east-1/g5.xlarge ; https://calculator.holori.com/aws/ec2/g5.xlarge/us-east-1

---

## 20. How to use this document day to day
1. At the start of every work session: read `progress.md` (status snapshot first), then the relevant stage here.
2. Do the stage's steps; when something deviates from this plan, record a decision `D-###` (and a pivot `P-###` if the plan changes) in `progress.md` first, then update this file and bump the version.
3. At the end of every session: append an activity-log entry, update the status snapshot, budget ledger, run registry, data ledger, legal tracker and unknowns register as applicable.
4. Never edit past log entries; correct them with a new dated entry.
