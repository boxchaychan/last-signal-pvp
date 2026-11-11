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
Guides can also come from the owner's Meta AI clips (motion only, the face does not matter): Claude runs
`python3 tools/art/video_pose_guide.py <clip.mp4> <action> <frames> [start s] [end s]` (N evenly spaced frames → grey
silhouettes, numbered). Example: `walk_video_POSES.png` = one walk cycle of the owner's clip (1.0-2.35 s, 12 frames).

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

## Several sheets per move (owner 2026-11-11 "สั่งชีทแบบละเอียด แบ่งหลายชีท")
Big moves are split into PARTS, one picture per part, 12 frames each (6x2). The LAST frame of a part and the FIRST frame of
the next part are the SAME pose, so Claude can join them without a jump. Attach the previous part's picture too, so the
character stays identical. File names: `anim/<action>_p1.png`, `anim/<action>_p2.png`, ...

## Queue
| # | action | part | frames / grid | what happens in this part (draw small, even steps) | status |
|---|--------|------|---------------|-----------------------------------------------------|--------|
| 1 | idle | 1 | 12 / 6x2 | Standing ready, sword on the right shoulder. One slow heavy breath: rise (1-6), cape lifts a little, come down, knees bend slightly at the lowest point (7-12). 12 leads back into 1. | todo |
| 2 | walk | - | 12 / 6x2 | (done by the owner, `anim/walk_sheet_owner.webp`) | done |
| 3 | run | 1 | 12 / 6x2 | Heavy run, leaning forward, sword on the shoulder: right foot lands (1), lowest (3), push off (4), airborne (5), left knee forward (6), left foot lands (7), lowest (9), push off (10), airborne (11), right knee forward (12). Loops. | todo |
| 4 | attack1 | p1 | 12 / 6x2 | HIT 1 wind-up: from the ready pose (1) he takes the sword off the shoulder (2-5) and pulls it far back behind him, body twisting away, weight on the back foot (6-12). | todo |
| 5 | attack1 | p2 | 12 / 6x2 | HIT 1 strike: from the last pose of p1 (1) he steps forward and swings the blade round at waist height (2-5), IMPACT at 6 (arms fully stretched, blade level, reaching FAR in front), follow-through past the front (7-12). | todo |
| 6 | attack1 | p3 | 12 / 6x2 | HIT 1 recovery: from the last pose of p2 (1) he brings the sword back (2-8) and rests it on the shoulder in the ready pose (9-12). | todo |
| 7 | attack2 | p1 | 12 / 6x2 | HIT 2 wind-up: from the ready pose (1) he drops the blade low behind him and crouches (2-12). | todo |
| 8 | attack2 | p2 | 12 / 6x2 | HIT 2 strike: sweeps the blade forward low (1-5), IMPACT at 6 (rising diagonal, tip high in front, arms stretched), blade carries on above the head (7-12). | todo |
| 9 | attack2 | p3 | 12 / 6x2 | HIT 2 recovery: from above the head back down to the ready pose (1-12). | todo |
| 10 | attack3 | p1 | 12 / 6x2 | HIT 3 wind-up: both hands on the grip (1-4), lifting the sword straight up high above the head, up on his toes (5-12). | todo |
| 11 | attack3 | p2 | 12 / 6x2 | HIT 3 slam: big step forward, the blade comes down (1-5), IMPACT at 6 (the blade smashes into the ground FAR in front, deep crouch), holds the low pose with a small shake (7-12). | todo |
| 12 | attack3 | p3 | 12 / 6x2 | HIT 3 recovery: pulls the sword out of the ground (1-6), back to the ready pose (7-12). | todo |
| 13 | jump | 1 | 12 / 6x2 | Crouch (1-2), take-off (3), rising knees tucked (4-5), top (6-7), falling legs reaching down (8-10), landing crouch (11-12). Feet off the ground in 3-10. | todo |
| 14 | hurt | 1 | 8 / 4x2 | Hit from the front: head and chest jerk back (1-2), staggers back (3-4), recovers (5-6), ready (7-8). | todo |
| 15 | death | p1 | 12 / 6x2 | Struck, staggers back (1-4), drops to one knee, sword point on the ground (5-8), leans on the sword (9-12). | todo |
| 16 | death | p2 | 12 / 6x2 | The sword falls (1-4), he tips forward (5-8), lies face down, cape settling over him, then still (9-12). | todo |
| 17 | chain | p1 | 12 / 6x2 | Skill Q (sword stays on the right shoulder): left arm pulled far back (1-5), whips forward (6-8), the chain flies out straight to the right to the cell edge (9-12). | todo |
| 18 | chain | p2 | 12 / 6x2 | Arm fully out, chain taut (1-3), yanks the chain back hard, leaning back (4-8), back to the ready pose (9-12). | todo |
| 19 | spin | p1 | 12 / 6x2 | Skill E: from ready (1) the sword comes out to the side at waist height with both hands (2-4), turning round (5-12: side, 3/4 back, back, 3/4 back, ...), the blade always stretched out. | todo |
| 20 | spin | p2 | 12 / 6x2 | Turning on (1-8: 3/4 front, front, 3/4 front, side), blade in front (9), back to the ready pose (10-12). | todo |
| 21 | slam | p1 | 12 / 6x2 | Skill R: crouch (1-3), jumps up raising the sword (4-8), high in the air, sword overhead (9-12). | todo |
| 22 | slam | p2 | 12 / 6x2 | Falling forward (1-5), IMPACT at 6 (lands and slams the blade into the ground in front, deep crouch), holds (7-12). | todo |
| 23 | slam | p3 | 12 / 6x2 | Rises and pulls the sword up (1-8), ready (9-12). | todo |
| 24 | rage | p1 | 12 / 6x2 | Skill X: crouches, fists clenched (1-5), throws his head back, chest out, arms spread in a roar (6-12). | todo |
| 25 | rage | p2 | 12 / 6x2 | Holds the roar (1-4), brings the sword back to the ready pose (5-10), ready with the eyes glowing brighter (11-12). | todo |
| 26 | climb | 1 | 8 / 4x2 | BACK VIEW (the back of `2_TURNAROUND.png`): climbing a rope, sword on his back: right hand high, left knee up (1-2), pull (3-4), left hand high, right knee up (5-6), pull (7-8). Loops. | todo |
