# Codex / image-AI package for the new cast (owner 2026-11-06: no more kids and animals, the whole game becomes legends:
# white..red = normal units, gold = HEROES, rainbow = GODS; chibi like the owner's Wukong picture).
# Output: docs/codex/legends/ (PROMPT.md, prompts/*.txt, refs/, README_TH.txt) + docs/codex/legends_codex.zip
# Run from the repo root: python3 tools/art/legends_codex.py <style picture>
import os, sys, shutil, zipfile
from PIL import Image

OUT = 'docs/codex/legends'
STYLE = sys.argv[1] if len(sys.argv) > 1 else None

C = [  # key, name, Thai, tier, class job, who, look, expression, head, body, back, weapon, pose, silhouette, palette
 ('hero_warrior', 'Lu Bu', 'ลิโป้', 'hero', 'warrior (heavy hitter, smashes groups)', 'the mightiest warrior of the Three Kingdoms, a young man',
  'long black hair flowing out of the helmet, sharp red-brown eyes', 'a fierce proud smirk',
  'a tall golden crown-helmet with two VERY long pheasant tail feathers (white with dark bands) sweeping up and back, a red tassel on top',
  'heavy dark crimson and black lamellar armour with gold trims, big shoulder guards, a gold tiger-face belt buckle, armoured boots',
  'a long red cape and red sash ends flowing behind him',
  'a huge halberd "Sky Piercer": a long red shaft, a spear tip with a crescent blade on each side, a red tassel under the blade, held in his fist',
  'a wide battle stance, the halberd held across his body ready to sweep', 'the two huge pheasant feathers and the crescent halberd',
  [('crimson', '#5e0f14 / #9a1c22 / #d63a3a'), ('black armour', '#16131a / #2c2632 / #4a4250'), ('gold', '#8a5a12 / #d8a22a / #ffe07a'), ('feathers', '#f2ead8 / #6a5040')]),
 ('hero_assassin', 'Hattori Hanzo', 'ฮัตโตริ ฮันโซ', 'hero', 'assassin (fast critical strikes)', 'the legendary ninja master of Iga, a young man',
  'short spiky dark hair, sharp steel-grey eyes', 'a cool confident half-smile',
  'a dark indigo ninja hood with a steel forehead plate engraved with a crest, the face mask pulled DOWN to the neck so the whole face shows',
  'fitted dark indigo ninja garb with dark steel arm guards and shin guards, a crimson sash belt, wrapped hands, split-toe boots',
  'a long crimson scarf flowing behind him',
  'two short straight blades (tanto) in a REVERSE GRIP: a small ring or guard on top of each fist, the blade coming out of the BOTTOM of the fist and pointing back along the forearm',
  'a low ready stance, one blade forward at chest height, the other held back by his hip', 'the ninja hood with the steel forehead plate and the flowing crimson scarf',
  [('indigo', '#141a33 / #232c55 / #3a4880'), ('steel', '#4a5060 / #8a92a6 / #d8dde8'), ('crimson', '#7a1018 / #c42a30 / #ff6a5a'), ('gold accents', '#c8962a / #ffd36a')]),
 ('hero_hunter', 'Robin Hood', 'โรบินฮู้ด', 'hero', 'archer (long range, piercing arrows)', 'the outlaw archer of Sherwood Forest, a young man',
  'messy auburn hair, bright green eyes', 'a cheeky confident grin',
  'a forest-green hooded cap with a long red feather tucked in it',
  'a brown leather jerkin over a green tunic, leather bracers with gold rims, a belt with pouches and a gold buckle, a quiver of arrows on his back, soft leather boots',
  'a short forest-green hooded cape with a ragged edge flowing behind him',
  'a tall yew longbow with green wraps on the grip, an arrow ready on the string, held in his front fist',
  'a confident stance, the bow held forward and slightly raised', 'the green feathered cap, the longbow and the quiver',
  [('forest green', '#173a1e / #2e6a32 / #5aa24e'), ('leather', '#3a2414 / #6e4628 / #a87448'), ('red feather', '#a01e1e / #e04a3a'), ('gold', '#b8862a / #ffd36a')]),
 ('hero_mage', 'Merlin', 'เมอร์ลิน', 'hero', 'mage (spells that hit areas)', 'the great wizard of King Arthur\'s court, a cheerful old man',
  'a long fluffy white beard, bushy white eyebrows, bright blue eyes', 'a wise knowing smile',
  'a tall floppy pointed wizard hat, deep blue with silver stars and crescent moons',
  'a deep blue wizard robe with silver star embroidery and a wide belt with a silver moon buckle, wide sleeves, curled pointed shoes',
  'a long midnight-blue cloak with silver edges flowing behind him',
  'a tall gnarled wooden staff topped with a big glowing cyan crystal held in its roots, gripped in his fist',
  'standing proudly, the staff planted beside him, the free hand raised with fingers open as if casting', 'the starry pointed hat, the long white beard and the crystal staff',
  [('royal blue', '#141c4a / #24357a / #3f5cbc'), ('silver', '#8a90a8 / #d6dbe8 / #ffffff'), ('beard', '#d8d6e0 / #ffffff'), ('crystal', '#1a9ab8 / #5ae0ff / #d6faff')]),
 ('hero_support', 'Zhuge Liang (Kongming)', 'ขงเบ้ง', 'hero', 'support (heals and buffs allies)', 'the genius strategist of the Three Kingdoms, a young man',
  'long straight black hair, calm dark eyes', 'a calm gentle smile',
  'a black scholar\'s cap (guan) tied with ribbons',
  'flowing white and sky-blue Han scholar robes with cloud patterns and gold trims, wide sleeves, a black sash with a jade pendant, cloth shoes',
  'long white robe tails and blue ribbons flowing behind him',
  'the iconic white crane-feather fan held up in his fist',
  'a relaxed elegant stance, the feather fan raised in front of him, the other hand behind his back', 'the white feather fan and the black scholar cap',
  [('white robe', '#c8ccd8 / #e8ecf4 / #ffffff'), ('sky blue', '#2a5a8a / #4a8ac8 / #9ad0ff'), ('black', '#141418 / #2a2a33'), ('gold and jade', '#c8962a / #ffd36a / #3aa87a')]),
 ('hero_curse', 'Cleopatra', 'คลีโอพัตรา', 'hero', 'curse caster (poison and weakening)', 'the last queen of ancient Egypt, a young woman',
  'a straight black bob with blunt bangs, bold kohl eyeliner, bright amber eyes', 'a mysterious confident smile',
  'a golden crown with a rearing cobra (uraeus) on the front and gold and lapis stripes',
  'a wide gold and lapis-blue collar (usekh), a white linen dress with a gold belt, gold arm cuffs and bracelets, gold sandals',
  'a long deep purple cape with gold edges flowing behind her',
  'a golden cobra scepter: a staff topped with a rearing cobra head with glowing emerald eyes, held in her fist',
  'an elegant regal stance, the cobra scepter held forward', 'the cobra crown, the black bob and the gold collar',
  [('gold', '#8a5a12 / #d8a22a / #ffe07a'), ('lapis blue', '#142a6a / #2a4aa8 / #5a82e0'), ('white linen', '#d8d2c0 / #f6f2e6'), ('purple and emerald', '#3a1650 / #6a2a8a / #2ad07a')]),
 ('god_warrior', 'Sun Wukong', 'ซุนหงอคง', 'god', 'warrior (heavy hitter, smashes groups)', 'the Monkey King, the Great Sage Equal to Heaven',
  'a monkey face with golden-brown fur, wild spiky golden-brown hair, fierce red eyes, round monkey ears', 'a fierce toothy grin',
  'a golden circlet with cloud swirls on his forehead (exactly like the style example)',
  'black and gold armour with a gold dragon shoulder guard, a red rope sash with white fur trim, black baggy trousers, black and gold boots',
  'long red scarves with gold cloud patterns flowing behind him, a curling monkey tail',
  'the Ruyi Jingu Bang: a red staff with ornate gold ends, resting on his shoulder in his fist',
  'a wide battle stance, the staff on his shoulder, the free hand open like a claw (same character as the example, now standing on the ground)', 'the golden circlet, the monkey tail and the red-and-gold staff',
  [('fur', '#6a3a1a / #a8642a / #e0a050'), ('red', '#7a1018 / #c42a30 / #ff6a5a'), ('black', '#16131a / #2c2632'), ('gold', '#8a5a12 / #d8a22a / #ffe07a')]),
 ('god_assassin', 'Loki', 'โลกิ', 'god', 'assassin (fast critical strikes)', 'the Norse trickster god born of fire, a young man',
  'wild flame-red hair, sly emerald-green eyes', 'a sly mischievous grin',
  'a black leather hood with a serpent-scale pattern pushed back so the flame-red hair spills out, a thin gold circlet shaped like a snake biting its tail on the forehead',
  'black and deep purple leather armour with gold serpent knotwork, a high collar, gold bracers shaped like coiled snakes, slim black boots; faint glowing emerald runes on the armour',
  'a long dark purple cape with a ragged edge and an emerald lining flowing behind him',
  'two curved daggers shaped like white serpent fangs with gold hilts, in a REVERSE GRIP: a ring on top of each fist, the blade coming out of the BOTTOM of the fist and curving back toward the body',
  'a low sly stance, one fang dagger forward, the other held back', 'the flame-red hair under the serpent hood and the fang daggers',
  [('black and purple', '#121216 / #2a1a3a / #4a2a6a'), ('flame hair', '#8a1a0a / #e0441a / #ffa040'), ('gold', '#8a5a12 / #d8a22a / #ffe07a'), ('emerald', '#0e5a3a / #1ab874 / #8affc8')]),
 ('god_hunter', 'Artemis', 'อาร์เทมิส', 'god', 'archer (long range, piercing arrows)', 'the Greek goddess of the hunt and the moon, a young woman',
  'long silver-white hair in a high ponytail, bright silver-blue eyes', 'a determined confident smile',
  'a silver crescent-moon tiara glowing softly on her forehead',
  'a short white Greek chiton with silver armour pieces (chest plate with a moon emblem, shoulder guard, bracers), a silver belt, laced silver sandals up the calves',
  'a light pale-blue cloak flowing behind her, a quiver of silver-fletched arrows on her back',
  'a silver bow shaped like a crescent moon with a glowing pale-blue string, an arrow ready, held in her front fist',
  'a poised hunter stance, the bow held forward', 'the crescent-moon tiara and the crescent-moon bow',
  [('silver', '#6a7088 / #b8c0d6 / #f2f6ff'), ('white', '#d6dae6 / #ffffff'), ('pale blue', '#3a6aa8 / #7ab0e8 / #c8e6ff'), ('moon gold', '#c8a24a / #ffe6a0')]),
 ('god_mage', 'Odin', 'โอดิน', 'god', 'mage (spells that hit areas)', 'the Allfather, king of the Norse gods, an old man',
  'a long braided white beard, an eye patch over his left eye, a bright blue right eye', 'a stern wise look',
  'a golden helmet with two white wings on the sides',
  'steel-blue armour with gold trims and Norse knotwork, a grey wolf-fur mantle over the shoulders, a wide belt with a gold buckle, fur-topped boots; two small black ravens perched on his shoulders',
  'a long steel-blue cloak flowing behind him',
  'the spear Gungnir: a long gold-and-steel spear with glowing blue runes along the blade, held in his fist',
  'a commanding stance, the spear held upright, the free hand raised with glowing runes floating close to the palm', 'the winged helmet, the eye patch, the ravens and the rune spear',
  [('steel blue', '#1a2a44 / #34507a / #6a8ab8'), ('grey fur', '#5a5a62 / #9a9aa6 / #d6d6de'), ('gold', '#8a5a12 / #d8a22a / #ffe07a'), ('rune glow', '#3ac8ff / #c8f2ff')]),
 ('god_support', 'Apollo', 'อพอลโล', 'god', 'support (heals and buffs allies)', 'the Greek god of the sun, music and healing, a young man',
  'curly golden-blond hair, warm golden eyes', 'a warm bright smile',
  'a golden laurel wreath',
  'a white toga-style chiton with gold sun embroidery, a gold chest plate with a sun disc emblem, gold arm cuffs, laced gold sandals',
  'a flowing orange-gold cape like sunset light',
  'a golden lyre with glowing strings held in one arm, the other hand plucking it',
  'a cheerful stance, the lyre held up in front of him', 'the laurel wreath, the sun emblem and the golden lyre',
  [('white', '#d6dae6 / #ffffff'), ('gold', '#8a5a12 / #d8a22a / #ffe07a'), ('sun orange', '#c8501a / #ff8a2a / #ffc86a'), ('hair', '#c8902a / #ffd060 / #fff0a8')]),
 ('god_curse', 'Anubis', 'อนูบิส', 'god', 'curse caster (poison and weakening)', 'the jackal-headed Egyptian god of the dead',
  'a black jackal head with tall pointed ears, glowing teal eyes', 'a calm stern look',
  'a gold and lapis striped headdress (nemes) behind the jackal ears',
  'a dark-skinned body with a wide gold and lapis collar, gold arm bands, a white linen kilt with a gold belt and an ankh hanging from it, gold sandals',
  'a long black cape with gold edges flowing behind him',
  'a was-sceptre: a tall dark staff topped with a stylised jackal head and forked at the bottom, held in his fist',
  'a solemn guardian stance, the sceptre planted beside him, the free hand raised with an open palm', 'the jackal head with tall ears and the striped headdress',
  [('black', '#0e0e14 / #22222c / #3a3a48'), ('gold', '#8a5a12 / #d8a22a / #ffe07a'), ('lapis', '#142a6a / #2a4aa8 / #5a82e0'), ('teal glow', '#1ac8b8 / #9affee')]),
]

