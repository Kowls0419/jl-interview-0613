# Project memory — 新店礦業文化路徑 導覽影片

## Session 1 — 2026-07-05

**Strategy:** Inventory + evaluation complete. No cutting yet — waiting on materials
(photo scans etc.) requested from the producer. Kyle's materials-request list (in
Traditional Chinese) was sent to the producer; see "Materials requested" below.

**What this project is:**
Eight (±) ~3-minute Mandarin explainer videos for a QR-code self-guided heritage
tour. Association 新北市陳昌梯醫師山林保育協會, funded by 新北市文化局 community
grants. Year-115 plan: pre-record explanation clips → edit → upload to the
association's YouTube channel → QR codes printed next to on-site photo displays.
Visitors scan QR at each physical point to watch the matching clip.
Deadline context: filming complete end of July 2026, installation end of August 2026.

**Planned deliverables (from 115 plan PDF, in this dir):**
- 和美煤礦 (point A): 2 clips
- 陳外科醫院 (point C1): 2 clips
- 102台車巷 (point C2): 4 clips
- Possible extra: 過水橋/林秀卿故宅 (point D) — footage strongly supports it; Kyle
  hasn't confirmed adding it.
Target format (proposed, not yet confirmed by Kyle): 1080p horizontal, ~3 min each,
burned-in Traditional Chinese subtitles.

**Source footage (this directory, ~29 min total, all 1920×1080 H.264/AAC):**
- 002A4880.MP4 (27s, 30fps) — mic rehearsal/sound check. Utility; discard or BTS.
- 002A4881.MP4 (16.4min, 30fps) — producer explains project on camera (~first 90s,
  states intended 3-section structure: 光陰的故事/環境的影子/期待的未來), then
  interview part 1: childhood, move from 彰化和美 to Taipei at 7, wartime schooling,
  chasing the slow 新店–萬華 train, the Japanese-style family house, 瑠公圳. Interviewee standing, often looking sideways (weaker framing).
- 002A4882.MP4 (97s, 30fps) — continuation: swimming against current in 瑠公圳.
  Contains on-camera direction ("可以看一下鏡頭").
- 002A4883.MP4 (5min, 60fps) — seated doorway setup, best framing. All 和美煤礦:
  boat-transported coal, 和美山步道 origin, workers, financing the hospital.
- 002A4884.MP4 (5min, 60fps) — same setup. 振山煤礦, 光明街, 102台車巷 (she names
  光明街102巷 as the old coal-cart lane), railway, zoo trip, RETAKE of train-chasing
  story (better than 4881 version).
Interviewee = daughter of 林秀卿 (the mining figure the trail commemorates).

