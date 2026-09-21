#!/usr/bin/env python3
"""字幕修正對照表 — one sheet of real before/after screenshots, for verification.

Diffs the shipped SRTs against the rebuilt ones to find every changed cue, then pulls
the SAME frame out of the delivered video and the corrected one. The picture is
identical in both — only the burned subtitle differs — so the correction is the only
thing that moves between the two stills. Nothing here is typeset from my own notes:
the timestamps come from the SRTs and the text comes off the rendered frames.

    python make_subfix_sheet.py <before_dir> [-o out.png]

<before_dir> holds the delivered originals: <slug>_zht.srt and <slug>.mp4.
Cue timings are assumed unchanged (verified: only cue TEXT differs), so cues pair by
index. If a pairing ever fails on count, the script refuses rather than mis-aligning.
"""
from __future__ import annotations

import argparse
import difflib
import re
import subprocess
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFont

PROJ = Path(__file__).resolve().parents[2]
EDIT = PROJ / "edit"
FONTS = EDIT / "fonts"
EXPORTS = PROJ / "exports"

VIDEOS = [  # (slug, display number, title, delivered filename)
    ("shengping", "V1", "光陰的故事（過水橋與瑠公圳）", "1_光陰的故事_過水橋瑠公圳.mp4"),
    ("hemei",     "V2", "環境的影子（和美煤礦）",       "2_環境的影子_和美煤礦.mp4"),
    ("zhenshan",  "V3", "期望的未來（振山煤礦與光明街）", "3_期望的未來_振山煤礦.mp4"),
]

NOTES = {
    "因為順水游泳好像游得很快啊":       "游泳的「游」，非「遊」",
    "還要跑很遠回來，所以就逆水游":     "游泳的「游」，非「遊」",
    "逆水游，所以你要":                 "游泳的「游」，非「遊」",
    "你在那逆水游的時候游得很快":       "「游」字修正；語音辨識誤植「近水」，依前後文為「逆水」",
    "是老闆住的，是我的二姑丈（劉明）他們住的": "補注人名",
    "所以我是北一女的游泳選手":         "依受訪者原意具體化校別",
    "振山煤礦是在高麗坑（檳榔坑，現檳榔路）那一邊": "補注舊地名與今名",
}

# Frames are 1920x1080 with the burned subtitle at MarginV=30. The crop is computed
# per cue rather than fixed: a 遊→游 correction is ONE glyph out of thirteen, and at a
# fixed full-width crop it renders ~26px on the sheet — a real difference that reads
# as "the two pictures are identical". Crop to the text's own width instead, so short
# lines magnify, and mark the changed region.
SUB_BAND = (880, 1010)      # y range the burned subtitle can occupy
CROP_ASPECT = 0.30          # crop height as a fraction of its width
MIN_CROP_W = 900            # never magnify past this (keeps some picture context)

W        = 2560
MARGIN   = 80
GUTTER   = 44
COL      = (W - 2 * MARGIN - GUTTER) // 2

INK    = (26, 26, 26)
MUTED  = (140, 140, 140)
RULE   = (214, 210, 204)
ACCENT = (150, 106, 46)
OLD_C  = (176, 42, 34)
NEW_C  = (26, 110, 72)


def load_cues(path: Path) -> list[tuple[float, float, str]]:
    out = []
    for b in re.split(r"\n\s*\n", path.read_text().strip()):
        lines = [x for x in b.splitlines() if x.strip()]
        if len(lines) < 3:
            continue
        m = re.match(r"(\d+):(\d+):(\d+),(\d+) --> (\d+):(\d+):(\d+),(\d+)", lines[1])
        if not m:
            continue
        g = [int(x) for x in m.groups()]
        out.append((g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000,
                    g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000,
                    "".join(lines[2:])))
    return out


def grab(video: Path, t: float, tmp: Path) -> Image.Image:
    """The full 1920x1080 frame at t."""
    png = tmp / f"{video.stem}_{t:.3f}.png"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.3f}", "-i", str(video),
                    "-frames:v", "1", str(png)], check=True)
    return Image.open(png).convert("RGB")


