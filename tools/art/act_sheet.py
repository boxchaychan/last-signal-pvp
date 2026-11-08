# PixelLab character download (unzipped) -> sprite sheets + json for action.html (owner 2026-11-08, dagger rogue).
#   python3 tools/art/act_sheet.py <unzipped dir>/<state> <out prefix> <anim>=<folder> [<anim>=<folder> ...] [options]
#   e.g. python3 tools/art/act_sheet.py art/incoming/action/rogue/pl2_dl/Idle art/action/rogue run=run idle=idle \
#        attack=@art/incoming/action/rogue/pl_dl/Idle::attack_2hit_b,attack_back
# Writes <prefix>.json, <prefix>_still.png (the 8 rotations in one row) and <prefix>_<anim>.png per animation (one
# row per direction it has, so no sheet gets too big for phones). PixelLab centres a 128 still inside its bigger
# animation canvas (+22 px at 172), so every cell is the biggest canvas and smaller frames are centred in it.
# <folder> can be a,b (a redo in b replaces a for the directions b has) and @<other download state dir>::a,b.
# Options: --hits=<dir>:<f>,<f>[;...] hit frames by hand (attack only) · --skip=<dir>,... leave directions empty
# (the game mirrors the other side) · --alias=<dir>:<from>[~],... play another direction's row (~ = mirrored).
import sys, os, glob, json
from PIL import Image

src, out = sys.argv[1], sys.argv[2]
opts = [a for a in sys.argv[3:] if a.startswith('--')]
FIX, SKIP, ALIAS = {}, set(), {}
for a in opts:
    if a.startswith('--hits='):
        for part in a[7:].split(';'):
            d, fs = part.split(':'); FIX[d if '/' in d else 'attack/' + d] = [int(f) for f in fs.split(',')]
    # --skip / --alias entries are "<anim>/<dir>"; a bare "<dir>" means the attack
    elif a.startswith('--skip='): SKIP |= {p if '/' in p else 'attack/' + p for p in a[7:].split(',')}
    elif a.startswith('--alias='):
        for part in a[8:].split(','):
            d, f = part.split(':'); d = d if '/' in d else 'attack/' + d
            ALIAS[d] = (f.rstrip('~'), f.endswith('~')); SKIP.add(d)
anims = [a.split('=', 1) for a in sys.argv[3:] if not a.startswith('--')]
DIRS = ['east', 'south-east', 'south', 'south-west', 'west', 'north-west', 'north', 'north-east']

def dedust(im):
    # PixelLab leaves dust puffs / specks floating beside a run or a roll even when told not to: drop every
    # see-through-separated blob except the biggest that is small (< 120 px) or mostly pale (light dust)
    import numpy as np
    from scipy import ndimage
    a = np.array(im); m = a[..., 3] > 0
    lab, n = ndimage.label(m, structure=np.ones((3, 3)))
    if n < 2: return im
    sz = ndimage.sum(m, lab, range(1, n + 1)); big = 1 + int(np.argmax(sz))
    for k in range(1, n + 1):
        if k == big: continue
        blob = lab == k; px = a[blob][:, :3].astype(int)
        pale = (px.min(1) > 165).mean() > .6
        if sz[k - 1] < 120 or (pale and sz[k - 1] < 900): a[blob] = 0
    return Image.fromarray(a)

SMEAR = [(214, 198, 164), (238, 226, 200), (255, 251, 239)]   # one blade-arc ramp for every direction (owner 2026-11-08)
PAL = None

def smear(im):
    # PixelLab paints each direction's blade arc in its own colours (white, beige, cyan...). Arc pixels = colours the
    # character's still pictures do not have (more than 30 away from every still colour) that are light or bluish;
    # they are repainted on SMEAR by brightness, so every direction's arc looks the same. Body colours are untouched.
    import numpy as np
    a = np.array(im).astype(int); rgb = a[..., :3]; m = a[..., 3] > 0
    d = np.full(m.shape, 1e9)
    for c in PAL: d = np.minimum(d, ((rgb - c) ** 2).sum(2))
    L = .3 * rgb[..., 0] + .59 * rgb[..., 1] + .11 * rgb[..., 2]
    arc = m & (d > 30 * 30) & ((L > 150) | (rgb[..., 2] > rgb[..., 0] + 35))
    for lo, c in zip([-1, 150, 205], SMEAR): a[arc & (L > lo), :3] = c
    return Image.fromarray(a.astype('uint8'))

