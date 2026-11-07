# Animation package split into small jobs, ONE picture per prompt (owner 2026-11-07).
# History: the 4-direction Wukong run came back with east idle + attack only ("เอามาให้ครบ สั่งใหม่แค่ที่ขาด"), so the work was split:
# first a still turnaround (front, side, back) because the generator could not turn the character by itself (that worked), then each
# direction from that still. The first version asked for whole run folders per direction (frames_full, clean sheets, GIFs) and the
# generator did not make them ("มันเจนไม่ได้ แก้พรอมต์ใหม่"), so now every prompt asks for ONE image only: one action in a small grid
# (idle 2x2, attack / skill 3x2), white background. Claude cuts the cells, lines them up and builds the sheets itself.
#   python3 tools/art/legends_fill_pack.py <out dir> <key> <east frames picture | -> [--turn=<turnaround.png>] [jobs]
#     east frames picture = frames already done facing right (top row idle, bottom row attack), so the new ones match;
#                           -  = a new character with nothing done yet
#     --turn=<png>        = a turnaround that is already made (put in the zip, the turnaround job is skipped)
#     jobs                = comma list of turn, east_idle, east_attack, east_skill, south_idle, ..., north_skill
#                           (default: everything a new character needs, or turn + east_skill + south_* + north_* when east is done)
# Run from the repo root. Writes <out dir>/anim4_<key>.zip (new) or fill_<key>.zip (missing parts).
import sys, os, zipfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from legends_codex import ANIM

args = [x for x in sys.argv[1:] if not x.startswith('--turn=')]
turnpng = next((x[7:] for x in sys.argv[1:] if x.startswith('--turn=')), None)
out, key, done = args[0], args[1], args[2]
fresh = done == '-'
ACTS = ['idle', 'attack', 'skill']
if len(args) > 3: jobs = args[3].split(',')
else:
    jobs = ['turn'] + (['east_' + x for x in ACTS] if fresh else ['east_skill']) + ['south_' + x for x in ACTS] + ['north_' + x for x in ACTS]
if turnpng and 'turn' in jobs: jobs.remove('turn')
a = next(x for x in ANIM if x[0] == key)
k, en, th, desc, idle, an, asteps, sn, swhat, ssteps = a[:10]
extra = a[10] if len(a) > 10 else ''
st = lambda L: '\n'.join('  %d. %s' % (i + 1, x) for i, x in enumerate(L))

REF0 = ('Attached: %s.png = the final design of %s (%s)' % (key, en, desc)
       + ('' if fresh else '; east_done.png = frames already made facing right (match their size and detail, do not redo them)'))
REF = REF0 + '; turnaround.png = the same character from the front, the side and the back.\n\n'

TURN = (REF0 + '.\n\n' + 'Make ONE image, a character turnaround: draw this exact character three times side by side, standing in the same idle stance as the reference, '
        'the same size and on the same ground line:\n'
        '  1. FRONT view: facing the viewer (south), both eyes and the whole face visible\n'
        '  2. SIDE view: facing right (east), the same three-quarter view as the reference\n'
        '  3. BACK view: back to the viewer (north): the back of the hair, the back of the outfit, cape or scarf ends, and the weapon as it would look from behind\n'
        'Every costume part, colour and the weapon stay the same in all three views; only the camera moves around the character. '
        'Full size, pixel art like the reference, plain white background, no text, no labels, no effects. Save it as turnaround.png. '
        'Do ONLY this one picture now, even if other job files are attached: the animation frames come in later messages, one picture each.')

VIEW = {'east': ('facing right (east)', 'SIDE view', ''),
        'south': ('facing the viewer (south, toward the camera)', 'FRONT view',
                  'Facing the viewer: "forward", "in front" and "to the right" in the steps mean toward the viewer (down the picture).\n'),
        'north': ('with the back to the viewer (north, away from the camera)', 'BACK view',
                  'Back to the viewer: "forward", "in front" and "to the right" in the steps mean away from the viewer (up the picture).\n')}

def pic(d, act):
    look, view, aim = VIEW[d]
    n = 4 if act == 'idle' else 6
    grid = '2 columns x 2 rows' if n == 4 else '3 columns x 2 rows'
    if act == 'idle': title, body = 'Idle, 4 frames, a smooth loop (frame 4 leads back to frame 1)', '  ' + idle + '. Only small changes between frames.'
    elif act == 'attack': title, body = 'Attack, 6 frames - ' + an, st(asteps)
    else: title, body = 'Skill, 6 frames - %s (in the game it %s)' % (sn, swhat), st(ssteps)
    return (REF + 'Make ONE image: %s %s, drawn exactly like the %s in turnaround.png. ' % (en, look, view)
            + 'A sprite sheet of %d frames in a grid of %s, read left to right, top row first. ' % (n, grid)
            + 'All cells the same size, empty space around the figure in every cell, nothing touching the next cell. '
            'The character is the same size in every frame as in turnaround.png' + ('' if fresh else ' and east_done.png')
            + ', feet on the same line in every cell unless a step says jump. Plain white background. No text, no numbers, no motion lines, no effects.\n\n'
            + title + ':\n' + body + '\n\n' + aim + (extra + '\n' if extra and (act == 'skill' or 'skill frames' not in extra) else '')
            + 'Same pixel-art style, colours and detail as the reference. Give me only this one image; no other files are needed. '
            'Do ONLY this one picture now, even if other job files are attached: the other directions and actions come in later messages.')

