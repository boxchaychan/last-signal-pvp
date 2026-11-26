# Shorter legs for the pixgrind hero, free (owner 2026-11-26 "ตัวละครขายาวไป"): in every frame a band of rows across the shins / knees
# is taken out and everything above it moves down, so the feet stay on the ground row and the body keeps its pixels.
#   python3 tools/art/pixgrind_shortlegs.py <in strip.png> <out strip.png> <cell px> <rows to remove> [band top above the feet, 17]
# The band starts <top> rows above the lowest opaque row of each frame (the feet; airborne run frames move with them).
import sys
import numpy as np
from PIL import Image

src, dst, cell, n = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
top = int(sys.argv[5]) if len(sys.argv) > 5 else 17
a = np.asarray(Image.open(src).convert('RGBA')).copy()
out = np.zeros_like(a)
for k in range(a.shape[1] // cell):
    f = a[:, k * cell:(k + 1) * cell]
    rows = np.where(f[..., 3].max(1) > 0)[0]
    if not len(rows): continue
    feet = rows.max(); b0 = max(0, feet - top); b1 = b0 + n
    g = np.zeros_like(f)
    g[b1:] = f[b1:]                      # band bottom .. feet stay where they are
    g[n:b1] = f[:b0]                     # everything above the band moves down by n
    out[:, k * cell:(k + 1) * cell] = g
Image.fromarray(out, 'RGBA').save(dst)
print(dst, 'frames', a.shape[1] // cell, 'removed', n, 'rows')
