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
# --scale=p/q shrinks every sheet to p/q (owner 2026-11-08 "ย่อตัวลงหน่อย ... ตัวมันสูงไป", without blur): each output
# pixel takes the most common colour of the source area it covers (a dark outline wins when it fills 30% of it),
# so the result is crisp pixel art, not a blurred scale
SCALE = None
for _a in sys.argv[3:]:
    if _a.startswith('--scale='): SCALE = tuple(int(v) for v in _a[8:].split('/'))

def shrink(im, soft=False):
    if not SCALE: return im
    import numpy as np
    p, q = SCALE; W, H = im.size
    if soft: return im.resize((W * p // q, H * p // q), Image.LANCZOS)
    a = np.array(im.convert('RGBA'))
    up = a.repeat(p, 0).repeat(p, 1)                      # p x p nearest, then q x q blocks = exact p/q
    Hh, Ww = up.shape[0] // q, up.shape[1] // q; up = up[:Hh * q, :Ww * q]
    flat = up.reshape(-1, 4); key = (flat[:, 0].astype(np.int64) << 24) | (flat[:, 1].astype(np.int64) << 16) | (flat[:, 2].astype(np.int64) << 8) | flat[:, 3]
    key[flat[:, 3] == 0] = -1
    uniq, inv = np.unique(key, return_inverse=True); inv = inv.reshape(Hh * q, Ww * q)
    best = np.full((Hh, Ww), -1); bestn = np.zeros((Hh, Ww)); darkn = np.zeros((Hh, Ww)); darki = np.full((Hh, Ww), -1); transn = np.zeros((Hh, Ww))
    for ci, k in enumerate(uniq):
        n = (inv == ci).reshape(Hh, q, Ww, q).sum((1, 3))
        if k < 0: transn = n; continue
        r, g, b = (k >> 24) & 255, (k >> 16) & 255, (k >> 8) & 255
        if .3 * r + .59 * g + .11 * b < 60: m = n > darkn; darkn = np.maximum(darkn, n); darki[m] = ci
        m = n > bestn; bestn[m] = n[m]; best[m] = ci
    pick = np.where(darkn >= .3 * q * q, darki, best)
    out = np.zeros((Hh, Ww, 4), np.uint8)
    for ci, k in enumerate(uniq):
        if k < 0: continue
        m = pick == ci; out[m] = [(k >> 24) & 255, (k >> 16) & 255, (k >> 8) & 255, k & 255]
    out[transn > .5 * q * q] = 0
    return Image.fromarray(out)
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

# one WHITE blade-arc ramp for every direction (owner 2026-11-08: the arcs looked brown; then "ไม่ต้องทำมาซ้อน" =
# fix the arc inside the attack frames, no extra wave drawn on top)
SMEAR = [(196, 210, 226), (228, 236, 244), (255, 255, 255)]
# owner 2026-11-08 "ทำสีเหมือนอากาศหน่อย": the arcs are now pale air blue-white; outside the body they are see-through
SMEAR = [(168, 212, 238), (206, 236, 250), (246, 253, 255)]
AIRA = [120, 170, 215]   # alpha of the three steps where the arc sticks out beyond the body (over the body it stays solid)
# --arc=gold|air|white picks the arc colour; owner 2026-11-08 sent a clip with strong, glowing golden arcs ("สีแรงแสง"),
# so the attack also gets a glow sheet (<prefix>_attack_glow.png: the arc pixels blurred) that the game adds on top
ARCS = {'air': ([(168, 212, 238), (206, 236, 250), (246, 253, 255)], [120, 170, 215], (120, 200, 255)),
        'gold': ([(255, 150, 30), (255, 214, 70), (255, 248, 196)], [235, 245, 255], (255, 170, 40)),
        'white': ([(196, 210, 226), (228, 236, 244), (255, 255, 255)], [255, 255, 255], (255, 240, 210))}
GLOWC = ARCS['air'][2]
for _a in sys.argv[3:]:
    if _a.startswith('--arc='): SMEAR, AIRA, GLOWC = ARCS[_a[6:]]

def arcwhite(fr, grow=3):
    # PixelLab often paints the arc with the skin's own colours, so colour alone cannot find it: on a swing frame
    # (much wider than the median) every pixel outside the nearby narrow frames' silhouettes (grown by `grow` px) is arc
    import numpy as np
    from scipy import ndimage
    A = [np.array(im) for im in fr]
    w = [(lambda xs: xs[-1] - xs[0] if len(xs) else 0)(np.where((a[..., 3] > 0).any(0))[0]) for a in A]
    med = sorted(w)[len(w) // 2]; out = []
    for i, a in enumerate(A):
        a = a.copy()
        if w[i] > 1.15 * med:
            near = [j for j in range(max(0, i - 3), min(len(A), i + 4)) if j != i and w[j] <= 1.1 * med]
            ref = np.zeros(a.shape[:2], bool)
            for j in near: ref |= A[j][..., 3] > 0
            rgb = a[..., :3].astype(int); L = .3 * rgb[..., 0] + .59 * rgb[..., 1] + .11 * rgb[..., 2]
            body = ndimage.binary_dilation(ref, iterations=grow)
            arc = (a[..., 3] > 0) & ~body & (L > 100)   # dark limb outlines stay
            lab, n = ndimage.label(arc, structure=np.ones((3, 3)))
            if n:   # thin slivers left by a head or leg that moved a few pixels are not arcs: keep blobs of 30+ px only
                sz = ndimage.sum(arc, lab, range(1, n + 1)); arc &= np.isin(lab, 1 + np.where(sz >= 30)[0])
            out_arc = arc.copy()
            if arc.sum() >= 120 and near:
                # where the arc crosses the body it is painted in light skin tones over the dark clothes: grow the arc
                # into light pixels that were dark / empty in the nearest narrow frame (owner: one tone for every arc)
                pj = min(near, key=lambda j: abs(j - i)); pr = A[pj][..., :3].astype(int)
                Lp = .3 * pr[..., 0] + .59 * pr[..., 1] + .11 * pr[..., 2]
                cand = (a[..., 3] > 0) & (L > 120) & ((A[pj][..., 3] == 0) | (Lp < L - 55))
                ys = np.where((a[..., 3] > 0).any(1))[0]
                cand[:ys[0] + int((ys[-1] - ys[0]) * .3)] = False   # never into the head (her face moved between frames)
                for _ in range(60):
                    nb = ndimage.binary_dilation(arc) & cand & ~arc
                    if not nb.any(): break
                    arc |= nb
            for lo, c, al in zip([-1, 120, 190], SMEAR, AIRA):
                a[arc & (L > lo), :3] = c; a[out_arc & (L > lo), 3] = al   # see-through only beyond the body
            if out_arc.sum() >= 60:
                # owner "ทำคลื่นฟันให้กว้างกว่านี้": a wider wave = two faint see-through bands round the arc, on empty pixels only
                b1 = ndimage.binary_dilation(out_arc, iterations=3) & (a[..., 3] == 0)
                b2 = ndimage.binary_dilation(out_arc, iterations=6) & (a[..., 3] == 0) & ~b1
                a[b1, :3] = SMEAR[1]; a[b1, 3] = max(60, AIRA[0] - 30)
                a[b2 & (BAY[:a.shape[0], :a.shape[1]] < .55), :3] = SMEAR[0]; a[b2 & (BAY[:a.shape[0], :a.shape[1]] < .55), 3] = max(40, AIRA[0] - 70)
        out.append(Image.fromarray(a))
    return out
import numpy as _np0
BAY = _np0.tile(_np0.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16, (300, 300))   # ordered dither
PAL = None

def smear(im):
    # PixelLab paints each direction's blade arc in its own colours (white, beige, cyan...). Arc pixels = colours the
    # character's still pictures do not have (more than 30 away from every still colour) that are light or bluish;
    # they are repainted on SMEAR by brightness, so every direction's arc looks the same. Body colours are untouched.
    import numpy as np
    a = np.array(im).astype(int); rgb = a[..., :3]; m = a[..., 3] > 0
    if not len(SMEAR): return im
    d = np.full(m.shape, 1e9)
    for c in PAL: d = np.minimum(d, ((rgb - c) ** 2).sum(2))
    L = .3 * rgb[..., 0] + .59 * rgb[..., 1] + .11 * rgb[..., 2]
    arc = m & (d > 30 * 30) & ((L > 150) | (rgb[..., 2] > rgb[..., 0] + 35))
    for lo, c in zip([-1, 120, 190], SMEAR): a[arc & (L > lo), :3] = c
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
    if name in ('attack', 'chop') and out: return arcwhite([smear(im) for im in out])   # attacks keep their detached blade smears
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
if SCALE: C = -(-C // SCALE[1]) * SCALE[1]          # cells a multiple of q so every cell shrinks to whole pixels
K = SCALE[0] / SCALE[1] if SCALE else 1
pad = (C - rot[0].width) // 2
pre = os.path.basename(out)
os.makedirs(os.path.dirname(out) or '.', exist_ok=True)
still = Image.new('RGBA', (8 * C, C))
for i, im in enumerate(rot): still.alpha_composite(im, (i * C + pad, pad))
shrink(still).save(out + '_still.png', optimize=True)
meta = {'cell': round(C * K), 'fx': round(C // 2 * K), 'fy': round((pad + 125) * K), 'k': K, 'dirs': DIRS, 'still': pre + '_still.png', 'anims': {},
        'arc': {'ramp': SMEAR, 'alpha': AIRA, 'glow': GLOWC}}
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
    sheet = shrink(sheet); sheet.save(f'{out}_{name}.png', optimize=True); meta['anims'][name] = M
    if name == 'attack':
        # glow layer: every arc pixel (exactly a SMEAR colour) blurred into a soft halo of GLOWC, added by the game
        import numpy as np
        from scipy import ndimage
        s = np.array(sheet); m = np.zeros(s.shape[:2], bool)
        for c in SMEAR: m |= (s[..., 3] > 0) & (s[..., 0] == c[0]) & (s[..., 1] == c[1]) & (s[..., 2] == c[2])
        g = ndimage.gaussian_filter(m.astype(float), 3.5) * 2.2 + ndimage.gaussian_filter(m.astype(float), 10) * 1.8
        gl = np.zeros(s.shape, np.uint8); gl[..., :3] = GLOWC; gl[..., 3] = (np.clip(g, 0, 1) * 255).astype(np.uint8)
        Image.fromarray(gl).save(f'{out}_{name}_glow.png', optimize=True); M['glow'] = f'{pre}_{name}_glow.png'
    print(name.ljust(7), sheet.size, 'dirs', len(have), 'frames', cols, {d: M[d].get('hits') for d in DIRS if d in M and 'hits' in M[d]})
json.dump(meta, open(out + '.json', 'w'), indent=1)
print('cell', meta['cell'], 'feet', meta['fx'], meta['fy'], 'scale', K)
