"""A drawn animation row of a character sheet (numbered frames on a flat dark panel) -> frames on one canvas, feet on one line, + a rig for rig.html
with that move as a drawn-frame clip (rig.clips) and the first frame as the standing picture (one piece, breathing by bones). Nothing is redrawn.
First used for the owner's Apollo sheet (2026-11-28, "เทส").   python3 tools/art/sheet_frames.py apollo"""
import json, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage as nd
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..')
SHEETS = {
  'apollo': dict(sheet='art/incoming/apollo/owner_sheet_raw.png', title='อพอลโล (จากแผ่นของคุณ)', move='attack2', n='ยิงธนู (เฟรมวาด)', flip=False,
    rows=[(722, 822, [60, 147, 235, 321, 408, 496, 584, 672, 755, 841, 926, 1013, 1100, 1187, 1279, 1372, 1465]),
          (862, 968, [61, 149, 239, 330, 424, 523, 618, 711, 801, 891, 992, 1080, 1176, 1258, 1338, 1416, 1483])],
    ms=1000 / 30, release=None),
}
name = sys.argv[1] if len(sys.argv) > 1 else 'apollo'; C = SHEETS[name]; OUT = os.path.join(R, 'art/rigs', name); os.makedirs(os.path.join(OUT, 'clip'), exist_ok=True)
A = np.asarray(Image.open(os.path.join(R, C['sheet'])).convert('RGB')).astype(np.float32); cells = []
for y0, y1, xs in C['rows']:
    a = A[y0:y1]; bg = np.median(a.reshape(-1, 3), 0)
    for i, x in enumerate(xs):
        l = (xs[i - 1] + x) // 2 if i else x - 46; r = (x + xs[i + 1]) // 2 if i < len(xs) - 1 else x + 46
        c = a[:, l:r]; d = np.abs(c - bg).sum(2); m = nd.binary_closing(d > 55, iterations=2); lab, n = nd.label(m)
        if not n: continue
        keep = np.zeros_like(m)
        for j, sl in enumerate(nd.find_objects(lab)):
            if (lab[sl] == j + 1).sum() > 40 and sl[0].stop > c.shape[0] * .35: keep |= lab == j + 1   # the figure + its effects; specks out
        keep = nd.binary_fill_holes(keep); al = np.clip((d - 30) / 50, 0, 1) * nd.binary_dilation(keep, iterations=1)
        ys, xx = np.nonzero(keep); cells.append((np.dstack([c, al * 255]).astype(np.uint8), ys.max(), np.median(xx[ys > ys.max() - 10])))
# line the frames up by the LEGS (lower 35 % of the figure, alpha), not by one foot column: each frame slid sideways onto the first
def legs(im, bot): al = im[..., 3].astype(np.float32) / 255; h = al.shape[0]; return al[max(0, int(bot - h * .35)):int(bot) + 1].sum(0)
ref_l = legs(cells[0][0], cells[0][1]); ref_c = np.sum(ref_l * np.arange(len(ref_l))) / ref_l.sum(); aligned = [cells[0]]
for im, bot, fx in cells[1:]:
    l = legs(im, bot); best = None
    for sh in range(-40, 41):
        x0 = int(round(ref_c - sh)); 
        a_ = np.zeros(200); b_ = np.zeros(200); a_[100 - int(ref_c):100 - int(ref_c) + len(ref_l)] = ref_l; o = 100 - x0; 
        if o < 0 or o + len(l) > 200: continue
        b_[o:o + len(l)] = l; sc = (np.minimum(a_, b_)).sum()
        if best is None or sc > best[0]: best = (sc, x0)
    aligned.append((im, bot, best[1]))
cells = [(cells[0][0], cells[0][1], ref_c)] + aligned[1:]
CW = max(c[0].shape[1] for c in cells) + 40; CH = max(c[0].shape[0] for c in cells) + 10; FOOT = CH - 6; frames = []
for i, (im, bot, fx) in enumerate(cells):
    can = Image.new('RGBA', (CW, CH), (0, 0, 0, 0)); can.alpha_composite(Image.fromarray(im, 'RGBA'), (int(CW / 2 - fx), int(FOOT - bot))); f = f'f{i:02d}.png'; can.save(os.path.join(OUT, 'clip', f)); frames.append(f)
# the standing picture = frame 1, as one piece
Image.open(os.path.join(OUT, 'clip', frames[0])).save(os.path.join(OUT, 'body.png')); b = np.asarray(Image.open(os.path.join(OUT, 'body.png')))[..., 3] > 128; ys, xs = np.nonzero(b)
fig = float(ys.max() - ys.min()); feet = [CW / 2, float(FOOT)]
rig = dict(v=2, name=name, title=C['title'], dir=f'art/rigs/{name}/', ref='body.png', size=[CW, CH], feet=feet, view='front', flip=C['flip'], figH=fig, checks=dict(throw=False),
  parts=dict(body=dict(img='body.png', n='ตัวทั้งตัว', role='body', p='', pv=[feet[0], feet[1]], at=feet, r=0, s=1)), order=['body'],
  clips={C['move']: dict(dir='clip/', frames=frames, durs=[round(C['ms'])] * len(frames), foot=feet, figH=fig, ev=[], n=C['n'])})
json.dump(rig, open(os.path.join(R, f'art/rigs/{name}.json'), 'w'), ensure_ascii=False, indent=1); print(f'art/rigs/{name}.json', len(frames), 'frames', CW, 'x', CH)
