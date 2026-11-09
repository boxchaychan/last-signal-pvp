# Clean what is left of the GPT background in prop pictures (owner 2026-11-09, a crop of a stilt house: "ดูด้วยตายังเห็น
# เลยตัดยังไง" — cream patches between the stilts and pale dots round the outline). Two kinds of leftovers:
#  A. holes: the background seen between posts, rails, under floors. In the reduced palette it is ONE flat pale colour
#     (cream, a different shade per picture), at least 3 px thick, and mostly ringed by dark outline → made see-through.
#     A flat pale strip under 7 px thick (a roof ridge, a beam) is kept, and so are pale areas not ringed by outline
#     (white temple walls, the stupa).
#  B. the fringe: props_px adds a 1 px dark outline round the cut figure; where the cut kept a line of background
#     between that outline and the picture's own edge, light dots show. A pale pixel next to that added outline whose
#     neighbourhood is mostly not pale gets the colour of the nearest non-pale pixel inside.
#   python tools/art/prop_bgclean.py [--dry] [--noholes] [--mark=<dir>] <png> [<png> ...]     (in place unless --dry)
# 2026-11-09 run: holes on t_granary t_library t_palace t_smithy t_teahouse t_twin v_boatshed v_fishhut v_stilt cart oxcart,
# --noholes on every other prop.
import sys, os
import numpy as np
from PIL import Image
from scipy import ndimage

DRY = '--dry' in sys.argv
NOHOLES = '--noholes' in sys.argv   # fringe only (cream plaster walls of the western houses read as holes)
MARK = next((a.split('=', 1)[1] for a in sys.argv if a.startswith('--mark=')), None)
OUTL = (29, 26, 34)        # the outline colour props_px adds
for f in [a for a in sys.argv[1:] if not a.startswith('--')]:
    a = np.array(Image.open(f).convert('RGBA')).astype(int); al = a[..., 3] > 0; rgb = a[..., :3]
    L = .3 * rgb[..., 0] + .59 * rgb[..., 1] + .11 * rgb[..., 2]; sat = rgb.max(-1) - rgb.min(-1)
    # A. holes
    pale = al & (rgb.min(-1) > 190) & (sat < 70); key = rgb[..., 0] * 65536 + rgb[..., 1] * 256 + rgb[..., 2]
    hole = np.zeros_like(al); cand = []
    for c in np.unique(key[pale]):
        m = pale & (key == c); lab, k = ndimage.label(m)
        if not k: continue
        for i, s in enumerate(ndimage.sum(m, lab, range(1, k + 1))):
            if s < 16: continue
            mm = lab == i + 1
            if ndimage.binary_erosion(mm, iterations=3).sum() < 4: continue
            ring = ndimage.binary_dilation(mm, iterations=2) & ~mm & al
            if ring.sum() and (L[ring] < 80).mean() > .4: hole |= mm; cand.append((int(c), int(s)))
    if NOHOLES: hole[:] = False; cand = []
    if cand:   # every hole of a picture is the same background colour: keep the colour with the most area and its near shades
        tot = {}
        for c, n in cand: tot[c] = tot.get(c, 0) + n
        bg = max(tot, key=tot.get); bc = np.array([bg >> 16, (bg >> 8) & 255, bg & 255])
        far = hole & (np.abs(rgb - bc).sum(-1) > 24); hole &= ~far
    # B. the fringe inside the added outline: drop it (twice, it can be 2 px), then put the 1 px outline back round the figure
    out = a.copy(); out[hole, 3] = 0; nf = 0; gone = np.zeros_like(al)
    lite = (L > 135) & (sat < 125)
    for _ in range(2):
        al2 = out[..., 3] > 0; r2 = out[..., :3]
        added = al2 & np.all(r2 == OUTL, -1) & ndimage.binary_dilation(~al2, structure=np.ones((3, 3)))
        zone = al2 & ~added & ndimage.binary_dilation(added | ~al2)
        frac = ndimage.uniform_filter((lite & al2 & ~added).astype(float), 7) / np.maximum(ndimage.uniform_filter((al2 & ~added).astype(float), 7), 1e-6)
        fringe = zone & lite & (frac < .4)
        if not fringe.any(): break
        nf += int(fringe.sum()); gone |= fringe; out[fringe, 3] = 0; out[added & ndimage.binary_dilation(fringe, structure=np.ones((3, 3))), 3] = 0
    al2 = out[..., 3] > 0; ring = ~al2 & ndimage.binary_dilation(al2) & (a[..., 3] > 0) & ~hole   # the 1 px outline back, where pixels were taken away
    out[ring] = (*OUTL, 255); fringe = gone
    print(f'{os.path.basename(f):22s} holes {int(hole.sum()):6d}  fringe {nf:5d}')
    if MARK:
        os.makedirs(MARK, exist_ok=True); b = a.copy(); b[hole] = (255, 0, 255, 255); b[fringe] = (0, 255, 255, 255)
        Image.fromarray(b.astype(np.uint8)).save(os.path.join(MARK, os.path.basename(f)))
    if not DRY: Image.fromarray(out.astype(np.uint8)).save(f, optimize=True)
