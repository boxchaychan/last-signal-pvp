---
name: game-project-architect
description: Decide where code, art and notes go in this repository and how work is shipped. Use before adding a new page, tool, asset folder or doc, and when cleaning up.
---
# Project layout and shipping

- Pages are single self-contained HTML files in the repo root (`map.html`, `gem.html`, `bag.html`, `td.html`, `combo.html`, `dogcat.html`, `vfxlab.html`, `vfxcut.html`; `action.html` = code base without hero art). No build step; art loaded by relative path. Patch with exact string replacement and check each anchor is unique.
- Art in use: `art/td/` (maps), `art/action/mobs*`, `props*`, `ground*`, `art/dogcat/`, `art/poses/`, `fx/`. Raw / incoming: `art/incoming/<task>/` (keep raw files). Tools: `tools/art/*.py`, one job per script, the command in its header comment. Test scripts for a page (need node + Playwright, so the cloud session only): `tools/qa/*.js`.
- Notes: `CLAUDE.md` stays short (rules + current work); progress, decisions and the PixelLab job log go at the end / top of `docs/action-game.md`. Codex briefs: `docs/codex/action/*.md` + `AGENTS.md`.
- Ship every batch: branch `main-8rp02y` → commit → push → PR → merge to `main`. GitHub Pages needs 3-5 minutes; give links with `&v=N`.
- Deleted on 2026-11-13 (old games, old heroes): do not bring back unless asked; history has them (`70e92df`).
- Ask before deleting; under-delete when the owner's words are unclear and list what was left.
