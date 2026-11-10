# The Berserker's effects (owner 2026-11-10 "ทำ vfx ไว้ โทนแดงนีออน ดำ ไฟ"): every effect the swordsman's kit draws is
# recoloured by brightness onto one ramp: black smoke -> deep crimson -> neon red -> red-orange fire -> hot white core.
# Shapes and timing stay the same; the game swaps <key> for <key>_bz when the hero is the Berserker.
#   python3 tools/art/bz_fx.py            -> fx/<key>_bz.png + manifest entries
#   python3 tools/art/bz_fx.py --preview <out.png>   -> before / after strip of a few frames each
import json, sys
import numpy as np
from PIL import Image

KEYS = ['pfx_fireline', 'pfx_earthsplit', 'pfx_whirl', 'pfx_whirl_k', 'pfx_dashstrike_v', 'pfx_swcharge', 'pfx_swslash', 'cslam', 'gslam', 'quake', 'parry',
        'wvfx1', 'wvfx2', 'wvfx3', 'wvfx4', 'wvfx5']
# brightness -> colour (the ramp), brightness 0..1
RAMP = [(0.00, (8, 3, 6)), (0.25, (45, 4, 14)), (0.45, (150, 10, 34)), (0.62, (255, 28, 60)),
        (0.80, (255, 80, 44)), (0.93, (255, 130, 70)), (1.00, (255, 215, 170))]   # cores stay fire-orange, not white

def recolour(im):
    a = np.asarray(im.convert('RGBA')).astype(float)
    rgb, al = a[..., :3] / 255, a[..., 3]
    L = .45 * rgb.max(-1) + .55 * (rgb @ [.3, .55, .15])          # bright cores stay bright, coloured midtones fall in the middle
    L = np.clip(L, 0, 1) ** 1.5                                   # absolute brightness, midtones pushed down: dust and smoke go black-red
    xs = [r[0] for r in RAMP]; out = np.zeros_like(a)
    for c in range(3): out[..., c] = np.interp(L, xs, [r[1][c] for r in RAMP])
    out[..., 3] = al
    return Image.fromarray(out.clip(0, 255).astype(np.uint8))

def frames(im, m, idx):
    w, h, cols = m['w'], m['h'], m.get('cols', m['n'])
    return [im.crop(((i % cols) * w, (i // cols) * h, (i % cols + 1) * w, (i // cols + 1) * h)) for i in idx]

if __name__ == '__main__':
    man = json.load(open('fx/manifest.json'))
    if '--preview' in sys.argv:
        out = sys.argv[sys.argv.index('--preview') + 1]; rows = []
        for k in KEYS[:11]:
            m = man[k]; im = Image.open(f'fx/{k}.png').convert('RGBA'); n = m['n']; idx = [n // 5, n // 3, n // 2, 2 * n // 3]
            src = frames(im, m, idx); dst = frames(recolour(im), m, idx); sc = min(1, 120 / m['h'])
            cells = [f.resize((max(1, int(f.width * sc)), max(1, int(f.height * sc)))) for f in src + dst]
            W = sum(c.width for c in cells) + 30; row = Image.new('RGBA', (W, max(c.height for c in cells)), (96, 140, 70, 255)); x = 0
            for i, c in enumerate(cells):
                if i == len(src): x += 30
                row.alpha_composite(c, (x, 0)); x += c.width
            rows.append(row)
        sheet = Image.new('RGBA', (max(r.width for r in rows), sum(r.height for r in rows) + 4 * len(rows)), (40, 40, 40, 255)); y = 0
        for r in rows: sheet.alpha_composite(r, (0, y)); y += r.height + 4
        sheet.save(out); print(out, sheet.size); sys.exit()
    for k in KEYS:
        recolour(Image.open(f'fx/{k}.png')).save(f'fx/{k}_bz.png', optimize=True)
        man[k + '_bz'] = dict(man[k], src=man[k].get('src', '') + ' / Berserker tone (tools/art/bz_fx.py)')
    json.dump(man, open('fx/manifest.json', 'w'), separators=(',', ':')); print(len(KEYS), 'sheets -> fx/*_bz.png')
