# grind3d.html: picture jobs for Codex / GPT (written by Claude, 2026-11-17)

The new level-grinding game `grind3d.html` is 3D (three.js): the hero is a chibi archer girl (Tripo AI model, look at
`art/incoming/tribe3d/warrior_split_look.png` and `art/incoming/grind3d/room_look.png`), the world is bright stylized low-poly
(Quaternius / KayKit style), camera about 35 degrees from above. Codex makes 2D pictures only; Claude turns them into game parts.
Rules of AGENTS.md apply: new branch, pictures in `art/incoming/<folder>/` full size PNG + `REPORT_TH.txt`, open a pull request, never merge.
Original designs only, no text, no watermark, no logos.

## Job A: "ทำไอคอนสกิล" (branch `codex/grind3d-icons`, folder `art/incoming/grind3d_icons/`)
Four round skill-button icons, 1024 x 1024 PNG each, see-through background (if that fails: flat #00B140 green):
- `icon_shoot.png` ยิงธนู: a bow drawn with an arrow, warm gold / orange
- `icon_dodge.png` กลิ้งหลบ: a fast sideways swoosh / dash trail, sky blue
- `icon_rain.png` ฝนธนู: many arrows falling into a glowing gold circle on the ground
- `icon_pierce.png` ธนูทะลวง: one big glowing cyan arrow piercing forward with a burst
Style: bright painted mobile-RPG icons, thick dark outline, strong light, simple shapes that still read at 64 px. One icon per picture.

## Job B: "ทำพื้นแมพ" (branch `codex/grind3d-ground`, folder `art/incoming/grind3d_ground/`)
Seamless TILEABLE ground textures seen straight from above, 1024 x 1024 PNG each:
`grass.png` (bright green grass, a few tiny white / yellow flowers), `dirt.png` (warm brown trodden earth, small pebbles),
`stone.png` (old grey flagstones with moss in the gaps), `forest.png` (forest floor: leaves, twigs, moss).
Painted, stylized, soft; NO light direction, NO cast shadows, no big single objects (the game lights it). Left edge must continue
into the right edge and top into bottom: put a 2 x 2 test tiling of each into `tile_test_<name>.png`.

## Job C: "วาดตัวละครใหม่ <บอกว่าเป็นใคร>" (branch `codex/grind3d-hero-<name>`, folder `art/incoming/grind3d_hero_<name>/`)
A design picture of ONE new chibi hero that Tripo AI will turn into 3D (image to 3D), so it must be clean:
- `front.png`: full body, straight FRONT view, A-pose (arms 30-45 degrees away from the body, hands open, legs a little apart),
  about 2.5 heads tall like the huntress, plain light grey background, even soft light, no ground shadow, nothing cut off.
- `weapon.png`: the hero's weapon alone, flat side view, same style (the weapon is NOT in the hands in front.png).
- `hat.png`: only if the hero has a hat / hood / helmet: the hat alone, and in front.png draw the hero WITHOUT it (hair shown),
  so the hat can be taken off in the game.
- `three_quarter.png` (optional): the same hero at a 3/4 front view, same pose.
Bright, cute, fantasy tribal / adventure clothes; readable shapes; no thin loose strings or floating bits.

## Job D: "วาดแมพ" (branch `codex/grind3d-maps`, folder `art/incoming/grind3d_maps/`)
Three concept paintings (1920 x 1080) of possible FIRST maps for the grinding game, each seen from the game camera (about 35 degrees
from above, looking a little forward): `map_forest.png` sunny forest clearings joined by paths, `map_ruins.png` old stone ruins
in a jungle, `map_river.png` riverside with wooden bridges. Each shows open fields for monster packs, paths between them and one
bigger arena for a boss. Bright stylized low-poly look, no characters needed.
