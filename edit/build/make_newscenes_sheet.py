#!/usr/bin/env python3
"""新增畫面對照表 — one sheet of the newly added scenes, straight off the finished file.

Locates each named card on the OUTPUT timeline by accumulating the actual durations of
the rendered clips_graded segments (not the EDL's nominal ones — per-segment frame
quantization drifts them by a couple of hundred ms over a full video), grabs a frame
from the middle of each, and lays them out with the on-screen caption quoted beside.

    python make_newscenes_sheet.py <slug> CARD_a,CARD_b,... [-o out.png]
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

PROJ = Path(__file__).resolve().parents[2]
EDIT = PROJ / "edit"
FONTS = EDIT / "fonts"
EXPORTS = PROJ / "exports"

DELIVERED = {"shengping": "1_光陰的故事_過水橋瑠公圳.mp4",
             "hemei": "2_環境的影子_和美煤礦.mp4",
             "zhenshan": "3_期望的未來_振山煤礦.mp4"}
TITLES = {"shengping": "V1　光陰的故事（過水橋與瑠公圳）",
          "hemei": "V2　環境的影子（和美煤礦）",
          "zhenshan": "V3　期望的未來（振山煤礦與光明街）"}

# What each card says on screen, and one line on why it was added.
NOTES = {
    "CARD_today_mine":  ("今日的和美煤礦坑口", "原為單張，右側新增導覽當日坑口鐵柵前畫面"),
    "CARD_today_ferry": ("碧潭到和美渡船照", "新增：碧潭往和美的渡船"),
    "CARD_today_signs": ("和美煤礦坑口外的解說牌", "新增：坑口外解說牌三張一排"),
    "CARD_today_river": ("今日的新店溪與和美山", "未更動"),
}

W, MARGIN = 2200, 70
INK, MUTED, RULE, ACCENT = (26, 26, 26), (140, 140, 140), (214, 210, 204), (150, 106, 46)


def dur_of(p: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(p)], capture_output=True, text=True,
                         check=True)
    return float(out.stdout.strip())


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("cards", help="comma-separated EDL source names, in timeline order")
    ap.add_argument("-o", "--out", type=Path)
    args = ap.parse_args()
    wanted = [c for c in args.cards.split(",") if c]
    out_path = args.out or EXPORTS / "print" / f"新增畫面對照表_{args.slug}.png"

    edl = json.loads((EDIT / f"edl_{args.slug}.json").read_text())
    clips = EDIT / "clips_graded"
    video = EXPORTS / DELIVERED[args.slug]
    if not video.exists():
        raise SystemExit(f"delivered file not found: {video}")

    # Accumulate REAL segment durations so the offsets match the rendered timeline.
    offsets, t = {}, 0.0
    for i, r in enumerate(edl["ranges"]):
        seg = clips / f"seg_{i:02d}_{r['source']}.mp4"
        d = dur_of(seg)
        if r["source"] in wanted and r["source"] not in offsets:
            offsets[r["source"]] = (t, d)
        t += d
    missing = [c for c in wanted if c not in offsets]
    if missing:
        raise SystemExit(f"cards not found in the EDL: {missing}")

    f_title = ImageFont.truetype(str(FONTS / "NotoSerifTC-Medium.otf"), 56)
    f_sub = ImageFont.truetype(str(FONTS / "NotoSansTC-Medium.otf"), 28)
    f_cap = ImageFont.truetype(str(FONTS / "NotoSerifTC-Medium.otf"), 36)
    f_meta = ImageFont.truetype(str(FONTS / "NotoSansTC-Medium.otf"), 26)

    shot_w = W - 2 * MARGIN
    shot_h = round(shot_w * 9 / 16)
    row_h = 46 + shot_h + 14 + 46 + 32 + 30      # meta, shot, caption, note, rule
    H = MARGIN + 210 + len(wanted) * row_h + 2 * MARGIN

    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    y = MARGIN
    d.text((MARGIN, y), "新增畫面對照表", font=f_title, fill=INK); y += 78
    d.text((MARGIN, y), f"{TITLES[args.slug]}　—　新增之今貌畫面", font=f_sub, fill=MUTED)
    y += 42
    d.text((MARGIN, y), f"共 {len(wanted)} 處；畫面擷取自實際輸出檔案，字幕為影片中實際呈現之說明文字。",
           font=f_sub, fill=MUTED)
    y += 48
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=INK, width=3); y += 40

    for i, card in enumerate(wanted):
        start, dur = offsets[card]
        t_mid = start + dur / 2
        png = Path(f"/tmp/_ns_{args.slug}_{card}.png")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t_mid:.3f}",
                        "-i", str(video), "-frames:v", "1", str(png)], check=True)
        caption, why = NOTES.get(card, (card, ""))
        mm, ss = divmod(int(t_mid), 60)
        d.text((MARGIN, y), f"{mm:02d}:{ss:02d}", font=f_meta, fill=MUTED)
        d.text((MARGIN + 110, y), f"{dur:.1f} 秒", font=f_meta, fill=MUTED)
        y += 46
        img.paste(Image.open(png).convert("RGB").resize((shot_w, shot_h), Image.LANCZOS),
                  (MARGIN, y))
        d.rectangle([MARGIN, y, MARGIN + shot_w, y + shot_h], outline=RULE, width=2)
        y += shot_h + 14
        d.text((MARGIN, y), f"字幕：{caption}", font=f_cap, fill=ACCENT)
        y += 46
        if why:
            d.text((MARGIN, y), why, font=f_meta, fill=MUTED)
        y += 32
        if i < len(wanted) - 1:
            d.line([(MARGIN, y), (W - MARGIN, y)], fill=RULE, width=1)
        y += 30

    if y + MARGIN > H:
        raise SystemExit(f"content overflows the canvas ({y + MARGIN} > {H})")
    img = img.crop((0, 0, W, y + MARGIN))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path)
    print(f"{out_path}  ({len(wanted)} scenes, {img.width}x{img.height})")


if __name__ == "__main__":
    main()