**Decisions so far:**
- Transcripts: cached in edit/transcripts/*.json, packed view at edit/takes_packed.md.
  (Public repo copy is trimmed to the passages used in the three published videos.)
  NEVER re-transcribe (Scribe costs credits; sources unchanged).
- Proper-noun corrections (Scribe mis-heard; PDF spellings are authoritative):
  林秀卿 (not 林秀清), 陳外科 (not 成外科/城外科), 振山煤礦 (not 鎮山/正山煤礦).
- **KYLE'S RULE (2026-07-05): ALL project output must be Traditional Chinese** —
  subtitles, titles, on-screen text, documents, messages to the producer. The cached
  Scribe transcripts are Simplified (fine as internal working data; timestamps are
  what matter) — convert text at subtitle/title generation time, e.g. OpenCC `s2twp`
  (Taiwan phrasing), then re-apply the proper-noun corrections above.
- Mixed 30/60fps sources → conform output (probably 30fps or per-clip; decide at cut).
- First clip to build once materials arrive: 和美煤礦 #1 from 4883 (cleanest footage),
  to lock the template with Kyle before batch-producing the rest.

**Materials requested from producer (pending):**
1. High-res scans of every photo the interviewee discusses on camera (蓄炭場,
   family photo by rail, wartime schooling, family house + hand-drawn floor plan,
   過水橋, zoo outing, etc.)
2. Association's collected 振山煤礦 photos (originals of those embedded in 115 PDF)
3. Present-day site photos/clips of each point (optional B-roll)
4. Association + 文化局 logos, official project title text for title cards
5. YouTube channel info; prior bird-guide video link as format reference
6. Name/place spelling confirmations

**Reasoning log:**
- The 115 PDF (115年一般性計畫補助須知附件8-9(團體)修正計畫.pdf) is the project
  spec; the 114 PDF is last year's closing report (context only). Photos embedded in
  the 115 PDF can be extracted as fallback cutaways if scans never arrive.
- Producer says on camera during 4881 that photos will be inserted in post — cutaway
  photo overlays are expected, not optional.
- ElevenLabs key lives in ~/Developer/video-use/.env (restricted key: Speech-to-Text
  permission only; /v1/user check returns 401 missing_permissions — that is EXPECTED
  and does not mean the key is bad).
- video-use venv: use ~/Developer/video-use/.venv/bin/python for all helpers
  (Homebrew Python is PEP-668 locked; pypdf/pdfplumber also installed in this venv).

**Outstanding:**
- ~~Kyle to confirm~~ → CONFIRMED 2026-07-06: **3 videos** (one per photo folder), the interviewee's
  voice only, interviewer questions become text cards, style = Claude's call.
- ~~Materials~~ → ARRIVED: folders 1/ (振山煤礦, 15 photos), 2/ (和美煤礦, 17), 3/ (生平/過水橋, 19).

## Session 2 — 2026-07-06

**Strategy:** Built video 2/3 (和美煤礦) as the approved-style template. Cold open on her
strongest quote (船運煤 hook) → title card → Q-card + answer blocks → end card with credits.
~2:54 total. Warm archival style: BG (18,15,12), cream Songti TC, amber accent; photos as
full-frame Ken Burns overlays (slow ease-in-out zoom, cream border, soft shadow, 0.4s fades);
subtitles Heiti TC 17 white/outline burned LAST (after overlays), MarginV=30.

**Deliverables (in edit/):**
- `hemei_preview.mp4` — 1080p preview WITH subs (2:54) ← show Kyle
- `hemei_nosub.mp4` — 1080p no subs (re-burn source, keeps one encode)
- `edl_hemei.json`, `hemei_zht.srt` (Traditional, OpenCC s2twp + fixes)
- `build/common.py` — shared card/Ken Burns/style machinery for videos 1 & 3
- `build/video2_hemei.py` — full spec: TIMELINE segments, QUESTIONS, OVERLAYS (photo→anchor
  time→duration), SUB_FIXES. Copy this file per video, edit the spec block.
- `cards_hemei/`, `kb_hemei/` — rendered assets

**Decisions:**
- Cam segments from 002A4883 only: 55.97-62.75 hook, 7.48-18.25 origin, 28.38-50.14 visit,
  65.30-105.66 boats (starts past her 是,所以是 stumble), 114.06-137.74 trail,
  162.06-184.42 workers, 198.52-221.99 memory. Cards: title 4.0s, questions 2.6s, end 5.5s.
- Cards are silent EDL sources (silent AAC baked in) so render.py concat just works.
- render.py used with --no-subtitles; SRT burned in a separate last pass because the built-in
  builder does 2-word UPPERCASE chunks (unusable for Chinese) and hardcodes Helvetica.
- Subtitle chunker: break at 。？！ always, at ，、； when ≥8 chars, hard cap 16 with
  fallback to last soft boundary (never splits mid-word).
- Subtitle text drops fillers (呃) and the garble 一沒使用; audio untouched. 臺→台.
- Self-eval passed: 9 boundary filmstrips clean (no pops, no flash frames), subs render
  over photos, duration 174.4s ≈ EDL 174.3s.

**Reasoning log:**
- 60fps source → render.py conforms everything to 24fps/1080p; cards+KB built at 24fps to match.
- Photo windows never cross cut boundaries; MEMORY overlay ends ~211s so her face carries
  the final "都一百多歲啦" beat.

**Session 2 revisions (Kyle feedback, same day):**
- 阿板塞 → 阿板師 (SUB_FIXES). 加州旅社 still needs producer confirmation.
- Removed the 2-2 photo overlay over the stocks passage (talking-head only there).
- NEW OPENING (replaces cold-open cam segment), v2 choreographed per Kyle's storyboard:
  calligraphy brush WRITES the actual inscriptions lifted from the photo (plaque 和美煤礦
  right→left at 0.2-1.8s; outer door columns 注意保安/努力生產 at 1.55-3.05; inner columns
  節約資材/改善生活 at 2.4-3.9) as dark ink on paper with faint structural pencil (people
  area suppressed) → pencil sketch draws the PEOPLE left→right 3.95-6.35 → whole scene
  sketches in → crossfade to real photo 6.6-8.1 → push-in, fade out. Her hook line V.O.
  (source 55.97-62.75, delayed 0.9s), 10s total. Built by `build/make_opening.py`: text ink
  masks come from percentile thresholds inside hand-mapped photo regions (bright text on
  dark doors, dark text on light plaque; region coords at top of file), noisy sweep fronts
  simulate the brush. EXTRA_CUES in build_srt carry the V.O. subtitles. Gemini refused this
  (real-minors policy); procedural approach is policy-free and reproducible.
- VISIT overlay photo now 2-11 (girls at gate) since 2-14 became the opening.
- KB clips now cached by photo number + duration (kb_pNN_Ns.mp4), not index.
- Font decision PENDING: comparison sheet at edit/verify/font_options.png
  (Heiti TC / Noto Sans TC / Noto Serif TC / LXGW WenKai TC / jf-openhuninn; files in
  edit/fonts/). Current preview burned with Heiti TC. To switch: re-run the subtitles burn
  with fontsdir=edit/fonts and force_style FontName=<family>.
- Current preview: edit/hemei_preview.mp4, 2:57.5.

**Session 2, revision 3 (Kyle feedback):**
- Font LOCKED: LXGW WenKai TC (edit/fonts/LXGWWenKaiTC-Regular.ttf; burn with
  fontsdir=fonts, FontName=LXGW WenKai TC, FontSize=18, Outline=1.6).
- Opening now SILENT (Kyle may add BG music later); hook line restored as the cam segment
  answering q3. Opening reveals are all stroke-based: structural pencil sweeps in
  diagonally, photo revealed by 5 alternating brush swipes (REVEAL 6.5-8.4s) — no fades.
- Cut tightened: long pauses/stumbles trimmed (see labeled TIMELINE in video2_hemei.py);
  every splice hidden under a photo block. Runtime 2:49.6.
- KB overlays are now ProRes 4444 .mov WITH ALPHA (transparent bg, soft shadow over
  footage) — photos crossfade over the live footage, 0.5s alpha fades. Photo-to-photo
  chains overlap 1.0s (= 2x fade) so footage never ghosts through mid-dissolve.
- Fewer switches: photos consolidated into 6 blocks (VISIT pair, BOATS pair x2 windows,
  TRAIL, WORKERS, MEMORY singles). No photo repeats; ORIGIN is talking-head only.
- Grade (natural historic warm) applied in the subtitle-burn pass so cards/photos/footage
  shift together: colorbalance rs=.02 gs=.005 bs=-.025 rm=.025 gm=.008 bm=-.02 +
  eq contrast=1.04 saturation=0.95. Skin tones checked.

**Session 2, revision 4 (Kyle caught missing 所"以" at 0:44):**
- ROOT CAUSE (applies to ALL future videos): Scribe pads each word's `end` through the
  following silence. Filtering segment words by end-time drops real words whose pause-pad
  crosses a trim cut (lost 以 at src 46.8, 到 at 73.5). build_srt now filters by word
  START (a-0.02 <= start < b-0.05). Also: visit_b end 47.00→47.30 (keep spoken 以),
  visit_a end 32.55→32.38 (was clipping onset of spoken 但), VISIT block pdur 8.2→8.4.
- Boundary audit snippet (check every cam cut against every word span, ignore cuts inside
  pause-padding) should be run whenever segment times change.

**Session 2, revision 5 (2026-07-07): flicker fix + titles**
- FLICKER: rolling horizontal bands = fluorescent flicker in 60fps sources aggravated by
  60→24 decimation. Fix: EDL `"grade": "tmix=frames=5"` — runs in the per-segment
  extraction chain at source fps BEFORE render.py's -r 24, averaging across flicker
  phases. Real color grade stays in the subtitle-burn pass. Measured on 4883 @118s:
  no-tmix mean=0.398/max=1.036 → tmix=3 0.321/0.679 → tmix=5 0.217/0.408 (chosen; no
  visible smear on seated subject; tmix=7 =0.163 but more smear risk). Verified on final
  render via 12x-amplified frame diffs: no band stripes.
- Metric (reusable): row_mean per frame → highpass (subtract gaussian σ=25) → std of
  consecutive-frame differences of that profile. Static-scene metrics DON'T work (encoder
  skip-blocks freeze frames).
- PER-SOURCE flicker survey: 4881 (30fps) mean=0.376 max=1.251 — BAD, video 3 needs
  anti-flicker; at 30fps tmix=5 = 167ms smear risk, and she STANDS/gestures in 4881 —
  test tmix=3 vs 5 on gestures before choosing. 4882 (30fps) 0.123 — clean, no tmix.
  4884 (60fps) 0.149 at 100s — cleaner than 4883, but re-measure other spots when
  building video 1; grade field is per-EDL so each video chooses its own.
- TITLES/NAME (Kyle): main title 光陰的故事, speaker 陳林彩薇 (this resolves Scribe's
  「陳英采薇」garble from 4881 — she is 林秀卿's daughter, married into the 陳外科 family).
  Title card: 新店礦業文化路徑 / 光陰的故事 / 和美煤礦 / 口述：陳林彩薇. End card credits
  include 口述 陳林彩薇（林秀卿先生之女）. make_title_card now takes optional sub2.
  NOTE: 光陰的故事 was the producer's section-1 name; videos 1/3 may be 環境的影子 /
  期待的未來 — confirm with Kyle at build time.

## Session 3 — 2026-07-07 — all four videos built

**Kyle confirmed series structure:** 1 光陰的故事 (和美煤礦, built), 2 環境的影子,
3 期望的未來 (Kyle's spelling: 期望 not 期待), 4 製作花絮 (BTS).

**Previews in edit/ (all 1080p, LXGW WenKai TC subs, warm grade, awaiting approval):**
- `hemei_preview.mp4` 光陰的故事・和美煤礦 (2:49.5) — spec build/video2_hemei.py
- `zhenshan_preview.mp4` 環境的影子・振山煤礦/光明街 (2:35.9) — build/video1_zhenshan.py,
  source 002A4884 (measured flicker-clean at 4 spots → grade ""), opening photo 1-7
  (本坑職員移動留影 37.4.1 inscription = calligraphy phase), hook = 102巷台車道 line,
  ends on 振山煤礦鳥瞰 illustration (1-9) + 從後山看得出來 contemplation.
- `shengping_preview.mp4` 期望的未來・過水橋/瑠公圳 (3:21.7) — build/video3_shengping.py,
  MULTI-SOURCE (002A4881 + 002A4882; spec format ("cam", src_key, a, b, label)).
  grade tmix=frames=3 (4881 flicker 0.376; tmix=5 smears face at 30fps — tested crops).
  Opening photo 3-2 (北一女 class photo, caption = calligraphy). 16 cam segments,
  8 Q-cards, closes 碧潭水都很乾淨 over modern canal photo (3-8) → 期望的未來 theme.
  NOTE: photo 3-9 has a baked-in yellow 'A' mark — used 3-10 instead.
- `huaxu_preview.mp4` 製作花絮 (0:55) — build/video4_huaxu.py. Mic rehearsal (4880)
  + directing moments (先一段一段 / 阿媽等一下你要看這裡 / 可以看一下鏡頭 / 先停了).
  Montage, straight cuts, no overlays.

**Name fixes this session:** 精美→景美, 柳公圳→瑠公圳, 近水游→逆水游, 高麗跟→高麗坑,
蓄碳廠→蓄炭場, 抬車→台車 (all in per-video SUB_FIXES; audio untouched).
Unverified names for producer: 加州旅社 (hemei ~1:02), 阿板師 spelling, 營區小車站
(likely 螢橋? left as-heard in shengping? — actually that line wasn't included), 灌溉俊
(not included). 高麗坑 inferred — confirm.

**Session 3 addendum (2026-07-08):**
- PROJECT MOVED: everything now lives back at the Google Drive path
  `.../2TB PURZ/Projects/2026/JL Interview 0613/` (the old local archive copy
  is gone). Build scripts are path-relative so they work; EDLs contain
  absolute paths -> RE-RUN each build script before any re-render.
- Folder 4/ arrived: 11 production stills (crew rigging ring light/tripod, director
  briefing with grandma listening, her portrait framed in the ring light, group photo
  with the crew, one plan-cover scan 4-11 unused).
- Huaxu v2 (1:04): stills as alpha KB overlays — rigging pair over the mic-test stretch,
  director-briefing still over 先一段一段, ring-light portrait over 可以看一下鏡頭 —
  plus a 9s silent photo coda (group photo 4-9 -> courtyard smile 4-2) on a blank card
  before credits. Coda is music-ready.

**PRODUCT FOLDER RULE (updated 2026-07-10):** `product/` holds the four deliverables as
REAL FILE COPIES with numbered Chinese names. ⚠️ MUST be copies, NOT symlinks: the project
lives on Google Drive, which does NOT sync symlinks (they show stale/broken on Kyle's
devices — he caught this). After ANY re-render/re-burn, run `edit/build/sync_product.sh`
to refresh the copies (it maps each *_preview.mp4 → its numbered name). Current mapping:
  1_光陰的故事_過水橋瑠公圳 ← shengping_preview
  2_環境的影子_和美煤礦     ← hemei_preview
  3_期望的未來_振山煤礦     ← zhenshan_preview
  4_製作花絮               ← huaxu_preview
For final full-q renders, point sync at edit/*_final.mp4 (edit the script's src).

**Outstanding:**
- Kyle: watch all four previews, give notes.
- After approval: FINAL renders = re-run render.py per EDL WITHOUT --preview, then re-burn
  subs with the same command (swap input to *_nosub final). Upload to YouTube + QR.
- BG music: openings are silent; Kyle may add music later (opening is 0:00-0:10 in the
  three main videos; whole 花絮 could take light music).
- Then build video 1 (振山煤礦, 002A4884 + folder 1) and video 3 (生平/過水橋,
  002A4881+4882 + folder 3) by copying video2_hemei.py and editing the spec block.
- Ask producer: 「加州旅社」 spelling (~01:02 in video).
- Final renders: render.py without --preview + re-burn subs, per video, after approval.


## Session 4 — 2026-07-08 (Kyle review round 1)

**Done:**
- Title-card 「・」 glyph missing in Songti TC (rendered as box) → replaced with 「與」
  in vids 2/3 subtitles lines. RULE: never use ・ in card text.
- Vid 2: 1-14 (貯炭場台車) moved from train-story splice to the final 運煤路線 answer,
  chained with 1-9 鳥瞰圖; train splice now covered by 1-13 (era family portrait).
- Vid 2 INTERVIEWER CROP: EDL source is now edit/proxy/4884_crop.mp4
  (crop=1408:792:512:170, crf16 intermediate, audio copy — timestamps preserved).
  CRITICAL LESSON: proxy crop MUST be exact 16:9 — first attempt (1420x798) scaled to
  1920x1078 vs cards' 1080; the -c copy concat of mixed heights silently broke the last
  3 overlays in the composite. 1408x792 → exactly 1080 ✓.
- Vid 3 gaze pass (Kyle's rule: looking at camera → footage; not looking → photo):
  LOOKING (kept): intro, war, gone_a/b, hero, clean, typhoon start, canal start, hook_a.
  NOT LOOKING (now photo-covered): school_a/b ([3-5,3-4] 10.4s each), dad (3-11),
  hook_b mid (3-10 extended 6.5s), swim edges (3-3 added at start), typhoon tail
  ([3-17,3-7] chain).
  INTERVIEWER IN FRAME: home whole segment ([3-6,3-13] full cover), canal_a head poke
  (3-15 re-anchored to cover). No global crop for 4881/4882 — he overlaps her when he
  intrudes; photo cover is the fix. Laptop bottom-left OK per Kyle.
- Photo verification table (all 4 videos, 41 rows: thumbnail + timecode window + the
  subtitle text spoken during the window): edit/photo_table.html (shared privately for review).
  Regenerate after any overlay/cut change (script inline in session; rebuild from EDL+SRT).

**PENDING KYLE (vid 3 opening/ending restructure — proposals sent, do not edit until
he picks):**
- Opening (hook lacks context): (A) add Q-card 「以前要怎麼過瑠公圳？」 between title and
  hook — minimal; (B) open with intro (彰化搬來) instead, move bridge lines into q7 flow;
  (C) scene-setting text card before hook.
- Ending (too abrupt, no 期望的未來 thesis): (A) closing text card before credits, e.g.
  「如今，過水橋與瑠公圳仍在。願這些記憶，隨水長流。」; (B) reorder to end on 游泳選手
  laugh + modern photos + text card.
- Recommended: Opening A + Ending A.

## Session 5 — 2026-07-08 (Kyle review round 2) — DONE
Model switched to opus-4-8. Worked sequentially w/ edit/WORKLOG.md (recovery log).
- V1 光陰: dropped 2-17 (dup of 2-16). 2:49.5
- V2 環境: removed 1-4 (school photo, not zoo) & 1-13 (family, not train) → those beats
  now footage; ending 1-14→1-9 shows right after q6 card then LANDS on her face (no
  face<->photo bounce). Fixed proxy crop to exact 16:9 (1408x792) — earlier non-16:9
  broke overlays. 2:35.9
- V3 期望: BIGGEST. Opening C = scene statement card 「過水橋，曾是這戶人家出入家門的
  唯一通道。」 before hook. Ending A = 今日的過水橋(3-7)+今日的瑠公圳(3-8) photo cards +
  thesis card 「如今，過水橋與瑠公圳仍在，願這段光陰，隨水長流。」 before credits. Removed
  3-6 (unclear plan). 3-12+3-13 now ONLY in home/house-living block. 3-3 dropped (dup of
  3-1... kept 3-1 on swim). Modern shots (3-7,3-8) moved from mid to the ending. NEW:
  make_statement_card + make_photo_card in common.py; make_kenburns cover= param (blurred
  full-bleed fill) for home & canal_a where interviewer walks INTO frame — fully hides him
  (COVER_LABELS). 3:40.6
- V4 花絮: added 3 new BTS stills from 4/new (HEIC→jpg via sips, copied as folder-4
  #20/21/22 = IMG_6448/6452/6444); coda montage extended to 18s. 1:12.8
- CARD GLYPH RULE reaffirmed: ・ boxes in Songti → use 與 / 今日的… (hit again in captions).
- photo_table.html regenerated (40 rows) + republished to same artifact URL.
- Rotated HEICs (6446/6447/6449/6451) NOT used (sideways, no exif bake).

**Outstanding:** Kyle review round 2 of all 4 in product/. Then FINAL full-q renders.

## Session 6 — 2026-07-09 (folder-4 media round 3) — DONE
Kyle removed IMG_6444 (was folder-4 #22) + IMG_6446 from 4/new; asked to remove from
vid4 and utilize ALL remaining media. Remaining new: 6447,6448,6449,6450.MOV,6451,6452.
- Placed uprighted stills via exif_transpose: #23=6447, #24=6451, #25=6449;
  #20=6448, #21=6452 (from before). #22=6444 DELETED.
- IMG_6450.MOV = live BTS clip → NEW proxy edit/proxy/bts_mov.mp4 (portrait phone clip,
  operator filming through doorway; scaled to 1040h fg over gblur=32 + eq brightness=-0.12
  blurred pillarbox fill, 1920x1080@24, 7.875s). Added as TIMELINE "bts_live" segment
  (out 49.3-56.8s) before coda. tmix=3 verified clean on the moving operator (hx2.png).
- Redistributed overlay stills to use everything: rehearsal[3,4,23] look_at_lens[7,25]
  one_at_a_time[6] coda[9,2,20,21,24]. coda card 18→16s.
- huaxu_preview rebuilt = 1:18 (78.3s). product/4 symlink auto-updated. WORKLOG round 3.

**Outstanding:** Kyle review of all 4 in product/ (vid4 now 1:18). Then FINAL full-q renders.

## Session 7 — 2026-07-09 (captions / bridge photos / fades) — DONE
- FADE POLICY (all vids): fades are now EASED (ease-in-out cubic), not linear —
  linear alpha at 24fps read as "clear steps." common._fade_k() envelope used by
  png_to_card_mp4, make_photo_card, make_kenburns. Card fades baked per-frame in PIL
  (blend toward warm BG) rather than ffmpeg's linear `fade`. Photo-overlay alpha ramp
  eased + 0.5→0.6s. Photo overlays crossfade over footage so they never go fully blank.
  CAVEAT still open: consecutive CARDS still dip through BG between each other (concat
  -c copy). True card↔card cross-dissolve = render.py xfade rework; deferred (would
  shift overlay offsets unless done only on the tail card run).
- CAPTION BAND (make_photo_card): when caption set, reserve bottom 13% band and center
  photo above it, so the Ken-Burns zoom never grows over the caption. Fixed vid3
  今日的過水橋 / 今日的瑠公圳 cards (zoom was overlapping text). zoom_to 1.08→1.07.
- Vid3: 3-10 + 3-17 (both 過橋 photos) now shown TOGETHER on the hook (bridge intro
  only); 3-17 removed from typhoon (typhoon now footage — her on-camera telling of the
  橋翻下去 story). hook block [10,17] anchor hook_a end -0.8, pdur 4.3, xover 1.0.
- Vid2: removed 1-4 from zoo block. 1-4 is the Xindian-elementary class photo (kids +
  teacher at 碧潭吊橋), NOT a "went out to play" image — Kyle: use it only for the
  elementary-school context (vid2 has none, so it just doesn't appear). zoo now footage.
- KB caches (kb_*/) MUST be cleared when a fade/zoom default changes — overlays are
  cached by filename (kb_pN_DURs.mov) and won't regenerate otherwise. rebuild_one.sh
  (scratchpad) does clear→build→render→burn per video.
