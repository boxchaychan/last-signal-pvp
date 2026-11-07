# "Only what is missing" package for one character's animation (owner 2026-11-07 "เอามาให้ครบ สั่งใหม่แค่ที่ขาด", after the
# 4-direction Wukong run came back with east idle + attack only). The missing work is split into small jobs, because the generator
# could not turn the character by itself: first a still turnaround (front, side, back), then each missing direction from that still.
#   python3 tools/art/legends_fill_pack.py <out dir> <key> <east frames picture | -> [jobs]
#     east frames picture = the frames that are already done (top row idle, bottom row attack), shown so the new ones match
#     -  = a new character with nothing done yet (owner 2026-11-07 "ตัวต่อไป" after asking for complete sets): turnaround, east, south, north
#     jobs = comma list from turn,east,east_skill,south,north (default: turn,east_skill,south,north, or turn,east,south,north with -)
# Run from the repo root. Writes <out dir>/fill_<key>.zip (reference picture, east_done.png, one prompt file per job, README_TH.txt).
import sys, os, zipfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from legends_codex import ANIM

out, key, done = sys.argv[1], sys.argv[2], sys.argv[3]
fresh = done == '-'
jobs = sys.argv[4].split(',') if len(sys.argv) > 4 else ['turn', 'east' if fresh else 'east_skill', 'south', 'north']
a = next(x for x in ANIM if x[0] == key)
k, en, th, desc, idle, an, asteps, sn, swhat, ssteps = a[:10]
extra = a[10] if len(a) > 10 else ''
st = lambda L: '\n'.join('  %d. %s' % (i + 1, x) for i, x in enumerate(L))

HEAD = ('Files: %s.png = the final design of %s (%s). It is the only reference: every frame must match it exactly: the same character, face, hair, '
        'outfit, colours, weapon and pixel-art detail.\n\n') % (key, en, desc) if fresh else ('Files: %s.png = the final design of %s (%s). east_done.png = the frames that are ALREADY DONE facing right (east): '
        'top row idle 4 frames, bottom row attack 6 frames. Do not redo them. Every new frame must match them exactly: the same character, face, hair, '
        'outfit, colours, weapon, size on the canvas and pixel-art detail.\n\n') % (key, en, desc)
RULES = (('SAME SCALE in every frame and every job: the same height as the figures in turnaround.png.' if fresh else 'SAME SCALE as east_done.png in every frame.') + ' Smooth animation: every frame is a small step from the one before; both feet on the same ground line '
         'unless a step says jump; hair, cape and cloth follow through and settle. Keep the whole body and weapon inside every frame. '
         'No detached effects (no swooshes, slash trails, projectiles, sparks, dust or shadows): the game draws those. Transparent background, no text.\n'
         + (extra + '\n' if extra else ''))
DELIVER = ('Deliver it like this: frames_full/ (every frame of this job as a 1024x1024 PNG on ONE shared canvas: the same scale and the same '
           'ground line for all of them, transparent background), clean/ (128x128 cells, one strip per action), previews/ (GIFs), generated/ (the untouched '
           'full-size generated images). Zip everything. Do not shrink the generated images.')

def direction(name, view, aim, still):
    return (HEAD + 'Job: the %s direction: %s. Use the %s of turnaround.png as the look for this direction. Actions, all facing this way:\n\n'
            'Idle (4 frames, a smooth loop): %s.\n\n'
            'Attack (6 frames) - %s:\n%s\n\n'
            'Skill (6 frames) - %s (in the game it %s):\n%s\n\n'
            '%s'
            % (name, view, still, idle, an, st(asteps), sn, swhat, st(ssteps),
               'In this direction "forward", "in front" and "to the right" in the steps mean %s.\n' % aim if aim else '')) + RULES + DELIVER

