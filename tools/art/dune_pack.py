"""Pack frame strips (from tools/art/blue_sheet_cut.py) into small grid WebP sheets for dune.html.

  python tools/art/dune_pack.py <strip.png> <out.webp> <scale> [first last]

-> <out.webp>  frames first..last (inclusive, default all) in a grid at most 2048 px wide, each frame trimmed to the shared box
   prints one JSON line {"n", "w", "h", "foot", "cols"}; art/dune/sprites.json is built from these lines by the caller.
"""
import sys, json
from PIL import Image

src, out, k = sys.argv[1], sys.argv[2], float(sys.argv[3])
meta = json.load(open(src[:-4] + '.json'))
im = Image.open(src).convert('RGBA'); fw, fh, n = meta['w'], meta['h'], meta['n']
a = int(sys.argv[4]) if len(sys.argv) > 4 else 0
b = int(sys.argv[5]) if len(sys.argv) > 5 else n - 1
frames = [im.crop((i * fw, 0, (i + 1) * fw, fh)) for i in range(a, b + 1)]
box = None
for f in frames:
    bb = f.getchannel('A').point(lambda v: 255 if v > 12 else 0).getbbox()
    if bb: box = bb if box is None else (min(box[0], bb[0]), min(box[1], bb[1]), max(box[2], bb[2]), max(box[3], bb[3]))
x0, y0, x1, y1 = max(0, box[0] - 2), max(0, box[1] - 2), min(fw, box[2] + 2), min(fh, box[3] + 2)
w, h = max(1, round((x1 - x0) * k)), max(1, round((y1 - y0) * k))
cols = min(len(frames), max(1, 2048 // w)); rows = (len(frames) + cols - 1) // cols
sheet = Image.new('RGBA', (cols * w, rows * h), (0, 0, 0, 0))
for i, f in enumerate(frames):
    sheet.paste(f.crop((x0, y0, x1, y1)).resize((w, h), Image.LANCZOS), (i % cols * w, i // cols * h))
sheet.save(out, 'WEBP', quality=90, alpha_quality=95, method=6)
print(json.dumps({'n': len(frames), 'w': w, 'h': h, 'foot': round((meta['foot'] - y0) * k), 'cols': cols, 'cx': round((fw / 2 - x0) * k)}))
