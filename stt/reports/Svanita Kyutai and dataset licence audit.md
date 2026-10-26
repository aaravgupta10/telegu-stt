# Svanita, Kyutai, base models and datasets: licence and feasibility audit for a commercial on-device Hindi / Telugu / English-India STT

**Facts checked: 2026-10-12. Method: read-only (public pages, HF/GitHub/PyPI APIs, arXiv, AIKosh, OpenSLR). Nothing was downloaded, no login was used, no gate was accepted, nobody was contacted.**
**Risk tiers in this report are engineering risk tiers, not legal advice. Counsel should review the decisive items (Section 5.2 Nemotron chain; Section 6 T2 datasets we actually train on; Kyutai/NVIDIA upstream-data residual risk).**

Evidence labels (as in `CLAUDE.md`): **[M]** read or measured from a cited primary source; **[V]** vendor/author claim; **[E]** our estimate or arithmetic; **[P]** proposal, not validated; **[U]** unverified or unreadable; **[OURS]** our own read of a public page/API (no runs were made). Tier legend: **T1** clearly safe, **T2** usable with documented caveats, **T3** unresolved (do not train until answered in writing), **T4** unusable for a commercial model. Where sources disagree the more restrictive reading is used.

Inputs: six research notes in `research_notes/Svanita Kyutai and dataset licence audit/` (`svanita_prasad.md`, `kyutai_repos.md`, `models_tools_licences.md`, `datasets_ai4bharat.md`, `datasets_other.md`, `datasets_discovery_inventory.md`), `progress.md` (A-015 to A-018), `research_notes/context_from_normal_chats_2026-10-12.md`, and the earlier report/notes (read only to state what changes). This report does not edit `pipeline.md`; Section 8 is recommendations only.

---

## 1. Executive summary

