"""Build video 期望的未來 (生平/過水橋/瑠公圳) — multi-source: 002A4881 + 002A4882.

4881 (30fps) flickers (mean 0.376): grade tmix=frames=3 (tmix=5 smears her face at
30fps — tested). 4882 is clean; tmix=3 on it is harmless. Photos: folder 3/.
Opening: build/make_opening_shengping.py (photo 3-2 北一女 class photo).

Run:  .venv python edit/build/video3_shengping.py
Then: render.py edit/edl_shengping.json -o edit/shengping_nosub.mp4 --preview --no-subtitles
Then burn (same grade + LXGW WenKai TC command).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import (make_title_card, make_question_card, make_end_card,
                    make_statement_card, make_photo_card,
                    png_to_card_mp4, make_kenburns,
                    make_credits_grid_mp4, credits_grid_duration)

BASE = Path(__file__).resolve().parents[2]
EDIT = BASE / "edit"
CARDS = EDIT / "cards_shengping"
KB = EDIT / "kb_shengping"
SOURCES = {"S80": ("002A4880.MP4", "002A4880.json"),   # BTS: mic rehearsal
           "S81": ("002A4881.MP4", "002A4881.json"),
           "S82": ("002A4882.MP4", "002A4882.json")}
PHOTOS = BASE / "3"
BTS_PHOTOS = BASE / "4"

QCARD_DUR = 2.6
TITLE_DUR = 4.0
OPENING_DUR = 10.0
TODAY_DUR = 4.6

# 今貌 shot 2026-08. Placed FIRST of the three so it lands straight off her
# last line (碧潭的水都很乾淨) — and so the thesis card, which names only
# 過水橋 and 瑠公圳, still follows those two.
TODAY_BITAN = BASE / "IRL" / "今日的碧潭.jpg"

# 手術室 stills for the closer grid — Kyle's r02 re-pick via edit/v1_grid.html
# (dropped N6448 as a near-dup of P20).
BTS_STILLS = [
    BTS_PHOTOS / "LINE_ALBUM_2026.7.6 _3_260708_1.jpg",    # P1
    BTS_PHOTOS / "LINE_ALBUM_2026.7.6 _3_260708_4.jpg",    # P4
    BTS_PHOTOS / "LINE_ALBUM_2026.7.6 _3_260708_20.jpg",   # P20
    BTS_PHOTOS / "LINE_ALBUM_2026.7.6 _3_260708_23.jpg",   # P23
    BTS_PHOTOS / "LINE_ALBUM_2026.7.6 _3_260708_24.jpg",   # P24
]
# 手術室 BTS clips — SILENT tiles inside the closer grid, not full-screen beats
# (Kyle, review r01 note 2). Longer ones are sped up to fit the play window;
# every tile lands its last frame together. No subtitles.
BTS_CLIPS = [
    (BASE / "002A4880.MP4",  10.72,  17.36),   # K3 我有回音什麼的…這距離 OK 嗎
    (BASE / "002A4881.MP4", 339.90, 342.00),   # K10 看那個鏡頭
]
END_DUR = credits_grid_duration(len(BTS_STILLS) + len(BTS_CLIPS), has_clips=True)

CREDITS = [
    ("口述", "陳林彩薇（林秀卿先生之女）"),
    ("攝影", "李承洋"),
    ("後製剪輯", "楊大謙"),
    ("指導單位", "新北市政府文化局"),
    ("執行單位", "新北市陳昌梯醫師山林保育協會"),
]

# ("cam", src_key, a, b, label) — splices/source-switches hidden under photos.
TIMELINE = [
    ("card", "opening", OPENING_DUR),
    ("card", "title", TITLE_DUR),
    ("card", "scene", 4.2),                     # opening C: scene-setting
    ("cam", "S81", 913.55, 915.71, "hook_a"),   # 當時只有這一條橋可以出入啊
    ("cam", "S81", 926.15, 932.95, "hook_b"),   # 用木頭蓋起來…走木頭上面
    ("card", "q1", QCARD_DUR),
    ("cam", "S81", 103.74, 119.98, "intro"),    # 住在彰化的和美…搬到新店來
    ("card", "q2", QCARD_DUR),
    ("cam", "S81", 391.79, 416.80, "war"),      # 學校當作陸軍醫院…一面躲空襲一面讀書
    ("card", "q3", QCARD_DUR),
    ("cam", "S81", 572.05, 578.91, "school_a"), # 國語實小…考進北一女
    ("cam", "S81", 583.33, 596.29, "school_b"), # 白色衣服藍色褲子…裙子這樣
    ("card", "q4", QCARD_DUR),
    ("cam", "S81", 606.15, 609.99, "dad"),      # 爸爸說女孩子讀到這裡就好了
    ("card", "q5", QCARD_DUR),
    ("cam", "S81", 638.61, 653.75, "home"),     # 一千兩百坪大宅院…二姑丈住的
    ("card", "q6", QCARD_DUR),
    ("cam", "S81", 720.65, 723.45, "gone_a"),   # 後來開馬路的時候拆了
    ("cam", "S81", 725.95, 732.00, "gone_b"),   # 新店到安坑大橋…拆了這個房子
    ("card", "q7", QCARD_DUR),
    ("cam", "S81", 933.39, 956.95, "typhoon"),  # 颱風把橋翻下去…我都走在水裡面
    ("card", "q8", QCARD_DUR),
    ("cam", "S81", 971.11, 976.40, "canal_a"),  # 瑠公圳源頭在碧潭新店國小那一帶
    ("cam", "S81", 979.85, 983.35, "canal_b"),  # 水很乾淨 我們都在這裡游泳
    ("cam", "S82",   6.64,  20.14, "swim"),     # 水流很快 我們都朝著逆水游泳
    ("cam", "S82",  48.72,  58.30, "hero"),     # 逆水游…我是等於一個游泳選手
    ("cam", "S82",  74.96,  83.06, "clean"),    # 當時碧潭的水都很乾淨
    ("card", "today_bitan", TODAY_DUR),         # 碧潭今貌 (IRL/, 2026-08)
    ("card", "today_bridge", 4.6),              # 3-7 過水橋今貌
    ("card", "today_canal", 4.6),               # 3-8 瑠公圳今貌
    ("card", "thesis", 5.5),                    # ending A: closing thesis
    ("card", "end", END_DUR),   # credits → shrink left + 花絮 grid (stills + silent clips)
]

QUESTIONS = {
    "q1": "妳是怎麼來到新店的？",
    "q2": "戰爭的時候怎麼上學？",
    "q3": "後來讀哪裡？",
    "q4": "為什麼沒有繼續升學？",
    "q5": "老家是什麼樣子？",
    "q6": "後來房子呢？",
    "q7": "颱風來的時候呢？",
    "q8": "瑠公圳的水怎麼樣？",
}

P = "LINE_ALBUM_2026.7.6 _2_260706_{}.jpg"
# (photos, anchor_label, "end"/"start", delta, per_photo_dur, xover)
# Gaze-driven (Kyle): where she looks at camera keep footage; where she looks
# away (school/dad, hook_b mid, swim edges) or the interviewer intrudes (home
# whole segment, canal_a head at left) cover with photos.
OVERLAY_BLOCKS = [
    ([P.format(10), P.format(17)], "hook_a", "start", 1.0, 3.9, 1.0),  # 過水橋：兩張過橋身影 (framed, ~1s footage each side of the pics — no card flash)
    ([P.format(19)], "intro", "start", 6.0, 7.0, 0.0),          # 全家福
    ([P.format(14)], "war", "start", 8.0, 8.0, 0.0),            # 吊橋邊的孩子們
    ([P.format(5), P.format(4)], "school_a", "start", 1.0, 9.3, 1.0),  # 女學生/年輕身影 (framed: ~1s footage each side)
    ([P.format(11)], "dad", "start", -0.6, 5.8, 0.0),          # COVER; extra-long tail so it stays opaque ~1s into q5 card (beats concat frame-drift → no exit flash)
    ([P.format(12), P.format(13)], "home", "start", -0.6, 9.1, 1.0),  # 圓窗→鋼琴 COVER; tail stays opaque ~1s into q6 card (no exit flash)
    ([P.format(15)], "canal_a", "start", -0.2, 8.9, 0.0),        # 圳中游泳
    ([P.format(1)], "swim", "start", 0.3, 7.5, 0.0),            # 圳邊少女 (3-3 dropped as dup)
]

SUB_FIXES = {
    # MUST STAY FIRST. OpenCC s2twp converts 游→遊 (the "travel" sense), which is
    # wrong for every 游 in this interview — she is talking about swimming
    # throughout. The ASR is 游 everywhere; the 遊 is introduced by the conversion.
    # Keeping this first also revives "近水游"→"逆水游" below, which never fired
    # because s2twp had already turned the string into 近水遊.
    "遊": "游",
    "精美": "景美",
    "柳公圳": "瑠公圳",
    "近水游": "逆水游",
    "二姑丈": "二姑丈（劉明）",
    "所以我是等於一個游泳選手": "所以我是北一女的游泳選手",
    "百平": "百坪",   # 大宅院面積：坪 not 平
    "千平": "千坪",
    "臺": "台",
    "，呃，": "，",
    "呃，": "",
    "呃": "",
    "啊，但是": "但是",
}
MAX_CUE = 14
EXTRA_CUES: list = []
GRADE = "tmix=frames=3"  # 4881 flicker; =5 smears at 30fps (tested)

# --------------------------------------------------------------------------


def build_cards() -> None:
    CARDS.mkdir(parents=True, exist_ok=True)
    p = CARDS / "title.png"
    make_title_card(p, "新店礦業文化路徑", "光陰的故事", "過水橋與瑠公圳",
                    "口述：陳林彩薇")
    png_to_card_mp4(p, CARDS / "title.mp4", TITLE_DUR)
    p = CARDS / "scene.png"
    make_statement_card(p, ["過水橋，曾是這戶人家", "出入家門的唯一通道。"])
    png_to_card_mp4(p, CARDS / "scene.mp4", 4.2)
    p = CARDS / "thesis.png"
    make_statement_card(p, ["如今，過水橋與瑠公圳仍在，", "願這段光陰，隨水長流。"])
    png_to_card_mp4(p, CARDS / "thesis.mp4", 5.5)
    assert TODAY_BITAN.exists(), f"missing 今貌 photo: {TODAY_BITAN}"
    make_photo_card(TODAY_BITAN, CARDS / "today_bitan.mp4", TODAY_DUR,
                    caption="今日的碧潭")
    make_photo_card(PHOTOS / P.format(7), CARDS / "today_bridge.mp4", 4.6,
                    caption="今日的過水橋")
    make_photo_card(PHOTOS / P.format(8), CARDS / "today_canal.mp4", 4.6,
                    caption="今日的瑠公圳")
    for name, q in QUESTIONS.items():
        p = CARDS / f"{name}.png"
        make_question_card(p, q)
        png_to_card_mp4(p, CARDS / f"{name}.mp4", QCARD_DUR)
    for ph in BTS_STILLS:
        assert ph.exists(), f"missing BTS still: {ph}"
    d = make_credits_grid_mp4(CARDS / "end.mp4", "光陰的故事", CREDITS,
                              BTS_STILLS, BTS_CLIPS)
    assert abs(d - END_DUR) < 1e-6, f"closer {d} != TIMELINE {END_DUR}"
    print(f"  closer → end.mp4 ({d:.2f}s, {len(BTS_STILLS)} stills)")
    print(f"cards → {CARDS}")


# labels using full-bleed cover fill (interviewer intrudes, or Kyle wants
# "just the pic, blur bg" — no footage). Cover photos may go card→cover directly.
COVER_LABELS = {"home", "canal_a", "dad"}


def kb_name(fname: str, dur: float, cover: bool = False) -> str:
    num = fname.rsplit("_", 1)[-1].split(".")[0]
    return f"kb_p{num}_{dur:g}s{'_cov' if cover else ''}.mov"


def build_kenburns() -> None:
    KB.mkdir(parents=True, exist_ok=True)
    for photos, lbl, _pt, _delta, pdur, _xo in OVERLAY_BLOCKS:
        cov = lbl in COVER_LABELS
        for fname in photos:
            out = KB / kb_name(fname, pdur, cov)
            if out.exists():
                continue
            make_kenburns(PHOTOS / fname, out, pdur, cover=cov)
            print(f"  {out.name} ← {fname}{' [cover]' if cov else ''}")
    print(f"ken burns → {KB}")


def out_offsets() -> list[tuple]:
    rows, off = [], 0.0
    for seg in TIMELINE:
        dur = (seg[3] - seg[2]) if seg[0] == "cam" else seg[2]
        rows.append((seg[0], seg, off, dur))
        off += dur
    return rows


def label_bounds() -> dict[str, tuple[float, float]]:
    return {seg[4]: (off, off + dur)
            for kind, seg, off, dur in out_offsets() if kind == "cam"}


def _load_words(json_name: str) -> list[dict]:
    tr = json.loads((EDIT / "transcripts" / json_name).read_text())
    return [w for w in tr["words"] if w.get("type") == "word"
            and w.get("start") is not None]


def audit_boundaries() -> None:
    for src_key, (_mp4, jname) in SOURCES.items():
        words = [w for w in _load_words(jname)
                 if w["text"].strip() not in "，。？！、；："]
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
        cov = lbl in COVER_LABELS
        for pi, fname in enumerate(photos):
            overlays.append({"file": str(KB / kb_name(fname, pdur, cov)),
                             "start_in_output": round(t0 + pi * (pdur - xover), 3),
                             "duration": pdur})

    total = sum(r[3] for r in out_offsets())
    edl = {"version": 1, "sources": sources, "ranges": ranges,
           "grade": GRADE, "overlays": overlays,
           "total_duration_s": round(total, 2)}
    path = EDIT / "edl_shengping.json"
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

    path = EDIT / "shengping_zht.srt"
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
