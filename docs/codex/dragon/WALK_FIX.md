# Dragon walk, second try: LOW steps (painted 2D)

Owner phrase: "แก้ท่าเดินมังกร" (owner 2026-11-20 after seeing the first walk in the game: "เดินมันยกขาสูงจัง" = he lifts his legs too high).
Branch `codex/dragon-walk2`, pictures into `art/incoming/dragon_walk2/` (full size PNG), plus `REPORT_TH.txt` (Thai, short). Commit after each sheet.
Open a pull request if you can, do not merge. When you stop, switch the folder back with `git checkout main`.

## The character
`art/incoming/dragon_moves/base_side.png` (THE look) and the first walk sheets `art/incoming/dragon_moves/walk_side.png`, `walk_front.png`, `walk_back.png`
(same size, same cell layout: match them). Painted 2D chibi, NOT pixel art, NO wings, NO tail.

## What was wrong
In the first sheets frames 6 and 14 pull the knee up high like marching. The new walk must look like a calm, smooth walk of a short chibi:
- the feet stay CLOSE TO THE GROUND: the lifted foot only clears the ground a little (at most a quarter of the leg length), never a high knee;
- short steps, the legs swing forward and back under the body, the body bobs only slightly;
- the spear stays upright in the front hand, the cloak and the mane sway gently a little behind the motion.

## Sheets (the same rules as `docs/codex/dragon/MOVES.md`)
16 frames, 4 columns x 4 rows, portrait 1024 x 1536, cells 256 x 384, flat blue #0248BA, a thin dark ground line in every cell, the same size in every frame,
walking in place in the middle of the cell, frame 16 flows into frame 1. No text, no numbers, no effects, no shadow.
1. `walk_side.png`: side view facing RIGHT.
2. `walk_front.png`: walking toward the viewer, seen a little from above.
3. `walk_back.png`: walking away from the viewer, seen a little from above.

## Check before you finish
Put each new sheet next to the old one: same character and size, and NO frame where a knee comes up high. Say in `REPORT_TH.txt` what is off.
