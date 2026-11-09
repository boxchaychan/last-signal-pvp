# Map art for the action game (`action.html`) — queue for Codex

Owner 2026-11-09: monsters and maps go by country; keep generating until the credits run out. Reply in Thai, short and plain.

## Rules
- ONE picture per row of the queue. Attach the style picture named in the row every time (it sets pixel size, dark outline,
  shading, colours and the camera angle: seen from the front-corner and a little from above).
- Plain pure-white background, every object separate with white space round it, nothing touching, no text, no letters, no
  grid lines, no shadows on the background, no glow, no people, no statues of gods. Keep the full generated size.
- Save as `art/incoming/maps/<key>.png`; one Thai line per file in `art/incoming/maps/REPORT_TH.txt`; mark the row `done`.
- Work in the worktree `../last-signal-pvp-codex` on your own branch, never switch branches in `C:\last-signal-pvp`, never push
  to `main`, never merge. Before a new batch: `git -C ../last-signal-pvp-codex merge origin/main` to get new rows.

## Queue
Owner 2026-11-09: "เจนแบบมาพร้อมประกอบเลย gptเราโควต้าเยอะ หมดก็รอ": make 0a and 0b as pieces ready to put together, spend the quota; when it runs out, stop and wait.
Owner 2026-11-09: cities are separate places and field maps join between them into a world map, so not every map is a
city; the village, nature, props and ground sheets are for those field maps.
Owner 2026-11-09 "เมืองต่อเป็นเมืองใหญ่เลยนะ": the China map is a BIG walled city (much bigger than the Thai one), so it gets two building sheets (2 and 2b).
| # | key | status | style picture to attach | what |
|---|-----|--------|-------------------------|------|
| 0a | thai_gate_4view | todo (URGENT, do first) | art/action/props/t_gate.png + art/action/props/wall_front.png + art/action/props/wall_side.png | the Thai city gate from 4 views |
| 0b | thai_wall_kit | todo (URGENT, right after 0a) | art/action/props/wall_front.png + art/action/props/t_gate.png + art/action/props/t_fort_w.png | wall pieces that fit together: straight runs, corners, ends, wall walk |
| 1 | thai_wall_top | dropped (part of 0b) | art/action/props/wall_front.png + art/action/props/t_gate.png | Thai city wall pieces seen from above |
| 2 | china_buildings | todo | art/incoming/action/map/gpt_thai_city.png | China city buildings |
| 2b | china_buildings2 | todo | art/incoming/action/map/gpt_thai_city.png | more China city buildings (the China map is a BIG city) |
| 3 | china_village | todo | art/incoming/action/map/gpt_thai_city.png | China village buildings |
| 4 | china_nature | todo | art/incoming/action/map/gpt_nature.png | China trees and rocks |
| 5 | china_props | todo | art/incoming/action/map/gpt_thai_city_props.png | China props |
| 6 | china_ground | todo | art/incoming/action/map/gpt_ground.png | China ground textures |

## Prompts

### 0a thai_gate_4view (owner 2026-11-09 "ประตูเจนมาเลย 4 มุม")
```
Use the attached pictures as the style guide: t_gate.png is THIS gate seen from the front, wall_front.png and
wall_side.png are the city wall it stands in. Draw THE SAME Thai city gate (same white plaster and bricks, the same
tiered red-tiled roof with the spire, the same wooden double doors, sema merlons, same pixel size, dark outline,
shading, colours and scale) from 4 views for a top-down action game, the camera a little from above like the attached
gate, in one row on a plain pure-white background, every view separate with wide white space round it:
1. FRONT: seen from outside the city, like the attached gate (redraw it cleanly, same size).
2. BACK: seen from inside the city: the inner side of the same gate tower, the same doors, short stairs up to the wall
walk on both sides.
3. LEFT SIDE: the gate turned 90 degrees, seen from its side: the wall runs straight away from the camera (north to
south), the gateway passage goes left-right through the tower, the doors face LEFT, the tiered roof seen from the side.
4. RIGHT SIDE: the same as 3 but the doors face RIGHT.
All four the same height and scale as the attached gate, standing on the same ground line. No text, no letters, no
grid lines, no shadows on the background, no glow, no people.
```

