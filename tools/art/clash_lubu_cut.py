"""Lu Bu commander from the owner's ChatGPT 2 x 2 sheet (owner 2026-11-23, after "เอาตัวไม่สวยไปเป็นแบบ มันจะสวยกว่าแบบได้ไง": GPT drew him freely,
no attachment). FREE route first: key out the magenta, cut the 4 poses, shrink each to fit H px (area average), alpha threshold, then pixel_punch.
  python3 tools/art/clash_lubu_cut.py [H=40]
-> art/incoming/clash/lubu/gpt/cut_<n>.png (full size, keyed), lubu_<n>_<H>.png (raw shrink), lubu_<n>_<H>_p.png (punched), compare_<H>.png"""
import sys, os, subprocess, numpy as np
from PIL import Image
H = int(sys.argv[1]) if len(sys.argv) > 1 else 40
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../art/incoming/clash/lubu/gpt'); R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..')
im = np.asarray(Image.open(os.path.join(D, 'gpt_lubu4.png')).convert('RGBA')).astype(int)
r, g, b = im[..., 0], im[..., 1], im[..., 2]
mag = (r > 150) & (b > 150) & (g < 110) & (abs(r - b) < 90)          # the flat magenta and its JPEG-ish fringe
a = np.where(mag, 0, 255).astype(np.uint8); out = im.copy().astype(np.uint8); out[..., 3] = a
# figures cross the half lines, so cut by pieces: label the opaque pieces (after a small grow so a figure's feathers / halberd join it),
# the 4 biggest = the 4 poses in reading order, every other piece goes to the nearest pose
from scipy import ndimage
h, w = a.shape; grown = ndimage.binary_dilation(a > 0, iterations=6); lab, nl = ndimage.label(grown); sizes = ndimage.sum(grown, lab, range(1, nl + 1))
big = sorted(sorted(range(1, nl + 1), key=lambda i: -sizes[i - 1])[:4], key=lambda i: (round(ndimage.center_of_mass(grown, lab, i)[0] / (h / 2)), ndimage.center_of_mass(grown, lab, i)[1]))
cen = [ndimage.center_of_mass(grown, lab, i) for i in big]; owner = np.zeros(nl + 1, int)
for i in range(1, nl + 1): c0 = ndimage.center_of_mass(grown, lab, i); owner[i] = big[int(np.argmin([(c0[0] - cc[0]) ** 2 + (c0[1] - cc[1]) ** 2 for cc in cen]))]
cells = []
for n, bi in enumerate(big, 1):
    keep = (owner[lab] == bi) & (a > 0); o2 = out.copy(); o2[..., 3] = np.where(keep, 255, 0)
    c = Image.fromarray(o2); bb = c.getbbox(); c = c.crop(bb); c.save(os.path.join(D, f'cut_{n}.png'))
    s = H / max(c.size); sw, sh = max(1, round(c.width * s)), max(1, round(c.height * s))
    # premultiplied area shrink so the magenta-free edge does not darken, then a hard alpha cut
    arr = np.asarray(c).astype(float); pm = arr.copy(); pm[..., :3] *= arr[..., 3:4] / 255
    sm = np.asarray(Image.fromarray(pm.astype(np.uint8)).resize((sw, sh), Image.BOX)).astype(float); al = np.asarray(c.split()[3].resize((sw, sh), Image.BOX)).astype(float)
    rgb = np.where(al[..., None] > 0, sm[..., :3] * 255 / np.maximum(al[..., None], 1), 0); A = np.where(al > 110, 255, 0)
    o = np.dstack([np.clip(rgb, 0, 255), A]).astype(np.uint8); cv = Image.new('RGBA', (H, H), (0, 0, 0, 0)); cv.paste(Image.fromarray(o), ((H - sw) // 2, H - sh))
    f = os.path.join(D, f'lubu_{n}_{H}.png'); cv.save(f); fp = os.path.join(D, f'lubu_{n}_{H}_p.png')
    subprocess.run([sys.executable, os.path.join(R, 'tools/art/pixel_punch.py'), f, fp, '1.0', '28'], check=True); cells.append((Image.open(f).convert('RGBA'), Image.open(fp).convert('RGBA')))
# compare sheet: per pose raw shrink / punched, next to a soldier (hk_rider) and the old commander c8_02 at the same zoom
Z = 6; ref = [Image.open(os.path.join(R, 'art/clash/units/hk_rider.png')).convert('RGBA'), Image.open(os.path.join(R, 'art/incoming/clash/batch8/raw/c8_02.png')).convert('RGBA')]
tiles = [t for pair in cells for t in pair] + ref; Wd = sum(t.width for t in tiles) * Z + 10 * (len(tiles) + 1); Hd = max(t.height for t in tiles) * Z + 20
sheet = Image.new('RGBA', (Wd, Hd), (92, 120, 60, 255)); x = 10
for t in tiles: sheet.alpha_composite(t.resize((t.width * Z, t.height * Z), Image.NEAREST), (x, Hd - 10 - t.height * Z)); x += t.width * Z + 10
sheet.save(os.path.join(D, f'compare_{H}.png')); print('ok', [c[0].size for c in cells])
