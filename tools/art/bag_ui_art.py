"""Web-ready UI art of the backpack game from the Codex pictures (owner 2026-11-28: "UI ทำทุกอย่างให้สวย"), free.

  python tools/art/bag_ui_art.py

In:  art/incoming/bag3d/ui1/  arena_target.png (the look of the 3D arena), title_bg.png, shop_bg.png, ui_frames.png (7 ornaments, transparent)
     art/incoming/bag3d/ui2/  arena_grave.png, arena_volcano.png, arena_snow.png (the same arena in the other lands), ui_glyphs.png (4 x 3 symbols)
Out: art/bag3d/ui/arena_<land>.jpg (forest = the sunny one), title_bg.jpg, shop_bg.jpg,
     art/bag3d/ui/f_<name>.webp = each ornament of ui_frames cut out by its own shape (banner, panel, ring, shield, btn_gold, btn_blue, btn_round),
     art/bag3d/ui/glyphs.webp = the 12 symbols, 96 px cells in one row + art/bag3d/ui/ui.json (sizes, glyph names).
The raw pictures stay where they are (briefs: BRIEF.md in the two folders).
"""
import json, os
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

OUT = 'art/bag3d/ui'; os.makedirs(OUT, exist_ok=True); J = {}
def jpg(src, dst, q=88, size=None):
    if not os.path.exists(src): print('missing', src); return
    im = Image.open(src).convert('RGB')
    if size: im = im.resize(size, Image.LANCZOS)
    im.save(f'{OUT}/{dst}', quality=q, optimize=True, progressive=True); J[dst.split('.')[0]] = list(im.size); print(dst, im.size, os.path.getsize(f'{OUT}/{dst}') // 1024, 'KB')
jpg('art/incoming/bag3d/ui1/arena_target.png', 'arena_forest.jpg'); jpg('art/incoming/bag3d/ui2/arena_grave.png', 'arena_grave.jpg'); jpg('art/incoming/bag3d/ui2/arena_volcano.png', 'arena_volcano.jpg'); jpg('art/incoming/bag3d/ui2/arena_snow.png', 'arena_snow.jpg')
jpg('art/incoming/bag3d/ui1/title_bg.png', 'title_bg.jpg', 84); jpg('art/incoming/bag3d/ui1/shop_bg.png', 'shop_bg.jpg', 82)
def keyed(path):   # RGBA with a clean alpha: a transparent picture as it is, a flat background keyed by the corner colour
    im = Image.open(path).convert('RGBA'); a = np.asarray(im).copy(); k = a[2, 2]
    if k[3] > 16:
        d = np.abs(a[..., :3].astype(int) - k[:3].astype(int)).sum(axis=2); a[..., 3] = np.where(d < 90, 0, np.where(d < 170, (a[..., 3] * (d - 90) / 80).astype(np.uint8), a[..., 3]))
    return a
# ---- the ornaments: connected shapes, big ones only, named by where they sit (top row, middle row left to right, bottom row left to right)
f = 'art/incoming/bag3d/ui1/ui_frames.png'
if os.path.exists(f):
    a = keyed(f); lab, n = ndi.label(ndi.binary_dilation(a[..., 3] > 40, iterations=6)); boxes = []
    for i, sl in enumerate(ndi.find_objects(lab)):
        h, w = sl[0].stop - sl[0].start, sl[1].stop - sl[1].start
        if w * h > 12000: boxes.append((sl[0].start, sl[1].start, sl[0].stop, sl[1].stop, i + 1))
    H0 = a.shape[0]; boxes.sort(key=lambda b: (0 if (b[0] + b[2]) / 2 < H0 * .3 else 1 if (b[0] + b[2]) / 2 < H0 * .68 else 2, b[1])); names = ['banner', 'panel', 'ring', 'shield', 'btn_gold', 'btn_blue', 'btn_round']
    print('ornaments found:', len(boxes))
    for nm, (y0, x0, y1, x1, li) in zip(names, boxes):
        c = a[y0:y1, x0:x1].copy(); c[..., 3] = np.where(lab[y0:y1, x0:x1] == li, c[..., 3], 0); ys, xs = np.where(c[..., 3] > 24); c = c[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
        Image.fromarray(c, 'RGBA').save(f'{OUT}/f_{nm}.webp', quality=90, method=6); J['f_' + nm] = [c.shape[1], c.shape[0]]; print('f_' + nm, c.shape[1], 'x', c.shape[0])
# ---- the symbols: 4 x 3 cells, each trimmed and fitted into 96 px
g = 'art/incoming/bag3d/ui2/ui_glyphs.png'; GN = ['heart', 'coin', 'boss', 'duel', 'mon', 'lock', 'unlock', 'rot', 'sell', 'star', 'fast', 'bag']
if os.path.exists(g):
    a = keyed(g); H, W = a.shape[:2]; Z = 96; sheet = Image.new('RGBA', (Z * 12, Z), (0, 0, 0, 0))
    for n in range(12):
        c = a[n // 4 * H // 3:(n // 4 + 1) * H // 3, n % 4 * W // 4:(n % 4 + 1) * W // 4]; ys, xs = np.where(c[..., 3] > 40)
        if len(xs) < 50: print('glyph', GN[n], 'is empty'); continue
        im = Image.fromarray(c[ys.min():ys.max() + 1, xs.min():xs.max() + 1], 'RGBA'); k = (Z - 6) / max(im.size); im = im.resize((max(1, round(im.width * k)), max(1, round(im.height * k))), Image.LANCZOS)
        sheet.paste(im, (n * Z + (Z - im.width) // 2, (Z - im.height) // 2))
    sheet.save(f'{OUT}/glyphs.webp', quality=92, method=6); J['glyphs'] = {'cell': Z, 'names': GN}; print('glyphs', sheet.size)
json.dump(J, open(f'{OUT}/ui.json', 'w'), indent=1); print('wrote', OUT + '/ui.json')
