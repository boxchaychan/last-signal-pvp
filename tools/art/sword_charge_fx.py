# (only the grey smoke + rocks survive the cut; the game adds its own red flash, ring and sparks)
# Swordsman R (owner 2026-11-09 "ปรับสีให้เข้าโทน ละเอาไว้ท่าชาร์จ"): the pasted 6 x 6 sheet (a streak strikes down, a starburst, a
# ground ring, rocks and grey smoke) came with its glow flattened into solid white / pink / red / yellow bands. Kept: textured parts
# away from the flat bands, the smoke, the rocks; the bright parts pushed to his red-orange tone; a soft orange glow.
#   python3 tools/art/sword_charge_fx.py  -> fx/pfx_swcharge.png + manifest (anchor = the impact on the ground)
import json
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage
SRC, KEY, C, R, K = 'art/incoming/pfx/sword-charge-sheet.png', 'pfx_swcharge', 6, 5, .5
a = np.array(Image.open(SRC).convert('RGB')).astype(float); H, W = a.shape[:2]; cw, ch = W / C, H / R
ow, oh = round(cw * K), round(ch * K); out = Image.new('RGBA', (8 * ow, -(-C * R // 8) * oh))
BANDS = ([255, 255, 255], [255, 128, 128], [255, 0, 0], [255, 255, 0], [255, 200, 200], [255, 170, 170], [0, 255, 255], [255, 255, 160])
for i in range(C * R):
    x0, y0 = round(i % C * cw), round(i // C * ch); q = a[y0:y0 + round(ch), x0:x0 + round(cw)]
    sd = 0
    for c in range(3):
        u = ndimage.uniform_filter(q[..., c], 5); sd = sd + np.sqrt(np.maximum(0, ndimage.uniform_filter(q[..., c] ** 2, 5) - u * u))
    band = np.zeros(q.shape[:2], bool)
    for col in BANDS: band |= np.abs(q - col).max(-1) < 30
    keep = np.zeros(q.shape[:2], bool)   # the band seams read as stripes: only the smoke and rocks are kept, the flash and ring are drawn by the game
    grey = (np.abs(q[..., 0] - q[..., 2]) < 30) & (q.max(-1) > 60) & (q.max(-1) < 235)           # smoke and rocks
    keep |= grey & (sd > 4)
    keep = ndimage.binary_opening(keep, iterations=1); lab, n = ndimage.label(keep)
    if n: sz = ndimage.sum(keep, lab, range(1, n + 1)); keep = np.isin(lab, 1 + np.nonzero(sz >= 14)[0])
    rgb = q.copy(); warm = keep & ~grey                                                              # bright bits -> red / orange / gold
    v = rgb[warm].max(-1) / 255; rgb[warm] = np.stack([255 * np.ones_like(v), 70 + 150 * v ** 2, 30 + 90 * v ** 4], -1)
    al = np.where(keep & grey, 230, np.where(keep, 255, 0)).astype(np.uint8)
    t = Image.fromarray(np.dstack([rgb.clip(0, 255).astype(np.uint8), al])).resize((ow, oh), Image.LANCZOS)
    g = Image.new('RGBA', (ow, oh), (255, 90, 30, 0)); g.putalpha(t.split()[3].filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(6)).point(lambda v: v * .45))
    g.alpha_composite(t); out.alpha_composite(g, (i % 8 * ow, i // 8 * oh))
out.save('fx/' + KEY + '.png', optimize=True)
man = json.load(open('fx/manifest.json'))
man[KEY] = {'w': ow, 'h': oh, 'n': C * R, 'cols': 8, 'fps': 30, 'ax': ow // 2, 'ay': round(oh * .55), 'src': "owner's pasted strike sheet, swordsman tone (tools/art/sword_charge_fx.py)"}
json.dump(man, open('fx/manifest.json', 'w'), separators=(',', ':')); print(KEY, out.size, ow, oh)