STYLE_TXT = ('The attached picture is the STYLE EXAMPLE (a chibi Sun Wukong). Copy its art style exactly: chibi proportions with a big head (about 40-45% of the '
  'height), crisp clean pixel art on one even grid, a bold dark outline, rich clean shading, smooth tidy shapes with no noise, lots of fine gold ornament, cloth and '
  'scarves that flow with motion, a fierce expressive face with big bright eyes, plain white background.')

def prompt(c, wk=False):
    k, en, th, tier, job, who, look, face, head, body, back, weapon, pose, sil, pal = c
    tierline = ('GOLD tier = HERO: a legendary human, real armour and clothes, impressive but earthly.' if tier == 'hero' else
                'RAINBOW tier = GOD: divine and the most impressive of all, extra gold ornament and small glowing divine details that are PART of the costume (runes, moon, sun, eyes).')
    ex = ('This IS the character in the style example: keep his design, colours and staff exactly, only redraw him STANDING on the ground in a battle stance.' if wk else
          'Copy only the style of the example, NOT its monkey features, colours or staff.')
    return (STYLE_TXT + ' ' + ex + '\n\n'
        'Draw ' + en + ' (' + who + ') as a chibi pixel-art game character. Class: ' + job + '. ' + tierline + '\n\n'
        'Face: ' + look + ', ' + face + '. Both eyes bright and clearly visible' + (' (Odin\'s eye patch is the one exception)' if k == 'god_mage' else '') + ', no hair over the eyes.\n'
        'Head: ' + head + '.\nBody: ' + body + '.\nBack: ' + back + '.\nWeapon: ' + weapon + '.\n'
        'Pose: three-quarter view facing RIGHT, ' + pose + '. Both feet on the ground (the characters stand on tiles in the game), with the energy and flowing cloth of the example.\n'
        'Must read as ' + en + ' at a glance: ' + sil + '.\n'
        'Original design: do not copy any existing game, film, anime or comic version of ' + en + ' (for example no Marvel, Dragon Ball or Black Myth look).\n'
        'Colours (dark / mid / light): ' + '; '.join(n + ' ' + h for n, h in pal) + '.\n\n'
        'Square canvas, plain pure white background with nothing else, the character centred, full body from the top of the head gear to the feet, filling about 85-90% of the height. '
        'No aura or glow round the body, no effects, no sparkles, no ground, no shadow, no text, no watermark.')

