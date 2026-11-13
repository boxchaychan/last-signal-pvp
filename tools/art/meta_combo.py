# Meta AI video -> combo frames (owner 2026-11-13 sent art/incoming/dogcat/meta/shiba_combo_meta.mp4: 1280x720, 24 fps, 10 s,
# made from start_shiba2_magenta.png + PROMPT_META_shiba_combo.txt). Meta redrew the shiba (bigger body, round topknot, sheath at
# the hip, he turns toward the camera in hit 2) but keeps ITS version steady through the clip. Nothing is removed from the frames.
# Picked frames (1-based video frames): idle 181-217, hit 1 = 19-35 (draw + slash), hit 2 = 41-65 (raise + low sweep),
# hit 3 = 105-133 (jump slam), recovery 171-179. Key: magenta out, 1/3 size (box), hard alpha. Cell 340x204, feet at (143, 200).
#   python3 tools/art/meta_combo.py [frames dir] -> art/poses/combo/shiba_meta_frames.png (8 columns) + .json
import sys, os, json, subprocess, tempfile, numpy as np
from PIL import Image
V = 'art/incoming/dogcat/meta/shiba_combo_meta.mp4'; O = 'art/poses/combo/shiba_meta_frames'
D = sys.argv[1] if len(sys.argv) > 1 else tempfile.mkdtemp()
if not os.path.exists(D + '/f001.png'): subprocess.run(['ffmpeg', '-v', 'error', '-i', V, D + '/f%03d.png'], check=True)
SETS = dict(idle=[181, 187, 193, 199, 205, 211, 217], h1=[19, 21, 23, 25, 27, 29, 31, 35], h2=[41, 43, 47, 53, 55, 57, 59, 61, 65],
            h3=[105, 109, 111, 113, 115, 117, 121, 125, 127, 129, 133], rec=[171, 173, 175, 177, 179])
X0, CW, CH = 150, 340, 204
def cut(i):
    a = np.asarray(Image.open(D + '/f%03d.png' % i).convert('RGB')).astype(int); r, g, b = a[..., 0], a[..., 1], a[..., 2]
    bg = (r > 120) & (b > 120) & (g < r * .62) & (g < b * .62) & (abs(r - b) < 90)
    rgba = np.dstack([a, np.where(bg, 0, 255)]).astype(np.uint8)[0:612, X0:X0 + CW * 3]
    im = Image.fromarray(rgba).resize((CW, CH), Image.BOX); p = np.asarray(im).copy(); p[..., 3] = np.where(p[..., 3] > 140, 255, 0)
    k = (p[..., 3] > 0) & (p[..., 0] > 140) & (p[..., 2] > 140) & (p[..., 1] < 110); p[k, 3] = 0     # magenta fringe
    return Image.fromarray(p)
order = [i for k in ('idle', 'h1', 'h2', 'h3', 'rec') for i in SETS[k]]; n = len(order); sheet = Image.new('RGBA', (CW * 8, CH * -(-n // 8)))
for j, i in enumerate(order): sheet.alpha_composite(cut(i), (j % 8 * CW, j // 8 * CH))
sheet.save(O + '.png', optimize=True); st = 0; idx = {}
for k in ('idle', 'h1', 'h2', 'h3', 'rec'): idx[k] = [st, len(SETS[k])]; st += len(SETS[k])
json.dump(dict(cw=CW, ch=CH, cols=8, fx=143, fy=200, sets=idx, video_frames=SETS), open(O + '.json', 'w')); print(sheet.size, idx)
