"""Cut characters out of the owner's own pictures for divine.html (free): GrabCut inside a box + keep the biggest piece + fill holes.
  python3 tools/art/divine_cut.py
Sources: art/incoming/divine_game/ref/owner_target_mockup_full.jpg (the owner's mock-up, full size) and owner_tone_zeus_boy_full.jpg.
-> art/incoming/divine_game/cut/<name>.png (transparent, trimmed) + cut_check.png (all of them on a checker)."""
import os, sys
import numpy as np, cv2
from PIL import Image, ImageDraw
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'); REF = os.path.join(R, 'art/incoming/divine_game/ref'); OUT = os.path.join(R, 'art/incoming/divine_game/cut')
MOCK = 'owner_target_mockup_full.jpg'; TONE = 'owner_tone_zeus_boy_full.jpg'
BOX = {   # name: (source, x0, y0, x1, y1) in the source's own pixels
    'robot_a': (MOCK, 492, 470, 650, 665), 'robot_b': (MOCK, 708, 512, 858, 705), 'ghoul_a': (MOCK, 892, 488, 1116, 712), 'ghoul_b': (MOCK, 1140, 488, 1366, 722),
    'robot_c': (MOCK, 934, 1958, 1075, 2100),
    'soldier': (MOCK, 1076, 1080, 1232, 1262), 'thor': (MOCK, 676, 1392, 840, 1582), 'monkey': (MOCK, 858, 1558, 1034, 1758), 'anubis': (MOCK, 676, 1692, 840, 1915),
    'zeus_boy': (TONE, 420, 760, 1400, 1960), 'zeus_spirit': (TONE, 470, 150, 1460, 880),
}
def cut(name, src, x0, y0, x1, y1):
    im = cv2.imread(os.path.join(REF, src)); H, W = im.shape[:2]; pad = 14
    X0, Y0, X1, Y1 = max(0, x0 - pad), max(0, y0 - pad), min(W, x1 + pad), min(H, y1 + pad); sub = im[Y0:Y1, X0:X1].copy()
    mask = np.zeros(sub.shape[:2], np.uint8); rect = (pad, pad, (x1 - x0), (y1 - y0))
    if src == TONE and name == 'zeus_boy':   # white page: the boy = everything inside his dark outline (his white tunic stays solid; the spirit's glow is left out)
        lum = sub.astype(float) @ np.array([.11, .59, .3]); m = cv2.morphologyEx((lum < 95).astype(np.uint8), cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
    else:
        bg, fg = np.zeros((1, 65), np.float64), np.zeros((1, 65), np.float64)
        cv2.grabCut(sub, mask, rect, bg, fg, 6, cv2.GC_INIT_WITH_RECT); m = ((mask == 1) | (mask == 3)).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
    if n > 1: big = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA])); m = (lab == big).astype(np.uint8)
    ff = m.copy(); h, w = m.shape; fl = np.zeros((h + 2, w + 2), np.uint8); cv2.floodFill(ff, fl, (0, 0), 1); m = m | (1 - ff)   # fill holes
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    rgba = cv2.cvtColor(sub, cv2.COLOR_BGR2RGBA); rgba[..., 3] = m * 255
    if name == 'zeus_spirit':   # drawn on white: soft alpha from the distance to white, colour un-blended from white
        c = sub[..., ::-1].astype(float); dist = np.abs(c - 255).max(2); al = np.clip(dist / (110 if name == 'zeus_spirit' else 70), 0, 1)
        if name == 'zeus_spirit': al = al * 1.0; al *= np.clip((sub.shape[0] - np.arange(sub.shape[0])[:, None] - pad) / (sub.shape[0] * .3), 0, 1)   # fades out at the bottom
        al = al * (m > 0); q = np.maximum(al, 1e-3)[..., None]; col = np.clip((c - (1 - q) * 255) / q, 0, 255)
        rgba = np.dstack([col, al * 255]).astype(np.uint8)
    a = Image.fromarray(rgba); a = a.crop(a.getbbox()); a.save(os.path.join(OUT, name + '.png')); return a
os.makedirs(OUT, exist_ok=True); outs = [(n, cut(n, *b)) for n, b in BOX.items()]
S = 150; sheet = Image.new('RGBA', (S * 6, S * 2 + 30), (255, 255, 255, 255)); d = ImageDraw.Draw(sheet)
for y in range(0, sheet.height, 10):
    for x in range(0, sheet.width, 10):
        if (x // 10 + y // 10) % 2: d.rectangle([x, y, x + 9, y + 9], fill=(205, 205, 205, 255))
for i, (n, a) in enumerate(outs):
    k = min((S - 10) / a.width, (S - 10) / a.height); t = a.resize((max(1, int(a.width * k)), max(1, int(a.height * k))), Image.LANCZOS)
    sheet.alpha_composite(t, ((i % 6) * S + 5, (i // 6) * (S + 15) + 15)); d.text(((i % 6) * S + 5, (i // 6) * (S + 15) + 2), n, fill=(0, 0, 0, 255))
sheet.save(os.path.join(OUT, 'cut_check.png')); print('ok', [(n, a.size) for n, a in outs])
