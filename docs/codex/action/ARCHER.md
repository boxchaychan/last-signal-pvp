# ARCHER: move sheets for "Sky Huntress" (side game, painted 2D)

Owner 2026-11-15: "แก้ทำละเจนท่าที่ต้องใช้ ... ให้มันละเอียด". The archer is the first hero of the NEW cast for the side game
(`hoodfall.html`). Art is PAINTED 2D, NOT pixel art.

- Character: `art/incoming/archer/REF_sky_huntress.png` (3 views; version 1, the squat one Claude recommended), side view alone:
  `art/incoming/archer/REF_sky_huntress_side.png`. Keep her design exactly: tanned girl, dark-brown double braids with blue beads,
  red eyes, red face marks, white wolf-skull hood with bronze horns and gold ornaments, ivory and gold armour, blue scarf, spotted
  fur skirt, white-gold winged boots, ivory-gold wing bow with a light-blue string, quiver on the back. About 2.3 heads tall.
- Branch `codex/archer-moves`, pictures into `art/incoming/archer/` as `<file>` below (full-size PNG), plus `REPORT_TH.txt`.
- ONE SHEET PER MOVE (attacks: one sheet per hit). Do the next 2 `todo` rows each time, then stop and open the PR.
- Owner phrase: "ทำท่านักธนู" = the next 2 `todo` rows.

## Sheet format (the same for every row)
Paste this, with the character picture attached, and put the row's move text in place of [MOVE] and its frame count / grid:

```
Make an animation sprite sheet of THIS exact character (same face, hair, hood, outfit, colours, proportions and painted 2D style as the attached picture). NOT pixel art: smooth painted 2D with clean lines, the same quality as the picture.
Move: [MOVE]
Layout, follow exactly:
- [FRAMES] frames in a grid of [COLS] columns x [ROWS] rows, read left to right, top to bottom. Image 1536 x 1024, all cells the same size.
- Flat solid green background (#00B140) everywhere, no gradient, no texture, no borders or lines between cells.
- In every cell a thin dark ground line at the same height near the bottom of the cell; her feet stand on it (when jumping, the line stays and she is drawn higher).
- She is the same size in every frame, TRUE SIDE VIEW FACING RIGHT, and stays in the middle of her cell.
- Smooth, detailed animation: many small in-between steps, no big jumps between frames; braids, scarf and fur skirt follow the motion.
- The bow is held in her LEFT hand (front hand toward the right), arrows drawn from the quiver on her back with the right hand.
- Effects (arrow trails, glowing string, sparks, wind, dust) bright and clear, mostly in FRONT of her, inside her own cell.
- No text, no numbers, no frame labels, no watermark.
```

