# Monsters for the action game (`action.html`) — brief for Codex

The owner (Thai, not a programmer) wants a whole set of monsters for the top-down action game. Make ONE picture per
monster, in the order of the queue below. Reply to the owner in Thai, short and plain.

## How to deliver (rules from AGENTS.md)
- Work on a new branch `codex/mobs` and open a pull request. Never push to `main`, never merge.
- Save each picture as `art/incoming/mobs/<key>.png`, full size as generated (do not shrink, do not convert to a pixel grid).
- Add `art/incoming/mobs/REPORT_TH.txt`: one line per file in Thai (which monster, anything that came out wrong).
- Mark finished rows `done` in the queue below in the same pull request. If you cannot finish all of them in one run,
  stop after any finished picture; next time the owner says "ทำมอนต่อ", continue with the first `todo` row.
- Each picture is its OWN generation with the style picture attached. Never put several monsters in one picture.

## Style picture
Attach `docs/codex/action/refs/00_STYLE_hero.png` (the swordsman hero) to every generation and match its style exactly:
chibi pixel art, big head, thick dark outline, few flat colours with one shade step, bright colours, plain white
background, front / side / back views in one row.

## Shared prompt (put this first, then the monster's own lines)
```
Pixel art game character turnaround sheet in the SAME style as the attached picture (chibi pixel art, big head, thick
dark outline, few flat colours with one shade step, bright colours).
Show 3 full-body views of ONE monster in one row on a plain pure white background:
1) front view facing the viewer, 2) true side view facing RIGHT (pure profile), 3) back view.
Same size in all three views, feet (or the lowest point) on the same ground line, evenly spaced, nothing touching or
crossing into the next view, the whole body inside the picture.
Picture size 1536x1024 landscape; the tallest view fills about 85% of the picture height.
Neutral ready pose (not attacking), any weapon held the same way in every view. No shadow, no ground, no text, no
labels, no frame, no particles or glow outside the body.
Original design: do not copy any existing game, anime, film or comic monster.
```

## Queue
| # | key | status | map | size in game (Claude scales it) |
|---|-----|--------|-----|--------------|
| 1 | shroom | done | forest | small |
| 2 | wolf | done | forest | medium |
| 3 | goblin_archer | done | forest | small |
| 4 | boar_guard | done | forest | large |
| 5 | skeleton | done | ruins | medium |
| 6 | wisp | done | ruins | small |
| 7 | golem | done | ruins | large |
| 8 | boss_treant | done | forest boss | huge |
| 9 | krahang | done | Thai city | medium |
| 10 | khamot | done | Thai village | small |
| 11 | phrai | done | Thai river | medium |
| 12 | pret | done | Thai city | large |
| 13 | monkey | done | Thai city | small |
| 14 | croc_guard | done | Thai river | large |
| 15 | boss_chalawan | done | Thai boss | huge |
| 16 | jiangshi | done | China | medium |
| 17 | paper_doll | done | China | small |
| 18 | terracotta_archer | done | China | medium |
| 19 | terracotta_general | done | China | large |
| 20 | fox_spirit | done | China | medium |
| 21 | toad_demon | done | China | large |
| 22 | boss_nian | done | China boss | huge |
| 23 | kappa | done | Japan | small |
| 24 | kasa_obake | done | Japan | small |
| 25 | oni | done | Japan | large |
| 26 | tengu | done | Japan | medium |
| 27 | rokurokubi | done | Japan | medium |
| 28 | nekomata | done | Japan | medium |
| 29 | boss_orochi | done | Japan boss | huge |
| 30 | mummy | done | Egypt | medium |
| 31 | scarab | done | Egypt | small |
| 32 | jackal_warrior | done | Egypt | medium |
| 33 | sand_scorpion | done | Egypt | large |
| 34 | cobra_priest | done | Egypt | medium |
| 35 | sand_golem | done | Egypt | large |
| 36 | boss_sphinx | done | Egypt boss | huge |
| 37 | draugr | done | Norse | medium |
| 38 | frost_wolf | done | Norse | medium |
| 39 | troll | done | Norse | large |
| 40 | ice_wraith | done | Norse | small |
| 41 | dwarf_berserker | done | Norse | small |
| 42 | ice_golem | done | Norse | large |
| 43 | boss_jotun | done | Norse boss | huge |
| 44 | dokkaebi_fire | done | Korea | small |
| 45 | dokkaebi | done | Korea | medium |
| 46 | gwisin | todo | Korea | medium |
| 47 | haetae | todo | Korea | medium |
| 48 | jangsan_tiger | todo | Korea | large |
| 49 | jeoseung_saja | todo | Korea | medium |
| 50 | boss_bulgasari | todo | Korea boss | huge |
| 51 | satyr | todo | Greece | medium |
| 52 | harpy | todo | Greece | medium |
| 53 | spartoi | todo | Greece | medium |
| 54 | gorgon | todo | Greece | medium |
| 55 | cyclops | todo | Greece | large |
| 56 | minotaur | todo | Greece | large |
| 57 | boss_chimera | todo | Greece boss | huge |
| 58 | domovoi | todo | Slavic | small |
| 59 | kikimora | todo | Slavic | small |
| 60 | rusalka | todo | Slavic | medium |
| 61 | vukodlak | todo | Slavic | medium |
| 62 | vodyanoy | todo | Slavic | medium |
| 63 | leshy | todo | Slavic | large |
| 64 | boss_izba | todo | Slavic boss | huge |
| 65 | knocker | todo | Celtic | small |
| 66 | redcap | todo | Celtic | small |
| 67 | pooka | todo | Celtic | medium |
| 68 | banshee | todo | Celtic | medium |
| 69 | kelpie | todo | Celtic | medium |
| 70 | spriggan | todo | Celtic | large |
| 71 | boss_wyrm | todo | Celtic boss | huge |
| 72 | babi_ngepet | todo | Southeast Asia | small |
| 73 | orang_minyak | todo | Southeast Asia | medium |
| 74 | pocong | todo | Southeast Asia | medium |
| 75 | pontianak | todo | Southeast Asia | medium |
| 76 | tikbalang | todo | Southeast Asia | large |
| 77 | kapre | todo | Southeast Asia | large |
| 78 | boss_bakunawa | todo | Southeast Asia boss | huge |

