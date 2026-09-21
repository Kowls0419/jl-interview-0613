#!/bin/zsh
# Copy the current previews into product/ as REAL FILES (numbered Chinese names).
# product/ lives on Google Drive, which does NOT sync symlinks — so we copy, not link.
# Run after any re-render/re-burn. Idempotent.
PROJ="${0:A:h:h:h}"   # project root = two levels above edit/build/
cd "$PROJ"
# V4 製作花絮 abandoned as a standalone (Kyle, 2026-08-13) — its material now
# lives in each video's animated closer, so it is no longer synced here.
# product/4_製作花絮.mp4 from the old build is left in place; delete when ready.
declare -A MAP=(
  [shengping]="1_光陰的故事_過水橋瑠公圳"
  [hemei]="2_環境的影子_和美煤礦"
  [zhenshan]="3_期望的未來_振山煤礦"
)
for base out in ${(kv)MAP}; do
  src="edit/${base}_preview.mp4"
  dst="product/${out}.mp4"
  if [ -f "$src" ]; then
    cp "$src" "$dst"
    echo "  product/${out}.mp4  ← ${base}_preview.mp4  ($(ffprobe -v error -show_entries format=duration -of csv=p=0 "$dst" 2>/dev/null)s)"
  else
    echo "  MISSING $src — skipped"
  fi
done
