# Moon blade swordsman (นักดาบจันทรา): third job of the desert side-scroller

Owner phrases (2026-11-25): "ใช้เลย" (class = moon blade), "สั่ง codex เลย", "เอาเนียนๆ", "ท่าเดินท่าอะไรสั่งพร้อมไปเลยยาวๆ", "แมพสวย เอาแบบคมกริบทั้งตัวละครและสกิล".
Branch `codex/moon-blade` made from the newest `origin/main` (run `git fetch` first), pictures in `art/incoming/moon_blade/`, plus `REPORT_TH.txt` (Thai, short). Commit and push after EVERY picture. Open a PR, do not merge. Do not edit html, tools or CLAUDE.md.
Moves are drawn FRAMES (no bones). They must be as smooth and alive as `art/incoming/dragon_moves/attack2.png`: many small in-between steps, no jumps between frames, cloth and hair follow the weight of the move.

## Lock the character
Design = `art/incoming/human_sword/moon_knight_v1.webp` (the owner's picture): chibi human boy, fluffy white hair with violet tips, crescent moon hairpin, violet eyes, black-violet plate armour with big silver crescent moons on the shoulders, cape, gloves, armoured boots, long violet crystal sword with a crescent guard. Keep that design and its colours.
Style for a SMALL game body (he is only 60-90 px tall on screen next to a big map): thick clean dark outline, flat cel shading with one shadow tone, high contrast, crisp edges, no blur, no watercolour texture. Drop tiny details (lace, small moon prints) and keep the big shapes: hair, hairpin, shoulder crescents, cape, sword. NOT pixel art, NOT 3D.
Body size = the same height feet to top of head as the dragon in `art/incoming/dragon_moves/base_side.png` / `idle.png`.

## 1. `base_side.png` (do this first)
One standing figure, full body, side view facing RIGHT, guard stance, sword in the front hand pointing forward and down, cape a little behind, clean white background, same picture size and figure height as `art/incoming/dragon_moves/base_side.png`. Put it beside the dragon and the owner's picture and redo it if the face, hair, armour or sword drift, or the size is off. ZOOM ON THE HANDS: the sword hand must be the front hand in every picture. Attach this picture for every sheet below.

## 2. Move sheets
Each `<name>.png`: landscape 1536 x 1024, exactly 16 frames, 4 columns x 4 rows, read left to right, top to bottom; cells 384 x 256.
- Flat blue #0248BA background, no borders, one thin dark ground line at the same height near the bottom of every cell.
- Side view facing RIGHT. EXACTLY the same character size in all frames and all sheets, about 190 px tall without the sword, like the dragon sheets.
- Keep every frame in the middle of its cell. Hair, cape and sword stay fully inside their own cell with at least 24 px of empty blue on every side and never cross into another cell.
- Feet stay on the ground line unless the move leaves the ground.
- Really redraw every frame with small steps (smooth, "เนียน"): legs, hips, cape and hair follow the move; the sword keeps its size and shape and stays in the same hand.
- Only the character and the sword. No trails, glow, slash arcs, dust, shadows, text or numbers: the game adds the effects.
- Except idle and run, frame 1 and frame 16 are the normal guard pose, so moves chain smoothly.

3. `idle`: calm breathing in the guard stance, hair and cape sway, frame 16 flows into frame 1.
4. `run`: fast light run, sword held low behind, cape and hair flying, frame 16 flows into frame 1.
5. `attack1`: quick forward slash (high to low).
6. `attack2`: step and a rising backhand slash (low to high).
7. `attack3`: strong finisher: spin once and a wide horizontal slash, cape snaps round.
8. `skill_dash`: low fast dash forward with the sword held back, recovers to the guard pose.
9. `skill_leap`: jump up, flip the sword down and slash down onto the ground, land in a crouch, recover.
10. `skill_cast`: raise the sword up to the sky with both hands (calling the moon), hold, bring it down in one big vertical cut.
11. `walk`: calm walk with the sword held low, frame 16 flows into frame 1.
12. `jump`: crouch, take off, rise, top of the jump, fall, land, recover (frames 1-16 in that order; the game picks rise / fall frames).
13. `climb`: climbing a ladder seen from the side, sword on the back, hands and feet alternate, frame 16 flows into frame 1.
14. `skill_spin`: spin slashes round the body for the whole sheet (about two full turns), recovers to guard on frame 16.
15. `hurt`: hit from the front, flinches back, recovers.
16. `death`: staggers, drops to the knees, falls and stays down (no return to standing).

Open each sheet beside `base_side.png` and the dragon's `idle.png`. Redo it if the character changes, the sword changes hand or shape, the size differs, a frame is cut off or touches another cell, or the motion jumps. Say in `REPORT_TH.txt` what still looks off.
