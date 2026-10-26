#!/usr/bin/env bash
# Set up a fresh Linux GPU machine (a SageMaker ml.g5.2xlarge notebook on Amazon Linux, or an Ubuntu EC2 GPU box) for Pocket TTS training.
# STATUS: UNTESTED draft (written 2026-10-14). Read it before running. It makes no payments and never touches Hugging Face tokens.
set -euo pipefail

echo "== GPU =="
nvidia-smi || { echo "No NVIDIA GPU or driver found. Stop here."; exit 1; }

echo "== Disk (we want 300 GB or more free on the data disk) =="
df -h /

echo "== System packages =="
# SageMaker notebook instances run Amazon Linux (dnf/yum), NOT Ubuntu (apt). Handle both.
if command -v apt-get >/dev/null 2>&1; then
  sudo apt-get update -y
  sudo apt-get install -y git ffmpeg sox tmux
elif command -v dnf >/dev/null 2>&1; then
  sudo dnf install -y git tmux
elif command -v yum >/dev/null 2>&1; then
  sudo yum install -y git tmux
else
  echo "No known package manager found; install git, tmux, ffmpeg and sox by hand."
fi
# ffmpeg is missing from Amazon Linux's default repos. Install a bundled static build from PyPI into an ISOLATED venv
# (do NOT touch the notebook's shared conda base environment; other projects may use it).
if ! command -v ffmpeg >/dev/null 2>&1; then
  python3 -m venv "$HOME/SageMaker/tts/venv_tools"
  "$HOME/SageMaker/tts/venv_tools/bin/pip" install -q imageio-ffmpeg
  mkdir -p "$HOME/SageMaker/bin"
  ln -sf "$("$HOME/SageMaker/tts/venv_tools/bin/python" -c 'import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())')" "$HOME/SageMaker/bin/ffmpeg"
fi

# IMPORTANT (SageMaker notebooks): only ~/SageMaker survives Stop/Start and instance-type changes.
# Everything we want to keep (uv, Python interpreters, caches, repo, venv, data) goes under ~/SageMaker.
# System packages (git, tmux, ffmpeg, sox) are NOT kept: re-run this script after every Start.
BASE="$HOME/SageMaker/tts"
mkdir -p "$BASE" "$HOME/SageMaker/bin"
export UV_INSTALL_DIR="$HOME/SageMaker/bin"
export UV_CACHE_DIR="$HOME/SageMaker/uv-cache"
export UV_PYTHON_INSTALL_DIR="$HOME/SageMaker/uv-python"
export HF_HOME="$HOME/SageMaker/hf-home"
export PATH="$HOME/SageMaker/bin:$PATH"
# Make these settings stick for every new terminal after a Start:
grep -q 'SageMaker/bin' "$HOME/.bashrc" 2>/dev/null || cat >> "$HOME/.bashrc" <<'EOF'
export UV_INSTALL_DIR="$HOME/SageMaker/bin"
export UV_CACHE_DIR="$HOME/SageMaker/uv-cache"
export UV_PYTHON_INSTALL_DIR="$HOME/SageMaker/uv-python"
export HF_HOME="$HOME/SageMaker/hf-home"
export PATH="$HOME/SageMaker/bin:$PATH"
EOF

echo "== uv (Python tool Kyutai's repo uses) =="
[ -x "$HOME/SageMaker/bin/uv" ] || curl -LsSf https://astral.sh/uv/install.sh | sh

echo "== Kyutai pocket-tts repo =="
cd "$BASE"
[ -d pocket-tts ] || git clone https://github.com/kyutai-labs/pocket-tts.git
cd pocket-tts
uv sync

echo "== Check torch sees the GPU =="
uv run python -c "import torch; print('torch', torch.__version__, '| cuda available:', torch.cuda.is_available())"

mkdir -p "$BASE/data/raw" "$BASE/data/work" "$BASE/runs"

echo
echo "Done. Next steps (you run these yourself):"
echo "  1) hf auth login        # paste your OWN Hugging Face token on the instance only; never in chat"
echo "  2) create ~/syspin_urls.txt (see download_syspin.sh) and run: bash download_syspin.sh"
echo "  3) uv run pocket-tts generate   # quick test that the English model runs (needs the gate accepted)"
