# Plan: 3D map + video effects (2026-11-10, owner "ทำไมทำอะไรต้องทำ 3-4 รอบ ... วางแผนหน่อย")

Decide once, then build without rounds of fixes.

## Fixed numbers
- Character: PixelLab 128 px canvas, figure ~113 px; in the world ~76 units tall (ARX 1.5 art px per unit).
- 2D world: 6000 x 4000 units. A full 3D map at the same scale: ~190 x 126 tiles (hero 2.4 tiles tall, as in hd3d.html).
- Hero on screen: always a whole number of screen px per art px (PC 1, 3x phone 2), drawn flat on top of the 3D scene.

## Step 1 · camera (owner picks one of A-F in art/incoming/action/hd3d_cameras.png)
- A 30, B 40, C 54 (current), D 65, E 80 degrees, F 54 with a wide lens. Try any with `hd3d.html?pitch=40` (`&fov=`, `&dist=`).
- Our sprites are PixelLab "low top-down": the lower angles (A/B) match them; at D/E the upright trees, houses and the hero look
  like flat paper cut-outs from above.

## Step 2 · effect sizes (set by the cutter, not by the video)
`tools/video/vfx_cut.py` SIZE (world units, the hero is 76): hit 60, swing 200, chain_all / chain_ring 300, triple 260,
slam 190 (blast) + slam_ring 260, crack_line 300, shackle 200, rage 70, wave 120, hook 300. The video only has to stay inside its frame.

## Step 3 · videos (owner, Meta AI)
- Every video: attach `art/incoming/action/berserker/video_start/start_fx_spark.png` (small spark in the middle of a 16:9 green
  frame) + one block from `VFX_BERSERKER.txt` (each block already says EXTREME WIDE SHOT, landscape, the spark is the start).
- Meta AI ignores sizes written as fractions; the start picture + the wide-shot line keep it small; whatever still runs off the
  frame fades at the edge in the cutter.

## Step 4 · cut and check (Claude, one pass per clip)
`python3 tools/video/vfx_cut.py <mp4> <key>` (size from SIZE) → preview next to the Berserker → owner OK.

## Step 5 · into the game (after the owner's OK)
- B upright effects: billboards facing the camera. D ground effects: laid flat on the ground (decal), turned to the aim.
  S side effects: turned / mirrored toward the target.
- 2D action.html first (pfx), then the 3D map once the camera is chosen.

## First try of the reference look: `hd3d2.html` (2026-11-10)
Owner "ลองทำให้ได้ตามแบบแมพเค้า": camera 52 degrees, fov 18, distance 85 (zoom button 85 / 64 / 48); the hero from the half-size
sheets `art/action/h64/` (figure 55 px, built like berserker_build.sh with `--scale=1/2`), whole screen px per art px; map 72 x 52
tiles (crossroads, river + bridge, pond with island / stepping stones / watermill, camp, stone circle), ground merged per material
(side faces only where the neighbour is lower), grass / ferns / flowers / bushes instanced, trees 5-7 tiles tall, desaturated beige road,
low warm sun from the upper left, softer tilt-shift, wolves wandering. Screenshot `art/incoming/action/hd3d2_test.png`.

## Effects as parts (owner 2026-11-10 "ทำแค่อันเดียวแล้วให้ทำตามทิศทาง ไม่เอาสกิลเป็นก้อน")
Like game VFX artists: small single pieces made once, assembled by code per skill (turned to the aim, stretched to the distance,
repeated per target, moved, timed) = a particle system, so every skill follows its direction and targets. First: Q chains (one arm
cut from the star clip, `tools/video/vfx_one_arm.py`, one chain per monster). Parts to make (`docs/vfx-pack.html`, set
"เบอร์เซิร์กเกอร์ · ชิ้นส่วน", `art/incoming/action/berserker/video_start/VFX_BERSERKER_PARTS.txt`): slash, hit, boom, smoke,
sparks, flame (loop), crack. Already as parts: chain (vfx_bzchain1), ring cleave, ground ring, rune circle.
