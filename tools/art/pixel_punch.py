# "Punch" for our pixel sprites (owner 2026-11-14: colours not deep / crisp enough; liked the look of map 1 = few, deep colours,
# bold shadows, crisp dark edges). Free post-process; the input is never overwritten.
#   python3 tools/art/pixel_punch.py in.png out.png [strength 1.0] [colours 24]
# 1) saturation up, 2) shadows deeper / highlights a touch brighter (S-curve on value), 3) colours merged to a small palette
# (flat areas, no stray in-between pixels), 4) the outer edge becomes a dark version of its own colour (crisp outline).
import sys, colorsys, numpy as np
from PIL import Image
src, dst = sys.argv[1], sys.argv[2]; S = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0; NC = int(sys.argv[4]) if len(sys.argv) > 4 else 24
im = Image.open(src).convert('RGBA'); a = np.asarray(im).astype(float); al = a[..., 3] > 0
rgb = a[..., :3] / 255
mx, mn = rgb.max(2), rgb.min(2); v = mx; s = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
# hue-preserving: scale the chroma part (rgb - v) for saturation, then remap v
s2 = np.clip(s * (1 + .35 * S), 0, 1); v2 = np.clip(v + S * (.18 * np.sin((v - .5) * np.pi) * (1 - v) * 1.2 - .06 * (v < .35)), 0, 1)
v2 = np.where(v < .35, v * (1 - .22 * S), v2)   # shadows deeper
k = np.where(s > 1e-6, s2 / np.maximum(s, 1e-6), 1)[..., None]
out = (v[..., None] - (v[..., None] - rgb) * k); out = out * (v2 / np.maximum(v, 1e-6))[..., None]; out = np.clip(out, 0, 1)
b = a.copy(); b[..., :3] = out * 255
# small palette over the opaque pixels only
op = Image.fromarray(b.astype(np.uint8)); q = op.convert('RGB').quantize(colors=NC, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert('RGB')
b[..., :3] = np.where(al[..., None], np.asarray(q).astype(float), b[..., :3])
# crisp outline: opaque pixels touching transparency get a dark version of their colour
edge = al & ~(np.roll(al, 1, 0) & np.roll(al, -1, 0) & np.roll(al, 1, 1) & np.roll(al, -1, 1))
glow = (rgb.max(2) > .7) & (((rgb[..., 0] > .8) & (rgb[..., 2] < .6)) | (rgb.min(2) > .68))   # bright orange / white: effects, sparks, glowing parts
edge &= ~glow
dark = b[..., :3] * .28 + np.array([12, 8, 22]) * .72
b[..., :3] = np.where(edge[..., None], np.minimum(b[..., :3], dark), b[..., :3])
b[..., :3] = np.where(glow[..., None], np.maximum(b[..., :3], a[..., :3]), b[..., :3])   # effects / sparks: never darker than drawn
Image.fromarray(np.clip(b, 0, 255).astype(np.uint8)).save(dst)
