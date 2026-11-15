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
| 6 | `skill_rain.png` | 12 / 4 x 3 | Skill 1 pose "arrow rain": kneel, aim high, fire one glowing arrow straight up, hold the pose looking up, stand back up to the ready stance. (Only a small glow on the arrow: the big effect comes from Meta.) | todo |
| 7 | `jump.png` | 12 / 4 x 3 | Jump: crouch, leap up, tuck in the air with the braids flying, fall and land softly back in the ready stance. | todo |
| 8 | `hurt.png` | 12 / 4 x 3 | Hurt: get hit from the right, flinch back with a pained face, stagger one step, recover to the ready stance. | todo |
| 9 | `death.png` | 12 / 4 x 3 | Down: get hit hard, fall backwards to the ground, the bow drops beside her, lie still (last 3 frames the same). | todo |
| 10 | `skill_gale.png` | 12 / 4 x 3 | Skill 2 pose "gale arrow": plant the feet wide, draw the bow fully for a long moment, release forward with a strong recoil, recover. (Small effects only.) | todo |
| 11 | `skill_fan.png` | 12 / 4 x 3 | Skill 3 pose "fan shot": draw three arrows at once, release them in a fan to the right, recover. (Small effects only.) | todo |
| 12 | `skill_frost.png` | 12 / 4 x 3 | Skill 4 pose "frost bloom": aim down at the ground a few steps ahead, fire, then step back. (Small effects only.) | todo |
| 13 | `skill_flip.png` | 12 / 4 x 3 | Skill 5 pose "backflip shot": backflip away to the left while firing one arrow to the right at the top of the flip, land ready. | todo |
| 14 | `skill_wolf.png` | 12 / 4 x 3 | Skill 6 (ULT) pose "spirit wolf": raise the bow overhead, the wolf-skull hood's eyes glow, bring the bow down and fire forward with both feet planted, hold, recover. (Small effects only.) | todo |

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