# owner 2026-11-06: "เจนท่ายืดกระบองด้วย กระโดดยืดกระบองฟาด" = Wukong's attack: leap up, the staff grows long, smash down
WK_ATK = (STYLE_TXT + ' This IS the character in the style example: keep his design, colours and staff exactly.\n\n'
  'Draw Sun Wukong (the Monkey King) in his ATTACK pose, same chibi pixel art: he has leapt high into the air and holds the Ruyi Jingu Bang high over his head in both '
  'fists, ready to smash down to the right. The magic staff has GROWN very long (about three times its normal length), the red shaft with ornate gold ends stretching '
  'far up and forward, slightly curved by the swing. His knees are tucked, the red scarves and his tail whip up behind him, a fierce toothy shout on his face.\n'
  'Three-quarter view facing RIGHT. Original design: do not copy any existing game, film or anime version of Sun Wukong.\n\n'
  'Square canvas, plain pure white background with nothing else, the whole character and the whole staff inside the picture. No aura, no glow round the body, '
  'no speed lines, no effects, no ground, no shadow, no text.')
WK_ANIM = ('Use $game-character-sprites.\n'
  'Reference: the attached picture (Sun Wukong, the Monkey King, chibi pixel art). Keep the exact same character, face, outfit, colours and staff in every frame.\n'
  'Scope: cell 128x128 only. One direction only: east (facing right, the same view as the reference). Actions: idle (4 frames) and attack (6 frames). No walk, no other directions.\n'
  'Idle: standing battle stance with the staff on his shoulder, gentle breathing, the feet do not move.\n'
  'Attack, 6 frames:\n'
  '  1. standing battle stance with the staff on his shoulder\n'
  '  2. crouch low, gripping the staff in both fists\n'
  '  3. leap up high, the staff raised over his head\n'
  '  4. at the top of the jump the magic staff GROWS very long, stretching far up and forward\n'
  '  5. smash: he swings the long staff down to the ground in front of him (to the right) and lands\n'
  '  6. the staff shrinks back to normal and he returns to the standing stance\n'
  'Keep the whole body and the whole long staff inside the frame (the long staff may reach the frame edge in frames 4-5). Keep both feet on the same ground line in frames 1, 2, 5 and 6.\n'
  'No detached effects, no dust, no shadows, transparent background.\n'
  'When done, zip the whole run folder (including the full-size raw images in source/ and generated/, the clean sheets and the GIF previews) plus one large preview picture of both rows. Do not shrink anything.')

