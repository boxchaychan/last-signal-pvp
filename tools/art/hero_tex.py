"""Texture of the red-scarf hero (owner's design picture 2026-11-17, art/incoming/tribe3d/hero_ref.png) for tribe3d.html: the KayKit
Knight atlas, top half as it is (face, skin), bottom half (unused by the Knight's body) = new swatches the hero's body parts point to
(tools/art/hero_build.mjs remaps their UVs per part): purple tunic, dark purple, brown boots, gold bands, brown hair, bare-hand skin.
Each swatch keeps the light-to-dark profile of the steel / leather swatch it came from. Same lift as kaykit_recolor.py.
   python3 tools/art/hero_tex.py art/incoming/kaykit/adventurers_2.0/characters/knight_texture.png art/tribe3d/people/tex_hero_0.png"""
import sys, colorsys
from PIL import Image
CW, CH = 128, 256   # one swatch cell of the 1024 atlas: 8 columns x 4 rows
# slot (col, row in the bottom half) <- source cell (col, row), (hue, sat, value factor); hue None = keep the source colour
SLOTS = {
    (0, 2): ((3, 0), (256, .4, .78)),     # P    purple tunic          <- light steel
    (1, 2): ((7, 0), (256, .44, .66)),   # PD   dark purple           <- steel column
    (2, 2): ((7, 1), (254, .44, .6)),    # PD2  darker purple
    (3, 2): ((3, 0), (24, .5, .62)),     # B    brown boots           <- light steel
    (4, 2): ((7, 0), (22, .52, .5)),     # BD
    (5, 2): ((7, 1), (20, .52, .46)),    # BD2
    (6, 2): ((6, 0), (40, .78, 1.3)),     # G    gold bands            <- leather
    (7, 2): ((0, 1), (40, .78, 1.15)),    # G2   gold                  <- red rosette
    (0, 3): ((1, 1), (40, .78, .95)),     # G3   gold                  <- white
    (1, 3): ((1, 0), (14, .66, .42)),    # H    reddish-brown hair    <- blond hair
    (2, 3): ((4, 0), (255, .42, .7)),    # PD4  dark purple           <- dark steel
    (3, 3): ((0, 0), (None, 1, 1)),      # SK   skin (bare hands)     <- skin
    (4, 3): ((3, 0), (220, .1, .82)),    # S    steel grey (gorget)   <- light steel
    (5, 3): ((6, 0), (22, .55, .58)),    # BL   dark brown belt       <- leather
}
LIFT, SAT = .85, 1.1
src, out = sys.argv[1], sys.argv[2]
im = Image.open(src).convert('RGBA'); px = im.load(); o = im.copy(); q = o.load()
for (dc, dr), ((sc, sr), (nh, ns, vk)) in SLOTS.items():
    for y in range(CH):
        for x in range(CW):
            r, g, b, a = px[sc * CW + x, sr * CH + y]; h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            if nh is not None: h, s, v = nh / 360, ns, min(1, v * vk)
            q[dc * CW + x, dr * CH + y] = tuple(round(c * 255) for c in colorsys.hsv_to_rgb(h, s, v)) + (a,)
for y in range(o.height):
    for x in range(o.width):
        r, g, b, a = q[x, y]; h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        q[x, y] = tuple(round(c * 255) for c in colorsys.hsv_to_rgb(h, min(1, s * SAT), v ** LIFT)) + (a,)
o.save(out, optimize=True); print('wrote', out)