## Rows
| # | file | frames / grid | move ([MOVE]) | status |
|---|------|---------------|---------------|--------|
| 1 | `run.png` | 12 / 4 x 3 | Run cycle: light, fast run, bow held low in the left hand, braids and scarf bouncing; seamless loop (frame 12 flows into frame 1). | todo |
| 2 | `idle.png` | 12 / 4 x 3 | Idle: stand ready, slow breathing, braids and scarf swaying a little, a small bow adjust, seamless loop. | todo |
| 3 | `shot1.png` | 12 / 4 x 3 | Hit 1 of a 3-hit combo: quick shot. From the ready stance, raise the bow, draw an arrow fast, release a glowing light-blue arrow to the right (the arrow leaves the cell), small recoil, end ready to flow into hit 2. | todo |
| 4 | `shot2.png` | 12 / 4 x 3 | Hit 2 of a 3-hit combo: double shot. First frame continues from the last frame of `shot1.png` (attach it); spin half a turn on the spot and fire two arrows in a row to the right; end ready to flow into hit 3. | todo |
| 5 | `shot3.png` | 12 / 4 x 3 | Hit 3, the finisher: first frame continues from `shot2.png` (attach it); jump back a little, draw the bow fully with a strong light-blue glow, fire one big piercing arrow with a spiral wind trail, land and return to the ready stance. | todo |
| 6 | `skill_rain.png` | 12 / 4 x 3 | Skill 1 pose "arrow rain" (strong, dynamic): 1-3 sink low into a deep crouch, back knee almost on the ground, pull an arrow from the quiver; 4-6 lean far back and aim straight up at the sky, bow drawn to full with the string bending, braids and scarf blown back; 7 explosive release, the whole body snaps up, small light-blue flash at the bow; 8-10 hold the follow-through pose looking up, bow arm still raised, scarf fluttering down; 11-12 spin the bow once and land back in the ready stance. (Small effects only: the big effect comes from Meta.) | todo |
| 7 | `jump.png` | 12 / 4 x 3 | Jump: crouch, leap up, tuck in the air with the braids flying, fall and land softly back in the ready stance. | todo |
| 8 | `hurt.png` | 12 / 4 x 3 | Hurt: get hit from the right, flinch back with a pained face, stagger one step, recover to the ready stance. | todo |
| 9 | `death.png` | 12 / 4 x 3 | Down: get hit hard, fall backwards to the ground, the bow drops beside her, lie still (last 3 frames the same). | todo |
| 10 | `skill_gale.png` | 12 / 4 x 3 | Skill 2 pose "gale arrow" (strong, dynamic): 1-2 step forward and plant the feet very wide; 3-6 draw the bow slowly to full, body twisting, the string glowing brighter, wind pulling the braids, fur skirt and scarf toward the bow; 7 release with a huge recoil, she slides back half a step, dust bursts at her feet; 8-10 hold the release pose, bow arm locked forward, hair whipping back; 11-12 straighten up into the ready stance. (Small effects only: the big effect comes from Meta.) | todo |
| 11 | `skill_fan.png` | 12 / 4 x 3 | Skill 3 pose "fan shot" (strong, dynamic): 1-2 hop half a step back; 3-5 grab three arrows at once between the fingers and nock them, the bow tilted sideways; 6 sweep the bow from low to high while releasing, arrows leaving in a fan; 7-9 the body follows the sweep, turning slightly, one foot lifted, scarf swinging wide; 10-12 land and settle into the ready stance. (Small effects only: the big effect comes from Meta.) | todo |
| 12 | `skill_frost.png` | 12 / 4 x 3 | Skill 4 pose "frost bloom" (strong, dynamic): 1-3 jump up a little and aim steeply down at the ground a few steps ahead; 4-5 draw hard in the air, frost mist on the arrow tip; 6 release downward, the recoil pushes her up and back; 7-9 flip back once in the air, braids circling; 10-12 land crouched with one hand on the ground, then rise to the ready stance. (Small effects only: the big effect comes from Meta.) | todo |
| 13 | `skill_flip.png` | 12 / 4 x 3 | Skill 5 pose "backflip shot" (strong, dynamic): 1-2 quick crouch; 3-5 spring into a high backflip to the left, body arched, braids and scarf trailing; 6-7 upside down at the top of the flip, draw and fire one arrow to the right; 8-10 finish the rotation, legs tucked; 11-12 land low sliding a little to the left, then rise to the ready stance. (Small effects only: the big effect comes from Meta.) | todo |
| 14 | `skill_wolf.png` | 12 / 4 x 3 | Skill 6 (ULT) pose "spirit wolf" (strongest, dramatic): 1-3 raise the bow high overhead with both hands, head thrown back, the wolf-skull hood's eye sockets light up blue, braids lifting as if in a wind; 4-5 swing the bow down and nock a large glowing arrow; 6-8 deep wide stance, draw to full with the whole body leaning back, a fierce shout; 9 release, a big flash, she is pushed back with her boots dragging; 10-11 hold the release pose, hair and scarf blown back; 12 back to the ready stance. (Small effects only: the big effect comes from Meta.) | todo |

## Skills (design) and their effects
Big effects are made separately by the owner with Meta AI (owner: "ทำสกิลมา ละฉันจะไปให้ meta เจน vfx"): effect only, pure black
background, side view, moving left to right, palette light blue / white with gold sparks. Claude plays them over the pose sheets.
1. ฝนธนู Arrow Rain: one arrow up, a rain of light-blue arrows falls on an area ahead (hits many, 3 waves).
2. ธนูพายุ Gale Arrow: one big arrow wrapped in a spiral wind tunnel flies straight through every enemy in a line.
3. ธนูพัด Fan Shot: 5 glowing arrows in a fan, each with a short trail.
4. ดอกน้ำแข็ง Frost Bloom: the arrow hits the ground and a flower of ice crystals bursts up, enemies inside are slowed.
5. ตีลังกายิง Backflip Shot: dodge back + one fast arrow (escape skill).
6. ULT วิญญาณหมาป่า Spirit Wolf: a giant wolf made of light-blue light leaps out of the arrow and runs forward through all enemies.

Claude cuts the sheets (green out, feet lined up on the ground line, frames joined) and puts them into `hoodfall.html`.
