"""Stone-age colour variants of the KayKit character textures for tribe3d.html (clothes swatches only: the Barbarian's
blue shirt, the Rogue's green / teal cloth become leather, ochre, rust, moss). Then every colour is lifted (value ** LIFT,
a little more saturation): the game's camera looks down on dark hoods and capes, unlifted people read as dark blobs.
   python3 tools/art/kaykit_recolor.py <kaykit .../Characters/gltf> art/tribe3d/people"""
import sys, colorsys
from PIL import Image
src, out = sys.argv[1], sys.argv[2]
JOBS = {   # texture: (hue range of the cloth in degrees, [(new hue, saturation factor, value factor), ...])
    'barbarian': ((190, 235), [(30, .8, 1.05), (85, .6, .95), (5, 1, 1)]),
    'rogue': ((95, 200), [(27, .7, 1), (42, .8, 1.1), (8, .85, .95), (128, .62, .8), (172, .85, .9)]),   # 3 = forest green (hooded hunters), 4 = deep teal (2-star archer)
    'knight': ((0, 0), [(None, 1, 1), [('grey', 45, .58, 1.45)]]),   # 0 = lift only, 1 = ★★: grey steel -> bright gold armour
    'mage': ((230, 300), [(None, 1, 1), [(225, 300, 268, 1.2, .62), (300, 345, 350, 1.05, .6), (12, 45, 45, 1.1, 1.2, .62, .62)]]),   # + the pink cape -> deep crimson   # gold only on the bright saturated orange trim (not skin / hair)   # 0 = lift only, 1 = ★★ shaman: deep royal violet robes + gold trim
}
LIFT, SAT = .85, 1.1
for name, ((h0, h1), variants) in JOBS.items():
    im = Image.open(f'{src}/{name}_texture.png').convert('RGBA'); px = im.load()
    for vi, var in enumerate(variants):
        rules = var if isinstance(var, list) else [(h0, h1) + tuple(var)]   # a variant = one (hue, sat, value) or a list of (h0, h1, hue, sat, value)
        o = im.copy(); q = o.load()
        for y in range(o.height):
            for x in range(o.width):
                r, g, b, a = px[x, y]; h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
                for rule in rules:
                    if rule[0] == 'grey':   # ('grey', hue, sat, value factor): tint the unsaturated metal (not white eyes / dark lines)
                        if s < .14 and .3 < v < .93: h, s, v = rule[1] / 360, rule[2], min(1, v * rule[3])
                        break
                    a0, a1, nh, sk, vk = rule[:5]; smin, vmin = (rule[5], rule[6]) if len(rule) > 5 else (.2, 0)
                    if nh is not None and s > smin and v >= vmin and a0 <= h * 360 <= a1: h, s, v = nh / 360, min(1, s * sk), min(1, v * vk); break
                r2, g2, b2 = colorsys.hsv_to_rgb(h, min(1, s * SAT), v ** LIFT); q[x, y] = (round(r2 * 255), round(g2 * 255), round(b2 * 255), a)
        o.save(f'{out}/tex_{name[:5]}_{vi}.png', optimize=True); print(name, vi)
