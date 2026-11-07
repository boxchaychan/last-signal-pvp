ARTEMIS / GOD HUNTER — EXTRACTED ANIMATION DRAFTS

Directions: SOUTH (toward player), EAST (right), NORTH (back). WEST can be mirrored from EAST in Godot.
Actions: idle 4 frames, attack 6 frames, skill 6 frames. No walk in exported game sheets.
Each game PNG sprite sheet uses 128x128 px cells, uniform size, with transparent alpha background.
The 4-frame sheets are 2 columns x 2 rows (256x256), and 6-frame sheets 3 columns x 2 rows (384x256).
Source: AI illustration/sprite layouts based on the user's Artemis reference.
turnaround/turnaround.png: three views (SOUTH, EAST, NORTH).
frames_128: 48 standalone PNG sprites.
sheets_128: nine sheets for the three directions and actions.
gifs: nine looping previews on white background.
east_detail_128: an alternate higher-detail right-facing set (16 frames) cropped from a separate generated sheet.
sources: full-sized untouched generated masters and original reference; do not mistake these for polished gameplay sheets.

IMPORTANT: These are a preliminary automated extraction from generated illustration, not manually corrected animation.
Some frames may contain visual energy/arrow effects, unlike the source prompt which requested none.
The still poses, uniform baseline, bow and quiver should be checked against the original reference before a production release.

Godot 4 import: Add sheet PNG as SpriteFrames > Add frames from a Sprite Sheet; select Hframes=2/Vframes=2 for idle, or 3/2 for attack/skill.
Frame order: left-to-right, first top then bottom. Suggested FPS: idle=4, attack=8, skill=8.
