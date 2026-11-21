"""Cream / beige -> clean cool white on pixel sprites (owner 2026-11-21 "ปรับสีให้มันขาวหน่อย ตัวนกมันสีขาว").

PixelLab drew the eagle's white feathers as cream (251,237,222) with a peach shade (217,185,166).
Every light, low-saturation, warm pixel is turned into a neutral-to-cool white of the same brightness,
so the shading steps stay but the feathers read as white. Saturated colours (gold, blue, brown) are not touched.

python3 tools/art/cream_to_white.py <out_dir> <png> [<png> ...]      (originals are not changed)
"""
import os
import sys

from PIL import Image

SAT_MAX = .40      # only low-saturation colours (gold 0.84, the yellow highlight 0.44 stay)
VAL_MIN = 150      # only light colours (brown leather, dark outline stay)
TINT = (.97, 1.0, 1.04)   # a touch of blue = reads whiter next to the warm sand
GAIN = 1.03


def whiten(p):
    r, g, b, a = p
    mx, mn = max(r, g, b), min(r, g, b)
    if a == 0 or mx < VAL_MIN or (mx - mn) / mx > SAT_MAX or not (r >= b):
        return p
    lum = .3 * r + .59 * g + .11 * b
    return tuple(min(255, round(lum * GAIN * t)) for t in TINT) + (a,)


def main():
    out, files = sys.argv[1], sys.argv[2:]
    os.makedirs(out, exist_ok=True)
    for f in files:
        im = Image.open(f).convert('RGBA')
        im.putdata([whiten(p) for p in im.getdata()])
        dst = os.path.join(out, os.path.basename(f))
        im.save(dst)
        print(dst)


if __name__ == '__main__':
    main()
