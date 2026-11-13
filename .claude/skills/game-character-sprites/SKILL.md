---
name: game-character-sprites
description: Make or convert a game character's pictures for this project (3-view sheet, pixel version at a chosen size, pose-sheet prompts for GPT / Codex / Meta AI). Use when the owner brings a character picture, asks for a new character, a size test, or a prompt for a move.
---
# Character sprites (this project)

Who draws: GPT / Codex / Meta AI draw; PixelLab only redraws to true pixels; our tools cut and check. Never generate with PixelLab unless the owner says "เจน" / "ทำเลย"; say the job and its credit cost first; never pro modes first; log every job in `docs/action-game.md`.

Recipe that works for the chibi pixel style:
1. A 3-view sheet (front, side facing right, back) on white, neutral pose, weapon in the right hand. Prompt pattern: `art/incoming/darkchibi/PROMPT_swordsman_3view_fromref.txt`.
2. Have GPT redraw it as a pixel-STYLE sheet with a pixel example attached (`art/incoming/darkchibi/sword_v1/PROMPT_GPT_pixelstyle.txt`). "8 bit / 16 bit" in the prompt only changes shading steps.
3. True pixels: if the sheet is already on an even grid (~9 px blocks) snap it free: `GPTPX_GRID=8.6,9.5 python3 tools/art/gptpx.py in.png out.png 16`. Otherwise PixelLab `image_to_pixelart` redraw B (default mode, 1 credit, output ≤ 512 px; split the sheet if bigger) through `PL_KEY=proxy-injected python3 tools/pl_rpc.py`.
4. Size: this costume is crisp at body 128 or 256, readable at 64, mush at 36. Open the exact input picture before any paid job.

Moves: shared, not generated per character. Pose sheets: `art/poses/std/` (idle, run, roll, hurt, death, weapon attacks), `art/poses/ref_sketch/` (sketch-based slash combo), `tools/art/pose_guide.py` / `combo_guide.py` for new ones. One move per picture, 8 numbered cells, the character picture attached second. For Codex add a row to `docs/codex/action/SLASH.md`.

Never strip effects or parts a generator drew without asking; keep raw files. Another artist's signed work is reference only and is not stored.
