# TTS Pipeline v1: low-cost, per-language, on-device text-to-speech (Telugu first)

| | |
|---|---|
| **Document** | `tts/pipeline.md` |
| **Date** | 2026-10-14 |
| **Status** | PROPOSED. Not approved by the senior. Nothing started. **Several inputs are assumed, see Section 1.** |
| **Log file** | `tts/progress.md` (record every action, decision and number there) |
| **Evidence labels** | **[M]** read from a cited primary source; **[V]** vendor or author claim; **[E]** our estimate; **[P]** our proposal; **[U]** unverified. Everything about our own training speed, hours and cost is [E] until the spike measures it. |

---

> ## REVISION v1.2 (2026-10-14): DEADLINE UNDER ONE WEEK, HINDI FIRST (overrides the day counts and language order below)
> - **Language order:** **Hindi first, Telugu as a stretch** (decision TD-006). Reasons: Hindi has strong, permissively licensed Wav2Vec2-CTC models for alignment (Harveenchadha Hindi Wav2Vec2 models, Apache-2.0 tag; AI4Bharat IndicWav2Vec, MIT), whereas Telugu aligners are weaker (an Apache-2.0 XLSR-53 Telugu model reports ~45% WER; IndicWav2Vec Telugu is MIT); our speech-recogniser judge (IndicConformer) is far more accurate on Hindi (~14 WER) than Telugu (~26), so Hindi scores are more trustworthy; community Hindi Pocket TTS models exist as baselines (one trained on only ~90 h). Telugu has Prasad's recipe as precedent and the senior named it, so it starts as soon as the Hindi pipeline works.
> - **Hindi data:** SYSPIN Hindi (IISc official download, CC-BY-4.0) + Rasa Hindi (50.8 h, CC-BY-4.0); one SYSPIN voice (~50 h) for the student.
> - **Under-a-week schedule [P]:** Day 1 access (owner submits the SYSPIN form, accepts the Rasa gate), GPU instance and training environment, baselines; Day 2 data prep and alignment; Day 3 teacher fine-tune; Day 4 distillation; Day 5 evaluation, int8, laptop timing; Day 6 package and report, Telugu if aligned. Budget about $15-35 for Hindi, $30-60 with Telugu [E].
> - **Gate status:** the owner **accepted the Kyutai `pocket-tts` gate on 2026-10-14** (account `10xwath`).
> - **Judge fallback:** if IndicConformer (needs AI4Bharat's NeMo fork) cannot be installed quickly, use a Hindi Wav2Vec2-CTC model or Whisper as the reading-back judge.
> - **Hindi-specific text point:** Hindi sentences end with the danda (`।`); split on `।`, `.`, `?`, `!` before synthesis, for the same reason as Telugu.
>
> ## REVISION v1.1 (2026-10-14): read this first; it overrides the text below where they conflict
> After reading the primary sources in the browser pane (evidence: `evidence/2026-10-14_pages_captured_via_browser_pane.md`):
> - **Data licences resolved or narrowed.** **SYSPIN** is CC-BY-4.0 per IISc's own page (920 h, 9 languages, 18 speakers, studio 48 kHz 24-bit): use the **official IISc download** (a form the owner submits), **not** the third-party re-upload (no licence tag). **Rasa** is CC-BY-4.0 (consistent): **Telugu 52.26 h** (female 27.28 + male 24.98), **Hindi 50.83 h** (female 27.05 + male 23.78). **IndicTTS Telugu** has no licence tag on the HF page (unknown; treat as unusable until read). **IndicVoices-R** is tagged CC-BY-4.0 on HF but the AIKosh CC BY-ND conflict stands (ambiguous). Quality of the SYSPIN Hindi/Telugu data should be checked (organisers of an older release reported errors).
> - **Prasad's 124 h is most likely IndicTTS Telugu + SYSPIN Telugu (both voices)**; his student used the SYSPIN female voice, 53.0 h / 20,599 clips [derived, E]. Telugu teacher data for us: **SYSPIN Telugu ~110 h + Rasa 52.3 h = about 160 h** (IndicTTS only if its licence is confirmed); Hindi: **SYSPIN Hindi + Rasa 50.8 h**.
> - **Aligner correction:** Kyutai's README uses a **language-specific Wav2Vec2-CTC model** for forced alignment (a Telugu/Hindi one is needed; Meta's MMS aligner fails on Telugu). My earlier idea of using IndicConformer's CTC head is **not** in the README and is unproven; Step 4 must test a Telugu Wav2Vec2-CTC model first (candidates and licences not yet checked) and IndicConformer-CTC as the alternative.
> - **Official training numbers** [M, Kyutai README, 2,000 h of English, batch 64]: teacher 6.3 steps/s on 1x H100 (54 GiB peak; **~16 GB works at batch 16 with 4x gradient accumulation**), distillation 10.5 steps/s (9.8 GiB). So an **A10G (24 GB) fits**, and a 40 GB A100 fits batch 32. Prasad's 15k teacher steps are ~40 min on an H100 [E]; on an A10G expect several times longer (guess 4-5 h teacher, 6-8 h distillation per language, about $10-16 per language at g5 on-demand prices [E, unmeasured]). `finetune_language.yaml` re-initialises the text embedding and reached the same WER ~2.5x sooner than scratch on Czech [M].
> - **Always synthesize one sentence at a time** (Prasad's warning: Pocket TTS finds sentence ends using its own tokenizer tokens, which an Indic tokenizer does not produce, so long Telugu text silently drops words). Add sentence splitting (`.`, `?`, `!`) to the application and the test harness.
> - **Evaluation tools:** Kyutai's recipe scores WER with an ASR, speaker similarity with WavLM, and UTMOS (English-trained; "might be less accurate" for other languages), so our **listening test stays the real quality check**.
> - **Deployment evidence (Prasad's claims, unverified):** int8 via `pocket-tts --quantize` is about 5.5x real time on a desktop CPU; an ONNX bundle (86-139 MB) exists via `KevinAHM/pocket-tts-onnx-export` and he says it runs in sherpa-onnx on Android/iOS.
> - **Gate status:** the pane is signed in as `10xwath`; the Kyutai gate shows a prohibited-use text (voice cloning without explicit and lawful consent, deception, fake recordings, harmful content) and an "Agree and access repository" button. **The owner has not yet accepted it.** Nothing was accepted or submitted by me.

---

## 1. What this plan is, and what it assumes

**Goal.** One small text-to-speech model **per language** (Telugu, Hindi, English; senior's requirement of separate monolingual models), each a single fixed voice, that runs on a laptop CPU (and ideally a phone), built by **fine-tuning an existing open model**, with licences that allow commercial use, on a very small budget.

**Constraints carried over from the STT project** (see `../stt/progress.md`): compute is **rented on AWS**; **budget very tight** (the STT plan was costed at about $100); **open data only**; the team is under time pressure ("urgent"); every claim is labelled and logged.

**Assumptions I made because the owner has not answered yet (each is an open question TQ-01..TQ-10 in `tts/progress.md`):**
| # | Assumption | Why |
|---|---|---|
| A1 | **Telugu first, then Hindi.** English uses the existing English model as is. | The senior repeatedly named Telugu; Prasad's recipe is Telugu. |
| A2 | **One fixed voice per language** (no voice cloning in the shipped model). | Distilled small models lose cloning (Prasad's did); a fixed licensed voice is also simpler legally. |
| A3 | **Target = laptop CPU first**, phones second. | STT said laptops; devices still unconfirmed. |
| A4 | **Budget about $100 or less per language pair** and a deadline of roughly **3 weeks**. | Same constraints as STT. |
| A5 | Output is an **internal demo with listening and accuracy evidence**, not a commercially cleared release. | Licences cannot all be confirmed in 3 weeks. |

If any assumption is wrong, the plan changes where noted.

---

## 2. Are Kyutai and Prasad useful here? Yes, for TTS

| Item | How it helps | Limits |
|---|---|---|
| **Kyutai Pocket TTS** (`github.com/kyutai-labs/pocket-tts`) | **The base model and the recipe.** Released in January 2026; **training code added August 2026** [M]: data prep, forced alignment, SentencePiece 4k tokenizer (no phonemizer needed), a language fine-tune recipe (`finetune_language.yaml`) and a depth-distillation recipe (24-layer teacher to a 6-layer student). ~100M-class student, CPU-friendly. Code is MIT. | Weights `kyutai/pocket-tts` are **CC BY 4.0 and gated**, with a prohibited-use text that someone must accept. Default voices `cosette` and `jean` come from non-commercial datasets. The base model is **English-pretrained**, so Telugu and Hindi are new languages for it (Kyutai says "we simply don't know" how fine-tuning behaves on a language unseen in pretraining). |
| **Prasad Vittaldev's Telugu TTS** (`prasadvittaldev/pocket-tts-telugu-female-syspin`) | **Proof the recipe works for Telugu at small scale, and a template of settings**: teacher fine-tuned on 124 h for 15k steps, forced-aligned in native Telugu script, then depth-distilled for 40k steps on one speaker's 53 h. Also a **baseline to compare against** in a listening test, and he is a possible source of tips (public author, not contacted). | **Quality is unmeasured** (no WER or listening scores). Data provenance is unclear (about 8.7 h from IndicTTS Telugu plus a third-party SYSPIN re-upload with no licence; the 124 h is not fully accounted for). His published student is a **single fixed voice** (~110M); his 24-layer teacher is **not published**. **Do not use his weights as our base**; use them only as a baseline. |
| **Community builds** (Hindi `saryps-labs/pocket-tts-hindi` 932 h, `Indus-Labs/indus-pocket-tts` ~90 h, "Jugnu" 647 h) | Evidence about how much data is needed and how the quality looks (the 932 h Hindi model: 23.3% WER under a Whisper judge vs 26.7% for real speech). Baselines for Hindi. | Each has its own data and licence questions. |

**The senior's instinct is right for TTS** (the Kyutai route works), but "swap in Telugu data, PoC in an hour or two" is only true for the **GPU time** of the teacher fine-tune (about 40 minutes at 15k steps on one H100 at Kyutai's published rate [E]). The real work is aligned, licence-clean data, a Telugu aligner, text cleaning, and listening tests. Budget days, not hours.

---

## 3. The data (what we can use, per language)

TTS wants **clean, single-speaker, studio-style** speech. Our candidates (from the STT audit; **licences must be re-verified at the source, see Step 1**):

| Language | Source | Hours | Licence found | Status |
|---|---|---|---|---|
| **Telugu** | SYSPIN (one male, one female voice) | ~115 | CC BY 4.0 on AIKosh; an earlier note found none | **Conflict: verify** |
| | Rasa (AI4Bharat, expressive, 2 speakers) | ~52 | CC BY 4.0, consistent | Use after check |
| | IndicTTS (IIT Madras) | ~8.7 (SPRINGLab copy) | Licence text **unread** | Verify |
| | IndicVoices-R | ~136 | CC BY 4.0 (HF) vs CC BY-ND (AIKosh) | **Ambiguous; avoid until resolved** |
| **Hindi** | SYSPIN | ~119 | as above | Verify |
| | Rasa | ~51 | CC BY 4.0 | Use after check |
| | IndicVoices-R | ~75 | conflict | Avoid until resolved |
| **English** | Not needed for the model itself (Pocket TTS is English). For an Indian-accent English voice: SYSPIN/LIMMITS English ~80 h | | **no stated licence** | Skip in v1 |

**Plan for the data (per language) [P]:**
- **Teacher data** (teaches the language): all verified-licence studio data, about **120-175 h for Telugu** (SYSPIN both voices + Rasa + IndicTTS) and about **170 h for Hindi** (SYSPIN + Rasa). Kyutai's guidance is 100 h minimum, 200 h "speaks", 2,000 h "sounds good" [M]; we will be in the "speaks" range, so expect clear speech, not top naturalness.
- **Student data** (one chosen voice): **~50 h of one speaker** (Prasad used 53 h), which fixes the voice.
- **Test sentences:** about **100 sentences per language** written by us (numbers, dates, names, English words inside Telugu/Hindi, long and short sentences), not from the training data.

Disk is small (about 60 GB per 1,000 h for latents [M]), so storage cost is negligible.

---

## 4. The pipeline, step by step

Compute plan: **free tier or a cheap on-demand GPU** for the spike; **small AWS GPU instances in bursts** for training (A10G g5 at about $1.01-1.21 per hour on-demand; spot about half). No 8-GPU instance (a p4d is about $21.96 an hour). Always stop the instance when a job ends.

**Step 1. Access and paperwork (about 1-2 days).**
1. The owner decides **which Hugging Face account** accepts the `kyutai/pocket-tts` gate and reads its **prohibited-use text** (we never accept gates for you). Capture a dated screenshot into `tts/evidence/`.
2. Verify, **at the source**, the licences of SYSPIN, Rasa and IndicTTS (and resolve IndicVoices-R's CC BY vs CC BY-ND if we want it). Record them in a licence manifest.
3. Settle the **voice policy**: a fixed voice taken from licensed studio data; if anyone records a new voice, a written consent form.
4. Send nothing to anyone without the owner's go-ahead.

**Step 2. Spike: does it work at all? (about 2-3 days, ~$0-10).**
1. Run the **pretrained English Pocket TTS** on a laptop CPU: measure speed (real-time factor), first-audio delay and memory.
2. Run **Prasad's Telugu model** and the **community Hindi models** on our test sentences; **listen**; measure how well a speech recogniser reads them back.
3. Check the **training repo** runs on a small sample: data preparation, the aligner, and a few hundred training steps. **Find out the real training speed and memory on an A10G**, because we have no measured number.
4. Check the **int8 / ONNX path** (the repo has a quantization evaluation script; ONNX ports of the student exist [V]) and what runtime we will use on devices (sherpa-onnx TTS support for this model is **unverified**).
5. **Gate 1:** the repo trains on our hardware, speed and memory are known, and the baselines can be run. If the repo does not work as documented, tell the owner before spending more.

**Step 3. The yardstick (about 2 days, in parallel).**
- **Test sentences:** about 100 per language, frozen before training.
- **Accuracy judge:** an Indic speech recogniser reads the synthesized audio back and we measure the character error rate. **Use IndicConformer (hi, te) as the judge; Whisper is unreliable for Telugu.** Always compare with the same judge on **real speech from the same speaker** (the judge itself makes errors).
- **Listening test:** 8-10 colleagues rate naturalness 1-5 and do A/B against Prasad's model; include numbers, dates and English words.
- **Speed:** real-time factor, first-audio delay, RAM on the target laptop (and phone if available).
- **Proposed pass marks [P]:** judge CER within **1.2x of real speech**; average listening score **>= 3.5 / 5**; **>= 95%** of sentences with no skipped or repeated words; **>= 90%** of numbers and dates read correctly; **>= 3x real time** on the laptop CPU in int8; first audio **<= 300 ms**.

**Step 4. Prepare the data (about 3-4 days, mostly CPU, cheap).**
1. Resample to **24 kHz** mono; trim silences; remove bad clips.
2. **Clean the text:** numbers, dates and currency written out as words in the language; punctuation and sentence splitting (Indic full stops); remove symbols.
3. Build the manifest (`path`, `duration`, `transcript`).
4. **Word-level alignment:** the training needs a start and end time for every word. Use a **Telugu/Hindi CTC aligner** built on IndicConformer's CTC head (needs AI4Bharat's NeMo fork, shared with the STT work). **Meta's MMS aligner reportedly fails on Telugu**, and Whisper is unreliable for Telugu. Check a sample of alignments by ear and by eye.
5. Train the **4k SentencePiece tokenizer** on the language's text, as the repo does.
6. Pick the **student speaker** (~50 h) and set aside a validation set.

**Step 5. Fine-tune the teacher (about 1 day, ~$5-10 [E]).**
- Start from Kyutai's **24-layer English teacher**, run `finetune_language.yaml` with our manifest and tokenizer, **15k to 25k steps** (Prasad used 15k) [M/V].
- Time: about 40 minutes at 15k steps on one H100; on an A10G we expect **several times slower, roughly 3-8 hours** [E, unmeasured]; the Step 2 spike replaces this guess. Checkpoint every 15-30 minutes; stop the instance when done.

**Step 6. Distill to the small single-voice student (about 1 day, ~$5-10 [E]).**
- Run the depth-distillation recipe to the **6-layer (~110M)** model on the chosen speaker's ~50 h, about **40k steps** (Prasad's setting), then evaluate. Keep the 12- or 24-layer teacher as a fallback if the student is poor (in a Korean community run the 100M student was "quite poor" while the 300M teacher was "quite usable" [V]).

**Step 7. Evaluate (about 1-2 days).**
- Score every model against the Step 3 pass marks and against Prasad's Telugu model (and the community Hindi model for Hindi). Run the listening test. Write down failures (numbers, long sentences, English words).
- **Gate 2:** pass marks met, or a clear list of what is not.

**Step 8. Shrink and run on devices (about 2 days).**
- Quantize to **int8**, check the accuracy and listening scores did not drop, export to **ONNX**, and measure speed and memory on your laptop and phone. Fallbacks: ship the 12-layer or 24-layer model in int8 on laptops only.

**Step 9. English (about 1 day).**
- Use the **pretrained English Pocket TTS as is**, with a licensed voice. Check its default voices' licences (some come from non-commercial data) and use a consented voice prompt if a different voice is wanted. Measure quality and speed with the same yardstick.

**Step 10. Hindi (repeat Steps 4-8 with Hindi data, about 3-4 days if Telugu worked).**

**Step 11. Package and document (about 2 days).**
- Signed, versioned bundle; a **notices file** with credits (Kyutai CC BY 4.0, the datasets); a record of **voice rights** and the Kyutai acceptable-use terms; a short report with the numbers and audio samples; update `tts/progress.md`.

---

## 5. Cost (estimates; the spike will replace them)

| Item | Cost |
|---|---|
| Spike (free tier or a few hours on a cheap GPU) | $0-10 |
| Telugu: teacher fine-tune (~3-8 GPU-h) + distillation (~5-8 GPU-h) | ~$10-20 (on-demand g5, $1.01-1.21/h) |
| Hindi: same | ~$10-20 |
| Re-runs, evaluation, export | ~$10-20 |
| Storage (~100 GB for the project) | ~$5 |
| **Total for Telugu + Hindi** | **about $50-100**, Telugu alone about $25-50 |

Not priced: colleagues' time for the listening test, any recording of a new voice, legal review. **Uncertainty is large (about 3x either way)** because we have no measured A10G speed for Pocket TTS. Spot instances would roughly halve it.

---

## 6. Risks and fallbacks

| Risk | What we do |
|---|---|
| The base is English-pretrained; Kyutai says Telugu behaviour is unknown | The spike checks it early; fallback is a bigger teacher or more data; report honestly |
| Word alignment for Telugu is hard | IndicConformer-CTC aligner; check samples by ear; Prasad's recipe shows it can be done |
| Only about 100-175 h of Telugu studio data | Accept "speaks, not best"; add verified data; do not use ambiguous sets |
| Data licence conflicts (SYSPIN, IndicTTS, IndicVoices-R) | Verify at the source first; keep the demo internal until confirmed |
| Student model sounds poor (as in the Korean run) | Ship the 12/24-layer model on laptops; add data or steps |
| Numbers, names and English words read badly | Text normalisation before synthesis; a special test slice |
| Voice rights and consent | Use licensed data voices; written consent for any recorded voice |
| Kyutai gate and prohibited-use terms | The owner reads and accepts under the company's chosen account; keep the dated copy |
| Speed on phones is unproven | Measure in Step 8; laptop first |
| Our cost and speed guesses are off | Measure in the spike; re-issue the cost table |

---

## 7. What I need from the owner (open questions)
1. **Languages and order:** Telugu first, then Hindi? Is English only "use the existing model"?
2. **Voices:** one fixed voice per language? Is voice cloning wanted?
3. **Devices:** laptops, phones, both?
4. **Deadline and budget:** how many days, and is about $100 acceptable?
5. **Quality bar:** who judges (a colleague panel)? What counts as good enough?
6. **Hugging Face account** for the Kyutai gate, and who approves licences.
7. **Recording:** can we record a consented voice, or open data only?

---

## 8. How this plan connects to the logs
Every day's work, number and decision goes into `tts/progress.md` (see its Section 0). If this plan changes, log a decision (`TD-###`) first, then edit this file and note it at the top. The STT plans live in `../stt/`.
