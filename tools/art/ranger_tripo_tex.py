"""The ★★★ archer's outfit in the colours of the owner's Tripo huntress (owner 2026-11-17 "ชุดด้วย"): the KayKit Adventurers 2.0 Ranger
atlas (8 x 3 swatch cells of 128 x 256) recoloured cell by cell, each cell keeping its own light-to-dark profile; skin stays as KayKit
painted it. Then the same lift as tools/art/kaykit_recolor.py (the game camera looks down on the people).
Cells (found by painting each one a test colour): r0c0 skin, r0c1 hair / brows / beard, r0c2 eyes, r0c3 buckles, r0c5 shirt + trousers,
r0c6 vest sides, r0c7 belt + straps, r1c0 scarf + cape, r1c1 wrist bands, r1c6 quiver, r2c0 shoulder leaves, r2c3 boots, r2c7 gloves.
   python3 tools/art/ranger_tripo_tex.py art/incoming/kaykit/adventurers_2.0/characters/ranger_texture.png art/tribe3d/people/tex_range_t.png"""
import sys, colorsys
from PIL import Image
src, out = sys.argv[1], sys.argv[2]
CELLS = {   # (row, col): target colour of the cell's brightest part (Tripo huntress palette)
    (0, 1): (92, 58, 42),     # hair: dark chocolate like her braids
    (0, 3): (236, 190, 84),   # buckles: gold
    (0, 5): (246, 240, 228),  # shirt + trousers: ivory
    (0, 6): (226, 204, 168),  # vest sides: warm cream (her fur)
    (0, 7): (120, 78, 52),    # belt + straps: brown leather
    (1, 0): (88, 176, 236),   # scarf + cape: her sky blue
    (1, 1): (236, 190, 84),   # wrist bands: gold
    (1, 6): (128, 84, 56),    # quiver: leather
    (2, 0): (240, 234, 222),  # shoulder leaves -> white fur tufts
    (2, 3): (244, 238, 226),  # boots: white
    (2, 7): (110, 72, 50),    # gloves: brown
}
LIFT, SAT = .85, 1.1
im = Image.open(src).convert('RGBA'); px = im.load()
for (r, c), (tr, tg, tb) in CELLS.items():
    x0, y0 = c * 128, r * 256
    lum = lambda p: .3 * p[0] + .59 * p[1] + .11 * p[2]
    top = max(lum(px[x, y]) for x in range(x0, x0 + 128) for y in range(y0, y0 + 256)) or 1
    for y in range(y0, y0 + 256):
        for x in range(x0, x0 + 128):
            p = px[x, y]; k = lum(p) / top
            px[x, y] = (int(tr * k), int(tg * k), int(tb * k), p[3])
for y in range(im.height):   # lift every colour like the other people textures
    for x in range(im.width):
        r, g, b, a = px[x, y]; h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255); v = v ** LIFT; s = min(1, s * SAT)
        r, g, b = colorsys.hsv_to_rgb(h, s, v); px[x, y] = (round(r * 255), round(g * 255), round(b * 255), a)
im.save(out); print('wrote', out)
