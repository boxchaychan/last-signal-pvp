# Effects for the action game — queue for Codex

Owner 2026-11-09. Reply to the owner in Thai, short and plain.

## Rules
- ONE picture per row: one effect, 6 frames in a 3x2 grid on PURE BLACK (the game turns the black into see-through).
  No reference picture is needed.
- Save full size as `art/incoming/fx_codex/<key>.png`; one Thai line per file in `art/incoming/fx_codex/REPORT_TH.txt`.
- Mark the row `done` here. Work in the order of the queue; "ทำเอฟเฟคต่อ" = continue at the first `todo`.
- Branch `codex/fx`, commit, never merge, never push to `main`. Claude works in this same folder on `main`: when you stop,
  switch the folder back with `git checkout main`.

## Queue
| # | key | status | thai | for |
|---|-----|--------|------|-----|
| 1 | fireball | todo | ลูกไฟ | mage Q |
| 2 | meteor | todo | อุกกาบาต | mage Z |
| 3 | meteor_hit | todo | อุกกาบาตตก | mage Z |
| 4 | frost_nova | todo | วงน้ำแข็ง | mage R |
| 5 | mana_shield | todo | โล่เวท | mage X |
| 6 | blink | todo | วาร์ป | mage F |
| 7 | ground_crack | todo | รอยแยกพื้น | swordsman Q |
| 8 | whirlwind | todo | พายุดาบ | swordsman E |
| 9 | berserk | todo | คลั่ง | swordsman X |
| 10 | leap_slam | todo | กระโดดทุบ | swordsman F |
| 11 | spore_cloud | todo | สปอร์เห็ด | mushroom attack |
| 12 | ghost_fire | todo | ไฟผี | lantern wisp + khamot shots |
| 13 | root_spikes | todo | รากแทงพื้น | treant boss |
| 14 | water_wave | todo | คลื่นน้ำ | Chalawan boss + phrai |
| 15 | steam | todo | ไอน้ำระเบิด | mage reaction fire+ice |
| 16 | shatter | todo | น้ำแข็งแตก | mage reaction ice+lightning |
| 17 | overload | todo | ระเบิดสายฟ้า | mage reaction lightning+fire |

