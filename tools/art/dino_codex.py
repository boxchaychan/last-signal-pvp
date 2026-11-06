# Builds the Codex / image-AI package for the prehistoric special forms (owner 2026-11-06: "ขอคำสั่งเจนแบบยาวๆ จะเอาให้ codex ทำ").
# Output: docs/codex/dino/ (PROMPT.md long brief, prompts/<kid>.txt paste-ready, refs/ pictures, README_TH.txt) + docs/codex/dino_codex.zip
# Run from the repo root: python3 tools/art/dino_codex.py [path to the owner's full-size Tan picture]
import os, sys, shutil, zipfile
from PIL import Image

OUT = 'docs/codex/dino'
STYLE_SRC = sys.argv[1] if len(sys.argv) > 1 else None   # the owner's original 1254 px Tan picture (best quality); else the game picture x6

KIDS = [
 dict(cls='assassin', en='Nin', th='นิล', he='girl', creature='velociraptor', why='fast, sleek, sickle claws = her twin daggers',
  old='a black panther kigurumi assassin (gold tier: black hood with panther ears and gold trims, two curved golden daggers)',
  hair='short straight black bob hair with blunt bangs above the eyes', eyes='golden-yellow eyes', skin='light warm skin',
  face='a cool, calm, slightly smug little smile', pose='a low ready stance, knees bent, weight forward, one dagger held forward at chest height and the other held back by her hip',
  sil='a long narrow toothy snout jutting forward, a crest of feathers on the head, big curved sickle claws on the feet, a long thin tail behind',
  head='a big velociraptor head worn as a helmet hood: a long narrow snout jutting forward over her forehead with a row of small sharp white teeth along the jaw, a crest of deep purple feathers sweeping back from the top, one sharp glowing violet eye on the side of the dinosaur head, small nostril holes on the snout tip',
  body='sleek light armour made of black raptor scales: pointed shoulder guards trimmed with a fringe of purple feathers, a fitted chest plate with a silver claw-mark emblem, dark wrapped forearms with silver bracers, a purple sash belt with a silver buckle, short scaled skirt plates, slim greaves, and boots that each end in one big curved bone-white sickle claw',
  back='a long thin cape shaped like a feathered raptor tail, sweeping out behind her to the left: dark scales down the middle with a fringe of purple feathers along both edges, ending in a pointed feather tip',
  weapon='two big curved sickle-claw daggers made of bone-white raptor claws with silver hilts, held in a REVERSE GRIP exactly like her gold picture: a silver ring sits on top of each fist, the curved blade comes out of the BOTTOM of the fist (the little-finger side) and curves back toward her body. The blades never come out of the sleeve',
  pal=[('black scale hide','#1b1a22 / #2e2c3a / #4a4760'),('deep purple feathers','#3d2266 / #6a3fb0 / #a07ae6'),('bone-white claws and teeth','#efe4d0 / #c8b79c'),('silver metal','#e2e4ec / #a4a8b8 / #6c7084'),('hair black','#141319 / #2a2833'),('eyes','#f2b630'),('skin','#f6d2b8 / #e0aa8c')]),
 dict(cls='hunter', en='Fah', th='ฟ้า', he='girl', creature='pteranodon', why='a flying reptile with sharp eyes, fits the hawk archer',
  old='a brown hawk kigurumi archer (gold tier: feathered hawk hood with glowing sky-blue eyes, feather wing cape with sky-blue tips, big carved wooden longbow)',
  hair='brown shoulder-length hair with bangs', eyes='big warm brown eyes', skin='light warm skin with rosy cheeks',
  face='a bright cheerful open-mouth smile', pose='standing tall and proud, the longbow held upright in her front (right) fist, an arrow nocked and held lightly with the other hand, not fully drawn',
  sil='a long pointed beak and a long crest sweeping back so the head makes one long horizontal line, folded leathery wings with claws at the wing joints',
  head='a big pteranodon head worn as a helmet hood: a long straight pointed beak jutting forward over her forehead and a long pointed crest sweeping far back behind her head, one big amber eye on the side of the head, small gold rivets along the base of the crest',
  body='light ranger armour made of warm brown pteranodon hide: shoulder guards shaped like folded wing joints each with a small hooked claw, a chest plate with a wing emblem, leather bracers with gold rims, a belt with a gold buckle, a quiver of arrows with sky-blue fletching on her hip, short layered skirt flaps, light boots with cream bone toe caps',
  back='a cape shaped like two folded pteranodon wings sweeping out behind her to the left: sky-blue leathery membrane stretched between long brown wing bones, small claws at the wing joints, a gold-trimmed scalloped edge',
  weapon='a big longbow made of two curved cream pteranodon wing bones joined by a gold-wrapped grip, with a glowing sky-blue string and an arrow with a sky-blue arrowhead',
  pal=[('warm brown hide','#5e3a22 / #8f5c38 / #b8834f'),('sky-blue membrane','#2f8fd6 / #5fbdf2 / #a8e2ff'),('cream bone','#f2e4c6 / #cdb88e'),('gold trims','#b9781e / #e0a42c / #ffd36a'),('hair brown','#4a2a18 / #6e4128'),('eyes','#6a3c1e'),('skin','#f6d2b8 / #e0aa8c'),('cheeks','#f2a0a0')]),
 dict(cls='mage', en='Ratri', th='ราตรี', he='girl', creature='stegosaurus', why='the plates on its back become glowing magic crystals',
  old='a purple owl kigurumi mage (gold tier: tall pointed wizard hat with owl ears and a silver crescent moon, starry night-blue cape, staff topped with a silver crescent moon)',
  hair='silver-white hair in two small buns with soft side locks', eyes='violet eyes', skin='fair skin',
  face='a calm, wise little smile', pose='standing calmly, the staff planted on the ground in her front (right) fist, the other hand open at her side with the palm turned out',
  sil='a row of tall upright plates running from the top of the head down the back, and a tail ending in four long spikes',
  head='a big stegosaurus head worn as a helmet hood: a small beaked snout jutting forward over her forehead, one big glowing violet eye on the side of the head, and a row of tall glowing violet crystal plates standing up along the top of the hood',
  body='a mage armour-robe made of deep purple stegosaurus scales: shoulder guards shaped like small crystal plates, a chest plate with a glowing violet crystal emblem, a long night-blue robe skirt with small silver stars and a silver trim, a belt with a silver crescent buckle, scaly purple boots',
  back='a cape shaped like a stegosaurus back and tail sweeping out behind her to the left: two rows of glowing violet crystal plates running down it, ending in a thick tail with four long bone spikes',
  weapon='a tall staff of dark wood wrapped in silver, topped with a big glowing violet crystal shaped like a stegosaurus plate',
  pal=[('deep purple scales','#2e1c55 / #4f3290 / #7558bf'),('glowing violet crystals','#8d4be6 / #b97cff / #ead6ff'),('night-blue cloth','#1a2048 / #2b3672'),('silver','#eceef6 / #aeb2c8 / #73789a'),('hair silver-white','#f2f0f8 / #cfcae0 / #a39dbd'),('eyes','#9a5cf0'),('skin','#f8dcc8 / #e3b49a')]),
 dict(cls='support', en='Chan', th='จันทร์', he='boy', creature='triceratops', why='its big frill is a shield that protects friends, fits the healer',
  old='a white rabbit kigurumi healer (gold tier: long rabbit ears with pink insides, a small silver crescent moon on the hood, white-and-pink cape, scepter topped with a glowing pink crystal carrot)',
  hair='fluffy honey-blonde hair', eyes='bright blue eyes', skin='light warm skin',
  face='a kind, cheerful smile', pose='standing firm and friendly, the healing staff held upright in his front (right) fist, a small round frill shield on his other forearm',
  sil='a huge round frill rising behind the head like a halo, two long horns over the forehead and a small nose horn',
  head='a big triceratops head worn as a helmet hood: a wide round frill rising behind his head like a halo shield with pink scalloped edges and small gold studs, two long cream horns above his forehead and a small horn on the snout, one big pink eye on the side of the head',
  body='rounded guardian armour made of cream-white triceratops hide: round shoulder plates with pink edges, a chest plate with a pink heart emblem, a leaf-green healer sash across the body, a belt with a gold buckle, round knee guards and sturdy cream boots',
  back='a short cape shaped like a thick triceratops tail sweeping out behind him to the left, cream-white with pink plate edges and a gold-trimmed hem; a small round frill-shaped shield strapped to his free forearm',
  weapon='a healing staff wrapped in gold, topped with a big glowing pink crystal shaped like a triceratops horn',
  pal=[('cream-white hide','#f6f1e8 / #ddd2c2 / #b5a690'),('soft pink','#d46a98 / #f39ac0 / #ffd0e2'),('leaf-green','#3f9a45 / #74c876'),('gold','#b9781e / #e0a42c / #ffd36a'),('hair honey-blonde','#f4c96a / #d9a040 / #a86f22'),('eyes','#3a8ee0'),('skin','#f8dcc8 / #e3b49a')]),
 dict(cls='curse', en='Mok', th='หมอก', he='girl', creature='spinosaurus', why='the sail on its back is a dark mysterious cape',
  old='a dark crow kigurumi curse-caster (gold tier: big black feather wings with purple edges, a silver crow mask on the hood, a dark staff with a glowing purple eye orb)',
  hair='messy black hair with one grey streak', eyes='purple eyes', skin='pale skin',
  face='a mischievous little smirk', pose='standing with a sly lean, the staff held forward in her front (right) fist, the other hand raised at chest height with fingers curled like casting',
  sil='a very tall sail on the back, and a long narrow crocodile-like snout',
  head='a big spinosaurus head worn as a helmet hood: a long narrow crocodile-like snout jutting forward over her forehead with small white teeth, one glowing purple eye on the side of the head, a small sail-shaped crest on top',
  body='dark witch armour made of dark navy spinosaurus scales with thin glowing purple veins: pointed shoulder guards with bone spikes, a chest plate with a glowing purple eye emblem, a ragged dark robe skirt, a necklace of small bones and teeth, scaly boots',
  back='a tall ragged sail rising high from her back like a spinosaurus sail: dark navy membrane with glowing purple veins stretched between long bone-white spines, ending in a long scaly tail cape that sweeps out to the left',
  weapon='a staff made of a long spinosaurus jaw bone full of small teeth, topped with a glowing purple eye orb held in a bone claw',
  pal=[('dark navy scales','#121528 / #1f2546 / #333c6a'),('purple glow','#7a35d6 / #a25cff / #d3b0ff'),('bone','#ece2d0 / #b9ab94'),('dark silver','#5f6378 / #9a9eb2'),('hair black + grey streak','#121216 / #2a2a33 + #8a8a96'),('eyes','#a45cff'),('pale skin','#f2dccf / #d8b4a4')]),
]