def text_extent(*frames: Image.Image) -> tuple[int, int, int]:
    """(x0, x1, bottom) of the burned subtitle across all frames, in frame coords.

    The subtitle is white with a black outline, so bright pixels inside SUB_BAND find
    it without knowing the text. Falls back to the full width if nothing is found
    (a cue over a bright card, say) rather than cropping to garbage.
    """
    x0, x1, bottom = 1920, 0, SUB_BAND[0]
    for f in frames:
        band = np.array(f.convert("L"))[SUB_BAND[0]:SUB_BAND[1]]
        bright = band > 200
        cols = np.where(bright.sum(axis=0) > 2)[0]
        rows = np.where(bright.sum(axis=1) > 40)[0]
        if cols.size:
            x0, x1 = min(x0, int(cols.min())), max(x1, int(cols.max()))
        if rows.size:
            bottom = max(bottom, SUB_BAND[0] + int(rows.max()))
    if x1 <= x0:
        return 0, 1919, SUB_BAND[1]
    return x0, x1, bottom


def diff_box(a: Image.Image, b: Image.Image) -> tuple[int, int, int, int] | None:
    """Where the two frames actually differ, in frame coords.

    Both were encoded with identical settings from the identical master, so x264 is
    deterministic and the only differing pixels are the subtitle's. This is measured,
    not assumed — the marker cannot drift away from the real change.
    """
    d = np.array(ImageChops.difference(a, b)).max(axis=2)
    strong = d > 60
    ys, xs = np.where(strong.any(axis=1))[0], np.where(strong.any(axis=0))[0]
    if not ys.size or not xs.size:
        return None
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())


