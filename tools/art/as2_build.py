# Assassin v2 in the game (owner 2026-11-12 "ลองเอาเข้าแมพยัง"): her PixelLab side-view clips (art/incoming/action/rogue/class2/v2/)
# -> one shared cell 196x152, feet at (70, 146), facing right (the game mirrors her). The pink swooshes, white streaks and dust that
# PixMiniMax drew into the attack are removed (her outfit is dark purple / black, the swooshes are light pink-white).
#   python3 tools/art/as2_build.py -> art/action/as2/{still,run,attack,front,back}.png + as2.json
import os, json, numpy as np
from PIL import Image
from scipy import ndimage
S = 'art/incoming/action/rogue/class2/v2/'; O = 'art/action/as2/'; os.makedirs(O, exist_ok=True)
CW, CH = 196, 152
def clean(im, fx=False):
    a = np.asarray(im.convert('RGBA')).astype(int).copy()
    if fx:
        r, g, b = a[..., 0], a[..., 1], a[..., 2]; mn = a[..., :3].min(2); mx = a[..., :3].max(2)
        a[(mn > 140) & (np.abs(r - b) < 45)] = 0                                  # pink / white swooshes
        a[(mx - mn < 26) & (mx > 95) & (mx < 200) & (a[..., 3] > 0) & (np.mgrid[0:a.shape[0], 0:a.shape[1]][1] > 100)] = 0   # grey smoke ahead of her
        a[(np.mgrid[0:a.shape[0], 0:a.shape[1]][0] > 138) & (r > 150) & (g > 120) & (b < 150) & (r - b > 30)] = 0   # beige dust at the feet
    m = a[..., 3] > 0; lab, n = ndimage.label(m, structure=np.ones((3, 3)))
    if n > 1:
        sz = ndimage.sum(m, lab, range(1, n + 1))
        for i, s in enumerate(sz):
            if s < 30: a[lab == i + 1] = 0
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))
def row(frames, fx=False):
    out = Image.new('RGBA', (CW * len(frames), CH))
    for i, f in enumerate(frames): out.alpha_composite(clean(Image.open(f), fx), (i * CW, 0))
    return out
CL = {'run': ([S + 'test_run/f%02d.png' % i for i in range(3, 17)], False),
      'attack': ([S + 'test_attack/f%02d.png' % i for i in (1, 3, 4, 5, 9, 10, 11, 12, 13)], True),
      'still': ([S + 'start_run.png'], False), 'front': ([S + 'front.png'], False), 'back': ([S + 'back.png'], False)}
meta = {'cw': CW, 'ch': CH, 'fx': 70, 'fy': 146, 'n': {}, 'hits': {'attack': [1, 5]}}
for k, (fs, fx) in CL.items():
    row(fs, fx).save(O + k + '.png'); meta['n'][k] = len(fs)
json.dump(meta, open(O + 'as2.json', 'w')); print(meta)
