# Worklog — Kyle review round 2 (2026-07-08)
Status legend: [ ] todo  [~] in progress  [x] done  [!] blocked/needs Kyle

## Decisions locked
- Vid 3 opening = C (scene-setting text card before hook)
- Vid 3 ending = A (closing text card before credits, 期望的未來 thesis)

## Tasks (ordered; do sequentially, log after EACH render)
### Video 1 (光陰/和美, folder 2 photos)
- [x] T1.1 2-16 & 2-17 are near-duplicates → keep one, replace/drop other
- [x] T1.R render + burn + verify + update product symlink (auto)

### Video 2 (環境/振山, folder 1 photos, cropped proxy)
- [x] T2.1 1-4 is Xindian ELEMENTARY SCHOOL photo, not "go out to play" → remove from zoo block
- [x] T2.2 1-13 is FAMILY not train → remove from vid2 (belongs to vid3 idea)
- [x] T2.3 ending 1-14 & 1-9: no rapid face<->image bounce. Show image(s) right AFTER
        question card, then END on speaker face. (restructure q6ans overlay timing)
- [x] T2.R render + burn + verify + update product

### Video 3 (期望/過水橋, folder 3 photos)
- [x] T3.1 opening C: scene text card before hook
- [x] T3.2 ending A: closing thesis text card before credits
- [x] T3.3 remove 3-6 (unclear floor plan)
- [x] T3.4 3-12 (round window) & 3-13 (piano) ONLY during house-living segment (home)
- [x] T3.5 3-17 = wedding-procession bridge; 3-7 = bridge today (context ok, keep in typhoon? re-check fit)
- [x] T3.6 3-3 & 3-1 near-duplicate → keep one
- [x] T3.7 3-8 (modern canal) show LATER / it's not that clean → move toward end
- [x] T3.R render + burn + verify + update product

### Video 4 (花絮, folder 4)
- [x] T4.1 inventory 4/new/ additional BTS photos
- [x] T4.2 add best new photos to montage/coda
- [x] T4.R render + burn + verify + update product

### Finalize
- [x] TF regenerate photo_table.html + republish artifact
- [x] TF project.md session log

