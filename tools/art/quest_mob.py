# Pack one PixelLab object (monster: one facing, right) with its clips into a sheet for quest.html.
#   python tools/art/quest_mob.py <unzipped object dir> <out name, e.g. art/quest/mob_mush> walk=<folder prefix> attack=<folder prefix> [extra=<prefix> ...]
# Rows in the order given; cell = the biggest frame, frames centred (PixelLab keeps one pivot); feet anchor = bottom of the standing
# sprite, x = middle of its lowest rows. Colours: tools/art/pixel_punch.py on the whole sheet; <out>_orig.png = untouched.
import sys, os, glob, json, subprocess
import numpy as np
from PIL import Image
src, out = sys.argv[1], sys.argv[2]; moves = [a.split('=') for a in sys.argv[3:] if '=' in a and not a.startswith('--')]
opts = dict(a[2:].split(':') for a in sys.argv[3:] if a.startswith('--'))
rows = []; meta = {'anims': {}}
for name, pre in moves:
    d = [p for p in sorted(glob.glob(os.path.join(src, 'animations', '*'))) if os.path.basename(p).startswith(pre)]
    if not d: raise SystemExit('no clip starting with ' + pre)
    fr = [Image.open(f).convert('RGBA') for f in sorted(glob.glob(os.path.join(d[0], '*', 'frame_*.png')))]
    meta['anims'][name] = {'row': len(rows), 'n': len(fr)}; rows.append(fr)
cw = max(i.size[0] for r in rows for i in r); ch = max(i.size[1] for r in rows for i in r); cols = max(len(r) for r in rows)
sheet = Image.new('RGBA', (cols * cw, len(rows) * ch), (0, 0, 0, 0))
for y, r in enumerate(rows):
    for x, im in enumerate(r): sheet.paste(im, (x * cw + (cw - im.size[0]) // 2, y * ch + (ch - im.size[1]) // 2))
base = rows[0][0]; a = np.asarray(base)[..., 3] > 0; ys, xs = np.where(a); bot = ys.max(); low = xs[ys >= bot - 3]
ox, oy = (cw - base.size[0]) // 2, (ch - base.size[1]) // 2
meta.update({'cw': cw, 'ch': ch, 'ax': int(round((low.min() + low.max() + 1) / 2)) + ox, 'ay': int(bot) + 1 + oy, 'top': int(ys.min()) + oy, 'bw': int(xs.max() - xs.min() + 1), 'w': sheet.size[0], 'h': sheet.size[1]})
os.makedirs(os.path.dirname(out), exist_ok=True); sheet.save(out + '_orig.png')
subprocess.check_call([sys.executable, os.path.join(os.path.dirname(__file__), 'pixel_punch.py'), out + '_orig.png', out + '.png', opts.get('punch', '0.6'), opts.get('colours', '32')])
b = np.asarray(Image.open(out + '.png').convert('RGBA')).copy(); b[..., 3] = np.asarray(sheet)[..., 3]; Image.fromarray(b).save(out + '.png')
json.dump(meta, open(out + '.json', 'w'), separators=(',', ':')); print(out, sheet.size, meta)