## Monster lines (add after the shared prompt)

**1 shroom** (เห็ดพิษ)
```
Monster: a small grumpy walking mushroom. Big purple cap with pale yellow spots, a stubby cream stem body with two short
legs and tiny arms, angry little eyes under the cap rim, a few spores drifting from the cap. Cute but mean.
```
**2 wolf** (หมาป่าเงา)
```
Monster: a shadow wolf on four legs. Dark grey-blue fur with a lighter belly, glowing amber eyes, one torn ear, scars,
a smoky dark tail tip, bared fangs. Lean and fast-looking. In the side view we see its whole body in profile.
```
**3 goblin_archer** (ก็อบลินนักธนู)
```
Monster: a small goblin archer. Green skin, long pointy ears, a sly grin with one tooth, a hood made of big leaves,
a patched brown tunic, a short wooden bow in the left hand, a quiver of crude arrows on the back. Arrows point the right
way: the arrowhead at the front, the feathers at the back.
```
**4 boar_guard** (นักรบหมูป่า)
```
Monster: a big stocky boar-headed warrior standing on two legs. Brown bristly fur, two curved tusks, small fierce eyes,
a fur vest and leather belt, a round wooden shield with an iron rim on the left arm, a heavy spiked wooden club in the
right hand. Bulky and slow-looking.
```
**5 skeleton** (ทหารโครงกระดูก)
```
Monster: a skeleton soldier from old ruins. Ivory bones, glowing blue eye lights, a rusty dented helmet, a tattered red
cloth tied at the waist, a cracked round shield on the left arm, a chipped short sword in the right hand.
```
**6 wisp** (ภูตตะเกียง)
```
Monster: a small floating spirit with no legs. A dark hooded little cloak whose bottom fades into ragged wisps, two
glowing white eyes inside the hood, holding an old iron lantern with a blue flame. It floats a little above the ground
line.
```
**7 golem** (โกเลมหิน)
```
Monster: a big chunky golem made of mossy ruin stones. A square stone body and head, huge stone fists, short thick legs,
green moss and small vines on the shoulders, a glowing teal rune carved in the chest and two teal eye slits.
```
**8 boss_treant** (บอส ต้นไม้อสูร)
```
Monster: a huge ancient tree giant, the forest boss. A dark twisted bark body, a face in the bark with glowing purple
eyes and a jagged mouth, glowing purple cracks, two long branch arms ending in thorny claws, thick roots as feet, a crown
of dead branches with a few leaves, small mushrooms growing on the shoulders. Menacing but still chibi.
```
**9 krahang** (ผีกระหัง)
```
Monster: a Thai folklore flying ghost. A thin wild-haired man-ghost with grey-green skin and glowing eyes, wearing only a
dark loincloth, flying with two round woven bamboo rice-winnowing baskets strapped to his arms as wings, sitting astride
a long wooden rice pestle like a broom. Funny and creepy, not gory.
```
**10 khamot** (ผีโขมด)
```
Monster: a Thai swamp ghost-light. A floating ball of pale green fire with a faint grinning skull-like face inside the
flame, a short flame tail behind it, no body. It floats above the ground line.
```
**11 phrai** (พรายน้ำ)
```
Monster: a Thai river water spirit. A pale ghost woman with very long dripping black hair, glowing cyan eyes, an old
faded Thai wrap skirt and shoulder cloth, water weeds tangled in the hair, bare feet in a small splash of water.
Spooky but not gory, chibi.
```
**12 pret** (เปรต)
```
Monster: a Thai hungry ghost (pret). Extremely tall and thin, grey skin, a long thin neck, a tiny pinhole mouth, sunken
glowing eyes, very long thin arms and fingers, sparse hair, ragged grey cloth. Eerie, not gory.
```
**13 monkey** (ลิงโจร)
```
Monster: a mischievous macaque bandit. Brown-grey fur, a cheeky grin, a stolen red headcloth tied on the head, a small
cloth bag of stones and fruit on the hip, one fruit held ready to throw in the right hand. Standing on two legs.
```
**14 croc_guard** (ทหารจระเข้)
```
Monster: a crocodile-headed warrior standing on two legs. Olive-green scales, yellow eyes, rows of teeth, old Thai
soldier gear: a bronze-coloured chest plate and arm guards, a red waist sash, a long Thai glaive (a curved blade on a
long pole) held upright in the right hand.
```
**15 boss_chalawan** (บอส ชาละวัน)
```
Monster: Chalawan, the crocodile king from a Thai folk tale, the Thai map boss. A huge crocodile standing upright,
jade-green scales with a pale belly, glowing gold eyes, a tall pointed gold Thai-style crown, gold armlets and a jewelled
collar, a red and gold royal sash, a big curved Thai sword in the right hand, a long heavy tail. Proud and menacing,
still chibi.
```

