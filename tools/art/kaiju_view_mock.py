# Camera-angle mock for the kaiju city-smasher idea (owner 2026-11-15 "ลองจำลองมุมมาก่อน เผื่อผิด"): two quick drawings made in
# code, NOT game art: A = top view (camera straight down), B = isometric (base-building camera like kingdom.html).
#   python3 tools/art/kaiju_view_mock.py  -> art/incoming/kaiju/view_mock_top_vs_iso.png
import math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S = 2; W, H = 760, 520
OUT = 'art/incoming/kaiju/view_mock_top_vs_iso.png'
FONT = ImageFont.truetype('/usr/share/fonts/opentype/tlwg/Loma-Bold.otf', 26 * S)
OL = (24, 16, 26); BODY = (44, 36, 52); BODY2 = (70, 58, 82); PUR = (176, 60, 255); PUR2 = (226, 150, 255); EYE = (250, 220, 255)
random.seed(4)

def top_view():
    im = Image.new('RGB', (W * S, H * S), (92, 112, 84)); d = ImageDraw.Draw(im)
    road = (64, 66, 74); B = 150
    for x in range(-20, W, B): d.rectangle((x * S, 0, (x + 34) * S, H * S), fill=road)
    for y in range(-20, H, B): d.rectangle((0, y * S, W * S, (y + 34) * S), fill=road)
    for x in range(-20, W, B):
        for y in range(0, H, 24): d.rectangle(((x + 16) * S, y * S, (x + 18) * S, (y + 10) * S), fill=(220, 210, 150))
    for y in range(-20, H, B):
        for x in range(0, W, 24): d.rectangle((x * S, (y + 16) * S, (x + 10) * S, (y + 18) * S), fill=(220, 210, 150))
    roofs = [(196, 92, 70), (120, 132, 150), (210, 180, 120), (150, 90, 80), (110, 150, 130), (180, 180, 190)]
    cx, cy = W / 2, H / 2 + 20
    for bx in range(-20, W, B):
        for by in range(-20, H, B):
            x0, y0 = bx + 40, by + 40
            for (ox, oy, w, h) in ((0, 0, 50, 46), (56, 0, 48, 46), (0, 52, 104, 50)):
                r = roofs[random.randrange(len(roofs))]; X0, Y0 = x0 + ox, y0 + oy
                if math.hypot(X0 + w / 2 - cx, Y0 + h / 2 - cy) < 120:   # smashed near the monster: rubble
                    for _ in range(14):
                        rx, ry = X0 + random.random() * w, Y0 + random.random() * h; s = 3 + random.random() * 6
                        d.rectangle((rx * S, ry * S, (rx + s) * S, (ry + s) * S), fill=tuple(int(c * .7) for c in r), outline=OL)
                    continue
                d.rectangle(((X0 + 6) * S, (Y0 + 6) * S, (X0 + w + 6) * S, (Y0 + h + 6) * S), fill=(40, 46, 40))   # shadow
                d.rectangle((X0 * S, Y0 * S, (X0 + w) * S, (Y0 + h) * S), fill=r, outline=OL, width=2 * S)
                d.rectangle(((X0 + 4) * S, (Y0 + 4) * S, (X0 + w - 4) * S, (Y0 + 9) * S), fill=tuple(min(255, c + 30) for c in r))
                d.rectangle(((X0 + w - 16) * S, (Y0 + h - 16) * S, (X0 + w - 6) * S, (Y0 + h - 6) * S), fill=(150, 150, 160), outline=OL)
    # the kaiju seen from straight above, facing up
    sh = Image.new('L', im.size, 0); ImageDraw.Draw(sh).ellipse(((cx - 70 + 14) * S, (cy - 70 + 18) * S, (cx + 70 + 14) * S, (cy + 120 + 18) * S), fill=120)
    im.paste((20, 24, 20), (0, 0), sh.filter(ImageFilter.GaussianBlur(10 * S))); d = ImageDraw.Draw(im)
    P = lambda pts: [(x * S, y * S) for x, y in pts]
    d.polygon(P([(cx - 22, cy + 40), (cx + 22, cy + 40), (cx + 30, cy + 110), (cx + 8, cy + 170), (cx - 4, cy + 178), (cx - 14, cy + 120)]), fill=BODY, outline=OL, width=3 * S)   # tail
    for fx, fy in ((-46, -10), (46, -10), (-40, 46), (40, 46)): d.ellipse(((cx + fx - 16) * S, (cy + fy - 14) * S, (cx + fx + 16) * S, (cy + fy + 14) * S), fill=BODY2, outline=OL, width=3 * S)
    for fx, fy in ((-46, -24), (46, -24)):
        for k in (-8, 0, 8): d.polygon(P([(cx + fx + k - 3, cy + fy + 4), (cx + fx + k + 3, cy + fy + 4), (cx + fx + k, cy + fy - 6)]), fill=(240, 220, 240), outline=OL)
    d.ellipse(((cx - 48) * S, (cy - 50) * S, (cx + 48) * S, (cy + 62) * S), fill=BODY, outline=OL, width=3 * S)   # body
    d.ellipse(((cx - 30) * S, (cy - 92) * S, (cx + 30) * S, (cy - 32) * S), fill=BODY2, outline=OL, width=3 * S)   # head
    d.polygon(P([(cx - 18, cy - 86), (cx + 18, cy - 86), (cx + 12, cy - 118), (cx - 12, cy - 118)]), fill=BODY2, outline=OL, width=3 * S)   # snout
    for ex in (-13, 13): d.ellipse(((cx + ex - 6) * S, (cy - 80) * S, (cx + ex + 6) * S, (cy - 70) * S), fill=EYE, outline=PUR)
    for i in range(9):   # purple flames along the spine and tail, blowing back
        t = i / 8; x = cx + math.sin(i * 1.7) * 10; y = cy - 40 + t * 190; s = 34 - t * 18
        for side in (-1, 1):
            d.polygon(P([(x, y - s * .3), (x + side * s, y + s * .2), (x + side * s * .6, y + s * 1.3), (x + side * s * .2, y + s * .5)]), fill=PUR, outline=(90, 20, 140))
        d.ellipse(((x - s * .25) * S, (y - s * .2) * S, (x + s * .25) * S, (y + s * .5) * S), fill=PUR2)
    for a, b in (((cx - 30, cy - 10), (cx - 10, cy + 20)), ((cx + 26, cy + 4), (cx + 6, cy + 36)), ((cx - 20, cy + 40), (cx + 4, cy + 52))): d.line(P([a, b]), fill=PUR2, width=3 * S)
    return im

