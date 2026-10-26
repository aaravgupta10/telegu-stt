# Evaluation methodology and published baselines for Hindi / Telugu / Indian-English (code-switched) streaming ASR (as of 2026-10-08)

Conventions used below: "WER" is word error rate in percent (lower is better). "OIWER" is Orthographically-Informed WER (lattice of accepted spellings), NOT comparable to strict single-reference WER. "[MEASURED-3P]" = number produced by an independent/third-party paper; "[MEASURED-SELF]" = produced by the model's own authors/vendor on a public set; "[VENDOR]" = vendor docs/blog/press claim, unverified. Where I could not read a PDF table directly (WebFetch cannot parse PDFs), I say so. Inferences are labelled as such and are mine, not the sources'.

---

## 1. Which benchmarks exist, their licenses, and which test splits are usable (Vistaar, IndicVoices, Kathbath, FLEURS, CV, MUCS, Svarah, Lahaja, Shrutilipi, SPRING-INX, Vaani, Open ASR Leaderboard, 2025-26 newcomers, Telugu-English code-switch)

### Takeaway
There is a usable open core (Vistaar test sets, IndicVoices, Kathbath, Svarah, Lahaja, Vaani-Benchmark-V1.0, Monsoon hi-IN/en-IN), mostly CC BY 4.0 but many are gated on Hugging Face and several have unclear or conflicting license statements, so the legal check must be done per card. There is NO open Telugu-English code-switch benchmark; Hindi-English has MUCS-2021, Vaani-V1.0 token tagging, and synthetic CS-FLEURS, so the team must build its own Telugu-English set. The Open ASR Leaderboard added Hindi and Indian English (Monsoon) in late Aug 2026 but not Telugu.

