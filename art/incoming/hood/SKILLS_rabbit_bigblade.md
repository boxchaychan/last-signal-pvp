# Hooded rabbit, big saw-blade: skill ideas (owner 2026-11-14 "เตรียมคิดสกิลไว้นะ ดาบใหญ่")
Side view, grinding game. Normal combo = 3 hits (done). Skills = big, bright, reach far, fit the saw-blade: it REVS, GRINDS, THROWS SPARKS.
Each skill = ONE GPT sheet of 12 frames (4 x 3, blue, ground line; `PROMPT_GPT_move_sheet.txt`) for the body, plus long-range effects in code
(the `fxDraw` family in side.html) so the reach does not depend on the drawing. Free; nothing is generated in PixelLab.

| # | Skill (Thai name) | What it does | Feel | Body sheet (12 frames) | Code effect |
|---|---|---|---|---|---|
| 1 | Saw Dash (พุ่งเลื่อย) | dash forward ~200 px, hits everything on the way | fast, gets you out of trouble | crouch, burst forward low with the blade in front, slide to a stop | speed streaks + sparks along the ground behind |
| 2 | Grinder Spin (หมุนบด) | hold the key: spin in place, many small hits, pulls monsters in | crowd killer for packs | spin loop (frames 4-9 loop while held), wind-down | wide ring like the spin hit, growing; sparks flying out |
| 3 | Quake Slam (ทุบแผ่นดิน) | leap and slam; a line of rock / fire spikes runs forward ~250 px | the big ground-target skill | crouch, leap, blade over head, slam, recover | the ground-spike run already built (`slam`), longer |
| 4 | Rev Up (เร่งเครื่อง) | buff 6 s: blade glows, attacks faster, +30 % damage, every hit throws sparks | turns the combo hot | pull the cord / grip, blade roars, glow builds, ready pose | orange glow aura on the blade, heat shimmer pixels |
| 5 | Saw Throw (ขว้างเลื่อย) | throw the blade like a boomerang, it spins out ~260 px and comes back, hitting both ways | the ranged option | wind up, throw, empty-handed wait, catch | spinning blade sprite drawn in code from a frame of the sheet + trail |
| 6 | ULT Sky Saw (เลื่อยฟ้าถล่ม) | jump off-screen, a giant glowing blade drops on a target spot with a red warning first, huge blast | screen-shaking finisher, long cooldown | big jump up, (off-screen), land kneeling, stand up | red ground warning, falling giant blade, shockwave rings, screen flash + shake |

Controls (phone landscape): attack button = combo; 2 skill buttons on the right (1 + 3 to start), ultimate on a charge bar.
Order to build: 3 (effect already exists) → 1 → 2 → 4 → 5 → 6.

## GPT [MOVE] lines (paste into PROMPT_GPT_move_sheet.txt, 12 frames 4 x 3)
1. Saw Dash: crouch low, burst forward with the saw-blade held out in front, a long low dash, slide to a stop with sparks, back to the ready stance.
2. Grinder Spin: plant the feet and spin round and round with the saw-blade held out flat (frames 4 to 9 must loop smoothly), slow down, back to the ready stance.
3. Quake Slam: crouch, leap high, lift the saw-blade over the head, slam it into the ground hard, crouch on impact, stand back up to the ready stance.
4. Rev Up: hold the saw-blade upright, pull its starter cord, the blade roars and glows brighter orange, a confident ready pose.
5. Saw Throw: wind up, hurl the saw-blade forward (it leaves the hands), wait empty-handed, catch it as it comes back, back to the ready stance.
6. Sky Saw: crouch, jump straight up out of the top of the frame (empty frames are fine), then land kneeling with a heavy impact and stand up.
