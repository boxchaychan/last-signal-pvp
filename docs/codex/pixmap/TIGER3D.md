# Tiger for 3D: T-pose front / back / side pictures (flat 2D drawings, for Tripo AI image-to-3D, multi-view)

Owner 2026-11-20: "ทำ t pose ดิ หน้า หลัง ข้าง": 2D painted drawings in a T-pose, NOT 3D renders.

Owner phrase: "ทำรูปเสือ 3D" (owner 2026-11-20: "เจนใหม่ เอาพร้อมรูป หน้า หลัง มาจะเอาเข้า 3D", after the first Tripo model came out with a tail that was far too long).
Branch `codex/tiger-3d-views`, pictures into `art/incoming/tiger_3d_views/` (full size PNG, not shrunk), plus `REPORT_TH.txt` (Thai, short: which file is which, what may be off). Open a pull request, do not merge.

## The character (use ONLY this, same look in every view)
- `art/incoming/pixmap/tiger3d/gpt_tiger_tail.png` = THE tiger: painted chibi cartoon (NOT pixel art, NOT 8 / 16 bit), big head, small body, thick dark outline.
  Orange fur with black stripes, black hood with tiger ears, big cream-white fur collar, gold shoulder buttons with a red braided cord, black and gold clothes,
  red sash with a gold swirl, brown gauntlets with fur cuffs and big silver claws, black trousers, brown paws.
- Also for the face / colours: `art/incoming/war/gpt_tiger_stand_cut.png`.

## What to draw: 3 separate pictures, the SAME tiger at the SAME size, flat 2D painted drawings (not 3D renders)
1. `tiger_front.png`: T-pose, facing the viewer straight on.
2. `tiger_back.png`: T-pose, seen straight from behind (the hood back, the collar from behind, the tail).
3. `tiger_side.png`: exact side view, facing RIGHT (arms straight out to the sides, so from the side they point toward / away from the viewer).

Rules for all three (this is what a 3D model maker needs):
- Pose: T-POSE: standing straight, feet a little apart, both arms straight out to the sides, level with the shoulders, palms down, claws open, nothing in front of the body.
- TAIL: SHORT, about half the height of the body, curving UP behind the back (S-shape, tip curled). The last model had a long straight tail sticking far out: do NOT do that.
- Flat straight-on view, no perspective, no three-quarter turn, camera at the middle of the body.
- Full body, centred, the same height in every picture (top of the ears to the soles at the same place), plain pure white background, square 1024 x 1024 or larger (wide enough for the arms).
- No shadow, no ground, no text, no numbers, no effects, no border.

## Check before you finish
Put the three next to each other and next to `gpt_tiger_tail.png`: same face, colours, clothes, size? Back view matches the front (collar, sash knot, tail)?
Side view a true profile? Arms level in a T in front / back? Tail short and curled up in all three? If one is off, redraw it. Say in `REPORT_TH.txt` what still looks off.
