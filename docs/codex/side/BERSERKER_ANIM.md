# Berserker (side-scrolling game) — animation queue for Codex

Owner 2026-11-11: a 2D side-scroller like MapleStory / Ghost Online, PAINTED art (not pixel art). Codex draws the hero's moves,
Claude cuts them and puts them in the game. Reply to the owner in Thai, short and plain.

## References (attach BOTH every time)
- `art/incoming/side/berserker/refs/1_SIDE_main.png` — THE design: side view facing right, greatsword resting on the right shoulder.
- `art/incoming/side/berserker/refs/2_TURNAROUND.png` — front / side / back, for the parts the side view hides.

## Pose guides (owner 2026-11-11 "ไม่รู้ว่าจะทำท่าทางแบบไหน")
For most rows there is a pose guide `art/incoming/side/berserker/poses/<action>_POSES.png`: numbered grey silhouettes of the
same kind of greatsword berserker doing the move, frame by frame (the red number = the hit frame). Attach it as a THIRD
picture and copy its POSES and its timing frame by frame; draw the character only from `1_SIDE_main.png` (the silhouettes
are an older design: copy the body positions, not the shapes of the armour). Guides: idle, run, attack1 (horizontal slash),
attack3 (overhead slash), spin, chain, slam, roll, hurt, death. Rows without a guide follow the text.

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
- MANY frames = smooth motion (owner 2026-11-11 "เจนเยอะๆ ท่ามันจะสมูท"): the frame counts below are the minimum; the steps
  between two neighbouring frames must be SMALL and even, like an animator's in-betweens (no big jumps between frames).
- Keep the full generated size (at least 320 px per cell, the whole picture at least 2000 px wide). Save as PNG (not GIF, not JPG).
- NO dust, NO slash trails, NO sparks, NO shadows, NO text: Claude adds the effects in the game so they can turn and scale.
- Save as `art/incoming/side/berserker/anim/<action>.png`; add one Thai line per file to
  `art/incoming/side/berserker/anim/REPORT_TH.txt` (anything that came out wrong).
- Mark the row `done` here. Work in order; when the owner says "ทำท่าเบอร์เซิร์กเกอร์ต่อ", continue at the first `todo`.
- Branch `codex/hero-berserker`, open a pull request, never merge, never push to `main`. When you stop, `git checkout main`.

## Queue
| # | action | frames / grid | what happens (key poses; draw the in-betweens evenly between them) | status |
|---|--------|---------------|------------------------------|--------|
| 1 | idle | 12 / 6x2 | Standing ready, sword on the right shoulder. One slow heavy breath: chest and shoulders rise (frames 1-6), the cape lifts a little, then come down, knees bending slightly at the lowest point (7-12). Frame 12 leads back into 1. Only small moves. | todo |
| 2 | walk | 12 / 6x2 | (done by the owner, `anim/walk_sheet_owner.webp`) | done |
| 3 | run | 12 / 6x2 | Heavy run, body leaning forward, sword stays on the shoulder. 1 right foot lands far in front, 3 lowest, 4 push off, 5 both feet off the ground, 6 left knee drives forward, 7 left foot lands, 9 lowest, 10 push off, 11 airborne, 12 right knee forward. Cape streams back. Loops. | todo |
| 4 | attack1 | 12 / 6x2 | HIT 1, wide horizontal slash. 1 ready pose (as the reference); 2-4 wind-up: takes the sword off the shoulder and pulls it far back, body twisted away; 5-6 step forward, the blade comes round at waist height; 7 IMPACT: arms fully stretched, the blade level and reaching FAR in front; 8-9 follow-through past the front; 10-12 sword back onto the shoulder. | todo |
| 5 | attack2 | 12 / 6x2 | HIT 2, rising slash. 1 ready; 2-4 drops the blade low behind him, crouching; 5-6 sweeps it forward low near the ground; 7 IMPACT: swings up diagonally, the tip high in front, arms stretched; 8-9 blade above the head; 10-12 back to the ready pose. | todo |
| 6 | attack3 | 16 / 4x4 | HIT 3, crushing overhead slam. 1 ready; 2-4 both hands on the grip, lifting; 5-6 sword straight up high above the head, up on his toes; 7-8 the blade starts down, big step forward; 9 IMPACT: the blade smashes into the ground FAR in front, deep crouch; 10-12 holds the low pose (small shake); 13-14 pulls the sword up; 15-16 ready pose. | todo |
| 7 | jump | 12 / 6x2 | 1-2 crouch to jump; 3 take-off, legs straight; 4-5 rising, knees tucked, cape below; 6-7 top of the jump; 8-10 falling, legs reaching down, cape up; 11-12 landing crouch. Sword stays on the shoulder. Feet leave the ground line in 3-10. | todo |
| 8 | hurt | 8 / 4x2 | 1-2 hit from the front: head and chest jerk back; 3-4 staggers half a step back; 5-6 recovers balance; 7-8 ready pose. | todo |
| 9 | death | 12 / 6x2 | 1-2 struck, staggers back; 3-4 drops to one knee, the sword point on the ground; 5-6 leans on the sword; 7-8 the sword falls, he tips forward; 9-10 lands face down, cape settling over him; 11-12 still. | todo |
| 10 | chain | 12 / 6x2 | Skill Q, chain throw with the LEFT arm, the sword stays on the right shoulder. 1 ready; 2-3 left arm pulled far back; 4-5 whips the arm forward, the chain flies out straight to the right; 6-7 arm fully out, chain taut and long (to the cell edge); 8-10 yanks the chain back hard, leaning back; 11-12 ready. | todo |
| 11 | spin | 12 / 6x2 | Skill E, one full spin slash. 1 ready; 2-3 sword held out to the side at waist height with both hands; 4-9 turns round on the spot in even steps (side, three-quarter back, back, three-quarter front, front, three-quarter front), the blade always stretched out; 10 side again, blade in front; 11-12 ready. | todo |
| 12 | slam | 16 / 4x4 | Skill R, leaping slam. 1-2 crouch; 3-4 jumps up raising the sword; 5-7 high in the air, sword overhead; 8-9 falling forward; 10 IMPACT: lands and slams the blade into the ground in front, deep crouch; 11-12 holds; 13-14 rises; 15-16 ready. | todo |
| 13 | rage | 12 / 6x2 | Skill X, rage awakening. 1 ready; 2-4 crouches, fists clenched; 5-7 throws his head back, chest out, arms spread (roar); 8-9 holds the roar; 10-11 brings the sword back to the ready pose; 12 ready with the eyes glowing brighter. | todo |
| 14 | climb | 8 / 4x2 | BACK VIEW (use the back of `2_TURNAROUND.png`): climbing a rope, sword on his back: 1-2 right hand reaches high, left knee up; 3-4 pulls up; 5-6 left hand high, right knee up; 7-8 pulls up. Loops. | todo |
