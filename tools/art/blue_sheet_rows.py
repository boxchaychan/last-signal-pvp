"""Re-space a 4 x 4 blue move sheet whose spear tips poke over the even row lines, so nothing gets cut.

  python tools/art/blue_sheet_rows.py <sheet.png> <out.png> [rows]

Every row ends at its own ground line, so the rows are split just under those lines and pasted into equal, taller rows.
No pixel of the figures is changed. Then cut <out.png> with tools/art/blue_sheet_cut.py as usual.
"""
import sys
import numpy as np
from PIL import Image

src, out = sys.argv[1], sys.argv[2]; R = int(sys.argv[3]) if len(sys.argv) > 3 else 4
a = np.array(Image.open(src).convert('RGB')); H, W = a.shape[:2]; ch = H / R; dark = a.max(2) < 80; lines = []
for r in range(R):
    y0, y1 = int((r + .75) * ch), min(H, int((r + 1) * ch)); cnt = dark[y0:y1].sum(1)
    if cnt.max() < W * .3: raise SystemExit(f'row {r + 1}: no ground line found')
    lines.append(y0 + int(np.argmax(cnt)))
cuts = [0] + [min(H, y + 5) for y in lines]; T = max(cuts[i + 1] - cuts[i] for i in range(R)) + 2
bg = a[4, 4]; o = np.tile(bg, (T * R, W, 1)).astype(np.uint8)
for r in range(R):
    p = a[cuts[r]:cuts[r + 1]]; o[(r + 1) * T - len(p):(r + 1) * T] = p
Image.fromarray(o).save(out); print(f'{src}: ground lines {lines}, rows now {T} px, sheet {W}x{T * R}')
