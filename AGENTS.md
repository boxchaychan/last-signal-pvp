# Notes for Codex / GPT agents

The owner speaks Thai and is not a programmer: reply in Thai, short and plain.

NEWEST (2026-11-20): the pixel map `pixmap.html` (3D map drawn as pixel art + a 2D pixel TIGER hero). Picture jobs: `docs/codex/pixmap/TIGER.md` ("ทำเฟรมเสือวิ่ง", "ทำเฟรมเสือยืน", "ทำเฟรมเสือฟัน").

Older (2026-11-17): the 3D level-grinding game `grind3d.html` (chibi archer hero, three.js). Picture jobs for it: `docs/codex/grind3d/ART.md`
("ทำไอคอนสกิล", "ทำพื้นแมพ", "วาดตัวละครใหม่ <ใคร>", "วาดแมพ"). The briefs below are for older games.

Older (2026-11-15): the side-scrolling game `hoodfall.html` with a NEW cast in PAINTED 2D (not pixel art); first hero = the archer "Sky Huntress" (`docs/codex/action/ARCHER.md`). Older briefs below were for the earlier pixel game. The old games (Babies & Beasts, the city game, the legends cast, the old hero classes) were removed from the repository on 2026-11-13; do not recreate them. The live pages are GitHub Pages from `main`.

Who does what:
- **Claude Code** writes the game code (`*.html`, `tools/`, `CLAUDE.md`) and brings new art into the game.
- **GPT / Codex** makes pictures and animations.

## Rules
- Do not edit any `.html`, `CLAUDE.md` or `tools/` unless the owner asks for exactly that in this task.
- Never push to `main` and never merge a pull request. Work on a new branch named `codex/<short-task>` and open a pull request; the owner hands it to Claude.
- Put generated pictures in `art/incoming/<short-task>/`: full-size PNG, not shrunk, not converted to a small pixel grid (Claude's converters do that), plus a short `REPORT_TH.txt` saying which file is which and anything that did not come out right.
- Keep each file under about 10 MB. When you stop, switch the folder back with `git checkout main`.

## Where the briefs are
- `docs/codex/pixmap/TIGER.md`: NEWEST, frames of the 8-bit tiger for the pixel map (run / idle / claw attack; branch `codex/tiger-frames`, pictures in `art/incoming/tiger_frames/`).
- `docs/codex/grind3d/ART.md`: NEWEST, the 3D grinding game: skill icons, tileable ground textures, a new chibi hero design for Tripo, first-map concepts.
- `docs/codex/action/ARCHER.md`: (side game) move sheets of the archer, painted 2D, one sheet per move ("ทำท่านักธนู" = next 2 todo rows; branch `codex/archer-moves`, pictures in `art/incoming/archer/`).
- `docs/codex/action/SLASH.md`: run cycle + sword-combo frames for the new chibi pixel swordsman (pose sheet + character picture in `art/poses/ref_sketch/`; branch `codex/chibi-slash`; "ทำท่าวิ่ง" = row 0, "ทำท่าฟัน" = the first `todo` slash row; rows 0 and 1 first, then stop).
- `docs/codex/action/MOBS.md`, `MOB_ANIM.md`: monsters and their frames (kept; "ทำมอนต่อ", "ทำเฟรมมอนต่อ").
- `docs/codex/action/FX.md`: skill / attack effects ("ทำเอฟเฟคต่อ").
- `docs/codex/action/MAPS.md`: map art.

## Picture rules
- Side game (ARCHER.md): painted 2D, NOT pixel art, flat green #00B140 background as the brief says. Older pixel briefs: pixel art, characters face RIGHT unless the task asks for other directions, plain white or see-through background, no text, no watermark, original designs only.