### Cited Findings
**Vistaar (AI4Bharat, Interspeech 2023)**
- 59 benchmarks assembled from 7 public datasets (Kathbath, Kathbath-Hard, CommonVoice, FLEURS, IndicTTS, MUCS, GramVaani) across 12 languages (incl. hi, te); training set >10,700 h; repo says "Vistaar is MIT-licensed" for the fine-tuned models, but lists NO per-dataset licenses and no normalization description; eval script takes a JSON-lines manifest (`audio_filepath`, `duration`, `text`) and per-language train/valid/test folders — [Vistaar GitHub](https://github.com/AI4Bharat/vistaar)
- Telugu coverage in Vistaar: Kathbath, Kathbath-Hard, FLEURS, IndicTTS, MUCS only (no CommonVoice/GramVaani Telugu) — [Vistaar GitHub](https://github.com/AI4Bharat/vistaar)
- Vistaar finding: ranking models on one benchmark can be weakly correlated with results on another — [Vistaar paper listing/secondary summary](https://ar5iv.labs.arxiv.org/html/2305.15386) (claim relayed by search summary; not verified in the PDF)

**IndicVoices (AI4Bharat, ACL Findings 2024)**
- Paper: ~7,348 h of speech, 16,237 speakers, 145 districts, 22 languages, 1,639 h transcribed — [arXiv 2403.01926](https://arxiv.org/abs/2403.01926)
- HF card now states CC BY 4.0, gated (must agree to share contact info), and totals "23.7K hours overall, 11.2K transcribed"; card lists a `valid` split in its example and `_train` archives; it does NOT document test split sizes, per-language hours, or code-switch annotation — [IndicVoices HF card](https://huggingface.co/datasets/ai4bharat/IndicVoices). NOTE the paper (7.3K h) and the card (23.7K h) disagree on total size (dataset has apparently grown); AIKosh also lists CC BY 4.0 — [AIKosh IndicVoices](https://aikosh.indiaai.gov.in/home/datasets/details/indicvoices.html)
- IndicVoices contains monolingual and code-switched speech (search summary of CoSTA) — [CoSTA](https://arxiv.org/pdf/2406.10993)

**Kathbath (IndicSUPERB)**
- 1,684 h, 12 languages, gated. License is internally inconsistent on the card: metadata tag cc-by-4.0 but the "Licensing Information" text says packaging is CC0, with raw text from IndicCorp (not owned by AI4Bharat). Card does not list test-known/test-unknown/noisy splits or Hindi/Telugu hours — [Kathbath HF card](https://huggingface.co/datasets/ai4bharat/Kathbath). Official IndicSUPERB page offers clean and noisy download splits — [IndicSUPERB GitHub](https://github.com/AI4Bharat/IndicSUPERB)

**Svarah (Indian-accented English)**
- 9.6 h, 117 speakers, 65 districts, 19 states, `test` split only, CC BY 4.0, gated — [Svarah HF card](https://huggingface.co/datasets/ai4bharat/Svarah)

**Lahaja (Hindi accents)**
- 12.5 h, 132 speakers (122 non-native Hindi speakers), 19 native languages, read + voice-assistant + extempore + named-entity prompts; `test` only, gated; card text says CC BY 4.0 but metadata tag says MIT (conflict) — [Lahaja HF card](https://huggingface.co/datasets/ai4bharat/Lahaja), [Lahaja paper](https://arxiv.org/html/2408.11440v1)

**Shrutilipi**
- Mined from All India Radio news bulletins: Hindi 1,620 h, Telugu 390 h; CC BY 4.0 (AI4Bharat/AIKosh). A third-party HF mirror (amithm3/shrutilipi) lists apache-2.0, conflicting — use the AI4Bharat source — [AIKosh Shrutilipi](https://aikosh.indiaai.gov.in/home/datasets/details/shrutilipi.html). I did not find a Shrutilipi "test split" definition in sources.

**SPRING-INX (IIT Madras)**
- ~2,000 h across 10 languages (Assamese, Bengali, Gujarati, Hindi, Kannada, Malayalam, Marathi, Odia, Punjabi, Tamil) — NO Telugu — [arXiv 2310.14654](https://arxiv.org/pdf/2310.14654). Malayalam AIKosh entry shows CC BY 4.0; official page says data was collected via paid vendors; Hindi license not confirmed — [AIKosh SPRING-INX Malayalam](https://aikosh.indiaai.gov.in/home/datasets/details/spring_inx_malayalam.html), [SPRING-INX data page](https://asr.iitm.ac.in/dataset)

**Vaani (ARTPARK-IISc/Google)**
- Vaani-Benchmark-V1.0 (arXiv 2606.21408): Hindi, CC BY 4.0, 5,050 utterances, 1,062 speakers, 10.91 h, 102 districts, 3 independent reference transcripts per utterance, English code-switch tokens tagged; splits not described in the text I could read — [Vaani Benchmark V1.0](https://arxiv.org/html/2606.21408)
- IndicConformer-600M model card reports Hindi WER 13.2 on `ARTPARK-IISc/Vaani-Benchmark-V1.0` — [IndicConformer card](https://huggingface.co/ai4bharat/indic-conformer-600m-multilingual)

**Open ASR Leaderboard (Hugging Face)**
- Multilingual track originally European only (de, fr, it, es, pt) — [HF blog](https://huggingface.co/blog/open-asr-leaderboard), [paper 2510.06961](https://arxiv.org/abs/2510.06961v2)
- Aug 2026: "Voice Arena Monsoon" en-IN (in default columns, counts to Average WER) and hi-IN (Multilingual tab) added. Splits: en-IN public 5.62 h/1,444 spk, private 5.58 h/1,405 spk; hi-IN public 1.33 h/468 spk/753 clips, private 4.47 h/1,571 spk; conversational, dual-channel peer-to-peer, own devices; transcripts corrected by native linguists through a five-level process; hi-IN scored by OIWER against lattices with open-source `voi-oiwer`; private split evaluated via PR — [HF blog: global south](https://huggingface.co/blog/open-asr-leaderboard-global-south), [aireiter mirror, updated 2026-08-29](https://aireiter.com/blog/open-asr-leaderboard-monsoon-hindi-indian-english). Dataset cards: [en-IN](https://huggingface.co/datasets/VoiceArena/MonsoonASR-Open-ASR-leaderboard-en-IN), [hi-IN](https://huggingface.co/datasets/VoiceArena/MonsoonASR-Open-ASR-leaderboard-hi-IN). A search summary stated CC-BY-4.0 for the datasets but the mirror page I read did not state a license — check the cards. No Telugu on the leaderboard (found no source saying otherwise).

**2025-2026 newcomers**
- Voice of India (Josh Talks + AI4Bharat-derived OIWER): 15 languages, 536 h, 306,230 utterances, 36,691 speakers, 139 regional clusters, unscripted telephonic conversations; CLOSED test set, open subset via GitHub submission pipeline (github.com/JoshTalks/voice-of-india), private eval on request; no license stated — [VoI paper](https://arxiv.org/html/2604.19151), [search summary](https://voiceofindiablogs.ai.joshtalks.com/)
- Agricultural-context ASR benchmark (Digital Green; Hindi, Telugu, Odia; 10,864 pairs on HF; license not stated in paper; no text normalization described) — [arXiv 2602.03868](https://arxiv.org/html/2602.03868v2)
- Vividh-ASR (Hindi + Malayalam only; tiers by acoustic complexity A studio/read, B broadcast, C spontaneous, D noisy; Hindi 36.96 h) — [Vividh blog](https://huggingface.co/blog/adalat-ai/vividh-benchmark)
- IndicST (Krutrim) is a speech TRANSLATION corpus built on Kathbath/Svarah-style data, not an ASR WER benchmark — [IndicST](https://huggingface.co/datasets/krutrim-ai-labs/IndicST)
- Sarvam: Saaras v4 post (2026-09-25) evaluates on Vistaar-style sets (Common Voice, FLEURS, GramVaani, IndicTTS, Kathbath, Kathbath Noisy, MUCS) and for English incl. Svarah; also introduces IndicContextEval; no scores in text — [Saaras v4](https://www.sarvam.ai/blogs/introducing-saaras-v4)

**Code-switch benchmarks**
- MUCS 2021: Hindi-English and Bengali-English code-switch tracks plus monolingual tracks incl. Telugu; NOT Telugu-English; Hindi-English blind test 6.24 h — [MUCS overview](https://arxiv.org/abs/2104.00235), [code-switched Indic paper](https://arxiv.org/pdf/2203.16578). License not verified.
- CS-FLEURS (Interspeech 2025): 4 test sets, 113 code-switched pairs across 52 languages, partly TTS-generated; whether Telugu-English is included and its license NOT confirmed — [CS-FLEURS](https://arxiv.org/pdf/2509.14161)
- CoSTA authors cut ~2 h of Telugu code-switched speech from IndicVoices for evaluation (the only real Telugu-English eval-size precedent found; derived-set license unstated) — [CoSTA](https://arxiv.org/pdf/2406.10993)
- Telugu-English text-only treebank (UD TECT) exists; a 200 h Telugu-English corpus is mentioned on a forum but is access-by-request; JSALT-2022 slides mention 15 h Telugu-English CS train speech, availability unstated — [UD TECT](https://universaldependencies.org/treebanks/qte_tect), [DeepLearning.AI forum](https://community.deeplearning.ai/t/request-for-telugu-english-code-switched-speech-corpus-asr-project/890896), [JHU CLSP slides](https://www.clsp.jhu.edu/wp-content/uploads/2022/07/2022_07_06.pdf)

### Inferences
- A cleared-for-commercial-use evaluation stack today is: Vistaar test sets (check each source license), Kathbath (resolve CC0 vs CC BY text), IndicVoices test/valid (CC BY 4.0), Svarah, Lahaja, Vaani-Benchmark-V1.0, Monsoon public splits. Keep a license ledger per dataset card snapshot (date-stamped) because cards are inconsistent.
- Telugu has no non-AI4Bharat independent open conversational test set except the Agricultural benchmark and VoI open subset; treat IndicVoices-te as the primary spontaneous Telugu set and build an in-house one to avoid depending on a single source.
- Because the Open ASR Leaderboard hi-IN public split is only 1.33 h and Hindi is scored with OIWER, it is useful for a public-facing comparison but too small for fine-grained regressions.

### Gaps
- FLEURS (hi_in, te_in) and Common Voice (hi, te) test-split sizes/licenses: the HF FLEURS fetch returned nothing; I did not verify CV hi/te license or split sizes in this session.
- Official IndicVoices/Kathbath/Shrutilipi "test" split definitions and per-language hours for hi/te.
- License of MUCS 2021 data, SPRING-INX Hindi, Agricultural benchmark, Voice of India open subset.
- Whether CS-FLEURS contains Telugu-English; CS-FLEURS license.
- Vaani eval sets beyond Vaani-Benchmark-V1.0 (Hindi only); no Telugu Vaani benchmark found. RESPIN (used by SraVaani) not investigated.

---

## 2. Published baseline WER/CER per benchmark per language, by model, with source/date and measured-vs-vendor flags; streaming vs offline

### Takeaway
Offline open-model state of the art (mean across mixed Indic test sets): Hindi roughly 13-14% WER and Telugu roughly 25-26% WER (IndicConformer-600M 13.8 / 26.4; SraVaani-1.0 14.0 / 25.1; IndicWhisper 13.6 / 28.8 on Vistaar), while on hard conversational/telephony audio (Voice of India, OIWER) IndicConformer gets 8.2 (hi) / 23.7 (te) and Telugu is 2-3x harder than Hindi. Whisper large-v3 is poor on Hindi (~30-33% WER) and unusable on Telugu; Omnilingual-LLM looks superb on its own CER table but is poor on third-party conversational Telugu/Hindi. The only open streaming models with published Hindi numbers are NVIDIA Nemotron-3.5-ASR-Streaming (Hindi FLEURS 6.8-8.1% WER, likely in-domain), and SraVaani-0.5-live (Hindi 18-22%, Telugu 30-35%); I found NO controlled offline-vs-streaming study for Indic, but same-family evidence suggests a +15-25% relative WER penalty at 0.3-2 s chunks and a much larger absolute gap at zero look-ahead.

### Cited Findings

**Master table (all WER unless marked CER; lower is better)**

| Model / system | Benchmark | Hindi | Telugu | English-IN | Source, date, flag |
|---|---|---|---|---|---|
| IndicConformer-600M-multi (MIT, gated, 22 langs, hybrid CTC+RNNT, offline) | mean over 8 (hi) / 6 (te) test sets (CV, FLEURS, IndicTTS, Kathbath, RESPIN, GramVaani, MUCS, VAANI) | 13.8 | 26.4 | - | SraVaani 1.0 paper, Aug 2026 [MEASURED-3P-ish; authors are a competing model's authors] — [arXiv 2608.08235](https://arxiv.org/html/2608.08235) |
| IndicConformer-600M | Voice of India (telephony, OIWER) | 8.2 | 23.7 | - | VoI paper, Apr 2026 [MEASURED-3P] — [arXiv 2604.19151](https://arxiv.org/html/2604.19151) |
| IndicConformer-600M | Vaani-Benchmark-V1.0, Approach 1/2/3 (1/2/3 references) | 20.0 / 16.8 / 13.1 | - | - | Vaani V1.0 paper, Jun 2026 [MEASURED-3P] — [arXiv 2606.21408](https://arxiv.org/html/2606.21408) |
| IndicConformer-600M | Vaani-Benchmark-V1.0 (model card) | 13.2 | - | - | AI4Bharat card [MEASURED-SELF]; conflicts with 20.0 (1 ref) above — likely different reference/scoring — [card](https://huggingface.co/ai4bharat/indic-conformer-600m-multilingual) |
| IndicConformer (community GGUF repack, Hindi) | Kathbath test / FLEURS | 13.5 / 15.2 | - | - | community repack, not official [MEASURED-SELF, unverified] — via search summary of [GGUF card](https://huggingface.co/Singla0009/IndicConformer-GGUF) |
| IndicWhisper (Whisper fine-tuned on Vistaar train) | Kathbath / Kathbath-Hard / CV / FLEURS / IndicTTS / MUCS / GramVaani | 10.3 / 12.0 / 11.4 / 15.0 / 7.6 / 12.0 / 26.8 (avg 13.6) | 25.0 / 27.8 / - / 25.4 / 33.8 / 32.1 / - (avg 28.8) | - | AI4Bharat README, 2023 [MEASURED-SELF, in-domain training splits] — [Vistaar](https://github.com/AI4Bharat/vistaar) |
| Google STT / Azure / IndicWav2vec / NVIDIA-large (Hindi) | same Vistaar sets, avg | 23.9 / 20.0 / 21.0 / 18.6 | - | - | Vistaar README [MEASURED-SELF]; NOTE the comparison table lists IndicWhisper FLEURS=11.4 and CV=15.0, swapped vs the per-language table (CV 11.4, FLEURS 15.0): column-order ambiguity in the README, so don't quote per-column from it without checking |
| IndicWhisper | Lahaja | see IndicASR rows | - | - | Lahaja paper does not name IndicWhisper |
| IndicASR M1 (IndicVoices mono) / M2 (multi) / M3 (Vistaar+SPRING-INX+IndicVoices) / M4 (+synthetic Eng-Hindi) | Lahaja | 19.4 / 16.7 / 14.3 / 18.6 | - | - | Lahaja paper, Aug 2024 [MEASURED-SELF] — [arXiv 2408.11440](https://arxiv.org/html/2408.11440v1) |
| Whisper large-v3 | Lahaja | 32.4 | - | - | same paper [MEASURED-SELF] |
| Whisper large-v3 | Vaani-Benchmark-V1.0 (1/2/3 refs) | 32.8 / 30.0 / 26.4 | - | - | Vaani V1.0 [MEASURED-3P] |
| Whisper large-v3 (zero-shot) | FLEURS + CV combined, normalised (BuzzASR table) | WER 30.98, CER 11.92 | WER 101.25, CER 74.67 | - | BuzzASR, 2026-10-04 [MEASURED-3P] — [arXiv 2609.09554](https://arxiv.org/html/2609.09554) |
| Whisper large-v3-turbo | 75-sentence FLEURS-style run on one MacBook | 30.42 | - | - | Whisper Notes blog [VENDOR, tiny sample] — [blog](https://whispernotes.app/blog/qwen3-asr-vs-whisper) |
| Whisper (OpenAI API) | Agricultural benchmark | 46.8 | Telugu "incoherent", excluded | - | Digital Green paper, Jan 2026 [MEASURED-3P] — [arXiv 2602.03868](https://arxiv.org/html/2602.03868v2) |
| Whisper large-v3 | Svarah (and large 1550M) | - | - | 7.2 (medium 8.3, base 13.6; LibriSpeech 2.7) | Svarah paper, 2023 [MEASURED-SELF] — [arXiv 2305.15760](https://arxiv.org/pdf/2305.15760) (via search summary; table not read directly) |
| Whisper-large-v3-turbo etc. (8 models) | Monsoon en-IN public | - | - | 4.81-4.99 WER (indistinguishable) | HF blog, Aug 2026 [MEASURED] — [HF blog](https://huggingface.co/blog/open-asr-leaderboard-global-south) |
| Omnilingual ASR 7B LLM | Meta per-language CSV (test set not stated in CSV; header "Language, Training Hours, CER") | CER 3.6 (236.7 h train) | CER 6.5 (229.3 h) | CER 3.0 (63,591 h) | Meta repo [MEASURED-SELF] — [CSV](https://github.com/facebookresearch/omnilingual-asr/blob/main/per_language_results_table_7B_llm_asr.csv) |
| OmniASR LLM 7B / 1B | Voice of India (OIWER) | 13.7 / 14.9 | 50.7 / 57.3 | - | VoI [MEASURED-3P] |
| Omni 7B / 1B | BuzzASR combined FLEURS+CV | WER 65.71 / 59.00; CER 46.00 / 38.77 | WER 32.29 / 36.80; CER 8.64 / 9.62 | - | BuzzASR [MEASURED-3P]; CONFLICT: Hindi CER 46 here vs 3.6 in Meta's CSV; unresolved (likely script/normalization/test-set mismatch — verify) |
| OmniASR_LLM_1B | Vaani V1.0 (1/2/3 refs) | 32.2 / 29.3 / 25.6 | - | - | Vaani V1.0 [MEASURED-3P] |
| Qwen3-ASR 0.6B / 1.7B (Apache-2.0; Telugu NOT supported) / Flash-1208 (proprietary API) | FLEURS | 19.12 / 17.15 / 13.77 | not supported | accented-English avg over 16 accents 16.62 / 16.07 (not India-specific) | Qwen3-ASR report, Jan 2026 [MEASURED-SELF] — [arXiv 2601.21337](https://arxiv.org/html/2601.21337) |
| NVIDIA Nemotron-3.5-ASR-Streaming-0.6B (OpenMDW-1.1; Hindi in top tier; Telugu and en-IN NOT listed) | FLEURS, 80ms / 160 / 320 / 560 / 1120 ms, language known | 8.13 / 7.97 / 7.41 / 7.05 / 6.81 | not supported | - | NVIDIA card [MEASURED-SELF; FLEURS and Common Voice are in its training data] — [card](https://huggingface.co/nvidia/nemotron-3.5-asr-streaming-0.6b) |
| Nemotron-3.5 (same) | FLEURS, auto language-ID | 11.47 / 10.83 / 9.88 / 9.26 / 8.23 | - | - | same card |
| Nemotron-3.5 (same) | Vaani-Benchmark-V1.0 | 20.2 | - | - | same card [MEASURED-SELF] (out-of-domain; ~3x worse than FLEURS) |
| SraVaani-0.5-live (MIT, ~430M, cache-aware FastConformer-CTC, 63 languages, streaming) lookahead 0 / 80 / 480 / 1040 ms | 8 test sets (Vaani, RESPIN, FLEURS, IndicTTS, CV, GramVaani, Kathbath, MUCS) | 22.1 / 21.3 / 19.3 / 18.0 | 34.6 / 33.6 / 31.4 / 30.3 | - | ARTPARK-IISc card [MEASURED-SELF] — [card](https://huggingface.co/ARTPARK-IISc/SraVaani-0.5-live) |
| SraVaani-1.0 (offline, FastConformer hybrid TDT-CTC) | same sets | 12.4 (card) vs 14.0 (paper) | 25.1 (both) | - | card vs [arXiv 2608.08235](https://arxiv.org/html/2608.08235): Hindi conflict (12.4 vs 14.0), unresolved |
| Hindi/Hinglish Zipformer-M CTC (Apache-2.0, 64.6M, causal chunked 16/32/64/full, greedy, no LM) | IndicVoices-hi / internal Hinglish calls / Svarah | 25.7 / 39.9 / 44.5 (phase 3, ~337 h base) | - | Svarah 44.5 | community card [MEASURED-SELF; trained on IndicVoices-hi, Svarah subset] — [card](https://huggingface.co/Vengadanathan/hindi-hinglish-zipformer-ctc-streaming) |
| Indian-English Streaming Zipformer (Apache-2.0, 66.1M, int8 ~68 MB, chunk 64=640 ms) | Svarah | - | - | 20.73 (icefall greedy), 26.90 (fp32 sherpa mod. beam), 27.96 (int8 sherpa greedy); base model 41.03 | community card [MEASURED-SELF]; fine-tuned on 277 h NPTEL with Whisper-large-v3 pseudo-labels — [card](https://huggingface.co/Akshatkasera007/STT-streaming-zipformer-indian-en) |
| Sarvam Audio / Saarika 2.5 / Gemini 3 Pro / Amazon / ElevenLabs Scribe v2 / Gemini 3 Flash / Deepgram Nova-3 / GPT-4o-transcribe / AssemblyAI | Voice of India OIWER | 5.0 / 6.2 / 6.0 / 6.8 / 7.7 / 8.3 / 13.0 / 33.9 / 19.3 | 18.2 / 18.9 / 21.9 / 19.7 / 23.0 / 27.9 / 43.1 / 69.3 / 105.0 | - | VoI [MEASURED-3P; benchmark run by Josh Talks, an interested party; Scribe v2 report hosted on Josh Talks domain, draft v2 Aug 2026 — [report](https://elevenlabsreport.ai.joshtalks.com/)] |
| Sarvam Saarika v2.5 | Sarvam's own Vistaar run | 11.81 (English 8.26, 11-lang avg 18.32) | CER ~5.47 (table garbled; position-inferred, low confidence) | - | Sarvam docs [VENDOR] — [docs](https://docs.sarvam.ai/api/models/saarika) |
| Sarvam Saaras v2.5 / v3 | IndicVoices (top-10 / 11 languages) | aggregate ~22% / ~19% (19.3 per press) | aggregate only | - | Sarvam blog/press [VENDOR] — [blog](https://www.sarvam.ai/blogs/asr); Saaras/Saarika weights are API-only (no evidence of open weights) |
| Google STT / Vaani-Whisper / Gemini 2.5 Pro / Azure / Sarvam API / MMS / AI4Bharat | Agricultural benchmark | 16.2 / 16.6 / 18.5 / 25.6 / 28.7 / 51.4 / 59.8 | 33.2 / 38.7 / 37.9 / 41.8 / 46.5 / 67.5 / (AI4Bharat not evaluated) | - | Digital Green paper [MEASURED-3P] |
| Whisper-based Hindi fine-tunes (Vaani Large-v3 1.5B, IndicWhisper, Whisper-medium/small FT) | Vividh-ASR Hindi (global weighted, 36.96 h incl. noisy) | 21.05 / 25.01 / 15.73 / 18.73 | - | - | Vividh blog [MEASURED-SELF] — [blog](https://huggingface.co/blog/adalat-ai/vividh-benchmark) |
| NVIDIA Canary-1B-v2 / Parakeet-TDT-v3 | - | NOT supported (25 European languages) | NOT supported | - | [Canary-1b-v2 card](https://huggingface.co/nvidia/canary-1b-v2) (Parakeet-v3 coverage = same 25 European languages per [paper listing 2509.14128](https://arxiv.org/pdf/2509.14128), not read in detail). CONFLICT: a page branded as NVIDIA "FAQ" claims Canary 1B v2 includes Hindi, but it is AI-generated with tracking links — [FAQ page](https://perspectives.nvidia.com/nemotron-speech/task/faq/what-open-speech-models-handle-hindi-english-or-mandarin-english-code-switching/); trust the model card |
| Moonshine | - | Hindi not listed (en, ja, es, zh, ko, vi, uk, ar per Mar 2026 article) | not listed | English only usable | [Techno-Edge, 2026-03-02](https://www.techno-edge.net/article/2026/03/02/4891.html) (secondary) |
| Kyutai STT | - | - | - | English (and French): stt-2.6b-en (2.5 s delay), stt-1b-en_fr (500 ms) | [Kyutai 1B card](https://huggingface.co/kyutai/stt-1b-en_fr); no Indian-English number found |

**Other relevant findings**
- Fine-tuned Whisper per-language Hindi on FLEURS: BuzzASR Hindi fine-tune FLEURS CER 17.06, Telugu 13.53 vs Whisper-large-v3 zero-shot CER 9.28 on Hindi FLEURS in a different card (inconsistent test conditions) — [BuzzASR Hindi card](https://huggingface.co/BuzzASR/hindi), [BuzzASR Telugu card](https://huggingface.co/BuzzASR/telugu) (via search snippet; unverified).
- Omnilingual: Apache-2.0 for code and models (dataset CC-BY-4.0); CTC models 300M (1.3 GiB fp32), 1B (3.7 GiB), 3B, 7B; LLM-ASR 300M-7B (6.1-30 GiB); inference limited to <40 s audio; no streaming; no CPU guidance — [Omnilingual repo](https://github.com/facebookresearch/omnilingual-asr). Meta says 7B LLM-ASR has CER <10 for 78% of 1,600+ languages — [arXiv 2511.09690](https://arxiv.org/abs/2511.09690)
- Agricultural paper: "Whisper (OpenAI API)" Odia 125.6% WER, i.e. insertions dominate — [arXiv 2602.03868](https://arxiv.org/html/2602.03868v2)
- Lahaja: best model ranges from ~10.5 WER (Urdu/Sindhi native-language speakers) to 20.5 (Assamese) by speaker mother tongue; named-entity prompts: Google Chirp 63.2 vs IndicASR M3 24.4 — [Lahaja](https://arxiv.org/html/2408.11440v1)
- Telugu is ~2x harder than Hindi even for best systems (VoI: Sarvam Audio 5.0 vs 18.2; IndicConformer 8.2 vs 23.7; Kathbath: IndicWhisper 10.3 vs 25.0) — [VoI](https://arxiv.org/html/2604.19151), [Vistaar](https://github.com/AI4Bharat/vistaar)
- Telugu script collapse in vanilla Whisper-large-v3 (script fidelity rate 0.46-0.71) vs Hindi SFR >= 0.98 — [Menta, arXiv 2605.03073](https://arxiv.org/html/2605.03073)

**Streaming vs offline evidence**
- SraVaani-0.5-live Hindi: 22.1 (0 ms look-ahead) -> 18.0 (1040 ms); Telugu 34.6 -> 30.3. Versus the larger offline SraVaani-1.0 (Hindi 12.4 card / 14.0 paper; Telugu 25.1): gap +4.0 to +9.7 abs (Hindi), +5.2 to +9.5 abs (Telugu) — confounded by model size/training differences (card values) — [card](https://huggingface.co/ARTPARK-IISc/SraVaani-0.5-live)
- Nemotron-3.5: Hindi FLEURS WER improves 8.13 -> 6.81 (-16% rel.) from 80 ms to 1.12 s chunks; auto-LID adds +1.4 to +3.3 abs; NVIDIA states 80 ms-1120 ms are runtime-selectable without retraining — [card](https://huggingface.co/nvidia/nemotron-3.5-asr-streaming-0.6b), [wavect review](https://wavect.io/blog/nvidia-nemotron-3-5-asr-production-review.md)
- Nemotron English streaming model: 0.16 s -> 0.56 s chunk lowers WER 7.84 -> 7.22 — [HF blog](https://huggingface.co/blog/nvidia/nemotron-speech-asr-scaling-voice-agents)
- Qwen3-ASR, one model offline vs streaming at 2 s chunks (English/Chinese only, no Hindi streaming reported): 1.7B FLEURS-en 3.35 -> 4.02, avg 2.69 -> 3.33 (+24% rel.); 0.6B 4.39 -> 5.38, avg 3.48 -> 4.40 (+26% rel.) — [arXiv 2601.21337](https://arxiv.org/html/2601.21337)
- Korean icefall streaming Zipformer (174M): offline CER 7.16; streaming 7.51 (1.28 s chunk), 7.83 (640 ms), 8.36 (320 ms) — i.e. +5% to +17% rel. — [HF card](https://huggingface.co/kangkyu/icefall-asr-ko-streaming-zipformer-174m)
- NeMo cache-aware (English LibriSpeech, original paper): cache-aware chunked RNN-T 6.3% at 1,360 ms vs buffered 11.3% at 2,000 ms; zero-lookahead RNN-T around 10.6% — secondary write-up; check the paper — [Stateful Conformer paper](https://arxiv.org/html/2312.17279v3)
- Streaming degradation in the wild: a cache-aware Nepali Conformer reports 59.87 WER on real call audio vs 31.5 on gold read speech (520 ms look-ahead) — [card](https://huggingface.co/ampixa/nepali-conformer-streaming)
- Int8: Indian-English Zipformer int8 RTF 0.035 (28.5x realtime) vs fp32 0.183 on a 4-thread Xeon; int8 greedy 27.96 vs fp32 modified-beam 26.90 WER on Svarah (confounded by decoding method, so not a clean quantization penalty) — [card](https://huggingface.co/Akshatkasera007/STT-streaming-zipformer-indian-en)

### Inferences
- "Best open offline" today = IndicConformer-600M (MIT) or SraVaani-1.0 for Hindi/Telugu; Hindi ~13-14 (mean of mixed sets), Telugu ~25-26. Headline per-benchmark numbers differ 3x with test difficulty (Nemotron Hindi 6.8 FLEURS vs 20.2 Vaani; IndicConformer 8.2 telephony OIWER vs 13.8 mixed-set mean vs 20.0 Vaani single-ref), so no target is meaningful without naming the test set and scoring.
- Expected streaming penalty (my synthesis): +15-25% relative for 0.5-1.1 s chunks vs same-architecture offline; larger (+30-50% rel. or ~+9 abs) at 0-80 ms look-ahead; small-model (<100M) + int8 will likely add a further +10-30% rel. Nothing published measures all three together for Hindi/Telugu; the team must measure.
- Omnilingual is not a good Indic CPU-streaming candidate (no streaming, 40 s limit, large) and its third-party Telugu conversational numbers (OIWER 50.7) are far from its own CSV CER (6.5) — domain shift plus metric difference (CER vs WER; Telugu WER/CER ratio ~3.7x in BuzzASR table: 32.29/8.64).
- Whisper large-v3 for Telugu should be excluded as a baseline except to document its failure (script collapse, WER >100).

### Gaps
- Qwen3-ASR Telugu: not supported (Table 1, 30 languages), so no number.
- No published IndicConformer IndicVoices per-language test WER found (AI4Bharat card only gives Vaani Hindi 13.2; Sarvam gives aggregate only).
- Whisper large-v3 / turbo official FLEURS hi/te WER: Whisper paper table could not be extracted (PDF); only third-party numbers above.
- Omnilingual per-language CER test set definition and CTC (non-LLM) hi/te numbers: CSV covers only 7B LLM-ASR; paper PDF unreadable via tool.
- Streaming Indic ASR with offline counterpart from the same checkpoint: not found. SraVaani paper streaming section not read (HTML did not include it). IndicConformer has no published streaming variant.
- Vaani models' own numbers on Telugu; Parakeet-TDT-v3 per-language details; Moonshine official language list; Kyutai Indian-English numbers; Saaras v4 numeric results (post text has no scores).
- Telugu-English code-switch baselines: none found for any model.

---

## 3. Text normalization for WER (NFC, nukta, anusvara/chandrabindu, numerals, punctuation, English-in-Devanagari, Telugu ZWNJ/conjuncts, Whisper vs Indic normalizers, mixed-script metrics, CER vs WER for Telugu)

### Takeaway
Whisper's default non-English normalizer destroys Indic orthography (strips mark-class characters = matras and virama) and artificially lowers WER, so it must not be used for Indic. Published Indic benchmarks mostly normalize minimally (lowercase + punctuation removal) or not at all, and the 2026 trend (Voice of India, Monsoon hi-IN, Vaani V1.0) is multi-reference/lattice scoring (OIWER) to forgive legitimate spelling and English-script variation. Recommended protocol: report strict WER (minimal, documented normalization) AND a lattice/multi-reference or script-normalized WER, plus CER, and a code-switch-token breakdown.

### Cited Findings
- Whisper's multilingual normalizer replaces Unicode mark-class characters with spaces, which removes vowel signs and virama in Indic scripts; METEOR similarity original-vs-normalized: English 0.97, Hindi 0.38, Tamil/Malayalam 0. Whisper-small FLEURS raw WER: Hindi 86.9, Tamil 93.3, Malayalam 287.4; normalization lowered these by 21.9, 41.5, 152.2 points ("suspicious"). Telugu not reported. Authors call for language-specific normalization built with native speakers — [Manohar et al., EMNLP 2024, arXiv 2409.02449](https://arxiv.org/html/2409.02449v4)
- Collabora Hindi fine-tune: Whisper normalization gives 10.11% vs 17.35% with IndicNLP normalization (keeps diacritics) — vendor blog — [Collabora](https://collabora.com/news-and-blog/news-and-events/breaking-language-barriers-fine-tuning-whisper-for-hindi.html)
- Candidate character-level Indic normalizations (from Kunchukuttan's indic-nlp-library): collapse nukta forms to base, canonicalize anusvara / chandrabindu / visarga variants; each changes WER, so state which are applied — [medical-ASR paper, arXiv 2512.17562](https://arxiv.org/pdf/2512.17562)
- Script-Normalized WER (SN-WER, MeLLM 2026): transliterate reference and hypothesis into a canonical script before scoring; reports it narrows inflated model gaps by up to 12% on FLEURS; proposed as a companion score — [SN-WER](https://www.alphaxiv.org/abs/2606.02548.md)
- What published benchmarks do: Vistaar README documents none (only `--do_normalize_eval` flag) — [Vistaar](https://github.com/AI4Bharat/vistaar); SraVaani 1.0 lowercases + removes punctuation, jiwer convention — [arXiv 2608.08235](https://arxiv.org/html/2608.08235); Factors-study removes punctuation, tags and non-verbal artifacts — [arXiv 2606.09335](https://arxiv.org/html/2606.09335); BuzzASR leaves FLEURS transcripts as-is, CV lowercased + punctuation regex, jiwer, greedy — [arXiv 2609.09554](https://arxiv.org/html/2609.09554); Agricultural paper and Vividh describe none — [2602.03868](https://arxiv.org/html/2602.03868v2), [Vividh](https://huggingface.co/blog/adalat-ai/vividh-benchmark); Lahaja: not described; Vaani V1.0: "identical normalisation" for Lahaja comparison only
- OIWER (AI4Bharat-originated, used by Voice of India and Monsoon hi-IN): lattice of validated variants incl. multi-word segmentation variants and optional disfluencies; open-source `voi-oiwer`; flattening lattices to single refs raises error rates unevenly and swaps system ranks — [VoI](https://arxiv.org/html/2604.19151), [HF blog](https://huggingface.co/blog/open-asr-leaderboard-global-south)
- Multi-reference effect (Vaani V1.0, 3 annotators, ten systems): mean WER 24.80 (1 ref) -> 19.66 (2) -> 17.76 (3); Approach 3 counts a word correct if it matches under any reference alignment — [Vaani V1.0](https://arxiv.org/html/2606.21408)
- Code-switch scoring: conventional WER is inflated by script ambiguity of English words (Devanagari vs Latin); transliteration-based metrics toWER / T-WER (English reference word counts correct in English or transliterated Devanagari form): Hindi-English MUCS blind set standard WER ~26.5 vs T-WER ~25.3 (modest) — [Indic code-switch paper, arXiv 2203.16578](https://arxiv.org/pdf/2203.16578); across metric benchmarking, best human-correlation came from transliteration followed by text normalization (Arabic/English study, not Hindi) — [arXiv 2211.16319](https://arxiv.org/pdf/2211.16319)
- MER (mixed error rate: WER on word-segmented languages + CER on character languages) only applies to pairs with character-based scripts and does not address Devanagari/Latin ambiguity (Deepgram guide, vendor) — [Deepgram](https://deepgram.com/learn/what-is-code-switching-asr-guide)
- Vaani V1.0 tags English tokens: Shrutam-HindiASR-1.0 error rate on code-switched tokens 28.3 vs 12.8 on others (+15.6), Google Chirp 3 12.8 vs 10.2 (+2.6); all systems worse on CS tokens — [Vaani V1.0](https://arxiv.org/html/2606.21408)
- Whisper tends to output English words in Devanagari (anecdotal blog) — [Trelis Tara card](https://huggingface.co/Trelis/tara) (vendor; custom Devanagari normalizer)
- Telugu CER vs WER: Omni-7B Telugu WER 32.29 vs CER 8.64; BuzzASR FFT Telugu WER 45.49 vs CER 13.03 (ratio 3.5-3.7x) — [BuzzASR](https://arxiv.org/html/2609.09554). Agglutinative-language effect on WER is expected; see inference.
- Numerals: no source examined Devanagari digits vs ASCII vs spelled-out handling; Menta's entity metric uses per-class normalization for phone numbers, amounts — [Menta](https://arxiv.org/html/2605.03073)

### Inferences (recommended protocol, my synthesis)
1. Unicode: NFC (not NFKC for Telugu/Devanagari without checking: NFKC can alter some forms); remove ZWJ/ZWNJ/ZWSP (or map ZWNJ to nothing in both ref and hyp) — Telugu ZWNJ/conjunct-variant behavior was not found in any source; test empirically on your data and freeze the rule list.
2. Never use Whisper's BasicTextNormalizer/EnglishTextNormalizer for hi/te. Apply a documented minimal pipeline: NFC, strip punctuation (keep marks!), lowercase Latin, collapse whitespace, remove annotator tags/disfluency markers, optional nukta-folding (ड़->ड, ज़->ज) and chandrabindu/anusvara canonicalization applied identically to both sides, digits mapped to one form (ASCII) via a fixed table, and report results with and without the optional folds.
3. Report four numbers per slice: strict WER (minimal norm), lattice/multi-reference WER (OIWER via `voi-oiwer` for Hindi; build 2-3 references for a subset for Telugu), CER, and WER on code-switch tokens vs native tokens (with transliterated-equivalence for English words: T-WER or SN-WER style, using a Latin<->Devanagari/Telugu transliteration table for the English lexicon in the test set).
4. Decide an output policy for English words in Hindi/Telugu code-switch (native script vs Latin) and make the reference lattice accept both; otherwise Hindi WER can be artificially inflated by script choice alone.
5. For Telugu, headline CER next to WER and consider treating WER as insensitive to near-miss agglutinated forms; publish both.
6. Publish a normalization spec file (versioned, hashed) with the evaluation code, and re-run all baselines through the exact same code; never mix numbers normalized differently.

### Gaps
- No source on Telugu-specific ZWNJ / conjunct (e.g., consonant clusters, virama sequences) normalization, nor on Devanagari digit vs ASCII handling in published benchmarks.
- Exact normalization steps in the AI4Bharat IndicVoices/IndicASR eval and the `indic-nlp-library` normalizer behaviors were not read directly.
- The numbers on SN-WER and OIWER agreement with human judgments were not reviewed beyond abstracts.

---

## 4. Streaming metrics and tooling (first-token latency, finalization latency, average lag, RTF, WER vs chunk-size curve, endpoint accuracy; NeMo scripts, sherpa-onnx, SimulEval, WhisperLive; edge metrics)

### Takeaway
Define latency against forced-alignment word boundaries and report P50/P90 for first-token emission delay, finalization latency (end-of-speech to final text), and endpointing delay paired with a false-cutoff rate, with RTF measured both paced and unpaced; sweep chunk size/look-ahead to produce WER-vs-latency curves. I found no authoritative sherpa-onnx or NeMo doc that defines these metrics, and nothing for SimulEval/WhisperLive in an ASR-only streaming context, so the harness must be defined and published by the team.

### Cited Findings
- First-token emission delay = time from true speech onset (ignoring leading silence) to the first non-blank token; P50/P90 across utterances; user-perceived latency measured separately; computation metrics (FLOPs, RTF) are not strongly correlated with user-perceived latency — [Dissecting user-perceived latency of on-device E2E ASR](https://ar5iv.labs.arxiv.org/html/2104.02207)
- Ground-truth boundaries via forced alignment (Montreal Forced Aligner); for chunk models token timestamps equal chunk end time, so latency is inflated unless corrected — same source
- Finalization latency = gap from end of turn/speech to final transcript; endpointing is separate from VAD; evaluate endpoint delay together with false-cutoff rate and interruption rate — [AssemblyAI voice-agent evaluation guide](https://www.assemblyai.com/docs/streaming/evaluations/voice-agents.md) (vendor)
- RTF: report paced and unpaced; disable built-in endpointing (`enable_endpoint_detection=False`) and use greedy search when isolating model finalization on sherpa-onnx int8 on a 6-core CPU — [Softcery Nemotron-on-CPU write-up](https://softcery.com/lab/hosting-nemotron-asr-streaming-on-a-cpu) (numbers not retrieved)
- Chunk/look-ahead sweeps: Nemotron-3.5 modes 80/160/320/560/1120 ms via `att_context_size` (e.g. `[56,0]`=80 ms, `[56,13]`=1.12 s) — [card](https://huggingface.co/nvidia/nemotron-3.5-asr-streaming-0.6b); SraVaani-0.5-live `[70,13]`=1.12 s chunk/1040 ms lookahead, `[70,6]`=0.56 s/480 ms (recommended balance), `[70,1]`=0.16 s/80 ms, `[70,0]`=0.08 s/0 ms — [card](https://huggingface.co/ARTPARK-IISc/SraVaani-0.5-live); icefall/sherpa-onnx Zipformer streaming chunks 16/32/64 frames (sherpa-onnx supports only these) — [Korean zipformer card](https://huggingface.co/kangkyu/icefall-asr-ko-streaming-zipformer-174m)
- Whisper-derived streaming systems (Whisper-Streaming, Simul-Whisper, two-pass Whisper) exist as research approaches — [Turning Whisper into real-time](https://arxiv.org/pdf/2307.14743), [Simul-Whisper](https://arxiv.org/pdf/2406.10052), [Two-pass Whisper](https://arxiv.org/pdf/2506.12154)
- Edge measurements to copy: model size (params, int8 file MB: 66.1M/~68 MB int8 Zipformer), RTF on named CPU and thread count (0.035 int8 vs 0.183 fp32, 4-thread Xeon) — [card](https://huggingface.co/Akshatkasera007/STT-streaming-zipformer-indian-en). Omnilingual VRAM/CPU unspecified; Nemotron 3.5 gives GPU stream counts only (H100: 240 streams at 80 ms vs 2,400 at 1.12 s) and offers a C++ GGUF runtime — [wavect review](https://wavect.io/blog/nvidia-nemotron-3-5-asr-production-review.md), [card](https://huggingface.co/nvidia/nemotron-3.5-asr-streaming-0.6b)
- Vendor latency claims to treat as unverified: Saaras v4 time-to-first-token <150 ms — [Saaras v4](https://www.sarvam.ai/blogs/introducing-saaras-v4); another vendor "24 ms median TTFT" without method (search summary only)
- Nemotron reviewers note FLEURS results are "not proof for accented 8 kHz calls, cross-talk, product names, addresses" — [wavect review](https://wavect.io/blog/nvidia-nemotron-3-5-asr-production-review.md)

### Inferences
- Minimum streaming report per model/config: (a) WER/CER at each chunk (e.g. 160/320/640/1280 ms) and offline; (b) first-token delay P50/P90; (c) finalization latency P50/P90 after VAD-end; (d) endpoint false-cutoff and miss rates with fixed silence thresholds; (e) token revision rate (partial hypothesis instability / flicker); (f) RTF paced and unpaced at 1, 2, 4 threads on the lowest target laptop CPU (name the CPU, OS, power mode); (g) peak RSS, steady-state RSS, model size on disk (fp32/int8), cold-start load time, CPU utilization %.
- Use identical audio, forced-alignment reference timestamps, and endpointing settings across sherpa-onnx and any NeMo baselines; scoring script should live in repo and be unit-tested.
- Average lag (SimulEval-style AL) is mainly a translation metric; for ASR, per-word emission delay vs aligned word end is the more interpretable analogue.

### Gaps
- No sherpa-onnx benchmark documentation, NeMo streaming eval script documentation, SimulEval-for-ASR, or WhisperLive metric definitions were retrieved.
- No laptop-CPU RTF/RAM numbers for any Hindi/Telugu model (IndicConformer, SraVaani-live, Nemotron-3.5 CPU) found; SraVaani-live card only says "runs in real time on CPU".
- Endpoint-accuracy benchmarks for Indic languages: none found.

---

## 5. Robustness slices and building a cheap in-house test set (noise/SNR, far-field, 8 kHz telephony, dialects, rate, entities, numbers, CS density; sizing, annotation, IAA; synthetic TTS limits)

### Takeaway
Published studies show which slices matter most: spontaneous/conversational vs read speech (largest gap), telephony/low-bit codecs (GSM worst), competing background speech, speaker L1 accent (Lahaja), named entities, and code-switched tokens. Credible precedents for in-house set size are 1.3-12.5 h (Monsoon hi-IN public 1.33 h; Svarah 9.6 h; Lahaja 12.5 h; Vaani V1.0 10.9 h), so 2-5 h per language per slice family is defensible when paired with multi-reference scoring and speaker-clustered confidence intervals. TTS synthetic sets are useful for entities/numbers but have documented limits.

### Cited Findings
- Read vs conversational gap: Google STT Hindi 14.3% (Kathbath read) vs 59.9% (GramVaani) in Vistaar — [Vistaar](https://github.com/AI4Bharat/vistaar); Nemotron Hindi 6.8 (FLEURS) vs 20.2 (Vaani) — [card](https://huggingface.co/nvidia/nemotron-3.5-asr-streaming-0.6b); Agricultural field audio: best Hindi 16.2, best Telugu 33.2 — [2602.03868](https://arxiv.org/html/2602.03868v2); Vividh: fine-tuning on spontaneous Tier C improved C but regressed Tier B broadcast (32.43 -> 43.12), so report per tier, not just global — [Vividh](https://huggingface.co/blog/adalat-ai/vividh-benchmark)
- Controlled degradations on Hindi (Indic Conformer, Whisper-large-v3-based, Voxtral, Shrutam): GSM (2G) codec worst; narrowband (3G)/wideband (4G) near original; Opus marginal; 8-bit amplitude and below degrades sharply; competing background speech causes strongest noise degradation; Whisper-based models more robust than Conformer-based to noise; neural super-resolution (VoiceFixer, AudioSR) increased WER; speaking-rate effect non-monotonic and language dependent (Hindi WER decreases with higher rate; other languages degrade); very short utterances worse — [Factors affecting ASR performance, arXiv 2606.09335](https://arxiv.org/html/2606.09335)
- Accent: Lahaja best model 10.5 (Urdu/Sindhi L1 speakers) to 20.5 (Assamese L1); error increases from Central/West toward North-East/South India; named entities worst — [Lahaja](https://arxiv.org/html/2408.11440v1). Monsoon en-IN: by zone, Voxtral varies 1.68 WER across zones (Central 4.38, East 6.06), Whisper-turbo 0.46; worst zone differs per model — [HF blog](https://huggingface.co/blog/open-asr-leaderboard-global-south). No Telangana-vs-Andhra Telugu dialect benchmark found.
- Vaani V1.0 slices to copy: gender balance (536 M/526 F), age 20-70, 567 PIN codes, SNR bands via DNS64, recording device, noise-event categories; reports no dialect-specific WER — [Vaani V1.0](https://arxiv.org/html/2606.21408)
- Annotation process precedent (Monsoon): LLM-generated topic prompts reviewed by native linguists; automatic checks for language, gender, spontaneity, signal quality; seed transcripts from internal ASR; five-level native-linguist correction with independent verification at each level; informed consent and paid contributors — [HF blog](https://huggingface.co/blog/open-asr-leaderboard-global-south)
- Multi-reference: three independent transcriptions per utterance (Vaani V1.0) reduce average WER by 7 points vs one reference — [Vaani V1.0](https://arxiv.org/html/2606.21408)
- Synthetic TTS test/training sets: ~22,000 entity-dense utterances for <$50 using multiple open TTS systems; entity-hit-rate (EHR) metric; LoRA on that data raised Telugu EHR 0.027 -> 0.473 and generalised to a 20-utterance single-speaker native check (0.516), but regressed read-prose FLEURS-Te WER by +6.6 pp, all pre-registered EHR targets were missed, holdouts were n=86-102, no bootstrap CIs — [Menta, arXiv 2605.03073](https://arxiv.org/html/2605.03073). CS-FLEURS uses generative TTS for part of its code-switch test sets — [CS-FLEURS](https://arxiv.org/pdf/2509.14161)
- Code-switching at 8 kHz telephony degrades models with unified vocab (vendor hypothesis) — [Gnani.ai](https://gnani.ai/resources/research/code-switching-at-8khz)

### Inferences (recommended in-house set design)
- Size: per language, 3-5 h split as ~40% spontaneous/conversational (2+ speakers, own phones), ~20% telephony 8 kHz (codec-processed from the same utterances: GSM/AMR-NB/Opus), ~15% read named-entity/number prompts, ~15% code-switch (stratify by density: <10%, 10-30%, >30% foreign tokens), ~10% noisy/far-field. 3-5 h is ~1,500-3,500 utterances / ~20-45k words; the naive word-level standard error at 20% WER is about 0.2-0.3 abs, but speaker/clip clustering makes real CIs ~2-3x wider; use speaker-level bootstrap and report CIs. Aim for >=60-100 speakers per language, balanced gender/age, >=2 dialect regions (Telangana vs Andhra/Rayalaseema; Hindi belt: Delhi/UP/Bihar/Rajasthan/MP plus L1-Telugu/Tamil/Bengali speakers).
- Annotation: native-script transcripts, explicit guideline on English words (write in Latin, or native, per frozen policy), numbers (words vs digits), disfluency tags, non-speech tags; first-pass from an ASR model then correct (as Monsoon); double-annotate >=100% of the 1-1.5 h "gold" core and 20% of the remainder; report IAA as inter-annotator WER/CER (annotator A vs B treated as ref/hyp) and token-level kappa on code-switch language tags; target inter-annotator WER <=5% on read, <=10% on spontaneous; keep multiple references on the gold core and score with lattice/any-match (OIWER-style).
- Ethics/legal: consented, paid, own-recorded data owned by the team gives a contamination-free, license-clean test set; keep it private (never train on it; hash and escrow audio; use a held-back second split so you can retire the dev split).
- TTS limits: use synthetic audio ONLY for entity/number/CS-lexicon stress tests and for regression of specific failure modes, not for headline accuracy; expect optimistic acoustics (clean, single prosody, no disfluencies, no real accent variation), phoneme errors for Telugu/Hindi TTS, and training-test leakage if the same TTS generated training data; report synthetic and human-recorded results separately.

### Gaps
- No Telangana-vs-Andhra or Hindi-belt dialect WER studies found; no published far-field Indic benchmark; no source on recommended annotator-agreement thresholds for Indic ASR transcripts (the targets above are my proposals).
- Costs per hour of Indic transcription/recording not sourced.

---

## 6. Go/no-go gating: realistic targets for MVP vs production, regression suite, contamination, Whisper hallucination

### Takeaway
Set gates RELATIVE to named open baselines re-run in the team's own harness (IndicConformer-600M offline and SraVaani-0.5-live / Nemotron-3.5 streaming for Hindi) plus absolute floors derived from the published numbers: the team's small int8 streaming model should realistically land near today's published streaming models (Hindi ~18-25% and Telugu ~30-40% on mixed public sets; English-IN ~20-28% on Svarah for a 66M model, improvable to ~10-15% with more data), not near the 13/26 offline SOTA. Contamination and in-domain training make most headline numbers optimistic; the held-out in-house set is the trust anchor.

### Cited Findings
- Anchors for achievable small streaming accuracy: 64.6M Hindi/Hinglish Zipformer 25.7% on IndicVoices-hi from ~337 h (vs 37.2% from ~89 h) — [card](https://huggingface.co/Vengadanathan/hindi-hinglish-zipformer-ctc-streaming); 430M SraVaani-0.5-live Hindi 18-22 / Telugu 30-35 — [card](https://huggingface.co/ARTPARK-IISc/SraVaani-0.5-live); 66M Indian-English Zipformer 20.7-28.0% Svarah (277 h NPTEL) — [card](https://huggingface.co/Akshatkasera007/STT-streaming-zipformer-indian-en); offline English Whisper large Svarah 7.2, Monsoon en-IN open models ~4.8-5.0 — [Svarah](https://arxiv.org/pdf/2305.15760), [HF blog](https://huggingface.co/blog/open-asr-leaderboard-global-south)
- Contamination / in-domain risks (documented): IndicWhisper is trained on Vistaar training splits of the same datasets it is benchmarked on — [Vistaar](https://github.com/AI4Bharat/vistaar); Nemotron-3.5 training data includes FLEURS and Common Voice (train splits) while FLEURS is its headline Hindi number — [card](https://huggingface.co/nvidia/nemotron-3.5-asr-streaming-0.6b); SraVaani-1.0 uses VAANI and RESPIN as both fine-tuning sources and evaluation benchmarks (authors acknowledge same underlying dataset) — [arXiv 2608.08235](https://arxiv.org/html/2608.08235); Hindi/Hinglish Zipformer trains on 8.4 h of Svarah and reports Svarah WER — [card](https://huggingface.co/Vengadanathan/hindi-hinglish-zipformer-ctc-streaming); Lahaja authors' IndicASR M3 trained on Vistaar + SPRING-INX + IndicVoices — [Lahaja](https://arxiv.org/html/2408.11440v1)
- I found no audit of overlap between Kathbath/IndicVoices test data and public model training sets; general ASR-LLM contamination work shows leakage is not necessarily visible in WER — [Evaluation of LLMs in Speech is Often Flawed](https://arxiv.org/pdf/2505.22251)
- Whisper failure modes in Indic: Telugu "incoherent" (excluded) and Odia WER 125.6% in agricultural benchmark — [2602.03868](https://arxiv.org/html/2602.03868v2); Telugu script collapse SFR 0.46-0.71 and Script Fidelity Rate metric — [Menta](https://arxiv.org/html/2605.03073); Telugu Whisper WER 101-122 and Malayalam 287% raw — [BuzzASR](https://arxiv.org/html/2609.09554), [Manohar](https://arxiv.org/html/2409.02449v4); AssemblyAI Universal Telugu OIWER 105 and GPT-4o-transcribe Hindi 33.9 on VoI — [VoI](https://arxiv.org/html/2604.19151). Insertion-driven WER >100 is the hallucination signature.
- Benchmark rank fragility and the need for several test sets: Vistaar finding above; Vividh per-tier regression; Monsoon: single-reference vs lattice scoring swaps system ranks — [HF blog](https://huggingface.co/blog/open-asr-leaderboard-global-south)

### Inferences (proposed gates — these are my proposals, not published figures)
Scored on the in-house private set with the Section 3 protocol (strict WER; OIWER/multi-ref in brackets), streaming at <=640 ms chunk, int8, single model on a stated laptop CPU:

| Slice | MVP gate (ship to design partners) | Production gate (GA) | Rationale/anchor |
|---|---|---|---|
| Hindi, clean/read (Kathbath/FLEURS-style) | <=18 WER | <=12 WER | IndicConformer 13.8 mean offline; Nemotron streaming 6.8-8.1 FLEURS (in-domain); SraVaani-live 18-22 |
| Hindi spontaneous (Vaani V1.0 / IndicVoices-hi / in-house) | <=28 strict (<=20 multi-ref) | <=20 strict (<=14 multi-ref) | IndicConformer 20.0 single-ref / 13.1 multi-ref; Nemotron 20.2; hybrid-zipformer 25.7 on IndicVoices-hi |
| Telugu, clean/read (Kathbath/FLEURS-te) | <=32 WER (<=10 CER) | <=24 WER (<=7 CER) | IndicWhisper 25.0-25.4; IndicConformer 26.4 mean; SraVaani-live 30-35 |
| Telugu spontaneous / telephony (IndicVoices-te, VoI-style) | <=40 strict | <=28 strict | VoI IndicConformer 23.7 OIWER; Agricultural best 33.2 |
| English-IN (Svarah / Monsoon en-IN) | <=15 WER | <=9 WER | Whisper large 7.2 Svarah, ~4.8-5.0 Monsoon; small streaming 20.7-28 |
| Code-switch (Hi-En; Te-En in-house) | no worse than +8 abs (MVP) vs same model on monolingual spontaneous; transliteration-invariant WER reported | within +4 abs; CS-token WER <=1.6x native-token WER | Vaani V1.0: CS-token penalty +2.6 (Chirp 3) to +15.6 abs; no Te-En baseline exists |
| Relative gate (all slices) | <=1.3x the WER of IndicConformer-600M offline and <=1.15x of the best open streaming baseline run in-house | <=1.15x offline IndicConformer; parity with best open streaming | Streaming penalty +15-25% rel. is the expected floor |
| Robustness | 8 kHz telephony WER <=1.6x clean; SNR 10 dB <=1.5x clean | <=1.3x and <=1.25x | Factors-study: GSM worst, competing speech worst |
| Hallucination/stability | insertion rate <=3%, no output >1.2x reference length on non-speech/silence clips; script-fidelity >=0.98 | insertion <=1.5%, SFR >=0.995 | Whisper Indic failure modes above |
| Edge | RTF<=0.5 (unpaced, 1 thread) on target laptop; peak RSS <=1.5 GB; first-token P90 <=800 ms | RTF<=0.3; RSS <=1 GB; first-token P90 <=500 ms; finalization P90 <=300 ms after endpoint | no published laptop-CPU Indic numbers; Zipformer-66M int8 RTF 0.035 on 4-thread Xeon sets a feasibility ceiling for small models |

- Go/no-go rule suggestion: MVP = all Hindi + English slices pass AND Telugu within +10% of gate AND hallucination/edge gates pass; production adds Telugu, code-switch, and telephony slices. No-go if the gap to the relative baseline widens by more than X (e.g. >5% rel.) between releases on any slice (regression gate) or if results rely on any test set overlapping the training manifest (hash/duplicate check on audio fingerprints and normalized transcripts).
- Regression suite: (1) frozen private in-house set (versioned, per slice); (2) public sanity sets: Kathbath test (read), FLEURS hi/te (read), IndicVoices test/valid (spontaneous), Vaani-V1.0 (multi-ref Hindi), Svarah + Monsoon en-IN, Lahaja (accent, Hindi), MUCS Hi-En (CS); (3) synthetic entity/number set (separate reporting); (4) adversarial: silence/music/noise-only clips for hallucination, 1-3 s utterances, long (>60 s) streams for drift/memory leaks; (5) latency harness on target hardware; (6) per-slice dashboards with bootstrap CIs and a paired-bootstrap test vs previous release.
- Contamination protocol: audio-fingerprint and transcript n-gram de-dup of the training manifest against every public test set; train only on train splits; remember model-card "in-domain" caveats when comparing against baselines (IndicWhisper, Nemotron FLEURS, SraVaani VAANI/RESPIN); prefer out-of-domain sets (Vaani V1.0, Lahaja, Svarah, Monsoon, in-house) for headline claims.

### Gaps
- No published absolute thresholds for hallucination metrics on Indic; the insertion-rate/SFR gates above are my proposals, informed by the observed failure modes.
- Costs/effort to reach the proposed gates (training hours needed) not sourced; Hindi-Hinglish Zipformer shows 89 h -> 337 h improves IndicVoices-hi 37.2 -> 25.7, but scaling to Telugu is unmeasured.

---

## Key question A. What do the best open models hit today (offline) on Telugu and Hindi, and what degradation when going streaming + small + int8?

### Takeaway
Best open offline: Hindi 13-14% WER and Telugu 25-26% WER on mixed public test sets (IndicConformer-600M, SraVaani-1.0); on harder telephony conversation OIWER 8.2 / 23.7 (IndicConformer); Telugu is ~2x harder. Streaming cache-aware at ~0.5-1 s costs about +15-25% relative (published Hindi streaming: SraVaani-live 18-19 / 30-31; Nemotron FLEURS 6.8-7.1 but in-domain), and zero-look-ahead costs more; small (60-70M) models trained on a few hundred hours reach ~25-45% on Hindi spontaneous/Hinglish and ~21-28% on Svarah, so combined degradation vs offline SOTA is roughly 1.5-2x in WER terms.

### Cited Findings
See Section 2 master table and streaming evidence. Key sources: [SraVaani 1.0](https://arxiv.org/html/2608.08235), [SraVaani-0.5-live](https://huggingface.co/ARTPARK-IISc/SraVaani-0.5-live), [VoI](https://arxiv.org/html/2604.19151), [Nemotron-3.5 card](https://huggingface.co/nvidia/nemotron-3.5-asr-streaming-0.6b), [Hindi/Hinglish Zipformer](https://huggingface.co/Vengadanathan/hindi-hinglish-zipformer-ctc-streaming), [Indian-English Zipformer](https://huggingface.co/Akshatkasera007/STT-streaming-zipformer-indian-en)

### Inferences
- Int8 quantization penalty for Indic is unmeasured in public sources (the only int8-vs-fp32 pair is confounded by decoding method); plan to measure and budget +3-10% relative.

### Gaps
- Controlled same-checkpoint offline vs streaming vs int8 numbers on Hindi/Telugu: not found.

## Key question B. What target is realistic for the team's model?

### Takeaway
See the gate table in Section 6: the team should expect to match the published small streaming models first (Hindi ~18-25 / Telugu ~30-40 on spontaneous-mixed public sets, English-IN ~15-28), and aim for ~1.15-1.3x offline IndicConformer by production. Code-switch (especially Telugu-English) has no public baseline, so the in-house set defines it.

### Cited Findings
Anchors listed in Section 6: [SraVaani-live](https://huggingface.co/ARTPARK-IISc/SraVaani-0.5-live), [Hindi/Hinglish Zipformer](https://huggingface.co/Vengadanathan/hindi-hinglish-zipformer-ctc-streaming), [IndicConformer in SraVaani paper](https://arxiv.org/html/2608.08235).

### Inferences
- Targets are proposals; validate by running the three open baselines on the in-house set in week 1 before fixing thresholds.

### Gaps
- No evidence on what accuracy ~100-300M-param int8 streaming models achieve on Telugu with open-only data.

## Key question C. What evaluation protocol would make the seniors trust the results?

### Takeaway
A pre-registered protocol: frozen, private, speaker-disjoint in-house set with multi-reference gold core; strict + lattice/multi-ref + CER + code-switch-token metrics under one versioned normalizer; baselines re-run by the team (not copied from papers) on identical audio; per-slice bootstrap CIs; contamination checks; latency/edge numbers on named hardware; and public sets reported for comparability but never as the headline.

### Cited Findings
Supporting methodology precedents: multi-reference scoring ([Vaani V1.0](https://arxiv.org/html/2606.21408)), OIWER and private-split submission ([HF blog](https://huggingface.co/blog/open-asr-leaderboard-global-south)), normalization pitfalls ([Manohar et al.](https://arxiv.org/html/2409.02449v4)), per-tier reporting ([Vividh](https://huggingface.co/blog/adalat-ai/vividh-benchmark)), pre-registered targets and honest limitation reporting ([Menta](https://arxiv.org/html/2605.03073)), in-domain/contamination caveats ([SraVaani 1.0](https://arxiv.org/html/2608.08235)).

### Inferences
- Publish the evaluation harness (normalizer spec hash, scoring scripts, baseline configs) and have a second engineer reproduce one baseline number to within 0.2 abs WER before sign-off.

### Gaps
- Org-specific acceptance criteria and who owns the private set are outside the sources.
