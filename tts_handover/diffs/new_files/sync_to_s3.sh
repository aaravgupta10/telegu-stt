#!/usr/bin/env bash
# Keep a training run's checkpoints and samples backed up to S3 while it trains (crash protection).
# STATUS: UNTESTED draft (written 2026-10-15).
#
# Usage (inside its own tmux window, next to the training run):
#   export BUCKET=your-bucket-name
#   export RUN_DIR=$HOME/tts/pocket-tts/runs/hindi_teacher     # the run_dir from the YAML
#   export RUN_NAME=hindi_teacher
#   bash sync_to_s3.sh            # syncs every 10 minutes; press Ctrl-C to stop
#
# Needs: an IAM role (or AWS profile) on the notebook that may read/write s3://$BUCKET. No keys in this file.
# Restore after a crash (on a new notebook):
#   aws s3 sync s3://$BUCKET/checkpoints/$RUN_NAME $RUN_DIR
# then restart training from the latest checkpoint as described in Kyutai's training README.
set -uo pipefail

: "${BUCKET:?set BUCKET}"
: "${RUN_DIR:?set RUN_DIR}"
: "${RUN_NAME:?set RUN_NAME}"
INTERVAL="${INTERVAL:-600}"

while true; do
  if [ -d "$RUN_DIR" ]; then
    echo "$(date -u +%FT%TZ) syncing $RUN_DIR -> s3://$BUCKET/checkpoints/$RUN_NAME/"
    aws s3 sync "$RUN_DIR" "s3://$BUCKET/checkpoints/$RUN_NAME/" \
      --exclude "*" \
      --include "args.yaml" --include "progress.jsonl" \
      --include "checkpoint_*.pt" --include "optim_*.pt" \
      --include "model.safetensors" --include "samples/*" \
      || echo "sync failed this round; will retry"
  else
    echo "waiting for $RUN_DIR to exist"
  fi
  sleep "$INTERVAL"
done
