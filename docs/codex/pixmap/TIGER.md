# Pixel map hero: the TIGER (for `pixmap.html`, 3D map + 2D pixel tiger)

Owner phrases: "ทำเฟรมเสือวิ่ง" = task 1. "ทำเฟรมเสือยืน" = task 2. "ทำเฟรมเสือฟัน" = task 3.
Branch `codex/tiger-frames`, pictures into `art/incoming/tiger_frames/` (full size PNG, not shrunk), plus `REPORT_TH.txt` (Thai, short: which file is which, what may be off). Open a pull request, do not merge.

## The character (use ONLY these, same look in every frame)
- `art/incoming/war/gpt_tiger_8bit.png` = THE tiger: 8 bit pixel art, standing, three-quarter view facing right and toward the viewer, black hood with ears, white fur collar, red sash, black clothes, claws, striped tail behind.
- Style: 8 bit pixel art, chunky bold pixels, thick black outline, few colours (the owner: "8 bit" makes it pretty). Same pixel size as that picture.

## Task 1: run cycle (8 frames)
Motion reference: `art/poses/std/common/run.png` (8 numbered cells, 4 x 2, a side-view run loop). Use it ONLY for the poses (lean, arms, legs, which foot is down).
Draw the tiger once per cell in the same pose, keeping the tiger's own view (three-quarter, facing right and toward the viewer). The tail swings with the run.
One sheet, 4 x 2 grid, order 1-8 (top row left to right, then bottom row), the same size in every cell, feet on one ground line, nothing crossing cells.
No numbers, borders, ground line, motion lines, dust, shadow or text. Plain flat pure white background, 1536 x 1024. File: `tiger_run.png`.

## Task 2: idle (4 frames)
Motion reference `art/poses/std/common/idle.png`. Same rules, a 4 x 1 or 4 x 2 grid: breathing, the tail sways, claws relaxed. File: `tiger_idle.png`.

## Task 3: claw attack (8 frames)
One sheet, 4 x 2: wind-up (pull the right claw back), a fast forward slash with both claws, follow-through, back to the idle stance. Same view and size. No swoosh / effects (the game adds them). File: `tiger_claw.png`.

## Check before you finish
Put the finished sheet next to `gpt_tiger_8bit.png` and look: same face, same colours, same size? If a cell is off, redraw that sheet. Say in `REPORT_TH.txt` what still looks off.
