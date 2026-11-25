"""Cut a Meta / Gemini effect video (black background) into a game sprite sheet for divine.html. Free.
  python3 tools/art/divine_vfx.py <video> <name> <first frame>|<a-b,c-d> <last frame> [step=2] [height=520] [fps] [edgefade 0..0.3]
fps = playback speed (default real time = 24 / step); edgefade = fade the left / right borders (Meta often runs an effect off the frame,
this hides the straight cut).
The sheet keeps the BLACK background (the game draws it with additive light, so black = invisible) and is saved as JPEG (small).
The crop is the union of every bright pixel in the chosen frames; the anchor = the centre of the brightest blob in the strongest frame
(where the effect hits). -> art/divine/vfx_<name>.jpg + vfx_<name>.json {n, cols, fw, fh, fps, ax, ay}"""
import sys, os, json, subprocess, tempfile, glob
import numpy as np
from PIL import Image
from scipy import ndimage as nd
vid, name = sys.argv[1], sys.argv[2]; RANGES = [tuple(map(int, r.split('-'))) for r in sys.argv[3].split(',')] if '-' in sys.argv[3] else [(int(sys.argv[3]), int(sys.argv[4]))];   # '<a>-<b>,<c>-<d>' skips a part (e.g. a full-white flash)
step = int(sys.argv[5]) if len(sys.argv) > 5 else 2; TH = int(sys.argv[6]) if len(sys.argv) > 6 else 520
FPS = float(sys.argv[7]) if len(sys.argv) > 7 else 24 / step; EF = float(sys.argv[8]) if len(sys.argv) > 8 else 0
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'); OUT = os.path.join(R, 'art/divine')
tmp = tempfile.mkdtemp(); subprocess.run(['ffmpeg', '-v', 'error', '-i', vid, os.path.join(tmp, '%04d.png')], check=True)
allf = sorted(glob.glob(os.path.join(tmp, '*.png'))); fs = [f for (ra, rb) in RANGES for f in allf[ra:rb + 1:step]]; ims = [np.asarray(Image.open(f).convert('RGB')).astype(np.float32) for f in fs]
lum = [im.max(2) for im in ims]; union = np.zeros_like(lum[0], bool)
for l in lum: union |= l > 28
ys, xs = np.where(union); pad = 8; x0, y0, x1, y1 = max(0, xs.min() - pad), max(0, ys.min() - pad), min(union.shape[1], xs.max() + pad), min(union.shape[0], ys.max() + pad)
k = TH / (y1 - y0); fw, fh = round((x1 - x0) * k), TH
peak = int(np.argmax([l.sum() for l in lum])); hot = nd.gaussian_filter(lum[peak], 6); cy, cx = np.unravel_index(np.argmax(hot[y0:y1, x0:x1]), hot[y0:y1, x0:x1].shape)
n = len(ims); cols = min(n, 8); rows = (n + cols - 1) // cols; sheet = Image.new('RGB', (cols * fw, rows * fh), (0, 0, 0))
for i, im in enumerate(ims):
    fr = Image.fromarray(np.clip(im[y0:y1, x0:x1], 0, 255).astype(np.uint8)).resize((fw, fh), Image.LANCZOS)
    a_ = np.asarray(fr).astype(np.float32)
    if EF: xx = np.linspace(0, 1, fw); win = np.clip(np.minimum(xx, 1 - xx) / EF, 0, 1) ** 1.5; a_ *= win[None, :, None]
    a_[a_.max(2) < 18] = 0; sheet.paste(Image.fromarray(a_.astype(np.uint8)), ((i % cols) * fw, (i // cols) * fh))
sheet.save(os.path.join(OUT, f'vfx_{name}.jpg'), quality=86)
meta = {'n': n, 'cols': cols, 'fw': fw, 'fh': fh, 'fps': round(FPS, 2), 'ax': round(cx / (x1 - x0), 3), 'ay': round(cy / (y1 - y0), 3)}
json.dump(meta, open(os.path.join(OUT, f'vfx_{name}.json'), 'w')); print(meta, sheet.size, os.path.getsize(os.path.join(OUT, f'vfx_{name}.jpg')) // 1024, 'KB')
