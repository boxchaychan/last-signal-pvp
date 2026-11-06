# Frames laid out loosely on one picture (e.g. a Codex "game-character-sprites" preview: an idle row and an attack row on a
# see-through or white background) -> one FANIM strip for bb.html. Owner 2026-11-06 (Tan ankylosaurus attack from Codex).
#   python3 tools/art/frames_import.py <picture> <out.png> <row> [frames] [colours]
#     row     = which row of figures to use (0 = top)
#     frames  = comma list of figure indexes in that row, left to right (default: all); the first one is the standing frame
#     colours = shared palette size (default 48)
# Feet: every frame is pinned by its BACK boot (the leftmost boot, the kid faces right), so a forward step looks like a step;
# the slot centre (fx) sits between the two boots of the standing frame. Prints the FANIM line (hit = first frame reaching
# furthest forward, check it by eye).
import sys
import numpy as np
from PIL import Image
from scipy import ndimage

src, out = sys.argv[1], sys.argv[2]
row = int(sys.argv[3]) if len(sys.argv) > 3 else 0
pick = [int(v) for v in sys.argv[4].split(',')] if len(sys.argv) > 4 and sys.argv[4] else None
NC = int(sys.argv[5]) if len(sys.argv) > 5 else 48

im = Image.open(src).convert('RGBA'); a = np.array(im)
if (a[..., 3] < 250).mean() > .05: mask = a[..., 3] >= 128          # see-through background
else:   # flat background (white, or the skill's chroma-key colour): the most common border colour
    bd = np.concatenate([a[0, :, :3], a[-1, :, :3], a[:, 0, :3], a[:, -1, :3]]).astype(int)
    keys, cnt = np.unique((bd // 8), axis=0, return_counts=True); bgc = keys[cnt.argmax()] * 8 + 4
    mask = np.abs(a[..., :3].astype(int) - bgc).sum(2) > 90
    print('background', bgc.tolist())
    # colour spill: pixels within 3 px of the background that lean toward the key colour get that lean removed
    # (only near the edge, so a green sash or a pink cape inside the figure keeps its colour)
    near = ndimage.binary_dilation(~mask, iterations=3) & mask
    rgb = a[..., :3].astype(int); kc = int(np.argmax(bgc)); oth = [c for c in range(3) if c != kc]
    lim = np.maximum(rgb[..., oth[0]], rgb[..., oth[1]]) if bgc[kc] - max(bgc[oth[0]], bgc[oth[1]]) > 120 else None
    if lim is not None:
        spill = near & (rgb[..., kc] > lim + 24)
        a[..., kc][spill] = lim[spill]
        print('despilled', int(spill.sum()), 'edge pixels')
lab, n = ndimage.label(mask); objs = ndimage.find_objects(lab)
figs = [(i + 1, o) for i, o in enumerate(objs) if (lab[o] == i + 1).sum() > 3000]
# keep only figures, not big dark preview panels: a panel is much wider than tall
figs = [(i, o) for i, o in figs if (o[1].stop - o[1].start) < 1.6 * (o[0].stop - o[0].start)]
figs.sort(key=lambda f: f[1][0].stop)
rows = []
for f in figs:   # group by the ground line (bottom y)
    if rows and abs(rows[-1][0][1][0].stop - f[1][0].stop) < 25: rows[-1].append(f)
    else: rows.append([f])
for r in rows: r.sort(key=lambda f: f[1][1].start)
print('rows:', [len(r) for r in rows])
R = rows[row]; R = [R[k] for k in pick] if pick else R

def boots(sub, x0):
    """runs of solid pixels 6 rows above the bottom: [(start, end), ...] in picture x"""
    h = sub.shape[0]; xs = np.where(sub[h - 7])[0]; runs = []; s = None
    for j in range(len(xs)):
        if s is None: s = xs[j]
        if j == len(xs) - 1 or xs[j + 1] != xs[j] + 1:
            if xs[j] - s > 8: runs.append((x0 + int(s), x0 + int(xs[j])))
            s = None
    return runs

frames = []
for i, o in R:
    sub = lab[o] == i; rgba = a[o].copy(); rgba[..., 3] = np.where(sub, 255, 0)
    b = boots(sub, o[1].start); back = (b[0][0] + b[0][1]) / 2
    frames.append(dict(rgba=rgba, x0=o[1].start, y1=o[0].stop, back=back, runs=b, h=sub.shape[0]))
st = frames[0]; mid_off = ((st['runs'][0][0] + st['runs'][-1][1]) / 2 - st['back']) if len(st['runs']) > 1 else 0
L = max(f['back'] - f['x0'] for f in frames); Rr = max(f['x0'] + f['rgba'].shape[1] - f['back'] for f in frames)
H = max(f['h'] for f in frames); pad = 2
cw = int(np.ceil(L + Rr)) + 2 * pad; ch = H + 2 * pad; bx = int(round(L)) + pad
strip = np.zeros((ch, cw * len(frames), 4), np.uint8)
for k, f in enumerate(frames):
    ox = k * cw + bx - int(round(f['back'] - f['x0'])); oy = ch - pad - f['h']; r = f['rgba']
    region = strip[oy:oy + r.shape[0], ox:ox + r.shape[1]]; m = r[..., 3] > 0; region[m] = r[m]
# one shared palette for every frame, so colours don't flicker between frames
op = strip[..., 3] > 0; rgb = strip[..., :3].copy(); rgb[~op] = (255, 0, 255)
q = Image.fromarray(rgb).quantize(colors=NC + 1, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert('RGB')
res = np.dstack([np.array(q), np.where(op, 255, 0).astype(np.uint8)])
Image.fromarray(res).save(out, optimize=True)
# hit guess: the first frame whose solid pixels reach furthest to the right of the back boot
reach = [int((res[:, k * cw:(k + 1) * cw, 3] > 0).any(0).nonzero()[0].max()) for k in range(len(frames))]
hit = int(np.argmax(reach)) if len(frames) > 1 else 0
fx = bx + int(round(mid_off)); fy = ch - pad
print('frames %d, cell %dx%d, standing height %d, reach %s' % (len(frames), cw, ch, st['h'], reach))
print("FANIM line: {n:%d,cw:%d,ch:%d,fx:%d,fy:%d,h0:%d,hit:%d,lead:.5,post:.45}" % (len(frames), cw, ch, fx, fy, st['h'], hit))