# owner 2026-11-06: "ท่ายืน ท่าที่ใช้ เอาดีๆ ตามสกิล ... เนียนๆ" = an animation set per character that acts out its skills (docs/legends-skills.html):
# idle 4 (a smooth loop), attack 6 (the normal hit), skill 6 (the ultimate). key, name, Thai, picture, idle, attack name, 6 steps, skill name, what it does, 6 steps
ANIM = [
 ('god_warrior', 'Sun Wukong', 'ซุนหงอคง', 'chibi Sun Wukong with the red-and-gold staff',
  'wide battle stance, the staff resting on his shoulder, gentle breathing, the tail curls and the scarves sway',
  'staff combo', ['battle stance, staff on the shoulder', 'swing the staff back behind him in both fists', 'a big horizontal sweep to the right, the body twisting', 'follow-through, the staff fully extended in front', 'twirl the staff once in front of him', 'back to the stance, staff on the shoulder'],
  'Cloud Somersault smash (ตีลังกาเมฆ)', 'leaps onto groups of demons and smashes them, the magic staff growing very long',
  ['battle stance, staff on the shoulder', 'crouch low gripping the staff in both fists', 'leap up high, the staff raised over his head', 'at the top of the jump the magic staff GROWS very long, stretching far up and forward', 'smash: he swings the long staff down to the ground in front of him and lands', 'the staff shrinks back to normal and he returns to the stance']),
 ('god_assassin', 'Loki', 'โลกิ', 'chibi Loki with flame-red hair, serpent hood and two fang daggers',
  'low sly stance, both fang daggers in a reverse grip, a sly grin, the cape and hair sway, he shifts his weight from foot to foot',
  'fang cross slash', ['sly stance, daggers in a reverse grip', 'crouch low, both daggers crossed in front of his chest', 'dash forward, the front foot stepping ahead', 'X slash: both fang daggers slash across in front of him, body stretched forward', 'follow-through, arms crossed past the body, cape flaring', 'hop back to the stance'],
  'King of Tricks (ราชันแห่งเล่ห์)', 'bewitches the strongest demons so they fight each other, then finishes the weak ones',
  ['sly stance', 'raises his free hand, the emerald runes on his armour glowing brighter', 'snaps his fingers with a wicked grin, his eyes glowing green', 'spins the fang daggers in his fingers (still in a reverse grip)', 'lunges forward and slashes down hard with both daggers', 'straightens up laughing and returns to the stance'],
  'Keep the reverse grip in every frame: a ring on top of each fist, the curved blade coming out of the bottom of the fist and curving back toward the body.'),
 ('god_hunter', 'Artemis', 'อาร์เทมิส', 'chibi Artemis with the silver crescent-moon bow',
  'poised hunter stance, the bow held forward, the ponytail and pale-blue cloak sway gently',
  'moon arrow', ['stance, bow forward, an arrow nocked', 'start drawing the string back', 'full draw: string at her cheek, aiming straight ahead', 'release: the string snaps forward, the arrow is gone, small recoil', 'follow-through, the bow arm still forward', 'reach back to the quiver for the next arrow and return to the stance'],
  'Night of the Hunt (ราตรีแห่งการล่า)', 'marks the five strongest demons with the moon and shoots giant moon arrows at them',
  ['stance', 'drop to one knee, pull THREE arrows from the quiver', 'nock all three arrows, the crescent tiara glowing brighter', 'full draw aiming high up and forward', 'release upward (the arrows are gone), the cloak whips back', 'stand up and return to the stance'],
  'Do not draw flying arrows: the game draws the shots itself.'),
 ('god_mage', 'Odin', 'โอดิน', 'chibi Odin with the rune spear Gungnir and two ravens',
  'commanding stance, the spear upright, the ravens shift on his shoulders, small blue runes float above his open palm, the fur and cloak sway',
  'rune cast', ['stance, spear upright, palm open', 'raise the free hand, the runes on the spear blade glow', 'thrust the open palm forward, casting', 'hold the cast, the beard and cloak blown back', 'lower the hand', 'back to the stance'],
  'Gungnir (หอกกุงเนียร์)', 'hurls the spear along the whole road, then freezes every demon in time',
  ['stance', 'lift the spear overhead into a throwing grip, the ravens take off from his shoulders', 'lean far back winding up, the runes along the blade blazing', 'throw: his arm whips forward and the spear leaves his hand (no spear in the hand now)', 'follow-through, the cloak flaring forward', 'the spear has flown back into his hand, the ravens land back on his shoulders'],
  'The small floating runes are part of his pose; no other effects.'),
 ('god_support', 'Apollo', 'อพอลโล', 'chibi Apollo with the golden lyre',
  'cheerful sway, gently plucking the lyre, the curly hair and orange cape bounce',
  'sun chord', ['stance, lyre in front', 'raise the lyre', 'strum hard with a big arm sweep, the strings glowing', 'lyre held forward, singing', 'hold, a happy grin', 'back to the stance'],
  'Sun Chariot (รถม้าสุริยะ)', 'makes every unit on the board twice as strong and sets all demons on fire',
  ['stance', 'lift the lyre high above his head in both hands', 'the sun emblem on his chest and the lyre glow brightly, the cape billows up', 'bring the lyre down and strum with a huge sweeping arm', 'arms spread wide, head back, singing joyfully', 'back to the stance']),
 ('god_curse', 'Anubis', 'อนูบิส', 'chibi Anubis with the was-sceptre and the ankh',
  'solemn guardian stance, the sceptre planted, the free hand slowly turning palm up, the cape sways',
  'sceptre curse', ['stance, sceptre planted', 'raise the sceptre', 'point the jackal head of the sceptre forward, his eyes glowing teal', 'thrust forward, casting', 'hold the cast', 'plant the sceptre back down, stance'],
  'Judgement of the Duat (พิพากษาแห่งดูอัต)', 'curses every rival gang and sends giant mummies to their houses',
  ['stance', 'lift the golden ankh from his belt in the free hand', 'hold the ankh high, the eye emblem and his eyes glowing teal', 'slam the forked end of the sceptre into the ground', 'hold, the cape flaring up behind him', 'back to the stance']),
 ('hero_warrior', 'Lu Bu', 'ลิโป้', 'chibi Lu Bu with the crescent halberd and two long pheasant feathers',
  'wide battle stance, the halberd held across his body in both fists, the long feathers and red cape sway, a fierce grin',
  'halberd sweep', ['battle stance, halberd across the body', 'raise the halberd back over his shoulder', 'a huge horizontal sweep to the right, the body twisting', 'follow-through, the crescent blade fully extended in front', 'pull the halberd back across the body', 'back to the stance'],
  'Break Ten Thousand Troops (ทะลวงหมื่นทัพ)', 'leaps onto three groups of demons in a row and stuns the whole field',
  ['battle stance', 'crouch low, the halberd held back', 'leap up high, the halberd raised over his head in both fists', 'at the top of the jump the feathers and cape whip up behind him', 'smash the halberd down to the ground in front of him and land', 'rise back into the stance']),
 ('hero_assassin', 'Hattori Hanzo', 'ฮัตโตริ ฮันโซ', 'chibi ninja Hattori Hanzo with two short blades in a reverse grip',
  'low ninja stance, both blades in a reverse grip, the red scarf and hood tail flutter, a slight bob',
  'twin slash', ['ninja stance', 'crouch low', 'dash forward, the front foot stepping ahead', 'double slash, both blades crossing in front of him', 'follow-through, the red scarf flaring', 'back to the stance'],
  'Shadow Clone Technique (คาถาแยกเงา)', 'slashes demons all over the field 40 times',
  ['ninja stance', 'bring the blades together in front of his chest and make a ninja hand sign', 'crouch very low, the scarf rising', 'lunge far forward, body stretched low', 'rising slash upward with both blades', 'land back in the stance'],
  'Keep the reverse grip in every frame: the blade comes out of the bottom of the fist and runs back along the forearm.'),
 ('hero_hunter', 'Robin Hood', 'โรบินฮู้ด', 'chibi Robin Hood with the longbow and the red-feathered cap',
  'confident archer stance, bow held ready, the red feather and green cape sway',
  'piercing arrow', ['stance, an arrow nocked', 'draw the string', 'full draw aiming straight ahead', 'release (the arrow is gone), a cheeky grin', 'follow-through', 'take a new arrow, back to the stance'],
  'Sherwood Arrow Rain (ฝนธนูเชอร์วูด)', 'rains 50 arrows over the whole field',
  ['stance', 'grab a handful of arrows from the quiver', 'nock several arrows at once, aiming high', 'full draw upward', 'release upward (the arrows are gone), laughing', 'back to the stance'],
  'Do not draw flying arrows: the game draws the shots itself.'),
 ('hero_mage', 'Merlin', 'เมอร์ลิน', 'chibi Merlin with the crystal staff',
  'wise stance, the staff planted, the free hand wiggling its fingers as if casting, the beard and cloak sway',
  'crystal bolt', ['stance', 'lift the staff, the crystal brightening', 'point the staff forward', 'hold the cast, the hat brim blown back', 'lower the staff', 'back to the stance'],
  'Meteor Shower (ฝนดาวตก)', 'calls 20 meteors down on the field',
  ['stance', 'raise the staff high overhead in both hands, the crystal blazing', 'look up, the robe and beard billowing in a magic wind', 'bring the staff down to point forward', 'hold, a proud grin', 'back to the stance']),
 ('hero_support', 'Zhuge Liang (Kongming)', 'ขงเบ้ง', 'chibi Kongming with the white feather fan',
  'calm elegant stance, slowly fanning himself with the feather fan, the ribbons and robe sway',
  'fan gust', ['stance, fan raised', 'draw the fan back', 'sweep the fan forward in a wide arc', 'follow-through, sleeves flowing', 'fan held forward', 'back to the stance'],
  'Battle of Red Cliffs (ศึกผาแดง)', 'sets every demon on the field on fire',
  ['stance', 'hold the fan high, eyes closed in focus', 'the robe and ribbons lift in a rising wind', 'eyes open, sweep the fan in a big horizontal arc', 'point the fan forward, commanding', 'back to the stance']),
 ('hero_curse', 'Cleopatra', 'คลีโอพัตรา', 'chibi Cleopatra with the golden cobra scepter',
  'regal stance, the cobra scepter held up, the free hand gesturing elegantly, the purple cape sways',
  'cobra curse', ['stance', 'raise the scepter, the cobra eyes glowing green', 'point the scepter forward, the free hand pushing', 'hold the cast', 'lower the scepter', 'back to the stance'],
  "Pharaoh's Curse (คำสาปฟาโรห์)", 'curses every rival gang and steals their gold',
  ['stance', 'raise the scepter high overhead in both hands', 'the cobra crown and the scepter eyes glow bright green, the cape lifts', 'slam the scepter base down to the ground', 'hold, a commanding smile, the free hand spread wide', 'back to the stance']),
]

