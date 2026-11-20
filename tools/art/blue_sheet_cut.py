"""Cut a Codex / Meta move sheet on flat blue (#0248BA, a ground line in every cell) into a game strip.

  python tools/art/blue_sheet_cut.py <sheet.png> <out_prefix> [cols rows] [frame_height]

-> <out_prefix>.png   one row of frames, all the same size, cropped to the union box of every frame (so the character's
                      movement inside its cell is kept), feet on the ground line, smooth alpha edge, blue spill removed
   <out_prefix>.json  {"n", "w", "h", "foot": y of the ground line in the frame, "src"}
   <out_prefix>_preview.gif  for a quick look (half size, 12 fps)
Cells are a fixed grid (the sheets keep it). The ground line: the darkest long row in the lower 25 %% of each cell; pixels on it with
nothing of the figure just above are removed. frame_height (default: keep) resizes the strip (Lanczos) for the game.
"""
import sys, json
import numpy as np
from PIL import Image
from scipy import ndimage as nd

src, out = sys.argv[1], sys.argv[2]
C = int(sys.argv[3]) if len(sys.argv) > 3 else 4
Rn = int(sys.argv[4]) if len(sys.argv) > 4 else 4
FH = int(sys.argv[5]) if len(sys.argv) > 5 else 0
a = np.array(Image.open(src).convert('RGB')).astype(float); H, W = a.shape[:2]; cw, ch = W / C, H / Rn
r, g, b = a[..., 0], a[..., 1], a[..., 2]
blueness = np.clip(((b - np.maximum(r, g)) - 40) / 80, 0, 1)          # 1 = background blue, 0 = figure
cells, lines = [], []
for i in range(C * Rn):
    x0, y0 = int(round((i % C) * cw)), int(round((i // C) * ch)); x1, y1 = int(round((i % C + 1) * cw)), int(round((i // C + 1) * ch))
    c = a[y0:y1, x0:x1]; bl = blueness[y0:y1, x0:x1]; h, w = bl.shape
    fig = bl < .5
    dark = c.max(2) < 80; lo = int(h * .75); cnt = dark[lo:].sum(1); ly = lo + int(np.argmax(cnt)) if cnt.max() > w * .3 else None
    if ly is not None:
        for y in range(ly - 3, min(h, ly + 4)):
            above = fig[max(0, y - 10):max(0, y - 4)].any(0); fig[y] &= above
    fl, fn = nd.label(fig, structure=np.ones((3, 3)))
    if fn:
        sz = nd.sum(fig, fl, range(1, fn + 1)); fig = np.isin(fl, np.where(sz > max(60, sz.max() * .004))[0] + 1)
    alpha = np.clip(1 - bl, 0, 1) * nd.binary_dilation(fig, iterations=1)
    rgb = c.copy(); spill = np.clip(rgb[..., 2] - np.maximum(rgb[..., 0], rgb[..., 1]), 0, None) * (1 - alpha)   # take the blue out of soft edge pixels
    rgb[..., 2] -= spill
    cells.append(np.dstack([np.clip(rgb, 0, 255), alpha * 255]).astype(np.uint8)); lines.append(ly if ly is not None else h - 1)
hs, ws = min(c.shape[0] for c in cells), min(c.shape[1] for c in cells)
cells = [c[:hs, :ws] for c in cells]
foot = int(np.median(lines))
box = None
for c in cells:
    ys, xs = np.where(c[..., 3] > 20)
    if not len(ys): continue
    bb = [xs.min(), ys.min(), xs.max() + 1, ys.max() + 1]; box = bb if box is None else [min(box[0], bb[0]), min(box[1], bb[1]), max(box[2], bb[2]), max(box[3], bb[3])]
box[3] = max(box[3], foot + 2)
frames = [Image.fromarray(c, 'RGBA').crop(tuple(box)) for c in cells]
fw, fh = frames[0].size; footy = foot - box[1]
if FH:
    k = FH / fh; fw, fh = max(1, round(fw * k)), FH; footy = round(footy * k); frames = [f.resize((fw, fh), Image.LANCZOS) for f in frames]
strip = Image.new('RGBA', (fw * len(frames), fh))
for i, f in enumerate(frames): strip.alpha_composite(f, (i * fw, 0))
strip.save(out + '.png')
json.dump({'n': len(frames), 'w': fw, 'h': fh, 'foot': footy, 'src': src}, open(out + '.json', 'w'))
pv = [Image.alpha_composite(Image.new('RGBA', (fw, fh), (232, 214, 180, 255)), f).resize((max(1, fw // 2), max(1, fh // 2)), Image.LANCZOS).convert('P', palette=Image.ADAPTIVE, colors=255) for f in frames]
pv[0].save(out + '_preview.gif', save_all=True, append_images=pv[1:], duration=83, loop=0, disposal=2)
print(f'{len(frames)} frames {fw}x{fh}, foot at {footy} -> {out}.png')
