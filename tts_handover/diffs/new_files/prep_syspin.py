#!/usr/bin/env python3
"""Prepare SYSPIN Telugu clips for Pocket TTS fine-tuning.

STATUS: written 2026-10-18 against the real SYSPIN layout; tested only on 4 clips (see tts/progress.md TA-030).

Input  (one extracted SYSPIN speaker folder):
    <root>/*Transcripts.json   {"Transcripts": {"<id>": {"Transcript": "...", "Domain": "..."}}}
    <root>/wav/<id>.wav        48 kHz, 24-bit, mono studio recordings
Output (under --out):
    wavs/<id>.wav              24 kHz, mono, 16-bit, edges trimmed (about 0.25 s kept), loudness normalised
    train.jsonl, valid.jsonl   one {"path", "duration", "transcript"} per line (Kyutai manifest format)
    rejected.tsv               id <TAB> reason <TAB> text   (so every drop can be reviewed)
    stats.json                 counts, hours, domains

What it does to the text: Unicode NFC; remove zero-width characters; tidy punctuation (keep , . ? !);
collapse spaces; drop any clip whose text still contains digits, Latin letters or other non-Telugu
characters, or has fewer than 2 words. (Digit-to-Telugu-words is NOT implemented; digit clips are dropped and counted.)
What it does to the audio (needs ffmpeg): trim silence at both ends only (threshold -40 dB, keep 0.25 s at the
start and 0.3 s at the end), loudness-normalise, resample to 24 kHz mono 16-bit; drop clips under 1 s or over 30 s.

Usage:
    python prep_syspin.py --root <extracted speaker folder> --out <output folder> [--limit-hours 10] [--workers 8]
"""
import argparse
import hashlib
import json
import random
import re
import subprocess
import sys
import unicodedata
import wave
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ALLOWED_PUNCT = ",.?!"
ZERO_WIDTH = {ord(c): None for c in "​‌‍⁠﻿"}
TELUGU_CHAR = re.compile(r"[ఀ-౿]")
DIGITS = re.compile(r"[0-9౦-౯]")
REPLACEMENTS = {"“": '"', "”": '"', "‘": "'", "’": "'", "–": "-", "—": "-", "…": "..."}

AUDIO_FILTER = (
    "silenceremove=start_periods=1:start_silence=0.25:start_threshold=-40dB,"
    "areverse,"
    "silenceremove=start_periods=1:start_silence=0.3:start_threshold=-40dB,"
    "areverse,"
    "loudnorm=I=-23:LRA=11:TP=-2,"
    "aresample=24000"
)
MIN_SEC, MAX_SEC = 1.0, 30.0


def clean_text(text: str) -> str:
    t = unicodedata.normalize("NFC", text).translate(ZERO_WIDTH)
    for a, b in REPLACEMENTS.items():
        t = t.replace(a, b)
    t = t.replace(":", ",").replace(";", ",")
    t = re.sub(r"[\"'()\[\]{}«»]", "", t)
    t = re.sub(r"[-/\\|_*#~@^<>=+&%$]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    t = re.sub(r"\s+([,.?!])", r"\1", t)
    t = re.sub(r"([,.?!])\1+", r"\1", t)
    return t


def reject_reason(text: str):
    if not text:
        return "empty"
    if DIGITS.search(text):
        return "digits"
    bad = sorted({c for c in text if not (TELUGU_CHAR.match(c) or c == " " or c in ALLOWED_PUNCT)})
    if bad:
        return "chars:" + "".join(bad)[:20]
    if len(text.split()) < 2:
        return "too_short"
    return None


def wav_seconds(path: Path) -> float:
    with wave.open(str(path), "rb") as w:
        return w.getnframes() / float(w.getframerate())


def process_one(job):
    clip_id, src, dst, text = job
    dst = Path(dst)
    try:
        if not dst.exists() or dst.stat().st_size < 1000:
            dst.parent.mkdir(parents=True, exist_ok=True)
            cmd = ["ffmpeg", "-y", "-v", "error", "-i", src, "-af", AUDIO_FILTER,
                   "-ac", "1", "-ar", "24000", "-c:a", "pcm_s16le", str(dst)]
            r = subprocess.run(cmd, capture_output=True, text=True)
            if r.returncode != 0:
                return clip_id, None, "ffmpeg:" + r.stderr.strip()[:120], text
        dur = wav_seconds(dst)
    except Exception as e:  # noqa: BLE001
        return clip_id, None, "error:" + repr(e)[:120], text
    if dur < MIN_SEC:
        return clip_id, None, f"too_short_audio:{dur:.2f}s", text
    if dur > MAX_SEC:
        return clip_id, None, f"too_long_audio:{dur:.2f}s", text
    return clip_id, dur, None, text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--limit-hours", type=float, default=0.0, help="stop after this many hours of processed audio (0 = all)")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--valid-modulo", type=int, default=50, help="clip goes to valid when md5(id) %% N == 0 (about 2%%)")
    args = ap.parse_args()

    jsons = list(args.root.glob("*Transcripts.json"))
    if not jsons:
        sys.exit(f"No *Transcripts.json in {args.root}")
    data = json.load(open(jsons[0], encoding="utf-8"))["Transcripts"]

    rejected, jobs, domains = [], [], Counter()
    for clip_id, rec in data.items():
        text = clean_text(rec.get("Transcript", ""))
        why = reject_reason(text)
        src = args.root / "wav" / f"{clip_id}.wav"
        if why is None and not src.exists():
            why = "missing_wav"
        if why:
            rejected.append((clip_id, why, rec.get("Transcript", "").strip()))
            continue
        jobs.append((clip_id, str(src), str(args.out / "wavs" / f"{clip_id}.wav"), text))
        domains[rec.get("Domain", "?")] += 1

    random.Random(args.seed).shuffle(jobs)
    args.out.mkdir(parents=True, exist_ok=True)
    kept, total_sec = [], 0.0
    limit_sec = args.limit_hours * 3600
    batch = max(args.workers * 8, 64)
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        for i in range(0, len(jobs), batch):
            for clip_id, dur, why, text in pool.map(process_one, jobs[i:i + batch]):
                if why:
                    rejected.append((clip_id, why, text))
                else:
                    kept.append((clip_id, dur, text))
                    total_sec += dur
            print(f"processed {min(i + batch, len(jobs))}/{len(jobs)}  kept {len(kept)}  {total_sec / 3600:.2f} h", flush=True)
            if limit_sec and total_sec >= limit_sec:
                break

    train, valid = [], []
    for clip_id, dur, text in kept:
        row = {"path": str((args.out / "wavs" / f"{clip_id}.wav").resolve()), "duration": round(dur, 3), "transcript": text}
        is_valid = int(hashlib.md5(clip_id.encode()).hexdigest(), 16) % args.valid_modulo == 0
        (valid if is_valid else train).append(row)
    for name, rows in (("train", train), ("valid", valid)):
        with open(args.out / f"{name}.jsonl", "w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(args.out / "rejected.tsv", "w", encoding="utf-8") as f:
        for r in rejected:
            f.write("\t".join(str(x).replace("\t", " ") for x in r) + "\n")
    reasons = Counter(r[1].split(":")[0] for r in rejected)
    stats = {"clips_in_json": len(data), "kept": len(kept), "train": len(train), "valid": len(valid),
             "hours_kept": round(total_sec / 3600, 3), "rejected": len(rejected), "reject_reasons": dict(reasons),
             "domains_selected": dict(domains)}
    json.dump(stats, open(args.out / "stats.json", "w"), indent=2)
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
