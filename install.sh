#!/usr/bin/env bash
set -euo pipefail

SRC_DIR="$(cd "$(dirname "$0")" && pwd)/skills"
DEST_DIR="${HOME}/.agents/skills"

mkdir -p "$DEST_DIR"

SKILLS=(
  max-image-gen
  max-video-gen
  max-tts
  max-voice-clone
  max-music-gen
  max-music-cover
  max-search
  max-vision
  max-text-chat
)

for d in "${SKILLS[@]}"; do
  if [ -d "$SRC_DIR/$d" ]; then
    if [ -d "$DEST_DIR/$d" ]; then
      rm -rf "$DEST_DIR/$d"
    fi
    cp -R "$SRC_DIR/$d" "$DEST_DIR/"
    echo "Installed: $d"
  else
    echo "Skip (not found in package): $d"
  fi
done

echo "Done. Skills installed to: $DEST_DIR"
