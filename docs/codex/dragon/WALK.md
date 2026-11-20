# Dragon spear warrior: WALK sheets, smooth, many frames (painted 2D)

Owner phrase: "ทำท่าเดินมังกร" (owner 2026-11-20: "ทำพรอม ท่าเดิน ของ codex ให้ครบ" + "เอาเนียนๆ หลายๆ เฟรม").
Branch `codex/dragon-walk`, pictures into `art/incoming/dragon_walk/` (full size PNG, not shrunk), plus `REPORT_TH.txt` (Thai, short: which file is which,
what may be off). Open a pull request, do not merge. When you stop, switch the folder back with `git checkout main`.

## The character (use ONLY this, the same look in every frame)
- `art/incoming/dragon/ref_owner_spear.png` = THE character (the owner's original): a white-maned dragon / fox-like chibi spear warrior, two swept-back red
  horns, red eye, red face markings, black cloak with red and gold flame patterns, black clothes, gold belt, gold spear.
- Style: NORMAL 2D painted chibi cartoon (NOT pixel art, NOT 8 / 16 bit), thick dark outline, big head, small body. NO wings, NO tail.
- If `art/incoming/dragon/2d_base.png` exists (the owner's Meta picture of him standing), match it too.

## Task 0 (only if `art/incoming/dragon/2d_base.png` does not exist): base picture
One big clean picture: standing still, side view facing RIGHT, spear held upright beside him with the butt on the ground, full body,
plain flat white background, no shadow, no text. File: `base_side.png`. Use it as the character for the sheets below.

## Tasks 1-3: walk cycles, 16 frames each (one sheet per direction)
1. `walk_side.png`: side view facing RIGHT, walking to the right.
2. `walk_front.png`: walking TOWARD the viewer (front view, seen a little from above, like a top-down RPG).
3. `walk_back.png`: walking AWAY from the viewer (back view: the mane and the cloak from behind, seen a little from above).
(Left = the game mirrors the side sheet; diagonals are not needed.)

The move in all three: a calm confident WALK (not a run): one full cycle = two steps (left foot, right foot) over the 16 frames, the body bobs
a little up on each passing step and down on each contact, the spear held in the front hand, upright and slightly tilted, swinging only a little
with the step, the cloak and the mane sway behind with a small delay. Frame 16 flows straight back into frame 1 (seamless loop).
Smooth: every frame only a small step from the one before, no jumps, no frame repeated.

## Sheet rules (all three sheets, follow exactly)
- 16 frames in a grid of 4 columns x 4 rows (4 frames in each row), read left to right, top to bottom. Portrait picture 1024 x 1536, each cell 256 x 384.
- Flat solid blue background (#0248BA) everywhere, no gradient, no texture, no borders or lines between cells.
- In every cell a thin dark ground line at the same height near the bottom of the cell; the feet touch it on the contact frames.
- The character is the SAME SIZE in every frame and in all three sheets, standing in the middle of its cell (walking in place: he does not travel across
  the cell), never crossing into another cell. The spear tip stays inside its cell.
- No text, no numbers, no frame labels, no motion lines, no dust, no shadow, no watermark.

## Check before you finish
Put each sheet next to `ref_owner_spear.png`: same face, colours, cloak pattern, spear, size? Feet on the line? The loop: does frame 16 lead into frame 1?
Front and back sheets: really front / back, not side? If a sheet is off, redraw it. Say in `REPORT_TH.txt` what still looks off.
Claude then cuts the frames (blue and ground line off, feet lined up) and puts him in `pixmap.html`.
