# Dragon spear warrior: 3 new skill moves + their effects

Owner phrase: "ทำสกิลมังกรเพิ่ม". The dragon is the SPEAR job and gets 7 skills. Four moves already exist; draw the 3 missing ones. Moves are drawn FRAMES (no bones), and must look as smooth and alive as `art/incoming/dragon_moves/attack2.png`.
Branch `codex/dragon-skills7`, pictures in `art/incoming/dragon_skills7/`, plus `REPORT_TH.txt` (Thai, short). Commit and push after EVERY picture. Do not merge. Do not edit html, tools or CLAUDE.md.

## Lock the character
Attach and match `art/incoming/dragon_moves/base_side.png` and `art/incoming/dragon_moves/idle.png`: same face, white and red mane, black and gold robe, red flame cape, flame on the back, gold boots with white toes, same long gold spear. No wings. Same painted 2D style, thick dark outline, smooth cel shading. NOT pixel art.

## Body sheets
Each `<name>.png`: landscape 1536 x 1024, exactly 16 frames, 4 columns x 4 rows, read left to right, top to bottom; cells 384 x 256.
- Flat blue #0248BA background, no borders, one thin dark ground line at the same height near the bottom of every cell.
- Side view facing RIGHT. EXACTLY the same character size in all frames and all sheets, about 190 px tall without the spear. Frame 1 and frame 16 are his normal standing pose with the spear upright, so the moves chain smoothly.
- Feet stay on the ground line unless the move leaves the ground. The whole body and whole spear stay inside the cell and never touch another cell.
- Really redraw every frame with small steps: legs, hips, cape, mane and tail flame follow the weight of the move.
- Only small flames touching the spear. No big effects, trails, dust, shadows, text or numbers: the game adds the effects.

1. `skill_sweep`: DRAGON TAIL SWEEP. He drops low, plants his front foot, swings the spear in one huge low horizontal circle around his body with his cape flying, ends low, rises.
2. `skill_rise`: RISING DRAGON. Deep crouch, spear low behind him, then an explosive upward spear strike that lifts him off the ground, spear pointing to the sky at the top, lands softly.
3. `skill_rain`: SPEAR RAIN. He leans back and hurls a burst of fire upward with a big overhead spear motion, holds the spear high while calling it down, then snaps it forward and returns to stance. He keeps the spear in his hand.

## Effect sheets
Each 1024 x 1024, strict 4 x 4 grid, 16 frames, PURE BLACK #000000 background, no character, bright painted anime-style fire in red, orange, gold and white, each frame fully inside its cell, starting small and fading out at the end.

4. `fx_sweep`: a wide flat crescent ring of fire whipping around at ground level, shaped like a dragon's tail.
5. `fx_rise`: a fire dragon spiralling straight UP from the bottom of the cell, with rising embers.
6. `fx_spear`: one blazing spear of light falling straight DOWN, striking the ground at the bottom of the cell and bursting into flame.

Open each sheet beside `base_side.png`. Redo it if the character changes, the spear changes hand or shape, a frame is cut off, or the motion jumps. Say in `REPORT_TH.txt` what still looks off.
