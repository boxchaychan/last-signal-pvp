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

| date | what | id | cost | result |
|---|---|---|---|---|
| 2026-11-09 | create_character v3 "Berserker 128" (cloud session, this same trial account; owner "เอาให้หมดก่อน" = use this account up first): reference = `berserker/px128/south.png`, direction_images east + north (ours), PixelLab drew the other 5 | 0e6da505-2c74-479e-bb52-1b6c01659dfe | 2 (+5 daily bonus) | ✅ 8 views good (`berserker/pl_dl/Idle/rotations/`, `pl_rot_preview.png`): south-east holds the sword upright behind the right shoulder (foreshortened) |
| 2026-11-09 | 3 attacks, PixMiniMax 8 frames, south-east only (`berserker/jobs_attack.json` via `pl_queue.py`): `bz_sweep` horizontal sweep · `bz_spin` 360 spin (Q's second press) · `bz_slam` overhead slam into the ground (R, E's third cut) | sweep dc5cf88c-993d-4ed7-a65c-cb2f0bee0b1a · spin cea10df2-939a-437d-985c-b016ba8cede3 · slam 020e63c9-d4c9-4312-938a-3ae82057d1c8 | 3 | ✅ all good (`attacks_se.gif`, canvas 172): sweep = wind-up 1, a big black-red arc PixelLab drew itself on 2, follow-through 3–6, back on the shoulder 7–8 (9 frames); spin = draw back 1, side 2, back view 3, other side 4, front 5, stance 6–7 with blade arcs on 2–3 (8 frames); slam = raise overhead 1–3, blade into the ground with cracks on 4–5, pull out 6–7, shoulder 8 (his helm reads rounder while he looks down, 4–7). Account empty after this (43.75 used = 40 + the 5 daily bonus) |
| 2026-11-10 | create_character v3 "Guardian 128" (cloud, trial account, owner "ทำพวก pixlab ... ก่อน"): reference = `guardian/px128/south.png` (turnaround front), direction_images east = `side_right.png` + north = turnaround back (`white_cut --no-ring` → `join_views.py` → `turn128.py 128 32`) | a468e926-b5aa-4692-aa27-15b00a3c67c2 | 2 | queued (~20 min wait on the trial account) |
| 2026-11-10 | 3 attacks, PixMiniMax 8 frames, south-east (`guardian/jobs_attack.json` via `pl_queue.py`, run after the character): `gd_slash` forward slash · `gd_bash` shield bash · `gd_overhead` overhead chop | (see `guardian/pl_dl/queue.log`) | 3 | running |
| 2026-11-10 | PAID account (Apprentice, cloud key fixed): imports `Guardian 128 paid` 4577584b… + `Berserker 128 paid` eac57807… (0.25 each, our 8 rotations) and their base moves (`jobs_base.json` 36 each + Berserker `jobs_skills.json` chain) → `<hero>/pl_dl_paid/` | see queue.log | ~73 | running |
| 2026-11-10 | VFX: free `vfx_workbench` spin_slash round the swordsman (`fx_raw/sword_spin_e`, My effects 7c6eb20c…) and the PAID VFX Creator over REST `POST /v2/vfx` (lite, sprite = swordsman south still): "sword whirlwind" loop 12 f 160 px (`fx_raw/sword_whirlwind_e`, effect 22e7ce2c…) | | 0 + 3 | owner "ไม่สวย เก็บเครดิตไว้ ทำท่าตัวละครดีกว่า": no more paid VFX, credits go to character moves |
| 2026-11-10 | Gunner test: `animate_image_pixminimax` on `gunner/east132.png` (128 view padded to 132 px = the cheaper price step), 16 frames, alternating right / left pistol shots with recoil, side view | job 9bcf3d4e-65a6-4f75-b618-05fed2494391 | 1 | `gunner/test_shoot/` (aim, fire, kick up, lower, twice; muzzle flashes drawn though asked not to; both shots from the near hand in the side view) |
| 2026-11-10 | Laser-bow archer (owner's GPT turnaround, green tech; `laserbow/px128` checked first) — 2 shot tests, `animate_image_pixminimax` 16 frames on `laserbow/east132.png`: `aimed` (draw, hold, release) and `rapid` (3 quick shots) | 135fdb1a… / 65d286dc… | 1 + 1 | `laserbow/test_*`, `test_both.gif`: rapid = green bolts flying forward (good); aimed = the light arrow drawn pointing back through her, a squiggle on release |
| 2026-11-10 | Laser-bow archer v2 (owner's GPT redo in the Guardian's style, `laserbow2/`, 128 views checked): 2 whole-body shot tests at 132 px, 16 frames (`spin` = spin into a lunge, fire, recoil slide; `leap` = jump back, fire mid-air, land crouched) + `create_character` v3 "Laser Bow Archer 128" from our south / east / north | spin 12cb95f2… · leap 831d5ad1… · character f58ac29c-8dc6-4872-8457-bddb6d8d0aa8 | 1 + 1 + 2 | both shots good (`laserbow2/test_both.gif`) |
| 2026-11-10 | Laser-bow v2 normal shot (6194c77d…, 1) · Gunner v2 (owner's GPT redo in the Guardian's style, `gunner2/`): whole-body alternating dual shots at 132 px 16 f (b9b43968…, 1) + `create_character` v3 "Gunner 128" dee7d10e-cd50-4819-837e-cd6b856eeb5e (2) | | 4 | balance 1,633.9 after |
| 2026-11-10 | Gunner v2 crit (both pistols together, in place; 3d74c041…, 1) · Guardian v2 (long sword on the shoulder, owner's GPT redo, `guardian2/`, 128 views at one shared size): 3 sword moves at 132 px 16 f (`combo1` rise + downward cut 76abec1f…, `combo2` full spin d632958a…, `combo3` lunge thrust c60914ff…) + `create_character` v3 "Guardian Longsword 128" 96c2d44c-7e95-4a11-bd9c-7280e428d39d | | 1 + 3 + 2 | `guardian2/combo.gif`; big drawn swooshes in combo1/2/3 |
| 2026-11-10 | Rogue class 2 Assassin: `image_to_pixelart` 128x128 faithful, strength 200 from the owner's GPT chibi game view (`rogue/class2/assassin_gameview_gpt.png`, job f05e052f…) -> `rogue/class2/assassin_pl128.png` | | 1 | compare with the free converter `tools/art/chibi_px.py` in `assassin_compare_x4.png` |
| 2026-11-10 | Base moves, side view at 132 px (`animate_image_pixminimax`, owner "เจนภาพที่เหลือ pixlab"): idle 16 · run 16 · roll 16 · hurt 8 · death 16 for guardian2, laserbow2, gunner2 → `<key>/base_<move>/`, `base_moves.gif` | jobs in each folder's order | 15 | all usable; laserbow hurt draws a green shot, gunner hurt small sparks. Guardian v2 sheets rebuilt with them (`guardian2_build.sh`) |

### Second PixelLab account (owner's other key, from 2026-11-08)
The app kept the old key until restarted, so jobs go through `tools/pl_rpc.py` (HTTP JSON-RPC with the key from the
user env var, never printed; `--upload` for images). Balance at start: 40 + 20 daily bonus (refills +5 a night, up to 20).
| date | what | id | cost | result |
|---|---|---|---|---|
| 2026-11-08 | import "Dagger Rogue 128": all 8 views from `pl_rot/` (the first account's PixelLab rotations) | 6f024d02-2df1-4fb1-aaae-43922ac724ce | 0.25 | ✅ "nothing generated"; downloaded back to `pl2_rot/` and compared: all 8 views identical to `pl_rot/` (0 pixels differ) |
| 2026-11-08 | NW attack redo "attack_ul" (owner: the upper diagonals still had one sweep + a stab): two wide SIDEWAYS sweeps, seen from behind, never facing the camera; NE mirrors it | group d9721383-636b-4fb0-9421-c5b2feab6d6e | 1 | ✅ owner chose it ("B") over attack_2hit_b NW: NW = attack_ul, NE = its mirror (`rogue_build.sh`) |
| 2026-11-08 | base moves, owner "เอาทุกอย่างที่ใช้เจนไป ยกเว้นสกิล": run 8f ×8 (loop, keep_first_frame off), idle 8f ×8 (loop), roll 8f ×8, hurt 4f ×8, death 8f ×4 (E S W N) — 36 jobs from `art/incoming/action/rogue/jobs_base.json` via `tools/pl_queue.py` (one at a time, ZIP into `pl2_dl/` after each, log `pl2_dl/queue.log`, group ids `pl2_dl/groups.json`; rerunning skips what is downloaded) | see groups.json | 36 (3.75 + daily bonus left) | ✅ all 36 done 15:13–15:49; dust puffs beside the run / roll are cut by `act_sheet.py` (`dedust`: small or pale separate blobs). In the game: idle loop 7 fps, run loop 13 fps at speed 230, roll 0.4 s, hit 0.28 s, death 0.9 s (nearest of E S W N) |
| 2026-11-08 | VFX Creator chat, Lite (owner "เจน 1 เครดิตเอง"): "Cyan sword cut" | My effects 3b257bb0-20fd-43d8-9dbb-3554b2f0e459 | 1 | ✅ used for skill 4's cuts |
| 2026-11-08 | VFX Creator chat, Lite (owner "ให้ดูเหมือนรอยผ่า"): lens-shaped wound | My effects 1aefbc42-0270-479d-9cfd-222c00743d9c | 1 | ✅ skill 4's cuts (in green) |
| 2026-11-08 | VFX Creator chat, Pro, by the owner: "Cyan lightning dash" | My effects 3997ec67-2cf4-49f9-ba5d-caeab4cd24b0 | 4 | ✅ skill 4's dash streak |
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
- Cuts (owner "ไม่เอาเส้นตรง" → "รอยฟันแบบรอยผ่า"): skill 4 puts a big cyan VFX `cross_slash` (`fx/xcut.png`, size 2.6) on every
  monster each pass; the spin throws crescents (`slash_trail`, cyan, 8 facings × 3 sizes: `dslashs*` 1.5, `dslash*` 2.3,
  `dslashl*` 3.3; `slashFor(deg, size)` picks the one that bulges that way) in three layers round her every other step
  (owner's picture: 3–4 overlapping swirls of different sizes). Then (owner "ซ้อนกันให้ได้วงกลม วงละ 90 องศา"): every 4 steps a
  full circle = 4 crescents bulging out 90° apart, two sizes at once (mid + large, the large a beat later), each set turned
  45° from the last; 55% see-through with a weaker glow, only the arc nearest the camera in front of her, so her body shows. Made with `tools/pl_vfx.py <export> <key> '<part json>'`
  (start → add_part → export → download → `vfx_import.py`, all free); `_glow` copies for each.
  Dash lightning (owner asked for a straight dash line with lightning chasing it; their own VFX Creator try was lost unsaved):
  VFX `dash_slash` (cyan, 2.4) + two own `bolt` layers along it (jag .07, 2 branches, growing back to front, flickering) +
  a spark burst, My effects "rogue_dash_bolt" → `fx/dashbolt.png` (orange tip sparks recoloured) + mirrored `dashbolt_l`;
  skill 4's passes now cross the field left / right in turn with a slight slant (`nextCut`), one streak per pass.
  Then the owner's own VFX Creator effect "Cyan lightning dash" (My effects 3997ec67-2cf4-49f9-ba5d-caeab4cd24b0, made with
  the prompt above, Pro = 4 generations) replaced it: opened with `start --effect <id>` (the id was read from the VFX
  Creator page's "Open" button, `vfx-library-open-<id>`, after the owner signed in in the built-in browser), ×1.7, exported
  as "rogue_lightning_dash_game" → `fx/dashbolt.png` + mirrored `dashbolt_l` + glows.
  Owner "เอารอยฟันเก่าออก": the X cuts are gone; "เจนรอยผ่าดูเผื่อสวย 1 เครดิตเอง" → generated in the VFX Creator chat in the
  built-in browser (Lite, 1 generation): "Cyan sword cut" (3b257bb0-20fd-43d8-9dbb-3554b2f0e459: a thin diagonal gash, flash,
  sparks, splits apart) ×1.6 → `fx/swordcut.png` + mirrored `swordcut_m` + glows, on every monster each pass (alternating).
  Then (owner "ให้ดูเหมือนรอยผ่า") a second Lite run in the same chat: a lens-shaped wound with a dark split, flash and sparks,
  saved as new (My effects 1aefbc42-0270-479d-9cfd-222c00743d9c) ×1.4 → `fx/woundcut.png` + `woundcut_m`, used instead of the thin
  cut. Then (owner "เปลี่ยนสกิลให้เขียวเรืองแสงสวยๆ ทั้งสกิลเลย") the whole of skill 4 is glowing green: `<key>_g` sheets of
  dashbolt / dashbolt_l / woundcut / woundcut_m / dashhit / dashcharge (each pixel moved onto a green ramp by its brightness)
  + green glows, the field sprite's colours, the field glow, the hit sparks, a green glow on her while she dashes.
  Owner then "เปลี่ยนสีฟ้าดีกว่า": back to cyan-blue (the `_g` sheets stay in fx/, not loaded).
  Then "ไม่ฟ้าแบบนี้ ฟ้าแบบน้ำเงินสายฟ้า": electric blue `_b` sheets (ramp #0a1248 #1c3cd2 #4080ff #a5cdff #f5faff, glow 70,130,255) for
  every skill-4 effect, the field and her glow — current.
  **Skill 4 as a STAR** (owner: "เอฟเฟกต์ฟันไม่สวย เอาออก ให้ฟัน 5 ที เป็นรูปดาว", "ทำวงสวยๆ เพิ่มเอฟเฟกต์", "ให้ดูหนักหน่วง รุนแรง"):
  no cut marks, no horizontal streak; a spinning VFX `rune_circle` (5 points, electric blue, `fx/starrune.png`, drawn at 50%
  under the bodies by `drawField`, field 160 × .42); she blinks to the top point and dashes the pentagram (`STAR` order
  0 2 4 1 3 0), each line stays on the ground as crackling light (`drawStarLines`: re-jagged every 2 frames, dark edge / blue /
  light / white core, glow), a VFX `bolt_strike` (`fx/starbolt.png`) at every point she reaches, everything inside hit per
  line (5 × 9); `starFinish`: the star flashes, five strikes together, VFX `shockwave_ring` (`fx/starshock.png`), a burst,
  22 damage, hit-stop .14, shake 11, camera kick.
  Owner "ไม่สวย เอาดาวออก": the rune circle re-made without its hexagram / star ring (My effects "rogue_rune_nostar" →
  `fx/starrune.png`), and each dash line now only flashes (.22 s after the dash) instead of staying, so no star builds up;
  the five dashes, lightning strikes and the heavy finish stay.
  Owner's picture of "Cyan sword cut" recoloured blue in VFX Creator, "ใส่อันนี้ ให้ทิ้งรอยไว้ หน่วง" + "ใช้แทนพุ่งสายฟ้าเลย":
  3b257bb0 re-exported ×2.8 ("rogue_big_cut"), pixels moved onto the owner's blue (sampled from their screenshot: #081a46
  #0d5694 #0fc3ff #83f4f9 #f0fcff), the clean-line frame held 9 frames (~0.65 s) with a slow fade, then turned offline
  (nearest, about its centre) to 12 angles `fx/bigcut0..165.png` + glows. Skill 4's dashes now cross the middle of the
  circle at `CUTS` 0 / 135 / 45 / 165 / 105° (alternating sides, length 280), each leaving one big cut that lingers; no
  lightning line, no strikes per dash (the finish keeps five strikes + shockwave). `fx/bluecut*` = the smaller held cut.
  Owner "ท่าจบ ลบเส้นสีขาวออก": the dash is drawn from an arc-free copy (`noArcOf(sheet)` = `makeNoArc`, cached per sheet,
  also for the dash after-images) and skips frame 5 (the one with PixelLab's big slash arc): lunge 3–4, then 6.
  Owner: "เอาสายฟ้าตอนจบออก" → no lightning strikes at the finish (shockwave + burst stay); then "สายฟ้าพุ่งในภาพ แทนรอยฟัน"
  + their own exported game pack `art/incoming/fx_raw/owner_lightning_dash/` ("rogue_lightning_dash_game" re-coloured by them:
  black lightning, red flecks, blue-purple streak; "เอา แต่งให้แล้ว" = use it as is) → `whole` clip turned offline to 24
  headings `fx/ldash0..345.png` (nearest, about the anchor) + glows from the bright pixels only; each skill-4 dash plays the
  heading it travels (`nextCut`), the blue cut (`bigcut*`) is no longer drawn.
  Then owner "ไม่ต้องใช้อะไรเลย ตัวมันพุ่งเป็นเงารางๆ สีฟ้าก็พอ" + "ใส่ฟ้าให้เงา ให้เห็นเงามันด้วย": no effect on the dashes at all;
  only her after-images, every 12 ms, in a blue copy of the dash sheet (`blueOf`: arc-free sheet tinted #3d9bff at 82%), up to
  ~67% and fading over .34 s (ghosts now take their own `life`). Also effect pictures load with `?v=<hash of fx/manifest.json>`
  (fetched no-cache), because the owner's browser kept old effect pictures.
  Then the owner's Zenitsu clip ("เอาแบบนี้", "เอาแค่สกิลพุ่ง"): she vanishes and zips rim to rim in a zigzag (`rimPt`, each
  ~150-165° on from the last, the last ending near the middle), each dash a thin bright streak (VFX `dash_slash` in white /
  pale yellow / cyan, orange tip sparks made yellow, turned to 24 headings `fx/zstreak*` + warm glows) and a flash star
  (VFX `hit_star`, `fx/zstar.png`) where she lands; she is drawn only for the blink at each landing point; no after-images.
  Owner "ดีละ วงเอาออก ไม่สวย เพิ่มเอฟเฟกต์ตอนลง กระจายประกาย หรือเพิ่มเป็น 6 ฮิต": the ground circle is gone (no `field` fx;
  the aim ring still shows the area), a VFX `star_burst` (`fx/zspark.png`: a ring flash, little stars scattering) with the
  flash star at every landing point, and 6 dashes (`SK4.n` 6).
  Then: "ตอนจบไม่เอาวงแบบนี้" → the finish has no shockwave / puff ring / ring burst, the sparkle re-made without its ring layer,
  skill-4 hits skip the normal ring burst (`hitMob(..., noRing)`); the owner pasted pixelfx's crit-hit code → its sheet
  (`fx/critx.png`, already rendered from pixelfx impacts/crit-hit) is the finishing hit and the hit on every monster each
  pass ("เอาเอฟเฟกต์ตอนมอนสเตอร์มาใส่"); "สีเหลืองเข้มกว่านี้" + "เหลืองขอบดำเข้มๆ" → streaks / stars / sparkles moved to deep gold
  (#f0a800 / #ffce28 / #ffec78) with a 2 px near-black outline (1 px on the sparkle), faint pixels and tiny specks dropped.
  Then "เอาสีเดียวกับแสงฟัน": every skill-4 effect re-made from the original VFX sheets in the attack's slash-light ramp
  (`rogue.json` arc ramp #a8d4ee / #ceecfa / #f6fdff, glow 120,200,255), no outline; `fx/critx_ice.png` for the finish;
  per-effect strengths `PFXA` (crit-hit glow .18, sparkle .3, star .45: stacked glows washed the monsters white); a flash
  star on each monster hit instead of a crit-hit each.
  Throws (owner "ปาให้ดูแรงกว่านี้ ไม่เอาย้อย"): the dagger flies straight at 1700 px/s with a longer streak and lands with an
  impact star, sparks and a shake; the bomb is thrown flat (arc 16 px, .26 s) trailing fuse smoke.
- **New heroes + monster brief** (owner 2026-11-09 "ทำพรอมต์สร้างตัว ดาบชาย เมจชาย", "คำสั่งเจนมอนเป็นชุด จะให้ Codex ทำ"):
  the owner made both heroes in GPT from my prompts (pixel-style turnarounds, front / right profile / back, both correct):
  `art/incoming/action/swordsman/turnaround_gpt.png` (2000x667 as pasted, greatsword on the right shoulder, red scarf) and
  `art/incoming/action/mage/turnaround_gpt.png` (1448x1086, indigo hood + robe, teal cape, staff with a teal crystal).
  The figures are different sizes only because GPT drew them on different canvases; they are scaled to one height when
  they go into PixelLab / the game. PixelLab characters for them wait for the owner's go (credits).
  Monsters: `docs/codex/action/MOBS.md` (15: forest/ruins 7 + treant boss, Thai map 6 folklore + Chalawan boss; one
  picture each, 1536x1024, style = the swordsman sheet `refs/00_STYLE_hero.png`), Codex delivers on `codex/mobs` into
  `art/incoming/mobs/`.
- **Priestess (5th hero, `?hero=priest`)** (owner: "นักบวช มีหน้าที่บัพ ดีบัพ เกมส์เรายาแพง หายาก ต้องการให้ทุกคลาสมีที่ยืน"; GPT
  turnaround from the archer style picture → `art/incoming/action/priest/`, `turn128.py` after cutting 9 white pockets
  between the staff and her body; PixelLab character f1767069-1186-47bb-8d7f-af569369a329 "Sun Priestess 128" (v3 import,
  ~2 gen); 49 move jobs (`jobs_all.json`: idle/run/roll/hurt 8 dirs, attack 5, death 4, pray + bless 4 dirs) run by
  pl_queue in the background with `tools/keep_awake.py` holding the PC awake; `hero_build.sh priest` builds whatever has
  arrived). Role: survives without potions. Basic attack = gold holy bolt (`holyBolt`, homing, medium range), passive
  ศรัทธา = every hit heals 1 (max 4/s), her heals +20% (`healP`). `PRS`: Q ฟื้นฟู heal 25 + 15 over 4 s (pray move), E
  ทัณฑ์สวรรค์ gold sky pillar (`pfx_skyarrow_y`), 26 dmg and frail 5 s (+25% damage taken, `m.frail`), R พรนักรบ +30%
  damage 8 s (bless move, `p.bless`), F ก้าวแสง short blink leaving a healing patch (`G.zones`), Z คำสาป slow 40% + hits
  30% weaker 6 s (`m.curse`, purple rune ring), X ปาฏิหาริย์ 10 s: a killing blow leaves her at 40, else heal 30 at the
  end (`p.mir`). Gold / green effect copies: `pfx_skyarrow_y`, `pfx_dashstrike_y`, `pfx_heal_y` (fx_tint.py).
- **Map pass** (owner asleep, 30/100: "แมพให้มันไม่รก ดูสภาพแมพก่อนใส่ของ ใส่กองทับกันมั่ว ... น้ำให้กว้างๆ ... บ้านติดกันเกิน ... ตัดไม่หมด
  ... วางตำแหน่งคลายกัน ทำแบบแผน ... มอนให้เยอะกว่านี้"): every prop picture knows its opaque box (`GPROP[n].bbA/bbB`,
  `gp().bb`); `add(s, x, y, o)` refuses a spot whose box overlaps anything already placed by more than 5% (10% with soft
  props, 30% between soft ones) or whose base stands on a road, the bridge or water (`o.water` for stilt houses, `o.force`
  for walls, gates, forts, signs), and returns whether it placed. Planned buildings use `put` with a spiral of nearby
  spots (`NUDGE`), so the plan holds without piles. Fewer filler props on every map (decoration counts about halved),
  the Thai village is a plan (a slot every 460 px on each bank: a stilt house half on the bank in every other slot, a
  land house behind, one pot / basket / banana), the ruins' planned pieces go down before the rocks. Rivers wider
  (Thai SWC 190, forest 92). Thai city: side walls get Codex's side-view gates (`t_gate_l` / `_r`, from
  `art/incoming/maps/thai_gate_4view.png` via props_px at 380 px), corner forts lost their outer wing
  (`t_fort_wl` / `_wr`, the wing stuck out past the side wall). Plants cleaned with `tools/art/prop_clean.py --veg`
  (white pockets between branches cut, the dull olive band inside the outline darkened). Monster camps:
  `spawnCamps` puts 12 groups of 3-5 (two kinds each) round the map, they mill about until she comes within 330 or
  hits one, refill 70 s after being cleared when she is far; waves are bigger (5 + 3 per wave, up to 24) and start when
  no monster is chasing her.
- **Archer pass 2** (owner asleep: "สกิลนักธนูไม่สวย ปรับโดนให้สีเขียว ให้มีระบบออโต้ ตีธรรมดาให้ลูกตรง"): her tone is green now
  (`ACY`, `HEX.leaf`/`RGB.leaf`); green copies of the effect sheets by `tools/art/fx_tint.py <src> <dst> <ramp> [pad glow gamma]`
  (`pfx_skyarrow_g`, `pfx_starfall_g` from the haze-free `_c`, `pfx_dashstrike_g`); every arrow hit plays Dash Strike's hit
  frames in green along the arrow, arrows bigger with a ring at the bow; split arrow = 5 arrows plunging straight out of the
  sky onto the monsters; the charged beam flashes on each monster. Straight shots: `faceDir(name, dx, dy)` picks the
  direction whose pose (`rowFacing`, follows aliases and mirrors) points closest to the target, so a down-right target no
  longer shows the side pose; her real south-east attack + crit (4 gen) are queued after the priestess
  (`art/incoming/action/archer/jobs_se.json`, log `queue_se.log`; rebuild her sheets with hero_build.sh and drop the
  south-east / south-west aliases for attack + crit when they land). Auto attack for every hero: button ออโต้ (T),
  saved in `act.auto`; while standing still it attacks whenever a monster is within `AUTOR[HERO]`.
- **Afternoon pass 2026-11-09** (owner woke up: "ทำไมหยุด"; the overnight queues had finished at 14:16 and pushed the
  priestess's full sheets + the archer's own south-east shot; Codex had stopped to report, told to go on): Japan + mummy +
  scarab move frames in (`mob_frames.py`). Thai map: rice paddies painted in code (`paddyPx`: flooded cells, rows of green
  rice 7 px deep with 2 px of sky-tinted water, a dark drop under each grassy dike, a dike all round; was the brown
  `reeds` swamp square), ruin floor moss = small round patches per 44×36 cell (`hash2`; was long diagonal streaks).
  Archer effects on green grass: `PRIM` = a dark rim (the sheet grown 2 px, `rimOf`) drawn under `pfx_dashstrike_g`,
  `pfx_skyarrow_g`, `pfx_starfall_g` (.22, its soft glow made a dark haze at more) and `croots_g`; arrows get a dark
  underline; root shot = green vines `fx/croots_g.png` (fx_tint of croots). **Start menu** (the first thing seen was a dark
  box on black): the real map pans behind it (`G.menu`, `menuCam`, only `stepAmbient` runs, the hero is not drawn),
  logo LAST SIGNAL / สัญญาณสุดท้าย, five hero cards (south-east still, the chosen one plays its idle in `menuTick`), role
  + kit line (`HROLE`, `HDESC`), start map (`MAPN`), เริ่มเล่น; another hero / map reloads with `&auto=1`, which starts at
  once. **HUD**: framed panel with the hero's face (front view's head, `#hpor`), level badge, HP number + a pale trail that
  holds .45 s after a hit then drains (`HUDL`), banded bars; score in the same panel style; boss bar clear of the panel;
  defeat screen with wave / kills / level, เล่นใหม่ / เลือกตัวละคร. Trees fade when a fighting monster stands behind them
  too. Camps keep `cityD` ≥ 1.7 (were right against the wall). Tests: `?test=view&camp=1&n=<steps>` (next to the nearest
  camp, auto on). The Codex wall kit (`thai_wall_kit.png`, big boxy pieces) was looked at and not used: the code walls
  read better at game scale.
- **Prop background leftovers** (owner 2026-11-09, a crop of the stilt house: "ดูด้วยตายังเห็นเลยตัดยังไง"): the cut kept the
  GPT background as one flat cream colour (a different shade per picture, e.g. v_stilt 254,250,213) between stilts / rails /
  under floors, and a 1-2 px cream line between props_px's added outline (29,26,34) and the picture's own edge (the pale
  dots). `tools/art/prop_bgclean.py`: A. holes = a flat pale colour patch ≥ 16 px, still ≥ 4 px after 3 erosions (roof
  ridges and beams are thinner), ≥ 40% of its 2 px ring dark outline, and only the picture's main hole colour (the
  grindstone in t_smithy is the same cream but ringed less) → see-through; B. fringe = light pixels next to the added
  outline in a mostly non-light neighbourhood → removed (twice) and the 1 px outline put back. Holes only on t_granary
  t_library t_palace t_smithy t_teahouse t_twin v_boatshed v_fishhut v_stilt cart oxcart (the western houses' cream
  plaster walls read as holes), `--noholes` (fringe only) on every other prop. Props no longer stand on the rice paddies
  (`groundOk` rejects TK 8).
  Owner: "รอบนี้ก็ยังไม่หมด" → cleaning the reduced pictures could not tell the leftovers from real light paint, so every
  prop is now rebuilt from its full-size sheet with the background cleaned BEFORE the colour reduction: Thai sets in
  `thai_props.py` (`clean_holes`: enclosed near-white patches ≥ 20 px cut except in the white-walled items `WHITE_OK`, the
  near-white line on every cut edge, and GPT's antialias ring outside its own dark outline = an edge pixel 35+ lighter than
  the darkest pixel just inside it), the other sets in `tools/art/rebuild_props.py` (same clean, enclosed white only on
  nature + ruins; each item rebuilt at its current height). `prop_bgclean.py` is no longer needed.
- **Berserker (class 2 of the swordsman) design kept** (owner 2026-11-09 "เอาแบบนี้เก็บไว้ก่อน"): GPT turnaround from my prompt
  (black full plate, spiked pauldrons, horned helm with red eyes, torn red cape + tabard, chains, huge chipped greatsword with
  red cracks on the right shoulder) → `art/incoming/action/berserker/turnaround_gpt.png` (1536x1024). The first prompt's
  wolf-skull helm read like Guts (Berserk); this run has a horned helm instead. Before PixelLab: the middle view is a 3/4
  view, not a true right profile, so the east view needs a redo or a fix; the owner has not given the PixelLab go.
- **Guardian (shield knight, class 2 of the swordsman, the Berserker's opposite) design kept** (owner 2026-11-09, "เอาเท่ๆ" prompt):
  `art/incoming/action/guardian/turnaround_gpt.png` (1536x1024, figures ~710 px; Berserker ~645 px): dark steel + gold angular plate,
  winged helm with a glowing V visor, navy tabard + torn cape, rune longsword, kite shield with a gold lion. Both are big enough
  for PixelLab (128-256 canvas). Both middle views are 3/4 views, not true profiles: a side-view redo (one picture) is needed
  before PixelLab.
  Guardian side redo in: `art/incoming/action/guardian/side_right.png` (true right profile; the sword is in the near = LEFT hand and
  the shield on the far arm, the front view has them the other way round; fine for one diagonal + mirror). Berserker side redo in: `art/incoming/action/berserker/side_right.png` (true right profile, blade over the shoulder pointing back, glowing eye). Both ready for PixelLab (waiting for the owner's go).
  Berserker v2 (owner: the sword was too small, then GPT kept drawing it bent; fixed by a new chat, the sword drawn alone first, then one view at a time with it attached): `front_v2.png` (straight sword as long as he is tall, one red rune line). `side_v2.png` (true right profile; owner "ดาบสั้น": the blade stretched by 130 px in code (a plain stretch between the rune stars repeated, the tip moved out) so it matches the front view; GPT original kept as `side_v2_gpt.png`). `back_v2.png` (from behind, the sword level across the shoulders in the right hand). Berserker v2 complete: front_v2 / side_v2 / back_v2 are the ones to use for PixelLab (the first turnaround is superseded).
- **Thai town hub** (owner 2026-11-09 "ฉากเมือง ทำแค่เมือง ไม่ต้องมีมอน เอาไว้รับเควส ละก็วาร์ป ... ใช้กำแพงเป็นแมพเลย ไม่ต้องกว้างมาก"): `?map=town`
  (`TOWN`, TH ground + `thaiProps`, so the walled city of the Thai map is reused): she can only move inside the walls
  (`cityD` > .86 pushes her back except on the road at the gates), the camera stays on the city, no camps / waves
  (`ROSTER.town` = []), the wave counter is hidden (`.town`). Gates: west → `west`, east → `jungle` (`TOWNX`); the west field's
  east exit and the jungle's west exit now lead to the town. Warp circle (`drawTown`, `townTick`/`townUI`: stand on it → a
  list `WARPS` → `travel`) and a quest board (noticeboard prop + "ยังไม่มีเควส"; quests not built). The old `thai` map
  (city + fields) is now named ทุ่งนาเมืองไทย and reached by the warp. Next: the owner's plan of 4 maps round each town
  (north / south / east with the boss), GPT houses made to be placed per direction, the quest system.
- **Frost wolf moves in** (owner made it with GPT from the pack `frost_wolf_pack.zip`, 2026-11-09): their zip had white and see-through 3x2 sheets; `white_cut` punched holes in its white fur, so the see-through sheets were put in `anim_cut/` directly (newer than the source, so `mob_frames.py` uses them as they are) → `art/action/mobs/frost_wolf.png`. For white monsters, ask for / use see-through sheets.
- **Swordsman R release blast** (owner 2026-11-09 "ปรับสีให้เข้าโทน ละเอาไว้ท่าชาร์จ"; pasted 6x5 strike sheet, glow flattened into white / pink / red bands, raw `art/incoming/pfx/sword-charge-sheet.png`): only its grey smoke + rocks survive the cut (`tools/art/sword_charge_fx.py` → `fx/pfx_swcharge.png`, the band seams read as stripes); `chargeBlast(p, lv)` plays it from frame 6 on the ground 70 px in front, with a code red-orange flash (`sbang` with `red`), two rings, sparks, dirt and landing dust, bigger per level (replaces the Frostwindz sweep there).
- **Swordsman normal combo = the owner's orange crescents** (2026-11-09 "ท่าฟันเอาให้เข้ากับฟันธรรมดา"; pasted 6x5 sheet with flattened glow bands, raw `art/incoming/pfx/sword-slash-sheet.png`): `tools/art/sword_slash_fx.py` keeps the thin bright crescent and the dark debris at full, the band seams faint → `fx/pfx_swslash.png`; `swSlash(p, i)` plays slash 1 / 2 / 3 (frames 0-9, 10-17, 18-29) on combo hits 1 / 2 / finisher, 22 px in front of him, following him. A clean GIF of it would look better. Owner "เอาเอฟเฟกต์ตีธรรมดาออก ไม่สวย" → off again (the call is commented out).
- **Archer E = the owner's green bolt** (2026-11-09 "สกิลนี้แทน สายฟ้า เปลี่ยนโทนสีด้วย"; pasted 6x6 sheet 3408x2016, glow flattened into cyan / green / white bands, raw `art/incoming/pfx/green-bolt-sheet.png`): `tools/art/green_bolt_fx.py` keeps the white-hot cores (orb, bolt, impact flash, not the big white patches at the cell edges) and the dark smoke, archer look (pale core + neon rim, ink smoke) → `fx/pfx_gbolt_k.png`; then the owner sent the same effect as a clean GIF (`art/incoming/pfx/green-bolt.gif`, see-through, real glow) → `tools/art/green_bolt_gif.py` (half size, soft dark rim) replaces it. `javelin()` plays it turned from her bow to the spot (scale = distance / 148, .7–1.7), damage at .12 s. Renamed ลูกพลังเขียว.
- **Star rain = one pass, longer** (owner "สกิล4 คือฝนดาวตก ทิศสกิลมันแปลก ... ให้มันมารอบเดียวแต่ยาวขึ้น"; the owner counts the star rain as skill 4 — I first changed the leap back by mistake, undone): one copy of `pfx_starfall_c_k` (the mirrored second copy made the streaks fall two ways), played at `SF.fps` 18 instead of 30 (~3.5 s), the 10 ticks spread over the landing part, the closing blast at the end.
- **Archer F bomb blast in neon green** (owner 2026-11-09 "สกิล4 นักธนู เปลี่ยนสีเขียวนีออน"): `fx_tint.py pfx_bombarrow pfx_bombarrow_g 021208,0a3a16,1fbf4a,46ff7d,d8ffe0` (the black + neon `archer_fx` copy turned the fireball into a flat blob), dark rim via `PRIM`, ring / hit colour / fuse spark `ACK.neon`.
- **Swordsman red slashes** (owner's zip 2026-11-09 "Pixel Art Animations - Warrior FREE" by Frostwindz, itch.io; licence: use in
  games, modify, NO redistribution, so the zip / frames are not in this public repo, only the cut sheets): `tools/art/warrior_vfx.py
  <unzipped>` → `fx/wvfx1..5.png` (128 px, facing right). `wSlash(p, v, sc)` plays one in front of him, turned to his facing:
  normal combo hit 1 = VFX1 double slash, hit 2 = VFX3 thrust, finisher = VFX2 big crescent; R release = VFX4 sweep (bigger
  per level); Z counter = VFX5 rising burst. Owner "ตีธรรมดาเอาออก มันไกลไป": off on normal hits again (his old cutFx back); then "ฟันธรรมดามีคลื่นออกมา ยังไม่เอาออก" = the flying ice crescent `swordArc` (moves 260 px out): no longer on normal swings (R / Z keep it). His blue `cutFx` streaks on hit are off (the pale cyan arcs drawn inside his
  attack frames stay).
- **Swordsman E = the owner's sword storm** (2026-11-09 "พายุดาบ เปลี่ยนโทนส้ม นีออนดำ แบบพวกมีด ธนู"; pasted 9x8 sheet 5436x5440 on
  black, its glow flattened into solid red / yellow / orange / pink bands, raw `art/incoming/pfx/sword-storm-sheet.png`):
  `tools/art/sword_storm_fx.py` drops the band colours (and 4 px round them), keeps the dark smoke + textured streaks, black
  ink + neon orange rim + orange glow → `fx/pfx_swstorm_k.png` (72 frames 302x340). `whirlTick` played it round him; owner "พายุไม่เวิร์ค เปลี่ยนกลับใช้ของเดิม" → back to the old whirl ring; then "ใส่พายุแดงที่ให้ไป" + the same sheet again → `tools/art/sword_storm_red.py` = the sheet in its own colours (black → see-through, the flat glow bands at alpha 150 so he shows inside) → `fx/pfx_swstorm_r.png`; owner "เอาสีแดงออกไว้ก่อน" → off again (`sw = false`), old whirl ring.
  Found on the way: `swordSk` k 2 paid the cost and then `startWhirl` paid again, so E never spun; the first payment is gone.
- **Dash + landing dust** (owner 2026-11-09 "เสริมพวก เดส กระโดด", two pasted sheets → `fx/pfx_dustdash.png` 24 frames, puff at
  50,64 with a ~380 px trail to the right; `fx/pfx_dustland.png` 19 frames, anchor on the ground 84,140): `dashDust` at the start of
  every roll and the archer's leap back (turned to the way she goes), `landDust` at the end of a roll, the archer's landing, the
  swordsman's leap slam and a thrown monster landing (sized by its radius).
- **Skill effect prompts for the owner** (2026-11-09 "เอาพรอม gpt มา ... ฉันสั่งเอง", chose skill effects): `docs/fx-prompts.html`
  (built by `tools/art/fx_prompts.py`, one card + copy button per skill still on an old or borrowed effect: swordsman E R F Z X,
  rogue R Z X, mage all six, priest all six; the archer, swordsman Q and rogue F are left out). Every prompt: ONE effect, a
  6x4 grid (4x4 for loops) of equal square cells, the layout the game needs (`LAYOUT`: shot left → right, ground centred, sky,
  round the hero, swing to the right), the hero tone (`TONE`), transparent background, no characters / text. Results come back
  as files → `pfx_paste.py`; mark finished ones in `DONE`.
- **Hit feel: knockback + impact** (owner 2026-11-09 "ทำเอฟเฟคโดนตีให้ดี กระเด็น กระแทก"): `shove(m, ux, uy, kb, big)` from `hitMob`
  and the melee `doHit`: speed 7 x kb (9 x when the hit kills), capped at 420 px/s (a blast right under one had thrown it 150 px);
  kb 40+ or a kill throws a light monster off its feet (`m.kz` height, `m.kvz`, gravity 1200, no walking while in the air, less
  friction in the air, lands with dust + a ring), bosses and stout ones only slide; dying bodies keep sliding / flying and still
  stop at walls and water; skid dust while sliding fast; every hit an impact star (`hstar`, `drawHitStar`) and a kick of dust,
  big hits / kills add hit-stop + shake; the hit flash is solid white for its first 50 ms.
- **One view for every screen** (owner 2026-11-09 "ให้เห็นเท่ากัน ไม่งั้นเสียเปรียบ เอาเท่าที่ส่งมาให้ดู", replaces the phone zoom
  below): every screen shows the same `FVW` x `FVH` = 1266 x 585 world px (the 2x phone view). `onResize`: `S` = whole canvas
  px per world px (ceil of fit x DPR), `Q` = canvas px per CSS px (= DPR on a 3x phone, finer elsewhere, then the browser
  scales the canvas down smoothly: `image-rendering` auto unless Q = DPR), `OX`/`OY` = where the view starts; other screen
  shapes get dark bars (PC 16:9 thin top/bottom, 4:3 tablets big ones). Mouse → world = (mouse * Q - OX) / S + cam; the
  screen-space overlay uses `setTransform(Q)`. Owner then: "ไม่ได้บอกคมเท่ากัน หมายถึงระยะมองเห็นเท่ากัน" → every screen draws at its
  own pixels (`Q` = DPR, `S` = fit x DPR, a whole number on a 3x phone, 1.33 on a 2x phone, 1.52 on a 1080p PC; the world
  offset is rounded to whole pixels); `?sharp=1` brings back the finer whole-S drawing scaled down by the browser.
- **Star rain v3** (owner "ทำไมเป็นแท่ง ในต้นแบบมันไม่ได้เป็นแบบนั้น"): the light pillars and code comets are gone; two copies of the
  original Starfall Barrage sheet in black + neon (`pfx_starfall_c_k` from the haze-free copy: `archer_fx.py` options `w_min`
  = near-white only, `thin` = strokes eroded so the glow is not a fat black stake, `hollow` = big shapes see-through inside a
  black band) play over the circle from frame 28 (the second mirrored, .36 s later), 10 ticks while they land, a bigger copy
  in the middle and the closing blast. The dark rune circle stays.
- **Phone zoom** (owner 2026-11-09 "เอาซูม2เท่าเลย" after side-by-side shots of 1x and 2x on a 3x phone; asked first whether the
  heroes could go back to the 128 size or become painted: no, PixelLab frames cannot be turned into paintings, only redrawn):
  `onResize` picks, on touch screens smaller than 600 CSS px, the whole-number `S` that brings the view closest to 600 world px
  tall (3x phone 1170 → 2x = 585; 2.75x → 2x = 523; 2x phone 780 stays 1x); the PC keeps `floor(dh / 950)`; `?zoom=N` forces
  one. The touch skill buttons are a little see-through (opacity .84) since more of the fight sits under them.
- **Swordsman Q = Earthsplitter Cleave** (owner 2026-11-09 "Earthsplitter Cleave ให้ดาบแทนท่าเก่า", pasted sheet →
  `fx/pfx_earthsplit.png`, 42 frames, anchor = the start of the ground crack 70,219, the crack runs ~155 px right): `groundSplit`
  pushes an `esplit` fx (`drawEarthSplit`): anchored in front of him, turned to the aim (mirrored for the left), stretched to
  the crack length (sx = L/155, sy 1.3), starting at frame 3 so the red arc lands at once; each monster on the line is hit
  when the fire reaches it (.04 + 0.4 x its place along the line). The Codex crack + `gslam` stay as the fallback.
- **Archer kit from the owner's pasted sheets + the rogue's look** (owner 2026-11-09, five pictures pasted in chat, pulled out of the
  session log as base64; raw copies in `art/incoming/pfx/`: `charge-shot-sheet.webp`, `bomb-arrow-sheet.webp`,
  `rapier-flurry-sheet.png`, `thorn-vine-sheet.webp`, `earthsplitter-cleave-sheet.webp`): `tools/art/pfx_paste.py` cuts such a
  sheet (cells that are not whole pixels) into `fx/<key>.png` + manifest. "สกิลโทนเขียว ... ให้คล้ายกับสกิลโทนสีของมีด": every
  archer skill effect is now black strokes + a neon green rim + green glow like the rogue's purple (`tools/art/archer_fx.py`
  → `fx/<key>_k.png`; `ACK` = ink/neon in code); black also reads on grass. Q ยิงรัว (Rapier Flurry, "แทนท่า 1", was the
  split arrow): `rapier()` draws the sheet from the bow to the spot (anchor = target, turned, scaled to the distance), 8 thrust
  hits + a big last one (`ARS[1]` n/dmg/fin). R: the charge sheet gathers at the bow while held (`drawCharge`, frames by level),
  the release burst at its own size, the bolt (frames 21-38) stretched along the beam, reach follows the drawn head, bigger per
  level. F: the parting shot is a bomb arrow (`bombArrow`/`bombStick`) flying straight from the bow ("ไม่ต้องโค้ง"; the sheet's
  lob is not used), short fuse, the sheet's fire blast (kept orange) 30 in r 95. Z ธนูหนาม ("ยิงฝั่งดิน ละมีใครมาในระยะค่อยพุ่งใส่"):
  the arrow plants a seed (`G.seeds`, dotted reach ring, a sprout per strike left); a monster within 150 gets the thorn vine
  (`vineStrike`: sheet turned ±0.6 rad / mirrored, scaled to the distance) 24 + rooted 2 s, 3 strikes, 12 s. E javelin + arrow
  hit flashes use the `_k` copies; the star rain is redrawn black + neon. Tests: `?test=hsk&hero=archer&k=1..6&n=` (`&rel=` lets
  go of R).
- **Archer X ฝนดาว redone** (owner 2026-11-09 "Starfall Barrage ของนักธนูดูใช้จริงไม่รุ่นแรงเลย"): the green copy of ParticleFX's
  sheet (`pfx_starfall_g`) was pale lime on green grass, two thin streaks, nothing hit for 1.3 s. Now all code (`starRain`,
  `SF`): the ground in the circle darkens (flat dark disc `FXS.darkEm`) with two turning rune rings (`drawStarZone`), a white
  diamond star opens in the sky over it (`drawStarOrb`) and pours 20 comets (`drawComet`: white head, green body, dark edge,
  trail glow) from 0.28 s, one every 0.075 s; every 2nd is a damage tick (S.dmg on everything in the circle, 10 ticks as
  before) and lands on a monster in it; each landing (`starLand`): light pillar + white cross (`drawStarBang`), two rings, a
  burnt crater with a cooling rim (`drawStarCrater`), green/white sparks, dirt, embers, shake + hit-stop. Then a giant star:
  2 x S.dmg in 1.15 x the circle, kb 30, two shockwaves with light rays (`drawStarShock`), flash, kick, shake 13. First
  damage now at ~0.6 s (was 1.4). The sheet is kept for the skill icon. Check: `?test=hsk&hero=archer&k=6&n=<steps>`.
- **Norse: draugr moves in** (cloud session 2026-11-09): Codex's `codex/mobs-china` had draugr walk / attack / death
  (rows 145-147, hurt not drawn yet); copied into `art/incoming/mobs/anim/` with its REPORT_TH lines, `mob_frames.py draugr`
  → `art/action/mobs/draugr.png` (cell 90×84, anchor 50,81). The game picks it up from `index.json`; on `?set=norse` it is
  the only Norse monster with a sheet until the others arrive. Check: `?test=mobs&set=norse&clear=1&ph=0|1|2`.
- **Rogue Q and E in the black-purple tone** (owner "สกิล q e ทำให้เข้าโทนด้วย", "e ให้หมุน ละจังหวะสุดท้ายให้ลมสะบัดออก"):
  Q's dagger trail is black-edged purple with a violet glow, its landing and each hit play Dash Strike's hit flash from
  `pfx_dashstrike_v` (frames 13-24), puffs purple, the blink behind uses `pfx_step_v`. E's ring is `pfx_whirl_k` (the
  whirlwind in the same tone, made by `rogue_dash_fx.py`), hits flash `pfx_dashstrike_v`, the spin frames lose their
  pale air arcs (`noArcOf`) and the glow and after-images are violet (`vioOf`); when the spin ends `rogueGust`: everything
  within 1.7 x its radius takes `SK2.fin` (24, scales with level) and is blown back, a big whirl, two rings, wind lines.
- **Rogue skill 4, new look, IN THE GAME** (owner "เออสวย" on the demo, then "ใส่เลย"):
  six dashes along the same zigzag as now (`nextCut`), each one ParticleFX's Dash Strike black with a neon purple rim like the X
  (owner "Dash Strike โทนเดียวกันได้ไหม"; `fx/pfx_dashstrike_v.png`, the monster's hit flash violet: streak frames 0-11 along the dash, its own hit flash 13-28 on every monster), no
  thousand cuts, then the closing X = twin fang black from its first frame with a neon purple rim
  (`fx/pfx_twinfang_k.png`); colours sampled from the owner's neon samurai picture; one dash 0.2 s (SK4.cut is 0.12
  now), Dash Strike played at 20 fps; she holds the dash row's frame 6 with a violet glow until the X ends. Sheets made
  by `tools/art/rogue_dash_fx.py`. In the game: `nextCut` lays the streak along each dash (frames 0-11, rotated, scaled to the
  dash length, `fps: 20`), every hit plays frames 13-28 on each monster in the circle, `starFinish` plays
  `pfx_twinfang_k` x1.3 at the circle's middle, she glows violet; SK4 cut .2, end .85; `drawPfx` now takes `f.fps` and
  scales turned effects (`rot` + `sc`).
- **Archer fixes** (owner "ลูกธนูไม่ตรง สกิลไม่สวย", "6 ให้นักธนู"): PixelLab drew its own arrow flying off (often upward) in
  the attack / crit frames while the game shot its cyan arrow at the target = two arrows that did not line up; those rows
  are now built with `act_sheet.py --detach=attack,crit` (only the blob joined to the figure stays; `hero_build.sh`
  passes it for the archer). The game arrow starts at the bow (h 46), its tail never reaches back past the bow, it has
  a pointed head, and arrows flying up the screen are depth-sorted behind bodies (`away`). X is now ฝนดาว: aim a spot,
  she shoots up, ParticleFX's starfall barrage (`fx/pfx_starfall_c.png`, recoloured to the archer cyan, haze and cell
  edges faded) rains for ~1.4 s from 1.3 s in (10 ticks of 12 on everything in r 150) and she gets the old hawk eye for
  8 s. Owner: don't touch the rogue's skill 4 yet (they are making GPT art for it). Test views: `?test=arr&hero=archer&a=<deg>`
  one shot at a monster in that direction.
- **Thai forest map** (`?map=jungle`, owner "เมืองไทยก็ให้แผนที่ต่อไปเป็นป่าเมืองไทย มอนเมืองไทย ละค่อยๆ ไล่ไปจนถึงเมืองอื่น"):
  `JG` (TH stays true, so the Thai ground and props are used), no city (`HAMLET` off the map), jungle groves
  (`FORESTS` x7) round a winding road, a creek with the plank bridge, a lotus pond, prang ruins (`RUINS`), a hunters'
  camp and a pavilion in two clearings (`MEADOWS`), Thai monsters (`ROSTER.jungle`, boss Chalawan); built by
  `jungleProps`. Roads: `EXITS[MAP]` = west / east end → map (null = sign only): west ↔ thai ↔ jungle → China (sign
  "เมืองจีน → (เร็วๆ นี้)" until the China city exists); `spawnAt` puts her at the end she came in by.
- **World layout** (owner 2026-11-09 "อันนี้เมืองนะ ในเกมส์ให้มีเมืองแยกๆ ไป ละก็มีแมพต่อกันเป็นแผนที่ ไม่ต้องทำเมืองแบบนี้ตลอด"):
  cities are their own places (the Thai walled city is one); between them come field maps joined edge to edge into a
  world map. Not every map needs a walled city. Per country: one city (China's is big) + several linked field maps
  (forest, village, river, ruins ...) with that country's monsters; the boss sits on a field map or at the city.
- **China monsters in** (Codex `codex/mobs-china`, 2026-11-09): paper_doll, jiangshi (hops in, lunge), fox_spirit (blue
  fox-fire shots), terracotta_archer (crossbow bolts), toad_demon (tongue, reach 130), terracotta_general (stout), boss
  boss_nian (sheet once Codex finishes it); `ROSTER.china`, `BOSSK.china`; until the China map exists they can be tried
  on any map with `?set=china` (`MSET`); `?test=mobs&set=china&x=3400&y=2700&clear=1` shows them in a row without props.
  Owner: the China map is a BIG city ("เมืองต่อเป็นเมืองใหญ่เลยนะ") → MAPS.md 2 + 2b building sheets. Owner "ประตูเจนมาเลย
  4 มุม" + "เจนแบบมาพร้อมประกอบ": MAPS 0a (Thai gate front / back / left / right) and 0b (wall kit: across runs front +
  back, north-south runs west + east, end caps, 4 corners) go first; the grass gap the owner saw was only the join
  between two of my screenshots (the game's fort tops are complete).
- **Long Codex queue** (owner "สั่งเลย ไม่ต้องรอฉัน มอนเจนจนเครดิต Codex หมด"): 21 more monsters in MOBS.md rows 23-43
  (Japan: kappa, kasa_obake, oni, tengu, rokurokubi, nekomata, boss_orochi; Egypt: mummy, scarab, jackal_warrior,
  sand_scorpion, cobra_priest, sand_golem, boss_sphinx; Norse: draugr, frost_wolf, troll, ice_wraith, dwarf_berserker,
  ice_golem, boss_jotun), their walk / attack / death / hurt in MOB_ANIM.md (`tools/art/mob_anim.py`, sizes in
  `mob_frames.py`), and `docs/codex/action/MAPS.md` (Thai wall top pieces, China buildings / village / nature / props /
  ground sheets). Owner sent a crop of a corner where the side walkway looked missing: "เจนบนกำแพงมาปิด" → MAPS row 1.
- **Thai city walls rebuilt** (owner "แมพไทยไม่สวย กำแพง"): the city is a rounded rectangle (`cityD`, |dx/rx|^8 + |dy/ry|^8;
  ground, yard checks and walls follow it; the west map keeps its ellipse). `tools/art/thai_wall.py` makes a seamless
  54 px front tile from wall_sema (no bushes: they were painted on both ends and piled up), a raised side-wall walkway
  piece (`wall_side`, its feet = picture bottom so the walkway sits 80 px up) and the corner fort in whitewash
  (`t_fort_w`, brick mapped onto the plaster ramp, roof kept). Straight north/south runs, straight east/west runs open at
  the road, forts on the 4 corners, gates where the road crosses.
- **2nd class at level 50** (owner 2026-11-09 "เปลี่ยนคลาส 2 ที่ 50 ยังไม่ได้ทำ", "มอนเราจะต้องเยอะ"): hero level cap raised to
  50; the class change itself is not built (rogue rank 2 = two daggers, needs new moves). Many more monsters needed for
  50 levels: one set per country map (forest/ruins, Thai, China next).
- **Archer playable** (2026-11-09, `?hero=archer`, pick button นักธนู): sheets from `hero_build.sh archer` (adds the `crit`
  row; hurt / death merged from two download groups; release frames by hand). Normal shot = one cyan code-drawn arrow
  (`arrow`, `archerShot`); crit (12% base, +40% in hawk eye, or the nearest monster beyond 420 = passive) plays the
  kneeling crit row and fires a bigger piercing gold-edged arrow; passive ล่าเหยื่อ: up to +50% damage by distance, beyond
  420 always a crit; hit timing from pixelfx's moves/arrow-shot (held breath `preMs` 120, thud = hit-stop .07 + shake).
  Skills `ARS`: Q split arrow (the owner's ParticleFX emitter graph rebuilt in code, cyan: lead arrow → star flash + ring →
  5 arrows drop on the nearest monsters, each with flash, sparks, ring, ground glow `gmark`), E thunder javelin
  (`fx/pfx_skyarrow` from the owner's thunder-javelin sheet, lands 0.43 s in, +1 javelin every 3 levels; `G.later` timers),
  R charged shot (hold, 3 draw levels on the crit row, release = a long piercing cyan beam, owner "ชาร์จง้าง ดูยิงรุนแรงไกล"),
  F leap back on the roll row + a parting shot, Z vine arrow (roots 2 s, Codex root spikes), X hawk eye (`p.hawk`, 8 s).
  All her effects share one cyan tone (`ACY`, owner "ปรับให้สีโทนเดียวกัน"). Skill moves (shoot up, leap back) not made.
- **Frozen monsters in an ice block** (owner pasted pixelfx's `ice/freeze` code): exported with an empty actor so only the
  block, floor frost and shatter show (`fx/pfx_freeze`, 121 frames 176x128, pivot 88,108); `statusTick` notes when a
  freeze starts (`m.frzOn`, `m.frz0`), `drawMob2` plays the climb + seal (0.6 s), loops the held block, cracks in the last
  0.3 s, then the burst plays as an effect; scaled to the monster's size. `drawPfx` takes `sc`.
- **Monster hurt rows in** (Codex, `codex/mob-hurt`, 15 pictures, made in its own worktree as asked): `mob_frames.py`
  now builds 4 rows (walk / attack / death / hurt) and skips monsters without pictures (the China set); stout monsters
  (golem, bosses) flinch with the first hurt frames without stopping (`m.flT`). `?test=mobs&ph=3` shows them.
- **Buffs from ParticleFX** (owner 2026-11-09): orbiting rock shield ("เอาไว้เป็นบัฟให้ตัวเพิ่มป้องกัน", 10x9 frames →
  `fx/pfx_rockshield`) = the swordsman's iron shield (passive renamed เกราะหิน): rocks orbit him while the shield has points
  (bigger as it fills, far half behind him, near half in front: `rockRing`), and hits are cut 15% before the shield takes
  them. Wind barrier ("บัฟหลบหลีก", 8x8 → `fx/pfx_wind`) = an evasion buff `EVADE` for every hero: 3 s after each
  dodge or teleport, half the blows miss ("หลบ!"), `windRing`. Tests `&iron=30`, `&evade=1` on `?test=hsk`.
  Also downloaded, not used: `freeze-effect-sheet.png` (ParticleFX's own knight freezing; a sprite effect on their sample
  character; owner asked about a form: it needs our own sprite in "Effects on my sprite").
- **More ParticleFX sheets** (owner 2026-11-09, sent without a skill named; placed by Claude): `whirlwind-sheet` (5x5) →
  `fx/pfx_whirl` = the E whirlwind ring of the rogue and swordsman (and their icons); `blazing-combo-sheet` (6x5, three
  fire arcs round a centre, anchor 'b' = box centre) → `fx/pfx_blaze` = the swordsman's swings while berserk (arc 1 frames
  0-9 for the first hit, arc 3 with its impact frames 18-29 for the last, turned to the facing; `drawPfx` now takes `f0`,
  `fn`, `rot`); `dash-strike-sheet` (6x5) → `fx/pfx_dashstrike` (frames 12-28, the violet cut) on every monster the rogue's
  F zigzag hits, turned along the cut. Test `?test=hsk&hero=swordsman&k=0&rage=1`.
- **Mage E chain lightning = ParticleFX** (owner 2026-11-09 "สกิล 2 เมจ", `art/incoming/pfx/chain-lightning-sheet.png`, 6x6
  frames of 684x488, 4 orbs joined by bolts): `tools/art/pfx_chain_parts.py` cuts one orb (`fx/pfx_orb`, put on every
  monster hit) and one bolt laid flat (`fx/pfx_bolt`, stretched and turned between each pair in `drawChain`), the faint
  full-frame haze removed; the code ground bolt stays. Icon = the orb.
- **Dodge → teleport upgrade** (owner 2026-11-09 "เอาท่าเทเลพอร์ตไปใส่แทนกลิ้ง ให้อัพสกิลที่วิ 1 พอยท์"): a row in the skill book
  (Space · กลิ้งหลบ, + = 1 point) sets `p.tele`; `startRoll` then calls `startTele` (`TELE`: 210 px in the move direction,
  avoids water, 0.35 s untouchable, 22 stamina) with ParticleFX's shadow step at both ends (`fx/pfx_step_v` violet for the
  rogue, `pfx_step_t` the original teal for the others; 48 frames, `pfx_sheet_import.py` now takes a frames folder).
  Carried between maps; the phone button reads วาร์ป. Then (owner) the mage teleports from level 1, and the teleport has
  5 levels (`p.tele` = 0..5, 1 point each, reach `teleDist` = 170 + 40 x level: 210 → 370).
- **Rogue R smoke = ParticleFX cartoon smoke poof** (owner 2026-11-09 "ควันใช้อันนี้"): `art/incoming/pfx/smoke-poof-sheet.png`
  (870x864 = 6x6 cells of 145x144, 36 frames; 6x7 cut the clouds) → `fx/pfx_smoke.png` (200 px wide, 30 fps). Also from
  ParticleFX, waiting for the owner: frost crescent slash (`fx/pfxfrost<deg>`), teal star missile (came out white / red,
  a thin streak: maybe the archer's arrow), violet shadow step (came out teal; recoloured copies in
  `art/incoming/pfx/*_violet`, `*_teal`).
- **Archer** (2026-11-09): owner's GPT turnaround (`art/incoming/action/archer/turnaround_gpt.png`, front and side views
  touched: split by hand + `T128_GAP=2`), PixelLab character fcf9d983-0c95-4e43-8fb8-59053eb5fa7e "Forest Archer 128" (v3,
  2 generations, 8 views good). Owner "ท่ายิงสวยๆ ให้ขยับตัวยิง 1 หากคริให้เปลี่ยนท่ายิง": `hero_jobs.py archer` = 46 jobs
  (idle / run / roll / hurt 8 dirs, attack = one lively shot 16 f and crit = kneeling power shot 16 f in E S N NE NW,
  death E S W N), queued 2026-11-09 ~09:55 (1845.5 generations left before).
- **Meteor experiments** (2026-11-09): `?mfx=parts` (Codex pieces moved by code, owner: "ไม่ผ่าน"), `?mfx=codex`, `?mfx=star`
  (ParticleFX Studio's starfall barrage, `tools/art/pfx_sheet_import.py`, sheets the owner downloaded in
  `art/incoming/pfx/`); owner "ใช้ของเดิม": the default stays pixelfx (first meteor = Codex ink comet). ParticleFX Studio
  (particlefx.studio) has an MCP server (https://mcp.particlefx.studio/mcp, `Authorization: Bearer ${PFX_API_KEY}`, key from
  its billing page, MCP calls paid from build packs); not connected yet (adding it to `.mcp.json` needs the owner's OK).
  Reference pictures for its "Match a reference" in `art/incoming/pfx_ref/`.
- **Living effects** (owner 2026-11-09, a clip of a side-view pixel action game: "การแพรี่ การฟัน สกิล มันเหมือนมีชีวิต",
  "สกิลเหมือนมันแยกกัน", "เค้าไม่ได้เจนภาพมาเป็นก้อนไหม"; note: pixelfx's meteor is 46 frames, Codex's pictures 6): code
  parts tie the effects to the body: `parts()` shards with gravity and bounce / embers / speed lines (`G.fx` k 'pt');
  `weaponTip(p)` = staff crystal or blade; casts gather light there during the wind-up (`act` option `wind`, `drawWindUp`)
  and burst out on release (`releaseAt`, the hero glows in the skill's colour `heroGlow`); chain lightning also runs along
  the ground; slam / leap throw debris; the parry is a ring of light round the body that shatters into shards on a
  counter; hits throw sparks off the blade; monsters flash in the colour that hit them (`m.hitC`, `tintSheet`), shocked
  ones flicker violet, burning ones glow orange.
- **Ink effects, moving effects, monster flinch** (2026-11-09): Codex's 3 ink pictures on green (`fx_codex_import.py` mode
  `green` = chroma key) → `cinkflurry` (rogue F finish, `starFinish`), `cinkcres` (swordsman charge level 3 = a flying
  sword wave `G.pshots` k 'wave' that cuts every monster it passes once; the counter = a crescent sliding forward),
  `cinkcomet` (the first meteor of the mage's shower). Owner "ทำ vfx ให้เคลื่อนไหวได้": `f.mv` (steady speed) and
  `f.dox/doy` (a follow effect sliding away) in the fx step; the swing's ice crescent slides forward; hotbar icons loop
  their effect's frames while the skill is ready (`iconFrames` / `skIconAnim`). Monsters flinch when hit (squash + lean
  back from `m.hit`) until Codex draws a `hurt` row: MOB_ANIM.md now has a hurt row per monster (88 rows) and
  `mob_frames.py` adds the row when `<key>_hurt.png` exists; `drawMob2` plays it during the stagger.
- **Skill levels to 10, meteor shower** (owner 2026-11-09 "สกิลเมเทโอ ... เลเวล 10 5 ลูก ดาเมจคำนวณเอาไปก่อน"): `SKMAX` 10,
  `SKUPD` +10% damage and `SKUPC` -4% cooldown per level, heroes up to level 40. Mage Z drops `meteorN(lv)` meteors
  (owner's correction "8 ก็ 4 ลูกสิ": level / 2, at least 1: levels 1-3 one, 4-5 two, 6-7 three, 8-9 four, 10 five), the first on the aimed spot, the rest around it 0.2 s apart, each
  full damage (60 x level factor). Test `?test=hsk&hero=mage&k=5&lv=8&n=96`.
- **Skill bar + skill book** (owner 2026-11-09 "ทำ ui ให้มีสกิลลงช่องล่าง และตารางอัพสกิล"): PC hotbar of 6 slots bottom centre
  (`#hotbar`, icons cropped from each skill's effect sheet `SKICON`, cooldown shade + seconds, level pips, hover tip); the old
  PC squares `#skpc` are hidden; phones keep the round buttons. Levels: kills give XP (`gainXp`, max hp / 8), `needXp(lv)` =
  40 + 30 (lv-1), up to 20, 1 skill point per level, XP bar under the stamina. Skill book (`B` or the สกิล button, pauses with
  `G.paused`): name, description, cooldown, level 1-5 pips and a + button; each level = +20% damage, -8% cooldown
  (`applySkLv` rescales the numbers in `SKS` from `SKBASE`). Level, XP, points and skill levels travel between the maps.
- **Rogue E = whirlwind, mage Z = pixelfx meteor** (owner 2026-11-09 "สกิล E นักดาบเอาไปใส่ให้มีด", then pasted pixelfx's
  meteor code + "สกิลอุกกาบาตเมจ"): `startWhirl(p, S, k)` shared by both (rogue: tap = a short spin, held = keeps
  spinning; her body turns through the 8 swing frames `whirlDrawRogue` like the old spin, Codex's wind ring, after-images;
  old `startSpinOld` kept). Meteor: pixelfx `fire/meteor` → `fx/pmeteor.png` (`pixelfx_import.py <dir> fx pmeteor`, 46
  frames at first; owner: "152 เฟรม ในตัวเว็บบอกเอง" → now all 151 frames at 30 fps, rendered with `tools/pfx_export.py`, 12 columns so
  the sheet stays under 4096 px), lands at 0.8 s, spawned 0.8 s before the impact so it lands on time; Codex's meteor stays as the fallback.
- **Codex effects in** (2026-11-09, 17 pictures on black from `codex/fx`, squashed in): `tools/art/fx_codex_import.py` →
  `fx/c*.png` (mode add = brightness becomes see-through, solid = black joined to the edge goes; size = widest frame in
  game px; fireball, ghost fire and the ground crack also as 24 turned copies `<key><deg>`, the crack squashed to the
  ground). Used for: mage fireball flight + hit, meteor fall (from the top left) + hit, frost nova, mana shield bubble,
  blink; swordsman ground crack, whirlwind ring, berserk aura, leap slam; reactions steam / shatter / overload; monster
  ghost shots (khamot = hue-shifted green), shroom spores, treant roots, Chalawan / phrai water wave (`MOBT.fx`, mirrored
  with `pfx(..., {flip})`). The three ink-style big skills (FX.md rows 18-20) are still to do by Codex.
- **Swordsman + mage playable** (2026-11-09; pick on the start screen, `?hero=` or the last pick in localStorage `act.hero`;
  `HERO`, sheets `art/action/<hero>*.png` from `bash tools/art/hero_build.sh <hero>` (hit frames by hand there, leap landing
  frame = the leap row's hit)). PixelLab: base moves 41 jobs each (idle / run / roll / hurt 8 dirs, attack 16 f E S N NE NW,
  death E S W N) + skills (`hero_jobs.py <hero> skills`: swordsman spin S, leap 16 f / guard 4 f / charge 8 f in E S N NW;
  mage cast_up / staff_slam 8 f in E S N NW) = ~100 generations for both; 1847.5 left on 2026-11-09. The queues stopped
  when the PC slept; `pl_queue.py` now downloads a job the server already finished instead of stopping.
  Code: skills play frame lists in an `act` state (`playAct` / `endAct`: frames, times, events per frame, tick, loop for
  held skills; `HOLD` + `holding(k)` for E / R of the swordsman). Swordsman (`SWS`): normal attack sweep + slam with
  streak cuts + a white X flash (`cutFx`) and a big ice crescent per swing (`swordArc` = the rogue's PixelLab `dslashl` crescents;
  owner's clips 2026-11-09: clip 3 ice sword = normal, clip 2 crimson = while berserk, `CUTP` + a hue filter on the crescent); Q `groundSplit` crack line + stun,
  E whirlwind while held (stamina drain, rogue's spin ring), R charge 3 levels then the sweep (level 3 = gold crit), F leap
  to the aimed spot (lands on the hit frame, ring + quake + stun), Z parry (`swCounter`: no damage, x3 counter), X berserk
  (`p.rage`: 28% faster swings, lifesteal, -20% damage, red aura `au_red`); passive iron shield (`IRON`, bar under the
  stamina). Mage (`MGS`): two homing bolts per attack (`mageBolt`, `G.pshots`), Q fireball (burn), E chain lightning,
  R frost nova (`m.frz`), F blink (move direction), Z meteor (`G.meteors`, telegraph ring, 1 s), X mana shield (`p.msh`,
  bursts into lightning when broken); passive elements (`applyEl` / `react`: steam, shatter, overload, floating Thai text
  `G.tags`). Mob statuses: `m.stun`, `m.frz` (blue tint), `m.burn`. Test `?test=hsk&hero=..&k=0..6&n=steps[&rel=]`.
  Codex works in the same folder and switches branches, so Claude now works in a separate worktree
  (`C:\last-signal-pvp-claude`, branch `claude/work`, preview "game-claude" on port 8001) and pushes to main.
- **Monsters in the game** (2026-11-09): slimes replaced by the sprite monsters (`MOBT` stats per kind, `ROSTER` per map:
  west = shroom wolf skeleton goblin_archer wisp boar_guard golem, thai = khamot monkey krahang phrai croc_guard pret;
  `BOSSK` treant / Chalawan every 5th wave with a boss bar at the top). `stepMob2`: walk to the player (shooters hold
  `keep` distance and strafe), attack = frames 1-3 wind-up over `tell` with a red ring under them, frame 4 the hit
  (`mobStrike`: melee reach in front, or a shot: arrow / fruit / ghost fire in `G.mshots`), frames 5-6 recover, then
  `cd`; hits stagger them unless `stout`; `kb` scales knock-back; flying ones ignore water; blinded / player hidden =
  wander. Death row plays, then fades. Slime code kept as the fallback (`spawnSlimes`) and for the old tests.
  `?test=mobs[&map=thai]&ph=0|1|2` = every monster of the map in a row (walk / attack / death frame).
- **China monster set queued** (owner 2026-11-09 "มอนเราเป็นแถบประเทศ ต่อไปเป็นจีน"): MOBS.md rows 16-22 (jiangshi, paper_doll,
  terracotta_archer, terracotta_general, fox_spirit, toad_demon, boss_nian; folklore only, no worshipped gods) and their
  walk / attack / death in MOB_ANIM.md rows 46-66 (after the turnarounds); sizes already in `mob_frames.py`.
- **pixelfx without Node** (owner: "มี md ที่จะทำให้ Claude ทำ vfx สวยๆ ไหม"): the pixelfx Claude skill is installed as
  `.claude/skills/pixelfx/SKILL.md` (with a local note); checkout in `.tools/pixelfx` (untracked, re-clone on a new
  machine); `python tools/pfx_export.py` serves it with an export page for the built-in browser (`contact()`, 
  `exportAll()` → `.tools/pfx_out/`). 35 effects already rendered as a fallback (meteor, fireball, frost-nova,
  ice-shatter, chain-lightning, blink, divine-shield, spin-slash, ground-slam, root-snare, spore-burst, status
  rage / stunned / frozen / burning ...). Owner: Codex's effects first, pixelfx when those are not pretty.
- **Monster frames in** (Codex finished 45/45 by 07:55 on 2026-11-09, `codex/mob-anim` squashed into main): pixel sheets
  `art/action/mobs/<key>.png` + `.json` + `index.json` from `tools/art/mob_frames.py` (white cut, 3x2 cells, each action
  scaled so its frame 1 is `SIZE[key]` px tall: small ~46-58, medium ~60-80, large ~96-118, bosses ~160; feet of frame 1 =
  anchor, other frames keep their place in the cell; 32 colours + 1 px outline; khamot is flipped, Codex drew it facing
  left; its last death frame is empty on purpose). Rows walk / attack / death, 6 frames, hit = frame 4 (index 3).
- **Effects brief for Codex**: `tools/art/fx_codex.py` → `docs/codex/action/FX.md` (17: mage fireball, meteor + hit,
  frost nova, mana shield, blink; swordsman ground crack, whirlwind, berserk, leap slam; monsters spore cloud, ghost fire,
  root spikes, water wave; mage reactions steam, shatter, overload). 3x2 on PURE BLACK → brightness becomes alpha on import.
- **Monster frames by Codex** (owner 2026-11-09 "มอนไม่เจน PixelLab", "เฟรมเจนเอา ให้ codex ทำ"): `tools/art/mob_anim.py` →
  `docs/codex/action/MOB_ANIM.md` (45 jobs = 15 monsters × walk / attack / death; one picture each, 6 frames in a 3x2 grid
  of 512 px cells on white, side view facing right only, the game mirrors it; the monster's turnaround attached;
  attack frame 4 = the hit). Files arrive as `art/incoming/mobs/anim/<key>_<action>.png`. The same prompts are on
  `docs/action-prompts.html` for ChatGPT. Monsters only face left / right in the game (no front / back rows).
- **Monsters from Codex** (2026-11-09, ~8 min, Codex worked straight in this folder on `main` instead of a branch): all 15
  in `art/incoming/mobs/<key>.png` (1536x1024, cel-shaded chibi turnarounds, front / right profile / back, all usable) +
  `REPORT_TH.txt`; 128 px views (free, `white_cut.py --no-ring` → `turn128.py`, each figure 118 px tall for now) in
  `art/incoming/mobs/px128/<key>/`; Chalawan's views nearly touch → `T128_GAP=4`. Ready-to-paste GPT page
  `docs/action-prompts.html` (`tools/art/action_prompts_page.py`, from MOBS.md). Not in PixelLab yet (credits: ask).
- **Swordsman + mage in PixelLab** (owner "เอาท่าจำเป็นก่อน สกิลยังไม่ต้อง" → "เจนเลย"): 128 px views from the GPT pictures
  (`px128/`; the mage needed the inside-white cut, no `--edge-only`), characters made with v3 + our south / east / north:
  swordsman 5b37a57c-6137-4831-9e9e-fea7115e3d2f, mage f04219c6-4a1a-4efa-a52e-5deadb67984d (2 generations each, all 8
  views good; the mage's north-west hides the staff behind him). Base moves = `tools/art/hero_jobs.py <key>` →
  `art/incoming/action/<key>/jobs_base.json` (41 jobs: idle + run 8 dirs, attack 16 f E S N NE NW, roll + hurt 8 dirs,
  death E S W N) through `pl_queue.py` into `<key>/pl_dl/`.
- **Poison 10 s + passive** (owner 2026-11-09 "บัพพิษอยู่นานกว่านี้ 10 วิ ... เพิ่มคูลดาวน์ เพิ่มพาสซีฟสกิล"): `SK6` dur 10, cd 20.
  Passive "จังหวะสังหาร" (`PAS`): every 4th strike that lands (one count per game step, so a swing that hits 3 monsters
  counts once and all 3 crit) does ×2 with a gold crit-hit (`fx/critg.png` = `critx_ice` recoloured gold, free) and big
  gold numbers; 4 diamond pips under the bars (`#pas`, all glowing when the next strike crits) + a gold glint at her blade;
  every kill gives 10 stamina (`mobDie`, now the only kill path; guarded against double kills). PC skill squares moved to
  top 74 px. Test `?test=pas&n=<steps>`.
- **Skills 5 and 6** (owner "สกิล 5 6 ช่วยคิด" → my two proposals → "จัดมา ขอสวยๆ"; no new moves, no credits): Z / ล่องหน =
  **vanish** (`SK5`: 4 s, cost 20, cd 12): purple VFX `smoke_poof` (`fx/vanish.png`), she is drawn as a see-through purple
  shadow (ctx.filter grayscale → sepia → hue 228° → saturate, alpha .62, purple glow, rising purple wisps), runs 30%
  faster, monsters lose her (random hops, no lunges); her next attack or attacking skill (`unstealth` in `startAtk` /
  `startSk`) opens a .9 s ambush: every hit ×3 with a purple VFX `crit_hit` (recoloured, `fx/ambush.png`) and big purple
  numbers. X / พิษ = **poison blades** (`SK6`: 7 s, cost 15, cd 14): VFX `charge_up` green on cast, a green glow on her
  hand, green bubbles, her slash glow hue-rotated green; every hit adds a stack (`poisonAdd`, max 5, ticks 2 × stacks every
  .6 s for 4 s, green numbers, VFX `poison_bubbles` loop over the monster + one pip per stack); at 5 stacks it bursts (28,
  VFX `fire_blast` recoloured green `fx/pburst.png`) and splashes 2 stacks onto monsters within 90. Every hit of hers goes
  through `rogueDmg` (doHit, hitMob, knifeLand); deaths by poison via `mobDie`. Phone: 2 more buttons (ล่องหน, พิษ) left of
  the arc, purple / green while active; PC squares Z X. Tests `?test=stealth|venom&n=<steps>`.
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

## Thai map (owner 2026-11-08 chose "a separate map")
`action.html?map=thai`: walk off the east end of the first map's road (signpost + "เมืองไทย →" label) → fade, hp / stamina /
kills carried in sessionStorage (`act.carry`), `?map=thai&from=west` starts at the west end of the Thai road; its west end
leads back (`travel`, `spawnAt`). Same chunk ground with the owner's riverside textures (`TEXF`: rv_dirt road, rv_mud shore,
rv_water, planks for the bridge deck, reeds in the paddies) and layout per map (`TH`): a wide river (`SWC` 118 ± 16,
`riverX`) through the middle with a plank bridge, a walled royal city west of it (sema walls, four forts, two gates on the
road, palace, temple, stupa, bell tower, sala, library on the lotus pond, lions, flags, elephant statues, houses, smithy, tea
house, elephant stable, a market of stalls along the road, Thai lanterns), stilt houses standing in the river on both banks
with kitchens, granaries, wells, jars behind, boats and lotus on the river, a temple on the east bank, rice paddies with
dikes (`PADDY`, kind 8) with a watchtower, buffalo pen, granary, huts, an ox cart, prang ruins in the north-east jungle,
jungle groves of coconut / sugar palms / bananas / rain trees (`thaiProps`). Pieces: the owner's four GPT sheets (`gpt_thai_*`)
→ `white_cut.py --edge-only --no-ring`, spaced into a 6×3 grid → `tools/art/thai_props.py` (heights per item, water cut in
the full-size sheet under stilt houses before the colours are reduced) and `ground_px.py ... 0.44 20 rv_dirt,rv_mud,
rv_water,planks,straw,reeds`. Overview: `action.html?map=thai&test=map`.

### Map fixes (owner 2026-11-08 "แก้แมพต่อ บางอย่างแบ็คกราวด์เอาออกไม่หมด เงาลอย ไปทำน้ำ ไม่ต้องรออนุญาต")
- Leftover white background between posts: flat pure-white patches (> 60 px, min channel > 225, chroma < 16) plus their pale
  fringe cut from v_pen, v_well, t_stall, v_kitchen, v_pavilion, t_sala, v_stall, v_granary, v_watchtower, v_bridge,
  bridge_curve. NOT from t_palace, t_temple, v_stupa, t_stupa, t_gate, t_belltower, v_temple, shop, chapel (their own white
  walls / awning stripes; checked by marking the patches in magenta).
- Floating: most GPT props have 4–10 empty rows under their base, so they stood above their shadows → `loadProps` finds each
  picture's lowest opaque row (`GPROP[n].foot`) and `gp` pins it (fy = foot - 2); the crown shade (`ao`) only under oak /
  pine / blossom / rain tree, smaller and on the ground round the trunk (on palms and bananas it hung mid-trunk).
- Water: the Thai map uses the clear blue `water` texture (the muddy `rv_water` looked dull grey); foam laps at every shore on
  both maps (`SHORE_PTS` = water cells next to land with the way to land, drawn in `drawGround`: a short white / pale line
  washing toward the land and back, a slow wave along the shore); twice the sparkles on the Thai river.
- Thai city floor: `art/action/ground/laterite.png` = the cobble texture's brightness on an old red laterite / brick ramp
  (#4a261e … #d69668, 20 colours), used for the Thai map's yard instead of the grey European cobbles.

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
- **Berserker skill kit planned** (owner 2026-11-09 "สกิลจุดเด่นแรง ท่าค่อนข้างกว้าง แต่ช้า แต่หนักหน่วง ให้มีท่ารวบโดยใช้โซ่ โทนดำแดงนีออน"):
  `docs/berserker.md` (passive + Q chain gather → 360 cleave, E triple cleave, R charged ground slam, F chain hook dash, Z chain
  shackle ring, X berserk ult; wide, slow wind-ups with super armor, heavy stagger; the PixelLab moves list). Side view fixed in code
  (`tools/art/berserker_side_fix.py`: red X moved off the sword hand, shorter grip) → `side_v4_fix.png`. Effect prompts `bz_*` in
  `docs/fx-prompts.html` (tone black + neon red); `archer_fx.py --tone=red <key>` makes `fx/<key>_r.png` in that tone. Not in the game yet.
- **Swordsman X rage changed** (owner 2026-11-09 "เอาลดดาเมจออก เปลี่ยนโจมตีแรง 20 ... ของเดิมไม่มีดูดเลือด ต้องเป็นเบอร์เซิร์กก่อน"): no lifesteal, no
  damage reduction; faster swings + damage +2% per skill level (+20% at 10) (`SWS[6].atk`, in `heroDmg`); then 10 s, cooldown 60 s (Berserker awakened: 15 s, 60 s). Lifesteal etc. come with the
  Berserker's awakened rage (`docs/berserker.md`).
- **Berserker PixelLab prep** (2026-11-09 evening, cloud session in "boxchaychan games"): `get_balance` there = the FIRST trial
  account (1.25 of 40 + 5 daily bonus = 6.25 usable; its characters are the old rogue / Wukongs). The paid Apprentice account
  (~1,800 left) is only on the owner's PC (`PL_KEY`); the cloud secret was never switched to it. 128 px views made (free):
  `white_cut.py --no-ring` on front_v2 / side_v4_fix / back_v2 → `tools/art/join_views.py` (the three separate GPT pictures came at
  different sizes: each scaled to the same body height, feet to head top over the feet, so the sword over the head does not
  count) → `turn128.py ... 128 32` → `art/incoming/action/berserker/px128/` (south 113×111, east 113×107, north 116×105; the
  greatsword makes him wide, so `turn128.py` now shrinks a figure to keep `T128_MARGIN`=6 px free at both sides). Body ≈105 px
  vs the swordsman's 120 → build his sheets with `--scale=3/4` (not 2/3) so he stands as tall as the swordsman in the game.
  Plan on the trial account: create_character v3 (south + east + north given, PixelLab draws the rest, 2) + 3 PixMiniMax
  8-frame south-east jobs (horizontal sweep, 360 spin, overhead slam, 1 each) = 5 of the 6.25. Owner: "มีเป็นพัน คนละรหัส เอาให้หมด
  ก่อน" → done, the trial account is now empty (log table above). Next, on the PAID account (PC, `PL_KEY`): import him first
  (`create_character` v3, reference = `berserker/pl_dl/Idle/rotations/south.png`, `direction_images` = the other 7 files there =
  0.25, nothing redrawn, like the rogue), then `pl_queue.py art/incoming/action/berserker/jobs_base.json <new id> art/incoming/
  action/berserker/pl_dl` (36 jobs: idle / run / roll / hurt 8 dirs, death E S W N, no attack) and `jobs_skills.json` (chain throw
  with the LEFT arm, south-east 8 f = Q / F). The 3 attacks stay in this download (they live in the trial account's character
  0e6da505; copy `bz_*` folders across if the new download overwrites `pl_dl/`). Not in the game yet.
- **Berserker handoff 2026-11-10**: attacks viewer `docs/berserker-attacks.html` (frames embedded; normal 12 fps / slow 4 fps / frame by
  frame / mirror; hit frames marked: sweep 2, spin 2-3, slam 4-5). Paid key on the cloud: re-saved through the secure form, but the
  proxy still reached the trial account for 12+ minutes (see CLAUDE.md); check `get_balance` first. Effect pictures for `bz_*`: the owner
  makes them in ChatGPT from `docs/fx-prompts.html`.
- **Sharp pixels everywhere** (owner 2026-11-10 "ภาพมันไม่ชัด" → "เอาไม่ย่อ" → "เอาฉากให้คม"): the blur came from scaling pixel art by
  fractions (heroes shrunk 2/3 at build time, then the whole world drawn ×1.52 on a 1080p PC). Now: heroes use PixelLab's own
  size (`art/action/n128/`, `N128=1 bash tools/art/hero_build.sh <hero>` / `rogue_build.sh`), drawn at a whole number of screen
  px per art px (`drawCell`); the world is drawn at S = a multiple of 1.5 (`ARX` 1.5 art px per world px, `onResize`; the view
  follows the screen, ≈1280×640 on a PC, 1.5 on most phones), and everything in it has 1.5× pictures drawn 1 art px per screen
  px: ground chunks painted at 1.5× (`chunkStep`, textures `art/action/ground_hr/` from `ground_px.py ... 0.66`, laterite from
  the cobble brightness), props `art/action/props_hr/` (`PROP_K=1.5` in `rebuild_props.py` / `thai_props.py` +
  `tools/art/props_hr_extra.py` for the wall / fort pieces; gates = props_px on the cut `thai_gate_4view.png` at 0=570;
  `drawProp` pins the hr picture at the low-res one's bottom centre), monsters `art/action/mobs_hr/` (`MOB_K=1.5 mob_frames.py`,
  `MOBS[k].d`; frost_wolf has no hr sheet, its see-through source frames are not in the repo). Effects are still scaled.
  `?ar=0` = the old soft fit, `?n128=0` = the old shrunk heroes, `?zoom=N` / `?hz=N` = zoom tests.
- **Swordsman Q = the owner's ParticleFX fire line** (2026-11-10, pasted 9x8 sheet on see-through, 66 frames, raw
  `art/incoming/pfx/fire-line-sheet.webp`; "ไปใช้คู่กับท่า 1 ดาบ ละทำช่องสกิลเป็นแนวยาว"): cut on a 222x79 grid → `fx/pfx_fireline.png`
  (manifest `len` 133 = the line x 35..168 at y 50, anchor at its near end). `groundSplit` lays it along the crack (k 'esplit' with
  `key`, from frame 0, scaled to the crack's length, height ×.85 of that), hits land as the fire runs out (t × .55 s); the
  Earthsplitter sheet stays as the fallback. Skills with `line: 1` (SWS[1]) draw a straight band as their aim marker (the
  crack's reach and width) instead of the range ring + target circle. Its skill icon uses the fire line too.
- **Norse monsters in** (Codex, branch `codex/mobs-china`, 2026-11-10): draugr hurt + troll, ice_wraith, dwarf_berserker, ice_golem,
  boss_jotun (walk / attack / death / hurt) → `mob_frames.py` + `MOB_K=1.5` (both sheets); `?test=mobs&set=norse` shows all seven
  with the boss. Queue `docs/codex/action/MOB_ANIM.md` copied from Codex's branch (172 rows done). frost_wolf keeps its low-res
  sheet (its see-through source frames are not in the repo).
- **Rogue 3-hit combo** (owner 2026-11-10 with Ozzbit Games' free hero template zip, "คอมโบเค้าสวยมาก ใช้กับมีดเราได้ไหม" → "คอมโบ 3";
  that pack is personal / non-commercial only, so nothing of it is used, only the idea): `atkPlan` gives the rogue's normal
  attack a frame list `fr` = the sheet's two swings, then its first swing again as a finisher (hits 10 / 11 / 17); each hit
  calls `rogueCres` = a crescent drawn in code (`drawCres`: fat white middle, neon rim, dark edge, squashed to the ground
  angle, the tail eaten toward the tip after 25%, sparkles off the tip), alternating forehand / backhand, the finisher
  bigger; red during rage.
- **Move-copy tool** (owner 2026-11-10 "ทำทูลขึ้นมาสำหรับการลอกท่า ... ให้ใช้ในโทรศัพท์ได้"): copies an example animation's POSES onto
  our own character (no pixels of theirs). Steps: PixelLab `estimate_skeleton` on every example frame (small figures are cropped
  and enlarged first, the 256 px limit) and on our still (0.1 each) → retarget: each of our bones takes the example bone's
  angle and keeps our length, built out from our hips; our own face rides on the neck → `animate_with_skeleton_v3`
  (`first_frame_url` = our still, `first_frame_keypoints`, view low top-down; 3 frames 2 gen, 4-14 = 3, 15 = 4), results from
  `GET /mcp/images/<job>/download?index=N`. Command line: `tools/art/pose_copy.py <frames dir | sheet.png[:cols]> <still.png>
  <out> "<looks>" [action] [direction] [--dry]`. Phone page: `posecopy.html` (GitHub Pages; the owner's PixelLab key is typed
  in and kept in that browser's localStorage only; PixelLab's API allows calls from boxchaychan.github.io): example file(s) →
  hero + direction from `art/action/n128/<hero>_still.png` (or an own picture) → อ่านท่า (preview of both skeletons) →
  สร้างท่า (plays the result, saves a one-row PNG). First test: Ozzbit's combo_1 + end (7 frames) on the rogue, east, 3 gen
  → `art/incoming/action/rogue/pose_copy_ozzbit/` (low lunge with the dagger forward, back to standing; she keeps her look).
- **Lessons from the owner's sample idle / walk** (2026-11-10 `sampleidlewalk.zip`, hand-made 64 px Aseprite files, not kept in
  the repo): idle 10 frames at 60 ms (the body barely moves, the hair and cloak sway and lag = secondary motion), walk 26 frames
  at 50 ms with a turn-around inside it, a 2-frame "from idle" link into the walk, 26-27 colours. Taken into the game (free):
  heroes turn through the in-between directions (`p.vd`, a step every 45 ms; a half-turn passes the front view), idle / run
  start from their first frame when the state changes (`p.stT0`), idle 7 → 9 fps. For future PixelLab idles / runs: ask for
  hair and cape swaying and lagging behind, more frames (12-16) where it matters.
- **Guardian moves copied from a knight pack** (owner 2026-11-10, "FREE Knight 2D Pixel Art v1.2": games OK incl. commercial, no
  redistribution as an asset, so its sheets are NOT in this repo; frames 112x96): `pose_copy.py` ATTACK 1 (8) / 2 (9) / 3 (11) /
  BLOCK (6) onto the Guardian's east rotation (paid character 4577584b…), 3 gen each = 12 → `art/incoming/action/guardian/
  pose_copy_knight/<move>/r*.png` + `preview.gif`: overhead cut into a lunge, a thrust, a low lunge cut, shield raised.
- **Guardian playable** (owner 2026-11-10 "ทำอัศวินโล่ให้เสร็จ ... แค่กลับด้าน", no new PixelLab jobs): `tools/art/guardian_build.sh`
  puts the paid download's idle / run / roll / hurt / death (8 dirs, death 4) together with the attacks we have: attack = knight
  copy 1 + 2 (east, hits 3 / 12) and gd_slash + gd_bash (south-east, hits 4 / 13); leap and charge = knight copy 3 (east) /
  gd_overhead (south-east); guard = knight block (east); every other direction plays one of those, mirrored for the left →
  `art/action/n128/guardian.*` + `art/action/guardian.*` (2/3, menu card). In action.html `?hero=guardian` (menu card อัศวินโล่):
  `SWL` = swordsman or guardian runs the swordsman's kit (SWS, `swordSk`, iron passive, parry on Z), the Guardian takes 25% less
  damage (`hurtPlayer`); skill names / icons / help copied from the swordsman (Z = ยกโล่สวน).
- **Guardian attack fixed** (owner "ท่าฟันโคตรไม่สวย", "ดาบก็สั้น ขยายระยะฟัน", "เสียเครดิตเจนไปตั้งเยอะ"): the knight-pose copies looked
  bad as attacks (the sword vanishes, the cape smears; ~16 credits that did not pay off, only the block is used), so the PixelLab
  south-east slash + bash (and the overhead chop for leap / charge) now play in every direction, mirrored for the left. Reach
  ×1.35, cone wider, and each hit draws a long gold-white crescent off his blade (`rogueCres(..., big)`).
- **Outfit system tried and dropped** (owner 2026-11-10 "ระบบประกอบชุด" → test → "เละตามเคย" → "ไปทำแบบเดิม"): a helmet drawn in code
  on the swordsman's head (head found per frame, hair cut above / beside it, back + front layers like the owner's clip) works
  technically but looks pasted on: our heroes are one flat picture, a real outfit system needs characters drawn in layers from
  the start. Classes stay separate characters (like the Guardian). The test stays behind `?helm=1/2/3` (off by default). A plain
  base body was made in PixelLab before testing (Base Body 128, 670a351b…, 3 gen; not used).
- **Berserker playable** (owner 2026-11-10 "เบอร์เซิร์กเกอร์ทำยัง", no new PixelLab jobs): `tools/art/berserker_build.sh` = paid base moves +
  chain + the trial's south-east attacks (attack = bz_sweep + bz_slam, hits 2 / 13; leap / charge = bz_slam; spin (E) = bz_spin),
  every other direction plays south-east, mirrored for the left → `art/action/n128/berserker.*` + `art/action/berserker.*`.
  `?hero=berserker` (menu card เบอร์เซิร์กเกอร์): the swordsman's kit via `SWL`, slower heavier swings (ATK base 54 / hit 115),
  damage ×1.3, reach ×1.35, red crescent cuts. His own kit from `docs/berserker.md` (chain Q, awakened rage X) is not built yet.
- **Guardian v2 in the game** (owner 2026-11-10 "ทำมาดิ อย่าโม้"): `tools/art/guardian2_build.sh` replaces the Guardian's sheets with the
  long-sword one: `attack` / `attack2` / `attack3` = combo1 (rise + downward cut, hits 4 / 7) / combo2 (spin, 3 / 8) / combo3
  (lunge thrust, 7), side view, every direction plays them (mirrored for the left); idle / run = the new character's 8 stills
  (96c2d44c…, downloaded to `guardian2/dl/`) on the same 132 canvas (no base moves made yet, so no roll / hurt / death frames:
  the code still falls back to the still); `fy` = the still's lowest row. `startAtk`: the Guardian steps through the three
  (`p.gc`), back to the first after 1.1 s without attacking. His code crescent is off (the moves carry drawn swooshes).
- **HD-2D test** (owner 2026-11-10, screenshots of a pixel game in a 3D world: "ลองดู"): `hd3d.html` (three.js r147 from jsdelivr) =
  a 30×22-tile test map of blocks (grass raised 0.32 above the road, water sunk, our `ground_hr` textures in world-space UVs, one
  picture per 4 tiles, nearest filter), trees / houses / tent / grass tufts and the Guardian (his n128 idle / run frames drawn
  into a canvas texture) as upright cards turned to the camera that cast real shadows (alpha-tested depth material), a warm low
  sun with soft shadows, fog, and one full-screen pass with a tilt-shift blur at the top / bottom, warm grade and vignette.
  WASD / left stick to walk, buttons for the blur and the zoom. Not connected to action.html; no monsters or combat.


### Berserker effects + chain Q (2026-11-10 evening)
- Owner "ทำ vfx ไว้ โทนแดงนีออน ดำ ไฟ": `tools/art/bz_fx.py` recolours every effect of the swordsman's kit by brightness onto one ramp
  (black smoke → crimson → neon red → red-orange fire core) → `fx/<key>_bz.png` (+ manifest); `BZFX` in action.html loads them for the
  Berserker only and swaps them in. The rage flames (`crage`) were already red and stay. His crescents (`swordArc`, `cutFx`) are always
  crimson, the charge / leap rings red; `chargeBlast` now keeps its orange glow under its own key (`glowOr`, it used to tint the berserk glow).
- Owner's own Q sheet (6×4 cells of 320 px on flat green, `art/incoming/pfx/bz_chain_sheet.png`) → `tools/art/bz_chain_import.py` →
  `pfx_bzchain` (chains, anchor = the caster's ring, turned to the aim) + `pfx_bzring` (ring cleave squashed .55 to the ground).
  Berserker Q is now "โซ่รวบวิญญาณ" (`bzChain` / `bzChainCast`): chain throw row, chains within 80° of the aim catch monsters (45% dmg,
  1.1 s stun, dragged in front of him), then at .5 s the ring cleave hits everything within 150 for 150%. In-game clip:
  `art/incoming/action/berserker/q_chain_ingame.gif`.
- Meta AI videos: `tools/video/vid2px.py` (green key, one shared scale for a locked camera, palette from a still, outline added later).
  The Berserker slash video (`meta_attack/`) is cut but not in the game yet; prompts in `berserker/video_start/`, video prompts on every
  card of `docs/fx-prompts.html`. Claude cannot make the videos (needs the owner's Meta AI login).
- Not on the live game yet (owner "หยุดประกอบ", "มันไม่สวย" about the recolours): the red effects, red crescents / rings and the
  chain Q only switch on with `?bz=1` (`BZTRY`).
- Effect videos → game sheets (owner "ทำทูลตัดเอฟเฟกต์จากวิดีโอไว้ใช้เลย"): `tools/video/vfx_cut.py <mp4> <key> --from --to --dur --size`
  (key colour read from the border, green or magenta; whatever reaches the frame edge fades out over `--edge` px; `--size` = the
  ground width in world px, from the widest band in the lower third; anchor = middle of that band, 10% above the bottom; 256-colour
  sheet → fx/<key>.png + manifest; preview GIF next to the Berserker in `art/incoming/fx_video/<key>/`). Phone page with the same
  rules: `vfxcut.html` (pick a clip, set range / length / width / edge fade, preview next to the Berserker, download PNG + JSON).
  First: `vfx_bzslam` from the owner's cartoon explosion clip (`art/incoming/fx_video/bz_slam_v1.mp4`, 0.7–7 s → 2 s, 260 wide),
  not used by the game yet. Ready prompts with game sizes: `art/incoming/action/berserker/video_start/VFX_VIDEO_READY.txt`.

### Tree of Savior proportions (2026-11-10)
Owner "ลองสัดส่วนเท่า Tree of Savior ดู กลับไปแมพ 2D": trees were 5.7x the hero, houses ~3x. `PROP_S=tos` in
`tools/art/rebuild_props.py` rebuilds named props from their full-size sheets at height x factor (trees oak/pine/blossom/dead_tree .62 ->
~3.5x the hero, houses .82 -> ~2.5x, big buildings .75, statue/arch .85), props_hr pass first (`PROP_S=tos PROP_K=1.5`), then 1x.
Thai props unchanged. hd3d2 map scale back to 1 (the props themselves are smaller now). Screenshot `art/incoming/action/tos_scale_2d.png`.

### Assassin (rogue class 2) test skin (2026-11-11)
Owner's GPT chibi assassin -> PixelLab `image_to_pixelart` 128 (1 gen) for the still; Meta AI clips (attack, attack2, run, hurt +
death) cut with `tools/video/vid2px.py` on the PixelLab still's palette, feet locked, one cell (`tools/art/assassin_video_build.py`
name=<dir>:<first,last> ...) -> `art/action/assassin/`. Removed from the game 2026-11-11 (owner "เอาแอสซาซินออก"; the raw clips and the build tool stay); it was `action.html?hero=rogue&skin=assassin`
(`ASN`, `drawAssassin`): the two attack clips take turns, run while moving, hurt, death; the rogue's kit is unchanged.
Meta redraws her a little differently in every clip (owner: "ไม่เหมือนต้นฉบับ"); PixelLab moves from the pixel still would keep
her exact look (about 1 gen a move).