### China set (owner 2026-11-09: monsters go by country, "ต่อไปเป็นจีน"; Chinese folklore, no worshipped gods)

**16 jiangshi** (ผีกระโดดจีน)
```
Monster: a Chinese hopping vampire (jiangshi). Pale grey-green skin, a stiff body, arms stretched straight out in front,
an old Qing-dynasty official's robe in dark blue with a square embroidered badge on the chest, a round official's hat,
a yellow paper talisman with red brush marks stuck on the forehead hanging over the face, long fingernails. Creepy but cute.
```
**17 paper_doll** (ตุ๊กตากระดาษ)
```
Monster: a small paper effigy servant come alive. A flat figure made of folded white and red paper with painted pink
cheeks, a painted smile and black painted hair buns, paper sleeves that flutter, a little paper fan in the right hand,
thin paper legs. Light and eerie, not gory.
```
**18 terracotta_archer** (ทหารดินเผานักธนู)
```
Monster: an animated clay soldier archer. Body of reddish-brown terracotta with cracks and chipped edges, a topknot,
layered clay armour plates, a wooden crossbow held in both hands, a quiver of bolts on the hip, small glowing amber
eyes. The crossbow bolts point the right way: the head at the front.
```
**19 terracotta_general** (นายพลดินเผา)
```
Monster: a big animated clay general. Bulky reddish-brown terracotta body with cracks, a tall general's headdress,
heavy layered clay scale armour with bronze-green studs, a long bronze halberd (a spear with a side blade) held
upright in the right hand, glowing amber eyes, a stern face. Heavy and slow-looking.
```
**20 fox_spirit** (ปีศาจจิ้งจอก)
```
Monster: a sly fox demon standing on its hind legs. White fur with pale gold tips, three big fluffy tails, narrow
glowing violet eyes, a red tassel charm hanging from its neck, small floating blue fox-fire flames by its paws. An
animal, not a human woman. Elegant and tricky.
```
**21 toad_demon** (ปีศาจคางคก)
```
Monster: a fat toad demon standing on two short legs. Warty olive-green skin with a yellow belly, big bulging orange
eyes, a huge wide mouth with a long sticky tongue curled inside, a torn brown cloth vest, a small wooden club in one
hand. Bulky and gross-cute, not scary.
```
**22 boss_nian** (บอส เหนียนโซ่ว)
```
Monster: Nian, the New Year beast from Chinese folklore, the China map boss. A huge lion-like beast standing on four
legs with a big round head, a single curved horn, a wide toothy mouth, bulging eyes, a thick red and gold mane, a red
scaly back with gold spikes, a fluffy tail, firecracker-red colours. Fierce but still chibi, like a festival beast.
```

