# Tribe game (fort-design.md v3) sprites -> art/tribe/: character sheets from the PixelLab zips (art/incoming/tribe/<name>/zip),
# the 5 village objects and the map-1 monsters we already had. Untouched copies in art/tribe/orig/, game copies colour-punched
# (owner's pixel recipe, tools/art/pixel_punch.py).
import json, os, glob, shutil, subprocess
from PIL import Image
OUT = 'art/tribe'; DIRS = ['south', 'east', 'north', 'west']
def punch(src, dst, n=24): subprocess.run(['python3', 'tools/art/pixel_punch.py', src, dst, '1.0', str(n)], check=True)
meta = {}
for ch, anims in (('villager', ['walking', 'cross_punch_attack', 'picking_up']), ('champion', ['walking', 'cross_punch_attack'])):
    base = f'art/incoming/tribe/{ch}/zip/Idle'
    rows = [[Image.open(f'{base}/rotations/{d}.png').convert('RGBA')] for d in DIRS]; info = {'idle': {'row': 0, 'n': 1}}
    for a in anims:
        info[{'walking': 'walk', 'cross_punch_attack': 'attack', 'picking_up': 'work'}[a]] = {'row': len(rows), 'n': len(glob.glob(f'{base}/animations/{a}/south/*.png'))}
        for d in DIRS: rows.append([Image.open(f) .convert('RGBA') for f in sorted(glob.glob(f'{base}/animations/{a}/{d}/*.png'))])
    cw, chh = rows[0][0].size; ncol = max(len(r) for r in rows)
    sheet = Image.new('RGBA', (cw * ncol, chh * len(rows)), (0, 0, 0, 0))
    for y, r in enumerate(rows):
        for x, im in enumerate(r): sheet.alpha_composite(im, (x * cw, y * chh))
    bb = rows[0][0].getbbox()   # south idle: feet = bottom of the sprite, centre = middle of the canvas
    sheet.save(f'{OUT}/orig/{ch}.png'); punch(f'{OUT}/orig/{ch}.png', f'{OUT}/{ch}.png')
    meta[ch] = {'cw': cw, 'ch': chh, 'feet': [cw // 2, bb[3]], 'anims': info}
for o in ('hut', 'fire', 'fence', 'tower', 'berry'):
    shutil.copy(f'art/incoming/tribe/obj_{o}.png', f'{OUT}/orig/{o}.png'); punch(f'{OUT}/orig/{o}.png', f'{OUT}/{o}.png')
    im = Image.open(f'{OUT}/{o}.png'); bb = im.getbbox(); meta[o] = {'w': im.width, 'h': im.height, 'base': bb[3]}
mj = json.load(open('art/td/map1/map.json'))['mobs']
for m in ('wolf', 'boar_guard', 'golem', 'skeleton', 'goblin_archer'):
    shutil.copy(f'art/td/map1/mob_{m}.png', f'{OUT}/orig/mob_{m}.png'); punch(f'{OUT}/orig/mob_{m}.png', f'{OUT}/mob_{m}.png')
    meta['mob_' + m] = mj[m]
json.dump(meta, open(f'{OUT}/sprites.json', 'w'), indent=1)
print(json.dumps({k: (v['anims'] if 'anims' in v else v) for k, v in meta.items()})[:900])
