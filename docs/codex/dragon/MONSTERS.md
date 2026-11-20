# Desert monsters for the dragon's map (painted 2D)

Owner phrase: "ทำมอนทะเลทราย" (owner 2026-11-20 "สั่งไปเรื่อยๆ codex": keep Codex busy; the level-grinding map `pixmap.html` needs monsters).
Branch `codex/desert-monsters`, pictures into `art/incoming/desert_monsters/` (full size PNG), plus `REPORT_TH.txt` (Thai, short). Commit after each picture.
Open a pull request if you can, do not merge. When you stop, switch the folder back with `git checkout main`.

## Style (all monsters)
- The SAME painted 2D chibi game style as the hero `art/incoming/dragon_moves/base_side.png` (thick dark outline, clean smooth painted shading,
  bright readable colours). NOT pixel art. Original designs: do not copy monsters from other games.
- Desert / oasis setting: sand, sun-baked rock, old tomb ruins.
- Each monster reads at a glance by its silhouette and has ONE accent colour.

## The monsters (in this order; sizes compared with the hero's height H)
1. `scorpion`: sand scorpion, low and wide (0.6 H tall), orange-tan shell, big pincers, a glowing green poison sting.
2. `wolf`: dune wolf, lean, sand-yellow fur with dark stripes, a red scarf (0.8 H at the shoulder).
3. `mummy`: tomb mummy, hunched, loose bandages, glowing blue eyes, a rusty curved blade (1.0 H).
4. `cactus`: walking cactus, round, green with pink flowers on the head, spiky arms (0.9 H).
5. `golem` (BOSS): sand-stone golem with gold tomb runes glowing orange, huge fists (2.0 H).

## For each monster, 4 pictures
- `<name>_base.png`: one big picture, side view facing RIGHT, standing ready, plain flat white background, no shadow, no text.
- `<name>_walk.png`, `<name>_attack.png`, `<name>_hurt_death.png`: sheets with these rules:
  - 16 frames, 4 columns x 4 rows (4 in each row), left to right, top to bottom. Portrait picture 1024 x 1536, cells 256 x 384 (the golem too: same grid, he simply fills more of his cell).
  - Flat solid blue background (#0248BA), no borders or lines between cells; a thin dark ground line at the same height near the bottom of every cell.
  - Same size in every frame, side view facing RIGHT, in the middle of its cell, moving in place, never touching another cell.
  - Smooth: small steps between frames. No text, no numbers, no watermark.
  - walk: a full walk loop (frame 16 flows into frame 1).
  - attack: wind-up, the strike (pincer snap / bite / blade slash / spike punch / ground smash), a bright flash on the hit frame, recover.
  - hurt_death: frames 1-6 = get hit, flinch and recover; frames 7-16 = get hit hard and die (fall, fade or crumble), lying still in the last 3 frames.

## Check before you finish
Each sheet next to its base picture: same design, colours, size in every frame? Feet on the line? Walk loop closes? Say in `REPORT_TH.txt` what still looks off.
Claude then cuts the frames and puts them in `pixmap.html`.
