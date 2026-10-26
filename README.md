# Telugu Speech Technology (STT & TTS)

Comprehensive speech technology research, evaluation pipelines, and prototypes for Telugu (along with Hindi and English research), covering both **Speech-to-Text (STT)** and **Text-to-Speech (TTS)** workstreams.

---

## Repository Overview

```
.
├── stt/                     # Speech-to-Text workstream
│   ├── pipeline.md          # Architecture & comprehensive plan
│   ├── pipeline_3week_lean.md# Fast-track 3-week low-cost deployment plan
│   ├── progress.md          # Session log, decision records, and status snapshots
│   ├── reports/             # Dataset audits, licence audits, and analysis
│   └── research_notes/      # Benchmarks, Whisper/Conformer notes, Kyutai audit
├── tts/                     # Text-to-Speech workstream
│   ├── pipeline.md          # TTS engineering & training architecture
│   ├── progress.md          # Training log, evaluation records, and decision logs
│   ├── telugu_teacher_run_sheet.md
│   ├── hindi_run_sheet.md
│   ├── eval/                # Evaluation sentences and test scripts
│   ├── samples/             # Audio samples across training checkpoints (2.5k, 10k, 15k)
│   └── scripts/             # Data prep (SYSPIN, Rasa), training scripts, evaluation
├── tts_handover/            # Complete TTS engineering handover package
│   ├── INDEX.md             # File index and byte counts
│   ├── PROCESS_REPORT.md    # 16-section technical report of data, training, & metrics
│   ├── artifacts/           # Tokenizer (tokenizer.json, tokenizer.model - 4,000 pieces)
│   ├── audio_samples/       # Generated clips across pilot & checkpoints
│   ├── configs/             # Training and evaluation YAML configs
│   ├── data_samples/        # Cleaned dataset lines, TSVs, and statistics
│   ├── diffs/               # Script modifications and reproduction instructions
│   └── logs/                # Training loss curves, eval CER metrics, progress logs
├── telugu_eval/             # Audio evaluation suite (10,000 & 15,000 step checkpoints)
├── demo_investor/           # Pre-rendered web demo (index.html) with 20 sample sentences
├── demo_live/               # Offline CPU live TTS web interface (server.py)
├── demo_bundle/             # Portable standalone demo bundle documentation & launcher
├── tokenizer.json           # Trained Telugu SentencePiece / Unigram tokenizer
├── tokenizer.model          # SentencePiece model binary
└── pilot_test.wav           # Baseline audio validation clip
```

---

## Workstreams

### 1. Text-to-Speech (TTS)
- **Base Architecture**: Kyutai Pocket TTS fine-tuned on open Telugu speech corpora (SYSPIN and Rasa).
- **Tokenizer**: Custom 4,000-token Unigram Telugu tokenizer (`tokenizer.json` / `tokenizer.model`) capturing native Telugu script.
- **Training Checkpoints**: Iterative training checkpoints evaluated at step 2,500, step 10,000, and step 15,000.
- **Evaluation**: Read-back evaluation using automatic STT transcription verifying character error rates (CER) against reference audio.
- **Deliverables**: See [`tts_handover/PROCESS_REPORT.md`](tts_handover/PROCESS_REPORT.md) for full reproduction steps, data preparation recipes, and hardware benchmarks.

### 2. Speech-to-Text (STT)
- **Goal**: High-accuracy, low-cost native Telugu script speech recognition.
- **Pipelines**: Contains both the full production roadmap ([`stt/pipeline.md`](stt/pipeline.md)) and the budget-conscious 3-week execution plan ([`stt/pipeline_3week_lean.md`](stt/pipeline_3week_lean.md)).
- **Documentation**: Audits on dataset licensing, commercial constraints, compute budgets, and acoustic model comparisons in [`stt/`](stt/).

---

## Demos

### 1. Pre-recorded Audio Player (Investor Demo)
A zero-setup web interface allowing immediate playback and evaluation of 20 benchmark sentences and 30-second passages across both male and female Telugu voices.

- **To run**: Simply open [`demo_investor/index.html`](demo_investor/index.html) in any web browser.

### 2. Live Offline CPU Demo (`demo_live`)
A lightweight, self-contained Python web server that accepts Telugu text input and synthesizes speech locally on standard CPU hardware without cloud dependencies.

- **Requirements**: Python 3.10+, PyTorch, and dependencies listed in [`tts_handover/environment.txt`](tts_handover/environment.txt).
- **Model Checkpoint**: Place the fine-tuned weights (`model.safetensors`, ~1.34 GB) into `demo_live/files/`.
- **To run**:
  ```bash
  cd demo_live
  python server.py --port 8000
  ```
  Then open `http://127.0.0.1:8000/` in your browser.

> **Note on Model Weights**: Due to GitHub's 100 MB single-file limit, `model.safetensors` (~1.34 GB) is excluded from git tracking. All configurations (`gen_local.yaml`), tokenizers (`tokenizer.json`), reference voice prompts (`files/voices/`), and generation scripts are fully tracked.

---

## Handover & Reproduction

For detailed engineering logs, hardware configurations, training event tables, loss curves, and reproduction diffs, refer to:
- [`tts_handover/INDEX.md`](tts_handover/INDEX.md)
- [`tts_handover/PROCESS_REPORT.md`](tts_handover/PROCESS_REPORT.md)
- [`stt/progress.md`](stt/progress.md)
- [`tts/progress.md`](tts/progress.md)