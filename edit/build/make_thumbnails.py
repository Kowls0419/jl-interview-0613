"""YouTube thumbnails (1280x720) for the three videos, two options each.

    .venv python edit/build/make_thumbnails.py

  A_card   the title card, exactly as it appears in the film
  B_split  warm text panel on the LEFT, a frame of her on the RIGHT — the same
           composition the credits closer uses, so it reads as part of the set

Frames come from *_nosub.mp4 (no burned subtitles) and get the same warm grade
the burn pass applies, so they match the finished films.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

from PIL import Image, ImageDraw

import sys
sys.path.insert(0, str(Path(__file__).parent))
from common import font, _centered, BG, CREAM, AMBER, DIM, _fit_cell

BASE = Path(__file__).resolve().parents[2]
EDIT = BASE / "edit"
OUT = BASE / "exports" / "thumbnails"

TW, TH = 1280, 720
GRADE = ("colorbalance=rs=.02:gs=.005:bs=-.025:rm=.025:gm=.008:bm=-.02,"
         "eq=contrast=1.04:saturation=0.95")

# slug, cards dir, title, subtitle, frame time in the NOSUB render
# frame times = Kyle's picks from the 8-up variant sheets (shen-01/hemei-07/zhen-01)
SITES = [
    ("shengping", "cards_shengping", "光陰的故事", "過水橋與瑠公圳", 49.68),
    ("hemei",     "cards_hemei",     "環境的影子", "和美煤礦",       135.56),
    ("zhenshan",  "cards_zhenshan",  "期望的未來", "振山煤礦與光明街", 22.30),
]


def grab(slug: str, t: float) -> Image.Image:
    tmp = OUT / f"_f_{slug}.png"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.3f}",
                    "-i", str(EDIT / f"{slug}_nosub.mp4"), "-frames:v", "1",
                    "-vf", GRADE, str(tmp)], check=True)
    im = Image.open(tmp).convert("RGB")
    tmp.unlink()
    return im


def opt_a(cards: str, slug: str) -> Path:
    im = Image.open(EDIT / cards / "title.png").convert("RGB")
    im = im.resize((TW, TH), Image.LANCZOS)
    p = OUT / f"{slug}_A_card.jpg"
    im.save(p, quality=94)
    return p


PANEL = 600            # left text column; type below is sized to fit INSIDE it


def _centre_in(d: ImageDraw.ImageDraw, cx: int, y: int, s: str, f, fill,
               track: int = 0) -> None:
    """Centre on an arbitrary x, not the frame — common._centered assumes the
    full 1920 frame, which silently cropped this panel's text the first time."""
    ws = [d.textbbox((0, 0), c, font=f)[2] - d.textbbox((0, 0), c, font=f)[0]
          + track for c in s]
    total = sum(ws) - track
    x = cx - total / 2
    for c, w in zip(s, ws):
        d.text((x, y), c, font=f, fill=fill)
        x += w


def opt_b(slug: str, title: str, sub: str, t: float) -> Path:
    canvas = Image.new("RGB", (TW, TH), BG)
    shot = _fit_cell(grab(slug, t), TW - PANEL, TH)
    canvas.paste(shot, (PANEL, 0))

    # soften the seam so the photo doesn't butt hard against the panel
    grad = Image.new("L", (170, TH), 0)
    gd = ImageDraw.Draw(grad)
    for x in range(170):
        gd.line([(x, 0), (x, TH)], fill=int(255 * (1 - x / 170) ** 1.4))
    canvas.paste(Image.new("RGB", (170, TH), BG), (PANEL, 0), grad)

    d = ImageDraw.Draw(canvas)
    cx = PANEL // 2
    _centre_in(d, cx, 214, "新店礦業文化路徑", font(28, bold=False), DIM, 10)
    _centre_in(d, cx, 282, title, font(84), CREAM, 16)
    d.rectangle([cx - 70, 410, cx + 70, 413], fill=AMBER)
    _centre_in(d, cx, 446, sub, font(32, bold=False), AMBER, 7)
    _centre_in(d, cx, 512, "口述：陳林彩薇", font(25, bold=False), DIM, 3)

    p = OUT / f"{slug}_B_split.jpg"
    canvas.save(p, quality=94)
    return p


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    # Kyle chose B (split). opt_a is kept — it is one line to bring back — but
    # is no longer generated, so the plain title-card files don't reappear
    # every run after being cleaned out.
    for slug, cards, title, sub, t in SITES:
        b = opt_b(slug, title, sub, t)
        kb = b.stat().st_size / 1024
        print(f"  {b.name:<28} {kb:6.0f} KB")
    print(f"\nthumbnails → {OUT}   (1280x720, YouTube limit 2 MB)")


if __name__ == "__main__":
    main()


def playlist() -> Path:
    """Series thumbnail: the three rooms as a triptych under the series name.

    YouTube normally shows the first video's card for a playlist, so this is
    for anywhere you present the series as one thing — a slide, a print, a
    channel section.
    """
    canvas = Image.new("RGB", (TW, TH), BG)
    slice_w = TW // 3
    for i, (slug, _c, _t, _s, _time) in enumerate(SITES):
        still = Image.open(OUT / f"_still_{slug}.png").convert("RGB")
        canvas.paste(_fit_cell(still, slice_w + (TW - slice_w * 3 if i == 2 else 0),
                               TH), (i * slice_w, 0))
    # warm scrim so the type sits on top of it
    canvas = Image.blend(canvas, Image.new("RGB", (TW, TH), BG), 0.70)
    d = ImageDraw.Draw(canvas)
    _centre_in(d, TW // 2, 196, "陳林彩薇　口述影像", font(30, bold=False), DIM, 12)
    _centre_in(d, TW // 2, 268, "新店礦業文化路徑", font(96), CREAM, 20)
    d.rectangle([TW / 2 - 96, 424, TW / 2 + 96, 427], fill=AMBER)
    _centre_in(d, TW // 2, 462, "過水橋　和美煤礦　振山煤礦", font(34, bold=False),
               AMBER, 6)
    _centre_in(d, TW // 2, 540, "三支影片", font(26, bold=False), DIM, 6)
    p = OUT / "playlist.jpg"
    canvas.save(p, quality=94)
    return p
