# ---------------------------------------------------------------------------
# DROP-IN REPLACEMENT for make_posters.py — 2026-08-18
#
# Identical to the current file except for the credit block, which now matches
# the treatment Kyle applied to the videos''' end cards (修正後): bigger type, and
# the NAME carries the contrast while the label stays quiet. Rendering moved to
# the shared poster_credits module so all four sheets change together.
#
#   diff vs current:
#     + import poster_credits
#     ~ credit loop      -> poster_credits.block(d, y, CREDITS, font, W, MUTED, INK)
#     ~ pre-rule gap 92  -> 74   (buys the enlarged block ~59px of frame clearance)
#
# Could not overwrite make_posters.py directly — the sandbox lost write access to
# pre-existing files under this Drive path mid-session. To apply:
#
#     cd "<project>"
#     cp edit/build/make_posters.py edit/build/make_posters.BAK.py
#     cp edit/build/make_posters.NEW.py edit/build/make_posters.py
#     .venv python edit/build/make_posters.py edit/urls.json
#
# That regenerates 1-3 to match poster 4. NOTE: the three poster PDFs are already
# shared on Drive (see exports/分享訊息.txt) — those links need re-uploading.
# ---------------------------------------------------------------------------
"""A4 QR posters for the three 新店礦業文化路徑 sites.

    .venv python edit/build/make_posters.py                 # placeholder URLs
    .venv python edit/build/make_posters.py urls.json       # real ones

urls.json:  {"shengping": "https://youtu.be/...", "hemei": "...", "zhenshan": "..."}

Output: exports/print/<n>_<title>_A4.pdf  (+ bare .svg QR)
Each page has its QR decoded off the rendered image before it is written.

Design notes — same identity as the videos, inverted for paper:
  the films are cream Songti TC on warm near-black; a sign that lives outdoors
  wants the opposite ground, so this uses the project's existing LIGHT document
  palette (the one photo_table.html / bts_rooms.html already use). Same amber
  accent, same Songti TC, same letterspaced kicker — reads as one family.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import segno
from PIL import Image, ImageDraw, ImageFont

import poster_credits          # shared with make_poster_cct — see that module

BASE = Path(__file__).resolve().parents[2]
OUT = BASE / "exports" / "print"

DPI = 300
W, H = 2480, 3508                      # A4 portrait @300dpi
MARGIN = 236                           # 20 mm

# Page ground is PURE WHITE, not the palette's cream — a full-bleed tint over
# a whole A4 is a lot of toner for no reading benefit (Kyle). The identity is
# carried by the type and the amber accent instead, which cost almost nothing
# to print.
PAPER = (255, 255, 255)
INK = (43, 36, 26)                     # --ink  #2b241a
MUTED = (125, 113, 95)                 # --muted #7d715f
AMBER = (169, 118, 47)                 # --accent #a9762f
LINE = (227, 217, 198)                 # --line #e3d9c6
QRINK = (26, 21, 16)                   # near-black, still warm

SONGTI = "/System/Library/Fonts/Songti.ttc"
BOLD, LIGHT = 2, 5

SITES = [
    ("shengping", "1", "光陰的故事", "過水橋與瑠公圳", "3:52"),
    ("hemei",     "2", "環境的影子", "和美煤礦",       "3:05"),
    ("zhenshan",  "3", "期望的未來", "振山煤礦與光明街", "2:53"),
]

# Three lines each — enough to tell a passer-by what they'd be watching.
BLURB = {
    "shengping": ["戰爭時躲著空襲讀書，後來考進北一女。",
                  "一千兩百坪的大宅院，為了開馬路拆了。",
                  "那時候，瑠公圳與碧潭的水都很乾淨。"],
    "hemei":     ["和美煤礦，由她的母親經營。",
                  "台灣最特殊的一座礦——煤不用車運，用船，",
                  "從新店溪一路運到萬華。"],
    "zhenshan":  ["振山煤礦，最後因為一場災變結束。",
                  "光明街底下曾經是鐵路用地，鬧了很多年。",
                  "運煤的路線，今天還看得出來。"],
}
# The still from each video's thumbnail. Deliberately the PHOTO only, not the
# composed B_split — that one carries the title in large type, and the poster
# already says it at 186px directly above.
THUMBS = BASE / "exports" / "thumbnails"
# All three videos as one list — the small corner code on every sheet.
PLAYLIST_URL = "https://www.youtube.com/playlist?list=PLePG5FUoVOJI"
CREDITS = [("口述", "陳林彩薇（林秀卿先生之女）"),
           ("攝影", "李承洋"),
           ("後製剪輯", "楊大謙"),
           ("指導單位", "新北市政府文化局"),
           ("執行單位", "新北市陳昌梯醫師山林保育協會")]


def font(sz: int, bold: bool = True) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(SONGTI, sz, index=BOLD if bold else LIGHT)


def centred(d: ImageDraw.ImageDraw, y: int, s: str, f, fill, track: int = 0) -> int:
    if track:
        ws = [d.textbbox((0, 0), c, font=f)[2] - d.textbbox((0, 0), c, font=f)[0]
              + track for c in s]
        x = (W - (sum(ws) - track)) / 2
        for c, w in zip(s, ws):
            d.text((x, y), c, font=f, fill=fill)
            x += w
    else:
        bb = d.textbbox((0, 0), s, font=f)
        d.text(((W - (bb[2] - bb[0])) / 2 - bb[0], y), s, font=f, fill=fill)
    return y


def qr_image(url: str, target: int) -> Image.Image:
    """High error-correction QR — these live outdoors and get scuffed."""
    qr = segno.make(url, error="h")
    n = len(qr.matrix) + 8                    # incl. quiet zone (border=4)
    scale = max(1, target // n)               # integer scale = no resampling blur
    tmp = OUT / "_qr_tmp.png"
    qr.save(str(tmp), scale=scale, border=4, dark=_hex(QRINK), light=_hex(PAPER))
    im = Image.open(tmp).convert("RGB")
    tmp.unlink()
    return im


def _hex(rgb) -> str:
    return "#%02x%02x%02x" % rgb


def poster(slug: str, num: str, title: str, sub: str, dur: str, url: str) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)   # qr_image writes a temp file here
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)

    # hairline frame
    d.rectangle([MARGIN - 44, MARGIN - 44, W - MARGIN + 44, H - MARGIN + 44],
                outline=LINE, width=4)

    # Everything below FLOWS from y. Mixing a flowing top with a bottom pinned
    # to H-MARGIN is what collided once the still and blurb were added.
    y = MARGIN + 56
    centred(d, y, "新店礦業文化路徑", font(50), MUTED, track=20)
    y += 150
    centred(d, y, title, font(158), INK, track=26)
    y += 218
    d.rectangle([W / 2 - 130, y, W / 2 + 130, y + 5], fill=AMBER)
    y += 60
    centred(d, y, sub, font(62), AMBER, track=10)

    # ---- still from the video (16:9) ----
    y += 160
    still = Image.open(THUMBS / f"_still_{slug}.png").convert("RGB")
    sw = 1450
    still = still.resize((sw, round(sw * 9 / 16)), Image.LANCZOS)
    sx = (W - sw) // 2
    d.rectangle([sx - 5, y - 5, sx + sw + 5, y + still.height + 5],
                outline=LINE, width=5)
    im.paste(still, (sx, y))
    y += still.height + 84

    # ---- blurb ----
    for line in BLURB[slug]:
        centred(d, y, line, font(46), INK, track=3)
        y += 70

    # ---- QR block ----
    qr = qr_image(url, 600)
    qx, qy = (W - qr.width) // 2, y + 60
    pad = 32
    d.rectangle([qx - pad, qy - pad, qx + qr.width + pad, qy + qr.height + pad],
                fill=PAPER, outline=LINE, width=3)
    im.paste(qr, (qx, qy))

    y = qy + qr.height + pad + 58
    centred(d, y, "掃描觀看　口述影像", font(66), INK, track=10)
    y += 96
    centred(d, y, f"影片長度 {dur}　·　中文字幕", font(42), MUTED, track=6)

    # ---- credits ----
    y += 74          # was 92 — pulls the enlarged credit block clear of the frame
    d.rectangle([W / 2 - 280, y, W / 2 + 280, y + 3], fill=LINE)
    y += 48
    y = poster_credits.block(d, y, CREDITS, font, W, MUTED, INK)
    assert y < H - 120, f"poster overflows: content ends at {y} of {H}"

    # ---- small playlist QR, bottom-right corner ----
    # The credit lines are centred and ~900px wide, so the right side of the
    # frame is empty; this tucks into it without crowding them.
    pl = qr_image(PLAYLIST_URL, 400)
    px_ = (W - MARGIN + 44) - 40 - pl.width
    py_ = (H - MARGIN + 44) - 44 - pl.height
    im.paste(pl, (px_, py_))
    d.rectangle([px_ - 8, py_ - 8, px_ + pl.width + 8, py_ + pl.height + 8],
                outline=LINE, width=3)
    lab = "全系列播放清單"
    lf = font(34)
    lw = sum(d.textbbox((0, 0), c, font=lf)[2]
             - d.textbbox((0, 0), c, font=lf)[0] + 3 for c in lab) - 3
    lx = px_ + (pl.width - lw) / 2
    for c in lab:
        d.text((lx, py_ - 60), c, font=lf, fill=MUTED)
        lx += (d.textbbox((0, 0), c, font=lf)[2]
               - d.textbbox((0, 0), c, font=lf)[0]) + 3

    # Decode the QR back off the FINISHED PAGE before saving — this is what a
    # phone pointed at the print actually sees. A poster that renders perfectly
    # but encodes the wrong link looks fine right up until someone scans it.
    import cv2
    import numpy as np
    ok, decoded, _pts, _st = cv2.QRCodeDetector().detectAndDecodeMulti(
        np.array(im.convert("RGB"))[:, :, ::-1])
    found = set(decoded) if ok else set()
    want = {url, PLAYLIST_URL}
    if not want <= found:
        raise SystemExit(f"QR MISMATCH on {title}: expected {want}, "
                         f"page decodes to {found} — not saving")

    OUT.mkdir(parents=True, exist_ok=True)
    stem = f"{num}_{title}_{sub}"
    pdf = OUT / f"{stem}_A4.pdf"
    im.save(pdf, "PDF", resolution=DPI)
    segno.make(url, error="h").save(str(OUT / f"{stem}_QR.svg"), scale=10,
                                    border=4, dark=_hex(QRINK), light=None)
    return pdf


def main() -> None:
    urls = {}
    if len(sys.argv) > 1:
        urls = json.loads(Path(sys.argv[1]).read_text())
    placeholder = not urls
    for slug, num, title, sub, dur in SITES:
        url = urls.get(slug, f"https://youtu.be/PLACEHOLDER-{slug}")
        p = poster(slug, num, title, sub, dur, url)
        print(f"  {p.name}   ← {url}")
    if placeholder:
        print("\n*** PLACEHOLDER URLs — these QR codes do NOT work. ***")
        print("    Rerun with a urls.json once the videos are up.")
    print(f"\nposters → {OUT}")


if __name__ == "__main__":
    main()