### Japan set (owner 2026-11-09: one set per country map; folklore only)

**23 kappa** (กัปปะ)
```
Monster: a small river kappa: green scaly skin, a turtle shell on its back, a water-filled dish on top of its head with a ring of shaggy hair, a beak-like mouth, webbed hands and feet, a cheeky grin.
```
**24 kasa_obake** (ร่มผี)
```
Monster: a haunted paper umbrella yokai: a red and white oiled-paper umbrella with one big eye and a long lolling tongue, hopping on a single wooden leg with a sandal.
```
**25 oni** (ยักษ์โอนิ)
```
Monster: a big red oni ogre: red skin, two short horns, wild black hair, tusks, a tiger-skin loincloth, a heavy iron kanabo club studded with spikes held in both hands.
```
**26 tengu** (นกเทงงู)
```
Monster: a crow tengu: a black crow head with a sharp beak, black feathered wings folded on the back, a small black cap, mountain-monk robes, holding a feathered fan in the left hand and a short straight sword in the right.
```
**27 rokurokubi** (ผีคอยาว)
```
Monster: a long-necked rokurokubi ghost woman: a pale face with long black hair in an old-fashioned bun, a faded kimono, her neck stretched long and curling like a snake so the head floats above her body; eerie, not gory.
```
**28 nekomata** (แมวสองหาง)
```
Monster: a nekomata cat demon on its hind legs: a big black and white cat with two long tails, glowing yellow eyes, sharp claws, a red ribbon collar with a little bell, blue ghost flames floating by its tails.
```
**29 boss_orochi** (บอสยามาตะโนะโอโรจิ)
```
Monster: the boss: a giant eight-headed serpent from Japanese folklore, many long scaly necks rising from one huge coiled body, deep red and dark green scales, glowing red eyes, fangs, mossy rocks on its back; menacing but still chibi and readable.
```

### Egypt set (owner 2026-11-09: one set per country map; folklore only)

**30 mummy** (มัมมี่)
```
Monster: a shambling mummy: grey-beige bandages wrapped all over, loose ends trailing, glowing green eyes in the dark gaps, arms stretched forward.
```
**31 scarab** (ด้วงสการับ)
```
Monster: a big glossy scarab beetle: shiny dark blue-green shell with a gold sheen, six legs, small mandibles, a little gold sun disc pattern on the shell.
```
**32 jackal_warrior** (นักรบหัวหมาจิ้งจอก)
```
Monster: a jackal-headed warrior (a soldier, not a god): a black jackal head with tall ears, a gold and blue striped headcloth, a bronze chest plate, a white kilt, a curved khopesh sword and a small round shield.
```
**33 sand_scorpion** (แมงป่องทะเลทราย)
```
Monster: a big desert scorpion: sandy yellow armoured body, two big pincers, a curled tail with a glowing purple stinger, small black eyes.
```
**34 cobra_priest** (นักบวชงูเห่า)
```
Monster: a cobra-hooded serpent priest: a snake body standing upright with a wide cobra hood, gold and turquoise collar, holding a crooked staff with a glowing green gem.
```
**35 sand_golem** (โกเลมทราย)
```
Monster: a big golem made of packed desert sand and sandstone blocks, carved hieroglyph patterns on its chest glowing amber, sand trickling from its joints.
```
**36 boss_sphinx** (บอสสฟิงซ์)
```
Monster: the boss: a great stone sphinx come alive, a lion body of sandstone with a striped blue and gold royal headdress, glowing amber eyes, cracked stone, sand pouring from the cracks; still chibi.
```

### Norse set (owner 2026-11-09: one set per country map; folklore only)

