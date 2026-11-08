# Action game (Dimraeth-like) — progress log

Owner direction 2026-11-08: a top-down pixel action RPG like Dimraeth, built around CLASSES (อาชีพ) instead of the legends.
Outfits change by recolouring (free); new outfit shapes later with PixelLab `transfer_outfit` (paid tier).
Reference clips the owner sent: Dimraeth trailer (one sword swing ≈ 5–6 poses at ~12 fps, characters ~32 px tall,
big white slash arcs drawn apart from the sprite) and a real-time monster-battle fan game (almost no character
animation, skills fire instantly as big effects, telegraph rings, a dodge button) — owner: "ไม่สวยแต่รวดเร็ว".

## Decisions
- Canvas 128 px (owner chose 128 after seeing 64 vs 128 side by side; figure ~118 px tall).
- 8 directions in the game. Default plan: animate 5 (south, south-east, east, north-east, north) and mirror the
  rest; mirroring puts a one-handed weapon in the other hand (owner told; not decided yet).
- First class: dagger rogue, a young woman. Rank 1 holds ONE dagger (right hand); rank 2 holds two (needs new moves).
- Normal attack = 2 hits (owner 2026-11-08).
- New characters: design in ChatGPT first (turnaround front / side facing right / back on white, neutral standing
  pose, arms a little away from the body, weapon held low), convert locally, show the owner, and only then PixelLab.
  Never start a PixelLab job without the owner's plain go.

## Files
- `art/incoming/action/rogue/turnaround_gpt.png` — the owner's GPT turnaround (1448×1086).
- `art/incoming/action/rogue/turnaround_cut.png` — white cut (`white_cut.py --edge-only --no-ring`).
- `art/incoming/action/rogue/px128/{south,east,north}.png` + `preview.png` — `tools/art/turn128.py` (one shared scale,
  figure 118 px tall, 32 colours, 1 px outline, feet 4 px above the bottom). south = front, east = side, north = back.