- Rebuilt all 4: 1:2:49.8  2:2:36.1  3:3:40.8  4:1:18.3.

**Outstanding:** Kyle review of all 4 in product/. Then FINAL full-q renders (render.py
without --preview + re-burn subs). Optional: true card↔card cross-dissolves if Kyle
still finds the between-card BG dip too strong. Producer name checks: 加州旅社/阿板師/高麗坑.

## Session 8 — 2026-07-09 (RE-PAIR poetic titles ↔ content) — DONE
Kyle re-paired the three poetic titles with different content (place-subtitle + footage
stay bundled; only the big 主標題 + end-card title changed + product numbering).
⚠️ INTERNAL FILENAMES NO LONGER MATCH POETIC TITLES — use this map:
  | product # | 主標題      | 內容/place        | build script          | preview file        | edl            |
  |-----------|-------------|-------------------|-----------------------|---------------------|----------------|
  | 1         | 光陰的故事  | 過水橋與瑠公圳    | video3_shengping.py   | shengping_preview   | edl_shengping  |
  | 2         | 環境的影子  | 和美煤礦          | video2_hemei.py       | hemei_preview       | edl_hemei      |
  | 3         | 期望的未來  | 振山煤礦與光明街  | video1_zhenshan.py    | zhenshan_preview    | edl_zhenshan   |
  | 4         | 製作花絮    | BTS               | video4_huaxu.py       | huaxu_preview       | edl_huaxu      |
