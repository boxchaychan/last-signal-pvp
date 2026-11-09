# Swordsman E in the owner's own colours (2026-11-09 "ใส่พายุแดงที่ให้ไป", after the black + orange copy did not work for them):
# the pasted 9 x 8 sheet as it is, black background -> see-through, the flat red / yellow / orange / pink glow bands kept but
# half see-through so the tornado inside shows, the textured tornado and smoke fully opaque; half size.
#   python3 tools/art/sword_storm_red.py  -> fx/pfx_swstorm_r.png + manifest
import json
import numpy as np
from PIL import Image
from scipy import ndimage
SRC, KEY, C, R, K = 'art/incoming/pfx/sword-storm-sheet.png', 'pfx_swstorm_r', 9, 8, .5
a = np.array(Image.open(SRC).convert('RGB')).astype(float); H, W = a.shape[:2]; cw, ch = W / C, H / R
ow, oh = round(cw * K), round(ch * K); out = Image.new('RGBA', (8 * ow, -(-C * R // 8) * oh))
for i in range(C * R):
    x0, y0 = round(i % C * cw), round(i // C * ch); q = a[y0:y0 + round(ch), x0:x0 + round(cw)]
    band = np.zeros(q.shape[:2], bool)
    for col in ([255, 255, 0], [255, 0, 0], [255, 130, 0], [255, 130, 130], [255, 255, 255], [255, 255, 130]):
        band |= np.abs(q - col).max(-1) < 34
    bg = q.max(-1) < 18; bg = ndimage.binary_opening(bg, iterations=1)
    al = np.where(bg, 0, np.where(band, 150, 255)).astype(np.uint8)
    t = Image.fromarray(np.dstack([q.astype(np.uint8), al])).resize((ow, oh), Image.LANCZOS)
    out.alpha_composite(t, (i % 8 * ow, i // 8 * oh))
out.save('fx/' + KEY + '.png', optimize=True)
man = json.load(open('fx/manifest.json'))
man[KEY] = {'w': ow, 'h': oh, 'n': C * R, 'cols': 8, 'fps': 30, 'ax': ow // 2, 'ay': round(oh * .78), 'src': "owner's pasted sword storm sheet, own colours (tools/art/sword_storm_red.py)"}
json.dump(man, open('fx/manifest.json', 'w'), separators=(',', ':')); print(KEY, out.size)
