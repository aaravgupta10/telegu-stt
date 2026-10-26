# AI4Bharat / IIT Madras speech datasets: dataset-by-dataset licence and usefulness audit

Audit date: 2026-10-12. Scope: commercial usability + usefulness for three separate monolingual on-device streaming STT models (Hindi, Telugu, English-India), each needing Latin-script English words inside Hindi/Telugu output. Read-only audit: public HTTP GETs of web pages, HF dataset pages and HF API JSON, GitHub raw files, arXiv HTML, AIKosh pages; HTTP HEAD (headers only) on a few public object-store URLs to read Content-Length. No dataset/audio files downloaded, no login, no gate accepted, no form submitted. Two public viewer previews (first 100 rows, text columns only) were read to check transcript conventions (noted where used). This is an engineering risk assessment, not legal advice.

Evidence labels (as in CLAUDE.md): [M] measured/stated by a cited primary source; [V] vendor claim; [E] our estimate/arithmetic; [P] proposal; [U] unverified / could not see; [OURS] our own measurement (here only the public-preview reads and header reads, no run IDs).

Prior notes checked and corrected: `research_notes/Edge streaming Indic STT pipeline/datasets_licenses.md` (2026-10-08). Corrections are listed in section 2.7.

---

## 0. Bottom line (read this first)

| Rank | Dataset | Verdict in one line |
|---|---|---|
| 1 | IndicVoices (HF `ai4bharat/IndicVoices`) | Only large, consent-based, consistently CC BY 4.0 AI4Bharat corpus. Participant consent text said data would be used for "both commercial and non-commercial purposes". Tier T1 (small residual caveats). Hindi ~0.5-0.85k h, Telugu ~0.4-0.5k h transcribed [E]. Core training set. |
| 2 | SPRING-INX (IITM SPRING Lab; AIKosh) | Hindi 351 h (Phase 1). CC BY 4.0 on AIKosh vs "public domain" in paper; vendor-collected. Tier T2. Keeps English words in Latin script in transcripts in the languages I could preview. Valuable for code-mix. No Telugu. |
| 3 | Kathbath | Read news-style sentences, 16 kHz, ~141 h Hindi / ~145 h Telugu on HF. Licence labels conflict (CC0 packaging / CC BY 4.0 tag / CC BY-SA on AIKosh); sentences from crawled IndicCorp; consent said "research purposes". Tier T2. Supplement and standard eval set. |
| eval | Svarah (English, 9.6 h), Lahaja (Hindi, 12.5 h) | Eval only. Licence tags missing (Svarah) or contradictory (Lahaja `mit` tag vs CC BY 4.0 body). Tier T2. |
| avoid | Shrutilipi | Mined from All India Radio (newsonair) bulletins. AIR's own copyright page: personal, non-commercial use only; anything else needs prior written permission. AI4Bharat's CC BY 4.0 cannot override. Tier T3 leaning T4. HF copy is also much smaller than advertised. |
| avoid | Vistaar (bundle), Kathbath-Hard (via Vistaar zip), IndicVoices-ST mined sets (NPTEL, Mann ki Baat, WordProject etc.), Dhwani/MahaDhwani | Aggregates of third-party data or YouTube scrapes; no coherent licence. T3/T4. |
| not for STT | IndicVoices-R, Rasa, IndicTTS, IndicVoices-ST (IV part) | TTS/ST resources. IndicVoices-R has a live licence conflict (HF/paper/GitHub CC BY 4.0 vs AIKosh CC BY-ND 4.0). |
| gap | English-India | Nothing trainable in this family. Svarah is 9.6 h, eval-only. |
| gap | Telugu Latin-script English | No Telugu data in the family keeps English in Latin script (IndicVoices writes English words in native script, as far as I could verify for Hindi). |

Key cross-cutting findings (details in section 2):
1. The "gate conditions" on all AI4Bharat gated HF speech datasets are the HF default only: "You need to agree to share your contact information..." There is no `extra_gated_prompt` anywhere (the HF API does expose `extra_gated_prompt` when present: verified on `speechcolab/gigaspeech`, which shows it). So there is no hidden terms text to capture; the gate is contact-collection plus auto-approval. [M]/[OURS]
2. The gate is not an access control: the full-length IndicVoices archives, Kathbath tars, IndicVoices-R tars, Nirantar, and Vistaar zips sit on public object-store URLs that answered HTTP 200 to anonymous HEAD requests. [OURS]
3. AIKosh licence fields are not authoritative: several are blanket labels from Bhashini bulk uploads by third-party uploaders (e.g. CC BY-SA 4.0 stamped on Kathbath, Gramvaani and Common Voice benchmark copies on the same day). [M]
4. AI4Bharat's CC BY 4.0 on the HF pages is a licence on AI4Bharat's own collection (IndicVoices, IV-R, Lahaja, Svarah, Rasa) and on its packaging of third-party material (Kathbath text, Shrutilipi). It cannot extend to the third-party part.
5. Hour figures for IndicVoices are snapshots in time (7.3k -> 12k -> 23.7k total; 1.6k -> 3.2k -> 11.2k transcribed), not a conflict.

---

## 1. Verdict table

Tier legend (same as earlier note): T1 clearly safe; T2 usable with documented caveats; T3 unresolved; T4 unusable. Hours are transcribed hours unless stated. "(E)" = our estimate with method given in the dataset section.

