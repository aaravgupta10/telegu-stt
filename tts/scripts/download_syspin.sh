#!/usr/bin/env bash
# Download and unpack the SYSPIN archives on the AWS instance.
# STATUS: UNTESTED draft (written 2026-10-14).
#
# The signed download links from IISc's email are SECRET-ish (anyone with a link can download for 7 days) and expire
# about 2026-10-21 11:36 UTC. They must NOT be put in git or in our project files. Instead, create this file ON THE
# INSTANCE ONLY: ~/syspin_urls.txt, with ONE line per archive: the file name, a space, then the full URL.
#   IISc_SYSPINProject_Hindi_Female_Spk001_HC.tar.gz https://objectstore.e2enetworks.net/...(the long signed link)
#   IISc_SYSPINProject_Hindi_Male_Spk001_HC.tar.gz   https://objectstore.e2enetworks.net/...
#   IISc_SYSPINProject_Telugu_Female_Spk001_HC.tar.gz https://objectstore.e2enetworks.net/...
#   IISc_SYSPINProject_Telugu_Male_Spk001_HC.tar.gz  https://objectstore.e2enetworks.net/...
# (Copy the URL from inside the quotes of each wget line in the email.) Delete ~/syspin_urls.txt when done.
#
# Run inside tmux so it survives a dropped connection:  tmux new -s dl   then   bash download_syspin.sh
set -uo pipefail

LIST="$HOME/syspin_urls.txt"
OUT="$HOME/SageMaker/tts/data/raw"   # must be under ~/SageMaker (the 400 GB persistent volume)
MIN_FREE_GB=60
mkdir -p "$OUT"

[ -f "$LIST" ] || { echo "Missing $LIST (see the comments at the top of this script)"; exit 1; }

while read -r name url; do
  [ -z "${name:-}" ] && continue
  if [ -f "$OUT/$name.done" ]; then echo "skip (already done): $name"; continue; fi

  free_gb=$(df -BG --output=avail "$OUT" | tail -1 | tr -dc '0-9')
  if [ "$free_gb" -lt "$MIN_FREE_GB" ]; then echo "Only ${free_gb} GB free (< ${MIN_FREE_GB}). Stopping."; exit 1; fi

  echo "== downloading $name  ($(date))"
  # -c resumes a partial download if the connection drops; re-run this script to continue.
  wget -c --tries=20 --waitretry=10 "$url" -O "$OUT/$name" || { echo "download failed for $name; re-run to resume"; exit 1; }

  echo "== extracting $name"
  dest="$OUT/${name%.tar.gz}"
  mkdir -p "$dest"
  tar -xzf "$OUT/$name" -C "$dest" || { echo "extract failed for $name"; exit 1; }

  rm -f "$OUT/$name"        # free the space taken by the archive
  touch "$OUT/$name.done"
  echo "== finished $name  ($(date))"
done < "$LIST"

echo "All archives processed. Sizes:"
du -sh "$OUT"/*/ 2>/dev/null || true
echo "Now delete $LIST (it contains signed links)."
