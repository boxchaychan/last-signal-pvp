# Fort game (build by day, defend by night) — plan before building
Owner 2026-11-14: liked the genre of Thronefall ("Thronefall ชอบอยู่นะ รายละเอียดก่อนทำ"). GENRE ONLY: our own name, art, maps, rules.
Working title: **Hoodfall: ป้อมคืนเผ่าฮู้ด** (owner may rename). Page to be: `fort.html` (top-down, single canvas, phone landscape first).

## The loop
1. DAY: walk the hero to glowing build spots, stand on one, press BUILD (cost shown) or UPGRADE. Red arrows at the map edge show where tonight's monsters come from.
2. Press START NIGHT. Monsters walk in along the paths in waves. Towers / soldiers fight on their own, the hero fights too (combo + 2 skills).
3. DAWN: houses and farms pay gold, fallen walls can be rebuilt, the hero heals. Next day.
4. Survive N nights (5 on map 1, 8 on map 2, 10 on map 3). LOSE if the tribe's heart (a big crystal totem in the middle) is destroyed.
   The hero does not die for good: knocked out -> back at the heart after 5 s.

## Maps (already made, free)
The three top-down maps of `map.html` (`tools/art/td_map.py`, the look the owner loves): green forest = map 1, autumn = map 2, dark forest = map 3.
Each gets: the heart spot, 12-16 build spots, 2-4 monster entry paths (roads), and where walls can go.

## Buildings (8 to start, each 3 levels; the picture changes per level)
| Building | Does | Lv up |
|---|---|---|
| House | +gold each dawn | more gold |
| Farm | +gold each dawn, cheap, weak | more gold |
| Palisade wall | blocks a path, monsters must break it | stone wall, spikes |
| Archer tower | shoots the nearest monster | range, double shot |
| Fire totem | splash fire on a spot (ground area) | bigger area, burn |
| Barracks | 3 soldiers that guard its spot | more / stronger soldiers |
| Healing shrine | heals hero and soldiers nearby | faster heal |
| Gate tower | wall + archer in one, on the main road | sturdier |

## Hero
- First playable: the dagger girl or swordsman already top-down in `map.html` (moves exist, free).
- Target: the hooded rabbit with the saw-blade, top-down (needs new clips, see art).
- Skills (ground-targeted, our direction): Quake Slam (spikes along a line), Grinder Spin (area around the hero).

## Monsters
Our 42 monsters (`art/td/map*/mob_*.png` are top-down already for map 1); fast ones, tanks that hit walls, ranged ones; a BOSS on the last night with red ground warnings.

## Between maps (light meta, not a build system)
After a won map: pick 1 of 3 bonuses (e.g. +start gold, towers +range, walls +HP); unlocks the next map.

## Phone controls
Left thumb: move (virtual stick). Right: attack, skill 1, skill 2; BUILD / UPGRADE pops up when standing on a spot; START NIGHT button in the day.

## Art: what exists and what costs (PixelLab only on the owner's "เจน"; standard 1-credit first, punch every sprite)
| Need | How | Credits (est.) |
|---|---|---|
| 3 maps, monsters, effects | already ours | 0 |
| 8 buildings x 3 levels + a ruined/empty build spot | PixelLab map objects, top-down, 1 each | ~25-30 |
| The heart crystal totem (+ cracked state) | PixelLab, 1-2 | ~2 |
| Soldiers (2 kinds) walk + attack, 4 directions | PixelLab character + animations | ~20-30 |
| Rabbit hero top-down, 4 dirs, walk + attack + 2 skills | PixelLab character from the rabbit + animations, or GPT sheets (free) | ~0-40 |
| Total | | ~50-100 of the ~1,260 left (reset 2026-12-08) |

## Build order
1. FREE prototype on map 1: day / night loop, build spots, buildings drawn as simple coloured blocks in code, the dagger girl as hero, 5 nights, gold, lose / win. Owner plays it and says what is fun / boring.
2. Buildings art (on "เจน", ~30 credits) -> real buildings, 3 levels.
3. Soldiers + rabbit top-down (on "เจน").
4. Maps 2 and 3, the boss, bonuses, balance tests (headless, like `tools/qa/gem_balance.js`).