STYLE_BREAKDOWN = """The style example (refs/00_STYLE_EXAMPLE_tan_ankylosaurus.png) is Tan, an 8-year-old boy, in his ANKYLOSAURUS ARMOUR. The game owner made it and loves it. It is the quality bar and the style bar for all five new pictures. Study it closely:

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

Copy all of that. Do NOT copy: the ankylosaurus, the brown and orange colours, the hammer, or Tan's face and hair. Each new kid keeps their OWN face and gets their OWN creature, colours and weapon."""

RULES = """- Same kid, new costume: the face must match the kid's gold picture (face shape, eye shape and colour, hair style and colour, skin tone, the kind of expression). They are 8 years old: cute chibi children, not teenagers, not adults.
- Both eyes fully visible and bright with a big highlight. No hair over the eyes, no dark shadow over the top half of the eyes, no helmet edge covering the eyes.
- NOT a mascot suit: the face is completely open; the dinosaur head sits ON TOP of the head like a helmet hood.
- The creature must be recognisable from the silhouette alone (see each kid's "must read as" line). Never a T-rex.
- Facing right, three-quarter view, full body from the top of the helmet to the soles of the boots, nothing cut off by the edge.
- Hands: normal small hands with 5 fingers or a clean fist. The weapon is gripped in a fist. No extra arms, legs or fingers.
- Same canvas size, same pixel size and about the same character height as the style example, so all six pictures look like one set.
- This form is legendary (the same power level as the gold tier), so it should look rich and impressive. It does not have to be gold-coloured.
- No aura, no glow round the body, no sparkles, no particles, no motion lines, no ground shadow, no background scenery, no frame, no text, no signature, no watermark. Small glowing parts that belong to the costume (a crystal, an eye, a bowstring) are fine."""

