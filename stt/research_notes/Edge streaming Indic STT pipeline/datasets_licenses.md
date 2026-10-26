# Open speech/text datasets (Hindi, Telugu, Indian English, code-switch): hours, licenses, commercial-use risk, and a training mix

All facts verified 2026-10-08 (fetch date) unless stated. "HF" = Hugging Face dataset card/API. Hours marked "(est.)" are my own arithmetic and are labelled as inferences. Not legal advice: tiers below are engineering risk tiers.

Risk tier legend used throughout:
- T1 = permissive license (CC0 / CC-BY) on a consent-based, creator-collected corpus. Use freely, keep attribution manifest.
- T2 = open license BUT a caveat: ShareAlike (SA), scraped/third-party upstream audio or text (AIR radio, IndicCorp crawl, YouTube), or license inconsistent across official pages. Usable with documented risk acceptance; prefer to keep share of mix limited.
- T3 = license ambiguous/undeclared/unreadable, or terms I could not read. Do not use until resolved in writing.
- T4 = unusable for commercial training (NC, research-only, academic-only, custom restrictive terms).

---

## Q1. Which datasets are clearly safe for commercial training vs ambiguous vs unusable (license quoted, link)?

### Takeaway
The only large Indic corpora that are both CC-BY and consent-collected (not scraped) are IndicVoices (+ IndicVoices-R), Vaani, and SPRING-INX; Common Voice is CC0 but nearly empty for Hindi/Telugu. Anything from Microsoft/SpeechOcean, Gram Vaani, GigaSpeech, SPGISpeech, Skit-S2I, CS-FLEURS, Emilia (non-YODAS) is non-commercial/academic-only and must be excluded. Several "CC-BY" Indic releases carry internal inconsistencies (Kathbath, Lahaja, SLR103, Vaani page) that must be recorded in a manifest.

### Cited Findings