### 0b thai_wall_kit (pieces ready to put together)
```
Use the attached pictures as the style guide: wall_front.png is a piece of THIS wall seen from the front, t_gate.png
and t_fort_w.png stand in it. Pixel-art KIT of matching CITY WALL PIECES for a top-down action game that the game
puts together into a closed rectangular city wall (the camera looks from the south, a little from above). Same white
plaster with the cross-shaped holes, the same pointed sema merlons, same pixel size, dark outline, shading, colours and
height as the attached wall. Plain pure-white background, every piece separate with wide white space round it, laid
out in 3 rows:
Row 1 - walls running ACROSS (east-west), each piece exactly the same width and height so they join edge to edge
seamlessly: 1. front face seen from outside (south wall), 2. back face seen from inside the city (north wall: the
inner face with the wall walk and merlons on top), 3. an end cap where an across wall stops.
Row 2 - walls running AWAY from the camera (north-south), seen from above at the same angle, each piece the same
width and length so they stack top to bottom seamlessly: 4. the west wall (outer face on its left side, the wall walk
between two rows of merlons on top), 5. the east wall (outer face on its right side), 6. an end cap of a north-south
wall seen from the front.
Row 3 - the four CORNERS where they meet, seen from the camera: 7. north-west, 8. north-east, 9. south-west,
10. south-east; each corner's arms end exactly like the pieces in rows 1 and 2 so they join without a gap.
No text, no letters, no grid lines, no shadows on the background, no glow, no plants, no people.
```

### 1 thai_wall_top (dropped, part of 0b)
```
Use the two attached pictures as the style guide: the same white-plaster wall, pixel size, dark outline, shading and colours,
same camera angle (seen from the front and a little from above). Pixel-art asset sheet of matching CITY WALL PIECES for a
top-down action game, on a plain pure-white background, every piece separate with white space round it:
1-3. three pieces of the SAME wall running straight AWAY from the camera (north-south), seen from above: the top walkway
between two rows of square merlons along both edges, the left side face of the wall visible, the pieces tile seamlessly one
after another top to bottom (identical width, same height, the merlons line up), each piece about as long as the wall is
thick;
4. the corner where a wall running away from the camera meets a wall running across (an L seen from above, merlons round
the outer edge);
5. the end of a wall running away from the camera: its front face with merlons, as tall as the attached wall.
Same scale as the attached wall. No text, no letters, no grid lines, no shadows on the background, no glow, no plants.
```

### 2 china_buildings
```
Use the attached picture as the style guide: same pixel size, same dark outline, same shading and colours, same camera angle
(seen from the front-corner and a little from above). Pixel-art asset sheet of an ANCIENT CHINESE WALLED CITY, on a plain
pure-white background. Every building separate, with white space around it, nothing touching. All at the same scale as the
attached buildings. 18 buildings, 3 rows of 6:
1. grand palace hall on a white stone terrace with red columns and a double yellow-glazed hip roof with upturned eaves,
2. five-storey pagoda tower with green-glazed roofs, 3. city gate tower over an arched gate in a grey brick wall,
4. two-storey tea house with red lanterns and carved wooden balconies, 5. shop with an open front, hanging cloth sign and
shelves of goods, 6. courtyard house with a grey tiled roof and a round moon gate in its wall,
7. drum tower, 8. bell tower, 9. scholar's study pavilion, 10. noodle shop with a steaming pot at the front,
11. apothecary with drawers and jars, 12. blacksmith with a forge,
13. inn with a balcony and a wine banner, 14. grey brick watchtower, 15. open hexagonal garden pavilion,
16. stone arched bridge, 17. guardhouse at a gate, 18. rich family's house with red doors and door gods painted as
simple patterns (no faces).
No people, no statues of gods, no text, no letters, no grid lines, no shadows on the background, no glow.
```

