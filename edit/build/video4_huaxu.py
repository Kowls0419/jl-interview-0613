"""Build video 製作花絮 (behind-the-scenes) — mic rehearsal + directing moments.

Sources: 002A4880 (rehearsal), 002A4881/002A4882 (direction interjections).
Montage of straight cuts, no photo overlays, no question cards.
grade tmix=frames=3 for the 4881 flicker (harmless on the others).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import (make_title_card, make_end_card, png_to_card_mp4,
                    make_kenburns, make_photo_pair_card)

BASE = Path(__file__).resolve().parents[2]
EDIT = BASE / "edit"
CARDS = EDIT / "cards_huaxu"
KB = EDIT / "kb_huaxu"
PHOTOS = BASE / "4"
SOURCES = {"S80": ("002A4880.MP4", "002A4880.json"),
           "S81": ("002A4881.MP4", "002A4881.json"),
           "S82": ("002A4882.MP4", "002A4882.json")}

TITLE_DUR = 3.5
END_DUR = 5.5

TIMELINE = [
    ("card", "title", TITLE_DUR),
    ("cam", "S80",   1.30,  27.15, "rehearsal"),   # 收音測試…那我去找阿媽/當心
    ("cam", "S81",  84.50,  90.60, "one_at_a_time"),  # 我覺得先一段一段
    ("cam", "S81", 100.98, 103.60, "look_here"),   # 阿媽等一下你要看這裡
    ("cam", "S82",  26.70,  33.75, "look_at_lens"),   # 可以看一下鏡頭 這樣好嗎
    ("cam", "S81", 339.90, 342.00, "watch_camera"),   # 看那個鏡頭
    ("cam", "S82",  95.30,  97.35, "cut_ok"),      # 來我們先停了嘛。好。
    ("card", "ending", 4.4),                        # 合影 | 庭院微笑 — 雙圖模糊底 as ending (replaces the live MOV clip)
    ("card", "end", END_DUR),
]

P = "LINE_ALBUM_2026.7.6 _3_260708_{}.jpg"
# (photos, anchor_label, "end"/"start", delta, per_photo_dur, xover)
# All stills are framed overlays ON the playing footage (Kyle: no standalone pic
# cards). Deduped — one shot per "kind" (dropped near-dupes 3,4,5,10,24,25,1).
OVERLAY_BLOCKS = [
    ([P.format(23), P.format(8), P.format(20), P.format(21)],
        "rehearsal", "start", 2.0, 4.5, 1.0),      # 架燈/走廊/棚內全景/過肩 (over the long setup take)
    ([P.format(6)], "one_at_a_time", "start", 0.8, 4.5, 0.0),   # 導演說戲
    ([P.format(7)], "look_at_lens", "start", 1.0, 4.5, 0.0),    # 環燈中的阿媽
]
# 9 & 2 now form the blur-bg diptych ENDING card (see build_cards), not an overlay.
ENDING_PAIR = (P.format(9), P.format(2))

SUB_FIXES = {
    "臺": "台",
    "，呃，": "，",
    "呃，": "",
    "呃": "",
}
MAX_CUE = 14
GRADE = "tmix=frames=3"

# --------------------------------------------------------------------------


def build_cards() -> None:
    CARDS.mkdir(parents=True, exist_ok=True)
    p = CARDS / "title.png"
    make_title_card(p, "新店礦業文化路徑", "製作花絮", "拍攝側記")
    png_to_card_mp4(p, CARDS / "title.mp4", TITLE_DUR)
    lf, rf = ENDING_PAIR
    make_photo_pair_card(PHOTOS / lf, PHOTOS / rf, CARDS / "ending.mp4", 4.4, blur_bg=True)
    print(f"  ending pair card ← {lf} | {rf} (blur bg)")
    p = CARDS / "end.png"
    make_end_card(p, "製作花絮", [
        ("口述", "陳林彩薇（林秀卿先生之女）"),
        ("指導單位", "新北市政府文化局"),
        ("執行單位", "新北市陳昌梯醫師山林保育協會"),
    ])
    png_to_card_mp4(p, CARDS / "end.mp4", END_DUR)
    print(f"cards → {CARDS}")


def kb_name(fname: str, dur: float) -> str:
    num = fname.rsplit("_", 1)[-1].split(".")[0]
    return f"kb_p{num}_{dur:g}s.mov"


def build_kenburns() -> None:
    KB.mkdir(parents=True, exist_ok=True)
    for photos, _lbl, _pt, _delta, pdur, _xo in OVERLAY_BLOCKS:
        for fname in photos:
            out = KB / kb_name(fname, pdur)
            if out.exists():
                continue
            make_kenburns(PHOTOS / fname, out, pdur)
            print(f"  {out.name} ← {fname}")
    print(f"ken burns → {KB}")


def label_bounds() -> dict:
    return {seg[4]: (off, off + dur)
            for kind, seg, off, dur in out_offsets() if kind == "cam"}


def out_offsets() -> list[tuple]:
    rows, off = [], 0.0
    for seg in TIMELINE:
        dur = (seg[3] - seg[2]) if seg[0] == "cam" else seg[2]
        rows.append((seg[0], seg, off, dur))
        off += dur
    return rows


def _load_words(json_name: str) -> list[dict]:
    tr = json.loads((EDIT / "transcripts" / json_name).read_text())
    return [w for w in tr["words"] if w.get("type") == "word"
            and w.get("start") is not None]


def audit_boundaries() -> None:
    for src_key, (_mp4, jname) in SOURCES.items():
        words = [w for w in _load_words(jname)
                 if w["text"].strip() not in "，。？！、；：（）()"]
        for seg in TIMELINE:
            if seg[0] != "cam" or seg[1] != src_key:
                continue
            a, b = seg[2], seg[3]
            for w in words:
                spoken_end = min(w["end"], w["start"] + 0.45)
                for cut in (a, b):
                    if w["start"] + 0.02 < cut < spoken_end - 0.02:
                        print(f"  WARN {seg[4]}: cut {cut} may slice "
                              f"{w['text']!r} ({w['start']:.2f}-{w['end']:.2f})")


def build_edl() -> Path:
    sources = {k: str(BASE / mp4) for k, (mp4, _j) in SOURCES.items()}
    ranges = []
    for kind, seg, off, dur in out_offsets():
        if kind == "cam":
            ranges.append({"source": seg[1], "start": seg[2], "end": seg[3],
                           "beat": seg[4], "quote": "", "reason": ""})
        else:
            name = seg[1]
            key = f"CARD_{name}"
            sources[key] = str(CARDS / f"{name}.mp4")
            ranges.append({"source": key, "start": 0.0, "end": dur,
                           "beat": f"card {name}", "quote": "", "reason": ""})

    bounds = label_bounds()
    overlays = []
    for photos, lbl, pt, delta, pdur, xover in OVERLAY_BLOCKS:
        base_t = bounds[lbl][1] if pt == "end" else bounds[lbl][0]
        t0 = base_t + delta
        for pi, fname in enumerate(photos):
            overlays.append({"file": str(KB / kb_name(fname, pdur)),
                             "start_in_output": round(t0 + pi * (pdur - xover), 3),
                             "duration": pdur})

    total = sum(r[3] for r in out_offsets())
    edl = {"version": 1, "sources": sources, "ranges": ranges,
           "grade": GRADE, "overlays": overlays,
           "total_duration_s": round(total, 2)}
    path = EDIT / "edl_huaxu.json"
    path.write_text(json.dumps(edl, ensure_ascii=False, indent=2))
    print(f"EDL → {path}  (total {total:.1f}s = {int(total//60)}:{total%60:04.1f})")
    return path


def build_srt() -> Path:
    from opencc import OpenCC
    cc = OpenCC("s2twp")
    words_by_src = {k: _load_words(j) for k, (_m, j) in SOURCES.items()}

    cues = []
    for kind, seg, off, dur in out_offsets():
        if kind != "cam":
            continue
        src_key, a, b = seg[1], seg[2], seg[3]
        if src_key not in words_by_src:
            continue
        seg_words = [w for w in words_by_src[src_key]
                     if a - 0.02 <= w["start"] < b - 0.05]

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
            plain = re.sub(r"[，。？！、；：（）()]", "", joined)
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

    final = []
    for w_start, w_end, text, off, seg_a in cues:
        text = cc.convert(text)
        for k, v in SUB_FIXES.items():
            text = text.replace(k, v)
        text = text.strip("，、； ").rstrip("。").strip("（）()")
        if not re.sub(r"[，。？！、；：（）()]", "", text):
            continue
        o_start = w_start - seg_a + off
        o_end = max(o_start + 0.5, w_end - seg_a + off)
        final.append((o_start, min(o_end, o_start + 7.0), text))
    final.sort(key=lambda c: c[0])

    lines, n = [], 0
    for o_start, o_end, text in final:
        n += 1
        lines += [str(n), f"{ts(o_start)} --> {ts(o_end)}", text, ""]

    path = EDIT / "huaxu_zht.srt"
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
