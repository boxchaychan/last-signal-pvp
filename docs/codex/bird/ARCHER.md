# Eagle archer: second job of the desert side-scroller

Owner phrase: "นกนักธนูธีมเดียวกับมังกร ขนาดเท่ากัน เจนรอเลย". The eagle comes from the same set of animal warriors as the dragon. Moves are drawn FRAMES (no bones) and must be as smooth and alive as `art/incoming/dragon_moves/attack2.png`.
Branch `codex/bird-archer`, pictures in `art/incoming/bird_archer/`, plus `REPORT_TH.txt` (Thai, short). Commit and push after EVERY picture. Do not merge. Do not edit html, tools or CLAUDE.md.

## Lock the character
Design = `art/incoming/eaglearcher/eagle_src.png` (also `art/incoming/eaglearcher/gpt_turnaround.png`, and row 2 column 1 of `art/incoming/champions/owner_12animals_sheet.png`): white feathered eagle head, yellow beak, blue and gold crest feathers, blue and gold feather cape, brown belt and trousers, long curved blue and gold bow. Keep that design and its colours.
Style and body = `art/incoming/dragon_moves/base_side.png` and `art/incoming/dragon_moves/idle.png`: the same painted 2D style, thick dark outline, smooth cel shading, the same chibi proportions, head size, arm and leg size, and the same height from feet to top of head as the dragon. NOT pixel art.

## 1. `base_side.png` (do this first)
One standing eagle, full body, side view facing RIGHT, bow held upright in the front hand, clean white background, same picture size and same figure height as `art/incoming/dragon_moves/base_side.png`. Put it beside the dragon and redo it if the body is bigger, smaller, taller or thinner. Attach this picture for every sheet below.

## 2. Move sheets
Each `<name>.png`: landscape 1536 x 1024, exactly 16 frames, 4 columns x 4 rows, read left to right, top to bottom; cells 384 x 256.
- Flat blue #0248BA background, no borders, one thin dark ground line at the same height near the bottom of every cell.
- Side view facing RIGHT. EXACTLY the same character size in all frames and all sheets, about 190 px tall without the bow, like the dragon sheets.
- Keep every frame in the middle of its cell. Head, crest, cape, bow and arrow stay fully inside their own cell with at least 24 px of empty blue on every side and never cross into another cell.
- Feet stay on the ground line unless the move leaves the ground.
- Really redraw every frame with small steps: legs, hips, cape and crest feathers follow the weight of the move. The bow stays the same size and shape and stays in the same hand.
- Only the arrow in the bow. No trails, glow, dust, shadows, text or numbers: the game adds the effects.
- Except idle and run, frame 1 and frame 16 are the normal standing pose, so moves chain smoothly.

3. `idle`: calm breathing loop, cape and crest sway, frame 16 flows into frame 1.
4. `run`: fast light run loop, bow held low, cape flying, frame 16 flows into frame 1.
5. `attack1`: quick shot: draw, release, small recoil.
6. `attack2`: step forward and a second quick shot from a lower stance.
7. `attack3`: strong shot: lean back, full draw, big release, cape snaps back.
8. `skill_dash`: low fast dash forward with the cape streaming, recovers to standing.
9. `hurt`: hit from the front, flinches back, recovers.
10. `death`: staggers, drops to the knees, falls on the ground and stays down (no return to standing).

Open each sheet beside `base_side.png` and the dragon's `idle.png`. Redo it if the character changes, the bow changes hand or shape, the size differs, a frame is cut off or touches another cell, or the motion jumps. Say in `REPORT_TH.txt` what still looks off.
