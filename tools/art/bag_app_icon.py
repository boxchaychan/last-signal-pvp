"""The home-screen icon of bag3d.html (art/bag3d/app192.png, app512.png): the knight class's first pose (the Tripo demon knight since
2026-11-28) on a dark rounded square with a warm glow and a gold rim. Free, made from our own render:
  python3 -m http.server 8000 ; node tools/art/cls_portraits.js --icon ; python3 tools/art/bag_app_icon.py"""
from PIL import Image, ImageDraw, ImageFilter
src = Image.open('/tmp/bag_icon/knight512.png').convert('RGBA')
cell = src.crop((0, 0, 512, 512)); bb = cell.getbbox(); body = cell.crop(bb)
N = 1024; bg = Image.new('RGBA', (N, N), (0, 0, 0, 0)); d = ImageDraw.Draw(bg)
d.rounded_rectangle((16, 16, N - 16, N - 16), 150, fill=(22, 12, 30, 255))
glow = Image.new('RGBA', (N, N), (0, 0, 0, 0)); ImageDraw.Draw(glow).ellipse((N * .18, N * .26, N * .82, N * .9), fill=(255, 150, 40, 150)); glow = glow.filter(ImageFilter.GaussianBlur(90))
mask = Image.new('L', (N, N), 0); ImageDraw.Draw(mask).rounded_rectangle((16, 16, N - 16, N - 16), 150, fill=255)
bg.alpha_composite(Image.composite(glow, Image.new('RGBA', (N, N), (0, 0, 0, 0)), mask))
h = int(N * .8); w = int(body.width * h / body.height)
if w > N * .86: w = int(N * .86); h = int(body.height * w / body.width)
body = body.resize((w, h), Image.LANCZOS); bg.alpha_composite(body, ((N - w) // 2, int(N * .9) - h))
ImageDraw.Draw(bg).rounded_rectangle((16, 16, N - 16, N - 16), 150, outline=(232, 184, 74, 255), width=18)
for s in (512, 192): bg.resize((s, s), Image.LANCZOS).save(f'art/bag3d/app{s}.png'); print(f'art/bag3d/app{s}.png')
