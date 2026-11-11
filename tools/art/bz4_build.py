# Berserker v4 test moves (owner 2026-11-11 "เอามา 1 ทิศก่อน"): the PixelLab side-view clips in art/incoming/action/berserker/v4_cool
# (test_sweep 240x160, test_vert 224x240, test_spin 256x176) -> one shared cell, side view facing right (the game mirrors it).
# Each clip keeps its canvas anchor (the feet of its first frame), so steps forward stay in the art.
# Outline style B: the pale rim left from GPT's white background is removed, the black outline stays.
# PixelLab's own swooshes: blue + white dust in the vertical slash are stripped; the sweep's white swoosh frame (3) is skipped.
#   python3 tools/art/bz4_build.py   -> art/action/bz4/{still,sweep,vert,spin}.png + bz4.json
import os, json, numpy as np
from PIL import Image
from scipy import ndimage
SRC = 'art/incoming/action/berserker/v4_cool/'; OUT = 'art/action/bz4/'; os.makedirs(OUT, exist_ok=True)
# clip: folder, feet point of the canvas, frames used, hit frames (index into the used list)
CLIPS = {
    'sweep': ('test_sweep', (72, 154), [1, 2, 4, 5, 6, 8, 10, 12, 13, 14, 15, 16], [2]),
    'vert':  ('test_vert', (72, 234), [1, 2, 3, 4, 6, 7, 9, 11, 13, 14, 15, 16], [4]),
    'spin':  ('test_spin', (128, 170), list(range(1, 25)), [4, 10, 16]),
    'run':   ('test_run', (72, 146), list(range(4, 17)), []),   # 1-3 = starting from the stance, 4-16 loop
}

def clean(im, strip=False):
    a = np.asarray(im.convert('RGBA')).astype(int).copy()
    if strip:   # PixelLab's blue swoosh and white dust (he has no blue and no near-white)
        r, g, b = a[..., 0], a[..., 1], a[..., 2]
        a[((b > r + 30) & (b > g + 20)) | (a[..., :3].min(2) > 215)] = 0
    for _ in range(2):   # pale rim on the outside edge (style B)
        m = a[..., 3] > 0; e = m & ~ndimage.binary_erosion(m); a[e & (a[..., :3].min(2) > 110)] = 0
    m = a[..., 3] > 0; lab, n = ndimage.label(m, structure=np.ones((3, 3)))   # drop loose specks
    if n > 1:
        sz = ndimage.sum(m, lab, range(1, n + 1))
        for i, s in enumerate(sz):
            if s < 12: a[lab == i + 1] = 0
    return Image.fromarray(a.astype(np.uint8))

L = max(fx for _, (fx, fy), _, _ in CLIPS.values()); T = max(fy for _, (fx, fy), _, _ in CLIPS.values())
R = 0
for k, (d, (fx, fy), fr, _) in CLIPS.items():
    w = Image.open(SRC + d + '/f00.png').width; R = max(R, w - fx)
cw, ch = L + R, T + 6
meta = {'cw': cw, 'ch': ch, 'fx': L, 'fy': T, 'n': {}, 'hits': {}}
for k, (d, (fx, fy), fr, hits) in CLIPS.items():
    row = Image.new('RGBA', (cw * len(fr), ch))
    for i, f in enumerate(fr):
        im = clean(Image.open(SRC + d + '/f%02d.png' % f), strip=(k == 'vert'))
        row.alpha_composite(im, (i * cw + L - fx, T - fy))
    row.save(OUT + k + '.png'); meta['n'][k] = len(fr); meta['hits'][k] = hits
st = Image.new('RGBA', (cw, ch)); st.alpha_composite(clean(Image.open(SRC + 'test_sweep/f00.png')), (L - 72, T - 154)); st.save(OUT + 'still.png')
json.dump(meta, open(OUT + 'bz4.json', 'w'))
print(meta)