def frames(folder, d, name):
    # folder: a,b | @<state dir>::a,b | several of those joined by "|" (later ones win per direction)
    fs = []
    for seg in folder.split('|'):
        base, fl = src, seg
        if seg.startswith('@'): base, fl = seg[1:].split('::')
        for f in fl.split(','):
            fs = sorted(glob.glob(os.path.join(base, 'animations', f, d, 'frame_*.png'))) or fs
    out = [Image.open(f).convert('RGBA') for f in fs]
    if name in ('attack', 'chop'): return [smear(im) for im in out]   # attacks keep their detached blade smears
    return [dedust(im) for im in out]

def hits(fr):
    # swing frames: PixelLab draws a blade smear there, so the figure is widest; a hit = a local maximum of the
    # width that is at least 1.25x the median width (checked on the rogue's directions 2026-11-08)
    w = [(lambda b: b[2] - b[0] if b else 0)(im.getbbox()) for im in fr]
    med = sorted(w)[len(w) // 2]
    return [i for i in range(1, len(w) - 1) if w[i] >= 1.25 * med and w[i] >= w[i - 1] and w[i] >= w[i + 1] and (w[i] > w[i - 1] or w[i] > w[i + 1])]

rot = [Image.open(os.path.join(src, 'rotations', d + '.png')).convert('RGBA') for d in DIRS]
import numpy as _np
PAL = _np.unique(_np.concatenate([_np.array(r)[_np.array(r)[..., 3] > 0][:, :3] for r in rot]), axis=0).astype(int)
data = {name: {d: ([] if f'{name}/{d}' in SKIP else frames(folder, d, name)) for d in DIRS} for name, folder in anims}
C = max([rot[0].width] + [fr[0].width for a in data.values() for fr in a.values() if fr])
pad = (C - rot[0].width) // 2
pre = os.path.basename(out)
os.makedirs(os.path.dirname(out) or '.', exist_ok=True)
still = Image.new('RGBA', (8 * C, C))
for i, im in enumerate(rot): still.alpha_composite(im, (i * C + pad, pad))
still.save(out + '_still.png', optimize=True)
meta = {'cell': C, 'fx': C // 2, 'fy': pad + 125, 'dirs': DIRS, 'still': pre + '_still.png', 'anims': {}}
for name, A in data.items():
    have = [d for d in DIRS if A[d]]
    if not have: continue
    cols = max(len(A[d]) for d in have)
    sheet = Image.new('RGBA', (cols * C, len(have) * C)); M = {'img': f'{pre}_{name}.png'}
    for r, d in enumerate(have):
        fr = A[d]; o = (C - fr[0].width) // 2
        for i, im in enumerate(fr): sheet.alpha_composite(im, (i * C + o, r * C + o))
        M[d] = {'r': r, 'n': len(fr)}
        if name not in ('run', 'idle'): M[d]['hits'] = FIX.get(f'{name}/{d}') or hits(fr)
    for key, (f, mir) in ALIAS.items():
        an, d = key.split('/')
        if an == name and f in M: M[d] = dict(M[f], flip=mir, alias=f)
    sheet.save(f'{out}_{name}.png', optimize=True); meta['anims'][name] = M
    print(name.ljust(7), sheet.size, 'dirs', len(have), 'frames', cols, {d: M[d].get('hits') for d in DIRS if d in M and 'hits' in M[d]})
json.dump(meta, open(out + '.json', 'w'), indent=1)
print('cell', C, 'feet', meta['fx'], meta['fy'])
