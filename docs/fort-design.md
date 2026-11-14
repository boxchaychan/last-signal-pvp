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