CHECK = """- [ ] Plain white background, square canvas, character centred, nothing cut off
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
- [ ] Looks as rich and polished as the Tan example, and like the same set"""

def kid_prompt(K, two=True):
    he, his, him = ('he', 'his', 'him') if K['he'] == 'boy' else ('she', 'her', 'her')
    pal = '; '.join(n + ' ' + h for n, h in K['pal'])
    head = ('Two pictures are attached. Picture 1 = ' + K['en'] + "'s gold picture (use it for " + his + ' face and identity). '
            'Picture 2 = a finished example of this costume style: a different kid (Tan) in an ankylosaurus armour. Copy its style, level of detail, chunky armour shapes, shading, outline, pose energy, canvas and quality, '
            'but NOT its creature, colours, weapon or face.\n\n') if two else ''
    return (head +
        'Draw ' + K['en'] + ', the SAME 8-year-old ' + K['he'] + ' as picture 1, in a new legendary special form: ' + K['creature'].upper() + ' ARMOUR. '
        + K['en'] + ' normally wears ' + K['old'] + '; this form replaces that costume with a prehistoric ' + K['creature'] + ' armour.\n\n'
        'Identity (keep exactly): ' + K['hair'] + ', ' + K['eyes'] + ', ' + K['skin'] + ', ' + K['face'] + '. Both eyes fully visible and bright, no hair over the eyes.\n\n'
        'Head: ' + K['head'] + '. ' + his.capitalize() + ' whole face is open and fully visible below the dinosaur jaw, which frames it like a visor; ' + his + ' hair spills out at the sides.\n\n'
        'Body: ' + K['body'] + '.\n\n'
        'Back: ' + K['back'] + '.\n\n'
        'Weapon: ' + K['weapon'] + '.\n\n'
        'Pose: three-quarter view facing right, ' + K['pose'] + '.\n\n'
        'Must read as a ' + K['creature'] + ' from the silhouette: ' + K['sil'] + '.\n\n'
        'Colours (lit from the top left, 3-4 shade steps each): ' + pal + '.\n\n'
        'Style: chibi pixel art game character, big head (helmet and head about 40% of the height), full body, standing. Rich detailed pixel art like a high-quality RPG sprite: chunky readable shapes, clear light-and-shadow shading on every armour piece, about 40 colours, '
        'every pixel a perfect square of the same size on one even grid, no blur, no anti-aliasing, a bold dark outline. Square canvas, plain pure white background, the character centred and filling about 85-90% of the height. '
        'No aura, no sparkles, no effects, no ground shadow, no text.')

