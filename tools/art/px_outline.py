# Clean outline for PixelLab / GPT-converted sprites (owner 2026-11-12 "พวกคลาส 1 ดูคมหมด", the class-2 heroes looked broken):
# class-1 heroes have a solid 1 px dark outline; the Assassin / Berserker clips have a speckled pale rim left from the white
# background and no outline. This drops pale pixels on the outer edge (2 passes), lone specks, and draws a 1 px dark outline
# round the silhouette (the neighbour's own colour darkened, like a hand-drawn line).
import numpy as np
from scipy import ndimage
def outline(a, pale=95, dark=.28):
    a = a.astype(int).copy()
    for _ in range(2):
        m = a[..., 3] > 0; e = m & ~ndimage.binary_erosion(m)
        a[e & (a[..., :3].min(2) > pale)] = 0
    m = a[..., 3] > 0; lab, n = ndimage.label(m, structure=np.ones((3, 3)))
    if n > 1:
        sz = ndimage.sum(m, lab, range(1, n + 1))
        for i, s in enumerate(sz):
            if s < 8: a[lab == i + 1] = 0
    m = a[..., 3] > 0; a[m, 3] = 255
    ring = ndimage.binary_dilation(m, structure=np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])) & ~m
    # colour of the ring = the darkest opaque neighbour, darkened
    acc = np.full(a.shape[:2] + (3,), 999); 
    for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        sh = np.roll(np.roll(a, dy, 0), dx, 1); ok = sh[..., 3] > 0
        lum = sh[..., :3].sum(2); cur = acc.sum(2)
        better = ok & (lum < cur); acc[better] = sh[better][:, :3]
    a[ring, :3] = (acc[ring] * dark + np.array([20, 14, 26]) * (1 - dark)).astype(int); a[ring, 3] = 255
    return a.clip(0, 255).astype(np.uint8)
