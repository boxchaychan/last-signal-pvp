# Assassin v2 as a PixelLab character (owner 2026-11-12 "เอาเข้าเกมส์ยัง"): character 11dc25a4 (char_dl/ = its ZIP) -> one 168 px
# cell per frame (feet 84,144), rows per move and direction, + as3.json. PixMiniMax drew big swooshes, rings, an X flash and dust
# into the slash and spin clips: bright / white / dust-grey patches bigger than 45 px are removed (her face, hands and gems are
# small), then a 1 px black outline like class 1. The spin keeps one turn. The template run's bad halves are left out.
#   python3 tools/art/as3_build.py -> art/action/as3/{still,run,attack,spin}.png + as3.json
import os, glob, json, sys, numpy as np
from PIL import Image
from scipy import ndimage
sys.path.insert(0, 'tools/art'); from px_outline import outline
S = 'art/incoming/action/rogue/class2/v2/char_dl/Idle/'; O = 'art/action/as3/'; os.makedirs(O, exist_ok=True)
C, FX, FY = 168, 84, 144
def anim(key): return [x for x in glob.glob(S + 'animations/*') if key in x][0]
def frames(key, d): return sorted(glob.glob(anim(key) + '/' + d + '/*.png'), key=lambda f: int(os.path.basename(f).split('.')[0].split('_')[-1]))
PAL = None
def palette():   # her own colours: every colour of the 8 still views (the swooshes / rings / dust are not among them)
    global PAL
    if PAL is None:
        cs = np.concatenate([np.asarray(Image.open(S + 'rotations/%s.png' % d).convert('RGBA')).reshape(-1, 4) for d in
                             ['east', 'south-east', 'south', 'north', 'north-east', 'west', 'south-west', 'north-west']])
        PAL = np.unique(cs[cs[:, 3] > 0][:, :3], axis=0).astype(int)
    return PAL
def clean(im, fx):
    a = np.asarray(im.convert('RGBA')).copy()
    if fx:
        P = palette(); op = a[..., 3] > 0; px = a[op][:, :3].astype(int)
        d = np.full(len(px), 1e9)
        for i in range(0, len(P), 64): d = np.minimum(d, ((px[:, None, :] - P[None, i:i + 64, :]) ** 2).sum(2).min(1))
        far = np.zeros(op.shape, bool); far[op] = d > 38 ** 2                       # not one of her colours
        far = ndimage.binary_dilation(far, iterations=1) & op & ~ndimage.binary_erosion(op & ~far, iterations=2)   # + its rim
        a[far] = 0
        m = a[..., 3] > 0; lab, n = ndimage.label(m, structure=np.ones((3, 3)))   # keep the body (the biggest piece) and pieces near it
        if n > 1:
            sz = ndimage.sum(m, lab, range(1, n + 1)); keep = np.argmax(sz) + 1; near = ndimage.binary_dilation(lab == keep, iterations=3)
            for i in range(1, n + 1):
                if i != keep and not (near & (lab == i)).any(): a[lab == i] = 0
                elif i != keep and sz[i - 1] < 6: a[lab == i] = 0
        hsv = np.asarray(Image.fromarray(a[..., :3]).convert('HSV')).astype(int); yy = np.mgrid[0:a.shape[0], 0:a.shape[1]][0]
        dust = (a[..., 3] > 0) & (hsv[..., 1] < 45) & (hsv[..., 2] > 150) & (yy > a.shape[0] * .74)   # white / grey dust puffs at the feet
        lab, n = ndimage.label(dust, structure=np.ones((3, 3)))
        if n: sz = ndimage.sum(dust, lab, range(1, n + 1)); a[np.isin(lab, 1 + np.where(sz >= 8)[0])] = 0
    return Image.fromarray(outline(a, black=(14, 10, 18)))
def put(im):
    c = Image.new('RGBA', (C, C)); o = (C - im.width) // 2; c.alpha_composite(im, (o, o)); return c
rows = {}; meta = {'cw': C, 'ch': C, 'fx': FX, 'fy': FY, 'anims': {}}
def add(name, key, dirs, pick=None, fx=False, raw=False):
    imgs = []; meta['anims'][name] = {}
    for d, sel in dirs.items():
        src = d
        if isinstance(sel, tuple): src, sel = sel          # another direction's frames stand in
        fs = frames(key, src); fs = [fs[i] for i in sel] if sel else fs
        row = [put(Image.open(f).convert('RGBA') if raw else clean(Image.open(f), fx)) for f in fs]
        area = [int((np.asarray(r)[..., 3] > 0).sum()) for r in row]; med = sorted(area)[len(area) // 2]
        feet = [int((np.asarray(r)[FY - 14:FY + 2, :, 3] > 0).sum()) for r in row]; fm = sorted(feet)[len(feet) // 2]
        if not raw: row = [r for r, ar, ft in zip(row, area, feet) if ar > med * .55 and ft > fm * .45]   # frames that were mostly effect (the X flash) or lost their legs behind a swoosh are dropped
        meta['anims'][name][d] = {'r': len(imgs), 'n': len(row)}; imgs.append(row)
    n = max(len(r) for r in imgs); out = Image.new('RGBA', (C * n, C * len(imgs)))
    for j, r in enumerate(imgs):
        for i, im in enumerate(r): out.alpha_composite(im, (i * C, j * C))
    out.save(O + name + '.png')
# stills: the 8 rotations
st = Image.new('RGBA', (C * 8, C)); DIRS = ['east', 'south-east', 'south', 'south-west', 'west', 'north-west', 'north', 'north-east']
for i, d in enumerate(DIRS): st.alpha_composite(put(clean(Image.open(S + 'rotations/%s.png' % d), False)), (i * C, 0))
st.save(O + 'still.png')
# run: east has grey 'robot' arms -> the south-east run stands in for the side; north / north-east: the matching half only
add('run', 'running', {'east': ('south-east', None), 'south-east': None, 'south': None, 'north-east': [0, 1, 2, 3], 'north': [4, 5, 6, 7]})
SL = [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 16]            # 13-14 = the X flash
add('attack', 'a_fast', {'east': SL, 'south-east': SL, 'south': SL}, fx=True)
SP = [0, 3, 4, 5, 6, 7, 8, 9, 13, 15, 16]                        # one turn, then the landing
add('spin', 'a_critical', {'east': SP, 'south-east': SP, 'south': SP}, fx=True)
# owner 2026-11-12 "วงไว้ทำตอนสกิล ... ทำไมจะลบเอฟเฟกต์": the spin WITH PixMiniMax's own glowing rings, untouched, for the E whirl skill
add('spinfx', 'a_critical', {'east': list(range(3, 14)), 'south-east': list(range(3, 14)), 'south': list(range(3, 14))}, raw=True)
json.dump(meta, open(O + 'as3.json', 'w')); print(json.dumps(meta)[:400])
