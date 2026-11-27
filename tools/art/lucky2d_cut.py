# Cut the Codex cartoon sheets of lucky.html ("ผู้กล้าเสี่ยงดวง", smooth 2D) into single sprites.
#   python tools/art/lucky2d_cut.py
# Reads art/incoming/lucky2d/<sheet>.png (grids of equal cells, transparent or one flat background colour), writes
# art/lucky2d/<prefix><name>.png + sprites.json (name -> f, w, h in design units, ax / ay = foot point) + arena.jpg.
# One scale per sheet (from the median figure height), so the figures keep the sizes the sheet drew them at: sizes stay in proportion.
import os, json
import numpy as np
from PIL import Image
SRC, OUT, PXU = 'art/incoming/lucky2d', 'art/lucky2d', 3.4   # PXU = stored pixels a design unit (a 390-unit-wide phone screen at 3x)
SHEETS = [
    ('heroes_a.png', 3, 2, 'h_', ['recruit', 'archer', 'icemage', 'firemage', 'ninja', 'paladin'], 47),
    ('monsters_a.png', 3, 2, 'm_', ['slime', 'mush', 'goblin', 'wolf', 'ghost', 'skel'], 33),
    ('boss_a.png', 1, 1, 'm_', ['king'], 92),
    ('icons_a.png', 4, 2, 'ic_', ['coin', 'clover', 'skull', 'heart', 'swords', 'scroll', 'gem', 'clock'], 30),
]
def alpha_of(im):
    a = np.asarray(im).astype(int)
    if a[..., 3].min() < 250: return a[..., 3].astype(np.uint8), a
    key = np.median(np.concatenate([a[:6, :6, :3].reshape(-1, 3), a[-6:, -6:, :3].reshape(-1, 3), a[:6, -6:, :3].reshape(-1, 3), a[-6:, :6, :3].reshape(-1, 3)]), axis=0)
    d = np.sqrt(((a[..., :3] - key) ** 2).sum(-1)); al = np.clip((d - 60) / 60 * 255, 0, 255)       # flat background colour -> alpha, soft edge
    return al.astype(np.uint8), a
os.makedirs(OUT, exist_ok=True); meta = {}
if os.path.exists(os.path.join(OUT, 'sprites.json')): meta = json.load(open(os.path.join(OUT, 'sprites.json')))
for f, cols, rows, pre, names, target in SHEETS:
    p = os.path.join(SRC, f)
    if not os.path.exists(p): print('no', f); continue
    im = Image.open(p).convert('RGBA'); al, a = alpha_of(im); rgba = np.dstack([a[..., :3].astype(np.uint8), al]); W, H = im.size; cw, ch = W // cols, H // rows; cells = []
    for i, name in enumerate(names):
        cx, cy = (i % cols) * cw, (i // cols) * ch; c = rgba[cy:cy + ch, cx:cx + cw]; ys, xs = np.where(c[..., 3] > 40)
        if not len(ys): print('empty cell', name); continue
        cells.append((name, Image.fromarray(c[ys.min():ys.max() + 1, xs.min():xs.max() + 1])))
    med = float(np.median([c.size[1] for _, c in cells])); k = target / med * PXU                   # one scale for the whole sheet
    for name, c in cells:
        w, h = max(1, round(c.size[0] * k)), max(1, round(c.size[1] * k)); c2 = c.resize((w, h), Image.LANCZOS); b = np.asarray(c2)[..., 3] > 60; ys, xs = np.where(b); low = xs[ys >= ys.max() - max(2, h // 14)]
        c2.save(os.path.join(OUT, pre + name + '.png')); meta[pre + name] = {'f': pre + name + '.png', 'w': round(w / PXU, 2), 'h': round(h / PXU, 2), 'ax': round((low.min() + low.max() + 1) / 2 / PXU, 2), 'ay': round(h / PXU, 2)}
    print(f, 'median px', med, '->', target, 'units;', ' '.join('%s %dx%d' % (n, round(c.size[0] * k / PXU), round(c.size[1] * k / PXU)) for n, c in cells))
ar = os.path.join(SRC, 'arena_a.png')
if os.path.exists(ar): Image.open(ar).convert('RGB').resize((784, 1176), Image.LANCZOS).save(os.path.join(OUT, 'arena.jpg'), quality=90); print('arena.jpg')
json.dump(meta, open(os.path.join(OUT, 'sprites.json'), 'w'), separators=(',', ':')); print(len(meta), 'sprites')