## PixelLab log (do not regenerate what is listed here)
| date | what | id | cost | result |
|---|---|---|---|---|
| 2026-11-08 | create_character v3 128 from a text description ("Dual Dagger Rogue 128") | 15471b83-0238-4cd9-99dc-1c0452b29133 | 1 (cancelled at once) | nothing — started by mistake before the GPT design; ignore |
| 2026-11-08 | create_character v3 "Dagger Rogue 128": reference = px128/south.png, direction_images east + north (ours), PixelLab draws west + 4 diagonals | fbbd1333-71e1-46a9-85f2-2ea35b2affca | 2 | ✅ all 8 views good, dagger stays in the RIGHT hand in every view (west hides it behind the body); saved in `art/incoming/action/rogue/pl_rot/` + `_preview.png` |
| 2026-11-08 | animate_character pixminimax 8 frames, east only, "attack_2hit" (forward slash + backhand slash, back to stance) | group 4923405d-94db-47e3-89dc-9d0c42582e98 | 1 | done — canvas 172×172, 9 frames incl. the reference (`pl_dl/Idle/animations/attack_2hit/east/`, sheet `attack_2hit_east_sheet.png`, gif `attack_2hit_east.gif`). Hit 1 = forward thrust (frames 2–3) good; hit 2 (frames 4–6) sweeps BEHIND her to the left and her body turns toward the camera — waiting for the owner: keep as a spin slash or redo | owner: "ไม่ชัดเลย" → redone below |
| 2026-11-08 | animate_character pixminimax 16 frames, east, "attack_2hit_b" (owner: slash left-right there and back, whole body + legs moving): step + forehand sweep in front, second step + backhand sweep in front, settle | group 8bc94204-f588-4a93-8feb-60156d39633d | 1 (16 frames billed 1 at 128) | ✅ much better: 17 frames, hit 1 = horizontal sweep on frame 4, hit 2 = big sweep on frame 9 (PixelLab drew its own blade smears anyway, they look good), legs step and widen; frames 5–8 are almost the same wind-up pose (skip 6–7 in the game to keep it snappy); 10–12 follow-through over the shoulder, 13–16 back to standing. Previews `attack_2hit_b_east{,_slow}.gif`, `_sheet.png` (`tools/art/pl_preview.py`) |
| 2026-11-08 | same group, the other 7 directions one at a time (owner "ทำเลย"); prompt = east's with "facing <dir>" instead of side view | group 8bc94204-f588-4a93-8feb-60156d39633d | 1 each (7) | all done. Hits found by width (`act_sheet.py`): E 4,9 · SE 4,7,10 · S 3,8 · SW 3,6,10 · W 3,9 · NW 3,5 (by hand `--hits=north-west:3,5`) · N 4,8 · NE 3,6. Quality: SE / S / SW turn left-right between swings (reads as a flurry, OK); W turns to face right in frames 4–7 (reads as a spin); **N and NE are wrong: she turns round to face the camera mid-attack**. NW used a much firmer back-view prompt ("seen from BEHIND for the whole clip … she NEVER turns around … her face is never visible") and kept her back to the camera → use that wording for back views; redo N and NE with it (2 credits, waiting for the owner) |
| 2026-11-08 | redo N then NE with the back-view wording, new animation "attack_back" (owner: "หน้ากับหลังใช้คำสั่งแยกก็ได้") | group 3113d083-9ed6-42b5-b299-bba6daf42df1 | 1 (N only) | N redo: no longer faces the camera but still turns side-on mid-attack — better than the first, used. NE NOT redone: the game mirrors NW (clean back view) instead (`--skip=north-east`). Owner found SE / SW odd (she turns left-right between swings) and W turns mid-attack → they now play the clean east clip (`--alias=south-east:east,south-west:east~,west:east~`, ~ = mirrored). Then (owner "แก้บนด้วย") N once more as "attack_back_v" (group 43d9d3be-e7d8-4a44-93f4-1f7f63e25bc1, 1 credit): VERTICAL cuts (overhead chop down, then a rising slash) so she has no reason to turn side-on to show the blade. ✅ worked: back view kept, overhead raise (4–5), chop smear (6), big rising slash (11). Then NW the same way (same group, 1 credit; NE mirrors it) ✅ back view kept, chop on 6, rising slash 9–10. Current build: `python tools/art/act_sheet.py art/incoming/action/rogue/pl_dl/Idle art/action/rogue.png attack=attack_2hit_b,attack_back,attack_back_v --skip=north-east "--alias=south-east:east,south-west:east~,west:east~" "--hits=north-west:6,9;north:6,11"`. Old account balance after: 1.25. Owner then: trial key used up → switching to their other PixelLab key. **Next account plan:** the character lives in the old account, so import it into the new one: `create_character` mode v3, reference = `art/incoming/action/rogue/pl_rot/south.png`, `direction_images` = the other 7 files in `pl_rot/` (an import, 0.25), then walk 8 frames × 8 directions (8 credits; firm "seen from behind, never turns" wording for the back views). Build command (before the vertical redos): `python tools/art/act_sheet.py art/incoming/action/rogue/pl_dl/Idle art/action/rogue.png attack=attack_2hit_b,attack_back "--hits=north-west:3,5" --skip=north-east "--alias=south-east:east,south-west:east~,west:east~"` |

Balance after: 1.25 of 40 (first trial key, 2026-11-08, all attacks done). The owner switches to another key next.

