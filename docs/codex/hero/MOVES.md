# Eclipse Knight: every move as hand-drawn frames

Owner phrase: "ทำท่าอัศวินทั้งหมด". Owner decision: the main hero uses drawn FRAMES, not bones. It must look as smooth and alive as `art/incoming/dragon_moves/attack1.png`.
Branch `codex/hero-frames`, pictures in `art/incoming/hero_frames/`, plus `REPORT_TH.txt` (Thai, short). Commit and push after EVERY picture. Do not merge. Do not edit html, tools or CLAUDE.md.

## Lock the character
Look at `art/incoming/hero_eclipse/hero_base.png` (design), `hero_blade.png` (weapon) and `title_art.png` (how he holds it). Same face, amber eyes, spiky silver-white hair with ember-orange tips, gold crescent circlet, red neck scarf, black and gold armour with molten-orange seams, black-sun chest emblem. Same painted 2D style, thick dark outline, smooth cel shading. NOT pixel art. He holds the crescent greatsword in his hand in every frame.

## 0. `base_side.png` first (1024 x 1024)
Him in a ready stance, true SIDE view facing RIGHT, greatsword held low and forward, plain flat blue #0248BA background. Use this picture as the reference for every sheet below.

## Sheet rules (every move)
- `<move>.png`, landscape 1536 x 1024, exactly 16 frames: 4 columns x 4 rows, read left to right, top to bottom. Cells are 384 x 256.
- Perfectly flat blue #0248BA background; no borders between cells; one thin dark ground line at the same height near the bottom of every cell.
- Side view facing RIGHT. Same character size in every frame and every sheet (about 190 px tall). Feet on the ground line unless the move leaves the ground. The whole body and the whole sword stay inside the cell and never touch another cell.
- Really redraw each frame: limbs, hair, scarf and body weight change smoothly with small steps between frames. No sliding copies of one pose.
- Only small flames touching the blade are allowed. No big effects, smears, trails, dust, shadows, text or numbers: the game adds the big effects.

## The moves, in this order
1. `idle`: relaxed ready stance, breathing, hair and blade sway; frame 16 flows into frame 1.
2. `run`: fast run in place, low strong strides, sword held low; a perfect loop.
3. `jump`: frames 1-3 crouch, 4-7 rising, 8-9 top, 10-13 falling, 14-16 land and recover.
4. `climb`: seen from the side climbing a ladder, sword on his back, hands and feet alternate; a perfect loop.
5. `attack1`: fast horizontal slash forward: wind-up, strike, follow-through, recover.
6. `attack2`: reverse rising slash from low to high.
7. `attack3`: heavy jumping overhead chop into the ground, recover.
8. `skill_sun`: deep wind-up, then a huge full-body crescent slash forward, hold, recover.
9. `skill_meteor`: crouch, leap high, flip with the sword overhead, plunge down and stab the ground, rise.
10. `skill_ring`: whirl the sword around his body in full spins; frames 4-13 loop.
11. `skill_eclipse`: raise the sword to the sky, power up with hair and scarf lifting, hold, then slam it forward in a final heroic pose.
12. `dash`: explosive low forward dash, body almost horizontal, recover.
13. `hurt`: hit from the front, flinch back, recover.
14. `death`: hit hard, stagger, fall, lie still in the last 3 frames with the sword beside him.

Open each sheet beside `base_side.png`. Redo it if the face or armour changes, the sword changes hand or shape, a frame is cut off, or the motion jumps. Say in `REPORT_TH.txt` what still looks off.