# owner 2026-11-06: video AI (Meta AI) redraws faces, "เจนสกิลเอา เอฟเฟกต์ไม่น่าเพี้ยน" = use it for the skill EFFECTS instead:
# one short clip per ultimate on pure black (black turns see-through in the game: bright = glow), still camera, no characters
FX = [
 ('fx_god_warrior', 'ซุนหงอคง · ตีลังกาเมฆ', 'a giant golden staff smashing down from above into the ground: a burst of golden-red light, a ring shockwave of swirling Chinese auspicious clouds spreading out, glowing cracks, golden sparks'),
 ('fx_god_assassin', 'โลกิ · ราชันแห่งเล่ห์', 'emerald-green illusion magic: twisting green smoke with snake shapes coiling in a circle, glowing green runes flashing, then a sharp burst of green sparks'),
 ('fx_god_hunter', 'อาร์เทมิส · ราตรีแห่งการล่า', 'a silver crescent moon glowing above, then a shining silver moonlight arrow streaking down into the ground with a bright pale-blue starburst and falling star glitter'),
 ('fx_god_mage', 'โอดิน · หอกกุงเนียร์', 'a glowing blue rune circle on the ground, then a bolt of blue lightning shaped like a spear strikes its centre, with crackling blue electric arcs and flying rune symbols'),
 ('fx_god_support', 'อพอลโล · รถม้าสุริยะ', 'a radiant golden sun bursting open with long golden light rays spinning outward, warm orange flames curling around the rim, golden music-note sparkles floating up'),
 ('fx_god_curse', 'อนูบิส · พิพากษาแห่งดูอัต', 'a dark curse: a swirling vortex of purple-black smoke and golden sand, a glowing teal Eye of Horus symbol appearing in the middle, ghostly teal wisps rising'),
 ('fx_hero_warrior', 'ลิโป้ · ทะลวงหมื่นทัพ', 'a huge red crescent slash wave sweeping across from left to right, with crimson energy and golden sparks trailing behind it'),
 ('fx_hero_assassin', 'ฮันโซ · คาถาแยกเงา', 'a ninja smoke bomb: a puff of dark indigo smoke bursting outward, many fast white slash lines crossing through it, small silver shuriken spinning out'),
 ('fx_hero_hunter', 'โรบินฮู้ด · ฝนธนูเชอร์วูด', 'a burst of glowing green leaves and golden light where many arrows hit the ground at once, leaves spinning outward and drifting down'),
 ('fx_hero_mage', 'เมอร์ลิน · ฝนดาวตก', 'a blazing blue-white meteor falling from the top and exploding on the ground into a starry blast of blue and white sparkles and a shockwave ring'),
 ('fx_hero_support', 'ขงเบ้ง · ศึกผาแดง', 'a strong east wind carrying a wave of orange-red flames sweeping across from left to right, swirling fire and glowing embers'),
 ('fx_hero_curse', 'คลีโอพัตรา · คำสาปฟาโรห์', 'a golden cobra made of light rearing up and striking down, leaving a splash of glowing green poison and golden hieroglyph sparks'),
]
def fx_prompt(f):
    return ('A visual effect for a 2D pixel art game: ' + f[2] + '. '
        'Pure black background, the camera completely still, the effect centred in the frame, no characters, no ground, no scenery, no text. '
        'The effect starts small, bursts to full size, then fades out completely back to black by the end. Bright saturated glowing colours, '
        'crisp pixel art style with chunky pixels, smooth motion, about 2 seconds.')