Changed only make_title_card 主標題 arg + make_end_card title arg in each of the 3 build
scripts. Openings carry NO title text (safe). thesis card in #1 ("願這段光陰，隨水長流")
now echoes its new title 光陰的故事 — happy fit. product/ symlinks renumbered:
  1_光陰的故事_過水橋瑠公圳 → shengping_preview
  2_環境的影子_和美煤礦 → hemei_preview
  3_期望的未來_振山煤礦 → zhenshan_preview
  4_製作花絮 → huaxu_preview
Durations unchanged (1:3:40.8  2:2:49.8  3:2:36.1  4:1:18.3).

**Outstanding:** Kyle review of all 4 (new titles/order) in product/. Then FINAL full-q
renders. Producer name checks: 加州旅社/阿板師/高麗坑.

## Session 9 — 2026-07-10 (fine notes on new-numbered cuts) — DONE
Notes use NEW numbering: V1=光陰/過水橋(shengping) V2=環境/和美(hemei)
V3=期望/振山(zhenshan) V4=花絮(huaxu).
- [V1] dad photo (3-11) was appearing over the q4 question card → now starts on footage
  (delta 0.25, pdur 3.8). home cover (3-12/13) was reverting ~1s to footage before the
  q6 card → now the last cover dissolves INTO the q6 card (delta 0.0, pdur 8.5). RULE
  learned: a framed-photo overlay whose window straddles a card boundary reveals the
  card; keep photo starts ≥ footage-start, and to hand a cover straight to a card, end
  the overlay ~0.6s (=fade) INTO the card so the fade-out happens over the card not footage.
- [V2] subtitle: 電氣師傅→電器師傅, 聯絡→聯繫 (SUB_FIXES). Text-only → re-burned from the
  existing hemei_nosub.mp4 (skip re-render; saves the extraction pass).
- [V3] subtitle 追著上→追的上. q6ans overlay delta 0.2→-0.4 so the q6 card dissolves
  straight into the coal-cart pic (no 0.2s footage flash). Still lands on her face after.
- [V4] MOV in-point 0.15→0.70: the live phone clip is the SAME directing moment as the
  cut_ok cam segment, so its first ~0.5s audio repeated cut_ok's "好" tail — trimming the
  in-point drops the echo. CODA redesign: new common.make_photo_pair_card() renders two
  stills side-by-side (framed, subtle synced zoom, eased fade); coda is now 3 diptychs
  (9|2, 20|21, 24|8) instead of a 16s one-at-a-time overlay montage → tighter, 1:12.5.
- make_photo_pair_card is reusable for any future 2-up beat.
- Durations now: V1 3:40.8  V2 2:49.8  V3 2:36.1  V4 1:12.5.

**Outstanding:** Kyle review. Then FINAL full-q renders (render.py w/o --preview + reburn).
Producer name checks: 加州旅社/阿板師/高麗坑. Open question if Kyle notes it: V1 typhoon is
~23s of continuous footage (no overlay) since 3-17 moved to the bridge intro.

## Session 10 — 2026-07-10 (LOUDNORM audio bug + transition rules) — DONE
⚠️ ROOT-CAUSE FIX: the render loudnorm pass was bleeding/pumping audio into silent
gaps — THIS was the V4 0:50 "repeat" (heard cut_ok's tail over the silent MOV clip) AND
the V1 2:00 "cut sound". Not a MOV/edit problem at all. Proof: render --no-loudnorm →
MOV region -91 dB (silent); with loudnorm → -18.5 dB. FIX: all preview renders now use
--no-loudnorm (rebuild_*.sh updated). YouTube re-normalizes loudness on upload, so no
loss. FINAL renders must also use --no-loudnorm (or a fixed, non-bleeding loudness step).
Also muted the MOV proxy audio (bts_mov_silent.mp4) since it's the same 好/停 moment as
cut_ok — belt-and-suspenders.

TRANSITION RULES (Kyle's rules, now standard — see also make_photo_pair_card):
  • FRAMED photo after a question card → start ~1s INTO the footage (card → ~1s
    footage → pic). Never let a framed photo sit over the card's brown bg. And it should
    END within footage (pic → footage → card), never straddle into the next card.
  • COVER (blur-bg full-bleed) photo → may go card→cover directly (fills frame, no bg
    mismatch). For clean both-ends, start it ~0.6s before footage (fade-in over the
    prev card) and end it ~0.6s into the next card (fade-out over that card) so footage
    never peeks. Implemented for V1 dad/home (delta -0.6, pdur sized to reach into card).
  • Audio: rely on the 30ms per-segment fades + NO loudnorm; cuts land in the silence
    after the last word.
Applied: V1 dad → COVER (Kyle: "just pic, blur bg"); V1 home cover tightened both ends;
V1 school framed → delta 0.5→1.0 (1s footage after q3 card); V3 q6ans framed → delta
-0.4→1.0. V1 subtitle 平→坪 (兩千坪/一千兩百坪).
V4 reorg (Kyle: overlay only location-matched, others after): rehearsal [23,3],
look_at_lens [7]; moved 4 & 25 into a 4th coda diptych. coda now 9|2 20|21 24|8 4|25.

Durations: V1 3:40.8  V2 2:49.7  V3 2:36.1  V4 1:16.3.

## Session 11 — 2026-07-10 (flash rule both-sides + V4 overlay-on-footage) — DONE
- TRANSITION RULE now BOTH sides: a framed overlay must have ≥1s footage BEFORE and
  AFTER the pic — it must never touch a card (entry OR exit). Cover (blur) photos handle
  card↔photo directly. diag3.py (scratchpad) audits every overlay's card margins from the
  EDL. V2 & V3 were already compliant (all exit margins ≥1.8s) — untouched. V1 fixed:
  hook 3-17 ended exactly on the q1 card (the flash) → framed delta 1.0/pdur 3.9; school
  pdur 9.5→9.3. Short/mostly-pic segments should be COVER, not framed.
- V4 flipped to the OPPOSITE of V1/2/3 (Kyle): NO standalone pic cards — all stills are
  framed overlays ON the playing footage; deduped to 8 shots (dropped 3,4,5,10,24,25,1).
  rehearsal [23,8,20,21], one_at_a_time [6], look_at_lens [7], MOV-finale [9,2]. 1:02.3.
  make_photo_pair_card now unused in V4 (kept in common.py for future).
- Durations: V1 3:40.8  V2 2:49.7  V3 2:36.1  V4 1:02.3.

**Outstanding:** Kyle review (ensure fresh Drive sync — see product fingerprints in
WORKLOG). Then FINAL full-q renders WITH --no-loudnorm. Producer names: 加州旅社/阿板師/高麗坑.

## Session 12 — 2026-07-21 (skill upgrade: review app + learning loop; DaVinci dropped)
DIRECTION CHANGE (Kyle): abandon the FCPXML/DaVinci export path — `helpers/edl_to_fcpxml.py`
stays but is no longer pursued. Instead upgraded the **video-use skill itself** with the two
mechanisms from the referenced IG reel:
1. **Review app (審片)** — `helpers/review_server.py` + `helpers/review.html`. Local server
   serves a `*_preview.mp4` to the browser; Kyle scrubs (Space/←→/Shift+←→), comments at a
   timestamp (Enter), and draws pen/arrow/box on the frame. Writes
   `edit/review/<stem>_rNN.json` + flattened annotated PNGs under `review/frames/`. I read the
   JSON + PNGs directly — no more long "at 1:32 the text is cropped" prompts. Verified E2E
   (Range/206 scrubbing, seek to 1:32 shows the right frame, note write + convergence report).
2. **Learning loop (流程改善)** — GLOBAL, scope-tagged ledger at the skill root
   (`video-use/lessons.md`), seeded from this project's WORKLOG rules (L01 loudnorm bleed,
   L02 framed-touching-card flash, L03 cover→card drift, L04 ・→box, L05 平→坪 class, L06
   Traditional-only, L07 Drive-no-symlinks, L08 gaze-cover). `helpers/lessons.py report` tracks
   corrections/round (convergence). SKILL.md now: Hard Rule 13 (consult lessons before every
   render; promote new recurring mistakes after each review round), process step 0 (recall) +
   step 8 (審片 review) + step 9 (close loop), a Review & Learning section, and anti-patterns.
   Skill lives at `~/Library/CloudStorage/GoogleDrive-…/My Drive/claude-skills/video-use/` (moved 2026-08-18 from ~/Developer).

**How to use next time:** `python helpers/review_server.py <edit>/<name>_preview.mp4` → Kyle
annotates → I ingest `edit/review/*.json` + frames → fix. Before any render, read
`video-use/lessons.md` and self-check.

## Session 13 — 2026-08-13 (花絮 folded into V1–V3; V4 abandoned)

**Direction (Kyle):** drop V4 製作花絮 as a standalone. Its material goes to the END of
each location video, with staff credits added. Also queued: 今貌 daylight footage for V2
and V3 (NOT SHOT YET — add later; V1 already has today_bridge/today_canal photo cards).
Then final render + music → YouTube unlisted → QR → professor.

**Room mapping (Kyle confirmed via edit/bts_rooms.html).** The shoot was one morning in
one building, three setups = three videos:
  手術室 (4880/81/82) → V1 光陰的故事 · 走廊・中庭 (4883) → V2 環境的影子 ·
  照片陳列室 (4884) → V3 期望的未來
  stills  A: P4 P20 P23 P24 N6448 P1 · B: P5 P10 P21 N6452 P3 · C: P6 P7 P2 P8 P9
  unused: P25 N6446 N6447 N6449 N6451 P11(計畫書) N6444(bike)

**Closer design** (`make_credits_grid_mp4` in build/common.py): end card holds full-frame,
then eases down-LEFT (S=0.46) while a grid of 花絮 material staggers in on the RIGHT.
Stills are static tiles; CLIPS are SILENT playing tiles (no audio, no subtitles), all
landing their last frame together — longer clips time-compressed to the play window,
shorter ones hold frame 0 then start late. `credits_grid_duration()` is frame-quantized
and called by BOTH the build script (for TIMELINE) and the renderer, so the EDL can never
clip the closer's tail.

**Review rounds (Dailies):**
- r01 (2 notes): (1) left margin 291px vs right 40px → shifted composition left, now
  ~171/144. (2) BTS videos should NOT be full-screen beats before the credits — make them
  silent tiles inside the grid. Reworked; this also removed all BTS subtitles.
- r02: V1's grid had too many similar shots. Built `edit/v1_grid.html` (13 clip GIFs +
  all 23 stills, click to toggle) → Kyle re-picked **clips K3, K10 · stills P1 P4 P20 P23
  P24** = 7 tiles, 4×2 with the short last row centred.

