"""Opening for 和美煤礦 — follows Kyle's storyboard:

  1. Calligraphy brush "writes" the mine-name plaque (right→left) and the two
     door inscriptions (vertical columns, outer column first, both doors in
     parallel) as dark ink on paper.
  2. Pencil sketch draws the people in the middle (left→right sweep).
  3. The rest of the scene sketches in faintly, then the whole drawing
     crossfades into the real photograph with a slow push-in.

Her hook line (002A4883 55.97-62.75) runs underneath as V.O.
Output: edit/cards_hemei/opening.mp4  (10.0s, 1920x1080@24, with audio)
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps

sys.path.insert(0, str(Path(__file__).parent))
from common import W, H, FPS, BG

BASE = Path(__file__).resolve().parents[2]
PHOTO = BASE / "2" / "LINE_ALBUM_2026.7.6 _1_260706_14.jpg"
SRC = BASE / "002A4883.MP4"
OUT = BASE / "edit" / "cards_hemei" / "opening.mp4"

DUR = 10.0
REVEAL_A, REVEAL_B = 6.5, 8.4   # brush-band photo reveal window (no plain fade)
FADEOUT = 0.4

BORDER = 10
PAPER = (242, 236, 222)
INK = np.array([28, 21, 14], np.float32)

# regions in photo pixel coords (1175x832)
PLAQUE = (460, 138, 688, 198)          # 和美煤礦, brush right→left
RD_A = (988, 308, 1082, 600)           # 注意保安 (outer right col)
RD_B = (900, 325, 988, 570)            # 節約資材
LD_A = (205, 295, 280, 630)            # 努力生產 (outer left col)
LD_B = (133, 320, 205, 630)            # 改善生活
PEOPLE = (285, 325, 895, 705)

# (region, kind, bright?, t_start, t_end, direction)
INK_STEPS = [
    (PLAQUE, "dark", 0.20, 1.80, "rtl"),
    (RD_A, "bright", 1.55, 3.05, "ttb"),
    (LD_A, "bright", 1.55, 3.05, "ttb"),
    (RD_B, "bright", 2.40, 3.90, "ttb"),
    (LD_B, "bright", 2.40, 3.90, "ttb"),
]
PEOPLE_T = (3.95, 6.35)
REST_T = (5.90, 6.70)
STRUCT_T = (0.30, 1.60)


def ease(t: float) -> float:
    if t < 0.5:
        return 4 * t ** 3
    return 1 - (-2 * t + 2) ** 3 / 2


def main() -> None:
    ph = Image.open(PHOTO).convert("RGB")
    pw, phh = ph.size
    photo_np = np.asarray(ph).astype(np.float32)
    g = ImageOps.autocontrast(ph.convert("L"), cutoff=1)
    g_np = np.asarray(g).astype(np.float32)

    # pencil sketch layer (dodge + edges)
    inv_blur = np.asarray(Image.fromarray((255 - g_np).astype(np.uint8)).filter(
        ImageFilter.GaussianBlur(9))).astype(np.float32)
    dodge = np.clip(g_np * 255.0 / (256.0 - inv_blur), 0, 255)
    edges = np.asarray(g.filter(ImageFilter.FIND_EDGES).filter(
        ImageFilter.GaussianBlur(1))).astype(np.float32)
    edge_ink = np.clip((edges - 18) * 2.2, 0, 255)
    sketch_ink = np.maximum((255.0 - dodge) * 0.85, edge_ink * 0.75)  # 0..255 ink amt
    struct_ink = np.clip(edge_ink * 0.32, 0, 255)                     # faint structure

    # text ink masks
    def region_mask(box, kind) -> np.ndarray:
        x0, y0, x1, y1 = box
        r = g_np[y0:y1, x0:x1]
        if kind == "bright":
            m = (r > np.percentile(r, 82)).astype(np.float32)
        else:
            m = (r < np.percentile(r, 35)).astype(np.float32)
        full = np.zeros_like(g_np)
        full[y0:y1, x0:x1] = m
        full = np.asarray(Image.fromarray((full * 255).astype(np.uint8)).filter(
            ImageFilter.GaussianBlur(0.8))).astype(np.float32) / 255.0
        return full

    ink_masks = [(box, region_mask(box, kind), t0, t1, d)
                 for box, kind, t0, t1, d in INK_STEPS]

    # people soft mask
    pm = Image.new("L", (pw, phh), 0)
    ImageDraw.Draw(pm).rounded_rectangle(PEOPLE, radius=60, fill=255)
    people_mask = np.asarray(pm.filter(ImageFilter.GaussianBlur(30))).astype(np.float32) / 255.0

    # keep the people area blank until their pencil pass (struct would pre-echo them)
    struct_ink = struct_ink * (1.0 - people_mask * 0.85)

    yy, xx = np.mgrid[0:phh, 0:pw].astype(np.float32)
    rng = np.random.default_rng(7)
    noise = np.asarray(Image.fromarray(
        (rng.random((phh // 8, pw // 8)) * 255).astype(np.uint8)
    ).resize((pw, phh), Image.BILINEAR)).astype(np.float32) / 255.0 - 0.5

    # broad brush bands for the final photo reveal: 5 alternating diagonal swipes
    NB = 5
    band_v = np.clip((0.22 * xx / pw + 0.78 * yy / phh) * NB, 0, NB - 1e-4)
    band_i = np.floor(band_v)
    along = xx / pw
    along = np.where(band_i % 2 == 0, along, 1.0 - along)  # alternate direction
    BAND_SWEEP, BAND_STAGGER = 1.05, 0.22

    paper_np = np.zeros((phh, pw, 3), np.float32)
    paper_np[:] = PAPER
    paper_np -= (noise[..., None]) * 9

    # canvas geometry (same as Ken Burns clips)
    target_h = int(H * 0.84)
    scale = target_h / phh
    tw = int(pw * scale)
    if tw > int(W * 0.90):
        tw = int(W * 0.90)
        target_h = int(phh * (tw / pw))
    px_c, py_c = (W - tw) // 2, (H - target_h) // 2

    bg_frame = Image.new("RGB", (W, H), BG)
    ImageDraw.Draw(bg_frame).rectangle(
        [px_c - BORDER, py_c - BORDER, px_c + tw + BORDER, py_c + target_h + BORDER],
        fill=(226, 216, 196))

    def sweep(box, t0, t1, t, direction) -> float | np.ndarray:
        """0..1 reveal field over the region box with a noisy brush front."""
        if t <= t0:
            return 0.0
        if t >= t1 + 0.25:
            return 1.0
        p = min(1.0, (t - t0) / (t1 - t0)) * 1.12
        x0, y0, x1, y1 = box
        if direction == "ttb":
            axis = (yy - y0) / max(1, (y1 - y0))
        elif direction == "rtl":
            axis = (x1 - xx) / max(1, (x1 - x0))
        else:  # ltr
            axis = (xx - x0) / max(1, (x1 - x0))
        return np.clip((p - axis + noise * 0.10) / 0.07, 0, 1)

    frames_dir = OUT.parent / "_frames_opening"
    frames_dir.mkdir(parents=True, exist_ok=True)
    n = round(DUR * FPS)

    for i in range(n):
        t = i / FPS
        img = paper_np.copy()

        # faint structural pencil, swept in diagonally like quick underdrawing
        sp = np.clip((t - STRUCT_T[0]) / (STRUCT_T[1] - STRUCT_T[0]), 0, 1) * 1.15
        s_axis = (xx / pw + yy / phh) / 2.0
        s_rev = np.clip((sp - s_axis + noise * 0.10) / 0.09, 0, 1)
        total_ink = struct_ink * s_rev

        # people pencil sketch
        rev = sweep(PEOPLE, *PEOPLE_T, t=t, direction="ltr")
        total_ink = np.maximum(total_ink, sketch_ink * people_mask * rev)

        # rest of scene sketches in just before the crossfade
        r_fade = np.clip((t - REST_T[0]) / (REST_T[1] - REST_T[0]), 0, 1)
        total_ink = np.maximum(total_ink, sketch_ink * 0.62 * r_fade)

        img -= total_ink[..., None] * (img - 30) / 255.0 * 0.95

        # calligraphy ink (opaque dark strokes, wet-front emphasis)
        for box, mask, t0, t1, d in ink_masks:
            rv = sweep(box, t0, t1, t=t, direction=d)
            a = np.clip(mask * rv * 1.05, 0, 1)[..., None]
            img = img * (1 - a) + INK * a

        # photo revealed by broad brush swipes (not a plain fade)
        if t >= REVEAL_B + 0.2:
            img = photo_np.copy()
        elif t > REVEAL_A:
            tt_r = t - REVEAL_A
            prog = np.clip((tt_r - band_i * BAND_STAGGER) / BAND_SWEEP, 0, 1) * 1.15
            pm_rev = np.clip((prog - along + noise * 0.12) / 0.08, 0, 1)
            img = img * (1 - pm_rev[..., None]) + photo_np * pm_rev[..., None]

        frame = bg_frame.copy()
        frame.paste(Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
                    .resize((tw, target_h), Image.LANCZOS), (px_c, py_c))

        # slow push-in
        z = 1.0 + 0.045 * ease(t / DUR)
        vw, vh = W / z, H / z
        frame = frame.crop((int((W - vw) / 2), int((H - vh) / 2),
                            int((W + vw) / 2), int((H + vh) / 2))).resize((W, H), Image.LANCZOS)

        if t > DUR - FADEOUT:
            a = (t - (DUR - FADEOUT)) / FADEOUT
            frame = Image.blend(frame, Image.new("RGB", (W, H), BG), a)

        frame.save(frames_dir / f"f{i:04d}.png")

    # silent audio track (Kyle may add background music later)
    subprocess.run([
        "ffmpeg", "-y",
        "-framerate", str(FPS), "-i", str(frames_dir / "f%04d.png"),
        "-f", "lavfi", "-t", f"{DUR}",
        "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
        "-map", "0:v", "-map", "1:a", "-shortest",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        str(OUT)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    shutil.rmtree(frames_dir)
    print(f"opening → {OUT}  ({DUR}s, silent, stroke reveals)")


if __name__ == "__main__":
    main()