def anim_prompt(a):
    k, en, th, desc, idle, an, asteps, sn, swhat, ssteps = a[:10]
    extra = a[10] if len(a) > 10 else ''
    st = lambda L: '\n'.join('  %d. %s' % (i + 1, x) for i, x in enumerate(L))
    return ('Use $game-character-sprites.\n'
        'Reference: the attached picture (' + desc + '). It is the final design: keep the exact same character, face, hair, outfit, colours, weapon and level of detail in every frame.\n'
        'Scope: ONE direction only: east (facing right, the same three-quarter view as the reference). Actions: idle (4 frames), attack (6 frames) and skill (6 frames). No walk, no other directions. Cell 128x128 for the clean sheets.\n\n'
        'Idle (4 frames, a smooth loop that ends where it starts): ' + idle + '.\n\n'
        'Attack (6 frames) - ' + an + ':\n' + st(asteps) + '\n\n'
        'Skill (6 frames) - ' + sn + ', the ultimate (in the game it ' + swhat + '):\n' + st(ssteps) + '\n\n'
        + (extra + '\n' if extra else '') +
        'Smooth animation: every frame is a small step from the one before; the same size, proportions and outline in every frame; both feet on the same ground line unless a step says jump; '
        'hair, cape and cloth follow through and settle.\n'
        'Keep the whole body, weapon and cape inside every frame. No detached effects (no flying projectiles, slash trails, magic bolts, sparks, dust or shadows): the game draws those. '
        'Parts of the costume or weapon that already glow may glow brighter. Transparent background.\n'
        'When done, zip the whole run folder including the full-size raw images in source/ and generated/, the clean sheets and the GIF previews, '
        'plus one large preview picture of all three rows. Do not shrink anything.')

