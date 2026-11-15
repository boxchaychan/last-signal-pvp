# Kaiju top view (GPT picture, facing up, on green) -> pixel sprite + turning test (owner 2026-11-15 "แล้วเวลามันหันละ").
#   python3 tools/art/kaiju_top_cut.py  -> art/incoming/kaiju/kaiju_top_cut.png, kaiju_top_px.png (+ _raw), kaiju_turn8.png, kaiju_turn.gif
# One picture is enough in a top view: every direction = the same picture rotated (each rotation made from the big picture, then pixelised).
import subprocess, numpy as np
from PIL import Image
D = 'art/incoming/kaiju/'; PX = 112   # sprite height in game pixels (head to tail tip)
im = np.array(Image.open(D + 'gpt_kaiju_topview.webp').convert('RGB')).astype(float)
r, g, b = im[..., 0], im[..., 1], im[..., 2]; gr = g - np.maximum(r, b)
a = np.clip(1 - (gr - 30) / 50, 0, 1)                      # greener than red / blue = background (its soft green shadow goes too)
out = im.copy(); out[..., 1] = np.where(a < 1, np.minimum(g, np.maximum(r, b) + 10), g)
cut = Image.fromarray(np.dstack([out, a * 255]).clip(0, 255).astype(np.uint8)); cut = cut.crop(cut.getbbox()); cut.save(D + 'kaiju_top_cut.png')
def pixel(big, h=PX):
    s = big.resize((round(big.width * h / big.height), h), Image.LANCZOS); x = np.array(s); x[..., 3] = np.where(x[..., 3] > 110, 255, 0)
    Image.fromarray(x).save('/tmp/_k.png'); subprocess.run(['python3', 'tools/art/pixel_punch.py', '/tmp/_k.png', '/tmp/_kp.png', '1.0', '24'], check=True)
    return Image.open('/tmp/_kp.png').convert('RGBA')
p = pixel(cut); p.save(D + 'kaiju_top_px.png'); Image.open('/tmp/_k.png').save(D + 'kaiju_top_px_raw.png')
# turning: rotate the big picture (square canvas so nothing is cut), then pixelise at the same scale
side = int(max(cut.size) * 1.05); sq = Image.new('RGBA', (side, side)); sq.paste(cut, ((side - cut.width) // 2, (side - cut.height) // 2), cut)
k = PX / cut.height; H = round(side * k)
def rot(deg): return pixel(sq.rotate(-deg, Image.BICUBIC), H)
ground = (88, 92, 100, 255); Z = 3
frames8 = [rot(d) for d in range(0, 360, 45)]
sheet = Image.new('RGBA', (H * 8 * Z + 9 * 10, H * Z + 20), ground)
for i, f in enumerate(frames8): sheet.alpha_composite(f.resize((H * Z, H * Z), Image.NEAREST), (10 + i * (H * Z + 10), 10))
sheet.convert('RGB').save(D + 'kaiju_turn8.png')
gif = []
for d in list(range(0, 360, 15)):
    f = rot(d); c = Image.new('RGBA', (H * Z, H * Z), ground); c.alpha_composite(f.resize((H * Z, H * Z), Image.NEAREST)); gif.append(c.convert('RGB'))
gif[0].save(D + 'kaiju_turn.gif', save_all=True, append_images=gif[1:], duration=90, loop=0)
print('ok', p.size, H)
