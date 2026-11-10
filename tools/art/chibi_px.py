# A GPT character picture on white -> clean pixel art at given heights (owner 2026-11-10 "ลองทำพิกเซลดู เอาแค่อาร์ตก่อน").
# Lanczos down + a light unsharp, one palette, single-pixel speckles merged into their surroundings, a dark 1-px outline.
#   python3 tools/art/chibi_px.py <picture.png> <out prefix> [heights=128,170] [colours=32]
#   (white background: tools/art/white_cut.py <in> <cut> --edge-only --no-ring first, or pass the cut file)
import sys, numpy as np
from PIL import Image, ImageFilter
def px(f, H, ncol=32):
    k = H / f.height; w, h = round(f.width * k), round(f.height * k)
    arr = np.asarray(f.resize((w, h), Image.LANCZOS)).copy(); m = arr[..., 3] > 128
    q = Image.fromarray(arr[..., :3]).filter(ImageFilter.UnsharpMask(1.2, 80, 2)).quantize(ncol, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    idx = np.asarray(q).copy(); pal = np.array(q.getpalette()[:ncol * 3]).reshape(-1, 3); out = idx.copy()
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            if not m[y, x]: continue
            nb = np.delete(idx[y - 1:y + 2, x - 1:x + 2].ravel(), 4); v, c = np.unique(nb, return_counts=True)
            if c.max() >= 7 and v[c.argmax()] != idx[y, x]: out[y, x] = v[c.argmax()]
    o = np.zeros((h + 2, w + 2, 4), np.uint8); o[1:-1, 1:-1, :3] = pal[out]; o[1:-1, 1:-1, 3] = m * 255
    al = o[..., 3] > 0; nb = np.zeros_like(al)
    for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)): nb |= np.roll(np.roll(al, dy, 0), dx, 1)
    o[nb & ~al] = (12, 6, 8, 255); return Image.fromarray(o)
if __name__ == '__main__':
    src, pre = sys.argv[1], sys.argv[2]; hs = [int(v) for v in (sys.argv[3] if len(sys.argv) > 3 else '128,170').split(',')]
    nc = int(sys.argv[4]) if len(sys.argv) > 4 else 32
    f = Image.open(src).convert('RGBA'); f = f.crop(f.getbbox()); outs = []
    for H in hs: p = px(f, H, nc); p.save(f'{pre}_{H}.png'); outs.append(p); print(H, p.size)
    z = Image.new('RGBA', (sum(o.width for o in outs) + 20 * (len(outs) + 1), max(o.height for o in outs) + 20), (92, 150, 62, 255)); x = 20
    for o in outs: z.alpha_composite(o, (x, z.height - 10 - o.height)); x += o.width + 20
    z.resize((z.width * 3, z.height * 3), Image.NEAREST).save(f'{pre}_x3.png')