#### Tier-1 / near-Tier-1 Indic ASR corpora
- **IndicVoices** (AI4Bharat): HF metadata `cc-by-4.0`; card says "This dataset is released under the CC BY 4.0". Gated (accept conditions + share contact info; conditions text only visible when logged in). 23.7K h total, 11.2K h transcribed (update 23 Dec 2025), 51K speakers, 22 languages, 400+ districts; 76% extempore / 15% conversational / 8% read. Full-length audio in incremental archives v1-v5, 745 GB. Funded by Bhashini/MeitY/Nilekani Philanthropies. — [HF card](https://huggingface.co/datasets/ai4bharat/IndicVoices); [HF API (lastModified 2026-06-15)](https://huggingface.co/api/datasets/ai4bharat/IndicVoices)
- IndicVoices paper says dataset will be released under CC-BY-4.0 "which allows commercial usage"; tools MIT; participants gave consent, ethics committee approval (stated in the IndicVoices-R paper). — [IndicVoices (ar5iv)](https://ar5iv.labs.arxiv.org/html/2403.01926); [IndicVoices-R paper](https://ar5iv.labs.arxiv.org/html/2409.05356)
- IndicVoices GitHub repo itself has no license text/no releases; AI4Bharat site footer says "All rights reserved" and that datasets were being moved to HF. — [GitHub](https://github.com/AI4Bharat/IndicVoices); [AI4Bharat page](https://ai4bharat.iitm.ac.in/datasets/indicvoices)
- **IndicVoices-R** (restored/enhanced TTS-quality derivative of IndicVoices): `cc-by-4.0`, gated; 1,704 h, 10,496 speakers, 22 languages; 93.25% extempore; "released under the same CC BY 4.0 license" as parent. Per-language table: Hindi ~74.6 h; Telugu 136.4 h (6.91 read + 129.49 other). Overlaps IndicVoices - do not double count. — [HF](https://huggingface.co/datasets/ai4bharat/indicvoices_r); [paper](https://ar5iv.labs.arxiv.org/html/2409.05356)
- **Vaani** (IISc/ARTPARK): `cc-by-4.0`, gated. HF card: ~31,278 h audio, 105 languages, 165 districts (Phase 1: 80, Phase 2: 85), 156K speakers; 2,122 h transcribed; image-prompted spontaneous speech. Per-language (audio / transcribed): Hindi 14,923.7 / 1,003.78 h; Telugu 2,326.47 / 184.48 h; English 336.79 / 22.46 h. Project site: CC-BY-4.0, future versions via Bhashini; target 150,000+ h. — [HF](https://huggingface.co/datasets/ARTPARK-IISc/Vaani); [Vaani site](https://vaani.iisc.ac.in/); [HF API (lastModified 2026-09-17)](https://huggingface.co/api/datasets/ARTPARK-IISc/Vaani)
- Vaani paper (arXiv 2603.28714): 31,255 h speech, 2,043 h transcribed (slightly different from HF 31,278/2,122); describes "a permissive license"; consent forms checked by automated QC; speaker residence verified via PAN/Aadhaar. — [paper HTML](https://arxiv.org/html/2603.28714)
- **SPRING-INX** (SPRING Lab IIT Madras; NLTM Speech Consortium): AIKosh lists "Attribution 4.0 International (CC BY- 4.0)", ~3,400 h labelled, 10 languages (Phase 1 ~2,000 h; Phase 2 ~1,400 h), 16 kHz, monologue + conversational, code-mixed transcripts. Paper (Phase 1, ~2,000 h) says data is "released in the public domain" and does not name a CC license; vendor-collected "legally sourced" data under tender. — [AIKosh](https://aikosh.indiaai.gov.in/home/datasets/details/spring_inx_odia.html); [paper](https://ar5iv.labs.arxiv.org/html/2310.14654)
- **Common Voice**: CC0 for Mozilla Data Collective releases (checked: example Scripted Speech datasets listed CC0-1.0; per-dataset license should be checked). Since Oct 2025 CV is distributed only via Mozilla Data Collective (HF `mozilla-foundation/common_voice_17_0` is empty). Latest as of 2026-10-08: Scripted Speech v27.0 (cut-off 2026-09-11), Spontaneous Speech v5.0, a Code-Switching dataset "Alpha" with no releases yet. The cv-dataset repo's MPL-2.0 license covers code, not audio. — [cv-dataset](https://github.com/common-voice/cv-dataset); [Data Collective search summary](https://prod.datacollective.mozillafoundation.org); [HF CV17 notice](https://huggingface.co/datasets/mozilla-foundation/common_voice_17_0)
- **Google FLEURS**: HF `cc-by-4.0` (README YAML), not gated; read speech of FLoRes sentences, 102 languages; Vistaar counts FLEURS train as 7 h Hindi / 8 h Telugu. — [HF README](https://huggingface.co/datasets/google/fleurs/raw/main/README.md); [HF API](https://huggingface.co/api/datasets/google/fleurs); [Vistaar](https://arxiv.org/html/2305.15386)
- **IndicVoices-ST / BhasaAnuvaad** (speech translation, Bhashini/AI4Bharat): `cc-by-4.0`, gated; 44,400 h speech for 13 Indian languages + English; NPTEL subset repo `ai4bharat/NPTEL` also `cc-by-4.0`, gated. NPTEL lecture audio provenance (YouTube/NPTEL) not independently verified. — [IndicVoices-ST HF API](https://huggingface.co/api/datasets/ai4bharat/IndicVoices-ST); [NPTEL HF API](https://huggingface.co/api/datasets/ai4bharat/NPTEL)

#### Tier-2: open license with provenance / SA / inconsistency caveats
- **Kathbath**: license statements conflict. HF metadata `cc-by-4.0`; HF body text says "We license the actual packaging of all this data under the Creative Commons CC0 license"; GitHub (IndicSUPERB) says packaging CC0, code MIT (sidebar shows Apache-2.0); AIKosh Kathbath-Telugu pages say CC BY-SA 4.0 (listed author "Microsoft", likely metadata error). Text is from IndicCorp ("a crawl of publicly available websites"; AI4Bharat "do not own the raw text"). Read speech (sentences of 8-15 words from IndicCorp), 1,218 speakers, 1,684 h total/12 languages; Hindi 150.2 h clean + 47.7 h noisy; Telugu 154.9 h clean + 74.8 h noisy. — [HF](https://huggingface.co/datasets/ai4bharat/Kathbath); [GitHub](https://github.com/AI4Bharat/IndicSUPERB); [AIKosh Telugu](https://aikosh.indiaai.gov.in/home/datasets/details/telugu_asr_benchmark_dataset_for_news_and_general_domains_kathbath_telugu.html); [paper](https://ar5iv.labs.arxiv.org/html/2208.11761)
- **Shrutilipi** (AIR news bulletins): HF `cc-by-4.0` and AIKosh "CC BY-4.0"; >6,400 h, 12 languages; mined audio-text pairs from All India Radio news bulletins; no ownership disclaimer on AIKosh page. Vistaar training mix uses 1,620 h Hindi / 390 h Telugu from it. Underlying audio = state broadcaster's content; AI4Bharat's CC-BY covers their packaging/alignment only. — [HF](https://huggingface.co/datasets/ai4bharat/Shrutilipi); [AIKosh](https://aikosh.indiaai.gov.in/home/datasets/details/shrutilipi_ai4bharat.html); [Vistaar Table 2](https://arxiv.org/html/2305.15386)
- **MUCS 2021 Hindi-English (and Bengali-English) = OpenSLR SLR104**: OpenSLR page says CC BY-SA 4.0; MUCS data page also says CC BY-SA 4.0. 89.86 h train + 5.18 h test (Hindi-En), spoken tutorials (lecture style). SLR104 note: data updated 16 Feb 2021. — [SLR104](https://www.openslr.org/104/); [MUCS data page](https://navana-tech.github.io/MUCS2021/data.html)
- **YODAS / YODAS2** (YouTube-derived, ESPnet): HF `cc-by-3.0`; "made sure that our dataset only consisted of videos with CC licenses"; "Manual caption only indicates that it is uploaded by users, but not necessarily transcribed by a human"; removal-request email provided. Hindi: hi000 480.79 h manual + hi100 2.75 h automatic; Telugu: te000 5.67 h manual; English ~29,155 h manual + ~140,697 h automatic. Video license ≠ necessarily rights in uploaded captions or music/third-party content in the video. — [YODAS](https://huggingface.co/datasets/espnet/yodas); [YODAS2](https://huggingface.co/datasets/espnet/yodas2)
- **People's Speech** (English, archive.org): "licensed for academic and commercial usage under CC-BY-SA and CC-BY 4.0"; CC-BY subsets = clean/dirty, CC-BY-SA = clean_sa/dirty_sa; 30,000+ h; mostly American accents; some training transcripts likely ASR output; poorly aligned portion. — [HF](https://huggingface.co/datasets/MLCommons/peoples_speech)
- **VoxPopuli** (European Parliament): "distributed under CC0 license, see also European Parliament's legal notice for the raw data"; metadata cc0-1.0 + other; English 543 h transcribed; accented English 29 h (non-native European accents, not Indian). — [HF](https://huggingface.co/datasets/facebook/voxpopuli)
- **NVIDIA Granary**: `cc-by-4.0` annotations (JSONL pseudo-labels) over English subsets en_librilight, en_voxpopuli, en_yodas, en_ytc; no Hindi/Telugu subset visible; no per-source caveats on card (inherits YODAS/YouTube provenance). — [HF](https://huggingface.co/datasets/nvidia/Granary)
- **LibriSpeech**: OpenSLR "CC BY 4.0", ~1000 h read English (LibriVox audiobooks, public-domain texts). — [SLR12](https://www.openslr.org/12/). **Multilingual LibriSpeech** HF `cc-by-4.0` (English portion hours not retrieved) — [HF API](https://huggingface.co/api/datasets/facebook/multilingual_librispeech)
- **Telugu SLR66 (Google crowdsourced)**: OpenSLR license "Attribution-ShareAlike 4.0 International" (the SLR63-66/78/79 family is commonly assumed CC-BY; the page says BY-SA); copyright Google 2018-19; TTS-style read sentences by volunteers; hours not stated. — [SLR66](https://www.openslr.org/66/)
- **Edinburgh EdAcc** (accented English conversations, ~40 h total; includes Indian-English speakers per paper): CC-BY-SA; DataShare record flagged "superseded & withdrawn due to a change in license", so current license must be re-checked. — [paper/search summary](https://arxiv.org/pdf/2303.18110); [DataShare](https://datashare.ed.ac.uk/handle/10283/4836)
- **Svarah** (Indian-accented English eval): body text CC BY 4.0 on HF and AIKosh (HF API shows no license tag); 9.6 h, 117 speakers, 65 districts, 19 states, read + spontaneous; gated. Too small to train on; use as test set. — [HF](https://huggingface.co/datasets/ai4bharat/Svarah); [AIKosh](https://aikosh.indiaai.gov.in/home/datasets/details/svarah.html)
- **Lahaja** (Hindi multi-accent eval): body text CC BY 4.0, HF metadata tag `mit` (inconsistent); ~12.5 h, 132 speakers, 83 districts, read + extempore; gated. Eval only. — [HF](https://huggingface.co/datasets/ai4bharat/Lahaja)
- **Sarvam Indic DiarBench** (2026): `cc-by-4.0`; Hindi 10.7 h, Telugu 9.3 h (near-field, far-field, YouTube "in-the-wild" parts); conversational with English code-mixing; benchmark-size only, and the YouTube part has the usual provenance question. — [HF](https://huggingface.co/datasets/sarvamai/indic-diarbench)

#### T3: terms unresolved
- **MUCS 2021 sub-task 1 (SLR103: Hindi 95.05 h train/5.55 h test, 8 kHz stories; Marathi; Odia)**: OpenSLR page gives only a link to a Microsoft Open Data license ID (f1f352a6-...); I could not resolve it (host not found). MUCS page says Hindi/Marathi/Odia and Tamil/Telugu/Gujarati licenses both link to Microsoft Open Data. Microsoft's C-UDA-1.0 (a possible candidate) permits redistribution/modification "solely for Computational Use" and does not mention commercial use, but I could not confirm that is the license in question. — [SLR103](https://www.openslr.org/103/); [MUCS data page](https://navana-tech.github.io/MUCS2021/data.html); [C-UDA-1.0](https://github.com/microsoft/Computational-Use-of-Data-Agreement/blob/master/C-UDA-1.0.md)
- **IndicTTS (IIT Madras)**: IITM site requires agreeing to "License For Use of Indic TTS" (text not retrieved); HF derivative `SPRINGLab/IndicTTS_Telugu` (8.74 h, 2 speakers) is "subject to the original Indic TTS license terms"; AIKosh pages tag Phase-3 Hindi and Telugu IndicTTS as CC BY 4.0 / CC BY-SA 4.0 (conflicting). Studio TTS data, tiny for ASR (Vistaar: 20 h Hindi, 36 h Telugu). — [IITM page (via search)](https://www.iitm.ac.in/donlab/indictts/database); [HF](https://huggingface.co/datasets/SPRINGLab/IndicTTS_Telugu)
- **IISc SYSPIN TTS** (reported 40 h each Hindi/Telugu): license not found. — [SYSPIN](https://syspin.iisc.ac.in/datasets) (page content not retrievable; hours from search summary)
- **NPTEL2020 Indian English** (Zenodo): Zenodo metadata license `cc-by-4.0` on test-part2 record; audio is from NPTEL lecture videos with subtitles; NPTEL's own terms not verified. — [Zenodo 4596748](https://zenodo.org/records/4596748)
- **CMU Wilderness (bible.is audio)**: no published data license found; source papers say audio is copyrighted and not redistributable (repo ships download scripts); treat as T4. — [SpeechTaxi](https://arxiv.org/pdf/2409.06372); [Luhya paper](https://arxiv.org/pdf/2104.01624)

#### T4: unusable for commercial training
- **Microsoft Speech Corpus (Indian languages)** (Telugu, Tamil, Gujarati; 12.3 GB; v1.0; published 7/15/2024): "Data provided in this dataset shall not be used for commercial purposes. You may use the data solely for research purposes." Attribution "Data provided by Microsoft and SpeechOcean.com". MUCS 2021's 40 h Telugu train set (16 kHz) is hosted via Microsoft Open Data and therefore presumptively the same restriction. A university mirror calls the license C-UDA v1.0; conflict - treat as NC. — [Microsoft Download](https://www.microsoft.com/en-us/download/details.aspx?id=105292); [MUCS data](https://navana-tech.github.io/MUCS2021/data.html)
- **Gram Vaani 1111-hour Hindi ASR (SLR118)**: "can be used freely for academic purposes"; commercial use requires permission via contact@gramvaani.org. 100 h train + 5 dev + 3 eval labelled, ~1,000 h unlabeled telephone speech, 8 kHz mp3. — [SLR118](https://www.openslr.org/118/)
- **Skit-S2I**: HF `cc-by-nc-4.0`. — [HF API](https://huggingface.co/api/datasets/skit-ai/skit-s2i)
- **CS-FLEURS** (code-switched FLEURS, includes Hindi-English per a derived HF set): `cc-by-nc-4.0`. — [HF API](https://huggingface.co/api/datasets/byan/cs-fleurs)
- **GigaSpeech**: HF tag `apache-2.0` but Terms of Access limit use to "non-commercial research and educational purposes" with indemnity, and SpeechColab "does not own the copyright of the audio files"; 10,000 h (audiobooks 2,655, podcasts 3,498, YouTube 3,845). Card says trained models "may be eligible for commercial license" subject to Fair Use. Inconsistent - treat as T4. — [HF](https://huggingface.co/datasets/speechcolab/gigaspeech)
- **SPGISpeech**: Kensho terms - "academic research purposes and internal use only"; 5,000 h earnings calls with L1/L2 accents; derivative works need written consent. — [HF](https://huggingface.co/datasets/kensho/spgispeech)
- **Emilia (original)**: "only for non-commercial purposes under the CC BY-NC-4.0 license" despite HF tag cc-by-4.0; Emilia-YODAS part CC-BY (derived from YODAS2); English 46.8k h (Emilia) + 92.2k h (YODAS); no Hindi/Telugu; Emilia "does not own the copyright to the audio". — [HF](https://huggingface.co/datasets/amphion/Emilia-Dataset)
- **Multilingual TEDx (SLR100)**: CC BY-NC-ND 4.0 (no Indian languages anyway). — [SLR100](https://www.openslr.org/100/)
- **Silencio Network Indian-languages sample**: CC BY-NC 4.0 sample of commercial catalogue (Hindi 2,000 h / Telugu 293 h claimed, commercial purchase). — [search summary of HF page](https://huggingface.co/datasets/SilencioNetwork/indian-languages-speech)
- **Samanantar (parallel text)**: HF tag and licensing section "Creative Commons Attribution-NonCommercial 4.0" - unusable even for text. — [HF](https://huggingface.co/datasets/ai4bharat/samanantar)

#### Noise / RIR / augmentation
- **MUSAN (SLR17)**: OpenSLR "CC BY 4.0"; authors state they only included commercial-OK content; per-subdirectory LICENSE files map each wav to its license (music from Jamendo/FMA/Incompetech, noise from Freesound-type sources) so attribution list must come from those files. — [SLR17](https://www.openslr.org/17/); [MUSAN paper](https://arxiv.org/pdf/1510.08484)
- **RIRS_NOISES (SLR28)**: OpenSLR "Apache 2.0"; bundles real RIRs from RWCP, REVERB 2014, Aachen AIR, simulated RIRs, and point-source noises from MUSAN; component licenses not individually verified. — [SLR28](https://www.openslr.org/28/)
- **DEMAND** (Zenodo 1227121): description says CC BY-SA 3.0 Unported; Rights metadata says CC BY 4.0 (inconsistent); 16-channel recordings in 18 environment codes, 7.4 GB; hours not stated. — [Zenodo](https://zenodo.org/records/1227121)

#### Text-only (LM / text normalization)
- **IndicCorp v2**: HF card: "All the datasets created as part of this work will be released under a CC-0 license" (no license tag on HF API); Kathbath README states IndicCorp is "a crawl of publicly available websites" and AI4Bharat does not own the raw text. — [HF card](https://huggingface.co/datasets/ai4bharat/IndicCorpV2); [Kathbath HF](https://huggingface.co/datasets/ai4bharat/Kathbath)
- **Sangraha**: `cc-by-4.0`, 251B tokens, 22 languages; "Verified" portion includes scraped sites, OCR of PDFs, and "transcribed data from various Indic language videos, podcasts, movies, courses". — [HF](https://huggingface.co/datasets/ai4bharat/Sangraha)
- **UD Telugu-English TECT** (code-switch text, no audio): CC BY-SA 4.0; sentences romanized and modified to include a code-switch. — [UD](https://universaldependencies.org/treebanks/qte_tect)
- A self-published HF forum scan (Aug 2026) claims 65.1% of 4,893 Indic HF datasets have no license tag and 154 are CC-BY-NC; methodology not disclosed - low-credibility, use only as a reminder. — [HF forum](https://discuss.huggingface.co/t/a-free-monthly-refreshed-compliance-matrix-of-all-4-893-indic-language-datasets-on-the-hub-showing-that-65-declare-no-license-so-teams-can-avoid-licensing-traps-and-missing-tag-repos-before-they-train-on-them/178373)

### Inferences
- The "AI4Bharat gated CC-BY" family is the practical backbone, but the gate's actual condition text is only visible after login and is not in the license metadata; it should be captured (screenshot/text, dated) at download time as part of the manifest.
- Inconsistent license labels (Kathbath, Lahaja, SLR103, MS corpus mirror, Emilia tag, GigaSpeech tag) show tags on aggregator pages are unreliable; the primary page/terms text should always win and the more restrictive reading should be assumed until resolved.
- Re-uploads on HF can silently relicense (e.g. `dianavdavidson/MUCS-Hinglish` is tagged cc-by-4.0 while the original SLR104 is CC BY-SA 4.0 per [HF search](https://huggingface.co/api/datasets?search=hinglish&limit=30&sort=downloads)); always pull from the originator.

### Gaps
- Could not read IndicVoices/Vaani/Kathbath gate-condition text (login-only) or the "License For Use of Indic TTS" text or the Microsoft Open Data license ID f1f352a6-.... Could not retrieve MLS English hours, FLEURS Hindi/Telugu exact hours (only Vistaar's 7 h/8 h), CV Hindi/Telugu license page on Mozilla Data Collective directly (generic CC0 statement via search), or SYSPIN's license.
- Did not verify NPTEL's own content license (matters for NPTEL-derived AI4Bharat sets), nor Bhashini/Anuvaad release pages beyond IndicVoices-ST/BhasaAnuvaad on HF (no separate Bhashini ASR dataset found). No other 2026 open Hindi/Telugu speech corpora from Sarvam found beyond Indic DiarBench (eval-size); Sarvam's 2026 open releases found were language models.

---

## Q2. Hours per language, style, domain, annotation quality, transcript conventions (Hindi, Telugu, English-IN, code-switch)

### Takeaway
Transcribed, permissive Hindi is roughly 2k h (IndicVoices ~0.8k est., Vaani 1.0k, SPRING-INX 0.35k, small CV/FLEURS), Telugu only ~0.7k h (IndicVoices ~0.5k est., Vaani 0.18k), and Indian-accented English transcribed data is tiny (Vaani-English 22 h; CV en "indian" accent ~224 h of clips). Transcript conventions for English words in code-switched speech differ by corpus and are only partly documented; native-script vs Latin handling must be normalised in your pipeline.

### Cited Findings

Catalogue table (hours = transcribed unless noted).

| Dataset | Hi h | Te h | En-IN h | Style / domain | Script / conventions | Source |
|---|---|---|---|---|---|---|
| IndicVoices | ~790 (est.) | ~480 (est.) | 0 | 76% extempore, 15% conversational, 8% read; 13 read-domains, 21 extempore domains | HF fields `verbatim`, `normalized`, `unsanitized_*`; Level-1 verbatim "using the corresponding grapheme", Level-2 standardised spelling; 89 non-speech tags; ~9 s Silero-VAD segments; maker-checker-superchecker QC (~700 transcribers) | [HF API](https://huggingface.co/api/datasets/ai4bharat/IndicVoices); [paper](https://ar5iv.labs.arxiv.org/html/2403.01926) |
| IndicVoices-R | ~75 | ~136 | 0 | restored speech, 93% extempore | as IndicVoices | [paper](https://ar5iv.labs.arxiv.org/html/2409.05356) |
| Vaani | 1,003.78 | 184.48 | 22.46 | image-prompted spontaneous, phone-recorded crowd | local scripts per Unicode Indian Scripts reference; tags [unintelligible], [inaudible], <UNKNOWN_SEGMENT>, <PAUSE>, {correction}; segment invalid if >25% words unintelligible; English proper names case-sensitive | [HF](https://huggingface.co/datasets/ARTPARK-IISc/Vaani); [paper](https://arxiv.org/html/2603.28714) |
| SPRING-INX | 351 (316 train/30 valid/5 test) | 0 (Telugu not released) | 0 | monologue (read/extempore) + 2-4 speaker conversations; ~10% of conversational meant to be code-mixed | code-mixed; native + Romanised/English words; borrowed English spellings normalised via mapped list; whitespace/non-printable chars/tags removed | [paper](https://ar5iv.labs.arxiv.org/html/2310.14654); [AIKosh](https://aikosh.indiaai.gov.in/home/datasets/details/spring_inx_odia.html) |
| Kathbath | 150.2 (+47.7 noisy) | 154.9 (+74.8 noisy) | - | read, IndicCorp news-like sentences 8-15 words, 1,218 speakers | alphanumeric sentences only | [paper](https://ar5iv.labs.arxiv.org/html/2208.11761) |
| Shrutilipi (Vistaar usage) | 1,620 | 390 | - | AIR news bulletins, broadcast read news | mined/aligned (noisier alignment) | [Vistaar](https://arxiv.org/html/2305.15386) |
| NPTEL (Vistaar usage) | 157 | 183 | - | STEM lectures, Indian-accented | from lecture subtitles | [Vistaar](https://arxiv.org/html/2305.15386) |
| Common Voice v27.0 | 26.74 total / 15.71 validated (485 speakers) | 3.2 total / 0.94 validated (75 speakers) | en total 3,795.9 h / 2,826.8 validated; "indian" accent 153,048 of 2,591,456 clips (~5.9%; ~224 h of clips est.) | read prompts | punctuated sentences | [CV v27 stats JSON](https://raw.githubusercontent.com/common-voice/cv-dataset/main/datasets/scripted-speech/cv-corpus-27.0-2026-09-11.json) |
| FLEURS | ~7 (Vistaar count) | ~8 | - | read FLoRes sentences, ~10 h/lang total | HF has `raw_transcription` and normalised `transcription` fields | [Vistaar](https://arxiv.org/html/2305.15386); [HF README](https://huggingface.co/datasets/google/fleurs/raw/main/README.md) |
| MUCS Hindi-English (SLR104) | 89.86 train + 5.18 test (+6.24 blind) | - | - | CS lecture tutorials (16 kHz) | English words appear BOTH in Latin and native scripts in train; blind test references use Latin for English words; paper defines transliterated WER | [SLR104](https://www.openslr.org/104/); [MUCS paper](https://ar5iv.labs.arxiv.org/html/2104.00235) |
| MUCS sub-task 1 | 95.05 (8 kHz stories) | 40 (MS-hosted, NC) | - | | | [MUCS data](https://navana-tech.github.io/MUCS2021/data.html) |
| Indic DiarBench | 10.7 | 9.3 | - | conversational eval | two formats: native-script (English in Indic script) and normalised (English in Roman, Arabic digits) | [HF](https://huggingface.co/datasets/sarvamai/indic-diarbench) |
| Svarah | - | - | 9.6 (eval) | read + spontaneous Indian-accented English | | [HF](https://huggingface.co/datasets/ai4bharat/Svarah) |
| Lahaja | 12.5 (eval) | - | - | read + extempore multi-accent Hindi | | [HF](https://huggingface.co/datasets/ai4bharat/Lahaja) |
| YODAS (manual subs) | 480.79 | 5.67 | ~29k (global English) | YouTube, user-uploaded captions | not necessarily human-made | [HF](https://huggingface.co/datasets/espnet/yodas) |

- Vistaar's own train mix totals 2,150 h Hindi and 806 h Telugu (Shrutilipi 1,620/390, Kathbath 137/142, CV 13/0, NPTEL 157/183, MUCS 95/40, IndicTTS 20/36, Gramvaani 100/0, FLEURS 7/8, Google TTS 0/6, IIIT-IndicSpeech 1/2) - it includes NC/academic sources (MUCS Telugu, Gramvaani), so not a commercial-safe recipe. — [Vistaar Table 2](https://arxiv.org/html/2305.15386)
- IndicVoices HF card lists per-language splits (Hindi: 445,160 train + 5,530 valid examples; Telugu: 269,306 train + 3,295 valid examples); the whole HF set has 6,379,012 examples. — [HF API](https://huggingface.co/api/datasets/ai4bharat/IndicVoices)
- Vaani paper's fine-tuning subset uses 593.93 h Hindi and 113.04 h Telugu (Section 6; 331 h / 69 h in Appendix A.1) - lower than the HF page's transcribed totals (1,003.78 / 184.48), so the paper and card disagree or describe different filtered subsets. — [paper HTML](https://arxiv.org/html/2603.28714)
- Vaani HF card is internally ambiguous on phases (says current version includes both phases, also says "open-sourced version is from Phase 1"). — [HF](https://huggingface.co/datasets/ARTPARK-IISc/Vaani)
- Common Voice Hindi is 96% of clips but only 485 speakers and Telugu 75 speakers - speaker diversity too low for acoustic modelling. — [CV v27 JSON](https://raw.githubusercontent.com/common-voice/cv-dataset/main/datasets/scripted-speech/cv-corpus-27.0-2026-09-11.json)

### Inferences
- IndicVoices hours (est.): 11,200 h / 6,379,012 examples ≈ 6.3 s average; Hindi 450,690 examples ≈ 790 h and Telugu 272,601 ≈ 480 h. This assumes the HF set equals the 11.2K transcribed hours; ±15% uncertainty. The old paper Table 6 train hours (Hindi ~65 h / Telugu ~102 h) refer to the 2024 v1 release and are obsolete.
- There is no unified convention for English words in code-mixed segments across IndicVoices/SPRING-INX/MUCS/Vaani. Normalising to a single policy (suggest: native script for Indic words, Latin for English words, Arabic digits, plus a lexicon mapping) is a required preprocessing step; MUCS evidence shows mixed-script ground truth inflates WER.
- Indian-accented English transcribed hours that are open and commercial-safe are scarce: CV en indian-accent clips (~224 h est.; fewer validated), Vaani-En 22 h, plus eval-size Svarah.

### Gaps
- Exact IndicVoices code-mixing proportion, script policy for English tokens, and per-language hours are not published on the card; Telugu-English code-mixed proportion in IndicVoices/Vaani unknown. CV validated hours for the Indian-accent subset not computed (JSON truncated at ~100k characters in my read of the accent section beyond 'en').

---

## Q3. CC-BY attribution obligations; legal risk where packaging is CC0/CC-BY but underlying audio/text is scraped; practical tiering and mitigation

### Takeaway
CC-BY obligations are attribution, license notice, and indication of modification when you "share" material; Creative Commons' own guidance suggests a dataset credit/link in model documentation, but explicitly does not settle whether weights themselves carry attribution or are "adaptations". A CC0/CC-BY wrapper cannot license rights the packager does not hold, so All-India-Radio audio (Shrutilipi) and crawled IndicCorp text (Kathbath prompts, IndicCorp, Sangraha) stay T2 regardless of label.

### Cited Findings
- CC BY 4.0 §3(a)(1): if you share licensed material (including modified versions) you must retain creator identification, copyright notice, license notice, warranty-disclaimer notice and a link where reasonably practicable, and indicate modifications; §3(a)(2) allows any reasonable manner (a link may suffice); §3(a)(3) requires removing attribution on licensor request; §5 is "as-is" with no warranty and no liability. — [CC BY 4.0 legal code](https://creativecommons.org/licenses/by/4.0/legalcode.en)
- CC guidance: "All CC licenses require attribution to the creator(s)"; for training, attribution "could be a simple link to the source of the dataset used to train the model"; CC licenses apply only when copyright permission is needed (if an exception/limitation applies, license terms don't); if models/outputs are based on ShareAlike content and shared publicly, following SA "would require AI developers to use the same CC license"; NC requires all stages non-commercial; ND content should not be used. The primer does not state that BY attribution must be embedded in weights, and does not classify weights as adapted material. CC itself warns its guidance may lead to over-compliance. — [CC: using CC-licensed works for AI training](https://creativecommons.org/using-cc-licensed-works-for-ai-training-2/); [summary of the same](https://creativecommons.org/using-cc-licensed-works-for-ai-training-2/)
- AI4Bharat explicitly disclaims ownership of IndicCorp raw text ("a crawl of publicly available websites") and licenses only "the actual packaging" under CC0 (Kathbath, IndicSUPERB GitHub). — [Kathbath HF](https://huggingface.co/datasets/ai4bharat/Kathbath); [IndicSUPERB](https://github.com/AI4Bharat/IndicSUPERB)
- Shrutilipi: data "mined" from AIR news bulletins; AIKosh page carries no ownership disclaimer. — [HF](https://huggingface.co/datasets/ai4bharat/Shrutilipi); [AIKosh](https://aikosh.indiaai.gov.in/home/datasets/details/shrutilipi_ai4bharat.html)
- IndicVoices-R authors contrast their consent-based collection with "web-mined data, where it is more challenging to adhere to licensing terms". — [IndicVoices-R paper](https://ar5iv.labs.arxiv.org/html/2409.05356)
- Emilia/GigaSpeech terms require indemnity and state the packagers do not own audio copyrights; employer of for-profit researchers is bound. — [Emilia](https://huggingface.co/datasets/amphion/Emilia-Dataset); [GigaSpeech](https://huggingface.co/datasets/speechcolab/gigaspeech)
- India policy context: DPIIT's Dec 8, 2025 working paper (Part 1) proposed a "mandatory blanket license with statutory remuneration" for AI training on lawfully accessed works, royalties due once the AI system is commercialised, no opt-out; consultation extended to 6 Feb 2026; it is a proposal and I found no report of a final decision. — [Mondaq](https://www.mondaq.com/india/copyright/1718746/exploring-the-dpiits-working-paper-on-generative-ai-and-copyright); [Storyboard18](https://www.storyboard18.com/digital/dpiit-releases-working-paper-on-copyright-and-ai-proposes-hybrid-licensing-model-85551.htm); [Storyboard18 extension](https://www.storyboard18.com/digital/dpiit-extends-consultation-on-generative-ai-copyright-framework-till-february-6-87006.htm)
- Vaani and IndicVoices: explicit consent forms, ethics approval, residency verification documented in the papers (primary evidence for creator-collected provenance). — [Vaani paper](https://arxiv.org/html/2603.28714); [IndicVoices-R paper](https://ar5iv.labs.arxiv.org/html/2409.05356)

### Inferences
- Practical tiering (engineering view): T1 = IndicVoices, IndicVoices-R, Vaani, SPRING-INX (resolve BY vs "public domain" wording), Common Voice (CC0), FLEURS, LibriSpeech, IndicVoices-ST/BhasaAnuvaad non-NPTEL parts. T2 = Shrutilipi (AIR), Kathbath (read speech is fresh crowd audio but prompts come from crawled text; low risk but inconsistent license labels), NPTEL-derived, YODAS/Granary/People's Speech (archive.org, YouTube), VoxPopuli (EP legal notice), anything CC-BY-SA (SLR104, SLR66, EdAcc, DEMAND). T3 = MUCS sub-task 1 (unreadable MS license), IndicTTS, SYSPIN, Svarah/Lahaja (eval only anyway). T4 per Q1.
- Kathbath audio is newly recorded by consenting speakers, so the scraped-text issue concerns only the short prompt sentences; I judge its risk as lower than Shrutilipi (whole broadcast audio + transcripts of a third party) - this is my judgement, not a sourced claim.
- Mitigations: (1) keep a per-source data manifest (dataset, version/hash, download date, license text snapshot, gate terms, URL, attribution string, tier, hours used); (2) cap T2 share of mix, and train a T1-only ablation so the product can be rebuilt without T2 if challenged; (3) ship a third-party-notices / model-card list crediting each CC-BY dataset (CC's suggested dataset-link practice); (4) avoid SA data in the shipped weights if you cannot accept SA-on-model risk, or isolate SA data to eval/tuning of internal-only models; (5) avoid distributing raw audio; (6) treat DPDP/voice-privacy obligations separately (not researched here).

### Gaps
- No authoritative legal source found on whether trained weights are "adapted material" under CC BY or whether Indian copyright law has a TDM exception; I did not research India's DPDP Act implications for voice data. DPIIT outcome after Feb 2026 unknown.

---

## Q4. Is there enough clearly-licensed Telugu and Hindi-English code-switch data? Estimated commercial-safe hours per language

### Takeaway
Hindi: enough (~2.0-2.2k transcribed T1 hours). Telugu: marginal (~0.65-0.7k T1 transcribed hours; ~1.1-1.4k if T2 Kathbath/Shrutilipi/NPTEL are accepted), and Telugu-English code-switch has no dedicated open commercial-safe corpus. Hindi-English code-switch: only SLR104 (~90 h, BY-SA) is dedicated; the rest must come from naturally code-mixed segments in IndicVoices/SPRING-INX/Vaani.

### Cited Findings
- Hindi T1 components: IndicVoices ~790 (est.), Vaani 1,003.78, SPRING-INX 351, CV 15.71 validated, FLEURS ~7. (sources in Q2)
- Telugu T1 components: IndicVoices ~480 (est.), Vaani 184.48, CV 0.94 validated, FLEURS ~8; SPRING-INX released data excludes Telugu. (sources in Q2)
- Telugu T2: Kathbath 154.9 h (+74.8 noisy), Shrutilipi ~390 h (Vistaar usage), NPTEL ~183 h (Vistaar usage), YODAS manual 5.67 h, SLR66 (BY-SA, hours not stated).
- Telugu non-usable: MS Speech Corpus/MUCS Telugu 40 h (non-commercial).
- Hindi-English CS: SLR104 89.86 h train (BY-SA); Indic DiarBench 10.7 h eval; CS-FLEURS (NC); HiACC (Hinglish adult+child, 5.24 h; license not found). Telugu-English: a search for an open speech corpus found no confirmed open release; CoSTA built a ~2 h Telugu-English eval set from IndicVoices; a 200 h Telugu-English corpus is mentioned only in a forum post requiring contact with authors. — [HiACC](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12329218/); [CoSTA](https://arxiv.org/pdf/2406.10993); [forum post](https://community.deeplearning.ai/t/request-for-telugu-english-code-switched-speech-corpus-asr-project/890896)
- CV Code-Switching dataset exists as "Alpha" with no releases yet as of 2026-10-08. — [cv-dataset](https://github.com/common-voice/cv-dataset)
- Hindi-English transcripts in SPRING-INX: ~10% of conversational data intended code-mixed (Tanglish/Hinglish). — [SPRING-INX paper](https://ar5iv.labs.arxiv.org/html/2310.14654)

### Inferences
- Estimated clean (T1) transcribed hours: Hindi ≈ 2,150 (range 1.9-2.3k); Telugu ≈ 670 (range 0.55-0.75k) ; Indian-accent English ≈ 22 h (Vaani) + ~100-224 h (CV en-IN clips, partly unvalidated) ≈ 0.1-0.25k h; Hindi-English CS: ~0 T1 dedicated, ~90 h T2 (SLR104), plus unknown hours of naturally code-mixed T1 segments (could be tens to a couple hundred hours; needs LID/script-mix mining of IndicVoices/Vaani/SPRING-INX).
- T1+T2 (excluding T3/T4): Hindi ≈ 4.0-4.5k (adds Shrutilipi 1,620, Kathbath 150, NPTEL 157, YODAS 481, SLR104 90); Telugu ≈ 1.4k (adds Shrutilipi 390, Kathbath 155, NPTEL 183).
- Telugu is the binding constraint; plan pseudo-labelling (see Q5) and synthetic code-switching (splicing Telugu + English utterances, or TTS-augment) to cover Telugu-English, as no real corpus qualifies.

### Gaps
- Real per-language code-switch proportions in T1 sets are unmeasured. IndicVoices Telugu/Hindi untranscribed vs transcribed release split not confirmed. HiACC and Indic DiarBench are too small to matter.

---

## Q5. Best unlabeled-audio source that is commercial-safe for pseudo-labeling/distillation (and other unlabeled sources)

### Takeaway
Vaani untranscribed audio (CC-BY-4.0, consent-based) is the best commercial-safe unlabeled source: ~13.9k h Hindi, ~2.1k h Telugu, ~0.3k h English (derived). Others (YODAS2, Gram Vaani unlabeled, Shrutilipi) are either small for Hi/Te, academic-only, or provenance-risky.

### Cited Findings
- Vaani: audio minus transcribed ≈ Hindi 13,920 h, Telugu 2,142 h, English 314 h (derived from HF per-language table); license CC-BY-4.0; phone-quality spontaneous speech; gated HF with streaming recommended. — [HF](https://huggingface.co/datasets/ARTPARK-IISc/Vaani)
- IndicVoices: 23.7K total vs 11.2K transcribed means ~12.5K h not transcribed; full-length audio archives are provided in v1-v5 (745 GB); whether the untranscribed remainder is in the HF release is not stated. — [HF](https://huggingface.co/datasets/ai4bharat/IndicVoices)
- Gram Vaani SLR118: ~1,000 h unlabeled Hindi telephone audio but academic-only (T4). — [SLR118](https://www.openslr.org/118/)
- YODAS: Hindi 480.79 h manual + 2.75 h automatic, Telugu 5.67 h (v1 listing); English ~170k h (CC-BY-3.0, YouTube CC-videos). Granary provides pseudo-label JSONL for English subsets. — [YODAS](https://huggingface.co/datasets/espnet/yodas); [Granary](https://huggingface.co/datasets/nvidia/Granary)
- Pseudo-label teacher license: not researched per model (Whisper/others) - see gap. Vaani paper benchmarks Whisper and Parakeet-TDT. — [Vaani paper](https://arxiv.org/html/2603.28714)
- Vaani roadmap: 150k+ h target; future versions via Bhashini; reported plan to open-source 16,000 h via Bhashini (2024 report; no confirmation found). — [Vaani site](https://vaani.iisc.ac.in/)

### Inferences
- Use Vaani untranscribed with a strong teacher (permissively licensed) and confidence/LID filtering, noting Vaani is image-description speech (limited domain) and phone-recorded, so pseudo-label gains concentrate on acoustic diversity and Telugu volume.
- Pseudo-labelled data derived from T1 audio remains T1 for audio rights; teacher model license terms for outputs must be checked separately.

### Gaps
- No verified output-license terms for candidate teacher models (Whisper, IndicConformer, Parakeet, etc.). Unlabeled English-with-Indian-accent commercial-safe audio beyond Vaani-En (314 h) and CV unvalidated clips not found. Whether any 2026 Vaani release increased the open untranscribed audio beyond the card's figures is unconfirmed (HF last modified 2026-09-17).

---

## Q6. Recommended training mix (MVP and Production), per language and per source

### Takeaway
MVP (~1.3k h, T1 only): ~550 h Hindi, ~400 h Telugu, ~280 h English (Indian-accent-weighted), ~50 h code-switch (synthetic + mined). Production (~4.2k h incl. ~1.2k h pseudo-labelled): Hindi ~1.5k, Telugu ~1.0k (0.6k pseudo), English ~1.2k, code-switch ~0.3k; T2 sources optional and capped (<=20% per language), with a T1-only fallback model.

### Cited Findings
(Constraint basis) Available T1 hours per source as listed in Q2/Q4; Vistaar's baseline used 2,150 h Hindi/806 h Telugu for Indic ASR. — [Vistaar](https://arxiv.org/html/2305.15386)

### Inferences (proposed mix; my recommendation, not sourced)

MVP, T1-only, ~1,280 h:
| Language | Source | Hours | Why |
|---|---|---|---|
| Hindi (550) | IndicVoices | 250 | spontaneous, many speakers/districts |
| | Vaani (QC-filtered) | 200 | phone-channel diversity |
| | SPRING-INX | 80 | conversational + code-mixed |
| | CV + FLEURS | 20 | read, clean |
| Telugu (400) | IndicVoices | 280 | largest T1 Telugu |
| | Vaani | 110 | all-ish of quality-filtered |
| | CV + FLEURS | 10 | |
| English (280) | CV en, Indian-accent-weighted subset | 180 | CC0, ~224 h Indian-accent clips est. |
| | LibriSpeech | 50 | clean read baseline |
| | Vaani-En | 22 | spontaneous Indian English |
| | VoxPopuli | 28 | CC0 (+EP notice) |
| Code-switch (50) | synthetic splice of T1 Hi/Te + En utterances; mined code-mixed T1 segments (LID filter); optionally SLR104 as T2 eval/tune | 50 | no T1 corpus exists |
Eval only (never train): Svarah, Lahaja, FLEURS test, CV test, Indic DiarBench, MUCS Hi-En test.

Production, ~4,200 h (≈3.0k labelled + ≈1.2k pseudo-labelled):
| Language | Source | Hours |
|---|---|---|
| Hindi ~1,500 | IndicVoices ~600, Vaani ~400 (QC), SPRING-INX ~300, CV+FLEURS ~25, Kathbath T2 ~100 (optional), Vaani pseudo-labels ~350 (removed if teacher license fails) |
| Telugu ~1,000 | IndicVoices ~450, Vaani ~180, Kathbath T2 ~110 (optional), CV+FLEURS ~10, Vaani pseudo-labels ~250 |
| English ~1,200 | CV en ~400, LibriSpeech ~300, People's Speech CC-BY clean ~150 (T2), VoxPopuli ~100, Vaani-En 22 + pseudo-labelled ~228 |
| Code-switch ~300 | synthetic/mined ~200, SLR104 ~90 (T2, BY-SA) |
Shrutilipi (AIR, T2) and NPTEL are held out of the base mix; add only if Telugu WER stalls and risk is accepted in writing. Noise/RIR augmentation: MUSAN + RIRS_NOISES (+ DEMAND if BY/SA terms acceptable).

Justification: (a) one A10G favours a few thousand hours with high diversity over scale; (b) T1 Telugu is capped ~0.7k h so pseudo-labelling from Vaani is the main lever; (c) English is weighted to Indian accents but only Vaani/CV provide commercial-safe data; (d) code-switch is synthetic/mined because no open commercial-safe corpus exists; (e) keep T2 <20% per language so a clean rebuild is cheap.

### Gaps
- Mix proportions are not validated experimentally; optimal Hindi:Telugu:English ratio for a streaming small model on laptop CPUs unknown. Streaming-quality of phone-channel Vaani for laptop-mic deployment unverified.
