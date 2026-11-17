"""Stone-age colour variants of the KayKit character textures for tribe3d.html (clothes swatches only: the Barbarian's
blue shirt, the Rogue's green / teal cloth become leather, ochre, rust, moss). Now for Adventurers 2.0 (see JOBS). Then every colour is lifted (value ** LIFT,
a little more saturation): the game's camera looks down on dark hoods and capes, unlifted people read as dark blobs.
   python3 tools/art/kaykit_recolor.py art/incoming/kaykit/adventurers_2.0/characters art/tribe3d/people"""
import sys, colorsys
from PIL import Image
src, out = sys.argv[1], sys.argv[2]
JOBS = {   # KayKit Adventurers 2.0 textures (owner 2026-11-17: 2.0 only). A variant = (hue, sat, value) for the cloth hue range, or a list of
    # rules (h0, h1, hue, sat, value[, min sat, min value]) / ('grey', hue, sat, value) for unsaturated metal; None = lift only
    'barbarian': ((15, 40), [(None, 1, 1), (24, 1.15, .78), [(190, 230, 355, 1.6, 1.05), (40, 60, 45, 1.25, 1.15, .4, .5)]]),   # 0 villager, 1 darker leather, 2 chief: crimson + bright gold
    'rogue': ((120, 180), [(None, 1, 1), (27, .7, 1), (42, .8, 1.1), (8, .85, .95)]),   # 0 hooded hunter ★ (forest green), 1-3 villager women: leather, ochre, rust
    'knight': ((0, 0), [(None, 1, 1), [('grey', 45, .58, 1.45), (340, 360, 222, .9, .9), (0, 15, 222, .9, .9)],
                        [('grey', 262, .28, .58), (340, 360, 352, 1.3, 1.05), (0, 15, 352, 1.3, 1.05), (35, 60, 45, 1.3, 1.25, .3, .4)]]),   # ★ steel, ★★ gold + royal blue cape, ★★★ obsidian + crimson + gold
    'mage': ((230, 290), [(None, 1, 1), [(225, 300, 268, 1.2, .62), (300, 345, 350, 1.05, .6), (12, 45, 45, 1.1, 1.2, .62, .62)],
                          [(225, 300, 232, .9, .38), (300, 345, 186, 1.2, 1.1), (12, 45, 186, 1, 1.25, .62, .62), (150, 200, 186, 1.2, 1.2)]]),   # ★ purple, ★★ royal violet + gold, ★★★ midnight + arcane cyan
    'ranger': ((195, 235), [(None, 1, 1), [(195, 235, 355, 1.1, .9), (20, 45, 40, 1.1, .75, .1, .3)]]),   # ★★ archer (blue scarf), ★★★ crimson scarf + dark leather
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
