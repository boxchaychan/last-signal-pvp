# One arm of a star effect (owner 2026-11-10 "โซ่ทำให้ดึงตามเป้าไม่ได้หรือ"): from the cut star sheet (fx/<key>.png, chains all round)
# take the arm nearest to pointing right, turn it to point exactly right and keep only a wedge round it, so the game can send one
# chain to each target (turned toward it, stretched to its distance).
#   python3 tools/video/vfx_one_arm.py vfx_bzchainall vfx_bzchain1 [wedge degrees]
import json, sys, numpy as np
from PIL import Image
from scipy import ndimage
src, dst = sys.argv[1], sys.argv[2]; WG = float(sys.argv[3]) if len(sys.argv) > 3 else 15
man = json.load(open('fx/manifest.json')); m = man[src]; sh = np.asarray(Image.open(f'fx/{src}.png').convert('RGBA'))
w, h, cols, n, cx, cy = m['w'], m['h'], m.get('cols', m['n']), m['n'], m['ax'], m['ay']
fr = [sh[(i // cols) * h:(i // cols + 1) * h, (i % cols) * w:(i % cols + 1) * w] for i in range(n)]
yy, xx = np.mgrid[0:h, 0:w]; ang = np.degrees(np.arctan2(yy - cy, xx - cx)); rr = np.hypot(yy - cy, xx - cx)
hist = np.zeros(360)
for f in fr[n // 4: n // 2]: hist += np.bincount(((ang % 360).astype(int))[(rr > 40) & (f[..., 3] > 80)], minlength=360)[:360]
hs = np.convolve(np.r_[hist[-10:], hist, hist[:10]], np.ones(9) / 9, 'same')[10:-10]
cand = [a for a in range(360) if hs[a] == hs[max(0, a - 12):a + 13].max() and hs[a] > hs.mean()]
a0 = min(cand, key=lambda a: min(a, 360 - a)); a0 = a0 if a0 < 180 else a0 - 360
print('arm at', a0, 'deg')
out = []
for f in fr:
    r = ndimage.rotate(f, a0, axes=(1, 0), reshape=False, order=1)          # turn the arm onto 0 degrees (pointing right)
    keep = (np.abs(ang) < WG) & (xx > cx - 6) | (rr < 18)
    soft = np.clip((WG + 4 - np.abs(ang)) / 4, 0, 1); a = r[..., 3].astype(float) * np.where(rr < 18, 1, soft * (xx > cx - 6))
    r = r.copy(); r[..., 3] = a.astype(np.uint8); out.append(r)
al = np.stack([o[..., 3] > 30 for o in out]).any(0); ys, xs = np.nonzero(al)
x0, x1, y0, y1 = max(0, cx - 12), xs.max() + 2, ys.min() - 1, ys.max() + 2
W2, H2 = x1 - x0, y1 - y0; S = Image.new('RGBA', (W2 * cols, H2 * (-(-n // cols))))
for i, o in enumerate(out): S.paste(Image.fromarray(o[y0:y1, x0:x1]), ((i % cols) * W2, (i // cols) * H2))
S.save(f'fx/{dst}.png', optimize=True)
man[dst] = dict(w=int(W2), h=int(H2), n=n, cols=cols, fps=m['fps'], ax=int(cx - x0), ay=int(cy - y0), len=int(xs.max() - cx), src=f'one arm of {src}, tools/video/vfx_one_arm.py')
json.dump(man, open('fx/manifest.json', 'w'), separators=(',', ':')); print(dst, man[dst])
