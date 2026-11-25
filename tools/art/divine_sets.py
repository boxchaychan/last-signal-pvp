"""Game-size crops of the Codex god sets for divine.html (free).
  python3 tools/art/divine_sets.py
Each set in art/divine/<set>/ has idle_key / attack_key / skill_key (512 frames, feet at 256,500, same body size as Zeus), a spirit and one effect.
All poses of all sets use ONE scale (Zeus's idle body 322 px -> 200 px), so the gods keep the sizes Codex drew them at.
-> art/divine/<set>_<pose>.png, <set>_spirit.png, <set>_fx.png and art/divine/sets.json (sizes + x anchor of the body)."""
import json, os
from PIL import Image
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'); D = os.path.join(R, 'art/divine')
SETS = {'zeus': ('vfx_zeus_spirit', 'vfx_lightning_slash', 240), 'thor': ('vfx_thor_spirit', 'vfx_hammer_shock', 220), 'anubis': ('vfx_anubis_spirit', 'vfx_sand_beam', 240)}
F = 200 / 322; out = {}
for name, (spirit, fx, fxw) in SETS.items():
    src = os.path.join(D, name); o = {}
    if not os.path.isdir(src): continue
    for pose in ('idle', 'attack', 'skill'):
        im = Image.open(os.path.join(src, pose + '_key.png')).convert('RGBA'); x0, y0, x1, y1 = im.getbbox(); c = im.crop((x0, y0, x1, y1))
        w, h = round(c.width * F), round(c.height * F); c.resize((w, h), Image.LANCZOS).save(os.path.join(D, f'{name}_{pose}.png'))
        o[pose] = {'w': w, 'h': h, 'ax': round((256 - x0) / (x1 - x0), 3)}
    im = Image.open(os.path.join(src, spirit + '.png')).convert('RGBA'); c = im.crop(im.getbbox()); c = c.resize((round(c.width * 300 / c.height), 300), Image.LANCZOS); c.save(os.path.join(D, f'{name}_spirit.png')); o['spirit'] = {'w': c.width, 'h': 300}
    im = Image.open(os.path.join(src, fx + '.png')).convert('RGBA'); c = im.crop(im.getbbox()); c = c.resize((fxw, round(c.height * fxw / c.width)), Image.LANCZOS); c.save(os.path.join(D, f'{name}_fx.png')); o['fx'] = {'w': fxw, 'h': c.height}
    out[name] = o
json.dump(out, open(os.path.join(D, 'sets.json'), 'w'), indent=1); print(json.dumps(out))