**37 draugr** (ดรากร์)
```
Monster: a draugr: an undead Viking warrior with frost-blue skin, glowing ice-blue eyes, a rusty horned-free iron helmet, a torn fur cloak, a notched axe and a round wooden shield.
```
**38 frost_wolf** (หมาป่าหิมะ)
```
Monster: a frost wolf: thick white and pale blue fur, icicles along its back, glowing ice-blue eyes, frosty breath.
```
**39 troll** (โทรลล์)
```
Monster: a big mountain troll: grey-green warty skin, a huge nose, small eyes, moss and pebbles on its shoulders, a tree-trunk club, a ragged hide loincloth.
```
**40 ice_wraith** (วิญญาณน้ำแข็ง)
```
Monster: a floating ice wraith: a ragged pale blue hooded cloak with no legs, a dark hood with two white glowing eyes, long icy claws, snowflakes swirling round it.
```
**41 dwarf_berserker** (คนแคระคลั่ง)
```
Monster: a wild dwarf berserker: a big braided red beard, a bear-skin hood, bare arms with blue war paint, a double-bladed axe in each hand.
```
**42 ice_golem** (โกเลมน้ำแข็ง)
```
Monster: a big golem of blue glacier ice and black rock, frost mist rising from it, a glowing cold-blue core in its chest.
```
**43 boss_jotun** (บอสยักษ์น้ำแข็ง)
```
Monster: the boss: a frost giant from Norse legend (a giant, not a god): ice-blue skin, a long white beard with icicles, a crown of jagged ice, heavy furs and iron armour, a huge ice-crystal hammer.
```

### Korea set (owner 2026-11-10 "อย่าให้ codex ว่าง": next country sets; Korean folklore only)

**44 dokkaebi_fire** (ไฟผีโดกเกบี)
```
Monster: a small floating will-o-wisp of blue-green goblin fire with a cheeky grinning face in the flame and two tiny flame horns.
```
**45 dokkaebi** (โดกเกบี)
```
Monster: a stocky Korean goblin: red skin, one short horn, wild black hair, a grin with tusks, a tiger-pelt loincloth, a big spiked wooden club.
```
**46 gwisin** (ผีสาวเกาหลี)
```
Monster: a pale ghost woman in a long white hanbok, very long straight black hair hiding most of her face, floating a little above the ground, bare pale hands.
```
**47 haetae** (แฮแท)
```
Monster: a stone guardian lion-dog statue come alive: grey stone body with a curly stone mane, one small horn, glowing amber eyes, cracks with moss.
```
**48 jangsan_tiger** (เสือภูเขาขาว)
```
Monster: a big white mountain tiger with black stripes, glowing pale eyes, mist curling off its fur.
```
**49 jeoseung_saja** (ยมทูตเกาหลี)
```
Monster: a grim reaper messenger: a tall black gat hat, a long black robe, a pale face, holding a scroll of names and a black iron chain.
```
**50 boss_bulgasari** (บอสบุลกาซารี)
```
Monster: the boss: a huge iron-eating beast: a bear-like body covered in overlapping iron and bronze plates, a bull head with iron horns, molten glowing seams, iron spikes along its back.
```

### Greece set (Greek myth creatures only (no gods))

**51 satyr** (ซาเทียร์)
```
Monster: a goat-legged satyr: goat horns, curly hair, a pointed beard, hairy goat legs with hooves, a reed pan-flute and a short wooden club.
```
**52 harpy** (ฮาร์ปี้)
```
Monster: a harpy: a wild-haired woman upper body with big grey-brown wings for arms, bird legs with sharp talons, a screeching face.
```
**53 spartoi** (ทหารกระดูกกรีก)
```
Monster: a skeleton hoplite: a bronze Corinthian helmet with a red crest, a round bronze shield, a spear, a torn red cloak over bones.
```
**54 gorgon** (กอร์กอน)
```
Monster: a gorgon: a woman with a green scaly snake tail instead of legs, hair of hissing green snakes, glowing yellow eyes, a bronze bow.
```
**55 cyclops** (ไซคลอปส์)
```
Monster: a big one-eyed giant: one huge eye, a bald head, a leather loincloth, a big stone club, bulky arms.
```
**56 minotaur** (มิโนทอร์)
```
Monster: a bull-headed minotaur: brown fur, big curved horns, a nose ring, a bronze armour skirt, a huge double-bladed bronze axe.
```
**57 boss_chimera** (บอสคิเมร่า)
```
Monster: the boss: a chimera: a lion body and mane, a goat head growing from its back, a snake for a tail, fire glowing in the lion mouth.
```

