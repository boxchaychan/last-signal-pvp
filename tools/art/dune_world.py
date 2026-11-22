"""Cut Codex's dune world pictures (art/incoming/dune, flat magenta) into game files: art/dune/env/*.webp + art/dune/world.json.

  python tools/art/dune_world.py <folder with the pictures> art/dune/env
Sheets are split into objects by connected parts, named in reading order (rows top to bottom, left to right).
"""
import sys, os, json
import numpy as np
from PIL import Image
from scipy import ndimage as nd

SRC, OUT = sys.argv[1], sys.argv[2]; os.makedirs(OUT, exist_ok=True); META = {}
KEY = np.array([255., 0., 255.])


def key(path):
    a = np.array(Image.open(path).convert('RGB')).astype(float)
    m = np.minimum(a[..., 0], a[..., 2]) - a[..., 1]                   # how magenta a pixel is
    al = 1 - np.clip((m - 62) / 118, 0, 1)
    solid = nd.binary_opening(al > .5, iterations=1)
    lb, n = nd.label(solid, structure=np.ones((3, 3)))
    if n:
        sz = nd.sum(solid, lb, range(1, n + 1)); solid = np.isin(lb, np.where(sz > 90)[0] + 1)
    al = al * nd.binary_dilation(solid, iterations=2)
    q = np.clip(al, .08, 1)[..., None]
    rgb = np.clip((a - (1 - q) * KEY) / q, 0, 255)                     # take the magenta out of soft edges
    edge = (al > 0) & (al < .98)
    rgb[edge, 2] = np.minimum(rgb[edge, 2], np.maximum(rgb[edge, 0], rgb[edge, 1]) * 1.04)
    return np.dstack([rgb, al * 255]).astype(np.uint8)


def save(name, arr, k=1, q=90):
    im = Image.fromarray(arr, 'RGBA' if arr.shape[2] == 4 else 'RGB')
    if k != 1: im = im.resize((max(1, round(im.width * k)), max(1, round(im.height * k))), Image.LANCZOS)
    im.save(f'{OUT}/{name}.webp', 'WEBP', quality=q, alpha_quality=95, method=6); META[name] = {'w': im.width, 'h': im.height}


def trim(a, pad=2):
    ys, xs = np.where(a[..., 3] > 10)
    return a[max(0, ys.min() - pad):ys.max() + pad + 1, max(0, xs.min() - pad):xs.max() + pad + 1]


def parts(a, gap=13, min_area=2500):
    solid = a[..., 3] > 90; joined = nd.binary_dilation(solid, iterations=gap); lb, n = nd.label(joined, structure=np.ones((3, 3))); out = []
    for i, sl in enumerate(nd.find_objects(lb)):
        mask = lb[sl] == i + 1; p = a[sl].copy(); p[..., 3] = p[..., 3] * mask
        if (p[..., 3] > 90).sum() >= min_area: out.append((sl[0].start, sl[0].stop, sl[1].start, trim(p)))
    out.sort(key=lambda o: (o[0] + o[1]) / 2); rows = []
    for o in out:
        c = (o[0] + o[1]) / 2
        if rows and c < rows[-1]['bot']: rows[-1]['o'].append(o); rows[-1]['bot'] = max(rows[-1]['bot'], o[1])
        else: rows.append({'bot': o[1], 'o': [o]})
    return [o[3] for r in rows for o in sorted(r['o'], key=lambda q: q[2])]


def has(n): return os.path.exists(f'{SRC}/{n}.png')


if has('bg_sky'): save('sky', np.array(Image.open(f'{SRC}/bg_sky.png').convert('RGB')), q=86)
for n, o in (('bg_far', 'far'), ('bg_mid', 'mid')):
    if has(n):
        a = key(f'{SRC}/{n}.png'); top = np.where((a[..., 3] > 10).any(1))[0][0]; save(o, a[max(0, top - 2):], q=88); META[o]['crop'] = int(max(0, top - 2))
if has('ground'):
    a = key(f'{SRC}/ground.png'); top = np.where((a[..., 3] > 10).any(1))[0][0]; save('ground', a[max(0, top - 2):], q=88)
    surf = np.array([(np.where(a[:, x, 3] > 128)[0][0] if (a[:, x, 3] > 128).any() else a.shape[0]) for x in range(a.shape[1])]) - max(0, top - 2)
    META['ground']['top'] = int(np.median(surf))
for sheet, names in {'props_plants': ['palm1', 'palm2', 'palm3', 'shrub', 'cactus', 'tuft'], 'props_ruins': ['column', 'columnb', 'arch', 'obelisk', 'statue', 'blocks'],
                     'props_camp': ['tent', 'stall', 'lantern', 'jars', 'crates', 'chest', 'sign'], 'props_water': ['pond', 'fall', 'well']}.items():
    if not has(sheet): continue
    ps = parts(key(f'{SRC}/{sheet}.png')); print(sheet, len(ps), 'parts for', len(names))
    for n, p in zip(names, ps): save(n, p)
if has('platforms'):
    a = key(f'{SRC}/platforms.png'); ps = parts(a, gap=6); print('platforms', len(ps))
    for n, p in zip(['plat_l', 'plat_m', 'plat_r', 'plat_s'], ps): save(n, p)
if has('climb'):
    a = key(f'{SRC}/climb.png'); ps = parts(a, gap=8, min_area=800); ps = sorted(ps, key=lambda p: -p.shape[1]); print('climb', len(ps))
    save('ladder', ps[0]); save('rope', ps[1])
for n, o, k in (('portal', 'portal', .8), ('npc_merchant', 'merchant', .46), ('npc_elder', 'elder', .46)):
    if has(n): save(o, trim(key(f'{SRC}/{n}.png')), k=k)
if has('title_art'): save('title', np.array(Image.open(f'{SRC}/title_art.png').convert('RGB')), q=86)
if has('icons'):
    a = key(f'{SRC}/icons.png'); save('icons', a, k=.5)
json.dump(META, open(f'{OUT}/../world.json', 'w'), separators=(',', ':'))
print(len(META), 'files')