P = {}
P['turn'] = (HEAD + 'Job: ONE still picture, a character turnaround. Draw this exact character three times side by side, standing in the same idle stance as '
             + ('the reference' if fresh else 'the first idle frame') + ', the same size and on the same ground line:\n'
             '  1. FRONT view: facing the viewer (south), both eyes and the whole face visible\n'
             '  2. SIDE view: facing right (east), the same three-quarter view as ' + ('the reference' if fresh else 'east_done.png') + '\n'
             '  3. BACK view: back to the viewer (north): the back of the hair, the back of the outfit, cape or scarf ends, and the weapon as it would look from behind\n'
             'Every costume part, colour and the weapon stay the same in all three views; only the camera moves around the character. '
             'Full size, pixel art like the reference, transparent or plain white background, no text, no labels, no effects. Save it as turnaround.png.')
P['east_skill'] = (HEAD + 'Job: the missing SKILL row facing right (east), 6 frames - %s (in the game it %s):\n%s\n\n' % (sn, swhat, st(ssteps)) + RULES + DELIVER)
P['east'] = direction('EAST', 'the character faces right, the same three-quarter view as the reference', '', 'SIDE view')
P['south'] = direction('SOUTH', 'the character faces the viewer (toward the camera)', 'toward the viewer (down the screen)', 'FRONT view')
P['north'] = direction('NORTH', 'the character has the back to the viewer (away from the camera)', 'away from the viewer (up the screen)', 'BACK view')
FN = {'turn': '1_TURNAROUND.txt', 'east': '2_EAST.txt', 'east_skill': '2_EAST_SKILL.txt', 'south': '3_SOUTH.txt', 'north': '4_NORTH.txt'}
TH = {'turn': 'รูปหมุนตัว 3 ด้าน (หน้า ข้าง หลัง) รูปเดียวนิ่งๆ', 'east': 'หันขวา 3 ท่า (ยืน ตี ไม้ตาย)', 'east_skill': 'ท่าไม้ตาย หันขวา', 'south': 'หันหน้าเข้าจอ 3 ท่า (ยืน ตี ไม้ตาย)', 'north': 'หันหลัง 3 ท่า (ยืน ตี ไม้ตาย)'}
steps = ''.join('%d. พิมพ์: ทำตาม %s  → %s\r\n' % (i + 1, FN[j], TH[j]) for i, j in enumerate(jobs))
readme = ('%s (%s): ' + ('ท่าครบ 4 ทิศ (ซ้าย = เกมกลับภาพจากขวาให้เอง)' if fresh else 'สั่งเฉพาะส่วนที่ยังขาด') + '\r\n\r\n'
          'ทำในแชตเดียวกัน ทีละงาน: แนบ zip นี้ครั้งแรกครั้งเดียว แล้วพิมพ์ทีละบรรทัด\r\n%s\r\n'
          'ทำไมต้องวาดรูปหมุนตัวก่อน: ตัววาดหมุนตัวละครไปหันหน้า/หันหลังเองไม่ได้ (ลองกับซุนหงอคงแล้ว) ให้วาดรูปนิ่งๆ ของแต่ละด้านก่อน แล้วค่อยทำท่าจากรูปนั้น\r\n'
          'ถ้ารูปหันหน้าหรือหันหลังไม่เหมือนตัวเดิม ให้สั่งข้อ 1 ใหม่จนเหมือนก่อน แล้วค่อยทำข้อต่อไป\r\n\r\n'
          'แต่ละงานเสร็จ ดาวน์โหลด zip ส่งให้ Claude ได้เลย ไม่ต้องรอครบทุกงาน (ห้ามย่อไฟล์)\r\n') % (th, en, steps)
os.makedirs(out, exist_ok=True)
zp = os.path.join(out, ('anim4_%s.zip' if fresh else 'fill_%s.zip') % key)
with zipfile.ZipFile(zp, 'w', zipfile.ZIP_DEFLATED) as z:
    z.write('art/incoming/legends/%s.png' % key, key + '.png')
    if not fresh: z.write(done, 'east_done.png')
    for j in jobs: z.writestr(FN[j], P[j] + '\n')
    z.writestr('README_TH.txt', readme.encode('utf-8-sig'))
print(zp, os.path.getsize(zp))
