#!/usr/bin/env python3
"""Pack a champion's PixelLab clips (east) into one sheet for bag.html.
usage: champ_sheet.py <download dir with animations/idle/east, attack/east> <out.png>
9 columns of 204 px: row 0 = idle frames 0-8, rows 1-2 = attack frames 0-16 (cell 9+f). Nothing is stripped."""
import sys, glob
from PIL import Image
src, out = sys.argv[1], sys.argv[2]
C = 204
sh = Image.new('RGBA', (9 * C, 3 * C), (0, 0, 0, 0))
for a, base in (('idle', 0), ('attack', 9)):
    for i, f in enumerate(sorted(glob.glob(f'{src}/animations/{a}/east/*.png'))):
        c = base + i
        sh.alpha_composite(Image.open(f).convert('RGBA'), (c % 9 * C, c // 9 * C))
sh.save(out, optimize=True)
print(out, sh.size)
