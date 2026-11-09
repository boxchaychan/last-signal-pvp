# Monster animation frames (action game) — queue for Codex

Owner 2026-11-09: the monsters' frames are made by Codex (not PixelLab). Reply to the owner in Thai, short and plain.

## Rules
- ONE picture per row of the queue: one monster, one action, 6 frames in a 3x2 grid on white. Attach the monster's own
  turnaround `art/incoming/mobs/<key>.png` every time (it is the reference for face, colours and size).
- Save full size as `art/incoming/mobs/anim/<key>_<action>.png`; add one Thai line per file to
  `art/incoming/mobs/anim/REPORT_TH.txt` (anything that came out wrong: a frame crossing a cell, a turned view, a missing frame).
- Mark the row `done` here. Work in the order of the queue; when the owner says "ทำเฟรมมอนต่อ", continue at the first `todo`.
- Branch `codex/mob-anim`, open a pull request, never merge, never push to `main`. Claude works in this same folder on
  `main`: when you stop, switch the folder back with `git checkout main` so the other agent's work does not land on your branch.

## Queue
| # | key | action | status | file |
|---|-----|--------|--------|------|
| 1 | shroom | walk | done | `art/incoming/mobs/anim/shroom_walk.png` |
| 2 | shroom | attack | done | `art/incoming/mobs/anim/shroom_attack.png` |
| 3 | shroom | death | done | `art/incoming/mobs/anim/shroom_death.png` |
| 4 | shroom | hurt | done | `art/incoming/mobs/anim/shroom_hurt.png` |
| 5 | wolf | walk | done | `art/incoming/mobs/anim/wolf_walk.png` |
| 6 | wolf | attack | done | `art/incoming/mobs/anim/wolf_attack.png` |
| 7 | wolf | death | done | `art/incoming/mobs/anim/wolf_death.png` |
| 8 | wolf | hurt | done | `art/incoming/mobs/anim/wolf_hurt.png` |
| 9 | goblin_archer | walk | done | `art/incoming/mobs/anim/goblin_archer_walk.png` |
| 10 | goblin_archer | attack | done | `art/incoming/mobs/anim/goblin_archer_attack.png` |
| 11 | goblin_archer | death | done | `art/incoming/mobs/anim/goblin_archer_death.png` |
| 12 | goblin_archer | hurt | done | `art/incoming/mobs/anim/goblin_archer_hurt.png` |
| 13 | boar_guard | walk | done | `art/incoming/mobs/anim/boar_guard_walk.png` |
| 14 | boar_guard | attack | done | `art/incoming/mobs/anim/boar_guard_attack.png` |
| 15 | boar_guard | death | done | `art/incoming/mobs/anim/boar_guard_death.png` |
| 16 | boar_guard | hurt | done | `art/incoming/mobs/anim/boar_guard_hurt.png` |
| 17 | skeleton | walk | done | `art/incoming/mobs/anim/skeleton_walk.png` |
| 18 | skeleton | attack | done | `art/incoming/mobs/anim/skeleton_attack.png` |
| 19 | skeleton | death | done | `art/incoming/mobs/anim/skeleton_death.png` |
| 20 | skeleton | hurt | done | `art/incoming/mobs/anim/skeleton_hurt.png` |
| 21 | wisp | walk | done | `art/incoming/mobs/anim/wisp_walk.png` |
| 22 | wisp | attack | done | `art/incoming/mobs/anim/wisp_attack.png` |
| 23 | wisp | death | done | `art/incoming/mobs/anim/wisp_death.png` |
| 24 | wisp | hurt | done | `art/incoming/mobs/anim/wisp_hurt.png` |
| 25 | golem | walk | done | `art/incoming/mobs/anim/golem_walk.png` |
| 26 | golem | attack | done | `art/incoming/mobs/anim/golem_attack.png` |
| 27 | golem | death | done | `art/incoming/mobs/anim/golem_death.png` |
| 28 | golem | hurt | done | `art/incoming/mobs/anim/golem_hurt.png` |
| 29 | boss_treant | walk | done | `art/incoming/mobs/anim/boss_treant_walk.png` |
| 30 | boss_treant | attack | done | `art/incoming/mobs/anim/boss_treant_attack.png` |
| 31 | boss_treant | death | done | `art/incoming/mobs/anim/boss_treant_death.png` |
| 32 | boss_treant | hurt | done | `art/incoming/mobs/anim/boss_treant_hurt.png` |
| 33 | krahang | walk | done | `art/incoming/mobs/anim/krahang_walk.png` |
| 34 | krahang | attack | done | `art/incoming/mobs/anim/krahang_attack.png` |
| 35 | krahang | death | done | `art/incoming/mobs/anim/krahang_death.png` |
| 36 | krahang | hurt | done | `art/incoming/mobs/anim/krahang_hurt.png` |
| 37 | khamot | walk | done | `art/incoming/mobs/anim/khamot_walk.png` |
| 38 | khamot | attack | done | `art/incoming/mobs/anim/khamot_attack.png` |
| 39 | khamot | death | done | `art/incoming/mobs/anim/khamot_death.png` |
| 40 | khamot | hurt | done | `art/incoming/mobs/anim/khamot_hurt.png` |
| 41 | phrai | walk | done | `art/incoming/mobs/anim/phrai_walk.png` |
| 42 | phrai | attack | done | `art/incoming/mobs/anim/phrai_attack.png` |
| 43 | phrai | death | done | `art/incoming/mobs/anim/phrai_death.png` |
| 44 | phrai | hurt | done | `art/incoming/mobs/anim/phrai_hurt.png` |
| 45 | pret | walk | done | `art/incoming/mobs/anim/pret_walk.png` |
| 46 | pret | attack | done | `art/incoming/mobs/anim/pret_attack.png` |
| 47 | pret | death | done | `art/incoming/mobs/anim/pret_death.png` |
| 48 | pret | hurt | done | `art/incoming/mobs/anim/pret_hurt.png` |
| 49 | monkey | walk | done | `art/incoming/mobs/anim/monkey_walk.png` |
| 50 | monkey | attack | done | `art/incoming/mobs/anim/monkey_attack.png` |
| 51 | monkey | death | done | `art/incoming/mobs/anim/monkey_death.png` |
| 52 | monkey | hurt | done | `art/incoming/mobs/anim/monkey_hurt.png` |
| 53 | croc_guard | walk | done | `art/incoming/mobs/anim/croc_guard_walk.png` |
| 54 | croc_guard | attack | done | `art/incoming/mobs/anim/croc_guard_attack.png` |
| 55 | croc_guard | death | done | `art/incoming/mobs/anim/croc_guard_death.png` |
| 56 | croc_guard | hurt | done | `art/incoming/mobs/anim/croc_guard_hurt.png` |
| 57 | boss_chalawan | walk | done | `art/incoming/mobs/anim/boss_chalawan_walk.png` |
| 58 | boss_chalawan | attack | done | `art/incoming/mobs/anim/boss_chalawan_attack.png` |
| 59 | boss_chalawan | death | done | `art/incoming/mobs/anim/boss_chalawan_death.png` |
| 60 | boss_chalawan | hurt | done | `art/incoming/mobs/anim/boss_chalawan_hurt.png` |
| 61 | jiangshi | walk | done | `art/incoming/mobs/anim/jiangshi_walk.png` |
| 62 | jiangshi | attack | done | `art/incoming/mobs/anim/jiangshi_attack.png` |
| 63 | jiangshi | death | done | `art/incoming/mobs/anim/jiangshi_death.png` |
| 64 | jiangshi | hurt | done | `art/incoming/mobs/anim/jiangshi_hurt.png` |
| 65 | paper_doll | walk | done | `art/incoming/mobs/anim/paper_doll_walk.png` |
| 66 | paper_doll | attack | done | `art/incoming/mobs/anim/paper_doll_attack.png` |
| 67 | paper_doll | death | done | `art/incoming/mobs/anim/paper_doll_death.png` |
| 68 | paper_doll | hurt | done | `art/incoming/mobs/anim/paper_doll_hurt.png` |
| 69 | terracotta_archer | walk | done | `art/incoming/mobs/anim/terracotta_archer_walk.png` |
| 70 | terracotta_archer | attack | done | `art/incoming/mobs/anim/terracotta_archer_attack.png` |
| 71 | terracotta_archer | death | done | `art/incoming/mobs/anim/terracotta_archer_death.png` |
| 72 | terracotta_archer | hurt | done | `art/incoming/mobs/anim/terracotta_archer_hurt.png` |
| 73 | terracotta_general | walk | done | `art/incoming/mobs/anim/terracotta_general_walk.png` |
| 74 | terracotta_general | attack | done | `art/incoming/mobs/anim/terracotta_general_attack.png` |
| 75 | terracotta_general | death | done | `art/incoming/mobs/anim/terracotta_general_death.png` |
| 76 | terracotta_general | hurt | done | `art/incoming/mobs/anim/terracotta_general_hurt.png` |
| 77 | fox_spirit | walk | done | `art/incoming/mobs/anim/fox_spirit_walk.png` |
| 78 | fox_spirit | attack | done | `art/incoming/mobs/anim/fox_spirit_attack.png` |
| 79 | fox_spirit | death | done | `art/incoming/mobs/anim/fox_spirit_death.png` |
| 80 | fox_spirit | hurt | done | `art/incoming/mobs/anim/fox_spirit_hurt.png` |
| 81 | toad_demon | walk | done | `art/incoming/mobs/anim/toad_demon_walk.png` |
| 82 | toad_demon | attack | done | `art/incoming/mobs/anim/toad_demon_attack.png` |
| 83 | toad_demon | death | done | `art/incoming/mobs/anim/toad_demon_death.png` |
| 84 | toad_demon | hurt | done | `art/incoming/mobs/anim/toad_demon_hurt.png` |
| 85 | boss_nian | walk | done | `art/incoming/mobs/anim/boss_nian_walk.png` |
| 86 | boss_nian | attack | done | `art/incoming/mobs/anim/boss_nian_attack.png` |
| 87 | boss_nian | death | done | `art/incoming/mobs/anim/boss_nian_death.png` |
| 88 | boss_nian | hurt | done | `art/incoming/mobs/anim/boss_nian_hurt.png` |
| 89 | kappa | walk | done | `art/incoming/mobs/anim/kappa_walk.png` |
| 90 | kappa | attack | done | `art/incoming/mobs/anim/kappa_attack.png` |
| 91 | kappa | death | done | `art/incoming/mobs/anim/kappa_death.png` |
| 92 | kappa | hurt | done | `art/incoming/mobs/anim/kappa_hurt.png` |
| 93 | kasa_obake | walk | done | `art/incoming/mobs/anim/kasa_obake_walk.png` |
| 94 | kasa_obake | attack | done | `art/incoming/mobs/anim/kasa_obake_attack.png` |
| 95 | kasa_obake | death | done | `art/incoming/mobs/anim/kasa_obake_death.png` |
| 96 | kasa_obake | hurt | done | `art/incoming/mobs/anim/kasa_obake_hurt.png` |
| 97 | oni | walk | done | `art/incoming/mobs/anim/oni_walk.png` |
| 98 | oni | attack | done | `art/incoming/mobs/anim/oni_attack.png` |
| 99 | oni | death | done | `art/incoming/mobs/anim/oni_death.png` |
| 100 | oni | hurt | done | `art/incoming/mobs/anim/oni_hurt.png` |
| 101 | tengu | walk | done | `art/incoming/mobs/anim/tengu_walk.png` |
| 102 | tengu | attack | done | `art/incoming/mobs/anim/tengu_attack.png` |
| 103 | tengu | death | done | `art/incoming/mobs/anim/tengu_death.png` |
| 104 | tengu | hurt | done | `art/incoming/mobs/anim/tengu_hurt.png` |
| 105 | rokurokubi | walk | done | `art/incoming/mobs/anim/rokurokubi_walk.png` |
| 106 | rokurokubi | attack | done | `art/incoming/mobs/anim/rokurokubi_attack.png` |
| 107 | rokurokubi | death | todo | `art/incoming/mobs/anim/rokurokubi_death.png` |
| 108 | rokurokubi | hurt | todo | `art/incoming/mobs/anim/rokurokubi_hurt.png` |
| 109 | nekomata | walk | todo | `art/incoming/mobs/anim/nekomata_walk.png` |
| 110 | nekomata | attack | todo | `art/incoming/mobs/anim/nekomata_attack.png` |
| 111 | nekomata | death | todo | `art/incoming/mobs/anim/nekomata_death.png` |
| 112 | nekomata | hurt | todo | `art/incoming/mobs/anim/nekomata_hurt.png` |
| 113 | boss_orochi | walk | todo | `art/incoming/mobs/anim/boss_orochi_walk.png` |
| 114 | boss_orochi | attack | todo | `art/incoming/mobs/anim/boss_orochi_attack.png` |
| 115 | boss_orochi | death | todo | `art/incoming/mobs/anim/boss_orochi_death.png` |
| 116 | boss_orochi | hurt | todo | `art/incoming/mobs/anim/boss_orochi_hurt.png` |
| 117 | mummy | walk | todo | `art/incoming/mobs/anim/mummy_walk.png` |
| 118 | mummy | attack | todo | `art/incoming/mobs/anim/mummy_attack.png` |
| 119 | mummy | death | todo | `art/incoming/mobs/anim/mummy_death.png` |
| 120 | mummy | hurt | todo | `art/incoming/mobs/anim/mummy_hurt.png` |
| 121 | scarab | walk | todo | `art/incoming/mobs/anim/scarab_walk.png` |
| 122 | scarab | attack | todo | `art/incoming/mobs/anim/scarab_attack.png` |
| 123 | scarab | death | todo | `art/incoming/mobs/anim/scarab_death.png` |
| 124 | scarab | hurt | todo | `art/incoming/mobs/anim/scarab_hurt.png` |
| 125 | jackal_warrior | walk | todo | `art/incoming/mobs/anim/jackal_warrior_walk.png` |
| 126 | jackal_warrior | attack | todo | `art/incoming/mobs/anim/jackal_warrior_attack.png` |
| 127 | jackal_warrior | death | todo | `art/incoming/mobs/anim/jackal_warrior_death.png` |
| 128 | jackal_warrior | hurt | todo | `art/incoming/mobs/anim/jackal_warrior_hurt.png` |
| 129 | sand_scorpion | walk | todo | `art/incoming/mobs/anim/sand_scorpion_walk.png` |
| 130 | sand_scorpion | attack | todo | `art/incoming/mobs/anim/sand_scorpion_attack.png` |
| 131 | sand_scorpion | death | todo | `art/incoming/mobs/anim/sand_scorpion_death.png` |
| 132 | sand_scorpion | hurt | todo | `art/incoming/mobs/anim/sand_scorpion_hurt.png` |
| 133 | cobra_priest | walk | todo | `art/incoming/mobs/anim/cobra_priest_walk.png` |
| 134 | cobra_priest | attack | todo | `art/incoming/mobs/anim/cobra_priest_attack.png` |
| 135 | cobra_priest | death | todo | `art/incoming/mobs/anim/cobra_priest_death.png` |
| 136 | cobra_priest | hurt | todo | `art/incoming/mobs/anim/cobra_priest_hurt.png` |
| 137 | sand_golem | walk | todo | `art/incoming/mobs/anim/sand_golem_walk.png` |
| 138 | sand_golem | attack | todo | `art/incoming/mobs/anim/sand_golem_attack.png` |
| 139 | sand_golem | death | todo | `art/incoming/mobs/anim/sand_golem_death.png` |
| 140 | sand_golem | hurt | todo | `art/incoming/mobs/anim/sand_golem_hurt.png` |
| 141 | boss_sphinx | walk | todo | `art/incoming/mobs/anim/boss_sphinx_walk.png` |
| 142 | boss_sphinx | attack | todo | `art/incoming/mobs/anim/boss_sphinx_attack.png` |
| 143 | boss_sphinx | death | todo | `art/incoming/mobs/anim/boss_sphinx_death.png` |
| 144 | boss_sphinx | hurt | todo | `art/incoming/mobs/anim/boss_sphinx_hurt.png` |
| 145 | draugr | walk | todo | `art/incoming/mobs/anim/draugr_walk.png` |
| 146 | draugr | attack | todo | `art/incoming/mobs/anim/draugr_attack.png` |
| 147 | draugr | death | todo | `art/incoming/mobs/anim/draugr_death.png` |
| 148 | draugr | hurt | todo | `art/incoming/mobs/anim/draugr_hurt.png` |
| 149 | frost_wolf | walk | todo | `art/incoming/mobs/anim/frost_wolf_walk.png` |
| 150 | frost_wolf | attack | todo | `art/incoming/mobs/anim/frost_wolf_attack.png` |
| 151 | frost_wolf | death | todo | `art/incoming/mobs/anim/frost_wolf_death.png` |
| 152 | frost_wolf | hurt | todo | `art/incoming/mobs/anim/frost_wolf_hurt.png` |
| 153 | troll | walk | todo | `art/incoming/mobs/anim/troll_walk.png` |
| 154 | troll | attack | todo | `art/incoming/mobs/anim/troll_attack.png` |
| 155 | troll | death | todo | `art/incoming/mobs/anim/troll_death.png` |
| 156 | troll | hurt | todo | `art/incoming/mobs/anim/troll_hurt.png` |
| 157 | ice_wraith | walk | todo | `art/incoming/mobs/anim/ice_wraith_walk.png` |
| 158 | ice_wraith | attack | todo | `art/incoming/mobs/anim/ice_wraith_attack.png` |
| 159 | ice_wraith | death | todo | `art/incoming/mobs/anim/ice_wraith_death.png` |
| 160 | ice_wraith | hurt | todo | `art/incoming/mobs/anim/ice_wraith_hurt.png` |
| 161 | dwarf_berserker | walk | todo | `art/incoming/mobs/anim/dwarf_berserker_walk.png` |
| 162 | dwarf_berserker | attack | todo | `art/incoming/mobs/anim/dwarf_berserker_attack.png` |
| 163 | dwarf_berserker | death | todo | `art/incoming/mobs/anim/dwarf_berserker_death.png` |
| 164 | dwarf_berserker | hurt | todo | `art/incoming/mobs/anim/dwarf_berserker_hurt.png` |
| 165 | ice_golem | walk | todo | `art/incoming/mobs/anim/ice_golem_walk.png` |
| 166 | ice_golem | attack | todo | `art/incoming/mobs/anim/ice_golem_attack.png` |
| 167 | ice_golem | death | todo | `art/incoming/mobs/anim/ice_golem_death.png` |
| 168 | ice_golem | hurt | todo | `art/incoming/mobs/anim/ice_golem_hurt.png` |
| 169 | boss_jotun | walk | todo | `art/incoming/mobs/anim/boss_jotun_walk.png` |
| 170 | boss_jotun | attack | todo | `art/incoming/mobs/anim/boss_jotun_attack.png` |
| 171 | boss_jotun | death | todo | `art/incoming/mobs/anim/boss_jotun_death.png` |
| 172 | boss_jotun | hurt | todo | `art/incoming/mobs/anim/boss_jotun_hurt.png` |

