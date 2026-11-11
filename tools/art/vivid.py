# Owner 2026-11-11 "ทำสีให้สดได้ไหม สีมันขุ่น": brighter, cleaner colours for a picture (RGBA kept): vibrance (dull colours get
# more saturation than already strong ones), a little contrast, lifted shadows, a light sharpen.
#   python3 tools/art/vivid.py <in> <out> [strength=1]
import sys, numpy as np
from PIL import Image, ImageFilter
def vivid(im, k=1.0):
    im = im.convert('RGBA'); a = np.asarray(im).astype(float) / 255; rgb = a[..., :3]
    mx, mn = rgb.max(2, keepdims=True), rgb.min(2, keepdims=True); sat = mx - mn; grey = rgb.mean(2, keepdims=True)
    boost = 1 + .55 * k * (1 - sat)                                  # vibrance
    rgb = grey + (rgb - grey) * boost
    rgb = (rgb - .5) * (1 + .12 * k) + .5 + .03 * k                  # contrast + a touch brighter
    rgb = rgb + .06 * k * (1 - rgb) * (rgb < .35)                    # lift the deepest shadows (less muddy)
    out = np.dstack([np.clip(rgb, 0, 1), a[..., 3:]])
    o = Image.fromarray((out * 255).astype(np.uint8), 'RGBA')
    return o.filter(ImageFilter.UnsharpMask(1.2, int(40 * k), 2))
if __name__ == '__main__':
    k = float(sys.argv[3]) if len(sys.argv) > 3 else 1
    vivid(Image.open(sys.argv[1]), k).save(sys.argv[2])
