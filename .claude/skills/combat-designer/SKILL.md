---
name: combat-designer
description: Design or tune attacks, combos and hit feel for this project's action game (timings, chaining, hit-stop, knock-back, skill shapes). Use when adding a move, a combo step or a skill, or when the owner says a hit feels weak or stiff.
---
# Combat rules of thumb (from combo.html)

Direction: level-grinding action RPG; monsters in packs; most skills aimed at a spot on the ground; big bright effects; bosses warn with red ground marks. No build / loadout system.

A combo step = frame list with seconds per frame + the hit frame + damage, lunge, knock-back, hit-stop, effect scale.
- Wind-up short (0.05-0.09 s a frame), hit frame held a little longer, recovery cancellable by the next input.
- Input buffer ≈ 0.28 s; the next step may start when the current one ends or in the first recovery frames.
- Weight comes from: hit-stop (light 0.05, heavy 0.12 s), target knock-back + squash, a white flash, 2-5 px screen shake on the heavy hit, damage numbers bigger for the finisher.
- Three hits should read as three different moves (side slash, rising / overhead, jump slam or spin), damage rising about 10 / 14 / 30.
- Drawn frames beat cut-out bones for big attacks; bones are for idle / walk and for designing poses.
Keep numbers in one table per character so they can be tuned without touching logic.
