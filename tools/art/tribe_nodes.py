# Tribe game: resource nodes and building spots on map 1 -> art/tribe/map1_nodes.json
# trees / rocks come from the map's own props (classified by size + colour); approach point = nearest walkable spot below the prop.
import json, numpy as np
from PIL import Image
from scipy import ndimage as nd
m = json.load(open('art/td/map1/map.json')); atlas = np.asarray(Image.open('art/td/map1/props.png').convert('RGBA')).astype(int)
blk = np.asarray(Image.open('art/td/map1/block.png').convert('L')) > 128   # 2 world px per cell
free = ~blk; dist = nd.distance_transform_edt(free) * 2
FIRE = (560, 700)
def walk_near(x, y, r=60):
    best = None
    for yy in range(max(0, int(y) - r), min(1099, int(y) + r), 4):
        for xx in range(max(0, int(x) - r), min(1799, int(x) + r), 4):
            if dist[yy // 2, xx // 2] >= 10:
                d = (xx - x) ** 2 + (yy - y) ** 2
                if best is None or d < best[0]: best = (d, xx, yy)
    return best and (best[1], best[2])
nodes = []
for i, p in enumerate(m['props']):
    sx, sy, w, h = p['a']; reg = atlas[sy:sy + h, sx:sx + w]; a = reg[..., 3] > 0
    if a.sum() < 200: continue
    r, g, b = [reg[..., k][a].mean() for k in range(3)]
    kind = 'tree' if h >= 100 and g >= r - 2 and w < 300 else 'rock' if w <= 50 and h <= 50 and abs(r - g) < 10 and r > 70 else None   # big olive props = trees, small grey = rocks (brown = logs, skipped)
    if not kind: continue
    ap = walk_near(p['x'] + w / 2, p['y'] + h * .92, 110 if kind == 'tree' else 60)
    if not (0 < p['x'] + w / 2 < 1800): continue
    if ap: nodes.append({'kind': kind, 'prop': i, 'x': ap[0], 'y': ap[1]})
# berry bushes: placed by us in open grass 120-260 px from the fire
ang = np.linspace(0, 2 * np.pi, 9)[:-1]; berries = []
for k, a in enumerate(ang):
    for rr in (150, 190, 230, 270):
        x, y = FIRE[0] + np.cos(a + .3) * rr * 1.2, FIRE[1] + np.sin(a + .3) * rr * .8
        if 0 < x < 1800 and 0 < y < 1100 and dist[int(y) // 2, int(x) // 2] >= 26: berries.append({'kind': 'berry', 'x': int(x), 'y': int(y)}); break
# hut / defence spots: rings around the fire on open ground, nearest first
spots = []
for rr in range(90, 420, 46):
    n = max(6, int(2 * np.pi * rr / 70))
    for k in range(n):
        a = 2 * np.pi * k / n + rr * .01; x, y = FIRE[0] + np.cos(a) * rr * 1.25, FIRE[1] + np.sin(a) * rr * .85
        if 40 < x < 1760 and 60 < y < 1060 and dist[int(y) // 2, int(x) // 2] >= 30 and all((x - b['x']) ** 2 + (y - b['y']) ** 2 > 50 ** 2 for b in berries):
            spots.append({'x': int(x), 'y': int(y), 'r': rr})
json.dump({'fire': FIRE, 'spawns': [[56, 704], [1770, 780], [900, 1052], [1286, 140]], 'nodes': nodes + berries, 'spots': spots}, open('art/tribe/map1_nodes.json', 'w'))
from collections import Counter
print(Counter(n['kind'] for n in nodes + berries), 'spots', len(spots))
