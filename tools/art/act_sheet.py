# PixelLab character download (unzipped) -> one sprite sheet + json for action.html (owner 2026-11-08, dagger rogue).
#   python3 tools/art/act_sheet.py <unzipped dir>/<state> <out.png> <anim>=<folder> [<anim>=<folder> ...]
#   e.g. python3 tools/art/act_sheet.py art/incoming/action/rogue/pl_dl/Idle art/action/rogue.png attack=attack_2hit_b
# Row 0 = the 8 still rotations (padded to the animation cell, PixelLab centres a 128 still inside its 172 frames, +22 px).
# Then one row per animation per direction, in DIRS order (east, south-east, south, ... clockwise on screen). A direction
# the download does not have yet is left empty and listed as missing; the game falls back to a mirrored / nearby one.
import sys, os, glob, json
from PIL import Image

src, out = sys.argv[1], sys.argv[2]
# --hits=<dir>:<f>,<f>[;<dir>:...] sets a direction's hit frames by hand when the width rule misses one
FIX = {}
for a in sys.argv[3:]:
    if a.startswith('--hits='):
        for part in a[7:].split(';'):
            d, fs = part.split(':'); FIX[d] = [int(f) for f in fs.split(',')]
# --skip=<dir>,<dir> leaves those directions empty so the game mirrors the opposite side instead (a bad run)
SKIP = set(sum([a[7:].split(',') for a in sys.argv[3:] if a.startswith('--skip=')], []))
# --alias=<dir>:<from dir>[~],... plays another direction's frames instead (~ = mirrored), e.g. the clean east clip
ALIAS = {}
for a in sys.argv[3:]:
    if a.startswith('--alias='):
        for part in a[8:].split(','):
            d, f = part.split(':'); ALIAS[d] = (f.rstrip('~'), f.endswith('~')); SKIP.add(d)
anims = [a.split('=') for a in sys.argv[3:] if not a.startswith('--')]
DIRS = ['east', 'south-east', 'south', 'south-west', 'west', 'north-west', 'north', 'north-east']
rows = []  # (name, dir, [frames])
rot = [Image.open(os.path.join(src, 'rotations', d + '.png')).convert('RGBA') for d in DIRS]
C = rot[0].width
for name, folder in anims:
    for d in DIRS:
        fs = []
        for f in folder.split(','):   # attack=a,b: a redo in folder b replaces folder a for the directions b has
            fs = sorted(glob.glob(os.path.join(src, 'animations', f, d, 'frame_*.png'))) or fs
        if d in SKIP: fs = []
        fr = [Image.open(f).convert('RGBA') for f in fs]
        if fr: C = max(C, fr[0].width)
        rows.append((name, d, fr))
cols = max([8] + [len(r[2]) for r in rows])
sheet = Image.new('RGBA', (cols * C, (1 + len(rows)) * C))
pad = (C - rot[0].width) // 2
for i, im in enumerate(rot): sheet.alpha_composite(im, (i * C + pad, pad))
meta = {'cell': C, 'fx': C // 2, 'fy': pad + 125 if rot[0].height == 128 else C - 25, 'dirs': DIRS, 'idle': 0, 'anims': {}}
def hits(fr):
    # swing frames: PixelLab draws a blade smear there, so the figure is widest; a hit = a local maximum of the
    # width that is at least 1.25x the median width (checked on the rogue's 5 directions 2026-11-08)
    w = []
    for im in fr:
        bb = im.getbbox(); w.append(bb[2] - bb[0] if bb else 0)
    med = sorted(w)[len(w) // 2]
    return [i for i in range(1, len(w) - 1) if w[i] >= 1.25 * med and w[i] >= w[i - 1] and w[i] >= w[i + 1] and (w[i] > w[i - 1] or w[i] > w[i + 1])]

for j, (name, d, fr) in enumerate(rows):
    o = (C - fr[0].width) // 2 if fr else 0
    for i, im in enumerate(fr): sheet.alpha_composite(im, (i * C + o, (1 + j) * C + o))
    meta['anims'].setdefault(name, {})[d] = {'r': 1 + j, 'n': len(fr), 'hits': FIX.get(d) or hits(fr)} if fr else None
for name in meta['anims']:
    for d, (f, mir) in ALIAS.items():
        v = meta['anims'][name].get(f)
        if v: meta['anims'][name][d] = dict(v, flip=mir, alias=f)
os.makedirs(os.path.dirname(out) or '.', exist_ok=True)
sheet.save(out, optimize=True)
json.dump(meta, open(os.path.splitext(out)[0] + '.json', 'w'), indent=1)
have = {n: [d for d, v in a.items() if v] for n, a in meta['anims'].items()}
print(sheet.size, 'cell', C, 'feet', meta['fx'], meta['fy'], have)
