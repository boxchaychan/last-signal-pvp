"""The owner's 16-frame "throw the bolt" row (bottom of art/incoming/zeus_sheet/owner_sheet_raw.png) cut into frames, nothing redrawn, effects kept.
Background (flat dark grey) taken out by colour distance with a soft edge; every frame on one canvas, feet on one line, body centred.
  python3 tools/art/zeus_throw_cut.py  -> art/incoming/zeus_sheet/throw16/f01..f15.png + sheet.png + throw.gif (x3, 1/15 s a frame)"""
import os, numpy as np
from PIL import Image
from scipy import ndimage as nd
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'); OUT = os.path.join(R, 'art/incoming/zeus_sheet/throw16')
A = np.asarray(Image.open(os.path.join(R, 'art/incoming/zeus_sheet/owner_sheet_raw.png')).convert('RGB')).astype(np.float32); Y0, Y1 = 848, 976
row = A[Y0:Y1]; bg = np.median(row.reshape(-1, 3), 0); d = np.abs(row - bg).sum(2); m = nd.binary_closing(d > 45, iterations=3); lab, n = nd.label(m)
objs = sorted([sl for i, sl in enumerate(nd.find_objects(lab)) if (lab[sl] == i + 1).sum() > 300], key=lambda s: s[1].start)
CW, CH, FOOT = 150, 132, 124; frames = []
for i, sl in enumerate(objs):
    x0, x1 = sl[1].start - 4, sl[1].stop + 4; a = row[:, x0:x1]; dd = np.abs(a - bg).sum(2); al = np.clip((dd - 25) / 45, 0, 1)
    keep = nd.binary_dilation(lab[:, x0:x1] > 0, iterations=3); al *= keep; im = Image.fromarray(np.dstack([a, al * 255]).astype(np.uint8), 'RGBA')
    ys, xs = np.nonzero(al > .5); body = al[:, :] > .5; cx = np.median(xs) if len(xs) else im.width / 2; bot = ys.max() if len(ys) else 0
    c = Image.new('RGBA', (CW, CH), (0, 0, 0, 0)); is_bolt = (sl[0].stop - sl[0].start) < 60   # frame 10 = the bolt alone, flying
    c.alpha_composite(im, (int(CW / 2 - (im.width / 2 if is_bolt else cx)), int((FOOT - 40 - im.height / 2) if is_bolt else FOOT - bot)))
    c.save(os.path.join(OUT, f'f{i + 1:02d}.png')); frames.append(c)
sh = Image.new('RGBA', (CW * len(frames), CH), (0, 0, 0, 0))
for i, f in enumerate(frames): sh.alpha_composite(f, (i * CW, 0))
sh.save(os.path.join(OUT, 'sheet.png'))
big = [Image.alpha_composite(Image.new('RGBA', (CW, CH), (61, 83, 200, 255)), f).resize((CW * 3, CH * 3), Image.LANCZOS).convert('RGB') for f in frames]
dur = [140, 90, 90, 110, 80, 70, 70, 60, 60, 60, 70, 90, 110, 120, 400][:len(big)]
big[0].save(os.path.join(OUT, 'throw.gif'), save_all=True, append_images=big[1:], duration=dur, loop=0); print(len(frames), 'frames')
