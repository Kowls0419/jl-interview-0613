"""A4 QR poster for 陳外科醫院 — the Dots Global documentary.

    .venv python edit/build/make_poster_cct.py

Output: exports/print/4_陳外科醫院_光明街_A4.pdf  (+ bare .svg QR)

Why a separate file from make_posters.py: that script is the 新店礦業文化路徑
series — one kicker, one playlist QR, one credit block, three sites. This film
is a different production (Dots Global, © 2026), so it needs its own kicker,
its own credits, and a corner QR pointing at the film's own site rather than
the series playlist. Everything that defines the LOOK — palette, Songti, the
centred/tracked setting, the QR generator — is imported from make_posters so
the four sheets stay one family and there is still a single source of truth.

Layout is identical to the series sheet, so a passer-by who has seen one of
the mine posters recognises this as the same programme of work.
"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))   # sibling make_posters
from make_posters import (AMBER, INK, LINE, MARGIN, MUTED, PAPER, QRINK,
                          W, H, DPI, centred, font, qr_image, _hex)
import poster_credits          # shared with make_posters — see that module's docstring
import segno

BASE = Path(__file__).resolve().parents[2]
OUT = BASE / "exports" / "print"
THUMBS = BASE / "exports" / "thumbnails"

KICKER = "新北市的第一所醫院"
TITLE = "陳外科醫院"
SUB = "光明街　Since 1958"
DUR = "3:53"

VIDEO_URL = "https://youtu.be/UVZ8Esm8AZA"
SITE_URL = "https://ccthospital.dotsglobal.co/"

# Three lines, condensed from the film's own synopsis on ccthospital.dotsglobal.co
# — same voice as the site, short enough to read off a wall in passing.
BLURB = ["1950 年代的新店，醫療，還很遙遠。",
         "和美煤礦的經營者，決定在光明街蓋一間醫院。",
         "許多人，因此能夠活下來。"]

# Only what the film and the site actually state. No director/photographer
# credit card appears in either, so none is invented here.
CREDITS = [("製作", "Dots Global"),
           ("專題網站", "ccthospital.dotsglobal.co"),
           ("版權", "© 2026 Dots Global")]

# The site's own hero banner (2400x749, ~3.2:1), not a frame from the film —
# Kyle's call. It is not cropped to the series' 16:9: a 3.2:1 banner squeezed
# into a 16:9 box would lose the type at both ends, so the slot takes the
# banner's native ratio and gets wider instead to hold the same visual weight.
BANNER = THUMBS / "_banner_cct.jpg"

# EVERY box on this sheet must match the three series sheets exactly — same
# picture box, same QR box, same rules, same frame — so the four read as one
# set on a wall. So the geometry below is not re-chosen here; it is imported
# from make_posters as PIC_W / PIC_RATIO / QR_TARGET / QR_PAD and friends.
#
# The banner is 2400x749 (~3.2:1) and the box is 16:9, so it is centre-cropped
# rather than squeezed. The crop keeps the full title block: the lettering and
# both illustrations sit within the middle 1331px of the 2400px source.


# qr_image() sizes a code as (modules + quiet zone) x an INTEGER scale, so the
# rendered pixel size depends on how much data the URL carries. The series'
# playlist URL is 50 chars and lands on QR version 6 -> 392px; this poster's
# site URL is 34 chars and lands on version 4 -> 369px. Left alone that prints a
# corner box 23px smaller than the other three sheets, which is exactly the kind
# of drift that shows when the set is pinned up together. So both codes are
# pinned to the series' rendered sizes and padded into them.
SERIES_QR_MAIN = 574                       # https://youtu.be/<11> at target 600
SERIES_QR_CORNER = 392                     # playlist URL at target 400


def _pin(im: Image.Image, size: int) -> Image.Image:
    """Centre a code on a PAPER square of exactly `size` px.

    Padding only widens the quiet zone, so the code still scans; what it buys is
    an outline box identical to the other three posters.
    """
    if im.width == size and im.height == size:
        return im
    if im.width > size:
        raise SystemExit(f"QR renders {im.width}px, larger than the series' {size}px")
    canvas = Image.new("RGB", (size, size), PAPER)
    canvas.paste(im, ((size - im.width) // 2, (size - im.height) // 2))
    return canvas


def _crop_169(im: Image.Image) -> Image.Image:
    """Centre-crop to 16:9 so the banner fits the series' picture box.

    The banner is wider than 16:9, so this trims the textured left and right
    edges and keeps the full title block — lettering plus both illustrations
    live inside the middle ~1331px of the 2400px source.
    """
    want = 16 / 9
    have = im.width / im.height
    if abs(have - want) < 1e-6:
        return im
    if have > want:                                # too wide → trim the sides
        w = round(im.height * want)
        x = (im.width - w) // 2
        return im.crop((x, 0, x + w, im.height))
    h = round(im.width / want)                     # too tall → trim top/bottom
    y = (im.height - h) // 2
    return im.crop((0, y, im.width, y + h))


def poster() -> Path:
    OUT.mkdir(parents=True, exist_ok=True)   # qr_image writes a temp file here
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)

    d.rectangle([MARGIN - 44, MARGIN - 44, W - MARGIN + 44, H - MARGIN + 44],
                outline=LINE, width=4)

    y = MARGIN + 56
    centred(d, y, KICKER, font(50), MUTED, track=20)
    y += 150
    centred(d, y, TITLE, font(158), INK, track=26)
    y += 218
    d.rectangle([W / 2 - 130, y, W / 2 + 130, y + 5], fill=AMBER)
    y += 60
    centred(d, y, SUB, font(62), AMBER, track=10)

    # ---- picture box: IDENTICAL to the series (1450 wide, 16:9, 5px LINE) ----
    y += 160
    art = Image.open(BANNER).convert("RGB")
    art = _crop_169(art)
    sw = 1450
    art = art.resize((sw, round(sw * 9 / 16)), Image.LANCZOS)
    sx = (W - sw) // 2
    d.rectangle([sx - 5, y - 5, sx + sw + 5, y + art.height + 5],
                outline=LINE, width=5)
    im.paste(art, (sx, y))
    y += art.height + 84

    for line in BLURB:
        centred(d, y, line, font(46), INK, track=3)
        y += 70

    # ---- QR block ----
    qr = _pin(qr_image(VIDEO_URL, 600), SERIES_QR_MAIN)
    qx, qy = (W - qr.width) // 2, y + 60
    pad = 32
    d.rectangle([qx - pad, qy - pad, qx + qr.width + pad, qy + qr.height + pad],
                fill=PAPER, outline=LINE, width=3)
    im.paste(qr, (qx, qy))

    y = qy + qr.height + pad + 58
    centred(d, y, "掃描觀看　紀錄片", font(66), INK, track=10)
    y += 96
    centred(d, y, f"影片長度 {DUR}　·　中英文字幕", font(42), MUTED, track=6)

    y += 74          # was 92 — pulls the enlarged credit block clear of the frame
    d.rectangle([W / 2 - 280, y, W / 2 + 280, y + 3], fill=LINE)
    y += 48
    y = poster_credits.block(d, y, CREDITS, font, W, MUTED, INK)
    assert y < H - 120, f"poster overflows: content ends at {y} of {H}"

    # ---- small site QR, bottom-right corner (where the series puts the playlist) ----
    pl = _pin(qr_image(SITE_URL, 400), SERIES_QR_CORNER)
    px_ = (W - MARGIN + 44) - 40 - pl.width
    py_ = (H - MARGIN + 44) - 44 - pl.height
    im.paste(pl, (px_, py_))
    d.rectangle([px_ - 8, py_ - 8, px_ + pl.width + 8, py_ + pl.height + 8],
                outline=LINE, width=3)
    lab = "專題網站"
    lf = font(34)
    lw = sum(d.textbbox((0, 0), c, font=lf)[2]
             - d.textbbox((0, 0), c, font=lf)[0] + 3 for c in lab) - 3
    lx = px_ + (pl.width - lw) / 2
    for c in lab:
        d.text((lx, py_ - 60), c, font=lf, fill=MUTED)
        lx += (d.textbbox((0, 0), c, font=lf)[2]
               - d.textbbox((0, 0), c, font=lf)[0]) + 3

    # Decode both codes back off the FINISHED PAGE — a poster that renders
    # perfectly but encodes the wrong link looks fine right up until a scan.
    import cv2
    import numpy as np
    ok, decoded, _pts, _st = cv2.QRCodeDetector().detectAndDecodeMulti(
        np.array(im.convert("RGB"))[:, :, ::-1])
    found = set(decoded) if ok else set()
    want = {VIDEO_URL, SITE_URL}
    if not want <= found:
        raise SystemExit(f"QR MISMATCH on {TITLE}: expected {want}, "
                         f"page decodes to {found} — not saving")

    stem = f"4_{TITLE}_光明街"
    pdf = OUT / f"{stem}_A4.pdf"
    im.save(pdf, "PDF", resolution=DPI)
    segno.make(VIDEO_URL, error="h").save(str(OUT / f"{stem}_QR.svg"), scale=10,
                                          border=4, dark=_hex(QRINK), light=None)
    return pdf


if __name__ == "__main__":
    p = poster()
    print(f"  {p.name}   ← {VIDEO_URL}")
    print(f"  corner QR  ← {SITE_URL}")
    print(f"\nposter → {OUT}")
