# ผู้กล้าเสี่ยงดวง (lucky.html): art set 2, Codex brief ("ทำภาพเกมเสี่ยงดวงชุด 2")

Set 1 is in `art/incoming/lucky2d/` (`heroes_a.png`, `monsters_a.png`, `boss_a.png`, `arena_a.png`, `icons_a.png`) and is the STYLE AND SCALE
reference for everything here: smooth 2D cartoon for a cute mobile game, chibi about 2.2 heads tall, thick dark outline, flat bright colours
with simple soft cel shading, NOT pixel art. Original designs only, no text, no watermark, no ground shadow, transparent background
(or one flat #FF00FF background if transparency is not possible).

Branch `codex/lucky-art2`, pictures in `art/incoming/lucky2d_b/` with a short `REPORT_TH.txt`. Open a pull request, do not merge it, do not
edit `lucky.html` (Claude cuts the sheets with `tools/art/lucky2d_cut.py` and wires them in). Make sheet 1 first and check it against
`heroes_a.png` before the rest.

Every hero / monster sheet: 1536 x 1024, a 3 x 2 grid of equal 512 x 512 cells, one figure centred in each cell, all six at the SAME scale
as the figures of set 1 (heroes about 90 % of the cell height, small monsters about 75 %), feet on one line per row, nothing touching the
cell edges. Heroes face the viewer, turned slightly to the right, relaxed ready pose. Monsters are in side view facing LEFT, walking.

## 1. `heroes_b.png`: six more heroes
1. Bomber kid: goggles on the forehead, orange scarf, a round black bomb with a lit fuse in one hand, a bag of bombs.
2. Acolyte girl: white and gold robe, short brown hair, a small bell staff, a soft glow.
3. Shield knight: steel armour, blue plume, a big tower shield and a short mace.
4. Crossbow gunner girl: brown cap, red jacket, a big repeating crossbow.
5. Druid boy: leaf cloak, antler headband, a gnarled staff with a green glowing seed.
6. Storm shaman: feathered headdress, teal robe, a drum, small lightning sparks round the hands.

## 2. `heroes_c.png`: six more heroes (higher ranks, a little more ornate)
1. Holy priestess: long white hair, white and blue dress with gold trim, a tall cross staff, a small halo.
2. Moon archer: silver hair, dark blue cloak with moon and stars, a glowing crescent bow.
3. Dragon tamer girl: red twin tails, leather armour, a tiny orange dragon sitting on her shoulder, a spear.
4. Thunder king (mythic): gold crown, dark blue armour with yellow lightning trim, cape, a crackling lightning sword.
5. Snow queen (mythic): ice crown, long pale blue hair, white fur gown, an ice sceptre, snowflakes round her.
6. Flame demon lord (mythic): small horns, black and crimson armour, a burning greatsword, embers round him (cute, not scary).

## 3. `heroes_a_attack.png`: the six heroes of `heroes_a.png` again, same order, same scale, each in ONE attack pose
Recruit: sword swung forward. Archer: bow fully drawn. Ice mage: staff thrust forward, crystal flaring. Fire wizard: both hands thrown
forward, a fireball leaving. Ninja: mid throw, one kunai released. Paladin: greatsword raised high, glowing.
Keep faces, outfits and sizes exactly as in `heroes_a.png`.

## 4. `monsters_b.png`: six more small monsters (side view facing LEFT, walking, about 75 % of the cell height)
Bat with a round body; armoured beetle; cactus creature with a flower; little imp with a pitchfork; rock golem pup; jelly fish spirit floating.

## 5. `bosses_b.png`, 1536 x 1024, two bosses side by side (each fills about 85 % of its half), side three-quarter view facing LEFT
Left: giant skeleton general with a broken crown and a huge rusty sword. Right: night dragon, dark indigo scales, magenta wing membranes,
glowing cyan eyes.

## 6. `icons_b.png`, 1024 x 1024, eight icons in a 4 x 2 grid (same look as `icons_a.png`)
Anvil with a hammer (enhance), open spell book (mythic recipes), praying hands with sparkles (wish), trash bin (sell), speed arrows x2,
gear (settings), trophy, speaker.
