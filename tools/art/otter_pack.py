"""Cut the otter's Codex move sheets (4 x 4 on flat blue) into game frames for dune.html.

  python tools/art/otter_pack.py

Reads art/incoming/otter_fist/<move>.png, removes the blue and the ground line, makes every move the same body size by finding the
head of the guard pose, stands the feet on one line, writes art/dune/otter/<move>.webp and adds otter_<move> to art/dune/sprites.json.
Prints, for each move, the frame where the fist reaches furthest (use it as the hit frame). The water orb comes from side_ref.png.
"""
import json, os
import numpy as np, cv2
from PIL import Image

IN, OUT = 'art/incoming/otter_fist/', 'art/dune/otter/'; os.makedirs(OUT, exist_ok=True)
MOVES = ['idle', 'run', 'attack1', 'attack2', 'attack3', 'skill_dash', 'skill_flurry', 'skill_upper', 'skill_drop', 'skill_spin', 'hurt', 'death']
BLUE = np.array([2, 72, 186]); K = .815   # standing body = 59 world units next to the dragon
def cut(c):
    bg = (np.abs(c.astype(int) - BLUE).max(2) < 46).astype(np.uint8); n, l = cv2.connectedComponents(bg, connectivity=4); e = set(np.unique(np.r_[l[0], l[-1], l[:, 0], l[:, -1]])) - {0}
    al = (~np.isin(l, list(e)) * 255).astype(np.uint8); h = c.shape[0]; rows = (c.max(2) < 70)[int(h * .6):].sum(1); ly = int(h * .6) + int(np.argmax(rows)); al[ly - 1:] = 0
    # keep the figure, drop specks left by the line
    n, l, st, _ = cv2.connectedComponentsWithStats((al > 40).astype(np.uint8), 8)
    if n > 1: al[~np.isin(l, [i for i in range(1, n) if st[i, 4] > 24])] = 0
    al = cv2.GaussianBlur(cv2.erode(al, np.ones((2, 2), np.uint8)), (0, 0), .55); return np.dstack([c, al]), ly
def sheet(name):
    a = np.array(Image.open(f'{IN}{name}.png').convert('RGB')); H, W = a.shape[:2]; cw, ch = W // 4, H // 4; out = []
    for i in range(16):
        f, ly = cut(a[(i // 4) * ch:(i // 4 + 1) * ch, (i % 4) * cw:(i % 4 + 1) * cw]); out.append((f, ly))
    return out, cw, ch
base, cw, ch = sheet('attack2'); g0 = base[0][0]; ys, xs = np.where(g0[..., 3] > 60); top = ys.min(); head = cv2.cvtColor(g0[top + 6:top + 74, xs.min() + 56:xs.min() + 150, :3], cv2.COLOR_RGB2GRAY)
def body_scale(f):
    g = cv2.cvtColor(f[..., :3], cv2.COLOR_RGB2GRAY); best = (-1, 1)
    for s in np.arange(.86, 1.16, .01):
        t = cv2.resize(head, None, fx=s, fy=s, interpolation=cv2.INTER_AREA if s < 1 else cv2.INTER_CUBIC)
        if t.shape[0] >= g.shape[0] or t.shape[1] >= g.shape[1]: continue
        v = cv2.minMaxLoc(cv2.matchTemplate(g, t, cv2.TM_CCOEFF_NORMED))[1]
        if v > best[0]: best = (v, float(s))
    return best
def feet_mid(f, ly):
    low = f[max(0, ly - 16):ly - 2, :, 3] > 60; x = np.where(low.any(0))[0]; return (x.min() + x.max()) / 2 if len(x) else f.shape[1] / 2
sp = json.load(open('art/dune/sprites.json'))
for name in MOVES:
    if not os.path.exists(f'{IN}{name}.png'): print(name, 'not drawn yet'); sp.pop('otter_' + name, None); continue
    fr, cw, ch = sheet(name); conf, s = body_scale(fr[0][0]); s = 1 if conf < .55 else s; k = K / s; mid = feet_mid(*fr[0]); box = None
    for f, _ in fr:
        bb = Image.fromarray(f[..., 3]).point(lambda v: 255 if v > 12 else 0).getbbox()
        if bb: box = bb if box is None else (min(box[0], bb[0]), min(box[1], bb[1]), max(box[2], bb[2]), max(box[3], bb[3]))
    ly = max(q[1] for q in fr); x0, y0, x1 = max(0, box[0] - 2), max(0, box[1] - 2), min(cw, box[2] + 2); w, h = round((x1 - x0) * k), round((ly - y0) * k); cols = min(16, 2048 // max(1, w)); rows = (16 + cols - 1) // cols
    S = Image.new('RGBA', (cols * w, rows * h), (0, 0, 0, 0)); dy = []
    for i, (f, l) in enumerate(fr):
        S.paste(Image.fromarray(f, 'RGBA').crop((x0, y0 + l - ly, x1, l)).resize((w, h), Image.LANCZOS), (i % cols * w, i // cols * h))
    p = f'{OUT}{name}.webp'; S.save(p, 'WEBP', quality=88, alpha_quality=92, method=6)
    sp['otter_' + name] = {'src': p, 'n': 16, 'w': w, 'h': h, 'foot': h, 'cols': cols, 'cx': round((mid - x0) * k)}
    reach = [int(np.where((f[:int(l * .72), :, 3] > 60).any(0))[0].max()) for f, l in fr]
    print(f'{name}: head match {conf:.2f} scale {s:.2f} cell {w}x{h} {os.path.getsize(p) // 1024} KB, furthest fist on frame index {int(np.argmax(reach))}')
r = np.array(Image.open(IN + 'side_ref.png').convert('RGB'))[505:690, 770:1000]; bg = (r.min(2) >= 238).astype(np.uint8); n, l = cv2.connectedComponents(bg, connectivity=4); e = set(np.unique(np.r_[l[0], l[-1], l[:, 0], l[:, -1]])) - {0}
al = cv2.GaussianBlur((~np.isin(l, list(e)) * 255).astype(np.uint8), (0, 0), .8); ys, xs = np.where(al > 40); yb = ys.max() - 42  # the fingers under the orb are left out
o = Image.fromarray(np.dstack([r, al]), 'RGBA').crop((xs.min(), ys.min(), xs.max() + 1, yb)).resize((64, 64), Image.LANCZOS); o.save(OUT + 'orb.webp', 'WEBP', quality=90, alpha_quality=95, method=6)
sp['otter_orb'] = {'src': OUT + 'orb.webp', 'n': 1, 'w': 64, 'h': 64, 'cols': 1}
json.dump(sp, open('art/dune/sprites.json', 'w'), separators=(',', ':'))
