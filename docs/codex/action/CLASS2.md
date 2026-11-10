# Class 2 heroes (action game) — brief for Codex

Owner 2026-11-10 "คลาส 2 นักธนู ปืนคู่ กับ ธนูใหญ่": the archer gets two class-2 forms, like the swordsman's Berserker and
Guardian. Reply to the owner in Thai, short and plain.

## Rules
- ONE picture per row of the queue, each its own generation. Attach BOTH reference pictures every time:
  1. `art/incoming/action/archer/turnaround_gpt.png` — the archer as she is now (her face, hair, colours, proportions);
  2. `docs/codex/action/refs/00_STYLE_hero.png` — the game's style picture.
- Save full size as generated (do not shrink, do not convert to a pixel grid) as `art/incoming/action/<key>/turnaround_gpt.png`,
  plus one Thai line per picture in `art/incoming/action/CLASS2_REPORT_TH.txt` (anything that came out wrong).
- Mark the row `done` here. Branch `codex/class2`, open a pull request, never merge, never push to `main`.
- The side view MUST be a true right profile (facing right, nose pointing right, we see only one eye). Earlier runs drew
  a 3/4 view there and it had to be redone.

## Queue
| # | key | status | what |
|---|-----|--------|------|
| 1 | gunner | todo | dual-pistol gunslinger (ปืนคู่) |
| 2 | greatbow | todo | great-bow archer (ธนูใหญ่) |

## Shared prompt (put this first, then the row's own lines)
```
Pixel art game character turnaround sheet in the SAME style as the attached pictures (chibi pixel art, big head, thick
dark outline, few flat colours with one shade step, bright colours, crisp pixels).
This is the CLASS 2 form of the attached archer girl: the SAME young woman (same face, same eye colour, same wavy brown
hair in a high ponytail with the little leaf clip, same height and chibi proportions), now in stronger, cooler gear.
Show 3 full-body views in one row on a plain pure white background:
1) front view facing the viewer, 2) TRUE SIDE VIEW facing RIGHT (pure profile, nose to the right, one eye visible),
3) back view.
Same size in all three views, feet on the same ground line, evenly spaced, nothing touching or crossing into the next view,
the whole body inside the picture. Picture size 1536x1024 landscape; each figure about 85% of the picture height.
Neutral ready pose (not attacking), weapons held the same way in every view. No shadow, no ground, no text, no labels,
no frame, no glow or particles outside the body. Original design: do not copy any existing game, anime or film character.
```

## Row lines

**1 gunner** (มือปืนคู่ สมัยใหม่ — owner 2026-11-10 "ชุดหมวกเท่ๆ ปืนพกคู่ ให้ดูสมัยใหม่ไปเลย")
```
Class: modern dual-pistol gunslinger, stylish and cool. A cropped black tactical jacket with teal accents and a high collar,
a fitted dark top, a utility belt with magazine pouches, fingerless tactical gloves, slim cargo trousers, sturdy combat
boots, a thigh holster on each leg. A cool black cap worn slightly tilted (a baseball-style cap with a small teal emblem)
with her wavy brown ponytail coming out of the back, small round tinted sunglasses pushed up on the cap. Two sleek MODERN
semi-automatic handguns (matte black with teal details), one in each hand, held low at her sides, barrels pointing at the
ground. Keep her leaf hair clip as a small badge on the jacket. Colours: black, charcoal, teal, a little gold, brown hair.
```

**2 greatbow** (ธนูใหญ่)
```
Class: great-bow archer. A huge carved wooden war bow almost as tall as she is, with green-and-gold rune carvings and a
silver tip at each end, held upright in her LEFT hand; a big quiver of long fletched arrows on her back. A hooded forest
green mantle with a few feathers at the collar and a wind-swept cape, one leather shoulder guard on the bow arm, leather
bracers, a belt with a hunting knife, tall brown boots. Colours: forest green, brown leather, cream, gold rune lines.
```
