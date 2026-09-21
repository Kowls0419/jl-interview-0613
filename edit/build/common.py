"""Shared build assets for the 新店礦業文化路徑 QR-tour videos.

Style: warm archival — near-black warm background, cream serif text (Songti TC),
amber accent. Cards are silent 1920x1080@24 MP4 sources for the EDL; photos
become full-frame Ken Burns overlay clips.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1920, 1080
FPS = 24

BG = (18, 15, 12)
CREAM = (236, 227, 209)
AMBER = (198, 150, 84)
DIM = (128, 119, 105)

SONGTI = "/System/Library/Fonts/Songti.ttc"
TC_BOLD = 2   # Songti TC Bold
TC_LIGHT = 5  # Songti TC Light


def font(size: int, bold: bool = True) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(SONGTI, size, index=TC_BOLD if bold else TC_LIGHT)


def _text_w(d: ImageDraw.ImageDraw, s: str, f: ImageFont.FreeTypeFont) -> float:
    box = d.textbbox((0, 0), s, font=f)
    return box[2] - box[0]


def _centered(d: ImageDraw.ImageDraw, y: int, s: str, f: ImageFont.FreeTypeFont,
              fill, tracking: int = 0) -> None:
    if tracking:
        widths = [_text_w(d, ch, f) + tracking for ch in s]
        total = sum(widths) - tracking
        x = (W - total) / 2
        for ch, w in zip(s, widths):
            d.text((x, y), ch, font=f, fill=fill)
            x += w
    else:
        d.text(((W - _text_w(d, s, f)) / 2, y), s, font=f, fill=fill)


def _fade_k(tt: float, dur: float, fade: float) -> float:
    """Eased (ease-in-out cubic) fade envelope in [0,1] at time tt.
    Linear fades read as 'clear steps' at 24fps on flat backgrounds; easing
    concentrates the change mid-ramp so the ends glide instead of stepping."""
    k = 1.0
    if tt < fade:
        k = ease_in_out_cubic(max(0.0, min(1.0, tt / fade)))
    rem = dur - tt
    if rem < fade:
        k = min(k, ease_in_out_cubic(max(0.0, min(1.0, rem / fade))))
    return k


def png_to_card_mp4(png: Path, out: Path, dur: float, fade: float = 0.55) -> None:
    """Static PNG -> silent 1920x1080@24 MP4 with an EASED fade baked to BG.

    Fades are baked per-frame in PIL (eased) rather than via ffmpeg's linear
    `fade` filter, so card in/out glides smoothly instead of stepping."""
    import shutil
    img = Image.open(png).convert("RGB")
    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)
    bg = Image.new("RGB", (W, H), BG)
    workdir = out.parent / f"_frames_{out.stem}"
    workdir.mkdir(parents=True, exist_ok=True)
    n = max(1, round(dur * FPS))
    for i in range(n):
        k = _fade_k(i / FPS, dur, fade)
        frame = img if k >= 0.999 else Image.blend(bg, img, k)
        frame.save(workdir / f"f{i:04d}.png")
    subprocess.run([
        "ffmpeg", "-y", "-framerate", str(FPS), "-i", str(workdir / "f%04d.png"),
        "-f", "lavfi", "-t", f"{dur:.3f}",
        "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
        "-map", "0:v", "-map", "1:a", "-shortest",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        str(out)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    shutil.rmtree(workdir)


def make_title_card(out_png: Path, kicker: str, title: str, sub: str,
                    sub2: str | None = None) -> None:
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    _centered(d, 300, kicker, font(40, bold=False), DIM, tracking=14)
    _centered(d, 400, title, font(150), CREAM, tracking=26)
    d.rectangle([W / 2 - 130, 630, W / 2 + 130, 633], fill=AMBER)
    _centered(d, 676, sub, font(42, bold=False), AMBER, tracking=10)
    if sub2:
        _centered(d, 756, sub2, font(32, bold=False), DIM, tracking=6)
    im.save(out_png)


def make_question_card(out_png: Path, question: str) -> None:
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    d.rectangle([W / 2 - 26, 388, W / 2 + 26, 391], fill=AMBER)
    _centered(d, 470, question, font(72), CREAM, tracking=10)
    im.save(out_png)


def _end_card_image(title: str, lines: list[tuple[str, str]]) -> Image.Image:
    """The end-card face as an image (shared by the static card and the
    animated credits+grid closer)."""
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    _centered(d, 300, "新店礦業文化路徑", font(40, bold=False), DIM, tracking=12)
    _centered(d, 388, title, font(92), CREAM, tracking=16)
    d.rectangle([W / 2 - 110, 560, W / 2 + 110, 562], fill=AMBER)
    # Credits were Songti TC Light 34 in DIM — light weight, small, and low
    # contrast on a near-black ground. Bold 42, with the NAME in CREAM and only
    # the role label held back, so the block reads at a glance and still reads
    # when the closer shrinks the card to 46% beside the 花絮 grid (42 * 0.46 ≈
    # 19px on screen, where 34 * 0.46 was ~16px).
    y = 620
    for label, value in lines:
        f = font(42)
        wl = _text_w(d, label, f) + 4 * len(label)
        wv = _text_w(d, value, f) + 4 * len(value)
        total = wl + 30 + wv
        assert total <= W - 160, f"credit line too wide for the card: {label} {value}"
        x = (W - total) / 2
        for s, colour in ((label, DIM), (value, CREAM)):
            for ch in s:
                d.text((x, y), ch, font=f, fill=colour)
                x += _text_w(d, ch, f) + 4
            x += 30 - 4
        y += 80
    assert y <= H - 60, f"credits block overflows the card ({y}px)"
    return im


def make_end_card(out_png: Path, title: str, lines: list[tuple[str, str]]) -> None:
    """lines: [(label, value), ...] rendered small under the title."""
    _end_card_image(title, lines).save(out_png)


def make_statement_card(out_png: Path, lines: list[str]) -> None:
    """1-2 line contemplative statement — amber rule above, cream serif,
    smaller than the question face. For scene-setting and closing thesis."""
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    d.rectangle([W / 2 - 26, 392, W / 2 + 26, 395], fill=AMBER)
    y = 474 if len(lines) > 1 else 500
    for ln in lines:
        _centered(d, y, ln, font(58), CREAM, tracking=8)
        y += 104
    im.save(out_png)


def ease_in_out_cubic(t: float) -> float:
    if t < 0.5:
        return 4 * t ** 3
    return 1 - (-2 * t + 2) ** 3 / 2


def ease_out_cubic(t: float) -> float:
    return 1 - (1 - t) ** 3


def _fit_cell(img: Image.Image, cw: int, ch: int) -> Image.Image:
    """Center-crop to the cell aspect, then resize — uniform grid tiles."""
    ar_c, ar_i = cw / ch, img.width / img.height
    if ar_i > ar_c:                      # too wide: crop sides
        nw = int(round(img.height * ar_c))
        left = (img.width - nw) // 2
        box = (left, 0, left + nw, img.height)
    else:                                # too tall: crop top/bottom
        nh = int(round(img.width / ar_c))
        top = (img.height - nh) // 2
        box = (0, top, img.width, top + nh)
    return img.resize((cw, ch), Image.LANCZOS, box=box)


def credits_grid_duration(n_tiles: int, *, has_clips: bool = False,
                          hold: float = 2.8, trans: float = 1.3,
                          stagger: float = 0.14, reveal: float = 0.55,
                          window: float = 5.5, tail: float = 1.4) -> float:
    """Duration of the animated closer, QUANTIZED TO WHOLE FRAMES.

    The build script needs this before it can lay out TIMELINE, and the value
    must match the rendered clip exactly or the EDL clips its tail — so both
    sides call this."""
    dur = (hold + trans * 0.55 + stagger * max(0, n_tiles - 1) + reveal
           + (window if has_clips else 0.0) + tail)
    return round(dur * FPS) / FPS


def _clip_tile_frames(src: Path, start: float, end: float, cw: int, ch: int,
                      window: float, workdir: Path) -> list[Image.Image]:
    """Decode one BTS clip into cell-sized frames, sped up to fit `window`.

    Clips longer than the window are time-compressed (setpts) so nothing is
    lost; shorter clips play at 1x and simply start later, holding their first
    frame — see the caller, which lands every tile's last frame together."""
    workdir.mkdir(parents=True, exist_ok=True)
    for old in workdir.glob("*.png"):
        old.unlink()
    dur = end - start
    speed = max(1.0, dur / window)          # >1 = faster; never slow a clip down
    subprocess.run([
        "ffmpeg", "-y", "-v", "error", "-ss", f"{start:.3f}", "-i", str(src),
        "-t", f"{dur:.3f}",
        "-vf", (f"setpts=PTS/{speed:.6f},"
                f"scale={cw}:{ch}:force_original_aspect_ratio=increase,"
                f"crop={cw}:{ch}"),
        "-r", str(FPS), "-an", str(workdir / "t%04d.png")],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    frames = [Image.open(p).convert("RGB")
              for p in sorted(workdir.glob("t*.png"))]
    if not frames:
        raise RuntimeError(f"no frames decoded from {src} {start}-{end}")
    return frames


def make_credits_grid_mp4(out_mp4: Path, title: str, lines: list[tuple[str, str]],
                          photos: list[Path],
                          clips: list[tuple[Path, float, float]] | None = None,
                          *, hold: float = 2.8,
                          trans: float = 1.3, stagger: float = 0.14,
                          reveal: float = 0.55, window: float = 5.5,
                          tail: float = 1.4, fade: float = 0.7,
                          cols: int | None = None,
                          workdir: Path | None = None) -> float:
    """Animated closer: the end card holds full-frame, then eases down to the
    LEFT while the behind-the-scenes material staggers in as a grid on the
    RIGHT. Stills sit as photos; `clips` become SILENT playing tiles, all
    landing their last frame together (Kyle, review r01 note 2).

    Returns the clip duration so the caller can put it in the TIMELINE.
    """
    import shutil

    clips = clips or []
    card = _end_card_image(title, lines)
    n_tiles = len(photos) + len(clips)
    if cols is None:
        cols = 3 if n_tiles <= 6 else 4
    rows = max(1, (n_tiles + cols - 1) // cols)

    # --- right-hand grid geometry ---
    # r01 note 1: the whole composition sits too far right — left margin was
    # ~290px against a 40px right margin. Shifted left so both are ~165px.
    GX, GW = 755, 1000                       # grid column: x 755..1755
    gap = 20
    cw = (GW - gap * (cols - 1)) // cols
    ch = int(round(cw * 3 / 4))              # uniform 4:3 tiles
    grid_h = rows * ch + gap * (rows - 1)
    GY = (H - grid_h) // 2

    def _place(i: int) -> tuple[int, int]:
        r, c = divmod(i, cols)
        in_row = min(cols, n_tiles - r * cols)      # centre a short last row
        pad = ((cols - in_row) * (cw + gap)) // 2
        return GX + pad + c * (cw + gap), GY + r * (ch + gap)

    def _tile(im: Image.Image) -> Image.Image:
        cell = Image.new("RGB", (cw, ch), CREAM)   # cream border
        cell.paste(im, (3, 3))
        return cell

    # Spread the clips evenly across the grid so the motion isn't clumped in
    # one row — with few clips a simple interleave puts them all up front.
    slots = set()
    if clips:
        for i in range(len(clips)):
            s = int(round((i + 0.5) * n_tiles / len(clips))) - 1
            while s in slots or not (0 <= s < n_tiles):
                s = (s + 1) % n_tiles
            slots.add(s)
    order: list[tuple[str, object]] = []
    ph_q, cl_q = list(photos), list(clips)
    for i in range(n_tiles):
        if i in slots and cl_q:
            order.append(("clip", cl_q.pop(0)))
        elif ph_q:
            order.append(("photo", ph_q.pop(0)))
        elif cl_q:
            order.append(("clip", cl_q.pop(0)))

    dur = credits_grid_duration(n_tiles, has_clips=bool(clips), hold=hold,
                                trans=trans, stagger=stagger, reveal=reveal,
                                window=window, tail=tail)
    reveal_end = hold + trans * 0.55 + stagger * max(0, n_tiles - 1) + reveal
    video_end = reveal_end + (window if clips else 0.0)

    workdir = workdir or out_mp4.parent / f"_frames_{out_mp4.stem}"
    workdir.mkdir(parents=True, exist_ok=True)

    tiles = []          # (kind, payload, x, y, start_frame)
    for i, (kind, payload) in enumerate(order):
        x, y = _place(i)
        if kind == "photo":
            im = _fit_cell(Image.open(payload).convert("RGB"), cw - 6, ch - 6)
            tiles.append(("photo", _tile(im), x, y, 0))
        else:
            src, a, b = payload
            frames = _clip_tile_frames(src, a, b, cw - 6, ch - 6, window,
                                       workdir / f"_clip{i}")
            # land every clip's LAST frame on video_end
            start_f = int(round((video_end - len(frames) / FPS) * FPS))
            tiles.append(("clip", [_tile(f) for f in frames], x, y, start_f))

    # --- card target transform (shrink toward the left column) ---
    # 0.46 keeps the credit lines legible on a phone; the card's text block is
    # centred and narrower than the frame, so it clears the grid at x=755.
    S = 0.46
    TX, TY = -109, (H - int(H * S)) // 2

    n = max(1, round(dur * FPS))

    for i in range(n):
        t = i / FPS
        canvas = Image.new("RGB", (W, H), BG)

        p = 0.0 if t <= hold else (
            1.0 if t >= hold + trans
            else ease_in_out_cubic((t - hold) / trans))
        s = 1.0 + (S - 1.0) * p
        cw2, ch2 = max(1, int(round(W * s))), max(1, int(round(H * s)))
        canvas.paste(card.resize((cw2, ch2), Image.LANCZOS),
                     (int(round(TX * p)), int(round(TY * p))))

        for idx, (kind, payload, cx, cy, start_f) in enumerate(tiles):
            t0 = hold + trans * 0.55 + idx * stagger
            k = ease_out_cubic(max(0.0, min(1.0, (t - t0) / reveal)))
            if k <= 0.001:
                continue
            if kind == "photo":
                cell = payload
            else:                                   # hold frame 0, then play
                j = min(max(0, i - start_f), len(payload) - 1)
                cell = payload[j]
            y = cy + int(round(26 * (1 - k)))        # slight upward slide
            region = canvas.crop((cx, y, cx + cell.width, y + cell.height))
            canvas.paste(Image.blend(region, cell, k), (cx, y))

        kf = _fade_k(t, dur, fade)
        if kf < 0.999:
            canvas = Image.blend(Image.new("RGB", (W, H), BG), canvas, kf)
        canvas.save(workdir / f"f{i:04d}.png")

    subprocess.run([
        "ffmpeg", "-y", "-framerate", str(FPS), "-i", str(workdir / "f%04d.png"),
        "-f", "lavfi", "-t", f"{dur:.3f}",
        "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
        "-map", "0:v", "-map", "1:a", "-shortest",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        str(out_mp4)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    shutil.rmtree(workdir)
    return dur


def make_photo_card(photo: Path, out_mp4: Path, dur: float,
                    zoom_from: float = 1.02, zoom_to: float = 1.07,
                    fade: float = 0.6, caption: str | None = None,
                    workdir: Path | None = None) -> None:
    """Photo -> full-frame OPAQUE 1920x1080@24 card (BG baked in): framed photo
    on warm-dark bg, cream border + soft shadow, slow zoom, eased fade to BG.
    Silent audio. Used for standalone slideshow beats (e.g. the 'today' close).

    When `caption` is set, a bottom band is reserved and the photo is centered
    ABOVE it, so the slow zoom never grows over the caption text."""
    import shutil
    workdir = workdir or out_mp4.parent / f"_frames_{out_mp4.stem}"
    workdir.mkdir(parents=True, exist_ok=True)

    ss = 1.25
    cw, ch = int(W * ss), int(H * ss)
    world = Image.new("RGB", (cw, ch), BG)
    ph = Image.open(photo).convert("RGB")
    # reserve a bottom band for the caption so the zoom never overlaps it
    cap_band = int(ch * 0.13) if caption else 0
    avail_h = ch - cap_band
    target_h = int(avail_h * 0.82)
    scale = target_h / ph.height
    tw = int(ph.width * scale)
    if tw > int(cw * 0.86):
        tw = int(cw * 0.86)
        target_h = int(ph.height * (tw / ph.width))
    ph = ph.resize((tw, target_h), Image.LANCZOS)
    px, py = (cw - tw) // 2, (avail_h - target_h) // 2
    border = 8
    sh = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rectangle(
        [px - border, py - border, px + tw + border, py + target_h + border],
        fill=(0, 0, 0, 150))
    sh = sh.filter(ImageFilter.GaussianBlur(26))
    world.paste(Image.new("RGB", (cw, ch), BG), (16, 20), sh)
    ImageDraw.Draw(world).rectangle(
        [px - border, py - border, px + tw + border, py + target_h + border],
        fill=(226, 216, 196))
    world.paste(ph, (px, py))

    bg = Image.new("RGB", (W, H), BG)
    n = max(1, round(dur * FPS))
    for i in range(n):
        t = i / max(1, n - 1)
        z = zoom_from + (zoom_to - zoom_from) * ease_in_out_cubic(t)
        vw, vh = cw / z, ch / z
        x0, y0 = (cw - vw) / 2, (ch - vh) / 2
        frame = world.crop((int(x0), int(y0), int(x0 + vw), int(y0 + vh))).resize((W, H), Image.LANCZOS)
        if caption:
            d = ImageDraw.Draw(frame)
            _centered(d, H - 92, caption, font(34, bold=False), CREAM, tracking=6)
        k = _fade_k(i / FPS, dur, fade)
        if k < 0.999:
            frame = Image.blend(bg, frame, k)
        frame.save(workdir / f"f{i:04d}.png")

    subprocess.run([
        "ffmpeg", "-y", "-framerate", str(FPS), "-i", str(workdir / "f%04d.png"),
        "-f", "lavfi", "-t", f"{dur}", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
        "-map", "0:v", "-map", "1:a", "-shortest",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        str(out_mp4)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    shutil.rmtree(workdir)


def _framed(im: Image.Image, world: Image.Image, x: int, y: int,
            border: int = 8) -> None:
    """Paste `im` onto `world` at (x,y) with the house cream border + soft
    shadow — the same treatment make_photo_card gives its single photo."""
    cw, ch = world.size
    sh = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rectangle(
        [x - border, y - border, x + im.width + border, y + im.height + border],
        fill=(0, 0, 0, 150))
    sh = sh.filter(ImageFilter.GaussianBlur(26))
    world.paste(Image.new("RGB", (cw, ch), BG), (12, 16), sh)
    ImageDraw.Draw(world).rectangle(
        [x - border, y - border, x + im.width + border, y + im.height + border],
        fill=(226, 216, 196))
    world.paste(im, (x, y))


def _encode_card(workdir: Path, out_mp4: Path, dur: float) -> None:
    import shutil
    subprocess.run([
        "ffmpeg", "-y", "-framerate", str(FPS), "-i", str(workdir / "f%04d.png"),
        "-f", "lavfi", "-t", f"{dur:.3f}",
        "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
        "-map", "0:v", "-map", "1:a", "-shortest",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        str(out_mp4)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    shutil.rmtree(workdir)


def make_photo_grid_card(photos: list[Path], out_mp4: Path, dur: float,
                         caption: str | None = None, zoom_from: float = 1.0,
                         zoom_to: float = 1.03, fade: float = 0.6,
                         gap: int = 26, workdir: Path | None = None) -> None:
    """Several photos in one row -> full-frame 1920x1080@24 card in the same
    language as make_photo_card (cream border, soft shadow, slow synchronized
    zoom, caption band at the bottom). Silent audio."""
    workdir = workdir or out_mp4.parent / f"_frames_{out_mp4.stem}"
    workdir.mkdir(parents=True, exist_ok=True)

    ss = 1.25
    cw, ch = int(W * ss), int(H * ss)
    world = Image.new("RGB", (cw, ch), BG)

    cap_band = int(ch * 0.13) if caption else 0
    avail_h = ch - cap_band
    n_ph = len(photos)
    max_w = int(cw * 0.88) - gap * (n_ph - 1)
    ims = [Image.open(p).convert("RGB") for p in photos]

    # one shared height so the row reads as a set; then clamp to the width budget
    target_h = int(avail_h * 0.74)
    while True:
        widths = [int(im.width * (target_h / im.height)) for im in ims]
        if sum(widths) <= max_w or target_h < 80:
            break
        target_h = int(target_h * 0.97)
    ims = [im.resize((w, target_h), Image.LANCZOS) for im, w in zip(ims, widths)]

    total_w = sum(widths) + gap * (n_ph - 1)
    x = (cw - total_w) // 2
    y = (avail_h - target_h) // 2
    for im in ims:
        _framed(im, world, x, y)
        x += im.width + gap

    bg = Image.new("RGB", (W, H), BG)
    n = max(1, round(dur * FPS))
    for i in range(n):
        t = i / max(1, n - 1)
        z = zoom_from + (zoom_to - zoom_from) * ease_in_out_cubic(t)
        vw, vh = cw / z, ch / z
        x0, y0 = (cw - vw) / 2, (ch - vh) / 2
        frame = world.crop((int(x0), int(y0), int(x0 + vw),
                            int(y0 + vh))).resize((W, H), Image.LANCZOS)
        if caption:
            _centered(ImageDraw.Draw(frame), H - 92, caption,
                      font(34, bold=False), CREAM, tracking=6)
        k = _fade_k(i / FPS, dur, fade)
        if k < 0.999:
            frame = Image.blend(bg, frame, k)
        frame.save(workdir / f"f{i:04d}.png")
    _encode_card(workdir, out_mp4, dur)


def make_clip_photo_card(clip: Path, clip_a: float, clip_b: float, photo: Path,
                         out_mp4: Path, dur: float, caption: str | None = None,
                         fade: float = 0.6, gap: int = 30,
                         clip_first: bool = True,
                         workdir: Path | None = None) -> None:
    """A time-lapsed CLIP beside a still PHOTO -> full-frame 1920x1080@24 card,
    both framed in the house style with a caption band. The clip is compressed
    to fill `dur` (so a 40s walk becomes a ~6s timelapse) and plays silently."""
    workdir = workdir or out_mp4.parent / f"_frames_{out_mp4.stem}"
    workdir.mkdir(parents=True, exist_ok=True)
    n = max(1, round(dur * FPS))

    cap_band = int(H * 0.13) if caption else 0
    avail_h = H - cap_band
    target_h = int(avail_h * 0.80)

    # decode the clip, sped up so its whole length lands in `dur`
    src_dur = clip_b - clip_a
    speed = src_dur / dur
    cdir = workdir / "_clip"
    cdir.mkdir(exist_ok=True)
    subprocess.run([
        "ffmpeg", "-y", "-v", "error", "-ss", f"{clip_a:.3f}", "-i", str(clip),
        "-t", f"{src_dur:.3f}",
        "-vf", f"setpts=PTS/{speed:.6f},scale=-2:{target_h}",
        "-r", str(FPS), "-an", str(cdir / "c%04d.png")],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    cframes = [Image.open(p).convert("RGB") for p in sorted(cdir.glob("c*.png"))]
    if not cframes:
        raise RuntimeError(f"no frames decoded from {clip}")
    cw_ = cframes[0].width

    ph = Image.open(photo).convert("RGB")
    pw = int(ph.width * (target_h / ph.height))
    budget = int(W * 0.88) - gap - cw_
    if pw > budget:                      # keep the pair inside the frame
        pw = budget
        ph = ph.resize((pw, int(ph.height * (pw / ph.width))), Image.LANCZOS)
        ph = _fit_cell(ph, pw, target_h)
    else:
        ph = ph.resize((pw, target_h), Image.LANCZOS)

    total_w = cw_ + gap + pw
    x_left = (W - total_w) // 2
    y = (avail_h - target_h) // 2
    cx, px = (x_left, x_left + cw_ + gap) if clip_first else (x_left + pw + gap, x_left)

    bg = Image.new("RGB", (W, H), BG)
    for i in range(n):
        frame = Image.new("RGB", (W, H), BG)
        _framed(ph, frame, px, y)
        _framed(cframes[min(i, len(cframes) - 1)], frame, cx, y)
        if caption:
            _centered(ImageDraw.Draw(frame), H - 92, caption,
                      font(34, bold=False), CREAM, tracking=6)
        k = _fade_k(i / FPS, dur, fade)
        if k < 0.999:
            frame = Image.blend(bg, frame, k)
        frame.save(workdir / f"f{i:04d}.png")
    _encode_card(workdir, out_mp4, dur)


def make_photo_pair_card(photo_l: Path, photo_r: Path, out_mp4: Path, dur: float,
                         zoom_from: float = 1.0, zoom_to: float = 1.035,
                         fade: float = 0.6, blur_bg: bool = False,
                         workdir: Path | None = None) -> None:
    """Two photos side-by-side -> full-frame 1920x1080@24 card, each framed with
    cream border + soft shadow, a subtle synchronized zoom on the whole diptych,
    eased fade. Silent audio.

    blur_bg=True fills the frame with a blurred, darkened cover of each photo (left
    photo behind the left half, right behind the right) instead of the flat warm-dark
    bg — matches the make_kenburns cover look. Used for the 花絮 ending."""
    import shutil
    from PIL import ImageOps
    workdir = workdir or out_mp4.parent / f"_frames_{out_mp4.stem}"
    workdir.mkdir(parents=True, exist_ok=True)

    ss = 1.15
    cw, ch = int(W * ss), int(H * ss)
    world = Image.new("RGB", (cw, ch), BG)
    if blur_bg:
        hw = cw // 2
        for idx, photo in enumerate((photo_l, photo_r)):
            ph = ImageOps.exif_transpose(Image.open(photo).convert("RGB"))
            s2 = max(hw / ph.width, ch / ph.height)
            pr = ph.resize((int(ph.width * s2) + 2, int(ph.height * s2) + 2), Image.LANCZOS)
            cx = (pr.width - hw) // 2
            cy = (pr.height - ch) // 2
            pr = pr.crop((cx, cy, cx + hw, cy + ch)).filter(ImageFilter.GaussianBlur(34))
            pr = Image.eval(pr, lambda v: int(v * 0.42 + BG[0] * 0.20))
            world.paste(pr, (idx * hw, 0))
    margin = int(cw * 0.045)
    gap = int(cw * 0.03)
    cell_w = (cw - 2 * margin - gap) // 2
    cell_h = int(ch * 0.74)
    cyy = (ch - cell_h) // 2
    for idx, photo in enumerate((photo_l, photo_r)):
        ph = ImageOps.exif_transpose(Image.open(photo).convert("RGB"))
        s = min(cell_w / ph.width, cell_h / ph.height)
        tw, th = int(ph.width * s), int(ph.height * s)
        ph = ph.resize((tw, th), Image.LANCZOS)
        cell_x = margin + idx * (cell_w + gap)
        px = cell_x + (cell_w - tw) // 2
        py = cyy + (cell_h - th) // 2
        border = 7
        sh = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
        ImageDraw.Draw(sh).rectangle(
            [px - border, py - border, px + tw + border, py + th + border],
            fill=(0, 0, 0, 150))
        sh = sh.filter(ImageFilter.GaussianBlur(22))
        world.paste((0, 0, 0), (12, 16), sh)
        ImageDraw.Draw(world).rectangle(
            [px - border, py - border, px + tw + border, py + th + border],
            fill=(226, 216, 196))
        world.paste(ph, (px, py))

    bg = Image.new("RGB", (W, H), BG)
    n = max(1, round(dur * FPS))
    for i in range(n):
        t = i / max(1, n - 1)
        z = zoom_from + (zoom_to - zoom_from) * ease_in_out_cubic(t)
        vw, vh = cw / z, ch / z
        x0, y0 = (cw - vw) / 2, (ch - vh) / 2
        frame = world.crop((int(x0), int(y0), int(x0 + vw), int(y0 + vh))).resize((W, H), Image.LANCZOS)
        k = _fade_k(i / FPS, dur, fade)
        if k < 0.999:
            frame = Image.blend(bg, frame, k)
        frame.save(workdir / f"f{i:04d}.png")

    subprocess.run([
        "ffmpeg", "-y", "-framerate", str(FPS), "-i", str(workdir / "f%04d.png"),
        "-f", "lavfi", "-t", f"{dur}", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
        "-map", "0:v", "-map", "1:a", "-shortest",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        str(out_mp4)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    shutil.rmtree(workdir)


def make_kenburns(photo: Path, out_mov: Path, dur: float,
                  zoom_from: float = 1.03, zoom_to: float = 1.10,
                  fade: float = 0.6, cover: bool = False,
                  workdir: Path | None = None) -> None:
    """Photo -> full-frame 1920x1080@24 overlay clip WITH ALPHA (ProRes 4444):
    photo + cream border + soft shadow on transparent bg, slow ease zoom,
    alpha fades at both ends so it crossfades over the footage.

    cover=True fills the whole frame with a blurred, darkened cover of the same
    photo (opaque) behind the framed photo — hides footage under the margins
    (e.g. an interviewer who walks into shot). Reads as an intentional look."""
    import shutil
    workdir = workdir or out_mov.parent / f"_frames_{out_mov.stem}"
    workdir.mkdir(parents=True, exist_ok=True)

    # Build oversized world canvas once, then crop/zoom per frame.
    ss = 1.25  # supersample so zoom crops never upsample
    cw, ch = int(W * ss), int(H * ss)
    world = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))

    ph = Image.open(photo).convert("RGB")

    if cover:
        # blurred, darkened cover fill (opaque) so no footage shows at margins
        cov = ph.copy()
        cs = max(cw / cov.width, ch / cov.height)
        cov = cov.resize((int(cov.width * cs) + 2, int(cov.height * cs) + 2), Image.LANCZOS)
        cx = (cov.width - cw) // 2
        cy = (cov.height - ch) // 2
        cov = cov.crop((cx, cy, cx + cw, cy + ch)).filter(ImageFilter.GaussianBlur(34))
        cov = Image.eval(cov, lambda v: int(v * 0.42 + BG[0] * 0.20))
        world.paste(cov.convert("RGBA"), (0, 0))

    target_h = int(ch * 0.84)
    scale = target_h / ph.height
    tw = int(ph.width * scale)
    if tw > int(cw * 0.90):
        tw = int(cw * 0.90)
        target_h = int(ph.height * (tw / ph.width))
    ph = ph.resize((tw, target_h), Image.LANCZOS)

    px, py = (cw - tw) // 2, (ch - target_h) // 2
    border = 8

    # soft shadow (semi-transparent, blurs over the footage)
    sh = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rectangle(
        [px - border, py - border, px + tw + border, py + target_h + border],
        fill=(0, 0, 0, 150))
    sh = sh.filter(ImageFilter.GaussianBlur(26))
    world.alpha_composite(sh, (16, 20))
    ImageDraw.Draw(world).rectangle(
        [px - border, py - border, px + tw + border, py + target_h + border],
        fill=(226, 216, 196, 255))
    world.paste(ph, (px, py))

    n = max(1, round(dur * FPS))
    for i in range(n):
        t = i / max(1, n - 1)
        z = zoom_from + (zoom_to - zoom_from) * ease_in_out_cubic(t)
        vw, vh = cw / z, ch / z
        x0 = (cw - vw) / 2
        y0 = (ch - vh) / 2
        frame = world.crop((int(x0), int(y0), int(x0 + vw), int(y0 + vh)))
        frame = frame.resize((W, H), Image.LANCZOS)
        # eased alpha crossfade (smoothstep) — glides over footage instead of
        # the stepped look a linear alpha ramp gives at 24fps.
        k = _fade_k(i / FPS, dur, fade)
        if k < 1.0:
            r, g, b, a = frame.split()
            a = a.point(lambda v: int(v * k))
            frame = Image.merge("RGBA", (r, g, b, a))
        frame.save(workdir / f"f{i:04d}.png")

    subprocess.run([
        "ffmpeg", "-y", "-framerate", str(FPS), "-i", str(workdir / "f%04d.png"),
        "-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le",
        str(out_mov)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    shutil.rmtree(workdir)
