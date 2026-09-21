"""Mix the hybrid music bed into a finished video.

    .venv python edit/build/mix_music.py <slug> <video.mp4> <out.mp4>

"Hybrid" (Kyle's pick): a quiet bed runs throughout, sitting well under her
voice, and rises wherever nobody is speaking — the opening animation, the
question cards, the 今貌 photos, and the credits closer.

Speech regions come from the burned SRT, so the bed follows the actual dialogue
rather than a guess. The envelope is built in numpy (smooth raised-cosine
ramps) instead of ffmpeg `volume=enable=`, which switches hard and clicks.
Music shorter than the video is looped with an equal-power crossfade.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

BASE = Path(__file__).resolve().parents[2]
EDIT = BASE / "edit"
MUSIC = EDIT / "music"

SR = 48000
DUCK = 0.24        # bed level under speech (matches the C_hybrid demo)
RAMP = 1.1         # seconds, raised-cosine
PAD_IN = 0.35      # start ducking this long before a line
PAD_OUT = 0.5      # hold the duck this long after it
# Gaps shorter than this stay ducked. Tuned so a 2.6s question card does NOT
# make the bed lift (1.1s ramps in a 2.6s hole just pumps), while a 4.6s 今貌
# photo, the 5.5s thesis card, the opening and the closer all DO open up.
MERGE_GAP = 3.0
XFADE = 3.0        # loop crossfade
FADE_IN = 1.5      # music eases in from silence as the video opens from black
FADE_OUT = 4.5     # ...and eases out at the end rather than cutting off


def srt_regions(srt: Path) -> list[tuple[float, float]]:
    def ts(s: str) -> float:
        h, m, rest = s.split(":")
        sec, ms = rest.split(",")
        return int(h) * 3600 + int(m) * 60 + int(sec) + int(ms) / 1000
    cues = []
    for blk in srt.read_text(encoding="utf-8").strip().split("\n\n"):
        lines = blk.strip().split("\n")
        if len(lines) >= 2 and "-->" in lines[1]:
            a, b = lines[1].split(" --> ")
            cues.append((ts(a.strip()), ts(b.strip())))
    cues.sort()
    merged: list[list[float]] = []
    for a, b in cues:
        a, b = a - PAD_IN, b + PAD_OUT
        if merged and a - merged[-1][1] < MERGE_GAP:
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])
    return [(max(0.0, a), b) for a, b in merged]


def envelope(n: int, regions: list[tuple[float, float]]) -> np.ndarray:
    """1.0 where nothing is spoken, DUCK inside speech, cosine ramps between."""
    env = np.ones(n, dtype=np.float32)
    r = int(RAMP * SR)
    ramp = 0.5 * (1 - np.cos(np.linspace(0, np.pi, r)))     # 0→1 smooth
    for a, b in regions:
        i0, i1 = int(a * SR), int(b * SR)
        i0, i1 = max(0, i0), min(n, i1)
        if i1 <= i0:
            continue
        seg = np.full(i1 - i0, DUCK, dtype=np.float32)
        k = min(r, (i1 - i0) // 2)
        if k > 0:
            seg[:k] = 1.0 - (1.0 - DUCK) * ramp[:k]
            seg[-k:] = DUCK + (1.0 - DUCK) * ramp[:k]
        env[i0:i1] = np.minimum(env[i0:i1], seg)

    # Top and tail. Without these the bed starts and stops abruptly — the
    # closing cut was audible against the picture's own fade to black.
    fi = min(int(FADE_IN * SR), n)
    if fi > 0:
        env[:fi] *= 0.5 * (1 - np.cos(np.linspace(0, np.pi, fi)))
    fo = min(int(FADE_OUT * SR), n)
    if fo > 0:
        env[-fo:] *= 0.5 * (1 + np.cos(np.linspace(0, np.pi, fo)))
    return env


def loop_to(music: np.ndarray, n: int) -> np.ndarray:
    """Tile with an equal-power crossfade so the seam is inaudible."""
    if len(music) >= n:
        return music[:n]
    x = int(XFADE * SR)
    out = np.zeros((n, music.shape[1]), dtype=np.float32)
    pos, first = 0, True
    while pos < n:
        chunk = music if first else music[x:]
        take = min(len(chunk), n - pos)
        if first:
            out[pos:pos + take] = chunk[:take]
            pos += take
            first = False
            continue
        # crossfade the incoming head over the tail already written
        f = np.linspace(0, 1, x, dtype=np.float32)[:, None]
        head = music[:x]
        s = max(0, pos - x)
        ln = min(x, len(out) - s, len(head))
        out[s:s + ln] = (out[s:s + ln] * np.cos(f[:ln] * np.pi / 2) ** 2
                         + head[:ln] * np.sin(f[:ln] * np.pi / 2) ** 2)
        out[pos:pos + take] = chunk[:take]
        pos += take
    return out[:n]


def main() -> None:
    slug, vid_in, vid_out = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3])
    srt = EDIT / f"{slug}_zht.srt"
    mus_path = next((MUSIC / f"{slug_short}{e}" for slug_short in
                     (slug, {"shengping": "v1", "hemei": "v2",
                             "zhenshan": "v3"}[slug])
                     for e in (".wav", ".mp3", ".m4a")
                     if (MUSIC / f"{slug_short}{e}").exists()), None)
    if mus_path is None:
        sys.exit(f"no music for {slug} in {MUSIC}")

    dur = float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(vid_in)],
        check=True, capture_output=True, text=True).stdout.strip())

    music, sr = sf.read(str(mus_path), dtype="float32", always_2d=True)
    if sr != SR:
        sys.exit(f"expected {SR} Hz music, got {sr}")
    n = int(dur * SR)
    regions = srt_regions(srt)
    speech = sum(b - a for a, b in regions)
    print(f"{slug}: video {dur:.2f}s · music {len(music)/SR:.2f}s "
          f"({'loop' if len(music) < n else 'covers'}) · "
          f"{len(regions)} speech regions, {speech:.1f}s "
          f"({speech/dur*100:.0f}% of runtime)")
    holes, prev = [], 0.0
    for a, b in regions:
        if a - prev > 0.5:
            holes.append((prev, a))
        prev = b
    if dur - prev > 0.5:
        holes.append((prev, dur))
    print(f"  music lifts in {len(holes)} hole(s): " + ", ".join(
        f"{a:.0f}-{b:.0f}s ({b-a:.1f}s)" for a, b in holes))

    bed = loop_to(music, n) * envelope(n, regions)[:, None]
    bed_path = MUSIC / f"_bed_{slug}.wav"
    sf.write(str(bed_path), bed, SR)

    vid_out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([
        "ffmpeg", "-y", "-v", "error", "-i", str(vid_in), "-i", str(bed_path),
        "-filter_complex",
        # highpass 85 Hz on the dialogue: removes plosive thumps and room
        # rumble. Her voice's fundamental sits ~180-220 Hz, well clear of it,
        # so nothing audible in the speech is touched.
        "[0:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,"
        "highpass=f=85:poles=2[v];"
        "[1:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo[m];"
        "[v][m]amix=inputs=2:weights=1 1:normalize=0,alimiter=limit=0.97[a]",
        "-map", "0:v", "-map", "[a]", "-c:v", "copy",
        "-c:a", "aac", "-b:a", "256k", "-ar", "48000", str(vid_out)],
        check=True, stderr=subprocess.PIPE)
    bed_path.unlink()
    print(f"  → {vid_out}")


if __name__ == "__main__":
    main()
