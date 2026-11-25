"""Cut the moon blade's Codex move sheets (4 x 4 on flat blue #0248BA, branch codex/moon-blade) into game frames for dune.html.

  git checkout origin/codex/moon-blade -- art/incoming/moon_blade && git reset -q
  python tools/art/moon_pack.py

Reads art/incoming/moon_blade/<move>.png, removes the blue and the ground line, scales every move by ONE factor so the standing body is
BODY px tall (Codex kept his size steady; the idle opening frame sets it), puts the feet on the ground line of each cell, keeps the
feet of every frame on one line (dy), sharpens a little (owner: "คมกริบ"), writes art/dune/moon/<move>.webp and moon_<move> in
art/dune/sprites.json. dune.html?hero=moon maps moon_<move> onto hero_<move>.
"""
import json, os
import numpy as np, cv2
from PIL import Image, ImageFilter

IN, OUT = 'art/incoming/moon_blade/', 'art/dune/moon/'; os.makedirs(OUT, exist_ok=True)
MOVES = ['idle', 'run', 'walk', 'jump', 'climb', 'attack1', 'attack2', 'attack3', 'skill_dash', 'skill_leap', 'skill_cast', 'skill_spin', 'hurt', 'death']
BLUE = np.array([2, 72, 186]); BODY = 180   # standing body in sprite px: x HERO_SC (1/3) = 60 world units (owner: small like the Maple-like genre)
def cut(c):
    h = c.shape[0]; rows = (c.max(2) < 70)[int(h * .6):].sum(1); ly = int(h * .6) + int(np.argmax(rows)); d = np.abs(c.astype(int) - BLUE).max(2)
    bg = (d < 46).astype(np.uint8); bg[ly - 2:] = 1
    n, l = cv2.connectedComponents(bg, connectivity=4); e = set(np.unique(np.r_[l[0], l[-1], l[:, 0], l[:, -1]])) - {0}; al = (~np.isin(l, list(e)) * 255).astype(np.uint8); al[ly - 1:] = 0
    n, l, st, _ = cv2.connectedComponentsWithStats((d < 24).astype(np.uint8), 4)   # blue pockets closed in by an arm, the cape or the sword
    for i in range(1, n):
        if st[i, 4] >= 10: al[cv2.dilate((l == i).astype(np.uint8), np.ones((3, 3), np.uint8)) > 0] = 0
    n, l, st, _ = cv2.connectedComponentsWithStats((al > 40).astype(np.uint8), 8)
    if n > 1: al[~np.isin(l, [i for i in range(1, n) if st[i, 4] > 24])] = 0
    al = cv2.GaussianBlur(cv2.erode(al, np.ones((2, 2), np.uint8)), (0, 0), .5); return np.dstack([c, al]), ly
def sheet(name):
    a = np.array(Image.open(f'{IN}{name}.png').convert('RGB')); H, W = a.shape[:2]; cw, ch = W // 4, H // 4
    return [cut(a[(i // 4) * ch:(i // 4 + 1) * ch, (i % 4) * cw:(i % 4 + 1) * cw]) for i in range(16)], cw, ch
def sole(f):   # lowest solid part of the body (a thin sword tip below the feet is ignored)
    o = cv2.morphologyEx((f[..., 3] > 90).astype(np.uint8), cv2.MORPH_OPEN, np.ones((9, 9), np.uint8)); y = np.where(o.any(1))[0]; return int(y.max()) if len(y) else f.shape[0] - 1
def feet_mid(f, s):
    low = f[max(0, s - 14):s + 1, :, 3] > 90; x = np.where(cv2.morphologyEx(low.astype(np.uint8), cv2.MORPH_OPEN, np.ones((3, 9), np.uint8)).any(0))[0]; return (x.min() + x.max()) / 2 if len(x) else f.shape[1] / 2
idle, _, _ = sheet('idle'); f0 = idle[0][0]; ys = np.where((f0[..., 3] > 90).any(1))[0]; K = BODY / (sole(f0) - ys.min() + 1); print(f'idle body {sole(f0) - ys.min() + 1} px -> scale {K:.3f}')
sp = json.load(open('art/dune/sprites.json'))
for name in MOVES:
    if not os.path.exists(f'{IN}{name}.png'): print(name, 'not drawn yet'); continue
    fr, cw, ch = sheet(name); soles = [sole(f) for f, _ in fr]; base = soles[0]; mid = feet_mid(fr[0][0], base)
    box = None
    for f, _ in fr:
        bb = Image.fromarray(f[..., 3]).point(lambda v: 255 if v > 12 else 0).getbbox()
        if bb: box = bb if box is None else (min(box[0], bb[0]), min(box[1], bb[1]), max(box[2], bb[2]), max(box[3], bb[3]))
    x0, y0, x1, y1 = max(0, box[0] - 2), max(0, box[1] - 2), min(cw, box[2] + 2), min(ch, box[3] + 2); w, h = round((x1 - x0) * K), round((y1 - y0) * K)
    cols = min(16, 2048 // max(1, w)); rows = (16 + cols - 1) // cols; S = Image.new('RGBA', (cols * w, rows * h), (0, 0, 0, 0))
    for i, (f, _) in enumerate(fr):
        im = Image.fromarray(f, 'RGBA').crop((x0, y0, x1, y1)).resize((w, h), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=.8, percent=45, threshold=2))
        S.paste(im, (i % cols * w, i // cols * h))
    p = f'{OUT}{name}.webp'; S.save(p, 'WEBP', quality=90, alpha_quality=92, method=6)
    air = name in ('jump', 'skill_leap', 'climb'); limit = 999 if air else 26
    sp['moon_' + name] = {'src': p, 'n': 16, 'w': w, 'h': h, 'cols': cols, 'foot': round((base - y0 + 1) * K), 'cx': round((mid - x0) * K),
                          'dy': [0 if air else (round((base - v) * K) if abs(base - v) <= limit else 0) for v in soles]}
    reach = [int(np.where((f[:int(sole(f) * .8), :, 3] > 60).any(0))[0].max()) for f, _ in fr]
    print(f'{name}: cell {w}x{h} {os.path.getsize(p) // 1024} KB, furthest reach on frame {int(np.argmax(reach))}')
json.dump(sp, open('art/dune/sprites.json', 'w'), separators=(',', ':'))
