# A glowing effect video on a BLACK background (Dreamina / Seedance clips, owner 2026-11-18) -> one additive sprite sheet for the game.
# Black adds nothing in additive blending, so no keying: the dim background (a dark floor the generator drew, noise) is crushed to black,
# a soft round fade toward the frame edge drops the corners (where the generator's marks sit) and keeps ring effects round,
# frames are sampled evenly between --from and --to, a fade-in / fade-out can be added, cells are packed in a grid.
#   python3 tools/video/fx_black_sheet.py <video.mp4> <out.png> [--from=0] [--to=5] [--n=16] [--cols=4] [--cell=256]
#        [--black=40] [--gamma=1] [--round=.47] [--soft=.06] [--fadein=0] [--fadeout=2] [--crop=x,y,w,h]
#   --black: luminance (0-255) that becomes black (raise it to remove a drawn floor); --round: radius of the round fade, as a
#   fraction of the cell (0 = off); --fadein / --fadeout: how many first / last frames ramp in / out.
# Prints a JSON line {"file","cols","rows","n","cell","fps"} for the game.
import sys, json, subprocess
import numpy as np
from PIL import Image

def opt(name, d):
    for a in sys.argv:
        if a.startswith('--' + name + '='): return a.split('=', 1)[1]
    return d

src, out = sys.argv[1], sys.argv[2]
t0, t1, n, cols, cell = float(opt('from', 0)), float(opt('to', 5)), int(opt('n', 16)), int(opt('cols', 4)), int(opt('cell', 256))
blk, gam, rnd, soft = float(opt('black', 40)), float(opt('gamma', 1)), float(opt('round', .47)), float(opt('soft', .06))
fin, fout = int(opt('fadein', 0)), int(opt('fadeout', 2))
crop = [int(v) for v in opt('crop', '').split(',')] if opt('crop', '') else None
pr = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', src], capture_output=True, text=True, check=True).stdout.strip().split(',')
W, H = int(pr[0]), int(pr[1])
rows = (n + cols - 1) // cols; sheet = np.zeros((rows * cell, cols * cell, 3), np.float32)
yy, xx = np.mgrid[0:cell, 0:cell]; r = np.hypot(xx - cell / 2 + .5, yy - cell / 2 + .5) / cell
mask = np.clip((rnd - r) / soft, 0, 1) if rnd > 0 else np.ones((cell, cell))
for i in range(n):
    t = t0 + (t1 - t0) * i / max(1, n - 1)
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t:.3f}', '-i', src, '-frames:v', '1', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(H, W, 3)
    im = Image.fromarray(fr)
    if crop: im = im.crop((crop[0], crop[1], crop[0] + crop[2], crop[1] + crop[3]))
    else: s = min(im.size); im = im.crop(((im.width - s) // 2, (im.height - s) // 2, (im.width - s) // 2 + s, (im.height - s) // 2 + s))
    a = np.asarray(im.resize((cell, cell), Image.LANCZOS)).astype(np.float32)
    lum = a.max(2, keepdims=True); k = np.clip((lum - blk) / max(1, 255 - blk), 0, 1) ** gam / np.maximum(lum / 255, 1e-3)   # crush the dark floor, keep the hue
    a = np.clip(a / 255 * k, 0, 1) * mask[..., None]
    f = 1.0
    if fin and i < fin: f = (i + 1) / (fin + 1)
    if fout and i >= n - fout: f = min(f, (n - i) / (fout + 1))
    rr, cc = divmod(i, cols); sheet[rr * cell:(rr + 1) * cell, cc * cell:(cc + 1) * cell] = a * f
Image.fromarray((sheet * 255).astype(np.uint8)).save(out, optimize=True)
print(json.dumps({'file': out, 'cols': cols, 'rows': rows, 'n': n, 'cell': cell, 'fps': round(n / max(.05, (t1 - t0)), 2)}))
