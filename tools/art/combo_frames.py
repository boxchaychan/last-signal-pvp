# The swordsman's own drawn frames (PixelLab, already paid for) packed for the combo test: idle 8 / run 8 / attack 17 / leap 17.
# Owner 2026-11-13 "ตอนนี้ไม่สวยเลยนะ" about the cut-out bone version -> the pretty route = drawn frames joined by OUR combo logic.
#   python3 tools/art/combo_frames.py -> art/poses/combo/swordsman_frames.png (17 columns x 4 rows of 172 px cells, feet at 86,147)
import glob
from PIL import Image
B = 'art/incoming/action/swordsman/pl_dl/Idle/animations/'; c = Image.new('RGBA', (172 * 17, 172 * 4))
for j, a in enumerate(('idle', 'run', 'attack', 'leap')):
    for i, f in enumerate(sorted(glob.glob(B + a + '/east/*.png'))): c.alpha_composite(Image.open(f).convert('RGBA'), (i * 172, j * 172))
c.save('art/poses/combo/swordsman_frames.png', optimize=True); print(c.size)