1. **Svanita is real, public and ungated, but it is not what the senior thinks.** It is a single-person fine-tune of NVIDIA Parakeet-TDT-0.6B-v3 (not Kyutai), offline (whole-utterance, not streaming), 622M parameters, fp32 only, trained on 1,136 h of AI4Bharat IndicVoices + Kathbath (Telugu 451 h, Hindi 685 h) on one RTX 5060 Ti 16 GB [V, author card]. Tagged CC-BY-4.0. The author's own table says IndicConformer-600M is more accurate (Hindi 15.5 vs 23.7 WER; Telugu 27.4 vs 37.7) and that int8 and ONNX conversions broke accuracy.
2. **Svanita verdict:** (a) as a base model to fine-tune: legally plausible, technically pointless (same public base + same public data; offline; int8-hostile); (b) as a baseline to beat: yes, cheap and useful; (c) as a pseudo-label teacher: weak. Provenance is thin (19 days old, no code, no manifests, no NOTICE; the v0.2 card dropped the v0.1 attribution section).
3. **The "Kyutai + consumer GPU + ~120 h" story is the TTS project.** Prasad Vittaldev's Telugu Pocket TTS (124 h teacher fine-tune, then a 6-layer student on one speaker's 53 h) is published as a single-voice ~110M model. The "3 voices / 316M / 3.39x on 2 cores" wording of the LinkedIn post does not match the HF card.
4. **Kyutai STT cannot be our base.** No Kyutai repo contains STT training code (34 repos, 45 DSM branches checked); the maintainer said on 2026-03-23 that none will be released; the models are 1B/2.6B, English/French (or English) only, GPU (CUDA) or Apple MLX; best community x86 laptop-CPU result is 0.24x to 0.67x real time; no Android path. The senior's belief that an STT release sits in the pocket-tts repo is false [M]: that repo is TTS-only.
5. **Kyutai TTS is a credible separate option if TTS is in scope.** Pocket TTS training code was released August 2026 (MIT code; weights CC BY 4.0, gated with a prohibited-use text); community Hindi and Telugu builds exist; CPU speeds 3x to 6x real time. "Swap in Telugu data" is roughly true for TTS (GPU time in hours, real work is aligned licence-clean data, a Telugu CTC aligner, evaluation), false for STT.
6. **Nemotron-3.5-ASR-Streaming-0.6B licence is resolved: OpenMDW-1.1 for the Hugging Face weights.** It is about as permissive as model licences get (no field-of-use limit, no share-alike, outputs unrestricted; duty = keep the agreement and notices when distributing). The "NVIDIA Open Model License" label comes from launch-day metadata (fixed 2026-06-05) and from the NIM/Together AI channel. Archive a dated copy; ask NVIDIA to confirm in writing; residual upstream-data risk sits with us.
7. **Telugu is not in Nemotron-3.5 and the tokenizer has zero Telugu characters** (13,087 BPE tokens; 196 Devanagari; 2,567 Latin). There is no CTC head. NVIDIA documents a new-language route (new tokenizer, merge, `update_tokenizer=true`, RNNT decoder retrained from scratch, encoder kept) and reserves a `te-IN` prompt slot (id 40), but gives no hours or hardware for it, and NVIDIA's own toy run reached only ~60% WER. The "few hundred hours" figure is not in any NVIDIA source read here.
8. **Teachers:** IndicConformer (MIT) and Nemotron-3.5 (OpenMDW; Hindi only) are usable; SraVaani (MIT tag + unread gate) is amber; **Parakeet-1.1B Indic (community licence forbids using outputs to improve other models) and Bodhan Indic-Transcribe (share-alike; "trained substantially on output" = derivative) should be avoided**; MMS, SeamlessM4T, canary-1b are non-commercial.
9. **Data position: Hindi is not a constraint; Telugu volume is no longer the binding limit but spontaneous Telugu diversity is.** Clearly licensed transcribed hours (low / best / high, Section 6c): Hindi ~1.5-1.9k / ~3.2k / ~5.1k; Telugu ~0.55-0.7k / ~1.9-2.0k / ~3.4-3.5k; English-India ~0.05k / ~0.25k / ~0.35k. About two thirds of the Telugu "best" is read, narrow-domain speech (RESPIN, SYSPIN) and RESPIN/Numo are T2.
10. **Code-switch: no large clearly licensed real corpus exists for Hindi-English or Telugu-English.** Hindi-English: HiACC 5.24 h (CC BY 4.0), SLR104 89.9 h (BY-SA). Telugu-English: nothing released (Microsoft Research's 243 h set is not public; a "200 h" forum claim is untraceable). We must mine Vaani (English kept in braces, e.g. `ट्रक {truck}`), SPRING-INX (Hindi, Latin retained), IndicVoices, and synthesise.
11. **"Datasets come clean as audio+transcript pairs" is only true of the pairing.** English words are written in native script in IndicVoices/Kathbath/RESPIN, in braces in Vaani, tags and punctuation conventions differ, labels carry errors, splits are missing (Vaani, IndicVoices test), and licence labels conflict on Kathbath, IndicVoices-R, Lahaja, SPRING-INX, IndicTTS and every aggregator.
12. **What must be asked or confirmed (nothing sent):** NVIDIA (OpenMDW on both channels; data clearance; Telugu route), AI4Bharat (IndicVoices/Kathbath commercial scope; IndicConformer gate), ARTPARK-IISc (SraVaani/Vaani gate terms), IISc SPIRE (RESPIN licence in writing), Poseidon (Numo consent), Prasad Vittaldev (data statement, commercial confirmation), Kyutai (voices/data provenance, only if TTS). Section 9 lists what needs the owner's browser; Section 10 has copy-ready drafts.

---

## 2. The senior's claims versus the evidence

Source of claims: WhatsApp 9 Oct as relayed in `context_from_normal_chats_2026-10-12.md` [U, second-hand]. Offered diplomatically: each claim has a true core that explains how it arose.

| Claim | Verdict | Evidence |
|---|---|---|
| Kyutai's architecture for STT is a good fit ("versatile on many devices") | **Partly true for TTS, false for STT** | Kyutai STT is a decoder-only Transformer over Mimi codec tokens at 12.5 Hz with delayed text streams; `stt-1b-en_fr` (0.99B, 0.5 s delay) and `stt-2.6b-en` (2.6B, 2.5 s delay) [M]. Official runtimes: PyTorch research, Rust/CUDA server, Apple MLX. Kyutai's own STT page speaks of H100/L40S servers, nothing about laptop CPUs [V]. Community CPU numbers: 3.0-8.4 frames/s against 12.5 needed (moshi.cpp alpha), 0.6x (f32) to 2.1x (q4) real time on Apple M-series CPU; WASM ~1.3x on a MacBook; "mobile not supported" [C]. The phrase "versatile on many devices" was not found anywhere; Pocket TTS ("runs on your laptop, no GPU", ~100M) is the likely source [M for Pocket TTS, U for the buzz]. |
| Prasad trained the STT on a consumer GPU with ~120 h of data | **Half right: consumer GPU yes; 120 h and Kyutai no** | Svanita: one RTX 5060 Ti 16 GB, **1,136 h** (Telugu 451 h, Hindi 685 h), NVIDIA Parakeet base [V, card]. The 124 h figure belongs to the Telugu Pocket TTS teacher fine-tune [M, card]. The TTS card does not state the GPU. |
| Swap in Telugu data and have a PoC in an hour or two on 8 GPUs | **TTS: GPU part yes, whole job no. STT: no** | TTS: Kyutai's `training/` code (Aug 2026) with `finetune_language.yaml`; Telugu build used 15,000 teacher steps + 40,000 distillation steps [M, card]; at Kyutai's published H100 step rates that is well under an hour of GPU for the teacher and about an hour for the student [E]; slower on consumer/A10-class cards [U]. The work that takes days is aligned licence-clean data, a Telugu CTC aligner (Meta MMS is unusable: it romanises), tokenizer/EOS/punctuation fixes, listening tests. STT: no training or fine-tuning code exists; maintainers: needs a few thousand hours of word-aligned audio, a new tokenizer, and they "don't know" how unseen languages behave [M]. A loop-runs smoke test in minutes (LoRA hack on `moshi-finetune`) says nothing about Telugu WER. |
| An STT code release exists in the pocket-tts repo | **False** [M] | Full tree and branches contain no STT/ASR module. `training/` is TTS-only; its only ASR-adjacent items are a CTC forced aligner and a WER-judge script for TTS evaluation. STT inference lives in `delayed-streams-modeling` (inference only) and `moshi`. |
| Kyutai is versatile on many devices | **True for Pocket TTS, false for Kyutai STT** | Pocket TTS: ~6x real time on a MacBook Air M4 using 2 cores [V]; community Hindi int8 3.74x / 6.3x on one server thread [V]; Prasad's Telugu student 5.5x int8 desktop [V]. STT: see row 1; the only phone evidence is an iPhone 16 Pro MLX demo (GPU, Apple only). |
| Datasets come as audio+transcript pairs, already clean | **Pairs yes; clean no** | Pairs: yes for every set we would train on. Not clean: native-script English (IndicVoices, Kathbath, RESPIN), brace-annotated English (Vaani), noise tags, no punctuation, reported label errors (Kathbath, IndicVoices discussions), alignment noise (Shrutilipi), contamination between sets, absent test splits, speaker overlap, conflicting licences, HF gates, and aggregator re-uploads with false licence labels (Section 6). |

---

## 3. Svanita and Prasad Vittaldev

### 3.1 What it is [M unless marked]

| Item | Finding |
|---|---|
| Location | https://huggingface.co/prasadvittaldev/svanita-0.6b; the lnkd.in short link resolves to exactly this repo. Not gated. `main` = v0.2 (2026-09-24), branch `v0.1` (2026-09-19). 340 downloads, 2 likes, 0 discussions, no derivatives on the Hub (2026-10-12). |
| Author | Hugging Face user created 2024-02-22; no organisation, bio, employer or email; GitHub shows a long-time Asterisk/FreePBX/WebRTC/Django telephony background; no paper, blog, talk, or independent mention found. Employer unknown [U]. They/them used here since pronouns are not stated. |
| Model | Parakeet FastConformer encoder (24 layers, d=1024, 8 heads, 8x subsampling, 128 mel) + TDT decoder (2-layer LSTM, 640), 621.8M params, `model.safetensors` 2.49 GB F32. Pure TDT, no CTC head. |
| Base | `nvidia/parakeet-tdt-0.6b-v3` (25 European languages, no Hindi/Telugu). v0.2 = v3 -> Telugu tuning (v0.1) -> Telugu+Hindi tuning. |
| Tokenizer | New 4,097-piece SentencePiece Unigram (Telugu + Hindi + Latin transcripts). Our count from `tokenizer.json`: ~1,709 Telugu, ~1,643 Devanagari, ~742 Latin pieces [OURS]. Only the decoder embedding and joint output (~5.3M params) were re-initialised; the 609M encoder was kept. |
| Streaming | **No.** Whole-utterance full-attention encoder; `transcribe_cpu.py` has no chunking or cache; never trained or tested with chunking. The "turn" in the posts is a complete 3-6 s clip. |
| Output convention | Native script for native words, Latin for English words, lowercase, no punctuation. Latin targets were derived from IndicVoices' `native [english]` annotation (e.g. `टाइम [time]` -> `time`) [V]. 46% of Telugu and 39% of Hindi training clips contain Latin English [V]. |
| Data | `ai4bharat/IndicVoices` + `ai4bharat/Kathbath` only. 625,184 clips: Telugu 451 h / 241,291 clips / 1,691 speakers; Hindi 685 h / 383,893 clips / 1,941 speakers [V]. 125,297 Hindi and 76,692 Telugu clips dropped for speaker overlap with validation splits. No pseudo-labels, no other corpora, no English-only audio (hence weak pure English). ~40% of clips degraded to 8 kHz telephone (noise corpus unstated). |
| Recipe | Three stages on one RTX 5060 Ti 16 GB: encoder-frozen head training (27,500 steps, 8-bit AdamW), full fine-tune (61,815 steps), Telugu-weighted top-up (12,000 steps; shipped step 10,000). bf16, gradient checkpointing, SpecAugment. GPU time, batch size, seed, cleaning rules not stated [V]. |
| Not published | Training/eval code, manifests, speaker lists, normaliser, `.nemo`, ONNX, int8, LICENSE/NOTICE. |

**Cross-check on IndicVoices hours [E]:** the card's clip counts imply ~6.4-6.7 s per clip. Using that, the pre-drop pool is roughly 900 h Hindi and 590 h Telugu including Kathbath, which suggests IndicVoices Hindi ~0.75-0.8k h and Telugu ~0.45k h, i.e. the upper (examples-anchored) end of the AI4Bharat note's range (Section 6c). Assumes uniform clip length; a `duration` sum after access settles it.

### 3.2 Licence chain [E, not legal advice]

Parakeet v3: CC-BY-4.0 (card: "governed by the CC-BY-4.0 license") [M]. Svanita: `cc-by-4.0` tag; the v0.1 card carried a "Licence and attribution" section crediting NVIDIA, IndicVoices and Kathbath; **the v0.2 card dropped it** and there is no NOTICE [M]. IndicVoices and Kathbath: HF tag `cc-by-4.0` [M]; the gate text on the AI4Bharat datasets is HF's default contact-sharing text, not a custom terms prompt (Section 6a). Reading: commercial use permitted with attribution to Prasad Vittaldev, NVIDIA and AI4Bharat; not "clean" until the author confirms in writing and AI4Bharat answers the Section 10 questions. Svanita adds no new data-licence exposure beyond what we take on by using AI4Bharat data ourselves, and no data advantage. Voice data of identifiable speakers raises DPDP-Act questions that CC-BY does not settle [U].

### 3.3 Numbers (author's, unverified) and how they compare [V]

Every metric is `verified: false` on HF; no third-party reproduction. Test sets are the author's "speaker-disjoint half" of IndicVoices `valid` (Hindi 2,599 clips / 4.19 h; Telugu 1,499 clips / 2.34 h): tiny, in-domain, no confidence intervals. Same normaliser for all systems (NFC, punctuation stripped, Latin lowercased). Baselines are vasista22 Whisper-large-v2 language fine-tunes and AI4Bharat IndicConformer-600M run by the author.

| WER % (either-script / Latin-required) | Svanita v0.2 | IndicConformer RNN-T | Whisper-large-v2 FT |
|---|---|---|---|
| Hindi IndicVoices | 23.7 / 23.8 (CER 13.6) | **15.5** / 20.6 (CER 16.1) | 37.3 / 40.0 |
| Hindi 8 kHz telephone copy | 26.5 | **17.6** | 45.2 |
| Hindi Kathbath read | 25.4 | **8.9** | 11.7 |
| Telugu IndicVoices | 37.7 / 38.0 (CER 17.0) | **27.4** / 39.1 (CER 22.1) | 44.0 / 52.3 |
| Telugu Kathbath read | 39.7 | **20.9** | n/a |

Svanita is ahead only on Latin-required WER (Telugu essentially tied) and CER, and keeps English in Latin script on 73-74% of occurrences versus 0% for the Whisper fine-tunes (which emit native script by construction, a convention difference). **Offline vs streaming:** Svanita's latency (3 s clip in 275 ms at 8 threads; 3.6 s in 326 ms; 6.4 s in 515 ms; Ryzen 5 8600G desktop, fp32) is time to decode a complete clip, not streaming latency, and not a laptop/low-power CPU. **int8/ONNX failure reports [V]:** PyTorch dynamic int8 doubled speed but raised dev WER from 38.6% to 69.3% (v0.1); an ONNX export gave 48.3%; the author recommends fp32. A naive dynamic-quantisation of LSTM/joint is not proof that careful static/QDQ int8 fails [E], but it is a warning for any TDT-style export.

### 3.4 Reconciliation with the LinkedIn-derived claims

| Claim in context file | Status |
|---|---|
| Svanita is NVIDIA-based, not Kyutai; FastConformer + TDT, ~620M, CC-BY-4.0, 16 kHz mono | **Right** [M] |
| v0.1 "Telugu + English" | **Imprecise:** v0.1 is Telugu with English words kept in Latin; pure English is poorly supported (no English-only audio). v0.2 = Telugu + Hindi [M] |
| 3 s in ~0.28 s (v0.1); ~350 ms (v0.2) | **Right** (275 ms / 326-387 ms for 3.6-3.9 s clips); the "10-12x real time" is consistent with the card; not streaming [M] |
| Hindi WER 23.7 vs Whisper FT 37.3; telephone 26.5 vs 45.2; IndicConformer 15.5 | **Right**, match the card exactly [M] |
| "73-74% English retained on code-mixed clips" | **Imprecise:** 73%/74% is over the full IndicVoices test halves, not only code-mixed clips [M] |
| "No Telugu numbers; no test set, data, hours or hardware stated" | **Wrong for the HF card:** Telugu WER 37.7 (v0.2) / 36.5 (v0.1) vs IndicConformer 27.4 is on the card, as are the test set, 1,136 h, sources and the RTX 5060 Ti. The LinkedIn posts may omit them |
| Not true streaming | **Right** |
| Not monolingual | **Right** (v0.2 is Hindi+Telugu in one checkpoint) |
| Telugu Pocket TTS: 124 h, single consumer GPU | **124 h right**; GPU not stated on the TTS card [M] |
| Telugu Pocket TTS: 3 voices, 24-layer 316M, int8 3.39x on 2 cores, "models on HF shortly" | **Not matched.** Found: `prasadvittaldev/pocket-tts-telugu-female-syspin` (created 2026-09-02, after the 30 Aug post), MIT tag, ~110M 6-layer **single fixed female voice**, int8 5.5x real time on a desktop x86 CPU, ONNX 3.98x (int4) / 4.08x (int8) on 4 threads. The 24-layer teacher (consistent with Kyutai's ~313M figure [E]) is not published; no 3-voice Telugu repo exists [M] |

### 3.5 Telugu Pocket TTS facts [M card, V numbers]

Recipe (Kyutai's own `finetune_language.yaml` + `depth_distill.yaml` path, Section 4.2): 24-layer English teacher fine-tuned on 124 h Telugu for 15,000 steps with a new Telugu tokenizer; native-script forced alignment (Meta MMS aligner rejected: it romanises); distilled to 6 layers for 40,000 steps on one speaker's 53.0 h / 20,599 clips. Voice cloning is lost in the student. No WER/CER/MOS on the card. **Data:** `SPRINGLab/IndicTTS_Telugu` (IIT Madras IndicTTS, ~8.74 h, 2 speakers, no HF licence tag, original licence PDF unread) and `arpit-tiwari/syspin-telugu-tts` (a third-party re-upload of IISc SYSPIN, no licence text). The 124 h cannot be reconciled from these two (8.7 h + SYSPIN) because no hours breakdown is given. The card says "MIT, matching upstream pocket-tts", while the weights it was fine-tuned from (`kyutai/pocket-tts`) are CC BY 4.0 with a gated prohibited-use text; the card tells users to check the corpora's licences before commercial use. Sister models: Hindi (131 h teacher), Tamil (164 h from a single audiobook narrator of unstated provenance: highest legal risk), Indian-English (246 h IndicTTS-English), plus ONNX repacks.

### 3.6 Verdict and questions

| Role | Verdict |
|---|---|
| (a) Base model | Legal-ish yes; practical value low. Same public base and data; offline; 2.49 GB fp32; int8 reported broken. Possible value only as a warm-started Indic encoder to save perhaps 1-2 A10G-days [E], at the cost of inheriting unknown cleaning choices and an offline-trained encoder (Section 8). |
| (b) Baseline | **Yes.** Re-measure on our test sets and our normaliser [OURS pending]; never quote the author's numbers as ours. Beating it on accuracy is a low bar (IndicConformer is the real accuracy reference); its distinctive features to match are Latin-script English output and telephone robustness. |
| (c) Teacher | **Weak.** Worse than IndicConformer in both languages, no punctuation, thin English. Only possible niche: a Latin-English labelling helper on code-mixed audio, filtered against IndicConformer. |

**What to ask the author (not sent; see Section 10):** written commercial/fine-tune/teacher confirmation and attribution wording; dataset versions and gate acceptance; the exact valid-split rule; manifests; training/eval scripts and normaliser; the exact int8/ONNX setup that failed; whether the 24-layer Telugu teacher and the licences of the 124 h will be published.

---

## 4. Kyutai

### 4.1 Kyutai STT (`delayed-streams-modeling`, `moshi`, `moshi-finetune`)

| Topic | Finding |
|---|---|
| Training code | **None** in any of 34 org repos; DSM has no `train/` or `finetune/`, 45 branches, 64 closed PRs, none adds it [M]. DSM FAQ still says some fine-tuning code is in `moshi-finetune`, but that code targets Moshi 7B speech-to-speech and has not been adapted to STT/TTS. |
| Maintainer statements (DSM issue #4, paraphrased) | Roughly a few thousand hours of time-aligned audio would be needed; the model was pretrained on >1M h of English and French; the tokenizer would have to change; they do not know what happens for a language absent from pretraining; fine-tuning "requires significant effort" on both sides. A smaller multilingual STT base was announced July 2025 and **never released** [M]. **2026-03-23:** no plan to release fine-tuning code for Pocket TTS, Kyutai TTS 1.6B or Kyutai STT [M]. |
| Community path | An unofficial patch on `moshi-finetune` (drop the audio loss, skip depformer, mono 30 s windows) reportedly runs in minutes on an L40S for a 3-file test [C]. Failure reports: PAD collapse after ~60 s with an extended 16k tokenizer, a degenerate repetition loop [C]. **Only one public new-language STT fine-tune exists:** `mideind/kyutai-stt-1b-is-en` (Icelandic, Latin script, 5 s delay, "not production-grade", hours/GPU/recipe undisclosed) [C]. A Hindi Moshi attempt (400 h stereo synthetic) has no reported result. |
| Sizes and runtime | 1B / 2.6B; 2.0-5.1 GB at F16, 636 MB (1B Q4_K) to 1.5 GB (2.6B Q4_K) in community GGUF [C]. Official: CUDA Rust server, PyTorch, MLX. CPU: moshi.cpp (alpha) 3.0 (i7-6700T) to 8.4 (Ryzen AI MAX+ 395) frames/s vs 12.5 needed [C]. No Android path. |
| Token density | At 12.5 Hz, fast-spoken or long-token languages were flagged by maintainers as possibly needing a faster codec frame rate (issue #171); byte-fallback tokenisation of non-Latin scripts explodes token counts (issue #64 commentary) [M/C]. Telugu/Hindi are exactly that case [E]. |
| Compute for a 1B full fine-tune | Memory roughly 16-24 GB/GPU [E, very rough]; Kyutai's own fine-tune used 16 H100 for 100k updates on 28k h [M]; A10 throughput unmeasured [U]. |

### 4.2 Kyutai TTS (Pocket TTS)

| Topic | Finding |
|---|---|
| Training code | **Yes**, `training/` in `kyutai-labs/pocket-tts`, announced August 2026 (MIT code): `scratch.yaml`, `depth_distill.yaml`, `finetune.yaml`, **`finetune_language.yaml`**, `drifting.yaml`, data prep, aligner and tokenizer scripts. Mimi codec is not trained there (frozen). |
| Recipe | JSONL manifest {path, duration, transcript} -> word-level alignment (needs a char-level `Wav2Vec2ForCTC` for the language) -> SentencePiece unigram 4,000 with byte fallback, native-script graphemes, no phonemizer -> teacher fine-tune from the English 24-layer teacher with a reset text embedding -> depth-distil to 6 layers. |
| Hours guidance (README) | "Something working" with ~100 h; strong model 1,000+ h; 200 h for a model that speaks, 2,000 h for one that sounds good; prefer hand-transcribed data [M]. |
| Hardware/time (README, 2,000 h English) | Default batch wants ~56 GB; a consumer GPU runs batch 16 x accumulation 4 in ~16 GB. 1xH100 6.3 steps/s, 8xH100 10.4 steps/s; distillation (200k steps) 5.3 h on 1xH100. No A10G numbers exist [U]. Kyutai's Czech run: 976 h, fine-tune reached ~12% WER (Whisper judge) by 10k steps. |
| Community builds | Hindi: Saryps Labs (932 h IndicVoices+Kathbath, from scratch, WER 23.3% under a Whisper judge vs 26.7% for real speech; CC BY 4.0), Indus-Labs (~90 h call-centre Hinglish), altslate Jugnu (647 h); Korean, Czech, Persian, Turkish and others; Telugu and Hindi by Prasad. Quality evidence is thin (Telugu card has no metric; Korean 100M student "quite poor") [C]. Hindi tokenizer maps "." to `<unk>` (patch #288); Pocket TTS' sentence splitter fails for Indic tokenizers: split text yourself [M/C]. |
| Device speeds | ~6x real time on MacBook Air M4 with 2 cores [V]; 2.3-2.5x on a 4-vCPU x86 cloud VM [M README]; Hindi community builds 3.4-3.7x (1 EPYC thread) and 6.3x int8 [V]. Ports: sherpa-onnx (Android/iOS/RPi), ONNX Runtime Web, WASM, CoreML, MLX, C++. |

### 4.3 Licences and training-data caveats

| Item | Finding |
|---|---|
| Code | MIT (pocket-tts, unmute), MIT + Apache (DSM, moshi), Apache-2.0 (moshi-finetune): commercial OK [M]. |
| Weights | Kyutai STT, Mimi, TTS 1.6B/0.75B: `cc-by-4.0`, ungated. **`kyutai/pocket-tts`: `cc-by-4.0`, gated auto with a prohibited-use acknowledgement** (no impersonation/cloning without consent, deception, etc.); the `-without-voice-cloning` repo is ungated. `hibiki-zero` weights are CC BY-NC-SA 4.0 [M]. Third-party GGUF/community cards mislabel (Apache, MIT): upstream is CC BY 4.0. |
| Upstream data | Kyutai's own STT paper lists SPGISpeech ("non-commercial") and TED-LIUM (BY-NC-ND), a 2.5M-hour pseudo-labelled web pool, plus Fisher and proprietary hours for the en/fr model; TTS data per the CALM paper includes GigaSpeech, SPGISpeech, TED-LIUM, Emilia (the Emilia gate says CC-BY-NC for Emilia proper) [M]. Pocket-TTS multilingual data sources are undisclosed. Whether this makes CC BY weights risky to ship is a legal question [U]; treat Kyutai weights as **T2 (risk-accepted), not T1**. |
| Voices | Default Pocket TTS voices `cosette` (Expresso) and `jean` (EARS) come from non-commercial datasets; `estelle`'s CC0 status is questioned in open DSM issue #180 (unanswered); several non-English default voices have no licence statement [M/U]. Do not ship those embeddings. |

### 4.4 Verdict

**STT: reject Kyutai** (reinforces D-009). Reasons: no training code and a maintainer statement that none is coming; guidance of thousands of word-aligned hours; tokenizer and codec-rate problems that are worse for Indic scripts; only one non-Latin-neutral community example and it is a work-in-progress; no CPU or Android runtime. A minimal credible attempt (`stt-1b-en_fr` + patched `moshi-finetune` + new Telugu/Hindi/Latin tokenizer + ~1,000-1,300 h word-aligned data + 2.5-5 s delay + later distillation for CPU) is weeks of research with unproven outcome [E].
**TTS: credible, as a separate project** (MIT code, CC BY weights, official training code, CPU real time, Hindi/Telugu checkpoints to benchmark against). Minimal path [E]: 100-300 h licence-clean read Telugu -> Telugu CTC aligner -> SentencePiece 4k -> `finetune_language.yaml` (15-25k steps) -> distil to 6L -> listening test + CER with an Indic ASR -> int8/ONNX -> sherpa-onnx. Days, not hours.

---

## 5. Base models, teachers and tools

### 5.1 Licence verdict table

Legend: G = green (commercial, derivative and on-device shipping allowed by text read; notice duties only), A = amber (allowed with real strings or unread parts), R = red. "Teacher" = suitability for pseudo-labelling.

| Item | Licence (authoritative reading) | Commercial | Derivative / redistribution | Teacher | Streaming | Hi / Te | Verdict |
|---|---|---|---|---|---|---|---|
| **nvidia/nemotron-3.5-asr-streaming-0.6b** | OpenMDW-1.1 (HF weights); NIM/Together channel says NVIDIA Open Model License [M] | Yes | Yes; keep agreement + notices of origin when distributing; no share-alike | Yes (outputs unrestricted) | Yes (cache-aware RNNT; 80-1120 ms) | Hi yes; **Te no** | **G** base and teacher |
| nvidia/nemotron-speech-streaming-en-0.6b | NVIDIA Open Model License | Yes | Yes; notice file; revocable; updates "comply or cease"; indemnity of NVIDIA | Yes (outputs not a Derivative Model) | Yes | English only | G with notice |
| parakeet-tdt-0.6b-v2 / v3; tdt_ctc-110m; canary-1b-v2 | CC-BY-4.0 | Yes | Yes with attribution | Yes | Offline | v3/canary: 25 European, no hi/te; v2/110m English | G (English teachers; not Indic) |
| nvidia/stt_en_fastconformer_hybrid_large_streaming_multi (~114M) | HF: CC-BY-4.0; NGC page: "NGC Terms of Use" (unread) | Probably | Use HF copy | Yes | Yes | English only | A until NGC terms read |
| canary-1b (original) | CC-BY-NC-4.0 | No | No | No | Offline | en/de/es/fr | R |
| **Parakeet-RNNT-1.1B multilingual/Indic** (NGC/NIM only) | NVIDIA Community Model License (NIM required for production; **no use of outputs to improve other models**) | Only via NIM | Restricted | **No** | NIM says streaming for multilingual | Indic variant bn/en/hi/ta, **no Te** | **R** |
| ai4bharat/indic-conformer-600m-multilingual | MIT (GitHub, LICENSE, HF card body, AIKosh); HF gate text unread | Yes | Yes, keep MIT notice | Yes | **No** (hybrid CTC+RNNT, official ONNX offline) | 22 langs incl. hi, te | A-G: best offline Indic teacher |
| indicconformer_stt_{hi,te}_hybrid_ctc_rnnt_large (~120M encoder) | MIT; gated | Yes | Yes | Yes | No | One language each | A-G |
| ARTPARK-IISc/SraVaani-0.5-live (~430M) | `mit` tag + gate (conditions unreadable) | Unconfirmed | Unconfirmed | Probably | **Yes** (cache-aware, CTC head only, TorchScript fp16) | 63 langs incl. hi, te | **A** |
| SraVaani-1.0 (~430M hybrid TDT-CTC); Vaani-FastConformer-Te/Hi | `mit` tag + gate; fine-tune checkpoints via separate access request | Unconfirmed | Unconfirmed | Probably | 1.0: offline | hi, te | A; upstream data licences unverified |
| bodhan-ai/indic-transcribe (core/flex/pro; base canary-1b-v2) | Indic Open Model License v1.0 + canary CC-BY-4.0 | Yes, 500M MAU / US$250M cap | **Any distributed derivative must carry the same licence + UI attribution; shipping on devices counts**; hosting needs approval; India law, indemnity | **A-R:** a model "trained substantially on Output" is a Derivative | No (lite sibling unread) | 25-27 Indian langs | A-R |
| ai4bharat/bhili (Nemotron-based) | `mit`; case-by-case gate; unreleased | n/a | n/a | n/a | Yes | Bhili only | Precedent only |
| IndicWhisper (Vistaar fine-tunes) | MIT (GitHub statement for models) | Yes | Yes | Yes | No | hi, te; Te weak | G licence-wise; weak |
| openai/whisper | MIT (GitHub); HF cards Apache-2.0 / MIT | Yes | Yes | Yes | No | Weak zero-shot; Te script collapse | G (weak Indic) |
| facebook/omniASR-CTC | Apache-2.0 (code, models); corpus CC-BY-4.0 | Yes | Yes | Yes | No (<40 s) | 1,600+ langs; hi/te evidence contradictory [U] | G licence-wise; not relied on |
| facebook/mms-*, seamless-m4t-v2 | CC-BY-NC-4.0 | No | No | No | No | many | **R** |
| Qwen3-ASR 0.6B/1.7B | Apache-2.0 | Yes | Yes | Yes | Yes (GPU-oriented) | Hindi yes; **no Telugu** | G; no Te |
| Voxtral-Mini-4B-Realtime | Apache-2.0 | Yes | Yes | Yes | Yes | Hindi yes; no Te; 4.4B | G; too big |
| Moonshine | MIT (except legacy non-English community-licence models) | Yes | Yes | n/a | Yes | No hi/te evidence | n/a |
| Kyutai STT | CC-BY-4.0 weights (NC/proprietary data upstream) | Yes (residual risk) | Yes | Yes | Yes | en/fr, en | Licence fine; not an option |
| **Svanita** | CC-BY-4.0 (tag); no NOTICE | Yes with attribution | Yes | Weak | **No** | hi, te | Baseline only |
| Software: NeMo, Lhotse, SentencePiece, PyTorch, sherpa-onnx, icefall/k2, ONNX/ORT, WeNet, whisper.cpp, faster-whisper, HF transformers/datasets | Apache-2.0 / MIT / BSD | Yes | Yes | n/a | n/a | n/a | G |
| **Silero VAD** | **MIT** (LICENSE, PyPI, README body); "CC BY-NC 4.0" is stale badge alt text | Yes | Yes | n/a | n/a | n/a | G default VAD (resolves U-15) |
| **TEN VAD** | Apache-2.0 + extra conditions: no competing with Agora / no enabling third parties to deploy Applications; "your Application and direct End Users" only | Own app probably yes | Derivatives stay under it | n/a | n/a | n/a | A: counsel first, especially if we ever offer an SDK |
| Aksharamukha | AGPL-3.0 (PyPI) / GPL-3.0 file | **Not in a shipped binary** | Copyleft | n/a | n/a | n/a | R for shipping |
| IndicXlit (new repo), indic-transliteration | MIT | Yes | Yes | n/a | n/a | n/a | G; old IndicNLP-Transliteration models are CC BY-SA |
| uroman | MIT-style + acknowledgement clause | Yes | Yes | n/a | n/a | n/a | G with acknowledgement |

### 5.2 Nemotron-3.5-ASR-Streaming-0.6B deep dive

**Resolved licence conflict [M].** The HF README on 2026-06-04 had front-matter `nvidia-open-model-license` but body text naming OpenMDW-1.1; three NVIDIA "Update License" commits on 2026-06-05 set the front-matter to `openmdw-1.1`. Current card, safety/explainability pages and NVIDIA's blog say OpenMDW-1.1. The NGC NIM container page and the Together AI listing still say NVIDIA Open Model License for the NIM-served builds. Conclusion: two channels; for weights we download from HF, OpenMDW-1.1 applies. **OpenMDW-1.1 summary (full text read):** permission to deal in the materials "without restriction" including patents; if you distribute any part you keep a copy of the agreement and the notices of origin; rights end if you sue claiming the materials infringe (unless countersuing); no restriction on outputs; as-is, and **you alone are responsible for clearing third-party rights**. For us: commercial use yes; fine-tune and ship derivatives yes with no share-alike and no naming rule; quantised/ONNX/GGUF copies are still "a portion of the Model Materials" so ship the OpenMDW text and "NVIDIA ... OpenMDW-1.1" notice; pseudo-labels from outputs unrestricted. The repo has no LICENSE/NOTICE file, so what counts as "notices of origin" is [U]: ship the full model card plus agreement. **Residual risk:** the training mix (proprietary Riva multilingual set, Granary, MLS, Common Voice, FLEURS, VoxPopuli) uses labels partly generated by Canary, Parakeet 1.1B, Whisper and FunASR; OpenMDW gives no indemnity. Compared with the NVIDIA Open Model License (revocable, updatable, guardrail-circumvention termination, indemnity of NVIDIA), OpenMDW is cleaner. Archive a dated README + licence snapshot at download.

**Facts [M unless marked]:**

| Item | Finding |
|---|---|
| Size and files | 637,997,088 params (F32); `.nemo` 2.37 GB; safetensors 2.55 GB; q8_0 GGUF 742 MB; not gated; created 2026-05-15, release 2026-06-04. Derived from `nemotron-speech-streaming-en-0.6b` plus language-ID prompt conditioning. |
| Architecture | 24-layer FastConformer (d=1024, 8 heads, conv kernel 9, 128 mel, 8x subsampling), RNNT decoder (2-layer LSTM, 640). Chunk setting `att_context_size=[56,N]`, N in {0,1,3,6,13} = 80/160/320/560/1120 ms, switchable without retraining. |
| Coverage | 40 locales: 19 transcription-ready (incl. **Hindi hi-IN**, en-US, en-GB), 13 broad-coverage, 8 adaptation-ready. **Telugu is in none.** Hindi FLEURS WER 8.13 (80 ms) to 6.81 (1.12 s) [V, card]; Hindi is 5.10% of the validation set. |
| Tokenizer | One merged BPE of 13,087 tokens: Latin 2,567, CJK 6,907, Cyrillic 402, Arabic 252, **Devanagari 196**, Greek 162, Hebrew 121, Thai 119, **Telugu 0**, Tamil 0, Bengali 0, Kannada 0, Malayalam 0 [OURS count from `tokenizer.json`]. `byte_fallback: true` but **no `<0xNN>` byte tokens exist**, so Telugu text would map to `<unk>` [OURS]. 39 language tags (`<hi-IN>` yes; no `<te-IN>` token). |
| Prompt dictionary | 128 slots, 121 keys, including reserved slots for unsupported languages: `bn-IN 36`, `ta-IN 39`, **`te-IN 40`**, `kn-IN 43`, `ml-IN 44`. NVIDIA's tutorial calls ~60 such languages "feasible to fine-tune". |
| CTC head | **None** (NeMo config: RNNT-only). Resolves U-03: no CTC hotwords or CTC fallback. |
| Training data (card) | Riva multilingual set, Granary, MLS, Common Voice, FLEURS, VoxPopuli/Europarl; 10k-1M h; code-switching samples were in training (NVIDIA staff, HF discussion #2). |
| Runtime | NeMo 26.06 / git main (stable releases lacked `EncDecRNNTBPEModelWithPrompt`; PyPI `nemo-toolkit` is now 3.0.0), HF Transformers >= 5.13.0; supported GPU architectures include Ampere (A10G), Hopper, Blackwell, Lovelace. sherpa-onnx has an export script (encoder/decoder/joiner + int8, prompt dictionary in metadata) since 2026-06-12; whether it works with a modified tokenizer/prompt table is [U] (it reads both from the model, so likely). NVIDIA's own English Q8_0 GGUF (NeMo-Speech.cpp): 27 ms per 160 ms chunk, ~6x real time, i7-11700K 8 threads [V]. |

**NVIDIA's documented new-language route [M, NVIDIA notebook `asr-extend-tokenizer-to-newlang-ft-acoustic-model.ipynb`, worked example Malay on Common Voice Spontaneous 3.0]:** (1) append the language tag after each sentence-final punctuation in transcripts; (2) train a small SentencePiece unigram tokenizer for the new language with the language tag as a user-defined symbol; (3) merge it into the existing tokenizer; (4) fine-tune with `++model.tokenizer.update_tokenizer=true` and the merged tokenizer directory, which retrains the RNNT decoder (prediction network + joint) from scratch while keeping the encoder; (5) evaluate at deployment chunk size. **Limits stated by NVIDIA:** the toy run produced meaningful Malay only after 40-60 epochs at ~60% WER, and a good decoder "requires larger dataset and much more training steps". For languages with no prompt slot you must repurpose an unused id or retrain with a redefined dictionary; **Telugu already has `te-IN: 40`**. No Telugu or other Dravidian Nemotron-3.5 fine-tune was found on the Hub.

**Hardware and LoRA.** The blog and notebooks give no GPU, memory, batch size or learning rate for fine-tuning. NVIDIA staff suggested an L40S and "no more than $50" for experiments on supported languages (HF discussion #1); notebook default `batch_duration` 200-400 s per GPU, reduce on out-of-memory. LoRA: "not supported now" (NVIDIA, blog comments and discussion #10); one community encoder-adapter exists (Egyptian Arabic, 2,384 utterances) [C]. A 24 GB A10G full fine-tune is plausible but unverified: fp32 weights + gradients + AdamW moments ~10.2 GB before activations [E]; one community Hinglish fine-tune ran on a 16 GB card with the encoder frozen [C].

**Hours reference points [C unless marked]:** Greek 35 -> 24 WER and Bulgarian 22 -> 15 on FLEURS with a ~2,000 h mix (tokenizer already covers them) [V, NVIDIA blog]; Swahili (Latin script, new language) 382 h -> 29.8% FLEURS WER at 1120 ms (base 114.7%); Slovenian 858 h -> 21.7-33.1% depending on test set; AI4Bharat Bhili ~200 h, no WER, unreleased; Hinglish (frozen encoder, 12k steps) 42.2 -> 24.6% on its own noisy test set, clean Hindi regressed ~2.9 points; NVIDIA's own Malay toy ~60% WER. **There is no NVIDIA "few hundred hours for a new language" figure** in the blog, the notebooks or the HF discussions read; the earlier project documents cited an NVIDIA FAQ [V], which this audit did not re-check. For a new script plus a from-scratch decoder, low hundreds of hours should give a weak-but-usable Telugu and thousands are needed for production quality [E].

**What this means for a Telugu-only model [P/E].** (i) The encoder carries no Telugu acoustic knowledge, so Telugu needs both decoder training and real encoder adaptation: expect it to be the most expensive of the three models. (ii) Tokenizer choice is a decision for a logged D-###: **merge** (keeps all 13k tokens and Hindi/English ids; decoder retrained on every language you want to keep) versus **new minimal Telugu+Latin tokenizer** (smaller joint network, faster CPU decoding, drops the 40-language vocabulary we do not need; Svanita used 4,097 pieces for Telugu+Hindi+Latin, so ~2k for Telugu+Latin is plausible). Both use the same flag and both retrain the decoder. (iii) Replay of English (and Hindi if kept) is needed to avoid forgetting; NVIDIA's own advice. (iv) Keep Latin pieces so English words in Latin script stay representable (the base vocabulary already has 2,567 Latin tokens). (v) The `<lang>` tag after punctuation is optional if we only ever run a fixed locale [P]. (vi) For Hindi, the base already works; only 196 Devanagari tokens suggests near-character segmentation [E], so measure tokens per word at Stage 1 before deciding whether to replace its tokenizer too.

---

## 6. Datasets

### 6a. Cross-cutting findings

1. **Gates.** The gate on all AI4Bharat gated speech datasets (IndicVoices, IV-R, Kathbath, Shrutilipi, Lahaja, Svarah, Rasa, IndicCMix) is Hugging Face's default contact-sharing text; the API exposes no `extra_gated_prompt` (it does for `speechcolab/gigaspeech`, which was used as a control) [OURS]. **This corrects the Svanita and model notes, which called the gate terms "unreadable".** What the HF modal says after login was not seen. Vaani's gate adds a "use for" selector (Research/Academic/Commercial/Education). Gates on model repos (IndicConformer, SraVaani, Bodhan, Bhili, `kyutai/pocket-tts`) were not tested the same way: Kyutai's is a known prohibited-use text; the others remain [U].
2. **The gate is not access control.** Full-length IndicVoices archives (Hindi ~150 GB, Telugu ~141 GB), Kathbath tars, IV-R tars, Nirantar and Vistaar zips answer HTTP 200 on public object-store URLs [OURS, HEAD only]. Availability is not consent evidence: log the licence snapshot, not the access path.
3. **AIKosh licence fields have low authority**: several are blanket labels from Bhashini bulk uploads (CC BY-SA stamped on Kathbath, Gramvaani and Common Voice copies on the same day) or uploaded by third parties. Use them as secondary evidence and as a list of questions.
4. **AI4Bharat's CC BY 4.0 covers AI4Bharat's own collection and packaging only**, not third-party material inside it (Kathbath's IndicCorp sentences; Shrutilipi's All India Radio audio).
5. IndicVoices hour figures are successive snapshots (paper v1 7.3k total/1.6k transcribed; GitHub 12k/3.2k; HF card 23.7k/11.2k), not a conflict.

### 6b. Source conflicts and how they are resolved

| Topic | Conflict | Treated as authoritative / tier |
|---|---|---|
| RESPIN-S1.0 tier | `datasets_other.md`: T2. `datasets_discovery_inventory.md`: T1-lean (provisional) | **T2.** Only AIKosh states CC BY 4.0 (uploader Prasanta Kumar Ghosh, 2025-06-18); GitHub repo and paper state none; SPIRE download-form terms and consent text unread. Promote only after written confirmation. |
| RESPIN hours | Paper Table 3: Hindi clean 944.93, Telugu clean 1,303.98 h. GitHub release: `train_hi_clean` 712.61, `train_te_clean` 1,021.16 h (discovery note read a scratchpad copy of the README, not the original URL) | **Plan on the repo numbers** (lower); gap of ~232/~283 h is unexplained. Re-read the original README. |
| IndicVoices hours | Earlier note ~790 / 480 h; AI4Bharat note byte-anchored 524-844 (Hindi) and 393-510 (Telugu); Svanita clip counts (Section 3.1) support the upper end | **Range Hindi 0.52-0.84k, Telugu 0.39-0.51k [E]**; best case 0.79k / 0.48k. Needs `duration` sum after access. |
| Kathbath licence | HF YAML cc-by-4.0; HF/GitHub body: CC0 for packaging, raw text not owned; AIKosh: CC BY-SA 4.0 (bulk upload); Svanita card: CC-BY-4.0 | **CC BY 4.0 attribution, T2.** Consent said "research purposes ... used for building AI models" (not explicitly commercial); sentences from crawled IndicCorp. |
| IndicVoices-R | HF YAML, card, paper, GitHub `LICENSE.md`: CC BY 4.0; AIKosh: CC BY-ND 4.0 | **BY-ND treated as the stricter reading until resolved; T2.** Not used for STT anyway (enhanced audio duplicates IndicVoices). |
| IndicTTS | HF mirrors: no tag, "subject to original licence"; AIKosh Phase-3 pages: CC BY 4.0; IITM PDF unread; informal maintainer remark | **T3** until the PDF is read in a browser. |
| Lahaja | YAML `mit`; body and AIKosh CC BY 4.0 | CC BY 4.0, T2, eval only. |
| SPRING-INX Hindi | AIKosh (Bhashini uploader): CC BY 4.0; paper: "public domain"; HF repos no tag, no Hindi repo | **CC BY 4.0, T2** (discovery treated it as T1 in its totals). |
| Rural Women ASR v2 (Hindi) | HF API: no tag, `datasets_ai4bharat.md` T3; discovery note: README says CC BY 4.0 (read via a scratchpad copy) | **T3** until the card is re-read. |
| NPTEL2020 Indian English | Both notes: T2; NPTEL's own site licence is ambiguous (BY-SA vs NC-SA reports) | **T2/T3; treat as T3 for any commitment.** |
| Model-repo gate wording | Svanita/model notes: unreadable; AI4Bharat note: dataset gates are HF default | Datasets: default text only [OURS]. Models: still [U]. |
| SLR103 | T3 (earlier) vs T2 now (licence ID maps to O-UDA-1.0 via a secondary source; text read on Microsoft GitHub) | T2, conditional on written confirmation of the ID mapping; low value (8 kHz). |

### 6c. Master verdict matrix

Hours are transcribed hours (hi / te / en) unless stated. **Style**: Sp = spontaneous/conversational, Rd = read. **Convention** = how English words appear in transcripts. "Role": **Train**, **Eval**, **Neither**.

**Tier 1: clearly safe (engineering view)**

| Dataset | Authoritative licence and source | Hours hi / te / en | Style | Convention | Role | Key caveat |
|---|---|---|---|---|---|---|
| IndicVoices (`ai4bharat/IndicVoices`) | CC BY 4.0: HF YAML + card + paper ("allowing commercial usage") + AIKosh agree; participants told "commercial and non-commercial purposes" [M] | ~0.52-0.84k / ~0.39-0.51k [E] / 0 | Sp (76% extempore, 15% conversational, 8% read); phone, 16 kHz FLAC; 8 kHz conversational origin | Native script; cleaned `text` has no Latin by construction; raw `unsanitized_*` fields may keep `native [english]` [U, Svanita claims so] | **Train** (+ `valid` as dev) | Later-phase consent wording [U]; Wikipedia/MASSIVE-derived prompts; no test split on HF; quality issues in discussions; DPDP |
| Vaani + `-transcription-part` (`ARTPARK-IISc/Vaani`) | cc-by-4.0: HF YAML, vaani.iisc.ac.in, paper arXiv 2603.28714; gate = contact fields + "use for" selector incl. Commercial [M] | 1,003.78 / 184.48 / 22.46 (audio total 14,923.7 / 2,326.47 / 336.79) [M] | Sp image-prompted; phone; 16 kHz | Native script + Latin original in braces: `ट्रक {truck}`; tags `[unintelligible]`, `<PAUSE>`, `--`; numbers as words [M] | **Train** (QC-filtered); pseudo-label source | No official splits; many Hindi districts are Bhojpuri/Maithili (filter `language`); gate text unread; narrow domain |
| Vaani-Benchmark-V1.0 | cc-by-4.0 [M] | ~10.9 h Hindi only | Sp | braces, 3 references | **Eval** (Hindi) | Held-out; speaker disjointness not measured |
| Vaani-Noise-Event | cc-by-4.0 [M] | 154.6 h noise timestamps | n/a | n/a | Augmentation | Derived from Vaani |
| Common Voice v27.0 scripted (Mozilla Data Collective) | CC0-1.0 + "Forbidden Usage" (no re-identification, no re-hosting) [M] | 15.71 / 0.94 / 2,826.8 validated (totals 26.74 / 3.2 / 3,795.9) | Rd, crowd mics, MP3 | n/a | **Train** English (Indian-accent weighted), Eval | Hindi/Telugu too small (485 / 75 speakers); "indian" accent includes Pakistan and Sri Lanka; MDC clause on synthetic data/outputs (ask Mozilla) |
| HiACC (Zenodo 15551669) | CC BY 4.0, open [M] | Hinglish 5.24 h | Rd + Sp, adults + children | English in CS tags | Train/Eval (CS) | Tiny; check child-consent in paper |
| LibriSpeech, MLS English | CC BY 4.0 (SLR12, SLR94); MLS card also "Public Domain" [M] | en ~1k / ~44.5k [U] | Rd audiobooks, US | n/a | English **replay** | Not Indian-accented |
| MUSAN | CC BY 4.0 (SLR17) [M] | noise/music/speech | n/a | n/a | Augmentation | Per-file attribution |
| Google SVQ | cc-by-4.0 [M] | 171,434 short queries, hi/te/en locales | phone, clean/background/traffic/media noise | n/a | **Eval** (noise) | Single split by design; per-locale hours not shown |
| Rasa (`ai4bharat/Rasa`) | CC-BY-4.0 (YAML, card, GitHub agree) [M] | 50.8 / 52.3 / 0 | acted/emotional, 2 speakers/language, 48 kHz | n/a | Neither for STT (TTS) | IndicTTS-derived neutral part may inherit its terms [U] |

**Tier 2: usable with caveats**

| Dataset | Licence and source | Hours hi / te / en | Style | Convention | Role | Key caveat |
|---|---|---|---|---|---|---|
| RESPIN-S1.0 (IISc SPIRE) | CC BY 4.0 on AIKosh only; repo/paper silent [M] | train clean 712.6 / 1,021.2 (paper clean 944.9 / 1,304.0); semi-noisy 273 / 186; noisy 305 / 128 [M repo] | Rd, agri/finance sentences (~20k sentences/language), mobile crowd, 2.3k speakers/language, 4-5 dialect regions | Native script; **English words removed**; digits expanded | **Train** (capped) | Licence in writing; 232/283 h discrepancy; text-repetition; read-style bias |
| Numo Indic Speech (`psdn-ai/numo-indic-speech`, Poseidon AI) | cc-by-4.0 tag + card text; gate auto; created 2026-10-02 [M] | 1,314.6 / 1,224.2 / 0 | Rd scripted, single-speaker clips, speaker count unstated | Keeps code-switching/English terms from prompts [V] | **Train** only after consent check | Consent asserted by vendor, not documented; privacy policy says content "may be licensed to third party AI companies"; 10 days old; DPDP |
| SPRING-INX Hindi (IITM SPRING Lab; AIKosh) | CC BY 4.0 (AIKosh); paper "public domain" [M] | 351 (316/30/5) Phase 1 [paper]; R2 unseen / none / none | Monologue + conversation; 16 kHz | **Latin retained for English** in other languages previewed (Gujarati 90/100 rows, Bengali 53/100); Hindi not previewed [OURS] | **Train** (Hindi code-mix) | Vendor-collected; consent undescribed; Hindi convention unconfirmed |
| Kathbath (`ai4bharat/Kathbath`) | See 6b | HF: ~141 / ~145 (clean train+valid); paper 150.2 / 154.9 clean + 47.7 / 74.8 noisy | Rd news-style, phone; 121 / 104 speakers | Native script; no code-mix; numbers to words in IndicSUPERB | Train (capped <=10-20%) + **Eval** (test-unknown via IndicSUPERB tar) | Consent "research purposes"; IndicCorp text; reported label errors; few speakers |
| SYSPIN_S1.0 (IISc) | CC BY 4.0 (AIKosh, project page); T&C unread [M] | ~119 / ~115 / 0 (+ Indian-English 80 h, licence unstated) | Studio read, 1 M + 1 F per language | n/a | TTS; ASR neither | 2 speakers; T&C unread |
| Lahaja; Svarah | CC BY 4.0 (body, AIKosh); tags `mit` / missing [M] | 12.5 / 0 / 0; 0 / 0 / 9.6 | Rd + Sp; 122 non-native Hindi speakers; 117 L2 English speakers | Devanagari; Switchboard-style | **Eval** only | Prompt-text overlap with IndicVoices; consent text not found |
| IndicVoices-R | See 6b | 74.6 / 136.4 / 0 | enhanced 44.1 kHz subset | as IndicVoices | Neither | Acoustically mismatched; may overlap IV train |
| Indic DiarBench (Sarvam) | CC BY 4.0 [M] | 10.7 / 9.3 / 0 | conversational, YouTube | two formats: native and normalised with Latin English | **Eval** | YouTube provenance |
| SLR104 MUCS Hi-En | CC BY-SA 4.0 [M] | 89.9 train + 5.2 test Hi-En | tutorial lectures, 16 kHz | English in both scripts [earlier note] | CS eval; train only if SA accepted | Share-alike on weights unsettled |
| SLR103 MUCS Hindi (+Marathi, Odia) | O-UDA-1.0 by ID (secondary) [S/M] | 95.1 + 5.6 test | 8 kHz stories | n/a | Low | ID mapping unconfirmed |
| SLR66 Telugu (Google) | CC BY-SA 4.0 [M] | / ~8 [E] / | TTS-style template sentences | n/a | Neither | BY-SA; unnatural |
| NPTEL2020 Indian English (AI4Bharat/Zenodo) | Zenodo cc-by-4.0; GitHub "Creative Commons" (YouTube) [M] | 0 / 0 / 15,700 | STEM lectures, subtitle labels (14.5% WER vs hand-checked sample) | English | Optional English **booster** (filtered) | **T2/T3**; NPTEL parent licence ambiguous; labels not verified |
| People's Speech (CC-BY configs), VoxPopuli, AMI | CC-BY / CC0 + EP notice / cc-by-4.0 [M] | English only (CC-BY clean ~5.8k [E]) | US/EU accents | n/a | Optional replay / far-field eval | Not Indian-accented; noisy labels (dirty) |
| YODAS, FLORAS | cc-by-3.0; YouTube-CC [M] | hi ~481 manual [U earlier] | YouTube | n/a | Optional | Caption provenance unclear |
| FLEURS | cc-by-4.0; text from FLORES (CC BY-SA 4.0) [M] | ~8.7 / ~10.3 / ~10.3 total [E] | Rd | n/a | **Eval only** | Likely in teachers' training sets [U]: optimistic baselines |
| DEMAND; RIRS_NOISES simulated RIRs | BY-SA 3.0 (description) vs cc-by-4.0 (metadata); Apache-2.0 [M] | n/a | n/a | n/a | Augmentation | Use BY-SA reading; use simulated RIRs only |

**Tier 3: unresolved (do not train)**

| Dataset | Licence evidence | Hours | Why unresolved |
|---|---|---|---|
| Shrutilipi (HF) | CC BY 4.0 label over All India Radio audio/text; AIR policy: personal non-commercial use, other use needs written permission [M] | HF copy ~850 hi / ~49 te [E] (paper 1,620 / 390) | T3 leaning T4; HF copy is much smaller than advertised |
| IndicTTS (IITM) | licence PDF unread | ~10.3 / ~8.7 | Tiny; Prasad's TTS credits it |
| Vistaar bundle; Kathbath-Hard (Vistaar zip) | MIT covers models only; bundle includes Gramvaani, MUCS Telugu, Shrutilipi, NPTEL | hi 2,150 / te 806 train mix | Use originals; regenerate noisy Kathbath |
| Nirantar | no licence anywhere; public tars | 138 / 221 | IndicVoices lineage; test may sit inside IV train |
| Rural Women ASR v2 (Hindi) | see 6b | ~90 h [E] | Licence tag absent |
| indicvoices-cleaned; SPRINGLab `Hindi-1482Hrs`; IndicVoices-R mirrors | no card/licence | unknown / ~1,482 [U] | Provenance unknown |
| IndicCMix (AI4Bharat, MIT) | MIT; F5-TTS synthetic English audio; source of English sentences unstated | text 104k sentences x 11 languages | Useful as CS text template only |
| BhasaAnuvaad (IndicVoices-ST, NPTEL, Spoken Tutorial, Mann-ki-Baat, WordProject, SeamlessAlign) | CC BY 4.0 labels over AIR/NPTEL/Bible/Meta-Seamless-NC sources | translation pairs | Not a transcript source; mined provenance |
| bolAIndia (Kapture CX) | no licence on card; STATS.md behind gate; repo holds ~99,976 `newsonair` manifests (AIR scrape) | 89.8k hi / 8.97k te / 9.98k en "published hours" | Treat as T4 until read |
| Chaashini (Kapture CX) | Apache-2.0 claim over scraped public spoken-word audio with ASR labels | 1,394.8 / 116.3 / 240.6 | A label cannot license scraped third-party audio |
| SPIRE-SIES | request form; licence unstated; only 23 h with transcripts (Whisper-based) | 170.8 h Indian English | Optional request |
| IITG-HingCoS, LDC-IL Telugu, IIIT-H CSTD (research-only as released) | forms / undertakings / challenge terms | 25 h Hi-En; 15.6 h Te; 2,000.8 h Te | T3-T4 as released |
| InfoBayAI | tag cc-by-4.0, card text "research and educational purposes only" | samples only | Use the stricter text |
| Aggregators: `agarwalayushi/hinglish`, `projectkaira/Pretraining-V1`, `sorika-labs/vaani-v3-dataset`, `abar-uwc/*` Vaani copies | CC-BY/Apache tags over mixed sources; Pretraining-V1 contains the non-commercial Microsoft corpus | various | Never use; pull from originators |

**Tier 4: unusable for a commercial model**

| Dataset | Reason |
|---|---|
| GigaSpeech | Gate: non-commercial research and education only; binds a for-profit employer (YAML says Apache-2.0: gate wins) |
| SPGISpeech | Academic and internal use only |
| TED-LIUM 1/2/3 | CC BY-NC-ND (secondary source) |
| Emilia | Gate: CC-BY-NC for Emilia proper |
| MUCS Telugu/Tamil/Gujarati = Microsoft Speech Corpus (Indian languages) | "shall not be used for commercial purposes" (Telugu 40 h) |
| Gram Vaani SLR118 | Academic; commercial only with written permission (contact@gramvaani.org); 8 kHz telephone |
| Skit-S2I, CS-FLEURS, Karya sanmati-stories, Vartalaap, Sonexis, Silencio, WorldSpeech, IndicSynth | Non-commercial |
| MahaDhwani / Dhwani | YouTube scrapes, URL lists |
| CMU Wilderness | Copyrighted Bible audio; cannot redistribute |
| BharatVani (Sheeba2026) | All rights reserved |
| Voice of India | Closed |

### 6d. Licence-label traps (record in the data manifest)

- **Tag says open, text says restricted:** `infobayai/*` (cc-by-4.0 vs "research and educational purposes only"); GigaSpeech (Apache YAML vs non-commercial gate); Emilia (cc-by-4.0 YAML vs CC-BY-NC gate).
- **Aggregators and re-uploads:** `projectkaira/Pretraining-V1` (CC-BY tag covers only the aggregation work; includes the NC Microsoft corpus); `agarwalayushi/hinglish` (CC BY 4.0 over 14 sources incl. AIR content); `sorika-labs/vaani-v3-dataset` (Apache on code; not IISc Vaani); `kapturecx/Chaashini` (Apache over scraped audio with ASR labels); `openslr/openslr` HF mirror (cc-by-sa over mixed licences); HF Common Voice mirrors (cc0 tags, but MDC forbids re-hosting); third-party IndicConformer/Kyutai ports (MIT/Apache over CC-BY upstreams); `abhisingh-18` Hinglish (Apache on transcripts only, no audio).
- **Conflicting first-party labels:** Spoken Tutorial (site BY-SA, AI4Bharat copy BY); IV-R (BY vs BY-ND); Kathbath (three labels); Lahaja (`mit` tag); SPRING-INX (BY vs "public domain"); AIKosh blanket CC BY-SA on Kathbath/Gramvaani/Common Voice copies; Karya custom "KPL BY-NC-SA-FS 1.0"; RIRS_NOISES Apache label over RWCP (research-only) and Aachen AIR RIRs.

### 6e. Per-language inventories and an MVP mix

Method: "Low" = T1 only; "Best" = T1 + T2 sources with identifiable provenance (RESPIN clean, SPRING-INX, Kathbath, SYSPIN/Rasa where relevant); "High" = Best + Numo + noisier RESPIN slabs. Overlapping copies (IV-R, Nirantar, IndicVoices-ST, aggregators) excluded. This follows the tier assignments in 6b, so it differs slightly from the discovery note, which counted SPRING-INX as T1. All values [E].

| Language | Low (T1) | Best | High | Spontaneous vs read |
|---|---|---|---|---|
| **Hindi** | ~1.5-1.9k (IndicVoices 0.52-0.84k + Vaani ~0.6-1.0k + CV/HiACC ~0.02k) | ~3.2k (+ SPRING-INX 0.35, RESPIN clean 0.71, Kathbath 0.14, SYSPIN 0.12, Rural Women 0.09, Rasa 0.05) | ~5.1k (+ Numo 1.31, RESPIN other slabs 0.58) | T1 spontaneous ~1.3-1.9k; best case ~2.1k spontaneous vs ~1.1k read |
| **Telugu** | ~0.55-0.7k (IndicVoices 0.39-0.51k + Vaani 0.11-0.18k + CV 0.001k) | ~1.9-2.0k (+ RESPIN clean 1.02, Kathbath 0.145, SYSPIN 0.115, Rasa 0.05) | ~3.4-3.5k (+ Numo 1.22, RESPIN other slabs 0.31) | Spontaneous only ~0.55-0.7k in every scenario; read is ~2/3 of Best and ~85% of High |
| **English-India (Indian accent)** | ~0.05k (Vaani-en 0.022k + small) | ~0.25k (+ Common Voice "indian" ~0.17-0.22k, partly unvalidated) | ~0.35k (+ SYSPIN English 0.08k, licence unstated) | Vaani-en spontaneous (image descriptions); CV read |

Generic English (T1/T2) is plentiful (LibriSpeech ~1k, Common Voice English 2.8k validated, MLS, People's Speech CC-BY ~5.8k clean [E]) but not Indian-accented; NPTEL2020 (15.7k h) is the only large Indian-accent pool and is T2/T3 with unverified labels. **Reference point from a real run:** Svanita used 451 h Telugu and 685 h Hindi to reach 37.7% / 23.7% WER on its own test halves [V] (offline, new decoder on a Parakeet encoder). The upper bounds for a first-iteration budget are lower than the pools: at ~30 audio-hours per A10G-hour [E from the project plan, up to 2x off] a 1,000 h epoch is ~33 GPU-hours.

**Proposed MVP mix per language [P, not validated; for a logged decision before any plan edit].** Percentages are shares of the language's training hours; every T2 source is gated on written risk acceptance, with a T1-only variant kept as the fallback arm.

| | Hindi (start from Nemotron hi-IN; tokenizer kept or replaced per Stage 1 measurement) | Telugu (new tokenizer + decoder; encoder adapted) | English-India (start from Nemotron en-US or the English checkpoint) |
|---|---|---|---|
| Target hours | ~600-800 | ~800-1,000 | ~250-400 |
| Spontaneous core (T1) | IndicVoices Hindi ~300 h sampled for speaker balance; Vaani Hindi ~150-200 h QC-filtered to Hindi districts | IndicVoices Telugu ~400-480 h (all); Vaani Telugu ~110-180 h (all QC-filtered) | Vaani-en 22 h (all); Common Voice Indian-accent ~100-150 h validated |
| T2 additions (capped) | SPRING-INX ~100-200 h (code-mix; <=25%); RESPIN clean <=100 h (<=15%); Kathbath <=50 h (<=8%) | RESPIN clean <=250-300 h (<=30%; raise only if the licence is confirmed and the spontaneous dev set shows no read bias); Kathbath <=100 h (<=10%) | NPTEL2020 filtered by teacher agreement ~100 h (<=30%, only if rights are clarified) |
| Replay / robustness | English replay ~5-10% | English replay ~10-15%; Hindi replay only if we keep Hindi capability | LibriSpeech/MLS/CV generic ~50-100 h (~20%) |
| Code-switch (CS) | CS-rich subset from Vaani braces, SPRING-INX, IndicVoices (target ~40-60 h with Latin English) | CS subset mined from Vaani/IndicVoices Telugu (measure first); synthetic splices (Section 6f) | n/a |
| Augmentation | MUSAN, simulated RIRs, Vaani-Noise-Event-derived noise, 8 kHz telephone copy (~20-40%) | same | same |
| Pseudo-labelled phase 2 (optional) | Not needed for volume | **Vaani Telugu untranscribed (~2.1k h) labelled by IndicConformer-Te/600M**, filtered by confidence/agreement, to add spontaneous volume | n/a |
| Dev/test | Vaani-Benchmark-V1.0, Lahaja (accent), Kathbath test-unknown, Indic DiarBench, SPRING-INX test, private mic set | Kathbath test-unknown, FLEURS te, SVQ te, DiarBench, private mic set; **build our own speaker-disjoint Vaani/IndicVoices dev/test** | Svarah, SVQ en, FLEURS en (US only), private mic set |

Held-out rules: dedupe text across IndicVoices, Lahaja, Svarah and Nirantar before any is used as eval; never train on any eval set's audio; Vaani has no official splits.

### 6f. Code-switch: what exists, what does not, how to build it

| Pair | Exists | Does not exist |
|---|---|---|
| Hindi-English | HiACC 5.24 h (CC BY 4.0, T1); SLR104 89.9 h (BY-SA, T2); SPRING-INX Hindi code-mixed transcripts (T2); natural insertions inside IndicVoices and Vaani (unmeasured); Indic DiarBench and Vaani-Benchmark (eval); IndicCMix text (MIT) | A large clearly licensed real corpus; a measured CS fraction in any T1 set |
| Telugu-English | Natural insertions in IndicVoices and Vaani Telugu (unmeasured); DiarBench Telugu 9.3 h (eval); CoSTA 2.3 h Telugu CS eval (promised CC-BY-4.0, not found released) | Any released real corpus. Microsoft Research India's 243 h CS set (arXiv 2006.00782) is not public; a "200 h / 400 speakers" corpus appears only in a March 2026 forum post with no owner or licence; common-voice code-switching is "Alpha", no releases |

**How to build [P]:** (1) measure first: the only measured CS rate is Svanita's [V] (46% of Telugu and 39% of Hindi clips contain Latin English, after recovery from IndicVoices annotations); (2) mine CS-rich clips from Vaani by taking brace content as the Latin token (delete the braces to get native-only) and from SPRING-INX; (3) check whether IndicVoices' raw `unsanitized_verbatim` retains `native [english]` pairs as Svanita claims [U]: if yes this is a free, high-quality Latin target for Hindi and Telugu; if not, use a lexicon + back-transliteration model and measure the error on SPRING-INX and DiarBench where Latin ground truth exists; (4) synthesise: IndicCMix text as templates (MIT; provenance of its English sentences unstated) rendered through licensed TTS, and splice monolingual English clips into native context; label as synthetic; (5) evaluate English tokens and native tokens separately on a private CS test set; (6) normalise to one convention (native for Indic words, Latin for English words); romanisation stays an optional post-process (CLAUDE.md rule).

### 6g. Unlabeled pools for pseudo-labelling [E where derived]

| Pool | Hindi | Telugu | English | Tier / note |
|---|---|---|---|---|
| Vaani untranscribed (audio minus transcribed) | ~13.9k h | ~2.1k h | ~0.31k h | **T1**, consent-based; best pool |
| IndicVoices untranscribed | ~12.5k h across 22 languages | | | T1; whether in the HF release is unstated |
| NPTEL2020 (subtitle labels ignored) | | | 15.7k h | T2/T3 |
| bolAIndia | 89.8k h | 8.97k h | 9.98k h | T3-T4; provenance behind the gate |
| Chaashini | 1.39k | 0.12k | 0.24k | T3 |
| BhasaAnuvaad NPTEL / SeamlessAlign audio | 1.4k / 2.4k | 0.74k / 0.87k | | T3; SeamlessAlign inherits non-commercial Seamless terms |
| Gram Vaani (SLR118) | ~1k | | | T4 |

Teacher choice is a licence question as much as an accuracy question (Section 5.1): IndicConformer (MIT) and Nemotron-3.5 (OpenMDW) are usable; Parakeet-1.1B Indic and Bodhan are not recommended. IndicConformer's Telugu error on IndicVoices is ~27% WER [V, Svanita's run], so pseudo-labels need confidence and agreement filtering.

### 6h. Noise and augmentation data

| Source | Licence | Verdict |
|---|---|---|
| MUSAN (SLR17) | CC BY 4.0 | T1; ship attribution list |
| Vaani-Noise-Event | cc-by-4.0 | T1; real Indian phone noise (154.6 h of timestamps) |
| Simulated RIRs (SLR26-type) | Apache-2.0 | T2 |
| RIRS_NOISES real RIRs (SLR28) | Apache label, but components: RWCP research-only, Aachen AIR unstated | T3: do not use |
| DEMAND | BY-SA 3.0 (description) vs cc-by-4.0 (metadata) | T2; use stricter |
| FSD50K, AudioSet, WHAM!, DNS, ESC-50, MS-SNSD | Not verified [U]; from general knowledge FSD50K has per-clip CC licences including NC clips, AudioSet is YouTube audio, WHAM! is non-commercial | Do not use until read |
| SVQ conditions; Kathbath noisy tars | CC BY 4.0; Kathbath rejected recordings | Eval; regenerate our own noisy Kathbath test instead of the Vistaar zip |

### 6i. TTS datasets (brief; only if TTS is in scope)

| Language | Best option | Notes |
|---|---|---|
| Hindi | SYSPIN ~119 h (1 M + 1 F, studio 48 kHz, CC BY 4.0 per AIKosh/project page, T&C unread); Rasa 50.8 h; IndicVoices-R 74.6 h (BY vs BY-ND) | IndicTTS ~10 h (T3); BharatVani T4; Chaashini T3 |
| Telugu | SYSPIN ~115 h; Rasa 52.3 h; IV-R 136.4 h | IndicTTS 8.74 h (T3); SLR66 ~8 h (BY-SA) |
| English-India | SYSPIN/LIMMITS English 80 h (licence unstated; third-party review reports errors) | IndicTTS-English (T3); LibriTTS-R licence unread |

Prasad's Telugu TTS used a **third-party re-upload** of SYSPIN with no licence text; going to the original (CC BY 4.0 per AIKosh) is cleaner. A Telugu CTC aligner (not Meta MMS) is required for Pocket TTS training.

### 6j. Transcript-convention problems and what the data pipeline must do

| Problem | Evidence | Pipeline action [P] |
|---|---|---|
| English written in native script (IndicVoices, Kathbath, RESPIN) | IndicVoices cleaned `text` has no Latin; preview shows e.g. "हाइवेस्टर"; Lahaja paper states Devanagari for code-mixing; RESPIN removed English | Decide the output policy (Latin for English), then recover Latin via raw annotations (if present), lexicon + back-transliteration, and measure error on sets with Latin ground truth |
| Vaani braces and tags | `ट्रक {truck}`, `[unintelligible]`, `<PAUSE>`, `--`, `{...}` also marks misspoken-word corrections; invalid if >25% marked; stray Latin letters in a Telugu sample ("bపార్కింగ్") | Parse braces into either native-only or Latin-substituted targets; drop `<UNKNOWN_SEGMENT>`; spot-check Telugu labels |
| Noise tags (89 in the IndicVoices schema) and verbatim vs normalised fields | IndicVoices has `verbatim`, `normalized`, `unsanitized_*`; spellings differ | Pick one field per policy; strip tags; log the normaliser version |
| No punctuation/casing | IndicVoices `text` is punctuation-free; NVIDIA's recipe expects punctuated, cased text | Decide punctuation policy; if punctuation is wanted, add a separate layer (Telugu/Devanagari have no case) |
| Numbers | Words in IndicVoices, Kathbath, Vaani; digits expanded in RESPIN; Latin/Arabic digits in DiarBench normalised form | Freeze one number policy; test ITN as a separate stage |
| Label errors | Kathbath Hindi errors (discussion #3), Malayalam corruption; IndicVoices truncated audio and shared speaker IDs (discussion #12, 2026-10-05); Shrutilipi alignment at clip edges | Length/CER filters against a teacher; speaker-ID audit; drop `verification_report` failures |
| Test leakage | IV-R test vs IV train; Nirantar test vs IV; Lahaja/Svarah prompts vs IV prompts; shared text in RESPIN; FLEURS/CV in teacher training | Text and speaker dedupe; speaker-disjoint splits we build ourselves |
| Licence provenance | Gates, AIKosh, aggregators | Per-source manifest: dataset, version/hash, URL, dated licence snapshot, gate text (screenshot), citation string, tier |
| Whisper normaliser | Known to mangle Indic text (project rule) | Use our frozen versioned normaliser only |

---

## 7. Corrections to earlier project documents

| Earlier claim / unknown | Now |
|---|---|
| **U-01** Nemotron-3.5 licence unresolved (OpenMDW vs NVIDIA Open Model License; text unread) | **Resolved:** HF weights = OpenMDW-1.1, full text read; OML only on NIM/Together channel and in launch-day metadata (fixed 2026-06-05). Keep L-01 for NVIDIA's written confirmation and counsel review of upstream-data risk. |
| **U-02** Is Telugu among the 8 adaptation-ready locales? | **Resolved: no.** Zero Telugu tokenizer tokens; `te-IN` prompt slot (40) is reserved. |
| **U-03** CTC head? | **Resolved: none** (RNNT-only). |
| Blog says nothing about adding new tokens | Blog silent, but NVIDIA's separate notebook documents the route (new tokenizer, merge, decoder re-init). |
| "NVIDIA says a few hundred hours adds a language" [V] | **Not found in any NVIDIA source read** (blog, notebooks, HF discussions); NVIDIA gives no hours; its toy run reached ~60% WER. Treat as unsupported. |
| NVIDIA gives no GPU spec | Still none; staff comment: L40S, <= $50 for experiments; default `batch_duration` 200-400 s. |
| NeMo-Speech.cpp has no CPU figures | Vendor figure exists: English Q8_0, 27 ms per 160 ms chunk, ~6x real time on i7-11700K [V]. |
| **U-15** Silero licence | **Resolved: MIT**; "CC BY-NC" is stale badge alt text. TEN VAD text read (Apache + non-compete); Aksharamukha AGPL-3.0; uroman MIT + acknowledgement. |
| **U-08** IndicConformer MIT vs CC-BY-4.0 | MIT is authoritative (GitHub, LICENSE, per-language cards, AIKosh); CC-BY-4.0 also sits on AI4Bharat's own `ai4bharat/IndicConformer` template repo. Gate text for model repos still unread. |
| Parakeet-1.1B Indic community licence | Read: NIM required for production and no use of outputs to improve other models; Indic variant has no Telugu. Disqualified. |
| Bodhan Indic-Transcribe "post-trained on Nemotron 3.5" (press) | HF metadata says base is `canary-1b-v2`; licence read in full: share-alike on shipped derivatives, "trained substantially on Output" = Derivative. |
| Gate text "only visible after login" for AI4Bharat/IIT-M datasets | Gate = HF default contact-sharing text; no custom prompt in the API [OURS]. Vaani adds a "use for" selector. Model-repo gates still unread. Gates do not control access (public tars). |
| Kathbath licence | Three labels (YAML BY, body CC0 packaging, AIKosh BY-SA); HF holds clean train+valid only (~141 / ~145 h), not the full 1,684 h; test and noisy splits only via IndicSUPERB tars. |
| IndicVoices-R | BY in four first-party places, BY-ND on AIKosh; treat as BY-ND. |
| IndicVoices hours | Successive snapshots (7.3k, 12k, 23.7k total); per-language hours are ranges (Hi 0.52-0.84k, Te 0.39-0.51k [E]). |
| Shrutilipi | HF copy ~850 h Hindi / ~49 h Telugu, not 1,620 / 390; AIR copyright makes it T3 leaning T4. |
| IndicTTS on AIKosh is BY-SA | Phase-3 pages are CC BY 4.0; BY-SA was on the 2025-02-24 Vistaar-copy bulk upload. IITM PDF still unread. |
| SPRING-INX | CC BY 4.0 on AIKosh vs "public domain" in the paper; Hindi has no HF repo; Telugu not released. |
| SLR103 T3; MUCS Telugu | SLR103 -> T2 (O-UDA-1.0 by ID, secondary source). MUCS Telugu/Microsoft Speech Corpus confirmed T4. |
| Telugu is the binding data constraint (~670 h T1 [E]) | Raw read volume is larger (RESPIN ~1.0-1.3k h, Numo 1.2k h, both T2; SYSPIN/Rasa small) but **spontaneous Telugu is still ~0.55-0.7k h**; the constraint shifts from volume to spontaneous diversity and licence confirmation. |
| Code-switch gap | Confirmed; HiACC added (5.24 h); Telugu-English: nothing released. |
| Svanita claims in the chat notes | See Section 3.4: Telugu numbers, data and hardware are on the HF card. |
| Kyutai: STT code might exist | Confirmed absent; maintainer will not release; D-009 strengthened. Pocket TTS training code is real (Aug 2026). |
| Context file: ~$340 on a single A10 | Unchanged; remains [E] and depends on Q17 (compute). |

---

## 8. Implications for the plan (proposals; `pipeline.md` is not edited)

Per `CLAUDE.md`, any change needs a logged D-### first.

1. **Per-language models [P].** Three separate models are feasible on one NVIDIA base: Hindi from `hi-IN` (already transcription-ready), English from en-US (or the English checkpoint), Telugu via the documented new-tokenizer route. Costs: three tokenizers, three export/quantisation/evaluation passes and three on-device bundles (~650 MB each at int8 [E from the chat notes], so a device keeps one loaded). Per-language models do not shrink the 600M encoder; a smaller student (~100-120M) is a later, separate decision.
2. **Telugu data position [P].** Treat the T1 spontaneous core (IndicVoices + Vaani, ~0.55-0.7k h) as the MVP anchor and the T2 read pools (RESPIN, Numo) as capped add-ons gated on written confirmation; use Vaani Telugu pseudo-labels (IndicConformer teacher, filtered) as the main lever for more spontaneous volume; do not claim the Telugu supply problem is solved.
3. **Tokenizer route [P].** Log a decision between merge and a minimal Telugu+Latin tokenizer; run both in the Stage 1 spike if budget allows. Measure tokens per word for Hindi before deciding whether Hindi keeps Nemotron's tokenizer.
4. **Compute [P].** Q17 (one A10G vs 8x A10 vs 8x A100) blocks every cost number. A10G is a listed supported architecture; full fine-tune memory fit and throughput remain unmeasured (U-17). Expect Telugu to cost the most (from-scratch decoder plus encoder adaptation). More GPUs shorten wall-clock, not GPU-hours. Re-base the budget only after Q17 and the Stage 1 throughput measurement.
5. **Base-model options [P/E].**
   - *Svanita encoder:* its published encoder dimensions match Nemotron-3.5's (24 layers, d=1024, 8 heads, kernel 9, 128 mel, 8x subsampling) [M both], but Svanita's is an offline full-attention encoder, Nemotron's is cache-aware with limited right context; a weight transfer is not a clean copy and nobody has shown it works. Low-probability shortcut: use Svanita as baseline only.
   - *IndicConformer:* offline teacher and reference; the ~120M per-language models are a possible small-student architecture but are not streaming.
   - *SraVaani-0.5-live:* the only Indic-native streaming checkpoint (Hindi + Telugu, ~430M, CTC only, TorchScript, gated, MIT tag). Keep it as Path C and the streaming-Telugu baseline; commercial terms and fine-tune-checkpoint access must be asked for before any commitment.
   - Parakeet-1.1B Indic, Bodhan, MMS, Seamless: out.
6. **TTS scope [P].** Adds a separate workstream, not an add-on: Kyutai Pocket TTS is the best-supported open starting point (MIT code, CC BY weights with prohibited-use terms), but needs aligned licence-clean data (SYSPIN, Rasa, IV-R), a Telugu CTC aligner, a listening evaluation and a decision on Kyutai's upstream-data risk. Decide Q21 before any TTS spend; STT does not depend on it.
7. **Kyutai for STT [P].** Keep rejected (D-009). If the senior wants a demonstration, offer a clearly labelled one-day smoke test of the unofficial patch, with the expectation that it shows only that a loop runs.
8. **A quick visible result for the senior [P].** In hours, not days: run the unmodified Nemotron-3.5 Hindi on a laptop through sherpa-onnx (export script exists) and show Hindi streaming; a Telugu tracer fine-tune (10-20 h) is the Stage 1 spike and takes days. This gives the senior a demonstration without the Kyutai-STT risk.
9. **Decisions needed from the owner/senior:** compute (Q17); three monolingual models confirmed (Q18); streaming required and which chunk size (Q19); phones vs laptops and which devices (Q20); TTS in scope (Q21); targets (Q22); whether to accept T2 data under written risk acceptance (RESPIN, Numo, SPRING-INX, Kathbath); output policy (Latin English in native-script text; punctuation); tokenizer route; go-ahead to send the Section 10 letters; counsel review of the OpenMDW/upstream-data and CC-BY-with-NC-upstream questions.

---

## 9. What could not be verified / needs the owner's browser or login

In order of decision importance:

| # | What | URL | What is hidden |
|---|---|---|---|
| 1 | Vaani gate and IndicVoices gate text, dated screenshot at acceptance | https://huggingface.co/datasets/ARTPARK-IISc/Vaani ; https://huggingface.co/datasets/ai4bharat/IndicVoices ; .../Kathbath | HF modal wording after login (API shows only default contact text, plus Vaani's "use for" selector) |
| 2 | RESPIN access form, terms, per-language hours, paper ethics/consent | https://spiredatasets.ee.iisc.ac.in/respincorpus ; paper PDF via OpenReview/NeurIPS | Form terms; the 232/283 h discrepancy; consent for open release |
| 3 | IndicConformer and SraVaani gate texts and SraVaani fine-tune-checkpoint terms | https://huggingface.co/ai4bharat/indic-conformer-600m-multilingual ; .../indicconformer_stt_{hi,te}_hybrid_ctc_rnnt_large ; .../ai4bharat/IndicConformer ; https://huggingface.co/ARTPARK-IISc/SraVaani-0.5-live ; .../SraVaani-1.0 ; .../Vaani-FastConformer-Telugu ; .../Vaani-FastConformer-Hindi | Conditions text; commercial wording |
| 4 | Numo gate and consent | https://huggingface.co/datasets/psdn-ai/numo-indic-speech ; https://www.psdn.ai/privacy | Gate conditions; whether speakers consented to open CC BY release |
| 5 | Raw `unsanitized_verbatim` field of IndicVoices Hindi/Telugu (does it keep `native [english]`?), and `duration` sums per language | https://huggingface.co/datasets/ai4bharat/IndicVoices (after access) | Decides Latin-English recovery cost and the true hours |
| 6 | bolAIndia STATS.md / MAP.md and gate | https://huggingface.co/datasets/kapturecx/bolAIndia | Source credits and usage conditions for the 190k h pool |
| 7 | IndicTTS licence PDF and database page | https://www.iitm.ac.in/donlab/indictts/downloads/license.pdf ; https://www.iitm.ac.in/donlab/indictts/database | Unreachable from our network; needed only if TTS is in scope or IndicTTS data is considered |
| 8 | LinkedIn profile and the 30 Aug / 19 Sep / 24 Sep posts | https://in.linkedin.com/in/prasadvittaldev | Authwall (HTTP 429 to the fetcher): employer, headline, comments, contact option; the exact "3 voices/316M/3.39x" wording |
| 9 | Gate for `kyutai/pocket-tts` (CC BY + prohibited-use) | https://huggingface.co/kyutai/pocket-tts | Dated copy needed if TTS proceeds |
| 10 | NGC Terms of Use; NVIDIA NIM-exemption PDF; NIM Indic profile table | https://catalog.ngc.nvidia.com/orgs/nvidia/teams/nemo/models/stt_en_fastconformer_hybrid_large_streaming_80ms ; https://www.nvidia.com/content/dam/en-zz/Solutions/license-agreements/enterprise-software/NVIDIA-Models-Community-License-2025-04-15-FINAL.pdf ; https://docs.nvidia.com/nim/speech/latest/reference/support-matrix/asr.html | Matters only for the 114M English model and Parakeet-1.1B (already excluded) |
| 11 | Bodhan gated licence files and lite model; Bhili gate | https://huggingface.co/bodhan-ai/indic-transcribe-flex ; .../indic-transcribe-lite ; https://huggingface.co/ai4bharat/bhili-asr-nemotron-600m | Public GitHub licence read instead |
| 12 | Mozilla Data Collective click-through terms | https://mozilladatacollective.com/datasets/cmu5vlext009to107ev1s9lk8 (Hindi) ; cmu617jv900jfo107hpm9aj8d (Telugu) ; cmu5jplf300nwmh07iqvk9leo (English) | Download-time terms |
| 13 | Microsoft licence IDs behind SLR103 / MUCS | https://www.openslr.org/103/ ; https://navana-tech.github.io/MUCS2021/data.html | Host dead; text only via a secondary source |
| 14 | NPTEL content licence; SPIRE-SIES form; IIIT-H challenge page; HiACC child-consent paper | https://nptel.ac.in ; https://forms.office.com/r/bF27ah1Fg9 ; https://asr.iiit.ac.in/asr_challenge ; https://www.sciencedirect.com/science/article/pii/S2352340925006109 | Ambiguous or unreachable |
| 15 | Not audited | n/a | FSD50K/AudioSet/WHAM!/DNS licences; EdAcc; MLS English hours; YODAS per-language hours; TED-LIUM direct pages; Kaggle sets; Omnilingual Hindi/Telugu CER; Kyutai X/Reddit/HN threads (X returned HTTP 402); `kyutai.org/next/stt` (JS-rendered); Kyutai HF discussion tabs; Pocket TTS technical report; A10G throughput for any of these (no data exists) |

---

## 10. Draft licensor/author questions (NOT SENT; each needs the owner's explicit go-ahead)

**NVIDIA (Nemotron team; HF discussions or Riva contact)**
1. Please confirm in writing that OpenMDW-1.1 governs the weights, `.nemo`, safetensors and q8_0 GGUF of `nvidia/nemotron-3.5-asr-streaming-0.6b`, including copies downloaded on or before 2026-06-05, and the NIM-served builds.
2. Does notice retention require a separate NOTICE file beyond the model card, and may we ship int8/ONNX conversions and fine-tuned derivatives on end-user devices under OpenMDW-1.1 alone?
3. Is the training data (Riva multilingual set, Granary, MLS, Common Voice, FLEURS, VoxPopuli; pseudo-labels from Canary, Parakeet 1.1B, Whisper, FunASR) cleared for commercial redistribution of derivative weights?
4. Is there a recommended recipe, hardware and data size for adding a Dravidian-script language (Telugu, slot `te-IN`), and is Telugu on the roadmap?

**AI4Bharat (IndicVoices, Kathbath, IndicConformer; contacts on the HF cards)**
5. Does CC BY 4.0 on IndicVoices cover audio, transcripts and metadata for commercial training and shipping of derived weights, across all collection phases up to 23.7k h? Which attribution string do you want?
6. Which HF split is the held-out speaker-disjoint benchmark? What are the per-language transcribed hours and speaker counts of the current release? Do `unsanitized_verbatim` fields keep `native [english]` annotations?
7. Kathbath: which of CC0 (packaging) and CC BY 4.0 governs? Is commercial reuse of the IndicCorp-derived sentences and recordings covered by the consent given ("research purposes")?
8. IndicVoices-R: is the licence CC BY 4.0 or CC BY-ND 4.0 (AIKosh)? Do IV-R test items appear in IndicVoices train?
9. IndicConformer (600M and per-language hi/te): confirm MIT as on GitHub; reconcile `ai4bharat/IndicConformer` (CC BY 4.0); what do the HF gate conditions require; which datasets trained the models and are they cleared for commercial use of the weights?
10. Shrutilipi: did AI4Bharat hold written permission from All India Radio / Prasar Bharati for commercial training and redistribution? NPTEL2020: what is the rights position on the subtitle text and YouTube-CC videos?

**ARTPARK-IISc / Vaani (vaanicontact@gmail.com, agneedh@artpark.in per cards)**
11. Does the Vaani gate (or any text behind it) allow commercial model training and redistribution of derived weights? Is Phase-2 audio in the public repo? Are Benchmark-V1.0 speakers disjoint from the public set? Preferred attribution?
12. SraVaani-0.5-live, SraVaani-1.0, Vaani-FastConformer-Te/Hi: do the gate terms (and the separate fine-tuning-checkpoint access) permit commercial products and commercial redistribution of fine-tuned/quantised derivatives under the stated MIT licence? Are the 24 labelled training datasets (SPICOR, SYSPIN, RESPIN, Spring-INX, IndicTTS, MUCS, GramVaani, ...) cleared for commercial use of derived weights?

**IISc SPIRE Lab / RESPIN (contact.respin@iisc.ac.in from a search summary [U])**
13. Please confirm in writing that RESPIN-S1.0 audio and transcripts are CC BY 4.0 for commercial model training, whether the access form adds terms, and the consent basis for open release. Why do paper Table 3 clean hours (944.9 Hindi / 1,304.0 Telugu) exceed the repo's `train_*_clean` (712.6 / 1,021.2)?
14. Are SYSPIN_S1.0 terms and conditions compatible with commercial TTS/ASR use, and is a SPIRE-SIES licence available?

**Poseidon AI / Numo (https://www.psdn.ai/contact)**
15. For Numo Indic Speech (CC BY 4.0): did every speaker consent to open publication under CC BY and to commercial model training? How many speakers per language, and what is the recording setup? How does your privacy statement ("may be licensed to third party AI companies") relate to the public release?

**Mozilla Data Collective / Common Voice**
16. Does the MDC clause on synthetic data and model outputs apply to ASR model weights and transcripts trained on Common Voice? Is the crowd-submitted Hindi sentence corpus (news-derived) CC0 in fact?

**Gram Vaani (contact@gramvaani.org)**
17. We would like to use Gram Vaani SLR118 for commercial ASR training. What licence terms or permission process apply, and what fee, if any?

**OpenSLR / Microsoft Research Open Data**
18. Please supply the text of the licences at the IDs `f1f352a6-243f-4905-8e00-389edbca9e83` (SLR103) and `a889b26e-5149-4486-866e-ec896bb728c4` (MUCS Telugu/Tamil/Gujarati) and confirm whether SLR103 is under the Open Use of Data Agreement v1.0 and whether upstream audio rights are cleared.

**Kapture CX**
19. For `kapturecx/bolAIndia` and `Chaashini`: what are the sources of the audio, what licences or permissions apply to each source, and does the Apache-2.0 label on Chaashini cover the audio? Why does the bolAIndia repo contain `newsonair` archives?

**Kyutai (GitHub issue/discussion; only if TTS proceeds)**
20. Which datasets and licences underlie the multilingual Pocket-TTS weights and the Mimi codec, given the NC-licensed corpora named in the CALM paper? Can you confirm the CC0 status of the default `estelle` voice and the licences of the non-English default voices (DSM #180)? Is the CC BY 4.0 + prohibited-use text the full set of terms for derived models?

**Prasad Vittaldev (HF Community tab of `svanita-0.6b`, or LinkedIn)**
21. May Svanita (v0.1, v0.2) be used commercially, fine-tuned and used as a pseudo-label teacher under CC-BY-4.0, and what attribution wording do you want? Which dataset versions and valid-split rule did you use, and will you release manifests/speaker lists, training and evaluation scripts, and the normaliser?
22. What exact int8/ONNX setup failed (+30 WER), and have you tried chunked or streaming inference?
23. For the Telugu Pocket TTS: will the 24-layer teacher be released, and which corpora and licences make up the 124 h (IndicTTS vs SYSPIN vs others)? Which GPU was used?

**Agora (TEN VAD)**
24. If ten-vad ships inside an on-device speech-recognition SDK offered to third-party app developers, does that fall under condition 1 (competing with Agora's offerings or enabling others to deploy Applications)?

**Bodhan AI (support@bodhan.ai per licence s15.6)**
25. Is a model trained on Indic-Transcribe transcriptions (pseudo-labels) a "Derivative" if the outputs are a small fraction of its training data? Is a real-time lite model released, and may it be a base for an on-device product without carrying the share-alike and attribution terms to end users?

---

## 11. Evidence pack for the senior: plain-language talking points

1. **There are two Prasad projects.** The Kyutai one is a Telugu text-to-speech model trained on 124 hours; the speech-to-text one (Svanita) is built on NVIDIA's Parakeet, used 1,136 hours and runs offline. The "Kyutai + home GPU + ~120 hours" story is the TTS.
2. **Prasad's STT is a useful yardstick, not a head start.** Its own table shows AI4Bharat's IndicConformer is better (Hindi 15.5 vs 23.7 WER; Telugu 27.4 vs 37.7), and the author reports that int8 and ONNX conversion broke accuracy. It runs on a desktop CPU in fp32 as a whole-utterance model, not streaming.
3. **Kyutai has not released any speech-to-text training code, and has said it won't.** Checked across their whole GitHub organisation; the pocket-tts repo is text-to-speech only.
4. **Kyutai's speech-to-text can't run live on a laptop CPU.** The models are 1-2.6 billion parameters; the best community laptop measurement is about two thirds of real time, there is no Android route, and Kyutai themselves describe GPU servers and Apple chips.
5. **"An hour or two" is true for a smoke test, not for a Telugu model.** For TTS, the GPU part is under an hour on a big card, but the days go into aligned, licensed data and listening tests. For STT, Kyutai themselves say a new language needs thousands of aligned hours and a new tokenizer.
6. **The NVIDIA route is the documented one.** Nemotron-3.5 already does streaming Hindi well, has a permissive licence (OpenMDW-1.1: commercial use, fine-tuning and shipping all allowed, outputs unrestricted), and NVIDIA publishes a recipe for adding a new language. Honest risk: Telugu is not in the model, so it needs a new decoder and real training data; NVIDIA gives no number for how much.
7. **Datasets are pairs, but not clean or free of strings.** English words appear in native script or in braces depending on the dataset; labels have errors; test splits are missing; several licence labels contradict each other; "open" aggregator copies often carry false licence tags. We keep a per-dataset licence log and use the stricter reading.
8. **We have more usable Telugu audio than we feared, but less of the right kind.** Clearly licensed Telugu is roughly 0.55-0.7k hours of spontaneous speech, plus 1.2-2.8k hours of read speech that needs a written licence check. No open Telugu-English code-switch corpus exists, so we build that ourselves.
9. **One person did Telugu+Hindi on one consumer GPU, so compute is not the obstacle.** The hard parts are data licences, streaming, a quantised (int8) model that keeps its accuracy, and testing on real laptop microphones.
10. **What we need from you:** the compute answer (one A10G, eight A10, or eight A100), confirmation of streaming and target devices, whether TTS is in scope, and approval to send licence questions to NVIDIA, AI4Bharat, ARTPARK and IISc. In return we can show Hindi streaming from the unmodified NVIDIA model on a laptop quickly, and a Telugu feasibility result after the spike.

---

## 12. Source list (all fetched 2026-10-12)

**Svanita / Prasad Vittaldev**
- https://huggingface.co/prasadvittaldev/svanita-0.6b (+ raw README, config.json, tokenizer.json, transcribe_cpu.py, refs, commits, discussions; v0.1 branch README); https://lnkd.in/gmpu42-w
- https://huggingface.co/prasadvittaldev (profile/API); https://github.com/prasadvittaldev (API, `indian-unmute` README)
- https://huggingface.co/prasadvittaldev/pocket-tts-telugu-female-syspin ; .../pocket-tts-hindi-female-syspin ; .../pocket-tts-tamil-female-audiobook ; .../pocket-tts-indian-english-male-indictts ; https://prasadtts.vercel.app
- https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3 ; https://huggingface.co/datasets/SPRINGLab/IndicTTS_Telugu ; https://huggingface.co/datasets/arpit-tiwari/syspin-telugu-tts
- https://in.linkedin.com/in/prasadvittaldev (authwall)

**Kyutai**
- https://github.com/kyutai-labs/delayed-streams-modeling (tree, FAQ, issues #4, #64, #69, #73, #121, #168, #171, #176, #180) ; https://github.com/kyutai-labs/pocket-tts (README, LICENSE, `training/README.md`, `training/configs/finetune_language.yaml`; issues #30, #118, #254, #261, #281, #288) ; https://github.com/kyutai-labs/moshi ; https://github.com/kyutai-labs/moshi-finetune (issues #4-#9, #21) ; https://github.com/kyutai-labs/unmute ; https://github.com/kyutai-labs/hibiki-zero
- https://huggingface.co/kyutai/pocket-tts ; .../stt-1b-en_fr ; .../stt-2.6b-en ; .../mimi ; .../tts-1.6b-en_fr ; .../tts-voices ; .../hibiki-zero-3b-pytorch-bf16
- Community: https://huggingface.co/saryps-labs/pocket-tts-hindi ; .../Indus-Labs/indus-pocket-tts ; .../altslate/jugnu-pocket-tts ; .../mideind/kyutai-stt-1b-is-en ; https://github.com/Codes4Fun/moshi.cpp ; https://github.com/lucky-bai/wasm-speech-streaming
- Papers: https://arxiv.org/abs/2509.08753 (Delayed Streams Modeling) ; https://arxiv.org/abs/2509.06926 (CALM)

**Models and tools**
- https://huggingface.co/nvidia/nemotron-3.5-asr-streaming-0.6b (README, config, tokenizer, discussions, commits) ; https://huggingface.co/blog/nvidia/fine-tuning-nemotron-35-asr ; https://github.com/nvidia-riva/tutorials (`asr-finetune-nemotron-3.5-asr-streaming-prompt.ipynb`, `asr-extend-tokenizer-to-newlang-ft-acoustic-model.ipynb`) ; https://github.com/NVIDIA-NeMo/NeMo (streaming prompt config) ; https://github.com/k2-fsa/sherpa-onnx/tree/master/scripts/nemo/nemotron-3.5-asr-streaming-0.6b ; https://github.com/NVIDIA/NeMo-Speech.cpp
- Licences: https://openmdw.ai/license/1-1/ ; https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license/ ; https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-ai-foundation-models-community-license-agreement/ ; https://github.com/Bodhan-AI/bodhan-model-info/blob/main/licenses/indic-open-model-license/v1/Indic_Open_Model_License.md ; https://raw.githubusercontent.com/TEN-framework/ten-vad/main/LICENSE ; https://raw.githubusercontent.com/snakers4/silero-vad/master/LICENSE ; https://raw.githubusercontent.com/isi-nlp/uroman/master/LICENSE.txt
- NGC/NIM: https://catalog.ngc.nvidia.com/orgs/nim/nvidia/containers/nemotron-asr-streaming ; https://together.ai/models/nvidia-nemotron-35-asr
- Indic: https://huggingface.co/ai4bharat/indic-conformer-600m-multilingual ; https://github.com/AI4Bharat/IndicConformerASR ; https://github.com/AI4Bharat/vistaar ; https://huggingface.co/ARTPARK-IISc/SraVaani-0.5-live ; .../SraVaani-1.0 ; https://arxiv.org/abs/2608.08235 ; https://huggingface.co/bodhan-ai/indic-transcribe-flex ; https://huggingface.co/ai4bharat/bhili-asr-nemotron-600m

**Datasets: AI4Bharat / IITM**
- https://huggingface.co/datasets/ai4bharat/{IndicVoices, indicvoices_r, Kathbath, Shrutilipi, Lahaja, Svarah, Rasa, IndicCMix, Rural_Women_ASR_v2} ; https://github.com/AI4Bharat/{IndicVoices, IndicVoices-R, IndicSUPERB, Lahaja, Svarah, Rasa, Nirantar, vistaar, NPTEL2020-Indian-English-Speech-Dataset}
- Papers: https://arxiv.org/abs/2403.01926 (IndicVoices), 2409.05356 (IV-R), 2208.11761 (IndicSUPERB/Kathbath), 2208.12666 (Shrutilipi), 2408.11440 (Lahaja), 2305.15760 (Svarah), 2310.14654 (SPRING-INX), 2411.04699 (BhasaAnuvaad), 2507.00534 (Nirantar)
- AIKosh pages (indicvoices, indicvoices_r, spring_inx_hindi, iisc_respin_s1_0_corpus, iisc_syspin_s1_0_corpus) under https://aikosh.indiaai.gov.in/home/datasets/details/ ; https://www.newsonair.gov.in/copyright-policy ; https://www.iitm.ac.in/donlab/indictts/downloads/license.pdf (unread)

**Datasets: other**
- https://huggingface.co/datasets/ARTPARK-IISc/Vaani (+ `-transcription-part`, `-Benchmark-V1.0`, `-Noise-Event-Dataset`) ; https://vaani.iisc.ac.in/ ; https://arxiv.org/abs/2603.28714
- https://github.com/saurabhk0317/respin_data_neurips25 ; https://spiredatasets.ee.iisc.ac.in/respincorpus ; https://papers.nips.cc/paper_files/paper/2025/hash/d88714d4f2c1e826d33d6c1eb1497ec9-Abstract-Datasets_and_Benchmarks_Track.html
- https://huggingface.co/datasets/psdn-ai/numo-indic-speech ; https://www.psdn.ai/privacy
- https://github.com/common-voice/cv-dataset ; https://mozilladatacollective.com/terms ; https://huggingface.co/datasets/google/fleurs ; https://huggingface.co/datasets/google/svq ; https://www.openslr.org/ (SLR12, 17, 26, 28, 66, 94, 103, 104, 118) ; https://github.com/microsoft/Open-Use-of-Data-Agreement ; https://www.microsoft.com/en-us/download/details.aspx?id=105292
- https://zenodo.org/records/15551669 (HiACC) ; https://zenodo.org/records/1227121 (DEMAND) ; https://huggingface.co/datasets/kapturecx/{bolAIndia, Chaashini, Vartalaap} ; https://huggingface.co/datasets/projectkaira/Pretraining-V1 ; https://huggingface.co/datasets/agarwalayushi/hinglish ; https://huggingface.co/datasets/sarvamai/indic-diarbench
- Code-switch references: https://arxiv.org/abs/2006.00782 (MSR Telugu-English) ; https://arxiv.org/abs/2406.10993 (CoSTA) ; https://arxiv.org/abs/2312.00698 (SPIRE-SIES)
- Gate-text controls: https://huggingface.co/datasets/speechcolab/gigaspeech ; https://huggingface.co/datasets/amphion/Emilia-Dataset

*End of report. Nothing here was sent to any third party; all drafts in Section 10 await the owner's explicit go-ahead.*
