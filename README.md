# Last Signal — pixel action game (work in progress)

- `map.html` — walk test on the pixel map with the new chibi swordsman (`?hero=chibi16`, `chibi64`, `&px=1..4`).
- `combo.html` — combo / animation test page.
- `dogcat.html` — dogs-vs-cats tower defense prototype.
- `vfxlab.html`, `vfxcut.html`, `fx/`, `art/incoming/pfx*`, `fx_*` — skill effects and the tools to cut / layer them.
- `action.html` — code of the earlier action RPG (skills, effects, monsters). Its hero art was removed on 2026-11-13; it does not run until the new hero is wired in.
- `docs/action-game.md` — progress notes and the PixelLab job log. `CLAUDE.md`, `AGENTS.md` — notes for the AI helpers.

Open through a small web server (`python -m http.server 8000`), art is loaded by relative path.
Third-party: `vendor/` (licences), `art/thirdparty/ozzbit_hero/` (free template, personal non-commercial use, credit "Ozzbit Games").
