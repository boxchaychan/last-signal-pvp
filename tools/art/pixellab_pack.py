# Files for making one legend in PixelLab by hand (owner 2026-11-07, Wukong first, then "พรอมต์ตัวต่อไป"):
# style pictures small enough for PixelLab's canvas (it refused the 1254 px picture) and the character's own colours.
#   python3 tools/art/pixellab_pack.py <key> <out dir> [turnaround.png]
# Writes <key>_front_256/128.png (the pixel picture art/incoming/legends/px/<key>.png at its native size, see-through),
# <key>_side_256/128.png (the turnaround's middle third, if given), <key>_palette_hex.txt (every colour of the pixel
# picture, darkest first, for "Paste hex colours") and <key>_palette.png (the same as swatches, for "From a palette image").
import sys, os, subprocess, tempfile
import numpy as np
from PIL import Image

key, out = sys.argv[1], sys.argv[2]
turn = sys.argv[3] if len(sys.argv) > 3 else None
os.makedirs(out, exist_ok=True)
px = Image.open('art/incoming/legends/px/%s.png' % key).convert('RGBA')
a = np.array(px); cols = np.unique(a[a[..., 3] > 0][:, :3], axis=0)
if len(cols) > 64:   # PixelLab palettes stay small: the 64 most used colours
    q = Image.fromarray(a[a[..., 3] > 0][:, :3].reshape(1, -1, 3)).quantize(64, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    cols = np.array(q.getpalette()[:192]).reshape(-1, 3)[np.bincount(np.array(q).ravel(), minlength=64) > 0]
cols = cols[np.argsort(cols @ np.array([.299, .587, .114]))]
hexs = ['#%02x%02x%02x' % tuple(int(v) for v in c) for c in cols]
open(os.path.join(out, key + '_palette_hex.txt'), 'w').write(' '.join(hexs) + '\n')
sw = Image.new('RGB', (len(hexs) * 16, 16))
for i, c in enumerate(cols): sw.paste(tuple(int(v) for v in c), (i * 16, 0, i * 16 + 16, 16))
sw.save(os.path.join(out, key + '_palette.png'))
pimg = Image.new('P', (1, 1)); flat = [int(v) for v in cols.flatten()][:765]; pimg.putpalette(flat + [0] * (768 - len(flat)))

def square(fig, n, pad=4):
    fig = fig.crop(fig.getbbox()); s = min((n - 2 * pad) / fig.width, (n - 2 * pad) / fig.height)
    if abs(s - 1) > 1e-6 or fig.width > n:
        fig = fig.resize((max(1, round(fig.width * s)), max(1, round(fig.height * s))), Image.LANCZOS)
    b = np.array(fig); b[..., 3] = np.where(b[..., 3] >= 128, 255, 0)
    q = np.array(Image.fromarray(b[..., :3]).quantize(palette=pimg, dither=Image.Dither.NONE).convert('RGB'))
    f2 = Image.fromarray(np.dstack([q, b[..., 3]]).astype(np.uint8))
    c = Image.new('RGBA', (n, n), (0, 0, 0, 0)); c.alpha_composite(f2, ((n - f2.width) // 2, n - pad - f2.height)); return c

for n in (256, 128): square(px, n).save(os.path.join(out, '%s_front_%d.png' % (key, n)))
if turn:
    t = Image.open(turn).convert('RGB'); w3 = t.width // 3; tmp = tempfile.mkdtemp()
    t.crop((w3, 0, 2 * w3, t.height)).save(tmp + '/s.png')
    subprocess.run([sys.executable, '-I', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'white_cut.py'), tmp + '/s.png', tmp + '/c.png',
                    '--edge-only', '--no-ring'], check=True, capture_output=True)
    side = Image.open(tmp + '/c.png').convert('RGBA')
    for n in (256, 128): square(side, n).save(os.path.join(out, '%s_side_%d.png' % (key, n)))
print(len(hexs), 'colours'); print(' '.join(hexs))
print(sorted(os.listdir(out)))