def sheet_prompt(K):
    his = 'his' if K['he'] == 'boy' else 'her'
    return ('Two pictures are attached. Picture 1 = ' + K['en'] + "'s gold picture (face and identity). Picture 2 = a finished example of the costume style (a different kid in an ankylosaurus armour): copy its style and quality, not its creature, colours or weapon.\n\n"
        'Character concept sheet for a pixel art game: 4 different design options of ' + K['en'] + ' (the same 8-year-old ' + K['he'] + ' as picture 1: ' + K['hair'] + ', ' + K['eyes'] + ') in ' + his + ' ' + K['creature'].upper() + ' ARMOUR form, '
        'in a 2x2 grid, full body, all in a three-quarter view facing right, a small number 1-4 under each option. Every option: a big ' + K['creature'] + ' head worn as a helmet hood with ' + his + ' whole face showing, armour made of ' + K['creature'] + ' hide, '
        'a cape made from its tail, wings or sail, and a big weapon made from its signature body part. Must read as a ' + K['creature'] + ': ' + K['sil'] + '. Main colours: ' + ', '.join(n for n, h in K['pal'][:4]) + '. '
        'Make each option clearly different in shape. Chibi, big head, rich detailed pixel art with clear shading, bold dark outline, both eyes fully visible, plain white background, no aura, no effects, no text except the small numbers.')

def ref_up(src, dst, k):
    im = Image.open(src).convert('RGBA'); big = im.resize((im.width * k, im.height * k), Image.NEAREST)
    bg = Image.new('RGBA', (big.width + 2 * k * 6, big.height + 2 * k * 6), (255, 255, 255, 255)); bg.alpha_composite(big, (k * 6, k * 6)); bg.convert('RGB').save(dst, optimize=True)

