"""'16-bit' look for a pixel sprite (owner 2026-11-24 "16 บิต"), FREE: 15 colours per sprite (one console sprite palette + transparent),
chosen by median cut so the shading steps stay, every channel snapped to 5 bits (32 levels, like 15-bit console colour),
a little saturation / contrast punch, outer edge a dark version of its own colour (not pure black).
  python3 tools/art/sixteenbit.py in.png out.png [colours=15]"""
import sys, numpy as np
from PIL import Image
src, dst = sys.argv[1], sys.argv[2]; NC = int(sys.argv[3]) if len(sys.argv) > 3 else 15
im = Image.open(src).convert('RGBA'); a = np.asarray(im).astype(float); op = a[..., 3] > 0
rgb = a[..., :3] / 255; v = rgb.max(2, keepdims=True); rgb = np.clip(v - (v - rgb) * 1.18, 0, 1); rgb = np.clip((rgb - .5) * 1.08 + .5, 0, 1)
b = a.copy(); b[..., :3] = rgb * 255
q = Image.fromarray(b.astype(np.uint8)).convert('RGB').quantize(colors=NC, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert('RGB')
c = np.asarray(q).astype(float); c = np.round(c / 255 * 31) / 31 * 255
out = a.copy(); out[..., :3] = np.where(op[..., None], c, a[..., :3])
edge = op & ~(np.roll(op, 1, 0) & np.roll(op, -1, 0) & np.roll(op, 1, 1) & np.roll(op, -1, 1)); out[edge, :3] = out[edge, :3] * .25 + np.array([16, 10, 24]) * .75
Image.fromarray(out.astype(np.uint8)).save(dst)
