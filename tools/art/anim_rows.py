# Several animation rows (each a strip from frames_import.py, with its own scale) -> ONE sheet at one shared scale,
# coloured with the still picture's palette so the animation and the standing picture match (owner 2026-11-06, Loki from Codex).
#   python3 tools/art/anim_rows.py <out.png> <palette/still.png> <height> <strip.png> <n,cw,ch,fx,fy,h0> <name> [<strip.png> <nums> <name> ...]
#     height = standing height wanted in the sheet (use the still picture's height so both line up)
# Every frame is scaled so that row's standing height (h0) becomes <height>, pinned at the row's feet point (fx,fy),
# alpha cut at 50 %, then mapped to the still's colours. Prints the sheet layout as JSON (rows, cell size, feet point).
import sys, json
import numpy as np
from PIL import Image

out, pal_src, H = sys.argv[1], sys.argv[2], float(sys.argv[3])
args = sys.argv[4:]
rows = []
for i in range(0, len(args), 3):
    n, cw, ch, fx, fy, h0 = [int(v) for v in args[i + 1].split(',')]
    rows.append(dict(im=Image.open(args[i]).convert('RGBA'), n=n, cw=cw, ch=ch, fx=fx, fy=fy, h0=h0, name=args[i + 2], k=H / h0))
L = max(r['fx'] * r['k'] for r in rows); Rr = max((r['cw'] - r['fx']) * r['k'] for r in rows)
T = max(r['fy'] * r['k'] for r in rows); Bt = max((r['ch'] - r['fy']) * r['k'] for r in rows)
pad = 2; CW = int(np.ceil(L + Rr)) + 2 * pad; CH = int(np.ceil(T + Bt)) + 2 * pad; FX = int(round(L)) + pad; FY = int(round(T)) + pad
NC = max(r['n'] for r in rows)
sheet = Image.new('RGBA', (CW * NC, CH * len(rows)), (0, 0, 0, 0))
for ri, r in enumerate(rows):
    for f in range(r['n']):
        cell = r['im'].crop((f * r['cw'], 0, (f + 1) * r['cw'], r['ch']))
        w2, h2 = max(1, round(r['cw'] * r['k'])), max(1, round(r['ch'] * r['k']))
        sm = cell.resize((w2, h2), Image.BOX)
        a = np.array(sm); a[..., 3] = np.where(a[..., 3] >= 128, 255, 0); sm = Image.fromarray(a)
        sheet.alpha_composite(sm, (f * CW + FX - round(r['fx'] * r['k']), ri * CH + FY - round(r['fy'] * r['k'])))
# the still's colours: every visible pixel goes to the nearest colour of the standing picture
st = np.array(Image.open(pal_src).convert('RGBA')); cols = np.unique(st[st[..., 3] > 0][:, :3], axis=0)
if len(cols) > 255:
    q = Image.fromarray(st[..., :3]).quantize(255, dither=Image.Dither.NONE); cols = np.array(q.getpalette()[:765]).reshape(-1, 3)
pimg = Image.new('P', (1, 1)); flat = list(cols.flatten()) + [0] * (768 - cols.size); pimg.putpalette(flat[:768])
a = np.array(sheet); vis = a[..., 3] > 0
q = Image.fromarray(a[..., :3]).quantize(palette=pimg, dither=Image.Dither.NONE).convert('RGB')
res = np.dstack([np.array(q), np.where(vis, 255, 0).astype(np.uint8)])
Image.fromarray(res).save(out, optimize=True)
meta = dict(rows=[dict(name=r['name'], n=r['n']) for r in rows], cw=CW, ch=CH, fx=FX, fy=FY - pad, h0=int(H))
print(json.dumps(meta))
