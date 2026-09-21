#!/bin/bash
# Rebuild one video end-to-end: cards+EDL+SRT -> render -> grade+subtitle burn.
#
#   ./rebuild.sh <slug> [--final]
#     slug: shengping (V1 光陰的故事) | hemei (V2 環境的影子) | zhenshan (V3 期望的未來)
#
# --no-loudnorm is MANDATORY: loudnorm bleeds the previous segment's tail into
# silent gaps (reflect L01). YouTube re-normalizes on upload, so nothing is lost.
# Subtitles burn LAST, after the grade, so overlays never hide them.
set -euo pipefail

SLUG="${1:?usage: rebuild.sh <shengping|hemei|zhenshan> [--final]}"
MODE="${2:-}"
# video-use skill checkout; override with VIDEO_USE_DIR. Default: first Google Drive account's copy.
VU="${VIDEO_USE_DIR:-$(ls -d "$HOME"/Library/CloudStorage/GoogleDrive-*/"My Drive/claude-skills/video-use" 2>/dev/null | head -n 1)}"
: "${VU:?set VIDEO_USE_DIR to the video-use skill directory}"
PY="$VU/.venv/bin/python"
EDIT="$(cd "$(dirname "$0")/.." && pwd)"

case "$SLUG" in
  shengping) BUILD=video3_shengping.py ;;
  hemei)     BUILD=video2_hemei.py ;;
  zhenshan)  BUILD=video1_zhenshan.py ;;
  *) echo "unknown slug: $SLUG" >&2; exit 1 ;;
esac

if [ "$MODE" = "--final" ]; then QUALITY=(); TAG=final; else QUALITY=(--preview); TAG=preview; fi

# natural historic warm grade, then subtitles LAST
GRADE="colorbalance=rs=.02:gs=.005:bs=-.025:rm=.025:gm=.008:bm=-.02,eq=contrast=1.04:saturation=0.95"
STYLE="FontName=LXGW WenKai TC,FontSize=18,Outline=1.6,Shadow=0,BorderStyle=1,\
PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,Alignment=2,MarginV=30"

echo "══ 1/3  build cards + EDL + SRT  ($BUILD)"
"$PY" "$EDIT/build/$BUILD"

echo "══ 2/3  render (no subs, no loudnorm)"
# ${A[@]+"${A[@]}"} — macOS bash 3.2 treats an EMPTY array expansion as an
# unbound variable under `set -u`, which is exactly the --final case.
"$PY" "$VU/helpers/render.py" "$EDIT/edl_${SLUG}.json" \
  -o "$EDIT/${SLUG}_nosub.mp4" ${QUALITY[@]+"${QUALITY[@]}"} \
  --no-subtitles --no-loudnorm

echo "══ 3/3  grade + burn subtitles + fade to black"
cd "$EDIT"
# The cards fade to the warm BG (18,15,12), which the grade then LIFTS to about
# (26,22,12) — so the picture never actually reached black. This final fade
# takes the graded image all the way down. It runs LAST, after the subtitles,
# so any trailing cue fades with the picture instead of sitting on top of it.
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "${SLUG}_nosub.mp4")
FADE=2.0
FSTART=$(echo "$DUR - $FADE" | bc)
echo "   fade to black: ${FSTART}s +${FADE}s  (of ${DUR}s)"
ffmpeg -y -v warning -stats -i "${SLUG}_nosub.mp4" \
  -vf "${GRADE},subtitles=${SLUG}_zht.srt:fontsdir=fonts:force_style='${STYLE}',fade=t=out:st=${FSTART}:d=${FADE}:color=black" \
  -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p \
  -c:a copy "${SLUG}_${TAG}.mp4"

echo "── done: $EDIT/${SLUG}_${TAG}.mp4"
ffprobe -v error -show_entries format=duration -of csv=p=0 "$EDIT/${SLUG}_${TAG}.mp4"
