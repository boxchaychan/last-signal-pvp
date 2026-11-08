# Preview a PixelLab animation folder (frame_000.png ...) for the owner: numbered frame sheet + a GIF at game speed
# + a slow numbered GIF. Owner 2026-11-08 (dagger rogue attack tests).
#   python3 tools/art/pl_preview.py <frames dir> <out prefix> [fps=20] [scale=2] [labels e.g. 3:HIT1,9:HIT2]
# Writes <prefix>_sheet.png, <prefix>.gif, <prefix>_slow.gif (3.3 fps).
import sys, glob, os
from PIL import Image, ImageDraw, ImageFont

src, pre = sys.argv[1], sys.argv[2]
fps = float(sys.argv[3]) if len(sys.argv) > 3 else 20
K = int(sys.argv[4]) if len(sys.argv) > 4 else 2
lab = {}
if len(sys.argv) > 5:
    for p in sys.argv[5].split(','):
        i, t = p.split(':'); lab[int(i)] = t
fr = [Image.open(f).convert('RGBA') for f in sorted(glob.glob(os.path.join(src, 'frame_*.png')))]
W, H = fr[0].size; BG = (126, 170, 92, 255)
F = ImageFont.truetype(r'C:\Windows\Fonts\arialbd.ttf', 22)

def tile(f, i, big=False):
    b = Image.alpha_composite(Image.new('RGBA', f.size, BG), f).resize((W * K, H * K), Image.NEAREST)
    if big is not None:
        ImageDraw.Draw(b).text((6, 4), f'{i} {lab.get(i, "")}', font=F, fill='white', stroke_width=3, stroke_fill='black')
    return b

cols = min(6, len(fr)); rows = (len(fr) + cols - 1) // cols
sheet = Image.new('RGBA', (cols * (W * K + 4) + 4, rows * (H * K + 4) + 4), (60, 80, 50, 255))
for i, f in enumerate(fr):
    sheet.paste(tile(f, i), (4 + (i % cols) * (W * K + 4), 4 + (i // cols) * (H * K + 4)))
sheet.save(pre + '_sheet.png')
g = [tile(f, i, None).convert('P', palette=Image.ADAPTIVE) for i, f in enumerate(fr)]
g[0].save(pre + '.gif', save_all=True, append_images=g[1:], duration=[400] + [round(1000 / fps)] * (len(g) - 1), loop=0)
s = [tile(f, i).convert('P', palette=Image.ADAPTIVE) for i, f in enumerate(fr)]
s[0].save(pre + '_slow.gif', save_all=True, append_images=s[1:], duration=[600] + [300] * (len(s) - 1), loop=0)
print(len(fr), 'frames', W, 'x', H)