def page(entries):
    """docs/legends-prompts.html: every prompt on one phone-friendly page with a copy button (owner: "ขอพรอมต์แบบจบตัว")"""
    import html
    cards = []
    for t, sub, txt in entries:
        cards.append('<section><h2>%s</h2><p class="sub">%s</p><pre>%s</pre><button type="button">คัดลอกคำสั่ง</button></section>' % (html.escape(t), sub, html.escape(txt)))
    return ('<!doctype html><html lang="th"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
      '<title>Legends Prompts</title><style>:root{--bg:#12131c;--card:#1c1e2b;--line:#2e3146;--txt:#ecebf5;--dim:#a6a8bf;--acc:#ffd36a}'
      '@media (prefers-color-scheme: light){:root:not([data-theme="dark"]){--bg:#f4f2ec;--card:#fff;--line:#ddd8cc;--txt:#1c1a24;--dim:#5e5a6e;--acc:#a8780a}}'
      'body{margin:0;background:var(--bg);color:var(--txt);font:16px/1.5 system-ui,"Noto Sans Thai",sans-serif}main{max-width:860px;margin:0 auto;padding:16px}'
      'h1{font-size:22px;margin:8px 0}h2{font-size:18px;margin:0 0 4px}.sub{color:var(--dim);margin:0 0 8px}section{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px;margin:12px 0}'
      'pre{white-space:pre-wrap;word-break:break-word;background:rgba(0,0,0,.18);border-radius:8px;padding:10px;font-size:13px;max-height:220px;overflow:auto}'
      'button{font:inherit;font-weight:700;padding:10px 16px;border-radius:8px;border:0;background:var(--acc);color:#1a1200;cursor:pointer;width:100%}button.ok{background:#5fd07a}'
      'img{max-width:180px;border-radius:8px;border:1px solid var(--line);background:#fff}a{color:var(--acc)}</style></head><body><main>'
      '<h1>🏛️ ตัวละครใหม่: วีรชน (ทอง) + เทพ (รุ้ง)</h1>'
      '<section><h2>วิธีใช้</h2><p class="sub">ChatGPT: แชตใหม่ทีละตัว แนบรูปตัวอย่างสไตล์ (กดค้างที่รูปแล้วบันทึก) แล้ววางคำสั่งของตัวนั้น · '
      'Codex ที่ต่อโปรเจกต์ไว้: พิมพ์ <code>Read docs/codex/legends/PROMPT.md and make all 12 pictures. Follow AGENTS.md.</code> · '
      '<a href="codex/legends_codex.zip" download>⬇ zip ทั้งชุด</a></p>'
      '<a href="codex/legends/refs/00_STYLE_wukong.png" download="style_wukong.png"><img src="codex/legends/refs/00_STYLE_wukong.png" alt="รูปตัวอย่างสไตล์ ซุนหงอคงจิบิ"></a>'
      '<p class="sub">⬆ รูปตัวอย่างสไตล์ (แนบทุกครั้ง)</p></section>' + ''.join(cards) +
      '<script>for(const b of document.querySelectorAll("section button")){b.onclick=async()=>{const t=b.previousElementSibling.textContent;'
      'try{await navigator.clipboard.writeText(t)}catch(e){const a=document.createElement("textarea");a.value=t;document.body.appendChild(a);a.select();document.execCommand("copy");a.remove()}'
      'b.textContent="คัดลอกแล้ว ✓";b.classList.add("ok");setTimeout(()=>{b.textContent="คัดลอกคำสั่ง";b.classList.remove("ok")},1600)}}</script></main></body></html>')