### Slavic set (Slavic folklore only)

**58 domovoi** (โดโมวอย)
```
Monster: a tiny shaggy house spirit: a little old man covered in grey-brown hair, a long beard to his feet, glowing eyes, a wooden spoon as a weapon.
```
**59 kikimora** (คิคิโมรา)
```
Monster: a skinny swamp hag spirit: long thin limbs, a bird-like beak nose, messy hair with reeds, a ragged dark dress, long spindly fingers.
```
**60 rusalka** (รูซาลก้า)
```
Monster: a drowned water maiden: pale blue-green skin, very long wet green hair with water lilies, a torn white dress dripping water, floating.
```
**61 vukodlak** (วูคอดลัก)
```
Monster: a Slavic werewolf: a hunched wolf-man with dark grey fur, red eyes, a torn peasant shirt and belt, long claws.
```
**62 vodyanoy** (โวเดียนอย)
```
Monster: a big frog-faced water spirit: green slimy skin, a long green beard of weed, webbed hands, fish scales, a crown of reeds.
```
**63 leshy** (เลชี)
```
Monster: a forest guardian: a tall figure of bark and moss, antler-like branches on its head, glowing green eyes, leaves for hair.
```
**64 boss_izba** (บอสบ้านขาไก่)
```
Monster: the boss: a living wooden hut walking on two giant chicken legs: log walls, a thatched roof, glowing windows like eyes, a door like a mouth, smoke from its chimney.
```

### Celtic set (Celtic / British Isles folklore only)

**65 knocker** (น็อคเกอร์)
```
Monster: a small mine goblin: a miner's helmet with a candle, a big nose, a soot-black face, a pickaxe, a lantern.
```
**66 redcap** (เรดแคป)
```
Monster: a vicious little goblin: a pointed red cap, iron boots, long sharp teeth, a rusty scythe-like pike.
```
**67 pooka** (พูก้า)
```
Monster: a shape-shifting black goat-hare spirit: black shaggy fur, long rabbit ears, small goat horns, glowing gold eyes, standing on hind legs.
```
**68 banshee** (แบนชี)
```
Monster: a wailing ghost woman: a grey hooded cloak, long white hair streaming upward, a pale open-mouthed face, floating, ghostly mist.
```
**69 kelpie** (เคลปี)
```
Monster: a water horse: a black horse made of dark lake water and weed, a dripping mane of green seaweed, glowing teal eyes.
```
**70 spriggan** (สปริกแกน)
```
Monster: a big stone-and-root guardian: a body of mossy rocks bound with roots, a small head with glowing eyes, huge stone fists.
```
**71 boss_wyrm** (บอสไวร์ม)
```
Monster: the boss: a huge wingless wyrm dragon: a long green-scaled serpent body, a horned head, small clawed front legs, a mossy back with stones.
```

### Southeast Asia set (Indonesian / Malay / Filipino folklore only)

**72 babi_ngepet** (หมูผีบาบีเงเปต)
```
Monster: a black demon boar: black bristly fur, red glowing eyes, a little bag of stolen coins tied to its neck.
```
**73 orang_minyak** (ผีน้ำมัน)
```
Monster: a "oily man" ghost: a shiny pitch-black slick body dripping black oil, white glowing eyes, long fingers.
```
**74 pocong** (โปจง)
```
Monster: a shroud ghost: a body wrapped tight in a white burial shroud tied at the head and feet, a pale grey face, hopping.
```
**75 pontianak** (ปอนเตียนัค)
```
Monster: a pale vampire ghost woman: a long white dress, very long black hair, long red nails, red eyes, floating.
```
**76 tikbalang** (ติกบาลัง)
```
Monster: a tall horse-headed trickster: a black horse head with a wild mane, very long thin human limbs, a ragged loincloth.
```
**77 kapre** (คาเปร)
```
Monster: a huge dark tree giant: very tall and hairy, a big beard, smoking a huge cigar, sitting-style hunch, a loincloth of leaves.
```
**78 boss_bakunawa** (บอสบากูนาวา)
```
Monster: the boss: a giant sea serpent-dragon: a long blue-silver scaled body, a huge mouth that could swallow the moon, fins like wings, glowing pale eyes.
```
