---
name: gameplay-qa
description: Check that a page of this project really works before reporting (loads without errors, the feature behaves, it looks right on a phone-sized screen). Use after every change to an .html page or to art a page loads.
---
# Checking a change

1. Serve locally: `python3 -m http.server 8000` in the repo root (stop it after).
2. Playwright (pre-installed, `require('playwright')`): open the page at 844x390 (phone, landscape) and, for layout questions, 1920x1000. Collect `pageerror`, failed requests and 4xx / 5xx responses: the list must be empty.
3. Drive the feature, do not just load: keys / pointer for movement, repeated attack presses for a combo. For exact frames stop `requestAnimationFrame` and step the page's own `step(dt)` / `draw()` (pages expose a small object such as `CB`).
4. Screenshot and LOOK at the result (crop + enlarge with nearest for pixel art). Check feet on the ground, frames not cut, sizes next to props, no stray pixels.
5. Report plainly in Thai: what was tested, what was not (e.g. not tried on a real phone), numbers seen. Never claim the live site was checked: it cannot be reached from the cloud session; check the Pages deploy run instead.