def main():
    if os.path.isdir(OUT): shutil.rmtree(OUT)
    os.makedirs(OUT + '/refs'); os.makedirs(OUT + '/prompts')
    if STYLE:
        im = Image.open(STYLE).convert('RGBA'); bg = Image.new('RGBA', im.size, (255, 255, 255, 255)); bg.alpha_composite(im)
        bg.convert('RGB').save(OUT + '/refs/00_STYLE_wukong.png', optimize=True)
    # the finished character pictures stay in art/incoming/legends/<key>.png (Codex attaches them from there; no copies, the repo stays small)
    for i, c in enumerate(C, 1):
        with open(OUT + '/prompts/%02d_%s.txt' % (i, c[0]), 'w', encoding='utf-8') as f:
            f.write('=== %s (%s) - %s ===\nAttach: refs/00_STYLE_wukong.png\nSave as: %s.png\n\n%s\n' % (c[1], c[2], 'HERO / gold' if c[3] == 'hero' else 'GOD / rainbow', c[0], prompt(c, c[0] == 'god_warrior')))
    md = ['# New cast: 6 heroes (gold) + 6 gods (rainbow), chibi pixel art\n',
          'The game drops the kids in animal costumes. New ladder per class: white..red = normal units, gold = HERO, rainbow = GOD.',
          'Style: `refs/00_STYLE_wukong.png` (the owner picked it). Attach it to EVERY picture.\n',
          '| File | Who | Tier | Class |', '|---|---|---|---|'] + ['| `%s.png` | %s (%s) | %s | %s |' % (c[0], c[1], c[2], 'hero (gold)' if c[3] == 'hero' else 'god (rainbow)', c[4].split(' (')[0]) for c in C]
    md += ['\n## How to work\n',
           '1. Look at `refs/00_STYLE_wukong.png` first: that is the quality and style for all twelve.',
           '2. Make the twelve pictures one at a time with the prompt below (word for word), always attaching the style picture.',
           '3. If the repository is attached: save them on a new branch `codex/legends` in `art/incoming/legends/` with a short `REPORT_TH.txt`, open a pull request, do not merge (see AGENTS.md). Otherwise zip them as `legends.zip`.',
           '4. Full size PNG, plain white background. Do not shrink or convert to a small pixel grid (Claude converts them for the game).\n',
           '## The twelve prompts\n']
    for i, c in enumerate(C, 1):
        md += ['### %d. %s (%s) -> `%s.png`\n' % (i, c[1], c[2], c[0]), '```', prompt(c, c[0] == 'god_warrior'), '```\n']
    md += ['## Extra: Sun Wukong attack (leap, the staff grows long, smash)\n',
           '### 13. Attack picture -> `god_warrior_attack.png` (attach the style picture)\n', '```', WK_ATK, '```\n',
           '### 14. Attack animation with $game-character-sprites (attach `god_warrior.png` once it is made, or the style picture)\n', '```', WK_ANIM, '```\n']
    open(OUT + '/PROMPT.md', 'w', encoding='utf-8').write('\n'.join(md))
    with open(OUT + '/prompts/13_god_warrior_attack.txt', 'w', encoding='utf-8') as f:
        f.write('=== Sun Wukong attack picture ===\nAttach: refs/00_STYLE_wukong.png\nSave as: god_warrior_attack.png\n\n' + WK_ATK + '\n')
    with open(OUT + '/prompts/14_god_warrior_anim.txt', 'w', encoding='utf-8') as f:
        f.write('=== Sun Wukong attack animation (Codex + $game-character-sprites) ===\nAttach: god_warrior.png (or refs/00_STYLE_wukong.png)\n\n' + WK_ANIM + '\n')
    ent = [('%d. %s · %s' % (i, c[2], c[1]), ('🥇 วีรชน ระดับทอง' if c[3] == 'hero' else '🌈 เทพ ระดับรุ้ง') + ' · คลาส ' + {'warrior':'นักรบ','assassin':'นักฆ่า','archer':'นักธนู','mage':'นักเวท','support':'ซัพพอร์ต','curse caster':'สาปแช่ง'}.get(c[4].split(' (')[0], c[4]) + ' · บันทึกเป็น ' + c[0] + '.png',
            prompt(c, c[0] == 'god_warrior')) for i, c in enumerate(C, 1)]
    ent += [('13. ซุนหงอคง ท่าโจมตี (รูปเดียว)', 'กระโดด ยืดกระบองยาว เตรียมฟาด · แนบรูปตัวอย่างสไตล์ · บันทึกเป็น god_warrior_attack.png', WK_ATK),
            ('14. ซุนหงอคง ภาพเคลื่อนไหว (Codex + สกิล)', 'ย่อ กระโดด กระบองยืด ฟาดลงพื้น กลับท่า · แนบรูปซุนหงอคงที่เจนเสร็จแล้ว', WK_ANIM)]
    md = open(OUT + '/PROMPT.md', encoding='utf-8').read().split('\n')
    md += ['## Animations: idle + attack + skill for every character (owner: acted out from the skills, smooth)\n']
    for i, a in enumerate(ANIM, 1):
        with open(OUT + '/prompts/anim_%02d_%s.txt' % (i, a[0]), 'w', encoding='utf-8') as f:
            f.write('=== %s (%s) animation ===\nAttach: art/incoming/legends/%s.png (the finished picture of this character)\n\n%s\n' % (a[1], a[2], a[0], anim_prompt(a)))
        md += ['### A%d. %s (%s) - attach `%s.png`\n' % (i, a[1], a[2], a[0]), '```', anim_prompt(a), '```\n']
        ent.append(('🎬 ท่า %d. %s · %s' % (i, a[2], a[1]), 'ยืน 4 · โจมตี 6 · สกิล "%s" 6 · แนบรูปของตัวนี้ (art/incoming/legends/%s.png)' % (a[7], a[0]), anim_prompt(a)))
    open(OUT + '/PROMPT.md', 'w', encoding='utf-8').write('\n'.join(md))
    md = open(OUT + '/PROMPT.md', encoding='utf-8').read().split('\n')
    md += ['## Skill effects for a video AI (Meta AI etc.): pure black background, still camera\n']
    for i, f in enumerate(FX, 1):
        with open(OUT + '/prompts/fx_%02d_%s.txt' % (i, f[0]), 'w', encoding='utf-8') as fo:
            fo.write('=== %s ===\nSave as: %s.mp4 (download the video file, do not screenshot)\n\n%s\n' % (f[1], f[0], fx_prompt(f)))
        md += ['### FX%d. %s -> `%s.mp4`\n' % (i, f[1], f[0]), '```', fx_prompt(f), '```\n']
        ent.append(('✨ เอฟเฟกต์ %d. %s' % (i, f[1]), 'ใช้ Meta AI หรือเว็บทำวิดีโออื่น ไม่ต้องแนบรูป · ได้แล้วดาวน์โหลด mp4 ส่งมาเป็นไฟล์', fx_prompt(f)))
    open(OUT + '/PROMPT.md', 'w', encoding='utf-8').write('\n'.join(md))
    open('docs/legends-prompts.html', 'w', encoding='utf-8').write(page(ent))
    open(OUT + '/README_TH.txt', 'w', encoding='utf-8').write(
        'ตัวละครชุดใหม่: วีรชน 6 (ระดับทอง) + เทพ 6 (ระดับรุ้ง) แบบจิบิ ตามรูปซุนหงอคงที่เลือก\r\n\r\n'
        'วีรชน: ลิโป้ (นักรบ) ฮัตโตริ ฮันโซ (นักฆ่า) โรบินฮู้ด (นักธนู) เมอร์ลิน (นักเวท) ขงเบ้ง (ซัพพอร์ต) คลีโอพัตรา (สาปแช่ง)\r\n'
        'เทพ: ซุนหงอคง (นักรบ) โลกิ (นักฆ่า) อาร์เทมิส (นักธนู) โอดิน (นักเวท) อพอลโล (ซัพพอร์ต) อนูบิส (สาปแช่ง)\r\n\r\n'
        'ใช้กับ Codex: แนบโฟลเดอร์นี้ (หรือถ้าต่อโปรเจกต์ไว้แล้ว ไม่ต้องแนบ) แล้วพิมพ์\r\n'
        '   Read docs/codex/legends/PROMPT.md and make all 12 pictures. Follow AGENTS.md.\r\n'
        'ใช้กับ ChatGPT ทีละรูป: แนบ refs/00_STYLE_wukong.png แล้ววางคำสั่งในโฟลเดอร์ prompts ของตัวนั้น\r\n'
        'ได้รูปแล้วส่งให้ Claude (หรือบอกว่า Codex ทำเสร็จแล้ว) Claude แปลงเป็นพิกเซลแล้วใส่เกมให้\r\n')
    z = 'docs/codex/legends_codex.zip'
    with zipfile.ZipFile(z, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, _, fs in os.walk(OUT):
            for f in sorted(fs):
                p = os.path.join(root, f); zf.write(p, os.path.join('legends', os.path.relpath(p, OUT)))
    print('wrote', OUT, z, os.path.getsize(z))

if __name__ == '__main__':
    main()
