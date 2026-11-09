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
| 16 | jiangshi | todo | China | medium |
| 17 | paper_doll | todo | China | small |
| 18 | terracotta_archer | todo | China | medium |
| 19 | terracotta_general | todo | China | large |
| 20 | fox_spirit | todo | China | medium |
| 21 | toad_demon | todo | China | large |
| 22 | boss_nian | todo | China boss | huge |

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

