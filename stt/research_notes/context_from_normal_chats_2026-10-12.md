# Context handoff from the user's normal Claude chats (pasted by the user on 2026-10-12)

> Source: pasted by the user into the Claude Code session, summarising earlier chats held "while I was away" (a chat sandbox with no general internet access). Stored verbatim for the project record. **Items marked [UNVERIFIED] / [TODO for Claude Code] are the original chat's own flags.** This is user-supplied material, not verified research. See `progress.md` A-015 and Q17-Q23 for how it relates to the rest of the project.

---

Project Context: Edge STT for English, Hindi, Telugu
Paste this at the start of a new chat. It summarizes a long earlier conversation. Items marked [UNVERIFIED] came from memory, an earlier research doc, or a screenshot and should be checked before relying on them. Items marked [TODO for Claude Code] are things the earlier chat could not do because its sandbox had no general internet access (it could reach GitHub, PyPI and npm only; no LinkedIn, no Hugging Face, no web search).

## 1. Problem statement
I'm an intern building speech-to-text (STT) for my company.

* Languages: English, Hindi, Telugu.
* Three separate monolingual models, one per language (senior's explicit requirement: "Telugu gets its own TTS and STT, and Hindi and English too").
* Edge deployment: phones and laptops. Models must be small enough and run on CPU.
* Commercial use, so accuracy must be high and every dataset and base-model licence must allow commercial use.
* Deliverable right now: a pipeline my senior can approve before building starts.
* Everything done so far is design and research only. Nothing has been trained or built.

### Compute (discrepancy to resolve)

* I told the earlier chat: 8x NVIDIA A10 (24 GB) on AWS, budget tight.
* My senior's WhatsApp says: "dgx level setup with 8 A100s".
* Confirm which it is. It changes batch sizes and whether a 600M model fits comfortably.

### Still unknown (ask or decide)

* Is streaming (live transcription) required, or is offline/chunked fine?
* Accuracy and latency targets (WER/CER, time to first word).
* Which phones/laptops specifically (RAM, CPU).
* Is TTS also in my scope, or only STT?
* Output policy: native script plus Latin English, or something else? (see section 6)

## 2. Senior's position (from WhatsApp, 9 Oct)

* Wants it done with Kyutai's architecture ("versatile on many devices, per Reddit buzz").
* Believes Prasad trained on a consumer RTX GPU with ~120 hours of data and got good results.
* Believes we can "take the exact same thing and swap in Telugu data" and have a PoC in "an hour or two" on 8 GPUs.
* Believes an STT code release exists in the pocket-tts repo.
* Says datasets come as audio + transcript pairs, already clean.
* Notes his own dictation tool (Wispr Flow) only works online, so on-device is a real advantage for us.

## 3. What I found out (the key correction)
### Prasad Vittaldev's two separate projects
Source: LinkedIn post screenshots I pasted. I could not open Hugging Face links.

**A. Telugu Pocket TTS (post dated Aug 30), the Kyutai one**

* Text-to-speech, not STT.
* Built on Kyutai's Pocket TTS; he credits Kyutai "for the base model and for open-sourcing the full training pipeline".
* Trained on 124 hours of Telugu speech, 3 voices (1 male, 2 female), on a single consumer GPU at home.
* 24-layer, 316M params, int8, runs at 3.39x real time on 2 CPU cores.
* Models were "on Hugging Face shortly". Demo video only; numbers are self-reported.

**B. Svanita (STT), NVIDIA-based, not Kyutai**

* v0.1 (Sep 19): Telugu + English, FastConformer encoder + TDT decoder, ~620M params, "built on NVIDIA's Parakeet TDT architecture", CC-BY-4.0, 16 kHz mono. 3 s of audio in ~0.28 s on a desktop CPU.
* v0.2 (Sep 24): Hindi + Telugu, 622M params, CC-BY-4.0.
   * Keeps English words in Latin script: 73-74% retained on code-mixed clips (Whisper: 0%).
   * 3 s turn in ~350 ms on a desktop CPU (his claim: "10-12x real-time"; my arithmetic gives ~9x).
   * Conversational Hindi WER 23.7% vs Whisper large-v2 fine-tune 37.3%. 8 kHz telephone audio: 26.5% vs 45.2%.
   * He admits AI4Bharat IndicConformer is better at 15.5% WER.
   * No Telugu numbers, no test set named, no training data/hours/hardware stated.
* Processes 3-second "turns", so it is not true streaming.
* Not monolingual (Hindi+Telugu, or Telugu+English, in one model).

Conclusion: The "Kyutai + consumer GPU + ~120h" story applies to TTS. His STT used NVIDIA's recipe. My senior merged the two.

### Kyutai: what it does and doesn't give us

* pocket-tts (github.com/kyutai-labs/pocket-tts): ~100M-class TTS, CPU-friendly, MIT, built on Kyutai's CALM approach (continuous audio latents). Has training code for new-language TTS. Does not cover Hindi or Telugu out of the box. Not an STT.
* Kyutai STT (github.com/kyutai-labs/delayed-streams-modeling, "delayed streams modeling"): English/French (~1B) and English (~2.6B). In the README I read, there was inference code only; I found no STT training code. Too big for edge anyway.
* So "swap in Telugu data" works for TTS, not for STT, as far as I could verify.
* [TODO for Claude Code] Double-check the delayed-streams-modeling repo (full tree, issues, any `train` directory) for STT training code. My check was README-level only.

### Data-volume point
124 h is enough for TTS (a few clean voices). For STT it's not enough even for a PoC; my working estimate is 300+ hours with many speakers, accents and noisy conditions. This is my judgement, not a measured number.

## 4. Chosen direction (my recommendation, pending senior's approval)
Fine-tune NVIDIA's Nemotron ASR (3.5, 0.6B streaming) per language, run via sherpa-onnx, quantize to int8.

Alternatives considered:

1. Parakeet-TDT-0.6B (Prasad's base): offline model; closest replica of what he did; CC-BY-4.0 per his posts. Trained on European languages, so no Hindi/Telugu.
2. Nemotron-3.5-ASR-Streaming-0.6B: built for streaming (chunk sizes roughly 80 ms to 1.1 s), reportedly already supports Hindi, has an export path to on-device runtimes and a public fine-tuning guide. [UNVERIFIED] details come from my earlier research doc. The licence is unclear (model card and a third-party listing disagreed), so check it.
3. Small ~100-120M streaming FastConformer per language trained or distilled, which suits phones better but is more work.
4. Kyutai-style STT from scratch: no code or pretrained model, research-risk only.

Why not just ship a 600M model on phones: int8 600M is about 650 MB and needs 1 GB+ RAM, which is fine on laptops and tight on phones. A smaller student model may be needed later.
Neither Parakeet nor Nemotron covers Telugu, so both need a new tokenizer and decoder.

## 5. The 8-step pipeline (repeat per language, Telugu first as PoC)

1. Setup: pin NeMo and sherpa-onnx versions; confirm GPUs; start a licence log for every dataset and model.
2. Base-model spike (1-2 days): compare Parakeet-TDT-0.6B and Nemotron-3.5-ASR-Streaming-0.6B: read licences, test Telugu tokenization, fine-tune each briefly on ~20 h of Telugu. Pick one.
3. Data: commercially usable paired audio+text (IndicVoices, Vaani, Kathbath, Common Voice, FLEURS, etc., each licence checked; don't trust Hugging Face labels). Convert to 16 kHz mono, filter by length, normalize transcripts (Unicode, digits, punctuation), decide English-word policy, deduplicate and remove test-set overlap, write NeMo manifests.
4. Tokenizer: train a new ~1k-token SentencePiece tokenizer per language (include Latin pieces for Hindi/Telugu). Reset decoder/joint layers, keep the pretrained encoder.
5. Training: short phase with encoder frozen, then full fine-tune at low LR; bf16, SpecAugment, duration-bucketed batches, gradient accumulation if memory is tight.
6. Evaluation: private test set with real phone/laptop mic audio and varied speakers; WER and CER; noisy and code-switched clips; compare against Svanita and IndicConformer.
7. Export: ONNX, int8 quantization, check output parity with the original.
8. Packaging and device tests: VAD and chunking, versioned bundle, measure speed and memory on real phones and laptops.

Rough scale notes [UNVERIFIED estimates]: ~700 h of commercially safe Telugu data is probably the binding limit; a PoC on 100-200 h is plausible in 1-2 weeks including data prep, with training itself taking hours to a day or so. My earlier research doc estimated roughly $340 on a single A10 for a multilingual plan. Measure real throughput in week 1 instead of trusting any of this.

## 6. Code-switching and romanization
Two separate problems:

**Code-switching (English words inside Hindi/Telugu speech)**

* Output policy: Hindi/Telugu words in native script, English words in Latin script (as Svanita does).
* Tokenizers must include Latin-script pieces.
* Most datasets write English words phonetically in native script (e.g. सर्विस), so convert back with a loanword lexicon, hand-check a sample (error-prone).
* No open commercial-safe Telugu-English code-mixed speech corpus that I know of; options: mine code-mixed clips from IndicVoices/Vaani, splice monolingual clips, small amounts of synthetic audio.
* Evaluate English tokens and native tokens separately on a private code-switched test set.

**Romanization (Hindi/Telugu written in Latin letters)**

* Keep it out of training. Output native script, then convert with a rule-based transliteration step after transcription. Check licence on any transliteration library.
* Open question: does the product need native script + Latin English, or fully romanized text?

## 7. Draft message to senior (already refined)
Hey, I went through Prasad's posts properly. His Telugu TTS is built on Kyutai's Pocket TTS and trained on 124 hours, so that's where the Kyutai and consumer GPU part comes from. His STT (Svanita) is a separate model, and per his post it's built on NVIDIA's Parakeet, not Kyutai. Kyutai's own STT models are English/French only and I couldn't find any training code for them, so swapping in Telugu data won't really work for STT.
124 hours is fine for TTS since it's just a few voices, but for STT it's not enough even for a PoC. We need at least 300 hours with a lot of different speakers.
So my suggestion is to fine tune Nemotron ASR 3.5 0.6B and run it on sherpa-onnx. We'd train a new tokenizer and decoder for each language, then quantize to int8 for edge devices. One model per language, like you wanted. Before we fully commit I'll run a quick test and check the licence, since this is for commercial use.
Let me know if you're okay with this.
(Waiting on senior's reply.)

## 8. Next actions for Claude Code

* [ ] Open the Svanita model card on Hugging Face (short link from his posts: `https://lnkd.in/gmpu42-w`) and summarize: base model, training data and hours, hardware, hyperparameters, licence, files (ONNX available?).
* [ ] Open Prasad's Telugu Pocket TTS Hugging Face page if released (data sources, licence).
* [ ] Read the Nemotron-3.5-ASR-Streaming-0.6B model card and licence text (commercial use? derivatives?) and the fine-tuning guide.
* [ ] Verify whether kyutai-labs/delayed-streams-modeling contains any STT training code.
* [ ] Check licences of each candidate dataset for commercial use, and how many hours of Telugu/Hindi/English each provides.
* [ ] Set up the environment and run the base-model spike (step 2) on the GPUs once the A10-vs-A100 question is answered.
* [ ] Check whether pretrained Indic models (IndicConformer, any per-language small variants) allow commercial use, and whether they are streaming.

## 9. Working notes

* Be honest about uncertainty. Flag unverified numbers; don't present guesses as facts.
* If naming papers, repos, or model cards, verify they exist; citations from memory may be wrong.
* Earlier I uploaded a long research doc (`Edge_streaming_Indic_STT_pipeline.docx`) as background only, not a settled plan. Two `Transfer_Dock_Text` txt files I uploaded were empty.
