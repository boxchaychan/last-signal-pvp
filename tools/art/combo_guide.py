# Pose sheets for GPT from OUR bone move file (owner 2026-11-13 "ทำไม่ได้ก็ปรับปรุงทูล": the free Ozzbit pack has one slash only,
# so the combo is our own: art/poses/combo/sword_combo.json = key poses; combo.html plays it with in-betweens).
# Each hit of the combo -> one 4x2 sheet of 8 poses sampled along the same in-betweens (the hit pose is always one of them),
# drawn with pose_guide's colour stick figure, + PROMPT + poses.json (feet / head / sword tip per cell for lining frames up).
#   python3 tools/art/combo_guide.py -> art/poses/std/weapon/sword_combo{1,2,3}.png + .json + PROMPT_sword_combo<n>.txt
import json, math, sys
sys.path.insert(0, 'tools/art'); import pose_guide as G
from PIL import Image, ImageDraw, ImageFont
O = 'art/poses/std/weapon/'; M = json.load(open('art/poses/combo/sword_combo.json')); CW, CH, GY = G.CW, G.CH, G.GY
def ease(k, e): k = max(0, min(1, k)); return k ** 3 if e == 'in' else 1 - (1 - k) ** 2 if e == 'out' else k * k * (3 - 2 * k)
def joints(p, ox):
    pt = G.pt; hip = (p[10], 0); J = dict(hip=hip, sh=pt(hip, -90 + p[0], 52), neck=pt(hip, -90 + p[0], 62)); J['head'] = pt(J['neck'], -90 + p[0] * .6, 66)
    J['elbF'] = pt(J['sh'], p[1], 40); J['handF'] = pt(J['elbF'], p[2], 36); J['tip'] = pt(J['handF'], p[3], 96); J['elbB'] = pt(J['sh'], p[4], 38); J['handB'] = pt(J['elbB'], p[5], 32)
    J['kneeF'] = pt(hip, p[6], 36); J['footF'] = pt(J['kneeF'], p[7], 40); J['kneeB'] = pt(hip, p[8], 36); J['footB'] = pt(J['kneeB'], p[9], 40)
    low = max(J['footF'][1], J['footB'][1]) + p[11]; return {k: (ox + v[0], GY + v[1] - low) for k, v in J.items()}
prev = M['stand']
for n, S in enumerate(M['steps'], 1):
    K = S['keys']; T = K[-1]['t']; ht = next(k['t'] for k in K if k.get('hit')); ts = [T * i / 7 for i in range(8)]
    hi = min(range(1, 7), key=lambda i: abs(ts[i] - ht)); ts[hi] = ht; base = K[0]['p'][10] if n > 1 else 0; d0 = prev[10]
    def at(t):
        a, t0 = prev, 0
        for k in K:
            if t <= k['t']: return [x + (y - x) * ease((t - t0) / (k['t'] - t0), k['e']) for x, y in zip(a, k['p'])]
            a, t0 = k['p'], k['t']
        return list(K[-1]['p'])
    im = Image.new('RGB', (CW * 4, CH * 2), (255, 255, 255)); d = ImageDraw.Draw(im); F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 30); out = []
    for i, t in enumerate(ts):
        p = at(t); p[10] -= d0; p[11] *= .55                      # each sheet starts at its own x; the jump is drawn lower so it stays in the cell
        ox, oy = i % 4 * CW, i // 4 * CH; J = joints(p, CW * .34); d.rectangle((ox, oy, ox + CW - 1, oy + CH - 1), outline=(190, 190, 190)); d.line((ox + 12, oy + GY + 12, ox + CW - 12, oy + GY + 12), fill=(150, 150, 150), width=3)
        G.draw(d, J, ox, oy); d.text((ox + 12, oy + 8), str(i + 1), fill=(90, 90, 90), font=F); out.append({k: [round(v[0]), round(v[1])] for k, v in J.items()})
    name = 'sword_combo%d' % n; im.save(O + name + '.png')
    json.dump({'move': name, 'group': 'weapon', 'th': 'คอมโบดาบ จังหวะ %d: %s' % (n, S['th']), 'loop': False, 'cell': [CW, CH], 'grid': [4, 2], 'ground': GY, 'hit': hi, 'times': [round(t, 3) for t in ts], 'poses': out, 'source': 'art/poses/combo/sword_combo.json'}, open(O + name + '.json', 'w'), ensure_ascii=False)
    pr = open(O + 'PROMPT_sword_slash.txt').read().replace('sword_slash.png', name + '.png').replace('ฟัน (อาวุธระยะใกล้)', 'คอมโบดาบ จังหวะ %d: %s' % (n, S['th'])) \
        .replace('showing a melee weapon ATTACK: wind-up, a wide swing, recovery of another character', 'showing hit %d of a 3-hit sword COMBO (%s) as a colour stick figure: yellow head with a nose pointing where it faces, blue body, red/orange FRONT arm holding the grey sword, purple/pink back arm, green front leg, teal back leg' % (n, S['name']))
    open(O + 'PROMPT_%s.txt' % name, 'w').write(pr); prev = K[-1]['p']
print('ok')
