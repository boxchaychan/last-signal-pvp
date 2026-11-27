# Pack a PixelLab character download into one sheet for quest.html ("ผู้กล้าแดนพิกเซล").
#   python tools/art/quest_sheet.py <download dir>/<State> <out name, e.g. art/quest/hero_sword> <anim=folder[,folder...]> ...
#   e.g. python tools/art/quest_sheet.py art/incoming/quest/sword/dl/Idle art/quest/hero_sword idle=idle run=run2 slash=slash2,slash2b chop=chop,chopb spin=slash1 death=death
# Rows = one per (move, direction) for south / south-east / east / north-east / north (the game mirrors the west side); a direction a move
# does not have falls back to east, then south. Every frame is put in a 96 px cell, canvas centre on cell centre (PixelLab's canvases
# share one pivot), so the feet stay on one spot: x 48, y 79. Last row = the 8 standing views. Colours: tools/art/pixel_punch.py on the
# whole sheet (one palette for every frame), glowing blade pixels kept as drawn. Writes <out>.png, <out>.json and <out>_orig.png (untouched).
import sys, os, glob, json, subprocess
import numpy as np
from PIL import Image
src, out = sys.argv[1], sys.argv[2]
moves = dict((a.split('=')[0], a.split('=')[1].split(',')) for a in sys.argv[3:] if '=' in a)
opts = dict(a[2:].split(':') for a in sys.argv[3:] if a.startswith('--'))
CELL = int(opts.get('cell', 96)); DIRS = ['south', 'south-east', 'east', 'north-east', 'north']; KEY = {'south': 'S', 'south-east': 'SE', 'east': 'E', 'north-east': 'NE', 'north': 'N'}
ALL8 = ['south', 'south-east', 'east', 'north-east', 'north', 'north-west', 'west', 'south-west']
def frames(folder, d):
    fs = sorted(glob.glob(os.path.join(src, 'animations', folder, d, 'frame_*.png'))); return [Image.open(f).convert('RGBA') for f in fs]
seen = {}
rows, meta = [], {'cell': CELL, 'ax': CELL // 2, 'ay': CELL // 2 + 31, 'anims': {}}
for mv, folders in moves.items():
    meta['anims'][mv] = {'rows': {}, 'n': 0}
    for d in DIRS:
        got = None
        for dd in (d, 'east', 'south'):   # a direction this move does not have: east, then south (the same row is shared, not copied)
            for f in folders:
                if frames(f, dd): got = (f, dd); break
            if got: break
        if not got: print('missing', mv, d); continue
        if got not in seen: seen[got] = len(rows); rows.append(frames(*got))
        meta['anims'][mv]['rows'][KEY[d]] = seen[got]; meta['anims'][mv]['n'] = max(meta['anims'][mv]['n'], len(rows[seen[got]]))
still = [Image.open(os.path.join(src, 'rotations', d + '.png')).convert('RGBA') for d in ALL8]
meta['still'] = {'row': len(rows), 'order': ['S', 'SE', 'E', 'NE', 'N', 'NW', 'W', 'SW']}; rows.append(still)
cols = max(len(r) for r in rows); sheet = Image.new('RGBA', (cols * CELL, len(rows) * CELL), (0, 0, 0, 0))
for y, r in enumerate(rows):
    for x, im in enumerate(r):
        if im.size[0] > CELL or im.size[1] > CELL: raise SystemExit('frame bigger than the cell: %s' % (im.size,))
        sheet.paste(im, (x * CELL + (CELL - im.size[0]) // 2, y * CELL + (CELL - im.size[1]) // 2))
os.makedirs(os.path.dirname(out), exist_ok=True)
sheet.save(out + '_orig.png')
subprocess.check_call([sys.executable, os.path.join(os.path.dirname(__file__), 'pixel_punch.py'), out + '_orig.png', out + '.png', opts.get('punch', '0.6'), opts.get('colours', '40')])
a = np.asarray(sheet).astype(int); b = np.asarray(Image.open(out + '.png').convert('RGBA')).astype(int).copy()
glow = (a[..., 3] > 0) & (a[..., 2] > 190) & (a[..., 1] > 150) & (a[..., 2] - a[..., 0] > 40)   # the cyan blade edge / light: kept as drawn
b[glow] = a[glow]; b[..., 3] = a[..., 3]
Image.fromarray(b.astype(np.uint8)).save(out + '.png')
meta['w'], meta['h'] = sheet.size
json.dump(meta, open(out + '.json', 'w'), separators=(',', ':'))
print(out, sheet.size, {k: (v['n'], sorted(v['rows'])) for k, v in meta['anims'].items()})
