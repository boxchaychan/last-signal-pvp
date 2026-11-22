# Otter water mage: new job of the desert side-scroller

Owner phrase: "เอานากมาทำ ตัวละครมันสูง ปรับให้เท่ามังกร" and "ต้องดูด้วยว่ามันคืออาชีพอะไร จะได้เจนท่าทางถูก".
Job, read from the owner's picture: **water mage (จอมเวทสายน้ำ)**. A swirling water orb floats over the open front hand, no weapon, wrapped fists, robe and scarf with wave patterns. It fights at middle range by casting from the hands. It never holds a staff, sword or spear.

Moves are drawn FRAMES (no bones) and must be as smooth and alive as `art/incoming/dragon_moves/attack2.png`.
Branch `codex/otter-mage`, pictures in `art/incoming/otter_mage/`, plus `REPORT_TH.txt` (Thai, short). Commit and push after EVERY picture. Do not merge. Do not edit html, tools or CLAUDE.md.

## Lock the character
Design = `art/incoming/otter_mage/otter_src.png`: brown otter head with round ears and a cream face, angry eyes, dark blue scarf with pale cloud-wave marks, sleeveless dark robe, teal knotted belt, white and blue wave panel on the robe, baggy dark trousers, wrapped shins, sandals, dark wrapped forearms, long brown otter tail, swirling blue water orb. Keep that design and its colours.

Style and body = `art/incoming/dragon_moves/base_side.png` and `art/incoming/dragon_moves/idle.png`: the same painted 2D style, thick dark outline, smooth cel shading. NOT pixel art.

**Keep the otter's body exactly as in the owner's picture (owner: "ไม่นะ เอาแบบนี้เลย"):** same head size compared with the body, same slim torso, same arm and leg length, same outfit. Do NOT turn it into the dragon's big-head chibi body. Only the overall size changes: the whole character is scaled to stand as tall as the dragon.

## 1. `base_side.png` (do this first)
One standing otter, full body, side view facing RIGHT, clean white background, picture size 1221 x 1289 like the dragon's `base_side.png`, soles on the same line as the dragon's (y about 1166). Height from soles to the top of the ears = about 820 px, which is the dragon's height without its horns. Front hand held forward at chest height, palm up, with the water orb floating just above it (orb about as wide as the otter's face is tall). Back hand is a relaxed fist. Tail and scarf trail to the left.
Put it beside the owner's otter and the dragon. Redo it if its proportions differ from the owner's otter or its height differs from the dragon's. Attach this picture for every sheet below.

## 2. Move sheets
Each `<name>.png`: landscape 1536 x 1024, exactly 16 frames, 4 columns x 4 rows, read left to right, top to bottom; cells 384 x 256.
- Flat blue #0248BA background, no borders, one thin dark ground line at the same height near the bottom of every cell. Because the background is blue, keep the orb clearly lighter (white-cyan core, dark outline) so it can be cut out.
- Side view facing RIGHT. EXACTLY the same character size in all frames and all sheets, about 190 px tall, like the dragon sheets.
- Keep every frame in the middle of its cell. Ears, scarf, tail, hands and orb stay fully inside their own cell with at least 24 px of empty blue on every side and never cross into another cell.
- Feet stay on the ground line unless the move leaves the ground.
- Really redraw every frame with small steps: legs, hips, scarf and tail follow the weight of the move.
- The orb keeps the same size and stays over the same front hand, except where a move says otherwise. No water blasts, trails, splashes, glow, dust, shadows, text or numbers: the game adds the effects.
- Except idle and run, frame 1 and frame 16 are the normal standing pose, so moves chain smoothly.

3. `idle`: calm breathing loop, orb bobs gently over the palm, scarf and tail sway, frame 16 flows into frame 1.
4. `run`: fast light run loop, orb hand held forward and low, other arm pumping, scarf and tail flying, frame 16 flows into frame 1.
5. `attack1`: quick one-hand cast: pull the orb hand back to the shoulder, then thrust the open palm straight forward, small recoil.
6. `attack2`: step forward and sweep the other hand across the body in a flat arc, palm leading, orb hand pulled in to the chest.
7. `attack3`: strong two-hand cast: lean back, both hands gather the orb at the chest, then step in and push both open palms forward, scarf snaps back.
8. `skill_dash`: low fast glide forward on both feet as if sliding on water, body leaning in, orb hand back, recovers to standing.
9. `hurt`: hit from the front, flinches back, orb hand drops, recovers.
10. `death`: staggers, the orb fades smaller and is gone by frame 8, drops to the knees, falls on the ground and stays down (no return to standing).

Open each sheet beside `base_side.png` and the dragon's `idle.png`. Redo it if the character changes, a weapon appears, the orb changes hand or size, the size differs, a frame is cut off or touches another cell, or the motion jumps. Say in `REPORT_TH.txt` what still looks off.
