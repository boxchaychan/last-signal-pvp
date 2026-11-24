#!/usr/bin/env python3
"""clash.html: join the PixelLab move frames (art/incoming/clash/anim/<key>_<move>/f*.png, from tools/art/clash_anim.py) into one
sheet per unit: row 0 = attack (13 cells, cell 0 = our still = idle), row 1 = walk / flight loop (8 cells) when there is one.
Walk frames are lined up on the still (same body centre; ground walkers also keep the feet on the same row) so the loop does not slide.
Raw sheet -> art/clash/orig/anim_<key>.png, colour recipe (pixel_punch 0.35, 48 colours, one palette for the whole sheet) ->
art/clash/anim/<key>.png; cell size, foot point and frame counts go into art/clash/units.json ("anim").
Run: python3 tools/art/clash_sheet.py [key ...]   (free; no keys = every unit; commanders use a bigger canvas, read from the frames: 68 -> foot 64, 132 -> foot 126)"""
import glob, json, os, subprocess, sys
import numpy as np
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
IN = os.path.join(ROOT, 'art/incoming/clash/anim'); C, FOOT = 68, 64; FLY = {'d_imp', 'g_angel', 'ax_saucer', 'an_thunder', 'an_phoenix', 'gd_seraph', 'gd_healer', 'gd_pegasus', 'mc_core'}   # flyers keep their own up / down in the loop
meta = json.load(open(os.path.join(ROOT, 'art/clash/units.json')))
def bbox(im):
    a = np.asarray(im)[..., 3] > 127; ys, xs = np.nonzero(a); return (xs.min(), ys.min(), xs.max(), ys.max()) if len(xs) else None
ONLY = set(sys.argv[1:]); FOOTS = {68: 64, 132: 126}
for k, m in meta.items():
    if ONLY and k not in ONLY: continue
    atk = sorted(glob.glob(os.path.join(IN, f'{k}_attack', 'f*.png'))); wk = sorted(glob.glob(os.path.join(IN, f'{k}_walk', 'f*.png')))[1:]
    if not atk: continue
    A = [Image.open(f).convert('RGBA') for f in atk]; Wf = [Image.open(f).convert('RGBA') for f in wk]; C = A[0].width; FOOT = FOOTS.get(C, C - 4)
    b0 = bbox(A[0]); cx0 = (b0[0] + b0[2]) // 2
    al = []
    for im in Wf:
        b = bbox(im); dx = cx0 - (b[0] + b[2]) // 2; dy = 0 if k in FLY else b0[3] - b[3]
        c = Image.new('RGBA', (C, C)); c.paste(im, (dx, dy), im); al.append(c)
    rows = 2 if al else 1; S = Image.new('RGBA', (C * len(A), C * rows))
    for i, im in enumerate(A): S.paste(im, (i * C, 0), im)
    for i, im in enumerate(al): S.paste(im, (i * C, C), im)
    a = np.asarray(S).copy(); a[..., 3] = np.where(a[..., 3] > 127, 255, 0); S = Image.fromarray(a)
    raw = os.path.join(ROOT, 'art/clash/orig', f'anim_{k}.png'); out = os.path.join(ROOT, 'art/clash/anim', f'{k}.png'); S.save(raw)
    subprocess.run([sys.executable, os.path.join(ROOT, 'tools/art/pixel_punch.py'), raw, out, '0.35', '48'], check=True)
    x = max(2, min(C - m['w'] - 2, round(C * .44) - m['w'] // 2))   # where clash_anim.py prep put the still
    m['anim'] = {'cw': C, 'ch': C, 'fx': x + m['w'] // 2, 'fy': FOOT, 'atk': len(A), 'walk': len(al)}
    print(k, 'attack', len(A), 'walk', len(al))
json.dump(meta, open(os.path.join(ROOT, 'art/clash/units.json'), 'w'), indent=1)
