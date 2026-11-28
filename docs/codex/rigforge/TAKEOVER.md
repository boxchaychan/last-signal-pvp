# RigForge 2D: GPT / Codex takes it over (owner 2026-11-28: "จะให้ gpt รับต่อ")

RigForge 2D is the owner's own GPT-made 2D rig / animation tool. The owner now wants GPT / Codex to keep developing it.
Reply to the owner in Thai, short and plain (not a programmer). The owner tells you each task; this file is only the hand-over.

## Permission (exception to AGENTS.md "do not edit .html")
For RigForge tasks you MAY edit `rigforge.html`, `vendor/rigforge/`, `tools/rigforge/` and `tools/qa/rigforge_check.js`. Nothing else.
Still: a new branch `codex/rigforge-<short-task>`, open a pull request, never push to `main`, never merge. Claude merges it after the check.

## Where things are
- `rigforge.html` = the whole tool, ONE page (about 1.4 MB: the Zeus / Poseidon pictures are inside as data). Live: https://boxchaychan.github.io/last-signal-pvp/rigforge.html
- `vendor/rigforge/tailwind.css` + `lucide.min.js`: the page used to load Tailwind and Lucide from the internet (cdn.tailwindcss.com, unpkg); Claude made them local files because the page fell apart without the network and was slow on a phone. How to rebuild the css after adding new Tailwind classes: `vendor/rigforge/NOTICE.md` (or write plain CSS in the page instead).
- `tools/rigforge/MANUAL_TH.md` = the Thai manual; `tools/rigforge/samples/` = practice sheets (zeus 16 parts, poseidon 17 parts on green).
- Notes and the review: section "RIGFORGE 2D" in `docs/action-game.md`.

## Rules for the page
- No internet at run time: no CDN scripts, no fetch / XHR / sockets (Google Fonts is the only thing loaded from outside, keep it optional). It must work offline on a PC and on a phone in landscape.
- Keep what works: the three rigs (Zeus parts, Poseidon parts, Zeus one-picture mesh), play, the game test (wave + ultimate), export = sprite sheet `.png` + rig `.json` named after the chosen character (`zeus_*`, `poseidon_*`, `zeus_mesh_*`), import of a green-screen parts sheet.
- Before the pull request run the check (needs Node + Playwright):
  `python3 -m http.server 8000` then `node tools/qa/rigforge_check.js` -> it must print `RIGFORGE OK` (1280 x 720 and 844 x 390, no page errors). If your change is meant to change what the check tests, change the check too and say so.
- Write `tools/rigforge/REPORT_TH.txt`: what you changed, how to try it, what is not done.

## Known weak points (Claude's review, 2026-11-28)
- The moves are small and a little stiff.
- One-picture mesh mode is weak: the body barely moves, only the effects carry it.
- On a phone the page stacks (viewport, timeline, bone list) and must be scrolled.
- What the tool will be used for is not decided yet: ask the owner.
