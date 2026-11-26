"""Cut the Codex hills kit (art/incoming/dune_hills/, magenta background, PR #822) into art/dune/env/ for dune.html's stepped hills.

  python tools/art/dune_hills_cut.py

hill_face  -> hill_face.webp   (tiling cliff wall; "top" = the row of the walkable sand surface)
hill_caps  -> hill_cap_l.webp, hill_cap_r.webp (rounded ends; same "top")
hill_props -> hp_hang, hp_rocks, hp_skull, hp_pillar, hp_crystal, hp_banner, hp_cactus (.webp)
bg_mesas   -> mesas.webp (a background layer between far and mid)
Adds them to art/dune/world.json (w, h, top). Raise BUILD in dune.html afterwards.
"""
import json
import numpy as np, cv2
from PIL import Image

IN, OUT = 'art/incoming/dune_hills/', 'art/dune/env/'
def unmagenta(a):
    r, g, b = [a[..., i].astype(int) for i in range(3)]; m = (r > 180) & (b > 180) & (g < 110) & (np.abs(r - b) < 90)   # flat #FF00FF and its soft edge
    al = np.where(m, 0, 255).astype(np.uint8); al = cv2.erode(al, np.ones((2, 2), np.uint8)); al = cv2.GaussianBlur(al, (0, 0), .6)
    rgb = a[..., :3].copy(); edge = (al > 0) & (al < 250); rgb[edge] = np.minimum(rgb[edge], [235, 150, 120])   # no pink fringe
    return np.dstack([rgb, al])
def top_row(al, frac=.88):   # first row where the picture is solid across most of its width = the walkable surface
    cov = (al > 128).mean(1); return int(np.argmax(cov > frac))
def save(name, a, extra=None):
    Image.fromarray(a, 'RGBA').save(OUT + name + '.webp', 'WEBP', quality=88, alpha_quality=90, method=6); d = {'w': a.shape[1], 'h': a.shape[0]}; d.update(extra or {}); W[name] = d; print(name, d)
W = json.load(open('art/dune/world.json'))
a = unmagenta(np.array(Image.open(IN + 'hill_face.png').convert('RGB'))); ys = np.where((a[..., 3] > 128).any(1))[0]; a = a[ys.min():]; save('hill_face', a, {'top': top_row(a[..., 3], .97)})
a = unmagenta(np.array(Image.open(IN + 'hill_caps.png').convert('RGB'))); n, lab, st, _ = cv2.connectedComponentsWithStats((a[..., 3] > 128).astype(np.uint8), 8)
big = sorted([i for i in range(1, n) if st[i, 4] > 20000], key=lambda i: st[i, 0])
for name, i in zip(['hill_cap_l', 'hill_cap_r'], big):
    x, y, w, h = st[i, :4]; c = a[y:y + h, x:x + w].copy(); c[..., 3] = np.where(lab[y:y + h, x:x + w] == i, c[..., 3], 0); save(name, c, {'top': top_row(c[..., 3], .8)})
a = unmagenta(np.array(Image.open(IN + 'hill_props.png').convert('RGB'))); m = cv2.dilate((a[..., 3] > 128).astype(np.uint8), np.ones((15, 15), np.uint8)); n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
parts = sorted([i for i in range(1, n) if st[i, 4] > 3000], key=lambda i: (st[i, 1] // 300, st[i, 0]))
for name, i in zip(['hp_hang', 'hp_rocks', 'hp_skull', 'hp_pillar', 'hp_crystal', 'hp_banner', 'hp_cactus'], parts):
    x, y, w, h = st[i, :4]; c = a[y:y + h, x:x + w].copy(); c[..., 3] = np.where(lab[y:y + h, x:x + w] == i, c[..., 3], 0); bb = Image.fromarray(c[..., 3]).getbbox(); c = c[bb[1]:bb[3], bb[0]:bb[2]]; save(name, c, {'top': top_row(c[..., 3], .7) if name == 'hp_hang' else 0})
a = unmagenta(np.array(Image.open(IN + 'bg_mesas.png').convert('RGB'))); ys = np.where((a[..., 3] > 128).any(1))[0]; save('mesas', a[ys.min():])
json.dump(W, open('art/dune/world.json', 'w'), separators=(',', ':'))