| Dataset | Licence (authoritative) and why | Tier | Hours hi / te / en (transcribed) | Train / eval / neither | Recommended role and exact reasons | Ask AI4Bharat in writing |
|---|---|---|---|---|---|---|
| IndicVoices | CC BY 4.0. HF YAML + HF card + paper footnote + both AIKosh listings agree; paper says "allowing commercial usage"; participant script said commercial and non-commercial. GitHub has no LICENSE file. | T1 | hi ~520-840 (E); te ~390-510 (E); en 0 | Train (and `valid` as dev) | Backbone for Hindi and Telugu. 16 kHz FLAC, spontaneous + read + conversational, 51K speakers. English words are written in native script (verified for Hindi), so needs re-mapping to Latin for our output spec. | See 6.1 |
| IndicVoices-R | CC BY 4.0 (HF YAML, HF card, paper section 6, GitHub `LICENSE.md` full text). AIKosh says CC BY-ND 4.0, uploaded by an AI4Bharat member: a real internal conflict. Adopt the stricter (ND) until resolved. | T2 | hi 74.6; te 136.4; en 0 | Neither (redundant with IndicVoices, denoised/TTS-style) | Not for STT. Same recordings as IndicVoices but demixed/dereverbed/enhanced and restricted to 44.1 kHz clips, so acoustically mismatched to phone/laptop-mic deployment. | Which licence is correct (BY vs BY-ND); are IV-R test speakers in IndicVoices train |
| Kathbath | Packaging: CC0 (HF body, GitHub README) AND `cc-by-4.0` (HF YAML); AIKosh says CC BY-SA 4.0 (third-party Bhashini bulk upload, low authority). Raw text not owned by AI4Bharat. Follow CC BY 4.0 attribution. | T2 | hi ~141 (E, HF) / 150.2 clean + 47.7 noisy (paper); te ~145 (E, HF) / 154.9 + 74.8 noisy; en 0 | Train (supplement) + eval (test-unknown) | Clean read speech, 121 Hindi and 104 Telugu speakers only. Sentences from IndicCorp crawl. Consent said "research purposes" + "publicly released and used for building AI models". Use capped share; keep T1-only baseline. | Confirm commercial use incl. IndicCorp-derived sentences; CC0 vs BY; consent wording |
| Kathbath-Hard | Not a separate dataset on HF. Vistaar-made (synthetic background noise added to Kathbath test). Inherits Kathbath; only distributed as a Vistaar zip with no licence statement. | T3 | n/a (test only) | Eval only | Robustness eval; regenerate our own noisy copy of Kathbath test-unknown instead of using the Vistaar zip. | None needed if regenerated |
| Shrutilipi | HF/AIKosh say CC BY 4.0 but that licences only AI4Bharat's alignment/packaging. Underlying audio/text = All India Radio (NSD, Prasar Bharati). AIR copyright page: personal non-commercial use only; other use needs prior written permission. | T3 (leaning T4) | hi ~850 (E, HF copy; paper 1,620); te ~49 (E, HF copy; paper 390) | Neither until permission | Exclude from commercial training. Also quality-noisy (document-level CTC alignment). | Did AI4Bharat have AIR/Prasar Bharati permission for commercial redistribution/training? Which tau/slice is on HF? |
| Lahaja | Body text "released under the CC BY 4.0" + AIKosh CC BY 4.0; HF YAML tag `mit` is inconsistent. Both permissive; treat as CC BY 4.0. No GitHub LICENSE. | T2 | hi 12.5 (eval); te 0; en 0 | Eval only | Hindi accent robustness test (122/132 non-native speakers). Do not train. Read prompts come from the same Wikipedia-sentence pool as IndicVoices, so check text overlap. | Fix YAML tag; confirm consent covers commercial eval/training; speaker overlap with IndicVoices |
| Svarah | Body text "released under the CC BY 4.0" + AIKosh CC BY 4.0; HF API has no licence tag. | T2 | hi 0; te 0; en 9.6 (eval) | Eval only | Only Indian-accent English eval in the family. 117 L2 speakers, read + extempore + use-case prompts, Switchboard-style transcription guidelines. | Add licence tag; consent text |
| Vistaar (benchmark + train bundle) | GitHub: "Vistaar is MIT-licensed. The license applies to all the fine-tuned language models". Data not licensed by that line. Bundle of Kathbath, FLEURS, Common Voice, IndicTTS, MUCS, Gramvaani (+ Shrutilipi, NPTEL, etc. in train). | T3 (bundle) | hi 2,150 train mix / te 806 (paper) | Neither as a bundle | Use original sources per their own licences. Bundle includes academic-only Gramvaani and Microsoft-hosted MUCS Telugu. | Clarify data licence of bundle |
| IndicSUPERB | Dataset = Kathbath (+ small QbE/KS sets). GitHub LICENSE file is Apache-2.0; README says code/models MIT, dataset packaging CC0. | T2 | see Kathbath | Eval (test sets only reachable via objectstore tars) | HF Kathbath has no test or noisy splits; the IndicSUPERB README links ungated tars for Test-Known/Unknown and noisy. Transcripts there are `transcripts_n2w` (numbers to words). | See Kathbath |
| IndicTTS (IITM) | IITM "License For Use of Indic TTS" (PDF unreadable from this environment; only a secondary web-search summary: perpetual, non-exclusive, worldwide, transferable, sub-licensable, royalty-free; Section 3 not seen). AIKosh Phase-3 pages (Hindi female, Telugu male and female): CC BY 4.0, uploaded by Bhashini division. | T3 | hi ~10.3 (2 speakers, HF mirror); te ~8.7 (2 speakers) | Neither | Studio TTS data, tiny. Only use: clean-read sanity eval (Vistaar uses it). Read the PDF in a browser before any use. | Request licence text; confirm commercial use |
| SPRING-INX | AIKosh (Bhashini uploader, Hindi page 2025-11-28): CC BY 4.0. Paper: "in the public domain" (not a CC dedication). HF `SPRINGLab/SPRING_INX_*` repos: no licence tag/card, and no Hindi repo. Vendor-collected under tender. | T2 | hi 351 (316/30/5 train/valid/test, Phase 1); R2 tar also listed on AIKosh (hours unseen) (U); te 0; en 0 (Indian English "being collected", not released) | Train (Hindi code-mix) | Best open source for Latin-script English inside native-script text (seen in Gujarati and Bengali previews; Hindi unpreviewed). Needs written confirmation of licence and vendor consent. | See 6.5 |
| Rasa | CC-BY-4.0 (HF YAML, HF card, GitHub README: consistent) | T1 | hi 50.8 (2 speakers); te 52.3 (2 speakers) | Neither | Studio-quality expressive TTS data, 2 speakers per language. | None needed for STT |
| IndicVoices-ST / BhasaAnuvaad (+ NPTEL, Spoken-Tutorial, Mann-ki-Baat, Vanipedia, WordProject, UGCE-Resources, SeamlessAlign) | CC BY 4.0 on every repo; card adds "Please contact us for any copyright concerns." | T2 (IV-derived); T3/T4 (mined sources) | no new ASR transcripts; targets are translations | Neither | IV-ST reuses IndicVoices audio with LLM-translated English; English side is synthetic TTS. Mined sources are NPTEL, AIR Mann ki Baat, Bible audiobooks, etc. | Per-source permissions |
| Nirantar | No licence anywhere (no LICENSE file; README silent). arXiv CC BY 4.0 is the paper's. Public ungated tars. | T3 | hi 138; te 221 (paper Table 2) | Neither (IndicVoices lineage, redundant) | 3,240 h snapshot of the IndicVoices programme (1,530 h from IV + 1,720 h new). Its test (50 h) may be inside IndicVoices HF train. | Licence; relation to IV HF splits |
| MahaDhwani / Dhwani | None. Raw audio collected with yt-dlp from YouTube; Dhwani is URL lists. | T4 | untranscribed | Neither | Pretraining-only; not distributable. | n/a |
| Rural_Women_ASR_v2 (Hindi) | No licence tag or text. Public, ungated. (Bhojpuri sibling `Rural_Women_Bhojpuri` is CC BY-SA 4.0.) | T3 | hi 30,827 clips, ~90 h (E from 31.4 GB); te 0 | Neither until licensed | Hindi rural-women phone speech, human transcripts, noise tags. Gap-filler if licensed. | Licence |
| indicvoices-cleaned | No card, no licence. Text-only TSVs (`correction`/`clean_output` columns). | T3 | text only | Neither | Undocumented derivative of IndicVoices text. | Provenance, licence |
| IndicCMix | MIT (HF YAML + card). Audio is F5-TTS synthetic English; source of the 104,809 English sentences and the translating model not stated. | T3 | 0 real speech | Neither (text idea only) | Native-script code-mixed text with English left in Roman is a useful template for synthetic code-switch text, but provenance is unstated. | Source of English sentences; LLM licence for outputs |
| (non-AI4Bharat) Sarvam Indic DiarBench | CC BY 4.0 (HF YAML + card), ungated | T2 (YouTube part) | hi 10.7; te 9.3 | Eval only | Conversational code-mixed eval, two transcript formats (native-script, and normalised with English in Roman and Arabic digits). Matches our output spec. | n/a |

Tier justification for the main three: see sections 3.1 (IndicVoices), 3.3 (Kathbath), 3.9 (SPRING-INX).

---

## 2. Cross-cutting findings

### 2.1 Gate conditions (what is actually visible)

Method: HF dataset API JSON (`https://huggingface.co/api/datasets/<id>`) and the public HTML dataset page. Raw README is 401 for gated repos; the HTML page still renders the card body and the gate banner. [OURS]

| Repo | `gated` | `extra_gated_prompt` | `extra_gated_fields` |
|---|---|---|---|
| ai4bharat/IndicVoices, indicvoices_r, Kathbath, Shrutilipi, Lahaja, Svarah, Rasa, SpeechArenaBench, IndicCMix | `auto` | absent | absent |
| ai4bharat/IndicVoices-ST, NPTEL, Spoken-Tutorial, Mann-ki-Baat, Vanipedia, WordProject, SeamlessAlign, UGCE-Resources | `auto` | absent | Name, Email, Affiliation, Position (text) |
| Control: speechcolab/gigaspeech | `auto` | present (quoted in API) | present |

Banner text on the page, verbatim: "You need to agree to share your contact information to access this dataset" and "This repository is publicly accessible, but you have to accept the conditions to access its files and content. Log in or Sign Up to review the conditions and access this dataset content." Since no custom prompt exists in the API, "the conditions" = HF's standard contact-sharing agreement. [M] [OURS]

What I could not see: nothing blocked that matters, but I did not log in, so I have not seen HF's own modal wording after login. Coordinator action (optional): when the user accepts a gate, screenshot and date it for the manifest (CLAUDE.md data rule). Gated URLs: `https://huggingface.co/datasets/ai4bharat/<IndicVoices|indicvoices_r|Kathbath|Shrutilipi|Lahaja|Svarah|Rasa>`.

### 2.2 Public object-store copies bypass the gate [OURS]

HEAD requests (headers only, nothing downloaded) on 2026-10-12 returned HTTP 200 with no authentication:
- IndicVoices full-length audio `https://iv-release.objectstore.e2enetworks.net/dmu_release/v{1..5}_<Language>_train.tgz`. Content-Length (bytes): Hindi v1 14,322,746,939; v2 17,907,042,598; v3 54,749,472,029; v4 41,575,197,894; v5 21,554,594,050 (sum ~150 GB). Telugu v1 24,415,796,161; v2 33,742,438,784; v3 43,432,199,625; v4 11,278,438,342; v5 28,364,410,065 (sum ~141 GB).
- Vistaar `https://indicwhisper.objectstore.e2enetworks.net/vistaar/kathbath.zip` (9.19 GB).
- Per README (not tested): Kathbath tars, IndicVoices-R tars (`indic-tts-public.objectstore...`), Nirantar tars, Lahaja models.
Implication: availability is not consent evidence. Use only for what the licence text permits, and log the licence snapshot, not the access path.

