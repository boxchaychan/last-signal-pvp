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
Row 1 is for later: the gap the owner saw was only the join between two screenshots, the game's wall is complete.
| # | key | status | style picture to attach | what |
|---|-----|--------|-------------------------|------|
| 1 | thai_wall_top | later (do it after 2-6) | art/action/props/wall_front.png + art/action/props/t_gate.png | Thai city wall pieces seen from above |
| 2 | china_buildings | todo | art/incoming/action/map/gpt_thai_city.png | China city buildings |
| 3 | china_village | todo | art/incoming/action/map/gpt_thai_city.png | China village buildings |
| 4 | china_nature | todo | art/incoming/action/map/gpt_nature.png | China trees and rocks |
| 5 | china_props | todo | art/incoming/action/map/gpt_thai_city_props.png | China props |
| 6 | china_ground | todo | art/incoming/action/map/gpt_ground.png | China ground textures |

## Prompts

### 1 thai_wall_top
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