**Credits now:** 口述 陳林彩薇（林秀卿先生之女）/ 攝影 李承洋 / 後製剪輯 楊大謙 /
指導單位 新北市政府文化局 / 執行單位 新北市陳昌梯醫師山林保育協會

**Pipeline restored:** `edit/build/rebuild.sh <shengping|hemei|zhenshan> [--final]` —
build → render (--preview --no-subtitles --no-loudnorm) → grade + burn subs LAST
(LXGW WenKai TC 18, Outline 1.6, MarginV 30; colorbalance+eq warm grade). The July
rebuild_*.sh scripts had been lost to scratchpad; this one lives in the repo.
Also rebuilt the video-use venv (was gone) — `uv venv` + `uv pip install -e .` + opencc.

**Durations:** V1 3:47.0 (was 3:40.8). V2/V3 wired (5 stills + 1 wrap clip each) but NOT
yet rendered.

**Outstanding:** V1 r03 review → build V2 → review → build V3 → review. Then 今貌 footage
for V2/V3 when shot, music, final renders (--final), YouTube unlisted, QR, send professor.

**Session 13b — card morph smeared by the EDL anti-flicker grade (Kyle caught it)**
Kyle asked whether the closer's shrink-to-left morph was the same style in all three.
Timing/geometry WERE identical (same make_credits_grid_mp4 defaults, no overrides; card
left edge hits x=376 @50% and x=192 @75% in all three, to the pixel) — but the RENDERED
look was not:
  V1 grade tmix=frames=3 → ghosted · V2 tmix=frames=5 → worst · V3 grade "" → clean
ROOT CAUSE (reusable): render.py applies the EDL-wide `grade` to EVERY range, cards
included. tmix temporally averages frames; on a STATIC card that is invisible, which is
why this hid for months. The closer is the first card with real motion, so tmix smeared
its animation — proportional to frames=N.
FIX: render.py now honours a per-range `"grade"` key that overrides the EDL-wide filter
("" = opt out entirely; backward compatible). All three build_edl() now emit
`"grade": ""` on card ranges — cards are synthetic, nothing to de-flicker, and the warm
colour grade still reaches them in the subtitle-burn pass. Also fixes the smeared slow
zooms on V1's today_bridge / today_canal photo cards.
VERIFY METHOD (reusable): sample all videos at the same offset relative to their closer
start, bbox the non-BG pixels in the left region only (x<740, so the grid can't pollute
it), compare across videos per phase. scratchpad verify_morph.py.
Durations unchanged: V1 227.04 · V2 175.75 · V3 162.25.

**Session 13c — 今貌 (present-day) footage added to V2 and V3**
Kyle shot the daylight material and dropped it in `IRL/`. Treatment follows V1's
today_bridge/today_canal: framed photo, slow zoom, small caption at the bottom.
- V2 (+9.2s → 3:04.9): today_mine `IRL/v2/627244688344613072.jpg` 「今日的和美煤礦坑口」·
  today_river `IRL/v2/627244688092954948.jpg` 「今日的新店溪與和美山」
- V3 (+11.0s → 2:53.2): today_tunnel = the four `IRL/v3/振山煤礦台車山區段隧道/*.jpg`
  in one row 「今日的振山煤礦台車山區段隧道」(name corrected by Kyle: 山區 not 山匾) ·
  today_lane = `IMG_7803.MOV` time-lapsed 39.5s→6.0s (6.6x) with `IMG_7802` framed
  beside it 「今日的102台車巷」
Two new reusable card builders in common.py, both in the make_photo_card language
(cream border via shared `_framed`, soft shadow, caption band, eased fade):
  `make_photo_grid_card(photos, ...)`  — N photos in one row, shared height,
      width-budget clamp so the row always fits.
  `make_clip_photo_card(clip, a, b, photo, ...)` — a clip time-compressed to fill the
      card duration, framed beside a still. Silent.
GOTCHA: PIL cannot read iPhone HEIC. video1_zhenshan.build_cards() shells out to `sips`
to cache IMG_7802.jpg next to the HEIC (idempotent — skipped if the jpg exists).
Durations now: V1 227.04 (3:47.0) · V2 184.92 (3:04.9) · V3 173.25 (2:53.2).

## Delivery status — 2026-08-14

**exports/ holds the finished full-quality deliverables** (1920x1080 @24, AAC 48k):
  1_光陰的故事_過水橋瑠公圳.mp4   3:51.6
  2_環境的影子_和美煤礦.mp4       3:04.9
  3_期望的未來_振山煤礦.mp4       2:53.2
Built by `edit/build/export_final.sh` = rebuild.sh --final (render, no --preview) →
warm grade + LXGW WenKai subtitle burn → 2s fade to true black → hybrid music mix.

**Music.** Kyle generated the tracks with Gemini (3-minute cap per track; prompts must
NOT mention durations or the tool errors). Sources in `audio/V1-V3.mp4`, normalised to
-20 LUFS as `edit/music/v1-v3.wav` — the originals were mastered hot (V1 peaked
-0.3 dBFS) and would have buried her voice. Treatment = **hybrid** (Kyle chose from
A/B/C demos): quiet bed at 0.24 gain under speech, full in the holes. Envelope built in
numpy with raised-cosine ramps — ffmpeg `volume=enable=` switches hard and clicks.
V1 and V2 loop (short by 59s / 36s) with a 3s equal-power crossfade; V3 covers.
Music lifts: V1 0-18s & 201-232s · V2 0-16s & 164-185s · V3 0-14s & 151-173s.
Question cards (2.6s) deliberately stay ducked — too short to lift without pumping.

