# Otter chi fist: new class of the desert side-scroller

Owner phrases: "เอานากมาทำ", "เอาแบบนี้เลย" (keep the otter's own body from the picture, do not make it a big-head chibi), "ออกแบบให้อยู่ในคลาส หมัดปราณ".
Class: **chi fist (หมัดปราณ)**. A bare-handed martial artist who fights mainly at point-blank range, middle range second, with fast attacks, and is always on the move: footwork makes up for the short reach. Water chi is its power. It never holds a staff, sword, spear or any other weapon.

Moves are drawn FRAMES (no bones) and must be as smooth and alive as `art/incoming/dragon_moves/attack2.png`.
Branch `codex/otter-fist`, pictures in `art/incoming/otter_fist/`, plus `REPORT_TH.txt` (Thai, short). Commit and push after EVERY picture. Do not merge. Do not edit html, tools or CLAUDE.md.

## Lock the character
Body and design = `art/incoming/otter_fist/side_ref.png` (from the owner's `art/incoming/otter_mage/otter_src.png`): same head, face, ears, same head size compared with the body, same slim torso, same arm and leg length, dark blue scarf with pale wave marks, sleeveless dark robe, teal knotted belt, white and blue wave panel, baggy dark trousers, wrapped shins, sandals, long brown tail. Keep all of it. Same painted 2D style, thick dark outline, smooth cel shading. NOT pixel art.

Two changes for the class only:
- No water orb in the hands. The game draws the water chi on the fists and the water orbs that circle the body (the class resource), so never draw orbs in the frames.
- The dark hand wraps cover the knuckles like a fighter's, with one small pale-cyan wave mark on the back of each fist.

## Hands: check them in EVERY picture (owner: "มือกลับด้าน")
Facing RIGHT, the arm nearest the viewer is the character's RIGHT arm and the far arm is the LEFT arm. Never mirror a hand.
- Far (left) fist in guard: the viewer sees the PALM side: four curled fingers and the thumb folded across them. The wave mark is on the back of the hand, so it is NOT visible.
- Near (right) fist in guard or at the waist: the viewer sees the BACK of the hand with the wave mark. The thumb is hidden on the far side.
- In a straight punch the palm faces down: the near fist shows its little-finger side, the far fist shows its thumb side.

## 1. `base_side.png` (do this first)
One otter, full body, side view facing RIGHT, clean white background, picture size 1118 x 1407, same body size as `side_ref.png`, soles on the same line (y about 1290). Pose: a ready martial arts guard. Feet apart, knees slightly bent, weight low, front fist raised forward at chin height, rear fist pulled back at the waist. Scarf and tail trail to the left. Fully inside the picture.
Put it beside `side_ref.png`. Redo it if the head, body, arms or legs change size or shape.

## Feel: flowing like water (owner: "สกิลเน้นพลิ้วๆ")
Every move is one unbroken flow, like a dancer or tai chi at high speed. No stiff stops and no held poses, except one short beat on the last hit of `attack3`. Arms travel in curves and spirals before they land. Hips turn in soft circles, feet glide and pivot on the balls of the feet. The end of each motion is already the start of the next. Scarf and tail lag two or three frames behind the body and draw long S-curves.

## 2. Move sheets
Each `<name>.png`: landscape 1536 x 1024, exactly 16 frames, 4 columns x 4 rows, read left to right, top to bottom; cells 384 x 256.
- Flat blue #0248BA background, no borders, one thin dark ground line at the same height near the bottom of every cell.
- Side view facing RIGHT. EXACTLY the same character size in all frames and all sheets, about 190 px from soles to top of the ears.
- Keep every frame in the middle of its cell. Ears, scarf, tail and fists stay fully inside their own cell with at least 24 px of empty blue on every side and never cross into another cell.
- Feet stay on the ground line unless the move leaves the ground.
- Really redraw every frame with small steps. Punches start from the hips: feet, hips, shoulders, then the fist. Scarf and tail follow the weight.
- Hands are fists unless a move says otherwise. No water, trails, glow, dust, shadows, text or numbers: the game adds the effects.
- Except idle and run, frame 1 and frame 16 are the guard pose of `base_side.png`, so moves chain smoothly.

3. `idle`: light bouncing guard, small weight shifts, scarf and tail sway, frame 16 flows into frame 1.
4. `run`: fast low run, fists near the chest, arms pumping, scarf and tail flying, frame 16 flows into frame 1.
5. `attack1`: quick whipping punch with the front fist: the arm uncoils in a small curve, lands, and flows back in a circle.
6. `attack2`: gliding step with a full hip turn, the rear fist spirals out from the waist into a punch, the body keeps turning through it.
7. `attack3`: finisher: both arms draw one big circle while the body sinks low, the circle closes at the hip, then the whole body uncoils into a spiralling punch, one short beat on impact, and melts back to guard.
8. `skill_dash`: very low gliding slip forward in a soft S-curve, body leaning and turning, scarf streaming, flows back to guard.
9. `skill_flurry`: six fast alternating straight punches, left, right, left, right, left, right, with small quick gliding steps so the feet never stop and the hips sway in a figure eight, each punch rolling out of the last, then back to guard. Each punch is clearly a different frame group. The figure stays in the middle of its cell: the game moves it.
10. `skill_upper`: sink and turn, then a spiralling rising uppercut that carries the whole body up in a corkscrew, floats at the top, lands softly on the ground line in guard.
11. `skill_drop`: rise in a smooth arc, the body rolls over in the air gathering the fist, pours down and lands the fist on the ground line, then rolls straight up into guard. The figure stays in the middle of its cell: the game moves it.
12. `skill_spin`: fast spinning backfists and spin kicks, body turning full circles on the balls of the feet, arms and one leg swinging wide, scarf and tail whipping round. Frames 4 to 13 loop smoothly.
13. `hurt`: hit from the front, flinches back, guard drops, recovers.
14. `death`: staggers, drops to the knees, falls on the ground and stays down (no return to standing).

Open each sheet beside `base_side.png` and the dragon's `art/incoming/dragon_moves/idle.png`. Redo it if the character changes, a weapon or orb appears, the size differs, a frame is cut off or touches another cell, or the motion jumps. Say in `REPORT_TH.txt` what still looks off.
