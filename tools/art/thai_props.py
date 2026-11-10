# The owner's four GPT sheets for the Thai map (2026-11-08) -> art/action/props/<name>.png
#   python tools/art/thai_props.py
# Each sheet was white-cut (white_cut.py --edge-only --no-ring) and spaced into a 6x3 grid (*_spaced.png). Every item is
# converted with props_px.py at its own height (one run per size group), so a jar is small and a palm tall; buildings
# share the European town's scale (x1.19), the palace / temple / stupa / gate are bigger. Water drawn at the foot of the
# riverside buildings is cut out so the river texture shows between the stilts.
import subprocess, os, shutil, sys, tempfile
import numpy as np
from PIL import Image

M = 'art/incoming/action/map/'
OUT = 'art/action/props/'
# PROP_K=1.5: the same props at 1.5x the pixels into art/action/props_hr/ (action.html draws them 1 art px per screen px)
K = float(os.environ.get('PROP_K', '1'))
if K != 1: OUT = 'art/action/props_hr/'; os.makedirs(OUT, exist_ok=True)
SHEETS = {
    'gpt_thai_village_spaced.png': ('v_stilt v_row v_hut v_kitchen v_granary v_veranda v_waterhouse v_fishhut v_boatshed v_stall v_pen '
                                    'v_watchtower v_temple v_stupa v_pavilion v_well v_bridge v_raintree').split(),
    'gpt_thai_city_spaced.png': ('t_house t_twin t_hut t_granary t_shophouse t_stall t_sala t_gate t_fort t_palace t_temple t_stupa t_prang '
                                 't_belltower t_library t_elephant t_smithy t_teahouse').split(),
    'gpt_thai_city_props_spaced.png': ('jar_dragon pots boat_fruit bridge_curve lotus banana coconut sugarpalm fence_bamboo baskets oxcart '
                                       'lantern_thai lion elephant_statue flagpole fruit_mat wall_sema noticeboard').split(),
}
# target heights in game pixels (the rogue is ~78 px tall); missing = the sheet's height x 1.19 (the town's scale)
H = {'v_raintree': 420, 'v_watchtower': 380, 'v_temple': 360, 'v_stupa': 400, 'v_bridge': 200,
     't_palace': 470, 't_temple': 430, 't_stupa': 470, 't_prang': 420, 't_gate': 380, 't_fort': 360, 't_belltower': 330,
     'jar_dragon': 70, 'pots': 66, 'boat_fruit': 66, 'bridge_curve': 150, 'lotus': 52, 'banana': 260, 'coconut': 390,
     'sugarpalm': 400, 'fence_bamboo': 72, 'baskets': 62, 'oxcart': 110, 'lantern_thai': 150, 'lion': 112, 'elephant_statue': 122,
     'flagpole': 220, 'fruit_mat': 56, 'wall_sema': 112, 'noticeboard': 128}
WATERY = {'v_waterhouse', 'v_fishhut', 'v_boatshed', 'v_pavilion', 'v_bridge', 't_shophouse', 't_library'}

def heights(path, n):
    # each item's height in the spaced sheet = props_px's own blob order: run it once at a known scale and read back
    tmp = tempfile.mkdtemp(); r = subprocess.run([sys.executable, 'tools/art/props_px.py', path, tmp, '0=100', '20'], check=True, capture_output=True, text=True)
    k = float(r.stdout.split('scale')[-1].split()[0])                  # sheet px -> output px at this run
    hs = [Image.open(os.path.join(tmp, f'prop{i}.png')).height / k for i in range(n)]   # = heights in the sheet
    shutil.rmtree(tmp); return hs

def unwater(png):
    # the turquoise water GPT drew under stilts / bridges: cut it in the lower 40% so the game's river shows through
    a = np.array(Image.open(png).convert('RGBA')).astype(int); h = a.shape[0]; r, g, b = a[..., 0], a[..., 1], a[..., 2]
    water = (b > r + 45) & (g > r + 25) & (a[..., 3] > 0); water[: int(h * .6)] = False
    a[water, 3] = 0; Image.fromarray(a.astype(np.uint8)).save(png); return int(water.sum())

