"""Build video 2/3: 和美煤礦 — cards, Ken Burns overlays, EDL, Traditional SRT.

Run:  .venv python edit/build/video2_hemei.py
Then: .venv python helpers/render.py edit/edl_hemei.json -o edit/hemei_nosub.mp4 --preview --no-subtitles
Then burn subs (see burn command printed at the end).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import (make_title_card, make_question_card, make_end_card,
                    png_to_card_mp4, make_kenburns, make_photo_card,
                    make_photo_grid_card,
                    make_credits_grid_mp4, credits_grid_duration)

BASE = Path(__file__).resolve().parents[2]   # <videos_dir>
EDIT = BASE / "edit"
CARDS = EDIT / "cards_hemei"
KB = EDIT / "kb_hemei"
SRC = BASE / "002A4883.MP4"
PHOTOS = BASE / "2"

QCARD_DUR = 2.6
TITLE_DUR = 4.0
OPENING_DUR = 10.0
TODAY_DUR = 4.6          # matches V1's today_bridge / today_canal

# 今貌 stills shot 2026-08 (IRL/v2/) — same treatment as V1's 今日的過水橋:
# framed photo, slow zoom, small caption at the bottom.
IRL = BASE / "IRL" / "v2"
TODAY_MINE = IRL / "627244688344613072.jpg"    # 坑口與解說牌
TODAY_RIVER = IRL / "627244688092954948.jpg"   # 新店溪渡船口，對岸和美山

# Second 今貌 batch (IRL/hemei irl/, 2026-08). TODAY_ADIT sits BESIDE the existing
# 坑口 photo as a two-up grid rather than its own card — it is the same subject from
# the導覽 that day, so a separate beat would read as a repeat.
IRL2 = BASE / "IRL" / "hemei irl"
TODAY_ADIT = IRL2 / "S__6840336_0.jpg"         # 坑口鐵柵前，導覽當日
TODAY_FERRY = IRL2 / "S__6840335_0.jpg"        # 渡船 981258，碧潭往和美
TODAY_SIGNS = [IRL2 / "S__6848537_0_0.jpg",    # 解說牌一排
               IRL2 / "S__6848541.jpg",        # 解說牌近拍（路徑圖 + QR）
               IRL2 / "S__9887751_0_0.jpg"]    # 解說牌與導覽人
MINE_DUR = 5.0     # two-up grid — same dwell as V3's 4-photo 隧道 grid
SIGNS_DUR = 5.0    # three-up grid

BTS_PHOTOS = BASE / "4"
# 走廊・中庭 stills for the closer grid — Kyle's re-pick via edit/hemei_grid.html
# (dropped P21).
BTS_STILLS = [
    BTS_PHOTOS / "LINE_ALBUM_2026.7.6 _3_260708_3.jpg",    # P3
    BTS_PHOTOS / "LINE_ALBUM_2026.7.6 _3_260708_5.jpg",    # P5
    BTS_PHOTOS / "LINE_ALBUM_2026.7.6 _3_260708_10.jpg",   # P10
    BTS_PHOTOS / "new_jpg" / "IMG_6452.jpg",               # N6452
]
# 走廊・中庭 BTS clip — SILENT tile inside the closer grid (Kyle, r01 note 2).
BTS_CLIPS = [
    (SRC, 305.90, 310.30),   # 好，那這個…和美到這邊，還有到這裡
]
END_DUR = credits_grid_duration(len(BTS_STILLS) + len(BTS_CLIPS), has_clips=True)

CREDITS = [
    ("口述", "陳林彩薇（林秀卿先生之女）"),
    ("攝影", "李承洋"),
    ("後製剪輯", "楊大謙"),
    ("指導單位", "新北市政府文化局"),
    ("執行單位", "新北市陳昌梯醫師山林保育協會"),
]

# ---- segments: (kind, a, b, label) source-time for cam; (kind, name, dur) cards
# Cam splits trim her long pauses / stumbles; every splice is hidden under a
# photo block (see OVERLAY_BLOCKS) so no jump cut is ever visible.
TIMELINE = [
    ("card", "opening", OPENING_DUR),   # calligraphy + pencil, silent
    ("card", "title", TITLE_DUR),
    ("card", "q1", QCARD_DUR),
    ("cam",   7.48, 18.25, "origin"),
    ("card", "q2", QCARD_DUR),
    ("cam",  28.38, 32.38, "visit_a"),      # 女生不能進去的啊 (cut before 但)
    ("cam",  35.70, 47.30, "visit_b"),      # (trim 那個呃) 我媽媽參與的…所以
    ("cam",  48.55, 50.14, "visit_c"),      # (trim pause) 我也有去
    ("card", "q3", QCARD_DUR),
    ("cam",  55.97, 62.75, "boats_hook"),   # 台灣最特殊的…船運運煤
    ("cam",  65.30, 70.80, "boats_b"),      # 我們要過去…運煤就
    ("cam",  72.24, 73.95, "boats_c"),      # (trim garble) 用船運煤到
    ("cam",  75.30, 105.66, "boats_d"),     # (trim pause) 加州旅社…載到萬華
    ("card", "q4", QCARD_DUR),
    ("cam", 114.06, 137.74, "trail"),
    ("card", "q5", QCARD_DUR),
    ("cam", 162.06, 164.80, "workers_a"),   # 有啊有過，而且都是
    ("cam", 167.60, 172.72, "workers_b"),   # (trim pause) 在一起工作…那邊
    ("cam", 175.96, 184.42, "workers_c"),   # (trim stumble) 煤礦結束的時候…
    ("card", "q6", QCARD_DUR),
    ("cam", 198.52, 212.50, "memory_a"),    # 原來是還有聯繫的…
    ("cam", 213.90, 221.99, "memory_b"),    # (trim pause) 現在說來…一百多歲
    ("card", "today_mine", MINE_DUR),       # 今貌：和美煤礦坑口（兩張並排）
    ("card", "today_river", TODAY_DUR),     # 今貌：新店溪與和美山
    ("card", "today_ferry", TODAY_DUR),     # 今貌：碧潭到和美的渡船
    ("card", "today_signs", SIGNS_DUR),     # 今貌：坑口外解說牌（三張一排）
    ("card", "end", END_DUR),   # credits → shrink left + 花絮 grid (stills + silent clip)
]

QUESTIONS = {
    "q1": "和美煤礦是怎麼來的？",
    "q2": "妳小時候去過煤礦嗎？",
    "q3": "煤是怎麼運出去的？",
    "q4": "和美山步道是怎麼來的？",
    "q5": "礦場裡有哪些工人？",
    "q6": "後來還有聯繫嗎？",
}

# ---- photo blocks: consolidated (fewer footage<->photo switches), each block
# is a chain of alpha-crossfading photos anchored to labeled segments.
# (photos, anchor_label, anchor_pt "end"/"start", delta, per_photo_dur, xover)
P = "LINE_ALBUM_2026.7.6 _1_260706_{}.jpg"
OVERLAY_BLOCKS = [
    # VISIT: covers both splices and runs to the q3 card (no 1.5s face pop)
    # xover = 1.0 (2x the 0.5s alpha fade) so photo-to-photo dissolves never
    # let the footage ghost through
    ([P.format(11), P.format(7)], "visit_a", "end", -2.5, 8.4, 1.0),
    # BOATS block 1: covers hook->b->c->d splices (渡船, 運煤船)
    ([P.format(10), P.format(16)], "boats_hook", "end", -1.5, 6.6, 1.0),
    # BOATS block 2: 挑煤 + 輸送帶棧道, inside boats_d at 用挑的
    ([P.format(6)], "boats_d", "start", 14.20, 6.6, 0.0),  # 2-17 dropped (dup of 2-16)
    # TRAIL: modern trailhead, single
    ([P.format(15)], "trail", "start", 13.84, 8.0, 0.0),
    # WORKERS: single photo covers both splices
    ([P.format(12)], "workers_a", "end", -1.2, 8.1, 0.0),
    # MEMORY: covers the splice, face returns for the 一百多歲 finale
    ([P.format(9)], "memory_a", "start", 6.0, 9.6, 0.0),
]

# subtitle text fixes applied AFTER OpenCC conversion
SUB_FIXES = {
    "正山煤礦": "振山煤礦",
    "阿板塞": "阿板師",
    "電氣師傅": "電器師傅",
    "聯絡": "聯繫",
    "一沒使用，": "",
    "一沒使用": "",
    "臺": "台",
    "，呃，": "，",
    "呃，": "",
    "呃": "",
    "啊，但是": "但是",
}
MAX_CUE = 14  # max chars per cue
EXTRA_CUES: list = []  # opening is silent now; hook line is a cam segment

# --------------------------------------------------------------------------


def build_cards() -> None:
    CARDS.mkdir(parents=True, exist_ok=True)
    p = CARDS / "title.png"
    make_title_card(p, "新店礦業文化路徑", "環境的影子", "和美煤礦",
                    "口述：陳林彩薇")
    png_to_card_mp4(p, CARDS / "title.mp4", TITLE_DUR)
    for name, q in QUESTIONS.items():
        p = CARDS / f"{name}.png"
        make_question_card(p, q)
        png_to_card_mp4(p, CARDS / f"{name}.mp4", QCARD_DUR)
    for ph in (TODAY_MINE, TODAY_RIVER, TODAY_ADIT, TODAY_FERRY, *TODAY_SIGNS):
        assert ph.exists(), f"missing 今貌 photo: {ph}"
    make_photo_grid_card([TODAY_MINE, TODAY_ADIT], CARDS / "today_mine.mp4",
                         MINE_DUR, caption="今日的和美煤礦坑口")
    make_photo_card(TODAY_RIVER, CARDS / "today_river.mp4", TODAY_DUR,
                    caption="今日的新店溪與和美山")
    make_photo_card(TODAY_FERRY, CARDS / "today_ferry.mp4", TODAY_DUR,
                    caption="碧潭到和美渡船照")
    make_photo_grid_card(TODAY_SIGNS, CARDS / "today_signs.mp4", SIGNS_DUR,
                         caption="和美煤礦坑口外的解說牌")
    print("  今貌 cards → today_mine(2) / today_river / today_ferry / today_signs(3)")
    for ph in BTS_STILLS:
        assert ph.exists(), f"missing BTS still: {ph}"
    d = make_credits_grid_mp4(CARDS / "end.mp4", "環境的影子", CREDITS,
                              BTS_STILLS, BTS_CLIPS)
    assert abs(d - END_DUR) < 1e-6, f"closer {d} != TIMELINE {END_DUR}"
    print(f"  closer → end.mp4 ({d:.2f}s, {len(BTS_STILLS)} stills)")
    print(f"cards → {CARDS}")


def kb_name(fname: str, dur: float) -> str:
    num = fname.rsplit("_", 1)[-1].split(".")[0]
    return f"kb_p{num}_{dur:g}s.mov"


def iter_block_overlays():
    """Yield (photo_fname, dur, block_index, pos_in_block) for OVERLAY_BLOCKS."""
    for bi, (photos, _lbl, _pt, _delta, pdur, _xo) in enumerate(OVERLAY_BLOCKS):
        for pi, ph in enumerate(photos):
            yield ph, pdur, bi, pi


def build_kenburns() -> None:
    KB.mkdir(parents=True, exist_ok=True)
    for fname, dur, _bi, _pi in iter_block_overlays():
        out = KB / kb_name(fname, dur)
        if out.exists():
            continue
        make_kenburns(PHOTOS / fname, out, dur)
        print(f"  {out.name} ← {fname}")
    print(f"ken burns → {KB}")


def out_offsets() -> list[tuple]:
    """Return list of (kind, meta, out_start, dur) in output-timeline order."""
    rows, off = [], 0.0
    for seg in TIMELINE:
        if seg[0] == "cam":
            dur = seg[2] - seg[1]
            rows.append(("cam", seg, off, dur))
        else:
            dur = seg[2]
            rows.append(("card", seg, off, dur))
        off += dur
    return rows


def label_bounds() -> dict[str, tuple[float, float]]:
    """label -> (out_start, out_end) for cam segments."""
    out = {}
    for kind, seg, off, dur in out_offsets():
        if kind == "cam":
            out[seg[3]] = (off, off + dur)
    return out


def build_edl() -> Path:
    sources = {"C4883": str(SRC)}
    ranges = []
    for kind, seg, off, dur in out_offsets():
        if kind == "cam":
            ranges.append({"source": "C4883", "start": seg[1], "end": seg[2],
                           "beat": seg[3], "quote": "", "reason": ""})
        else:
            name = seg[1]
            key = f"CARD_{name}"
            sources[key] = str(CARDS / f"{name}.mp4")
            # grade "" opts cards out of the EDL-wide anti-flicker filter:
            # cards are synthetic (nothing to de-flicker) and tmix smears the
            # animation baked into the closer. Warm grade still applies later,
            # in the subtitle-burn pass.
            ranges.append({"source": key, "start": 0.0, "end": dur,
                           "beat": f"card {name}", "quote": "", "reason": "",
                           "grade": ""})

    bounds = label_bounds()
    overlays = []
    for photos, lbl, pt, delta, pdur, xover in OVERLAY_BLOCKS:
        base = bounds[lbl][1] if pt == "end" else bounds[lbl][0]
        t0 = base + delta
        for pi, fname in enumerate(photos):
            start = t0 + pi * (pdur - xover)
            overlays.append({"file": str(KB / kb_name(fname, pdur)),
                             "start_in_output": round(start, 3),
                             "duration": pdur})

    total = sum(r[3] for r in out_offsets())
    # tmix runs in the per-segment extraction chain at the SOURCE fps (60),
    # before render.py's -r 24 decimation — averages across fluorescent-flicker
    # phases and cancels the rolling bands. Measured on src 118-121s: none
    # mean=0.398, tmix=3 0.321 (-19%), tmix=5 0.217 (-45%, no visible smear on
    # seated subject). No-op on static cards; color grade stays in the
    # subtitle-burn pass.
    edl = {"version": 1, "sources": sources, "ranges": ranges,
           "grade": "tmix=frames=5", "overlays": overlays,
           "total_duration_s": round(total, 2)}
    path = EDIT / "edl_hemei.json"
    path.write_text(json.dumps(edl, ensure_ascii=False, indent=2))
    print(f"EDL → {path}  (total {total:.1f}s = {int(total//60)}:{total%60:04.1f})")
    return path


def build_srt() -> Path:
    from opencc import OpenCC
    cc = OpenCC("s2twp")
    tr = json.loads((EDIT / "transcripts" / "002A4883.json").read_text())
    words = [w for w in tr["words"] if w.get("type") == "word"
             and w.get("start") is not None]

    cues = []
    for kind, seg, off, dur in out_offsets():
        if kind != "cam":
            continue
        a, b = seg[1], seg[2]
        # include words by their START time — Scribe pads a word's end through
        # any following silence, so end-based filtering drops real words whose
        # pause-padding crosses the cut (e.g. 所"以", 船運煤"到")
        seg_words = [w for w in words if a - 0.02 <= w["start"] < b - 0.05]

        def flush(buf: list) -> None:
            if not buf:
                return
            joined = "".join(x["text"].strip() for x in buf)
            starts = [x["start"] for x in buf
                      if x["text"].strip() not in "，。？！、；："]
            c_start = starts[0] if starts else buf[0]["start"]
            cues.append((max(a, c_start), min(b, buf[-1]["end"]), joined, off, a))

        cur, last_soft = [], -1  # last_soft: index in cur AFTER a soft punct
        for w in seg_words:
            txt = (w.get("text") or "").strip()
            if not txt:
                continue
            cur.append(w)
            if txt in "，、；":
                last_soft = len(cur)
            joined = "".join(x["text"].strip() for x in cur)
            plain = re.sub(r"[，。？！、；：]", "", joined)
            if txt in "。？！":
                flush(cur); cur, last_soft = [], -1
            elif txt in "，、；" and len(plain) >= 8:
                flush(cur); cur, last_soft = [], -1
            elif len(plain) >= MAX_CUE + 2:
                if last_soft > 0:
                    flush(cur[:last_soft])
                    cur = cur[last_soft:]
                else:
                    flush(cur); cur = []
                last_soft = -1
        flush(cur)

    def ts(x: float) -> str:
        ms = int(round(x * 1000))
        h, r = divmod(ms, 3600000); m, r = divmod(r, 60000); s, ms = divmod(r, 1000)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

    final = list(EXTRA_CUES)
    fired = dict.fromkeys(SUB_FIXES, 0)
    for w_start, w_end, text, off, seg_a in cues:
        text = cc.convert(text)
        for k, v in SUB_FIXES.items():
            fired[k] += text.count(k)
            text = text.replace(k, v)
        text = text.strip("，、； ").rstrip("。")
        if not re.sub(r"[，。？！、；：]", "", text):
            continue
        o_start = w_start - seg_a + off
        o_end = max(o_start + 0.5, w_end - seg_a + off)
        final.append((o_start, o_end, text))
    # A SUB_FIXES entry that never matches is dead code, and dead silently: it
    # looks identical to a fix that worked. "近水游"→"逆水游" sat dead for months
    # because OpenCC rewrote 游→遊 before the replace ran. Warn, never assert —
    # an entry can legitimately be zero once an earlier entry has fixed the text.
    dead = [k for k, n in fired.items() if n == 0]
    if dead:
        print(f"  ⚠ SUB_FIXES entries that never matched: {dead}")

    final.sort(key=lambda c: c[0])

    lines, n = [], 0
    for o_start, o_end, text in final:
        n += 1
        lines += [str(n), f"{ts(o_start)} --> {ts(o_end)}", text, ""]

    path = EDIT / "hemei_zht.srt"
    path.write_text("\n".join(lines))
    print(f"SRT → {path}  ({n} cues, Traditional)")
    return path


if __name__ == "__main__":
    build_cards()
    build_kenburns()
    build_edl()
    build_srt()
    print("\nnext:")
    print("  render.py edit/edl_hemei.json -o edit/hemei_nosub.mp4 --preview --no-subtitles")
    print("  then burn hemei_zht.srt with Heiti TC force_style")