## Prompts
### shroom walk (เห็ดพิษ)
Attach `art/incoming/mobs/shroom.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the small grumpy purple-capped walking mushroom, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: a bouncy waddle: it hops forward on its stubby legs, the cap squashing down on landing and stretching up on the hop. A smooth loop: frame 6 flows back into frame 1. It walks in place (it does not travel across the cells).
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### shroom attack (เห็ดพิษ)
Attach `art/incoming/mobs/shroom.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the small grumpy purple-capped walking mushroom, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it squashes down low, then springs up and puffs its cap forward to spit spores at the enemy in front of it, then settles back. Frames 1 and 6 show the ready pose; frames 2-3 are the wind-up, frame 4 is the hit, frame 5 the follow-through.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### shroom death (เห็ดพิษ)
Attach `art/incoming/mobs/shroom.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the small grumpy purple-capped walking mushroom, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit, wobbles, its cap droops and it shrinks and flops over on its side, lying still in the last frame.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### shroom hurt (เห็ดพิษ)
Attach `art/incoming/mobs/shroom.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the small grumpy purple-capped walking mushroom, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit (owner 2026-11-09 "โดนโจมตีแล้วสะดุ้ง"): frame 1 the ready pose, frame 2 a sharp flinch backward with its eyes squeezed shut, frame 3 knocked further back and leaning away, frame 4 staggering, frame 5 regaining its balance, frame 6 back to the ready pose. Short and snappy.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### wolf walk (หมาป่าเงา)
Attach `art/incoming/mobs/wolf.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the shadow wolf on four legs, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: a fast trot on four legs, legs moving in a clear gait, the smoky tail swaying. A smooth loop: frame 6 flows back into frame 1. It walks in place (it does not travel across the cells).
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### wolf attack (หมาป่าเงา)
Attach `art/incoming/mobs/wolf.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the shadow wolf on four legs, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it crouches low on its front legs, then lunges forward with jaws wide open for a bite (the furthest reach in frame 4), then lands back in the ready stance. Frames 1 and 6 show the ready pose; frames 2-3 are the wind-up, frame 4 is the hit, frame 5 the follow-through.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### wolf death (หมาป่าเงา)
Attach `art/incoming/mobs/wolf.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the shadow wolf on four legs, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it yelps and recoils, its legs buckle and it collapses onto its side, lying still in the last frame.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### wolf hurt (หมาป่าเงา)
Attach `art/incoming/mobs/wolf.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the shadow wolf on four legs, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit (owner 2026-11-09 "โดนโจมตีแล้วสะดุ้ง"): frame 1 the ready pose, frame 2 a sharp flinch backward with its eyes squeezed shut, frame 3 knocked further back and leaning away, frame 4 staggering, frame 5 regaining its balance, frame 6 back to the ready pose. Short and snappy.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### goblin_archer walk (ก็อบลินนักธนู)
Attach `art/incoming/mobs/goblin_archer.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the small goblin archer with the leaf hood and the short bow, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: a sneaky quick walk, knees bent, the bow held low. A smooth loop: frame 6 flows back into frame 1. It walks in place (it does not travel across the cells).
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### goblin_archer attack (ก็อบลินนักธนู)
Attach `art/incoming/mobs/goblin_archer.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the small goblin archer with the leaf hood and the short bow, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it pulls an arrow from the quiver, nocks it, draws the bow back and aims forward, releases (the arrow leaves the frame, the bowstring snaps forward in frame 4), then lowers the bow; arrows always point forward with the head at the front. Frames 1 and 6 show the ready pose; frames 2-3 are the wind-up, frame 4 is the hit, frame 5 the follow-through.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### goblin_archer death (ก็อบลินนักธนู)
Attach `art/incoming/mobs/goblin_archer.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the small goblin archer with the leaf hood and the short bow, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit, staggers back, drops the bow and falls on its back, lying still in the last frame.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### goblin_archer hurt (ก็อบลินนักธนู)
Attach `art/incoming/mobs/goblin_archer.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the small goblin archer with the leaf hood and the short bow, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit (owner 2026-11-09 "โดนโจมตีแล้วสะดุ้ง"): frame 1 the ready pose, frame 2 a sharp flinch backward with its eyes squeezed shut, frame 3 knocked further back and leaning away, frame 4 staggering, frame 5 regaining its balance, frame 6 back to the ready pose. Short and snappy.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### boar_guard walk (นักรบหมูป่า)
Attach `art/incoming/mobs/boar_guard.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the big boar-headed warrior with the round shield and spiked club, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: a heavy stomping walk, shoulders rocking, the shield held in front, the club resting on the shoulder. A smooth loop: frame 6 flows back into frame 1. It walks in place (it does not travel across the cells).
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### boar_guard attack (นักรบหมูป่า)
Attach `art/incoming/mobs/boar_guard.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the big boar-headed warrior with the round shield and spiked club, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it raises the spiked club high overhead, then smashes it down hard in front of it (the club hits the ground in frame 4), then lifts it back up. Frames 1 and 6 show the ready pose; frames 2-3 are the wind-up, frame 4 is the hit, frame 5 the follow-through.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### boar_guard death (นักรบหมูป่า)
Attach `art/incoming/mobs/boar_guard.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the big boar-headed warrior with the round shield and spiked club, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit, staggers, drops to one knee, the club and shield fall and it topples forward, lying still in the last frame.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### boar_guard hurt (นักรบหมูป่า)
Attach `art/incoming/mobs/boar_guard.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the big boar-headed warrior with the round shield and spiked club, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit (owner 2026-11-09 "โดนโจมตีแล้วสะดุ้ง"): frame 1 the ready pose, frame 2 a sharp flinch backward with its eyes squeezed shut, frame 3 knocked further back and leaning away, frame 4 staggering, frame 5 regaining its balance, frame 6 back to the ready pose. Short and snappy.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### skeleton walk (ทหารโครงกระดูก)
Attach `art/incoming/mobs/skeleton.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the skeleton soldier with the rusty helmet, cracked round shield and chipped sword, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: a stiff rattling march, bones jerking a little at each step, shield held in front. A smooth loop: frame 6 flows back into frame 1. It walks in place (it does not travel across the cells).
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### skeleton attack (ทหารโครงกระดูก)
Attach `art/incoming/mobs/skeleton.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the skeleton soldier with the rusty helmet, cracked round shield and chipped sword, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it pulls the sword back behind the shield, then steps in and slashes forward in a wide arc (the blade furthest forward in frame 4), then returns behind the shield. Frames 1 and 6 show the ready pose; frames 2-3 are the wind-up, frame 4 is the hit, frame 5 the follow-through.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### skeleton death (ทหารโครงกระดูก)
Attach `art/incoming/mobs/skeleton.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the skeleton soldier with the rusty helmet, cracked round shield and chipped sword, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit and falls apart: the bones come loose and collapse into a pile of bones with the helmet on top in the last frame.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### skeleton hurt (ทหารโครงกระดูก)
Attach `art/incoming/mobs/skeleton.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the skeleton soldier with the rusty helmet, cracked round shield and chipped sword, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit (owner 2026-11-09 "โดนโจมตีแล้วสะดุ้ง"): frame 1 the ready pose, frame 2 a sharp flinch backward with its eyes squeezed shut, frame 3 knocked further back and leaning away, frame 4 staggering, frame 5 regaining its balance, frame 6 back to the ready pose. Short and snappy.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### wisp walk (ภูตตะเกียง)
Attach `art/incoming/mobs/wisp.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the small floating hooded spirit holding a blue-flame lantern, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it floats forward, bobbing gently up and down, the ragged cloak tail rippling. A smooth loop: frame 6 flows back into frame 1. It walks in place (it does not travel across the cells).
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### wisp attack (ภูตตะเกียง)
Attach `art/incoming/mobs/wisp.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the small floating hooded spirit holding a blue-flame lantern, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it rears back, then swings the lantern forward and thrusts it at the enemy (the lantern furthest forward in frame 4), then floats back. Frames 1 and 6 show the ready pose; frames 2-3 are the wind-up, frame 4 is the hit, frame 5 the follow-through.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### wisp death (ภูตตะเกียง)
Attach `art/incoming/mobs/wisp.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the small floating hooded spirit holding a blue-flame lantern, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit, flickers, the cloak crumples inward and collapses empty to the ground with the lantern lying beside it in the last frame.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### wisp hurt (ภูตตะเกียง)
Attach `art/incoming/mobs/wisp.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the small floating hooded spirit holding a blue-flame lantern, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit (owner 2026-11-09 "โดนโจมตีแล้วสะดุ้ง"): frame 1 the ready pose, frame 2 a sharp flinch backward with its eyes squeezed shut, frame 3 knocked further back and leaning away, frame 4 staggering, frame 5 regaining its balance, frame 6 back to the ready pose. Short and snappy.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### golem walk (โกเลมหิน)
Attach `art/incoming/mobs/golem.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the big chunky mossy stone golem with the glowing teal rune, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: a slow heavy walk, the whole body rocking from side to side at each step. A smooth loop: frame 6 flows back into frame 1. It walks in place (it does not travel across the cells).
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### golem attack (โกเลมหิน)
Attach `art/incoming/mobs/golem.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the big chunky mossy stone golem with the glowing teal rune, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it pulls one huge stone fist far back, then punches forward hard with its whole weight (the fist furthest forward in frame 4), then pulls back to the ready stance. Frames 1 and 6 show the ready pose; frames 2-3 are the wind-up, frame 4 is the hit, frame 5 the follow-through.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### golem death (โกเลมหิน)
Attach `art/incoming/mobs/golem.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the big chunky mossy stone golem with the glowing teal rune, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit, cracks, the rune dims and it crumbles down into a heap of mossy stones in the last frame.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### golem hurt (โกเลมหิน)
Attach `art/incoming/mobs/golem.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the big chunky mossy stone golem with the glowing teal rune, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit (owner 2026-11-09 "โดนโจมตีแล้วสะดุ้ง"): frame 1 the ready pose, frame 2 a sharp flinch backward with its eyes squeezed shut, frame 3 knocked further back and leaning away, frame 4 staggering, frame 5 regaining its balance, frame 6 back to the ready pose. Short and snappy.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### boss_treant walk (บอสต้นไม้อสูร)
Attach `art/incoming/mobs/boss_treant.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the huge ancient tree giant boss, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: a slow lumbering walk on its thick roots, branches swaying. A smooth loop: frame 6 flows back into frame 1. It walks in place (it does not travel across the cells).
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### boss_treant attack (บอสต้นไม้อสูร)
Attach `art/incoming/mobs/boss_treant.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the huge ancient tree giant boss, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it rears back with both branch arms raised, then sweeps both thorny claws down and forward in front of it (the claws furthest forward in frame 4), then rises back up. Frames 1 and 6 show the ready pose; frames 2-3 are the wind-up, frame 4 is the hit, frame 5 the follow-through.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### boss_treant death (บอสต้นไม้อสูร)
Attach `art/incoming/mobs/boss_treant.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the huge ancient tree giant boss, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit, creaks and bends, then topples over and crashes to the ground, lying still in the last frame.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### boss_treant hurt (บอสต้นไม้อสูร)
Attach `art/incoming/mobs/boss_treant.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the huge ancient tree giant boss, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit (owner 2026-11-09 "โดนโจมตีแล้วสะดุ้ง"): frame 1 the ready pose, frame 2 a sharp flinch backward with its eyes squeezed shut, frame 3 knocked further back and leaning away, frame 4 staggering, frame 5 regaining its balance, frame 6 back to the ready pose. Short and snappy.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### krahang walk (ผีกระหัง)
Attach `art/incoming/mobs/krahang.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the Thai flying ghost with the winnowing-basket wings riding the rice pestle, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it flies forward on the pestle, flapping the two basket wings up and down in a clear flap cycle. A smooth loop: frame 6 flows back into frame 1. It walks in place (it does not travel across the cells).
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### krahang attack (ผีกระหัง)
Attach `art/incoming/mobs/krahang.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the Thai flying ghost with the winnowing-basket wings riding the rice pestle, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it pulls back, then dives forward on the pestle swinging both basket wings forward to strike (furthest forward in frame 4), then flies back up. Frames 1 and 6 show the ready pose; frames 2-3 are the wind-up, frame 4 is the hit, frame 5 the follow-through.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### krahang death (ผีกระหัง)
Attach `art/incoming/mobs/krahang.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the Thai flying ghost with the winnowing-basket wings riding the rice pestle, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit, the baskets fly loose, it falls off the pestle and drops to the ground, lying still in the last frame.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### krahang hurt (ผีกระหัง)
Attach `art/incoming/mobs/krahang.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the Thai flying ghost with the winnowing-basket wings riding the rice pestle, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit (owner 2026-11-09 "โดนโจมตีแล้วสะดุ้ง"): frame 1 the ready pose, frame 2 a sharp flinch backward with its eyes squeezed shut, frame 3 knocked further back and leaning away, frame 4 staggering, frame 5 regaining its balance, frame 6 back to the ready pose. Short and snappy.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### khamot walk (ผีโขมด)
Attach `art/incoming/mobs/khamot.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the floating ball of pale green ghost fire with the grinning face, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it floats forward bobbing up and down, the flame flickering and the flame tail trailing. A smooth loop: frame 6 flows back into frame 1. It walks in place (it does not travel across the cells).
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### khamot attack (ผีโขมด)
Attach `art/incoming/mobs/khamot.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the floating ball of pale green ghost fire with the grinning face, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it shrinks and pulls back, then shoots forward stretching into a long fireball with a wide grin (furthest forward in frame 4), then snaps back to a round ball. Frames 1 and 6 show the ready pose; frames 2-3 are the wind-up, frame 4 is the hit, frame 5 the follow-through.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### khamot death (ผีโขมด)
Attach `art/incoming/mobs/khamot.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the floating ball of pale green ghost fire with the grinning face, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit, flickers, shrinks smaller and smaller and goes out into a last tiny wisp in the last frame.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### khamot hurt (ผีโขมด)
Attach `art/incoming/mobs/khamot.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the floating ball of pale green ghost fire with the grinning face, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit (owner 2026-11-09 "โดนโจมตีแล้วสะดุ้ง"): frame 1 the ready pose, frame 2 a sharp flinch backward with its eyes squeezed shut, frame 3 knocked further back and leaning away, frame 4 staggering, frame 5 regaining its balance, frame 6 back to the ready pose. Short and snappy.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### phrai walk (พรายน้ำ)
Attach `art/incoming/mobs/phrai.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the pale Thai river water spirit with very long dripping black hair, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: a slow eerie glide forward, the long hair swaying, water dripping. A smooth loop: frame 6 flows back into frame 1. It walks in place (it does not travel across the cells).
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### phrai attack (พรายน้ำ)
Attach `art/incoming/mobs/phrai.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the pale Thai river water spirit with very long dripping black hair, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: she leans back, then lunges forward reaching with both pale hands while her long hair whips forward (furthest reach in frame 4), then drifts back. Frames 1 and 6 show the ready pose; frames 2-3 are the wind-up, frame 4 is the hit, frame 5 the follow-through.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### phrai death (พรายน้ำ)
Attach `art/incoming/mobs/phrai.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the pale Thai river water spirit with very long dripping black hair, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: she gets hit, recoils, sinks down and melts into a puddle of water with her hair spread out in the last frame.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### phrai hurt (พรายน้ำ)
Attach `art/incoming/mobs/phrai.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the pale Thai river water spirit with very long dripping black hair, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit (owner 2026-11-09 "โดนโจมตีแล้วสะดุ้ง"): frame 1 the ready pose, frame 2 a sharp flinch backward with its eyes squeezed shut, frame 3 knocked further back and leaning away, frame 4 staggering, frame 5 regaining its balance, frame 6 back to the ready pose. Short and snappy.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### pret walk (เปรต)
Attach `art/incoming/mobs/pret.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the extremely tall thin Thai hungry ghost, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: a slow swaying walk on long thin legs, the long arms hanging and swinging. A smooth loop: frame 6 flows back into frame 1. It walks in place (it does not travel across the cells).
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### pret attack (เปรต)
Attach `art/incoming/mobs/pret.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the extremely tall thin Thai hungry ghost, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it bends down and reaches far forward with both very long thin arms to grab (furthest reach in frame 4), then straightens up. Frames 1 and 6 show the ready pose; frames 2-3 are the wind-up, frame 4 is the hit, frame 5 the follow-through.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### pret death (เปรต)
Attach `art/incoming/mobs/pret.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the extremely tall thin Thai hungry ghost, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit, folds up at the knees and collapses in a heap of long thin limbs, lying still in the last frame.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### pret hurt (เปรต)
Attach `art/incoming/mobs/pret.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the extremely tall thin Thai hungry ghost, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit (owner 2026-11-09 "โดนโจมตีแล้วสะดุ้ง"): frame 1 the ready pose, frame 2 a sharp flinch backward with its eyes squeezed shut, frame 3 knocked further back and leaning away, frame 4 staggering, frame 5 regaining its balance, frame 6 back to the ready pose. Short and snappy.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### monkey walk (ลิงโจร)
Attach `art/incoming/mobs/monkey.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the mischievous macaque bandit with the red headcloth and the bag of fruit, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: a cheeky bouncy walk, tail swinging, the bag bouncing on the hip. A smooth loop: frame 6 flows back into frame 1. It walks in place (it does not travel across the cells).
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### monkey attack (ลิงโจร)
Attach `art/incoming/mobs/monkey.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the mischievous macaque bandit with the red headcloth and the bag of fruit, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it pulls a fruit from the bag, winds up and throws it overhand forward (the fruit leaves its hand in frame 4), then laughs in the ready pose. Frames 1 and 6 show the ready pose; frames 2-3 are the wind-up, frame 4 is the hit, frame 5 the follow-through.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### monkey death (ลิงโจร)
Attach `art/incoming/mobs/monkey.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the mischievous macaque bandit with the red headcloth and the bag of fruit, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit, tumbles backward, fruit spilling from the bag, and lies still on its back in the last frame.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### monkey hurt (ลิงโจร)
Attach `art/incoming/mobs/monkey.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the mischievous macaque bandit with the red headcloth and the bag of fruit, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit (owner 2026-11-09 "โดนโจมตีแล้วสะดุ้ง"): frame 1 the ready pose, frame 2 a sharp flinch backward with its eyes squeezed shut, frame 3 knocked further back and leaning away, frame 4 staggering, frame 5 regaining its balance, frame 6 back to the ready pose. Short and snappy.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### croc_guard walk (ทหารจระเข้)
Attach `art/incoming/mobs/croc_guard.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the crocodile-headed warrior with the bronze armour and the long Thai glaive, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: a heavy marching walk, the glaive held upright, the tail swaying behind. A smooth loop: frame 6 flows back into frame 1. It walks in place (it does not travel across the cells).
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### croc_guard attack (ทหารจระเข้)
Attach `art/incoming/mobs/croc_guard.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the crocodile-headed warrior with the bronze armour and the long Thai glaive, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it lowers the glaive and thrusts it forward with a step (the blade furthest forward in frame 4), then pulls it back upright. Frames 1 and 6 show the ready pose; frames 2-3 are the wind-up, frame 4 is the hit, frame 5 the follow-through.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### croc_guard death (ทหารจระเข้)
Attach `art/incoming/mobs/croc_guard.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the crocodile-headed warrior with the bronze armour and the long Thai glaive, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit, staggers, drops the glaive and falls forward onto its belly, lying still in the last frame.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### croc_guard hurt (ทหารจระเข้)
Attach `art/incoming/mobs/croc_guard.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the crocodile-headed warrior with the bronze armour and the long Thai glaive, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit (owner 2026-11-09 "โดนโจมตีแล้วสะดุ้ง"): frame 1 the ready pose, frame 2 a sharp flinch backward with its eyes squeezed shut, frame 3 knocked further back and leaning away, frame 4 staggering, frame 5 regaining its balance, frame 6 back to the ready pose. Short and snappy.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### boss_chalawan walk (บอสชาละวัน)
Attach `art/incoming/mobs/boss_chalawan.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is Chalawan the crocodile king with the gold Thai crown and two curved swords, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: a proud heavy walk, the long tail swaying, both swords held ready. A smooth loop: frame 6 flows back into frame 1. It walks in place (it does not travel across the cells).
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### boss_chalawan attack (บอสชาละวัน)
Attach `art/incoming/mobs/boss_chalawan.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is Chalawan the crocodile king with the gold Thai crown and two curved swords, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: he raises both curved swords, then steps forward and slashes them down crossing in front of him (the swords furthest forward in frame 4), then returns to the ready stance. Frames 1 and 6 show the ready pose; frames 2-3 are the wind-up, frame 4 is the hit, frame 5 the follow-through.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### boss_chalawan death (บอสชาละวัน)
Attach `art/incoming/mobs/boss_chalawan.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is Chalawan the crocodile king with the gold Thai crown and two curved swords, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: he gets hit, roars, drops to his knees, the swords fall and he crashes onto his side, the crown rolling off, in the last frame.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### boss_chalawan hurt (บอสชาละวัน)
Attach `art/incoming/mobs/boss_chalawan.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is Chalawan the crocodile king with the gold Thai crown and two curved swords, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit (owner 2026-11-09 "โดนโจมตีแล้วสะดุ้ง"): frame 1 the ready pose, frame 2 a sharp flinch backward with its eyes squeezed shut, frame 3 knocked further back and leaning away, frame 4 staggering, frame 5 regaining its balance, frame 6 back to the ready pose. Short and snappy.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### jiangshi walk (ผีกระโดดจีน)
Attach `art/incoming/mobs/jiangshi.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the Chinese hopping vampire with the talisman on its forehead, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it hops forward with both feet together, stiff body, arms stretched out in front, the talisman flapping at each hop. A smooth loop: frame 6 flows back into frame 1. It walks in place (it does not travel across the cells).
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### jiangshi attack (ผีกระโดดจีน)
Attach `art/incoming/mobs/jiangshi.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the Chinese hopping vampire with the talisman on its forehead, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it crouches, then makes a big stiff hop forward and claws down with both outstretched arms (the claws furthest forward in frame 4), then lands back. Frames 1 and 6 show the ready pose; frames 2-3 are the wind-up, frame 4 is the hit, frame 5 the follow-through.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### jiangshi death (ผีกระโดดจีน)
Attach `art/incoming/mobs/jiangshi.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the Chinese hopping vampire with the talisman on its forehead, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit, the talisman flies off, it goes rigid and topples straight over backward like a plank, lying still in the last frame.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### jiangshi hurt (ผีกระโดดจีน)
Attach `art/incoming/mobs/jiangshi.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the Chinese hopping vampire with the talisman on its forehead, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit (owner 2026-11-09 "โดนโจมตีแล้วสะดุ้ง"): frame 1 the ready pose, frame 2 a sharp flinch backward with its eyes squeezed shut, frame 3 knocked further back and leaning away, frame 4 staggering, frame 5 regaining its balance, frame 6 back to the ready pose. Short and snappy.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### paper_doll walk (ตุ๊กตากระดาษ)
Attach `art/incoming/mobs/paper_doll.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the small paper effigy servant, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it scurries forward in quick light steps, the paper sleeves fluttering. A smooth loop: frame 6 flows back into frame 1. It walks in place (it does not travel across the cells).
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### paper_doll attack (ตุ๊กตากระดาษ)
Attach `art/incoming/mobs/paper_doll.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the small paper effigy servant, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it leans back, then lunges forward slicing with the paper fan (the fan furthest forward in frame 4), then pulls back. Frames 1 and 6 show the ready pose; frames 2-3 are the wind-up, frame 4 is the hit, frame 5 the follow-through.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### paper_doll death (ตุ๊กตากระดาษ)
Attach `art/incoming/mobs/paper_doll.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the small paper effigy servant, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit, tears, crumples up into a ball of paper and falls flat in the last frame.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### paper_doll hurt (ตุ๊กตากระดาษ)
Attach `art/incoming/mobs/paper_doll.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the small paper effigy servant, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit (owner 2026-11-09 "โดนโจมตีแล้วสะดุ้ง"): frame 1 the ready pose, frame 2 a sharp flinch backward with its eyes squeezed shut, frame 3 knocked further back and leaning away, frame 4 staggering, frame 5 regaining its balance, frame 6 back to the ready pose. Short and snappy.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### terracotta_archer walk (ทหารดินเผานักธนู)
Attach `art/incoming/mobs/terracotta_archer.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the clay soldier archer with the crossbow, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: a stiff marching walk, the crossbow held across the body. A smooth loop: frame 6 flows back into frame 1. It walks in place (it does not travel across the cells).
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### terracotta_archer attack (ทหารดินเผานักธนู)
Attach `art/incoming/mobs/terracotta_archer.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the clay soldier archer with the crossbow, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it raises the crossbow, aims forward, shoots (the bolt leaves the frame, the crossbow kicks back in frame 4), then lowers it; bolts always point forward with the head at the front. Frames 1 and 6 show the ready pose; frames 2-3 are the wind-up, frame 4 is the hit, frame 5 the follow-through.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### terracotta_archer death (ทหารดินเผานักธนู)
Attach `art/incoming/mobs/terracotta_archer.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the clay soldier archer with the crossbow, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit, cracks spread over its body and it crumbles into a pile of clay pieces in the last frame.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### terracotta_archer hurt (ทหารดินเผานักธนู)
Attach `art/incoming/mobs/terracotta_archer.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the clay soldier archer with the crossbow, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit (owner 2026-11-09 "โดนโจมตีแล้วสะดุ้ง"): frame 1 the ready pose, frame 2 a sharp flinch backward with its eyes squeezed shut, frame 3 knocked further back and leaning away, frame 4 staggering, frame 5 regaining its balance, frame 6 back to the ready pose. Short and snappy.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### terracotta_general walk (นายพลดินเผา)
Attach `art/incoming/mobs/terracotta_general.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the big clay general with the bronze halberd, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: a heavy slow march, the halberd held upright, the armour plates clacking. A smooth loop: frame 6 flows back into frame 1. It walks in place (it does not travel across the cells).
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### terracotta_general attack (นายพลดินเผา)
Attach `art/incoming/mobs/terracotta_general.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the big clay general with the bronze halberd, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it raises the halberd high, then swings it down and forward in a big chop (the blade furthest forward in frame 4), then lifts it back up. Frames 1 and 6 show the ready pose; frames 2-3 are the wind-up, frame 4 is the hit, frame 5 the follow-through.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### terracotta_general death (นายพลดินเผา)
Attach `art/incoming/mobs/terracotta_general.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the big clay general with the bronze halberd, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit, cracks, drops the halberd and breaks apart into big clay chunks in the last frame.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### terracotta_general hurt (นายพลดินเผา)
Attach `art/incoming/mobs/terracotta_general.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the big clay general with the bronze halberd, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit (owner 2026-11-09 "โดนโจมตีแล้วสะดุ้ง"): frame 1 the ready pose, frame 2 a sharp flinch backward with its eyes squeezed shut, frame 3 knocked further back and leaning away, frame 4 staggering, frame 5 regaining its balance, frame 6 back to the ready pose. Short and snappy.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### fox_spirit walk (ปีศาจจิ้งจอก)
Attach `art/incoming/mobs/fox_spirit.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the white three-tailed fox demon, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: a light prancing walk on its hind legs, the three tails swaying. A smooth loop: frame 6 flows back into frame 1. It walks in place (it does not travel across the cells).
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### fox_spirit attack (ปีศาจจิ้งจอก)
Attach `art/incoming/mobs/fox_spirit.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the white three-tailed fox demon, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it raises one paw gathering blue fox-fire, then flicks the paw forward to throw it (the paw furthest forward in frame 4), then settles back. Frames 1 and 6 show the ready pose; frames 2-3 are the wind-up, frame 4 is the hit, frame 5 the follow-through.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### fox_spirit death (ปีศาจจิ้งจอก)
Attach `art/incoming/mobs/fox_spirit.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the white three-tailed fox demon, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit, yelps, spins and collapses onto its side, its tails limp, in the last frame.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### fox_spirit hurt (ปีศาจจิ้งจอก)
Attach `art/incoming/mobs/fox_spirit.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the white three-tailed fox demon, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit (owner 2026-11-09 "โดนโจมตีแล้วสะดุ้ง"): frame 1 the ready pose, frame 2 a sharp flinch backward with its eyes squeezed shut, frame 3 knocked further back and leaning away, frame 4 staggering, frame 5 regaining its balance, frame 6 back to the ready pose. Short and snappy.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### toad_demon walk (ปีศาจคางคก)
Attach `art/incoming/mobs/toad_demon.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the fat toad demon with the long tongue, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: a heavy waddle forward, belly bouncing. A smooth loop: frame 6 flows back into frame 1. It walks in place (it does not travel across the cells).
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### toad_demon attack (ปีศาจคางคก)
Attach `art/incoming/mobs/toad_demon.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the fat toad demon with the long tongue, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it puffs up its throat, then shoots its long sticky tongue straight forward (the tongue at full length in frame 4), then pulls it back in. Frames 1 and 6 show the ready pose; frames 2-3 are the wind-up, frame 4 is the hit, frame 5 the follow-through.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### toad_demon death (ปีศาจคางคก)
Attach `art/incoming/mobs/toad_demon.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the fat toad demon with the long tongue, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit, deflates, flops onto its back with its legs up, lying still in the last frame.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### toad_demon hurt (ปีศาจคางคก)
Attach `art/incoming/mobs/toad_demon.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the fat toad demon with the long tongue, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit (owner 2026-11-09 "โดนโจมตีแล้วสะดุ้ง"): frame 1 the ready pose, frame 2 a sharp flinch backward with its eyes squeezed shut, frame 3 knocked further back and leaning away, frame 4 staggering, frame 5 regaining its balance, frame 6 back to the ready pose. Short and snappy.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### boss_nian walk (บอสเหนียนโซ่ว)
Attach `art/incoming/mobs/boss_nian.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is Nian, the huge red and gold New Year beast on four legs, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: a heavy prowling walk on four legs, the mane bouncing. A smooth loop: frame 6 flows back into frame 1. It walks in place (it does not travel across the cells).
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### boss_nian attack (บอสเหนียนโซ่ว)
Attach `art/incoming/mobs/boss_nian.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is Nian, the huge red and gold New Year beast on four legs, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it rears up on its hind legs, then slams down forward with both front paws and a roaring bite (furthest forward in frame 4), then steps back. Frames 1 and 6 show the ready pose; frames 2-3 are the wind-up, frame 4 is the hit, frame 5 the follow-through.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### boss_nian death (บอสเหนียนโซ่ว)
Attach `art/incoming/mobs/boss_nian.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is Nian, the huge red and gold New Year beast on four legs, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit, staggers, its legs give way and it slumps to the ground, lying still in the last frame.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### boss_nian hurt (บอสเหนียนโซ่ว)
Attach `art/incoming/mobs/boss_nian.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is Nian, the huge red and gold New Year beast on four legs, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit (owner 2026-11-09 "โดนโจมตีแล้วสะดุ้ง"): frame 1 the ready pose, frame 2 a sharp flinch backward with its eyes squeezed shut, frame 3 knocked further back and leaning away, frame 4 staggering, frame 5 regaining its balance, frame 6 back to the ready pose. Short and snappy.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### kappa walk (กัปปะ)
Attach `art/incoming/mobs/kappa.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a small river kappa, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: a waddling walk, the water in its head dish sloshing. A smooth loop: frame 6 flows back into frame 1. It walks in place (it does not travel across the cells).
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### kappa attack (กัปปะ)
Attach `art/incoming/mobs/kappa.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a small river kappa, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it lunges forward and slaps with a webbed hand (the hand furthest forward in frame 4), then hops back. Frames 1 and 6 show the ready pose; frames 2-3 are the wind-up, frame 4 is the hit, frame 5 the follow-through.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### kappa death (กัปปะ)
Attach `art/incoming/mobs/kappa.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a small river kappa, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit, the water spills from its head dish, it wobbles and flops onto its shell, lying still in the last frame.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### kappa hurt (กัปปะ)
Attach `art/incoming/mobs/kappa.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a small river kappa, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit (owner 2026-11-09 "โดนโจมตีแล้วสะดุ้ง"): frame 1 the ready pose, frame 2 a sharp flinch backward with its eyes squeezed shut, frame 3 knocked further back and leaning away, frame 4 staggering, frame 5 regaining its balance, frame 6 back to the ready pose. Short and snappy.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### kasa_obake walk (ร่มผี)
Attach `art/incoming/mobs/kasa_obake.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a haunted paper umbrella yokai, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it hops forward on its one leg, the umbrella bouncing open and shut a little. A smooth loop: frame 6 flows back into frame 1. It walks in place (it does not travel across the cells).
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### kasa_obake attack (ร่มผี)
Attach `art/incoming/mobs/kasa_obake.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a haunted paper umbrella yokai, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it spins and lashes its long tongue forward (the tongue at full length in frame 4), then rolls it back. Frames 1 and 6 show the ready pose; frames 2-3 are the wind-up, frame 4 is the hit, frame 5 the follow-through.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### kasa_obake death (ร่มผี)
Attach `art/incoming/mobs/kasa_obake.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a haunted paper umbrella yokai, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit, the paper tears, it folds shut and topples over, lying still in the last frame.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### kasa_obake hurt (ร่มผี)
Attach `art/incoming/mobs/kasa_obake.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a haunted paper umbrella yokai, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit (owner 2026-11-09 "โดนโจมตีแล้วสะดุ้ง"): frame 1 the ready pose, frame 2 a sharp flinch backward with its eyes squeezed shut, frame 3 knocked further back and leaning away, frame 4 staggering, frame 5 regaining its balance, frame 6 back to the ready pose. Short and snappy.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### oni walk (ยักษ์โอนิ)
Attach `art/incoming/mobs/oni.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a big red oni ogre, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: a heavy stomping walk, the club over its shoulder. A smooth loop: frame 6 flows back into frame 1. It walks in place (it does not travel across the cells).
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### oni attack (ยักษ์โอนิ)
Attach `art/incoming/mobs/oni.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a big red oni ogre, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it raises the spiked club high and smashes it down in front of it (the club hits the ground in frame 4), then lifts it again. Frames 1 and 6 show the ready pose; frames 2-3 are the wind-up, frame 4 is the hit, frame 5 the follow-through.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### oni death (ยักษ์โอนิ)
Attach `art/incoming/mobs/oni.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a big red oni ogre, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit, staggers, drops the club and falls forward, lying still in the last frame.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### oni hurt (ยักษ์โอนิ)
Attach `art/incoming/mobs/oni.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a big red oni ogre, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit (owner 2026-11-09 "โดนโจมตีแล้วสะดุ้ง"): frame 1 the ready pose, frame 2 a sharp flinch backward with its eyes squeezed shut, frame 3 knocked further back and leaning away, frame 4 staggering, frame 5 regaining its balance, frame 6 back to the ready pose. Short and snappy.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### tengu walk (นกเทงงู)
Attach `art/incoming/mobs/tengu.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a crow tengu, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: a quick walk with the wings half spread, robes swaying. A smooth loop: frame 6 flows back into frame 1. It walks in place (it does not travel across the cells).
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### tengu attack (นกเทงงู)
Attach `art/incoming/mobs/tengu.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a crow tengu, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it leaps forward with the wings spread and slashes down with the sword (the blade furthest forward in frame 4), then lands back. Frames 1 and 6 show the ready pose; frames 2-3 are the wind-up, frame 4 is the hit, frame 5 the follow-through.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### tengu death (นกเทงงู)
Attach `art/incoming/mobs/tengu.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a crow tengu, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit, feathers burst off, it falls to its knees and collapses onto its side, lying still in the last frame.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### tengu hurt (นกเทงงู)
Attach `art/incoming/mobs/tengu.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a crow tengu, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit (owner 2026-11-09 "โดนโจมตีแล้วสะดุ้ง"): frame 1 the ready pose, frame 2 a sharp flinch backward with its eyes squeezed shut, frame 3 knocked further back and leaning away, frame 4 staggering, frame 5 regaining its balance, frame 6 back to the ready pose. Short and snappy.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### rokurokubi walk (ผีคอยาว)
Attach `art/incoming/mobs/rokurokubi.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a long-necked rokurokubi ghost woman, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: a slow shuffling walk, the long neck swaying the head left and right. A smooth loop: frame 6 flows back into frame 1. It walks in place (it does not travel across the cells).
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### rokurokubi attack (ผีคอยาว)
Attach `art/incoming/mobs/rokurokubi.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a long-necked rokurokubi ghost woman, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: the long neck shoots forward and the head bites at the enemy in front (the head furthest forward in frame 4), then the neck pulls back. Frames 1 and 6 show the ready pose; frames 2-3 are the wind-up, frame 4 is the hit, frame 5 the follow-through.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### rokurokubi death (ผีคอยาว)
Attach `art/incoming/mobs/rokurokubi.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a long-necked rokurokubi ghost woman, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: she gets hit, the neck snaps back short, she sinks down and lies in a heap of kimono in the last frame.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### rokurokubi hurt (ผีคอยาว)
Attach `art/incoming/mobs/rokurokubi.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a long-necked rokurokubi ghost woman, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit (owner 2026-11-09 "โดนโจมตีแล้วสะดุ้ง"): frame 1 the ready pose, frame 2 a sharp flinch backward with its eyes squeezed shut, frame 3 knocked further back and leaning away, frame 4 staggering, frame 5 regaining its balance, frame 6 back to the ready pose. Short and snappy.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### nekomata walk (แมวสองหาง)
Attach `art/incoming/mobs/nekomata.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a nekomata cat demon on its hind legs, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: a sly prowling walk on its hind legs, both tails swishing. A smooth loop: frame 6 flows back into frame 1. It walks in place (it does not travel across the cells).
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### nekomata attack (แมวสองหาง)
Attach `art/incoming/mobs/nekomata.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a nekomata cat demon on its hind legs, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it pounces forward swiping with both claws (the claws furthest forward in frame 4), then lands crouched. Frames 1 and 6 show the ready pose; frames 2-3 are the wind-up, frame 4 is the hit, frame 5 the follow-through.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### nekomata death (แมวสองหาง)
Attach `art/incoming/mobs/nekomata.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a nekomata cat demon on its hind legs, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit, yowls, rolls over and lies still with its tails limp in the last frame.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### nekomata hurt (แมวสองหาง)
Attach `art/incoming/mobs/nekomata.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a nekomata cat demon on its hind legs, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit (owner 2026-11-09 "โดนโจมตีแล้วสะดุ้ง"): frame 1 the ready pose, frame 2 a sharp flinch backward with its eyes squeezed shut, frame 3 knocked further back and leaning away, frame 4 staggering, frame 5 regaining its balance, frame 6 back to the ready pose. Short and snappy.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### boss_orochi walk (บอสยามาตะโนะโอโรจิ)
Attach `art/incoming/mobs/boss_orochi.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the the boss, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: its coils slide forward, the heads swaying. A smooth loop: frame 6 flows back into frame 1. It walks in place (it does not travel across the cells).
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### boss_orochi attack (บอสยามาตะโนะโอโรจิ)
Attach `art/incoming/mobs/boss_orochi.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the the boss, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: the heads rear back then strike forward together (the heads furthest forward in frame 4), then pull back. Frames 1 and 6 show the ready pose; frames 2-3 are the wind-up, frame 4 is the hit, frame 5 the follow-through.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### boss_orochi death (บอสยามาตะโนะโอโรจิ)
Attach `art/incoming/mobs/boss_orochi.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the the boss, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit, the heads droop one by one and the body slumps into a still coil in the last frame.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### boss_orochi hurt (บอสยามาตะโนะโอโรจิ)
Attach `art/incoming/mobs/boss_orochi.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the the boss, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit (owner 2026-11-09 "โดนโจมตีแล้วสะดุ้ง"): frame 1 the ready pose, frame 2 a sharp flinch backward with its eyes squeezed shut, frame 3 knocked further back and leaning away, frame 4 staggering, frame 5 regaining its balance, frame 6 back to the ready pose. Short and snappy.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### mummy walk (มัมมี่)
Attach `art/incoming/mobs/mummy.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a shambling mummy, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: a slow stiff shamble, arms forward, loose bandages swaying. A smooth loop: frame 6 flows back into frame 1. It walks in place (it does not travel across the cells).
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### mummy attack (มัมมี่)
Attach `art/incoming/mobs/mummy.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a shambling mummy, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it lurches forward and swipes with both bandaged arms (furthest forward in frame 4), then steps back. Frames 1 and 6 show the ready pose; frames 2-3 are the wind-up, frame 4 is the hit, frame 5 the follow-through.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### mummy death (มัมมี่)
Attach `art/incoming/mobs/mummy.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a shambling mummy, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit, the bandages unravel and it collapses into a pile of bandages and dust in the last frame.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### mummy hurt (มัมมี่)
Attach `art/incoming/mobs/mummy.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a shambling mummy, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit (owner 2026-11-09 "โดนโจมตีแล้วสะดุ้ง"): frame 1 the ready pose, frame 2 a sharp flinch backward with its eyes squeezed shut, frame 3 knocked further back and leaning away, frame 4 staggering, frame 5 regaining its balance, frame 6 back to the ready pose. Short and snappy.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### scarab walk (ด้วงสการับ)
Attach `art/incoming/mobs/scarab.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a big glossy scarab beetle, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: a quick scuttling walk on six legs. A smooth loop: frame 6 flows back into frame 1. It walks in place (it does not travel across the cells).
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### scarab attack (ด้วงสการับ)
Attach `art/incoming/mobs/scarab.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a big glossy scarab beetle, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it rears up and charges forward snapping its mandibles (furthest forward in frame 4), then backs off. Frames 1 and 6 show the ready pose; frames 2-3 are the wind-up, frame 4 is the hit, frame 5 the follow-through.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### scarab death (ด้วงสการับ)
Attach `art/incoming/mobs/scarab.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a big glossy scarab beetle, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit, flips onto its back with its legs curled, lying still in the last frame.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### scarab hurt (ด้วงสการับ)
Attach `art/incoming/mobs/scarab.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a big glossy scarab beetle, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit (owner 2026-11-09 "โดนโจมตีแล้วสะดุ้ง"): frame 1 the ready pose, frame 2 a sharp flinch backward with its eyes squeezed shut, frame 3 knocked further back and leaning away, frame 4 staggering, frame 5 regaining its balance, frame 6 back to the ready pose. Short and snappy.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### jackal_warrior walk (นักรบหัวหมาจิ้งจอก)
Attach `art/incoming/mobs/jackal_warrior.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a jackal-headed warrior (a soldier, not a god), exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: a disciplined marching walk, the shield held in front. A smooth loop: frame 6 flows back into frame 1. It walks in place (it does not travel across the cells).
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### jackal_warrior attack (นักรบหัวหมาจิ้งจอก)
Attach `art/incoming/mobs/jackal_warrior.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a jackal-headed warrior (a soldier, not a god), exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it steps in and slashes forward with the khopesh (the blade furthest forward in frame 4), then guards again. Frames 1 and 6 show the ready pose; frames 2-3 are the wind-up, frame 4 is the hit, frame 5 the follow-through.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### jackal_warrior death (นักรบหัวหมาจิ้งจอก)
Attach `art/incoming/mobs/jackal_warrior.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a jackal-headed warrior (a soldier, not a god), exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit, drops the khopesh and falls to the ground, lying still in the last frame.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### jackal_warrior hurt (นักรบหัวหมาจิ้งจอก)
Attach `art/incoming/mobs/jackal_warrior.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a jackal-headed warrior (a soldier, not a god), exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit (owner 2026-11-09 "โดนโจมตีแล้วสะดุ้ง"): frame 1 the ready pose, frame 2 a sharp flinch backward with its eyes squeezed shut, frame 3 knocked further back and leaning away, frame 4 staggering, frame 5 regaining its balance, frame 6 back to the ready pose. Short and snappy.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### sand_scorpion walk (แมงป่องทะเลทราย)
Attach `art/incoming/mobs/sand_scorpion.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a big desert scorpion, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it scuttles forward on eight legs, the tail swaying. A smooth loop: frame 6 flows back into frame 1. It walks in place (it does not travel across the cells).
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### sand_scorpion attack (แมงป่องทะเลทราย)
Attach `art/incoming/mobs/sand_scorpion.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a big desert scorpion, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it raises its tail high and stabs the stinger down forward (the stinger furthest forward in frame 4), then lifts it again. Frames 1 and 6 show the ready pose; frames 2-3 are the wind-up, frame 4 is the hit, frame 5 the follow-through.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### sand_scorpion death (แมงป่องทะเลทราย)
Attach `art/incoming/mobs/sand_scorpion.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a big desert scorpion, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit, curls up its legs and tail and lies still in the last frame.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### sand_scorpion hurt (แมงป่องทะเลทราย)
Attach `art/incoming/mobs/sand_scorpion.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a big desert scorpion, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit (owner 2026-11-09 "โดนโจมตีแล้วสะดุ้ง"): frame 1 the ready pose, frame 2 a sharp flinch backward with its eyes squeezed shut, frame 3 knocked further back and leaning away, frame 4 staggering, frame 5 regaining its balance, frame 6 back to the ready pose. Short and snappy.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### cobra_priest walk (นักบวชงูเห่า)
Attach `art/incoming/mobs/cobra_priest.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a cobra-hooded serpent priest, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it slithers forward upright, the hood flaring. A smooth loop: frame 6 flows back into frame 1. It walks in place (it does not travel across the cells).
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### cobra_priest attack (นักบวชงูเห่า)
Attach `art/incoming/mobs/cobra_priest.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a cobra-hooded serpent priest, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it raises the staff and thrusts it forward casting (the staff furthest forward in frame 4), then lowers it. Frames 1 and 6 show the ready pose; frames 2-3 are the wind-up, frame 4 is the hit, frame 5 the follow-through.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### cobra_priest death (นักบวชงูเห่า)
Attach `art/incoming/mobs/cobra_priest.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a cobra-hooded serpent priest, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit, the hood folds and it coils down onto the ground, lying still in the last frame.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### cobra_priest hurt (นักบวชงูเห่า)
Attach `art/incoming/mobs/cobra_priest.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a cobra-hooded serpent priest, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit (owner 2026-11-09 "โดนโจมตีแล้วสะดุ้ง"): frame 1 the ready pose, frame 2 a sharp flinch backward with its eyes squeezed shut, frame 3 knocked further back and leaning away, frame 4 staggering, frame 5 regaining its balance, frame 6 back to the ready pose. Short and snappy.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### sand_golem walk (โกเลมทราย)
Attach `art/incoming/mobs/sand_golem.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is a big golem made of packed desert sand and sandstone blocks, carved hieroglyph patterns on its chest glowing amber, sand trickling from its joints, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: a heavy slow walk, sand spilling at each step. A smooth loop: frame 6 flows back into frame 1. It walks in place (it does not travel across the cells).
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### sand_golem attack (โกเลมทราย)
Attach `art/incoming/mobs/sand_golem.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is a big golem made of packed desert sand and sandstone blocks, carved hieroglyph patterns on its chest glowing amber, sand trickling from its joints, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it swings a huge sandstone fist forward (the fist furthest forward in frame 4), then pulls back. Frames 1 and 6 show the ready pose; frames 2-3 are the wind-up, frame 4 is the hit, frame 5 the follow-through.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### sand_golem death (โกเลมทราย)
Attach `art/incoming/mobs/sand_golem.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is a big golem made of packed desert sand and sandstone blocks, carved hieroglyph patterns on its chest glowing amber, sand trickling from its joints, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit, cracks and crumbles into a pile of sand and blocks in the last frame.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### sand_golem hurt (โกเลมทราย)
Attach `art/incoming/mobs/sand_golem.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is a big golem made of packed desert sand and sandstone blocks, carved hieroglyph patterns on its chest glowing amber, sand trickling from its joints, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit (owner 2026-11-09 "โดนโจมตีแล้วสะดุ้ง"): frame 1 the ready pose, frame 2 a sharp flinch backward with its eyes squeezed shut, frame 3 knocked further back and leaning away, frame 4 staggering, frame 5 regaining its balance, frame 6 back to the ready pose. Short and snappy.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### boss_sphinx walk (บอสสฟิงซ์)
Attach `art/incoming/mobs/boss_sphinx.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the the boss, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: a heavy prowling walk on four legs, sand pouring. A smooth loop: frame 6 flows back into frame 1. It walks in place (it does not travel across the cells).
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### boss_sphinx attack (บอสสฟิงซ์)
Attach `art/incoming/mobs/boss_sphinx.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the the boss, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it rears up and slams both front paws down forward (the paws hit the ground in frame 4), then steps back. Frames 1 and 6 show the ready pose; frames 2-3 are the wind-up, frame 4 is the hit, frame 5 the follow-through.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### boss_sphinx death (บอสสฟิงซ์)
Attach `art/incoming/mobs/boss_sphinx.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the the boss, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit, cracks spread and it slumps down into a heap of sandstone in the last frame.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### boss_sphinx hurt (บอสสฟิงซ์)
Attach `art/incoming/mobs/boss_sphinx.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the the boss, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit (owner 2026-11-09 "โดนโจมตีแล้วสะดุ้ง"): frame 1 the ready pose, frame 2 a sharp flinch backward with its eyes squeezed shut, frame 3 knocked further back and leaning away, frame 4 staggering, frame 5 regaining its balance, frame 6 back to the ready pose. Short and snappy.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### draugr walk (ดรากร์)
Attach `art/incoming/mobs/draugr.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a draugr, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: a stiff heavy march, frost drifting off its body. A smooth loop: frame 6 flows back into frame 1. It walks in place (it does not travel across the cells).
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### draugr attack (ดรากร์)
Attach `art/incoming/mobs/draugr.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a draugr, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it raises the axe and chops down forward (the axe furthest forward in frame 4), then lifts it again. Frames 1 and 6 show the ready pose; frames 2-3 are the wind-up, frame 4 is the hit, frame 5 the follow-through.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### draugr death (ดรากร์)
Attach `art/incoming/mobs/draugr.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a draugr, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit, the glow in its eyes fades and it crumbles to the ground, lying still in the last frame.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### draugr hurt (ดรากร์)
Attach `art/incoming/mobs/draugr.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a draugr, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit (owner 2026-11-09 "โดนโจมตีแล้วสะดุ้ง"): frame 1 the ready pose, frame 2 a sharp flinch backward with its eyes squeezed shut, frame 3 knocked further back and leaning away, frame 4 staggering, frame 5 regaining its balance, frame 6 back to the ready pose. Short and snappy.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### frost_wolf walk (หมาป่าหิมะ)
Attach `art/incoming/mobs/frost_wolf.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a frost wolf, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: a fast trot on four legs, snow puffing at its paws. A smooth loop: frame 6 flows back into frame 1. It walks in place (it does not travel across the cells).
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### frost_wolf attack (หมาป่าหิมะ)
Attach `art/incoming/mobs/frost_wolf.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a frost wolf, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it crouches then lunges with jaws open for a bite (the furthest reach in frame 4), then lands back. Frames 1 and 6 show the ready pose; frames 2-3 are the wind-up, frame 4 is the hit, frame 5 the follow-through.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### frost_wolf death (หมาป่าหิมะ)
Attach `art/incoming/mobs/frost_wolf.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a frost wolf, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit, yelps, its legs buckle and it collapses onto its side, lying still in the last frame.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### frost_wolf hurt (หมาป่าหิมะ)
Attach `art/incoming/mobs/frost_wolf.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a frost wolf, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit (owner 2026-11-09 "โดนโจมตีแล้วสะดุ้ง"): frame 1 the ready pose, frame 2 a sharp flinch backward with its eyes squeezed shut, frame 3 knocked further back and leaning away, frame 4 staggering, frame 5 regaining its balance, frame 6 back to the ready pose. Short and snappy.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### troll walk (โทรลล์)
Attach `art/incoming/mobs/troll.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a big mountain troll, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: a lumbering walk, the club dragging. A smooth loop: frame 6 flows back into frame 1. It walks in place (it does not travel across the cells).
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### troll attack (โทรลล์)
Attach `art/incoming/mobs/troll.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a big mountain troll, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it lifts the tree-trunk club and swings it down in a big arc in front (the club hits the ground in frame 4), then lifts it again. Frames 1 and 6 show the ready pose; frames 2-3 are the wind-up, frame 4 is the hit, frame 5 the follow-through.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### troll death (โทรลล์)
Attach `art/incoming/mobs/troll.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a big mountain troll, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit, staggers and falls over backward, lying still in the last frame.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### troll hurt (โทรลล์)
Attach `art/incoming/mobs/troll.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a big mountain troll, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit (owner 2026-11-09 "โดนโจมตีแล้วสะดุ้ง"): frame 1 the ready pose, frame 2 a sharp flinch backward with its eyes squeezed shut, frame 3 knocked further back and leaning away, frame 4 staggering, frame 5 regaining its balance, frame 6 back to the ready pose. Short and snappy.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### ice_wraith walk (วิญญาณน้ำแข็ง)
Attach `art/incoming/mobs/ice_wraith.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a floating ice wraith, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it floats forward bobbing, snowflakes swirling. A smooth loop: frame 6 flows back into frame 1. It walks in place (it does not travel across the cells).
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### ice_wraith attack (วิญญาณน้ำแข็ง)
Attach `art/incoming/mobs/ice_wraith.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a floating ice wraith, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it rears back then slashes forward with its icy claws (the claws furthest forward in frame 4), then floats back. Frames 1 and 6 show the ready pose; frames 2-3 are the wind-up, frame 4 is the hit, frame 5 the follow-through.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### ice_wraith death (วิญญาณน้ำแข็ง)
Attach `art/incoming/mobs/ice_wraith.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a floating ice wraith, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit, shatters into ice shards and snowflakes that fall and fade in the last frame.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### ice_wraith hurt (วิญญาณน้ำแข็ง)
Attach `art/incoming/mobs/ice_wraith.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a floating ice wraith, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit (owner 2026-11-09 "โดนโจมตีแล้วสะดุ้ง"): frame 1 the ready pose, frame 2 a sharp flinch backward with its eyes squeezed shut, frame 3 knocked further back and leaning away, frame 4 staggering, frame 5 regaining its balance, frame 6 back to the ready pose. Short and snappy.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### dwarf_berserker walk (คนแคระคลั่ง)
Attach `art/incoming/mobs/dwarf_berserker.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a wild dwarf berserker, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: a fast angry stomping walk, the axes swinging. A smooth loop: frame 6 flows back into frame 1. It walks in place (it does not travel across the cells).
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### dwarf_berserker attack (คนแคระคลั่ง)
Attach `art/incoming/mobs/dwarf_berserker.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a wild dwarf berserker, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it spins and chops with both axes forward (the axes furthest forward in frame 4), then stops. Frames 1 and 6 show the ready pose; frames 2-3 are the wind-up, frame 4 is the hit, frame 5 the follow-through.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### dwarf_berserker death (คนแคระคลั่ง)
Attach `art/incoming/mobs/dwarf_berserker.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a wild dwarf berserker, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit, drops the axes and topples onto its back, lying still in the last frame.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### dwarf_berserker hurt (คนแคระคลั่ง)
Attach `art/incoming/mobs/dwarf_berserker.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the a wild dwarf berserker, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit (owner 2026-11-09 "โดนโจมตีแล้วสะดุ้ง"): frame 1 the ready pose, frame 2 a sharp flinch backward with its eyes squeezed shut, frame 3 knocked further back and leaning away, frame 4 staggering, frame 5 regaining its balance, frame 6 back to the ready pose. Short and snappy.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### ice_golem walk (โกเลมน้ำแข็ง)
Attach `art/incoming/mobs/ice_golem.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is a big golem of blue glacier ice and black rock, frost mist rising from it, a glowing cold-blue core in its chest, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: a heavy slow walk, frost mist trailing. A smooth loop: frame 6 flows back into frame 1. It walks in place (it does not travel across the cells).
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### ice_golem attack (โกเลมน้ำแข็ง)
Attach `art/incoming/mobs/ice_golem.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is a big golem of blue glacier ice and black rock, frost mist rising from it, a glowing cold-blue core in its chest, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it swings a huge ice fist forward (the fist furthest forward in frame 4), then pulls back. Frames 1 and 6 show the ready pose; frames 2-3 are the wind-up, frame 4 is the hit, frame 5 the follow-through.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### ice_golem death (โกเลมน้ำแข็ง)
Attach `art/incoming/mobs/ice_golem.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is a big golem of blue glacier ice and black rock, frost mist rising from it, a glowing cold-blue core in its chest, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit, cracks and shatters into ice chunks in the last frame.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### ice_golem hurt (โกเลมน้ำแข็ง)
Attach `art/incoming/mobs/ice_golem.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is a big golem of blue glacier ice and black rock, frost mist rising from it, a glowing cold-blue core in its chest, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit (owner 2026-11-09 "โดนโจมตีแล้วสะดุ้ง"): frame 1 the ready pose, frame 2 a sharp flinch backward with its eyes squeezed shut, frame 3 knocked further back and leaning away, frame 4 staggering, frame 5 regaining its balance, frame 6 back to the ready pose. Short and snappy.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### boss_jotun walk (บอสยักษ์น้ำแข็ง)
Attach `art/incoming/mobs/boss_jotun.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the the boss, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: a slow thunderous walk, frost cracking under its feet. A smooth loop: frame 6 flows back into frame 1. It walks in place (it does not travel across the cells).
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### boss_jotun attack (บอสยักษ์น้ำแข็ง)
Attach `art/incoming/mobs/boss_jotun.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the the boss, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it raises the ice hammer high and slams it down in front (the hammer hits the ground in frame 4), then lifts it. Frames 1 and 6 show the ready pose; frames 2-3 are the wind-up, frame 4 is the hit, frame 5 the follow-through.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### boss_jotun death (บอสยักษ์น้ำแข็ง)
Attach `art/incoming/mobs/boss_jotun.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the the boss, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit, falls to its knees and crashes forward, lying still in the last frame.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### boss_jotun hurt (บอสยักษ์น้ำแข็ง)
Attach `art/incoming/mobs/boss_jotun.png`.
```
Animation frames for a 2D action game, ONE picture. The monster is the the boss, exactly as in the attached picture: same face, colours, outfit and proportions, same art style (clean chibi cel-shaded illustration, thick dark outlines, flat colours).
Side view facing RIGHT in every frame, like the middle view of the attached picture.
Action: it gets hit (owner 2026-11-09 "โดนโจมตีแล้วสะดุ้ง"): frame 1 the ready pose, frame 2 a sharp flinch backward with its eyes squeezed shut, frame 3 knocked further back and leaning away, frame 4 staggering, frame 5 regaining its balance, frame 6 back to the ready pose. Short and snappy.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size with empty white space around the figure; nothing crosses into the next cell; the whole body stays inside its cell.
Same scale in every frame (the same size as in frame 1); the feet (or the lowest point) on the same ground line in every cell. Every frame must be a clearly DIFFERENT pose.
Plain pure white background, no grid lines, no numbers, no text, no shadow, no ground, no effects, no motion lines, no dust.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```