### 2.3 AIKosh licence fields are unreliable [M]

AIKosh pages (server-rendered, fetched 2026-10-12) show the licence and the uploader. Many are bulk uploads by Bhashini staff or a third-party foundation, not the dataset authors.

| AIKosh page | Licence shown | Author field / uploader / date |
|---|---|---|
| indicvoices.html | CC BY 4.0 | ai4bharat / Tahir Javed (AI4Bharat) / 2025-05-20; text says 23.7K h |
| indicvoices_1.html | CC BY 4.0 | AI4Bharat, IIT Madras / Parth Ranjit Singh, 1M1B Foundation / 2026-08-17 (redirected) |
| indicvoices_r.html | CC BY-ND 4.0 | IIT Madras Team / Nikhil Narasimhan (AI4Bharat) / 2025-05-09 |
| svarah.html, lahaja.html, shrutilipi (ai4bharat) | CC BY 4.0 | ai4bharat / Tahir Javed / 2025-05-20 |
| shrutilipi_ai4bharat.html | CC BY 4.0 | AI4Bharat, IIT Madras (funded by Bhashini/MeitY) / Parth Ranjit Singh, 1M1B Foundation / 2026-08-17 (redirected) |
| Kathbath Hindi test-known, test-unknown, validation | CC BY-SA 4.0 | AI4Bharat / Shailendra Pal Singh (Bhashini) / 2025-02-24 |
| Kathbath-Hard Hindi, Kathbath Telugu, Gramvaani Hindi, Common Voice Hindi, IndicTTS Hindi, IITM Hindi eval | CC BY-SA 4.0 (all) | "Microsoft" / Shailendra Pal Singh / 2025-02-24 |
| IndicTTS Phase 3 Hindi female, Telugu male, Telugu female | CC BY 4.0 | SMT Lab IIT Madras / Utkarsh Pathak (Bhashini) / 2025-08 |
| SPRING-INX Hindi, Odia, Tamil | CC BY 4.0 | SPRING LAB IITM / Gokulapriya (Bhashini) / 2025-11 to 2025-12 |

The 2025-02-24 bulk upload stamps CC BY-SA 4.0 on Gramvaani (which SLR118 says is academic-use-only) and Common Voice (CC0), which shows the label is a blanket default and not a per-dataset legal review. Decision: AIKosh licence fields carry low authority; use them as secondary evidence and as a list of questions to ask.

### 2.4 AI4Bharat website and GitHub