## Round 3 (2026-07-09) — folder-4 media revision
Kyle removed IMG_6444 (was folder-4 #22) and IMG_6446 from 4/new; utilize all remaining.
- [x] R3.1 drop #22 from vid4 overlays
- [x] R3.2 rebuild bts_mov.mp4 proxy from IMG_6450.MOV (blurred pillarbox, 24fps)
- [x] R3.3 add live MOV segment (bts_live, out 49.3-56.8s) + redistribute stills
        rehearsal[3,4,23] look_at_lens[7,25] coda[9,2,20,21,24] one_at_a_time[6]
- [x] R3.4 render huaxu_preview (1:18) + burn subs + verify frames (hx2.png clean)
- [x] R3.5 update product symlink (auto), WORKLOG + project.md

## Round 4 (2026-07-09) — captions, bridge photos, smoother fades
- [x] R4.1 [vid3] today_bridge/today_canal: photo zoom was growing over caption →
        make_photo_card reserves a bottom caption band (0.13*ch), photo centered above.
        Verified sp3_grid.png: captions clear below frame.
- [x] R4.2 [vid3] 3-10 + 3-17 grouped on hook (bridge talk) as a pair; 3-17 removed
        from typhoon (now footage). Both are 過橋 images. Verified frames 21/25.
- [x] R4.3 [ALL] smoother fades: make_kenburns eased (ease-in-out cubic) alpha ramp
        + 0.5→0.6s; png_to_card_mp4 + make_photo_card baked eased fades in PIL (blend
        toward warm BG) instead of ffmpeg linear fade. Removes the "clear steps."
        NOTE: card↔card still dips through BG (concat -c copy); a true card-to-card
        cross-dissolve would need render.py xfade work — flagged, not done.
- [x] R4.4 [vid2] removed 1-4 (Xindian-elementary class photo) from zoo/"went out to
        play"; zoo now footage-only.
- [x] R4.5 rebuild all 4 (cleared kb_* caches so eased fades regenerate) + burn + verify.
        1:2:49.8  2:2:36.1  3:3:40.8  4:1:18.3. product symlinks auto-updated.

## Round 5 (2026-07-09/10) — retitle + fine notes (NEW numbering V1..4)
V1=光陰/過水橋(shengping) V2=環境/和美(hemei) V3=期望/振山(zhenshan) V4=花絮(huaxu)
- [x] R5.0 re-pair poetic titles↔content + renumber product (Session 8, done earlier)
- [x] R5.1 [V1 shengping] 1:38 dad photo started over q4 CARD → delta -0.3→0.25 (starts
        on footage); pdur 4.4→3.8. Verified pic over footage.
- [x] R5.2 [V1 shengping] 2:00 home cover reverted ~1s to footage before q6 card →
        delta -0.3→0.0, pdur 8.2→8.5 so last cover dissolves INTO q6 card (no revert).
- [x] R5.3 [V2 hemei] SUB_FIXES: 電氣師傅→電器師傅, 聯絡→聯繫. Re-burned from existing
        nosub (no re-render needed — text-only). Verified in srt.
- [x] R5.4 [V3 zhenshan] SUB_FIX 追著上→追的上 (2:09-10). q6ans delta 0.2→-0.4 so the
        q6 card dissolves straight into the pic (no footage flash at 2:20). Verified.
- [x] R5.5 [V4 huaxu] MOV in 0.15→0.70 (skips ~0.5s repeated cut_ok tail audio @0:50);
        coda: replaced 16s one-at-a-time overlay montage with 3 side-by-side DIPTYCH
        cards (9|2, 20|21, 24|8) via new common.make_photo_pair_card → 1:18→1:12.5.
- [x] R5.6 re-render V1/V3/V4 + reburn V2 + verify grid. product auto-updated.
        1:3:40.8  2:2:49.8  3:2:36.1  4:1:12.5.

## Round 6 (2026-07-10) — sync fix + missed 坪
- [x] R6.1 product/ was SYMLINKS → Google Drive doesn't sync symlinks (Kyle saw stale).
        Replaced with REAL FILE COPIES; added edit/build/sync_product.sh; updated the
        PRODUCT FOLDER RULE in project.md. Copy after every render from now on.
- [x] R6.2 Verified via frames pulled from the PRODUCT files that R5 fixes ARE present
        (V1 1:38 card-only, V1 2:00 cover→card, V3 2:20 pic-direct). Kyle was viewing a
        pre-R5 synced copy — a Drive propagation lag, not a render miss.
- [x] R6.3 NEW note caught: V1 @1:49 subtitle 平→坪 (大宅院面積). SUB_FIXES 百平→百坪,
        千平→千坪. Re-burned shengping from existing nosub (text-only). Verified 兩千坪 in
        product file. Re-synced all 4 product copies.
VERSION FINGERPRINTS (to tell new build from old on a synced device):
  V4=1:16 & ends with FOUR side-by-side photo pairs (old=1:18/0:55 one-at-a-time)
  V1 title=光陰的故事 & @1:49 says 兩千坪 (old title=期望的未來, old sub=兩千平)

## Round 7 (2026-07-10) — LOUDNORM audio bug + transition polish
- [x] R7.1 ROOT CAUSE of V4 0:50 "repeat" + V1 2:00 "cut sound" = render loudnorm pass
        bleeding audio into silent gaps. Proven: --no-loudnorm → MOV -91dB silent; with
        loudnorm → -18.5dB. FIX: all previews render --no-loudnorm (rebuild_*.sh). Also
        muted MOV proxy (bts_mov_silent.mp4). Verified V4 waveform flat after cut.
- [x] R7.2 V1 dad → COVER (blur-bg, "just pic"); home cover tightened both ends (delta
        -0.6, pdur 8.7 → card↔cover, no footage peek); school framed delta 0.5→1.0.
- [x] R7.3 V3 q6ans framed delta -0.4→1.0 (card → ~1s footage → pic). Verified frames.
- [x] R7.4 V4 overlays: rehearsal [23,3], look_at_lens [7]; 4 & 25 → new coda4 diptych.
- [x] R7.5 re-rendered ALL 4 no-loudnorm + synced product copies + verified.
        V1 3:40.8  V2 2:49.7  V3 2:36.1  V4 1:16.3.
NEW FINGERPRINT: all 4 now have clean silence in card gaps (no faint audio swell/bleed).

## Round 8 (2026-07-10) — image→card flash rule + V4 overlay-on-footage
Diagnostic (scratchpad/diag3.py) checked every framed overlay's card margins:
V2 & V3 had NO exit<1s violations → already compliant, left untouched (saved renders).
- [x] R8.1 [V1] hook 3-17 ended EXACTLY at q1 card (0.0s) = the flash. Fixed: framed
        anchor hook_a start, delta 1.0, pdur 3.9 → ~1s footage each side of the pics.
        school 3-4 exit 0.82→1.2s (pdur 9.5→9.3). RULE: framed overlays need ≥1s footage
        before the pic AND ≥1s after (never touch a card); short/mostly-pic → cover.
- [x] R8.2 [V4] Kyle: overlays ON playing footage, no standalone pic cards, dedupe.
        Removed the 4 diptych coda cards + make_photo_pair_card usage. All stills now
        framed overlays on footage: rehearsal [23,8,20,21], one_at_a_time [6],
        look_at_lens [7], bts_live(MOV) [9,2] finale. Dropped near-dupes 3,4,5,10,24,25,1.
        1:16 → 1:02.
- [x] R8.3 rendered V1+V4, synced product. V1 3:40.8 V2 2:49.7 V3 2:36.1 V4 1:02.3.
FINGERPRINT update: V4 now 1:02 & ends on the live clip with the group photo overlaid
(no side-by-side pair cards anymore).

## Round 9 (2026-07-10) — cover→card flash (drift) + V4 blur ending / no subs
- [x] R9.1 [V1] cover→question-card flash CONFIRMED via frame-by-frame (homecut.png):
        cover faded out and revealed the red home footage BEFORE the q6 card. ROOT CAUSE:
        accumulated 24fps frame-rounding drift between nominal overlay start_in_output and
        the concatenated base (~0.14s) — the cover's baked fade-out landed over footage,
        not the card. FIX: extend the cover tails so they stay fully opaque ~1s INTO the
        card (dad pdur 5.1→5.8, home 8.7→9.1); fade-out then happens well inside the card,
        drift-proof. Verified homecut2.png: opaque across the whole cut, card still reads.
        (Only dad & home covers hit a card; canal_a → footage, fine.)
- [x] R9.2 [V4] ending: removed the live MOV clip; 9 & 2 now a blur-bg side-by-side
        diptych ENDING card (make_photo_pair_card blur_bg=True added to common.py).
- [x] R9.3 [V4] REMOVED subtitles — grade-only burn (no subtitles filter). 0:59.
- [x] R9.4 synced product. V1 3:40.8  V2 2:49.7  V3 2:36.1  V4 0:59.2.
DRIFT NOTE (reusable): framed overlays tolerate ~0.15s drift (footage both sides); COVER
overlays bridging a footage→card cut do NOT — always end a cover ≥~1s past the card start.


---

# 2026-08-18 — 海報 4：陳外科醫院（Dots Global 紀錄片）

> Intended as a section of `edit/WORKLOG.md`. It lives in its own file because
> mid-session the sandbox lost access to pre-existing files under this Google
> Drive path — new files could be created, but `WORKLOG.md` could not be opened
> even for append. Paste this in and delete the file when convenient.

Fourth A4 QR poster, joining the three 新店礦業文化路徑 sheets. A different
production (Dots Global, © 2026), same visual identity.

**Status: poster 4 is DONE and delivered. Posters 1–3 are NOT yet rebuilt** and
still carry the old credit block, so the set is currently inconsistent. See
*Open* below — the change is staged and one command away.

---

## Source material

- **Site** — https://ccthospital.dotsglobal.co/ — a single page, no nav, no
  subpages. Full inventory: hero banner (陳外科醫院 / Since 1958), the embedded
  film, a bilingual ZH/EN synopsis, `founders-lin.jpg` (林秀卿 & 林蔡美玉, 1950s),
  `founders-chen.jpg` (陳昌梯醫師 & 陳林彩薇), a full-width title plate, footer
  © 2026 Dots Global. Only outbound links go to dotsglobal.co.
- **Film** — https://youtu.be/UVZ8Esm8AZA — 3:53, channel Dots Global, uploaded
  2026-02-15, burned-in ZH+EN subtitles. Same video the site embeds.

## Build

- **New:** `edit/build/make_poster_cct.py`. Imports the palette (including
  `QRINK`), the Songti helpers, `centred()` and `qr_image()` from
  `make_posters.py`, so the sheets share one source of truth for colour.
- Kept as a separate script rather than a fourth entry in `SITES` because this
  one needs its own kicker, its own credit block, and a corner QR pointing at
  the film's own site instead of the series playlist. Folding three overrides
  into the series script would have made it worse, not shorter.
- Layout is the series grid unchanged: hairline frame → kicker → 158px title →
  amber rule → amber sub → 1450×816 picture box → 3-line blurb → QR box →
  掃描觀看 → duration line → credit rule → credits → corner QR.

## Content

| | |
|---|---|
| Kicker | 新北市的第一所醫院 |
| Title | 陳外科醫院 |
| Sub | 光明街　Since 1958 |
| Duration line | 影片長度 3:53　·　中英文字幕 |

- **Picture** — `exports/thumbnails/_banner_cct.jpg`, the site's own hero banner
  (2400×749). Centre-cropped to 16:9 in-script by `_crop_169()` rather than
  squeezed; the crop keeps the whole title block, since the lettering and both
  illustrations sit inside the middle ~1331px of the source.
  - Superseded an earlier choice: a frame from the film at 49.6s (the 陳外科醫院
    shopfront with the red cross), cropped `1600:900:160:0` to drop the burned-in
    subtitle band. Kept on disk as `exports/thumbnails/_still_cct.png` in case
    the banner is ever reverted.
- **Blurb** — three lines condensed from the site's own synopsis, same voice.
- **Credits** — 製作 Dots Global / 專題網站 ccthospital.dotsglobal.co / 版權
  © 2026 Dots Global. Deliberately thin: neither the film nor the site carries a
  credit card, so no 攝影 / 後製剪輯 / 指導單位 line was invented.
- **QR codes** — big one → the video; corner one → the site, labelled 專題網站
  (where the series puts the playlist).

## Unifying the set — boxes and colour

Kyle spotted slight differences across the four. Verified mechanically rather
than by eye: rendered a series sheet and this one from the same code, dumped the
lossless pre-PDF bitmaps, and diffed every long run of `LINE` / `AMBER` plus the
exact palette in use. Checker kept at `edit/build/check_unity.py`.

**The PDF's JPEG encoding destroys exact colour** — the first attempt at this
compared rasterised PDFs and found nothing, because every flat area had been
dithered. Comparing the bitmaps *before* PDF encoding is what surfaced the bugs.

Two real defects found and fixed:

1. **Corner QR box was 23px smaller than the other three.** `qr_image()` sizes a
   code as (modules + quiet zone) × an *integer* scale, so rendered size depends
   on URL length. The series playlist URL (50 chars) lands on QR version 6 →
   392px; this poster's site URL (34 chars) lands on version 4 → 369px. Fixed by
   `_pin()`, which centres a code on a PAPER square of the series' exact size —
   padding only widens the quiet zone, so it still scans. Both codes are now
   pinned (`SERIES_QR_MAIN = 574`, `SERIES_QR_CORNER = 392`).
2. **SVG QR used a hardcoded ink value** `(26, 21, 16)` instead of the shared
   `QRINK`. Same value today, but a drift waiting to happen. Now imported.

After the fix all nine chrome bands — frame top/bottom, picture box top/bottom,
QR box top/bottom, credit rule, corner QR box top/bottom — land on identical
pixel rows, and both pages use exactly the same six palette colours.

## Credit legibility — all four sheets

Same fix Kyle made on the videos' end cards (修正前 / 修正後): the credits were
small AND entirely MUTED, so they read as grey mush. Two changes:

- **Bigger** — 40px → 48px, line step 60 → 66.
- **The value carries the contrast, the label stays quiet.** On the dark video
  card the name goes brighter than the label; inverted for white paper that
  means the name drops to `INK` while the label stays `MUTED`. The label is
  signposting ("攝影"); the name is the information.

Rendering moved into a **new shared module `edit/build/poster_credits.py`** that
both scripts import, so the four sheets cannot drift on this the way the corner
QR did.

Sizing was capped by the series sheets' FIVE credit lines. At 48/72 the last
line's ink landed 17px off the frame at y=3313 — ~1.4mm, too tight to print.
**The overflow `assert` passed anyway**, because it tests the flowed `y`, not
where glyphs actually end; caught only by measuring ink directly. Settled on
step 66 plus pulling the block up (pre-rule gap 92 → 74):

| sheet | credit ink ends | clearance to frame (y=3313) |
|---|---|---|
| series, 5 lines | 3254 | 59px |
| poster 4, 3 lines | 3121 | 192px |

Unity re-verified after the change: all nine chrome bands still identical.

## Verification performed

- Both QR codes decoded off the **delivered PDF** at 300dpi (not just the
  pre-encode bitmap): `https://youtu.be/UVZ8Esm8AZA` and
  `https://ccthospital.dotsglobal.co/`.
- `check_unity.py`: 9/9 LINE bands identical, palette identical. The AMBER
  section shows differences by design — those are subtitle glyphs
  (和美煤礦 vs 光明街　Since 1958), not box geometry.
- Credit ink clearance measured on a real 5-line render, not inferred.
- `exports/print/` and `exports/QR Code Posters/` copies confirmed
  **pixel-identical** to the final build. Their md5s differ only because PIL
  stamps a PDF creation date — content is byte-for-byte equivalent once
  rasterised.

## Output

| file | |
|---|---|
| `exports/print/4_陳外科醫院_光明街_A4.pdf` | the poster |
| `exports/print/4_陳外科醫院_光明街_QR.svg` | bare video QR |
| `exports/QR Code Posters/4_陳外科醫院_光明街_A4.pdf` | copy alongside 1–3 |
| `exports/thumbnails/_banner_cct.jpg` | picture source |
| `exports/thumbnails/_still_cct.png` | superseded film still |
| `edit/build/make_poster_cct.py` | build script |
| `edit/build/poster_credits.py` | shared credit block (all four) |
| `edit/build/make_posters.NEW.py` | drop-in to rebuild 1–3 |
| `edit/build/check_unity.py` | geometry/colour checker |

## Open

- **REBUILD 1–3.** They still have the old small grey credits. Staged and ready:

      cp edit/build/make_posters.py edit/build/make_posters.BAK.py
      cp edit/build/make_posters.NEW.py edit/build/make_posters.py
      .venv python edit/build/make_posters.py edit/urls.json

  Could not be run here: `make_posters.py` was unwritable and the three stills
  (`_still_shengping/hemei/zhenshan.png`) unreadable. The new code was proven
  against a real 5-line sheet using a stand-in still, so the layout is verified;
  only the actual photos were missing. There is **no `.venv` in the project**
  despite the docstring referencing one — deps are segno, pillow,
  opencv-python-headless, numpy.
- **Re-upload after rebuilding.** The three poster PDFs are live on Drive via
  the links in `exports/分享訊息.txt`.
- **Ask the film's producers for the real credits** (director, camera, 指導單位). If they exist,
  add them to `CREDITS` in `make_poster_cct.py` and rerun.
- **The banner repeats the poster's own type** — it carries 新北市的第一所醫院 and
  陳外科醫院, which the sheet already sets as kicker and 158px title. Unified
  geometry was the priority so the series structure was kept and the repeat left
  in. Alternatives: drop the kicker/title and let the banner be the header, or
  go back to `_still_cct.png`.
- **Sub line is mixed-script.** 光明街　Since 1958 runs ~628px against the other
  three sheets' short CJK subs (和美煤礦, ~260px). Trimming to just 光明街 would
  match them and drop a second "1958", since the banner already says it.
- **`make_posters.py` still holds its geometry as literals inside `poster()`**,
  so `make_poster_cct.py` mirrors the numbers instead of importing them. Hoist
  picture-box width, QR targets and pads to module constants;
  `poster_credits.py` is the pattern to follow.
- `exports/分享訊息.txt` left untouched — that list is the 新店礦業文化路徑 series
  and this film is not part of it.

## Environment note

Partway through, Bash and Read lost read/list access to this Google Drive path
("Operation not permitted"). Files created during the session stayed readable
and writable; anything pre-existing could not be opened at all, for read or for
append — which is why `WORKLOG.md` was not updated in place and 1–3 could not be
rebuilt. Worked around it by staging `make_posters.py`, the images and the build
in the session scratchpad, rendering there, and copying results back.

That asymmetry (new files fine, pre-existing files blocked) suggests session-
scoped approval rather than a macOS-level permission problem, which a macOS
block would have applied uniformly. A fresh session in this directory should
have working access.

> MERGED into WORKLOG.md 2026-08-18 by the video-use session; the standalone
> file has been removed. The sandbox permission problem that forced it into its
> own file did not recur.
