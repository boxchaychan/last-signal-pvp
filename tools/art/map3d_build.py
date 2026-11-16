# Map 1 of map.html as data for the 3D-pixel test map3d.html (owner 2026-11-16 "ลองทำดู1แมพ"; free, code only, no PixelLab).
# The 2D map is an oblique picture: a plateau's top is drawn DH map px higher than its footprint, its wall hangs below it.
# This turns it back into a world seen from straight above (x, z on the ground, art pixels of 2 x 2 map px):
#   EXPORT3D=<tmp> python3 tools/art/td_map.py           (the painter's masks + a ground without tree / bush shadows)
#   python3 tools/art/map3d_build.py <tmp>               -> art/td/map1/3d/
#     top.png    the ground colours seen from above, from ground.png (with every painted shadow: the original-art look)
#     top3d.png  the same from the painter without the tree / bush shadows (the 3D-tree look casts real shadows)
#     grid.png   R = plateau footprint (255), G = walkable (255), B = water (255); world space, 1 px = 2 x 2 map px
#     geo.json   stairs, props, monster spawns, start, all in world map px (z = north-south on the ground)
# The walls take their colours straight from ../ground.png (the page maps each wall quad onto the painted wall).
import json, os, sys, numpy as np
from PIL import Image
from scipy import ndimage

SRC = sys.argv[1]; OUT = 'art/td/map1/3d/'; os.makedirs(OUT, exist_ok=True)
P = np.load(SRC + '/paint.npz'); PJ = json.load(open(SRC + '/props.json'))
g, fp, up, face, ramp, water = P['g'], P['fprint'], P['up'], P['face'], P['ramp'], P['water']
GH, GW = fp.shape; DH = PJ['dh']; DA = DH // 2                       # wall height in art px (31)
ground = np.asarray(Image.open('art/td/map1/ground.png').convert('RGB'))[::2, ::2]
blk = np.asarray(Image.open('art/td/map1/block.png')) > 127
M = json.load(open('art/td/map1/map.json'))
zz, xx = np.mgrid[0:GH, 0:GW]

def world(src):   # screen-space art picture -> seen from above
    vis = ~ndimage.binary_dilation(up | face | ramp, iterations=2)   # low ground the 2D picture shows (not the dark rim round a plateau)
    _, (iy, ix) = ndimage.distance_transform_edt(~vis, return_indices=True)
    for x in range(GW):                                               # hidden low ground (behind a plateau): the ground just north
        z = 0                                                         # of it mirrored, else the nearest visible colour
        while z < GH:
            if vis[z, x] or fp[z, x]: z += 1; continue
            a = z
            while z < GH and not vis[z, x] and not fp[z, x]: z += 1
            for k in range(a, z):
                m = a - 1 - (k - a)
                if m >= 0 and vis[m, x]: iy[k, x], ix[k, x] = m, x
    low = src[iy, ix]
    top = src[np.clip(zz - DA, 0, GH - 1), xx]                        # a plateau top is drawn DA art px higher
    return np.where(fp[..., None], top, low).astype(np.uint8)
Image.fromarray(world(ground)).save(OUT + 'top.png', optimize=True)
Image.fromarray(world(g)).save(OUT + 'top3d.png', optimize=True)

# walkable: the 2D walk mask read at the place each world cell is drawn; low ground hidden behind / beside a plateau is open
# (in 3D you can walk there; falling off is stopped by the height rule in the page)
near = ndimage.binary_dilation(up | face, iterations=3) & ~ramp
walk = np.where(fp, ~blk[np.clip(zz - DA, 0, GH - 1), xx] & (zz - DA >= 0), ~blk | near)
Image.fromarray(np.dstack([fp * 255, walk * 255, water * 255]).astype(np.uint8)).save(OUT + 'grid.png', optimize=True)

# stairs: runs of columns with a ramp; each climbs from the footprint's south edge out over the low ground
stairs = []; cols = np.where(ramp.any(0))[0]
for run in np.split(cols, np.where(np.diff(cols) > 1)[0] + 1):
    edges = []
    for x in run:
        ye = np.nonzero(ramp[:, x])[0].max()
        r = np.nonzero(fp[:ye + 3, x])[0]
        if r.size: edges.append(int(r.max()) + 1)                    # first low row south of the footprint
    stairs.append({'x0': int(run[0]) * 2, 'x1': int(run[-1] + 1) * 2, 'z0': min(edges) * 2, 'z1': max(edges) * 2})

def place(x, y):   # a screen point (map px) -> world x, z and whether it stands on a plateau
    ax, ay = min(GW - 1, max(0, int(x) // 2)), min(GH - 1, max(0, int(y) // 2))
    on = bool(up[ay, ax] and not face[ay, ax])
    return [int(x), int(y) + (DH if on else 0), 1 if on else 0]
props = []
for p, m in zip(PJ['props'], M['props']):
    if p['kind'] == 'crown': continue                                  # the dark crowns over the 2D picture's bottom edge
    name = os.path.basename(p['s'][0]).replace('.png', '')
    props.append({'k': p['kind'], 'n': name, 'h': int(p['s'][1]), 'fl': p['s'][2] == 'True', 'a': m['a'], 'p': place(p['x'], p['y'])})
J = {'w': M['w'], 'h': M['h'], 'gw': GW, 'gh': GH, 'dh': DH, 'stairs': stairs, 'props': props,
     'spawn': [[k] + place(x, y) for k, x, y in M['spawn']], 'start': place(*M['start']), 'mobs': M['mobs']}
json.dump(J, open(OUT + 'geo.json', 'w'), separators=(',', ':'))
print('ok', len(props), 'props,', len(stairs), 'stairs', stairs, 'walkable', int(walk.mean() * 100), '%')