## Theme change (owner 2026-11-14 "อยากให้เป็นย้อนยุคเลย ยุคหิน")
STONE AGE. Heart = the tribe's sacred FIRE (a big bonfire ringed with stones; cracked = the fire dying). Buildings become:
hut (gold -> food / shells as money), berry patch, sharpened-stake fence, lookout with spear throwers, fire pit (burning area),
hunters' camp (3 spear warriors), shaman's hut (heals), stone gate. Level-ups go wood -> wood + stone -> big stones and bones.
Enemies: wild beasts (wolves, boars, sabre-tooth, giant birds), rival tribes, and a mammoth / dinosaur-like beast as the boss.
Hero: a tribe champion in an animal-pelt hood (the hooded-rabbit idea fits: rabbit-pelt hood, stone / bone weapon).
Maps: map 1 (green forest) fits as it is; brick walls, arches and the paved road of maps 2-3 do not: those props / roads need a stone-age repaint later.
Open question to the owner: how much weight on the HERO vs the buildings (see chat).

## Direction change (owner 2026-11-14): long game, management first, smart NPCs, expanding land, rival tribes
Owner: "อยากให้เป็นเกมเล่นยาวๆ ใช้บริหารมากกว่าการเดินออกไปสู้เอง ให้พวก NPC มีค่าความฉลาดด้วย แล้วก็ขยายดินแดนไปเรื่อยๆ โดยให้มีศัตรูเล่นแบบเดียวกับเราด้วย".
So it is no longer a hero-defence game: it is a stone-age TRIBE MANAGEMENT game (closest genre references: Northgard = clans claim land
region by region, assign villagers to jobs, survive winter, rival AI clans do the same; Dawn of Man = stone age settlement).
Draft (not agreed yet):
- Map split into REGIONS (forest, river, cave, hills, ...). Claim a neighbouring region with food + scouting; each region has a resource and room for buildings.
- VILLAGERS are individuals: name, age, traits and stats (intelligence = learns jobs / research faster, strength = gathering / fighting,
  bravery, hunger); they choose tasks themselves by priorities the player sets (Claude's idea: simple "utility AI": every villager scores
  the open tasks and picks the best, so they look smart without micro-management).
- Seasons; winter = food crisis; beasts and raids.
- DISCOVERIES (fire, spear, pottery, farming, stone walls, ...) from smart villagers.
- RIVAL TRIBES run by the same rules (claim, gather, build, raid), each with its own animal totem / personality.
- The hero becomes the tribe's champion: a strong unit, not the whole game.
Open decisions for the owner: real-time with pause or season turns; map size / session length; how to win (unite all tribes, a great wonder, survive N years).

## Villager stats (owner 2026-11-14, idea from dungeon-game stats)
"ชาวบ้านมีสเตตัสเหมือนดันเจี้ยน แต่ทำงานได้ไม่เท่ากัน": STR = cuts / carries more per trip, AGI = walks and works faster,
INT = smarter choices (nearer resource, the one the tribe needs most). Claude's additions (draft): VIT = stamina / works longer, gets sick less;
LUK = finds rare things (flint, herbs, a lost animal). INT in practice: low = takes the first job seen, walks far, carries what is not needed;
high = scores every open job by need x distance x danger, drops off at the nearest store, comes home before dark / storms.
Stats grow with work (chopping raises STR) and with age; traits (lazy, brave, glutton...) bend them. Because AGI and INT only show when you
WATCH villagers move, time runs in real time with pause and x2 / x3 speed (the player sets priorities, villagers decide themselves,
so the phone stays calm). Supersedes the turn-based suggestion.
DECIDED (owner 2026-11-14 "ใช้แบบ A"): REAL TIME (pause + x2 / x3 speed). Still open: session length / saves, how to win.
First build step (free): a small village on map 1 with 6 villagers of different STR / AGI / INT who gather wood and food on their own, to see that smart and dull villagers really work differently.

## Priorities (owner 2026-11-14)
"ต่อไปจะมีผู้เล่นเยอะเวลาเล่นออนไลน์ แต่พอยต์คือมีศัตรูที่เป็นบอทอยู่แล้ว ยังไงก็ต้องเน้นสู้เอาตัวรอดก่อน":
1. FIRST: SURVIVAL + FIGHTING. Threats from day one (beasts at night, raids by the bot tribes, winter); gathering / building exists to survive and fight.
   Villagers also fight (STR = damage, AGI = dodge / flee, INT = when to retreat, group up, hide in huts); the champion leads.
2. Bot tribes play by the same rules as the player.
3. LATER: online with many players. Not possible on GitHub Pages alone (static files): needs a game server or a hosted realtime service.
   Prepare now, for free: every tribe (player or bot) is the same kind of "seat" that only sends ORDERS (priorities, build, attack),
   the simulation never reads the screen; later a human seat over the network replaces a bot seat.