- `https://ai4bharat.iitm.ac.in/datasets/<name>` pages are placeholders: "We are currently moving all our datasets to HuggingFace, Datasets will be accesible soon." Footer: "© 2024 AI4Bharat. All rights reserved". `/datasets/kathbath` and `/indicvoices_r` return 404 to my fetch; a web-search snippet (not fetched by me) claims the IndicVoices-R page lists CC-By-4.0 [U]. Treat the website as having no licence text.
- `admin.models.ai4bharat.org/datasets/` (public JSON API behind the site's catalogue): `license: []` for every speech dataset. Its description still says IndicVoices has 12000 h / 3200 h transcribed / 22563 speakers / 208 districts (stale).
- GitHub (LICENSE presence, raw files checked): IndicVoices none; Lahaja none; Svarah none; Rasa none (README says CC-BY-4.0); IndicVoices-R `LICENSE.md` = full CC BY 4.0 text; IndicSUPERB `LICENSE` = Apache-2.0 (README: code/models MIT); MahaDhwani MIT; Nirantar none; SRUTI none; Vistaar MIT with the "fine-tuned language models" limitation.

### 2.5 Consent evidence (primary-source wording)

| Collection | What participants were told | Source |
|---|---|---|
| IndicVoices | "Purpose of Data Collection: Your data will be utilized for both commercial and non-commercial purposes to enhance speech technology for your language." Also: coordinators explain purposes and compensation, signed consent form, Institute Ethics Committee approval, compensation at local daily-wage level. | arXiv 2403.01926v1 Appendix B and section 10 (Ethics) [M] |
| IndicVoices-R | Inherits IndicVoices: "anonymized speech from its parent dataset IndicVoices and is released under the same CC BY 4.0 license ... obtained explicit consent from each participant". | arXiv 2409.05356 section 6 [M] |
| Kathbath | "each participant understood that his/her voice samples were being collected for research purposes and that the data will be publicly released and used for building AI models." Terms shown in the Karya app before recording. Not explicit about commercial use. | arXiv 2208.11761 section 3 [M] |
| Lahaja, Svarah | Papers describe recruitment/paid speakers; no consent or licence wording found in the text I read. [U] | arXiv 2408.11440, 2305.15760 |
| SPRING-INX | Speaker IDs protected; vendors under tender; "legally sourced". No consent wording in paper. [U] | arXiv 2310.14654 |
| Shrutilipi | Not applicable (broadcast archive). | arXiv 2208.12666 |

### 2.6 Transcript conventions (what I could verify)

- IndicVoices family (IndicVoices, IV-R, Lahaja, Nirantar, Rasa partly): human maker-checker-superchecker transcription in Shoonya, two levels: Level 1 verbatim ("using the corresponding grapheme") and Level 2 standardised to textbook spelling; 89 noise tags (arXiv 2403.01926 sec 6, Table 13). HF fields: `text`, `verbatim`, `normalized`, `unsanitized_verbatim`, `unsanitized_normalized`, `verification_report` + speaker/demographic metadata. [M]
- The released cleaning script (`github.com/AI4Bharat/IndicVoices/data_prep_scripts/utils_dataset_clean.py`) builds `text` by NFKC normalising, stripping noise tags and punctuation (`? , : ; ! " - /` and sentence-enders such as `।` and `.` become spaces), then rejects any utterance containing characters outside a per-language character dictionary (`artifacts/dictionaries/hi.dict.txt`, `te.dict.txt` contain only that script; I checked: no Latin letters) or the `<unintelligible>` tag. [M] So the cleaned `text` field has no Latin script by construction.
- Public-preview check [OURS]: first 100 rows of the public mirror `SPRINGLab/IndicVoices-R_Hindi` (same schema as IndicVoices; a mirror of gated data, I read only the text columns): 0 rows with Latin letters, 0 with digits, 0 with punctuation; English words appear in Devanagari (e.g. "हाइवेस्टर"); `verbatim` and `normalized` differ in spelling ("घायो" vs "गायों"). Telugu not previewable (no public mirror). The Lahaja paper states the convention explicitly: "All transcripts are generated in the native Devanagari script of Hindi" and describes code-mixed content "written in Devanagari script, as is the case in code-mixing" (sec 2.3, M4 experiment). [M]
- Numbers: spelled as words in the previews and in Kathbath's IndicSUPERB transcripts (`transcripts_n2w`). Digit handling in IndicVoices Telugu: [U].
- SPRING-INX: AIKosh says "native-language text naturally incorporates Romanised and English words"; paper sec 4.3: English words extracted and spelling-corrected through a manual mapping (so English is retained, mostly in Latin); tags and non-printable characters removed. Public-preview check [OURS] (first 100 rows each): Gujarati R1 90/100 rows contain Latin tokens (e.g. "custom validater જોઈએ છે custom validater પર double click આપી છે"), Bengali R1 53/100, Marathi R1 0/100 (read news sentences with punctuation). Convention is therefore vendor- and language-dependent. Hindi not publicly previewable (not on HF). [OURS]
- Kathbath: sentences 8-15 words from IndicCorp restricted to "alphanumeric characters only"; read speech; no code-mix; Malayalam text corruption reported (HF discussion). [M]
- Svarah: transcription "same transcription guidelines as used for the Switchboard corpus". [M]
- Indic DiarBench (Sarvam): two formats, native-script and normalised (English in Roman, Arabic digits). [M]

### 2.7 Corrections to the earlier note (`datasets_licenses.md`, 2026-10-08)

1. "Gate-condition text only visible when logged in": incorrect for AI4Bharat sets. There is no custom gate text (section 2.1).
2. IndicVoices "7.3k in paper": paper (arXiv v1, 2024-03-04) says 7,348 h total / 1,639 h transcribed / 16,237 speakers / 145 districts. "12k" is the GitHub README and AI4Bharat catalogue (12,000 / 3,200 h / 22,563 speakers / 208 districts). "23.7K / 11.2K" is the HF card (update 2025-12-23) and AIKosh. These are successive snapshots.
3. The earlier IndicVoices per-language estimate (Hindi ~790 h, Telugu ~480 h from examples x 6.3 s) is one end of a range; byte-size anchoring gives lower numbers (section 3.1). Needs a `duration` sum after access.
4. Shrutilipi on HF is not 6,400 h: HF totals are 2,275,044 examples / 271.6 GB (vs 4.95M sentences in the paper); Hindi 734,675 examples (paper 1.10M), Telugu 56,082 examples (paper 0.43M). The Vistaar-train numbers (1,620 h Hindi, 390 h Telugu) are the paper's, not what HF hosts now. [M]/[E]
5. IndicTTS on AIKosh: the three Phase-3 pages I fetched (Hindi female, Telugu male, Telugu female) are CC BY 4.0, not BY-SA. The BY-SA seen earlier is on the 2025-02-24 Bhashini bulk upload of Vistaar benchmark copies, which also include an "IndicTTS Hindi" benchmark copy.
6. SPRING-INX is also on AIKosh as Hindi/Odia/Tamil pages (CC BY 4.0), with Hindi R1 and R2 tar files (37.87 GB); the "Hindi 351 h" is Phase-1 paper Table 1.
7. Kathbath HF contains clean train+valid only (no test-known/unknown, no noisy). The earlier note treated HF hours as the full 1,684 h figure for 12 languages.

---

## 3. Dataset sections

### 3.1 IndicVoices (`ai4bharat/IndicVoices`)

Sources and licence stated

| Source | URL | Licence / statement |
|---|---|---|
| HF API tags + cardData | https://huggingface.co/api/datasets/ai4bharat/IndicVoices (sha c96f9088..., lastModified 2026-06-15) | `license:cc-by-4.0` |
| HF card body | https://huggingface.co/datasets/ai4bharat/IndicVoices | "This dataset is released under the CC BY 4.0." (link creativecommons.org/licenses/by/4.0/) |
| Paper | https://arxiv.org/abs/2403.01926 (HTML v1) | "the dataset will be released with CC-BY-4.0 license" and "allowing commercial usage" (Ethics footnotes). Participants told "both commercial and non-commercial purposes". |
| GitHub | https://github.com/AI4Bharat/IndicVoices | No LICENSE file; README stale (12,000 h) |
| AI4Bharat site / catalogue | ai4bharat.iitm.ac.in/datasets/indicvoices; admin.models.ai4bharat.org/datasets/ | placeholder; `license: []` |
| AIKosh | .../indicvoices.html, .../indicvoices_1.html | CC BY 4.0 (both) |

Conflicts: none on licence (all agree CC BY 4.0). Conflicts exist only in hour/speaker figures (snapshots). Authoritative: HF YAML + card (the live distribution) corroborated by paper. Decision: T1.

Gate: HF auto-gate, contact info only (section 2.1). Full-length audio archives are public (section 2.2).

Provenance and risk
- Recorded by AI4Bharat/IIT Madras through paid local mobilisers and coordinators in 400+ districts (Karya-based Android app), ethics committee approved, signed consent forms. Sponsors: Bhashini, MeitY, Nilekani Philanthropies. [M]
- Prompts: read speech = 9K Wikipedia sentences (13 domains) manually translated into 22 languages by in-house translators; voice-assistant tasks = 9K English MASSIVE utterances translated colloquially "which contains code-mixing" and localised; digital payments (9.4K), grocery (9.3K) and government-services (9.2K) template instructions; 2.5K extempore questions with hints written with journalists/linguists (some assisted by ChatGPT); role-play scenarios. [M] Residual risk [E]: the read portion (8%) speaks human translations of Wikipedia sentences (CC BY-SA source text); the MASSIVE-derived prompts inherit MASSIVE's licence (not verified [U]). These are short prompts, not the speech, and I rate them minor.
- Another residual: the commercial-use consent wording is documented for the v1 collection (Appendix B); later phases (to 23.7K h) are [U] though presumably the same app flow.
- Legal commentary: none found specific to IndicVoices. Voice plus demographic metadata (age band, gender, district, occupation, qualification, speaker IDs) is personal data under India's DPDP Act; not researched here.

Content
- Totals (HF card, 2025-12-23): 23.7K h total, 11.2K h transcribed, 51K speakers, 400+ districts, 22 languages; 8% read / 76% extempore / 15% conversational. No English config (22 Indian languages only). [M]
- Hindi: 450,690 examples (train 445,160; valid 5,530). Telugu: 272,601 examples (train 269,306; valid 3,295). Whole set 6,379,012 examples, 739 GB. [M from HF API]
- Hours [E]: HF does not state per-language hours. A user in HF discussion #11 measured Nepali train = 467.37 h (1,076 speakers), and AI4Bharat replied that the dataset is continuously updated. Anchoring on that: Nepali train is 246,593 examples / 36.18 GB, i.e. 6.8 s/example and 77.4 MB/h. Applying it: Hindi train 524 h (by bytes) to 844 h (by examples); Telugu train 393 h (bytes) to 510 h (examples); dev ~6-10 h Hindi, ~3-6 h Telugu. Bytes-anchored total over all languages 9.5k h vs examples-anchored 12.1k h vs the card's 11.2k h; the spread shows the method error (compression varies). Use a `duration` sum after access. The Nirantar paper (mid-2025, earlier snapshot) lists Hindi 138 h and Telugu 221 h; the v1 paper Table 6 had Hindi 65 h train, Telugu 102 h. [E]
- Audio: HF stores 16 kHz mono 16-bit FLAC (HF discussion #5 metadata: codec flac, sample_rate 16000). Originals were 44.1 kHz for read/extempore and 8 kHz for conversational (IV-R paper section 3.2 and limitations). Full-length archives need downsampling to 16 kHz (GitHub README). Segments from Silero VAD, average ~9 s, max 20 s. [M]
- Recording conditions: Android phones, field/home/school/hotel, "constant buzz of fans", background noise; QC reject rate varies by language; 23 QC error categories. Speakers: age 18-60+, gender-balanced, 100-150 per district.
- Splits: HF has `train` and `valid` per language only; no `test`. The paper defines a speaker-disjoint test chosen from 20% of each district's speakers; which HF split corresponds to it is not stated [U]. If you train on `train` and eval on `valid`, speakers are probably disjoint [U].
- Distribution: HF parquet (gated) + object-store tgz for full-length audio (v1-v5 per language) + manifests. Size on disk: 739 GB HF parquet; Hindi full audio ~150 GB, Telugu ~141 GB.

Quality issues reported [M, HF discussions]: #12 (2026-10-05) Hindi valid: truncated audio vs verbatim and two speakers within one speaker ID for several clips; #5 corrupted Telugu train sample (fixed 2025-12-23); #4 text normalisation question answered with the cleaning script. Paper: speaker-ID fraud found in early collection and mitigated with a video check; coordinator over-scripting in pilots.

Usefulness for our case
- Hindi: strong. Spontaneous, many speakers, phone mic, 8 kHz conversational part gives telephony robustness. Telugu: the largest permissive Telugu set in this family (~0.4-0.5k h [E]).
- Code-switch: colloquial English insertion is built into prompts (assistant, payments, grocery, government services), but the transcript writes English words in native script. For our Latin-English output you need a native-script-to-Latin recovery step (lexicon or transliteration back) with measured error; this is a risk to track, not a blocker. IndicVoices has no English.
- Streaming: segments up to ~20 s, no punctuation/casing in `text`, which suits streaming CTC/RNNT targets; punctuation would need a separate layer.
- Overlaps: IV-R (denoised copy), IndicVoices-ST (IV audio + LLM English), Nirantar (earlier snapshot, includes test), Lahaja/Svarah read-prompt pools, SPRINGLab public mirror of IV-R Hindi (mirror of gated data with no licence tag).

What to ask: section 6.1.

---

### 3.2 IndicVoices-R (`ai4bharat/indicvoices_r`)

| Source | URL | Licence |
|---|---|---|
| HF API tags | https://huggingface.co/api/datasets/ai4bharat/indicvoices_r (lastModified 2025-03-06) | cc-by-4.0 |
| HF card | .../indicvoices_r | "License CC-BY-4.0" |
| Paper | https://arxiv.org/abs/2409.05356 section 6 | "released under the same CC BY 4.0 license" |
| GitHub | https://github.com/AI4Bharat/IndicVoices-R `LICENSE.md` | full text "Attribution 4.0 International" |
| AIKosh | https://aikosh.indiaai.gov.in/home/datasets/details/indicvoices_r.html | "Attribution-No Derivatives 4.0 International (CC BY-ND 4.0)" (uploader Nikhil Narasimhan, AI4Bharat, 2025-05-09) |
| AI4Bharat site | ai4bharat.iitm.ac.in/indicvoices_r | 404 to my fetch; a search snippet says CC-By-4.0 [U] |

Conflict and decision: four first-party sources say CC BY 4.0; AIKosh (uploaded by an AI4Bharat member) says CC BY-ND 4.0. CC BY-ND 4.0 section 2(a)(1)(B) grants only the right to "produce and reproduce, but not Share, Adapted Material" (legal code fetched 2026-10-12). IV-R is itself an adaptation (enhanced version) of IndicVoices audio, and a model trained on it could be argued to be Adapted Material under the stricter label. I treat CC BY 4.0 as the best reading (4 vs 1, and the GitHub LICENSE file is dispositive text) but keep T2 until AI4Bharat fixes AIKosh. Gate and consent as IndicVoices.

Content [M, paper Table 3 and HF]: 1,704 h, 10,496 speakers, 22 languages, 93.25% extempore, 48 kHz WAV, only the 44.1 kHz subset of IndicVoices, clips under 30 s, pipeline HTDemucs + VoiceFixer + DeepFilterNet3 + filtering. Hindi 74.60 h (4.31 read + 70.28 other; 399 speakers; HF 26,694 examples: train 26,318, test 376). Telugu 136.40 h (6.91 read + 129.49 other; 681 speakers; HF 47,547 examples: train 47,208, test 339). HF size 1.05 TB. Fields as IndicVoices plus SNR, C50, pitch, speaking rate, CER.
Usefulness: not for STT. Enhancement removes the noise/reverb we need to be robust to, and it duplicates IndicVoices. Possible later use for TTS-based synthetic data; out of scope here. The IV-R "test" split may overlap IndicVoices training speakers or utterances [U]; do not use it as an eval for a model trained on IndicVoices.
Public ungated mirror seen: `SPRINGLab/IndicVoices-R_Hindi` (no licence tag); avoid and cite the original.

---

### 3.3 Kathbath (`ai4bharat/Kathbath`) and IndicSUPERB

| Source | URL | Licence |
|---|---|---|
| HF API tags | https://huggingface.co/api/datasets/ai4bharat/Kathbath (lastModified 2025-03-07) | cc-by-4.0 |
| HF card body | .../Kathbath ("Licensing Information") | "We do not own any of the raw text used in creating this dataset. The text data comes from the IndicCorp dataset which is a crawl of publicly available websites. The audio transcriptions of the raw text and labelled annotations of the datasets have been created by us. We license the actual packaging of all this data under the Creative Commons CC0 license ("no rights reserved"). To the extent possible under law, AI4Bharat has waived all copyright and related or neighboring rights to the IndicSUPERB dataset. This work is published from: India." |
| GitHub README | https://github.com/AI4Bharat/IndicSUPERB | Same text; "code and models are released under the MIT License"; the repo LICENSE file is Apache-2.0 |
| AIKosh | Kathbath Hindi test-known/unknown/validation; Telugu benchmark | CC BY-SA 4.0 (Bhashini bulk upload 2025-02-24; Telugu page lists author "Microsoft", 341 MB, ~1,494 wavs) |
| Paper | https://arxiv.org/abs/2208.11761 | no licence statement beyond arXiv; consent wording in section 2.5 above |

Conflict and decision: HF YAML cc-by-4.0 vs HF/GitHub body CC0 (packaging) vs AIKosh BY-SA. The body text is AI4Bharat's own and more specific; CC0 is more permissive than BY, so the YAML (BY) is the more restrictive of the two AI4Bharat statements; follow BY attribution. AIKosh BY-SA is a third-party bulk label and, if applied, would add ShareAlike obligations; I rate that unlikely to be correct but unresolved (T2). Raw text: AI4Bharat expressly "do not own" it.

Provenance: audio newly recorded by paid speakers (a local coordinator hired through a data collection agency per language; DesiCrew thanked for connecting native speakers) on the Karya app (Microsoft's open-source crowd platform) during COVID; sentences = IndicCorp news/government/website text restricted to alphanumeric characters, 8-15 words, ~100K per language, each sentence read once; verification rejected ~60% in early phases; noisy set = rejected recordings with rating >=1 on accuracy/volume/quality. Consent wording: "research purposes ... publicly released and used for building AI models" (not explicitly commercial). [M]

Content [M unless E]: 1,684 h total, 12 languages, 1,218 speakers, 203 districts. Hindi clean 150.2 h + noisy 47.7 h; 58 male + 63 female speakers. Telugu clean 154.9 h + noisy 74.8 h; 53 male + 51 female speakers. Splits in paper: train; valid; test-known (5 h/lang, speakers also in train); test-unknown (3 h/lang, 10 M + 10 F unseen speakers); noisy test-known/unknown/valid. HF holds only train+valid: Hindi 94,903 examples (91,752 + 3,151), 16.3 GB; Telugu 73,052 (70,673 + 2,379), 16.7 GB. At 16 kHz 16-bit WAV (115 MB/h) that is ~141 h Hindi and ~145 h Telugu, which matches paper clean hours minus 8 h test (150.2 - 8 = 142; 154.9 - 8 = 147), so HF = clean train+valid only [E]. Test-known/unknown and noisy sets are on public tars via the IndicSUPERB README (`objectstore.e2enetworks.net/indic-superb/kathbath/...`; train 85 GB, valid 3 GB, test 2 GB each; transcripts `transcripts_n2w`).
Quality: HF discussion #3 (2025-06-28) reports errors in the first two pages of Hindi data (3 errors + 1 political sentence); #2 Malayalam consonant+virama corruption. Speaker count is small (121 / 104), which limits acoustic generalisation.
Kathbath-Hard: not on HF. Vistaar README: "Kathbath-Hard" is Kathbath test with background noise added; the paper says "We create a hard benchmark ... by adding background noise of various types to the audio files of the Kathbath benchmark". It exists only as `vistaar_benchmarks/kathbath_noisy.zip`. Distinct from the IndicSUPERB "noisy" split of rejected recordings. Third-party HF copies (e.g. `Trelis/vistaar-hi-kathbath_noisy-test`, tagged cc0-1.0) re-label it; ignore.
Usefulness: clean read news-style speech, phone-recorded. Role: supplemental Hindi/Telugu acoustic data capped at <=20% per language; Kathbath test-unknown is the community-standard comparable benchmark (needs the IndicSUPERB tar, not HF). It does not teach code-switch or conversational style.
IndicSUPERB task extras (speaker ID, LID, keyword spotting using LDC-IL words, QbE with 50 entity queries): irrelevant to STT.

---

### 3.4 Shrutilipi (`ai4bharat/Shrutilipi`)

| Source | URL | Licence |
|---|---|---|
| HF API + card | https://huggingface.co/datasets/ai4bharat/Shrutilipi | `license:cc-by-4.0`; "This dataset is released under the CC BY 4.0." |
| AIKosh | .../shrutilipi.html (AI4Bharat) and .../shrutilipi_ai4bharat.html (1M1B uploader) | CC BY 4.0 |
| Paper | https://arxiv.org/abs/2208.12666 | none; calls AIR archives "public data"/"public sources" |
| AIR copyright policy | https://www.newsonair.gov.in/copyright-policy (fetched 2026-10-12; page says Last Updated 12 Oct 2026) | "All the contents of newsonair.nic.in are Copyright protected by, NSD, All India Radio." Content may be used only for "own personal, non commercial use by anybody having access to the same". "Any other use of newsonair.nic.in content shall require the prior written permission of the News Services Division, AIR." |

Provenance [M]: audio bulletins and their PDF transcripts downloaded from AIR's site (2018-02-21 to 2021-05-17; 72,580 bulletins, 9,695 h, 12 languages), aligned at document level using CTC emissions from IndicWav2Vec and Needleman-Wunsch alignment, retained if Levenshtein similarity >= tau (6,457 h at tau 0.8, 3,239 h at tau 0.95). Hindi 1.62K h / 1.10M sentences (yield 69%); Telugu 0.39K h / 0.43M sentences (yield 47%). 4,050 pairs human-graded by 21 annotators: alignment errors mostly at segment start/end. Bulletins contain code-mixed English, music, non-transcribed clips and translated text.
Rights analysis [E, not legal advice]: both the audio and the transcript PDFs are AIR content; the CC BY 4.0 label is AI4Bharat's own and cannot license AIR's rights. AIR's page defaults to non-commercial. The Government statement (March 2026) that Prasar Bharati holds copyright in content it produces or commissions points the same way [U, from a search summary of newsonair.gov.in news item]. No AIR permission or MoU for AI4Bharat appears in the HF card, paper or AIKosh. Tier T3 leaning T4.
HF content: Hindi 734,675 examples / 97.8 GB; Telugu 56,082 / 5.7 GB; total 2,275,044 / 271.6 GB across 16 configs. At 16 kHz WAV (115 MB/h, calibrated by Kathbath above) this is ~850 h Hindi and ~49 h Telugu [E; assumes same encoding], well below the card's "over 6400 hours" and the paper's 1,620/390 h. Train-only (no valid/test). HF discussion #3 reports 3 errors (missing/cut words) in the first 10 Hindi clips.
Usefulness: formal read-news domain, studio-ish broadcast audio (not phone/laptop-mic), noisy alignment. Even if licensed, it would be a secondary source. Recommend exclusion.

---

### 3.5 Lahaja (`ai4bharat/Lahaja`)

| Source | URL | Licence |
|---|---|---|
| HF API tags (lastModified 2025-03-07) | https://huggingface.co/api/datasets/ai4bharat/Lahaja | `license:mit` |
| HF card body | .../Lahaja | "This dataset is released under the CC BY 4.0." |
| AIKosh | .../lahaja.html (Tahir Javed, 2025-05-20) | CC BY 4.0 |
| GitHub | https://github.com/AI4Bharat/Lahaja | no LICENSE, README silent |
| Paper | https://arxiv.org/abs/2408.11440 | arXiv HTML marked CC BY 4.0 (that is the paper) |

Decision: card body + AIKosh say CC BY 4.0; `mit` YAML tag is most likely a template leftover (MIT is a software licence). Either is permissive for commercial use. Tier T2 only because the labels conflict and no consent wording is published. Eval-only anyway.
Content [M]: 12.5 h Hindi (6.5 h male / 6.0 h female), 132 speakers (65 M / 67 F), 122 non-native speakers with 19 native languages, 18 states, 82-83 districts (abstract says 83, body 82), read (1K Wikipedia sentences "as released by" IndicVoices) + digital-interaction prompts + extempore. Recorded on Karya, segmented with Silero VAD, transcribed in Shoonya in Devanagari, 16 kHz mono 16-bit PCM. HF: single `test` split, 6,152 examples, 1.5 GB; fields include verbatim/normalized/text/native language/state/district. The paper notes "a significant" amount of code-mixing in the extempore speech.
Contamination: read-prompt pool and assistant/payment task templates come from the IndicVoices collection, so exact-text overlap with IndicVoices Hindi read/task utterances is likely [E]; filter by text before using Lahaja as a held-out eval. Speaker overlap with IndicVoices unknown [U].
Role: Hindi accent-robustness test; never train.

### 3.6 Svarah (`ai4bharat/Svarah`)

| Source | URL | Licence |
|---|---|---|
| HF API tags (lastModified 2025-03-10) | https://huggingface.co/api/datasets/ai4bharat/Svarah | none (no `license:` tag) |
| HF card body | .../Svarah | "This dataset is released under the CC BY 4.0." |
| AIKosh | .../svarah.html (Tahir Javed, 2025-05-20) | CC BY 4.0 |
| GitHub | https://github.com/AI4Bharat/Svarah | no LICENSE; README silent |

Decision: CC BY 4.0 by body text + AIKosh; tag missing. T2.
Content [M]: 9.6 h, 117 speakers (54 M / 63 F), 65 districts, 19 states, 19 native languages (all L2 English speakers). 1.4 h read (1K Wikipedia sentences, 9 domains), 6.4 h extempore, 1.7 h use-case prompts (grocery, UPI payments, government services). Recorded on Karya; transcribed by IIT students in a modified Label Studio with Switchboard guidelines. HF: single `test` split, 6,656 examples, 1.1 GB. Evaluations: Whisper family best; large WER gap vs LibriSpeech.
Role: the only Indian-accent English eval in this family. Too small and L2-only to train. Read portion's source sentences are Wikipedia (CC BY-SA text; minor).

---

### 3.7 Vistaar (benchmarks + training bundle)

- GitHub README (https://github.com/AI4Bharat/vistaar): "Vistaar is MIT-licensed. The license applies to all the fine-tuned language models". LICENSE file: MIT, "Copyright (c) 2023 AI4Bhārat". The licence line is explicitly about models; the data is not licensed by it. [M]
- Content: 59 benchmarks across Kathbath, Kathbath-Hard, CommonVoice, FLEURS, IndicTTS, MUCS, Gramvaani for 12 languages; train set 10,736 h (Hindi 2,150 h, Sanskrit 207 h smallest), curating 13 public datasets including Shrutilipi, NPTEL, MUCS, Gramvaani, IndicTTS, Kathbath, FLEURS, CV. Paper: "We will host these datasets in a public resource"; no licence stated. Download zips on `indicwhisper.objectstore.e2enetworks.net/vistaar/*.zip` and `/vistaar_benchmarks/*.zip` (public). [M]
- Third-party re-hosts on HF carry unrelated tags (cc0-1.0, cc-by-sa-4.0, mit, other); AIKosh copies are CC BY-SA 4.0 blanket.
- Verdict: T3 as a bundle. Contains academic-only (Gramvaani, SLR118), Microsoft-hosted MUCS (Telugu 40 h, NC per earlier note), AIR-derived Shrutilipi and NPTEL. Hindi 2,150 h is not a commercial-safe recipe. Evaluate on original test sets (Kathbath test-unknown, FLEURS test, CV test) under their own licences.

### 3.8 IndicTTS (IIT Madras SMT Lab) and its mirrors

| Source | URL | Licence |
|---|---|---|
| IITM database page | https://www.iitm.ac.in/donlab/indictts/database | unreadable from here (connection timeouts via curl and WebFetch); web-search summary: download = acceptance of "License For Use of Indic TTS"; requests by email to smtiitm@gmail.com |
| Licence PDF | https://www.iitm.ac.in/donlab/indictts/downloads/license.pdf | UNREAD. Secondary summary from a web search (not verbatim): perpetual, non-exclusive, worldwide, transferable, sub-licensable, royalty-free grant; effective on download; terminates on destroying data; Indian law; redistributors keep a copyright notice naming the 2016 TTS Consortium and IIT Madras. Section 3 and the data-grant wording were not in the excerpt. |
| AIKosh Phase-3 pages | telugu_male_mono_indictts_phase_3.html, telugu_female_mono_indictts_phase_3.html, hindi_female_mono_indictts_phase3.html | CC BY 4.0 (SMT Lab IIT Madras; Bhashini uploader) |
| HF `SPRINGLab/IndicTTS-Hindi`, `IndicTTS_Telugu` | https://huggingface.co/datasets/SPRINGLab/IndicTTS-Hindi | "This dataset is subject to the original Indic TTS license terms. Before using this dataset, please ensure you have read and agreed to the [License For Use of Indic TTS]" |
| HF discussion | https://huggingface.co/spaces/SPRINGLab/README/discussions/1 | A user asked about commercial use; maintainer `rumourscape`: "Yes, you can. There are no restrictions other than the ones stated in the given license, which includes citing the original authors in your work." (informal, 2025-03-20) |

Content: studio 48 kHz, 2 speakers per language, ~10 h per speaker; HF Hindi 10.33 h (5.16 M + 5.18 F; 11,825 utterances), Telugu 8.74 h. IITM statistics page lists Telugu with 21 and 36.71 h in unlabeled columns [U]. Verdict T3: the licence document has to be read in a browser before any use; even then it is tiny and studio-clean, so useful only as a read-speech sanity eval (Vistaar includes it). Neither for training.

### 3.9 SPRING-INX (IIT Madras SPRING Lab)

| Source | URL | Licence |
|---|---|---|
| AIKosh Hindi | https://aikosh.indiaai.gov.in/home/datasets/details/spring_inx_hindi.html (Digital India BHASHINI Division, uploader Gokulapriya, 2025-11-28) | "Attribution 4.0 International (CC BY- 4.0)" |
| AIKosh Odia, Tamil | spring_inx_odia.html, spring_inx_tamil.html | CC BY 4.0 |
| Paper | https://arxiv.org/abs/2310.14654 | "We are releasing the first set of valuable data amounting to 2000 hours ... in the public domain." No CC licence named. |
| HF `SPRINGLab/SPRING_INX_<Lang>_R1/R2` | e.g. .../SPRING_INX_Tamil_R1 | no licence tag, no card text; languages present: Assamese, Bengali, Gujarati, Kannada, Malayalam, Marathi, Odia, Punjabi, Tamil; no Hindi repo; no Telugu |
| HF `speechlab/SPRING_INX_R1` | https://huggingface.co/datasets/speechlab/SPRING_INX_R1 | Kaldi-style metadata only, no card |
| ESPnet recipe | github.com/espnet/espnet egs2/spring_speech | not fetched (404 on guessed paths) |

Decision: CC BY 4.0 (AIKosh, the only explicit licence) is more specific than "public domain", which is not a recognised dedication and could be read as either CC0-like or simply "publicly available". Use CC BY 4.0 attribution. Caveat: the AIKosh uploader is the Bhashini division, not SPRING Lab; SPRING Lab's own page (asr.iitm.ac.in) not checked [U]. Data collected by vendors "legally sourced" under a tendering process; consent not described. T2.
Content [M]: Phase 1 ~2,000 h across 10 languages (paper); AIKosh/HF say ~3,400 h (Phase 1 ~2,000 h + Phase 2 ~1,400 h). Hindi 351 h = 316 train / 30 valid / 5 test (Table 1); AIKosh Hindi has R1 and R2 tars totalling 37.87 GB (R2 hours not stated; 37.87 GB at 16 kHz WAV ~329 h, so the AIKosh Hindi package may be R1-sized or compressed [E, U]). 16 kHz (8 kHz narrow-band was upsampled; originals offered on request); monologue (read or extempore) + conversational (2-4 speakers); ~10% of conversational data intended code-mixed/code-switched (Hinglish); speakers 18-60, 10-30 min per speaker; quality control by KL University; CTC-alignment filtering; tags removed; English spellings normalised. Splits train/valid/test with 5 h test per language. Telugu: vendor collection mentions Telugu but it is not in the released 10 languages.
Public-preview findings [OURS]: Latin tokens present in 90/100 (Gujarati R1) and 53/100 (Bengali R1) first rows; Marathi R1 none. Hindi unknown.
Usefulness: the only open Indic corpus I verified that keeps English words in Latin script inside native-script transcripts, which matches our output spec for Hindi. Telugu: not available. Role: Hindi code-mix training and eval (its 5 h test is public).

### 3.10 Rasa (`ai4bharat/Rasa`)

Licence: HF YAML `cc-by-4.0`; HF card "License CC-BY-4.0"; GitHub README "License CC-BY-4.0". Consistent. Gate auto. Tier T1 for licence.
Content [M]: 1,145.44 h, 44 speaker-language pairs, 22 languages, 48 kHz mono, professional/actor speakers, neutral reading of Wikipedia and IndicTTS texts, six emotions, command prompts (Alexa, BigBasket, UMANG, DigiPay), conversations, news and book narration. Hindi: female 27.05 h + male 23.78 h (HF Hindi: train 25,713 + test 2,858 examples). Telugu: female 27.28 h + male 24.98 h (train 27,367 + test 3,043). HF discussion #4 notes the Hindi subset appeared late and a user later said only a male speaker was present [U].
Usefulness for STT: low (2 speakers per language, studio, acted). Neither.

### 3.11 BhasaAnuvaad family (`IndicVoices-ST`, `NPTEL`, `Spoken-Tutorial`, `Mann-ki-Baat`, `Vanipedia`, `WordProject`, `SeamlessAlign`, `UGCE-Resources`)

- All: `cc-by-4.0`, gated auto with Name/Email/Affiliation/Position fields; cards say "This dataset is released under the CC BY 4.0." and "Please contact us for any copyright concerns." Paper (arXiv 2411.04699) Ethics: "The code and datasets created in this work will be made available under permissible licenses." [M]
- Construction (paper): 44,400 h for 13 languages + English from (i) existing datasets (FLEURS etc.), (ii) mining from comparable sources: NPTEL (largest: 15,940.9 h En-Indic and 6,626.5 h Indic-En), Spoken Tutorial (499 h, YouTube channel), UGCE (UGC course translations), Mann ki Baat (PM's monthly radio address, transcribed and translated, manual re-recording), WordProject (Bible audiobooks, ~1,612 h), SeamlessAlign recreation (~7,500 h for 5 Indic languages), (iii) synthetic: IndicVoices verbatim transcripts translated to English by Llama-3.1-405B and spoken with TTS; English side of IndicVoices-ST is therefore synthetic speech; Indic side is real IndicVoices audio. [M]
- Rights: NPTEL: the nptel.ac.in footer reads "Distributed under Creative Commons Attribution-ShareAlike CC BY - NC - SA" (internally ambiguous: BY-SA name, BY-NC-SA code; fetched 2026-10-12); a 2014 secondary article says BY-NC-SA; treat NPTEL-derived sets as T3. Mann ki Baat audio is AIR/Prasar Bharati content. WordProject Bible audio is third-party. Spoken Tutorial and UGCE are Government/IIT content with their own terms [U].
- Usefulness: no additional ASR transcripts beyond IndicVoices; IV-ST Indic text is the `normalized` IndicVoices transcript. English audio from NPTEL has no clear licence. Recommend skipping all.

### 3.12 Nirantar (`github.com/AI4Bharat/Nirantar`)

No LICENSE file, README has no licence text. arXiv 2507.00534 is CC BY 4.0 (paper). Downloads are public objectstore tars (`nirantar/AUDIOS.tgz.aa-ae`, `LIL.tgz`, `DIL.tgz`, `LIDIL.tgz`, `*.csv`). Content [M]: 3,240 h human-transcribed, 22 languages, 208 districts; "In addition to the initial 1530 hours from IndicVoices, we collect an additional 1720 hours using the same procedure" (the abstract says 1,780 h newly released; the paper body says 1,720; arXiv abstract 3,240 vs text 3,250: small internal inconsistencies); Hindi 138 h / 490 speakers / 12 domains; Telugu 221 h / 767 speakers / 28 domains; test = max 15 min per domain, ~50 h total. Tier T3 (no licence). Redundant with IndicVoices HF; risk: its test items may be in IndicVoices HF train (contamination).

### 3.13 Other AI4Bharat/IITM speech releases found

| Item | State | Licence evidence | Note |
|---|---|---|---|
| MahaDhwani | GitHub (MIT code) | none for data | 279K h raw audio, 22 languages + English; pipeline downloads YouTube audio with yt-dlp; pretraining only; T4. |
| Dhwani (IndicWav2Vec) | GitHub URL lists | none | 17,000 h, 40 languages; URL lists only. T4 for any reuse. |
| SRUTI / Rural_Women_Bhojpuri | HF public | cc-by-sa-4.0 tag (Bhojpuri, 78.8k rows; 444 benchmark + 400 real + 78k synthetic) | Not our language. |
| Rural_Women_ASR_v2 | HF public, ungated | no tag, no text | Hindi 30,827 clips (31.4 GB, 48 kHz field recordings by rural women in MP/UP/Bihar via the Kathbath app, human-verified, noise tags, verbatim + normalised); Bhojpuri 33,616 clips. T3. |
| indicvoices-cleaned | HF public | none | text-only TSVs of IndicVoices-derived corrections; dataset viewer fails on mismatched columns; T3. |
| IndicCMix | HF gated auto, MIT | MIT (card) | 1,152,750 rows, 11 languages x ~104.8K English sentences; synthetic F5-TTS English audio; native-script code-mixed with English words left in Roman, full native, romanised casual. Source of English sentences not stated. T3. |
| SpeechArenaBench, MANGO, IndicOOV, Saffron | HF/GitHub | MIT / CC BY 4.0 tags | TTS evaluation (human ratings). Irrelevant to STT. |
| SPRINGLab mirrors: `Hindi-1482Hrs` (904,440 train / 2,566 valid, 16 kHz, 138 GB, no card/licence), `IndicVoices-R_Hindi`, `IndicTTS-*`, `speechlab/NPTEL_TECH_ENG_50` (English technical lectures, 33k clips, no licence) | HF public, no licence | none | Unlicensed mirrors/derivatives; do not use; cite originals. |
| Indic DiarBench | Sarvam (not AI4Bharat) | CC BY 4.0 | ~108 h, 22 languages; Hindi 10.7 h, Telugu 9.3 h; YouTube "in the wild" part has the usual provenance caveat; useful eval with Roman-English normalised format. |

I found no AI4Bharat "IndicST" dataset by that name (IndicVoices-ST/BhasaAnuvaad is the speech-translation family) and no separate Bhashini ASR release by AI4Bharat beyond those above and the AIKosh bulk uploads in section 2.3. No newer "IndicVoices" version than the Dec 2025 update of the HF card (lastModified 2026-06-15).

---

## 4. Overlaps and contamination map

| Pair | Relationship | Consequence |
|---|---|---|
| IndicVoices vs IndicVoices-R | IV-R = enhanced subset of IV 44.1 kHz read/extempore clips (<30 s) | Do not count hours twice; IV-R test may overlap IV train |
| IndicVoices vs IndicVoices-ST/BhasaAnuvaad | IV audio + normalised Indic text + LLM English | No new ASR value |
| IndicVoices vs Nirantar | Nirantar = earlier IV-programme snapshot (1,530 h from IV + new batches); its test is sampled per domain | Eval-leak risk if Nirantar test items sit in IV HF train |
| IndicVoices vs Lahaja/Svarah | Same collection methodology; Lahaja read sentences "as released by" IndicVoices (1K Wikipedia sentences) and shared task templates | Text-level overlap with IV training transcripts; filter test text vs training text. Speaker overlap [U] |
| Kathbath vs Shrutilipi vs Vistaar | Vistaar-train includes Kathbath and Shrutilipi; Kathbath test-known speakers are also in Kathbath train | Use test-unknown only; Vistaar's Kathbath benchmark = original Kathbath test |
| Kathbath text vs IndicCorp/Shrutilipi text | IndicCorp includes news sites; AIR bulletins are news | Possible sentence-level overlap [U] |
| IV vs `indicvoices-cleaned`, SPRINGLab `Hindi-1482Hrs` | derivative/unknown | Provenance unknown |
| SPRING-INX vs others | independent vendor collection | No known overlap |

---

## 5. Suitability summary for the three models

Transcribed hours in this family by licence status (our estimates labelled (E)):

| Language | T1 | T2 | T3/T4 (do not use) |
|---|---|---|---|
| Hindi | IndicVoices ~520-840 h (E) | SPRING-INX 351 h; Kathbath ~141 h | Shrutilipi HF ~850 h (E); Nirantar 138 h (redundant); Rural_Women_v2 ~90 h (E); IndicTTS ~10 h |
| Telugu | IndicVoices ~390-510 h (E) | Kathbath ~145 h | Shrutilipi HF ~49 h (E); Nirantar 221 h (redundant); IndicTTS ~9 h |
| English-India | none | none | NPTEL-derived sets; Svarah 9.6 h is eval-only (T2) |
| Hindi-English code-switch | IV colloquial insertions (native script) | SPRING-INX (Latin script, vendor-dependent) | IndicCMix synthetic text |
| Telugu-English code-switch | IV insertions (native script, unverified for Telugu) | none | none |

Fit for streaming/laptop-mic: IndicVoices (phone-recorded, 16 kHz after downsampling, some 8 kHz telephony origin) is closest to the target channel; Kathbath is phone-recorded clean read; SPRING-INX is vendor-recorded at 16 kHz/8 kHz; Shrutilipi is broadcast studio audio. None is laptop-mic.

Required preprocessing: (1) re-map native-script English words in IndicVoices/Kathbath to Latin using an English lexicon plus a back-transliteration model, and measure the error on SPRING-INX and DiarBench where Latin ground truth exists; (2) policy for digits (words in sources); (3) strip noise tags; (4) dedupe by text across IV, Lahaja, Svarah, Nirantar before using any as eval; (5) log the licence snapshot per dataset in the data manifest.

Suggested use (proposal [P], consistent with CLAUDE.md: log a decision in progress.md before changing pipeline.md): treat IndicVoices as T1 backbone, SPRING-INX and Kathbath as capped T2 supplements (<=20% per language), exclude Shrutilipi, Vistaar bundle, Nirantar, mirrors and unlicensed HF sets, and evaluate on Svarah (English), Lahaja (Hindi accents), Kathbath test-unknown, SPRING-INX test and Indic DiarBench.

---

## 6. What to ask AI4Bharat / IITM in writing (outward communication needs the user's go-ahead first)

6.1 IndicVoices (contacts on HF card: Tahir Javed tahir@cse.iitm.ac.in, Mitesh M. Khapra miteshk@cse.iitm.ac.in): (a) confirm CC BY 4.0 covers audio, transcripts and metadata for commercial training and shipping of derived model weights, with required attribution string; (b) confirm the participant consent script (including the "commercial and non-commercial" clause) applied to all collection phases up to 23.7K h, and that coordinators' consent forms are on file; (c) confirm that the Wikipedia-derived read prompts and MASSIVE-derived prompts impose no ShareAlike/other conditions on the speech; (d) per-language transcribed hours and speaker counts for the current HF release; (e) which HF split is the held-out speaker-disjoint benchmark; (f) licence of `verification_report`, `unsanitized_*` fields and the full-length v1-v5 archives (including untranscribed audio); (g) position on voice data under India's DPDP Act; (h) fix GitHub (add LICENSE) and AI4Bharat site.
6.2 IndicVoices-R: which is correct, CC BY 4.0 or CC BY-ND 4.0 (AIKosh); fix whichever is wrong; whether IV-R test speakers/utterances occur in IndicVoices train.
6.3 Kathbath: which of CC0 (packaging) / CC BY 4.0 governs; confirm commercial reuse of IndicCorp-derived sentences and recordings given the "research purposes" consent wording; location of test-known/unknown and noisy splits; AIKosh CC BY-SA label correction.
6.4 Shrutilipi: whether AIR/Prasar Bharati (News Services Division) granted written permission for commercial ASR training and redistribution; which tau/slice is on HF (2.28M examples vs 4.95M sentences).
6.5 SPRING-INX (IITM SPRING Lab, Prof. S. Umesh; also Bhashini): which licence governs (CC BY 4.0 vs "public domain"); vendor contracts and speaker consent allow commercial reuse; Hindi R2 hours and whether Hindi R1+R2 are 351 h or larger; whether Telugu and Indian English will be released; the transcript convention for English words in Hindi.
6.6 Lahaja/Svarah: fix licence tags (Lahaja `mit`, Svarah missing); consent text; speaker/text overlap with IndicVoices.
6.7 IndicTTS (smtiitm@gmail.com): send the full licence text; confirm commercial use and the grant wording; confirm CC BY 4.0 on AIKosh matches.
6.8 Nirantar, Rural_Women_ASR_v2, indicvoices-cleaned, IndicCMix: add licences and provenance; relationship to IndicVoices splits.
6.9 BhasaAnuvaad mined sources: per-source permissions (NPTEL, Mann ki Baat/AIR, WordProject, Spoken Tutorial, UGCE, SeamlessAlign).

---

## 7. Items the coordinator may need from the user (browser/login)

1. IITM "License For Use of Indic TTS" PDF (https://www.iitm.ac.in/donlab/indictts/downloads/license.pdf) and database page: not reachable from this environment (timeouts). Needs a browser read and verbatim capture.
2. After any HF gate acceptance: screenshot the gate text with date for the manifest (it will be the default contact-sharing text).
3. A `duration`-sum per language for IndicVoices Hindi/Telugu (needs access) to replace the hour ranges in section 3.1.
4. First 100 Hindi rows of SPRING-INX (AIKosh requires registration to preview/download) to confirm Latin-script English convention for Hindi.
5. NPTEL's formal licence page (the homepage footer is ambiguous).

---

## 8. Source log (all fetched 2026-10-12 unless stated)

- HF APIs: huggingface.co/api/datasets/ai4bharat/{IndicVoices, indicvoices_r, Kathbath, Shrutilipi, Lahaja, Svarah, Rasa, IndicVoices-ST, NPTEL, Spoken-Tutorial, Mann-ki-Baat, Vanipedia, WordProject, SeamlessAlign, UGCE-Resources, SpeechArenaBench, IndicCMix, MANGO, Rural_Women_ASR_v2, Rural_Women_Bhojpuri, indicvoices-cleaned}; SPRINGLab/*; speechlab/*; sarvamai/indic-diarbench; control repos ARTPARK-IISc/Vaani, speechcolab/gigaspeech (to confirm gate prompts appear in the API). HF discussions API for each AI4Bharat repo.
- HF dataset HTML pages (card bodies of gated sets) and raw README for non-gated sets.
- GitHub raw: AI4Bharat/{IndicVoices, IndicVoices-R, IndicSUPERB, Lahaja, Svarah, Rasa, Nirantar, MahaDhwani, Sruti, vistaar} READMEs and LICENSE files; IndicVoices `data_prep_scripts/utils_dataset_clean.py` and `artifacts/dictionaries/{hi,te}.dict.txt`. The GitHub API hit rate limits (so a few LICENSE detections rely on raw file existence).
- arXiv HTML: 2403.01926, 2409.05356, 2208.11761, 2208.12666, 2408.11440, 2305.15760, 2305.15386, 2310.14654, 2411.04699, 2507.00534.
- AIKosh dataset pages listed in section 2.3.
- AIR copyright policy (newsonair.gov.in/copyright-policy); NPTEL homepage footer; creativecommons.org/licenses/by-nd/4.0/legalcode.en.
- admin.models.ai4bharat.org/datasets/ (JSON), ai4bharat.iitm.ac.in/datasets/* (placeholders).
- Public viewer previews (first 100 rows, text columns only): SPRINGLab/IndicVoices-R_Hindi, SPRINGLab/SPRING_INX_{Marathi,Gujarati,Bengali}_R1.
- HEAD only (no download): iv-release.objectstore.e2enetworks.net IndicVoices tgz; indicwhisper.objectstore.e2enetworks.net/vistaar/kathbath.zip.
- Web searches used for: AIKosh page discovery, IndicTTS licence summary (secondary), NPTEL licence discussion (secondary), Prasar Bharati statement (secondary). Secondary-only claims are marked [U] above.
