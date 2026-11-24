"""clash.html batch 13 = DEMON TRIBE in true 16-bit (owner 2026-11-24 "ปีศาจต่อ" right after "สั่งแบบเดิม" for the machines;
same recipe as batch 11). 64 DIFFERENT demon-tribe units at 32 px (our soldiers' size), side view
facing right, all 8 classes, "16-bit console pixel art" in the text AND max_colors = 16. Style pictures = 4 god units from batch 1 + 4 crisp picks
of ours (NOT a previous batch together with the same list: batch 10 lesson). 64 x 32 px = 10 generations. Dry run by default; `--go` sends."""
import json, base64, sys, os, io
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')); os.environ.setdefault('PL_KEY', 'proxy-injected')
import numpy as np
from PIL import Image
from scipy import ndimage
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, '../..'); OUT = os.path.join(R, 'art/incoming/clash/batch13')
K = 'demon-tribe hell warrior, 16-bit console pixel art, chibi proportions, crimson and black with orange hellfire glow, horns, bold dark outline, few flat colours, menacing and fierce'
CL = {
 'tank': ['hell knight with a burning tower shield', 'lava golem with cracked molten skin', 'bone fortress demon with a rib shield', 'obsidian brute wrapped in chains',
   'armoured hellhound guard', 'iron maiden demon with spikes', 'molten rock turtle demon', 'gargoyle with stone wings as a shield'],
 'warrior': ['horned demon with a curved blade', 'devil with a flaming whip', 'executioner demon with a great axe', 'four-armed demon with four swords', 'minotaur demon with a fire hammer',
   'dark knight with a cursed greatsword', 'blood ogre with a cleaver', 'ram-horned berserker with claws', 'skeleton champion with a bone sword', 'chain reaper demon with a hook'],
 'spear': ['devil with a trident', 'hell pikeman with a burning spear', 'scorpion-tailed lancer demon', 'skeleton with a bone spear', 'serpent demon with a halberd', 'winged demon with a long lance'],
 'assassin': ['shadow imp with twin daggers', 'demon queen with sharp claws', 'hellcat stalker', 'masked night demon with twin sickles', 'ghost assassin with a spectral blade', 'spider demon with fangs'],
 'shooter': ['imp throwing fireballs', 'skull archer with a bone bow', 'hell crossbowman', 'lava spitting worm demon', 'cursed arrow wraith', 'demon with a brimstone cannon',
   'flying eyeball demon shooting a beam', 'bat demon spitting fire', 'bone javelin thrower', 'goblin demon with a fire bomb sack'],
 'mage': ['hell witch with a cursed flame staff', 'lich with green soul fire', 'blood mage with a red orb', 'shadow warlock with a dark tome', 'fire elemental demon', 'necromancer with a skull staff', 'plague demon with a toxic censer'],
 'support': ['dark priest with a bell', 'war drum demon', 'soul lantern bearer', 'blood shaman with a skull totem', 'banner devil with a flaming flag', 'cultist chanter with a black book', 'healing slime demon'],
 'rider': ['knight riding a nightmare horse', 'imp riding a hellhound', 'demon riding a giant bat', 'skeleton riding a bone horse', 'demon riding a lava salamander', 'rider on a giant demon spider'],
 'special': ['floating demon skull on fire', 'living hellfire cauldron', 'three-faced demon idol', 'tentacle horror from a portal'],
}
items, keys, names = [], [], {}
for cls, lst in CL.items():
    for d in lst:
        k = f'c13_{len(keys):02d}'; items.append(f'{K}, {d}, side view facing right, full body'); keys.append(k); names[k] = f'{cls}: {d}'
assert len(items) == 64 and len(set(items)) == 64, (len(items), len(set(items)))
SP = ['batch1/raw/32_d_horned_1', 'batch1/raw/34_d_breather_1', 'batch1/raw/36_d_witch_1', 'batch1/raw/38_d_bloodghost_1', 'batch3/raw/k3_02', 'batch3/raw/k3_14', 'batch7/raw/m7_12', 'batch3/raw/k3_10']
def clean(f):   # drop bits of the NEIGHBOUR cell at the slot edge (style copy only)
    a = np.asarray(Image.open(os.path.join(R, 'art/incoming/clash', f + '.png')).convert('RGBA')).copy(); lab, n = ndimage.label(a[..., 3] > 30)
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) < 24 and (xs.min() == 0 or ys.min() == 0 or xs.max() == a.shape[1] - 1 or ys.max() == a.shape[0] - 1): a[lab == i] = 0
    b = io.BytesIO(); Image.fromarray(a).save(b, 'PNG'); return base64.b64encode(b.getvalue()).decode()
style = [{'type': 'base64', 'base64': clean(f), 'format': 'png'} for f in SP]
args = {'description': f'tiny {K}, pixel art game sprite, side view facing right, full body', 'name': 'clash demon tribe 16-bit batch 13', 'view': 'sidescroller',
        'style_images': style, 'item_descriptions': items, 'max_colors': 16}
os.makedirs(OUT, exist_ok=True); json.dump(keys, open(os.path.join(OUT, 'keys.json'), 'w'), indent=1); json.dump(names, open(os.path.join(OUT, 'items.json'), 'w'), indent=1, ensure_ascii=False)
if '--go' in sys.argv:
    from pl_rpc import call
    r = call('create_1_direction_object', args); print(r); open(os.path.join(OUT, 'submit.txt'), 'w').write(r)
else: print(len(items), 'demon-tribe units, all different, max 16 colours; dry run')
