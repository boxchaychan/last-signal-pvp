"""clash.html batch 14 = SPECIAL UNITS for 5 tribes in true 16-bit (owner 2026-11-24 "ขอยูนิตพิเศษด้วยนะ 10 เครดิต เดี๋ยวมาเลือกเอา เอาแค่ 5 เผ่าพอ ปีศาจมี 3 แล้ว";
the demons already have 3). 64 DIFFERENT special units (no class) for human 13, alien 13, animal 13, machine 13, god 12 at 32 px (our soldiers' size), side view
facing right, all 8 classes, "16-bit console pixel art" in the text AND max_colors = 16. Style pictures = 4 god units from batch 1 + 4 crisp picks
of ours (NOT a previous batch together with the same list: batch 10 lesson). 64 x 32 px = 10 generations. Dry run by default; `--go` sends."""
import json, base64, sys, os, io
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')); os.environ.setdefault('PL_KEY', 'proxy-injected')
import numpy as np
from PIL import Image
from scipy import ndimage
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, '../..'); OUT = os.path.join(R, 'art/incoming/clash/batch14')
K = 'unique SPECIAL army unit, 16-bit console pixel art, chibi proportions, bold dark outline, few flat colours, striking and fierce'
TONE = {'human': 'human tribe, dark steel armour and cloth', 'alien': 'alien tribe, dark purple with toxic green glow', 'animal': 'animal tribe, beast with tribal war paint',
        'machine': 'machine tribe, light steel metal with neon blue lights', 'god': 'god tribe, white and gold with light blue holy glow'}
CL = {
 'human': ['wandering ronin with a straw hat and two swords', 'plague doctor with a beak mask and a lantern', 'alchemist throwing glowing potions', 'bard playing a war lute', 'executioner with a giant axe',
   'siege engineer pushing a small cannon', 'staff monk in orange robes', 'gladiator with a net and a trident', 'musketeer with a long musket', 'witch hunter with a crossbow and a wide hat',
   'knight riding a war bear', 'giant living suit of armour', 'battle priestess with a holy hammer'],
 'alien': ['floating brain alien with mind waves', 'crystal shard being', 'giant acid slime with bones inside', 'shapeshifter mimic half-transformed', 'insect hive queen',
   'plasma ghost alien', 'cloaked alien hunter with a trophy spear', 'parasite swarm cloud with eyes', 'giant burrowing alien worm', 'levitating probe orb with tendrils',
   'many-eyed tentacle seer', 'alien knight with a living sword', 'walking spore pod plant'],
 'animal': ['ape king with a crown and a club', 'ancient giant tortoise elder', 'white tiger spirit', 'thunder bison with lightning horns', 'scorpion king', 'owl sage with a book',
   'chimera beast', 'lion knight with a mane cape', 'giant cobra charmer', 'sabre-tooth shaman', 'spirit elk with glowing antlers', 'honey badger berserker', 'praying mantis swordsman'],
 'machine': ['clockwork knight with a wind-up key', 'steam golem with chimneys', 'laser drone swarm', 'walking cannon mech', 'robot samurai with a laser katana', 'tesla coil tower on legs',
   'walking bomb robot', 'small mech dragon', 'twin android sisters', 'scrap golem made of junk', 'drill tank robot', 'orbiting satellite robot', 'hologram AI warrior'],
 'god': ['titan of the sun with a burning crown', 'thunder god with a lightning hammer', 'moon goddess with a crescent bow', 'angel of judgment holding scales and a sword', 'golden sphinx guardian',
   'holy stone golem with glowing runes', 'time keeper with a giant hourglass', 'star child floating in starlight', 'archangel with a flaming sword', 'sea god with a trident and a wave',
   'phoenix god in golden flames', 'twin-faced god of light and dark'],
}
items, keys, names = [], [], {}
for cls, lst in CL.items():
    for d in lst:
        k = f'c14_{len(keys):02d}'; items.append(f'{K}, {TONE[cls]}, {d}, side view facing right, full body'); keys.append(k); names[k] = f'{cls}: {d}'
assert len(items) == 64 and len(set(items)) == 64, (len(items), len(set(items)))
SP = ['batch3/raw/k3_18', 'batch4/raw/a4_34', 'batch7/raw/m7_01', 'batch12/raw/c12_13', 'batch11/raw/c11_13', 'batch11/raw/c11_03', 'batch6/raw/p6_00', 'batch4/raw/a4_12']
def clean(f):   # drop bits of the NEIGHBOUR cell at the slot edge (style copy only)
    a = np.asarray(Image.open(os.path.join(R, 'art/incoming/clash', f + '.png')).convert('RGBA')).copy(); lab, n = ndimage.label(a[..., 3] > 30)
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) < 24 and (xs.min() == 0 or ys.min() == 0 or xs.max() == a.shape[1] - 1 or ys.max() == a.shape[0] - 1): a[lab == i] = 0
    b = io.BytesIO(); Image.fromarray(a).save(b, 'PNG'); return base64.b64encode(b.getvalue()).decode()
style = [{'type': 'base64', 'base64': clean(f), 'format': 'png'} for f in SP]
args = {'description': f'tiny {K}, pixel art game sprite, side view facing right, full body', 'name': 'clash special units 16-bit batch 14', 'view': 'sidescroller',
        'style_images': style, 'item_descriptions': items, 'max_colors': 16}
os.makedirs(OUT, exist_ok=True); json.dump(keys, open(os.path.join(OUT, 'keys.json'), 'w'), indent=1); json.dump(names, open(os.path.join(OUT, 'items.json'), 'w'), indent=1, ensure_ascii=False)
if '--go' in sys.argv:
    from pl_rpc import call
    r = call('create_1_direction_object', args); print(r); open(os.path.join(OUT, 'submit.txt'), 'w').write(r)
else: print(len(items), 'special units, all different, max 16 colours; dry run')
