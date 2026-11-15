# Thai map 1 kit for hoodfall.html?map=thai: cut Codex's 6 kit sheets (art/incoming/thai/kit/map1_kit_0N_*.png, 1536x1024,
# painted 2D on flat green #00B140) into single pieces -> art/sidegame/thai/<name>.webp + thai.json (sizes).
#   python3 tools/art/thai_kit_cut.py            (python3 tools/art/thai_kit_cut.py --boxes = only print the boxes found)
# - green keyed by colour distance to the key (the plants are green too, so no global despill: only edge pixels are cleaned)
# - pieces found as blobs on a coarse grid (parts closer than ~24 px join), named in reading order per sheet (NAMES)
# - kept at the sheet's own resolution: the game treats 3 sheet px = 1 world px and draws them on the full-res canvas
# - the wall piece is made seamless (left/right and top/bottom cross-fade) so it tiles; raw sheets stay untouched
import json, os, sys
import numpy as np
from PIL import Image
SRC, DST = 'art/incoming/thai/kit', 'art/sidegame/thai'
SHEETS = {
    'map1_kit_01_platforms': ['cap_l', 'cap_m', 'cap_r', 'wall', 'wall_root', 'corner'],
    'map1_kit_02_access': ['ladder_top', 'ladder_mid', 'ladder_bot', 'stairs_ur', 'stairs_ul', 'vines'],
    'map1_kit_03_summit': ['gate', 'prang', 'chedi', 'ruin_wall', 'stone_lantern'],
    'map1_kit_04_lower_props': ['sala', 'spirit_house', 'jars', 'coconut', 'sugarpalm', 'banana', 'campfire', 'lotus'],
    'map1_kit_05_upper_props': ['stele1', 'stele2', 'stele3', 'raintree', 'plinth', 'rootwall', 'grass', 'fl_white', 'fl_red', 'fl_violet', 'fl_yellow', 'wisp'],
    'map1_kit_06_backgrounds': ['bg_mount', 'bg_forest', 'bg_sky'],
}
SPLIT = {'map1_kit_05_upper_props': (1, 505)}   # [blob index, x]: two steles touching on grass, cut apart at x
SKIP = {'spirit_house'}   # owner "ไม่เอาศาลภูมินะ": not exported
KEY = np.array([0, 177, 64], float)

def key(rgb):
    d = np.sqrt(((rgb - KEY) ** 2).sum(2))
    a = np.clip((d - 45) / 50, 0, 1)
    out = rgb.copy()
    edge = (a > 0) & (a < 1)
    r, g, b = out[..., 0], out[..., 1], out[..., 2]
    gg = np.minimum(g, np.maximum(r, b) + 30)        # pull the key's green out of soft edge pixels only
    out[..., 1] = np.where(edge, gg, g)
    return out, a

def blobs(a, cell=8, join=1):
    h, w = a.shape; gh, gw = h // cell, w // cell
    m = a[:gh * cell, :gw * cell].reshape(gh, cell, gw, cell).max((1, 3)) > .5
    d = m.copy()
    for _ in range(join):                             # grow so parts close together join
        e = d.copy(); e[1:] |= d[:-1]; e[:-1] |= d[1:]; e[:, 1:] |= d[:, :-1]; e[:, :-1] |= d[:, 1:]; d = e
    lab = np.zeros(d.shape, int); n = 0; out = []
    for y in range(gh):
        for x in range(gw):
            if d[y, x] and not lab[y, x]:
                n += 1; st = [(y, x)]; lab[y, x] = n; ys, xs = [], []
                while st:
                    cy, cx = st.pop(); ys.append(cy); xs.append(cx)
                    for ny, nx in ((cy + 1, cx), (cy - 1, cx), (cy, cx + 1), (cy, cx - 1)):
                        if 0 <= ny < gh and 0 <= nx < gw and d[ny, nx] and not lab[ny, nx]: lab[ny, nx] = n; st.append((ny, nx))
                if len(ys) > 12: out.append([min(xs) * cell, min(ys) * cell, (max(xs) + 1) * cell, (max(ys) + 1) * cell])
    # reading order: rows (by centre y, ~ a third of the sheet tall), then x
    out.sort(key=lambda b: (round((b[1] + b[3]) / 2 / (h / 3)), b[0]))
    return out

def trim(rgba):
    al = rgba[..., 3]; ys, xs = np.where(al > 8)
    return rgba[ys.min():ys.max() + 1, xs.min():xs.max() + 1]

def seamless(rgba, f=0.18):
    im = rgba.astype(float); h, w = im.shape[:2]
    for axis, n in ((1, w), (0, h)):
        k = int(n * f); im = np.moveaxis(im, axis, 0)
        a, b = im[:k].copy(), im[-k:].copy(); t = np.linspace(0, 1, k)[:, None, None]
        im[-k:] = b * (1 - t) + a * t                 # the end fades into the start
        im = np.moveaxis(im[:-k], 0, axis)            # drop the start: the end now leads into it
    return im.clip(0, 255).astype(np.uint8)

def main():
    os.makedirs(DST, exist_ok=True); meta = {}
    for sheet, names in SHEETS.items():
        src = np.array(Image.open(f'{SRC}/{sheet}.png').convert('RGB')).astype(float)
        rgb, a = key(src)
        bx = blobs(a)
        if sheet in SPLIT:
            i, sx = SPLIT[sheet]; b = bx[i]; bx[i:i + 1] = [[b[0], b[1], sx, b[3]], [sx, b[1], b[2], b[3]]]
        print(sheet, len(bx), 'pieces', bx)
        if '--boxes' in sys.argv: continue
        if len(bx) != len(names): sys.exit(f'{sheet}: found {len(bx)} pieces, expected {len(names)}')
        for name, (x0, y0, x1, y1) in zip(names, bx):
            if name in SKIP: continue
            pad = 6; x0, y0, x1, y1 = max(0, x0 - pad), max(0, y0 - pad), min(src.shape[1], x1 + pad), min(src.shape[0], y1 + pad)
            pc = np.dstack([rgb[y0:y1, x0:x1], a[y0:y1, x0:x1] * 255]).clip(0, 255).astype(np.uint8)
            pc = trim(pc)
            if name == 'wall':
                pc = pc[8:-8, 8:-8]; pc[..., 3] = 255; pc = seamless(pc)
            if name.startswith('bg_'):
                pc = pc[2:-2, 4:-4]
            Image.fromarray(pc, 'RGBA').save(f'{DST}/{name}.webp', quality=88, method=6)
            meta[name] = [int(pc.shape[1]), int(pc.shape[0])]
    if meta:
        json.dump(meta, open(f'{DST}/thai.json', 'w'), separators=(',', ':'))
        print('wrote', len(meta), 'pieces to', DST)

main()
