# GPT animation sheet (3 rows x 4 frames, already snapped to pixels with gptpx.py) -> game sheet.
# usage: python3 tools/art/anim_sheet.py <pixel sheet.png> <out.png>
#   1) GPTPX_GRID=2.8,3.8 python3 tools/art/gptpx.py <GPT sheet> <pixel sheet> 14   (the sheets use a ~3.2 px grid;
#      if one axis comes out different, narrow the range, e.g. 3.05,3.5)
#   2) this script: finds the 3 rows and 4 frames by the empty gaps between them, lines every frame up on the feet
#      (frames in the air keep their height above the row's ground line) and packs them into equal cells.
# Prints the numbers for ANIMS in bb.html: cw, ch (cell size), h0 (height of the first idle frame = drawn as tall
# as the standing picture). The feet sit at (cw/2, ch-2) in every cell.
import sys, json, numpy as np
from PIL import Image
src, out = sys.argv[1], sys.argv[2]
A = np.array(Image.open(src).convert('RGBA'))
al = A[:, :, 3] > 0
H, W = al.shape

def bands(prof, gap=2, minlen=6):
    s, res, run = None, [], 0
    for i, v in enumerate(prof):
        if v:
            if s is None: s = i
            run = 0
        elif s is not None:
            run += 1
            if run >= gap: res.append([s, i - run + 1]); s, run = None, 0
    if s is not None: res.append([s, len(prof)])
    return [b for b in res if b[1] - b[0] >= minlen]

def fix(bs, n, total):
    # merge small pieces into a neighbour until n remain; split the widest if too few
    bs = [list(b) for b in bs]
    while len(bs) > n:
        i = min(range(len(bs)), key=lambda k: bs[k][1] - bs[k][0])
        j = i - 1 if i > 0 and (i == len(bs) - 1 or bs[i][0] - bs[i - 1][1] < bs[i + 1][0] - bs[i][1]) else i + 1
        a, b = sorted([i, j]); bs[a] = [bs[a][0], bs[b][1]]; del bs[b]
    while len(bs) < n:
        i = max(range(len(bs)), key=lambda k: bs[k][1] - bs[k][0]); a, b = bs[i]; m = (a + b) // 2
        bs[i:i + 1] = [[a, m], [m, b]]
    return bs

rows = fix(bands(al.any(1)), 3, H)
frames = []
for r, (y0, y1) in enumerate(rows):
    cols = fix(bands(al[y0:y1].any(0)), 4, W)
    fr = []
    for (x0, x1) in cols:
        m = al[y0:y1, x0:x1]; ys, xs = np.where(m)
        top, bot, lft, rgt = ys.min(), ys.max(), xs.min(), xs.max()
        band = m[max(top, bot - max(2, int((bot - top) * .08))):bot + 1]
        fy, fx = np.where(band)
        fr.append(dict(img=A[y0:y1, x0:x1], top=top, bot=bot, l=lft, r=rgt, feet=fx.mean() if len(fx) else (lft + rgt) / 2))
    g = max(f['bot'] for f in fr)
    onground = [f for f in fr if f['bot'] >= g - 2]
    off = np.mean([f['feet'] - (f['l'] + f['r']) / 2 for f in onground])
    for f in fr:
        f['g'] = g
        if f['bot'] < g - 2: f['feet'] = (f['l'] + f['r']) / 2 + off   # in the air: keep the body over the feet line
    frames.append(fr)

half = max(max(f['feet'] - f['l'], f['r'] - f['feet']) for row in frames for f in row)
cw = int(np.ceil(half * 2)) + 4
ch = max(f['g'] - f['top'] for row in frames for f in row) + 4
sheet = Image.new('RGBA', (cw * 4, ch * 3), (0, 0, 0, 0))
for r, row in enumerate(frames):
    for c, f in enumerate(row):
        # feet at (cw/2, ch-2) of the cell; paste only this frame's pixels, clipped to its cell
        im = Image.fromarray(f['img'])
        ox, oy = int(round(cw / 2 - f['feet'])), int((ch - 2) - f['g'])
        cell = Image.new('RGBA', (cw, ch), (0, 0, 0, 0)); cell.paste(im, (ox, oy), im)
        sheet.alpha_composite(cell, (c * cw, r * ch))
sheet.save(out, optimize=True)
h0 = frames[0][0]['g'] - frames[0][0]['top'] + 1
print(json.dumps({'cw': int(cw), 'ch': int(ch), 'h0': int(h0)}))
