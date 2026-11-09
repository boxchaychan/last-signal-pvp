# Archer E from the owner's green bolt GIF (2026-11-09, 568x336, 36 frames at 30 ms, see-through, real soft glow; better than
# the pasted sheet whose glow came flattened into bands). Frames as they are, half size, plus a soft dark rim so it reads on grass.
#   python3 tools/art/green_bolt_gif.py  -> fx/pfx_gbolt_k.png + manifest (anchor = the burst on the right; the orb sits ~150 px left at full size)
import json
from PIL import Image, ImageSequence, ImageFilter
SRC, KEY, K = 'art/incoming/pfx/green-bolt.gif', 'pfx_gbolt_k', .5
fr = [f.convert('RGBA') for f in ImageSequence.Iterator(Image.open(SRC))]
w, h = round(fr[0].width * K), round(fr[0].height * K); out = Image.new('RGBA', (8 * w, -(-len(fr) // 8) * h))
for i, f in enumerate(fr):
    f = f.resize((w, h), Image.LANCZOS)
    a = f.split()[3].point(lambda v: 255 if v > 60 else 0).filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(2)).point(lambda v: v * .35)
    rim = Image.new('RGBA', (w, h), (2, 18, 8, 0)); rim.putalpha(a); rim.alpha_composite(f)
    out.alpha_composite(rim, (i % 8 * w, i // 8 * h))
out.save('fx/' + KEY + '.png', optimize=True)
man = json.load(open('fx/manifest.json'))
man[KEY] = {'w': w, 'h': h, 'n': len(fr), 'cols': 8, 'fps': 30, 'ax': 228, 'ay': 89, 'src': "owner's green bolt GIF (tools/art/green_bolt_gif.py)"}
json.dump(man, open('fx/manifest.json', 'w'), separators=(',', ':')); print(KEY, out.size, w, h)
