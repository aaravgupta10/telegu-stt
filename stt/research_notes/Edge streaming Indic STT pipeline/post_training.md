# Post-training / fine-tuning techniques for streaming Hindi+Telugu+English ASR on a single A10G (researched 2026-10-08)

Conventions: "[measured]" = number reported by a cited source (their setup, not ours). "[estimate]" = my own first-principles/extrapolated figure, NOT sourced; must be validated by a short benchmark run. Everything in "Inferences" is my synthesis. Search budget was limited (~25 tool calls); several topics have thin primary evidence and are flagged under Gaps.

---

## 1. Full fine-tuning vs freezing vs staged unfreezing vs LoRA/adapters; memory of 120M/600M models on 24 GB

### Takeaway
There is no head-to-head Conformer/FastConformer LoRA-vs-full study for a new language in what I found; the closest evidence (Whisper adding Irish) shows full fine-tuning gives the best new-language WER but the most forgetting, while LoRA/adapters retain old skills but learn the new language materially worse. For a large acoustic/script shift (Telugu, code-switch), update most of the encoder; use freezing/LoRA mainly as a regularizer or when data is small.

### Cited Findings
- Whisper large-v3 + Irish (FLEURS) [measured]: baseline 110.4 WER; full FT 43.7; FT+EWC 46.7-47.0; LoRA (0.13% params) 54.8; soft prompt tuning 74.9; soft language-code tuning 81.4. Adaptation-only methods keep existing languages intact but reach much worse new-language WER. — [Learn and Don't Forget (arXiv 2407.06800)](https://arxiv.org/html/2407.06800v1)
- Same paper, forgetting after full FT [measured]: English FLEURS 4.1 -> 6.1, LibriSpeech 3.7 -> 8.8, Artie Bias 5.6 -> 13.0; EWC cut LibriSpeech to 5.4. Closely related language (Welsh) was destroyed (27.5 -> 96.8 WER; the paper text says "decreases", the table shows an increase - I report the table). Forgetting is worst for languages with high overlap with the new one. — [arXiv 2407.06800](https://arxiv.org/html/2407.06800v1)
- Swiss-German Whisper (2026 preprint): full FT 25.60 WER vs best LoRA 26.28; authors say comparable when LoRA is tuned (alpha scaling) but full FT is more robust and scales with data. — [arXiv 2606.07608](https://arxiv.org/pdf/2606.07608)
- Dysarthric-speech Whisper (2026 preprint): rank-8 LoRA 15-39% relative worse than full FT; authors suspect low capacity can't capture large distribution shift. A different dysarthric study found LoRA beat full FT on 5/6 sets (implicit regularization). Conflicting evidence. — [arXiv 2606.31722](https://arxiv.org/pdf/2606.31722) ; [search summary of the counter-study](https://arxiv.org/pdf/2607.04814)
- Cross-lingual Whisper study (2026): froze first 3 encoder layers, LoRA on remaining encoder + decoder layers; results "qualitatively identical" to full-model FT across both stages. — [arXiv 2607.04814](https://arxiv.org/pdf/2607.04814)
- LLM-based ASR: full encoder FT best, encoder LoRA second, partial FT most cost-effective. — [arXiv 2406.17272](https://arxiv.org/pdf/2406.17272)
- Conformer transducer speaker adaptation: adapting only self-attention gets >80% of full-network gain; value projection >> key/query. (Speaker, not language, adaptation.) — [Microsoft Research](https://microsoft.com/en-us/research/?p=767935)
- Multilingual CTC with LoRA shows a noticeable gap vs full FT, but full FT can overfit/degrade source domain. — [arXiv 2601.00557](https://arxiv.org/pdf/2601.00557)
- NeMo fine-tuning guidance: use lr 1e-4 to 1e-5 ("too high a learning rate can destroy pretrained features"); if pretrained config uses Noam, override with constant or cosine schedule so warmup does not reset LR high; typical max_epochs 50-100 for domain adaptation; use SpecAugment; `init_from_nemo_model_include/exclude` controls which modules load (e.g., include encoder+preprocessor, exclude decoder/joint). Docs do NOT describe freezing the encoder (partial loading != trainable flags). — [NeMo fine-tuning docs](https://docs.nvidia.com/nemo/speech/latest/asr/fine_tuning.html)
- Batch-by-duration: NeMo Lhotse dataloading sizes batches by total `batch_duration`, supports dynamic bucketing (`num_buckets`, `num_cuts_for_bins_estimate`), quadratic duration penalty for long cuts, and OOMptimizer to find max batch size; default configs use max_duration 16.7 s. — [NeMo Lhotse dataloading](https://docs.nvidia.com/nemo/speech/latest/dataloaders.html) ; [NeMo ASR datasets/configs](https://docs.nvidia.com/nemo/speech/latest/asr/datasets.html)
- FastConformer memory: 8x subsampling cuts attention cost; on one A100-80GB, max trainable context at batch 1 was 18 min (no flash attention) / 70 min (with). — [Fast Conformer paper, arXiv 2305.05084](https://arxiv.org/html/2305.05084v6) (via search summary)
- A Japanese FastConformer hybrid pretraining reference: 300k steps, dynamic bucketing, batch_duration 600 s/GPU on 32x A100-80GB (pretraining, not fine-tune). — [HF model card](https://huggingface.co/nvidia/parakeet-tdt_ctc-0.6b-ja/commit/dd1e3ba76d6a551ea59d845f0f4ba72fb6ead7b5)

### Inferences
- Staged unfreezing recipe (my proposal, not published as such): Stage A freeze encoder, train new decoder/joint/CTC head only (short, high-ish LR on head ~1e-3 acceptable since head is random-init); Stage B unfreeze all with LR 1e-4 to 5e-5 for encoder (layer-wise LR decay optional), cosine, few thousand warmup steps. Avoids large random-head gradients wrecking the encoder when the vocabulary is replaced.
- Memory [estimate]: with NeMo AMP (fp32 master weights + AdamW states), a 120M model needs ~2-3 GB for weights+grads+Adam (16 B/param) and a 600M model ~9-10 GB before activations -> 600M full FT fits in 24 GB only with modest batch_duration (~100-300 s), bf16 autocast, activation checkpointing; 8-bit Adam (bitsandbytes) saves ~2 B/param x... roughly 3.6 GB on 600M (not verified in this session). 120M model is comfortable: batch_duration ~600-1000 s plausible.
- For the stated target (new script Telugu, code-switch, streaming conversion) all three changes (vocab, attention mask, language) argue for full FT of a ~100-150M model rather than LoRA; LoRA is attractive only for the "keep original model's skills" variant or for a 600M teacher/offline model.

### Gaps
- No Conformer/FastConformer/Zipformer LoRA-vs-full study for new-language adaptation found; no A10G-specific memory table found (all memory figures above are A100/other or estimates). No source on bitsandbytes 8-bit Adam with NeMo was retrieved. No source on gradient checkpointing support/config in NeMo FastConformer retrieved.

---

## 2. Tokenizer strategy for Devanagari + Telugu + Latin; vocabulary surgery; code-switch handling

### Takeaway
NeMo's recommended multilingual route is an Aggregate/Concatenated tokenizer (one SentencePiece model per language, assigned contiguous ID ranges, `lang` field in manifests), which also yields per-token language ID; small per-language vocabs (256 for Telugu in an NVIDIA tutorial, 256 per language in NVIDIA's multilingual FastConformer) are standard. Replacing the vocabulary requires re-initializing decoder/joint (transducer) or final layer (CTC) but the encoder can be retained.

### Cited Findings
- Concatenated Tokenizer (Dhawan, Rekesh, Ginsburg, NVIDIA): reuses monolingual tokenizers, gives per-token language ID, builds CS training data from monolingual sources, English-Hindi and English-Spanish; reports SOTA on Miami Bangor CS corpus and >98% LID accuracy on FLEURS (abstract only; WER numbers not retrieved). — [arXiv 2306.08753](https://arxiv.org/abs/2306.08753)
- NeMo aggregate tokenizer: per-language tokenizers each assigned token-ID range in listed order; manifest needs `lang` field; inference routing by token-ID range. NVIDIA multilingual FastConformer used per-language SentencePiece with vocab 256, unigram, character coverage 1.0, no lowercasing. — [NVIDIA blog: multilingual and code-switched ASR with NeMo](https://developer.nvidia.com/blog/multilingual-and-code-switched-automatic-speech-recognition-with-nvidia-nemo/) ; [NeMo ASR configs](https://docs.nvidia.com/nemo-framework/user-guide/25.04/nemotoolkit/asr/configs.html)
- NeMo tutorial for Telugu transducer fine-tuning suggested limiting vocab to 256; NVIDIA maintainer advice: use spe unigram/bpe subwords and fine-tune a large FastConformer instead of training from scratch. — [NeMo discussion #8123](https://github.com/NVIDIA/NeMo/discussions/8123) ; [Transducers with HF Datasets tutorial](https://huggingface.co/Respair/NeMo_Canary/raw/main/tutorials/asr/Transducers_with_HF_Datasets.ipynb)
- Changing vocab: `change_vocabulary(new_tokenizer_dir, new_tokenizer_type)` replaces only decoder, keeps encoder/preprocessor; in fine-tuning script set the new tokenizer dir and exclude decoder/joint (transducer) or final linear (CTC) from init. — [NeMo ASR API](https://docs.nvidia.com/nemo/speech/latest/asr/api.html) ; [NeMo fine-tuning docs](https://docs.nvidia.com/nemo/speech/latest/asr/fine_tuning.html)
- Prompt/LID-conditioned hybrid: NeMo has `EncDecHybridRNNTCTCBPEModelWithPrompt` for multilingual use; Canary-style models use source_lang/target_lang prompts. — [NeMo models docs](https://docs.nvidia.com/nemo-framework/user-guide/latest/nemotoolkit/asr/models.html) ; [NeMo fine-tuning docs](https://docs.nvidia.com/nemo/speech/latest/asr/fine_tuning.html)
- IndicConformer-600M-multilingual provides per-language tokenizers (IndicVoices repo) and language-ID is passed as an input argument (`model(wav,"hi","rnnt")`); no vocab size listed. — [HF model card](https://huggingface.co/ai4bharat/indic-conformer-600m-multilingual)
- Romanization as encoding (not output layer): "Romanization Encoding for Multilingual ASR" studies romanized targets for multilingual ASR. — [arXiv 2407.04368](https://arxiv.org/pdf/2407.04368) (abstract-level only)
- Gnani.ai wrote about building an Indic-optimized tokenizer for an LLM (relevant only as analogy). — [Gnani](https://www.gnani.ai/resources/research/indic-tokenizer-nemotron)

### Inferences
- Recommended: three SPE unigram tokenizers (hi Devanagari ~256-512, te Telugu ~256-512, en Latin ~256 or reuse the English base model's 1024 tokenizer) aggregated -> total vocab ~1k-1.5k. Small total vocab keeps RNNT joint tensor small (see section 4) and CPU decode fast. Telugu agglutination argues for the upper end (512) for Telugu; verify via OOV/tokens-per-word stats.
- Keep English in Latin script for English words inside Hindi/Telugu sentences ("Latin-for-English") if the training transcripts allow it; conversely, if transcripts (e.g. IndicVoices) write English words in Devanagari/Telugu script, keep a single convention. Mixed conventions in training text are a major source of inconsistent output. Decide per-dataset normalization policy and apply a transliteration pass to enforce it (tools in section 9).
- Preserve pretrained knowledge: when starting from an English streaming checkpoint, KEEP its English tokenizer/ID range and its decoder/joint rows for those IDs, and initialize only the new rows (copy-then-extend instead of exclude-all). This is a "vocabulary extension" that I did not find documented as a NeMo built-in; needs custom code (extend embedding + joint output layer; init new rows from mean of existing). Mark as unverified.
- For code-switching LID: aggregate-tokenizer ID ranges give free per-token LID; no prompt token needed for streaming (a prompt would require known language up front, hurting intra-sentence switching).

### Gaps
- No published numbers found comparing aggregate vs single multilingual BPE for Hindi/Telugu/English; no evidence found for `change_vocabulary` accepting `agg` type on an English-only checkpoint; no documented embedding-extension utility in NeMo; ZWJ/ZWNJ handling in tokenizers not found.

---

## 3. Streaming: cache-aware FastConformer, offline->streaming conversion, chunk sizes, accuracy loss

### Takeaway
Cache-aware FastConformer (NVIDIA) with chunk-aware look-ahead and multi-lookahead training is the best-documented path; published numbers show roughly 25-90% relative WER loss vs offline at zero look-ahead on LibriSpeech test-other depending on decoder, shrinking to ~25% (RNNT 6.3 vs 5.0) at 1360 ms and ~50% (RNNT 7.5 vs 5.0) at 520 ms. Zipformer/icefall offers a comparable dynamic-chunk route.

### Cited Findings
- Stateful Conformer (NVIDIA, arXiv 2312.17279), ~114M FastConformer hybrid, 200+ epochs, BPE vocab 1024, AdamW wd 0.001 + Noam, effective batch 2048 (LibriSpeech)/4096 (ASRSET 3.0, ~26k h), hybrid CTC weight alpha 0.3, FastEmit lambda 0.005, average of best 5 checkpoints. — [Stateful Conformer paper](https://arxiv.org/pdf/2312.17279) (details via [alphaxiv summary](https://www.alphaxiv.org/abs/2312.17279.md))
- LibriSpeech test-other [measured]: offline CTC 5.7 / RNNT 5.0; cache-aware zero look-ahead (0 ms) CTC 10.6 / RNNT 9.5; chunk-aware 1360 ms CTC 7.1 / RNNT 6.3; regular look-ahead 1360 ms CTC 7.9 / RNNT 7.1; buffered streaming (1-2 s chunks) CTC 8.0 / RNNT 11.3. — [Stateful Conformer paper](https://www.alphaxiv.org/abs/2312.17279.md)
- Latency sweep, hybrid chunk-aware, test-other [measured]: CTC 10.6 (0), 10.1 (40), 8.8 (240), 8.4 (520), 8.0 (680), 7.1 (1360 ms); RNNT 9.5, 9.0, 7.8, 7.5, 7.3, 6.3. Latency ~ half the look-ahead window. — same source
- Multi-domain (ASRSET 3.0, avg over benchmarks) [measured]: RNNT cache-aware 12.1 (40 ms) / 11.3 (240 ms) / 10.6 (520 ms) vs buffered 2000 ms 15.0; CTC 13.3 / 12.6 / 11.2 vs buffered 12.0. — same source
- Multi-lookahead training (random chunk config per batch) matched or beat single-lookahead models: RNNT test-other 6.2/5.5/5.2 vs 6.4/5.9/5.4 at 40/240/520 ms; paper notes it may need more steps. — same source
- Causal conv with left padding k-1; BatchNorm replaced by LayerNorm; mel normalization removed (depends on whole utterance). — same source
- Hybrid vs non-hybrid: hybrid generally helps; non-hybrid RNNT slightly better at 0/40 ms (9.4/8.9 vs 9.5/9.0). — same source
- NeMo docs: chunk-aware look-ahead recommended for cache-aware models; ~6 s left context ≈ unlimited-left-context accuracy; multi-lookahead config e.g. `att_context_size=[[70,13],[70,6],[70,1],[70,0]]` with `att_context_probs`; fully causal: `att_context_size=[L,0]`, `conv_context_size=causal`; example configs in `examples/asr/conf/fastconformer/cache_aware_streaming/`; export with `cache_support=True`; FastConformer: 8x depthwise-conv subsampling, ~2.4x faster than Conformer. — [NeMo ASR models docs](https://docs.nvidia.com/nemo-framework/user-guide/latest/nemotoolkit/asr/models.html)
- Released NVIDIA streaming checkpoints (~114M, hybrid transducer+CTC): 80 ms (att_context [70,1]), 480 ms, 1040 ms. The 1040 ms card's description text says "80ms" (probable copy-paste error; check config). — [NGC 80ms](https://catalog.ngc.nvidia.com/orgs/nvidia/teams/nemo/models/stt_en_fastconformer_hybrid_large_streaming_80ms) ; [NGC 1040ms](https://catalog.ngc.nvidia.com/orgs/nvidia/teams/nemo/models/stt_en_fastconformer_hybrid_large_streaming_1040ms)
- U2 / dynamic chunk training (WeNet): chunk size sampled per batch from 1 to max length; one model serves streaming and non-streaming; AISHELL-1: 5.60% relative CER reduction offline vs standard transformer (WeNet toolkit paper says 5.03%, a discrepancy between the two papers), 5.33% CER at 640 ms streaming. — [U2 paper](https://arxiv.org/pdf/2012.05481) ; [WeNet](https://arxiv.org/pdf/2102.01547)
- Unified streaming/non-streaming Zipformer (2025): training chunk sizes {16,32,64} frames (10 ms frames), eval chunk 32 + 128 left context; right-context frames sampled from {0,64,128,256} per batch; zipformer-medium; LibriSpeech test-clean/other [measured]: streaming baseline 3.33/8.90 (0 RC) and 2.81/7.36 (256 RC); with RC training 4.43/9.50 (0 RC) and 2.43/6.55 (256 RC); non-streaming 2.38/5.72. — [arXiv 2506.14434](https://arxiv.org/html/2506.14434)
- icefall streaming Zipformer defaults: decode chunk 32 frames (320 ms), left context 4 chunks; supports simulated and real chunk-by-chunk decoding. — [icefall docs](https://icefall.readthedocs.io/en/latest/recipes/Streaming-ASR/librispeech/zipformer_transducer.html)
- Community Korean streaming Zipformer (CER): offline-best 7.16; int8 chunk-64 7.53 (~1.28 s); chunk-32 7.815 (640 ms). — [HF card](https://huggingface.co/kangkyu/icefall-asr-ko-streaming-zipformer-174m)
- FastEmit: regularizes non-blank emission to reduce latency without alignments; LibriSpeech WER 4.4/8.9 -> 3.1/7.5 and P90 latency 210 -> 30 ms reported by Google. — [FastEmit](https://arxiv.org/pdf/2010.11148)

### Inferences
- Chunk-size vocabulary for planning: 80 ms ~ att_context [L,0] with 1 frame; 160 ms ~ chunk 2; 480 ms ~ [70,6]; 1040 ms ~ [70,13]. Recommend multi-lookahead training over {0,1,6,13} (as in NeMo docs) so one checkpoint can be deployed at any latency; pick 480 ms (or 160-320 ms if UX requires) for laptop CPU.
- Published accuracy loss is English/large-data. With only a few thousand hours for Hindi/Telugu, loss from streaming conversion is probably larger in relative terms; budget ~10-30% relative WER penalty at ~500 ms [estimate, extrapolated from the LibriSpeech/ASRSET curve: RNNT 10.6 avg at 520 ms vs offline gap].
- Offline-to-streaming by fine-tuning is the only affordable path on A10G (the paper trains from scratch for 200+ epochs on 26k h). The paper does not evaluate fine-tuning an offline checkpoint into streaming (stated absent in retrieved text); I did not find a primary source with that ablation. Practical plan: start from an existing NVIDIA cache-aware streaming English hybrid checkpoint (already causal conv + LayerNorm + chunk masks) and adapt to Indic, rather than converting an offline Indic model (changing BatchNorm->LayerNorm / non-causal->causal conv breaks pretrained weights).
- Candidate base checkpoints: NVIDIA cache-aware streaming English hybrids (114M); IndicConformer per-language 120M offline models (Conformer-Large, 17 blocks, d=512 per the Punjabi model card via [AIKosh](https://aikosh.indiaai.gov.in/home/models/details/ai4bharat_indicconformer_stt_pa_hybrid_ctc_rnnt_large_punjabi_automatic_speech_recognition_model.html)) which are not streaming.

### Gaps
- No published offline->streaming fine-tune ablation (NeMo or WeNet) with numbers; no Hindi/Telugu streaming WER-vs-chunk data found; no memory-vs-chunk data for Zipformer; no check of NeMo `chunked_limited`/`att_context_style` docs (page did not mention them).

---

## 4. Decoder/loss: CTC vs RNNT vs TDT vs hybrid; RNNT memory; FastEmit; best for CPU edge streaming

### Takeaway
Hybrid CTC+RNNT (shared encoder, CTC weight ~0.3) is the best-supported choice in NeMo: RNNT is consistently more accurate than CTC in streaming (e.g., 6.3 vs 7.1 at 1360 ms) while the CTC head acts as auxiliary regularizer and cheap fallback decoder. RNNT joint memory is dominated by B*T*U*V; keep V ~1k, use FP16 loss + batch splitting (NeMo) or pruned RNNT (icefall/k2).

### Cited Findings
- RNNT vs CTC streaming gap [measured]: RNNT lower WER at every latency in Stateful Conformer tables (e.g. 520 ms: 7.5 vs 8.4 test-other; multi-domain avg 10.6 vs 11.2). — [Stateful Conformer](https://www.alphaxiv.org/abs/2312.17279.md)
- Joint tensor size = B x T x U x V x 2 x 4 bytes (FP32 activations + grads). Example: 20 s clip (~2000 frames at 100 Hz), U~100, V=1024, B=1 ~1.6 GB; batch of 10 OOMs 16 GB GPUs. FP16 halves it; batch splitting (fused batch) cuts peak further; smaller V and 8x subsampling reduce it. Needs NeMo >=1.20, Numba >=0.57, `trainer.precision=16`, `NUMBA_CUDA_USE_NVIDIA_BINDING=1`. — [NVIDIA: Numba FP16 RNNT blog](https://research.nvidia.com/labs/conv-ai/blogs/2023/2023-10-28-numba-fp16)
- Pruned RNN-T: cheap linear joiner computes pruning bounds, full joiner evaluated only within bounds -> faster, far less memory; code in k2 / `fast_rnnt`; used by icefall transducer recipes. — [Kuang et al., arXiv 2206.13236](https://arxiv.org/pdf/2206.13236) ; [fast_rnnt](https://github.com/k2-fsa/fast_rnnt)
- TDT (Xu et al., ICML 2023): joint outputs token + duration with independent normalization; decoding skips frames; up to 2.82x faster inference and better accuracy than conventional transducers on ASR; 2.27x faster ST. — [TDT paper](https://proceedings.mlr.press/v202/xu23g.html)
- Parakeet-TDT = FastConformer encoder + TDT decoder; parakeet-tdt-0.6b-v2 (English) / v3 (25 European languages); handles up to 24 min audio. — [NGC collection](https://catalog.ngc.nvidia.com/orgs/nvidia/-/collections/parakeet-tdt-0.6b-v2/-) (speed claims in secondary press not verified)
- A TDT-CTC hybrid for Indic exists: ARTPARK-IISc SraVaani FastConformer hybrid TDT-CTC fine-tuned on ~31,270 h across 63 Indian languages/dialects. — [HF SraVaani](https://huggingface.co/ARTPARK-IISc/SraVaani-1.0)
- Hybrid ablation: hybrid helps in most settings; FastEmit also helped the CTC head. — [Stateful Conformer](https://www.alphaxiv.org/abs/2312.17279.md)
- sherpa-onnx hotwords work only with transducer models and force modified_beam_search (>=4 active paths). — [sherpa-onnx wrapper docs (third party)](https://www.mintlify.com/xdcobra/react-native-sherpa-onnx/guides/hotwords)

### Inferences
- For CPU streaming: TDT's frame skipping mostly pays off at 80 ms-frame offline-style decoding; in streaming chunks the encoder dominates CPU cost, so TDT's decoder speedup is a secondary win; however it is cheap to try because NeMo supports it (TDT streaming with cache-aware encoders: I did not find a published result - treat as untested). Safe default: hybrid RNNT+CTC (greedy RNNT in production, CTC head for fast fallback and for forced alignment/filtering in data stages).
- FastEmit lambda 0.005 (value used by NVIDIA) is a reasonable start; higher values trade WER for latency. Not needed if chunk-aware 480 ms is acceptable.
- On A10G: use V~1k, FP16 RNNT loss, `fused_batch_size` splitting; or pruned RNNT if using icefall.

### Gaps
- No measured CPU latency/RTF for TDT vs RNNT streaming; no head-to-head TDT vs RNNT for streaming cache-aware models; no memory numbers beyond the formula.

---

## 5. Pseudo-labeling / KD from large teacher (IndicConformer-600M, Whisper large-v3, etc.)

### Takeaway
Pseudo-labeling with multi-model transcription plus evaluator filtering improved Hindi ASR on YouTube-style data without hurting out-of-domain sets (AI4Bharat/Sarvam), and label-free WER-heuristic or agreement filtering is the standard hallucination control; Whisper large-v3 has documented Telugu-specific failures, so IndicConformer-style teachers should be preferred for Telugu/Hindi.

### Cited Findings
- Bhogale et al., "Empowering Low-Resource Language ASR via Large-Scale Pseudo Labeling": multiple base models transcribe, evaluators score audio-text pairs; adding pseudo-labeled YouTube data improved IndicYT without degrading out-of-domain benchmarks (Hindi). Exact thresholds/numbers not retrieved (PDF fetch failed). — [arXiv 2408.14026](https://www.arxiv.org/pdf/2408.14026)
- Distil-Whisper: WER heuristic selects best pseudo-labels; distilled model less prone to long-form hallucination (English). — [Distil-Whisper](https://www.arxiv-vanity.com/papers/2311.00430)
- uDistil-Whisper (NAACL 2025): label-free filtering; unfiltered pseudo-labels give suboptimal students. — [arXiv 2407.01257](https://arxiv.org/html/2407.01257v5)
- Rangappa et al. (Interspeech 2025): filter Whisper+Zipformer pseudo-labels via WER prediction, NER, CER analysis (call-center/Fisher English). — via [search summary](https://www.arxiv.org/pdf/2408.14026) (source link from search; details not verified)
- Self-Taught Recognizer: Whisper lacks dropout so MC-dropout uncertainty not applicable; proposes alternative utterance-level uncertainty. — [arXiv 2405.14161](https://arxiv.org/pdf/2405.14161)
- Whisper-large-v3 Telugu "script collapse" (SFR 0.46-0.71, vs >=0.98 for Hindi/Tamil), raised to 0.81-0.97 by per-language LoRA (May 2026 preprint; SFR undefined in snippet). — [TTS-STT flywheel, arXiv 2605.03073](https://www.opentrain.ai/papers/the-tts-stt-flywheel-synthetic-entity-dense-audio-closes-the-indic-asr-gap-where--arxiv-2605.03073/)
- Whisper-large-v3 Hindi FLEURS 27.50 WER vs Sarvam 10.07 on a third-party card (script-aware normalizer); FLEURS-Tamil: Whisper-large-v3 48.58 vs IndicConformer-600M 25.49 (vendor-run). Treat as indicative only. — [liodon-ai card](https://huggingface.co/liodon-ai/whisper-large-v3-te) ; [friendli Tamil board](https://friendli.ai/models/osmapi/tamil-asr-qwen3)
- IndicConformer-600M-multilingual: 22 languages incl. Hindi and Telugu, hybrid CTC+RNNT, MIT license; only listed WER is Hindi 13.2 on Vaani-Benchmark-V1.0; training data not described on card; gated access. (A Medium post says 14 languages - conflicts with HF card's 22; HF is primary.) — [HF](https://huggingface.co/ai4bharat/indic-conformer-600m-multilingual) ; [Medium](https://medium.com/@anilmathewm/vexyl-stt-free-self-hosted-indian-language-speech-to-text-server-f2909003aaf6)
- Vividh-ASR/Hugging Face post: Indic ASR models biased toward studio/broadcast audio, degrade on spontaneous speech (FLEURS may overstate). — [HF blog](https://huggingface.co/blog/adalat-ai/vividh-benchmark)
- No Whisper repetition/hallucination metric for Telugu/Hindi ASR found; BuzzASR Hindi card used `no_repeat_ngram_size=3`, `repetition_penalty=1.2` (suggests repetition problem). — [BuzzASR](https://huggingface.co/BuzzASR/hindi)

### Inferences
- Licensing check needed: IndicConformer is MIT (teacher outputs are fine), Whisper Apache-2.0 (not verified here), gated HF access requires accepting terms.
- Filtering recipe (proposal): (1) two heterogeneous teachers (IndicConformer RNNT + Whisper/other); keep utterances where inter-teacher CER < ~10-15%; (2) LID check of text script ratio (Devanagari/Telugu/Latin fractions) vs audio LID; (3) drop utterances with repeated n-gram loops, chars/sec outside speaking-rate band, empty outputs; (4) CTC-forced-alignment score (using the student's CTC head) as a third vote. Thresholds are my estimates; calibrate on a held-out labeled set.
- Sequence-level KD (hard pseudo-labels) is the practical choice; logit KD for transducers needs matched tokenization (teacher vocab != student vocab), so skip it.

### Gaps
- Numeric gains from Indic pseudo-labeling (the paper's PDF could not be parsed); no source on logit KD for transducers; no source on Omnilingual or Qwen3-ASR as teachers (not searched successfully); no IndicVoices-specific pseudo-label study.

---

## 6. Data work: open data licenses, normalization, filtering, augmentation, CS synthesis, LM/biasing

### Takeaway
Commercial-safe open Indic data exists (IndicVoices, Kathbath, Vaani) but licenses are inconsistent across listings and must be verified per dataset before use; text normalization (NFC, nukta, digits) materially changes WER and must be fixed once, up front.

### Cited Findings
- IndicVoices: paper reports 7,348 h, 22 languages, 16,237 speakers; later listings say 12,000 h/22,563 speakers (conflict). AIKosh lists CC BY 4.0; AI4Bharat page shows no license field; HF card gated. — [IndicVoices paper](https://arxiv.org/html/2403.01926v1) ; [AIKosh](https://aikosh.indiaai.gov.in/home/datasets/details/indicvoices.html)
- Kathbath: 1,684 h, 12 languages (incl. Hindi, Telugu), CC-BY-4.0 per 2025 newsletter; gated; underlying text from IndicCorp. — [HF Kathbath](https://huggingface.co/datasets/ai4bharat/Kathbath) ; [IITH newsletter](https://pr.iith.ac.in/newsletter/download/24/KID%2020250306.pdf)
- Shrutilipi (AIR bulletins): AI4Bharat licenses packaging CC0 but says it does not own raw audio/text (crawled newsonair.gov.in); newsletter lists CC-BY-4.0 - conflict; commercial rights on broadcast audio unresolved. — [AI4Bharat](https://ai4bharat.iitm.ac.in/?p=1129) ; [AIKosh](https://aikosh.indiaai.gov.in/home/datasets/details/shrutilipi_ai4bharat.html)
- Vaani (IISc/ARTPARK): official site says CC-BY-4.0; some third-party subsets (Odia) list CC-BY-NC 4.0; Gram Vaani Hindi is CC BY-NC 4.0 (different dataset). — [Vaani](https://vaani.iisc.ac.in/) ; [HF Odia subset](https://huggingface.co/datasets/Minutor/vaani-or-dataset)
- IndicVoices-R (TTS-grade): HF card says CC-BY-4.0 but AIKosh lists CC BY-ND 4.0 (conflict). — [AI4Bharat](https://ai4bharat.iitm.ac.in/indicvoices_r) ; [AIKosh](https://aikosh.indiaai.gov.in/home/datasets/details/indicvoices_r.html)
- Normalization pitfalls: Whisper's default normalizer inflates Indic scores (strips matras/virama per vendor blog; the "What is lost in Normalization" paper argues common practice is flawed for Indic); precomposed nukta letters (U+0958-095F) are composition-excluded so NFC leaves them decomposed (base + U+093C); nukta with/without both valid in loanwords; digits vs words vs Devanagari numerals are all different tokens for WER; recommended pipeline NFC + nukta folding + digit-to-word + punctuation strip; SN-WER (script-normalized WER) as complement for code-mixed; Telugu inflectional WER (2008). ZWJ/ZWNJ not covered by any source. — [arXiv 2409.02449](https://arxiv.org/html/2409.02449v4) ; [dev.to Hindi numbers](https://dev.to/tushar9802/whisper-transcribes-spoken-hindi-numbers-as-words-not-digits-so-i-made-a-library-to-convert-them-3m95) ; [SN-WER](https://www.alphaxiv.org/abs/2606.02548.md) ; [arXiv 2609.20504](https://arxiv.org/pdf/2609.20504)
- Code-switch augmentation evidence: Hindi-English TTS + Mixup gave up to 5% absolute WER reduction (Sharma et al., Interspeech 2020, proprietary data); Mandarin-English: splicing and TTS each help, plus SpecAugment gains; Conformer favors TTS + speed perturbation, codec/pitch-shift can hurt; Transformer-Transducer text injection 16% relative TER reduction (1,800 h CS data). — [Sharma 2020](https://www.isca-archive.org/interspeech_2020/sharma20c_interspeech.html) ; [Du et al.](https://arxiv.org/abs/2107.06483v1) ; [Yu et al. 2023](https://arxiv.org/abs/2303.10949) ; [survey 2507.07741](https://arxiv.org/pdf/2507.07741)
- NVIDIA's code-switch data construction from monolingual data (concatenating monolingual utterances). — [arXiv 2306.08753](https://arxiv.org/abs/2306.08753)
- Hindi-English CS baselines: T-T WER 29.63 (Interspeech 2022); multilingual+LID 21.77; MUCS hybrid >35 (secondary). — [NITK](https://idr.nitk.ac.in/items/5ecb03aa-faf7-437a-84f9-b22126ba11ac/full) ; [Gnani](https://gnani.ai/resources/research/code-switching-at-8khz)
- Text-only/LM: icefall shallow fusion tutorial (LM scale ~0.3 typical, beam tradeoff, GPU recommended); internal-LM adaptation with text-only data and factorized neural transducer are options; sherpa-onnx hotwords require transducer + modified beam search. — [icefall](https://icefall.readthedocs.io/en/latest/decoding-with-langugage-models/shallow-fusion.html) ; [arXiv 2110.05354](https://arxiv.org/pdf/2110.05354) ; [arXiv 2212.01992](https://arxiv.org/pdf/2212.01992)
- Whisper tends to emit Hindi numbers as words; Hindi model cards show 6-gram KenLM on AI4Bharat corpus. — [dev.to](https://dev.to/tushar9802/whisper-transcribes-spoken-hindi-numbers-as-words-not-digits-so-i-made-a-library-to-convert-them-3m95) ; [HF stt_hi_conformer_ctc_large_v2](https://huggingface.co/parthiv11/stt_hi_conformer_ctc_large_v2/blame/main/README.md)

### Inferences
- Do own license diligence: use IndicVoices + Kathbath + Vaani (official CC-BY) + Common Voice/FLEURS/other as confirmed; treat Shrutilipi and IndicVoices-R as legal-review items; keep a manifest with per-source license.
- Suggested augmentation defaults [estimate from general practice, not sourced here]: speed perturbation 0.9/1.0/1.1; SpecAugment 2 freq masks (F~27) + 2-10 time masks (T~0.05 of length), NeMo defaults; add noise/RIR (MUSAN/openRIR - license check) and 8 kHz telephony/codec simulation only if target includes telephony (evidence above: codec/pitch augmentations can hurt Conformer on CS data - validate).
- Temperature sampling for language mix (p_i ~ n_i^0.5-0.7) [estimate]; keep >=20-30% English/CS to avoid English regression.
- n-gram LM via shallow fusion is feasible on CPU (KenLM) but sherpa-onnx streaming-support not verified; hotwords are verified for transducer.

### Gaps
- No source on CTC-segmentation/NeMo aligner parameters; no ZWJ/ZWNJ guidance; no Telugu-specific normalization standard; no published noise/RIR/telephony augmentation numbers for Indic; no evidence for a streaming Hinglish transducer with TTS/spliced data; no Telugu-English CS data source identified (Telugu-English CS corpora not searched).

---

## 7. Catastrophic forgetting, checkpoint averaging, EMA, model soup, QAT int8

### Takeaway
Weight averaging between the original and adapted model is the cheapest, best-evidenced forgetting control in ASR; EWC helps modestly; Conformer QAT to int8 (and lower) is well established in Google literature, with sherpa-onnx int8 PTQ already giving ~1.8-2x CPU speedup at small accuracy cost.

### Cited Findings
- Weight averaging of old and adapted ASR model (simple 0.5 average, optionally with KD loss) retains old-task performance while achieving new-task gains; works mono- and multilingual. — [arXiv 2210.15282](https://arxiv.org/pdf/2210.15282)
- Linear interpolation of several models fine-tuned from the same generalist performs well on all tested data. — [arXiv 2505.20477](https://arxiv.org/html/2505.20477v1)
- WiSE-FT (interpolate pretrained and fine-tuned weights with alpha). — [arXiv 2109.01903](https://arxiv.org/pdf/2109.01903)
- Whisper-merge study: best merging 12% relative WER reduction vs classic FT (dysarthric). — via [search results](https://arxiv.org/abs/2504.10478v1)
- EWC reduced forgetting (LibriSpeech 8.8 -> 5.4) at small new-language cost (43.7 -> 46.7). — [arXiv 2407.06800](https://arxiv.org/html/2407.06800v1)
- NVIDIA recipes average best-5 checkpoints. — [Stateful Conformer](https://www.alphaxiv.org/abs/2312.17279.md)
- 4-bit Conformer with native QAT: lossless 4-bit on LibriSpeech (~5.8x smaller than fp32); production model mixed 4/8-bit lossless ~5x smaller. Most practical systems use PTQ 8-bit. — [arXiv 2203.15952](https://arxiv.org/pdf/2203.15952)
- Sub-8-bit QAT for RNN-T: 4-16% relative WER improvement by enlarging model while improving latency 5%. — [arXiv 2206.15408](https://ar5iv.labs.arxiv.org/html/2206.15408)
- sherpa-onnx int8 (PTQ, community): Korean streaming Zipformer 1 thread: chunk-16 CER +0.005, RTF 0.134 -> 0.073 (1.84x); chunk-32 +0.080, RTF 0.098 -> 0.054. Indian-English Zipformer card: Xeon 4 threads int8 RTF 0.035 vs fp32 0.183; Svarah WER 27.96 (int8 greedy) vs 26.90 (fp32 modified beam) - confounded by decoding method. — [Korean card](https://huggingface.co/kangkyu/icefall-asr-ko-streaming-zipformer-174m) ; [Indian English card](https://huggingface.co/Akshatkasera007/STT-streaming-zipformer-indian-en)

### Inferences
- Soup/average: (a) average last N=5-10 checkpoints (EMA decay ~0.999 equivalent) in the final stage; (b) WiSE-style interpolation between the pretrained English checkpoint and the Indic-adapted one is only valid for same-shaped tensors, so do it after vocab extension (old rows) or interpolate encoder only. Tune alpha on both English (LibriSpeech/Common Voice-en) and Indic dev sets. Start alpha 0.5.
- QAT: do PTQ int8 first (ONNX dynamic/static) and measure WER; only run QAT if degradation >3-5% relative on code-switch/Telugu (Indic agglutinative tails may be more sensitive - unverified). QAT in NeMo/PyTorch is not documented in my sources; budget extra engineering.
- Regression suite: fixed English test (LibriSpeech/TED), Hindi, Telugu, CS sets; gate each stage on no >10% relative English regression.

### Gaps
- No NeMo-specific QAT recipe found; no measurements of int8 on Indic/Telugu models; no results for EMA/model soup in ASR for language addition on Conformers.

---

## 8. Training time/cost estimates and cloud prices

### Takeaway
No published A10G/NeMo throughput benchmarks were found; my first-principles estimates suggest a ~110-120M FastConformer fine-tunes at roughly 100-300 audio-hours per GPU-hour on A10G (so 5,000 h x 10 epochs ~ 170-500 GPU-hours, $85-500), while 600M is ~5x slower and only practical for short runs. A10G spot (~$0.43-0.52/h in us-east-1) beats on-demand ($1.006/h).

### Cited Findings
- AWS g5.xlarge on-demand ~$1.006/h (us-east-1, July 2026 snapshot); spot lowest $0.4277/h (DoiT snapshot), $0.5149/h cheapest AZ in a July Holori snapshot with >20% interruption rate; spot as low as $0.1383/h in eu-south-2; savings 47% (eu-west-1) to 82% (sa-east-1) by region. — [compute.doit.com](https://compute.doit.com/spot/us-east-1/g5.xlarge) ; [Holori](https://calculator.holori.com/aws/ec2/g5.xlarge/us-east-1) ; [DoiT eu-west-1](https://compute.doit.com/spot/eu-west-1/g5.xlarge) ; [DevZero](https://www.devzero.io/instances/aws/g5.xlarge)
- RunPod community: L4 ~$0.44/h, A100-80GB ~$1.39/h (secure SXM $1.59); Modal per-second: A10 ~$1.10/h, L4 ~$0.80/h, A100-80GB ~$2.50/h (another blog says $3.72, conflicting); Lambda A100-80GB ~$1.99-2.06/h, A10 $0.86-1.29 (conflicting). Aggregator sources dated Mar-Sep 2026; verify on provider pages. — [costbench RunPod vs Lambda](https://costbench.com/compare/lambda-labs-vs-runpod/) ; [costbench Modal vs RunPod](https://costbench.com/compare/modal-vs-runpod/) ; [Modal pricing summary](https://yangmao.ai/en/compute/modal/) ; [spendark](https://spendark.com/blog/gpu-cloud-pricing-compared/)
- Reference scale: Japanese Parakeet hybrid 600M pretraining used 32x A100-80GB, 300k steps. — [HF card](https://huggingface.co/nvidia/parakeet-tdt_ctc-0.6b-ja/commit/dd1e3ba76d6a551ea59d845f0f4ba72fb6ead7b5)
- NVIDIA 114M streaming model trained 200+ epochs on 26k h (hardware not stated). — [Stateful Conformer](https://www.alphaxiv.org/abs/2312.17279.md)
- Colab/Kaggle: no sourced 2026 pricing retrieved.

### Inferences (all [estimate])
- Throughput derivation: FastConformer-large ~110M encoder, 12.5 encoder frames/s after 8x subsampling -> ~2.75 GFLOPs/s audio forward, ~3x for training, ~2x overhead (attention, subsampling convs, RNNT joint) => ~15 GFLOP per audio-second => ~55 TFLOP per audio-hour. At ~6-10 TFLOPS effective on A10G (peak bf16 tensor dense ~70-125 TFLOPS per NVIDIA specs, not verified here; 8-15% MFU realistic) -> ~100-300 audio-h per GPU-h. Real number must be measured (data loading, bucketing efficiency, RNNT loss can cut this by 2x).
- Scenario table (120M, 10 epochs over data, 150 h/GPU-h midpoint): 500 h -> ~33 GPU-h ($33 OD / ~$16 spot); 2,000 h -> ~133 GPU-h ($134 / ~$65); 5,000 h -> ~333 GPU-h ($335 / ~$160). 600M at ~30 h/GPU-h: 500 h x 5 epochs ~ 83 GPU-h ($84); 2,000 h x 5 epochs ~ 333 GPU-h; 5,000 h not feasible within "few hundred dollars". Spot interruptions: checkpoint every ~15-30 min, use S3/EBS resume.
- $/hour-of-audio: L4 (24 GB, ~$0.44 community / ~$0.80 Modal) has lower memory bandwidth and roughly similar bf16 compute to A10G (unverified), so expect A10G >= L4 per hour; A100 (~$1.4-2.5/h) is ~2.5-3x faster than A10G (typical, unverified here) so A100 community/spot at ~$1.4/h can be cheaper per audio-hour than A10G on-demand at $1.0/h and allows larger batch. For total budget of a few hundred dollars, best value = A100 community/spot for the heavy stages (offline pseudo-label inference, teacher decoding) and A10G spot for dev/iteration. Validate by a 10-minute benchmark on each.
- Pseudo-labeling inference with a 600M teacher is typically cheaper than training (batch inference), but at thousands of hours still costs tens of GPU-hours.

### Gaps
- No measured A10G/L4 NeMo FastConformer throughput found; no icefall benchmark numbers retrieved; no Colab/Kaggle/Lambda L4/A10G sourced prices; spot pricing varies daily.

---

## 9. Romanization as an optional output layer

### Takeaway
Treat romanization as deterministic post-processing from native-script output (do not train on romanized targets); strict reversibility is not guaranteed by common tools, and English words written in Devanagari/Telugu need dictionary/back-transliteration handling.

### Cited Findings
- ISO 15919 covers Devanagari ... Telugu; 2001 edition confirmed 2022; draft 2nd edition exists. A Unicode proposal notes lack of Telugu nukta forces ad-hoc strategies (Aksharamukha uses U+00B7 as nukta equivalent). — [Wikipedia ISO 15919](https://en.wikipedia.org/wiki/ISO_15919) ; [Unicode L2/19-401](https://www.unicode.org/L2/L2019/19401-telugu-sign-nukta.pdf) ; [ISO 15919 catalogue](https://scc-ccn.ca/standardsdb/standards/8113493)
- indic-transliteration (Python) documented usage is scheme-to-script (HK/ITRANS), no round-trip guarantee stated. — [PyPI](https://www.pypi.org/project/indic-transliteration/1.3.1/) ; [GitHub](https://github.com/indic-transliteration/indic_transliteration_py)
- IndicXlit (AI4Bharat): learned Transformer (~11M params), 21 languages, top-4 candidates re-ranked with a word-level unigram LM; Aksharantar dataset; direction support inconsistent across sources (PyPI says Indic->English unsupported). Not deterministic. — [Aksharantar](https://arxiv.org/pdf/2205.03018) ; [PyPI](https://pypi.org/project/ai4bharat-transliteration/)
- Reversible-scheme tools: IITHLP claims 1:1 mapping (unverified); lipimala notes Gujarati/Devanagari are not 1:1 and uses a checksummed trailer for exact recovery. — [IITHLP](https://pypi.org/project/iithlp/) ; [lipimala](https://pypi.org/project/lipimala/)
- Romanized targets for multilingual ASR are studied separately. — [arXiv 2407.04368](https://arxiv.org/pdf/2407.04368)
- Whisper-style Hindi outputs often spell numbers as words, relevant to any romanization of numerals. — [dev.to](https://dev.to/tushar9802/whisper-transcribes-spoken-hindi-numbers-as-words-not-digits-so-i-made-a-library-to-convert-them-3m95)

### Inferences
- Pipeline: ASR (native script, with English words in Latin when detected via aggregate-tokenizer ID range) -> rule-based ISO-15919-like/Hunterian/ITRANS-like transliteration (indic-transliteration or Aksharamukha) for Devanagari/Telugu spans only -> Latin spans pass through untouched. Because LID is free from the token ID range, English words in Latin script need no transliteration; Devanagari-spelled English words (e.g., "कंप्यूटर") require an English lexicon lookup (CMU-dict-style back-mapping) or IndicXlit candidate ranking, accepting non-determinism.
- Test round-trip on all code points (including nukta, candrabindu, anusvara, chillu-like Telugu forms) before choosing; the Unicode proposal suggests Telugu nukta is the main risk.

### Gaps
- No quantitative romanization-quality numbers (e.g., user readability) found; no evaluation of ISO 15919 vs Hunterian for Telugu; no source on a best-practice for Devanagari-spelled English words.

---

## KEY QUESTION A: Single best staged recipe (stage 0..N) given the constraints

### Takeaway
My recommended recipe (synthesis; individual components sourced above, the combination is untested): start from a ~114M cache-aware streaming hybrid FastConformer, extend the tokenizer to an aggregate hi/te/en vocab, adapt in stages (head warmup -> full FT with multi-lookahead streaming -> pseudo-label scale-up -> CS synthesis -> averaging/PTQ), using 2,000-5,000 h of open data and ~150-400 GPU-hours total.

### Inferences (recipe)
- Stage 0 - Foundations (CPU/cheap): lock license manifest; build one Hindi/Telugu/English normalizer (NFC, nukta policy, digit/number-word policy, English-word script policy, punctuation); build fixed dev/test sets (IndicVoices/Kathbath/FLEURS/Vaani-benchmark Hindi + English) and report WER/CER plus SN-WER-style complement. Benchmark A10G throughput with OOMptimizer (1-2 hours, ~$2).
- Stage 1 - Teacher baselines and data: run IndicConformer-600M (MIT) on dev sets for reference; use it (and optionally a second model) to pseudo-label unlabeled commercially-usable audio; filter via agreement/LID/script/repetition/CTC-alignment gates; segment long-form with CTC segmentation.
- Stage 2 - Tokenizer + head warmup: aggregate SPE (hi/te ~256-512 each, en reuse), keep encoder, new decoder/joint, freeze encoder, ~2-5k steps. [estimate]
- Stage 3 - Full FT + streaming adaptation: unfreeze, lr 1e-4 to 5e-5 cosine, `att_context_size` multi-lookahead (e.g., [[70,13],[70,6],[70,1],[70,0]]), chunk-aware, hybrid CTC weight 0.3, FastEmit lambda ~0.005, SpecAugment on, speed perturbation, language-balanced temperature sampling, 20-50 epochs-equivalent on 500-2,000 h of supervised data, ~30-130 GPU-h on a 120M model. Keep English data (LibriSpeech-like) mixed in to limit forgetting.
- Stage 4 - Scale with pseudo-labeled data (noisy student): add filtered pseudo-labels (2-5k h), second FT round at lower LR; ablate with/without filtering.
- Stage 5 - Code-switch: build CS training data by splicing monolingual utterances (NVIDIA method), optionally TTS (Indic Parler-TTS etc. - license check) for English-in-Hindi/Telugu sentences with entity-dense text; ablate vs no-CS; keep real CS (IndicVoices conversational) in dev.
- Stage 6 - Regression control: average last 5-10 checkpoints / EMA; optional WiSE interpolation with the English pretrained encoder; require no >10% relative English regression.
- Stage 7 - Edge export: ONNX with cache support, int8 PTQ; sherpa-onnx style RTF check on target laptop CPU; optional QAT if degradation >3-5% relative; optional KenLM/hotwords for domain terms (hotwords => modified beam search).
- Stage 8 (optional) - Romanization layer as in section 9.
- Evidence-backed ablations to run (ordered by expected value): (1) vocab strategy (aggregate vs reuse-English-plus-extension); (2) multi-lookahead vs single lookahead (paper: 3-8% relative gain); (3) hybrid vs non-hybrid; (4) filtered vs unfiltered pseudo-labels (uDistil-Whisper, Distil-Whisper evidence); (5) with/without CS synthesis; (6) checkpoint average/WiSE alpha; (7) PTQ vs QAT.

### Gaps
- No published end-to-end Hindi+Telugu+English streaming FastConformer recipe; no verified compute totals; Telugu-English CS data not located; teacher licenses other than IndicConformer MIT not verified.

---

## KEY QUESTION B: Top 5 failure modes and mitigations

### Takeaway
(1) Repetition/hallucination, (2) language/script confusion and collapse (Telugu), (3) English-word mangling in code-switch, (4) Telugu agglutination/OOV and normalization-driven false WER, (5) streaming degradation (right-context loss, early-chunk errors, quantization), each with sourced mitigations below.

### Cited Findings
- Repetition/hallucination: Distil-Whisper WER-heuristic filtering reduces hallucinations; Whisper large-v3 Telugu script collapse (SFR 0.46-0.71) fixed partly by per-language LoRA (0.81-0.97); BuzzASR used no_repeat_ngram/repetition penalty (Whisper decoding). RNNT/CTC are structurally less hallucination-prone than autoregressive decoders (my inference, not sourced). — [Distil-Whisper](https://www.arxiv-vanity.com/papers/2311.00430) ; [arXiv 2605.03073](https://www.opentrain.ai/papers/the-tts-stt-flywheel-synthetic-entity-dense-audio-closes-the-indic-asr-gap-where--arxiv-2605.03073/) ; [BuzzASR](https://huggingface.co/BuzzASR/hindi)
- Language confusion / forgetting among related languages: full FT destroyed Welsh (27.5 -> 96.8) when adding Irish. — [arXiv 2407.06800](https://arxiv.org/html/2407.06800v1) (relevance: Hindi vs Telugu share script-less confusion less, but Hindi/Marathi-type pairs would)
- English-word mangling/CS: concatenated tokenizer gives per-token LID and >98% FLEURS LID; TTS/splicing and text injection improve CS WER (16% relative TER; up to 5% absolute WER). — [arXiv 2306.08753](https://arxiv.org/abs/2306.08753) ; [Yu 2023](https://arxiv.org/abs/2303.10949) ; [Sharma 2020](https://www.isca-archive.org/interspeech_2020/sharma20c_interspeech.html)
- Telugu agglutination/eval artifacts: normalization choices distort Indic WER; inflectional WER for Telugu; Telugu number tables not native-verified; CER as complement. — [arXiv 2409.02449](https://arxiv.org/html/2409.02449v4) ; [arXiv 2609.20504](https://arxiv.org/pdf/2609.20504)
- Streaming degradation: zero look-ahead RNNT 9.5 vs offline 5.0 test-other; right-context training gives non-streaming-like accuracy at larger RC (Zipformer: 6.55 vs 5.72); int8 CER deltas small in community Zipformer. — [Stateful Conformer](https://www.alphaxiv.org/abs/2312.17279.md) ; [arXiv 2506.14434](https://arxiv.org/html/2506.14434) ; [Korean card](https://huggingface.co/kangkyu/icefall-asr-ko-streaming-zipformer-174m)
- Domain mismatch: studio/broadcast-biased training degrades spontaneous speech; benchmark on conversational sets. — [HF Vividh](https://huggingface.co/blog/adalat-ai/vividh-benchmark)

### Inferences
- Mitigations: (1) transducer/CTC hybrid decoding + max symbols per frame + filter training/pseudo-label data for repeated n-grams/chars-per-second; (2) aggregate tokenizer with per-language ID ranges, balanced sampling, LID/script-ratio checks on pseudo-labels, English replay; (3) CS data (splice/TTS/text injection) + consistent script convention for English words + lexicon/hotwords biasing; (4) Telugu vocab 512, CER alongside WER, normalizer unit tests incl. ZWJ/ZWNJ and nukta, native review; (5) multi-lookahead training, deploy at >=480 ms if needed, FastEmit only if latency required, check PTQ vs QAT, EMA/averaging.

### Gaps
- No quantified rates for hallucination/language confusion in streaming transducers on Indic data; failure modes in rows 1-4 are partly my synthesis of adjacent evidence.
