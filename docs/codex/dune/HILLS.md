# Dune hills kit: stepped mesa terrain for the grinding field (painted 2D)

Owner phrases (2026-11-25): "ทำฉากให้มีที่เก็บเลเวล ให้มีหลายชั้นเป็นเขา ไม่ใช่ลอยๆ", "เนินยาวๆหน่อย", "ทำพร้อมเจนแมพรอเลย".
The game (`dune.html`) now builds the field from stepped HILLS: solid earth tiers 124 game units high stacked like a mountain, each tier a long flat walkable top. Right now their walls reuse `ground.png`, so a carved emblem repeats on every tier. This kit gives them their own art.
Branch `codex/dune-hills` from the newest `origin/main` (run `git fetch` first), pictures in `art/incoming/dune_hills/` (full-size PNG) plus `REPORT_TH.txt` (Thai, short). Commit and push after EVERY picture. Open a PR, do not merge. Do not edit html, tools or CLAUDE.md. Every file under 10 MB.

## Style lock
Match `art/incoming/dune/ground.png`, `art/incoming/dune/platforms.png` and `art/incoming/dune/props_ruins.png` (or the cut versions in `art/dune/env/ground.webp`, `plat_m.webp`, `column.webp`): smooth PAINTED 2D, confident dark outline, rich warm colour, soft cel shading, golden-hour desert, light from the upper left. NOT pixel art, not photo, not 3D. Crisp edges (the owner wants everything sharp). Genre only: nothing copied from any existing game.
Cut-out pictures: perfectly flat magenta background #FF00FF, no shadow on the background, no magenta inside objects, every object fully inside the picture and separated from the others by a wide gap.

## Pictures, in this order
1. `hill_face.png` (1536 x 1024, magenta above the top edge): a seamless LEFT-RIGHT tiling wall of a sandstone mesa terrace seen from the side. Top 12 %: a crisp sunlit sand lip with small dry tufts, nearly level. Below: layered sandstone strata, cracks, a few roots and pebbles, two or three small glowing turquoise rune stones set into the rock, getting darker and cooler toward the bottom. NO big carved emblem or anything that would repeat obviously; it must look good when only the top 25 % is shown and when the full height is shown.
2. `hill_caps.png` (1536 x 1024, magenta): two pieces on one row, widely spaced: the LEFT END and the RIGHT END of such a terrace, seen from the side: a weathered, slightly rounded sandstone corner with the same sand lip and the same strata as `hill_face.png` so they join it seamlessly, full picture height, each about 300 px wide.
3. `hill_props.png` (1536 x 1024, magenta): 7 separate objects standing on their base, side view: vines and roots hanging over a ledge edge (hanging DOWN from a flat top line), a pile of small boulders, a bleached desert beast skull with horns, a broken pillar stub with a glowing rune, a cluster of turquoise crystals, a tattered red banner on a wooden pole, a small flowering cactus.
4. `bg_mesas.png` (1536 x 1024, must tile seamlessly left to right, magenta above): a mid-distance range of STEPPED mesas and terraced cliffs with a few ruined arches on top, warm amber in the sun, violet in the shadows, across the lower 55 %, softer and lower contrast than the foreground.

Open each picture beside `art/incoming/dune/ground.png` and redo it if the style, light or colours drift, a tiling edge does not continue, or an object touches the border. Say in `REPORT_TH.txt` what still looks off.
