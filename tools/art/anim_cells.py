# Rows of animation frames from different pictures -> ONE sheet at the still's height, coloured with the still's palette.
# Each row is either a grid picture (one action, e.g. ChatGPT's 3x2 / 2x2 sheets, owner 2026-11-07 Wukong south/north) or a list
# of frames that already share one canvas (e.g. a run's frames_full/). Inside a row the frames keep their drawn positions (jumps,
# steps); every row is scaled on its own so that its FIRST frame (the standing pose) is <height> tall, because the generator drew
# each picture at a slightly different size (Wukong: 263-340 px). Rows are pinned at the first frame's ground line and the middle
# between its feet.
# --clean: cut what the generator's own background removal left (Wukong 2026-11-07): plain white caught between the legs and
#          the soft grey ground shadow under the feet. Only pure, untinted white patches go (white fur has a tint and stays).
#   python3 tools/art/anim_cells.py <out.png> <still.png> <height> [--clean] <name>=<grid.png>:<cols>x<rows>[:<n>] | <name>=<f.png,f.png,...> ...
# Prints the layout as JSON (rows, cw, ch, fx, fy, h0) like anim_rows.py / anim_aligned.py.
import sys, json
import numpy as np
from PIL import Image
from scipy import ndimage

out, pal_src, H = sys.argv[1], sys.argv[2], float(sys.argv[3])
CLEAN = '--clean' in sys.argv

def clean(f):
    a = np.array(f); rgb = a[..., :3].astype(int); al = a[..., 3]; mx, mn = rgb.max(2), rgb.min(2)
    lab, n = ndimage.label((al >= 128) & (mn >= 238) & (mx - mn <= 10))
    if n:
        sz = ndimage.sum(np.ones_like(al), lab, range(1, n + 1)); big = np.isin(lab, 1 + np.where(sz >= 120)[0]); al[big] = 0
    ys = np.where((al >= 128).any(1))[0]
    if len(ys):
        y0 = ys[-1] - max(4, (ys[-1] - ys[0]) * 8 // 100); band = np.zeros_like(al, bool); band[y0:] = True
        al[band & (al < 250) & (mx - mn <= 24) & (rgb.mean(2) > 110)] = 0
    a[..., 3] = al; return Image.fromarray(a)

rows = []
for arg in [x for x in sys.argv[4:] if x != '--clean']:
    name, spec = arg.split('=', 1)
    if ':' in spec:
        p = spec.split(':'); im = Image.open(p[0]).convert('RGBA'); c, r = [int(v) for v in p[1].split('x')]
        n = int(p[2]) if len(p) > 2 else c * r; cw, ch = im.width // c, im.height // r
        fr = [im.crop((i % c * cw, i // c * ch, i % c * cw + cw, i // c * ch + ch)) for i in range(n)]
    else:
        fr = [Image.open(f).convert('RGBA') for f in spec.split(',')]
    rows.append((name, [clean(f) for f in fr] if CLEAN else fr))

def feet(m):
    """ground row and the middle between the outer feet (runs a few rows above the ground) of a standing frame"""
    ys = np.where(m.any(1))[0]; gy = ys[-1]; probe = max(ys[0], gy - max(3, (gy - ys[0]) // 40))
    xs = np.where(m[probe])[0]
    return ys[0], gy, (xs[0] + xs[-1]) / 2

placed = []   # per row: k, and for each frame (scaled image, x offset, y offset) relative to the feet point
for name, fr in rows:
    m0 = np.array(fr[0])[..., 3] >= 128; top, gy, fx = feet(m0); k = H / (gy + 1 - top)
    out_fr = []
    for f in fr:
        w2, h2 = max(1, round(f.width * k)), max(1, round(f.height * k))
        s = f.resize((w2, h2), Image.BOX); a = np.array(s); a[..., 3] = np.where(a[..., 3] >= 128, 255, 0)
        out_fr.append((Image.fromarray(a), -fx * k, -(gy + 1) * k))
    placed.append((name, out_fr))
# common cell: the union of every scaled frame around the feet point
L = R = T = B = 0
for _, fr in placed:
    for im, ox, oy in fr:
        bb = im.getbbox()
        if not bb: continue
        L = min(L, ox + bb[0]); R = max(R, ox + bb[2]); T = min(T, oy + bb[1]); B = max(B, oy + bb[3])
pad = 2; CW = int(np.ceil(R - L)) + 2 * pad; CH = int(np.ceil(B - T)) + 2 * pad
FX = pad + int(round(-L)); FY = pad + int(round(-T))
NC = max(len(fr) for _, fr in placed)
sheet = Image.new('RGBA', (CW * NC, CH * len(placed)), (0, 0, 0, 0))
for ri, (_, fr) in enumerate(placed):
    for fi, (im, ox, oy) in enumerate(fr):
        sheet.alpha_composite(im, (fi * CW + FX + int(round(ox)), ri * CH + FY + int(round(oy))))
# the still's colours (same as anim_rows.py)
s = np.array(Image.open(pal_src).convert('RGBA')); cols = np.unique(s[s[..., 3] > 0][:, :3], axis=0)
if len(cols) > 255:
    q = Image.fromarray(s[..., :3]).quantize(255, dither=Image.Dither.NONE); cols = np.array(q.getpalette()[:765]).reshape(-1, 3)
pimg = Image.new('P', (1, 1)); flat = list(cols.flatten()) + [0] * (768 - cols.size); pimg.putpalette(flat[:768])
a = np.array(sheet); vis = a[..., 3] > 0
q = Image.fromarray(a[..., :3]).quantize(palette=pimg, dither=Image.Dither.NONE).convert('RGB')
Image.fromarray(np.dstack([np.array(q), np.where(vis, 255, 0).astype(np.uint8)])).save(out, optimize=True)
print(json.dumps(dict(rows=[dict(name=n, n=len(fr)) for n, fr in placed], cw=CW, ch=CH, fx=FX, fy=FY, h0=int(H))))
