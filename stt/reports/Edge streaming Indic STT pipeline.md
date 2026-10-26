# Post-train Nemotron 3.5 for edge Indic streaming

**Recommendation: post-train NVIDIA's Nemotron-3.5-ASR-Streaming-0.6B (cache-aware FastConformer-RNNT, Hindi already supported, commercial licence stated on the card) to add Telugu, Indian-English and Hindi-English/Telugu-English code-switching, then ship it as an int8 ONNX model through sherpa-onnx on x86 and Apple-silicon CPUs. Treat this as a conditional recommendation that must pass a 1-2 week de-risking spike before anything else is built.** No existing checkpoint meets all the constraints (true streaming, Hindi + Telugu + English, <=~600M parameters, clear commercial licence, CPU runtime). The nearest checkpoints each fail one: Nemotron 3.5 has no Telugu, SraVaani-0.5-live has Telugu but is CTC-only, gated and has no CPU export, and IndicConformer has both languages but is offline. So the project is a real post-training effort, not a model selection. The fallback is a ~114M cache-aware NeMo hybrid FastConformer retargeted with a new Hindi/Telugu/English tokenizer. Both paths go through the same sherpa-onnx export. The binding constraint is data, not compute: commercial-safe transcribed Telugu is only about 0.7k hours, and no open Telugu-English code-switch corpus exists, so synthetic data and a small in-house test set are mandatory. The compute plan (about 340 A10G GPU-hours, roughly $340 on-demand or $170 on spot, all estimates) fits a few-hundred-dollar budget. The honest accuracy expectation is that published streaming Telugu sits near 30 WER (SraVaani-live, 31.4 at 480 ms) versus about 25 for the best offline open models, so Telugu may reach MVP quality before production quality. Seniors should decide whether to scope Hindi + English as GA and Telugu as beta.

**Label legend used throughout.** **[M]** = measured and reported by a cited source (their setup, not ours); **[V]** = vendor-claimed, unverified; **[E]** = our estimate or extrapolation, not sourced, must be validated; **[P]** = our proposal (a threshold or design choice). Source conflicts are collected in Section 8 rather than smoothed over.

---

## Decision summary: one primary path, two fallbacks, a long disqualified list

