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
run dust, roll after-images that copy the roll frame.

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
