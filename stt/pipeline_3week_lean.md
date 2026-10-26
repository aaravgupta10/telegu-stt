# 10X_STT: 3-Week Lean Pipeline (Plan v2, the NEWER plan)

| | |
|---|---|
| **Document** | `pipeline_3week_lean.md` |
| **Date** | 2026-10-13 |
| **Status** | PROPOSED. **Likely to be the plan we use.** Not yet approved by the senior. No step has started. |
| **Relationship to the older plan** | The older, bigger plan is kept unchanged in `pipeline.md` (v1.0 plus revision notice v1.1) for reference. This file replaces it for day-to-day work only if the senior approves. |
| **Log file** | `progress.md` (record every action, decision and number there; see its Section 0) |

**Evidence labels:** **[M]** measured and published by a cited source; **[V]** vendor or author claim; **[E]** our estimate; **[P]** our proposal (we can change it by logging a decision); **[U]** unverified or from general knowledge. Everything about our own training speed, hours and cost is [E] until the Week-1 tests measure it.

---

## 1. What this plan is

**Why it exists.** The owner confirmed (D-021) a **very tight budget and only 3 weeks**, that the compute is **rented on AWS** (not owned), and that the earlier ~$650 estimate would not be approved. The older plan assumed 6-8 weeks, three full models and a larger GPU spend.

**Fixed decisions this plan relies on** (see `progress.md` Decision log):
- **D-016** three separate monolingual models (Hindi, Telugu, English-India).
- **D-017** the STT is **offline** (not streaming).
- **D-018** STT first; TTS later and out of scope here.
- **D-004** commercial product, open data only.
- **D-005** Romanized output (Hindi/Telugu in Latin letters) is **not** required.
- **D-021** very tight budget, 3 weeks.
- **D-023** (2026-10-13) the senior chose **native-script output**: English words inside Hindi/Telugu stay in native script (for example "meeting" is written as मीटिंग). **No Latin-letter variant, no tokenizer change.**

**What we deliver in 3 weeks:** an **internal demo and evidence package**, not a commercially cleared release:
1. A fine-tuned **Hindi** model and a fine-tuned **Telugu** model (from AI4Bharat IndicConformer-120M), each with before-and-after accuracy numbers.
2. A measured **English** choice (an existing model, trained only if clearly weak).
3. Proof that the models **convert to ONNX and run in sherpa-onnx** (or a documented fallback).
4. A short report, a demo, a licence/evidence pack, and an up-to-date `progress.md`.

**Why "not cleared for release":** several licences (IndicVoices, Vaani, IndicConformer gates; any ambiguous sets) still need written confirmation, and replies can take longer than 3 weeks. Nothing in this plan is sent to licensors without the owner's go-ahead.

---

## 2. What was cut compared with the older plan

| Older plan (`pipeline.md`) | This plan |
|---|---|
| 6-8 weeks, ~700 h training data per language | 3 weeks, **~300 h per language** |
| Bake-off between IndicConformer and Parakeet arms | **IndicConformer only** for Hindi and Telugu; Parakeet only for English |
| Pseudo-labelling, distillation, TTS phase | Not done |
| Large private test set (3-5 h per language) | **~1 h per language** plus public test sets |
| Ambiguous-licence data (Numo, Kathbath, SLR104) | **Not used**; only clearly-licensed sets |
| 8 A100 or large GPU boxes, ~255 GPU-hours (~$650 total) | **Free tier for Week 1**, then ~70 GPU-hours on cheap spot GPUs (**~$50-150**) |
| English fine-tune of a 600M model | English model **measured**, trained only if clearly weak |

---

## 3. The models

| For | Starting model | Size | Licence (per audit) | What we do |
|---|---|---|---|---|
| **Hindi** | AI4Bharat **IndicConformer Hindi** (`ai4bharat/indicconformer_stt_hi_hybrid_ctc_rnnt_large`) | ~120M (conformer-Large encoder, 17 blocks, hybrid CTC/RNNT) | MIT tag; default contact-sharing gate | Fine-tune (two variants, see Section 6) |
| **Telugu** | IndicConformer Telugu (`..._te_...`) | ~120M | MIT tag; default gate | Same |
| **English-India** | Best of a small shootout: NVIDIA Parakeet-TDT-0.6B-v2 (CC-BY-4.0), Parakeet-TDT-0.6B-v3 (CC-BY-4.0), Whisper small/medium (MIT), Moonshine English (MIT), a ~110M NVIDIA English model (licence not yet checked) | 27M to ~600M | See audit report Section 5 | **Measure first; train only if clearly weak** |

