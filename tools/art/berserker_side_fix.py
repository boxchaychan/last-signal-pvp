# Berserker side view (GPT try 4): the red X glow belongs on the LEFT glove (front/back views), not on the near right
# glove holding the sword -> painted out; the grip between the fist and the pommel was twice as long as in the front
# view -> the pommel moved in by 30 px.   python tools/art/berserker_side_fix.py <in> <out>
import sys, numpy as np, cv2
im = cv2.imread(sys.argv[1]); a = im.astype(int); b, g, r = a[..., 0], a[..., 1], a[..., 2]
m = np.zeros(im.shape[:2], np.uint8)
x0, x1, y0, y1 = 890, 985, 385, 470
sub = (r - b > 50) & (r > 120)
m[y0:y1, x0:x1] = sub[y0:y1, x0:x1]
m = cv2.dilate(m, np.ones((5, 5), np.uint8), iterations=1)
im = cv2.inpaint(im, m * 255, 6, cv2.INPAINT_TELEA)
s, X0, X1, Y0, Y1 = 30, 1040, 1160, 300, 430
blk = im[Y0:Y1, X0:X1].copy(); im[Y0:Y1, X0:X1] = 255; im[Y0:Y1, X0 - s:X1 - s] = blk
cv2.imwrite(sys.argv[2], im); print('ok', int(m.sum() // 255), 'px painted out')
