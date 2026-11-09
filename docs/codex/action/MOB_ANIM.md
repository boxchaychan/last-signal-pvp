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
| 4 | wolf | walk | done | `art/incoming/mobs/anim/wolf_walk.png` |
| 5 | wolf | attack | done | `art/incoming/mobs/anim/wolf_attack.png` |
| 6 | wolf | death | done | `art/incoming/mobs/anim/wolf_death.png` |
| 7 | goblin_archer | walk | done | `art/incoming/mobs/anim/goblin_archer_walk.png` |
| 8 | goblin_archer | attack | done | `art/incoming/mobs/anim/goblin_archer_attack.png` |
| 9 | goblin_archer | death | done | `art/incoming/mobs/anim/goblin_archer_death.png` |
| 10 | boar_guard | walk | done | `art/incoming/mobs/anim/boar_guard_walk.png` |
| 11 | boar_guard | attack | done | `art/incoming/mobs/anim/boar_guard_attack.png` |
| 12 | boar_guard | death | done | `art/incoming/mobs/anim/boar_guard_death.png` |
| 13 | skeleton | walk | done | `art/incoming/mobs/anim/skeleton_walk.png` |
| 14 | skeleton | attack | done | `art/incoming/mobs/anim/skeleton_attack.png` |
| 15 | skeleton | death | done | `art/incoming/mobs/anim/skeleton_death.png` |
| 16 | wisp | walk | done | `art/incoming/mobs/anim/wisp_walk.png` |
| 17 | wisp | attack | done | `art/incoming/mobs/anim/wisp_attack.png` |
| 18 | wisp | death | done | `art/incoming/mobs/anim/wisp_death.png` |
| 19 | golem | walk | done | `art/incoming/mobs/anim/golem_walk.png` |
| 20 | golem | attack | done | `art/incoming/mobs/anim/golem_attack.png` |
| 21 | golem | death | done | `art/incoming/mobs/anim/golem_death.png` |
| 22 | boss_treant | walk | done | `art/incoming/mobs/anim/boss_treant_walk.png` |
| 23 | boss_treant | attack | done | `art/incoming/mobs/anim/boss_treant_attack.png` |
| 24 | boss_treant | death | done | `art/incoming/mobs/anim/boss_treant_death.png` |
| 25 | krahang | walk | done | `art/incoming/mobs/anim/krahang_walk.png` |
| 26 | krahang | attack | done | `art/incoming/mobs/anim/krahang_attack.png` |
| 27 | krahang | death | done | `art/incoming/mobs/anim/krahang_death.png` |
| 28 | khamot | walk | done | `art/incoming/mobs/anim/khamot_walk.png` |
| 29 | khamot | attack | done | `art/incoming/mobs/anim/khamot_attack.png` |
| 30 | khamot | death | done | `art/incoming/mobs/anim/khamot_death.png` |
| 31 | phrai | walk | done | `art/incoming/mobs/anim/phrai_walk.png` |
| 32 | phrai | attack | done | `art/incoming/mobs/anim/phrai_attack.png` |
| 33 | phrai | death | done | `art/incoming/mobs/anim/phrai_death.png` |
| 34 | pret | walk | done | `art/incoming/mobs/anim/pret_walk.png` |
| 35 | pret | attack | done | `art/incoming/mobs/anim/pret_attack.png` |
| 36 | pret | death | done | `art/incoming/mobs/anim/pret_death.png` |
| 37 | monkey | walk | done | `art/incoming/mobs/anim/monkey_walk.png` |
| 38 | monkey | attack | done | `art/incoming/mobs/anim/monkey_attack.png` |
| 39 | monkey | death | done | `art/incoming/mobs/anim/monkey_death.png` |
| 40 | croc_guard | walk | done | `art/incoming/mobs/anim/croc_guard_walk.png` |
| 41 | croc_guard | attack | done | `art/incoming/mobs/anim/croc_guard_attack.png` |
| 42 | croc_guard | death | done | `art/incoming/mobs/anim/croc_guard_death.png` |
| 43 | boss_chalawan | walk | done | `art/incoming/mobs/anim/boss_chalawan_walk.png` |
| 44 | boss_chalawan | attack | done | `art/incoming/mobs/anim/boss_chalawan_attack.png` |
| 45 | boss_chalawan | death | done | `art/incoming/mobs/anim/boss_chalawan_death.png` |

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
