# A ParticleFX-style sheet the owner pasted into the chat (one picture, frames in a grid, see-through background, often
# scaled so the cells are not whole pixels) -> a clean sheet in fx/ with whole-pixel cells + its fx/manifest.json entry.
#   python tools/art/pfx_paste.py <sheet> <key> <cols> <rows> <first> <last> <ax> <ay> [cell w] [cell h] [fps=30] [src note]
#   ax ay = the anchor inside a cell (where the effect sits in the game: the bow, the ground under the bomb)
#   e.g. python tools/art/pfx_paste.py art/incoming/pfx/charge-shot-sheet.webp pfx_chargeshot 7 6 0 38 70 68
import json, sys
from PIL import Image

src, key = sys.argv[1], sys.argv[2]
cols, rows, f0, f1 = (int(v) for v in sys.argv[3:7])
ax, ay = float(sys.argv[7]), float(sys.argv[8])
im = Image.open(src).convert('RGBA'); W, H = im.size; pw, ph = W / cols, H / rows
cw = int(sys.argv[9]) if len(sys.argv) > 9 else int(pw + .999); chh = int(sys.argv[10]) if len(sys.argv) > 10 else int(ph + .999)
fps = int(sys.argv[11]) if len(sys.argv) > 11 else 30; note = sys.argv[12] if len(sys.argv) > 12 else src.split('/')[-1]
n = f1 - f0 + 1; oc = min(n, 8); out = Image.new('RGBA', (oc * cw, -(-n // oc) * chh))
for j, i in enumerate(range(f0, f1 + 1)):
    x0, y0 = round(i % cols * pw), round(i // cols * ph)
    out.alpha_composite(im.crop((x0, y0, x0 + cw, y0 + chh)), (j % oc * cw, j // oc * chh))
out.save('fx/' + key + '.png', optimize=True)
man = json.load(open('fx/manifest.json'))
man[key] = {'w': cw, 'h': chh, 'n': n, 'cols': oc, 'fps': fps, 'ax': round(ax), 'ay': round(ay), 'src': f'{note} frames {f0}-{f1} (tools/art/pfx_paste.py)'}
json.dump(man, open('fx/manifest.json', 'w'), separators=(',', ':')); print(key, out.size, man[key])