def dry_sheet(path, names):
    # cut GPT's turquoise water (and its dark teal rim, the pale foam) from the lower 45% of the watery items' cells in the
    # full-size sheet, before the colours are reduced (after that the water mixes with the greens)
    a = np.array(Image.open(path).convert('RGBA')).astype(int); G, cw, ch = 70, 256, 1024 / 3
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    water = ((b > r + 28) & (g > r + 12)) | ((b > r + 8) & (g > r + 4) & (r < 90)) | ((r > 185) & (g > 225) & (b > 220) & (b >= r + 10))
    keep = np.zeros(water.shape, bool)
    for i, n in enumerate(names):
        if n not in WATERY: continue
        col, row = i % 6, i // 6; x0, x1 = int(G * (col + 1) + col * cw), int(G * (col + 1) + (col + 1) * cw)
        y0, y1 = int(G * (row + 1) + row * ch), int(G * (row + 1) + (row + 1) * ch)
        ys = np.nonzero((a[y0:y1, x0:x1, 3] > 0).any(1))[0]
        if len(ys): keep[y0 + ys[0] + int((ys[-1] - ys[0]) * .55): y0 + ys[-1] + 1, x0:x1] = True
    cut = water & keep & (a[..., 3] > 0); a[cut, 3] = 0
    out = path.replace('_clean.png', '.png').replace('.png', '_dry.png'); Image.fromarray(a.astype(np.uint8)).save(out); return out, int(cut.sum())

# owner 2026-11-09 "ดูด้วยตายังเห็นเลยตัดยังไง": white_cut --edge-only only took the white joined to the sheet's border, so the
# background seen between stilts, posts and rails stayed, and the colour reduction turned it cream. Now every enclosed
# near-white patch is cut in the full-size spaced sheet too (not in the items whose own walls are white), and the light
# antialias line left round every cut edge goes (2 px; 1 px on the white-walled items).
WHITE_OK = {'v_temple', 'v_stupa', 't_temple', 't_stupa', 't_gate', 't_belltower', 't_prang', 't_palace', 'jar_dragon', 'lantern_thai',
            'wall_sema', 'lion', 'elephant_statue', 't_stall'}
def clean_holes(path, names):
    from scipy import ndimage
    a = np.array(Image.open(path).convert('RGBA')).astype(int); al = a[..., 3] > 0; rgb = a[..., :3]; G, cw, ch = 70, 256, 1024 / 3
    item = np.full(al.shape, -1)
    for i in range(len(names)):
        col, row = i % 6, i // 6; item[int(G * (row + 1) + row * ch): int(G * (row + 1) + (row + 1) * ch), int(G * (col + 1) + col * cw): int(G * (col + 1) + (col + 1) * cw)] = i
    ok = np.isin(item, [i for i, n in enumerate(names) if n in WHITE_OK])
    white = al & (rgb.min(-1) >= 240) & (rgb.max(-1) - rgb.min(-1) <= 10)
    lab, k = ndimage.label(white); sz = ndimage.sum(white, lab, range(1, k + 1)) if k else []
    big = np.isin(lab, [i + 1 for i, v in enumerate(sz) if v >= 20]) & ~ok
    a[big, 3] = 0; n1 = int(big.sum()); n2 = 0
    L = .3 * rgb[..., 0] + .59 * rgb[..., 1] + .11 * rgb[..., 2]
    for it in range(2):
        al = a[..., 3] > 0; edge = al & ndimage.binary_dilation(~al)
        lite = edge & (rgb.min(-1) >= 200) & (rgb.max(-1) - rgb.min(-1) <= 30)
        if it: lite &= ~ok
        a[lite, 3] = 0; n2 += int(lite.sum())
    # GPT's own dark outline has a 1-2 px antialias ring outside it (the colour blended with the white background: grey-olive
    # round leaves, khaki round wood). An edge pixel clearly lighter than the darkest pixel just inside it is that ring.
    for it in range(2):
        al = a[..., 3] > 0; edge = al & ndimage.binary_dilation(~al)
        Lin = np.where(al & ~edge, L, 999); dmin = ndimage.minimum_filter(Lin, size=5)
        ring = edge & (L > dmin + 35) & (dmin < 120)
        a[ring, 3] = 0; n2 += int(ring.sum())
    out = path.replace('.png', '_clean.png'); Image.fromarray(a.astype(np.uint8)).save(out)
    print(os.path.basename(path), 'enclosed white cut', n1, 'edge line cut', n2); return out

for sheet, names in SHEETS.items():
    path = clean_holes(M + sheet, names); hs = heights(path, len(names))
    dry, ncut = dry_sheet(path, names) if any(n in WATERY for n in names) else (path, 0)
    if ncut: print(sheet, 'water cut in the full-size sheet:', ncut)
    for i, n in enumerate(names):
        t = round(H.get(n, round(hs[i] * 1.19)) * K)
        tmp = tempfile.mkdtemp(); subprocess.run([sys.executable, 'tools/art/props_px.py', dry if n in WATERY else path, tmp, f'{i}={t}', '20'], check=True, capture_output=True)
        shutil.copy(os.path.join(tmp, f'prop{i}.png'), OUT + n + '.png'); shutil.rmtree(tmp)
        cut = 0
        im = Image.open(OUT + n + '.png'); print(n, im.size, ('water cut %d px' % cut) if cut else '')
