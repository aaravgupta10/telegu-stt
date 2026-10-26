# Dataset discovery and per-language inventory (Hindi, Telugu, English-India): newly found sources, commercial-safe hours, code-switch, unlabeled pools, TTS

Date-stamp: all pages fetched 2026-10-12 (read-only: no downloads, no logins, no forms, no contact). Not legal advice; tiers are engineering risk tiers.
Evidence labels: [M] read on the cited page, [V] vendor/owner claim, [E] my estimate/arithmetic, [U] unverified or could not be read, [EARLIER] number taken from `research_notes/Edge streaming Indic STT pipeline/datasets_licenses.md` (fetched 2026-10-08; not re-verified here; another team is re-auditing).
Tier legend (same as earlier notes): T1 clearly safe, T2 caveats, T3 unresolved, T4 unusable for commercial training.

Process note: the file `skills/deep-research/references/researcher.md` named in the brief does not exist at the given path (and a glob of that skills folder found nothing), so I followed the brief's own method (HF API sweeps, arXiv/NeurIPS, AIKosh, OpenSLR, Mozilla Data Collective, vendor pages) directly.

---

## 0. Headline findings (read this first)

1. **Telugu is much less binding than the earlier notes said, but only for READ speech.** Two sources not in the earlier notes add large CC-BY Telugu read-speech pools: **RESPIN-S1.0** (IISc SPIRE; Telugu train clean 1,021 h, 1,335 h incl. noisy/semi-noisy; AIKosh licence CC BY 4.0) and **Numo Indic Speech** (Poseidon AI, created 2026-10-02; Telugu 1,224.2 h; CC BY 4.0 on the card). Spontaneous/conversational Telugu with clear T1 status is still ~0.66 k h (IndicVoices + Vaani, [EARLIER]).
2. **Hindi is not a constraint**: ~1.9 k (strict) to ~5 k h (all CC-BY read pools) of transcribed T1/T1-lean hours.
3. **Indian-accented English transcribed and clearly safe is still tiny (~0.05-0.35 k h).** The only big pool is **NPTEL2020 Indian-English (15,700 h, YouTube-Creative-Commons lectures with uploaded subtitles)**, which is T2 (YouTube CC provenance, transcripts assumed-not-verified). SPIRE-SIES (170.8 h Indian English, IISc) is request-form only with licence unstated.
4. **Code-switch**: still no large clearly commercial-safe real corpus for either pair. Telugu-English: the 243 h set in Microsoft Research's 2020 paper is not released; the "200 h / 400 speakers" corpus on a DeepLearning.AI forum cannot be traced to any paper or owner. Hindi-English: only HiACC (5.24 h, CC BY 4.0, Zenodo) is newly found and clearly licensed; SLR104 (89.9 h, BY-SA) is the only sizeable one.
5. **Licence labels on aggregator/vendor-sample HF pages are unreliable** (examples in Section 5). Several large "open" HF corpora with an Apache/CC-BY tag are scraped or are samples of paid catalogues.
6. **Paid route price signals**: SpeechData.ai lists Hindi 2,000 h and Telugu 500 h conversational, signed commercial consent, **$65 per hour** [V]. At that price even 100 h costs ~$6.5 k, which is outside a few-hundred-dollar budget, so open data is the only path.

---

## 1. Newly discovered datasets (not in the earlier notes)

Columns: name / owner / date / languages and transcribed hours / style / licence verbatim and where / gate / provenance and consent / tier / usefulness. "Mono" = per-language monolingual training; "CS" = code-switch.

### 1A. Candidates that materially change the numbers