**Reference models we only measure (never ship):** untouched IndicConformer (our baseline to beat) and Svanita (`prasadvittaldev/svanita-0.6b`, an offline Parakeet-TDT-v3 fine-tune; CC-BY-4.0 tag; the author's own numbers are unverified).

**Needs:** AI4Bharat's NeMo fork (`github.com/AI4Bharat/NeMo`, branch `nemo-v2`, `reinstall.sh`) to load or train IndicConformer. English candidates use standard NeMo, `transformers` or sherpa-onnx tooling.

**Not used:** Nemotron-3.5 (streaming, no Telugu tokens), Kyutai STT (no training code), MMS, Parakeet-1.1B Indic, Indic-Transcribe, SraVaani (unclear data chain), Omnilingual (see audit report).

---

## 4. The data (what we train and test on)

### 4.1 Training mix (~300 h per language) [P, not yet tested]
| Language | Source | Hours used | Licence status (audit) | Notes |
|---|---|---|---|---|
| **Hindi** | IndicVoices | ~120 | CC-BY-4.0 (clearly safe) | Natural phone speech; total available ~0.8k h [E] |
| | Vaani | ~100 | CC-BY-4.0 | 1,004 h transcribed available [M] |
| | RESPIN (Hindi clean) | ~65 | CC-BY-4.0 per IISc README | Read speech; only ~19k unique sentences, so **cap repeats per sentence** |
| | Common Voice (Hindi) | ~15 | CC0 | 15.7 h validated available |
| **Telugu** | IndicVoices | ~130 | CC-BY-4.0 | Total available ~0.5k h [E] |
| | Vaani | ~120 | CC-BY-4.0 | 184 h transcribed available [M] |
| | RESPIN (Telugu clean) | ~50 | CC-BY-4.0 per IISc README | Same repeat cap; 1,021 h available |

**Not used in this plan:** Numo, Kathbath, SPRING-INX, SLR104, bolAIndia, Shrutilipi, NPTEL, anything with a conflicting or hidden licence. Code-mixed audio comes from the sets above (about 20 h per language mined) and is not bought or synthesised.

### 4.2 Cleaning rules (apply to every clip)
- Convert to 16 kHz mono WAV. Drop clips that are too short or too long (proposal: under 1 s or over about 20 s [P]).
- One frozen text normalizer (NFC, strip punctuation, collapse spaces, ASCII digits), written on Day 4, hashed, and used for every score. **Never use Whisper's normalizer for Hindi or Telugu.**
- **Speaker-disjoint split:** no speaker appears in both training and test data.
- Remove any training clip whose audio or text also appears in a test set.
- **English words inside Hindi/Telugu stay in native script** (decision D-023, e.g. मीटिंग), which is what IndicConformer already outputs. Use the plain transcript columns (IndicVoices `text`/`normalized`; RESPIN text; Common Voice text). For Vaani, strip the `{english}` brace tags and keep the native-script word. No tokenizer change and no Latin-letter extraction.

### 4.3 Test sets (never trained on)
| Purpose | Set | Size |
|---|---|---|
| Clean read speech | FLEURS Hindi / Telugu / English | 8.7 h / 10.3 h / 10.3 h [E] |
| Natural speech | Vaani-Benchmark-V1.0 (Hindi, 3 reference transcripts) | ~10.9 h |
| Hindi accents | Lahaja | ~12.5 h |
| Noise and phone-style audio | `google/svq` (Hindi, Telugu, English locales) | test split only |
| Indian-accent English | Svarah; Common Voice en-IN slice | ~9.6 h; slice |
| **Our own recordings** | In-house set, colleagues, phone and laptop mics, some noise, code-mixed sentences | **~1 h per language** [P] |

Scores to report per language: strict WER, CER (headline for Telugu, which has long words), and a separate score on sentences containing English loanwords written in native script. Spelling variants of the same loanword (for example कंप्यूटर and कम्प्यूटर) inflate WER, so report with and without spelling-variant folding, and use the multi-reference Vaani-Benchmark for Hindi. Include speaker-level confidence intervals where the sample allows.

---

## 5. The pipeline, day by day

### WEEK 1: free tier, $0 (prove the plan works before spending)

**Day 1. Access and setup.**
- Accept the Hugging Face gates (under the account the owner and senior agree on): IndicConformer Hindi and Telugu, IndicVoices, Vaani. Capture dated screenshots into `evidence/`.
- Set up Colab or Kaggle; install the AI4Bharat NeMo fork (fiddly; budget time). File the AWS GPU quota request now.
- Check the RESPIN Download tab (how files are obtained) and any forms. Do not submit anything without the owner's decision.
- Fix the Colab/Kaggle environment versions in `progress.md`.

**Day 2. ONNX export smoke test (Gate A).**
- Convert the **untouched** Hindi and Telugu models to ONNX (start with the CTC head), run them in sherpa-onnx, and compare their text with the original NeMo output on about 20 clips.
- **Pass:** transcripts match within 0.5 absolute WER [P].
- **Fail:** use the fallbacks (Section 8): ONNX Runtime directly, CTC-only export, copy the community converters, PyTorch's own exporter, or a different runtime.

**Day 3. Baselines (no training).**
- Score the untouched IndicConformer Hindi and Telugu on FLEURS, Vaani-Benchmark (Hindi), Lahaja and the noisy `svq` set.
- **English shootout** (about $0): run the 3-4 candidates on Svarah, Common Voice en-IN and FLEURS English; record accuracy and model size.
- Optionally score Svanita on a slice (large, slow on CPU; low priority).

**Day 4. Our test set and the normalizer.**
- Record ~1 h per language from colleagues (phone and laptop mics, some background noise, a few code-mixed sentences). Write consent wording (voice recordings are personal data).
- Write and hash the normalizer.

**Day 5. Tracer fine-tune (Gate B).**
- Fine-tune each model for a few minutes on 10-20 h (vocabulary unchanged), **export the fine-tuned checkpoint, run it in sherpa-onnx, and confirm it decodes.** This proves a fine-tuned model still converts (lower risk now that the vocabulary is unchanged).
- **Weekly decision:** with Gates A and B, the owner brings the senior the evidence and asks for the small capped budget for Week 2.

### WEEK 2: data prep and training (paid, small)

**Days 6-7. Data prep.**
- Download only the slices we need (never the full archives; IndicVoices full archives are ~150 GB Hindi and ~141 GB Telugu; RESPIN Telugu clean is ~118 GB [E]).
- Apply the cleaning rules in 4.2; build manifests (JSONL: audio path, duration, text, language, source); make the speaker-disjoint split; de-duplicate against the test sets.
- Native-script targets only (D-023); strip Vaani's `{english}` brace tags.
- Write the data card (hours per language and source, licence, manifest hash) and update the licence manifest.

**Days 8-9. Training: 2 core runs (1 per language) plus 2 optional runs with different settings.**
- **Core run (per language):** keep the native-script vocabulary unchanged; train all layers on the ~300 h with noise and phone-style augmentation. Aim: lower error and noise robustness.
- **Optional second run (per language), if budget allows:** same data with a different learning rate (for example 1e-4 versus 5e-5) or with and without the noise augmentation, as insurance. (The Latin-letter variant was dropped, D-023.)
- Settings as a starting point [P]: learning rate about 1e-4 to 5e-5, cosine schedule; SpecAugment; speed perturbation 0.9/1.0/1.1; about 6 passes over the data; batches by audio duration; save a checkpoint every 15-30 minutes; average the last few checkpoints at the end.
- Run on spot GPUs; if one dies, resume from the last checkpoint.

**Day 10. Scoring (Gate C).**
- Score every trained model on every test set and on our own recordings.
- **Pass:** at least one model per language beats its untouched baseline by **>= 10% relative on our in-house set and the noisy set**, with **no more than 5% relative loss on clean FLEURS** [P]. Also: no invented text on silence (insertions on silence/noise clips <= 3%) and correct script (>= 0.98) [P].

### WEEK 3: finish

**Days 11-12. Pick, export, test.**
- Pick the best model per language. Allow **one** rerun per language to fix what Gate C showed.
- Export to ONNX; verify parity against NeMo on 20 clips; test in sherpa-onnx. Test **int8** only if size or speed needs it (it is optional; Prasad's int8 failure was specific to his model and export). Measure speed and memory on the target devices (Q20: still unconfirmed).
- A 120M model in full precision is about 0.5 GB; a community Hindi build ran at about 16x real time on CPU [V/community].

**Day 13. English.** Record the shootout result. If the best English model is clearly weak on Indian accents, note the small fine-tune plan (Common Voice en-IN ~170-220 h, Vaani English 22 h) as next work; do not start it unless time and budget remain.

**Days 14-15. Report and hand-off.**
- Report: baseline vs trained numbers per language and test set; what worked and what didn't; export and speed results; licence status of every dataset and model used.
- Demo: a script that takes a recording and prints the transcript in each language; instructions for choosing the language (the user picks, or a language-detection step is added later).
- Shut down all AWS resources; update `progress.md`.

**Days 16-21. Buffer** for whatever slipped (NeMo fork setup, a failed export, spot interruptions).

---

## 6. Compute and cost [E, speed unmeasured; ~2x uncertainty]

**Where things run**
- **Week 1:** free Colab or Kaggle (a T4-class GPU, ~100 GB disk, session limits; free-tier limits are [U]). CPU only for export and sherpa-onnx tests.
- **Week 2-3 training:** AWS **spot** GPU instances in bursts: `g5.xlarge` (1x A10G, ~$0.43-0.52/h spot in earlier snapshots) or `g5.2xlarge` (8 vCPU, 32 GiB, $1.212/h on-demand) if data loading is the bottleneck. Never leave an instance idle; add an auto-stop at the end of every launch script and an idle watchdog.
- **A100s are not needed** for 120M models; a p4d.24xlarge (8x A100 40 GB) costs ~$21.96/h, so ~$11,000 if left on for three weeks (price-tracker figures; verify on AWS).

**Work estimate:** each run is about 300 h x 6 passes = 1,800 audio-hours; at ~150 audio-hours per A10G-hour [E] that is ~12 GPU-hours. 2 core runs = ~24; 2 optional second runs = ~24; tracer and reruns ~6; scoring/export ~7. **Total ~37 GPU-hours with only the core runs, ~61 with the optional second runs** (down from ~70 before D-023).

| Item | Cost |
|---|---|
| Week 1 on free Colab/Kaggle | $0 |
| ~37-61 GPU-hours | ~$16-32 spot; ~$37-74 on-demand |
| Storage (~200 GB for 3 weeks; S3 + temporary EBS) | ~$11 [U, general AWS pricing] |
| Contingency (30%) | ~$10-26 |
| **Total** | **~$35-110** (about $100 or less in most cases) |

**Not included:** colleagues' time for recording the test set; engineer time; legal review; devices. English training (if needed) adds ~$100 for a 600M model [E].

---

## 7. Licences and what we may say about the demo
- Use **only clearly-licensed data**: IndicVoices, Vaani, RESPIN (CC-BY-4.0 per IISc's README), Common Voice (CC0). Keep a licence manifest (dataset, version, date, licence text, gate text, attribution) in `legal/` or `evidence/`.
- **Attribution (CC-BY):** credit AI4Bharat, ARTPARK-IISc, IISc, NVIDIA (if Parakeet is used), Mozilla (Common Voice).
- Accepting a Hugging Face gate shares the account's email and username with the authors; the owner and senior should decide which account accepts.
- IndicConformer is tagged MIT on every repo read, but **AI4Bharat has not confirmed in writing** commercial use, fine-tuning, or use of outputs as labels. We do not use IndicConformer outputs as training labels in this plan.
- Nothing is sent to any licensor without the owner's explicit go-ahead. Drafts are in the audit report Section 10.
- Describe the 3-week result as an **internal demo**. Commercial release needs the confirmations first.

---

## 8. Risks and fallbacks

| Risk | What we do |
|---|---|
| AI4Bharat NeMo fork won't install on Colab | Try Kaggle or a small AWS instance; pin versions; start Day 1 |
| ONNX / sherpa-onnx conversion fails (Gate A or B) | ONNX Runtime directly with our own decoding; CTC-only export; community converters' code; PyTorch's exporter; another runtime (Core ML, GGUF); last resort Parakeet-TDT (better-documented export, sherpa support unverified) |
| Telugu improves only slightly with ~300 h | Report honestly; add RESPIN hours (cap repeats); use the spare buffer for one extra run |
| Data downloads are slow or too large | Download slices only; stream; verify disk space on Day 1 |
| Spot machines are interrupted | Checkpoint every 15-30 min; sync to S3; auto-resume |
| (Retired) IndicVoices English-pair extraction | No longer relevant: native-script output chosen (D-023) |
| Gates or RESPIN access are delayed | Raise on Day 1; the senior's yes on access is on the critical path |
| Free-tier limits run out | Move the spike's heavy parts to a small AWS instance (a few dollars) |
| Licence questions open | Keep the demo internal; keep the manifest; wait for written answers before any release |
| Our own estimates are wrong by 2x | Week 1 measures speed; re-issue this cost table after the tracer run |

---

## 9. Decisions and inputs needed

1. **Q10: answered (D-023):** English words inside Hindi/Telugu stay in native script; no Latin-letter variant.
2. **Senior's approval** for dataset access and the small capped budget (~$50-150), ideally on Day 1-5 with Gate A/B results.
3. **AWS:** region, whether spot is acceptable, any existing savings plan, who files the GPU quota request.
4. **RESPIN Download tab text** (how files are obtained; any form).
5. **Devices (Q20):** which phones and laptops, how much RAM (decides int8 and model size).
6. **Accuracy targets (Q22)** from the senior (the gates above are our proposals).
7. **Language selection in the app:** the user picks the language, or we add a language detector later.
8. **Which Hugging Face account** accepts the gates.

---

## 10. How this plan connects to the logs
- Every day's work, number and decision goes into `progress.md` (activity log, run registry, benchmark registry, data ledger, legal tracker, budget ledger) as described in its Section 0 and the session-close checklist.
- If this plan changes (a threshold, a dataset, a model), log a decision first, then edit this file and note the change at the top.
- The older plan (`pipeline.md`) is not edited by this plan.
