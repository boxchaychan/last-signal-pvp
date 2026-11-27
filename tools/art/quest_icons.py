# Pack the PixelLab icons of quest.html into one strip.
#   python tools/art/quest_icons.py      (reads art/incoming/quest/icons/<name>_raw.png, writes art/quest/icons.png)
# 32 px cells in this fixed order (the game draws them by index): atk, sk0, sk1, sk2, dodge, up_atk, up_hp, quest.
# Each icon gets tools/art/pixel_punch.py; the raw files stay as they are.
import os, subprocess, sys, tempfile
import numpy as np
from PIL import Image
ORDER = ['atk', 'sk0', 'sk1', 'sk2', 'dodge', 'up_atk', 'up_hp', 'quest']; SRC = 'art/incoming/quest/icons'
strip = Image.new('RGBA', (32 * len(ORDER), 32), (0, 0, 0, 0))
for i, n in enumerate(ORDER):
    f = os.path.join(SRC, n + '_raw.png'); im = Image.open(f).convert('RGBA'); tmp = os.path.join(tempfile.gettempdir(), 'qi_' + n + '.png')
    subprocess.check_call([sys.executable, 'tools/art/pixel_punch.py', f, tmp, '0.5', '24'])
    p = np.asarray(Image.open(tmp).convert('RGBA')).copy(); p[..., 3] = np.where(np.asarray(im)[..., 3] > 0, 255, 0)
    strip.paste(Image.fromarray(p).resize((32, 32), Image.NEAREST) if im.size != (32, 32) else Image.fromarray(p), (i * 32, 0))
strip.save('art/quest/icons.png'); print('art/quest/icons.png', strip.size)