## Prompts
### fireball (ลูกไฟ, mage Q)
Save as `art/incoming/fx_codex/fireball.png`.
```
Visual effect frames for a 2D pixel-art action game, ONE picture. Effect: a round fireball flying to the RIGHT: a bright yellow-white core inside orange and red flames with a short flame tail streaming to the left; a looping flight, every frame a slightly different flicker of the flames.
Style: bright, clean and bold game effect, crisp shapes with a soft glow, matching a cute chibi fantasy action game.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size; the effect is centred in its cell with empty black space around it; nothing crosses into the next cell.
Background: PURE BLACK (#000000) everywhere, no gradient, no stars, no ground, no character, no text, no numbers, no grid lines. Every frame must be clearly different.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### meteor (อุกกาบาต, mage Z)
Save as `art/incoming/fx_codex/meteor.png`.
```
Visual effect frames for a 2D pixel-art action game, ONE picture. Effect: a flaming meteor rock falling diagonally down to the right: a dark cracked rock with glowing orange cracks, wrapped in fire with a long fire trail behind it up to the top left; a looping fall, the flames flickering.
Style: bright, clean and bold game effect, crisp shapes with a soft glow, matching a cute chibi fantasy action game.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size; the effect is centred in its cell with empty black space around it; nothing crosses into the next cell.
Background: PURE BLACK (#000000) everywhere, no gradient, no stars, no ground, no character, no text, no numbers, no grid lines. Every frame must be clearly different.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### meteor_hit (อุกกาบาตตก, mage Z)
Save as `art/incoming/fx_codex/meteor_hit.png`.
```
Visual effect frames for a 2D pixel-art action game, ONE picture. Effect: a big fire explosion where a meteor hits the ground: frame 1 a white-hot flash on the ground, frames 2-3 a huge orange fireball blast with rocks and embers flying out, frames 4-5 a flat ring of fire and smoke spreading on the ground (a wide flat ellipse), frame 6 only glowing embers fading.
Style: bright, clean and bold game effect, crisp shapes with a soft glow, matching a cute chibi fantasy action game.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size; the effect is centred in its cell with empty black space around it; nothing crosses into the next cell.
Background: PURE BLACK (#000000) everywhere, no gradient, no stars, no ground, no character, no text, no numbers, no grid lines. Every frame must be clearly different.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### frost_nova (วงน้ำแข็ง, mage R)
Save as `art/incoming/fx_codex/frost_nova.png`.
```
Visual effect frames for a 2D pixel-art action game, ONE picture. Effect: an ice nova bursting outward on the ground around a centre point: frame 1 a small bright ice-blue flash, frames 2-4 a ring of sharp ice crystals and frost mist spreading outward as a wide flat ellipse lying on the ground, frames 5-6 the ice shards sparkling and fading.
Style: bright, clean and bold game effect, crisp shapes with a soft glow, matching a cute chibi fantasy action game.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size; the effect is centred in its cell with empty black space around it; nothing crosses into the next cell.
Background: PURE BLACK (#000000) everywhere, no gradient, no stars, no ground, no character, no text, no numbers, no grid lines. Every frame must be clearly different.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### mana_shield (โล่เวท, mage X)
Save as `art/incoming/fx_codex/mana_shield.png`.
```
Visual effect frames for a 2D pixel-art action game, ONE picture. Effect: a magic shield bubble: a see-through glowing teal sphere with a bright rim and faint floating hexagon runes, empty in the middle (a character stands inside it); a looping shimmer, the runes slowly drifting round.
Style: bright, clean and bold game effect, crisp shapes with a soft glow, matching a cute chibi fantasy action game.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size; the effect is centred in its cell with empty black space around it; nothing crosses into the next cell.
Background: PURE BLACK (#000000) everywhere, no gradient, no stars, no ground, no character, no text, no numbers, no grid lines. Every frame must be clearly different.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### blink (วาร์ป, mage F)
Save as `art/incoming/fx_codex/blink.png`.
```
Visual effect frames for a 2D pixel-art action game, ONE picture. Effect: a teleport flash: frame 1 a thin vertical teal light, frames 2-3 a burst of teal and white arcane sparks and small star shapes, frames 4-6 the sparks drifting up and fading.
Style: bright, clean and bold game effect, crisp shapes with a soft glow, matching a cute chibi fantasy action game.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size; the effect is centred in its cell with empty black space around it; nothing crosses into the next cell.
Background: PURE BLACK (#000000) everywhere, no gradient, no stars, no ground, no character, no text, no numbers, no grid lines. Every frame must be clearly different.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### ground_crack (รอยแยกพื้น, swordsman Q)
Save as `art/incoming/fx_codex/ground_crack.png`.
```
Visual effect frames for a 2D pixel-art action game, ONE picture. Effect: a glowing crack splitting the ground, running from the LEFT edge to the RIGHT: frame 1 a short crack at the left, frames 2-4 the jagged crack racing to the right with orange-yellow light and small rock chunks bursting up along it, frames 5-6 the whole crack glowing then dimming. The crack lies flat on the ground (seen from a low top-down angle).
Style: bright, clean and bold game effect, crisp shapes with a soft glow, matching a cute chibi fantasy action game.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size; the effect is centred in its cell with empty black space around it; nothing crosses into the next cell.
Background: PURE BLACK (#000000) everywhere, no gradient, no stars, no ground, no character, no text, no numbers, no grid lines. Every frame must be clearly different.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### whirlwind (พายุดาบ, swordsman E)
Save as `art/incoming/fx_codex/whirlwind.png`.
```
Visual effect frames for a 2D pixel-art action game, ONE picture. Effect: a whirlwind of sword slashes: a wide flat ring of bright white-blue wind and blade streaks spinning round an empty centre, lying almost flat like an ellipse seen from a low top-down angle; a looping spin, the streaks in a different place each frame.
Style: bright, clean and bold game effect, crisp shapes with a soft glow, matching a cute chibi fantasy action game.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size; the effect is centred in its cell with empty black space around it; nothing crosses into the next cell.
Background: PURE BLACK (#000000) everywhere, no gradient, no stars, no ground, no character, no text, no numbers, no grid lines. Every frame must be clearly different.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### berserk (คลั่ง, swordsman X)
Save as `art/incoming/fx_codex/berserk.png`.
```
Visual effect frames for a 2D pixel-art action game, ONE picture. Effect: a red rage aura: tall red and dark-red flames rising around an empty centre where a character stands, a few red sparks; a looping flicker, the flames rising and falling.
Style: bright, clean and bold game effect, crisp shapes with a soft glow, matching a cute chibi fantasy action game.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size; the effect is centred in its cell with empty black space around it; nothing crosses into the next cell.
Background: PURE BLACK (#000000) everywhere, no gradient, no stars, no ground, no character, no text, no numbers, no grid lines. Every frame must be clearly different.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### leap_slam (กระโดดทุบ, swordsman F)
Save as `art/incoming/fx_codex/leap_slam.png`.
```
Visual effect frames for a 2D pixel-art action game, ONE picture. Effect: a heavy ground slam: frame 1 a white impact flash, frames 2-3 a shockwave ring of dust and light bursting outward as a wide flat ellipse on the ground with rock chunks flying up, frames 4-6 dust settling and fading.
Style: bright, clean and bold game effect, crisp shapes with a soft glow, matching a cute chibi fantasy action game.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size; the effect is centred in its cell with empty black space around it; nothing crosses into the next cell.
Background: PURE BLACK (#000000) everywhere, no gradient, no stars, no ground, no character, no text, no numbers, no grid lines. Every frame must be clearly different.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### spore_cloud (สปอร์เห็ด, mushroom attack)
Save as `art/incoming/fx_codex/spore_cloud.png`.
```
Visual effect frames for a 2D pixel-art action game, ONE picture. Effect: a puff of poison spores: frames 1-2 a small burst of purple and pale yellow spores, frames 3-5 a round drifting cloud of purple spore dust with tiny sparkles, frame 6 thin wisps fading.
Style: bright, clean and bold game effect, crisp shapes with a soft glow, matching a cute chibi fantasy action game.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size; the effect is centred in its cell with empty black space around it; nothing crosses into the next cell.
Background: PURE BLACK (#000000) everywhere, no gradient, no stars, no ground, no character, no text, no numbers, no grid lines. Every frame must be clearly different.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### ghost_fire (ไฟผี, lantern wisp + khamot shots)
Save as `art/incoming/fx_codex/ghost_fire.png`.
```
Visual effect frames for a 2D pixel-art action game, ONE picture. Effect: a ghost fire shot flying to the RIGHT: a ball of pale blue-white spirit flame with a wavy tail to the left and a faint skull-like shape in the flame; a looping flight, the flame flickering.
Style: bright, clean and bold game effect, crisp shapes with a soft glow, matching a cute chibi fantasy action game.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size; the effect is centred in its cell with empty black space around it; nothing crosses into the next cell.
Background: PURE BLACK (#000000) everywhere, no gradient, no stars, no ground, no character, no text, no numbers, no grid lines. Every frame must be clearly different.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### root_spikes (รากแทงพื้น, treant boss)
Save as `art/incoming/fx_codex/root_spikes.png`.
```
Visual effect frames for a 2D pixel-art action game, ONE picture. Effect: thorny tree roots erupting from the ground: frame 1 the ground cracking, frames 2-3 sharp dark-brown roots with thorns stabbing up out of the ground in a cluster, frame 4 the roots at full height, frames 5-6 the roots sinking back into the ground.
Style: bright, clean and bold game effect, crisp shapes with a soft glow, matching a cute chibi fantasy action game.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size; the effect is centred in its cell with empty black space around it; nothing crosses into the next cell.
Background: PURE BLACK (#000000) everywhere, no gradient, no stars, no ground, no character, no text, no numbers, no grid lines. Every frame must be clearly different.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### water_wave (คลื่นน้ำ, Chalawan boss + phrai)
Save as `art/incoming/fx_codex/water_wave.png`.
```
Visual effect frames for a 2D pixel-art action game, ONE picture. Effect: a wave of river water rushing to the RIGHT along the ground: frame 1 a splash, frames 2-4 a curling wave of blue-green water with white foam surging forward, frames 5-6 the water spraying and falling apart.
Style: bright, clean and bold game effect, crisp shapes with a soft glow, matching a cute chibi fantasy action game.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size; the effect is centred in its cell with empty black space around it; nothing crosses into the next cell.
Background: PURE BLACK (#000000) everywhere, no gradient, no stars, no ground, no character, no text, no numbers, no grid lines. Every frame must be clearly different.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### steam (ไอน้ำระเบิด, mage reaction fire+ice)
Save as `art/incoming/fx_codex/steam.png`.
```
Visual effect frames for a 2D pixel-art action game, ONE picture. Effect: a steam explosion: frame 1 a bright white flash, frames 2-4 a big billowing burst of white steam with a little orange and ice-blue light inside, frames 5-6 the steam spreading thin and fading.
Style: bright, clean and bold game effect, crisp shapes with a soft glow, matching a cute chibi fantasy action game.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size; the effect is centred in its cell with empty black space around it; nothing crosses into the next cell.
Background: PURE BLACK (#000000) everywhere, no gradient, no stars, no ground, no character, no text, no numbers, no grid lines. Every frame must be clearly different.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### shatter (น้ำแข็งแตก, mage reaction ice+lightning)
Save as `art/incoming/fx_codex/shatter.png`.
```
Visual effect frames for a 2D pixel-art action game, ONE picture. Effect: ice shattering: frame 1 a block of ice cracked with yellow lightning lines, frames 2-3 the ice exploding into many sharp ice shards flying outward with sparks, frames 4-6 the shards falling and sparkling out.
Style: bright, clean and bold game effect, crisp shapes with a soft glow, matching a cute chibi fantasy action game.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size; the effect is centred in its cell with empty black space around it; nothing crosses into the next cell.
Background: PURE BLACK (#000000) everywhere, no gradient, no stars, no ground, no character, no text, no numbers, no grid lines. Every frame must be clearly different.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```

### overload (ระเบิดสายฟ้า, mage reaction lightning+fire)
Save as `art/incoming/fx_codex/overload.png`.
```
Visual effect frames for a 2D pixel-art action game, ONE picture. Effect: an electric fire explosion: frame 1 a violet-white flash, frames 2-3 a round blast of orange fire laced with purple and yellow lightning arcs, frames 4-6 crackling sparks and smoke fading.
Style: bright, clean and bold game effect, crisp shapes with a soft glow, matching a cute chibi fantasy action game.
LAYOUT: 6 frames in a 3 x 2 grid, read left to right, top row first. Each frame sits in its own square cell of equal size; the effect is centred in its cell with empty black space around it; nothing crosses into the next cell.
Background: PURE BLACK (#000000) everywhere, no gradient, no stars, no ground, no character, no text, no numbers, no grid lines. Every frame must be clearly different.
Picture size 1536x1024 (each cell 512x512). Keep the full generated size. Do ONLY this one picture now.
```