def main():
    if os.path.isdir(OUT): shutil.rmtree(OUT)
    os.makedirs(OUT + '/refs'); os.makedirs(OUT + '/prompts')
    sty = OUT + '/refs/00_STYLE_EXAMPLE_tan_ankylosaurus.png'
    if STYLE_SRC: Image.open(STYLE_SRC).convert('RGB').save(sty, optimize=True)
    else: ref_up('art/bb/dino_warrior.png', sty, 6)
    files = [('refs/00_STYLE_EXAMPLE_tan_ankylosaurus.png', 'Picture 2 for every kid: the finished, approved style example (Tan in ankylosaurus armour).')]
    for i, K in enumerate(KIDS, 1):
        name = 'refs/%02d_%s_gold.png' % (i, K['en'].lower())
        ref_up('art/bb/kid_%s_gold.png' % K['cls'], OUT + '/' + name, 6)
        files.append((name, 'Picture 1 for ' + K['en'] + ': ' + K['en'] + "'s gold-tier picture (face and identity reference, enlarged 6x)."))
        with open(OUT + '/prompts/%02d_%s.txt' % (i, K['en'].lower()), 'w', encoding='utf-8') as f:
            f.write('=== ' + K['en'] + ' - ' + K['creature'].upper() + ' ARMOUR ===\nAttach: ' + name + ' (picture 1) + refs/00_STYLE_EXAMPLE_tan_ankylosaurus.png (picture 2)\nSave as: dino_' + K['cls'] + '.png\n\n'
                    + kid_prompt(K) + '\n\n\n=== OPTIONAL: 4 design options to choose from ===\n\n' + sheet_prompt(K) + '\n')
    md = ['# Babies & Beasts - Prehistoric Armour forms: image brief\n',
          '## 0. The job\n',
          'Babies & Beasts is a pixel-art mobile tower-defense game: six 8-year-old kids in animal kigurumi costumes fight nightmare demons. When two of a kid\'s strongest units merge, there is a chance to get a secret special form: **PREHISTORIC ARMOUR**, a different prehistoric creature for each kid.',
          'Tan\'s form (ankylosaurus) is finished and approved by the game owner. **Make the other five in exactly the same style and quality.**\n',
          '| Kid | Gender | Creature | Why it fits | Save as |', '|---|---|---|---|---|']
    for K in KIDS: md.append('| %s (%s) | %s | %s | %s | `dino_%s.png` |' % (K['en'], K['th'], K['he'], K['creature'], K['why'], K['cls']))
    md += ['\n## 1. Attached files\n', '| File | What it is |', '|---|---|'] + ['| `%s` | %s |' % f for f in files]
    md += ['| `prompts/*.txt` | The same per-kid prompts as section 5, one file per kid, ready to paste into an image generator. |',
           '\n## 2. How to work\n',
           '1. Read this whole file first, then open and look at every picture in `refs/`.',
           '2. Make the five characters **one at a time**. For each one, give the image generator **both** reference pictures: the kid\'s gold picture (picture 1) and the style example (picture 2), and use that kid\'s prompt from section 5 word for word.',
           '3. If you can, make 2-3 versions of each kid and keep the best one, judged with the checklist in section 6. Keep the other versions in `candidates/` (for example `candidates/dino_assassin_2.png`).',
           '4. Save the chosen pictures as PNG with the file names in section 0, in a folder `output/`.',
           '5. These must be **generated illustrations** like the style example. Do not draw them with code (no SVG, canvas or Python drawing), do not trace or edit the reference pictures, and do not shrink or convert them to a small pixel grid yourself: the game\'s own converter does that afterwards.',
           '6. If you cannot generate images, say so clearly, and give the owner the prompts in `prompts/` to paste into ChatGPT with the two pictures attached.',
           '7. At the end, write a short report: which file is which kid, and anything that did not come out right.',
           '\n## 3. The style example: what to copy\n', STYLE_BREAKDOWN,
           '\n## 4. Rules for every kid\n', RULES,
           '\n## 5. The five kids\n']
    for i, K in enumerate(KIDS, 1):
        md += ['### 5.%d %s (%s) - %s armour -> `dino_%s.png`\n' % (i, K['en'], K['th'], K['creature'].capitalize(), K['cls']),
               '- **Attach:** `refs/%02d_%s_gold.png` (picture 1) + `refs/00_STYLE_EXAMPLE_tan_ankylosaurus.png` (picture 2)' % (i, K['en'].lower()),
               '- **Who:** an 8-year-old %s. Normally wears %s.' % (K['he'], K['old']),
               '- **Keep:** %s; %s; %s; %s.' % (K['hair'], K['eyes'], K['skin'], K['face']),
               '- **Must read as a %s:** %s.' % (K['creature'], K['sil']),
               '- **Head:** ' + K['head'] + '.', '- **Body:** ' + K['body'] + '.', '- **Back:** ' + K['back'] + '.', '- **Weapon:** ' + K['weapon'] + '.', '- **Pose:** three-quarter view facing right, ' + K['pose'] + '.',
               '- **Palette (hex, dark / mid / light):**'] + ['  - %s: `%s`' % p for p in K['pal']] + \
              ['\n**Prompt (use word for word):**\n', '```', kid_prompt(K), '```\n',
               '<details><summary>Optional: 4 design options to choose from</summary>\n', '```', sheet_prompt(K), '```', '</details>\n']
    md += ['## 6. Checklist for each picture\n', CHECK,
           '\n## 7. After you finish\n', 'The owner sends the five PNG files to Claude, who turns them into the game\'s pixel sprites (`art/bb/dino_<class>.png`) and puts them in the game. Big, clean, white-background pictures convert best.\n']
    open(OUT + '/PROMPT.md', 'w', encoding='utf-8').write('\n'.join(md))
    open(OUT + '/README_TH.txt', 'w', encoding='utf-8').write(
        'ชุดคำสั่งเจนรูป "ฟอร์มดึกดำบรรพ์" สำหรับ Codex (หรือ AI เจนรูปตัวอื่น)\r\n\r\n'
        'ในโฟลเดอร์นี้มี\r\n'
        '- PROMPT.md = คำสั่งยาวแบบละเอียด (ภาษาอังกฤษ) อธิบายงานทั้งหมด สไตล์ กฎ และคำสั่งของแต่ละตัว\r\n'
        '- refs/ = รูปแนบ: 00 = รูปตัวอย่างแทนแอนคิโลซอรัส (สไตล์ที่ต้องการ) · 01-05 = ร่างทองของ นิล ฟ้า ราตรี จันทร์ หมอก (ไว้ให้หน้าเหมือนเดิม)\r\n'
        '- prompts/ = คำสั่งแยกทีละตัว ก๊อปไปวางได้เลย (มีแบบ 4 ตัวเลือกท้ายไฟล์ด้วย)\r\n\r\n'
        'วิธีใช้กับ Codex\r\n'
        '1. แตกไฟล์ zip แล้วแนบทั้งโฟลเดอร์ (หรือแนบ PROMPT.md + รูปทั้งหมดใน refs) ให้ Codex\r\n'
        '2. พิมพ์: Read PROMPT.md carefully and follow it. Generate the 5 pictures.\r\n'
        '3. ได้รูปแล้ว ส่งไฟล์ PNG ทั้งหมดมาให้ Claude ในแชต (ส่งเป็นไฟล์หรือ zip) Claude จะแปลงเป็นพิกเซลแล้วใส่เกมให้\r\n\r\n'
        'ถ้า Codex เจนรูปไม่ได้: เปิด ChatGPT แชตใหม่ทีละตัว แนบ 2 รูป (ร่างทองของตัวนั้น + รูป 00 ตัวอย่างแทน) แล้วก๊อปคำสั่งในไฟล์ prompts/ ของตัวนั้นไปวาง\r\n')
    z = 'docs/codex/dino_codex.zip'
    with zipfile.ZipFile(z, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, _, fs in os.walk(OUT):
            for f in sorted(fs):
                p = os.path.join(root, f); zf.write(p, os.path.join('dino_codex', os.path.relpath(p, OUT)))
    print('wrote', OUT, 'and', z, os.path.getsize(z), 'bytes')

if __name__ == '__main__':
    main()