### 2b china_buildings2 (the China map is a big city)
```
Use the attached picture as the style guide: same pixel size, same dark outline, same shading and colours, same camera angle
(seen from the front-corner and a little from above). Pixel-art asset sheet of MORE buildings for a BIG ancient Chinese
walled city, on a plain pure-white background. Every building separate, with white space around it, nothing touching. All at
the same scale as the attached buildings. 18 buildings, 3 rows of 6:
1. magistrate's office (yamen) with a red gate and two drums, 2. three-storey restaurant with lanterns, 3. silk shop with
bolts of cloth, 4. pawn shop with a tall counter, 5. long two-storey shop row (4 shops joined), 6. grey courtyard house of a
poor family, 7. large merchant mansion with a garden wall, 8. archery hall with targets, 9. martial arts school with a
training yard, 10. teahouse on a lotus pond, 11. granary of the city with round silos, 12. stables with horses' stalls
(no horses), 13. paper lantern workshop, 14. ceramics shop with big blue-and-white vases, 15. opera stage with red
curtains, 16. city wall corner tower, 17. covered market hall, 18. small arched gate between two districts.
No people, no statues of gods, no text, no letters, no grid lines, no shadows on the background, no glow.
```

### 3 china_village
```
Use the attached picture as the style guide: same pixel size, same dark outline, same shading and colours, same camera angle.
Pixel-art asset sheet of a CHINESE COUNTRY VILLAGE by a river with rice terraces, on a plain pure-white background. Every
building separate with white space around it, nothing touching, all at the same scale. 18 buildings, 3 rows of 6:
1. farmhouse with mud walls and a thatched roof, 2. farmhouse with white walls and a grey tiled roof, 3. stilt house over
water, 4. rice granary on stone legs, 5. water mill with a wooden wheel, 6. bamboo house,
7. ox stable, 8. pig pen with a little shed, 9. village well with a roof, 10. small roadside shrine with a tiled roof and an
incense burner (no statue), 11. market stall with baskets of vegetables, 12. tea plantation hut,
13. fishing hut with nets drying, 14. wooden boat shed, 15. village gate (paifang) of wood, 16. chicken coop,
17. pottery kiln, 18. hanging laundry and drying racks with chillies.
No people, no statues of gods, no text, no letters, no grid lines, no shadows on the background, no glow.
```

### 4 china_nature
```
Use the attached picture as the style guide: same pixel size, same dark outline, same shading and colours, same camera angle.
Pixel-art asset sheet of CHINESE LANDSCAPE plants and rocks for a top-down action game, on a plain pure-white background,
every item separate with white space round it. 18 items, 3 rows of 6:
1. big plum blossom tree with pink flowers, 2. twisted mountain pine on a rock, 3. weeping willow, 4. tall bamboo clump,
5. ginkgo tree in yellow, 6. red maple, 7. small plum blossom tree, 8. young bamboo shoots, 9. lotus pads with flowers (to
stand in water), 10. tall scholar's rock with holes, 11. group of mossy boulders, 12. flowering azalea bush,
13. peony bush, 14. reeds, 15. tea bushes in a row, 16. tall karst rock pillar with a small pine on top, 17. fallen log
with mushrooms, 18. big round bush.
No people, no text, no letters, no grid lines, no shadows on the background, no glow.
```

### 5 china_props
```
Use the attached picture as the style guide: same pixel size, same dark outline, same shading and colours, same camera angle.
Pixel-art asset sheet of props for an ANCIENT CHINESE TOWN, on a plain pure-white background, every item separate with white
space round it. 18 items, 3 rows of 6:
1. red paper lantern on a post, 2. string of red lanterns, 3. pair of stone guardian lions, 4. big bronze incense burner
(no statue), 5. wooden water barrels, 6. stacked crates and sacks of rice,
7. wooden hand cart, 8. red banner on a pole (blank, no letters), 9. low grey brick wall with tiles on top, 10. bamboo fence,
11. stone lamp, 12. big ceramic water vat with lotus, 13. weapon rack with spears, 14. tea table with stools,
15. firecracker strings (unlit), 16. carved stone dragon pillar, 17. blank wooden signboard on a frame, 18. well bucket and
pole.
No people, no text, no letters, no grid lines, no shadows on the background, no glow.
```

### 6 china_ground
```
Use the attached picture as the style guide for colours and pixel size. Six square seamless ground texture tiles for a
top-down pixel-art game, each a separate square on a plain pure-white background, 2 rows of 3:
1. grey stone paving slabs, 2. old grey brick courtyard paving in a herringbone pattern, 3. packed yellow-brown earth road,
4. clear jade-green river water with small ripples, 5. green grass with a few fallen pink plum petals,
6. flooded rice terrace (shallow water with young green rice rows).
Every tile fills its whole square with no border, flat lighting, no shadows, no text.
```