def iso_view():
    im = Image.new('RGB', (W * S, H * S), (126, 176, 88)); d = ImageDraw.Draw(im)
    T = 40
    def iso(gx, gy): return (W / 2 + (gx - gy) * T, 60 + (gx + gy) * T / 2)
    for gx in range(-2, 12):
        for gy in range(-2, 12):
            x, y = iso(gx, gy); road = gx % 4 == 1 or gy % 4 == 1
            d.polygon([(x * S, y * S), ((x + T) * S, (y + T / 2) * S), (x * S, (y + T) * S), ((x - T) * S, (y + T / 2) * S)], fill=(70, 72, 80) if road else (118, 168, 84), outline=(60, 90, 50) if not road else (58, 60, 66))
    roofs = [(196, 92, 70), (120, 132, 150), (210, 180, 120), (150, 90, 80)]
    cells = sorted([(gx, gy) for gx in range(0, 11) for gy in range(0, 11) if gx % 4 != 1 and gy % 4 != 1], key=lambda c: c[0] + c[1])
    k = (6.2, 5.2)
    for gx, gy in cells:
        if math.hypot(gx - k[0], gy - k[1]) < 1.8: continue
        x, y = iso(gx, gy); h = 20 + (gx * 7 + gy * 13) % 4 * 14; r = roofs[(gx + gy * 3) % 4]
        top = [(x, y - h), (x + T * .8, y + T * .4 - h), (x, y + T * .8 - h), (x - T * .8, y + T * .4 - h)]
        d.polygon([(a * S, b * S) for a, b in [(x - T * .8, y + T * .4 - h), (x, y + T * .8 - h), (x, y + T * .8), (x - T * .8, y + T * .4)]], fill=(196, 190, 176), outline=OL, width=S)
        d.polygon([(a * S, b * S) for a, b in [(x + T * .8, y + T * .4 - h), (x, y + T * .8 - h), (x, y + T * .8), (x + T * .8, y + T * .4)]], fill=(150, 144, 134), outline=OL, width=S)
        d.polygon([(a * S, b * S) for a, b in top], fill=r, outline=OL, width=S)
        if (gx, gy) == (7, 7) or (gx, gy) == (8, 6): pass
    try:
        sp = Image.open('art/incoming/kaiju/kaiju_px128.png').convert('RGBA'); sp = sp.resize((sp.width * 2 * S, sp.height * 2 * S), Image.NEAREST)
        x, y = iso(*k); im.paste(sp, (int(x * S - sp.width / 2), int((y + 20) * S - sp.height)), sp)
    except FileNotFoundError: pass
    return im

def label(im, txt):
    d = ImageDraw.Draw(im); d.rectangle((0, 0, im.width, 44 * S), fill=(24, 18, 30)); d.text((14 * S, 6 * S), txt, font=FONT, fill=(255, 236, 190)); return im

a = label(top_view(), 'A  ท็อปวิว: มองตรงลงมาจากฟ้า'); b = label(iso_view(), 'B  ไอโซเมตริก: แบบเกมสร้างฐาน (kingdom.html)')
out = Image.new('RGB', (W * 2 * S + 20 * S, H * S), (255, 255, 255)); out.paste(a, (0, 0)); out.paste(b, (W * S + 20 * S, 0))
out = out.resize((out.width // S, out.height // S), Image.LANCZOS); out.save(OUT); print(OUT, out.size)