P = {'turn': TURN}
NUM = {'east': '2', 'south': '3', 'north': '4'}; LET = {'idle': 'a', 'attack': 'b', 'skill': 'c'}
DTH = {'east': 'หันขวา', 'south': 'หันหน้าเข้าจอ', 'north': 'หันหลัง'}; ATH = {'idle': 'ท่ายืน 4 ภาพ', 'attack': 'ท่าตี 6 ภาพ', 'skill': 'ท่าไม้ตาย 6 ภาพ'}
FN = {'turn': '1_TURNAROUND.txt'}; TH = {'turn': 'รูปนิ่ง 3 ด้าน (หน้า ข้าง หลัง)'}
for d in VIEW:
    for x in ACTS:
        j = d + '_' + x; P[j] = pic(d, x)
        FN[j] = '%s%s_%s_%s.txt' % (NUM[d], LET[x], d.upper(), x.upper()); TH[j] = '%s %s' % (DTH[d], ATH[x])
steps = ''.join('%d. พิมพ์: ทำตาม %s  → %s\r\n' % (i + 1, FN[j], TH[j]) for i, j in enumerate(jobs))
readme = ('%s (%s): ' + ('ท่าครบ 4 ทิศ (ซ้าย = เกมกลับภาพจากขวาให้เอง)' if fresh else 'สั่งเฉพาะส่วนที่ยังขาด') + '\r\n\r\n'
          'สำคัญ: พิมพ์ทีละบรรทัด รอให้ได้รูปก่อนแล้วค่อยพิมพ์บรรทัดถัดไป อย่าสั่งให้ทำทั้งหมดทีเดียว (ซุนหงอคงกับอาร์เทมิสโดนยัดทุกท่าทุกทิศในรูปเดียว ภาพเล็กจนใช้ไม่ได้)\r\n'
          'ทำในแชตเดียวกัน: ครั้งแรกแนบรูปที่ Claude ส่งแยกมา (' + ', '.join([key + '.png'] + ([] if fresh else ['east_done.png']) + (['turnaround.png'] if turnpng else [])) + ') พร้อม zip นี้ แล้วพิมพ์ทีละบรรทัด แต่ละบรรทัดได้ 1 รูป\r\n%s\r\n'
          + ('ข้อ 1 ต้องทำก่อน: ตัววาดหมุนตัวละครไปหันหน้า/หันหลังเองไม่ได้ ให้วาดรูปนิ่ง 3 ด้านก่อน ถ้าไม่เหมือนตัวเดิมให้สั่งใหม่จนเหมือน\r\n' if 'turn' in jobs else
             'รูปนิ่ง 3 ด้าน (turnaround.png) ทำเสร็จแล้ว อยู่ในไฟล์นี้\r\n') +
          'ได้รูปไหนก็ดาวน์โหลดเก็บไว้ ส่งให้ Claude ทีละรูปหรือรวมเป็น zip ก็ได้ (ห้ามย่อ)\r\n'
          'ถ้าตัววาดเสนอทำไฟล์อื่นเพิ่ม (GIF, แยกเฟรม ฯลฯ) ไม่ต้อง Claude ทำเอง\r\n') % (th, en, steps)
os.makedirs(out, exist_ok=True)
zp = os.path.join(out, ('anim4_%s.zip' if fresh else 'fill_%s.zip') % key)
with zipfile.ZipFile(zp, 'w', zipfile.ZIP_DEFLATED) as z:
    z.write('art/incoming/legends/%s.png' % key, key + '.png')
    if not fresh: z.write(done, 'east_done.png')
    if turnpng: z.write(turnpng, 'turnaround.png')
    for j in jobs: z.writestr(FN[j], P[j] + '\n')
    z.writestr('README_TH.txt', readme.encode('utf-8-sig'))
print(zp, os.path.getsize(zp))
# the pictures also go next to the zip, to be sent on their own: the owner attaches them by hand (2026-11-07 "ส่งไฟล์มาแล้วแนบรูปให้ ฉันจะแนบให้มันเอง")
import shutil
for src, name in [('art/incoming/legends/%s.png' % key, key + '.png')] + ([] if fresh else [(done, 'east_done.png')]) + ([(turnpng, 'turnaround.png')] if turnpng else []):
    shutil.copyfile(src, os.path.join(out, name)); print(os.path.join(out, name))
