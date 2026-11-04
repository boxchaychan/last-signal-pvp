#!/usr/bin/env python3
"""Bring an effect from PixelLab VFX Creator (the owner's zip: one folder per direction, each with whole/behind/front
sheets + manifest.json) into the game's fx/ folder as one sheet + an fx/manifest.json entry.

  python3 -I tools/art/pixellab_import.py <unzipped pack> <key> [dir=south] [clip=whole] [frames=a-b] [crop=x0,y0,x1,y1] [anchor=x,y] [fps=N]

dir    folder to take (the camera looks straight down, so a round effect looks the same in every folder)
frames keep only frames a..b (0-based, inclusive), e.g. to split a projectile clip into charge / flight / hit
crop   box inside each frame (frame pixels); the anchor (the "feet" point) moves with it
anchor own anchor in frame pixels (before crop), e.g. the head of a flying bolt
The anchor is the pack's own: frame pixel (-offset.x, -offset.y). drawFx places that point at the effect's x, y.
Run Python with -I on the owner's files (untrusted folder).
"""
import sys, json, os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def main(a):
    pack, key = a[0], a[1]
    opt = dict(s.split('=', 1) for s in a[2:])
    d = opt.get('dir', 'south')
    m = json.load(open(os.path.join(pack, d, 'manifest.json')))
    clip = [c for c in m['clips'] if c['name'] == opt.get('clip', 'whole')][0]
    W, H = clip['frame']['w'], clip['frame']['h']
    frames = []
    for sh in clip['sheets']:
        im = Image.open(os.path.join(pack, d, sh['file'])).convert('RGBA')
        for i in range(sh['frames']):
            c, r = i % sh['columns'], i // sh['columns']
            frames.append(im.crop((c * W, r * H, c * W + W, r * H + H)))
    ax, ay = -clip['offset']['x'], -clip['offset']['y']
    if 'anchor' in opt:
        ax, ay = map(int, opt['anchor'].split(','))
    if 'frames' in opt:
        f0, f1 = map(int, opt['frames'].split('-'))
        frames = frames[f0:f1 + 1]
    if 'crop' in opt:
        x0, y0, x1, y1 = map(int, opt['crop'].split(','))
        frames = [f.crop((x0, y0, x1, y1)) for f in frames]
        ax, ay, W, H = ax - x0, ay - y0, x1 - x0, y1 - y0
    n = len(frames)
    cols = min(n, 8)
    rows = (n + cols - 1) // cols
    out = Image.new('RGBA', (W * cols, H * rows), (0, 0, 0, 0))
    for i, f in enumerate(frames):
        out.paste(f, ((i % cols) * W, (i // cols) * H))
    out.save(os.path.join(ROOT, 'fx', key + '.png'), optimize=True)
    mp = os.path.join(ROOT, 'fx', 'manifest.json')
    man = json.load(open(mp))
    man[key] = {'w': W, 'h': H, 'fps': int(opt.get('fps', m['fps'])), 'n': n, 'cols': cols, 'ax': ax, 'ay': ay,
                'src': 'owner, PixelLab VFX Creator "' + m['name'] + '" ' + ' '.join(s for s in a[2:])}
    json.dump(man, open(mp, 'w'), ensure_ascii=False, separators=(',', ':'))
    print(key, man[key])


if __name__ == '__main__':
    main(sys.argv[1:])
