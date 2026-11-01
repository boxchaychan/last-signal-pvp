# Last Signal (สัญญาณสุดท้าย) — notes for Claude Code

The owner speaks Thai. Reply in Thai, short and plain (they are not a programmer). They test on a phone (landscape) and on a Windows PC.

## What the game is
Browser game, top-down map. Two sides, played against bots (online PvP is a later goal):
- **Humans** — 3-hero squad (player + 2 bots), twin-stick shooter with MOBA skills (Q, F, Space, ultimate E; hold to aim, release to cast), tower defense, capture zones, rescue civilians. Win: kill the ghost leader.
- **Ghosts/zombies** — two play styles chosen in the loadout:
  - `boss` (default): the player *is* the leader (Spider Queen / Alpha / Plague doctor), walks like a hero, 4 skills, builds nests (B), nests auto-produce 5 unit types, each type has an order: patrol / defend the flag (V) / attack. Queen dies → respawns at a nest; no nests left → lose.
  - `rts`: old commander mode (top-down camera, build/produce/send waves).
- Win for ghosts: destroy the human HQ.

## Files
- `index.html` — the whole game (HTML + CSS + one big `<script>`), ~4k lines, no build step. Open it through a local web server (art is loaded by relative path), e.g. `python -m http.server` in the repo root, then http://localhost:8000.
- `art/` painted sprites. Characters face RIGHT; the code flips them. Strips are one row of frames, feet-aligned. `art/px/` = optional pixel-art set.
- `fx/` pixelfx sprite effects (MIT, keep `vendor/pixelfx/LICENSE`).
- `vendor/` third-party licences/notices (pixelfx, agent-sprite-forge, three.js). Keep them.
- `docs/prompt-kit.html` — the owner's prompt pack for generating art (ChatGPT images + Google Flow videos).
- `tools/check.sh` — extracts the script and runs `node --check`.
- `tools/sim/sim.js` — headless simulation with a stub DOM: `node tools/sim/sim.js demo|boss|ults`. Run it after gameplay changes; it doubles as a smoke test.
- `tools/video/` — turning a Flow video (flat green/magenta background) into a frame strip: `sqproc.py` (keying, loop search, feet anchor, quantized PNG), `strip2.py` (grid sprite sheet → strip).
- `tools/blender/` — `ls_step1_prepare.py` (Meshy GLB → light, upright FBX for Mixamo), `ls_step2_merge.py` (Mixamo FBX files → one `storm_game.glb` with named animations). Blender 5.2 is at `C:\Program Files\Blender Foundation\Blender 5.2\blender.exe`; run with `blender -b --python <script>`.

## Code map (search these section comments in index.html)
`// ---------- grid & pathing` flow fields (`makeField`, `flowDir`, `ZBLK`) · `state` (`G` = whole match state, `P`/`keys`/`sticks` = input) · `damage` (`dealZ`, `dealS`, `hurtH`) · `MOBA skills` (`skillX`, `HEROES[k].s1/s2/s3/ul` with `tg` targeting) · `MOBA aiming` (`AIM`, `aimSolve`, `castAim`, `drawAim`; shared by hero and boss via `ctlU()`/`kitOf()`) · `hero art` / `3D heroes` (three.js r147 from CDN, `H3`, toggle in pause menu) · `player control`/`bot control` (`playerCtl`, `botCtl`, `botSkills`, `pickGoal`) · `updates` (`updHuman`, `updZombie`, `zAI` = AI ghost commander, `step` = main tick) · `HUD` (`setupHud`, `updHud`) · `input` · `boss mode` (`BK` boss kits, `bmAI`, `updBoss`, `bossCast`, `cycleMode`, `bmNest`, eggs `updEggs`, brood spiders, `disruptH` = stun/fear/confuse/web on humans) · `hero ultimates` (`ult()`, `updUlts`, cut-in `ultFlair`, engineer auto-repair) · `painted art` (`ARTDEF`, `drawStand`: idle/walk/atk/cast strips) · `tower defense` (`TW`, `updTowers`) · `levels & upgrades` · `loop`.

Data tables at the top of the script: `HEROES`, `HDEF` (default weapons), `WEAP`, `ZT` (unit stats; `brood:1` = spiders from eggs), `LEADERS`, `ZB` (ghost structures incl. `egg`), `TW` (human towers).

## Conventions
- Keep everything in `index.html` (single file). Patch with exact string replacements; check that each anchor appears once.
- After any edit: `bash tools/check.sh` then `node tools/sim/sim.js ults` / `boss` / `demo 3 480`.
- Balance target: bot-vs-bot demo should be roughly even (humans win about half, matches 4–8 min).
- Mobile first: landscape phone ~844×390. Left half of the screen = move stick, right side = skill arc. Don't cover the middle with UI.
- Art pipeline: owner makes a base image in ChatGPT, then an 8 s Google Flow clip (Frames to Video, same image as first and last frame, flat key-colour background). Use green for pink/magenta characters, magenta otherwise.

## Current state / next steps
- Spider Queen art: side view with idle/walk/attack/cast strips from Flow (`art/z_queen_*.png`). A top-down still (`z_queen_top.png`) exists behind a pause-menu toggle (owner chose side view).
- Heroes: only Storm has painted strips; the other 5 are code-drawn. Prompts for them are in `docs/prompt-kit.html` (Flow section).
- 3D test for humans: Storm model from Meshy (49 MB GLB in the owner's Downloads) → run `tools/blender/ls_step1_prepare.py` → Mixamo (owner uploads, downloads Rifle Idle / Rifle Run (in place) / Firing Rifle / Toss Grenade / Dying) → `ls_step2_merge.py` → `storm_game.glb` → load with GLTFLoader + AnimationMixer, toon shading + outline, gun attached to the right-hand bone, 2D/3D toggle.
- Wanted later: online PvP, port to Godot once the browser version is fun.