**>>> KYLE IS DOING THE YOUTUBE UPLOAD HIMSELF (unlisted). <<<**
Claude has no access to the account and must not attempt it. After Kyle has the three
URLs, Claude generates the QR codes locally (print-ready SVG/PNG, one per site) — that
part is still Claude's. Sending to the professor is Kyle's.

**Open / unresolved:**
- "Speaker pops" Kyle reported are NOT located. An 85 Hz high-pass is in the mix chain
  (removes real 20-60 Hz rumble, harmless to a ~180-220 Hz voice) but it did NOT fix
  what he heard — measured -0.7 dB on the one candidate, whose energy turned out to be
  180-300 Hz, i.e. a loud vowel. NEEDS TIMESTAMPS FROM KYLE. See reflect L28.
- Three separate QR codes assumed (one per physical site). If the professor wants a
  single link instead, build an index page rather than three codes.

## DELIVERED — 2026-08-14

Kyle uploaded the three videos to YouTube (unlisted) himself; everything below is final.

**Live URLs**
  V1 光陰的故事（過水橋與瑠公圳）3:51.6  https://youtu.be/X_w4xc4K4mQ
  V2 環境的影子（和美煤礦）      3:04.9  https://youtu.be/8fX-KAuwS7k
  V3 期望的未來（振山煤礦與光明街）2:53.2  https://youtu.be/DNgJGysthdo
  playlist  https://www.youtube.com/playlist?list=PLePG5FUoVOJI
  Saved in `edit/urls.json` — any poster rebuild picks these up automatically.

