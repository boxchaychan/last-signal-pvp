---
name: sprite-importer
description: Turn a sprite sheet, a GIF or a video the owner sends into game-ready frames (cut, background off, feet lined up, packed) and wire them into combo.html or map.html. Use when the owner says pictures are ready or uploads a sheet / clip.
---
# Importing sprites

1. Copy the raw file into `art/incoming/<task>/` unchanged. Look at it at full size; note grid, background, effects, turned views.
2. Cut:
   - sheet on white / see-through with figures not on a grid: copy the pattern of `tools/art/meta_sheet.py` (per-frame cut rules, pinned by the ground line / feet).
   - video on a flat key colour: `tools/art/meta_combo.py` (ffmpeg → key → pick frames by hand → pack).
   - white background: `tools/art/white_cut.py --edge-only --no-ring`; GPT pixel sheets: `tools/art/gptpx.py`.
   - still views for the map: `tools/art/chibi_map_hero.py <src> <name> <min size> [halo]`.
3. One cell size, one feet point for every frame of a set; hard alpha for pixel art, smooth for painted art.
4. View the packed sheet before wiring it (frames cut off, neighbours leaking in, size jumps).
5. Wire in: `combo.html` (a mode with steps = frame lists + hit frame) or `map.html` (`?hero=`). Test with the gameplay-qa skill.
6. Nothing drawn by the generator is removed without asking; say what was left out and why.
