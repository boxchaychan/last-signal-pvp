"""clash.html batch 9 = CHIBI ANIMAL-FOLK WARRIORS (owner 2026-11-24: showed a 12-chibi sheet "เอาพวกนี้มาทำได้ไหม ... สวยดีออก",
picked way 2 = PixelLab designs a new set in that look, then "เจน"). 64 DIFFERENT units at 32 px (our soldiers' size), side view facing right,
all 8 classes (tank 8, warrior 10, assassin 8, shooter 10, mage 10, support 8, rider 6, special 4). Style pictures = 8 CRISP 32 px sprites of ours
(the owner's chibis shrunk to 32 px came out blurry, so they are NOT used as style: art/incoming/clash/chibi12/style32_*.png kept as a record).
64 x 32 px = 10 generations. Dry run by default; `--go` only after "เจน"."""
import json, base64, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')); os.environ.setdefault('PL_KEY', 'proxy-injected')
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, '../..'); OUT = os.path.join(R, 'art/incoming/clash/batch9')
K = 'fierce chibi animal-folk warrior, big head about 2.5 heads tall, cool battle gear, bold dark outline, bright colours, battle ready'
CL = {
 'tank': ['lion knight with a golden tower shield', 'bear with a war hammer and a fur cape', 'rhino in spiked plate armour with a big shield', 'turtle with a shell shield and a mace',
   'bull with horned armour and a great axe', 'gorilla with stone gauntlets', 'elephant warrior with armoured tusks and a club', 'armadillo knight with a round shell shield'],
 'warrior': ['wolf swordsman with a glowing blue blade', 'tiger samurai with a katana', 'boar berserker with two axes', 'red dragon-folk spearman with a flame cape',
   'ram warrior with curled horns and a greatsword', 'badger brawler with iron claws', 'crocodile warrior with a jagged sword', 'hyena raider with a scimitar',
   'shark warrior with a trident', 'lion gladiator with a short sword and a round shield'],
 'assassin': ['fox rogue with twin daggers and a blue hood', 'rabbit ninja with a red hood and kunai', 'black panther with claw blades', 'snake assassin with poison daggers',
   'weasel thief with a curved knife', 'fennec fox shadow assassin with a dark scarf', 'raven ninja with a feathered cloak', 'mongoose duelist with a rapier'],
 'shooter': ['eagle archer with a longbow', 'owl crossbow sniper', 'raccoon throwing round bombs', 'frog blowgun hunter', 'squirrel slingshot scout', 'hawk javelin thrower',
   'monkey musketeer', 'porcupine shooting quills', 'hedgehog with a repeating crossbow', 'chameleon spear thrower'],
 'mage': ['cat mage with purple fire and a moon hat', 'penguin ice mage with a crystal staff and goggles', 'fox mage with blue fox fire', 'owl wizard with a glowing spellbook',
   'snake sorcerer with a green poison orb', 'chameleon illusionist with swirling colours', 'moth witch with glowing wings', 'octopus water mage with a water orb',
   'peacock light mage with a radiant fan', 'bat blood mage with a red orb'],
 'support': ['deer druid with a glowing antler staff', 'panda monk with a bamboo staff and a straw hat', 'owl healer with a lantern', 'sheep priest with a bell staff',
   'koala shaman with a leaf totem', 'swan priestess with a feather wand', 'goat banner bearer with a war drum', 'capybara medic with an herb bag'],
 'rider': ['monkey riding a war boar', 'mouse knight riding a frog', 'rabbit lancer riding a giant lizard', 'wolf cub riding a bear', 'cat knight riding a big war chicken', 'otter riding a turtle'],
 'special': ['nine-tailed fox spirit warrior', 'tanuki shapeshifter holding a magic leaf', 'little dragon knight with a big sword', 'phoenix-feather bird hero with a fire sword'],
}
items, keys, names = [], [], {}
for cls, lst in CL.items():
    for d in lst:
        k = f'c9_{len(keys):02d}'; items.append(f'{K}, {d}, side view facing right, full body'); keys.append(k); names[k] = f'{cls}: {d}'
assert len(items) == 64 and len(set(items)) == 64, (len(items), len(set(items)))
SP = ['batch3/raw/k3_02', 'batch3/raw/k3_18', 'batch3/raw/k3_07', 'batch3/raw/k3_14', 'batch3/raw/k3_20', 'batch4/raw/a4_00', 'batch7/raw/m7_33', 'batch6/raw/p6_08']
import io
from PIL import Image
from scipy import ndimage
import numpy as np
def clean(f):   # drop bits of the NEIGHBOUR cell at the slot edge (style copy only)
    im = Image.open(os.path.join(R, 'art/incoming/clash', f + '.png')).convert('RGBA'); a = np.asarray(im).copy(); lab, n = ndimage.label(a[..., 3] > 30)
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) < 24 and (xs.min() == 0 or ys.min() == 0 or xs.max() == a.shape[1] - 1 or ys.max() == a.shape[0] - 1): a[lab == i] = 0
    b = io.BytesIO(); Image.fromarray(a).save(b, 'PNG'); return base64.b64encode(b.getvalue()).decode()
style = [{'type': 'base64', 'base64': clean(f), 'format': 'png'} for f in SP]
args = {'description': f'tiny {K}, pixel art game sprite, side view facing right, full body', 'name': 'clash chibi animal-folk batch 9', 'view': 'sidescroller', 'style_images': style, 'item_descriptions': items}
os.makedirs(OUT, exist_ok=True); json.dump(keys, open(os.path.join(OUT, 'keys.json'), 'w'), indent=1); json.dump(names, open(os.path.join(OUT, 'items.json'), 'w'), indent=1, ensure_ascii=False)
if '--go' in sys.argv:
    from pl_rpc import call
    r = call('create_1_direction_object', args); print(r); open(os.path.join(OUT, 'submit.txt'), 'w').write(r)
else: print(len(items), 'chibi animal-folk warriors, all different; dry run')
