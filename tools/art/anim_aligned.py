# Frames that already share one canvas (same ground line, same scale, e.g. the "frames_full/" folder of a Codex/ChatGPT run,
# owner 2026-11-06 Wukong) -> ONE animation sheet at the still picture's height, coloured with the still's palette.
#   python3 tools/art/anim_aligned.py <out.png> <still.png> <height> <name>=<frame.png,frame.png,...> [<name>=...]
#     height = standing height wanted (the still picture's height); the FIRST frame of the first row is the standing frame
# Keeps the drawn positions (jumps stay in the air), crops every frame to the union of all frames, alpha cut at 50 %.
# Prints the layout as JSON (rows, cw, ch, fx = between the standing frame's boots, fy = its ground line, h0).
import sys, json
import numpy as np
from PIL import Image

out, pal_src, H = sys.argv[1], sys.argv[2], float(sys.argv[3])
rows = []
for arg in sys.argv[4:]:
    name, files = arg.split('=', 1)
    rows.append((name, [Image.open(f).convert('RGBA') for f in files.split(',')]))
al = [np.array(im)[..., 3] >= 128 for _, ims in rows for im in ims]
ys = [np.where(m.any(1))[0] for m in al]; xs = [np.where(m.any(0))[0] for m in al]
X0, X1 = min(x[0] for x in xs), max(x[-1] for x in xs) + 1; Y0, Y1 = min(y[0] for y in ys), max(y[-1] for y in ys) + 1
st = al[0]; sy = np.where(st.any(1))[0]; k = H / (sy[-1] + 1 - sy[0])
# feet point of the standing frame: ground = its lowest row, x = middle between its two boots (6 rows above the ground)
gy = sy[-1]; bx = np.where(st[gy - 6 * max(1, round(1 / k))])[0]
runs = np.split(bx, np.where(np.diff(bx) > 1)[0] + 1)
fx0 = (runs[0][0] + runs[-1][-1]) / 2 if len(runs) > 1 else (bx[0] + bx[-1]) / 2
pad = 2; CW = round((X1 - X0) * k) + 2 * pad; CH = round((Y1 - Y0) * k) + 2 * pad; NC = max(len(ims) for _, ims in rows)
sheet = Image.new('RGBA', (CW * NC, CH * len(rows)), (0, 0, 0, 0))
for ri, (_, ims) in enumerate(rows):
    for fi, im in enumerate(ims):
        c = im.crop((X0, Y0, X1, Y1)).resize((CW - 2 * pad, CH - 2 * pad), Image.BOX)
        a = np.array(c); a[..., 3] = np.where(a[..., 3] >= 128, 255, 0)
        sheet.alpha_composite(Image.fromarray(a), (fi * CW + pad, ri * CH + pad))
# the still's colours (same as anim_rows.py)
s = np.array(Image.open(pal_src).convert('RGBA')); cols = np.unique(s[s[..., 3] > 0][:, :3], axis=0)
if len(cols) > 255:
    q = Image.fromarray(s[..., :3]).quantize(255, dither=Image.Dither.NONE); cols = np.array(q.getpalette()[:765]).reshape(-1, 3)
pimg = Image.new('P', (1, 1)); flat = list(cols.flatten()) + [0] * (768 - cols.size); pimg.putpalette(flat[:768])
a = np.array(sheet); vis = a[..., 3] > 0
q = Image.fromarray(a[..., :3]).quantize(palette=pimg, dither=Image.Dither.NONE).convert('RGB')
Image.fromarray(np.dstack([np.array(q), np.where(vis, 255, 0).astype(np.uint8)])).save(out, optimize=True)
print(json.dumps(dict(rows=[dict(name=n, n=len(ims)) for n, ims in rows], cw=CW, ch=CH,
                      fx=pad + round((fx0 - X0) * k), fy=pad + round((gy + 1 - Y0) * k), h0=int(H))))
