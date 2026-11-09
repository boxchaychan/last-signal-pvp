# Archer E (owner 2026-11-09 "สกิลนี้แทน สายฟ้า เปลี่ยนโทนสีด้วย"): the owner's pasted 6 x 6 sheet (a green orb shoots a bolt of
# light to the right, a burst with dark smoke where it lands) came with its soft glow flattened into solid cyan / green / white
# bands. Kept: the white-hot cores (orb, the bolt's droplets, the impact flash) when they are not part of a big white patch
# touching the cell edge, and the dark smoke. Drawn in the archer's look: cores pale green-white with a neon green rim, smoke
# black-green ink with a neon rim, a soft green glow round both.
#   python3 tools/art/green_bolt_fx.py  -> fx/pfx_gbolt_k.png + manifest (anchor = the impact; the orb sits ~148 px to its left)
import json
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage
SRC, KEY, C, R, K = 'art/incoming/pfx/green-bolt-sheet.png', 'pfx_gbolt_k', 6, 6, .5
RIM, INK, CORE, GLOW = [70, 255, 125], [4, 26, 12], [225, 255, 232], [40, 225, 95]
a = np.array(Image.open(SRC).convert('RGB')).astype(int); H, W = a.shape[:2]; cw, ch = W / C, H / R
ow, oh = round(cw * K), round(ch * K); out = Image.new('RGBA', (8 * ow, -(-C * R // 8) * oh))
for i in range(C * R):
    x0, y0 = round(i % C * cw), round(i // C * ch); q = a[y0:y0 + round(ch), x0:x0 + round(cw)]
    white = q.min(-1) > 236
    lab, n = ndimage.label(white); keep = np.zeros_like(white)
    for j, sl in enumerate(ndimage.find_objects(lab), 1):
        part = lab[sl] == j; sz = part.sum(); ys, xs = sl
        edge = ys.start == 0 or xs.start == 0 or ys.stop >= q.shape[0] or xs.stop >= q.shape[1]
        if not edge and 6 <= sz < 9000: keep[sl] |= part
    smoke = (q.max(-1) < 150) & (q.max(-1) > 25)
    lab2, n2 = ndimage.label(smoke)
    for j, sl in enumerate(ndimage.find_objects(lab2), 1):                     # the black corner pieces of the bands go
        ys, xs = sl
        if ys.start == 0 or xs.start == 0 or ys.stop >= q.shape[0] or xs.stop >= q.shape[1]: smoke[sl] &= lab2[sl] != j
    sm = lambda m: np.array(Image.fromarray((m * 255).astype(np.uint8)).resize((ow, oh), Image.BOX)) > 100
    co, sk = sm(keep), sm(smoke); allm = co | sk
    o = np.zeros((oh, ow, 4), np.uint8)
    o[ndimage.binary_dilation(allm, iterations=2) & ~allm] = RIM + [255]
    o[sk] = INK + [240]; o[co] = CORE + [255]
    g = np.zeros((oh, ow, 4), np.uint8); g[..., :3] = GLOW; g[..., 3] = ndimage.binary_dilation(allm, iterations=4) * 150
    c = Image.fromarray(g).filter(ImageFilter.GaussianBlur(7)); c.alpha_composite(Image.fromarray(o))
    out.alpha_composite(c, (i % 8 * ow, i // 8 * oh))
out.save('fx/' + KEY + '.png', optimize=True)
man = json.load(open('fx/manifest.json'))
man[KEY] = {'w': ow, 'h': oh, 'n': C * R, 'cols': 8, 'fps': 30, 'ax': round(ow * .79), 'ay': round(oh * .5), 'src': "owner's pasted green bolt sheet (tools/art/green_bolt_fx.py)"}
json.dump(man, open('fx/manifest.json', 'w'), separators=(',', ':')); print(KEY, out.size, man[KEY])
