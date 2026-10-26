#!/usr/bin/env python3
"""Prepare Rasa Telugu (ai4bharat/Rasa, Parquet shards with embedded WAV bytes) for Pocket TTS fine-tuning.

STATUS: written 2026-10-18 against the schema seen on the notebook (columns filename, text, language, gender, style,
duration (string, seconds), wav_path, audio{bytes, path}); tested locally on a synthetic Parquet file only.

Same text rules and the same audio chain as prep_syspin.py (it imports them, so keep both files in one folder):
text: NFC, zero-width removal, punctuation tidy, drop clips with digits or non-Telugu characters or under 2 words;
audio: trim silence at both ends, loudness-normalise, 24 kHz mono 16-bit; drop clips under 1 s or over 30 s.
All Parquet files found (train and test shards) are used as training data; our own validation split is made by md5 of the id.

Needs pyarrow. Run it with:   uv run --with pyarrow python prep_rasa.py --root <dir with Telugu/> --out <dir>
Output (under --out): wavs/<id>.wav, train.jsonl, valid.jsonl, rejected.tsv, meta.tsv (id, gender, style, seconds), stats.json
"""
import argparse
import hashlib
import json
import subprocess
import sys
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from prep_syspin import AUDIO_FILTER, MAX_SEC, MIN_SEC, clean_text, reject_reason, wav_seconds  # noqa: E402


def process_one(job):
    clip_id, wav_bytes, text, out_dir = job
    dst = Path(out_dir) / f"{clip_id}.wav"
    try:
        cmd = ["ffmpeg", "-y", "-v", "error", "-i", "pipe:0", "-af", AUDIO_FILTER,
               "-ac", "1", "-ar", "24000", "-c:a", "pcm_s16le", str(dst)]
        r = subprocess.run(cmd, input=wav_bytes, capture_output=True)
        if r.returncode != 0:
            dst.unlink(missing_ok=True)
            return clip_id, None, f"ffmpeg:rc{r.returncode}:" + r.stderr.decode("utf-8", "replace").strip()[:100], text
        dur = wav_seconds(dst)
    except Exception as e:  # noqa: BLE001
        dst.unlink(missing_ok=True)
        return clip_id, None, "error:" + repr(e)[:120], text
    if dur < MIN_SEC:
        dst.unlink(missing_ok=True)
        return clip_id, None, f"too_short_audio:{dur:.2f}s", text
    if dur > MAX_SEC:
        dst.unlink(missing_ok=True)
        return clip_id, None, f"too_long_audio:{dur:.2f}s", text
    return clip_id, dur, None, text


def main():
    import pyarrow.parquet as pq

    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, type=Path, help="folder that contains Telugu/*.parquet (or the parquet files directly)")
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--workers", type=int, default=40)
    ap.add_argument("--styles", default="", help="comma list of Rasa styles to keep (default: all)")
    ap.add_argument("--valid-modulo", type=int, default=50)
    ap.add_argument("--batch-jobs", type=int, default=1500, help="clips handed to the worker pool at once")
    args = ap.parse_args()

    shards = sorted(args.root.glob("Telugu/*.parquet")) or sorted(args.root.glob("*.parquet"))
    if not shards:
        sys.exit(f"No parquet files under {args.root}")
    keep_styles = {s.strip() for s in args.styles.split(",") if s.strip()}
    wav_dir = args.out / "wavs"
    wav_dir.mkdir(parents=True, exist_ok=True)

    rejected, kept, meta, seen = [], [], {}, set()
    total_sec, n_rows = 0.0, 0
    styles_seen, reasons_pre = Counter(), Counter()
    buf = []

    def flush(pool):
        nonlocal total_sec
        for clip_id, dur, why, text in pool.map(process_one, buf, chunksize=4):
            if why:
                rejected.append((clip_id, why, text))
            else:
                kept.append((clip_id, dur, text))
                total_sec += dur
        buf.clear()
        print(f"rows {n_rows}  kept {len(kept)}  {total_sec / 3600:.2f} h  rejected {len(rejected)}", flush=True)

    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        for shard in shards:
            pf = pq.ParquetFile(shard)
            for batch in pf.iter_batches(batch_size=128, columns=["filename", "text", "gender", "style", "duration", "audio"]):
                for row in batch.to_pylist():
                    n_rows += 1
                    clip_id = row["filename"]
                    styles_seen[row["style"]] += 1
                    if keep_styles and row["style"] not in keep_styles:
                        reasons_pre["style_skipped"] += 1
                        continue
                    if clip_id in seen:
                        rejected.append((clip_id, "duplicate_id", row["text"]))
                        continue
                    seen.add(clip_id)
                    text = clean_text(row["text"] or "")
                    why = reject_reason(text)
                    try:
                        sec = float(row["duration"])
                    except (TypeError, ValueError):
                        sec = None
                    if why is None and sec is not None and not (MIN_SEC <= sec <= MAX_SEC + 5):
                        why = f"duration_column:{sec:.2f}s"
                    if why is None and not (row["audio"] and row["audio"].get("bytes")):
                        why = "no_audio"
                    if why:
                        rejected.append((clip_id, why, (row["text"] or "").strip()))
                        continue
                    meta[clip_id] = (row["gender"], row["style"])
                    buf.append((clip_id, row["audio"]["bytes"], text, str(wav_dir)))
                    if len(buf) >= args.batch_jobs:
                        flush(pool)
            print(f"finished shard {shard.name}", flush=True)
        if buf:
            flush(pool)

    train, valid = [], []
    for clip_id, dur, text in kept:
        row = {"path": str((wav_dir / f"{clip_id}.wav").resolve()), "duration": round(dur, 3), "transcript": text}
        is_valid = int(hashlib.md5(clip_id.encode()).hexdigest(), 16) % args.valid_modulo == 0
        (valid if is_valid else train).append(row)
    for name, rows in (("train", train), ("valid", valid)):
        with open(args.out / f"{name}.jsonl", "w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(args.out / "rejected.tsv", "w", encoding="utf-8") as f:
        for r in rejected:
            f.write("\t".join(str(x).replace("\t", " ").replace("\n", " ") for x in r) + "\n")
    with open(args.out / "meta.tsv", "w", encoding="utf-8") as f:
        for clip_id, dur, _ in kept:
            g, s = meta[clip_id]
            f.write(f"{clip_id}\t{g}\t{s}\t{dur:.3f}\n")
    reasons = Counter(r[1].split(":")[0] for r in rejected) + reasons_pre
    by_style = Counter()
    for clip_id, dur, _ in kept:
        by_style[meta[clip_id][1]] += dur / 3600
    stats = {"rows_in_parquet": n_rows, "kept": len(kept), "train": len(train), "valid": len(valid),
             "hours_kept": round(total_sec / 3600, 3), "rejected": len(rejected), "reject_reasons": dict(reasons),
             "styles_in_data": dict(styles_seen), "hours_kept_by_style": {k: round(v, 2) for k, v in by_style.items()}}
    json.dump(stats, open(args.out / "stats.json", "w"), indent=2)
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