| Item | Decision | Why (evidence label) |
|---|---|---|
| **Primary path (Path A)** | Nemotron-3.5-ASR-Streaming-0.6B, full fine-tune, multi-lookahead cache-aware training, new Telugu/code-switch language handling, int8 sherpa-onnx | Only candidate with native cache-aware streaming (80-1120 ms), Hindi in the top tier, a public fine-tuning recipe, a maintained sherpa-onnx loader and a card statement of commercial readiness ([card](https://huggingface.co/nvidia/nemotron-3.5-asr-streaming-0.6b)). Hindi FLEURS WER 8.13 (80 ms) to 6.81 (1.12 s) [M, vendor-run, FLEURS is in its training data]. |
| **Fallback 1 (Path B)** | ~114M cache-aware NeMo hybrid FastConformer (`stt_en_fastconformer_hybrid_large_streaming_*`) with a new aggregate hi/te/en tokenizer; run as bake-off Arm B | Roughly 4-5x cheaper per audio second on CPU [E], and 5x cheaper to train [E]. Weakness: English-only pretraining. The Typhoon precedent used ~10,000 h of Thai to retarget a 114M FastConformer-Transducer ([card](https://huggingface.co/typhoon-ai/typhoon-asr-realtime)), far more than our T1 Telugu supply. |
| **Fallback 2 (Path C)** | Continue from ARTPARK-IISc SraVaani-0.5-live (430M, streaming, Hindi + Telugu), only if ARTPARK grants fine-tuning-capable weights and written commercial terms | Best published open streaming Telugu number: 34.6/33.6/31.4/30.3 WER at 0/80/480/1040 ms lookahead [M, vendor-run] ([card](https://huggingface.co/ARTPARK-IISc/SraVaani-0.5-live)). Gated, CTC-only (no hotwords), TorchScript fp16 only, no ONNX. Also the key streaming Telugu baseline to beat. |
| **Floor option (Path D)** | icefall streaming Zipformer (~65M) trained or warm-started on our data, distilled from the Path A/B model | Mature sherpa-onnx loader; 66M int8 Zipformer measured at RTF 0.035 on a 4-thread Xeon [M, community] ([card](https://huggingface.co/Akshatkasera007/STT-streaming-zipformer-indian-en)). No Indic Telugu checkpoint exists, so only a last resort. |
| **Teachers (not deployed)** | IndicConformer-600M (MIT tag, gated) and SraVaani-1.0 (MIT tag, gated) for pseudo-labels and offline reference | Best open offline Hindi/Telugu: IndicConformer 13.8/26.4, SraVaani-1.0 14.0/25.1 mean WER [M] ([SraVaani paper](https://arxiv.org/html/2608.08235)). Not Whisper-large-v3 (Telugu script collapse) and not Sarvam/Gemini/Deepgram APIs (ToS risk). |
| **Disqualified** | MMS, Whisper-family (and WhisperRT), Voxtral Realtime, Qwen3-ASR, Kyutai, Parakeet-v3/Canary-v2, Parakeet Indic 1.1B, Indic-Transcribe, Omnilingual (as deployed model), Moonshine, Sarvam/Gnani | See the disqualified table in Section 1. |

**What "no checkpoint meets every constraint" implies.** (1) The project is a post-training programme with a real risk of failure, so a spike and a bake-off precede any large spend. (2) The first unknown is whether Nemotron 3.5's tokenizer and prompt mechanism can absorb Telugu; the notes could not verify this. (3) Every Telugu number we will ever show must come from our own data and our own harness, because no published streaming Telugu baseline other than SraVaani-live exists, and no published Telugu-English baseline exists for any model. (4) Commercial clearance is a separate gating workstream from engineering: several "MIT" Indic checkpoints are gated and several "CC-BY" datasets carry conflicting labels (Section 2).

---

## 1. Base-model and lab comparison: Nemotron wins on fit, Indic labs win on data

### 1.1 Candidate base models scored against the constraints

| Candidate | True streaming | Hindi | Telugu | Size | Licence | CPU/edge runtime | Evidence and caveats | Verdict |
|---|---|---|---|---|---|---|---|---|
| **Nemotron-3.5-ASR-Streaming-0.6B** | Yes, cache-aware RNNT, 80/160/320/560/1120 ms via `att_context_size=[56,N]` | Yes: FLEURS 8.13 to 6.81; Vaani benchmark 20.2 [M, vendor] | **No** (not among 40 locales; tokenizer coverage unverified) | ~600M | OpenMDW-1.1 "ready for commercial use" (HF card); Together AI listing says NVIDIA Open Model License (conflict) | sherpa-onnx >=1.13.3 loader; int8 ONNX ~650 MB; OpenVINO, GGUF, CoreML, MLX community ports ([changelog](https://pub.dev/packages/sherpa_onnx_linux/changelog)) | Public fine-tune recipe; full FT only (LoRA unsupported per author) ([blog](https://huggingface.co/blog/nvidia/fine-tuning-nemotron-35-asr)) | **Primary** |
| **NeMo 114M cache-aware hybrid** (EN, 80/480/1040 ms) | Yes | No (English-only) | No | ~114M | Not retrieved (gap) | NeMo-to-sherpa export scripts exist; RTF unmeasured | Needs new tokenizer; retargeting precedent needed ~10k h | **Fallback 1 / Arm B** |
| **SraVaani-0.5-live** | Yes, cache-aware FastConformer, CTC only | 22.1/21.3/19.3/18.0 WER [M, vendor] | 34.6/33.6/31.4/30.3 WER [M, vendor] | ~430M (fp16 TorchScript ~900 MB) | MIT tag, gated | No ONNX; `trust_remote_code`; "real-time-safe" CPU claim without numbers | Card inconsistent on Hindi-only streaming WER; no code-switch evaluation | **Fallback 2 / Arm C if access** |
| **IndicConformer 600M / 120M** | No (offline); streaming variant unreleased | 13.8 mean WER [M, 3P] | 26.4 mean WER [M, 3P] | 600M multi / ~120M per-language | MIT tag, gated (community GGUF says CC-BY-4.0) | Community ONNX/GGUF/CoreML; 120M Hindi Q8 GGUF RTF 0.06 [M, community, CPU unspecified] | Converting offline to cache-aware has no published recipe | **Teacher / offline reference** |
| **SraVaani-1.0** (offline) | No | 12.4 (card) vs 14.0 (paper) | 25.1 | ~430M | MIT tag, gated | ONNX "linked externally" | Code-switched transcripts removed from its fine-tuning data | **Teacher** |
| **icefall streaming Zipformer** | Yes | Community Hindi/Hinglish 64.6M CTC: 25.7% IndicVoices-hi from ~337 h [M, community] | None | 65-66M | Apache-2.0 (community cards) | Most mature sherpa-onnx path; int8 ~68 MB | Telugu from scratch impractical on one A10G | **Floor option** |
| **Qwen3-ASR 0.6B/1.7B** | Yes (2 s chunks) | FLEURS 19.12/17.15 [M] | **No** | 0.6B/1.7B | Apache-2.0 | GPU-serving oriented | Unsupported Indic language scored 153% WER after naive use (Tamil, community) | Disqualified |
| **Omnilingual CTC-300M** | No (<40 s inputs) | 7B-only CSV: CER 3.6 | 7B-only CSV: CER 6.5 | 325M | Apache-2.0 | fairseq2, no CPU guidance | Third-party conversational Telugu OIWER 50.7 (7B) | Teacher/SSL option only |

Sources for the table: Nemotron card and changelog as linked; [SraVaani-1.0 paper](https://arxiv.org/html/2608.08235); [IndicConformer card](https://huggingface.co/ai4bharat/indic-conformer-600m-multilingual); [Hindi/Hinglish Zipformer](https://huggingface.co/Vengadanathan/hindi-hinglish-zipformer-ctc-streaming); [Qwen3-ASR report](https://arxiv.org/html/2601.21337); [Omnilingual repo](https://github.com/facebookresearch/omnilingual-asr); [Voice of India](https://arxiv.org/html/2604.19151).

**Why Nemotron beats SraVaani as primary despite SraVaani's Telugu.** SraVaani-live already proves ARTPARK built a Hindi + Telugu cache-aware model, but it is CTC-only, which rules out hotwords and modified beam search in sherpa-onnx (those require a transducer) ([hotwords docs](https://k2-fsa.github.io/sherpa/onnx/hotwords/index.html)). It also ships only as TorchScript. Nemotron has the maintained export path and a 600M encoder trained on 10k-1M hours (vendor range). Path A's risk is Telugu, Path C's risk is access, licence and export; both are cheap to test in the spike and the bake-off.

**Evidence on the streaming penalty.** SraVaani-live versus the larger offline SraVaani-1.0 shows +5.2 to +9.5 absolute WER on Telugu and +4.0 to +9.7 on Hindi, confounded by model size and training differences [M]. Nemotron's Hindi improves 16% relative from 80 ms to 1.12 s chunks [M] ([card](https://huggingface.co/nvidia/nemotron-3.5-asr-streaming-0.6b)). Our working expectation is +15-25% relative at 0.5-1.1 s chunks versus the same architecture offline, and more at 0-80 ms, with a further +10-30% for a small int8 model [E]. No source measures all three together for Hindi or Telugu.

### 1.2 Lab methodologies: what each contributes at one-A10G scale

| Lab / methodology | Core recipe | Published compute and data | Transferable to our budget? | Rank |
|---|---|---|---|---|
| **NVIDIA NeMo** | Cache-aware FastConformer, hybrid RNNT/CTC, one model for many chunk sizes, LID prompt conditioning, Granary-style pseudo-label filtering ([Stateful Conformer](https://arxiv.org/html/2312.17279v3)) | Streaming paper: ~114M model, 200+ epochs, ~26k h; Parakeet-v3 final fine-tune 5k steps on 4 A100 with 7.5k h ([Canary-v2/Parakeet-v3](https://arxiv.org/html/2509.14128v2)) | **Yes**: the checkpoint is released; we only fine-tune. NVIDIA FAQ [V]: "a few hundred hours" adds a language ([FAQ](https://perspectives.nvidia.com/nemotron-speech/task/faq/how-much-training-data-do-i-need-to-fine-tune-a-multilingual-streaming-asr-model/)) | 1 |
| **AI4Bharat / IISc-ARTPARK** | Open Indic data (IndicVoices, Kathbath, Vaani), MIT FastConformer teachers, SSL + audio-image alignment (25% relative WER gain on FLEURS Indic, strongest at 10-100 h) ([arXiv 2606.24080](https://arxiv.org/abs/2606.24080)) | SraVaani-1.0: 31.3k h unlabelled SSL, ~30.6k h supervised | **Yes as data and teacher source**; SSL pretraining not affordable. AI4Bharat built a cache-aware Bhili model from Nemotron-600M with ~200 h ([card](https://huggingface.co/ai4bharat/bhili-asr-nemotron-600m)) | 2 |
| **k2 / Zipformer** | Causal chunked Zipformer, pruned RNN-T, ScaledAdam | Hindi/Hinglish Zipformer-M: single L4, ~337 h warm-start gave 25.7% IndicVoices-hi [M, community] | Yes for a small CPU-first model, but accuracy ceiling at small data and no Telugu checkpoint | 3 |
| **Meta Omnilingual / MMS** | wav2vec2 SSL to 7B, CTC or LLM decoder | 4.3M h SSL; compute not reported | Teacher/SSL option only: no streaming, <40 s inputs. MMS is CC-BY-NC | 4 |
| **Qwen / Mistral Voxtral** | Audio-LLM ASR, dynamic-window streaming | Qwen AuT ~40M h pseudo-labelled; Voxtral ~4.4B params | No: no Telugu, GPU-sized | Not feasible |
| **Kyutai DSM** | Delayed-streams decoder-only LM over Mimi tokens | 2.6B model: pretraining 1.6M steps on 48 H100, fine-tune 16 H100 ([DSM](https://arxiv.org/html/2509.08753v2)) | No: en/fr only, needs time-aligned data, GPU/CUDA | Not feasible |
| **OpenAI Whisper / IndicWhisper** | Seq2seq; IndicWhisper fine-tuned on 10.7k h | Telugu 28.8 mean WER [M] ([Vistaar](https://arxiv.org/html/2305.15386)) | No: not natively streaming; zero-shot Telugu WER 101 [M, third party] ([BuzzASR](https://arxiv.org/html/2609.09554)) | Not feasible |
| **Moonshine v2** | Sliding-window streaming encoder, 34-245M | 8 H100, ~300k h; Apple M3 latency 50-258 ms [M] | Architecture inspiration only: English-only | Not feasible |
| **Sarvam / Gnani / Krutrim** | Proprietary multi-stage pipelines | >1M h claimed [V] | No weights or ablations; API-only | Not feasible |

### 1.3 Disqualified options and reasons

| Option | Reason for disqualification |
|---|---|
| MMS-1B-all | CC-BY-NC 4.0, ~1B, not streaming ([card](https://huggingface.co/facebook/mms-1b-all)) |
| Whisper (any size) as base | Not natively streaming; retrofits (SimulStreaming, LocalAgreement) have no Indic streaming benchmark; Telugu script collapse (script-fidelity 0.46-0.71) and WER >100 [M, third party] ([arXiv 2605.03073](https://arxiv.org/abs/2605.03073)) |
| WhisperRT / CarelessWhisper | CC BY-NC 4.0 ([arXiv 2508.12301](https://arxiv.org/abs/2508.12301)) |
| Voxtral Mini 4B Realtime | ~4.4B parameters, vLLM/GPU, no Telugu, 13 languages ([card](https://huggingface.co/mistralai/Voxtral-Mini-4B-Realtime-2602)) |
| Qwen3-ASR | No Telugu; GPU serving; streaming Hindi unreported |
| Kyutai stt-1b-en_fr / stt-2.6b-en | English/French only; CUDA examples; no new-language training code |
| Parakeet-TDT-0.6B-v3 / Canary-1B-v2 | 25 European languages; Hindi and Telugu not supported ([card](https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3)) |
| Parakeet 1.1B Indic | 1.1B; bn/en/hi/ta only, no Telugu; community licence ([NGC](https://catalog.ngc.nvidia.com/orgs/nvidia/-/collections/parakeet-1-1b-rnnt-multilingual/-)) |
| Indic-Transcribe Core/Flex (Bodhan) | 1.2B, offline (<=30 s windows), "Indic Open Model License v1.0" unread, base-model terms also apply; the real-time "lite" variant could not be verified ([Flex card](https://huggingface.co/bodhan-ai/indic-transcribe-flex)). Its Telugu numbers (11.4/13.1 WER on its own Voice of India benchmark [V-ish, self-reported]) show what is possible but not what is deployable |
| nemotron-speech-streaming-en, parakeet-unified-en | English only; unified model runs buffered streaming in sherpa-onnx, not cache-aware |
| Moonshine | English-only MIT models; non-English legacy models non-commercial |
| Granite Speech, SenseVoice, FireRed, Gemma audio | No Hindi/Telugu evidence |
| Sarvam Saaras/Saarika, Gnani Vachana, Gemini, Deepgram | API-only, no open weights; also unsuitable as pseudo-label teachers (ToS risk) |

---

## 2. Data: Telugu is the binding constraint, and licence labels cannot be trusted

### 2.1 Licence tiers

Tiers are engineering risk tiers from the data notes, not legal advice. T1 = permissive licence on consent-collected audio. T2 = open licence with a caveat (ShareAlike, scraped upstream audio or text, or conflicting labels). T3 = terms unresolved. T4 = unusable commercially.

| Tier | Dataset (licence per source) | Hindi h | Telugu h | English-IN h | Key warnings |
|---|---|---|---|---|---|
| **T1** | **IndicVoices** (CC BY 4.0, gated) ([HF](https://huggingface.co/datasets/ai4bharat/IndicVoices)) | ~790 [E] | ~480 [E] | 0 | Hours are our arithmetic from example counts (+/-15%); paper says 7.3k h, card 23.7k h total / 11.2k transcribed; gate-condition text is login-only |
| T1 | **Vaani** (CC BY 4.0, gated) ([HF](https://huggingface.co/datasets/ARTPARK-IISc/Vaani)) | 1,004 transcribed (14,924 total) | 184 transcribed (2,326 total) | 22 transcribed (337 total) | Paper's fine-tuning subset is lower (594 h Hindi / 113 h Telugu); phone-recorded, image-prompted speech; some third-party subsets labelled NC |
| T1 | **SPRING-INX** (AIKosh: CC BY 4.0; paper: "public domain") ([paper](https://ar5iv.labs.arxiv.org/html/2310.14654)) | 351 | 0 (not released) | 0 | Wording conflict to resolve; ~10% of conversational data code-mixed |
| T1 | IndicVoices-R (HF: CC BY 4.0; AIKosh: CC BY-ND 4.0) | ~75 | ~136 | 0 | Overlaps IndicVoices (do not double count); ND conflict makes it T2 until resolved |
| T1 | Common Voice v27 (CC0), FLEURS (CC BY 4.0), LibriSpeech (CC BY 4.0) | CV 15.7 validated + FLEURS ~7 | CV 0.94 validated (75 speakers) + FLEURS ~8 | CV en-IN clips ~224 h [E, partly unvalidated] | CV Hindi 485 speakers, Telugu 75: too few for acoustic diversity ([CV stats](https://raw.githubusercontent.com/common-voice/cv-dataset/main/datasets/scripted-speech/cv-corpus-27.0-2026-09-11.json)) |
| **T2** | **Kathbath** (tag CC BY 4.0; text says CC0 packaging; AIKosh says CC BY-SA 4.0) ([HF](https://huggingface.co/datasets/ai4bharat/Kathbath)) | 150 (+48 noisy) | 155 (+75 noisy) | - | Prompts come from crawled IndicCorp text AI4Bharat does not own; audio itself is fresh crowd recordings |
| T2 | **Shrutilipi** (CC BY 4.0 packaging) ([HF](https://huggingface.co/datasets/ai4bharat/Shrutilipi)) | 1,620 | 390 | - | All India Radio broadcasts: packager's licence cannot grant the broadcaster's rights; keep out of base mix |
| T2 | NPTEL (CC BY 4.0 on HF) | 157 | 183 | - | Lecture audio provenance unverified |
| T2 | MUCS Hi-En / SLR104 (CC BY-SA 4.0) ([SLR104](https://www.openslr.org/104/)) | 90 (train) | - | - | ShareAlike on a model is untested; English appears in mixed scripts |
| T2 | YODAS, People's Speech, VoxPopuli, Granary labels | 481 (YODAS manual) | 5.7 (YODAS) | People's Speech, VoxPopuli | YouTube/archive.org/EP provenance; YODAS manual captions "not necessarily human-transcribed" |
| **T3** | MUCS sub-task 1 / SLR103 (Microsoft licence ID unresolved), IndicTTS, SYSPIN, SLR66 Telugu (BY-SA) | - | - | - | Do not use until resolved in writing |
| **T4** | **Microsoft/SpeechOcean Telugu corpus (also MUCS Telugu 40 h)**: "shall not be used for commercial purposes"; Gram Vaani SLR118 (academic only); GigaSpeech (tag apache-2.0 but non-commercial terms); Emilia (tag cc-by vs NC text); Skit-S2I, CS-FLEURS (CC-BY-NC); Samanantar (NC) | - | - | - | **Unusable.** HF re-uploads can silently relicense (e.g., a MUCS Hinglish re-upload tagged cc-by-4.0 while SLR104 is BY-SA) |

**Committed T1 supply [E, from the data notes].** Hindi about 2,150 h (range 1.9-2.3k), Telugu about 670 h (range 0.55-0.75k), Indian-accent English about 0.1-0.25k h, dedicated Hindi-English code-switch about 0 h, Telugu-English code-switch 0 h. Adding all T2 sources gives Hindi 4.0-4.5k h and Telugu about 1.4k h. Telugu is therefore the binding constraint: at 0.7k clean hours Telugu is below what IndicWhisper used (806 h) and well below SraVaani's 2,036 h, which still yielded 25.1 mean WER offline [M].

**Licence-conflict warnings to carry into the approval document.** Kathbath carries three different licences across metadata, body text and AIKosh. Lahaja is CC BY 4.0 in text but MIT in its tag (eval only anyway). IndicVoices-R is BY on HF but BY-ND on AIKosh. SPRING-INX is BY on AIKosh but "public domain" in its paper. Several gated cards (IndicVoices, Vaani, Kathbath, IndicConformer, SraVaani) show conditions only after login, so the gate text must be captured with date at download time. A CC BY wrapper cannot license rights the packager does not hold, which is why Shrutilipi (AIR) and crawled-text prompts stay T2 regardless of label ([CC guidance](https://creativecommons.org/using-cc-licensed-works-for-ai-training-2/)). Creative Commons does not settle whether weights are "adaptations" or must carry attribution, and no source examined Indian TDM law; the DPIIT mandatory-licence proposal (Dec 2025) was open for consultation until Feb 2026 with no final outcome found. DPDP implications for voice data were not researched.

### 2.2 Recommended data mix (proposals, not experimentally validated)

**MVP, T1 only, about 1,280 h [P]:**

| Language | Hours | Sources |
|---|---|---|
| Hindi | 550 | IndicVoices 250, Vaani (QC-filtered) 200, SPRING-INX 80, CV + FLEURS 20 |
| Telugu | 400 | IndicVoices 280, Vaani 110, CV + FLEURS 10 |
| English (Indian-accent weighted) | 280 | CV en-IN subset 180, LibriSpeech 50, Vaani-En 22, VoxPopuli 28 |
| Code-switch | 50 | Synthetic splices of Hi/Te + En utterances plus mined code-mixed T1 segments (LID/script filter) |

**Production, about 4,200 h (about 3.0k labelled plus 1.2k pseudo-labelled) [P]:** Hindi about 1,500 h (including ~350 h Vaani pseudo-labels and optionally Kathbath ~100 h, T2), Telugu about 1,000 h (including ~250 h Vaani pseudo-labels and optional Kathbath ~110 h), English about 1,200 h, code-switch about 300 h (synthetic/mined ~200 h plus SLR104 ~90 h, T2). Keep T2 at or below 20% per language and train a T1-only ablation so the product can be rebuilt without T2 if challenged. Shrutilipi and NPTEL stay out unless Telugu WER stalls and the risk is accepted in writing.

**Compute implication (our inference).** At the estimated 600M throughput of about 30 audio-hours per GPU-hour [E], 150 GPU-hours buys about 4,500 audio-hour-epochs. The MVP mix at about 3.5 epochs (about 4,500 audio-hours) fits; the 4,200 h production mix fits only as roughly one pass on the 600M model, or multiple epochs on the 114M arm (about 150 audio-hours per GPU-hour [E]). If measured A10G throughput is half the estimate, data volume must shrink or the bake-off tilts toward Arm B.

**Unlabelled audio for pseudo-labelling.** Vaani's untranscribed audio is the best commercial-safe source: about 13.9k h Hindi, 2.1k h Telugu, 0.3k h English (derived from the HF per-language table [E]) ([HF](https://huggingface.co/datasets/ARTPARK-IISc/Vaani)). It is image-description speech recorded on phones, so gains concentrate on acoustic diversity and Telugu volume, not conversational or laptop-microphone domains. Teacher choice is IndicConformer-600M and SraVaani-1.0 (Telugu 26.4 and 25.1 mean WER [M]), not Whisper-large-v3. Omnilingual-7B is risky: its own CSV gives Telugu CER 6.5, but third parties measure OIWER 50.7 on conversational Telugu (Section 8). The teachers' output terms are unverified.

### 2.3 Code-switching: no corpus, so build it

No open, commercial-safe Telugu-English speech corpus exists. CoSTA cut about 2 h of Telugu code-switched speech from IndicVoices for evaluation (derived-set licence unstated) ([CoSTA](https://arxiv.org/pdf/2406.10993)); a 200 h Telugu-English corpus is mentioned on a forum as access-by-request only ([forum](https://community.deeplearning.ai/t/request-for-telugu-english-code-switched-speech-corpus-asr-project/890896)); CS-FLEURS is NC; Common Voice's code-switching dataset is "Alpha" with no releases. Hindi-English has only SLR104 (BY-SA, ~90 h, lecture style). The plan is a three-part synthetic and mined recipe:

1. **Splicing** monolingual Hindi/Telugu and English T1 utterances, NVIDIA's method for building code-switch data from monolingual sources ([arXiv 2306.08753](https://arxiv.org/abs/2306.08753)).
2. **TTS plus LLM text**: one preprint reports ~22,000 entity-dense Indic-English utterances for under $50, raising Telugu entity-hit-rate from 0.027 to 0.473 on a synthetic holdout, but regressing read-speech FLEURS-Te WER by up to +6.6 points and missing every pre-registered target ([arXiv 2605.03073](https://arxiv.org/abs/2605.03073)) [M, single preprint]. Mix synthetic with real data and never use it for headline accuracy. TTS and LLM licences are unchecked.
3. **Mining** naturally code-mixed segments from IndicVoices, Vaani and SPRING-INX using script-mix and LID filters. Real code-mixed volume in T1 sets is unmeasured.

**Script policy (decide before training).** Training transcripts across corpora use no common convention for English words in Hindi/Telugu speech: MUCS training data mixes Latin and Devanagari, while its blind test uses Latin. We propose Latin for English words, native script for Indic words, ASCII digits, enforced by a transliteration-lexicon pass [P]. The SraVaani card warns that Latin-script code-switching can inflate WER against single-script references. This choice also determines the optional Romanization layer (Section 6).

**Punctuation constraint.** NVIDIA's fine-tune recipe expects punctuated and cased transcripts and a `target_lang` tag per clip ([blog](https://huggingface.co/blog/nvidia/fine-tuning-nemotron-35-asr)), while IndicConformer-style vocabularies mostly lack punctuation. Unpunctuated Indic targets would likely teach the model to drop punctuation for Hindi and Telugu (our inference). Options: punctuation restoration of training text with an LLM (Granary used Qwen2.5-7B, rejecting changes above 5% CER) or shipping unpunctuated Indic output with a downstream P&C model. This is a decision for the seniors (Section 9).

---

## 3. The pipeline: Stages 0-8 with gates

GPU estimates assume an A10G at $1.006/h on-demand (g5.xlarge, us-east-1, third-party July 2026 snapshot) or about $0.43-0.52/h spot, with spot interruption rates above 20% in one snapshot ([DoiT](https://compute.doit.com/spot/us-east-1/g5.xlarge), [Holori](https://calculator.holori.com/aws/ec2/g5.xlarge/us-east-1)). **No A10G NeMo FastConformer throughput benchmark exists in any source.** All GPU-hours below are [E], derived from first principles: about 150 audio-hours per GPU-hour for a ~120M model and about 30 for a 600M model, each possibly off by 2x. Stage 1 replaces these with measurements.

### Stage 0: Governance and foundations (weeks 0-2, parallel, CPU only)

- **Goal:** make the project legally and methodologically auditable before spending GPU.
- **Steps:** (1) per-source licence manifest (dataset, version/hash, download date, licence-text snapshot, gate terms, attribution string, tier, hours); (2) request access to IndicVoices, Vaani, Kathbath, IndicConformer, SraVaani-0.5-live and -1.0 and capture gate text; (3) send written licence questions to NVIDIA, AI4Bharat and ARTPARK (Section 9); (4) write the versioned normalizer spec and script policy; (5) pin NeMo, sherpa-onnx and ORT versions; (6) start recruiting speakers for the in-house test set.
- **Inputs/outputs:** none to licence manifest, normalizer spec, version-pin file, legal question list.
- **Cost:** about $0 GPU; storage of IndicVoices archives (745 GB) and Vaani is a non-GPU cost not sourced.
- **Exit gate:** no unresolved legal blocker on the Nemotron licence; manifest exists; access requests filed.

### Stage 1: De-risking spike (weeks 1-2)

- **Goal:** answer the five questions that decide whether Path A is viable, using an unmodified checkpoint plus one tracer bullet.
- **Steps:**
  1. Export unmodified Nemotron-3.5 with the sherpa-onnx `scripts/nemo/nemotron-3.5-asr-streaming-0.6b` recipe (fp32 plus int8 encoder/decoder/joiner, `tokens.txt`, metadata) at 320 and 560 ms, pinned to sherpa-onnx >=1.13.5 (greedy-decoding fix for NeMo streaming transducers landed in 1.13.5) ([changelog](https://pub.dev/packages/sherpa_onnx_linux/changelog)). Check parity against NeMo's `conformer_stream_step` simulation on a fixed clip (logit tolerance <1e-3 fp32 [P]).
  2. Measure RTF, peak RSS, first-token and finalization latency on the actual target laptops: at least one low-power x86 U-series, one mid x86, one base Apple M-series, one recent M-series; 1/2/4 threads; paced and unpaced; follow the Softcery harness hygiene (load-average gate, thread sweep) ([Softcery](https://softcery.com/lab/hosting-nemotron-asr-streaming-on-a-cpu.md)).
  3. Tokenizer and Telugu handling: tokenize Telugu text with Nemotron's SentencePiece model and measure unk rate, tokens per word and character coverage; inspect vocab size and byte fallback; run zero-shot Telugu to see what it emits.
  4. Prompt mechanism: read `prompt_dictionary` and `auto_prompt_id` in the export metadata; test whether a new locale (te, plus code-switch locales) can be added and whether sherpa-onnx accepts a modified dictionary. The 128-dim one-hot against 40 locales suggests free slots (our inference, unverified).
  5. A10G tracer bullet: run NeMo OOMptimizer for max `batch_duration`, measure full-FT throughput and memory for the 600M model (bf16, activation checkpointing, optionally 8-bit Adam), then fine-tune on 10-20 h of Telugu, export through sherpa-onnx and decode. This proves the loop train, export and decode works with a changed vocabulary or prompt table, which no source documents.
  6. Baselines on a 1-2 h dev slice: IndicConformer-600M, SraVaani-0.5-live (if access), unmodified Nemotron for Hindi and English.
- **Inputs/outputs:** unmodified checkpoints and 10-20 h Telugu to measured RTF table, tokenizer report, A10G throughput number, tracer-bullet pass/fail.
- **GPU/cost [E]:** about 12 GPU-hours, about $12 on-demand (about $6 spot).
- **Exit gate (all proposals [P]):** (a) fp32 ONNX matches NeMo streaming simulation; (b) int8 unpaced single-thread RTF <=0.5 at 560 ms and peak RSS <=1.5 GB on the lowest-spec target laptop; (c) a documented way to represent Telugu (extend tokenizer or replace decoder/joint) with a tracer-bullet pass; (d) measured A10G throughput at or above about 15 audio-hours per GPU-hour for the 600M model. **If (b) or (d) fails, Path B becomes primary.** If (c) fails for Nemotron, Path B or C becomes primary. If a licence blocker appears, stop and escalate.

### Stage 2: Evaluation harness, baselines and in-house test set (weeks 2-4)

- **Goal:** freeze the yardstick before building the model, so no threshold is tuned to the result.
- **Steps:** implement the Section 4 protocol (normalizer, strict WER, CER, OIWER/multi-reference, code-switch-token metrics, streaming and edge metrics); record and annotate the in-house set; re-run all baselines on identical audio; contamination checks (audio fingerprint plus transcript n-gram de-dup against every public test set).
- **Inputs/outputs:** baselines and recordings to private versioned test set, harness repo, baseline table.
- **GPU/cost [E]:** about 8 GPU-hours (baseline decoding), about $8. Recording and annotation cost is not sourced and is a budget decision.
- **Exit gate:** a second engineer reproduces one baseline number within 0.2 absolute WER ([P], from the evaluation notes); proposed MVP/production thresholds are re-confirmed against measured baselines in week 1 of this stage.

### Stage 3: Data build (weeks 3-5)

- **Goal:** produce the training manifest, tokenizer and pseudo-labelled and synthetic sets.
- **Steps:** download T1 sets; apply the script policy and lexicon pass; decide the tokenizer (Section 3.1); run teacher pseudo-labelling on Vaani untranscribed audio with filters (inter-teacher CER below about 10-15%, script-ratio versus audio-LID check, repeated-n-gram and chars-per-second filters, CTC forced-alignment score; thresholds are [E] and must be calibrated on a labelled holdout); synthesize code-switch data (splice, TTS plus LLM text) and mine real code-mixed segments; build the English replay set.
- **GPU/cost [E]:** about 40 GPU-hours (pseudo-label decoding of 1.5-2.5k h with a 600M teacher is "tens of GPU-hours" per the notes), about $40, plus about $50 for TTS synthesis (one preprint's figure for 22k utterances, [M, single preprint]). An A100 at about $1.39/h (community) may be cheaper per audio-hour for batch decoding, unverified; run a 10-minute benchmark.
- **Exit gate:** manifest with per-source tier and hours; T1-only and T1+T2 variants buildable; pseudo-label filter retention and agreement reported (Granary-style pipelines retain 47.9-74.6% [M]); zero overlap with test sets.

### Stage 4: Bake-off (weeks 5-7)

- **Goal:** choose the base by measurement, not by card claims.
- **Arms (equal data and cost cap [P]):** Arm A = Nemotron-3.5 (A1: keep tokenizer and extend for Telugu; A2: replace decoder/joint with a new aggregate tokenizer). Arm B = 114M cache-aware hybrid with aggregate tokenizer. Arm C = SraVaani-0.5-live continuation (only if fine-tuning weights are granted). Arm D (Zipformer) enters only if A fails the CPU gate.
- **Protocol:** identical supervised subset (about 300 h Telugu, 200 h Hindi, 100 h English-IN [P]), identical normalizer, identical recipe, at most about 30 GPU-hours per arm, multi-lookahead training over {0,1,3,6,13}. Report Telugu, Hindi and Indian-English WER and CER at 160/320/560 ms, RTF on the target laptops, code-switch slice, memory, and learning curve (WER at 25/50/100% of the subset).
- **Decision rule [P]:** choose Arm A if it passes the CPU gate and beats Arm B by at least 10% relative on Telugu at 560 ms. Choose Arm B if Arm A fails the CPU gate or the gain is below 10% and Arm B is at least 3x faster on CPU. Arm C wins only with written licence terms and an export path. The learning curve is the extrapolation tool: if the curves are still falling steeply at the subset limit, weight the arm with more headroom.
- **GPU/cost [E]:** three arms at about 30 GPU-hours each = about 90 GPU-hours, about $90 (about $45 spot).
- **Exit gate:** winner selected, decision memo with numbers; if no arm reaches within 1.5x of the SraVaani-live Telugu baseline at 560 ms on the equal-budget subset, escalate and reconsider scope.

### Stage 5: Main post-training of the winner (weeks 7-11)

- **Goal:** train the production candidate.
- **Steps (Path A shown):**
  - 5a Head warm-up (if the vocabulary or prompt table changed): freeze the encoder, train decoder/joint/prompt for 2-5k steps [E] at higher head LR.
  - 5b Full fine-tune: encoder LR 1e-4 to 5e-5, cosine, layer-wise decay optional (NeMo guidance 1e-4 to 1e-5; override Noam warmup) ([NeMo docs](https://docs.nvidia.com/nemo/speech/latest/asr/fine_tuning.html)); SpecAugment; speed perturbation 0.9/1.0/1.1; language sampling p_i proportional to n_i^0.5-0.7 with at least 20-30% English and code-switch [E]; multi-lookahead `att_context_size` over [56,{0,1,3,6,13}] (Nemotron-3.5 left context 56; fix and document the left context used at export because it sets cache shapes); FP16 RNNT loss and fused batch splitting for memory ([NVIDIA](https://research.nvidia.com/labs/conv-ai/blogs/2023/2023-10-28-numba-fp16)). Note: the Nemotron-3.5 card describes an RNNT model; whether a CTC head exists was not verified, so use IndicConformer's CTC for forced alignment if none.
  - 5c Pseudo-label round at lower LR, ablating filtered versus unfiltered labels.
  - 5d Code-switch data ablation with and without synthetic data, keeping real code-mixed data in dev.
  - 5e Average the last 5-10 checkpoints; optional WiSE-style interpolation with the original encoder; English regression must be no worse than 10% relative [P].
  - **Ablations in priority order:** tokenizer strategy, multi-lookahead versus single (3-8% relative gain in the NVIDIA paper [M]), filtered versus unfiltered pseudo-labels, with versus without code-switch synthesis, average/WiSE alpha, PTQ versus QAT.
- **GPU/cost [E]:** about 150 GPU-hours, about $150 (about $75 spot). Checkpoint every 15-30 minutes with S3/EBS resume if using spot.
- **Exit gate:** meets the MVP slices in Section 4.4 on the private set at 560 ms fp32; no more than 10% relative English regression; no insertion-rate violation.

### Stage 6: Compression and export (weeks 10-13)

- **Goal:** a verified int8 sherpa-onnx bundle per chunk size.
- **Steps:** export at the target chunk sizes with the same recipe as Stage 1; PTQ int8; weight-only int8 on encoder MatMuls is the best-documented path (8.03 fp32 to 8.01 WER for ORT int8 k-quant; 8.12 for int4-mixed; 10.14 when ConvInteger/MatMulInteger paths were used [M, English, 8-dataset average on a Microsoft ORT port]) ([arXiv 2604.14493](https://arxiv.org/html/2604.14493)). Keep subsampling convs, decoder LSTM, joiner and cache tensors in fp32. Validate on Indic dev sets because no public int8-versus-fp32 Hindi/Telugu measurement exists. QAT only if degradation exceeds 3-5% relative. Regress the exporter itself: the ORT port lost 0.75 absolute WER versus PyTorch (7.28 to 8.03) at fp32.
- **GPU/cost [E]:** about 10 GPU-hours, about $10.
- **Exit gate:** parity test passes in CI; int8 within the proposed 3-5% relative of fp32 on every slice, else QAT or fall back to fp32/int4-mixed per runtime.

### Stage 7: Evaluation gate and hardening (weeks 12-15)

- **Goal:** apply the MVP gate; collect the production-gap list.
- **Steps:** full regression suite (private set, public sanity sets, synthetic entity set, adversarial silence/music clips, long streams over 60 s, edge harness); paired bootstrap against baselines; reserve about 30 GPU-hours for ablations and fixes.
- **Cost [E]:** about 30 GPU-hours, about $30.
- **Exit gate:** MVP gate (Section 4.4). Decision: ship MVP to design partners, or iterate.

### Stage 8: Application layer, packaging and optional Romanization (weeks 12-16)

- **Goal:** a product-grade bundle.
- **Steps:** Silero VAD with at least 0.5 s pre-roll and a trailing-silence flush chunk; endpointing; punctuation and ITN decision (NeMo-text-processing has Hindi ITN; no Telugu ITN found); hotwords via modified beam search; signed, versioned model bundle (manifest with SHA-256, pinned runtime versions, tokenizer hash, chunk size, quantization recipe); optional Romanization module (Section 6); sidecar process isolation.
- **Exit gate:** CI green on latency/WER/parity; legal sign-off on bundle contents; attribution/notices file generated.

**Post-MVP (production) track:** T2 data under written risk acceptance, QAT, distillation to a Zipformer/114M model if CPU headroom is insufficient on the lowest-spec laptops, additional in-house data collection.

### 3.1 Tokenizer: an open design question with conflicting advice in the notes

The post-training notes recommend small aggregate tokenizers (per-script SentencePiece unigram, 256-512 pieces each, total about 1-1.5k) for per-token language ID, small RNNT joint memory and fast CPU decode. NVIDIA's Concatenated Tokenizer paper and the NeMo aggregate tokenizer support this ([NeMo/NVIDIA blog](https://developer.nvidia.com/blog/multilingual-and-code-switched-automatic-speech-recognition-with-nvidia-nemo/)). The lab-methodology notes instead point to a shared BPE of 5-8k units (SraVaani 5,000 shared across scripts; Canary-v2 found a unified tokenizer beat concatenated ones, with 8,192 about equal to 16,384 and both better than 4,096) ([Canary-v2](https://arxiv.org/html/2509.14128v2)). These are not reconciled; the bake-off should include one arm per option. Also open: whether to keep Nemotron's tokenizer and rows and extend them for Telugu (preserves the pretrained Hindi decoder knowledge but needs custom embedding and joint-extension code not documented as a NeMo built-in) or to replace decoder and joint (cheap, loses Hindi decoder knowledge). One further caution on Telugu: morphological splitting of targets cut Whisper-medium Telugu WER from 23.31 to 18.73 [M], but changes the output form and must be reversible and applied identically at evaluation.

---

## 4. Evaluation: pre-registered, private, multi-metric

### 4.1 Normalization

Never use Whisper's normalizer for Hindi or Telugu: it strips mark-class characters (matras and virama) and artificially lowers WER (METEOR similarity original versus normalized: English 0.97, Hindi 0.38) ([Manohar et al.](https://arxiv.org/html/2409.02449v4)). Proposed pipeline [P]: NFC (not NFKC without testing), remove ZWJ/ZWNJ on both sides, strip punctuation but keep combining marks, lowercase Latin, collapse whitespace, remove annotator tags and disfluency markers, map digits to one form (ASCII) via a fixed table, optional nukta folding and chandrabindu/anusvara canonicalization applied identically to reference and hypothesis, and report results with and without the optional folds. **No source covers Telugu ZWNJ/conjunct normalization or digit handling in published benchmarks;** test empirically and freeze. Publish a versioned, hashed normalizer spec and re-run every baseline through the same code; never mix numbers normalized differently.

### 4.2 Metrics and baselines

Report four numbers per slice: strict WER (minimal normalization), lattice/multi-reference WER (OIWER via the open-source `voi-oiwer` for Hindi; two to three references on a gold core for Telugu), CER (headline next to WER for Telugu: observed WER/CER ratios are 3.5-3.7x), and code-switch-token versus native-token WER with transliteration-invariant scoring (T-WER or SN-WER style). Multi-reference scoring materially changes results: mean WER fell from 24.80 (1 reference) to 17.76 (3 references) across ten systems on Vaani-Benchmark-V1.0 [M] ([paper](https://arxiv.org/html/2606.21408)), and flattening lattices can swap system rankings ([HF blog](https://huggingface.co/blog/open-asr-leaderboard-global-south)). Add script-fidelity rate (Whisper-large-v3 Telugu 0.46-0.71 [M]) and insertion rate on silence and noise clips as hallucination signatures.

**Baselines the team re-runs on identical audio (not copied from papers):** IndicConformer-600M (offline reference, CTC and RNNT); SraVaani-0.5-live at 80/480/1040 ms and SraVaani-1.0 if access; Nemotron-3.5 zero-shot for Hindi and English at 320/560 ms; unmodified 114M hybrid; the community Hindi/Hinglish and Indian-English Zipformers; Whisper-large-v3 only to document its Telugu failure. Published numbers are not comparable across vendors: Nemotron Hindi 6.8 on FLEURS versus 20.2 on Vaani; IndicConformer 8.2 on telephony OIWER versus 13.8 on mixed-set mean versus 20.0 on single-reference Vaani [M].

### 4.3 In-house test set

Per language, 3-5 h [P] at 60-100 speakers or more, split about 40% spontaneous/conversational on own phones, 20% telephony 8 kHz (codec-processed), 15% read named-entity and number prompts, 15% code-switch stratified by density (<10%, 10-30%, >30% foreign tokens), 10% noisy or far-field. Precedent sizes are 1.3-12.5 h (Monsoon hi-IN public 1.33 h, Svarah 9.6 h, Lahaja 12.5 h, Vaani V1.0 10.9 h). Annotation: ASR-seeded then native-linguist corrected (the Monsoon process), double annotation of the 1-1.5 h gold core and 20% of the rest, inter-annotator WER targets <=5% read and <=10% spontaneous [P]. Use at least two Telugu dialect regions (Telangana, Andhra/Rayalaseema) and Hindi L1-Telugu/Tamil/Bengali speakers. The set is private, hashed, never trained on, with a second held-back split so the dev split can be retired. Use speaker-level bootstrap CIs, which are roughly 2-3x wider than naive word-level CIs [E]. Synthetic TTS audio is for entity, number and lexicon stress tests only and is reported separately.

**Public sanity sets (never headline):** Kathbath test, FLEURS hi/te, IndicVoices test/valid, Vaani-Benchmark-V1.0 (Hindi, 3 references), Svarah, Monsoon en-IN and hi-IN public splits, Lahaja, MUCS Hi-En. Contamination is documented in the baselines (IndicWhisper trained on Vistaar training splits; Nemotron-3.5's training includes FLEURS and Common Voice; SraVaani uses VAANI and RESPIN for both fine-tuning and evaluation), so the in-house set is the trust anchor.

### 4.4 Proposed gates (all [P]; confirm against re-run baselines in Stage 2)

Scored on the private set, streaming at 640 ms or less, int8, on a stated laptop CPU:

| Slice | MVP gate | Production gate | Anchor evidence |
|---|---|---|---|
| Hindi clean/read | <=18 WER | <=12 | IndicConformer 13.8 mean offline; Nemotron 6.8-8.1 (in-domain); SraVaani-live 18-22 |
| Hindi spontaneous | <=28 strict (<=20 multi-ref) | <=20 (<=14) | IndicConformer 20.0/13.1 on Vaani V1.0; Nemotron 20.2; Zipformer 25.7 |
| Telugu clean/read | <=32 WER (<=10 CER) | <=24 (<=7 CER) | IndicWhisper 25.0-25.4; IndicConformer 26.4; SraVaani-live 30-35 |
| Telugu spontaneous/telephony | <=40 strict | <=28 | IndicConformer 23.7 OIWER on Voice of India; best agricultural 33.2 |
| English-IN (Svarah/Monsoon) | <=15 | <=9 | Whisper large 7.2 Svarah; small streaming 20.7-28 |
| Code-switch | within +8 abs of same model's monolingual spontaneous WER | within +4 abs; CS-token WER <=1.6x native | Vaani V1.0: CS-token penalty +2.6 to +15.6 abs; no Telugu-English baseline exists |
| Relative | <=1.3x IndicConformer-600M offline; <=1.15x best open streaming baseline | <=1.15x offline | Expected streaming penalty +15-25% relative [E] |
| Robustness | 8 kHz <=1.6x clean; 10 dB SNR <=1.5x | <=1.3x; <=1.25x | GSM codec and competing speech are the worst degradations [M] ([study](https://arxiv.org/html/2606.09335)) |
| Hallucination | insertion <=3%; no output >1.2x reference length on silence; script fidelity >=0.98 | insertion <=1.5%; SFR >=0.995 | Whisper Indic failure modes |
| Edge | RTF <=0.5 (unpaced, 1 thread); RSS <=1.5 GB; first-token P90 <=800 ms | RTF <=0.3; RSS <=1 GB; first-token P90 <=500 ms; finalization P90 <=300 ms | No published Indic laptop numbers |

**Go/no-go rule [P]:** MVP requires all Hindi and English slices plus the hallucination and edge gates, with Telugu within +10% of its gate. Production adds Telugu, code-switch and telephony. A regression of more than 5% relative on any slice between releases, or any overlap between training manifest and test sets, is a no-go.

**Expectation check.** Gates are proposals anchored on small streaming models (Hindi about 18-25, Telugu about 30-40 on mixed public sets). The best offline open models sit at Hindi 13-14 and Telugu 25-26 [M]; commercial APIs score Telugu OIWER 18.2 (Sarvam Audio) on the Voice of India benchmark [M, run by an interested party]. Telugu production gates are therefore the least likely to be met with 0.7k T1 hours.

### 4.5 Streaming latency and edge metrics

Report per model and per chunk size [P, built from the cited methodology]: WER/CER at 160/320/640/1280 ms and offline (the WER-versus-latency curve); first-token emission delay (speech onset to first non-blank token, P50/P90, against forced-alignment boundaries, because chunk-model token timestamps equal chunk end) ([paper](https://ar5iv.labs.arxiv.org/html/2104.02207)); finalization latency (end of speech to final transcript, P50/P90); endpoint delay paired with false-cutoff and miss rates; partial-hypothesis revision rate (no source defines it, so define and publish it); RTF paced and unpaced at 1/2/4 threads on a named CPU, OS and power mode; peak and steady-state RSS; model size on disk fp32/int8; cold-start load time; CPU utilization. SimulEval-style average lag is a translation metric; per-word emission delay against aligned word end is the ASR analogue. Disable built-in endpointing and use greedy decoding when isolating model latency.

---

## 5. Deployment: sherpa-onnx int8, with specific pitfalls

### 5.1 Stack

| Layer | Choice | Notes and caveats |
|---|---|---|
| Runtime | **sherpa-onnx >=1.13.5**, ORT CPU EP, 4-6 threads, `session.intra_op.spin_duration_us=200` | Apache-2.0; first-class NeMo cache-aware transducer support since 1.12.22/1.13.3; greedy-search fix for NeMo streaming only in 1.13.5. Older versions decoded Nemotron badly without error ([OpenWhispr](https://openwhispr.com/blog/local-streaming-speech-to-text)), so pin runtime and exporter together ([README](https://github.com/k2-fsa/sherpa-onnx)) |
| Apple silicon | Baseline: same ONNX bundle on CPU. Optional: MLX 8-bit or CoreML INT8 | MLX 8-bit 733 MB disk / 992 MB peak; 5-bit 539/800 MB (avg FLEURS WER 11.53 versus 11.01 for 8-bit) [M, community]; CoreML INT8 612 MB / 1,238 MB (M5 Pro). **No RTF published for any Apple path** ([soniqo](https://soniqo.audio/guides/nemotron)). Community ports cover stock vocabulary; a modified vocabulary needs re-conversion (our inference) |
| Intel alternatives | OpenVINO IR (FluidInference), GGUF (cstr: F16 1.3 GB, Q4_K 458 MB), ORT-direct three-session runtime | Community artifacts; no laptop RTF ([OV](https://huggingface.co/FluidInference/Nemotron-3.5-ASR-Streaming-Multilingual-0.6b-ov), [GGUF](https://huggingface.co/cstr/nemotron-3.5-asr-streaming-GGUF)) |
| VAD | Silero VAD (MIT per LICENSE file) | A "CC BY-NC 4.0" README badge conflicts and was not reconciled; counsel to verify. TEN VAD is smaller and faster but licensed "Apache 2.0 with additional conditions"; needs legal review |
| P&C / ITN | Train P&C in if transcripts allow; NeMo-text-processing Hindi ITN; Telugu ITN not found | Cadence-Fast (270M, Hindi/Telugu, MIT per a mirror) has no ONNX export found |
| Hotwords | Transducer plus modified beam search only | Not available with CTC-only models (rules out Path C's SraVaani-live as-is); CPU cost unquantified |

### 5.2 Measured RTF and size numbers (and why they are not interchangeable)

| Setup | Result | Source and caveats |
|---|---|---|
| sherpa-onnx 1.13.8, ORT 1.28.2, int8 Nemotron-3.5 multilingual, **Ryzen 7500F 6C desktop (AVX512)**, 4 threads, greedy, 16.7 s clip | Processing per audio second: 1120/560/320/160/80 ms chunks = 61.3/96.7/145.4/274.6/645.6 ms (RTF about 0.06/0.10/0.15/0.27/0.65); test-clip WER 7.91/7.99/8.27/8.88/9.43; finalization 45-75 ms; RAM ~1.0-1.1 GB after load | [M, Softcery Sept 2026] ([source](https://softcery.com/lab/hosting-nemotron-asr-streaming-on-a-cpu.md)); desktop CPU, not a laptop; English 0.6B model at 1120 ms gave 63.0 ms |
| Same, Mac M2, 1120 ms | 0.176 core-seconds per audio second (2 threads), final p50 85 ms; 4 threads 0.364 core-seconds | [M]; wall RTF of up to about 0.09 if saturated is our inference, not measured |
| Microsoft ORT port of Nemotron-0.6B, AMD EPYC 7V12 (AVX2), 32 cores, batch 1, 0.56 s delay | RTFx 6.7-7.3 (RTF about 0.14-0.15); at 0.16 s delay RTFx 2.87 | [M] ([arXiv 2604.14493](https://arxiv.org/html/2604.14493)); different CPU, ISA, runtime and chunking; do not mix with Softcery numbers |
| Streaming Zipformer 66M (Indian English), 4-thread Xeon | int8 RTF 0.035; fp32 0.183; int8 ~68 MB | [M, community] ([card](https://huggingface.co/Akshatkasera007/STT-streaming-zipformer-indian-en)); English-fine-tuned, not Telugu |
| IndicConformer-120M Hindi Q8_0 GGUF | RTF 0.06 (~16x real time), 225 MB, ~140 MB RAM | [M, community, CPU unspecified, offline] ([card](https://huggingface.co/Singla0009/IndicConformer-GGUF)) |

**What is not known:** RTF on i5/i7 U-series laptops or any M1/M3 for a streaming FastConformer; official sherpa-onnx RTF tables; int8-versus-fp32 WER on Hindi or Telugu. Planning inference [E]: a 600M streaming FastConformer int8 should run at RTF about 0.06-0.15 at 560-1120 ms on a 6-8-core AVX2/AVX512 laptop (unproven on 15 W parts); 160-320 ms chunks are the Pareto point on desktop; a 120M model should be 4-5x cheaper per audio second. User-perceived latency is approximately half the lookahead window plus finalization (45-75 ms) plus VAD/endpoint delay.

### 5.3 Export pitfalls (checklist for Stages 1 and 6)

1. **Normalization must be "NA" at export** in both the preprocessor object and config, otherwise the graph expects per-utterance normalization ([HF discussion](https://huggingface.co/Muno459/fastconformer-quran-streaming/discussions/5)).
2. **Cache support is baked per chunk size.** Export through `forward_for_export` with `export_cache_support`; inputs include `cache_last_channel`, `cache_last_time`, `cache_last_channel_len` and outputs return the next caches. Left context differs between models ([70,x] in Nemotron-EN, [56,x] in 3.5), so fix and document it for the post-trained model. No official NeMo page documents cache-aware ONNX export; the evidence is a community recipe and sherpa's scripts.
3. **sherpa requires separate encoder, decoder and joiner sessions plus metadata** (`model_type`, `vocab_size`, `subsampling_factor`, `normalize_type`, `pred_rnn_layers`, `pred_hidden`, `feat_dim`); NeMo emits a combined decoder-joint that must be split, and checkpoints without metadata fail with "No model_type in the metadata!" ([mirror](https://huggingface.co/pantinor/ovos-conformer-mirrors)).
4. **Nemotron-3.5 specifics:** `tokens.txt` from SentencePiece, `prompt_dictionary` and `auto_prompt_id` in encoder metadata, one export per chunk size. Whether a modified prompt dictionary or vocabulary loads is undocumented, which is why Stage 1 includes the tracer bullet.
5. **Quantization:** the ConvInteger CPU kernel is uint8-only, so QInt8 exports fail to load ("Could not find an implementation for ConvInteger(10)"); re-quantize to QUInt8 ([source](https://huggingface.co/nmukthap/vertexvoice-indic)). Integer-activation convolution paths degraded WER 8.20 to 10.14 [M]. Use weight-only block quantization on encoder MatMuls and keep convs, decoder, joiner and caches fp32. ORT docs flag U8S8 saturation on non-VNNI x86 ([docs](https://onnxruntime.ai/docs/performance/model-optimizations/quantization.html)).
6. **Front end parity:** replicate NeMo's mel front end exactly (128 mel for Nemotron, 80 for IndicConformer; 0.97 pre-emphasis, Slaney mels); omit no featurizer asset (`mel_filters.json`, `hanning_window.json` are often missing from upstream exports).
7. **Streaming practicalities:** feed one chunk of trailing silence or the final words are lost; use at least 0.5 s pre-roll after VAD; cut streams only at utterance ends; partials must be replaced not appended; unknown session option keys are silently dropped.
8. **Reduced left context lowers accuracy** (WER 7.28 to 8.51 when left context dropped from 10 chunks to 2 [M]); keep memory budget in mind when tuning.
9. **CoreML paths** from IndicConformer use fixed 1024-frame encoder input (non-streaming); `.mlmodelc` must be compiled on the target Mac.
10. **CI:** regress PyTorch cache-aware simulation versus ONNX streaming output on a fixed clip; fail on WER regression above 0.3 absolute [P], RTF above budget, or numerical divergence beyond threshold.

---

## 6. Optional Romanization: a deterministic layer, never a training target

Romanization is a post-process on native-script output, not a modelling choice. Design [P, from the edge-runtime notes' proposal]: (1) tokenise ASR output by script and pass Latin tokens through unchanged (the token-ID range or script gives free language ID); (2) look up Devanagari/Telugu-script English loanwords in a lexicon mined from our own code-switched training transcripts and emit the English spelling; (3) otherwise apply scheme-based transliteration with a Hindi schwa-deletion pass (Choudhury-style rules by default; Telugu keeps inherent vowels, which is background linguistics not in the sources); (4) version all tables so output is reproducible. Two modes: "scholarly" (ISO 15919, round-trip reversible) and "natural" (Hunterian-like, schwa-deleted, loanwords restored; not reversible).

**Tool and licence guidance.** `indic_transliteration` is MIT but README mentions no ISO 15919/Hunterian and no schwa deletion ([GitHub](https://github.com/sanskrit-coders/indic_transliteration)). Aksharamukha appears GPL-3.0 and should not ship in a closed binary ([GitHub](https://github.com/virtualvinodh/aksharamukha-python)). IndicXlit (MIT code and models) is a learned model with stochastic beam output, so use it only as a comparison baseline, not in the deterministic path ([AI4Bharat](https://ai4bharat.iitm.ac.in/?p=1121)). The uroman licence is unresolved (Apache-2.0 on the Rust port versus an MIT-like original). Known weak points: schwa deletion is unsolved by plain mappings ([Arora et al. ACL 2020](https://aclanthology.org/2020.acl-main.696)); loanword spelling in Hindi is inconsistent (डॉलर versus डालर) with no standard back-transliteration reference; Telugu lacks a nukta in Unicode, forcing ad-hoc handling ([Unicode L2/19-401](https://www.unicode.org/L2/L2019/19401-telugu-sign-nukta.pdf)).

**Evaluation.** Round-trip CER on all code points for the strict scheme (nukta, candrabindu, anusvara, Telugu forms); token-level agreement with attested romanizations from the Dakshina set for the natural mode (Dakshina is CC BY-SA 4.0, unconfirmed, evaluation use only); loanword recovery rate on the code-switch set; schwa-deletion accuracy against a lexicon; a small human preference panel. Romanization quality has no published quantitative baselines.

---

## 7. Risks, budget and timeline

### 7.1 Risk register (likelihood and impact are our proposals)

| # | Risk | L / I | Mitigation |
|---|---|---|---|
| 1 | **Telugu insufficient**: 0.7k T1 hours; streaming Telugu ~30 WER published | High / High | Pseudo-label Vaani Telugu (~2.1k h); phase scope (Hindi + English GA, Telugu beta); decide on T2 (Kathbath, Shrutilipi) under written risk acceptance; in-house data collection |
| 2 | **Nemotron tokenizer/prompt cannot take Telugu**; modified vocab does not export or load in sherpa-onnx | Medium / High | Stage 1 tracer bullet; Arm B fallback; custom vocabulary-extension code |
| 3 | **600M too heavy for target laptops** (no laptop RTF exists) | Medium / High | Stage 1 gate; 320-560 ms chunks; thread tuning; Arm B/D; distillation to a smaller student |
| 4 | **Licence blocker** (Nemotron OpenMDW-1.1 versus NVIDIA Open Model License; gated MIT cards; data conflicts; teacher output terms) | Medium / Critical | Written confirmations (Section 9); T1-only rebuildable model; attribution manifest; counsel review of OpenMDW-1.1 text (unread) |
| 5 | **Code-switch data quality**: no real Telugu-English corpus; synthetic data can regress read speech (+6.6 WER in one preprint) | High / Medium | Mix synthetic with real; in-house CS test set; ablate with and without; report synthetic separately |
| 6 | **Catastrophic forgetting** (English, Hindi) after Telugu full FT (Irish-on-Whisper: English LibriSpeech 3.7 to 8.8 [M]) | Medium / Medium | English replay at least 20-30%; EWC or WiSE interpolation; English regression gate |
| 7 | **Pseudo-label noise** (teacher Telugu ~25-26 WER) bounds student quality and teacher output terms unverified | High / Medium | Two-teacher agreement, script/LID/repetition filters, filtered-versus-unfiltered ablation, drop pseudo-labels if teacher licence fails |
| 8 | **Export/runtime drift**: silent mis-decoding on old sherpa versions; ONNX port loses accuracy (0.75 abs) | Medium / High | Version-pinned bundles, parity CI, sidecar isolation |
| 9 | **Compute estimate off by 2x** (no A10G benchmark exists) | Medium / Medium | Stage 1 measurement; reserve; spot plus checkpointing; consider A100 community for batch decoding |
| 10 | **Hallucination/repetition and script confusion** in streaming transducers on Indic | Medium / Medium | Structurally lower than seq2seq (our inference); insertion-rate and script-fidelity gates; training-data filters |
| 11 | **Normalization/evaluation artefacts** (Telugu agglutination, script choice for English words) mislead decisions | Medium / Medium | Frozen normalizer, CER plus WER, multi-reference gold core, transliteration-invariant code-switch scoring |
| 12 | **Domain mismatch**: Vaani is phone/image-prompted, test is laptop microphone | Medium / Medium | Noise/RIR augmentation (MUSAN, RIRS_NOISES), in-house laptop-microphone test set |

### 7.2 Budget (all estimates; see Section 3 for assumptions)

| Stage | GPU-hours [E] | On-demand @ $1.006/h | Spot @ ~$0.45/h |
|---|---|---|---|
| 0 Governance | 0 | $0 | $0 |
| 1 Spike | 12 | $12 | $5 |
| 2 Harness and baselines | 8 | $8 | $4 |
| 3 Data build (pseudo-labels) | 40 | $40 | $18 |
| 4 Bake-off (3 arms x 30) | 90 | $90 | $41 |
| 5 Main post-training | 150 | $151 | $68 |
| 6 Compression and export | 10 | $10 | $5 |
| 7 Evaluation and hardening | 30 | $30 | $14 |
| **GPU total** | **~340** | **~$341** | **~$153** |
| Synthetic TTS (single preprint figure for 22k utterances) | n/a | ~$50 [M, preprint] | ~$50 |
| Contingency (15%) | ~50 | ~$50 | ~$25 |
| **Planning range** | | **~$300-450** | **~$180-280** |

**Costs not sourced and not included:** storage (IndicVoices archives are 745 GB; Vaani is larger), recording and annotating the in-house test set (cost per hour of Indic transcription not found), engineer time, legal review. A100 community pricing (~$1.39/h) may be cheaper per audio-hour than A10G on-demand if it is 2.5-3x faster, which is unverified here; validate with a 10-minute benchmark.

### 7.3 Timeline (about 16 weeks, estimate [E], one to two engineers plus part-time legal)

| Weeks | Activity |
|---|---|
| 0-2 | Stage 0 governance; **Stage 1 spike**; start speaker recruitment |
| 2-4 | Stage 2 harness, baselines, in-house recording and annotation |
| 3-5 | Stage 3 data build, pseudo-labelling, code-switch synthesis |
| 5-7 | **Stage 4 bake-off**; approval checkpoint: base-model decision memo |
| 7-11 | Stage 5 main post-training and ablations |
| 10-13 | Stage 6 compression and export |
| 12-15 | Stage 7 evaluation gate and hardening; MVP go/no-go |
| 12-16 | Stage 8 application layer, packaging, optional Romanization, legal sign-off |

Approval structure: seniors approve the plan and spike after Section 9 items 1-3 are filed; a second approval after the Stage 1 gate; a third at the Stage 4 base-model decision; a final one at the MVP gate.

---

## 8. Source conflicts and unverified claims (surfaced, not resolved)

| Topic | Conflict or gap | Handling |
|---|---|---|
| Nemotron-3.5 licence | HF card: OpenMDW-1.1; Together AI listing: NVIDIA Open Model License; OpenMDW-1.1 text and derivative clauses unread | Counsel to read text; ask NVIDIA |
| Indic-Transcribe base model | Flex card names canary-1b-v2; a press report says "post-trained on Nemotron 3.5"; release dates differ (Sept 4 versus 12) | Not relevant to our choice; treat card as primary |
| Nemotron-3.5 Telugu | No source confirms Telugu is or is not among the 8 "tokenizer-recognized but un-fine-tuned" locales | Stage 1 tokenizer test |
| Nemotron-3.5 CTC head | Card describes RNNT; hybrid CTC presence unverified | Check in spike |
| SraVaani-0.5-live card | Says streaming WER is "reported for Hindi only" yet tabulates Telugu; "real-time-safe" CPU claim with no numbers | Re-measure |
| SraVaani-1.0 Hindi WER | 12.4 (card) versus 14.0 (paper) | Use re-run baseline |
| IndicConformer Hindi on Vaani-Benchmark-V1.0 | 13.2 (card) versus 20.0/16.8/13.1 by approach (paper); likely different reference counts or scoring | Use own multi-reference scoring |
| IndicConformer licence | MIT on AI4Bharat cards; community GGUF repack says CC-BY-4.0; training-data licences unstated | Written confirmation |
| Voxtral Realtime Hindi WER | Card: 2.4-5.6 FLEURS; paper: 10.7-14.3 | Normalization differs; not comparable; model disqualified anyway |
| Omnilingual Hindi/Telugu | Meta CSV: Hindi CER 3.6, Telugu 6.5 (7B LLM); BuzzASR: Hindi CER 46.0 / Telugu WER 32.3 (7B); Voice of India: Telugu OIWER 50.7 | Unresolved; likely script/normalization/test-set mismatch; do not rely on Omnilingual as teacher |
| Kathbath, Lahaja, IndicVoices-R, SPRING-INX, GigaSpeech, Emilia licences | Conflicting labels across metadata, body text and aggregator pages (Section 2) | More restrictive reading until resolved |
| IndicVoices hours | Paper 7.3k h; later listing 12k h; HF card 23.7k total / 11.2k transcribed; our per-language hours are estimates (+/-15%) | Recount from manifest after download |
| Vaani hours | HF 31,278 h / 2,122 transcribed versus paper 31,255 / 2,043; paper's fine-tuning subset lower (594/113 h) | Recount; check phase ambiguity on the card |
| sherpa-onnx int8 sizes | 464 MB (Softcery) versus ~632-650 MB (OpenWhispr) | Packaging differences suspected, not confirmed |
| Softcery single-stream RTF | Fetched table 0.085; search snippet 0.067 | Use fetched table |
| Microsoft versus Softcery RTF | RTFx ~7 (EPYC, 32 cores) versus ~16 (Ryzen, 4 threads) | Different CPU/runtime/chunking; measure ourselves |
| Whisper normalizer effect | Collabora vendor blog: 10.11 versus 17.35 WER by normalizer | Reinforces the frozen-normalizer rule |
| Vistaar README | IndicWhisper FLEURS/CV columns swapped between tables | Do not quote per-column without checking |
| Stateful Conformer paper | Inconsistent 4x versus 8x subsampling statements; paper does not evaluate fine-tuning offline checkpoints into streaming | We use NVIDIA's released streaming checkpoint instead |
| NVIDIA "FAQ" page | A page branded NVIDIA says Canary-1B-v2 includes Hindi; AI-generated with tracking links | Model card wins (no Hindi) |
| Silero VAD licence | MIT in LICENSE file; "CC BY-NC 4.0" badge in README | Counsel to verify |
| Cloud prices | Modal A100 $2.50 versus $3.72; Lambda A10 $0.86-1.29; spot varies daily | Verify on provider pages |
| Vendor/unverified claims carried | NVIDIA "few hundred hours" FAQ [V]; Saaras <150 ms TTFT [V]; Voice of India is run by an interested party and Scribe v2 report is hosted on the same domain; Danish 10 h Nemotron result is a single community anecdote; Bhili ~200 h model is unreleased | Not used as evidence of our result |
| Not retrieved at all | OpenMDW-1.1 text; Indic Open Model License v1.0 text; gate-condition text for IndicVoices/Vaani/Kathbath/IndicConformer/SraVaani; Whisper licence; NGC 114M streaming-model licences; unified-RNNT paper numbers; the full Nemotron fine-tune blog recipe beyond excerpts; laptop RTF for any Indic model; int8 versus fp32 on Hindi/Telugu; A10G throughput; Telugu ZWNJ and ITN guidance; TDT cache-aware export to sherpa-onnx | Stage 0 and Stage 1 tasks |

---

## 9. Open questions and decisions for the seniors

**Legal review items**
1. Read OpenMDW-1.1 in full (and resolve the Together AI "NVIDIA Open Model License" listing); confirm derivative-model, attribution and commercial-redistribution terms for a fine-tuned, int8-converted model shipped on end-user devices.
2. Obtain written confirmation from AI4Bharat and ARTPARK-IISc that MIT-tagged gated models (IndicConformer, SraVaani) permit commercial use, fine-tuning and use of their outputs as pseudo-labels.
3. Capture gate-condition text for IndicVoices, Vaani, Kathbath at download time and have counsel review it.
4. Decide the position on T2 data (Kathbath prompts from crawled text, Shrutilipi/AIR, NPTEL, BY-SA sets) and on whether CC BY-SA data may touch shipped weights.
5. Clarify attribution obligations for CC BY datasets in model documentation (CC's guidance does not decide whether weights are adaptations); confirm no Indian TDM exception or DPIIT licensing outcome affects the plan; assess DPDP implications for voice data in the in-house test set (consent, storage, retention).
6. Review TEN VAD, Silero VAD, Cadence-Fast, NeMo-text-processing and any TTS/LLM used for synthesis for licence compatibility.

**Engineering and product decisions**
7. **Scope:** commit to Hindi + Telugu + English at GA, or Hindi + English GA with Telugu beta given the 0.7k T1 hour ceiling and ~30 WER streaming floor.
8. **Latency target:** default chunk size (we suggest 320-560 ms) and acceptable first-token P90.
9. **Minimum-spec laptop:** the Stage 1 gate needs a named lowest-spec x86 and Apple device.
10. **Output policy:** Latin for English words, ASCII digits, punctuation and casing in or out for Indic output (affects data prep and the P&C workstream).
11. **Tokenizer strategy:** small per-script aggregate (256-512 each) versus shared 5-8k BPE (Section 3.1), and extend-versus-replace for Nemotron.
12. **Investment in the in-house test set:** budget and owner for recording and annotating about 3-5 h per language, and ownership of the private split.
13. **T1-only versus T1+T2 production target**, and whether a T1-only ablation is a release requirement.
14. **Compute decisions:** accept A10G on-demand versus spot with checkpointing; allow an A100 for batch pseudo-label decoding.
15. **Gate thresholds:** approve the Section 4.4 proposals after Stage 2 re-runs the baselines.

---

## Conclusion

The research changes the question from "which model should we use" to "which gap should we close first". Nemotron-3.5 closes the streaming, Hindi, runtime and licence-statement gaps in one checkpoint; the remaining gaps are Telugu data, code-switching data and laptop-class CPU speed, none of which a model choice fixes. The project's real critical path is therefore a de-risking spike (tokenizer, prompt table, export of a modified model, A10G throughput, laptop RTF) plus a legal workstream, with both settled before the bake-off spends most of the GPU budget.

Two implications deserve senior attention. First, the cheapest part of the plan is the compute: roughly $340 of A10G time covers every stage, but the in-house test set, legal review and storage are unpriced and may cost more. Second, the evidence base is thin precisely where the product is hardest: there are no published Telugu-English results from any model, no streaming Telugu measurement other than a single vendor card, and no Indic laptop RTF. The plan therefore promises a measured answer, not a guaranteed one, and builds in gates (a CPU gate, a Telugu learning-curve gate, an MVP gate) at which the team can switch to the 114M arm, narrow the scope to Hindi and English, or stop.
