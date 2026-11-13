# The standard motion library (owner 2026-11-13: "เราเก็บแบบไว้ใช้ได้กับทุกตัว สแตนดาร์ด"): reference sheets made from OUR OWN pixel heroes'
# PixelLab moves (side view, facing right). Attach one sheet + a character picture to GPT with the prompt next to it and it draws
# that character in the same poses; any style (pixel or painted). Free, no jobs.
# Two groups (owner: "แยกท่าออกมา วิ่ง / ฟันดาบ เพราะมันใช้เฉพาะนักดาบ"): common/ = every character uses them (idle, run, roll, hurt, death);
# weapon/ = only characters with that kind of weapon (sword_slash, bow_shoot, staff_cast). A new character = common set + ONE weapon sheet.
#   python3 tools/art/pose_lib.py -> art/poses/std/{common,weapon}/<move>.png (1536x1024, 4x2 numbered cells), .json, PROMPT_<move>.txt ; index.png
import glob, json, os
from PIL import Image, ImageDraw, ImageFont
A = 'art/incoming/action/'; O = 'art/poses/std/'; os.makedirs(O, exist_ok=True); CW, CH, GY = 384, 512, 452
#  move: (frames folder, loop?, Thai name, what it is for the prompt, weapon note)
LIB = {   # key: 'group/move'
 'common/idle':        (A + 'swordsman/pl_dl/Idle/animations/idle/east', 1, 'ยืนหายใจ', 'a standing IDLE (breathing) loop', 'held in the same resting position in every cell'),
 'common/run':       (A + 'swordsman/pl_dl/Idle/animations/run/east', 1, 'วิ่ง', 'a RUN cycle', 'carried in the same position in every cell'),
 'weapon/sword_slash':      (A + 'swordsman/pl_dl/Idle/animations/attack/east', 0, 'ฟัน (อาวุธระยะใกล้)', 'a melee weapon ATTACK: wind-up, a wide swing, recovery', 'swung the way the reference weapon is swung'),
 'weapon/bow_shoot':      (A + 'archer/pl_dl/Idle/animations/attack/east', 0, 'ยิง (ธนู / ปืน)', 'a ranged SHOT: aim, release, recoil, recovery', 'aimed forward to the right like the reference bow'),
 'weapon/staff_cast':       (A + 'mage/pl_dl/Idle/animations/attack/east', 0, 'ร่ายเวท / ปา', 'a spell CAST or throw: gather, thrust forward, recovery', 'held like the reference staff'),
 'common/roll':       (A + 'swordsman/pl_dl/Idle/animations/roll/east', 0, 'กลิ้งหลบ', 'a forward dodge ROLL', 'kept close to the body'),
 'common/hurt':       (A + 'swordsman/pl_dl/Idle/animations/hurt/east', 0, 'โดนตี', 'a HURT flinch: knocked back, then recovering', 'still in the hand'),
 'common/death':      (A + 'swordsman/pl_dl/Idle/animations/death/east', 0, 'ล้ม', 'a DEFEAT fall: stagger, fall, lying on the ground', 'dropped or still in the hand like the reference'),
}
PROMPT = '''(แนบ 2 รูปตามลำดับ: รูปที่ 1 = {move}.png (แผ่นท่ามาตรฐาน "{th}") · รูปที่ 2 = รูปตัวละครที่จะให้ทำท่า · แล้ววางข้อความด้านล่างทั้งหมด ได้ภาพแล้วส่งกลับมาเป็นไฟล์)

The FIRST picture is a motion reference: 8 numbered cells in a 4 x 2 grid showing {what} of another character, seen from the side, facing RIGHT.{loop} Use it ONLY for the poses (body lean, arm and leg positions, which foot is on the ground, how the weapon moves). Do not copy that character's look.

The SECOND picture is the character to draw. Draw THIS character once in every cell, in the same pose as the reference figure of that cell.

Rules:
- The same character in all 8 cells: same face, colours, outfit and proportions as the second picture, the SAME SIZE in every cell, seen from the side facing right. If the character has a weapon, it is {weapon}; if it has none, the hands do the same motion empty.
- Keep the 4 x 2 grid and the order 1 to 8 (top row left to right, then the bottom row). One figure per cell, placed like the reference, feet on the same ground line, nothing crossing into another cell.
- Do NOT draw the numbers, the cell borders or the ground line. No motion lines, no swoosh, no dust, no effects, no shadow, no text.
- Same art style as the second picture.
- Plain flat pure white background. Landscape picture, 1536 x 1024.
'''
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 30); thumbs = []
for key, (folder, loop, th, what, weapon) in LIB.items():
    grp, mv = key.split('/'); os.makedirs(O + grp, exist_ok=True); P = O + grp + '/'
    fs = sorted(glob.glob(folder + '/*.png')); fr = [Image.open(f).convert('RGBA') for f in fs]
    if not loop and len(fr) > 8: fr = fr[1:] if len(fr) % 2 else fr          # 9 or 17 frames: frame 0 is the standing reference
    idx = [round(i * (len(fr) - (0 if loop else 1)) / (8 if loop else 7)) % len(fr) for i in range(8)]
    bb = [fr[i].getbbox() for i in idx]; l = min(b[0] for b in bb); t = min(b[1] for b in bb); r = max(b[2] for b in bb); bt = max(b[3] for b in bb); w, h = r - l, bt - t
    k = max(1, min((CW - 24) // w, (CH - 90) // h)); im = Image.new('RGB', (CW * 4, CH * 2), (255, 255, 255)); d = ImageDraw.Draw(im)
    for n, i in enumerate(idx):
        ox, oy = n % 4 * CW, n // 4 * CH; c = fr[i].crop((l, t, r, bt)).resize((w * k, h * k), Image.NEAREST); d.rectangle((ox, oy, ox + CW - 1, oy + CH - 1), outline=(190, 190, 190))
        im.paste(c, (ox + (CW - w * k) // 2, oy + GY - h * k), c); d.line((ox + 12, oy + GY + 2, ox + CW - 12, oy + GY + 2), fill=(150, 150, 150), width=3); d.text((ox + 12, oy + 8), str(n + 1), fill=(90, 90, 90), font=F)
    im.save(P + mv + '.png'); json.dump({'move': mv, 'group': grp, 'th': th, 'loop': bool(loop), 'cell': [CW, CH], 'grid': [4, 2], 'ground': GY, 'scale': k, 'box': [w, h], 'frames': idx, 'source': folder}, open(P + mv + '.json', 'w'), ensure_ascii=False)
    open(P + 'PROMPT_' + mv + '.txt', 'w').write(PROMPT.format(move=mv, th=th, what=what, weapon=weapon, loop=' It is a loop: after cell 8 comes cell 1 again.' if loop else ' Cell 1 is the start, cell 8 is the end.'))
    thumbs.append((key, th, im.resize((384, 256), Image.LANCZOS))); print(mv, len(fs), idx, 'x%d' % k)
ix = Image.new('RGB', (384 * 2 + 30, (256 + 34) * 4 + 10), (245, 243, 232)); d = ImageDraw.Draw(ix); F2 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 20)
for i, (mv, th, t) in enumerate(thumbs): x, y = 10 + i % 2 * 394, 10 + i // 2 * 290; d.text((x, y), mv, fill=(30, 30, 30), font=F2); ix.paste(t, (x, y + 28))
ix.save(O + 'index.png')
