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
| 2 | greatbow | todo | laser-bow archer (ธนูเลเซอร์) |

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

**1 gunner** (มือปืนคู่ไฮเทค — owner 2026-11-10 "ปืนพกคู่ ให้ดูสมัยใหม่", "ให้ 2 ตัวนี้ดูมีเทคโนโลยีไปเลย")
```
Class: high-tech dual-pistol gunslinger, stylish and cool, clearly futuristic. A cropped black tech jacket with glowing
teal light seams and a high collar, a fitted dark bodysuit with thin armour plates, a utility belt with glowing energy
cells, fingerless tech gloves with small glowing panels, slim armoured trousers, sturdy boots with glowing teal soles,
a thigh holster on each leg. A cool black cap worn slightly tilted with a small glowing teal emblem, her wavy brown ponytail
coming out of the back, a slim see-through holographic visor over her eyes (thin teal glow). Two sleek FUTURISTIC energy
pistols (matte black and white with glowing teal cores and lines), one in each hand, held low at her sides, barrels
pointing at the ground. Keep her leaf hair clip as a small glowing badge on the jacket. Colours: black, charcoal, white,
glowing teal, a little gold, brown hair.
```

**2 greatbow** (ธนูเลเซอร์ — owner 2026-11-10 "ธนูเลเซอร์เลยก็ได้", modern like the gunner)
```
Class: high-tech laser archer, stylish and cool, clearly futuristic (the same tech style as the gunner). A big modern compound-style bow almost as tall as she is, made of matte
black and white armour plates with glowing teal light lines, and a bowstring of bright teal LIGHT (a glowing energy string),
held upright in her LEFT hand; no quiver, no wooden arrows (the bow fires light arrows). A sleek white-and-charcoal tech
jacket with a short hood down on her back, glowing teal seams, a fitted bodysuit, one armoured shoulder guard on the bow arm,
tech gauntlets, slim trousers, sturdy boots. A slim visor / headset over one ear with a small glowing teal lens, her wavy
brown ponytail kept. Keep her leaf hair clip as a small badge. Colours: white, charcoal, black, glowing teal, brown hair.
```
