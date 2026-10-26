# Licence and fine-tuning audit: base models, teacher models, software tools (2026-10-12)

Scope: commercial on-device Hindi / Telugu / English streaming STT (10X_STT). Read-only audit: no weights downloaded, no logins, no gates accepted, nothing sent to any licensor. Text files (README, config, tokenizer JSON, LICENSE) were read directly from public URLs. This is a technical reading of licence text, not legal advice. Counsel should confirm everything marked [U] and the "Ask the licensor" items.

Evidence labels follow CLAUDE.md: [M] measured/read from a cited primary source on 2026-10-12, [V] vendor claim, [E] my estimate, [P] proposal, [U] unverified/unreadable, [OURS] our own measurement (none in this note). The "researcher.md" instruction file named in the task did not exist at the given path (Glob found none), so I followed the task text directly.

---

## 0. Executive summary (the things that change decisions)

1. **Nemotron-3.5-ASR-Streaming-0.6B licence is OpenMDW-1.1 for the Hugging Face weights.** The "NVIDIA Open Model License" claim is explained: the HF card front-matter said `nvidia-open-model-license` for the first ~day after release (HF commit history: README at 2026-06-04 had front-matter `nvidia-open-model-license` but body text "governed by the OpenMDW-1.1"; three "Update License" commits by NVIDIA staff on 2026-06-05 21:56-21:59 UTC changed front-matter to `openmdw-1.1`). The NGC NIM container page and Together AI's listing still say "NVIDIA Open Model License" for the NIM-served model builds. Two different distribution channels, two licences; the open HF artefacts are OpenMDW-1.1 [M]. **Archive a dated copy of the HF README + licence text from the day we download** because the launch-day metadata disagreed.
2. **OpenMDW-1.1 is about as permissive as model licences get** (full text in section 2.1): free, no field-of-use limits, no share-alike, outputs unrestricted. Only real obligations: if you distribute any part of the Model Materials, keep a copy of the agreement and the notices of origin; patent/copyright-suit termination; and "you are solely responsible for clearing rights of other persons" (no IP warranty on NVIDIA's training data).
3. **Telugu is NOT in Nemotron-3.5.** It is not one of the 40 locales, not "adaptation-ready", and the tokenizer (13,087 BPE tokens) contains **zero Telugu characters** (I counted: 0 tokens in U+0C00-0C7F; 196 Devanagari tokens; byte_fallback is on but the vocab has no `<0xNN>` byte tokens, so Telugu text would map to `<unk>`). BUT the model's prompt dictionary reserves a slot `te-IN: 40` (and ta-IN 39, kn-IN 43, ml-IN 44, mr-IN 41, gu-IN 42, bn-IN 36, ...). So adding Telugu = new tokenizer + decoder retrain + fine-tune; NVIDIA publishes a tutorial notebook for exactly this (new tokenizer merge, `update_tokenizer=true`, decoder re-initialised from scratch, encoder kept). Section 4.
4. **NVIDIA's "AI Foundation Models Community License" (Parakeet-RNNT-1.1B multilingual/Indic, NGC/NIM only) is effectively disqualifying** for us: production use requires NVIDIA NIM / AI Enterprise unless a narrow exception applies, and it forbids using the model or "any output or results of them to develop or improve any other AI models" without NVIDIA's written approval. Not usable as base or teacher. No Telugu in the Indic variant anyway (bn, en, hi, ta).
5. **Indic Open Model License v1.0 (Bodhan Indic-Transcribe)** was read in full from the licensor's public GitHub. Commercial and fine-tuning allowed, but (a) any derivative given to a third party, **including shipping on end-user devices**, must carry the exact same licence (section 5, "no relicensing") and an attribution notice in the user-facing UI; (b) a model "trained substantially on Output of the Software" is itself a Derivative, so using it as a pseudo-label teacher drags our model under the licence; (c) 500M MAU / US$250M revenue ceiling; (d) hosting for third parties needs approval. Plus base model canary-1b-v2 terms (CC-BY-4.0). Not recommended as teacher unless we accept those strings. Section 5.4.
6. **IndicConformer is MIT** in the places that matter (GitHub README + LICENSE, per-language HF cards, 600M HF card body, AIKosh). The CC-BY-4.0 label is on the *template-style base repo* `ai4bharat/IndicConformer` and on community repacks. All are permissive; the safe combined reading is "retain MIT notice + attribute". The HF gate text is unreadable without login. No IndicConformer is streaming. Hindi and Telugu per-language models exist (120M encoder, hybrid CTC-RNNT). Section 5.1.
7. **Silero VAD is MIT** (LICENSE file; PyPI classifier MIT; README body says "permissive license (MIT)"). The "CC BY-NC 4.0" is the stale *alt text* of a badge whose image and link both say MIT. **TEN VAD** is Apache-2.0 plus a non-compete-with-Agora condition and an "only for your Application and your direct End Users" condition; shipping inside our own app is within its words but the non-compete clause is vague. Silero is the safe default. Section 7.
8. **Aksharamukha is copyleft** (PyPI/setup.py: AGPL-3.0; repo carries gpl-3.0.txt; inconsistent, both strong copyleft). Do not link into a shipped binary. Section 7.

---

## 1. Model-by-model verdict table

Legend for verdict: GREEN = commercial + derivative + on-device shipping clearly allowed by text I read, only notice duties; AMBER = allowed but with real strings or unreadable parts; RED = do not use for this purpose.

| Model | Params | Streaming | Languages | Licence (as read) | ONNX/sherpa | Verdict (base / teacher) |
|---|---|---|---|---|---|---|
| nvidia/nemotron-3.5-asr-streaming-0.6b | 637,997,088 (F32, HF API [M]); .nemo 2.37 GB, safetensors 2.55 GB, q8_0 GGUF 742 MB | Yes, cache-aware FastConformer-RNNT, att_context [56,{0,1,3,6,13}] = 80/160/320/560/1120 ms | 40 locales; Hindi transcription-ready; **no Telugu**; en-US, en-GB | OpenMDW-1.1 | sherpa-onnx export script + packages since 1.13.3; community ONNX/CoreML/MLX/OpenVINO/GGUF | GREEN (base and teacher) |
| nvidia/nemotron-speech-streaming-en-0.6b | 618,084,865 | Yes, att_context [70,{0,1,6,13}] | English only | NVIDIA Open Model License | sherpa-onnx since 1.12.22 [prior note, not re-checked] | GREEN-with-notice (base/teacher) |
| nvidia/parakeet-tdt-0.6b-v3 | 627,057,286 | Offline TDT; chunked "streaming" script only (buffered) | 25 European (no hi, no te) | CC-BY-4.0 | sherpa-onnx offline | Not useful for Hindi/Telugu; fine as English-ish teacher (attribution) |
| nvidia/parakeet-tdt-0.6b-v2 | ~600M (card) | Offline | English | CC-BY-4.0 | sherpa-onnx offline | GREEN (English teacher; attribution) |
| nvidia/parakeet-tdt_ctc-110m | ~110M | Offline hybrid | English | CC-BY-4.0 | NeMo hybrid exporter in sherpa-onnx (offline) | GREEN (small English teacher/baseline) |
| nvidia/parakeet_realtime_eou_120m-v1 | 120M | Streaming + end-of-utterance | English | NVIDIA Open Model License | not checked | GREEN-with-notice (EOU idea) |
| nvidia/parakeet-unified-en-0.6b | 600M | Unified offline + buffered streaming (min 160 ms) | English | NVIDIA Open Model License | sherpa-onnx 1.13.2 (buffered path) [prior note] | English only |
| nvidia/stt_en_fastconformer_hybrid_large_streaming_multi (and 80/480/1040 ms siblings) | ~114M | Yes, cache-aware hybrid CTC+RNNT, [70,{0,1,6,13}] | English only | **HF card: CC-BY-4.0; NGC page: "NGC TERMS OF USE" (unread)** | community sherpa archives; NeMo online CTC support | AMBER until NGC terms read; use the HF CC-BY-4.0 copy |
| nvidia/canary-1b-v2 | 978,998,272 | Offline AED | 25 European | CC-BY-4.0 | n/a | Not Hindi/Telugu |
| nvidia/canary-1b (original) | ~1B | Offline | en/de/es/fr | **CC-BY-NC-4.0** | n/a | RED |
| Parakeet-RNNT-1.1B multilingual / prompt / **Indic** (NGC/NIM only, not on HF) | 1.1B | NIM says streaming for multilingual; Indic profile unread | Indic variant = bn-IN, en-US, hi-IN, ta-IN (**no Telugu**) | AI Foundation Models Community License (= "NVIDIA Community Model License") | NIM container only | **RED** (see 2.3) |
| ai4bharat/indic-conformer-600m-multilingual | ~600M | **No** (offline, hybrid CTC+RNNT) | 22 scheduled incl. hi, te | MIT (+ gate, text unreadable) | Official ONNX files inside repo (assets/*.onnx), onnxruntime 1.20.1 pinned | AMBER (gate text unread) |
| ai4bharat/indicconformer_stt_hi_hybrid_ctc_rnnt_large / ..._te_... | ~120M encoder, 17 blocks, d=512 | **No** | Hindi / Telugu (one model each) | MIT (+ gate) | NeMo (AI4Bharat fork `nemo-v2` branch); community ONNX/GGUF | AMBER |
| ARTPARK-IISc/SraVaani-0.5-live | ~430M, fp16 TorchScript ~900 MB | **Yes** (cache-aware, CTC head only; [70,{0,1,6,13}]) | 63 Indian languages incl. hi, te; Urdu/Kashmiri not supported | "mit" tag + gate (text unreadable) | TorchScript only; no ONNX stated | AMBER |
| ARTPARK-IISc/SraVaani-1.0 | ~430M hybrid TDT-CTC | No (offline) | 65 languages | "mit" tag + gate | ONNX + sample script via a Google Drive link (card); fine-tune checkpoints on separate access request | AMBER |
| ARTPARK-IISc/Vaani-FastConformer-Telugu / -Hindi | not stated | Not stated (RNNT BPE in NeMo) | te / hi | "mit" tag + gate | NeMo | AMBER |
| bodhan-ai/indic-transcribe-core / flex / pro | 1,222,553,584 | No (lite sibling "real-time", gated 401, unread) | 25-27 Indian languages incl. te, hi | Indic Open Model License v1.0 (full text read) + base canary-1b-v2 terms | n/a | AMBER-to-RED (share-alike + teacher=derivative) |
| IndicWhisper (AI4Bharat Vistaar fine-tunes of Whisper, per language) | Whisper-medium class [E] | No | 12 languages incl. hi, te | MIT ("applies to all the fine-tuned language models") | whisper-style, offline | GREEN licence-wise; weak Telugu, big, no streaming |
| openai/whisper (all sizes) | 37.8M tiny ... 1.54B large-v3 | No | 99 | GitHub README: MIT ("code and model weights"); HF cards: Apache-2.0 for large-v3/small/tiny, MIT for large-v3-turbo | sherpa-onnx offline | GREEN (teacher/pseudo-labeller; weak Indic zero-shot) |
| facebook/omniASR-CTC-300M/1B, LLM-300M... | CTC 300M ~325M | No (<40 s clips) | 1,600+ | Apache-2.0 (code and models); corpus CC-BY-4.0 | none (fairseq2) | GREEN licence-wise; not streaming |
| facebook/mms-1b-all, mms-300m | ~965M | No | 1,100+ | **CC-BY-NC-4.0** | n/a | RED |
| facebook/seamless-m4t-v2-large | 2.3B | No | many | **CC-BY-NC-4.0** | n/a | RED |
| Qwen/Qwen3-ASR-0.6B / 1.7B | HF safetensors 0.94B / 2.35B | Yes (GPU-serving oriented) | 30 incl. Hindi; **no Telugu** (0 hits in card) | Apache-2.0 | GGUF/MLX community | GREEN licence-wise; no Telugu |
| mistralai/Voxtral-Mini-4B-Realtime-2602 | 4.43B | Yes, 80 ms..2.4 s delay | 13 languages incl. Hindi; no Telugu (0 hits) | Apache-2.0 | none confirmed | GREEN licence-wise; too big |
| Moonshine (moonshine-ai/moonshine; HF UsefulSensors/moonshine-tiny) | tiny 27.1M (HF) | Streaming models exist | English; non-English legacy models Arabic, Japanese, Korean, Mandarin, Spanish, Ukrainian, Vietnamese | Code MIT; models MIT "in every language and at every size" **except** the exhaustive legacy non-streaming list above = Moonshine Community License (non-commercial) | sherpa-onnx (offline) [not checked] | No hi/te evidence |
| kyutai/stt-1b-en_fr, stt-2.6b-en | 989M / 2.62B | Yes (delayed streams) | en+fr / en | Weights CC-BY-4.0 (HF tag and card line "Model weights are licensed under CC-BY 4.0") | none | licence fine; no hi/te (another researcher covers Kyutai) |
| typhoon-ai/typhoon-asr-realtime | ~114M | Real-time FastConformer-transducer | Thai | CC-BY-4.0 | n/a | precedent only |

---

## 2. NVIDIA licences, verbatim

### 2.1 OpenMDW-1.1 (full text, https://openmdw.ai/license/1-1/, read 2026-10-12)

> OpenMDW License Agreement, version 1.1 (OpenMDW-1.1)
>
> By exercising rights granted to you under this agreement, you accept and agree to its terms.
>
> As used in this agreement, "Model Materials" means the materials provided to you under this agreement, consisting of: (1) one or more machine learning models (including architecture and parameters); and (2) all related artifacts (including associated data, documentation and software) that are provided to you hereunder.
>
> Subject to your compliance with this agreement, permission is hereby granted, free of charge, to deal in the Model Materials without restriction, including under all copyright, patent, database, and trade secret rights included or embodied therein.
>
> If you distribute any portion of the Model Materials, you shall retain in your distribution (1) a copy of this agreement, and (2) all copyright notices and other notices of origin included in the Model Materials that are applicable to your distribution.
>
> If you file, maintain, or voluntarily participate in a lawsuit against any person or entity asserting that the Model Materials directly or indirectly infringe any patent or copyright, then all rights and grants made to you hereunder are terminated, unless that lawsuit was in response to a corresponding lawsuit first brought against you.
>
> This agreement does not impose any restrictions or obligations with respect to any use, modification, or sharing of any outputs generated by using the Model Materials.
>
> THE MODEL MATERIALS ARE PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND ... [full warranty disclaimer]
>
> YOU ARE SOLELY RESPONSIBLE FOR (1) CLEARING RIGHTS OF OTHER PERSONS THAT MAY APPLY TO THE MODEL MATERIALS OR ANY USE THEREOF, INCLUDING WITHOUT LIMITATION ANY PERSON'S COPYRIGHTS OR OTHER RIGHTS INCLUDED OR EMBODIED IN THE MODEL MATERIALS; (2) OBTAINING ANY NECESSARY CONSENTS, PERMISSIONS OR OTHER RIGHTS REQUIRED FOR ANY USE OF THE MODEL MATERIALS; OR (3) PERFORMING ANY DUE DILIGENCE OR UNDERTAKING ANY OTHER INVESTIGATIONS INTO THE MODEL MATERIALS OR ANYTHING INCORPORATED OR EMBODIED THEREIN.
>
> IN NO EVENT SHALL THE PROVIDERS OF THE MODEL MATERIALS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY ... ARISING FROM, OUT OF OR IN CONNECTION WITH THE MODEL MATERIALS, THE USE THEREOF OR OTHER DEALINGS THEREIN.
>
> (site footer: "Copyright The Linux Foundation and its contributors. | Site contents licensed under CC-BY-4.0")

Applied to our use case (my reading, not legal advice):

| Question | Reading |
|---|---|
| (a) Commercial use | Allowed; "deal in the Model Materials without restriction". No field-of-use, user-count, revenue, geography or hosting limits, no acceptable-use list. |
| (b) Fine-tune and distribute derivative models | Allowed; no share-alike, no requirement to use the same licence for the derivative, no naming requirement. If the derivative contains "any portion of the Model Materials" (weights are), shipping it requires keeping a copy of OpenMDW-1.1 and the notices of origin. You may add your own licence terms for your own contributions, but cannot strip NVIDIA's. |
| (c) Quantise/convert (ONNX, int8, GGUF, CoreML) and ship on devices | Same as (b): a converted copy is still a "portion of the Model Materials", so ship the OpenMDW-1.1 text + NVIDIA origin notice (e.g. in a licences screen/NOTICE file). NVIDIA itself ships a q8_0 GGUF in the repo. |
| (d) Outputs as pseudo-labels/training data | Explicitly unrestricted: "does not impose any restrictions or obligations with respect to any use, modification, or sharing of any outputs". |
| (e) Attribution | No "Built with" slogan. Notice-retention only. The HF repo has **no separate LICENSE or NOTICE file** (file listing from HF API [M]); the origin notices live in the model card and `.nemo`/README. What exactly counts as "notices of origin included in the Model Materials" is [U]; safe practice: ship the full HF README, the OpenMDW text and "NVIDIA Nemotron 3.5 ASR Streaming 0.6B, (c) NVIDIA, OpenMDW-1.1". |
| (f) Upstream/training-data caveats | Card lists training data: NVIDIA Riva multilingual ASR set (proprietary), Granary, MLS, Common Voice, FLEURS, VoxPopuli/Europarl-ASR; 10,000 to 1,000,000 h; labels partly synthetic from "NVIDIA Canary, Parakeet Multilingual 1.1B RNNT, Parakeet CTC 1.1B, OpenAI Whisper, FunASR" with punctuation/case from Qwen3-32B; no per-dataset licences listed. NVIDIA's safety.md says "dataset license constraints adhered to" [V]. OpenMDW gives us no warranty or indemnity and makes us "solely responsible" for rights clearing, so any residual risk in NVIDIA's data (e.g. YouTube-derived Granary subsets, a Canary variant with NC terms, Parakeet 1.1B under the Community licence) sits with us. Code-switching samples were in training (HF discussion #2, NVIDIA staff: "yes"). |

Patent/copyright retaliation clause: suing anyone alleging the Model Materials infringe ends our rights (low practical risk).

### 2.2 NVIDIA Open Model License Agreement (https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license/ ; "Last Modified: October 24, 2025"; read in full)

Applies to: nemotron-speech-streaming-en-0.6b, parakeet_realtime_eou_120m-v1, parakeet-unified-en-0.6b, multitalker-parakeet-streaming-0.6b-v1 (HF front-matter `nvidia-open-model-license`), and to the NIM-served Nemotron 3.5 builds.

Key verbatim clauses:

> NVIDIA models released under this Agreement are intended to be used permissively and enable the further development of AI technologies. Subject to the terms of this Agreement, NVIDIA confirms that: Models are commercially usable. You are free to create and distribute Derivative Models. NVIDIA does not claim ownership to any outputs generated using the Models or Derivative Models.

> "Derivative Model" means all (a) modifications to the Model, (b) works based on the Model, and (c) any other derivative works of the Model. An output is not a Derivative Model.

> If You institute copyright or patent litigation against any entity ... alleging that the Model or a Derivative Model constitutes direct or contributory copyright or patent infringement, then any licenses granted to You under this Agreement for that Model or Derivative Model will terminate ... If You bypass, disable, reduce the efficacy of, or circumvent any technical limitation, safety guardrail or associated safety guardrail hyperparameter, encryption, security, digital rights management, or authentication mechanism (collectively "Guardrail") contained in the Model without a substantially similar Guardrail appropriate for your use case, your rights under this Agreement will automatically terminate. ... NVIDIA may update this Agreement to comply with legal and regulatory requirements at any time and You agree to either comply with any updated license or cease Your copying, use, and distribution of the Model and any Derivative Model.

> License Grant. ... NVIDIA hereby grants to You a perpetual, worldwide, non-exclusive, no-charge, royalty-free, revocable (as stated in Section 2.1) license to publicly perform, publicly display, reproduce, use, create derivative works of, make, have made, sell, offer for sale, distribute (through multiple tiers of distribution) and import the Model.

> AI Ethics. Use of the Models under the Agreement must be consistent with NVIDIA's Trustworthy AI terms found at https://www.nvidia.com/en-us/agreements/trustworthy-ai/terms/.

> NVIDIA owns the Model and any Derivative Models created by NVIDIA. Subject to NVIDIA's underlying ownership rights ..., You are and will be the owner of Your Derivative Models. NVIDIA claims no ownership rights in outputs. You are responsible for outputs and their subsequent uses.

> Redistribution. ... If you distribute the Model, You must give any other recipients of the Model a copy of this Agreement and include the following attribution notice within a "Notice" text file with such copies: "Licensed by NVIDIA Corporation under the NVIDIA Open Model License"; ... You may add Your own copyright statement to Your modifications and may provide additional or different license terms and conditions for use, reproduction, or distribution of Your modifications, or for any such Derivative Models as a whole, provided Your use, reproduction, and distribution of the Model otherwise complies with the conditions stated in this Agreement.

> Indemnity. You will indemnify and hold harmless NVIDIA from and against any claim by any third party arising out of or related to your use or distribution of the Model, Derivative Models or outputs.

Plus: Cosmos-only "Built on NVIDIA Cosmos" clause (n/a), Separate Components, no trademarks, disclaimer, Delaware law / Santa Clara courts, export compliance.

Reading for us: commercial yes; fine-tune/derive yes; derivative may carry our own terms; quantise/convert covered by "modifications"; outputs free and **not** a Derivative Model, so pseudo-labels are fine; notice-file duty when distributing the Model (arguably when distributing a derivative too, ask counsel). Strings OpenMDW lacks: **revocable**, NVIDIA can push updated terms ("comply or cease"), **guardrail-circumvention termination**, Trustworthy-AI-terms compliance, **indemnity of NVIDIA**. If we have a choice, the OpenMDW-1.1 Nemotron 3.5 is cleaner than the OML English model; and Nemotron 3.5 already has en-US.

### 2.3 NVIDIA "AI Foundation Models Community License Agreement" = NVIDIA Community Model License (https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-ai-foundation-models-community-license-agreement/ ; page title "NVIDIA Community Model License", "Last Modified: January 30, 2025", "(v. April 15, 2025)")

This is the licence the NGC collection page for Parakeet-RNNT-1.1B (multilingual, prompt/LangID, Indic) names ("The use of this model is governed by the AI Foundation Models Community License Agreement"; trial separately under "NVIDIA API Trial Terms of Service"). Key verbatim clauses:

> General Downloadable Grant. ... NVIDIA grants you a limited, non-exclusive, revocable, non-transferable, non-sublicensable (except as expressly permitted in this Agreement), license to: (a) install, use and reproduce NVIDIA Models, (b) create Derivative Models (as defined below), and (c) distribute NVIDIA Models and Derivative Models with a copy of this Agreement, **except that to exercise these grants in production you must use an NVIDIA Inference Microservice runtime (NVIDIA NIM) available through an NVIDIA AI Enterprise subscription**, unless: (i) an NVIDIA Model is designated by NVIDIA for use with NVIDIA RTX or GeForce RTX GPUs ... (ii) an NVIDIA Model is listed at https://www.nvidia.com/content/dam/en-zz/Solutions/license-agreements/enterprise-software/NVIDIA-Models-Community-License-2025-04-15-FINAL.pdf if such NVIDIA Model or Derivative Model of such NVIDIA Model is: (a) used locally on an end user device, (b) not used in a commercial kiosk, server or similar system used to service multiple users and (c) integrated with an application.

> "Derivative Models" means ... (c) any other model that is created or initialized by transfer of patterns of the weights, parameters, activations or output of the NVIDIA Models, to the other model, in order to cause the other model to perform similarly to the NVIDIA Models, including (but not limited to) distillation methods that use intermediate data representations or methods based on the generation of synthetic data by the NVIDIA Models for training the other model.

> Limitations. You may not: ... **Use the NVIDIA Models, Derivative Models or any output or results of them to develop or improve any other AI models (excluding NVIDIA Models or Derivative Models), unless approved by NVIDIA in writing (email approval being sufficient).** ... Use the NVIDIA Models in any manner that would cause them to become subject to an open source software license ...

> TERMINATION. ... if you fail to comply ... Upon any termination, you must stop using and destroy all copies of the NVIDIA Models and Derivative Models.

Reading: for the Parakeet-1.1B Indic/multilingual weights (which are only distributed via NGC/NIM, not HF) this is RED for both roles: as a teacher (pseudo-labelling = "output ... to develop or improve any other AI models"; synthetic data distillation is literally in the Derivative Model definition) and as a base (production use must go through NIM unless the PDF list (unread [U]) covers it). Whether the exception list in the PDF (ii) names Parakeet-1.1B is [U]; even then the output-training ban stays. Note NVIDIA's own use of these models as teachers for Nemotron 3.5 is NVIDIA's affair; our rights come from OpenMDW, which is why OpenMDW "clear rights of other persons" is the residual risk (section 2.1 row f).

### 2.4 CC-BY-4.0 NVIDIA checkpoints

Parakeet-TDT-0.6B-v2/v3, parakeet-tdt_ctc-110m, canary-1b-v2, canary-1b-flash, parakeet-rnnt/ctc-1.1b (English, 2023): HF cards state "GOVERNING TERMS: Use of this model is governed by the CC-BY-4.0 license" and "ready for commercial/non-commercial use" [M]. CC-BY-4.0 = commercial yes, adapt yes, attribution + link to licence + indicate changes, no share-alike, no restriction on outputs (outputs are not covered by it). parakeet-tdt-0.6b-v3 supports 25 European languages (Bulgarian ... Ukrainian) per its card: **no Hindi, no Telugu** [M]; v3 trained for 150,000 steps on 128 A100 GPUs, 8,192-token unified SentencePiece [M]. parakeet-tdt-0.6b-v2 training includes 110,000 h of pseudo-labelled YTC (YouTube-Commons) and YODAS data [M] (upstream caveat: YouTube-derived corpora).

NeMo cache-aware hybrid streaming set (stt_en_fastconformer_hybrid_large_streaming_{80,480,1040}ms and _multi): HF card for `_multi` says `license: cc-by-4.0`; the NGC catalog pages I fetched (80 ms page, `_multi` page) say "License to use this model is covered by the NGC TERMS OF USE unless another License/Terms Of Use/EULA is clearly specified." Those two disagree; NGC Terms of Use text not read [U]. English-only, ~114M, hybrid CTC+RNNT, [70,{0,1,6,13}]. The HF cc-by-4.0 copy is the one to cite; the HF repos for 80/480/1040 ms do not exist (API returns nothing) [M].

### 2.5 The Together AI / NGC conflict, resolved

| Source | What it says | Reading |
|---|---|---|
| HF model card (current, 2026-10-12) | front-matter `license_name: openmdw-1.1`; body "Governing Terms: ... OpenMDW-1.1"; safety.md/explainability.md repeat OpenMDW-1.1; "ready for commercial use" | Governs HF open weights |
| HF README at 2026-06-04 (commit 3d849238) | front-matter `nvidia-open-model-license` + OML link; body OpenMDW-1.1 | Launch-day metadata inconsistency |
| HF commits 41defcb1, ab89ab0f, 24b151a8 (2026-06-05, user Jinhanw, NVIDIA) | "Update License": `OpenMDW-1.1` -> typo `openmwd-1.1` -> `openmdw-1.1` | NVIDIA corrected the metadata |
| Together AI page (https://together.ai/models/nvidia-nemotron-35-asr) | "Available under the NVIDIA Open Model License." (no link to text) | Hosted/NIM-packaged model terms |
| NGC NIM container `nemotron-asr-streaming` | "The NIM container is governed by the NVIDIA Software License Agreement" ... "use of the model is governed by the NVIDIA Open Model License Agreement"; licence field "NVIDIA proprietary" | NIM channel |
| NVIDIA HF blog (2026-06-04) | "License: OpenMDW-1.1" | consistent with HF |

Conclusion [M + my inference]: two parallel channels. For weights we download from HF, OpenMDW-1.1 applies. Anyone who fetched the `.nemo` on 2026-06-04 relied on conflicting metadata; ask NVIDIA to confirm in writing that OpenMDW-1.1 governs both channels' weights (question list, section 9).

Community repacks mislabel the licence: onnx-community int4 ONNX (MIT tag), nenad1002 (MIT), Hinglish fine-tune addyo07 (Apache-2.0), Arabic adapter Abdelkareem (CC-BY-4.0), v4xsh (CC-BY-4.0), Slovenian texdata (CC-BY-SA-4.0 chosen to honour ARTUR ShareAlike, correctly lists OpenMDW-1.1 as the base licence and "retain NOTICE"), Swahili Tonykip (correct: OpenMDW-1.1). Do not treat any community licence tag as authoritative; if we reuse a community fine-tune its chain is OpenMDW (kept) + the data licences.

---

## 3. Nemotron-3.5-ASR-Streaming-0.6B: full card facts [M unless marked]

Source: https://huggingface.co/nvidia/nemotron-3.5-asr-streaming-0.6b (README, config.json, processor_config.json, tokenizer files, HF API), read 2026-10-12.

- Created 2026-05-15 (repo), release date on card "06/04/2026"; last modified 2026-09-10; not gated; 1,275,605 downloads at read time. Files: model.safetensors (2,552,062,944 B), nemotron-3.5-asr-streaming-0.6b.nemo (2,368,284,501 B), q8_0 GGUF (742,090,464 B), tokenizer.json (752 KB), configs, bias/explainability/privacy/safety .md. **No LICENSE or NOTICE file** in the repo.
- Derived from nvidia/nemotron-speech-streaming-en-0.6b ("multilingual extension ... adding language-ID prompt conditioning"). Parameters F32 637,997,088.
- Architecture (config.json): FastConformer encoder, 24 layers, hidden 1024, FFN 4096, 8 heads, conv kernel 9, 128 mel bins, subsampling 8 (80 ms frames), sliding window 57; RNN-T decoder with 2 LSTM layers, decoder hidden 640; `vocab_size` 13088 (13,087 tokens + blank id 13087); `num_prompts` 128; `default_prompt_id` 101 (= "auto"). Feature extractor: 16 kHz, n_fft 512, win 400, hop 160, preemphasis 0.97, 128 mel.
- **CTC head: none.** NeMo's config for this model family states "This is the RNNT-only variant (no auxiliary CTC head)" (fastconformer_transducer_bpe_streaming_prompt.yaml, NeMo main). Card never mentions CTC either.
- **Language conditioning:** a 128-dim one-hot language vector broadcast over time, concatenated with the 1024-dim encoder output (D+K, T), then a projection into the RNN-T decoder (card). `target_lang` accepts a locale (`en-US`, `hi-IN`) or `auto`; in auto mode the model appends a language tag (e.g. `<hi-IN>`) after terminal punctuation (`strip_lang_tags` true/false). Training uses a per-dataset `prompt_mode` (langID / auto / unified; default `unified`, `unified_auto_ratio: 0.5`; YAML comment says `auto` is "use for code-switching") (NeMo YAML).
- **Prompt dictionary (config + NeMo YAML) has 128 slots, 121 keys, including reserved slots for languages the model was not trained on:** `bn-IN 36, ur-PK 37, fa-IR 38, ta-IN 39, te-IN 40, mr-IN 41, gu-IN 42, kn-IN 43, ml-IN 44, si-LK 45, ne-NP 46` etc. NVIDIA's own tutorial says "~60 new languages not yet supported by the current checkpoint but feasible to fine-tune towards".
- **Supported tiers (card):** Transcription-ready 19 locales (English en-US/en-GB, Spanish es-US/es-ES, French fr-FR/fr-CA, Italian, Portuguese pt-BR/pt-PT, Dutch, German, Turkish, Russian, Arabic, **Hindi hi-IN**, Japanese, Korean, Vietnamese, Ukrainian); Broad-coverage 13 (Polish, Swedish, Czech, Norwegian Bokmal, Danish, Bulgarian, Finnish, Croatian, Slovak, Mandarin, Hungarian, Romanian, Estonian); Adaptation-ready 8, "recognized by the tokenizer" (Greek, Lithuanian, Latvian, Maltese, Slovenian, Hebrew, Thai, Norwegian Nynorsk). Telugu is in none. Card text "The model supports uppercase and lowercase letters, punctuation, spaces, and apostrophes."
- **Tokenizer (tokenizer.json, my count):** BPE, 13,087 tokens, `byte_fallback: true` but no `<0xNN>` tokens present; 39 language tags in `extra_special_tokens` (`<hi-IN>` yes; no `<te-IN>`). Script coverage: Latin 2,567 tokens; CJK 6,907; Cyrillic 402; Arabic 252; **Devanagari 196**; Greek 162; Thai 119; Hebrew 121; **Telugu 0**, Tamil 0, Bengali 0, Kannada 0, Malayalam 0, Gujarati 0, Gurmukhi 0 (HF discussion #21 independently reports "0 Malayalam/Tamil tokens", unanswered). NVIDIA staff (discussion #26): "Just one tokenizer. We merged all langs tokenizers and removed duplicate tokens".
- **Chunk sizes:** `att_context_size=[56,N]`, N in {0,1,3,6,13} = 80/160/320/560/1120 ms; no retraining to switch.
- **Training data (card):** see 2.1 row (f). Hindi is 5.10% of the validation set (bias.md).
- **Metrics on card (FLEURS, LangID):** Hindi WER 8.13 (80 ms) ... 6.81 (1.12 s) [prior note confirmed present in card]; Throughput ~240 vs 14 concurrent streams at 80 ms on one H100 vs Parakeet RNNT 1.1B.
- **Runtime:** NeMo 26.06 (stable NeMo releases then lacked `EncDecRNNTBPEModelWithPrompt`; install from git main [sherpa-onnx README]); PyPI `nemo-toolkit` is now 3.0.0 (2026-10-12) [M, PyPI JSON]; Hugging Face Transformers >= 5.13.0 (`AutoModelForRNNT`, `Nemotron3_5AsrProcessor`); NeMo-Speech.cpp GGUF q8_0. Supported GPU architectures listed: Ampere (A10G is Ampere), Blackwell, Hopper, Jetson, Lovelace, Turing, Volta; Linux.
- **ONNX:** card silent; sherpa-onnx has an exporter at `scripts/nemo/nemotron-3.5-asr-streaming-0.6b` (encoder/decoder/joiner + int8, `tokens.txt` from SentencePiece, metadata `prompt_dictionary` and `auto_prompt_id`, 80/160/320/560/1120 ms), supported in master since 2026-06-12 (HF discussion #1, csukuangfj); sherpa-onnx PyPI 1.13.8. Whether the exporter works with a *modified* tokenizer/prompt dictionary is [U] (it reads both from the model, so likely, untested).
- **NVIDIA's own CPU data (EN Nemotron Speech Streaming 0.6B, Q8_0, NeMo-Speech.cpp, 160 ms chunks, Intel Core i7-11700K, 8 threads):** 27 ms per chunk, about 6x real time [V, README + BENCHMARK.md]. This corrects the prior note that NeMo-Speech.cpp had no CPU figures.
- **Discussions mentioning Indic or adaptation (HF discussions, read in full via API):** #12 (Malayalam) NVIDIA reply 2026-06-14: "Malayalam is not in the current supported set, but the model's tokenizer and architecture support adding new languages through fine-tuning ... We're tracking demand for Indic languages. Hindi is already transcription-ready, and expanding to more Indic locales is on the roadmap." #4 NVIDIA reply 2026-06-14: for a new script, "Train a new SentencePiece tokenizer that includes both the existing vocabulary and your new language's characters. Resize the model's embedding and output projection layers to match. Fine-tune from the base checkpoint with the expanded tokenizer." #26 and #25 point to the tokenizer-extension notebook and the fine-tuning blog. #1: NVIDIA staff (2026-06-02): "suggest to test the 'vanilla' model and then run a short fine-tuning task (no more than a 50$ spend on an L40S) to experiment with accuracy lift per langs of interest." #10 and blog comment: "Lora is not supported now, but we are working on it!"

---

## 4. Fine-tuning Nemotron-3.5: what NVIDIA documents, and can we add Telugu

Sources (all read 2026-10-12): HF blog https://huggingface.co/blog/nvidia/fine-tuning-nemotron-35-asr (published 2026-06-04); companion notebook https://github.com/nvidia-riva/tutorials/blob/main/asr-finetune-nemotron-3.5-asr-streaming-prompt.ipynb ; **new-language notebook** https://github.com/nvidia-riva/tutorials/blob/main/asr-extend-tokenizer-to-newlang-ft-acoustic-model.ipynb ; NeMo config https://github.com/NVIDIA-NeMo/NeMo/blob/main/examples/asr/conf/fastconformer/cache_aware_streaming/fastconformer_transducer_bpe_streaming_prompt.yaml .

The prior note said "blog says nothing about adding a new tokenizer/tokens". Correct for the blog, but NVIDIA has a separate notebook that does exactly that (not linked from the blog; linked from HF discussions #26, #4 and the blog's comments).

### 4.1 The blog recipe (supported-language fine-tune)

- Five moves: (1) point the trainer at tarred NeMo/Lhotse shards, (2) fine-tune from the base checkpoint with `init_from_nemo_model`, conditioned on each clip's language tag, (3) evaluate on held-out data at deployment latency (e.g. `att_context_size=[56,0]`), (4) add data where weak and retrain, (5) export/deploy.
- Data: "~2000-hour mix" over Greek and Bulgarian from Granary, Common Voice, FLEURS; each clip needs `target_lang` ("a value the model recognizes"); transcripts "punctuated, properly-cased ... since that's what the model produces". Manifest fields in the notebook: `audio_filepath, duration, text, lang, target_lang`.
- Training: "A straightforward full fine-tune ... driven by a fixed step budget ... runs on a single GPU for a quick pass and scales cleanly to multi-GPU ... an epoch is minutes". **No GPU model, memory, batch size, steps or learning rate in the blog.** LoRA: "not supported now" (NVIDIA reply in comments).
- Results (held-out FLEURS, 80 ms): Greek 35 -> 24 WER, Bulgarian 22 -> 15; adding ~2,000 h parliamentary speech took the pool from ~290 h to ~2,300 h and Bulgarian "dropping into the high-20s" (internally inconsistent with the 15 above; unexplained).
- "Protect the other languages. ... blend in a slice of the model's other languages ('replay')". "Get the language tag right ... unforgiving of mismatched language labels."
- Blog says a few hours of in-domain audio closes a surprising amount of the gap for already-supported long-tail locales. **The "a few hundred hours" claim for a new language is not in any NVIDIA source I found** (see 4.5).

### 4.2 Command lines (verbatim from NVIDIA's notebooks, abbreviated)

Supported-language fine-tune (asr-finetune-nemotron-3.5-asr-streaming-prompt.ipynb):

```
python NeMo/examples/asr/speech_to_text_finetune.py \
  --config-path="../asr/conf/fastconformer/cache_aware_streaming" \
  --config-name=fastconformer_transducer_bpe_streaming_prompt.yaml \
  +init_from_nemo_model={HF_CKPT} \
  ++model.train_ds.manifest_filepath=... ++model.validation_ds.manifest_filepath=... \
  ++model.optim.sched.d_model=1024 ++trainer.devices=1 ++trainer.max_epochs=1 \
  ++trainer.limit_train_batches=60 ++trainer.precision=bf16 \
  ++model.train_ds.batch_duration=200 ++model.optim.name="adamw" \
  ++model.optim.lr=0.1 ++model.optim.weight_decay=0.001 ++model.optim.sched.warmup_steps=100
```
(NVIDIA comment in the notebook: "Empirical evidence suggests that around 200 epochs should suffice. If you are getting out of memory errors, reduce ++model.train_ds.batch_duration"; the lr=0.1 / 2 values are Noam-scheduler scale factors, tied to `sched.d_model=1024`.) Notebook tokenizer note: "If training dataset is not enough (<50 hrs) we recommend using tokenizers from pretrained model itself." Eval: `speech_to_text_cache_aware_streaming_infer.py ... target_lang=auto att_context_size="[56,3]" decoder_type=rnnt pad_and_drop_preencoded=true batch_size=8 strip_lang_tags=false`.

### 4.3 Adding a new language and a new script (asr-extend-tokenizer-to-newlang-ft-acoustic-model.ipynb; worked example Malay ms-MY with Mozilla Common Voice Spontaneous Speech 3.0)

Steps NVIDIA lists: (1) train a tokenizer for the new language; (2) merge it with the existing 40-locale tokenizer; (3) fine-tune; (4) streaming eval before/after. "Same method can be applied to other ASR models".

1. **Text prep:** every sentence-final "." gets the language tag appended, e.g. `"... memasak. <ms-MY>"` (function `fix_text`); manifest has `target_lang` and `lang` = "ms-MY". NVIDIA's own Hindi tokenizer test string appends the tag after the danda: `"लड़का दौड़ रहा है।" + " <hi-IN>"`.
2. **Train the new-language tokenizer:** `process_asr_text_tokenizer.py --manifest=train.json --data_root=... --vocab_size=128 --tokenizer=spe --spe_type=unigram --spe_user_defined_symbols="<ms-MY>"` (registers the new language tag as a user-defined symbol).
3. **Merge:** unzip the `.nemo`; take `*_tokenizer.model` and `*_vocab.txt`; Python merge (appends new pieces to the end of the existing SentencePiece proto, keeps higher score on duplicates; merges vocab.txt as a sorted union). Output dir `40_ms_tokenizer/{tokenizer.model, vocab.txt}`; test on the 40 sample sentences plus new language.
4. **Fine-tune with the new tokenizer:** same `speech_to_text_finetune.py` command plus `++model.tokenizer.update_tokenizer=true ++model.char_labels.update_labels=false ++model.tokenizer.dir="$DATA_DIR/40_ms_tokenizer" ++model.train_ds.default_prompt_mode="langID"`; example used `trainer.max_steps=2000`, `accumulate_grad_batches=4`, `precision=bf16`, `batch_duration=200`, `optim.lr=2`, `warmup_steps=2000`.
5. **What `update_tokenizer=true` does (NVIDIA's words):** "Once `update_tokenizer` is flagged, RNNT decoder will be forcely trained from scratch, while other components initialized from the pre-trained model." So the encoder (the bulk of the 638M) is kept; the prediction network and joint (output layer sized to the vocabulary) are re-initialised.
6. **Result and caveat in the notebook:** "the model starts to predict meaningful Malay sentences around 40~60 epochs with WER ~60%" on a toy run; "Training a RNNT decoder from scratch to support new language with great performance requires larger dataset and much more training steps than this tutorial."
7. **Language id:** ms-MY already had prompt id 35 in the dictionary. For languages not in the dictionary: either map the new language onto an unused existing id (e.g. repurpose `sm-WS`) or retrain with `examples/asr/asr_transducer/speech_to_text_rnnt_bpe_prompt.py` with a redefined prompt dictionary (must pass the full model config because the script rebuilds the model and loads the state dict). **For Telugu no dictionary change is needed: `te-IN: 40` exists.**

### 4.4 Direct answers

| Question | Answer |
|---|---|
| Can we add Telugu to Nemotron-3.5? | Yes by NVIDIA's documented route; not zero-shot. Tokenizer has no Telugu characters, so add Telugu pieces + a `<te-IN>` tag token, set `update_tokenizer=true`, and train. Prompt slot `te-IN=40` already exists. Nobody has published a Telugu (or any Dravidian) Nemotron-3.5 fine-tune that I could find (HF API searches "nemotron telugu", "nemotron indic", "nemotron-3.5 hindi/tamil/kannada/malayalam/bengali" returned no such model). Closest: AI4Bharat Bhili. |
| Does the recipe support replacing the tokenizer/decoder? | Yes: `model.tokenizer.update_tokenizer=true` + `model.tokenizer.dir=...` re-initialises the RNNT decoder (pred net + joint) and keeps the encoder. Replacing the whole tokenizer with a Telugu+Hindi+English one (dropping the 40-language vocab) is the same mechanism (point `tokenizer.dir` at a different tokenizer); NVIDIA's example merges, which preserves existing token ids only in the sense of order, but the decoder is retrained anyway [my reading]. |
| LoRA/adapters? | NVIDIA: LoRA "not supported now ... working on it" (blog comments, discussion #10). Community: Abdelkareem trained a LinearAdapter (dim 64) on the encoder with NeMo adapter classes, Egyptian Arabic, 2,384 utterances, 1000 steps, WER 105.4 -> 43.0 (base was a poor starting point for arz). Not an NVIDIA-supported path. |
| Hardware NVIDIA uses for fine-tuning? | Not stated in blog/notebooks. NVIDIA staff suggested an L40S (48 GB) at "no more than $50" for experiments (discussion #1). Training the base model itself: not disclosed; for contrast parakeet-tdt-0.6b-v3 was trained 150k steps on 128 A100 [M]. Notebook default `batch_duration=200`-400 s of audio per GPU (YAML default 400); "if OOM reduce batch_duration". |
| Does a 24 GB A10G suffice for full fine-tune? | [E] plausible but unverified: fp32 master weights 2.55 GB + grads 2.55 GB + AdamW moments 5.1 GB = ~10.2 GB before activations; bf16 autocast, `batch_duration` ~100-200 s, gradient accumulation. Community: Hinglish fine-tune ran on an RTX 5070 Ti (16 GB) but with the **encoder frozen** (card says "Full fine-tune (all params trainable), encoder frozen", self-contradictory); NbAiLab North Sami used 1x H200, 3,000 steps, lr 2e-4. Needs our own memory test [U]. |
| Data format? | NeMo JSONL manifest/tarred Lhotse shards: `audio_filepath, duration, text, lang, target_lang`; 16 kHz mono wav; punctuated and cased transcripts; `<lang-tag>` after sentence-final punctuation for auto/lang-tag behaviour; segments `max_duration 39.99 s, min 0.1 s` (YAML). Telugu and Devanagari have no case; punctuation is still required by NVIDIA's text style, and most Indic training transcripts have none [E: our P&C data prep matters]. |
| Three monolingual models (hi, te, en) a supported pattern? | Not documented as a pattern. NVIDIA's pattern is one multilingual prompt model with replay. But single-language fine-tunes of the same checkpoint are common (Swahili, Slovenian, Hungarian, Sami, Arabic-arz, AI4Bharat Bhili) and licence-wise unrestricted under OpenMDW. For English NVIDIA recommends the separate EN checkpoint ("We would recommend Nemotron ASR Streaming (English) for English-only use"). [P] Hindi from Nemotron 3.5 hi-IN; English from Nemotron 3.5 en-US or the EN checkpoint (OML); Telugu via new-tokenizer fine-tune; or one tri-lingual model with `hi-IN/te-IN/en-US` prompts + `auto` for code-switching (training uses `prompt_mode: auto` "for code-switching"). |
| Data hours needed? | NVIDIA gives no number for a new language. Evidence ladder: Greek/Bulgarian (already tokenizer-supported) ~290 h -> 2,000 h gave 35->24 and 22->15 WER; Swahili (Latin script, new language): ~382 h Kenyan Swahili, full fine-tune, FLEURS WER 29.8% at [56,13] and 32.2% at [56,0] vs base 114.7% (card); Slovenian (supported tokenizer): 858 h ARTUR + Common Voice -> 21.7-33.1% WER depending on test set; AI4Bharat Bhili: ~200 h (card; no WER; unreleased, gated, "predominantly agricultural domain"); NVIDIA's ms-MY toy: ~60% WER after a short run; Arabic-arz adapter: 2.4k utterances. For a *new script* we additionally retrain the decoder from scratch: [E] low hundreds of hours gives a usable-but-weak Telugu, thousands for production quality. The "few hundred hours" figure circulating in the team is a community/AI4Bharat-derived rule of thumb, not an NVIDIA claim. |
| Real community fine-tunes with hours/results? | See previous row. Hindi-specific: addyo07/nemotron-3.5-0.6b-hinglish (Apache-2.0 tag, 12,000 steps, RTX 5070 Ti 16 GB, frozen encoder; Hinglish WER 42.2 -> 24.6, clean Hindi WER regressed +2.85 to 24.75 on its own noisy-Hinglish set; self-reported, not checked). |

### 4.5 Practical risks for a Telugu extension [E/P]

- Decoder is retrained from scratch: the English/Hindi behaviour the base model already has will drop unless we replay Hindi and English with the *merged* tokenizer. Decision for the team: either merge tokenizers (keeps Hindi/English token ids, decoder retrained on all three languages) or new minimal hi+te+en tokenizer (smaller joint, faster CPU decode, loses 40-language coverage which we do not need). Both use the same `update_tokenizer` flag. Log as a D-### before editing pipeline.md (CLAUDE.md rule).
- sherpa-onnx export of the modified model: untested [U].
- NVIDIA's prompt YAML trains `unified` mode half the time with `auto`; if we only ever run fixed `hi-IN/te-IN/en-US`, the `<lang>` tag after punctuation is optional [P].

---

## 5. Indic models

### 5.1 AI4Bharat IndicConformer

- GitHub `AI4Bharat/IndicConformerASR` README: "## License: IndicConformer is released under the MIT license." LICENSE file: MIT, "Copyright (c) 2024 AI4Bhārat" [M]. README lists direct, **ungated** download URLs on `objectstore.e2enetworks.net` for `indicconformer_stt_{hi,te,...}_hybrid_rnnt_large.nemo` and the 600M multi `indicconformer_stt_multi_hybrid_rnnt_600m.nemo`; install needs AI4Bharat's NeMo fork (`github.com/AI4Bharat/NeMo`, branch `nemo-v2`, itself Apache-2.0).
- HF `ai4bharat/indic-conformer-600m-multilingual`: metadata `license: mit`; body "IndicConformer is released under the MIT license."; auto-gated ("You need to agree to share your contact information to access this model"; "publicly accessible, but you have to accept the conditions"); "600M", multilingual Conformer hybrid CTC+RNNT; 22 languages incl. Hindi (hi) and Telugu (te); `trust_remote_code`, `onnxruntime==1.20.1`; the repo contains ONNX graphs (`assets/encoder.onnx`, `ctc_decoder.onnx`, `joint_*`); Vaani-Benchmark-V1.0 Hindi WER 13.2; **no streaming mention; no training data statement; no citation**; the card now recommends Indic-Transcribe instead ("better transcription quality"). Created 2025-03-15, modified 2026-10-08.
- HF `ai4bharat/indicconformer_stt_hi_hybrid_ctc_rnnt_large` and `..._te_...`: `license: mit`, gated, hybrid CTC-RNNT Conformer-Large, ~120M encoder params, 17 blocks, d_model 512, 16 kHz mono, NeMo with AI4Bharat fork; no streaming, training data, WER stated. AIKosh page for the Telugu model: licence "MIT" in Metadata and License Control, Visibility "Open", footer links to AIKosh Terms of Use (unread).
- **Licence conflict resolved:** MIT per GitHub README + LICENSE, every per-language HF card, the 600M card body, AIKosh. CC-BY-4.0 appears on (i) `ai4bharat/IndicConformer` HF base repo: card reads "License to use this model is covered by the CC-BY-4.0. By downloading the public and release version of the model, you accept the terms and conditions of the CC-BY-4.0" and is otherwise unfilled NVIDIA-template boilerplate (no size, languages, WER; training section describes ~64K h English that does not apply) [M via page text]; (ii) Singla0009/IndicConformer-GGUF (Hindi/Punjabi, 120M, claims both source and converted weights CC-BY-4.0). Others: vertexvoice-indic (Apache-2.0 tag), parismitaglobalsolutions sherpa-onnx (Apache-2.0 tag), EchoBharat ("mixed-mit-and-apache-2.0"), OpenVoiceOS hi-onnx (MIT), phequals CoreML (MIT). Practical resolution: all permissive; a distributor must at least retain the MIT copyright+permission notice; add CC-BY attribution if we ever use the CC-BY-labelled artefacts. Upstream data: IndicVoices, Kathbath, Shrutilipi, Vaani are CC-BY-4.0 on HF [M, API tags], but exact IndicConformer training sets are not stated [U].
- **Gate conditions: unreadable without login** (HF returns 401 for raw README; the card page shows only the generic "share your contact information"). To read: log in and open https://huggingface.co/ai4bharat/indic-conformer-600m-multilingual (same for `indicconformer_stt_hi_hybrid_ctc_rnnt_large`, `indicconformer_stt_te_hybrid_ctc_rnnt_large`, `ai4bharat/IndicConformer`) and copy the dated gate text.
- Streaming: none of these is streaming. Hindi and Telugu per-language models: yes. ONNX: official ONNX in the 600M repo (offline); community sherpa/GGUF/CoreML conversions are offline.
- Verdict: AMBER-GREEN for pseudo-labelling and as an offline teacher (MIT, outputs unrestricted); for a base model it would need cache-aware retraining.

### 5.2 ARTPARK-IISc (IISc Vaani)

- SraVaani-0.5-live: HF API licence tag `mit`; card body has no separate licence sentence; gated (same generic text, conditions unreadable); ~430M hybrid TDT-CTC base, live export keeps the CTC head, fp16 TorchScript ~900 MB, CPU/GPU; 63 Indian languages (19 scheduled + 44+ non-scheduled; Urdu, Kashmiri not supported); streaming `att_context_size` [70,13] 1040 ms (default), [70,6] 480 ms (recommended), [70,1] 80 ms, [70,0] 0 ms; `trust_remote_code=True` (custom code ships in repo; NeMo not required); contacts agneedh@artpark.in and vaanicontact@gmail.com. Created 2026-07-16.
- SraVaani-1.0: `mit` tag, gated; ~430M, 65 languages; pretraining ~31,255 h Vaani; 11 M audio-image pairs; fine-tune ~31,270 h; ONNX + sample inference via a "SraVaani ONNX" Google Drive link; fine-tuning checkpoints need a separate access request whose terms are in the README (unread). Paper arXiv 2608.08235: FastConformer hybrid TDT-CTC, 17-layer encoder, d_model 1024, 8x subsampling, 5,000-unit BPE; says the labelled corpus is "24 public datasets spanning 65 languages and dialects" but names only VAANI, RESPIN, IndicVoices, Spring-INX, SPICOR TTS_1.0, SYSPIN_S1.0 and two Tamil/Kannada papers; **no dataset licences, no model licence, no statement on streaming/ONNX/commercial use** [M]. Upstream caveat: several of those corpora (SPICOR, SYSPIN, RESPIN, Spring-INX, IndicTTS, MUCS, GramVaani) have their own licences that were not verified here (dataset audit covered by another researcher); an "MIT" model derived from them is only as clear as those terms [U].
- Vaani-FastConformer-Telugu/-Hindi: `mit`, gated, NeMo `EncDecRNNTBPEModel`; no params, WER, streaming; trained on ARTPARK-IISc/Vaani (dataset tag cc-by-4.0, gated). The org also hosts whisper-large-v3-vaani-{telugu,hindi} (1.54B, `apache-2.0` tag, not gated per API).
- **Licence tag vs actual terms:** only the "mit" tag and the generic contact-sharing gate are visible. What the gate asks you to accept (non-commercial? purpose declaration?) is unreadable. Needs login at https://huggingface.co/ARTPARK-IISc/SraVaani-0.5-live , .../SraVaani-1.0 , .../Vaani-FastConformer-Telugu , .../Vaani-FastConformer-Hindi, and the README link for the fine-tuning checkpoints.
- Verdict: AMBER. Technically the best Indic-native streaming starting point (SraVaani-0.5-live is cache-aware, Hindi+Telugu), but the commercial rights hinge on unread gate text and unverified upstream data licences.

### 5.3 AI4Bharat Bhili (Nemotron-based), as precedent

`ai4bharat/bhili-asr-nemotron-600m` (created 2026-09-01): `mit`, gate "This is an unreleased research model. Access is granted case by case"; ~600M Nemotron-based hybrid RNNT/CTC "multisoftmax" checkpoint (a `target_lang=bhb` head selector), ~200 h Bhili (read, conversational, spontaneous), encoder trained on seven attention-context configs at once, example `att_context_size=[96,7]`, no WER, no hardware, tokenizer handling not stated. Shows an Indic lab fine-tuned Nemotron for streaming from ~200 h.

### 5.4 Bodhan AI Indic-Transcribe (Indic Open Model License v1.0)

Core/flex/pro: 1,222,553,584 params, base `nvidia/canary-1b-v2` (HF API `base_model`), gated, `license: other`, repo files `Bodhan_AI_Open_Model_License.md` and `indic-open-license.md` (gated). **The licence text is public** at https://github.com/Bodhan-AI/bodhan-model-info/blob/main/licenses/indic-open-model-license/v1/Indic_Open_Model_License.md (v1.0, updated 05 September 2026, "Copyright (c) 2026 IITM BODHAN-AI FOUNDATION") and I read it fully. The "pro"/"flex" cards say streaming is not available (lite sibling is gated 401, unread). Key verbatim clauses:

> "Derivative" or "Derivative Model" means any model, weights, or configuration created by, or derived through, fine-tuning, distillation, merging, quantizing, or otherwise modifying the Software or an earlier Derivative, **or is trained substantially on Output of the Software.** (s0)

> 1. Grant of Rights: ... a worldwide, royalty-free, non-exclusive, perpetual (subject to Section 11.3, Termination) license to use, reproduce, copy, modify, merge, publish, Distribute, sublicense, sell, deploy, fine-tune, and create Derivatives from the Software.

> 2.1 Whenever the Software or a Derivative is Made Available to a Third Party, You must include the following notice ...: "Built with [Model Name] from Bodhan AI / AI4Bharat." 2.2 The Attribution Notice must appear in the user-facing interface of the product or service through which the Software or Derivative is Made Available or, if there is no user interface, in the top-level documentation ... at least as prominent as any credit given to any other third-party model ... 2.4 This Section 2 does not apply to Internal Use.

> 3.1 ... You must obtain Licensor's prior written approval, and enter into a separate written commercial agreement with Licensor on terms to be agreed, before You Host the Software or a Derivative for a Third Party. (Carve-outs: Internal Use; Eligible Public-Interest Entity; Open-Release Waiver s4: publicly release the Hosted Derivative under this licence within 90 days.)

> 5.1 If You Make Available a Derivative to a Third Party (by Distribution or Hosting), it must be licensed under this exact License. You must not rewrite, replace, or represent the Derivative as being offered under different or modified license terms, and must not sublicense it under any alternative license.

> 7. You may fine-tune, distill, quantize, and otherwise modify the Software without restriction for Internal Use. Obligations under this License attach only once a Derivative is Made Available to a Third Party ...

> 10. Prohibited Uses ... must not use the Software, any Derivative, or any Output to: ... mass surveillance ...; disinformation ...; impersonate a real, identifiable person's voice ...; power robocalls ... ; AI companion ... [list]. Licensor may update or expand this list ... at least 30 days' public notice.

> 14. If Your own product or service ... is powered by the Software or a Derivative and exceeds 500 million monthly active users or US$250 million in annual revenue, You must obtain a separate license from Licensor.

> 11.5 Indemnification. You must defend, indemnify, and hold harmless Licensor ... 12.1 governed by the laws of India ... arbitration seated in Chennai. 11.3: breach of s10/11.1/8/9 = immediate termination; else 30 days to cure. 9: Confidential Information; must not give it to a Third Party to develop a competing model. 16.2: "You are solely responsible for identifying any Upstream Components ... and for independently verifying and complying with the license terms that apply to them."

Reading for us: shipping an on-device model that is a Derivative (including one "trained substantially on Output") to customers = "Distribute" to Third Parties = same licence + UI attribution + 500M/$250M cap + Prohibited Uses list, India-law arbitration, indemnity. Using Indic-Transcribe as a pseudo-label teacher likely makes our model a Derivative (the "trained substantially on Output" limb; "substantially" undefined [U]). Self-hosted internal use only = no obligations. Plus canary-1b-v2 CC-BY-4.0 upstream (attribution). Verdict AMBER-RED as teacher unless we accept the share-alike on our shipped model; ask Bodhan whether pseudo-label training is intended to be a Derivative, and if a lite/real-time model can be a base.

### 5.5 IndicWhisper

AI4Bharat Vistaar (GitHub `AI4Bharat/vistaar`): "Vistaar is MIT-licensed. The license applies to all the fine-tuned language models" [M]. Per-language Whisper fine-tune checkpoints (e.g. `whisper-medium-hi_alldata_multigpu`) as ungated zip downloads on objectstore.e2enetworks.net, for 12 languages including Hindi and Telugu; trained on 10,700+ h; no streaming. Whisper medium is ~769M [E, from OpenAI size table, not re-verified]. HF has many third-party re-uploads (mit tags). Telugu quality weak per previous note (~28.8 avg WER).

### 5.6 Other IISc/community notes

HF community conversions: OpenVoiceOS hi-onnx (MIT, fp32+int8), phequals CoreML RNNT (MIT, fixed 1024-frame encoder), Singla0009 GGUF (CC-BY-4.0), nmukthap/vertexvoice-indic (Apache-2.0 tag; per-language packs; QInt8 ConvInteger failure known), parismitaglobalsolutions sherpa (Apache-2.0 tag), RaunakSaha EchoBharat ("mixed MIT and Apache-2.0"). All derivatives of an MIT upstream; none adds restrictions; none is streaming.

---

## 6. Other ASR models, briefly (licence + commercial verdict)

- **OpenAI Whisper:** repo README "Whisper's code and model weights are released under the MIT License"; LICENSE MIT 2022 OpenAI. HF cards: apache-2.0 on large-v3, small, tiny; mit on large-v3-turbo. Both permissive; commercial/derivative/on-device OK; outputs unrestricted. Training data 680k h web audio (undisclosed) is the upstream caveat. Not streaming; weak zero-shot Hindi/Telugu.
- **Meta Omnilingual ASR:** LICENSE Apache-2.0 (Meta, 2025); README "Omnilingual ASR code and models are released under the Apache 2.0"; HF cards apache-2.0; corpus CC-BY-4.0. CTC-300M, <40 s audio, no streaming/ONNX in README. Languages 1,600+ (Hindi, Telugu present per prior note CSV, not re-checked). Upstream data provenance not detailed [U].
- **MMS:** `facebook/mms-1b-all`, `mms-300m`: CC-BY-NC-4.0 (HF tags). Non-commercial: unusable. Also `seamless-m4t-v2-large` CC-BY-NC-4.0.
- **Qwen3-ASR (0.6B/1.7B):** Apache-2.0 (HF tag); Hindi supported; Telugu absent from the language table (0 matches in card text); streaming mode exists.
- **Voxtral-Mini-4B-Realtime-2602:** Apache-2.0 ("released in BF16 under the Apache-2 license, ensuring flexibility for both research and commercial use"); 4.43B params; Hindi yes, Telugu no.
- **Moonshine:** LICENSE preamble: "The code in this repo ... is licensed under the MIT License. Moonshine models are released under the MIT License by default, in every language and at every size. This includes all streaming speech-to-text models and all English-language models. ... The only speech-to-text models that are NOT MIT are the legacy non-streaming models for languages other than English, which remain under the Moonshine Community License, a non-commercial license" (list: Arabic Base/Tiny, Japanese Base/Tiny, Korean Base/Tiny, Mandarin Base/Tiny, Spanish Base, Ukrainian Base/Tiny, Vietnamese Base/Tiny). TTS/G2P data files under separate licences. No Hindi/Telugu models in the exhaustive NC list and none evidenced in MIT set.
- **Kyutai:** `stt-1b-en_fr`, `stt-2.6b-en`: CC-BY-4.0 weights (HF tags; card: "Model weights are licensed under CC-BY 4.0"). Another researcher covers repos.
- **NeMo-Speech.cpp (NVIDIA):** Apache-2.0 (NVIDIA-authored code), third-party notices separate.

---

## 7. Software and tools

All licence texts below were read from the repo LICENSE files via raw.githubusercontent.com on 2026-10-12 unless noted; PyPI JSON used to cross-check packaging metadata.

| Tool | Licence (as read) | Commercial/on-device OK? | Notes |
|---|---|---|---|
| NVIDIA NeMo (`NVIDIA/NeMo`, PyPI nemo-toolkit 3.0.0) | Apache-2.0 | Yes | Pretrained checkpoints have their own licences (section 2). Nemotron-3.5 needs NeMo main/26.06+. AI4Bharat NeMo fork also Apache-2.0. |
| NVIDIA NeMo-Speech.cpp | Apache-2.0 (+ NOTICE, third-party notices) | Yes | CPU/GGUF runtime; vendor CPU numbers above. |
| NVIDIA NeMo-text-processing | Apache-2.0 | Yes | Needs Pynini (Apache-2.0 on PyPI); pip install Linux x86_64 only, Windows/macOS need conda-forge (README). Hindi ITN/TN present per prior note; Telugu not. |
| Lhotse | Apache-2.0 | Yes | |
| SentencePiece | Apache-2.0 | Yes | Tokenizer *models* we train are our data. |
| PyTorch | BSD-3-Clause style (LICENSE has the BSD redistribution/no-endorsement text, multiple copyright holders) | Yes | |
| k2-fsa sherpa-onnx | Apache-2.0 | Yes | PyPI 1.13.8; bundles third-party code, check its notices when packaging [U]. |
| k2-fsa icefall, k2 | Apache-2.0 | Yes | |
| ONNX Runtime | MIT | Yes | PyPI 1.31.0. |
| ONNX | Apache-2.0 | Yes | |
| Silero VAD | MIT (LICENSE: "MIT License, Copyright (c) 2020-present Silero Team"); PyPI classifier MIT; README body: "Published under permissive license (MIT) Silero VAD has zero strings attached" | Yes | Conflict resolved: README line 1 has `[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-MIT-lightgrey...)](.../blob/master/LICENSE)` i.e. stale alt text "CC BY-NC 4.0" over a badge image that says "MIT" and links to the MIT LICENSE. Treat as MIT. NVIDIA's packaged Silero (Riva) is under Riva terms (prior note). Ship the MIT notice. |
| TEN VAD | Apache-2.0 **with additional conditions** (below) | Probably yes for our own app; vague non-compete | PyPI `ten-vad` 1.0.6.9 shows no licence metadata. |
| AI4Bharat IndicXlit (`AI4Bharat/IndicXlit`) | Code and models MIT ("The IndicXlit code (and models) are released under the MIT License"); PyPI `ai4bharat-transliteration` MIT | Yes | Older `AI4Bharat/IndicNLP-Transliteration` repo: code Apache-2.0, "All the NN models ... of Xlit - Transliteration are licensed under CC BY-SA 4.0" (share-alike; its badge links point to the BY URL), datasets CC BY 4.0. |
| indic-transliteration (sanskrit-coders) | MIT (PyPI 2.3.82) | Yes | |
| Aksharamukha (`aksharamukha-python`) | PyPI/setup.py: "GNU AGPL 3.0" ("License :: OSI Approved :: GNU Affero General Public License v3"); repo root file `gpl-3.0.txt` (GPLv3) | **No for a shipped closed binary** | Inconsistent labelling; both copyleft (AGPL network clause). Use only as an offline research baseline. |
| uroman | LICENSE.txt: MIT-style with an extra condition: "Any publication of projects using uroman shall acknowledge its use: 'This project uses the universal romanizer software 'uroman' written by Ulf Hermjakob, USC Information Sciences Institute (2015-2020)'" ; PyPI classifier says Apache Software License (its licence field holds the same MIT text) | Yes with acknowledgement | Prior note's "unresolved" resolved: text is MIT + acknowledgement; PyPI classifier is wrong/loose. |
| whisper.cpp | MIT (ggml authors 2023-2026) | Yes | |
| faster-whisper | MIT (SYSTRAN) | Yes | CTranslate2 MIT. |
| WeNet | Apache-2.0 | Yes | |
| Hugging Face transformers, datasets | Apache-2.0 | Yes | Transformers >= 5.13.0 needed for Nemotron-3.5. |
| Moonshine library | MIT | Yes | models see section 6 |

### TEN VAD conditions, verbatim (TEN-framework/ten-vad LICENSE)

> The ten-vad is licensed pursuant to the Apache License v2.0 (provided for your convenience below), with the following additional conditions. You may reproduce, prepare Derivative Works of, publicly display, publicly perform, sublicense, distribute, or otherwise make available (together, "Deploy") the ten-vad, for commercial or non-commercial purposes, provided that you agree to abide by the terms below:
> 1. You may not Deploy the ten-vad in a way that competes with Agora's offerings and/or that allows others to compete with Agora's offerings, including without limitation enabling any third party to develop or deploy Applications.
> 2. You may Deploy the ten-vad solely to create and enable deployment of your Application(s) solely for your benefit and the benefit of your direct End Users. If you prefer, you may include the following notice in the documentation of your Application(s): "Powered by ten-vad".
> 3. Derivative Works of the ten-vad remain subject to this Open Source License.
> 4. "End Users" shall mean the end-users of your Application(s) who access the ten-vad solely to the extent necessary to access and use the Application(s) you create or deploy using ten-vad.
> 5. "Application(s)" shall mean your software programs designed or developed by using the ten-vad or where deployment is enabled by the ten-vad.
> 6. Note that the project contains derived code from other open source project with BSD-3-Clause and BSD-2-Clause license, refer to the "NOTICES" file in the root directory for detailed information. Copyright 2025 Agora.

Reading: shipping ten-vad inside our own end-user app is within clause 2. Risks: clause 1 (Agora sells real-time voice/Conversational-AI infrastructure; whether a speech-recognition SDK/model that other developers embed "competes" or "allows others to ... deploy Applications" is unclear), and clause 3 (modified ten-vad stays under this licence). If we ever offer our STT as an SDK to third-party developers, clause 1 becomes live. The earlier note's warning about the *TEN-framework monorepo* licence (end-user-device restrictions) is a different repo; the ten-vad repo's own LICENSE is the one above [M]. Verdict: Silero MIT as default; TEN VAD only after counsel review.

---

## 8. Corrections to the prior team notes

(Files: research_notes/Edge streaming Indic STT pipeline/base_models.md and edge_runtime_output.md.)

| Prior claim | Correction / resolution |
|---|---|
| Nemotron 3.5 licence "OpenMDW-1.1" vs "NVIDIA Open Model License" unresolved | Resolved: HF weights = OpenMDW-1.1 (front-matter was OML until NVIDIA's 2026-06-05 fix); NIM/Together channel says NVIDIA OML. Full OpenMDW-1.1 and OML texts now read (sections 2.1, 2.2). |
| "OpenMDW-1.1 text not retrieved" | Retrieved in full. |
| "Nemotron 3.5 ... Telugu not listed; tokenizer details unknown; blog says nothing about adding tokens" | Telugu: 0 tokenizer tokens, `te-IN` prompt slot 40 present; NVIDIA has a separate notebook for adding a language/tokenizer (decoder retrained from scratch). |
| "NVIDIA ... gives no GPU spec" | Still no spec in blog/notebook; staff comment: L40S, ~$50 for short experiments; default `batch_duration` 200/400 s. |
| "LoRA unsupported" | Confirmed by NVIDIA reply; a community encoder-adapter exists. |
| "NeMo-Speech.cpp ... no published CPU RTF" | README/BENCHMARK: EN Nemotron Q8_0, i7-11700K 8 threads, 27 ms per 160 ms chunk, ~6x real time [V]. |
| IndicConformer "MIT vs CC-BY-4.0 on a repack" | MIT is authoritative (GitHub, per-language HF cards, AIKosh); CC-BY-4.0 also sits on AI4Bharat's own `ai4bharat/IndicConformer` template repo, so the conflict is inside AI4Bharat's HF org, not only in repacks. |
| Silero "licence conflict" | Resolved: MIT; stale badge alt text. |
| TEN VAD "conditions not read" | Read (section 7); different from the TEN-framework monorepo licence. |
| Aksharamukha "GPL-3" | PyPI/setup.py say AGPL-3.0; repo has gpl-3.0.txt; either way copyleft. |
| uroman "unresolved" | MIT + acknowledgement clause. |
| "Parakeet 1.1B Indic community licence" | Read: NVIDIA Community Model License (Jan 30 / Apr 15, 2025): NIM-for-production + no using outputs to improve other models; Indic = bn/en/hi/ta; no Telugu; NGC/NIM only. |
| Indic Open Model License v1.0 "unread" | Read in full (section 5.4). Share-alike for any distributed derivative, "trained substantially on Output" = Derivative. |
| "NGC 114M streaming-model licences unread" | HF `_multi` card = CC-BY-4.0; NGC catalog pages say "NGC TERMS OF USE" (unread). Unresolved [U]. |
| "Tech-Insider says Indic-Transcribe post-trained on Nemotron 3.5" | HF API `base_model: nvidia/canary-1b-v2` for core/flex/pro; the press claim is wrong or refers to another variant (lite unreadable). |
| Whisper licence "MIT from memory" | Verified: GitHub MIT; HF cards Apache-2.0 (most sizes) / MIT (turbo). |
| MMS CC-BY-NC | Confirmed (HF tag). |

---

## 9. Questions to put to licensors (drafts; nothing sent; CLAUDE.md requires the user's go-ahead before sending anything)

**NVIDIA (Nemotron team: HF discussions or nemotron@/Riva contact):**
1. Please confirm in writing that OpenMDW-1.1 (not the NVIDIA Open Model License) governs the weights, `.nemo`, safetensors and q8_0 GGUF distributed on Hugging Face as `nvidia/nemotron-3.5-asr-streaming-0.6b`, including copies downloaded on or before 2026-06-05, when the repo metadata named the NVIDIA Open Model License.
2. Does OpenMDW-1.1 notice retention require a separate NOTICE/attribution file beyond the model card, and may we redistribute int8/ONNX/CoreML conversions and fine-tuned derivatives on end-user devices under OpenMDW-1.1 alone?
3. Is the training data (Riva multilingual set, Granary, MLS, CV, FLEURS, VoxPopuli; pseudo-labels from Canary, Parakeet 1.1B, Whisper, FunASR) cleared for commercial redistribution of derivative weights? Which Canary and Parakeet variants produced the synthetic labels, and under which licences?
4. Is there a published recipe, hardware spec and expected data size for adding a Dravidian-script language (Telugu, prompt slot te-IN) including tokenizer merge, and is Telugu on the roadmap with a date?

**AI4Bharat (IndicConformer; Tahir Javed / Kaushal Bhogale per card, support contact on bodhan.ai for Bodhan):**
5. Please confirm the licence for each IndicConformer checkpoint (600M multi, 120M per-language hi/te) is MIT as stated on GitHub, and reconcile `ai4bharat/IndicConformer` (CC-BY-4.0). What do the gated-repo conditions require and do they restrict commercial use or redistribution of fine-tuned/converted derivatives?
6. Which datasets were used to train the 600M and per-language models and are all cleared for commercial use of the resulting weights?

**ARTPARK-IISc (agneedh@artpark.in, vaanicontact@gmail.com):**
7. Do the gate terms for SraVaani-0.5-live, SraVaani-1.0, Vaani-FastConformer-Telugu/Hindi (and the separate fine-tuning-checkpoint access) allow commercial products and commercial redistribution of fine-tuned/quantised derivatives under the stated MIT licence? Are the 24 labelled training datasets (SPICOR, SYSPIN, RESPIN, Spring-INX, IndicTTS, MUCS, GramVaani ...) all commercially usable for weights derived from them?

**Bodhan AI (support@bodhan.ai per licence s15.6):**
8. Is a model trained on Indic-Transcribe transcriptions (pseudo-labels) a "Derivative" if the output is a small fraction of its training data ("trained substantially")? Is a real-time lite model released, and may it be used as a base for an on-device product without carrying the share-alike/attribution terms to end users?

**Agora (ten-vad):**
9. Does shipping ten-vad inside an on-device speech-recognition SDK offered to third-party app developers fall under condition 1 (competes with Agora / allows others to deploy Applications)?

---

## 10. What I could not read (needs the user's browser/login)

| What | URL | Why |
|---|---|---|
| Gate conditions text, IndicConformer 600M | https://huggingface.co/ai4bharat/indic-conformer-600m-multilingual | raw README 401; page shows only generic contact-sharing line |
| Gate text, per-language hi/te | https://huggingface.co/ai4bharat/indicconformer_stt_hi_hybrid_ctc_rnnt_large , .../indicconformer_stt_te_hybrid_ctc_rnnt_large | same |
| Gate text, base repo | https://huggingface.co/ai4bharat/IndicConformer | same (CC-BY-4.0 card) |
| Gate + fine-tuning-checkpoint access terms | https://huggingface.co/ARTPARK-IISc/SraVaani-1.0 , .../SraVaani-0.5-live , .../Vaani-FastConformer-Telugu , .../Vaani-FastConformer-Hindi | same |
| Gated licence files and lite model | https://huggingface.co/bodhan-ai/indic-transcribe-flex (Bodhan_AI_Open_Model_License.md, indic-open-license.md); .../indic-transcribe-lite (401) | gated (public GitHub licence read instead) |
| Bhili gate text | https://huggingface.co/ai4bharat/bhili-asr-nemotron-600m | case-by-case gate |
| NGC Terms of Use; NGC licence field of 114M cache-aware streaming models | https://catalog.ngc.nvidia.com/orgs/nvidia/teams/nemo/models/stt_en_fastconformer_hybrid_large_streaming_80ms (and _480ms, _1040ms, _multi) | page only says "NGC TERMS OF USE"; terms document not opened |
| PDF list of models exempt from NIM-in-production rule | https://www.nvidia.com/content/dam/en-zz/Solutions/license-agreements/enterprise-software/NVIDIA-Models-Community-License-2025-04-15-FINAL.pdf | not opened |
| Parakeet 1.1B Indic NIM profile table | https://docs.nvidia.com/nim/speech/latest/reference/support-matrix/asr.html | streaming/profile details for the Indic type not extracted |
| Together AI licence link | https://together.ai/models/nvidia-nemotron-35-asr | text-only claim, no link |
| Training-data licences for SraVaani/IndicConformer | SraVaani paper arXiv 2608.08235 | licences not stated |
| Hindi/Telugu CER for Omnilingual CTC-300M | n/a | not re-checked this pass |

---

## 11. Source list (all fetched 2026-10-12)

- Nemotron-3.5: https://huggingface.co/nvidia/nemotron-3.5-asr-streaming-0.6b (README, config.json, processor_config.json, tokenizer.json, tokenizer_config.json, bias/explainability/privacy/safety.md, commits API, discussions API #1,#2,#4,#8,#10,#12,#19,#21,#25,#26,#29); https://huggingface.co/blog/nvidia/fine-tuning-nemotron-35-asr ; https://github.com/nvidia-riva/tutorials (asr-finetune-nemotron-3.5-asr-streaming-prompt.ipynb, asr-extend-tokenizer-to-newlang-ft-acoustic-model.ipynb, Language-Scaling/Hindi/README.md); https://github.com/NVIDIA-NeMo/NeMo/blob/main/examples/asr/conf/fastconformer/cache_aware_streaming/fastconformer_transducer_bpe_streaming_prompt.yaml ; https://github.com/k2-fsa/sherpa-onnx/tree/master/scripts/nemo/nemotron-3.5-asr-streaming-0.6b ; https://github.com/NVIDIA/NeMo-Speech.cpp (README, BENCHMARK.md).
- Licences: https://openmdw.ai/license/1-1/ ; https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license/ ; https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-ai-foundation-models-community-license-agreement/ ; https://github.com/Bodhan-AI/bodhan-model-info/blob/main/licenses/indic-open-model-license/v1/ (Indic_Open_Model_License.md, ..._Deed.md); https://raw.githubusercontent.com/TEN-framework/ten-vad/main/LICENSE ; https://raw.githubusercontent.com/snakers4/silero-vad/master/LICENSE and README.md ; https://raw.githubusercontent.com/moonshine-ai/moonshine/main/LICENSE ; https://raw.githubusercontent.com/isi-nlp/uroman/master/LICENSE.txt ; Apache/MIT LICENSE files for NeMo, Lhotse, SentencePiece, PyTorch, sherpa-onnx, icefall, k2, onnxruntime, onnx, IndicXlit, indic_transliteration, NeMo-text-processing, whisper.cpp, faster-whisper, CTranslate2, openai/whisper, WeNet, transformers, datasets, omnilingual-asr, NeMo-Speech.cpp (raw.githubusercontent.com).
- NGC/NIM: https://catalog.ngc.nvidia.com/orgs/nim/nvidia/containers/nemotron-asr-streaming ; https://catalog.ngc.nvidia.com/orgs/nvidia/collections/parakeet-1-1b-rnnt-multilingual ; https://catalog.ngc.nvidia.com/orgs/nvidia/teams/nemo/models/stt_en_fastconformer_hybrid_large_streaming_80ms and _multi ; https://together.ai/models/nvidia-nemotron-35-asr .
- Other NVIDIA HF cards (API + README): nemotron-speech-streaming-en-0.6b, parakeet-tdt-0.6b-v2/v3, parakeet-tdt_ctc-110m, parakeet_realtime_eou_120m-v1, parakeet-unified-en-0.6b, canary-1b-v2, canary-1b, stt_en_fastconformer_hybrid_large_streaming_multi.
- Indic: https://huggingface.co/ai4bharat/indic-conformer-600m-multilingual , ...indicconformer_stt_{hi,te}_hybrid_ctc_rnnt_large , ai4bharat/IndicConformer , ai4bharat/bhili-asr-nemotron-600m ; https://github.com/AI4Bharat/IndicConformerASR ; https://github.com/AI4Bharat/vistaar ; https://aikosh.indiaai.gov.in/home/models/details/ai4bharat_indicconformer_stt_te_hybrid_ctc_rnnt_large_telugu_automatic_speech_recognition_model.html ; https://huggingface.co/ARTPARK-IISc/{SraVaani-0.5-live,SraVaani-1.0,Vaani-FastConformer-Telugu} ; arXiv 2608.08235 ; https://huggingface.co/bodhan-ai/indic-transcribe-flex ; community cards (Tonykip swahili, texdata slovenian, addyo07 hinglish, NbAiLab sami, Abdelkareem arz, GaborMadarasz hu, Singla0009 GGUF).
- Others: HF API tags for openai/whisper-*, facebook/mms-*, omniASR-*, Qwen3-ASR, Voxtral-Realtime, kyutai stt, moonshine-tiny, typhoon-asr-realtime; PyPI JSON for aksharamukha, indic-transliteration, ai4bharat-transliteration, uroman, pynini, nemo-toolkit, nemo_text_processing, sherpa-onnx, onnxruntime, silero-vad, ten-vad, lhotse, faster-whisper.
