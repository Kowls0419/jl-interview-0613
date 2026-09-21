"""Build video 環境的影子 (振山煤礦/光明街) — cards, KB overlays, EDL, SRT.

Source: 002A4884.MP4 (60fps, flicker-clean: measured 0.13-0.15 at 4 spots, no tmix).
Photos: folder 1/. Opening: build/make_opening_zhenshan.py (photo 1-7).

Run:  .venv python edit/build/video1_zhenshan.py
Then: render.py edit/edl_zhenshan.json -o edit/zhenshan_nosub.mp4 --preview --no-subtitles
Then burn (same grade + LXGW WenKai TC command as 光陰的故事).
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import (make_title_card, make_question_card, make_end_card,
                    png_to_card_mp4, make_kenburns,
                    make_photo_grid_card, make_clip_photo_card,
                    make_credits_grid_mp4, credits_grid_duration)

BASE = Path(__file__).resolve().parents[2]
EDIT = BASE / "edit"
CARDS = EDIT / "cards_zhenshan"
KB = EDIT / "kb_zhenshan"
SRC = BASE / "edit" / "proxy" / "4884_crop.mp4"  # interviewer cropped out
TRANSCRIPT = "002A4884.json"
PHOTOS = BASE / "1"

QCARD_DUR = 2.6
TITLE_DUR = 4.0
OPENING_DUR = 10.0

# 今貌 shot 2026-08 (IRL/v3/) — V1's caption treatment, two variants:
#   today_tunnel: the four 隧道 stills as one row (Kyle: "put as a grid")
#   today_lane:   IMG_7803 time-lapsed (39.5s walk → 6s) with IMG_7802 beside it
IRL = BASE / "IRL" / "v3"
TUNNEL_DIR = IRL / "振山煤礦台車山區段隧道"
TUNNEL_PHOTOS = sorted(TUNNEL_DIR.glob("*.jpg"))
LANE_CLIP = IRL / "IMG_7803.MOV"      # 39.52s walk down the lane
LANE_PHOTO = IRL / "IMG_7802.jpg"     # converted from HEIC by build_cards
LANE_HEIC = IRL / "IMG_7802.HEIC"
TUNNEL_DUR = 5.0
LANE_DUR = 6.0

BTS_PHOTOS = BASE / "4"
# 照片陳列室 side-shots (Kyle's room mapping) — the grid in the animated closer.
BTS_STILLS = [
    BTS_PHOTOS / "LINE_ALBUM_2026.7.6 _3_260708_6.jpg",
    BTS_PHOTOS / "LINE_ALBUM_2026.7.6 _3_260708_7.jpg",
    BTS_PHOTOS / "LINE_ALBUM_2026.7.6 _3_260708_2.jpg",
    BTS_PHOTOS / "LINE_ALBUM_2026.7.6 _3_260708_8.jpg",
    BTS_PHOTOS / "LINE_ALBUM_2026.7.6 _3_260708_9.jpg",
]
# 照片陳列室 BTS clip — SILENT tile inside the closer grid (Kyle, r01 note 2).
BTS_CLIPS = [
    (SRC, 298.40, 303.66),   # 好，那它的部分就到這裡啊。就這樣。
]
END_DUR = credits_grid_duration(len(BTS_STILLS) + len(BTS_CLIPS), has_clips=True)

CREDITS = [
    ("口述", "陳林彩薇（林秀卿先生之女）"),
    ("攝影", "李承洋"),
    ("後製剪輯", "楊大謙"),
    ("指導單位", "新北市政府文化局"),
    ("執行單位", "新北市陳昌梯醫師山林保育協會"),
]

# Cam splits trim pauses/stumbles; every splice is hidden under a photo block.
TIMELINE = [
    ("card", "opening", OPENING_DUR),
    ("card", "title", TITLE_DUR),
    ("cam", 267.60, 280.26, "hook"),        # 102巷…台車道 (site-specific hook)
    ("card", "q1", QCARD_DUR),
    ("cam",  22.66, 26.75, "q1a"),          # 在高麗坑那一邊
    ("cam",  27.10, 29.94, "q1b"),          # 那振山煤礦它是 (trim 呃)
    ("cam",  30.78, 32.30, "q1c"),          # 它是怎麼結束的呢？
    ("cam",  36.66, 39.15, "q1d"),          # (trim stumble) 是一個災變，所以
    ("cam",  40.60, 42.60, "q1e"),          # (trim pause) 就這樣結束了
    ("card", "q2", QCARD_DUR),
    ("cam",  56.94, 60.62, "q2a"),          # 父親在振山煤礦上班
    ("cam",  63.98, 77.72, "q2b"),          # (trim 那那個) 陳外科=蓄炭場…上火車
    ("card", "q3", QCARD_DUR),
    ("cam",  91.58, 104.10, "q3a"),         # 光明街…鐵路用地 (trim 要呃)
    ("cam", 105.44, 112.10, "q3b"),         # 鐵路局要收回…鬧了很多年
    ("card", "q4", QCARD_DUR),
    ("cam", 140.96, 161.06, "zoo"),         # 上班族…去動物園玩 換很多道車
    ("card", "q5", QCARD_DUR),
    ("cam", 219.26, 241.12, "train_a"),     # 北一女坐火車…有時候追著上
    ("cam", 243.60, 249.86, "train_b"),     # (trim pause) 一個站沒追到…跑的很慢
    ("card", "q6", QCARD_DUR),
    ("cam", 287.48, 297.84, "q6ans"),       # 從後山接下來可能也看得出來
    ("card", "today_tunnel", TUNNEL_DUR),   # 今貌：台車山區段隧道（四張一排）
    ("card", "today_lane", LANE_DUR),       # 今貌：102台車巷縮時 + 巷口
    ("card", "end", END_DUR),   # credits → shrink left + 花絮 grid (stills + silent clip)
]

QUESTIONS = {
    "q1": "振山煤礦在哪裡？後來怎麼了？",
    "q2": "妳父親在哪裡工作？",
    "q3": "光明街以前是什麼樣子？",
    "q4": "小時候有出去玩過嗎？",
    "q5": "對新店線火車有什麼記憶？",
    "q6": "現在還看得出運煤的路線嗎？",
}

P = "LINE_ALBUM_2026.7.6_260706_{}.jpg"
# (photos, anchor_label, "end"/"start", delta, per_photo_dur, xover)
OVERLAY_BLOCKS = [
    ([P.format(6), P.format(5)], "q1a", "end", -2.0, 6.4, 1.0),   # 視察/貯炭場合影
    ([P.format(3)], "q2a", "end", -1.5, 9.0, 0.0),                # 蓄炭場鐵軌前
    ([P.format(10)], "q3a", "start", 9.0, 8.0, 0.0),              # 老合影+光明街現況
    # 1-4 (小學班級合影/碧潭吊橋) removed from zoo — it's the Xindian-elementary
    # school photo, not a "went out to play" image (Kyle round 3). zoo now footage.
    ([P.format(14), P.format(9)], "q6ans", "start", 1.0, 4.3, 1.0),  # 運煤台車→鳥瞰圖 (framed: q6 card → ~1s footage → pic, never over card bg), 最後落在臉上
]

SUB_FIXES = {
    "營區小車站": "螢橋車站",   # Scribe garble — 新店線 stop on the way to 北一女
    "鎮山煤礦": "振山煤礦",
    "鎮山": "振山",
    "追著上": "追的上",
    "城外科": "陳外科",
    "高麗跟": "高麗坑",
    # must follow 高麗跟→高麗坑 so the ASR garble also picks up the gloss.
    # Only one occurrence in the SRT, so this cannot annotate a second mention.
    "高麗坑": "高麗坑（檳榔坑，現檳榔路）",
    "蓄碳廠": "蓄炭場",
    "抬車": "台車",
    "臺": "台",
    "，呃，": "，",
    "呃，": "",
    "呃": "",
    "啊，但是": "但是",
}
MAX_CUE = 14
EXTRA_CUES: list = []
GRADE = ""  # 4884 measured flicker-clean; no tmix needed

# --------------------------------------------------------------------------


def build_cards() -> None:
    CARDS.mkdir(parents=True, exist_ok=True)
    p = CARDS / "title.png"
    make_title_card(p, "新店礦業文化路徑", "期望的未來", "振山煤礦與光明街",
                    "口述：陳林彩薇")
    png_to_card_mp4(p, CARDS / "title.mp4", TITLE_DUR)
    for name, q in QUESTIONS.items():
        p = CARDS / f"{name}.png"
        make_question_card(p, q)
        png_to_card_mp4(p, CARDS / f"{name}.mp4", QCARD_DUR)
    assert len(TUNNEL_PHOTOS) >= 2, f"no 隧道 photos in {TUNNEL_DIR}"
    make_photo_grid_card(TUNNEL_PHOTOS, CARDS / "today_tunnel.mp4", TUNNEL_DUR,
                         caption="今日的振山煤礦台車山區段隧道")
    print(f"  今貌 grid → today_tunnel.mp4 ({len(TUNNEL_PHOTOS)} photos)")

    if not LANE_PHOTO.exists():          # iPhone HEIC → jpg (PIL can't read HEIC)
        subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions",
                        "92", str(LANE_HEIC), "--out", str(LANE_PHOTO)],
                       check=True, stdout=subprocess.DEVNULL)
        print(f"  converted {LANE_HEIC.name} → {LANE_PHOTO.name}")
    lane_len = float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(LANE_CLIP)],
        check=True, capture_output=True, text=True).stdout.strip())
    make_clip_photo_card(LANE_CLIP, 0.0, lane_len, LANE_PHOTO,
                         CARDS / "today_lane.mp4", LANE_DUR,
                         caption="今日的102台車巷")
    print(f"  今貌 timelapse → today_lane.mp4 ({lane_len:.1f}s → {LANE_DUR}s, "
          f"{lane_len/LANE_DUR:.1f}x)")

    for ph in BTS_STILLS:
        assert ph.exists(), f"missing BTS still: {ph}"
    d = make_credits_grid_mp4(CARDS / "end.mp4", "期望的未來", CREDITS,
                              BTS_STILLS, BTS_CLIPS)
    assert abs(d - END_DUR) < 1e-6, f"closer {d} != TIMELINE {END_DUR}"
    print(f"  closer → end.mp4 ({d:.2f}s, {len(BTS_STILLS)} stills)")
    print(f"cards → {CARDS}")


def kb_name(fname: str, dur: float) -> str:
    num = fname.rsplit("_", 1)[-1].split(".")[0]
    return f"kb_p{num}_{dur:g}s.mov"


def iter_block_overlays():
    for photos, _lbl, _pt, _delta, pdur, _xo in OVERLAY_BLOCKS:
        for ph in photos:
            yield ph, pdur


def build_kenburns() -> None:
    KB.mkdir(parents=True, exist_ok=True)
    for fname, dur in iter_block_overlays():
        out = KB / kb_name(fname, dur)
        if out.exists():
            continue
        make_kenburns(PHOTOS / fname, out, dur)
        print(f"  {out.name} ← {fname}")
    print(f"ken burns → {KB}")


def out_offsets() -> list[tuple]:
    rows, off = [], 0.0
    for seg in TIMELINE:
        dur = (seg[2] - seg[1]) if seg[0] == "cam" else seg[2]
        rows.append((seg[0], seg, off, dur))
        off += dur
    return rows


def label_bounds() -> dict[str, tuple[float, float]]:
    return {seg[3]: (off, off + dur)
            for kind, seg, off, dur in out_offsets() if kind == "cam"}


def audit_boundaries() -> None:
    """Warn if any cam cut slices a SPOKEN word (ignore pause-padding)."""
    tr = json.loads((EDIT / "transcripts" / TRANSCRIPT).read_text())
    words = [w for w in tr["words"] if w.get("type") == "word"
             and w.get("start") is not None and w["text"].strip() not in "，。？！、；："]
    for seg in TIMELINE:
        if seg[0] != "cam":
            continue
        a, b = seg[1], seg[2]
        for w in words:
            spoken_end = min(w["end"], w["start"] + 0.45)  # ignore pause-pad tail
            for cut in (a, b):
                if w["start"] + 0.02 < cut < spoken_end - 0.02:
                    print(f"  WARN {seg[3]}: cut {cut} may slice "
                          f"{w['text']!r} ({w['start']:.2f}-{w['end']:.2f})")


def build_edl() -> Path:
    sources = {"CAM": str(SRC)}
    ranges = []
    for kind, seg, off, dur in out_offsets():
        if kind == "cam":
            ranges.append({"source": "CAM", "start": seg[1], "end": seg[2],
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
            overlays.append({"file": str(KB / kb_name(fname, pdur)),
                             "start_in_output": round(t0 + pi * (pdur - xover), 3),
                             "duration": pdur})

    total = sum(r[3] for r in out_offsets())
    edl = {"version": 1, "sources": sources, "ranges": ranges,
           "grade": GRADE, "overlays": overlays,
           "total_duration_s": round(total, 2)}
    path = EDIT / "edl_zhenshan.json"
    path.write_text(json.dumps(edl, ensure_ascii=False, indent=2))
    print(f"EDL → {path}  (total {total:.1f}s = {int(total//60)}:{total%60:04.1f})")
    return path


def build_srt() -> Path:
    from opencc import OpenCC
    cc = OpenCC("s2twp")
    tr = json.loads((EDIT / "transcripts" / TRANSCRIPT).read_text())
    words = [w for w in tr["words"] if w.get("type") == "word"
             and w.get("start") is not None]

    cues = []
    for kind, seg, off, dur in out_offsets():
        if kind != "cam":
            continue
        a, b = seg[1], seg[2]
        seg_words = [w for w in words if a - 0.02 <= w["start"] < b - 0.05]

        def flush(buf: list) -> None:
            if not buf:
                return
            joined = "".join(x["text"].strip() for x in buf)
            starts = [x["start"] for x in buf
                      if x["text"].strip() not in "，。？！、；："]
            c_start = starts[0] if starts else buf[0]["start"]
            cues.append((max(a, c_start), min(b, buf[-1]["end"]), joined, off, a))

        cur, last_soft = [], -1
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
                    flush(cur[:last_soft]); cur = cur[last_soft:]
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
        final.append((o_start, min(o_end, o_start + 7.0), text))
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

    path = EDIT / "zhenshan_zht.srt"
    path.write_text("\n".join(lines))
    print(f"SRT → {path}  ({n} cues, Traditional)")
    return path


if __name__ == "__main__":
    print("boundary audit:")
    audit_boundaries()
    build_cards()
    build_kenburns()
    build_edl()
    build_srt()
