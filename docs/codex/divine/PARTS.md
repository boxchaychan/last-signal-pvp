# ศึกผู้รับพร: Zeus in separate PARTS (test for the cut-out rig)

Goal: the game moves a god by turning his parts on joints (like keyframed 2D parts in Unity). Our current parts are cut out of one finished
picture, so the hidden areas (body behind the arm, the shoulder, the neck) are guessed. Please draw Zeus again as SEPARATE parts with the
hidden areas drawn complete.

Style and size: exactly the approved Zeus `art/divine/zeus/idle_key.png` (same face, laurel, tunic, gold trim, lightning bolt, same thick
dark-brown outline and colours, same body size). Same idle pose, 3/4 front view.

## Output (branch `codex/divine-zeus-parts`, folder `art/divine/zeus_parts/`)
Every part is a transparent PNG, 512 x 512, placed EXACTLY where it sits in the idle pose (so stacking all files in the order below rebuilds the
idle picture with the feet on y 500 and the body centred on x 256). Draw every part COMPLETE, including the areas another part normally hides,
and give each part its own outline.
1. `leg_back.png`: the leg further from the viewer, thigh to sandal
2. `arm_free_upper.png` + `arm_free_lower.png`: the empty arm (upper arm with the shoulder ball; forearm with the fist and gold bracer)
3. `torso.png`: chest, tunic, belt and skirt, with the neck stub and both shoulder sockets drawn (nothing missing under the arms or head)
4. `leg_front.png`: the leg nearer the viewer
5. `head.png`: head, hair and laurel, with the bottom of the neck drawn under the chin
6. `arm_weapon_upper.png` + `arm_weapon_lower.png`: the arm that holds the bolt (upper arm with shoulder ball; forearm with hand and bracer)
7. `bolt.png`: the lightning bolt alone (the hand's fingers stay on `arm_weapon_lower.png`, drawn closed round an empty grip)
8. `joints.json`: pixel position (x, y in the 512 frame) of each joint: neck, shoulder_weapon, elbow_weapon, grip, shoulder_free, elbow_free, hip_back, hip_front
9. `check_stacked.png`: all parts stacked in the order above (must look like the idle picture), and `check_spread.png`: the parts laid out apart on a grey background

Keep raw pictures in `art/incoming/divine_game/raw/zeus_parts/` and add `art/incoming/divine_game/reports/zeus_parts.md`.
Open a PR, do not merge it, and do not change `divine.html` (Claude wires it in).
