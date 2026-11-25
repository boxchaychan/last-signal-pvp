"""Skill icons for the moon blade, made from his own effect sheets (no new picture): python tools/art/moon_icons.py
-> art/dune/env/moon_icons.webp, 3 x 3 cells of 160 px. In dune.html an icon number from 300 up means this sheet:
0 K wave, 1 L shadow step, 2 U moon dance (spin), 3 I moonfall, 4 O blade storm (flurry), 5 R full moon, 6 dash, 7 chain button, 8 spare."""
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sp = json.load(open('art/dune/sprites.json')); C = 160
PICK = [('fx_m_wave', 14), ('fx_m_c3', 4), ('fx_m_spin', 8), ('fx_m_fall', 14), ('fx_m_flurry', 12), ('fx_m_moon', 5), ('fx_m_c1', 3), ('fx_m_c1', 5), ('fx_m_wave', 6)]
S = Image.new('RGBA', (C * 3, C * 3), (0, 0, 0, 0))
for n, (k, f) in enumerate(PICK):
    m = sp[k]; im = Image.open(m['src']).convert('RGBA'); f = min(f, m['n'] - 1); c = im.crop(((f % m['cols']) * m['w'], (f // m['cols']) * m['h'], (f % m['cols'] + 1) * m['w'], (f // m['cols'] + 1) * m['h']))
    bb = c.getchannel('A').point(lambda v: 255 if v > 40 else 0).getbbox(); c = c.crop(bb) if bb else c; c.thumbnail((C - 34, C - 34), Image.LANCZOS)
    cell = Image.new('RGBA', (C, C), (0, 0, 0, 0)); d = ImageDraw.Draw(cell)
    bg = Image.new('RGBA', (C, C)); g = np.zeros((C, C, 4), np.uint8); yy, xx = np.mgrid[0:C, 0:C]; r = np.hypot(xx - C * .45, yy - C * .4) / C
    g[..., 0] = np.clip(58 - r * 40, 14, 255); g[..., 1] = np.clip(22 - r * 14, 6, 255); g[..., 2] = np.clip(96 - r * 60, 28, 255); g[..., 3] = 255
    mask = Image.new('L', (C, C), 0); ImageDraw.Draw(mask).rounded_rectangle((4, 4, C - 5, C - 5), 26, fill=255); cell.paste(Image.fromarray(g, 'RGBA'), (0, 0), mask)
    if n == 7:   # chain button: two crescents linked
        c2 = c.copy().transpose(Image.FLIP_LEFT_RIGHT); cell.alpha_composite(c2, ((C - c.width) // 2 - 14, (C - c.height) // 2 + 6))
    cell.alpha_composite(c, ((C - c.width) // 2, (C - c.height) // 2))
    d.rounded_rectangle((4, 4, C - 5, C - 5), 26, outline=(205, 190, 255, 255), width=5); d.rounded_rectangle((10, 10, C - 11, C - 11), 21, outline=(40, 12, 60, 255), width=3)
    S.paste(cell, ((n % 3) * C, (n // 3) * C))
S.save('art/dune/env/moon_icons.webp', 'WEBP', quality=90, method=6); print('art/dune/env/moon_icons.webp')
