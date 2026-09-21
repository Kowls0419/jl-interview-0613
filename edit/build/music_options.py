"""Build three ~50s music-treatment demos from a finished video, so Kyle can
hear the options back to back before we commit to one.

    .venv python edit/build/music_options.py v1

Each demo stitches three moments that are far apart in the real timeline —
the silent opening animation, a passage where she is speaking, and the credits
closer — so every option can be judged in under a minute.

  A  continuous : bed under everything, side-chain ducked by her voice
  B  bookend    : music ONLY over the silent opening and the closer
  C  hybrid     : quiet bed throughout, rising wherever nobody is speaking
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
EDIT = BASE / "edit"
MUSIC = EDIT / "music"
OUT = MUSIC / "demo"

# slug -> (preview file, music stem, opening window, speech window, closer start)
VIDS = {
    "v1": ("shengping_preview.mp4", "v1", (0.0, 13.0), (96.0, 116.0), 219.83),
    "v2": ("hemei_preview.mp4",     "v2", (0.0, 13.0), (60.0, 80.0), 173.25),
    "v3": ("zhenshan_preview.mp4",  "v3", (0.0, 13.0), (60.0, 80.0), 161.58),
}

CLOSER_LEN = 16.0        # tail of the video to include in the demo
MUSIC_EXTS = (".mp3", ".wav", ".m4a", ".aac", ".flac", ".ogg")


def find_music(stem: str) -> Path:
    for ext in MUSIC_EXTS:
        p = MUSIC / f"{stem}{ext}"
        if p.exists():
            return p
    hits = [p for p in MUSIC.iterdir()
            if p.suffix.lower() in MUSIC_EXTS and p.stem.startswith(stem)]
    if hits:
        return sorted(hits)[0]
    sys.exit(f"no music found — put a file at {MUSIC / (stem + '.mp3')}")


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL,
                   stderr=subprocess.PIPE)


def cut(src: Path, a: float, dur: float, out: Path) -> None:
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{a:.3f}", "-i", str(src),
         "-t", f"{dur:.3f}", "-c:v", "libx264", "-preset", "veryfast",
         "-crf", "20", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", str(out)])


def main() -> None:
    slug = sys.argv[1] if len(sys.argv) > 1 else "v1"
    vid, stem, opening, speech, closer_at = VIDS[slug]
    src = EDIT / vid
    if not src.exists():
        sys.exit(f"missing {src}")
    mus = find_music(stem)
    OUT.mkdir(parents=True, exist_ok=True)
    work = OUT / "_work"
    work.mkdir(exist_ok=True)
    print(f"video : {src.name}\nmusic : {mus.name}")

    # ---- 1. three excerpts, concatenated into one demo body -----------------
    parts = [("open", opening[0], opening[1] - opening[0]),
             ("talk", speech[0], speech[1] - speech[0]),
             ("close", closer_at, CLOSER_LEN)]
    seg_paths = []
    for name, a, d in parts:
        p = work / f"seg_{name}.mp4"
        cut(src, a, d, p)
        seg_paths.append(p)
        print(f"  excerpt {name:5} {a:7.2f} +{d:5.2f}s")

    lst = work / "concat.txt"
    lst.write_text("".join(f"file '{p.resolve()}'\n" for p in seg_paths))
    body = work / "body.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
         "-i", str(lst), "-c", "copy", str(body)])

    body_len = sum(d for _n, _a, d in parts)
    t_open = parts[0][2]
    t_talk = t_open + parts[1][2]
    print(f"demo body: {body_len:.1f}s  (open→{t_open:.1f}  talk→{t_talk:.1f})")

    # ---- 2. three music treatments -----------------------------------------
    # A: continuous, side-chain ducked by the dialogue itself
    fa = (
        "[1:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,"
        f"atrim=0:{body_len:.3f},volume=0.75[m];"
        "[0:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,"
        "asplit=2[v0][key];"
        "[m][key]sidechaincompress=threshold=0.03:ratio=9:attack=12:release=420[mduck];"
        "[v0][mduck]amix=inputs=2:weights=1 1:normalize=0,alimiter=limit=0.95[a]"
    )
    # Smooth gate: 1 before T1, ramp down over D, 0 until T2, ramp back up.
    # Written as ONE volume expression — chaining afade=out then afade=in does
    # NOT work, the out-fade zeroes everything after it and the in-fade has
    # nothing left to raise.
    def gate(t1: float, t2: float, lo: float, d: float = 1.2) -> str:
        up = f"min(max(({t1:.2f}-t)/{d},0),1)"
        dn = f"min(max((t-{t2:.2f})/{d},0),1)"
        return (f"volume=eval=frame:volume='{lo}+(1-{lo})*max({up},{dn})'")

    # B: music only over the opening and the closer, silent under speech
    fb = (
        "[1:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,"
        f"atrim=0:{body_len:.3f},volume=1.0,"
        f"{gate(t_open - 0.4, t_talk - 0.2, 0.0)}[m];"
        "[0:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo[v0];"
        "[v0][m]amix=inputs=2:weights=1 1:normalize=0,alimiter=limit=0.95[a]"
    )
    # C: quiet throughout, rising where nobody speaks
    fc = (
        "[1:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,"
        f"atrim=0:{body_len:.3f},volume=0.9,"
        f"{gate(t_open - 0.4, t_talk - 0.2, 0.24)}[m];"
        "[0:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo[v0];"
        "[v0][m]amix=inputs=2:weights=1 1:normalize=0,alimiter=limit=0.95[a]"
    )

    for tag, filt in (("A_continuous", fa), ("B_bookend", fb), ("C_hybrid", fc)):
        out = OUT / f"{tag}.mp4"
        run(["ffmpeg", "-y", "-v", "error", "-i", str(body),
             "-stream_loop", "-1", "-i", str(mus),
             "-filter_complex", filt, "-map", "0:v", "-map", "[a]",
             "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
             "-shortest", str(out)])
        # music-only stem, same automation, so the treatment can be MEASURED
        # rather than assumed (an option that silently does nothing looks fine)
        stem_filt = filt.split("[v0][m]")[0].split("[0:a]")[0].rstrip(";")
        stem_filt = stem_filt.replace("[m]", "[a]")
        run(["ffmpeg", "-y", "-v", "error", "-i", str(body),
             "-stream_loop", "-1", "-i", str(mus),
             "-filter_complex", stem_filt, "-map", "[a]",
             "-c:a", "pcm_s16le", "-ar", "48000",
             "-t", f"{body_len:.3f}", str(OUT / f"_stem_{tag}.wav")])
        print(f"  → {out.name}")

    for p in work.glob("*"):
        p.unlink()
    work.rmdir()
    print(f"\ndemos → {OUT}")


if __name__ == "__main__":
    main()