**exports/**
  3 × mp4 (1920x1080@24, AAC 48k) — final renders, warm grade, LXGW WenKai burned
      subs, 2s fade to true black, hybrid music bed
  thumbnails/  3 × *_B_split.jpg (1280x720) + playlist.jpg + 3 × _still_*.png
      (_still_* are a BUILD INPUT for the posters, not leftovers — don't delete)
  print/       3 × A4.pdf @300dpi + 3 × QR.svg
  分享訊息.txt  the share message, all nine links

**New build scripts (all in edit/build/)**
  export_final.sh    rebuild --final → grade+burn+fade → mix_music → exports/
  mix_music.py       hybrid bed; envelope in numpy (raised-cosine), speech regions
                     from the SRT, loops short tracks with equal-power crossfade,
                     85 Hz HPF on dialogue, 1.5s in / 4.5s out fades
  make_posters.py    A4 posters; pure white ground, video QR + 33mm playlist QR,
                     DECODES BOTH OFF THE RENDERED PAGE and refuses to save on
                     mismatch. Needs exports/thumbnails/_still_<slug>.png.
  make_thumbnails.py B_split thumbnails + playlist() triptych
  rebuild.sh         per-video build → render → grade/burn/fade

**Gotchas hit this session (see also reflect ledger)**
  - macOS bash 3.2: `"${ARR[@]}"` on an EMPTY array trips `set -u`. Use
    `${ARR[@]+"${ARR[@]}"}`. Only bit on --final, the branch never run before.
  - `echo "exit=$?"` after a backgrounded script masks its failure as success.
  - EDL `grade` applies to CARD ranges too; tmix smears animated cards. Cards now
    carry `"grade": ""` (per-range override added to video-use render.py).
  - Songti TC has no U+30FB `・` (tofu). U+00B7 `·` is fine.
  - PIL cannot read HEIC — shell out to `sips`.
  - ffmpeg `afade=out` then `afade=in` zeroes everything after the first fade.

**Unresolved:** the "speaker pops" Kyle reported were never located; the 85 Hz HPF
did NOT fix the one candidate (-0.7 dB; its energy was 180-300 Hz = a loud vowel).
Needs timestamps if it still bothers him. Playlist ID PLePG5FUoVOJI is 13 chars vs
YouTube's usual 34 — flagged to Kyle twice, unverified by me.

## Session 14 — 2026-08-18 (subtitle typo pass, post-delivery)

**Direction (Kyle):** four subtitle corrections + a single verification image for the
professor. Videos were already live (unlisted) since 2026-08-14.

**The four, as asked:**
1. every 遊 → 游 (swimming, not travel)
2. 二姑丈 → 二姑丈（劉明）
3. 所以我是等於一個游泳選手 → 所以我是北一女的游泳選手
4. 高麗坑 → 高麗坑（檳榔坑，現檳榔路）

**ROOT CAUSE of #1 — OpenCC introduces the error, the ASR never had it.** The raw
Scribe output is 游 everywhere (逆水游/顺水游/游得/游泳). `s2twp` rewrites 游→遊 for the
travel sense and gets swimming wrong. So the fix belongs in SUB_FIXES (which runs
after `cc.convert`) and MUST BE THE FIRST ENTRY — see below.

**Dead-fix discovery.** V1's `"近水游" → "逆水游"` had NEVER FIRED. OpenCC turned the
string into 近水遊 before the replace ran, so the key could not match, and the shipped
V1 read 「你在那近水遊的時候遊得很快」 — wrong twice. Putting `"遊":"游"` first revives it,
so that line also changed (to 逆水游, consistent with the surrounding 逆水 passage).
Flagged to Kyle as a 5th change he did not ask for. → reflect **L40**.

**Guard added (all three build scripts).** `fired = dict.fromkeys(SUB_FIXES, 0)`,
counted per key, then a warning listing keys that never matched. WARN, not assert —
an entry can honestly be zero once an earlier key fixed the text (呃 after 呃，;
鎮山 after 鎮山煤礦). First run flagged 4 more benign no-ops. Regenerated SRTs were
byte-identical, so the guard is observation-only.

**Build shortcut used.** Only the SRT changed, so this did NOT re-run build+render.
Re-burned step 3/3 of rebuild.sh (grade → subtitles → 2s fade) straight onto the
existing full-quality `<slug>_nosub.mp4`, then mix_music.py → exports/. ~4 min/video
instead of ~40. V2 (hemei) regenerated byte-identical and was not touched at all.

**Verified:** 7 changed cues, 6 in V1 + 1 in V3. Durations bit-identical to the
delivered files (V1 231.624349, V3 173.249349). Sampled the burned subtitle band at
every changed cue in the ACTUAL exports — text correct, single line, no wrap, no tofu.
Longest new line 高麗坑（…）at 22 chars = 1125px = 58.6% of frame (previous project max
was 16 chars / 813px); measured by burning test lines onto a black frame and taking
the bbox, before committing to the change.

**New:** `build/make_subfix_sheet.py` → `exports/print/字幕修正對照表.png` (2560x3847).
Diffs shipped-vs-rebuilt SRTs to find the changed cues, then pulls the SAME frame from
the DELIVERED video and the corrected one and lays them out side by side — the picture
is identical in both, so the subtitle is the only thing that moves. First version
typeset the text instead of screenshotting it; Kyle wanted real frames ("i meant like
actual screenshots from the vid"), which is also the stronger evidence. Requires the
pre-fix exports, kept as `<before_dir>/<slug>.mp4`. Refuses to save on page overflow
(L36) and on a cue-count mismatch (would mean timings moved, so pairing by index
would silently misalign).

**Outstanding — Kyle's call:**
- V1 and V3 need re-upload. YouTube cannot replace a file, so both get NEW video IDs;
  urls.json, the two QR svgs and the two A4 posters must then be rebuilt
  (make_posters.py reads urls.json). **V2 is unchanged — its URL, QR and poster all
  stay valid.**
- 分享訊息.txt still carries the old V1/V3 links.

**Session 14b — quality pass. I was wrong about the encode; measured it.**
Kyle asked whether the videos could be upscaled. Sources are 1920x1080 h264 (4881
29.97fps @30Mbps; 4883/84 59.94fps @60Mbps) — no 4K headroom, the camera shot 1080p.
I claimed the 2.4-3.3 Mbps exports were over-compressed ("1/10th the source") and
proposed a lower-CRF re-render of all three. THEN MEASURED IT, against a lossless
reference of the same filter chain, on a 14s talking-head segment:
  CRF20-fast → CRF20-medium  =  3.4 Mbps,  SSIM 0.98463
  CRF14-slow → CRF16-slow    =  9.0 Mbps,  SSIM 0.98594
+0.0013 SSIM for 2.6x the size. Invisible. **Dropped the re-render.** The premise was
wrong: CRF is quality-targeted, the camera's bitrate is fixed-rate, and this content
(static talking head, flat walls, tmix smoothing) is genuinely cheap to encode. → L41.

**What was actually done instead:** `exports/upload_1440p/` — all three at 2560x1440,
`scale=...:flags=lanczos` applied BEFORE the subtitle burn so libass renders the text
natively at 1440p rather than upscaling it (verified: libass scales proportionally,
text is 21.1% of frame width at 1080p vs 21.2% at 1440p, so force_style needs no
change). Picture gains no real detail; the point is to clear YouTube's 1080p encode
tier — a platform behaviour I could NOT verify locally, so it is a bet, not a finding.
`exports/` keeps the native 1080p masters as the archive.
  V1 5.6 Mbps 161M · V2 7.9 Mbps 182M · V3 7.7 Mbps 160M, durations unchanged.
Verified: corrected cues present in the 1440p files, V2's subs intact, end fade
reaches black (max luma 1-2/255) in all three.

**render.py gained `--crf` / `--preset`** (shared video-use helper, backwards
compatible — defaults keep the existing ladder). Built for the re-render that then
turned out not to be worth doing; still the right hook when an intermediate should be
near-transparent.

**Kyle's decision:** re-upload ALL THREE (so V2 loses its URL too) and rebuild every
poster/QR. Waiting on the three new URLs. Also unresolved from 2026-08-14: whether
the playlist keeps its URL after delete+re-upload, and the PLePG5FUoVOJI playlist ID
being 13 chars vs YouTube's usual 34.

**Session 14c — end credits enlarged + bolded (grandma's note, via Kyle)**
`_end_card_image` in common.py: credits were Songti TC **Light 34** in DIM
(128,119,105) on BG (18,15,12) — light, small, low contrast. Now **Bold 42**, line
spacing 66→80, and the NAME draws in CREAM while the role label stays DIM (colour
split was my addition on top of the ask; Kyle approved it — contrast was hurting
legibility more than size was). Matters most in the closer's shrunk state: the card
scales to 46% beside the 花絮 grid, so 34px was ~16px on screen and 42px is ~19px.
Added asserts for over-wide credit lines and for the block overflowing the card (L36).

**Targeted rebuild instead of a full one** (`scratchpad/rebuild_closer.py`, pattern
worth keeping): only end.mp4 changed, so re-extract ONLY the `CARD_end` ranges into
clips_graded and reuse the other 31 segments, then call render.py's own
`concat_segments` + `build_final_composite` rather than reimplementing the overlay
PTS shifting and subtitles-last ordering. ~10 min/video instead of ~40. Guards: fails
if a reused segment file is missing, and asserts the rebuilt closer's duration is
unchanged — the EDL timeline is frame-quantized against it, so any drift there would
shift everything downstream. Verified on V1: 11.7917s → 11.7917s, nosub 231.6243s,
unchanged to 4dp.

**14c result.** All three rebuilt and re-exported at both resolutions. Durations
unchanged to the microsecond (V1 231.624349 · V2 184.916016 · V3 173.249349).
Verified the new credits render in the actual closers at BOTH phases — card
full-frame and card at 46% beside the 花絮 grid — in the 1440p files being uploaded.
  exports/            1080p  80M / 96M / 80M   ← archival masters
  exports/upload_1440p/ 1440p 160M / 176M / 160M ← UPLOAD THESE
Both sets carry the 7 subtitle corrections and the new credits.

## Session 15 — 2026-08-18 (re-uploaded; URLs, posters, QR rebuilt)

Kyle re-uploaded all three (unlisted) after the subtitle + credits changes.
**Playlist URL unchanged** (`PLePG5FUoVOJI`), so the 33mm playlist QR on every
poster stayed valid — only the per-video QR changed.

**New URLs** (edit/urls.json)
  V1 光陰的故事  https://youtu.be/8XRNyy2YZLI   (was X_w4xc4K4mQ)
  V2 環境的影子  https://youtu.be/AN6TMhs9ON8   (was 8fX-KAuwS7k)
  V3 期望的未來  https://youtu.be/4zpehkFpT30   (was DNgJGysthdo)

Rebuilt: 3 × A4.pdf + 3 × QR.svg (make_posters.py) and exports/分享訊息.txt.
Verified INDEPENDENTLY of the build script's own decode-before-save: rasterised each
PDF at 300dpi with pymupdf and decoded with cv2 — each page yields exactly its own
video URL plus the playlist URL.

GOTCHA (cost a false alarm): first decode attempt used `sips` to rasterise, which
renders PDFs at **72 dpi**. A 33mm QR at 72dpi is unreadable, so all four pages came
back "NO QR DETECTED" — including ones known good. The probe was broken, not the
PDFs (reflect L11: verify the output shape before believing an alarming result).
Use pymupdf `get_pixmap(dpi=300)`; `sips` is useless for QR verification.

**Unrelated file found in exports/print/, NOT mine and NOT touched:**
`4_陳外科醫院_光明街_A4.pdf` + `_QR.svg`, timestamped 04:45 today. Its QRs decode to
https://ccthospital.dotsglobal.co/ and https://youtu.be/UVZ8Esm8AZA — a separate
陳外科醫院 (cct) deliverable, consistent with thumbnails/_still_cct.png,
_banner_cct.jpg and the `make_poster_cct` reference in make_posters.py. It is not in
urls.json and was not regenerated by this session's run. Left alone; flagged to Kyle.

**Deferred at Kyle's request (usage credits):** the reflect logging/convergence pass
for this session. L40 (dormant fix downstream of a transform) and L41 (bitrate is not
a quality measurement) were already written during session 14; still to do is the
convergence check and any promotion from sessions 14b/14c/15.

## 2026-08-18 — videos RE-UPLOADED (new IDs) + posters 1–3 rebuilt

**The three YouTube videos were re-uploaded, so the IDs changed.** Anything
distributed with the old IDs is dead.

    old (2026-08-14)          new (current)
    X_w4xc4K4mQ           →   8XRNyy2YZLI    1 光陰的故事
    8fX-KAuwS7k           →   AN6TMhs9ON8    2 環境的影子
    DNgJGysthdo           →   4zpehkFpT30    3 期望的未來
    playlist unchanged:       PLePG5FUoVOJI

`edit/urls.json` and `exports/分享訊息.txt` both carry the new IDs and agree with
each other — that agreement is now the check, not urls.json alone.

**Poster credit block unified across all four sheets.** Applied the staged
`make_posters.NEW.py` (original preserved as `make_posters.BAK.py`); rendering
moved to the shared `edit/build/poster_credits.py`, which `make_poster_cct.py`
imports too, so the four sheets cannot drift again. 40px→48px, step 60→66, and
the NAME is now INK while the LABEL stays MUTED. Pre-rule gap 92→74.
Verified: 9/9 LINE chrome bands identical to poster 4 (y-rows AND x-extents),
identical 6-colour palette, ink clearance 57px on the 5-line sheets (predicted
~59) and 190px on poster 4 (predicted 192).

**Delivered:** `exports/QR Code Posters/` holds all four finals; `exports/print/`
has the same PDFs plus the bare QR SVGs. Every QR decoded back out of the
DELIVERED PDFs and cross-checked against 分享訊息.txt.

**NEAR MISS — read this before the next rebuild.** `urls.json` changed at
04:48:38, midway through the task. The explicit rebuild had already read the old
file and baked the DEAD IDs into all three posters, reporting success. They are
correct now only because `dump_lossless.py` — a colour-verification script — re-
called `poster()` afterwards, re-read urls.json and silently overwrote the PDFs.
A verification step accidentally repaired the deliverable. Two reasons it slipped:
  1. The build's QR guard decodes the page against the URL it just encoded, so it
     is self-consistent by construction — it cannot detect a wrong-but-consistent
     URL.
  2. The first delivered-file check used urls.json as its oracle, i.e. the same
     source the build used. One signal wearing two hats.
Fix used: cross-check against `分享訊息.txt` (what people actually click) as an
INDEPENDENT source. Do that on every future poster rebuild.

**Still open (from WORKLOG_2026-08-18_poster4.md):** poster 4's banner repeats the
sheet's own kicker/title; its sub line 光明街　Since 1958 is mixed-script and much
wider than the other three; real credits for the Dots Global film (director,
camera, 指導單位) still to come from the film's producers; `make_posters.py` geometry is still
literals inside `poster()` rather than shared constants.

## Session 16 — 2026-08-18 (V2 second 今貌 batch)

Kyle dropped 5 more present-day photos in `IRL/hemei irl/` for V2 only.

**Mapping (from looking at the photos, Kyle described them loosely):**
  S__6840335_0  渡船 981258 on the river      → today_ferry「碧潭到和美渡船照」(his wording)
  S__6840336_0  group at the gated adit       → paired BESIDE the existing 坑口 photo
  S__6848537_0_0 / S__6848541 / S__9887751_0_0  解說牌 → today_signs, three-up

**Cards.** today_mine became a two-up `make_photo_grid_card` (existing 坑口 + the adit
shot, caption unchanged 「今日的和美煤礦坑口」) — Kyle asked for it "next to the current
pic", and a separate beat would have read as a repeat of the same subject. Two new
cards: today_ferry (single, 4.6s) and today_signs (three-up, 5.0s, caption
「和美煤礦坑口外的解說牌」— my wording, Kyle only said "解說 outside the mine").
Grid durations 5.0s follow V3's 4-photo 隧道 grid precedent.

**Order:** 坑口(2) → 新店溪與和美山 → 渡船 → 解說牌 → closer. Ferry follows the river
card because it IS the crossing she describes; 解說牌 last as the trail's own coda.

**Duration 184.916 → 194.916s (3:04.9 → 3:14.9).** SRT regenerated BYTE-IDENTICAL,
which is the proof that every new card sits after the last cam segment — cam offsets
unchanged, so no subtitle or overlay timing moved.

**`scratchpad/rebuild_changed.py`** — generalised rebuild_closer.py. Re-extracts a
range when its seg file is missing (new range, or an index shifted by an insertion
earlier in the timeline), when the existing file's duration no longer matches, or when
its source is named in --force. 12 re-extracted, 15 reused.
GOTCHA: the duration tolerance was 0.02s, but one frame at 24fps is 0.042s, so
per-segment frame quantization tripped it on 8 unchanged cam segments. Harmless (the
encode is deterministic, the output is identical) but wasteful — tolerance should be
~1.5 frames / 0.07s.

**New:** `build/make_newscenes_sheet.py` → `exports/print/新增畫面對照表_hemei.png`.
Finds each card on the OUTPUT timeline by accumulating the ACTUAL rendered segment
durations rather than the EDL's nominal ones (they drift ~0.2s over a full video from
per-segment frame quantization), grabs a mid-card frame from the delivered file, and
shows it with the on-screen caption quoted.

**CONSEQUENCE: V2 must be re-uploaded AGAIN → its URL changes again.** V1 and V3 are
untouched and keep https://youtu.be/8XRNyy2YZLI and https://youtu.be/4zpehkFpT30.
Pending: new V2 URL → urls.json, V2 poster + QR, 分享訊息.txt.

**Session 16b — V2 re-uploaded, URL/poster/QR updated.**
V2 新 URL https://youtu.be/7xoPL_1h3pg (was AN6TMhs9ON8, which was itself only hours
old — V2 was uploaded twice today: once after the subtitle+credits pass, once after
the 今貌 batch). V1/V3 untouched: 8XRNyy2YZLI / 4zpehkFpT30. Playlist unchanged.
Rebuilt all three posters + QR svgs; 分享訊息.txt updated (V2 link AND runtime
3:05 → 3:15). Kyle had replaced the three per-PDF Drive links with a single folder
link — left as he set it.
Verified independently at 300dpi (pymupdf + cv2): each poster decodes to exactly its
own video URL + the playlist URL, checked against urls.json programmatically rather
than by eye.

**Still open:** the reflect logging/convergence pass Kyle deferred; and the
PLePG5FUoVOJI playlist ID is still 13 chars vs YouTube's usual 34 — flagged three
times now, never confirmed by opening it.

**Session 16c — the shared poster folder had drifted.**
`exports/QR Code Posters/` (the folder actually shared with the professor) is a
SEPARATE copy from `exports/print/` (what make_posters.py writes). The copy was
manual, so after the V2 re-upload the print/ poster was current while the shared copy
still carried the dead AN6TMhs9ON8 QR. Kyle caught it.

Diagnosis note: md5 reported all FOUR files as differing, which looks like everything
is stale — but PDFs embed a creation timestamp, so a byte-compare between two renders
ALWAYS differs. Wrong instrument. The right check is what the QR decodes to: only
poster 2 was actually stale; 1 and 3 already pointed at the current URLs.
(Same family as L11 — the probe's answer looked meaningful and wasn't.)

FIX: make_posters.py now mirrors the posters it wrote into `QR Code Posters/` as its
last step (`shutil.copy2`), skipped on placeholder runs so a dead QR can never be
published. It copies ONLY the files it generated, so the unrelated
`4_陳外科醫院_光明街_A4.pdf` in that folder is untouched.
Verified after the change: all three in the shared folder decode to their own current
URL + the playlist URL.

## Session 17 — 2026-08-18 (consolidation: other sessions folded in)

Kyle asked to pull in the other sessions' logs before reflecting. Two other CCD
sessions ran in this project directory today, both before this one:

a "video-use endpoint" session (ended 04:33) and a "documentary poster" session
(ended 07:04).

**What they produced — a FOURTH poster for a DIFFERENT production.**
陳外科醫院 (Dots Global, © 2026), not part of 新店礦業文化路徑:
  film  https://youtu.be/UVZ8Esm8AZA  3:53, ZH+EN burned subs, uploaded 2026-02-15
  site  https://ccthospital.dotsglobal.co/
  → `exports/print/4_陳外科醫院_光明街_A4.pdf` + `_QR.svg`, mirrored to QR Code Posters/
  → `build/make_poster_cct.py`, `build/poster_credits.py`, `build/check_unity.py`
That session left `edit/WORKLOG_2026-08-18_poster4.md` as a standalone file because the
sandbox lost read access to pre-existing files under this Drive path mid-session (new
files writable, pre-existing ones not openable even for append). **Now merged into
WORKLOG.md and the standalone deleted** — content diffed identical before removal. The
permission problem did not recur in this session, consistent with their guess that it
was session-scoped approval rather than a macOS-level block.

**Their main open item is now CLOSED, by accident of ordering.** They staged
`make_posters.NEW.py` (bigger credits via the shared `poster_credits` module, the paper
inversion of the video end-card fix: on white, the NAME drops to INK while the LABEL
stays MUTED) but could not run it. The swap into `make_posters.py` did happen, so when
I rebuilt 1–3 today for the URL changes they picked up the credit fix silently.
Verified rather than assumed: measured credit ink on the delivered PDF, series sheet
ends at y=3254, 59px clear of the frame — exactly the figure their note predicted.

**Two reusable findings from their session, worth keeping:**
- **The PDF's JPEG encoding destroys exact colour.** Comparing rasterised PDFs found
  nothing because flat areas get dithered; the bugs only surfaced when they diffed the
  lossless bitmaps BEFORE PDF encoding. (Cousin of today's md5-on-PDF trap.)
- **An overflow `assert` that tests the flowed `y` does not test where glyphs actually
  land.** Theirs passed while ink sat 17px off the frame. Measure ink, not the cursor.
  My `make_subfix_sheet.py` / `make_newscenes_sheet.py` asserts have the same weakness.

**Leftovers not cleaned up** (flagged, not deleted — BAK is a safety net):
  `build/make_posters.BAK.py` (pre-swap), `build/make_posters.NEW.py` (now redundant).

**Still open, inherited from their session:** ask the film's producers for the real 陳外科醫院 credits;
the banner repeats the poster's own title type; the mixed-script sub line
「光明街　Since 1958」 runs ~628px vs the series' ~260px CJK subs.

## Session 17b — reflect pass (2026-08-18)

**Convergence.** `jl-caption-pass R1 1 · R2 1 · R3 1` — flat. Logged to
`edit/.reflect/corrections.jsonl`. Flat at 1 is not the same as flat at 7, but it was
flat for a real reason: the three corrections looked like unrelated one-offs, so
nothing got generalized between them. They are one class —
  R1 the 對照表 typeset the text instead of screenshotting the video
  R2 the real frames were too small for the one-glyph change to be visible
  R3 the poster was correct in exports/print/ but not in the folder Kyle shares
each time the artefact satisfied MY model of done rather than the audience's use.

**Promoted**
  L43 (universal) — evaluate the deliverable in the audience's frame, not the
      builder's. Open it where they open it, at the size they see it, and try to do
      the task you are asking of them. Deliverable-side counterpart to L42.
  L44 (it-ops) — encoded documents defeat byte-comparison and default rasterisation:
      md5 on PDFs always differs (creation date), `sips` rasterises at 72dpi so QR
      decode fails, PDF JPEG dithering destroys flat colour. Compare semantics; choose
      the DPI; diff pre-encode bitmaps. Covers three false readings from today across
      two sessions.
  L36 (video) — STRENGTHENED rather than duplicated: assert on the INK, not the
      layout cursor. Both sheet generators had the weak form; poster 4's passed while
      ink sat 1.4mm off the frame.
  L42 (universal) — added a Seen: it RECURRED hours after being written. I decoded the
      posters' QRs and compared them to urls.json — the same file the build read. The
      check felt independent (different tool, different format, separate script) and
      was not. The test is whether the expected value came from a different SOURCE.

**Meta.** Writing L43 into universal.md, my own edit consumed the `### L43` heading
and left the body dangling under L42. Caught by grepping the ID inventory afterwards
instead of trusting that the append worked — which is L43 applied to L43. Added a
structural check (every entry has Context/Rule/Scope): all four files pass, no
duplicate IDs. Router counts corrected (it-ops was understated by 2). Next free ID
is now L45.
