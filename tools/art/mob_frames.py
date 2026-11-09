# Codex monster frames (art/incoming/mobs/anim/<key>_<walk|attack|death>.png: 6 frames in a 3x2 grid on white) -> one
# pixel-art sheet per monster for action.html: art/action/mobs/<key>.png + <key>.json (rows walk / attack / death,
# 6 columns, feet on one ground line). Owner 2026-11-09: monsters by Codex, not PixelLab.
#   python tools/art/mob_frames.py [key ...]        (no key = all 15)
# Each action picture is scaled on its own so its frame 1 is SIZE[key] px tall (Codex draws each picture at its own size);
# the feet of frame 1 set the anchor and every other frame keeps its place in its cell (so lunges and falls stay).
# One palette per monster (32 colours), 1 px dark outline, 1 art px = 1 world px like the heroes.
import sys, os, json, subprocess
import numpy as np
from PIL import Image
from scipy import ndimage

SIZE = {'shroom': 46, 'wolf': 60, 'goblin_archer': 58, 'boar_guard': 96, 'skeleton': 76, 'wisp': 56, 'golem': 100,
        'boss_treant': 168, 'krahang': 76, 'khamot': 46, 'phrai': 80, 'pret': 118, 'monkey': 56, 'croc_guard': 100,
        'boss_chalawan': 158}
FLIP = {'khamot'}          # drawn facing left by Codex
ACTS = ['walk', 'attack', 'death']
SRC, CUT, OUT = 'art/incoming/mobs/anim', 'art/incoming/mobs/anim_cut', 'art/action/mobs'
os.makedirs(CUT, exist_ok=True); os.makedirs(OUT, exist_ok=True)

def cells(path):
    a = np.array(Image.open(path).convert('RGBA')); H, W = a.shape[:2]; cw, ch = W // 3, H // 2; out = []
    for r in range(2):
        for c in range(3):
            q = a[r * ch:(r + 1) * ch, c * cw:(c + 1) * cw].copy(); m = q[..., 3] > 128
            lab, n = ndimage.label(m)
            if n:
                sz = ndimage.sum(m, lab, range(1, n + 1))
                for i, s in enumerate(sz):
                    if s < 60: q[lab == i + 1, 3] = 0           # specks
            out.append(q)
    return out

def bbox(q):
    ys, xs = np.nonzero(q[..., 3] > 128)
    return (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1) if len(xs) else None

def shrink(q, s):
    h, w = q.shape[:2]; p = q.astype(float) / 255; p[..., :3] *= p[..., 3:4]
    r = np.array(Image.fromarray((p * 255).astype(np.uint8)).resize((max(1, round(w * s)), max(1, round(h * s))), Image.BOX)).astype(float)
    al = r[..., 3:4] / 255; rgb = np.where(al > 0, r[..., :3] / np.maximum(al, 1e-6), 0).clip(0, 255)
    return rgb.astype(np.uint8), al[..., 0] > .5

def build(key):
    rows = []
    for a in ACTS:
        src = f'{SRC}/{key}_{a}.png'; cut = f'{CUT}/{key}_{a}.png'
        if not os.path.exists(cut) or os.path.getmtime(cut) < os.path.getmtime(src):
            subprocess.run([sys.executable, 'tools/art/white_cut.py', src, cut, '--no-ring'], check=True, capture_output=True)
        fr = cells(cut)
        if key in FLIP: fr = [q[:, ::-1].copy() for q in fr]
        b0 = bbox(fr[0]); s = SIZE[key] / (b0[3] - b0[1])
        y0 = b0[3]                                                        # ground = frame 1's lowest row
        m0 = fr[0][..., 3] > 128; foot = m0[max(b0[1], y0 - max(3, (b0[3] - b0[1]) // 6)):y0]
        x0 = np.nonzero(foot.any(0))[0].mean()                            # feet centre of frame 1
        row = []
        for q in fr:
            rgb, m = shrink(q, s); row.append((rgb, m, x0 * s, y0 * s))
        rows.append(row)
    # one palette for the monster
    allpx = np.concatenate([rgb[m] for row in rows for rgb, m, _, _ in row])[None]
    pal = Image.fromarray(allpx).quantize(32, method=Image.Quantize.MEDIANCUT)
    # extents relative to the anchor
    L = T = 0; R = B = 1
    for row in rows:
        for rgb, m, ax, ay in row:
            ys, xs = np.nonzero(m)
            if len(xs): L = min(L, xs.min() - ax); R = max(R, xs.max() + 1 - ax); T = min(T, ys.min() - ay); B = max(B, ys.max() + 1 - ay)
    fx, fy = int(np.ceil(-L)) + 2, int(np.ceil(-T)) + 2; CW, CH = fx + int(np.ceil(R)) + 2, fy + int(np.ceil(B)) + 2
    sheet = np.zeros((CH * 3, CW * 6, 4), np.uint8)
    for r, row in enumerate(rows):
        for c, (rgb, m, ax, ay) in enumerate(row):
            q = np.array(Image.fromarray(rgb).quantize(palette=pal, dither=Image.Dither.NONE).convert('RGB'))
            can = np.zeros((CH, CW, 4), np.uint8); h, w = m.shape
            ox, oy = int(round(fx - ax)), int(round(fy - ay))
            X0, Y0 = max(0, ox), max(0, oy); X1, Y1 = min(CW, ox + w), min(CH, oy + h)
            can[Y0:Y1, X0:X1, :3] = q[Y0 - oy:Y1 - oy, X0 - ox:X1 - ox]; can[Y0:Y1, X0:X1, 3] = m[Y0 - oy:Y1 - oy, X0 - ox:X1 - ox] * 255
            mm = can[..., 3] > 0; ring = ndimage.binary_dilation(mm) & ~mm; can[ring] = (30, 20, 24, 255)
            sheet[r * CH:(r + 1) * CH, c * CW:(c + 1) * CW] = can
    Image.fromarray(sheet).save(f'{OUT}/{key}.png', optimize=True)
    meta = {'w': CW, 'h': CH, 'fx': fx, 'fy': fy, 'n': 6, 'rows': {a: i for i, a in enumerate(ACTS)}, 'hit': 3, 'size': SIZE[key]}
    json.dump(meta, open(f'{OUT}/{key}.json', 'w'))
    print(key, 'cell', CW, 'x', CH, 'anchor', fx, fy)
    return meta

if __name__ == '__main__':
    keys = sys.argv[1:] or list(SIZE)
    idx = {}
    if os.path.exists(f'{OUT}/index.json'): idx = json.load(open(f'{OUT}/index.json'))
    for k in keys: idx[k] = build(k)
    json.dump(idx, open(f'{OUT}/index.json', 'w'), separators=(',', ':'))
