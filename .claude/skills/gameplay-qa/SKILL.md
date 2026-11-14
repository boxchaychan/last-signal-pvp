---
name: gameplay-qa
description: Check that a page of this project really works before reporting (loads without errors, the feature behaves, it looks right on a phone-sized screen). Use after every change to an .html page or to art a page loads.
---
# Checking a change

1. Serve locally: `python3 -m http.server 8000` in the repo root (stop it after).
2. Playwright (pre-installed, `require('playwright')`): open the page at 844x390 (phone, landscape) and, for layout questions, 1920x1000. Collect `pageerror`, failed requests and 4xx / 5xx responses: the list must be empty.
3. Drive the feature, do not just load: keys / pointer for movement, repeated attack presses for a combo. For exact frames stop `requestAnimationFrame` and step the page's own `step(dt)` / `draw()` (pages expose a small object such as `CB`).
   `gem.html` (all canvas, no DOM buttons): wait for `GM.ready`; `GM.hold = true` stops its own loop, then `GM.step(dt)` + `GM.draw()` give exact frames; `GM.ui()` lists what can be tapped on the screen that is drawn (id + CSS x / y, click those for a real tap), `GM.tap(id)` presses one from code; `GM.scr`, `GM.dlg`, `GM.fade` say where it is; `GM.simStage(ch, st, skill)` plays a whole stage with the auto-player (it does NOT pay the reward: call `GM.grant(win)` once, as `tools/qa/gem_balance.js` does). Ready-made runs: `node tools/qa/gem_play.js [shots folder]` (real clicks and drags, start to save), `gem_fuzz.js`, `gem_balance.js`. Always play once with REAL clicks / drags: hooks do not find a panel hidden behind another one.
   Run browser checks ONE AT A TIME: four Chromium runs side by side got the cloud session's worker killed (out of memory, 2026-11-14).
4. Screenshot and LOOK at the result (crop + enlarge with nearest for pixel art). Check feet on the ground, frames not cut, sizes next to props, no stray pixels.
5. Report plainly in Thai: what was tested, what was not (e.g. not tried on a real phone), numbers seen. Never claim the live site was checked: it cannot be reached from the cloud session; check the Pages deploy run instead.
