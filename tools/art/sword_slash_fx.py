# Swordsman normal combo (owner 2026-11-09 "ท่าฟันเอาให้เข้ากับฟันธรรมดา"): the pasted 6 x 5 sheet of three orange crescent slashes
# (frames 0-9, 10-17, 18-29) came with its glow flattened into solid red / yellow / white / pink / orange bands. Kept: the
# textured parts (local variation) away from the flat bands, the bright crescent stroke and the dark debris; a soft orange glow.
#   python3 tools/art/sword_slash_fx.py  -> fx/pfx_swslash.png + manifest
import json
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage
SRC, KEY, C, R, K = 'art/incoming/pfx/sword-slash-sheet.png', 'pfx_swslash', 6, 5, .5
a = np.array(Image.open(SRC).convert('RGB')).astype(float); H, W = a.shape[:2]; cw, ch = W / C, H / R
ow, oh = round(cw * K), round(ch * K); out = Image.new('RGBA', (8 * ow, -(-C * R // 8) * oh))
BANDS = ([255, 255, 0], [255, 0, 0], [255, 255, 255], [255, 130, 130], [255, 160, 64], [255, 200, 120], [255, 255, 130], [255, 130, 0])
for i in range(C * R):
    x0, y0 = round(i % C * cw), round(i // C * ch); q = a[y0:y0 + round(ch), x0:x0 + round(cw)]
    sd = 0
    for c in range(3):
        u = ndimage.uniform_filter(q[..., c], 5); sd = sd + np.sqrt(np.maximum(0, ndimage.uniform_filter(q[..., c] ** 2, 5) - u * u))
    flat = sd < 14
    band = np.zeros(q.shape[:2], bool)
    for col in BANDS: band |= np.abs(q - col).max(-1) < 30
    stroke = (q.min(-1) > 225) & ~ndimage.binary_opening(q.min(-1) > 225, iterations=4)     # thin bright crescent, not white floods
    keep = ((~flat & ~ndimage.binary_dilation(band & flat, iterations=2)) | stroke) & (q.max(-1) > 40)
    keep = ndimage.binary_opening(keep, iterations=1); lab, n = ndimage.label(keep)
    if n: sz = ndimage.sum(keep, lab, range(1, n + 1)); keep = np.isin(lab, 1 + np.nonzero(sz >= 12)[0])
    strong = stroke | (keep & (q.max(-1) < 170))        # the crescent stroke and the dark debris at full; the band seams faint
    al = np.where(strong, 255, np.where(keep, 90, 0)).astype(np.uint8)
    rgba = np.dstack([q.astype(np.uint8), al])
    t = Image.fromarray(rgba).resize((ow, oh), Image.LANCZOS)
    g = Image.new('RGBA', (ow, oh), (255, 140, 40, 0)); g.putalpha(t.split()[3].filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(5)).point(lambda v: v * .55))
    g.alpha_composite(t); out.alpha_composite(g, (i % 8 * ow, i // 8 * oh))
out.save('fx/' + KEY + '.png', optimize=True)
man = json.load(open('fx/manifest.json'))
man[KEY] = {'w': ow, 'h': oh, 'n': C * R, 'cols': 8, 'fps': 30, 'ax': ow // 2, 'ay': oh // 2, 'src': "owner's pasted orange slash sheet (tools/art/sword_slash_fx.py)"}
json.dump(man, open('fx/manifest.json', 'w'), separators=(',', ':')); print(KEY, out.size, ow, oh)
