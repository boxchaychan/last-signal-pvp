"""Zombie versions of the KayKit Adventurers 2.0 textures for zcity.html: peach skin -> sick grey-green, cloth faded / dirtied,
and a second variant with a different cloth tint so packs do not look cloned.
   python3 tools/art/zombie_skin.py art/incoming/kaykit/adventurers_2.0/characters art/zcity"""
import sys, colorsys, random
from PIL import Image
src, out = sys.argv[1], sys.argv[2]
JOBS = {'barbarian': [(0, 1.0), (200, .9)], 'rogue': [(0, 1.0), (30, .9)], 'knight': [(0, 1.0)], 'mage': [(0, 1.0), (110, .9)]}   # (cloth hue shift, value)
for name, variants in JOBS.items():
    im = Image.open(f'{src}/{name}_texture.png').convert('RGBA'); px = im.load()
    for vi, (shift, val) in enumerate(variants):
        o = im.copy(); q = o.load(); rnd = random.Random(vi * 7 + len(name))
        for y in range(o.height):
            for x in range(o.width):
                r, g, b, a = px[x, y]; h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
                if 0.02 < h < 0.11 and .18 < s < .55 and v > .8:   # skin (and its warm shadow)
                    h, s, v = 0.24 + (0.03 if v < .93 else 0), .32, v * .74
                elif v < .1:   # eyes / dark lines stay
                    pass
                else:   # cloth, leather, metal: faded, dirtier, a bit darker
                    h = (h + shift / 360) % 1; s = s * .55; v = v * .8 * val
                    h = h * .7 + 0.08 * .3 if s > .05 else h   # pulled toward mud
                q[x, y] = tuple(int(c * 255) for c in colorsys.hsv_to_rgb(h, min(1, s), min(1, v))) + (a,)
        o.save(f'{out}/ztex_{name}_{vi}.png'); print('wrote', f'{out}/ztex_{name}_{vi}.png')
