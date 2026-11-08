# GPT ground texture sheet (square swatches on white) -> seamless pixel-art textures for action.html.
# Owner 2026-11-08 ("Cartoon Ground Texture Tile Set.png": grass, dirt, sand, water, cobblestone, flower grass).
#   python3 tools/art/ground_px.py <sheet.png> <out dir> <scale> <colours> <name,name,...>
# Swatches = the big non-white blocks, top row first. Each is scaled (area) to <scale> so its detail matches the props,
# made seamless (the opposite edges are cross-faded over 18% of the tile, so the texture repeats without a seam),
# reduced to <colours> colours and saved as <name>.png.
import sys, os
import numpy as np
from PIL import Image
from scipy import ndimage

src, out, k, NC = sys.argv[1], sys.argv[2], float(sys.argv[3]), int(sys.argv[4])
names = sys.argv[5].split(',')
os.makedirs(out, exist_ok=True)
a = np.array(Image.open(src).convert('RGB')).astype(int)
m = ~((a.min(2) > 235) & (a.max(2) - a.min(2) < 18))            # not white
lab, n = ndimage.label(ndimage.binary_opening(m, iterations=3))
boxes = [s for s in ndimage.find_objects(lab) if (s[0].stop - s[0].start) > 100 and (s[1].stop - s[1].start) > 100]
boxes.sort(key=lambda s: (s[0].start // 200, s[1].start))
for s, nm in zip(boxes, names):
    y0, y1, x0, x1 = s[0].start + 4, s[0].stop - 4, s[1].start + 4, s[1].stop - 4      # skip the soft rim
    sw = Image.fromarray(a[y0:y1, x0:x1].astype(np.uint8))
    T = round(min(sw.size) * k); sw = sw.resize((T, T), Image.BOX)
    t = np.array(sw).astype(float); f = int(T * .18)
    w = np.clip(np.arange(T) / f, 0, 1); w = np.minimum(w, w[::-1])                    # 0 at the edges, 1 inside
    # seamless: blend with the half-shifted copy where the original is near an edge
    sh = np.roll(np.roll(t, T // 2, 0), T // 2, 1)
    wy, wx = w[:, None], w[None, :]; wt = (np.minimum(wy, wx))[..., None]
    seam = t * wt + sh * (1 - wt)
    img = Image.fromarray(seam.clip(0, 255).astype(np.uint8)).quantize(NC, method=Image.Quantize.MEDIANCUT).convert('RGB')
    img.save(os.path.join(out, nm + '.png')); print(nm, T)
