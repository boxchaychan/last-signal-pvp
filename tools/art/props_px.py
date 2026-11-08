# GPT prop sheet (white background already cut) -> one pixel-art PNG per prop at the game's pixel size.
# Owner 2026-11-08: map props drawn by GPT ("Chibi Nature Props Asset Sheet.png"), converted to sit next to the rogue.
#   python3 tools/art/props_px.py <cut.png> <out dir> <ref index>=<target height px> [colours=40] [names=a,b,c,...]
#   e.g. python3 tools/art/props_px.py art/incoming/action/map/gpt_nature_cut.png art/action/props 0=282 40 oak,pine,...
# Props = blobs of the alpha mask (small specks joined to the nearest blob), sorted top row first, left to right.
# ONE scale for the whole sheet (set so prop <ref index> becomes <target height> px tall), so GPT's relative sizes stay;
# area downscale, a palette per prop (a shared one turned the oak trunk pink), a 1 px dark outline. Prints each prop's size.
import sys, os
import numpy as np
from PIL import Image
from scipy import ndimage

src, out = sys.argv[1], sys.argv[2]
ri, th = sys.argv[3].split('='); ri, th = int(ri), int(th)
NC = int(sys.argv[4]) if len(sys.argv) > 4 else 40
names = sys.argv[5].split(',') if len(sys.argv) > 5 else None
os.makedirs(out, exist_ok=True)
im = Image.open(src).convert('RGBA'); a = np.array(im); m = a[..., 3] > 128
lab, n = ndimage.label(ndimage.binary_dilation(m, iterations=6))       # parts of one prop a few px apart join up
objs = ndimage.find_objects(lab)
boxes = [(s[0].start, s[1].start, s[0].stop, s[1].stop, li + 1) for li, s in enumerate(objs) if (s[0].stop - s[0].start) * (s[1].stop - s[1].start) > 900]
rows = []
for b in sorted(boxes, key=lambda b: b[0]):                           # group into rows by vertical overlap
    for r in rows:
        if b[0] < r[0][2] and b[2] > r[0][0]: r.append(b); break
    else: rows.append([b])
boxes = [b for r in rows for b in sorted(r, key=lambda b: b[1])]
k = th / (boxes[ri][2] - boxes[ri][0])
def shrink(y0, x0, y1, x1, li):
    # only this prop's own pixels: a neighbour reaching into the box is cleared (scraps of the next tree)
    aa = a[y0:y1, x0:x1].copy(); aa[lab[y0:y1, x0:x1] != li] = 0; sub = Image.fromarray(aa); w, h = max(1, round((x1 - x0) * k)), max(1, round((y1 - y0) * k))
    p = np.array(sub).astype(float) / 255; p[..., :3] *= p[..., 3:4]
    q = np.array(Image.fromarray((p * 255).astype(np.uint8)).resize((w, h), Image.BOX)).astype(float)
    al = q[..., 3:4] / 255; rgb = np.where(al > 0, q[..., :3] / np.maximum(al, 1e-6), 0).clip(0, 255)
    return rgb.astype(np.uint8), al[..., 0] > .5
small = [shrink(*b) for b in boxes]
for i, ((rgb, mm), b) in enumerate(zip(small, boxes)):
    pal = Image.fromarray(rgb[mm][None]).quantize(NC, method=Image.Quantize.MEDIANCUT)   # each prop its own colours
    q = np.array(Image.fromarray(rgb).quantize(palette=pal, dither=Image.Dither.NONE).convert('RGB'))
    h, w = mm.shape; can = np.zeros((h + 2, w + 2, 4), np.uint8)
    can[1:-1, 1:-1, :3] = q; can[1:-1, 1:-1, 3] = mm * 255
    mk = can[..., 3] > 0; ring = ndimage.binary_dilation(mk) & ~mk; can[ring] = (29, 26, 34, 255)
    nm = names[i] if names and i < len(names) else f'prop{i}'
    Image.fromarray(can).save(os.path.join(out, nm + '.png')); print(nm, w + 2, 'x', h + 2)
print('scale', round(k, 4), 'props', len(boxes))
