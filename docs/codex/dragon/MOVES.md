# Dragon spear warrior: ALL move sheets in one go (painted 2D)

Owner phrase: "ทำท่ามังกรทั้งหมด" (owner 2026-11-20: "สั่งหลายๆ อันนะ ประหยัดเวลา"). Only the walk: "ทำท่าเดินมังกร" = `WALK.md` (= sheets 1-3 below).
Branch `codex/dragon-moves`, pictures into `art/incoming/dragon_moves/` (full size PNG, not shrunk), plus `REPORT_TH.txt` (Thai, short: which file is which,
what may be off). Open a pull request, do not merge. Do the sheets in the order below and commit after each one, so a stop keeps what is done.
When you stop, switch the folder back with `git checkout main`.

## The character (use ONLY this, the same look in every frame of every sheet)
- `art/incoming/dragon/ref_owner_spear.png` = THE character (the owner's original): a white-maned dragon / fox-like chibi spear warrior, two swept-back red
  horns, red eye, red face markings, black cloak with red and gold flame patterns, black clothes, gold belt, gold spear.
- Style: NORMAL 2D painted chibi cartoon (NOT pixel art, NOT 8 / 16 bit), thick dark outline, big head, small body. NO wings, NO tail.
- If `art/incoming/dragon/2d_base.png` exists (the owner's Meta picture of him standing), match it too. If it does not, make sheet 0 first and use it.

## Sheet rules (every sheet, follow exactly)
- 16 frames in a grid of 4 columns x 4 rows (4 frames in each row), read left to right, top to bottom. Portrait picture 1024 x 1536, each cell 256 x 384.
- Flat solid blue background (#0248BA) everywhere, no gradient, no texture, no borders or lines between cells.
- In every cell a thin dark ground line at the same height near the bottom of the cell; the feet stand on it (when he jumps the line stays and he is drawn higher).
- The character is the SAME SIZE in every frame and in every sheet, in the middle of his cell (moves in place: he does not travel across the cell),
  never crossing into another cell; the spear and the effects stay inside the cell.
- Smooth: every frame only a small step from the one before, no jumps, no repeated frames. Loops: the last frame flows straight into the first.
- Effects (flash at the spear tip, red arc trail, flames) only where the move says, bright and clear, inside the cell. No motion lines, dust or shadow otherwise.
- No text, no numbers, no frame labels, no watermark.

## The sheets (side view facing RIGHT unless the line says otherwise; left = the game mirrors)
0. `base_side.png` (only if 2d_base.png is missing): one big picture, standing still, facing right, spear upright beside him, white background.
1. `walk_side.png`: WALK loop to the right: calm confident walk, two steps over the 16 frames, small up / down bob, spear in the front hand upright and
   slightly tilted, cloak and mane sway behind a little late.
2. `walk_front.png`: the same walk TOWARD the viewer (front view, seen a little from above, like a top-down RPG).
3. `walk_back.png`: the same walk AWAY from the viewer (back view, seen a little from above).
4. `idle.png`: IDLE loop: standing ready, spear upright, slow breathing, cloak and mane sway gently, a small grip adjust.
5. `run.png`: RUN loop: running fast, leaning forward, spear held low and level in both hands, cloak and mane flowing behind, two strides.
6. `attack1.png`: SPEAR COMBO HIT 1 of 3: from the ready stance pull the spear back, a fast straight thrust forward, a bright white-red flash at the tip
   on the hit frame, hold a moment, end ready for the next hit.
7. `attack2.png`: HIT 2 of 3: continue from the end of hit 1: a wide horizontal sweep of the spear from back to front with a red arc trail, end ready for the finisher.
8. `attack3.png`: HIT 3 of 3 (finisher): continue from the end of hit 2: jump up, spin the spear once, slam it down into the ground in front with a burst of
   red and gold flame, land, back to the ready stance.
9. `skill_dash.png`: SKILL "flame dash": crouch and charge with red flames around the spear, burst forward low with a flame trail, a strong thrust at the end,
   slide to a stop, back to the ready stance (he stays inside his cell: show the dash with the pose and the trail, not by moving across).
10. `hurt.png`: HURT: hit from the front, flinch back, stagger one step, mane and cloak jolt, recover to the ready stance.
11. `death.png`: DEATH: hit hard, stagger back, drop the spear, fall to the knees, fall on the side, lie still in the last 4 frames.

## Check before you finish
Each sheet next to `ref_owner_spear.png`: same face, colours, cloak pattern, spear, size? Feet on the line? Loops close? Hits 1-2-3 continue from each other?
Front / back walks really front / back? If a sheet is off, redraw it. Say in `REPORT_TH.txt` what still looks off.
Claude then cuts the frames (blue and ground line off, feet lined up) and puts him in `pixmap.html`.
