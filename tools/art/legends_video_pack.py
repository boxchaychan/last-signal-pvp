# Video animation package for one legend (owner 2026-11-07: "ลองเอาหงอคงทำอนิเมชั่นวิดีโอดู เอารูปแนบ พร้อมเจนวิดีโอมา",
# after a clip of DPS: Desktop Pension Squad whose characters move smoothly). A video AI (Google Flow "Frames to Video",
# the same picture as the first and the last frame) draws every in-between, so the motion is fluid; Claude keys the flat
# green background out and picks the frames for the game.
#   python3 tools/art/legends_video_pack.py <out dir> <key> <turnaround.png> [--bg=green|magenta]
#     turnaround.png = front / side / back on white; the middle third (the side view, facing right) is used
# Writes <out dir>/video_<key>.zip (start picture + 3 prompts + Thai steps) and the start picture next to it
# (sent on its own too: the owner attaches pictures by hand). Run from the repo root.
import sys, os, subprocess, zipfile, tempfile, shutil
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from legends_codex import ANIM

args = [a for a in sys.argv[1:] if not a.startswith('--')]
out, key, turn = args[0], args[1], args[2]
bgname = next((a[5:] for a in sys.argv[1:] if a.startswith('--bg=')), 'green')
BG = {'green': (0, 255, 0), 'magenta': (255, 0, 255)}[bgname]
HEX = {'green': '#00FF00', 'magenta': '#FF00FF'}[bgname]
a = next(x for x in ANIM if x[0] == key)
k, en, th, desc, idle, an, asteps, sn, swhat, ssteps = a[:10]

# start picture: side view cut out of the turnaround, on a flat key colour, 1920x1080; the figure is 54% of the height,
# a bit left of the middle with its feet at 82%, so a leap, a lunge to the right and a long weapon stay in the frame
tmp = tempfile.mkdtemp()
im = Image.open(turn).convert('RGB'); w3 = im.width // 3
im.crop((w3, 0, 2 * w3, im.height)).save(tmp + '/side.png')
subprocess.run([sys.executable, '-I', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'white_cut.py'),
                tmp + '/side.png', tmp + '/cut.png', '--edge-only', '--no-ring'], check=True, capture_output=True)  # --no-ring keeps the eye whites
fig = Image.open(tmp + '/cut.png').convert('RGBA'); fig = fig.crop(fig.getbbox())
W, H = 1920, 1080; s = H * .54 / fig.height
fig = fig.resize((round(fig.width * s), round(fig.height * s)), Image.LANCZOS)
al = np.array(fig)[..., 3]; al[al < 128] = 0; al[al >= 128] = 255; fa = np.array(fig); fa[..., 3] = al; fig = Image.fromarray(fa)
start = Image.new('RGBA', (W, H), BG + (255,))
start.alpha_composite(fig, (round(W * .38 - fig.width / 2), round(H * .86 - fig.height)))
start = start.convert('RGB')
shutil.rmtree(tmp)

st = lambda L: '\n'.join('  %d. %s' % (i + 1, x) for i, x in enumerate(L))
HEAD = ('Animate this exact character from the attached picture start_%s.png: %s, a 2D game character, side view facing right.\n\n'
        'Keep everything exactly as in the picture: the same face, hair, costume, colours, outlines, size and place in the frame. Only the pose moves.\n'
        'Camera: locked and static. No zoom, no pan, no shake, no cuts.\n'
        'Background: the same flat pure %s background for the whole video. No ground, no shadow, no dust, no sparks, no glow, '
        'no magic effects, no motion trails, no text, no other characters.\n'
        'Motion: smooth, fluid 2D game animation like a Spine / cut-out character: clear key poses with smooth in-betweens, '
        'anticipation before each move and follow-through after it, a little squash on hits and landings. '
        'The whole character and the weapon stay inside the frame all the time.\n'
        'The video starts and ends on exactly the pose in the picture, so it loops.\n\n') % (key, desc, bgname + ' (' + HEX + ')')
P = {
    '1_IDLE.txt': HEAD + 'Action, 8 seconds - idle, a calm loop: %s. Breathing in and out slowly, a blink, a small grin. '
                         'The feet stay planted. Keep this calm loop for the whole video, no attacks.' % idle,
    '2_ATTACK.txt': HEAD + ('Action, 8 seconds - attack "%s", done 3 times in a row with a short pause in the stance between them '
                            '(about 2 seconds each):\n%s\nBig, clear arcs. The weapon keeps its normal length and shape.') % (an, st(asteps)),
    '3_SKILL.txt': HEAD + ('Action, 8 seconds - ultimate "%s" (in the game he %s), once and slow enough to read (about 5 seconds), '
                           'then hold the stance until the end:\n%s\nThe grown weapon must stay inside the frame (it may reach close to the edge).') % (sn, swhat, st(ssteps)),
}
readme = ('%s (%s): ภาพเคลื่อนไหวจากวิดีโอ (ขยับลื่นแบบเกม DPS)\r\n\r\n'
          'ใช้ Google Flow (labs.google/flow) โหมด Frames to Video (วิดีโอจากภาพแรก + ภาพสุดท้าย)\r\n'
          '1. ใส่รูป start_%s.png เป็นทั้งภาพแรก (First frame) และภาพสุดท้าย (Last frame) รูปเดียวกันทั้งสองช่อง\r\n'
          '2. เปิดไฟล์ 1_IDLE.txt คัดลอกข้อความทั้งหมดไปวางในช่องคำสั่ง แล้วกดสร้าง (8 วินาที)\r\n'
          '3. ทำแบบเดียวกันกับ 2_ATTACK.txt (ท่าตี) และ 3_SKILL.txt (ท่าไม้ตาย) ใช้รูปเดิมทุกครั้ง\r\n'
          '4. ดาวน์โหลดวิดีโอ MP4 ขนาดใหญ่สุด ส่งให้ Claude ทั้ง 3 ไฟล์ (ไม่ต้องตัดต่อ ไม่ต้องลบพื้นเขียว Claude ทำเอง)\r\n\r\n'
          'ถ้าได้วิดีโอที่ตัวละครหน้าเปลี่ยน ชุดเปลี่ยน กล้องขยับ หรือพื้นหลังไม่เป็นสีเขียวเรียบ ให้สร้างใหม่ เลือกอันที่เหมือนรูปที่สุด\r\n'
          'ถ้าอยากลองก่อนอันเดียว เริ่มที่ 2_ATTACK.txt (ท่าตี) จะเห็นความลื่นชัดที่สุด\r\n') % (th, en, key)
os.makedirs(out, exist_ok=True)
sp = os.path.join(out, 'start_%s.png' % key); start.save(sp)
zp = os.path.join(out, 'video_%s.zip' % key)
with zipfile.ZipFile(zp, 'w', zipfile.ZIP_DEFLATED) as z:
    z.write(sp, 'start_%s.png' % key)
    for n, t in P.items(): z.writestr(n, t + '\n')
    z.writestr('README_TH.txt', readme.encode('utf-8-sig'))
print(zp, os.path.getsize(zp)); print(sp)
