# bag3d.html "ศึกแชมเปี้ยน 3D": three more arena looks + UI glyphs, Codex brief (2026-11-28)

Owner: "ทำเกมส์ให้สวยเลยนะ 3D ทำให้ดูดีมีชาติตระกูล ... UI ทำทุกอย่างให้สวย", "พวกเจนทั้งหลายทำก่อน".
You are making pictures only. Work ONLY inside the current folder. Do not use git, do not edit any other file of the repository.
Make 4 pictures with the image tool, save each as a PNG in the current folder with exactly the file names below, then write `REPORT_TH.txt`
(Thai, short: which file is which, and anything that did not come out right).

Two reference pictures are attached:
- `arena_target.png` = the look of our arena (sunny colosseum). The game changes land every five rounds, so we need the SAME arena in three
  other lands. KEEP the camera, the layout and every big shape exactly where it is: the round floor, the curved wall, the three gates (left,
  centre, right) with their bars, the braziers on the wall, the banners, the stands with the crowd, the medallion in the middle of the floor.
  Only the theme changes: materials, colours, light, decorations, sky. The pictures must line up with `arena_target.png` when laid over it.
- `ref_icons.png` = our item icons: the style for picture 4.

Same style as `arena_target.png` for pictures 1-3: beautiful stylized hand-painted 3D mobile-game look, NOT pixel art, NOT photo-real.
EMPTY arenas: no characters, no monsters, no user interface, no text. 1536 x 1024 each.

## 1. `arena_grave.png`: the midnight graveyard arena
Night. Dark blue-violet stone covered in moss and ivy, cracked and leaning in places; the floor is cold grey-violet earth with scattered
bones, old gravestones and candles near the wall; the medallion in the middle is a carved skull-and-moon seal. Braziers burn with eerie
blue-green ghost fire; banners are torn, dark purple and black with silver emblems; lanterns and candles give small warm points; thin
ground mist; the crowd in the stands is dim hooded figures and pale ghost lights. A big pale moon glow from the top left, cool rim light.

## 2. `arena_volcano.png`: the lava arena
Dark basalt and obsidian walls with glowing orange lava cracks running through them, iron chains and spikes; the floor is dark scorched
rock with thin glowing cracks and embers, a few lava pools near the wall (not in the middle); the medallion in the middle is a carved
flame-and-dragon seal with a faint orange glow. Braziers burn bright orange, banners are black and red with gold emblems; smoke and
sparks rise; the crowd is lit red from below. Sky glow deep red-orange, strong warm light from the lava, dark shadows.

## 3. `arena_snow.png`: the frozen peak arena
Bright cold day. Pale blue-grey stone walls capped with snow and long icicles, frost on the carved frieze; the floor is packed snow and
blue ice with drifts against the wall, a few frozen weapons and ice blocks near the wall; the medallion in the middle is a carved
snowflake seal under clear ice. Braziers burn with warm orange fire (the only warm colour), banners are white and ice-blue with silver
emblems; light snowfall; the crowd wears furs. Soft blue shadows, crisp white light, a faint aurora tint in the sky.

## 4. `ui_glyphs.png`, 1536 x 1024, TRANSPARENT background (or flat pure magenta #FF00FF if transparency is not possible)
12 small UI symbols in exactly the style of `ref_icons.png` (dark-fantasy pixel-art icons, thick dark outline, rich shading), in ONE picture
as a grid of 4 columns x 3 rows, every symbol centred in its own equal cell with clear empty space around it, no grid lines, no frames,
no text, no letters, no numbers. Order, left to right, top to bottom:
1 a red heart (a life)
2 a single shining gold coin
3 a horned demon skull (boss round)
4 two crossed swords over a small round shield (duel round)
5 a monster claw mark, three slashes (monster round)
6 a closed golden padlock
7 an open grey padlock
8 two curved arrows forming a circle (rotate), gold
9 a hand-sized coin purse with a coin dropping in (sell)
10 a five-pointed gold star
11 a double arrow pointing right (speed up), blue steel
12 an open leather backpack with a gem inside (the bag)
