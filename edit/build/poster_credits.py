"""The credit block, shared by all four A4 sheets.

Lives in its own module so make_posters.py and make_poster_cct.py render credits
from ONE definition. Changing the size or the contrast here changes all four
posters at once — which is the point: the last round of drift (a corner QR box
23px off, an ink value hardcoded instead of imported) came from geometry being
restated per sheet.

Why it looks the way it does — same fix Kyle made on the videos' end cards:
the old credits were small AND set entirely in MUTED, so on a wall they read as
grey mush. Two changes, both borrowed from the 修正後 card:

  * bigger — 40px -> 48px, with the line step opened 60 -> 72 to match, so the
    block breathes instead of just getting fatter.
  * the VALUE carries the contrast, the label stays quiet. On the dark video
    card the value goes brighter than the label; inverted for white paper that
    means the value drops to INK while the label stays MUTED. The label is
    signposting ("攝影"), the name is the information — so the name is what
    should survive being read at two metres.

Sizes are capped by the tightest sheet: the series posters carry FIVE credit
lines above a frame edge at y=3313. At 48/72 the last line's ink landed 17px
off that frame — about 1.4mm, too tight to print — so the step is 66 and the
callers also pull the block up (the pre-rule gap went 92 -> 74). That buys ~59px
of clearance while keeping the size bump, which is the part that matters.

Do NOT raise these from the overflow assert alone: it tests the flowed `y`, not
where the glyphs actually end. Measure ink instead — see scratchpad
check_unity.py and the clearance probe in the worklog.
"""
from __future__ import annotations

SIZE = 48          # was 40
STEP = 66          # was 60; see the clearance note above before changing
TRACK = 4
GAP = 30           # label -> value, replaces the ideographic space


def _w(d, s, f, track: int = TRACK) -> int:
    """Width of `s` once per-character tracking is applied."""
    if not s:
        return 0
    return sum(d.textbbox((0, 0), c, font=f)[2]
               - d.textbbox((0, 0), c, font=f)[0] + track for c in s) - track


def _draw(d, x: float, y: int, s: str, f, fill, track: int = TRACK) -> float:
    for c in s:
        d.text((x, y), c, font=f, fill=fill)
        x += (d.textbbox((0, 0), c, font=f)[2]
              - d.textbbox((0, 0), c, font=f)[0]) + track
    return x


def block(d, y: int, credits, font, page_w: int, label_fill, value_fill) -> int:
    """Draw the credit lines centred on the page. Returns the y after the block.

    `font` is the caller's font factory so both scripts keep using their own
    Songti handle; `credits` is the [(label, value)] list.
    """
    f = font(SIZE)
    for label, value in credits:
        total = _w(d, label, f) + GAP + _w(d, value, f)
        x = (page_w - total) / 2
        x = _draw(d, x, y, label, f, label_fill)
        _draw(d, x + GAP, y, value, f, value_fill)
        y += STEP
    return y