**RESPIN-S1.0** (IISc SPIRE Lab; Gates Foundation funded; collected with Navana Tech)
- URL: https://aikosh.indiaai.gov.in/home/datasets/details/iisc_respin_s1_0_corpus.html ; project/download form https://spiredatasets.ee.iisc.ac.in/respincorpus ; NeurIPS 2025 D&B paper https://papers.neurips.cc/paper_files/paper/2025/hash/d88714d4f2c1e826d33d6c1eb1497ec9-Abstract-Datasets_and_Benchmarks_Track.html
- Date: AIKosh upload stamp 18/06/25 [M]; NeurIPS 2025. 9 languages incl. Hindi and Telugu; >10,000 h validated, 38+ dialects, agriculture and finance sentence domains, crowdsourced mobile app, 16 kHz mono WAV [M].
- Hours (Hindi, Telugu): the AIKosh/abstract pages give no per-language hours [M]. A README copy found in the shared scratchpad (a sibling agent's fetch; I could not re-fetch the original URL, so treat as [U-source]) lists, in hours: Hindi train clean 712.61, semi-noisy 273.27, noisy 304.55, small 128.47; Telugu train clean 1,021.16, semi-noisy 186.10, noisy 127.66, small 155.89; dev/test ~2-3 h each; README total 12,652:50:00 h across 9 languages. Whether "small" overlaps "clean" is not stated. Telugu 2,287 speakers (1,819 re-speakers), Hindi 2,305 speakers.
- Dialects: Hindi D1-D5 = UP (Muzaffarnagar, Etah, Hamirpur), Rajasthan (Nagaur), Uttarakhand (Garhwali); Telugu D1-D4 = Guntur/Krishna, Chittoor/Anantapur, Karimnagar/Nalgonda, Srikakulam/Visakhapatnam [M, AIKosh].
- Style: READ speech of prompts written by native speakers and domain experts per pincode region; not spontaneous.
- Licence: "Attribution 4.0 International (CC BY- 4.0)" on AIKosh, Visibility "Open", "Hosted" [M]. The NeurIPS abstract page states no licence [M]. The SPIRE download page requires a form (content not visible to me) [U]. Third-party HF mirror `rimrafadii/respin-iisc` (test split only) also tags cc-by-4.0 [M].
- Consent: crowdsourced paid-app collection; ethics/consent statement not read (paper PDF not retrievable) [U].
- Tier: **T1-lean (provisional)**: needs the SPIRE form's terms captured with date and a read of the paper's ethics section. Mono: very useful for acoustic/lexical coverage in Hi and Te dialects, domain-narrow (agri/finance). CS: none.
- Contact path (do not contact): contact.respin@iisc.ac.in (from search summary) [U]; Telugu community post mentions RESPIN speaker recruitment.

**Numo Indic Speech** (Poseidon AI, Inc.; HF `psdn-ai/numo-indic-speech`)
- URL: https://huggingface.co/datasets/psdn-ai/numo-indic-speech ; created 2026-10-02T06:43:41Z, last modified 2026-10-02 [M, HF API]; v1.0, 2026.
- Languages/hours [M]: Hindi 1,314.6 h (101,450 recs), Telugu 1,224.2 h (132,488 recs), Bengali 745.1 h, Tamil 561.6 h; total 3,845.5 h, 1.23 TB.
- Style: scripted single-speaker READ speech with reference prompts (transcripts = the text the speaker read; ASR used only to compute per-recording WER/CER and a synthetic-speech suspicion score). Transcripts keep code-switching and common English terms from the prompts. Full-resolution WAV in Parquet. Speakers: pseudonymous IDs, count not stated.
- Licence: tag `cc-by-4.0`; card text "Numo Indic Speech is released under the CC BY 4.0 license" and credit Poseidon AI, Inc. [M].
- Gate: auto-gated (share contact info; "may contact you about related datasets") [M].
- Provenance/consent: card names no collection tool and describes no consent; Poseidon's site says "Collected with consent, licensed for commercial use" and Numo is a paid-task platform; Poseidon's privacy notice says submitted content "may be licensed to third party AI companies", biometric (voiceprint) use needs separate explicit consent, and public datasets contain anonymised samples [M, psdn.ai and psdn.ai/privacy]. The privacy page does not show a clear explicit step for general recordings being published openly under CC BY (my observation).
- Tier: **T2**. Licence is clear and commercial use explicit, but consent is asserted by the vendor, not documented; voice data is personal data under India's DPDP regime (not researched). Very new (10 days old), no independent audit. Mono: potentially the largest Telugu transcribed pool (read, uncertain speaker diversity). Plausibility check: 1.23 TB / 3,845 h ≈ 320 MB/h, consistent with ~44-48 kHz mono WAV [E].
- Contact path (do not contact): https://www.psdn.ai/contact ("Request dataset"); related sample repo `psdn-ai/telugu-speech-samples` has licence "poseidon-sample-preview" (5 clips, 16 MB) [M].

**SYSPIN_S1.0** (IISc SPIRE; TTS-grade studio corpus)
- URL: https://aikosh.indiaai.gov.in/home/datasets/details/iisc_syspin_s1_0_corpus.html ; https://vaani.iisc.ac.in/dataset/syspindataset
- 9 languages, 1 male + 1 female voice artist each, >47 h per speaker, studio 48 kHz/24-bit; Hindi ~119 h 17 min total (human-checked ~109.9 h; non-checked ~9.4 h), Telugu ~115 h 10 min (HC ~105.7 h; NHC ~9.5 h) [M, AIKosh, my addition of the listed male/female figures]. Date stamp 18/06/25.
- Licence: "Attribution 4.0 International (CC BY- 4.0)" (AIKosh); "CC-BY-4.0 license" (project page) [M]. Terms-and-conditions page linked but not readable [U].
- Tier: **T1-lean**. Read, agri/finance/education/health/sports domains. Mono ASR: small (2 speakers) but clean. Best use: TTS (Section 7).

**Rasa** (AI4Bharat; Interspeech 2024; expressive TTS)
- URL: https://huggingface.co/datasets/ai4bharat/Rasa ; last modified 2026-06-06 [M]. 22 languages, 48 kHz mono; Hindi 50.83 h (F 27.05 + M 23.78), Telugu 52.26 h (F 27.28 + M 24.98) [M]. Licence "CC-BY-4.0", gated [M]. Includes neutral Wikipedia and IndicTTS readings plus six emotions, commands, conversations, news, book narration [M], so the IndicTTS sub-part may inherit IndicTTS terms [U].
- Tier: T1-lean for TTS; for ASR it is acted/emotional speech, 2 speakers per language.

**Rural Women ASR v2** (AI4Bharat, "Recognizing Every Voice")
- URL: https://huggingface.co/datasets/ai4bharat/Rural_Women_ASR_v2 ; modified 2025-11-06. Hindi 30,827 examples (31.4 GB, 48 kHz WAV) and Bhojpuri 33,616 [M, from the card copy in the shared scratchpad]. Read + extempore, human-verified transcripts, mostly female rural speakers in MP/UP/Bihar, collected with the KathBath app. README: "Released under the Creative Commons Attribution 4.0 (CC-BY-4.0) License"; HF API shows no licence tag; v1 (Bhojpuri) is CC BY-SA 4.0 [M].
- Hours not stated; ~90 h Hindi by size [E: 31.4 GB / ~346 MB per hour]. Tier T1-lean, small, useful for demographic diversity. Overlap with IndicVoices unknown [U].

**Chaashini** (Kapture CX; HF `kapturecx/Chaashini`, modified 2026-10-06)
- 2,966.22 h, 33 languages; Hindi 1,394.84 h, English 240.61 h, Telugu 116.25 h; "single-speaker studio-grade"; transcripts produced by "a multilingual Indic ASR system" (not human); audio from "publicly available spoken-word recordings, such as talks, interviews, lectures, and podcasts" [M].
- Licence: "The corpus is released under Apache-2.0 for research and commercial speech-technology development." Gated (share contact info) [M].
- Tier: **T3**. The Apache label cannot grant rights over third-party public recordings that were scraped; ASR pseudo-labels. Do not use for training without provenance ("source_id" only). Useful only as a lead for what kinds of public audio exist.

**bolAIndia** (Kapture CX; HF `kapturecx/bolAIndia`, modified 2026-10-09; 18,890 downloads last month)
- 190.06 k h total (145.07 k transcribed "include human and automated annotations ... does not imply human verification"; 44.98 k untranscribed); Hindi 89.81 k h, Telugu 8.97 k h, English 9.98 k h, 12.89 k h unlabelled language; 12.8 TB [M].
- Licence: NOT stated on the card [M]. Format/filtering/"source credits and usage conditions" are in STATS.md, only readable after login and accepting gate (raw file fetch returned HTTP 401) [M].
- Tier: **T3 (unresolved)**. Largest Hindi/Telugu pool found, but provenance is hidden behind the gate. **Needs the user's browser**: https://huggingface.co/datasets/kapturecx/bolAIndia (files STATS.md, MAP.md after accepting conditions; capture dated text of source credits and usage conditions).

### 1B. Other new Hindi/Telugu/English datasets (smaller or lower tier)

| Dataset | Owner / URL | Hi / Te / En-IN hours | Licence (verbatim, where) | Gate / provenance | Tier | Usefulness |
|---|---|---|---|---|---|---|
| Nirantar (HF copy `shiprocket-ai/nirantar`, orig. AI4Bharat/Nirantar) | AI4Bharat; https://github.com/AI4Bharat/Nirantar ; https://huggingface.co/datasets/shiprocket-ai/nirantar | Hindi 135.50, Telugu 217.69 h (of 2,937 h, 22 langs; HF copy) [M] | HF copy tag `cc-by-4.0`; Zenodo record 11635731 "Creative Commons Attribution 4.0 International" covers only the 3.2 MB manifest zip [M]; GitHub page states no licence [M] | HF copy gated (contact info). Extempore + conversational, human-transcribed; hours originate from the IndicVoices-style collection, likely OVERLAPS IndicVoices [U]; third-party re-upload | T2 | Do not add to IndicVoices counts without dedup |
| Vaani-transcription-part | ARTPARK-IISc; https://huggingface.co/datasets/ARTPARK-IISc/Vaani-transcription-part | Hindi 1,003.78, Telugu 184.48, English 22.46 h (updated 2026-10-08: 2,122.20 h, 86 languages) [M] | `cc-by-4.0` | Gated auto | T1 | Same hours as the Vaani numbers in earlier notes; useful as the transcript-only repo |
| Vaani Atypical Speech / Noise Event / Benchmark V1.0 | ARTPARK-IISc (HF API list) | small; Atypical hi/mr/te; Benchmark Hindi (tags code-switching) | `cc-by-4.0` on all five repos [M] | open/gated | T1 | Noise-event data is a licensed augmentation source; Benchmark = eval |
| Spoken-Tutorial / NPTEL / Mann-ki-Baat / Vanipedia / WordProject / UGCE / SeamlessAlign / IndicVoices-ST (BhasaAnuvaad) | AI4Bharat HF; paper https://arxiv.org/abs/2411.04699 (Nov 2024) | Per paper tables A1/A2 [M]: NPTEL Indic-side speech Hindi 1,433.9 h, Telugu 738.4 h (En-Indic side 3,021.6 / 1,839.9 h); SeamlessAlign Indic-En Hindi 2,355.4, Telugu 873.3 h; Spoken Tutorial Hindi 63.6, Telugu 12.5 h; WordProject Hindi 88.5, Telugu 90.4 h; Mann Ki Baat Hindi 40.9, Telugu 35.3 h; "IndicVoices (synthetic)" Hindi 282.9, Telugu 377.5 h | All HF cards: "This dataset is released under the CC BY 4.0" [M]; the paper says licences "will be" permissive | Gated. This is a SPEECH TRANSLATION set: the text side is translation, not same-language transcript; NPTEL transcripts described only as "transcribed and re-recorded in multiple languages manually" [M]. NPTEL and Spoken Tutorial site licences differ (below) | T3 for ASR | Not a reliable ASR source; SeamlessAlign is mined audio and Meta's Seamless licence text is non-commercial ("solely for Noncommercial Research Uses") [M], so inheritance is a risk |
| Spoken Tutorial (IIT Bombay) licence | https://spoken-tutorial.org (search summary) | - | Site: "created on or before 31 Jan. 2025, by IIT Bombay is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License" [M via search summary]; HF copy says CC BY 4.0 | contradiction | - | Treat as BY-SA (more restrictive) |
| NPTEL licence | search summary of old sources | - | One 2014 article: NPTEL under "Attribution-NonCommercial-ShareAlike"; a slide deck: "CC BY SA"; Labnol: YouTube material "not available under a Creative Commons license" [M via search summary, low quality]; NPTEL's own current terms not read [U] | unresolved | T3 | Any NPTEL-derived set (BhasaAnuvaad, NPTEL2020, Vistaar) inherits this |
| HiACC (Hinglish adult + child) | Singh, Singh, Kadyan; https://zenodo.org/records/15551669 | Hinglish 5.24 h; 3,318 adult + 1,858 child utts [M] | "Creative Commons Attribution 4.0 International", Access "Open" [M] | Open download, 531.6 MB; published 2025-05-30; read + spontaneous + image prompts, manually transcribed with CS tags | T1 | Small but the only clean Hi-En CS with a clear licence |
| Indic DiarBench | Sarvam; https://huggingface.co/datasets/sarvamai/indic-diarbench | covered in earlier notes (10.7 / 9.3 h) | cc-by-4.0 | - | - | eval only |
| Voice of India | Josh Talks + AI4Bharat; https://arxiv.org/abs/2604.19151 | 536 h, 15 languages, telephonic, 36,691 speakers [M via search] | paper calls it closed source; no licence/download found [U] | none | T4 for training | eval benchmark only |
| SPIRE-SIES (Indian English spontaneous) | IISc SPIRE; https://arxiv.org/abs/2312.00698 | En-IN 170.83 h (162.6 h filtered), 1,607 speakers; transcripts only for 23 h and those are Whisper outputs "generated and validated" [M] | corpus licence not stated; only the arXiv paper is CC BY 4.0 [M] | request form https://forms.office.com/r/bF27ah1Fg9 ; image-description speech; paid volunteers; no ethics statement [M] | T3 | Good accent diversity if licensed; ask coordinator whether to request |
| NPTEL2020 Indian-English | AI4Bharat GitHub; https://github.com/AI4Bharat/NPTEL2020-Indian-English-Speech-Dataset ; Zenodo records 4596748 etc. (March 2021) | En-IN **15,700 h** scraped lectures (train ~5M chunks) [M] | GitHub: "Creative Commons" (links to YouTube's CC page); Zenodo test-part2: "Creative Commons Attribution 4.0 International" [M] | Videos selected had manually uploaded subtitles; authors "assume NPTEL has used Google ASR on top of which they have made reasonable amount of corrections" [M]; 1k "Pure Set" manually annotated; scripts crawl YouTube | T2 (lean T3) | Only big Indian-accent English source; labels not verified, domain = STEM lectures |
| Common Voice Scripted 26.0 "South Asian English (India, Pakistan, Sri Lanka)" | Mozilla Data Collective; https://mozilladatacollective.com/datasets?q=india | 3.83 GB MP3, hours not shown [M] | CC0-1.0 [M] | open | T1 | Indian-accent English; counts in earlier notes (~224 h of en-IN clips) [EARLIER] |
| Common Voice Scripted 27.0 Hindi / Telugu | MDC | Hindi 546.57 MB; Telugu 65.47 MB [M] | CC0-1.0 [M] | open | T1 | tiny; consistent with earlier notes (15.7 / 0.94 validated h) |
| Karya "sanmati-stories" | Karya; https://huggingface.co/datasets/karya/sanmati-stories (modified 2026-10-12) | clips (not hours): Hindi 293,337, Telugu 714,985 [M] | "KPL BY-NC-SA-FS 1.0 license" [M] | manual gate; workers get royalties from commercial profits | **T4** | NC |
| Kapture Vartalaap | https://huggingface.co/datasets/kapturecx/Vartalaap | Hinglish, synthetic-tagged | `cc-by-nc-4.0` | gated manual | T4 | NC |
| Humyn Labs Indic High-Fidelity ASR | https://huggingface.co/datasets/humyn-labs/Indic-High-Fidelity-MultiSpeaker-ASR | 37 rows (1.06 GB), 10-30 min each, dual-speaker spontaneous, human transcripts [M] | "Creative Commons Attribution 4.0 International (CC BY 4.0)" [M] | vendor sample; contact support@humynlabs.ai; no consent text | T2 | sample only |
| LiVA AI hindi-english-asr | https://huggingface.co/datasets/liva-ai/hindi-english-asr | 10 clips x 60 s (~10 min) [M] | `cc-by-4.0` tag; no text | vendor teaser; Hi-En CS conversational, 48 kHz | T2 | sample only |
| Sonexis "Hinglish code-switched conversations" | https://huggingface.co/datasets/naradatum/hinglish-code-switched-conversations-v1 | hours not stated (117 MB) | "cc-by-nc-4.0" | gated | T4 | NC sample |
| InfoBayAI Telugu/Hindi call-centre and podcast sets | https://huggingface.co/datasets/InfoBayAI/Telugu-Call-Center-Audio-Dataset-Single-Channel (also Dual, Podcast; Hindi equivalents); contact datareq@infobay.ai (on card) | cards claim 27,787 h (Telugu call centre) and 5,964 h (Telugu podcast) but total sample size is 18.9 MB / 148 MB, "contains only sample data" [M] | tag `cc-by-4.0` BUT card text: "This dataset is provided for research and educational purposes only." and points to "enterprise licensing options" [M] | gated; 8 kHz; "Procured through formal agreements"; PII muted | **T3/T4** | classic tag-vs-text conflict; use stricter reading |
| SpeechData.ai Hindi / Telugu conversational | https://huggingface.co/datasets/SpeechDataAI/telugu-conversational-speech (and hindi-) ; speechdata.ai/datasets/telugu | Telugu 500 h (50 speakers), Hindi 2,000 h (200 speakers) [V] | "speechdata-commercial"; "Commercial, for training and evaluation"; signed commercial-use consent per speaker [V] | audio not hosted; free sample on request with company email; **$65 per hour**, volume discounts [V] | paid T1-like | benchmark for what a paid route costs |
| BharatVani Hindi Speech Corpus | https://huggingface.co/datasets/Sheeba2026/bharatvani-hindi-speech-corpus | 205.3 h studio, verified Devanagari transcripts with word timestamps [V] | "ALL RIGHTS RESERVED. THECREATOR OS / BHARATVANI AI."; proprietary-commercial; paid tiers | manual gate; no provenance/consent stated | T4 unless licensed | |
| Nexdata Telugu 202 h | https://www.nexdata.ai/datasets/speechrecog/1391 | 202 h, 98% word accuracy [V] | "paid dataset licensed for commercial use"; quote only | - | paid | |
| Silencio Indian-languages (complete-voiceai) | HF `SilencioNetwork/*` | catalogue claims in earlier notes | `cc-by-nc-4.0` | - | T4 | [EARLIER] |
| IIITH-CSTD / IIIT-H Telugu challenge database | https://asr.iiit.ac.in/asr_challenge (host unreachable during my fetch; details from search summary) | 2,000.8 h crowdsourced Telugu (spontaneous, conversational, read), TDIL/MeitY pilot, 2022 | Challenge terms: participants "free to use this data for research purposes", training use only [M via search summary] | access outside challenge unknown | **T4 as released** | Largest Telugu corpus found; would need a written licence from IIIT-H/TDIL |
| LDC-IL Telugu corpora | https://data.ldcil.org/speech/telugu-sentence-aligned-speech-corpus-asm | 15.6 h sentence-aligned (80 speakers) [M]; also "Telugu Raw Speech Corpus" | separate "Commercial User Undertaking" and "Non-Commercial User Undertaking" forms; price not shown [M] | form-based | T3 | tiny |
| SpeechOcean / Microsoft Indian corpus mirrors | HF `deepdml/microsoft-speech-corpus-indian` (no licence tag; modified 2026-02-19) | - | original is non-commercial per earlier notes [EARLIER] | **appears inside** the aggregator `projectkaira/Pretraining-V1` (below) | T4 | trap |
| projectkaira / neh7777 / kenpath "Pretraining-V1" | https://huggingface.co/datasets/projectkaira/Pretraining-V1 | 26.3-26.9 k h aggregate: includes Kathbath, Rasa, Shrutilipi, IndicVoices-R, IndicTTS, SYSPIN, SPICOR (Indian English 99.4 h), `msft_indian` (134.9 h Hi/Ta/Te), Common Voice 22 via SIDON [M] | tag cc-by-4.0 "for the aggregation and schema normalization work"; "The underlying audio and text data retain the licenses of their respective sources" [M] | no consent text | T4 as a whole | contains the NC Microsoft corpus; never pull from aggregators |
| agarwalayushi/hinglish | https://huggingface.co/datasets/agarwalayushi/hinglish | "2,264+ h", 815,171 clips from 14 public corpora (521k clips NPTEL Hindi Spoken Tutorial, Kathbath, IndicTTS, CV17...) [M] | "released under Creative Commons Attribution 4.0 International (CC BY 4.0)"; "Each constituent dataset retains its original license" [M] | aggregator; includes BY-SA and unclear sources | T3 | pull from originators instead |
| IndicCMix | AI4Bharat; https://huggingface.co/datasets/ai4bharat/IndicCMix (2026-04-15) | 104k English sentences x 11 Indic languages; audio is SYNTHETIC English (F5-TTS, ~31 GB), text in code-mixed, native, romanised forms [M] | "MIT" [M] | gated | T1-ish (synthetic) | CS TEXT resource for synthetic CS generation, not real speech |
| SPRINGLab/Hindi-1482Hrs | https://huggingface.co/datasets/SPRINGLab/Hindi-1482Hrs | 907,006 rows, 159 GB; name suggests 1,482 h [U] | empty README; no licence | no source corpora named | T3 | do not use until provenance known |
| Praxel codeswitch-pairs-lase | https://huggingface.co/datasets/Praxel/codeswitch-pairs-lase | 1,118 pairs (~37 min) Hi/Te/Ta/En | "CC-BY-4.0" | ElevenLabs Multilingual v2 synthetic speaker-encoder data | T3 for ASR | not usable as ASR data |
| Karya / others NC or tiny | `kapturecx/Vartalaap` NC; `disco-eth/WorldSpeech` NC; `IndicSynth` NC deepfake sets; `Silencio` NC | - | cc-by-nc-4.0 | - | T4 | |
| Common-Voice-derived Hindi/Telugu | `projectkaira` etc. | Hindi 22.7 h, Telugu 2.6 h in cv22_sidon | CC0 upstream | - | T1 | negligible |
| Meta Omnilingual ASR corpus | https://huggingface.co/datasets/facebook/omnilingual-asr-corpus (modified 2025-11-14) | 3,350 h across 348 under-served languages; Hindi/Telugu not seen in the tag list I could read (tag list truncated at 30 of ~348) [U] | `cc-by-4.0`, not gated [M] | spontaneous speech, compensated local partnerships | T1 (licence) | no known Hi/Te/En-IN value |
| Google SVQ | https://huggingface.co/datasets/google/svq | 17 languages / 26 locales, ~700 speakers, eval set; Hindi/Telugu locales not shown on page text [U] | `cc-by-4.0` | evaluation only (create own splits) | T1 | eval (voice queries) |
| FLORAS (ESPnet) | https://huggingface.co/datasets/espnet/floras | ~32,000 h YouTube/YODAS-derived; Hindi included, Telugu not listed [M] | `cc-by-3.0` | YouTube-derived, subtitle provenance unclear | T2 | marginal |

---

## 2. Consolidated inventory table by language and tier

Hours are TRANSCRIBED hours unless marked. Rows tagged [EARLIER] are copied from the earlier notes (not re-verified). Overlaps are NOT double counted: IndicVoices-R, Nirantar, IndicVoices-ST and the Kathbath/Pretraining-V1 re-uploads are excluded from sums.

### Hindi

| Tier | Source | Hours | Style | Basis |
|---|---|---|---|---|
| T1 | IndicVoices | ~790 | extempore/conversational/read | [EARLIER] est. |
| T1 | Vaani | 1,003.78 (paper's fine-tuning subset 593.93) | image-prompted spontaneous, phone | [EARLIER]; HF card re-read today 2,122.2 h total transcribed [M] |
| T1 | SPRING-INX Hindi | 351 | monologue + conversation, code-mixed transcripts | [EARLIER]; AIKosh Hindi page re-read: CC BY 4.0, ~3,400 h across 10 languages [M] |
| T1 | CV 27.0 + FLEURS | ~16 + ~7 | read | [EARLIER] |
| T1-lean | SYSPIN Hindi | ~119 | studio read | new [M] |
| T1-lean | Rasa Hindi | 50.8 | expressive/studio | new [M] |
| T1-lean | Rural Women v2 Hindi | ~90 [E] | read + extempore, rural women | new, CC-BY in README |
| T1 | HiACC (Hinglish) | 5.24 | CS | new [M] |
| T1-lean (provisional) | RESPIN Hindi clean | 712.6 | read, agri/finance | new; hours from README copy [U-source] |
| T2 | RESPIN Hindi semi-noisy + noisy | 273.3 + 304.6 | read | new, same caveat |
| T2 | Numo Hindi | 1,314.6 | read | new [M] |
| T2 | Shrutilipi (AIR) | ~1,620 | broadcast news | [EARLIER] |
| T2 | Kathbath | ~150 (+48 noisy) | read | [EARLIER] |
| T2 | NPTEL (Vistaar usage) | ~157 | lectures | [EARLIER] |
| T2 | YODAS manual | ~481 | YouTube | [EARLIER] |
| T2 (BY-SA) | MUCS SLR104 (Hi-En CS) | 89.9 | lecture, CS | [EARLIER] |
| T2 (BY-SA) | Spoken Tutorial (BhasaAnuvaad Hi side) | 63.6 | lecture | new; transcript type [U] |
| T3 | bolAIndia Hindi | ~89,810 (human+auto labels) | mixed | licence hidden; gated |
| T3 | Chaashini Hindi | 1,394.8 | scraped, ASR labels | Apache tag, scraped audio |
| T3 | BhasaAnuvaad NPTEL Hindi-side | 1,433.9 (translation pairs) | lectures | transcript type unclear |
| T4 | Gram Vaani SLR118, MUCS SLR103, BharatVani, Silencio, Karya, Vartalaap | - | - | NC/proprietary |
| Paid | SpeechData.ai Hindi | 2,000 | conversational, consented | $65/h [V] |

**Hindi clearly commercial-safe transcribed hours (low / best / high):**
- Low **~1.9 k h** = earlier-notes T1 low (IndicVoices + Vaani-filtered + SPRING-INX + CV/FLEURS), no new sources.
- Best **~3.1 k h** = earlier T1 (~2.17 k) + SYSPIN 0.12 + Rasa 0.05 + Rural Women ~0.09 + HiACC 0.005 + RESPIN clean 0.71 [E].
- High **~5.0 k h** = Best + RESPIN semi-noisy/noisy 0.58 + Numo 1.31 [E].
- T1+T2 (add Shrutilipi/Kathbath/NPTEL/YODAS/SLR104 ≈ 2.5 k plus new T2) ≈ 7.5-9 k h.
- Spontaneous/conversational T1 only: ~1.8-2.2 k h (IndicVoices + Vaani + SPRING-INX).

### Telugu

| Tier | Source | Hours | Style | Basis |
|---|---|---|---|---|
| T1 | IndicVoices | ~480 | extempore/conversational | [EARLIER] est. |
| T1 | Vaani | 184.48 (paper subset 113.04) | image-prompted spontaneous | [EARLIER], re-read [M] |
| T1 | CV 27.0 + FLEURS | ~0.9 (65 MB MP3 file) + ~8 | read | [EARLIER]; MDC listing [M] |
| T1-lean | SYSPIN Telugu | ~115 | studio read | new [M] |
| T1-lean | Rasa Telugu | 52.3 | expressive | new [M] |
| T1-lean (provisional) | RESPIN Telugu clean | 1,021.2 | read, agri/finance, 4 dialect regions | new; hours from README copy [U-source] |
| T2 | RESPIN Telugu semi-noisy + noisy | 186.1 + 127.7 | read | new |
| T2 | Numo Telugu | 1,224.2 | read | new [M] |
| T2 | Shrutilipi (AIR) | ~390 | broadcast news | [EARLIER] |
| T2 | Kathbath | ~155 (+75 noisy) | read | [EARLIER] |
| T2 | NPTEL (Vistaar) | ~183 | lectures | [EARLIER] |
| T2 (BY-SA) | SLR66 | ~8 [E, 1.03 GB zips] | volunteer TTS-style read | OpenSLR [M] |
| T3 | bolAIndia Telugu | ~8,970 | mixed | licence hidden |
| T3 | Chaashini Telugu | 116.3 | scraped, ASR labels | |
| T3 | BhasaAnuvaad NPTEL Te-side | 738.4 (translation pairs) | lectures | |
| T4 | MS Speech Corpus / MUCS Telugu 40 h, IIITH-CSTD 2,000.8 h (research-only), InfoBay, Karya sanmati (714,985 clips, NC) | - | - | |
| Paid | SpeechData.ai Telugu | 500 | conversational, consented | $65/h [V]; Nexdata 202 h quote |

**Telugu clearly commercial-safe transcribed hours (low / best / high):**
- Low **~0.55 k h** (earlier low, no new sources).
- Best **~1.9 k h** = earlier T1 ~0.67 k + SYSPIN 0.115 + Rasa 0.052 + RESPIN clean 1.02 [E].
- High **~3.4 k h** = Best + RESPIN other slabs 0.31 + Numo 1.22 [E].
- T1+T2 add Shrutilipi/Kathbath/NPTEL ≈ +0.73 k → ~4.1 k at the High end.
- **Spontaneous/conversational Telugu T1 is unchanged at ~0.65-0.7 k h.** The extra 1.2-2.7 k h are READ prompts (agri/finance for RESPIN, TTS-style scripts for SYSPIN, unknown prompts for Numo), recorded on phones or in a studio.

### English (Indian accent)

| Tier | Source | Hours | Style | Basis |
|---|---|---|---|---|
| T1 | Vaani-English | 22.46 | spontaneous | [EARLIER] |
| T1 | Common Voice en "indian" accent + South Asian English set | ~224 h of clips est., fewer validated | read | [EARLIER]; MDC CC0 set [M] |
| T1 (eval) | Svarah | 9.6 | read + spontaneous | [EARLIER] |
| T1-lean (TTS-grade) | SYSPIN/LIMMITS Indian English | 80 h, 2 speakers (challenge pages); licence NOT stated | studio read | [M] challenge page; AIKosh licence unverified [U] |
| T3 | SPIRE-SIES | 170.8 (23 h with Whisper-based transcripts) | spontaneous | request form |
| T3 | kenpath/SPICOR Indian English (inside Pretraining-V1) | 99.4 | TTS | [U] |
| T2 | NPTEL2020 Indian English | 15,700 | STEM lectures, YouTube CC | [M] |
| T2 | People's Speech CC-BY, VoxPopuli, LibriSpeech, CV en (non-Indian) | multi-k h | non-Indian accents | [EARLIER] |
| Paid | Defined.ai/Nexdata/etc. | quote | | |

**Indian-accented English clearly commercial-safe transcribed hours (low / best / high):** Low ~0.05 k; Best ~0.25 k (22 + CV en-IN ~224 [E, partly unvalidated]); High ~0.35 k (+ SYSPIN English 80 h if its licence is confirmed CC BY). The only upside is NPTEL2020 (up to 15.7 k h) at T2 or a request for SPIRE-SIES.

### What this implies for each monolingual model (labelled data only; pseudo-labels in Section 4)

| Model | Realistic upper bound of labelled, clearly safe training hours | Notes |
|---|---|---|
| Hindi | ~3 k h best, up to ~5 k h if Numo and RESPIN noisy slabs are accepted. Spontaneous ~2 k h. | Not binding; one A10G budget caps usable hours at a few thousand anyway [E]. |
| Telugu | ~1.9 k h best; ~3.4 k stretch; spontaneous only ~0.7 k. | Binding constraint is now diversity/domain, not volume: ~65% of the best case is read, narrow-domain speech. Pseudo-labelling Vaani Telugu (2.1 k h untranscribed) remains the only way to add spontaneous volume. |
| English (India) | ~0.25 k Indian-accent h; general English T1 pool is multi-k h | Train on generic English T1 + weight Indian-accent data; NPTEL2020 is the optional T2 booster. |

---

## 3. Code-switched speech: every known corpus

| Pair | Corpus | Size | Licence / terms | Availability | Owner / contact path (do not contact) | Tier for training |
|---|---|---|---|---|---|---|
| Hi-En | MUCS 2021 sub-task 2 = OpenSLR SLR104 | 89.86 h train + 5.18 test (+6.24 blind) | CC BY-SA 4.0 | download | OpenSLR / Navana-Tech MUCS organisers | T2 [EARLIER] |
| Hi-En | **HiACC** | 5.24 h (adults + children), spontaneous + read | "Creative Commons Attribution 4.0 International" | open, Zenodo 15551669 (Data in Brief 2025) | Shruti Singh; supervisors Muskaan Singh, Virender Kadyan (via Zenodo record) | T1 |
| Hi-En | IITG-HingCoS (IIT Guwahati, 2019) | ~25 h, 9,251 CS sentences, phone recordings | licence not stated | request form on https://iitg.ac.in/eee/emstlab/HingCoS_Database/HingCoS.html [M] | IIT Guwahati EMST lab (no contact shown) | T3 |
| Hi-En | IIT Guwahati phone corpus (arXiv 1810.00662) | 7,005 utts, 71 speakers | not read | [U] | | T3 |
| Hi-En | CS-FLEURS (earlier) | small | cc-by-nc-4.0 | | | T4 [EARLIER] |
| Hi-En | LiVA AI sample / Sonexis sample | ~10 min / n.a. | cc-by (tag) / cc-by-nc | vendor samples | support via HF | T2 / T4 |
| Hi-En | Natural CS inside IndicVoices, Vaani, SPRING-INX (code-mixed transcripts), RESPIN/Numo prompts keep English terms | unmeasured | T1 | existing | | T1, needs LID/script-mix mining [EARLIER] |
| Hi-En | IndicCMix (text + synthetic English audio) | 104k sentences x 11 langs | MIT | gated HF | AI4Bharat | synthetic only |
| Hi-En | Indic DiarBench (10.7 h) and Vaani Benchmark V1.0 (Hindi, CS-tagged) | eval | cc-by-4.0 | | | eval |
| Hi-En | Hinglish aggregators (agarwalayushi, RidheshBhati/Codemixed_New) | "2,264 h"; 394k rows | CC-BY tag / none | | | T3 |
| Te-En | **Microsoft Research India code-switched set** (Shah et al., arXiv 2006.00782, June 2020) | 243 h train+dev CS (CMI 23.85) + 170 h mono; test 28 h CS | not stated; paper does not say who collected or whether released [M] | not released as far as found | authors Sanket Shah, Basil Abraham, Gurunath Reddy M, Sunayana Sitaram, Vikas Joshi (Microsoft Research India) | T3/T4 (internal) |
| Te-En | JHU JSALT 2022 workshop setup | ~15 h CS train (search summary) | not found | [U] | | T3 |
| Te-En | CoSTA (arXiv 2406.10993) | ~2.3 h Telugu CS eval (587 instances) + 2.5 h podcast eval, derived from IndicVoices | "authors intend to release the evaluation sets under CC-BY-4.0"; "will be publicly released upon publication" [M]; not found released | | paper authors | eval |
| Te-En | **"200 h / 400 speakers" corpus** | claimed 200 h, 400 speakers, POS/language/CS-point tags | none | only a DeepLearning.AI forum post by "ML_Explorer" dated 2026-03-26 18:33; no paper, owner, licence or reply; poster "already reached out to the author" [M] | untraceable | T3 (unverified claim; may refer to the MSR 243 h data [U]) |
| Te-En | UD Telugu-English TECT (text) / anishka/CodeSwitching-TE-EN (text) | text | BY-SA 4.0 / apache-2.0 | text only | | text only |
| Te-En | Praxel LASE (synthetic) | ~37 min | CC-BY-4.0 | synthetic ElevenLabs | | not ASR |
| Te-En | Natural CS in IndicVoices/Vaani Telugu | unmeasured | T1 | existing | | mine it |
| Both | Common Voice Code-Switching dataset | "Alpha", no releases | - | https://github.com/common-voice/cv-dataset [M] | Mozilla | none yet |

Gap: no source gives a measured Hi-En or Te-En code-switched T1 hour count. The practical plan from earlier notes (mine natural CS from IndicVoices/Vaani/SPRING-INX plus synthetic splicing) stands; IndicCMix text is now a licensed (MIT) source of code-mixed Hindi/Telugu text, usable to drive TTS-based or text-based synthetic CS [E].

---

## 4. Unlabeled but licensed audio for pseudo-labelling

| Pool | Hindi | Telugu | English | Licence / tier | Notes |
|---|---|---|---|---|---|
| Vaani untranscribed (derived: audio minus transcribed) | ~13.9 k h | ~2.1 k h | ~0.31 k h | CC BY 4.0, consent-based, T1 | [EARLIER]; HF Vaani card last modified 2026-09-17; transcribed totals re-read today (2,122.2 h) [M] |
| IndicVoices untranscribed | ~12.5 k h across 22 languages (not per language) | | | CC BY 4.0, T1 | whether present in HF release not stated [EARLIER] |
| RESPIN, Numo, SYSPIN | already transcribed | | | | not an unlabeled pool |
| NPTEL2020 | | | 15.7 k h with unverified subs | YouTube CC, T2 | usable as pseudo-label target if subs are ignored |
| bolAIndia | 89.8 k h (45% of all has no/automatic labels; 44.98 k h untranscribed overall) | 8.97 k h | 9.98 k h | licence hidden, T3 | biggest pool, provenance unknown; needs the gate text |
| Kapture Chaashini | 1.39 k h | 0.12 k h | 0.24 k h | Apache tag over scraped audio, T3 | |
| BhasaAnuvaad NPTEL / SeamlessAlign audio | 1.4 k / 2.4 k h | 0.74 k / 0.87 k h | | CC BY (tag) over NPTEL/mined audio, T3 | SeamlessAlign inherits Meta Seamless non-commercial terms [M via search] |
| Gram Vaani SLR118 | ~1 k h | | | academic only, T4 | [EARLIER] |
| Wikimedia spoken Wikipedia / LibriVox | negligible | negligible | | PD/CC | LibriVox has almost no Hindi/Telugu (forum threads: first Telugu book pending; Hindi texts hard to source) [M via search] |
| Kathbath noisy, YODAS2 Hindi | see earlier | | | T2 | [EARLIER] |

Teacher-model output licences remain unresearched (earlier gap).

---

## 5. Licence-label reliability traps found in this sweep (record in the manifest)

- InfoBayAI: tag `cc-by-4.0` but text "provided for research and educational purposes only" (card says only samples are hosted).
- Chaashini: tag/text Apache-2.0 for "research and commercial speech-technology development" over scraped public spoken-word audio with ASR labels.
- Pretraining-V1 aggregators and `agarwalayushi/hinglish`: CC-BY tag over mixed sources; Pretraining-V1 includes the Microsoft Indian corpus.
- Spoken Tutorial: site says CC BY-SA 4.0; AI4Bharat copy says CC BY 4.0.
- Sonexis Hinglish: NC while looking like an open conversational corpus.
- Karya: custom "KPL BY-NC-SA-FS 1.0".
- Deepdml/other re-uploads of the NC Microsoft corpus carry no licence tag.
- Abhisingh-18/hindi-english-codeswitch-dataset: Apache-2.0 on transcripts and metadata only (4,000 h Hindi, 1,000 h English, no audio; "Original audio keeps its own license") [M]; do not read it as a licence for audio.

---

## 6. Gaps, and cost/time to create (all numbers flagged)

Not available as clearly commercial-safe open data:
1. Spontaneous/conversational Telugu beyond ~0.7 k h; Telugu in laptop-mic or far-field conditions; Telugu domain text (numbers, names, dictation).
2. Real Telugu-English code-switched speech (any size) and measured CS fractions inside T1 sets.
3. Real Hindi-English CS beyond HiACC 5 h (and SLR104 BY-SA 90 h).
4. Indian-accent English, transcribed, with open licence beyond ~0.25 k h; conversational Indian English.
5. Close-talk laptop microphone speech (almost everything above is phone, telephone or studio).

Price signals (all dated 2026-10-12):
- SpeechData.ai: $65 per audio hour, consent per speaker, Telugu 500 h / Hindi 2,000 h catalogue [V]. 100 h ≈ $6.5 k; 500 h ≈ $32.5 k [E arithmetic].
- Defined.ai Data Access Plan (euros): 315 h €50,000; 625 h €100,000; 1,565 h €250,000; 3,125 h €500,000 → ~€159-160 per hour effective, catalogue not language-specific [V, via search; arithmetic E].
- Nexdata: Telugu 202 h "paid dataset licensed for commercial use", quote only; custom collection from US$20,000 minimum [V via search].
- Annotation only (already recorded audio), from the CoSTA paper's own appendix: "Hindi - Rs. 3000 per hour ... Telugu - Rs. 3500 per hour"; podcast set tasks "Rs.6000 per hour of audio" [M]. At an assumed ₹85-90/US$ that is ~US$34-41/h and ~US$67-70/h [E]. These cover transcript translation and manual verification, not collection.
- Crowd contributor pay in a job listing for Telugu/Hindi voice data: "$2 USD - $4 USD Per Hour" [V via search; recruiter listing]; vendor margins sit on top.
- My rough all-in estimate for a new consented Telugu spontaneous conversational set (recruit, record, transcribe with 2-pass QC): **US$40-120 per hour** (i.e. ~US$20-60 k for 500 h) [E: not sourced beyond the figures above]. Elapsed time for 500 h with a vendor panel of ~50-200 speakers: several months [E]. A few-hundred-dollar budget supports at most a few hours of this.
- Cheapest realistic mitigation: pseudo-label Vaani Telugu/Hindi untranscribed audio and mine natural CS from licensed sets; consider asking AI4Bharat/ARTPARK/IISc about additional releases (not done; sending outward needs the user's go-ahead).

---

## 7. TTS note (brief; only if TTS is in scope)

| Language | Dataset | Hours / speakers | Quality | Licence | Notes |
|---|---|---|---|---|---|
| Hindi | SYSPIN_S1.0 | ~119 h, 1 M + 1 F | studio 48 kHz/24-bit | CC BY 4.0 (AIKosh/project page) | best studio single-speaker pair; T&C page unread |
| Hindi | Rasa | 50.8 h, 1 M + 1 F | 48 kHz, expressive | CC-BY-4.0 | includes IndicTTS neutral sentences (inheritance [U]) |
| Hindi | IndicVoices-R (earlier) | ~74.6 h, many speakers | restored extempore | CC BY 4.0 | multi-speaker; [EARLIER] |
| Hindi | IndicTTS (IITM) | studio | licence unresolved | [EARLIER] T3 |
| Hindi | BharatVani 205 h studio | | proprietary | T4 |
| Hindi | Chaashini "studio-grade" 1,395 h | | Apache tag over scraped audio | T3 |
| Telugu | SYSPIN_S1.0 | ~115 h, 1 M + 1 F | studio | CC BY 4.0 | |
| Telugu | Rasa | 52.3 h, 1 M + 1 F | 48 kHz | CC-BY-4.0 | |
| Telugu | IndicVoices-R | ~136.4 h | restored | CC BY 4.0 | [EARLIER] |
| Telugu | IndicTTS Telugu (SPRINGLab copy) | 8.74 h, 2 speakers | studio | "subject to original Indic TTS license" | [EARLIER] T3 |
| Telugu | SLR66 | ~8 h [E], volunteers | crowdsourced "high-quality" | BY-SA 4.0 | share-alike risk |
| English (India) | SYSPIN/LIMMITS English | 80 h, 1 M + 1 F (challenge pages) | studio | licence not stated; a third-party review reports "many errors" in LIMMITS data [M via search] | verify before use |
| English (generic) | LibriTTS-R (SLR141), LibriSpeech | | | OpenSLR listing only seen, licence not read [U] | |

---

## 8. Items that need the user's browser or a login (exact URL and what is hidden)

1. https://huggingface.co/datasets/kapturecx/bolAIndia : STATS.md ("format, filtering, source credits and usage conditions") and MAP.md, and the gate-condition text (login). Decides whether the 190 k h pool is usable at all.
2. https://spiredatasets.ee.iisc.ac.in/respincorpus : download form and its terms (and per-language hours table); AIKosh Terms of Use link https://aikosh.indiaai.gov.in/home/terms-n-conditions (path partly inferred, [U]). Also OpenReview PDF https://openreview.net/pdf/a75242153008713de8b43aa6997257a3b1b0e85f.pdf (needs browser verification) for per-language hours, ethics/consent statements, speaker compensation.
3. https://huggingface.co/datasets/psdn-ai/numo-indic-speech : the gate-condition text (login) and the privacy policy interplay (https://www.psdn.ai/privacy); whether speakers consented to open CC BY release.
4. https://forms.office.com/r/bF27ah1Fg9 (SPIRE-SIES request form; submitting is a form action, not done) and the corpus licence.
5. https://asr.iiit.ac.in/asr_challenge : host was unreachable from my fetcher; page text came via search summary only.
6. Hugging Face gates for Rasa, Rural_Women_ASR_v2, Nirantar copy, BhasaAnuvaad repos: conditions text visible only when logged in.
7. NPTEL's own content licence (nptel.ac.in terms) to decide NPTEL2020 and NPTEL-derived sets.
8. HiACC licence text in the Zenodo record is already open (CC BY 4.0), but check the Data in Brief paper (https://www.sciencedirect.com/science/article/pii/S2352340925006109) for speaker/guardian consent for children.

---

## 9. Sources (fetched 2026-10-12 unless stated)

HF API sweeps (filters language:te / language:hi + task/modality, searches for telugu, hindi, hinglish, code-switch, indian english, accent india; authors sarvamai, ai4bharat, ARTPARK-IISc, kapturecx, snorbyte); dataset cards for psdn-ai/numo-indic-speech, kapturecx/bolAIndia and Chaashini, shiprocket-ai/nirantar, ai4bharat/Rasa, NPTEL, Spoken-Tutorial, Mann-ki-Baat, Vanipedia, SeamlessAlign, IndicVoices-ST, IndicCMix, krutrim-ai-labs/IndicST, SpeechDataAI, InfoBayAI, Sheeba2026/bharatvani, projectkaira/Pretraining-V1, agarwalayushi/hinglish, humyn-labs, liva-ai, naradatum, Praxel, bridgeconn/snow-mountain, espnet/floras, facebook/omnilingual-asr-corpus, google/svq, karya/sanmati-stories, SPRINGLab/Hindi-1482Hrs. Zenodo 15551669 (HiACC), 11635731 (Nirantar), 4596748 (NPTEL2020). AIKosh RESPIN, SYSPIN, SPRING-INX Hindi pages. arXiv 2411.04699 (BhasaAnuvaad), 2006.00782 (MSR code-switch), 2406.10993 (CoSTA), 2312.00698 (SPIRE-SIES), 2604.19151 (Voice of India), 2511.09690 (Omnilingual), 2206.01205 (Snow Mountain). OpenSLR resource list and SLR66. Mozilla Data Collective listings (Hindi, Telugu, India, code-switching) and cv-dataset README. LDC-IL Telugu corpus page. Nexdata Telugu page. psdn.ai and psdn.ai/privacy. DeepLearning.AI forum thread 890896. Sibling-scratchpad copies read: RESPIN README (respin_gh.md), Rural_Women_ASR_v2 README, slr66.txt (not fetched by me from the original URL for the first two).
