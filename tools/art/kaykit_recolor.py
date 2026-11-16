"""Stone-age colour variants of the KayKit character textures for tribe3d.html (clothes swatches only: the Barbarian's
blue shirt, the Rogue's green / teal cloth become leather, ochre, rust, moss). Then every colour is lifted (value ** LIFT,
a little more saturation): the game's camera looks down on dark hoods and capes, unlifted people read as dark blobs.
   python3 tools/art/kaykit_recolor.py <kaykit .../Characters/gltf> art/tribe3d/people"""
import sys, colorsys
from PIL import Image
src, out = sys.argv[1], sys.argv[2]
JOBS = {   # texture: (hue range of the cloth in degrees, [(new hue, saturation factor, value factor), ...])
    'barbarian': ((190, 235), [(30, .8, 1.05), (85, .6, .95), (5, 1, 1)]),
    'rogue': ((95, 200), [(27, .7, 1), (42, .8, 1.1), (8, .85, .95)]),
}
LIFT, SAT = .85, 1.1
for name, ((h0, h1), variants) in JOBS.items():
    im = Image.open(f'{src}/{name}_texture.png').convert('RGBA'); px = im.load()
    for vi, (nh, sk, vk) in enumerate(variants):
        o = im.copy(); q = o.load()
        for y in range(o.height):
            for x in range(o.width):
                r, g, b, a = px[x, y]; h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
                if s > .2 and h0 <= h * 360 <= h1: h, s, v = nh / 360, min(1, s * sk), min(1, v * vk)
                r2, g2, b2 = colorsys.hsv_to_rgb(h, min(1, s * SAT), v ** LIFT); q[x, y] = (round(r2 * 255), round(g2 * 255), round(b2 * 255), a)
        o.save(f'{out}/tex_{name[:5]}_{vi}.png', optimize=True); print(name, vi)
