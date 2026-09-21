#!/bin/bash
# Full-quality export: build → render (final) → grade+burn subs → music → exports/
#
#   ./export_final.sh            all three
#   ./export_final.sh shengping  just one
#
# Output lands in exports/ under the numbered Chinese delivery names.
set -euo pipefail

PROJ="$(cd "$(dirname "$0")/../.." && pwd)"
# video-use skill checkout; override with VIDEO_USE_DIR. Default: first Google Drive account's copy.
VU="${VIDEO_USE_DIR:-$(ls -d "$HOME"/Library/CloudStorage/GoogleDrive-*/"My Drive/claude-skills/video-use" 2>/dev/null | head -n 1)}"
: "${VU:?set VIDEO_USE_DIR to the video-use skill directory}"
PY="$VU/.venv/bin/python"
OUT="$PROJ/exports"
mkdir -p "$OUT"

name_for () {
  case "$1" in
    shengping) echo "1_光陰的故事_過水橋瑠公圳" ;;
    hemei)     echo "2_環境的影子_和美煤礦" ;;
    zhenshan)  echo "3_期望的未來_振山煤礦" ;;
  esac
}

SLUGS=${*:-"shengping hemei zhenshan"}
for slug in $SLUGS; do
  echo ""
  echo "════════════════════════════════════════ $slug"
  bash "$PROJ/edit/build/rebuild.sh" "$slug" --final
  "$PY" "$PROJ/edit/build/mix_music.py" "$slug" \
        "$PROJ/edit/${slug}_final.mp4" "$OUT/$(name_for "$slug").mp4"
done

echo ""
echo "════════════════════════════════════════ exports"
for f in "$OUT"/*.mp4; do
  printf "  %-46s %7.1fs  %s\n" "$(basename "$f")" \
    "$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f")" \
    "$(du -h "$f" | cut -f1)"
done