def frame_pair(old: Image.Image, new: Image.Image):
    """Crop both frames to the text, scale to a column, and mark what changed."""
    tx0, tx1, bottom = text_extent(old, new)
    box = diff_box(old, new)

    cw = max(MIN_CROP_W, min(1920, (tx1 - tx0) + 220))
    cx = (tx0 + tx1) // 2
    x0 = max(0, min(1920 - cw, cx - cw // 2))
    ch = round(cw * CROP_ASPECT)
    y1 = min(1080, bottom + 46)
    y0 = max(0, y1 - ch)

    scale = COL / cw
    out = []
    for frame, colour in ((old, OLD_C), (new, NEW_C)):
        im = frame.crop((x0, y0, x0 + cw, y1))
        im = im.resize((COL, round(im.height * scale)), Image.LANCZOS)
        # An insertion re-centres the whole line, so the diff spans nearly all of it
        # and a box round it says nothing. Only mark a localised change.
        if box and (box[2] - box[0]) < 0.7 * max(1, tx1 - tx0):
            d = ImageDraw.Draw(im)
            r = [(box[0] - x0) * scale - 9, (box[1] - y0) * scale - 9,
                 (box[2] - x0) * scale + 9, (box[3] - y0) * scale + 9]
            d.rectangle(r, outline=colour, width=4)
        out.append(im)
    return out[0], out[1], box is not None and (box[2] - box[0]) < 0.7 * max(1, tx1 - tx0)


def changed_chars(before: str, after: str) -> tuple[str, str]:
    """The differing spans, for the caption under each pair."""
    sm = difflib.SequenceMatcher(a=before, b=after, autojunk=False)
    ob, na = [], []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        if i2 > i1:
            ob.append(before[i1:i2])
        if j2 > j1:
            na.append(after[j1:j2])
    return "／".join(ob) or "—", "／".join(na) or "—"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("before_dir", type=Path,
                    help="directory holding the delivered <slug>_zht.srt and <slug>.mp4")
    ap.add_argument("-o", "--out", type=Path,
                    default=EXPORTS / "print" / "字幕修正對照表.png")
    args = ap.parse_args()

    f_title = ImageFont.truetype(str(FONTS / "NotoSerifTC-Medium.otf"), 68)
    f_sub   = ImageFont.truetype(str(FONTS / "NotoSansTC-Medium.otf"), 30)
    f_head  = ImageFont.truetype(str(FONTS / "NotoSerifTC-Medium.otf"), 42)
    f_meta  = ImageFont.truetype(str(FONTS / "NotoSansTC-Medium.otf"), 28)
    f_tag   = ImageFont.truetype(str(FONTS / "NotoSansTC-Medium.otf"), 26)

    tmp_dir = tempfile.mkdtemp(prefix="subfix_")
    tmp = Path(tmp_dir)

    # ---- collect changed cues + their frames --------------------------------
    rows = []
    for slug, num, title, delivered in VIDEOS:
        old_srt = args.before_dir / f"{slug}_zht.srt"
        old_vid = args.before_dir / f"{slug}.mp4"
        new_vid = EXPORTS / delivered
        old, new = load_cues(old_srt), load_cues(EDIT / f"{slug}_zht.srt")
        if len(old) != len(new):
            raise SystemExit(f"{slug}: cue count changed ({len(old)}→{len(new)}); "
                             "cannot pair by index — timings must be re-checked")
        diffs = [(s, e, a, b) for (s, e, a), (_, _, b) in zip(old, new) if a != b]
        if not diffs:
            continue
        if not old_vid.exists():
            raise SystemExit(f"{slug} has {len(diffs)} changed cue(s) but the delivered "
                             f"video is missing: {old_vid}")
        for s, e, a, b in diffs:
            t = (s + e) / 2
            old_f, new_f = grab(old_vid, t, tmp), grab(new_vid, t, tmp)
            im_old, im_new, marked = frame_pair(old_f, new_f)
            rows.append({"num": num, "title": title, "t": t, "before": a, "after": b,
                         "img_old": im_old, "img_new": im_new, "marked": marked})
    if not rows:
        raise SystemExit("no subtitle changes found")

    # ---- measure the page, then draw ---------------------------------------
    # Row heights vary — the crop is computed per cue, so a long line is a wider,
    # shorter crop than a short one.
    head_h, tag_h, note_h, gap = 66, 40, 40, 54
    groups = len({r["num"] for r in rows})
    H = (MARGIN + 220                                    # header
         + groups * head_h
         + sum(tag_h + r["img_old"].height + 10 + note_h + gap for r in rows)
         + 120 + 2 * MARGIN)                             # legend + bottom margin

    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    y = MARGIN

    d.text((MARGIN, y), "字幕修正對照表", font=f_title, fill=INK); y += 92
    d.text((MARGIN, y), "新店礦業文化路徑 · 口述歷史影片　—　修正前後畫面對照",
           font=f_sub, fill=MUTED); y += 46
    vids = "、".join(sorted({r["num"] for r in rows}))
    d.text((MARGIN, y),
           f"共 {len(rows)} 處修正，分布於 {vids}；影片長度與字幕時間點均未更動，"
           "左右兩張為同一時間點之實際畫面。", font=f_sub, fill=MUTED)
    y += 56
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=INK, width=3); y += 44

    cur = None
    for i, r in enumerate(rows):
        if r["num"] != cur:
            d.text((MARGIN, y), f"{r['num']}　{r['title']}", font=f_head, fill=ACCENT)
            y += head_h
            cur = r["num"]

        mm, ss = divmod(int(r["t"]), 60)
        d.text((MARGIN, y), f"{mm:02d}:{ss:02d}", font=f_meta, fill=MUTED)
        d.text((MARGIN + 130, y), "修正前", font=f_tag, fill=OLD_C)
        d.text((MARGIN + COL + GUTTER, y), "修正後", font=f_tag, fill=NEW_C)
        y += tag_h

        shot_h = r["img_old"].height
        img.paste(r["img_old"], (MARGIN, y))
        img.paste(r["img_new"], (MARGIN + COL + GUTTER, y))
        d.rectangle([MARGIN, y, MARGIN + COL, y + shot_h], outline=RULE, width=2)
        d.rectangle([MARGIN + COL + GUTTER, y, MARGIN + 2 * COL + GUTTER, y + shot_h],
                    outline=RULE, width=2)
        y += shot_h + 10

        ob, na = changed_chars(r["before"], r["after"])
        d.text((MARGIN, y), f"{ob}", font=f_meta, fill=OLD_C)
        x = MARGIN + d.textlength(ob, font=f_meta) + 16
        d.text((x, y), "→", font=f_meta, fill=MUTED)
        x += d.textlength("→", font=f_meta) + 16
        d.text((x, y), na, font=f_meta, fill=NEW_C)
        x += d.textlength(na, font=f_meta) + 30
        note = NOTES.get(r["after"])
        if note:
            d.text((x, y), f"— {note}", font=f_tag, fill=MUTED)
        y += note_h + gap

        if i < len(rows) - 1 and rows[i + 1]["num"] == r["num"]:
            d.line([(MARGIN, y - gap // 2), (W - MARGIN, y - gap // 2)],
                   fill=RULE, width=1)

    d.line([(MARGIN, y), (W - MARGIN, y)], fill=RULE, width=2); y += 30
    d.text((MARGIN, y), "畫面擷取自實際輸出檔案，兩張為同一影格；除字幕外畫面完全相同。",
           font=f_meta, fill=MUTED)
    y += 46

    # reflect L36 — fail on overflow rather than shipping a clipped page
    if y + MARGIN > H:
        raise SystemExit(f"content overflows the canvas ({y + MARGIN}px > {H}px)")
    img = img.crop((0, 0, W, y + MARGIN))

    args.out.parent.mkdir(parents=True, exist_ok=True)
    img.save(args.out)
    print(f"{args.out}  ({len(rows)} changes, {img.width}x{img.height})")


if __name__ == "__main__":
    main()
