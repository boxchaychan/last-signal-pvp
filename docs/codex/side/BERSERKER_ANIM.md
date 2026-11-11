# Berserker (side-scrolling game) — animation queue for Codex

Owner 2026-11-11: a 2D side-scroller like MapleStory / Ghost Online, PAINTED art (not pixel art). Codex draws the hero's moves,
Claude cuts them and puts them in the game. Reply to the owner in Thai, short and plain.

## References (attach BOTH every time)
- `art/incoming/side/berserker/refs/1_SIDE_main.png` — THE design: side view facing right, greatsword resting on the right shoulder.
- `art/incoming/side/berserker/refs/2_TURNAROUND.png` — front / side / back, for the parts the side view hides.

## Character checklist (check every frame against it)
1. Closed black demon helmet with a crown of tall jagged spikes and a red crest, narrow visor with glowing RED eyes, no face.
2. Black jagged plate armour with small glowing red "demon eye" gems on the shoulder, chest, belt and knee plates.
3. LEFT forearm: heavy black chains wrapped round it, a glowing red X on the gauntlet.
4. A long torn black-and-red cape with ragged holes, reaching below the knees.
5. A GIGANTIC straight cleaver greatsword: wide black blade with a red edge glow and a red centre line, spikes along the back,
   a spiked crossguard with a glowing red orb, red grip, spiked pommel. ONE perfectly straight sword, never bent.
6. Chibi proportions exactly like `1_SIDE_main.png`: same head size, same body thickness, same height.

## Rules for every picture
- ONE picture per row of the queue: one action, the frames in a grid (count and grid in the row), on plain pure WHITE.
- TRUE SIDE VIEW facing RIGHT in every frame, the same angle as `1_SIDE_main.png`. Never turn toward the camera (only the
  rows marked "back view" are drawn from behind).
- The character is the SAME SIZE in every cell (figure about 80% of the cell height when standing) and the feet stand on the
  same ground line in every cell, except in jump frames where he leaves the ground.
- Every frame in its own equal square cell with empty space round it: the whole sword and cape inside the cell, nothing
  crossing into the next cell. Every frame a clearly DIFFERENT pose (no repeated frames unless the row says so).
- Keep the full generated size (at least 384 px per cell). Save as PNG (not GIF, not JPG).
- NO dust, NO slash trails, NO sparks, NO shadows, NO text: Claude adds the effects in the game so they can turn and scale.
- Save as `art/incoming/side/berserker/anim/<action>.png`; add one Thai line per file to
  `art/incoming/side/berserker/anim/REPORT_TH.txt` (anything that came out wrong).
- Mark the row `done` here. Work in order; when the owner says "ทำท่าเบอร์เซิร์กเกอร์ต่อ", continue at the first `todo`.
- Branch `codex/hero-berserker`, open a pull request, never merge, never push to `main`. When you stop, `git checkout main`.

## Queue
| # | action | frames / grid | what happens, frame by frame | status |
|---|--------|---------------|------------------------------|--------|
| 1 | idle | 6 / 3x2 | Standing ready, sword on the right shoulder. A slow heavy breath: 1 neutral, 2 chest rises, 3 top of the breath (shoulders up a little, cape lifts), 4 coming down, 5 lowest (knees bend slightly), 6 back up to almost 1. Loops to 1. Only small moves. | todo |
| 2 | walk | 12 / 6x2 | (done by the owner, `anim/walk_sheet_owner.webp`) | done |
| 3 | run | 8 / 4x2 | Heavy run, body leaning forward, sword stays on the shoulder: 1 right foot lands far in front, 2 body passes over it (lowest), 3 push off, both feet off the ground, 4 left knee drives forward, 5 left foot lands, 6 lowest, 7 push off, 8 right knee forward. Cape streams back. Loops. | todo |
| 4 | attack1 | 6 / 3x2 | HIT 1, wide horizontal slash: 1 ready pose (as the reference), 2 wind-up: takes the sword off the shoulder and pulls it far back, body twisted away, 3 step forward, the blade starts to come round at waist height, 4 IMPACT: arms fully stretched, the blade level and reaching FAR in front, 5 follow-through past the front, 6 sword back on the shoulder. | todo |
| 5 | attack2 | 6 / 3x2 | HIT 2, rising slash: 1 ready pose, 2 drops the blade low behind him, crouching, 3 sweeps it forward low near the ground, 4 IMPACT: swings up diagonally, the tip high in front of him, arms stretched, 5 blade above the head, 6 back to the ready pose. | todo |
| 6 | attack3 | 8 / 4x2 | HIT 3, crushing overhead slam: 1 ready pose, 2 both hands on the grip, lifting, 3 sword straight up high above the head, up on his toes, 4 the blade starts down, big step forward, 5 IMPACT: the blade smashes into the ground FAR in front, deep crouch, 6 holds the low pose, 7 pulls the sword up, 8 ready pose. | todo |
| 7 | jump | 6 / 3x2 | 1 crouch to jump, 2 take-off, legs straight, 3 rising, knees tucked, cape below, 4 top of the jump, 5 falling, legs reaching down, cape up, 6 landing crouch. Sword stays on the shoulder. Feet leave the ground line in 2-5. | todo |
| 8 | hurt | 4 / 2x2 | 1 hit from the front: head and chest jerk back, 2 staggers half a step back, 3 recovers balance, 4 ready pose. | todo |
| 9 | death | 6 / 3x2 | 1 struck, staggers back, 2 drops to one knee, the sword point on the ground, 3 leans on the sword, 4 the sword falls, he tips forward, 5 lying face down, cape over him, 6 still (same as 5 but a little flatter). | todo |
| 10 | chain | 6 / 3x2 | Skill Q, chain throw with the LEFT arm while the sword stays on the right shoulder: 1 ready, 2 left arm pulled far back, 3 whips the arm forward, the chain flies out straight to the right (long, reaching the cell edge), 4 arm fully out, chain taut, 5 yanks the chain back hard, leaning back, 6 ready. | todo |
| 11 | spin | 6 / 3x2 | Skill E, spin slash: 1 ready, 2 sword held out to the side at waist height with both hands, 3 back view mid-turn, 4 front view mid-turn, 5 side again, the blade stretched out in front, 6 ready. | todo |
| 12 | slam | 8 / 4x2 | Skill R, leaping slam: 1 crouch, 2 jumps up raising the sword, 3 high in the air, sword overhead, 4 falling forward, 5 IMPACT: lands and slams the blade into the ground in front, deep crouch, 6 holds, 7 rises, 8 ready. | todo |
| 13 | rage | 6 / 3x2 | Skill X, rage awakening: 1 ready, 2 crouches, fists clenched, 3 throws his head back, chest out, arms spread (roar), 4 holds the roar, 5 brings the sword down to the ready pose, 6 ready with the eyes glowing brighter. | todo |
| 14 | climb | 4 / 2x2 | BACK VIEW (use the back of `2_TURNAROUND.png`): climbing a rope, sword on his back: 1 right hand high, left knee up, 2 pulling up, 3 left hand high, right knee up, 4 pulling up. Loops. | todo |
