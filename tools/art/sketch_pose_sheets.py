# The owner's slash-combo sketch (art/poses/ref_sketch/slash_sketch_ref.png, 736x385, somebody's rough animation: a little
# swordsman doing two side slashes, an overhead chop, a spin and a dash slash; used ONLY as a motion reference) cut into numbered
# pose sheets in our format (4x2 cells), so GPT / Meta can redraw OUR character in those poses, one move per picture.
# Frames overlap in the sketch, so each one has a hand-set box. Enlarged x2.6, feet on one line.
#   python3 tools/art/sketch_pose_sheets.py -> art/poses/ref_sketch/slash_{A,B,C,D}.png + PROMPT_slash_*.txt + CHAR_swordsman16_side.png
from PIL import Image, ImageDraw, ImageFont
D = 'art/poses/ref_sketch/'; S = Image.open(D + 'slash_sketch_ref.png').convert('RGB'); BG = (186, 186, 186)
R = [(20, 97), (99, 190), (196, 282), (284, 371)]
X = [[(11, 92), (98, 155), (160, 245), (245, 372), (378, 440), (440, 498), (492, 632), (632, 722)],
     [(11, 95), (98, 182), (183, 322), (322, 422), (425, 514), (516, 612), (610, 725)],
     [(15, 125), (131, 245), (254, 364), (370, 483), (491, 615), (634, 721)],
     [(31, 92), (100, 250), (255, 382), (385, 480), (480, 578), (581, 645), (651, 711)]]
MOVES = {'A': ('two fast horizontal slashes, left to right and back', [(0, i) for i in range(8)]),
         'B': ('an overhead chop down to the ground, then winding into a spin', [(1, i) for i in range(7)] + [(2, 0)]),
         'C': ('a spinning slash (frames 1-3), then a running dash into a wide slash (frames 4-8)', [(2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (3, 0), (3, 1), (3, 2)]),
         'D': ('the end of the dash slash: follow-through and back to the ready stance', [(3, 3), (3, 4), (3, 5), (3, 6)])}
CW, CH, K, GY = 384, 320, 2.6, 290; F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 30)
base = open('art/poses/std/weapon/PROMPT_sword_slash.txt').read().split('\n\n', 1)[1]
for name, (desc, fr) in MOVES.items():
    n = len(fr); rows = -(-n // 4); im = Image.new('RGB', (CW * 4, CH * rows), BG); d = ImageDraw.Draw(im)
    for j, (r, i) in enumerate(fr):
        x0, x1 = X[r][i]; y0, y1 = R[r]; c = S.crop((x0, y0, x1, y1)); c = c.resize((round(c.width * K), round(c.height * K)), Image.LANCZOS)
        ox, oy = j % 4 * CW, j // 4 * CH; im.paste(c, (ox + (CW - c.width) // 2, oy + GY - c.height))
        d.rectangle((ox, oy, ox + CW - 1, oy + CH - 1), outline=(120, 120, 120)); d.text((ox + 10, oy + 6), str(j + 1), fill=(60, 60, 60), font=F)
    im.save(D + 'slash_%s.png' % name)
    p = ("(แนบ 2 รูปตามลำดับ: รูปที่ 1 = slash_%s.png (แบบท่า) · รูปที่ 2 = CHAR_swordsman16_side.png (ตัวละคร) · แล้ววางข้อความด้านล่างทั้งหมด · ได้ภาพแล้วส่งกลับมาเป็นไฟล์)\n\n" % name
         + "The FIRST picture is a motion reference: %d numbered cells in a grid, a rough sketch of a small swordsman doing %s. Cell 1 is the start. Use it ONLY for the poses and the timing (body lean, legs, where the sword is, how big the slash arc is). Do not copy that sketch character's look.\n\n" % (n, desc)
         + "The SECOND picture is the character to draw: a chibi pixel-art swordsman (dark violet messy hair with an ahoge, violet eyes, torn red scarf-cape, white shirt, brown belt and gauntlets, dark trousers, brown boots, a straight silver sword with a gold guard in his right hand). Draw THIS character once in every cell, in the same pose as the sketch figure of that cell.\n\n"
         + "Rules:\n- The same character in all %d cells: same face, hair, colours, outfit and proportions as the second picture, the SAME SIZE in every cell, in the same chunky 16-bit pixel-art style (square pixels on one grid, dark outline, 3 shade steps), seen from the side, facing RIGHT unless the sketch figure of that cell is turned.\n" % n
         + "- Keep the grid and the order 1 to %d (left to right, top row first). One figure per cell with empty space around it, feet on the same ground line, nothing crossing into another cell.\n" % n
         + "- Where the sketch shows a slash arc, draw a clean white-blue slash arc of the same shape and size, kept inside its own cell. No other effects, no dust, no shadow.\n"
         + "- Do NOT draw the numbers or the cell borders.\n- Plain flat pure white background. Landscape picture, 1536 x %d.\n" % (1024 if rows == 2 else 512))
    open(D + 'PROMPT_slash_%s.txt' % name, 'w').write(p)
h = Image.open('art/td/map1/hero_chibi16.png').convert('RGBA').crop((113, 0, 226, 130)); h = h.resize((h.width * 6, h.height * 6), Image.NEAREST)
c = Image.new('RGBA', (1024, 1024), (255, 255, 255, 255)); c.alpha_composite(h, ((1024 - h.width) // 2, 960 - h.height)); c.convert('RGB').save(D + 'CHAR_swordsman16_side.png'); print('ok')