## Core rule (owner 2026-11-14) — this overrides the "rival tribes raid you" idea above
"เล่น 5 คนพร้อมกันได้ แต่ตอนทดลองเล่นคนเดียวก่อน ให้มีเวฟมาเลย เน้นต่อให้เล่นหลายคนก็เน้นมอนศัตรูที่มาโจมตี ใครแตกก่อนแพ้":
- Up to 5 tribes on one map (later online players; now 1 player + bot tribes, or the player alone for tests).
- The enemy is the MONSTER WAVES, coming from the very start and growing. Tribes do not mainly fight each other: it is a survival race.
- The tribe whose heart fire goes out is OUT; the last tribe standing wins (solo test: survive as many waves as possible, score = waves).
- So every tribe gets the same waves at the same time; land, villagers and buildings are how you outlast the others.
First playable (free): solo, map 1, a heart fire, 6 villagers with STR / AGI / INT, gather wood / food, build stake fences + a spear lookout,
waves of wolves / boars from the first minute, game over when the fire dies, wave counter as the score.

## Answers (owner 2026-11-14)
1. CHAMPION: not controlled, only ORDERED (go defend / clear a spot). Stronger than villagers, has skills and LEVELS. Dies = gone for good.
2. VILLAGERS die for good; new ones are BORN in the village as CHILDREN (grow up into workers; Claude's idea: stats partly from the parents).
   Badly hurt villagers may FLEE: INT decides when they retreat in time; STR (strength / toughness) decides whether they hold out
   (bleeding) until they reach home, where they heal.
3-7 not answered -> Claude's suggestions stand: expand by planting TOTEM poles (a ring of land each); 20-30 min a match, solo save;
   tribes only race to survive (no trading / sabotage at first); top-down pixel, units ~32-48 px, punch recipe, map-1 look;
   light unlocks after a match (new tribes with their own strengths, e.g. wolf tribe fights better, rabbit tribe gathers faster).
3 (owner, replaces the totem idea): NO explicit territory / borders. The player only marks space for housing (where the tribe may grow);
   when the population grows, villagers build huts and other buildings THEMSELVES there. The village grows on its own; the player's job is
   to keep it from being overrun (defence), and to send people out for resources.
1b (owner correction): the CHAMPION does NOT die for good: when killed it comes back after a LONG respawn time (keeps its level).
   Villagers still die for good.
3b (owner): building can spread anywhere, no limit, no totems. The only limit is the monsters: they go for whatever is outside the
   defended area, so a tribe that grows wider than it can guard loses huts and people. Monster AI should prefer the weakest, most exposed spot.
4 (owner): a match lasts 15-20 min, up to ~30, as long as the tribes hold: waves keep getting stronger so a match always ends.
5 (owner, replaces "race only"): "ยังไงก็ต้องก่อกวนกันอยู่แล้ว" = tribes DO harass each other. Draft ways (to agree later):
   lure / drive a wave toward a neighbour, small raids that steal stored food / wood, the champion ambushing a neighbour's gatherers.
   Monster waves stay the main threat.
5b (owner): NO trading of resources between tribes, ever. The focus is defending against the monsters; harassing neighbours stays possible.

## DIRECTION v3 (owner 2026-11-14) — newest, overrides the match / multiplayer parts above
"ทำเมืองเราเป็น idle แล้วบุกตามด่าน โดยกดสู้ มอนจะวิ่งมาตามด่าน":
- HOME VILLAGE = IDLE: it keeps working when the game is closed (villagers gather, are born, grow up, train; offline gains on return).
  Villager stats STR / AGI / INT, the ordered champion with levels and a long respawn, organic building all stay.
- STAGES: a stage map; pick a stage, press FIGHT; monsters run in along that stage's paths in waves; the tribe's fighters + defences hold.
  Win = stage cleared, rewards (food, wood, stone, rare items, new villagers / champions) go home to grow the village.
- The village feeds the stages (stronger people, better fences / weapons); the stages feed the village (resources, unlocks).
- Multiplayer later, async (no need to be online together): leaderboards, raiding sleeping villages; not in the first build.
Open: how much the player controls inside a stage (place defences before FIGHT? order the champion during the fight?).
Answer (owner): "ไม่ต้องรอก็ได้ ให้กดพร้อม เหมือนท้าสู้ แล้วมอนจะวิ่งมาบุกเอง จบเป็นเวฟ": no countdown; the player presses READY (a challenge)
whenever they like, the stage's monsters run in by themselves wave by wave, the fight plays itself (villagers, champion, defences act on
their own AI), the stage ends when the waves are cleared or the fire falls. Read as: the battle happens AT the tribe's village
(its own layout = its defence), stages = harder and harder challenges. Confirm with the owner if a separate battlefield was meant.
