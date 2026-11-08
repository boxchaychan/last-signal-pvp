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

Balance after: 4.25 of 40 (trial key, 2026-11-08). The owner has another key too.
Download the ZIP only between jobs (`/mcp/characters/<id>/download` answers "still being generated" while a job runs).

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
