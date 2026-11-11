# Owner 2026-11-11 "เอาวิดีโอ Meta AI มา หน้าไม่ต้อง เราปรับใช้ได้ไหม": a Meta AI clip used for its MOTION only. Takes N evenly
# spaced frames from a stretch of the clip, cuts the background (white or a flat key colour from the frame border), turns the
# figure into a numbered grey silhouette and writes a pose guide sheet for the Codex queue (the face / design is ignored).
#   python3 tools/art/video_pose_guide.py <clip.mp4> <action> <frames> [start s] [end s] [cols]
#   -> art/incoming/side/berserker/poses/<action>_POSES.png + <action>_preview.gif (the clip frames used)
import sys, os, subprocess, tempfile, glob, numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage
clip, act, N = sys.argv[1], sys.argv[2], int(sys.argv[3])
t0 = float(sys.argv[4]) if len(sys.argv) > 4 else 0; t1 = float(sys.argv[5]) if len(sys.argv) > 5 else None
cols = int(sys.argv[6]) if len(sys.argv) > 6 else (6 if N > 8 else 4)
OUT = 'art/incoming/side/berserker/poses/'; os.makedirs(OUT, exist_ok=True)
tmp = tempfile.mkdtemp()
dur = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', clip]).decode())
t1 = t1 if t1 is not None else dur
fr = []
for i in range(N):
    t = t0 + (t1 - t0) * i / N
    p = os.path.join(tmp, '%03d.png' % i); subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(t), '-i', clip, '-frames:v', '1', p], check=True)
    fr.append(Image.open(p).convert('RGB'))
def sil(im):
    a = np.asarray(im).astype(int); border = np.r_[a[0], a[-1], a[:, 0], a[:, -1]]; key = np.median(border, 0)
    far = np.abs(a - key).sum(2) > 60
    m = ndimage.binary_opening(far, iterations=1); lab, n = ndimage.label(m); sz = ndimage.sum(m, lab, range(1, n + 1))
    keep = np.isin(lab, [i + 1 for i, s in enumerate(sz) if s > sz.max() * .02]) if n else m
    yy = np.arange(a.shape[0])[:, None]
    dust = (a[..., 0] > 120) & (a[..., 0] - a[..., 2] > 25) & (a[..., 1] > 90) & (yy > a.shape[0] * .78) & (np.abs(a[..., 0] - a[..., 1]) < 60)
    return ndimage.binary_fill_holes(keep & ~dust)
ms = [sil(f) for f in fr]
ys = np.nonzero(np.any([m.any(1) for m in ms], 0))[0]; xs = np.nonzero(np.any([m.any(0) for m in ms], 0))[0]
y0, y1, x0, x1 = max(0, ys.min() - 20), ys.max() + 10, max(0, xs.min() - 20), xs.max() + 20
cw, ch = x1 - x0, y1 - y0; k = 460 / ch; cw, ch = int(cw * k), int(ch * k)
rows = (N + cols - 1) // cols; sheet = Image.new('RGB', (cw * cols, ch * rows), (255, 255, 255)); d = ImageDraw.Draw(sheet)
try: font = ImageFont.load_default(size=28)
except TypeError: font = ImageFont.load_default()
gif = []
for i, (m, f) in enumerate(zip(ms, fr)):
    s = Image.fromarray(np.where(m[y0:y1, x0:x1, None], np.array([150, 150, 158]), 255).astype(np.uint8)).resize((cw, ch), Image.LANCZOS)
    x, y = (i % cols) * cw, (i // cols) * ch; sheet.paste(s, (x, y))
    d.rectangle((x, y, x + cw - 1, y + ch - 1), outline=(200, 200, 200)); d.text((x + 10, y + 6), str(i + 1), fill=(60, 60, 60), font=font)
    gif.append(f.crop((x0, y0, x1, y1)).resize((cw // 2, ch // 2)).quantize(255))
sheet.save(OUT + act + '_POSES.png')
gif[0].save(OUT + act + '_preview.gif', save_all=True, append_images=gif[1:], duration=round(1000 * (t1 - t0) / N), loop=0)
print(act, N, 'frames from', t0, 'to', round(t1, 2), 's ->', OUT + act + '_POSES.png', sheet.size)