### Second PixelLab account (owner's other key, from 2026-11-08)
The app kept the old key until restarted, so jobs go through `tools/pl_rpc.py` (HTTP JSON-RPC with the key from the
user env var, never printed; `--upload` for images). Balance at start: 40 + 20 daily bonus (refills +5 a night, up to 20).
| date | what | id | cost | result |
|---|---|---|---|---|
| 2026-11-08 | import "Dagger Rogue 128": all 8 views from `pl_rot/` (the first account's PixelLab rotations) | 6f024d02-2df1-4fb1-aaae-43922ac724ce | 0.25 | ✅ "nothing generated"; downloaded back to `pl2_rot/` and compared: all 8 views identical to `pl_rot/` (0 pixels differ) |
| 2026-11-08 | NW attack redo "attack_ul" (owner: the upper diagonals still had one sweep + a stab): two wide SIDEWAYS sweeps, seen from behind, never facing the camera; NE mirrors it | group d9721383-636b-4fb0-9421-c5b2feab6d6e | 1 | ✅ owner chose it ("B") over attack_2hit_b NW: NW = attack_ul, NE = its mirror (`rogue_build.sh`) |
| 2026-11-08 | base moves, owner "เอาทุกอย่างที่ใช้เจนไป ยกเว้นสกิล": run 8f ×8 (loop, keep_first_frame off), idle 8f ×8 (loop), roll 8f ×8, hurt 4f ×8, death 8f ×4 (E S W N) — 36 jobs from `art/incoming/action/rogue/jobs_base.json` via `tools/pl_queue.py` (one at a time, ZIP into `pl2_dl/` after each, log `pl2_dl/queue.log`, group ids `pl2_dl/groups.json`; rerunning skips what is downloaded) | see groups.json | 36 (3.75 + daily bonus left) | ✅ all 36 done 15:13–15:49; dust puffs beside the run / roll are cut by `act_sheet.py` (`dedust`: small or pale separate blobs). In the game: idle loop 7 fps, run loop 13 fps at speed 230, roll 0.4 s, hit 0.28 s, death 0.9 s (nearest of E S W N) |
| 2026-11-08 | dash cut for skill 4 (`jobs_dash.json`): crouch, low lunge, slash, follow-through; E S N NW, 8 frames | group 1c6f5ef3-04e7-4e97-97c4-93dfbab67f9f | 4 | E good; S and N turned side-on / to the camera, so the game plays E (mirrored) for every direction |
| 2026-11-08 | skill moves (owner "เจนมาเลย"), `jobs_skills.json` via `pl_queue.py` (log `pl2_dl/queue_skills.log`): spin 16f south · bomb (lob a bomb with the LEFT hand) 8f east, south, north, north-west | spin d8158151-c872-4016-ae19-02844bacbe4b · bomb 512ebe0e-3e33-476b-bd3b-5467d242c0c7 | 5 (1985 left of the 2000 subscription) | ✅ spin: side crouch wind-up 1–4, turns 6–8 with a white ring PixelLab drew itself (kept, recoloured + glow like the attack), back to front 9–16. bomb: E / N / NW clean lobs; S drops the bomb at her feet instead of throwing (fine: the flying bomb is drawn by the game and `dedust` cuts PixelLab's loose bomb) |
**Back views (N, NE, NW): ask for VERTICAL cuts** (overhead chop, rising slash) plus "seen from BEHIND … never turns … face never visible"; sideways swings make PixMiniMax turn her side-on or toward the camera.
Download the ZIP only between jobs (`/mcp/characters/<id>/download` answers "still being generated" while a job runs).

**Owner 2026-11-08 after the vertical redo: "ไปแก้ฟันบนทำไม เอาอันเก่าเลย … มันฟันไม่เหมือนกัน"** — the vertical chops
did not match the sideways slashes of the other directions, so the attack is the FIRST run (`attack_2hit_b`) in N, NE, NW
again (they turn a bit, accepted); the vertical chops are kept as `chop` (N + NW) for a skill later. Lower diagonals + W
still play the east clip. Build: `bash tools/art/rogue_build.sh` (writes `art/action/rogue.json` + one PNG per move).

Blade arcs: PixelLab painted each direction's arc its own colour (white, beige, cyan); `act_sheet.py smear()` repaints every
pixel that is not a colour of the stills and is light or bluish onto one cream-white ramp (owner "ทำสีให้เหมือนกันทุกทิศ").
Hit effects (owner "ใส่เอฟเฟคให้เหมือนเกมต้นแบบ"): pixel impact star → ring → sparkles at the hit point (`starFrames`, big on
the last hit), slime splat on a kill (`splatFrames`), a 16% white screen flash + camera kick toward the swing on the last hit,
run dust, roll after-images that copy the roll frame. Slash wave (owner "ทำคลื่นฟันให้สวยๆ ใช้กับทุกทิศ"): `waveFrames(dir, R)`
= a pixel crescent on the ground plane (y ×0.6) drawn per direction (no runtime rotation), 4 frames, white cutting edge, a
cream trail that fades out in Bayer dither, sparkles at the end; on every swing (`doHit`), bigger on the last hit.
Then (owner "ไม่ต้องทำมาซ้อน" + "สีฟันคนละสี ทำให้อยู่โทนเดียวกัน"): the code wave is OFF (kept in `waveFrames` for skills); the
arcs INSIDE the attack frames are made white instead: `act_sheet.py arcwhite()` (on a swing frame, light pixels outside the
nearby narrow frames' silhouettes grown 3 px, blobs ≥ 30 px, then grown into light pixels that were dark in the nearest
narrow frame, never into the top 30% = the head) + `smear()` (non-still colours), both onto one white ramp `SMEAR`.
**Longer dagger (owner asked): not possible in code** — the blade uses exactly the skin colours (246,215,191 / 214,185,159 /
173,147,123), so it cannot be picked out; a longer blade means regenerating every move (~50 credits). Plan: order longer
blades in the GPT design of rank 2 (dual daggers).

Glow + reach (owner sent a clip of strong glowing golden arcs, "สีแรงแสง", and "ระยะฟันมันสั้น"): `act_sheet.py --arc=air|gold|white`
picks the arc ramp; the attack gets `rogue_attack_glow.png` (arc pixels blurred) that the game adds with 'lighter'; a see-through
air blade (`airFrames`, colours from `META.arc`) flies on from each hit (760 / 900 px/s, damping .965) with a soft glow
(`glowSprite`/`glowAt`), white-warm glow on impacts; reach 180 / 230. Owner still to choose A gold or B air (built: air).
Bigger world (owner: "ไม่อยากลดตัวละคร เดี๋ยวเบลอ ก็ขยายแมพ สิ่งก่อสร้าง ให้ใหญ่ ให้ตัวละครดูเล็ก" — the 2x2-merge far camera
was tried and dropped): field 4200×2800; `makeProps` = sprite props drawn in the depth pass (fade to 45% when the rogue
stands behind) with baked ground shadows and solid bases (`blockProps`: ellipses, building footprints `rect`): huge trees
(`bigTree`, ~3× the rogue), boulders, tall ruined pillars, a hamlet of 4 cottages (`house`) and 2 ruined watchtowers (`tower`).

Then (owner): air blade OFF ("ไม่เอาใบมีดลม"), reach back to 125 / 150 × `META.k`; rogue shrunk to 80% at build time
("ย่อตัวลงหน่อย ... ตัวมันสูงไป", owner checked a 100%/80% comparison for blur and chose 80): `act_sheet.py --scale=4/5`
(each output pixel = the most common colour of the area it covers, a dark outline wins at ≥30%; cells padded to a multiple
of 5 → cell 140, feet 70/118, `k` 0.8 in the json); wider waves ("ทำคลื่นฟันให้กว้างกว่านี้"): two faint see-through bands
round every outside arc (3 and 6 px, the outer one dithered) and a wider glow.

Owner's play clip 2026-11-08: every J attack swung toward the mouse cursor left at the top while the slime came from below →
aim: a mouse click aims at the mouse, J / the touch button auto-aim at the nearest slime within 260 (else the walk direction);
the hit blink is now 45% see-through instead of vanishing. The wave bands looked like a leftover white frame → one 2 px band in
the arc's own edge colour/alpha.

Owner: "สีขาวตอนกดฟัน 2 เหมือนเอา bg ออกไม่หมด" → the 16% white screen flash on the last hit is gone (camera kick stays), the
slime hit/warning flash is a 55% white overlay instead of a solid white silhouette, the hit glow is smaller/softer (smoothed).

Owner's screenshot (two red lines either side of her while attacking): the glow layer's faint tail filled the whole cell and
stopped at its border → `act_sheet.py` now blurs the glow one cell at a time, cuts the faint tail (< 8%) to zero and fades
it out over the last 14 px before each cell edge (every cell border is 0).

### Map art (owner subscribed: Tier 1 Pixel Apprentice on the second account, 2,000 generations, reset 2026-12-08)
The code-drawn map was judged poor ("ฝีมือการทำแมพกากมาก"); the lake / stream / hamlet code is in action.html but the owner
wants real art. Plan: props from PixelLab `create_object_pro_flash` (view low top-down, style_image = the rogue's
south-east still so pixel size / outline / shading match; 5 gens ≤96 px, 6 ≤208, 9 ≤256) or GPT (owner's choice after an
A/B test), ground from `create_topdown_tileset` mode pro view low top-down (15–25). Map tools themselves are free.
| date | what | id | cost | result |
|---|---|---|---|---|
| 2026-11-08 | ground test: create_topdown_tileset STANDARD 32 px, dirt path (lower) → grass (upper), flat (owner "ลองเจนสแตนดาดู 1 เครดิต") | tileset 97dd7c79-104f-4869-876b-01916a17558b (bases: dirt 12ee2be9…, grass 7f7aa800…) | 1 | (pending) |
| 2026-11-08 | test oak tree 208×256, pro flash, 1 direction, style = rogue south-east (upload) | object 3a6ec4fc-ec37-4509-a868-0d76313be787 | ~9 | done (`art/incoming/action/map/pl_oak_test.png`, tree ~155 px tall): darker and flatter than the GPT props |

A/B 2026-11-08: the owner's GPT sheet `gpt_nature.png` (oak, pine, blossom, bush, boulder, rocks, grass, flowers; prompt 1 in
this chat) → `white_cut.py --edge-only --no-ring` → `tools/art/props_px.py <cut> art/incoming/action/map/gpt_px 0=282 32
oak,pine,...` (one scale so the oak is 3× the rogue, each prop only its own blob, a palette per prop, 1 px outline) looks
clearly better than the PixelLab tree → map props from GPT. Owner on monsters: normal monsters frame by frame from GPT
like before (free); only bosses through PixelLab. **Decision (owner 2026-11-08 "เจน gpt แหละ pixellab เอาไว้ทำตัวละครหลังที่
เน้นควบคุมกับเอฟเฟค"): map + monsters from GPT; PixelLab only for the playable characters (controls) and skill effects.**
In the game: `art/action/props/<oak|pine|blossom|bush|boulder|rocks|grass|flowers>.png` replace the code trees / boulders /
pillars / grass clumps (`GPROP` in action.html, random horizontal flips); houses + towers stay code-drawn until the GPT
village sheet (prompt 2) arrives.

Ground + village (owner 2026-11-08): the 1-credit PixelLab standard tileset (grass ↔ dirt, 32 px) looked flat with stair-step
edges ("ไม่สวยเลย") → GPT ground textures `gpt_ground.png` (grass, dirt, sand, water, cobble, flower grass) →
`tools/art/ground_px.py <sheet> <out> 0.44 20 names` (scaled to the props' detail, made seamless by cross-fading with the
half-shifted copy, 20 colours; flower grass 40) → `art/action/ground/*.png`; `makeGround` samples them per pixel (`TEX`, `tx`)
times a big soft light/dark patch, ragged dithered edges between terrains, darker deep water, flower grass in the meadows;
the code ground is only a fallback. GPT village sheet `gpt_village.png` → `props_px.py ... 0=228 20 house_red,house_blue,
tower,well,fence,barrel,crate,lantern` → `art/action/props/`; houses / fences block as boxes (`GPDEF.rect`), houses are not
mirrored. Owner "เบาๆ ต้นไม้หน่อย": about half as many trees, bushes and grass clumps.

Bigger (owner 2026-11-08 "สิ่งก่อสร้างขยายได้อีกไหม", then "ให้ดูตัวละครเล็กลง ขยายแมพอีก มุมกล้องสูงอีก"): houses and the
tower re-cut 1.5× (`props_px.py ... 0=340`: house_red 330×342, house_blue 316×304, tower 272×418; footprints in `GPDEF`);
rogue 2/3 at build time (`rogue_build.sh --scale=2/3` → cell 116, feet 58/99, `k` .667; reach follows `META.k`); world
6000×4000 (`AR` = area vs the old 4200×2800, prop counts follow it; lake 1.35×, a longer stream, 7 meadows, 3 towers).
One 6000×4000 canvas is too big for phones, so the ground is painted in 512 px chunks (`CHUNKS`): `terr(x,y)` = what is at a
point (sets `TK`/`TA`/`TB`, path / stream widths cached per column / row in `PYC PWC SWC`, `streamD` skips far segments
`SEGB`), `groundPx` = its colour from the textures, `chunkStep` paints 16-row bands, then lily pads / reeds (`GND.deco`) and
the props' ground shadows (`PROPS[].shades`); `drawGroundChunks` draws what is on screen (paints a missing one at once) and
spends ~4 ms a frame on the nearest unpainted chunks in the ring round the view; far chunks are dropped above 60. The
walking water map `WATER` is worked out for the whole world in `setupGround`. Load paints only the start view (~0.5–1 s on
the PC); walking across the map: median 0.3 ms, 1 frame of ~675 over 16 ms. A "higher camera" can't be done with the
low-top-down art: the same feel comes from the smaller rogue (on a DPR-3 phone the screen shows 1170 world px of height,
she is ~1/17 of it).

Zones (owner 2026-11-08 "ทำแมพต่อ", free, existing art): `FORESTS` = two thick forests (north-east round the NE tower,
south-west; `forestF` > 0 inside): trees every ~118 px (pines first), bushes / rocks / grass under them, darker ground
(×.74, dithered edge), no flower grass, no random field trees near them; `RUINS` = broken cobble floor round the south tower
(kind 7: round grass patches from a sine pattern, dithered edge) ringed by boulders and rock piles; `SIDE` = 3 side paths
(Catmull-Rom `crv`, `sideD` with per-segment and per-path boxes) from the road to the three `TOWERS`; meadows moved out of
the forests. `ZF` = 32 px cells near a side path / forest, so most pixels skip those checks (`terr` 18 ms per chunk).
`?test=map` draws the whole world shrunk onto the screen (`drawMap`; picture `art/incoming/action/map/overview.png`).
Owner after playing: "เอาหญ้าออก ต้นไม้ใหญ่กว่านี้" → grass clumps gone (only flower clumps in the meadows); oak / pine /
blossom re-cut 1.5× (`props_px.py gpt_nature_cut.png <out> 0=423 20 oak,pine,blossom,bush,boulder,rocks,grass,flowers`,
only the three trees copied: oak 389×425, pine 275×446, blossom 274×324), trunk radii 30 / 24 / 22, edge trees every
320–470 px, forest trees ≥165 apart, field props ≥430 apart (the spacing, not the count, decides how thick the field is).
Town (owner 2026-11-08 pasted two GPT sheets: the ruins/forest/camp sheet from `PROMPT_ruins_forest.txt` and an
18-building sheet; pasted pictures come in the transcript as an `attachment` / `queued_command` line, saved as
`gpt_ruins.png` / `gpt_buildings.png`): ruins sheet `white_cut.py --no-ring` → `props_px.py ... 0=130 20
wall,wall_corner,arch,statue,pillar_down,pillar,rubble,stairs,stump,log,mushrooms,fern,dead_tree,mossy_rock,campfire,tent,
signpost,cart` (dead tree again at `12=330`) → `gpt_rpx/`; buildings sheet `white_cut.py --edge-only --no-ring`, then each
building moved into its own grid cell with gaps (`gpt_buildings_spaced.png`; neighbours touched and were read as one) →
`props_px.py ... 0=340 20 cottage_red,cottage_blue,cottage_thatch,guild,shop,healer,smithy,alchemist,library,armory,barn,
windmill,chapel,townhall,observatory,greenhouse,magetower,watermill` → `gpt_bpx/`; all copied to `art/action/props/`.
`GPDEF`: buildings `bld` (footprint 78% wide × 70, never mirrored), arch walk-through with a shadow (`shade`), dead tree
`tree` (canopy shade). Layout: `HAMLET` grown to 980 × 640 = a town round the well (`TOWN` slots: town hall, chapel,
library, shop, smithy, alchemist, guild, healer, armory, cottages; a slot too close to the road is skipped by
`roadClear`), a farm east of it (barn, windmill, greenhouse, thatched cottage), a watermill on the stream, a wizard's
corner north-west (mage tower, observatory); ruins `RUINS` 480 × 300: an arch where the side path comes in flanked by two
statues, walls, pillars, rubble, stairs, three dead trees round it; forests get ferns, mushrooms, stumps, logs, mossy rocks,
dead trees; a camp east of the lake (tent, fire, log, cart, barrel, crate); a signpost where each side path leaves the
road; fences keep out of buildings. Prompts waiting for the owner: `PROMPT_trees.txt` (16 trees), `PROMPT_thai_city.txt`
(old Thai capital: 18 buildings, 18 props, 6 ground tiles; attach `gpt_buildings.png`).
Earlier prompt: GPT sheet `art/incoming/action/map/PROMPT_ruins_forest.txt` (ruin walls, arch, pillars, rubble, stairs, statue,
stump, log, mushrooms, fern, dead tree, mossy rock, campfire, tent, signpost, cart; attach `gpt_village.png` for style).

## Skills (design in progress, owner 2026-11-08)
Proposed shape (owner asked "เอากี่สกิลดี"): 4 skill buttons on screen at once (room for thumbs round the attack button on a
phone) + attack + roll; about 8 skills per class to unlock up to level 50, the player picks which 4 to carry.
- **Skill 1 — throw dagger (owner):** throw at a spot on the ground (aimed area, not a target); if it hits a monster, the
  skill can be pressed again within 5 s → she appears BEHIND that monster. Built (free, no PixelLab): Q / 1 on PC (aims at
  the mouse), button ปา on phones (aims at the nearest slime in range, else straight ahead). `SK1` (range 380, area r 46,
  18 damage, stamina 18, cooldown 6 s, mark 5 s); the throw pose = the attack's second swing (owner "เอาคลื่นก็เหมือนปาแล้ว":
  `throwPlan` plays from 2 frames after the first hit to 4 after the last, the dagger leaves on the big arc; then owner
  "เอาคลื่นฟันออก": drawn from `makeNoArc(sheet)` = see-through arc pixels and the solid ramp colours removed, holes over
  the body filled from the neighbours, the arc's thin dark outline cut, no glow); `G.knives`
  fly in a slight arc with a ground shadow and stick in the ground; the monster nearest the landing spot gets `p.mark`
  (purple ring + arrow); the button turns purple "วาร์ป" / "Q!"; `blinkBehind` = after-image streak, purple puffs, she lands
  on the far side facing it (sides / stays put if that is water), .3 s i-frames. The flying dagger is a few code pixels
  (`drawKnife`) until the GPT dagger sheet arrives (`art/incoming/action/skills/PROMPT_dagger.txt` + `ref_rogue_dagger.png`:
  8 directions, 4 spin frames, 3 stuck-in-ground frames). Tests: `?test=sk1` (in flight), `?test=sk1b` (after the warp).
  Then (owner "มีดทำอันใหญ่กว่านี้นิด กำหนดระยะช่องสกิล มีดตอนปาทำแสดงด้วยจะได้เห็น"): aiming — hold Q (aims at the mouse)
  or press the ปา button and drag (70 css px = full range; a tap auto-aims), let go to throw; while aiming a dashed ring
  shows the longest throw, dots lead to a yellow circle where it lands (`AIM`, `aimStart`/`aimEnd`, `skTarget`,
  `ringSprite`, `?test=aim`); with the mark up a press warps at once. The flying dagger is ~30 px with a light streak and a
  soft glow, flies a little slower (900 px/s); the stuck one is bigger.
- **Skills 2–4 (owner 2026-11-08, "เจนมาเลยจาก pixellab"):** E / ปุ่ม หมุน = **spin slash** (PixelLab `spin`, south only —
  a spin looks the same from anywhere; played as wind-up, two turns with hits on both, recover; 2 × 13 to everything within
  108; she can drift; usable straight out of the throw or the warp = the owner's combo throw → warp behind → spin).
  R / ระเบิด = **smoke bomb** (PixelLab `bomb`, E S N NW, rest mirrored/aliased; aimed like skill 1, range 340; a high lob,
  blast r 96, 12 damage, **blind** 4 s: blind slimes hop at random, aim their lunges off and miss half the time; grey smoke
  circles their heads; `smokeSprite` cloud). F / พุ่ง = **flurry** (owner asked whether a vanishing move needs 8
  directions — no: no new moves at all): aim at a monster (range 300, red ring on it), she vanishes and cuts through it
  6 times 150° apart (`streak` fx + crescent + attack-frame after-images), 6 × 9 + 8, invulnerable, moves on to a monster
  close by if it dies, lands behind it. Cooldowns 5 / 9 / 10 s; costs 15 / 20 / 25 stamina. Phone: 4 skill buttons in an
  arc round ตี / กลิ้ง; PC: Q E R F (or 1–4) with squares under the bars. Tests `?test=spin|bomb|bomb2|flurry`.
  Spin redone (owner "หมุนตัวไม่สวย ... ดูแข็งไม่มีพลัง", "ให้มีระยะกว้างหน่อย"): PixelLab's spin only turned half way and played twice
  looked like twisting, so it is no longer used: she turns through the 8 directions twice (`SK2.step` 30 ms, the attack's
  swing frame of each direction with its arc + glow, after-images), wind-up 70 ms, settle 90 ms, hits at the end of each
  turn, reach 140; a PixelLab VFX `spin_slash` ring (size 2.8, air colours; My effects "rogue_spin_ring" 034322c3…,
  game pack → `fx/spinring_b.png` behind her + `fx/spinring_f.png` in front, `drawPfx` with `follow`/`depth`) at the
  start of each turn; a ring of dust at the feet. `?test=spin&n=<steps>`.
  Owner "เอฟเฟกต์ทำใสหน่อย มีแสง": `fx/<key>_glow.png` = a blurred, tinted copy of an effect (12 px padding, light cyan;
  lavender for nslash) for spinring_b / spinring_f / nslash; `drawPfx` draws such effects at 78% and adds the glow with 'lighter'.
- **Skill 4 redone like Murad's ultimate in ROV** (owner: "สกิล 4 ไม่สวยเลย" + a GPT pose sheet, then a clip of Murad, "พุ่งฟัน 5 ที"):
  aim at a spot (range 320); a see-through cyan field opens on the ground there (`fieldSprite`, an ellipse r 140 × .6, four
  opening steps, glow, glints round the rim); she dashes across it 5 times in a pentagram (`nextCut`, 144° apart) with the
  PixelLab `dash` move (generated 2026-11-08: E S N NW, group 1c6f5ef3-04e7-4e97-97c4-93dfbab67f9f, 4 generations; only the
  side view kept its facing, so every direction plays east / mirrored: crouch 2, lunge 3–4, slash 5 with its arc + glow,
  follow-through 6), after-images on the way, a cyan streak per pass, every monster in the field hit each pass (5 × 9),
  then a cyan burst in the middle (16, VFX `crit_hit` recoloured cyan = `fx/dashhit.png`) and she ends at the edge; a
  VFX `charge_up` (`fx/dashcharge.png`) at the start. Invulnerable throughout.
- Bomb blast (owner "ระเบิดเปลี่ยนเอฟเฟกต์ ใส่ระเบิดกับควันให้เข้าสกิล ตาบอด"): VFX `cartoon_boom` + a dark `smoke_puff`, ×1.85,
  1.5 s (My effects "rogue_smoke_bomb") → `fx/smokebomb.png` via `tools/art/vfx_import.py`.
- Skill effects (owner "สกิลได้ไปเอาจาก vfx ในpixellab ไหม" → "pixelfx อันนี้เราเคยใช้" → "ถ้าไม่มีก็เจนจาก pixellab"):
  pixelfx sheets already in `fx/` (bb.html) are loaded by action.html (`PFX`, `pfx(key, x, y)`, fx kind `pfx`): `darkx` =
  the smoke bomb's blast (the code `smokeSprite` stays as a fallback), `poof` = warp / flurry vanish and return, `nslash` =
  every other flurry cut. Missing in pixelfx → PixelLab **vfx_workbench (free: nothing generated, nothing charged; you
  build from parts and look at the frames)** through `tools/pl_rpc.py` (replies' pictures saved when `PL_IMG` is set) +
  `tools/pl_get.py` (downloads the exported gif / json / png): `stun_stars` recoloured grey-lavender = blind status,
  exported as "rogue_blind_stars" (My effects 5d41ccb5-d17a-44f9-a91b-8019d570a2de, raw in `art/incoming/fx_raw/
  rogue_blind_stars/`) → `fx/blindstars.png` + manifest entry, looped over blinded slimes. Its ready "dagger" throw was
  tried (`throw image dagger spin 2`): only 14 px long, smaller than the code dagger the owner asked to be bigger → not used.
- Effects: PixelLab VFX Creator (owner's screenshot, "Slash arc" preset: sweep / thickness / size / angle / trail / speed /
  frames sliders; the chat "Send" costs 1 generation) → export "For a game (ZIP)" → `pixellab_import.py` (from bb.html).

## Game: `action.html` (prototype, 2026-11-08)
One file. Bright meadow painted in code at 1 world px = 1 art px (`makeGround`: diamond tiles, grass tones with Bayer
dither, dirt path, tufts, flowers, rocks, bushes, a ring of trees), whole-number screen scale `S` (about 560 world px of
height on screen). Sprite sheet `art/action/rogue.png` + `.json` from `tools/art/act_sheet.py` (row 0 = 8 stills, then the
attack per direction; `hits` per direction). Rogue: 8-direction walk (still picture + 2 px bob, no run animation yet),
attack = the direction's own frames, hits from the json (2 hits 12+20, 3 hits 10+10+15), hit-stop, shake, sparks,
pixel damage digits, pixel arc; roll (Space / right click / K) 0.32 s with i-frames and after-images; stamina (attack 15,
roll 26, regen after 0.6 s). Mouse aims on PC; on phones a left-side stick, buttons ตี / กลิ้ง and auto-aim to the nearest
slime. Slimes (code-drawn pixel sprites, green / blue from wave 3) hop, then warn (flash + red ring) and lunge.
`?test=atk&dir=N` freezes on the last hit for screenshots (headless Edge: `msedge --headless=new --screenshot=...`).
Next: run animation, roll animation, redo N/NE attacks, then levels / map (owner asked about a leveling map).
