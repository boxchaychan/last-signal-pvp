# Babies & Beasts - Prehistoric Armour forms: image brief

## 0. The job

Babies & Beasts is a pixel-art mobile tower-defense game: six 8-year-old kids in animal kigurumi costumes fight nightmare demons. When two of a kid's strongest units merge, there is a chance to get a secret special form: **PREHISTORIC ARMOUR**, a different prehistoric creature for each kid.
Tan's form (ankylosaurus) is finished and approved by the game owner. **Make the other five in exactly the same style and quality.**

| Kid | Gender | Creature | Why it fits | Save as |
|---|---|---|---|---|
| Nin (นิล) | girl | velociraptor | fast, sleek, sickle claws = her twin daggers | `dino_assassin.png` |
| Fah (ฟ้า) | girl | pteranodon | a flying reptile with sharp eyes, fits the hawk archer | `dino_hunter.png` |
| Ratri (ราตรี) | girl | stegosaurus | the plates on its back become glowing magic crystals | `dino_mage.png` |
| Chan (จันทร์) | boy | triceratops | its big frill is a shield that protects friends, fits the healer | `dino_support.png` |
| Mok (หมอก) | girl | spinosaurus | the sail on its back is a dark mysterious cape | `dino_curse.png` |

## 1. Attached files

| File | What it is |
|---|---|
| `refs/00_STYLE_EXAMPLE_tan_ankylosaurus.png` | Picture 2 for every kid: the finished, approved style example (Tan in ankylosaurus armour). |
| `refs/01_nin_gold.png` | Picture 1 for Nin: Nin's gold-tier picture (face and identity reference, enlarged 6x). |
| `refs/02_fah_gold.png` | Picture 1 for Fah: Fah's gold-tier picture (face and identity reference, enlarged 6x). |
| `refs/03_ratri_gold.png` | Picture 1 for Ratri: Ratri's gold-tier picture (face and identity reference, enlarged 6x). |
| `refs/04_chan_gold.png` | Picture 1 for Chan: Chan's gold-tier picture (face and identity reference, enlarged 6x). |
| `refs/05_mok_gold.png` | Picture 1 for Mok: Mok's gold-tier picture (face and identity reference, enlarged 6x). |
| `prompts/*.txt` | The same per-kid prompts as section 5, one file per kid, ready to paste into an image generator. |

## 2. How to work

1. Read this whole file first, then open and look at every picture in `refs/`.
2. Make the five characters **one at a time**. For each one, give the image generator **both** reference pictures: the kid's gold picture (picture 1) and the style example (picture 2), and use that kid's prompt from section 5 word for word.
3. If you can, make 2-3 versions of each kid and keep the best one, judged with the checklist in section 6. Keep the other versions in `candidates/` (for example `candidates/dino_assassin_2.png`).
4. Save the chosen pictures as PNG with the file names in section 0, in a folder `output/`.
5. These must be **generated illustrations** like the style example. Do not draw them with code (no SVG, canvas or Python drawing), do not trace or edit the reference pictures, and do not shrink or convert them to a small pixel grid yourself: the game's own converter does that afterwards.
6. If you cannot generate images, say so clearly, and give the owner the prompts in `prompts/` to paste into ChatGPT with the two pictures attached.
7. At the end, write a short report: which file is which kid, and anything that did not come out right.

## 3. The style example: what to copy

The style example (refs/00_STYLE_EXAMPLE_tan_ankylosaurus.png) is Tan, an 8-year-old boy, in his ANKYLOSAURUS ARMOUR. The game owner made it and loves it. It is the quality bar and the style bar for all five new pictures. Study it closely:

- Canvas: square (about 1254 x 1254), pure plain white background, nothing else in the picture. The character stands in the middle and fills about 85-90% of the height, with a small white margin all round.
- Pixel art: real pixel art on one even grid (about 6 screen pixels per art pixel, so the character is roughly 200 art pixels tall). Every art pixel is the same size and perfectly square. Hard edges, no anti-aliasing, no blur, no soft airbrush; shading is done in clear pixel steps.
- Outline: a bold dark outline (one art pixel, very dark brown / near black) around the whole silhouette and around each big part (helmet, pauldrons, weapon, cape), so it still reads when shrunk to a small game sprite.
- Proportions: chibi. The head with the helmet is about 40% of the whole height. Short body, short sturdy legs, big hands and boots.
- Pose and view: three-quarter view facing RIGHT (toward the viewer's right), standing tall with the chest out, feet apart and planted, a big confident expression, the weapon held in a fist, the other hand a fist at the side.
- Helmet hood: the creature's whole head sits on top of the kid's head like a hood or helmet. Its snout juts forward (to the right) above the forehead, it has horns, and ONE big bright creature eye is visible on the side of the dinosaur head. The creature's jaw line frames the kid's face like a visor. The kid's whole face is open and fully visible underneath, with hair spilling out at the sides.
- Armour: every armour piece is made from the creature's own hide, showing its texture (bony studs, scales, plates). Pieces are chunky and oversized: big rounded shoulder pauldrons, a chest plate with an emblem, a belt with a buckle, layered skirt plates, knee guards, big armoured boots. Each piece has a bright accent rim (orange cloth) and metal rims and rivets (gold).
- Back: a cape made from the creature's tail sweeps out behind the kid to the LEFT. It is layered, with spikes along its edge and a scalloped trimmed hem. It balances the weapon on the other side, so the silhouette is wide and strong.
- Weapon: very big, made from the creature's signature body part (the ankylosaurus tail club becomes a war hammer resting on his shoulder). It is a key part of the silhouette and is gripped correctly in a fist.
- Colour: a limited palette (about 40 colours). One dark base hide colour, one light bone colour for spikes and studs, one warm accent cloth colour, one metal colour, plus skin and hair. Each colour has 3-4 shade steps, lit from the top left. Rich but clean and readable.
- No aura, no glow round the body, no sparkles, no motion lines, no ground shadow, no frame, no text.

Copy all of that. Do NOT copy: the ankylosaurus, the brown and orange colours, the hammer, or Tan's face and hair. Each new kid keeps their OWN face and gets their OWN creature, colours and weapon.

## 4. Rules for every kid

- Same kid, new costume: the face must match the kid's gold picture (face shape, eye shape and colour, hair style and colour, skin tone, the kind of expression). They are 8 years old: cute chibi children, not teenagers, not adults.
- Both eyes fully visible and bright with a big highlight. No hair over the eyes, no dark shadow over the top half of the eyes, no helmet edge covering the eyes.
- NOT a mascot suit: the face is completely open; the dinosaur head sits ON TOP of the head like a helmet hood.
- The creature must be recognisable from the silhouette alone (see each kid's "must read as" line). Never a T-rex.
- Facing right, three-quarter view, full body from the top of the helmet to the soles of the boots, nothing cut off by the edge.
- Hands: normal small hands with 5 fingers or a clean fist. The weapon is gripped in a fist. No extra arms, legs or fingers.
- Same canvas size, same pixel size and about the same character height as the style example, so all six pictures look like one set.
- This form is legendary (the same power level as the gold tier), so it should look rich and impressive. It does not have to be gold-coloured.
- No aura, no glow round the body, no sparkles, no particles, no motion lines, no ground shadow, no background scenery, no frame, no text, no signature, no watermark. Small glowing parts that belong to the costume (a crystal, an eye, a bowstring) are fine.

## 5. The five kids

### 5.1 Nin (นิล) - Velociraptor armour -> `dino_assassin.png`

- **Attach:** `refs/01_nin_gold.png` (picture 1) + `refs/00_STYLE_EXAMPLE_tan_ankylosaurus.png` (picture 2)
- **Who:** an 8-year-old girl. Normally wears a black panther kigurumi assassin (gold tier: black hood with panther ears and gold trims, two curved golden daggers).
- **Keep:** short straight black bob hair with blunt bangs above the eyes; golden-yellow eyes; light warm skin; a cool, calm, slightly smug little smile.
- **Must read as a velociraptor:** a long narrow toothy snout jutting forward, a crest of feathers on the head, big curved sickle claws on the feet, a long thin tail behind.
- **Head:** a big velociraptor head worn as a helmet hood: a long narrow snout jutting forward over her forehead with a row of small sharp white teeth along the jaw, a crest of deep purple feathers sweeping back from the top, one sharp glowing violet eye on the side of the dinosaur head, small nostril holes on the snout tip.
- **Body:** sleek light armour made of black raptor scales: pointed shoulder guards trimmed with a fringe of purple feathers, a fitted chest plate with a silver claw-mark emblem, dark wrapped forearms with silver bracers, a purple sash belt with a silver buckle, short scaled skirt plates, slim greaves, and boots that each end in one big curved bone-white sickle claw.
- **Back:** a long thin cape shaped like a feathered raptor tail, sweeping out behind her to the left: dark scales down the middle with a fringe of purple feathers along both edges, ending in a pointed feather tip.
- **Weapon:** two big curved sickle-claw daggers made of bone-white raptor claws with silver hilts, held in a REVERSE GRIP exactly like her gold picture: a silver ring sits on top of each fist, the curved blade comes out of the BOTTOM of the fist (the little-finger side) and curves back toward her body. The blades never come out of the sleeve.
- **Pose:** three-quarter view facing right, a low ready stance, knees bent, weight forward, one dagger held forward at chest height and the other held back by her hip.
- **Palette (hex, dark / mid / light):**
  - black scale hide: `#1b1a22 / #2e2c3a / #4a4760`
  - deep purple feathers: `#3d2266 / #6a3fb0 / #a07ae6`
  - bone-white claws and teeth: `#efe4d0 / #c8b79c`
  - silver metal: `#e2e4ec / #a4a8b8 / #6c7084`
  - hair black: `#141319 / #2a2833`
  - eyes: `#f2b630`
  - skin: `#f6d2b8 / #e0aa8c`

**Prompt (use word for word):**

```
Two pictures are attached. Picture 1 = Nin's gold picture (use it for her face and identity). Picture 2 = a finished example of this costume style: a different kid (Tan) in an ankylosaurus armour. Copy its style, level of detail, chunky armour shapes, shading, outline, pose energy, canvas and quality, but NOT its creature, colours, weapon or face.

Draw Nin, the SAME 8-year-old girl as picture 1, in a new legendary special form: VELOCIRAPTOR ARMOUR. Nin normally wears a black panther kigurumi assassin (gold tier: black hood with panther ears and gold trims, two curved golden daggers); this form replaces that costume with a prehistoric velociraptor armour.

Identity (keep exactly): short straight black bob hair with blunt bangs above the eyes, golden-yellow eyes, light warm skin, a cool, calm, slightly smug little smile. Both eyes fully visible and bright, no hair over the eyes.

Head: a big velociraptor head worn as a helmet hood: a long narrow snout jutting forward over her forehead with a row of small sharp white teeth along the jaw, a crest of deep purple feathers sweeping back from the top, one sharp glowing violet eye on the side of the dinosaur head, small nostril holes on the snout tip. Her whole face is open and fully visible below the dinosaur jaw, which frames it like a visor; her hair spills out at the sides.

Body: sleek light armour made of black raptor scales: pointed shoulder guards trimmed with a fringe of purple feathers, a fitted chest plate with a silver claw-mark emblem, dark wrapped forearms with silver bracers, a purple sash belt with a silver buckle, short scaled skirt plates, slim greaves, and boots that each end in one big curved bone-white sickle claw.

Back: a long thin cape shaped like a feathered raptor tail, sweeping out behind her to the left: dark scales down the middle with a fringe of purple feathers along both edges, ending in a pointed feather tip.

Weapon: two big curved sickle-claw daggers made of bone-white raptor claws with silver hilts, held in a REVERSE GRIP exactly like her gold picture: a silver ring sits on top of each fist, the curved blade comes out of the BOTTOM of the fist (the little-finger side) and curves back toward her body. The blades never come out of the sleeve.

Pose: three-quarter view facing right, a low ready stance, knees bent, weight forward, one dagger held forward at chest height and the other held back by her hip.

Must read as a velociraptor from the silhouette: a long narrow toothy snout jutting forward, a crest of feathers on the head, big curved sickle claws on the feet, a long thin tail behind.

Colours (lit from the top left, 3-4 shade steps each): black scale hide #1b1a22 / #2e2c3a / #4a4760; deep purple feathers #3d2266 / #6a3fb0 / #a07ae6; bone-white claws and teeth #efe4d0 / #c8b79c; silver metal #e2e4ec / #a4a8b8 / #6c7084; hair black #141319 / #2a2833; eyes #f2b630; skin #f6d2b8 / #e0aa8c.

Style: chibi pixel art game character, big head (helmet and head about 40% of the height), full body, standing. Rich detailed pixel art like a high-quality RPG sprite: chunky readable shapes, clear light-and-shadow shading on every armour piece, about 40 colours, every pixel a perfect square of the same size on one even grid, no blur, no anti-aliasing, a bold dark outline. Square canvas, plain pure white background, the character centred and filling about 85-90% of the height. No aura, no sparkles, no effects, no ground shadow, no text.
```

<details><summary>Optional: 4 design options to choose from</summary>

```
Two pictures are attached. Picture 1 = Nin's gold picture (face and identity). Picture 2 = a finished example of the costume style (a different kid in an ankylosaurus armour): copy its style and quality, not its creature, colours or weapon.

Character concept sheet for a pixel art game: 4 different design options of Nin (the same 8-year-old girl as picture 1: short straight black bob hair with blunt bangs above the eyes, golden-yellow eyes) in her VELOCIRAPTOR ARMOUR form, in a 2x2 grid, full body, all in a three-quarter view facing right, a small number 1-4 under each option. Every option: a big velociraptor head worn as a helmet hood with her whole face showing, armour made of velociraptor hide, a cape made from its tail, wings or sail, and a big weapon made from its signature body part. Must read as a velociraptor: a long narrow toothy snout jutting forward, a crest of feathers on the head, big curved sickle claws on the feet, a long thin tail behind. Main colours: black scale hide, deep purple feathers, bone-white claws and teeth, silver metal. Make each option clearly different in shape. Chibi, big head, rich detailed pixel art with clear shading, bold dark outline, both eyes fully visible, plain white background, no aura, no effects, no text except the small numbers.
```
</details>

### 5.2 Fah (ฟ้า) - Pteranodon armour -> `dino_hunter.png`

- **Attach:** `refs/02_fah_gold.png` (picture 1) + `refs/00_STYLE_EXAMPLE_tan_ankylosaurus.png` (picture 2)
- **Who:** an 8-year-old girl. Normally wears a brown hawk kigurumi archer (gold tier: feathered hawk hood with glowing sky-blue eyes, feather wing cape with sky-blue tips, big carved wooden longbow).
- **Keep:** brown shoulder-length hair with bangs; big warm brown eyes; light warm skin with rosy cheeks; a bright cheerful open-mouth smile.
- **Must read as a pteranodon:** a long pointed beak and a long crest sweeping back so the head makes one long horizontal line, folded leathery wings with claws at the wing joints.
- **Head:** a big pteranodon head worn as a helmet hood: a long straight pointed beak jutting forward over her forehead and a long pointed crest sweeping far back behind her head, one big amber eye on the side of the head, small gold rivets along the base of the crest.
- **Body:** light ranger armour made of warm brown pteranodon hide: shoulder guards shaped like folded wing joints each with a small hooked claw, a chest plate with a wing emblem, leather bracers with gold rims, a belt with a gold buckle, a quiver of arrows with sky-blue fletching on her hip, short layered skirt flaps, light boots with cream bone toe caps.
- **Back:** a cape shaped like two folded pteranodon wings sweeping out behind her to the left: sky-blue leathery membrane stretched between long brown wing bones, small claws at the wing joints, a gold-trimmed scalloped edge.
- **Weapon:** a big longbow made of two curved cream pteranodon wing bones joined by a gold-wrapped grip, with a glowing sky-blue string and an arrow with a sky-blue arrowhead.
- **Pose:** three-quarter view facing right, standing tall and proud, the longbow held upright in her front (right) fist, an arrow nocked and held lightly with the other hand, not fully drawn.
- **Palette (hex, dark / mid / light):**
  - warm brown hide: `#5e3a22 / #8f5c38 / #b8834f`
  - sky-blue membrane: `#2f8fd6 / #5fbdf2 / #a8e2ff`
  - cream bone: `#f2e4c6 / #cdb88e`
  - gold trims: `#b9781e / #e0a42c / #ffd36a`
  - hair brown: `#4a2a18 / #6e4128`
  - eyes: `#6a3c1e`
  - skin: `#f6d2b8 / #e0aa8c`
  - cheeks: `#f2a0a0`

**Prompt (use word for word):**

```
Two pictures are attached. Picture 1 = Fah's gold picture (use it for her face and identity). Picture 2 = a finished example of this costume style: a different kid (Tan) in an ankylosaurus armour. Copy its style, level of detail, chunky armour shapes, shading, outline, pose energy, canvas and quality, but NOT its creature, colours, weapon or face.

Draw Fah, the SAME 8-year-old girl as picture 1, in a new legendary special form: PTERANODON ARMOUR. Fah normally wears a brown hawk kigurumi archer (gold tier: feathered hawk hood with glowing sky-blue eyes, feather wing cape with sky-blue tips, big carved wooden longbow); this form replaces that costume with a prehistoric pteranodon armour.

Identity (keep exactly): brown shoulder-length hair with bangs, big warm brown eyes, light warm skin with rosy cheeks, a bright cheerful open-mouth smile. Both eyes fully visible and bright, no hair over the eyes.

Head: a big pteranodon head worn as a helmet hood: a long straight pointed beak jutting forward over her forehead and a long pointed crest sweeping far back behind her head, one big amber eye on the side of the head, small gold rivets along the base of the crest. Her whole face is open and fully visible below the dinosaur jaw, which frames it like a visor; her hair spills out at the sides.

Body: light ranger armour made of warm brown pteranodon hide: shoulder guards shaped like folded wing joints each with a small hooked claw, a chest plate with a wing emblem, leather bracers with gold rims, a belt with a gold buckle, a quiver of arrows with sky-blue fletching on her hip, short layered skirt flaps, light boots with cream bone toe caps.

Back: a cape shaped like two folded pteranodon wings sweeping out behind her to the left: sky-blue leathery membrane stretched between long brown wing bones, small claws at the wing joints, a gold-trimmed scalloped edge.

Weapon: a big longbow made of two curved cream pteranodon wing bones joined by a gold-wrapped grip, with a glowing sky-blue string and an arrow with a sky-blue arrowhead.

Pose: three-quarter view facing right, standing tall and proud, the longbow held upright in her front (right) fist, an arrow nocked and held lightly with the other hand, not fully drawn.

Must read as a pteranodon from the silhouette: a long pointed beak and a long crest sweeping back so the head makes one long horizontal line, folded leathery wings with claws at the wing joints.

Colours (lit from the top left, 3-4 shade steps each): warm brown hide #5e3a22 / #8f5c38 / #b8834f; sky-blue membrane #2f8fd6 / #5fbdf2 / #a8e2ff; cream bone #f2e4c6 / #cdb88e; gold trims #b9781e / #e0a42c / #ffd36a; hair brown #4a2a18 / #6e4128; eyes #6a3c1e; skin #f6d2b8 / #e0aa8c; cheeks #f2a0a0.

Style: chibi pixel art game character, big head (helmet and head about 40% of the height), full body, standing. Rich detailed pixel art like a high-quality RPG sprite: chunky readable shapes, clear light-and-shadow shading on every armour piece, about 40 colours, every pixel a perfect square of the same size on one even grid, no blur, no anti-aliasing, a bold dark outline. Square canvas, plain pure white background, the character centred and filling about 85-90% of the height. No aura, no sparkles, no effects, no ground shadow, no text.
```

<details><summary>Optional: 4 design options to choose from</summary>

```
Two pictures are attached. Picture 1 = Fah's gold picture (face and identity). Picture 2 = a finished example of the costume style (a different kid in an ankylosaurus armour): copy its style and quality, not its creature, colours or weapon.

Character concept sheet for a pixel art game: 4 different design options of Fah (the same 8-year-old girl as picture 1: brown shoulder-length hair with bangs, big warm brown eyes) in her PTERANODON ARMOUR form, in a 2x2 grid, full body, all in a three-quarter view facing right, a small number 1-4 under each option. Every option: a big pteranodon head worn as a helmet hood with her whole face showing, armour made of pteranodon hide, a cape made from its tail, wings or sail, and a big weapon made from its signature body part. Must read as a pteranodon: a long pointed beak and a long crest sweeping back so the head makes one long horizontal line, folded leathery wings with claws at the wing joints. Main colours: warm brown hide, sky-blue membrane, cream bone, gold trims. Make each option clearly different in shape. Chibi, big head, rich detailed pixel art with clear shading, bold dark outline, both eyes fully visible, plain white background, no aura, no effects, no text except the small numbers.
```
</details>

### 5.3 Ratri (ราตรี) - Stegosaurus armour -> `dino_mage.png`

- **Attach:** `refs/03_ratri_gold.png` (picture 1) + `refs/00_STYLE_EXAMPLE_tan_ankylosaurus.png` (picture 2)
- **Who:** an 8-year-old girl. Normally wears a purple owl kigurumi mage (gold tier: tall pointed wizard hat with owl ears and a silver crescent moon, starry night-blue cape, staff topped with a silver crescent moon).
- **Keep:** silver-white hair in two small buns with soft side locks; violet eyes; fair skin; a calm, wise little smile.
- **Must read as a stegosaurus:** a row of tall upright plates running from the top of the head down the back, and a tail ending in four long spikes.
- **Head:** a big stegosaurus head worn as a helmet hood: a small beaked snout jutting forward over her forehead, one big glowing violet eye on the side of the head, and a row of tall glowing violet crystal plates standing up along the top of the hood.
- **Body:** a mage armour-robe made of deep purple stegosaurus scales: shoulder guards shaped like small crystal plates, a chest plate with a glowing violet crystal emblem, a long night-blue robe skirt with small silver stars and a silver trim, a belt with a silver crescent buckle, scaly purple boots.
- **Back:** a cape shaped like a stegosaurus back and tail sweeping out behind her to the left: two rows of glowing violet crystal plates running down it, ending in a thick tail with four long bone spikes.
- **Weapon:** a tall staff of dark wood wrapped in silver, topped with a big glowing violet crystal shaped like a stegosaurus plate.
- **Pose:** three-quarter view facing right, standing calmly, the staff planted on the ground in her front (right) fist, the other hand open at her side with the palm turned out.
- **Palette (hex, dark / mid / light):**
  - deep purple scales: `#2e1c55 / #4f3290 / #7558bf`
  - glowing violet crystals: `#8d4be6 / #b97cff / #ead6ff`
  - night-blue cloth: `#1a2048 / #2b3672`
  - silver: `#eceef6 / #aeb2c8 / #73789a`
  - hair silver-white: `#f2f0f8 / #cfcae0 / #a39dbd`
  - eyes: `#9a5cf0`
  - skin: `#f8dcc8 / #e3b49a`

**Prompt (use word for word):**

```
Two pictures are attached. Picture 1 = Ratri's gold picture (use it for her face and identity). Picture 2 = a finished example of this costume style: a different kid (Tan) in an ankylosaurus armour. Copy its style, level of detail, chunky armour shapes, shading, outline, pose energy, canvas and quality, but NOT its creature, colours, weapon or face.

Draw Ratri, the SAME 8-year-old girl as picture 1, in a new legendary special form: STEGOSAURUS ARMOUR. Ratri normally wears a purple owl kigurumi mage (gold tier: tall pointed wizard hat with owl ears and a silver crescent moon, starry night-blue cape, staff topped with a silver crescent moon); this form replaces that costume with a prehistoric stegosaurus armour.

Identity (keep exactly): silver-white hair in two small buns with soft side locks, violet eyes, fair skin, a calm, wise little smile. Both eyes fully visible and bright, no hair over the eyes.

Head: a big stegosaurus head worn as a helmet hood: a small beaked snout jutting forward over her forehead, one big glowing violet eye on the side of the head, and a row of tall glowing violet crystal plates standing up along the top of the hood. Her whole face is open and fully visible below the dinosaur jaw, which frames it like a visor; her hair spills out at the sides.

Body: a mage armour-robe made of deep purple stegosaurus scales: shoulder guards shaped like small crystal plates, a chest plate with a glowing violet crystal emblem, a long night-blue robe skirt with small silver stars and a silver trim, a belt with a silver crescent buckle, scaly purple boots.

Back: a cape shaped like a stegosaurus back and tail sweeping out behind her to the left: two rows of glowing violet crystal plates running down it, ending in a thick tail with four long bone spikes.

Weapon: a tall staff of dark wood wrapped in silver, topped with a big glowing violet crystal shaped like a stegosaurus plate.

Pose: three-quarter view facing right, standing calmly, the staff planted on the ground in her front (right) fist, the other hand open at her side with the palm turned out.

Must read as a stegosaurus from the silhouette: a row of tall upright plates running from the top of the head down the back, and a tail ending in four long spikes.

Colours (lit from the top left, 3-4 shade steps each): deep purple scales #2e1c55 / #4f3290 / #7558bf; glowing violet crystals #8d4be6 / #b97cff / #ead6ff; night-blue cloth #1a2048 / #2b3672; silver #eceef6 / #aeb2c8 / #73789a; hair silver-white #f2f0f8 / #cfcae0 / #a39dbd; eyes #9a5cf0; skin #f8dcc8 / #e3b49a.

Style: chibi pixel art game character, big head (helmet and head about 40% of the height), full body, standing. Rich detailed pixel art like a high-quality RPG sprite: chunky readable shapes, clear light-and-shadow shading on every armour piece, about 40 colours, every pixel a perfect square of the same size on one even grid, no blur, no anti-aliasing, a bold dark outline. Square canvas, plain pure white background, the character centred and filling about 85-90% of the height. No aura, no sparkles, no effects, no ground shadow, no text.
```

<details><summary>Optional: 4 design options to choose from</summary>

```
Two pictures are attached. Picture 1 = Ratri's gold picture (face and identity). Picture 2 = a finished example of the costume style (a different kid in an ankylosaurus armour): copy its style and quality, not its creature, colours or weapon.

Character concept sheet for a pixel art game: 4 different design options of Ratri (the same 8-year-old girl as picture 1: silver-white hair in two small buns with soft side locks, violet eyes) in her STEGOSAURUS ARMOUR form, in a 2x2 grid, full body, all in a three-quarter view facing right, a small number 1-4 under each option. Every option: a big stegosaurus head worn as a helmet hood with her whole face showing, armour made of stegosaurus hide, a cape made from its tail, wings or sail, and a big weapon made from its signature body part. Must read as a stegosaurus: a row of tall upright plates running from the top of the head down the back, and a tail ending in four long spikes. Main colours: deep purple scales, glowing violet crystals, night-blue cloth, silver. Make each option clearly different in shape. Chibi, big head, rich detailed pixel art with clear shading, bold dark outline, both eyes fully visible, plain white background, no aura, no effects, no text except the small numbers.
```
</details>

### 5.4 Chan (จันทร์) - Triceratops armour -> `dino_support.png`

- **Attach:** `refs/04_chan_gold.png` (picture 1) + `refs/00_STYLE_EXAMPLE_tan_ankylosaurus.png` (picture 2)
- **Who:** an 8-year-old boy. Normally wears a white rabbit kigurumi healer (gold tier: long rabbit ears with pink insides, a small silver crescent moon on the hood, white-and-pink cape, scepter topped with a glowing pink crystal carrot).
- **Keep:** fluffy honey-blonde hair; bright blue eyes; light warm skin; a kind, cheerful smile.
- **Must read as a triceratops:** a huge round frill rising behind the head like a halo, two long horns over the forehead and a small nose horn.
- **Head:** a big triceratops head worn as a helmet hood: a wide round frill rising behind his head like a halo shield with pink scalloped edges and small gold studs, two long cream horns above his forehead and a small horn on the snout, one big pink eye on the side of the head.
- **Body:** rounded guardian armour made of cream-white triceratops hide: round shoulder plates with pink edges, a chest plate with a pink heart emblem, a leaf-green healer sash across the body, a belt with a gold buckle, round knee guards and sturdy cream boots.
- **Back:** a short cape shaped like a thick triceratops tail sweeping out behind him to the left, cream-white with pink plate edges and a gold-trimmed hem; a small round frill-shaped shield strapped to his free forearm.
- **Weapon:** a healing staff wrapped in gold, topped with a big glowing pink crystal shaped like a triceratops horn.
- **Pose:** three-quarter view facing right, standing firm and friendly, the healing staff held upright in his front (right) fist, a small round frill shield on his other forearm.
- **Palette (hex, dark / mid / light):**
  - cream-white hide: `#f6f1e8 / #ddd2c2 / #b5a690`
  - soft pink: `#d46a98 / #f39ac0 / #ffd0e2`
  - leaf-green: `#3f9a45 / #74c876`
  - gold: `#b9781e / #e0a42c / #ffd36a`
  - hair honey-blonde: `#f4c96a / #d9a040 / #a86f22`
  - eyes: `#3a8ee0`
  - skin: `#f8dcc8 / #e3b49a`

**Prompt (use word for word):**

```
Two pictures are attached. Picture 1 = Chan's gold picture (use it for his face and identity). Picture 2 = a finished example of this costume style: a different kid (Tan) in an ankylosaurus armour. Copy its style, level of detail, chunky armour shapes, shading, outline, pose energy, canvas and quality, but NOT its creature, colours, weapon or face.

Draw Chan, the SAME 8-year-old boy as picture 1, in a new legendary special form: TRICERATOPS ARMOUR. Chan normally wears a white rabbit kigurumi healer (gold tier: long rabbit ears with pink insides, a small silver crescent moon on the hood, white-and-pink cape, scepter topped with a glowing pink crystal carrot); this form replaces that costume with a prehistoric triceratops armour.

Identity (keep exactly): fluffy honey-blonde hair, bright blue eyes, light warm skin, a kind, cheerful smile. Both eyes fully visible and bright, no hair over the eyes.

Head: a big triceratops head worn as a helmet hood: a wide round frill rising behind his head like a halo shield with pink scalloped edges and small gold studs, two long cream horns above his forehead and a small horn on the snout, one big pink eye on the side of the head. His whole face is open and fully visible below the dinosaur jaw, which frames it like a visor; his hair spills out at the sides.

Body: rounded guardian armour made of cream-white triceratops hide: round shoulder plates with pink edges, a chest plate with a pink heart emblem, a leaf-green healer sash across the body, a belt with a gold buckle, round knee guards and sturdy cream boots.

Back: a short cape shaped like a thick triceratops tail sweeping out behind him to the left, cream-white with pink plate edges and a gold-trimmed hem; a small round frill-shaped shield strapped to his free forearm.

Weapon: a healing staff wrapped in gold, topped with a big glowing pink crystal shaped like a triceratops horn.

Pose: three-quarter view facing right, standing firm and friendly, the healing staff held upright in his front (right) fist, a small round frill shield on his other forearm.

Must read as a triceratops from the silhouette: a huge round frill rising behind the head like a halo, two long horns over the forehead and a small nose horn.

Colours (lit from the top left, 3-4 shade steps each): cream-white hide #f6f1e8 / #ddd2c2 / #b5a690; soft pink #d46a98 / #f39ac0 / #ffd0e2; leaf-green #3f9a45 / #74c876; gold #b9781e / #e0a42c / #ffd36a; hair honey-blonde #f4c96a / #d9a040 / #a86f22; eyes #3a8ee0; skin #f8dcc8 / #e3b49a.

Style: chibi pixel art game character, big head (helmet and head about 40% of the height), full body, standing. Rich detailed pixel art like a high-quality RPG sprite: chunky readable shapes, clear light-and-shadow shading on every armour piece, about 40 colours, every pixel a perfect square of the same size on one even grid, no blur, no anti-aliasing, a bold dark outline. Square canvas, plain pure white background, the character centred and filling about 85-90% of the height. No aura, no sparkles, no effects, no ground shadow, no text.
```

<details><summary>Optional: 4 design options to choose from</summary>

```
Two pictures are attached. Picture 1 = Chan's gold picture (face and identity). Picture 2 = a finished example of the costume style (a different kid in an ankylosaurus armour): copy its style and quality, not its creature, colours or weapon.

Character concept sheet for a pixel art game: 4 different design options of Chan (the same 8-year-old boy as picture 1: fluffy honey-blonde hair, bright blue eyes) in his TRICERATOPS ARMOUR form, in a 2x2 grid, full body, all in a three-quarter view facing right, a small number 1-4 under each option. Every option: a big triceratops head worn as a helmet hood with his whole face showing, armour made of triceratops hide, a cape made from its tail, wings or sail, and a big weapon made from its signature body part. Must read as a triceratops: a huge round frill rising behind the head like a halo, two long horns over the forehead and a small nose horn. Main colours: cream-white hide, soft pink, leaf-green, gold. Make each option clearly different in shape. Chibi, big head, rich detailed pixel art with clear shading, bold dark outline, both eyes fully visible, plain white background, no aura, no effects, no text except the small numbers.
```
</details>

### 5.5 Mok (หมอก) - Spinosaurus armour -> `dino_curse.png`

- **Attach:** `refs/05_mok_gold.png` (picture 1) + `refs/00_STYLE_EXAMPLE_tan_ankylosaurus.png` (picture 2)
- **Who:** an 8-year-old girl. Normally wears a dark crow kigurumi curse-caster (gold tier: big black feather wings with purple edges, a silver crow mask on the hood, a dark staff with a glowing purple eye orb).
- **Keep:** messy black hair with one grey streak; purple eyes; pale skin; a mischievous little smirk.
- **Must read as a spinosaurus:** a very tall sail on the back, and a long narrow crocodile-like snout.
- **Head:** a big spinosaurus head worn as a helmet hood: a long narrow crocodile-like snout jutting forward over her forehead with small white teeth, one glowing purple eye on the side of the head, a small sail-shaped crest on top.
- **Body:** dark witch armour made of dark navy spinosaurus scales with thin glowing purple veins: pointed shoulder guards with bone spikes, a chest plate with a glowing purple eye emblem, a ragged dark robe skirt, a necklace of small bones and teeth, scaly boots.
- **Back:** a tall ragged sail rising high from her back like a spinosaurus sail: dark navy membrane with glowing purple veins stretched between long bone-white spines, ending in a long scaly tail cape that sweeps out to the left.
- **Weapon:** a staff made of a long spinosaurus jaw bone full of small teeth, topped with a glowing purple eye orb held in a bone claw.
- **Pose:** three-quarter view facing right, standing with a sly lean, the staff held forward in her front (right) fist, the other hand raised at chest height with fingers curled like casting.
- **Palette (hex, dark / mid / light):**
  - dark navy scales: `#121528 / #1f2546 / #333c6a`
  - purple glow: `#7a35d6 / #a25cff / #d3b0ff`
  - bone: `#ece2d0 / #b9ab94`
  - dark silver: `#5f6378 / #9a9eb2`
  - hair black + grey streak: `#121216 / #2a2a33 + #8a8a96`
  - eyes: `#a45cff`
  - pale skin: `#f2dccf / #d8b4a4`

**Prompt (use word for word):**

```
Two pictures are attached. Picture 1 = Mok's gold picture (use it for her face and identity). Picture 2 = a finished example of this costume style: a different kid (Tan) in an ankylosaurus armour. Copy its style, level of detail, chunky armour shapes, shading, outline, pose energy, canvas and quality, but NOT its creature, colours, weapon or face.

Draw Mok, the SAME 8-year-old girl as picture 1, in a new legendary special form: SPINOSAURUS ARMOUR. Mok normally wears a dark crow kigurumi curse-caster (gold tier: big black feather wings with purple edges, a silver crow mask on the hood, a dark staff with a glowing purple eye orb); this form replaces that costume with a prehistoric spinosaurus armour.

Identity (keep exactly): messy black hair with one grey streak, purple eyes, pale skin, a mischievous little smirk. Both eyes fully visible and bright, no hair over the eyes.

Head: a big spinosaurus head worn as a helmet hood: a long narrow crocodile-like snout jutting forward over her forehead with small white teeth, one glowing purple eye on the side of the head, a small sail-shaped crest on top. Her whole face is open and fully visible below the dinosaur jaw, which frames it like a visor; her hair spills out at the sides.

Body: dark witch armour made of dark navy spinosaurus scales with thin glowing purple veins: pointed shoulder guards with bone spikes, a chest plate with a glowing purple eye emblem, a ragged dark robe skirt, a necklace of small bones and teeth, scaly boots.

Back: a tall ragged sail rising high from her back like a spinosaurus sail: dark navy membrane with glowing purple veins stretched between long bone-white spines, ending in a long scaly tail cape that sweeps out to the left.

Weapon: a staff made of a long spinosaurus jaw bone full of small teeth, topped with a glowing purple eye orb held in a bone claw.

Pose: three-quarter view facing right, standing with a sly lean, the staff held forward in her front (right) fist, the other hand raised at chest height with fingers curled like casting.

Must read as a spinosaurus from the silhouette: a very tall sail on the back, and a long narrow crocodile-like snout.

Colours (lit from the top left, 3-4 shade steps each): dark navy scales #121528 / #1f2546 / #333c6a; purple glow #7a35d6 / #a25cff / #d3b0ff; bone #ece2d0 / #b9ab94; dark silver #5f6378 / #9a9eb2; hair black + grey streak #121216 / #2a2a33 + #8a8a96; eyes #a45cff; pale skin #f2dccf / #d8b4a4.

Style: chibi pixel art game character, big head (helmet and head about 40% of the height), full body, standing. Rich detailed pixel art like a high-quality RPG sprite: chunky readable shapes, clear light-and-shadow shading on every armour piece, about 40 colours, every pixel a perfect square of the same size on one even grid, no blur, no anti-aliasing, a bold dark outline. Square canvas, plain pure white background, the character centred and filling about 85-90% of the height. No aura, no sparkles, no effects, no ground shadow, no text.
```

<details><summary>Optional: 4 design options to choose from</summary>

```
Two pictures are attached. Picture 1 = Mok's gold picture (face and identity). Picture 2 = a finished example of the costume style (a different kid in an ankylosaurus armour): copy its style and quality, not its creature, colours or weapon.

Character concept sheet for a pixel art game: 4 different design options of Mok (the same 8-year-old girl as picture 1: messy black hair with one grey streak, purple eyes) in her SPINOSAURUS ARMOUR form, in a 2x2 grid, full body, all in a three-quarter view facing right, a small number 1-4 under each option. Every option: a big spinosaurus head worn as a helmet hood with her whole face showing, armour made of spinosaurus hide, a cape made from its tail, wings or sail, and a big weapon made from its signature body part. Must read as a spinosaurus: a very tall sail on the back, and a long narrow crocodile-like snout. Main colours: dark navy scales, purple glow, bone, dark silver. Make each option clearly different in shape. Chibi, big head, rich detailed pixel art with clear shading, bold dark outline, both eyes fully visible, plain white background, no aura, no effects, no text except the small numbers.
```
</details>

## 6. Checklist for each picture

- [ ] Plain white background, square canvas, character centred, nothing cut off
- [ ] Real pixel art: one even grid, square pixels, hard edges, no blur or soft gradients
- [ ] Bold dark outline round the whole figure and the big parts
- [ ] Three-quarter view facing RIGHT
- [ ] Face, hair colour and eye colour match the kid's gold picture; looks 8 years old
- [ ] Both eyes fully visible and bright
- [ ] Dinosaur head worn as a helmet hood with one visible creature eye; the face fully open
- [ ] The creature is obvious from the silhouette (see "must read as")
- [ ] Armour made of the creature's hide, chunky pieces with trims and rivets, like the style example
- [ ] Cape from the tail / wings / sail sweeps out to the left
- [ ] Big weapon made from the creature's body part, gripped in a fist (Nin: reverse grip, blade from the bottom of the fist)
- [ ] Colours follow the kid's palette; no aura, no sparkles, no text
- [ ] Looks as rich and polished as the Tan example, and like the same set

## 7. After you finish

The owner sends the five PNG files to Claude, who turns them into the game's pixel sprites (`art/bb/dino_<class>.png`) and puts them in the game. Big, clean, white-background pictures convert best.
