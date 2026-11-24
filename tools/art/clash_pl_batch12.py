"""clash.html batch 12 = MACHINE TRIBE in true 16-bit (owner 2026-11-24 "ไปที่เครื่องจักร", after the god tribe;
same recipe as batch 11). 64 DIFFERENT machine-tribe units at 32 px (our soldiers' size), side view
facing right, all 8 classes, "16-bit console pixel art" in the text AND max_colors = 16. Style pictures = 4 god units from batch 1 + 4 crisp picks
of ours (NOT a previous batch together with the same list: batch 10 lesson). 64 x 32 px = 10 generations. Dry run by default; `--go` sends."""
import json, base64, sys, os, io
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')); os.environ.setdefault('PL_KEY', 'proxy-injected')
import numpy as np
from PIL import Image
from scipy import ndimage
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, '../..'); OUT = os.path.join(R, 'art/incoming/clash/batch12')
K = 'machine-tribe war robot, 16-bit console pixel art, chibi proportions, steel grey metal with orange warning stripes and glowing cyan lights, bold dark outline, few flat colours, heavy and fierce'
CL = {
 'tank': ['bulky robot with a riveted tower shield', 'walking steel bunker with a plow blade', 'heavy mech with an energy barrier arm', 'tracked tank-robot with a front ram',
   'riveted iron golem with a hydraulic fist', 'crab-legged siege walker with armour plates', 'spiked bulldozer robot', 'gear-shield sentinel with a bolt lance'],
 'warrior': ['robot knight with a chainsaw sword', 'combat android with a plasma blade', 'buzzsaw arm brawler robot', 'hammer drill robot', 'piston-fist boxer robot',
   'samurai cyborg with a heat katana', 'twin-axe lumberjack robot', 'jackhammer berserker robot', 'magnet claw grappler robot', 'scrap gladiator with a junk sword'],
 'spear': ['lance mech with a long drill spear', 'piston spearman robot', 'electro-pike trooper', 'harpoon launcher spearman', 'laser halberd guard robot', 'telescoping spear android'],
 'assassin': ['stealth ninja android with wrist blades', 'spider assassin bot', 'chrome scorpion robot with a stinger', 'invisible cloak drone hunter', 'twin-dagger cyber rogue', 'rocket-boot striker robot'],
 'shooter': ['gatling gun robot', 'sniper robot with a long rail rifle', 'rocket launcher mech', 'flamethrower trooper bot', 'mortar walker robot', 'twin laser turret on legs',
   'crossbow bolt-thrower robot', 'missile drone carrier', 'nail gun scrapper', 'shotgun cowboy robot'],
 'mage': ['tesla coil robot mage', 'plasma orb caster android', 'gravity field engineer robot', 'laser prism robot', 'EMP pulse robot', 'frost cannon robot', 'nanobot swarm caster'],
 'support': ['repair robot with a giant wrench', 'medic bot with a green cross light', 'shield generator robot', 'radar commander robot', 'battery charger robot', 'drone carrier mechanic', 'banner robot with a glowing flag'],
 'rider': ['pilot riding a mech spider', 'robot riding a hover bike', 'knight robot riding a mechanical horse', 'pilot in a walking chicken mech', 'trooper on a rolling wheel bike', 'robot riding a metal wolf'],
 'special': ['giant robot head on tank treads', 'living factory robot with chimneys', 'AI core sphere floating with cables', 'clockwork dragon'],
}
items, keys, names = [], [], {}
for cls, lst in CL.items():
    for d in lst:
        k = f'c12_{len(keys):02d}'; items.append(f'{K}, {d}, side view facing right, full body'); keys.append(k); names[k] = f'{cls}: {d}'
assert len(items) == 64 and len(set(items)) == 64, (len(items), len(set(items)))
SP = ['batch1/raw/00_m_drone_1', 'batch1/raw/02_m_turret_1', 'batch1/raw/04_m_tesla_1', 'batch1/raw/06_m_repair_1', 'batch3/raw/k3_02', 'batch3/raw/k3_14', 'batch4/raw/a4_29', 'batch3/raw/k3_10']
def clean(f):   # drop bits of the NEIGHBOUR cell at the slot edge (style copy only)
    a = np.asarray(Image.open(os.path.join(R, 'art/incoming/clash', f + '.png')).convert('RGBA')).copy(); lab, n = ndimage.label(a[..., 3] > 30)
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) < 24 and (xs.min() == 0 or ys.min() == 0 or xs.max() == a.shape[1] - 1 or ys.max() == a.shape[0] - 1): a[lab == i] = 0
    b = io.BytesIO(); Image.fromarray(a).save(b, 'PNG'); return base64.b64encode(b.getvalue()).decode()
style = [{'type': 'base64', 'base64': clean(f), 'format': 'png'} for f in SP]
args = {'description': f'tiny {K}, pixel art game sprite, side view facing right, full body', 'name': 'clash machine tribe 16-bit batch 12', 'view': 'sidescroller',
        'style_images': style, 'item_descriptions': items, 'max_colors': 16}
os.makedirs(OUT, exist_ok=True); json.dump(keys, open(os.path.join(OUT, 'keys.json'), 'w'), indent=1); json.dump(names, open(os.path.join(OUT, 'items.json'), 'w'), indent=1, ensure_ascii=False)
if '--go' in sys.argv:
    from pl_rpc import call
    r = call('create_1_direction_object', args); print(r); open(os.path.join(OUT, 'submit.txt'), 'w').write(r)
else: print(len(items), 'machine-tribe units, all different, max 16 colours; dry run')
