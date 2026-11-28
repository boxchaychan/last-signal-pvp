# find the camera that painted art/bag3d/ui/arena_forest.jpg: floor circle radius A = 8 on y = 0, camera south of it looking north
import numpy as np
from scipy.optimize import least_squares
W, H, A = 1536, 1024, 8.0
def proj(p, e, d, f, z0):
    cam = np.array([0, d * np.sin(e), z0 + d * np.cos(e)]); tgt = np.array([0, 0, z0]); fw = tgt - cam; fw /= np.linalg.norm(fw)
    rt = np.cross(fw, [0, 1, 0]); rt /= np.linalg.norm(rt); up = np.cross(rt, fw); v = np.asarray(p, float) - cam
    x, y, z = v @ rt, v @ up, v @ fw; t = np.tan(f / 2); return np.array([W / 2 + x / z / t * (H / 2), H / 2 - y / z / t * (H / 2)])
obs = dict(c=(782, 566), far=(785, 236), mfar=(782, 432), mnear=(782, 700), mright=(1000, 566), mleft=(565, 566), gl=(195, 335), gr=(1375, 335), el=(0, 470))
def res(q):
    e, d, f, z0, m, phi, psi = q; r = []
    r += list(proj((0, 0, 0), e, d, f, z0) - (768, obs['c'][1]))
    r += [proj((0, 0, -A), e, d, f, z0)[1] - obs['far'][1]]
    r += [proj((0, 0, -m), e, d, f, z0)[1] - obs['mfar'][1], proj((0, 0, m), e, d, f, z0)[1] - obs['mnear'][1]]
    r += [proj((m, 0, 0), e, d, f, z0)[0] - (768 + (obs['mright'][0] - obs['mleft'][0]) / 2)]
    g = proj((-A * np.sin(phi), 0, -A * np.cos(phi)), e, d, f, z0); r += list((g - (768 - (obs['gr'][0] - obs['gl'][0]) / 2, obs['gl'][1])) * .7)
    k = proj((-A * np.sin(psi), 0, -A * np.cos(psi)), e, d, f, z0); r += list((k - obs['el']) * .5)
    return r
best = None
for e0 in (.5, .7, .9):
    for f0 in (.5, .8, 1.1):
        s = least_squares(res, [e0, 22, f0, -1, 2.2, .8, 1.3], bounds=([.2, 6, .2, -8, .5, .2, .6], [1.4, 80, 1.6, 8, 5, 1.4, 2.2]))
        if best is None or s.cost < best.cost: best = s
e, d, f, z0, m, phi, psi = best.x
print('pitch deg %.1f  dist %.2f  fovV deg %.1f  look z %.2f  medallion r %.2f  gate angle deg %.1f  edge angle deg %.1f  cost %.1f' % (np.degrees(e), d, np.degrees(f), z0, m, np.degrees(phi), np.degrees(psi), best.cost))
print('residuals', np.round(res(best.x), 1))
for nm, p in [('centre', (0, 0, 0)), ('far wall', (0, 0, -A)), ('near wall', (0, 0, A)), ('left wall', (-A, 0, 0)), ('right gate', (A * np.sin(phi), 0, -A * np.cos(phi))), ('wall top far (h 2.2)', (0, 2.2, -A))]:
    print(nm, np.round(proj(p, e, d, f, z0)))
print('--- floor depth -> picture y (x = 0), and half-width of the picture at that depth in world units')
for z in (-8, -6, -4, -2.6, 0, 1, 2, 2.6, 3, 3.5, 4):
    y = proj((0, 0, z), e, d, f, z0)[1]; x1 = proj((1, 0, z), e, d, f, z0)[0] - 768; print('z %5.1f  y %6.0f   1 unit = %5.1f px   half width %.1f units' % (z, y, x1, 768 / x1))
print('hero 1.35 tall at z -2.6:', np.round(proj((0, 0, -2.6), e, d, f, z0)[1] - proj((0, 1.35, -2.6), e, d, f, z0)[1]), 'px of 1024')
print('cam pos (painting world):', 0, round(d * np.sin(e), 3), round(z0 + d * np.cos(e), 3), ' look z', round(z0, 3), 'fov', round(np.degrees(f), 2))
