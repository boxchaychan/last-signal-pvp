# Dune side-scrolling world: all the pictures (painted 2D)

Owner phrase: "ทำชุดภาพแมพทะเลทราย". The owner's only demand: IT MUST LOOK BEAUTIFUL, like a polished commercial 2D side-scrolling RPG.
Single-player side-scroller. Genre only: original designs, never copy names, characters, maps or art of any existing game.

Branch `codex/dune-world`, pictures in `art/incoming/dune/` (full-size PNG), plus `REPORT_TH.txt` (Thai, short: which file is which, what still looks off).
Commit after EVERY picture so nothing is lost. Do not edit html, tools or CLAUDE.md. Do not merge. Keep every file under 10 MB.

## Style lock (every picture)
- Look at `art/incoming/dragon_moves/base_side.png` first (the hero) and `git show codex/desert-monsters:art/incoming/desert_monsters/mummy_base.png` (a monster). Match them: smooth PAINTED 2D, confident dark outline on foreground objects, rich saturated colour, soft cel shading, warm light. NOT pixel art, not photo, not 3D render.
- World: a golden-hour desert oasis with sandstone tomb ruins, turquoise water, palms, red and gold cloth, warm lanterns. Palette: amber, terracotta, cream sand, teal shadow accents, deep violet distance.
- Light comes from the upper left in every picture.
- No text, letters, numbers, logos, watermark, UI frames or characters unless the item asks for them.
- Cut-out pictures: perfectly flat magenta background #FF00FF, no shadow on the background, no magenta inside objects, every object fully inside the picture and separated from the others by a wide gap.

## Pictures, in this order
Backgrounds (landscape 1536 x 1024, must tile seamlessly left to right: the left edge continues the right edge):
1. `bg_sky.png`: opaque golden-hour sky, big soft sun low on the left third, painterly layered clouds, violet at the top to peach at the horizon. No ground.
2. `bg_far.png`: distant violet-amber mesas and dunes across the lower 55 %, atmospheric and low contrast, magenta above them.
3. `bg_mid.png`: mid-distance sand dunes with silhouetted tomb ruins, broken arches, an obelisk and palm groups across the lower 60 %, warmer and clearer than bg_far, magenta above them.

Ground and platforms (cut-out, magenta):
4. `ground.png` (1536 x 1024): a seamless left-right strip of walkable ground seen from the side: a crisp sunlit sand top edge with small tufts in the top 15 %, below it rich layered sandstone cliff with cracks and buried carved blocks filling down to the very bottom of the picture. The top edge stays nearly level. Magenta only above it.
5. `platforms.png` (1536 x 1024): three separate pieces on one row, widely spaced: LEFT CAP, a MIDDLE piece that tiles seamlessly left-right, RIGHT CAP, all the same height: floating carved sandstone ledge, flat sand-covered walkable top, hanging roots and broken stone below. Below them, on a second row, one complete short floating platform.
6. `climb.png` (1024 x 1536): on the left a tall rope ladder of wood and red cloth that tiles top to bottom, on the right a knotted hanging rope that tiles top to bottom.

Props (cut-out, magenta, 1536 x 1024, about 5-7 well separated objects per sheet, standing on their base, side view):
7. `props_plants.png`: 3 different date palms (tall), desert shrub, flowering cactus, tufts of dry grass.
8. `props_ruins.png`: tall carved column, broken column, stone arch, obelisk, a sphinx-like original guardian statue, fallen blocks.
9. `props_camp.png`: striped market tent, merchant stall with cloth awning, hanging lanterns on a pole, clay jars, wooden crates, treasure chest, signpost without text.
10. `props_water.png`: a wide oasis pond seen from the side with reeds and lily flowers, a small waterfall from a carved stone spout, a stone well.
11. `portal.png` (1024 x 1024): an ornate sandstone gate with a swirling glowing turquoise portal inside.

Characters (same quality as the hero; side view facing RIGHT unless stated):
12. `npc_merchant.png` (1024 x 1024, magenta): a friendly chibi desert merchant, an original fennec-fox person with turban and big backpack, facing LEFT.
13. `npc_elder.png` (1024 x 1024, magenta): a wise chibi old tortoise person with staff and gold jewellery, facing LEFT.
14. `golem_base.png`: BOSS, sand-stone golem, gold tomb runes glowing orange, huge fists, heavy silhouette, 2 x the hero's height, plain flat white background.
15-17. `golem_walk.png`, `golem_attack.png`, `golem_hurt_death.png`: same sheet rules as `docs/codex/dragon/MONSTERS.md`: 16 frames, 4 x 4, portrait 1024 x 1536, flat blue #0248BA, thin dark ground line in each cell, same size every frame, moving in place, never touching another cell. Attack = raises both fists, smashes the ground with a burst of sand. Death = cracks and crumbles into a pile of glowing rubble.

Interface art (cut-out, magenta):
18. `icons.png` (1024 x 1024): a strict 4 x 4 grid of 16 painted game icons, each centred in its cell with a wide gap: spear thrust, spear sweep, fire leap, flame dash, red potion, blue potion, gold coin, turquoise gem, leather boots, gold ring, iron chest armour, flame spear, scroll, key, heart, star.
19. `ui_panel.png` (1536 x 1024): one ornate empty panel of dark teal cloth with a carved gold and sandstone frame, its middle plain and flat; below it, a wide empty gold-framed bar and one round gold-framed button.

Key art:
20. `title_art.png` (1536 x 1024, opaque): the hero from `base_side.png` in a heroic pose on a ruin ledge at golden hour above a vast oasis valley, with the mummy, scorpion and sand wolf far below. Leave the upper-middle sky clear for a title. Cinematic, the most beautiful picture of the set.

## Check before you finish
Open each picture. Redo any that looks muddy, has text, breaks the left-right seam, has an object touching the edge, or does not match the hero's style. Say in `REPORT_TH.txt` what still looks off.
