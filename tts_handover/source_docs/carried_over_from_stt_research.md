# TTS findings carried over from the STT research (as of 2026-10-14)

**What this file is.** While researching STT (Oct 8-13, 2026), our researchers also read Kyutai's TTS releases, Prasad Vittaldev's Telugu TTS, and TTS-suitable datasets. Those findings are copied here as a starting point for the TTS workstream. **They are researcher-compiled and have not been re-checked by us.** Labels: **[M]** read from a cited primary source; **[V]** vendor or author claim; **[E]** our estimate; **[U]** unverified. The full sources (and many more details) are in the STT folder; pointers are at the bottom.

Nothing about TTS has been trained, built, tested or listened to yet.

---

## 1. Kyutai Pocket TTS (the open starting point we know about)
- **Repo:** `github.com/kyutai-labs/pocket-tts`. Code is MIT. Weights `kyutai/pocket-tts` on Hugging Face are **CC BY 4.0 and gated**, with a prohibited-use text that must be accepted. [M]
- **What it is:** a small (~100M-class) CPU-friendly text-to-speech model based on Kyutai's CALM approach (continuous audio latents). It is **TTS only: no speech-to-text code in the repo.** [M]
- **Training code was released in August 2026** [M]: data preparation, forced alignment (a CTC aligner), a 4k SentencePiece tokenizer (no phonemizer), a language fine-tuning recipe (`finetune_language.yaml`) and a depth-distillation recipe (`depth_distill.yaml`, shrinks the 24-layer teacher to a 6-layer student).
- **Data guidance from Kyutai** [M]: about **100 hours minimum**, **200 hours "speaks"**, **2,000 hours "sounds good"**. Kyutai's own Czech run used 976 h and reached 12% WER with Whisper as the judge by 10k fine-tune steps. Their timing table: 8x H100 does about 10 steps per second on the 24-layer teacher; **speed on A10/A100 is unmeasured.**
- **CPU speed** [V]: Kyutai claims about 6x real time on a MacBook Air M4 using 2 cores. Community Hindi builds measured 3.7x to 6.3x real time on one CPU thread (server/desktop CPUs, not laptops). ONNX, int8 and mobile ports exist.
- **Licence caveats** [M/U]:
  - Two default voices (`cosette`, `jean`) come from non-commercial datasets (Expresso, EARS).
  - The non-English default voices have no licence statement. An open issue (DSM #180, opened 2026-10-10) asks about the French voice's CC0 status and was unanswered.
  - The weights are CC BY 4.0, but Kyutai's own STT fine-tune mix included non-commercial data; whether anything similar applies to the TTS training data is unknown.
  - A different Kyutai model, Hibiki-zero, is CC BY-NC-SA (non-commercial).
- **Community builds** [V]: Hindi `saryps-labs/pocket-tts-hindi` (932 h, a 400k-step teacher trained from scratch plus 200k steps of distillation; 23.3% WER under the same judge where real speech scores 26.7%; 3.7x real time on one CPU thread), Hindi/Hinglish `Indus-Labs/indus-pocket-tts` (~90 h, single voice), Hindi/Hinglish "Jugnu" (647 h), and the Telugu model below.
- **What the senior believed** (WhatsApp, 9 Oct, relayed second-hand): "take the exact same thing and swap in Telugu data and have a PoC in an hour or two on 8 GPUs." Researcher view: for TTS the **GPU part** of a Telugu teacher fine-tune is plausibly under an hour at Kyutai's published H100 step rates [E], but the real work is **aligned, licence-clean Telugu data, a Telugu aligner, tokenizer/EOS/punctuation fixes, and a listening test**, which takes days.

## 2. Prasad Vittaldev's Telugu Pocket TTS
- **HF page:** `prasadvittaldev/pocket-tts-telugu-female-syspin`; MIT per its card; created 2026-09-02; 0 downloads when checked. [M]
- **What is actually published:** a **6-layer, ~110M-parameter, single fixed-voice student** distilled from a 24-layer Telugu teacher; **5.5x real time on a desktop CPU with int8** [V]. The teacher (likely the "316M, 3.39x on 2 cores" in his LinkedIn post) is **not published**, and there are **no "3 voices"** on the card. [M]
- **Recipe from the card** [V]: Kyutai's English 24-layer teacher fine-tuned on **124 h of Telugu** (15k steps), forced-aligned in native Telugu script, then depth-distilled for 40k steps on **one speaker (53 h)**.
- **Data credited** [M]: `SPRINGLab/IndicTTS_Telugu` (about 8.7 h; IIT Madras licence PDF unread) and `arpit-tiwari/syspin-telugu-tts` (a third-party SYSPIN re-upload with no licence). **The 124 h is not fully accounted for.** The card says "check the dataset pages above before commercial use".
- **Quality is unmeasured:** no WER, no MOS or listening scores, only demos and self-reported speeds. A related note from the Telugu author: Meta's MMS aligner is unusable for Telugu (it romanises).
- **Tamil voice by the same author** uses unspecified audiobook audio, which is the riskiest provenance. [M]
- **Svanita** (his STT) is a separate NVIDIA-Parakeet fine-tune, not Kyutai-based; see the STT folder.

## 3. Datasets that could suit TTS (clean, single-speaker, studio-style)
| Dataset | What it is | Licence (as found) | Caveats |
|---|---|---|---|
| **SYSPIN** | Studio single-speaker; Hindi ~119 h, Telugu ~115 h, one male + one female voice each [per discovery note]; Indian English (SYSPIN/LIMMITS) ~80 h | CC BY 4.0 on AIKosh [per discovery note] | **Conflicting notes:** an earlier note found no licence for SYSPIN; Prasad used a third-party re-upload with no licence. Verify at the source before use. Indian-English portion has no stated licence. |
| **Rasa** (AI4Bharat) | Expressive speech; Hindi ~51 h, Telugu ~52 h; 2 speakers per language | CC BY 4.0, consistent across sources | Studio data, small speaker count |
| **IndicTTS** (IIT Madras) | Classic studio TTS corpus; Telugu ~8.7 h in the SPRINGLab copy | **Licence text unread** (the PDF was unreachable); AIKosh Phase-3 Hindi/Telugu pages say CC BY 4.0 | Small; licence needs reading at the source |
| **IndicVoices-R** | TTS-oriented set derived from IndicVoices; Hindi ~75 h, Telugu ~136 h | HF: CC BY 4.0; AIKosh: CC BY-ND 4.0 (**conflict**) | Treat as ambiguous until resolved; overlaps IndicVoices |
- ASR-style sets (IndicVoices, Vaani, RESPIN, Common Voice) are **noisy or multi-speaker** and not ideal for single-voice TTS, but RESPIN/IndicVoices-style data can help teachers learn pronunciation (our inference [E]; not tested).
- No Telugu-English or Hindi-English **TTS** corpus was found.

## 4. Things we do not know yet (TTS)
Which languages and how many voices; whether voice cloning is wanted; target devices; quality target and how it will be judged; deadline and budget; whether new voice recordings (with consent) are possible; the voice-licence position for any voice we ship. These are tracked as open questions in `tts/progress.md`.

---

## Where the full details are (relative to this folder)
- `../../stt/reports/Svanita Kyutai and dataset licence audit.md` (Section 4: Kyutai; Section 3: Prasad/Svanita; Section 6: datasets; Section 10: draft licensor questions, not sent)
- `../../stt/research_notes/Svanita Kyutai and dataset licence audit/kyutai_repos.md` (full Kyutai repo and TTS detail)
- `../../stt/research_notes/Svanita Kyutai and dataset licence audit/svanita_prasad.md` (Prasad's TTS and STT, author facts)
- `../../stt/research_notes/Svanita Kyutai and dataset licence audit/datasets_discovery_inventory.md` and `datasets_ai4bharat.md` (SYSPIN, Rasa, IndicTTS, IndicVoices-R)
- `../../stt/research_notes/context_from_normal_chats_2026-10-12.md` (the senior's claims and the owner's earlier chats)
- `../../stt/progress.md` (the STT log, with all decisions and the evidence conventions)
