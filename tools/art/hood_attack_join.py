# Join per-hit attack strips (hood_attack_cut.py v6a/b/c) into one strip with a shared cell and feet point.
import json
from PIL import Image
parts = [f'art/incoming/hood/attack/hit{n}_cut' for n in (1, 2, 3)]; OUT = 'art/sidegame/rabbit_attack6'
js = [json.load(open(p + '.json')) for p in parts]; ims = [Image.open(p + '.png') for p in parts]
L = max(j['feet'][0] for j in js); R = max(j['cw'] - j['feet'][0] for j in js); U = max(j['feet'][1] for j in js); D = max(j['ch'] - j['feet'][1] for j in js)
CW, CH, n = L + R, U + D, sum(j['frames'] for j in js)
out = Image.new('RGBA', (CW * n, CH), (0, 0, 0, 0)); k = 0
for j, im in zip(js, ims):
    for i in range(j['frames']):
        out.alpha_composite(im.crop((i * j['cw'], 0, (i + 1) * j['cw'], j['ch'])), (k * CW + L - j['feet'][0], U - j['feet'][1])); k += 1
out.save(OUT + '.png'); json.dump({'cw': CW, 'ch': CH, 'feet': [L, U], 'frames': n, 'hits': [j['frames'] for j in js]}, open(OUT + '.json', 'w'))
print(CW, CH, L, U, n)
