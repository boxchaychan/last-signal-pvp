# Rebuild the non-Thai GPT props (nature, village, ruins, European buildings) from their full-size cut sheets with the
# background cleaned first (owner 2026-11-09 "รอบนี้ก็ยังไม่หมด"): white_cut --edge-only kept the white seen between
# branches / posts and a light antialias ring outside GPT's own dark outline; once props_px reduced the colours these
# turned into cream patches and pale dots that no later clean-up could tell apart from real light paint.
# Every item keeps the size it has in the game now (its current file's height).
#   python tools/art/rebuild_props.py [sheet ...]        (sheet = nature, nature_big, village, ruins, buildings)
import subprocess, os, shutil, sys, tempfile
import numpy as np
from PIL import Image
from scipy import ndimage

M, OUT = 'art/incoming/action/map/', 'art/action/props/'
# PROP_K=1.5: the same props at 1.5x the pixels into art/action/props_hr/ (action.html draws them 1 art px per screen px)
K = float(os.environ.get('PROP_K', '1')); OUT2 = 'art/action/props_hr/' if K != 1 else OUT; os.makedirs(OUT2, exist_ok=True)
# PROP_S=tos (owner 2026-11-10 "ลองสัดส่วนเท่า Tree of Savior ดู กลับไปแมพ 2D"): trees ~3.5x the hero, houses ~2.5x, instead of 5.7x / 3x;
# each named prop is rebuilt from its full-size sheet at its current height times this factor (sharp, no runtime scaling).
# Run the PROP_K=1.5 pass FIRST (it reads the 1x heights in props/), then the 1x pass.
TOS = {**dict.fromkeys('oak pine blossom dead_tree'.split(), .62), **dict.fromkeys('house_red house_blue cottage_red cottage_blue cottage_thatch guild shop healer smithy alchemist library armory chapel'.split(), .82),
       **dict.fromkeys('tower barn windmill townhall observatory greenhouse magetower watermill'.split(), .75), **dict.fromkeys('statue arch'.split(), .85)}
SC = TOS if os.environ.get('PROP_S') == 'tos' else {}
SHEETS = {   # sheet: (file, names in props_px's blob order, cut enclosed white?)
    'nature': ('gpt_nature_cut.png', 'oak pine blossom bush boulder rocks grass flowers'.split(), True),
    'village': ('gpt_village_cut.png', 'house_red house_blue tower well fence barrel crate lantern'.split(), False),
    'ruins': ('gpt_ruins_cut.png', ('wall wall_corner arch statue pillar_down pillar rubble stairs stump log mushrooms fern dead_tree '
                                    'mossy_rock campfire tent signpost cart').split(), True),
    'buildings': ('gpt_buildings_spaced.png', ('cottage_red cottage_blue cottage_thatch guild shop healer smithy alchemist library armory '
                                               'barn windmill chapel townhall observatory greenhouse magetower watermill').split(), False),
}

def clean(path, holes):
    a = np.array(Image.open(path).convert('RGBA')).astype(int); al = a[..., 3] > 0; rgb = a[..., :3]
    L = .3 * rgb[..., 0] + .59 * rgb[..., 1] + .11 * rgb[..., 2]; n1 = n2 = 0
    if holes:   # white seen through the figure (between branches, posts): every enclosed near-white patch of 20+ px
        white = al & (rgb.min(-1) >= 240) & (rgb.max(-1) - rgb.min(-1) <= 10)
        lab, k = ndimage.label(white); sz = ndimage.sum(white, lab, range(1, k + 1)) if k else []
        big = np.isin(lab, [i + 1 for i, v in enumerate(sz) if v >= 20]); a[big, 3] = 0; n1 = int(big.sum())
    for _ in range(2):   # the near-white line left on the cut edge
        al = a[..., 3] > 0; e = al & ndimage.binary_dilation(~al) & (rgb.min(-1) >= 200) & (rgb.max(-1) - rgb.min(-1) <= 30)
        a[e, 3] = 0; n2 += int(e.sum())
    for _ in range(2):   # the antialias ring outside GPT's dark outline: an edge pixel clearly lighter than the dark just inside
        al = a[..., 3] > 0; edge = al & ndimage.binary_dilation(~al)
        dmin = ndimage.minimum_filter(np.where(al & ~edge, L, 999), size=5)
        ring = edge & (L > dmin + 35) & (dmin < 120); a[ring, 3] = 0; n2 += int(ring.sum())
    out = os.path.join(tempfile.mkdtemp(), 'clean.png'); Image.fromarray(a.astype(np.uint8)).save(out)
    print(os.path.basename(path), 'enclosed white cut', n1, 'edge cut', n2); return out

for key in sys.argv[1:] or SHEETS:
    f, names, holes = SHEETS[key]; src = clean(M + f, holes)
    for i, n in enumerate(names):
        if not os.path.exists(OUT + n + '.png'): continue
        h = Image.open(OUT + n + '.png').height
        if SC and n not in SC: continue
        tmp = tempfile.mkdtemp(); subprocess.run([sys.executable, 'tools/art/props_px.py', src, tmp, f'{i}={round(h * K * SC.get(n, 1))}', '20'], check=True, capture_output=True)
        with Image.open(os.path.join(tmp, f'prop{i}.png')) as im: size = im.size
        shutil.copy(os.path.join(tmp, f'prop{i}.png'), OUT2 + n + '.png'); shutil.rmtree(tmp, ignore_errors=True)
        print(' ', n, size)
