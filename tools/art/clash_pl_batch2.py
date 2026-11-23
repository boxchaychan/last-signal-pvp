"""clash.html batch 2 (owner 2026-11-23 "ลองดิเจนสิ10เครดิต"): dark CHIBI KNIGHTS, 64 DIFFERENT slots (lesson of batch 1: never repeat a
description). The look is written in words only: the owner's two reference pictures are other artists' work (watermark / signature),
so they are not uploaded anywhere and not stored. Style pictures = 8 of our own 32 x 32 units (art/incoming/clash/style32/), so the
size and pixel look match the game. Slots: human tribe as knights, 6 classes x 3 ranks (18) + their attack poses (6) + 40 enemy / boss knights.
create_1_direction_object, sidescroller, 64 slots of 32 x 32 = 10 generations. Dry run by default; `--go` sends it."""
import json, base64, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')); os.environ.setdefault('PL_KEY', 'proxy-injected')
from pl_rpc import call
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, '../../art/incoming/clash/batch2')
K = 'chibi dark knight with an oversized great helm and glowing eyes in the visor, spiky armour, tattered cape'
HU = 'dark steel armour with silver edges, royal blue cape and plume, glowing pale blue eyes'
R = {1: 'plain simple armour', 2: 'more spikes, a tall plume, gold trim', 3: 'huge spiky armour, a giant plume, glowing blue runes, oversized weapon'}
CL = {'tank': 'holding a sword and a big tower shield', 'spear': 'holding a long spear', 'assassin': 'light armour with a hooded helm, holding two daggers',
      'archer': 'holding a big crossbow', 'mage': 'battle mage knight holding a staff with a fire orb', 'cleric': 'cleric knight holding a mace that glows with holy light'}
ATK = {'tank': 'bashing forward with the tower shield', 'spear': 'thrusting the spear forward', 'assassin': 'slashing forward with both daggers',
       'archer': 'firing the crossbow, bolt flying', 'mage': 'casting a fireball forward from the staff', 'cleric': 'swinging the glowing mace down'}
ENEMY = ['flame knight with a burning plume and a flaming battle axe, black and orange armour', 'frost knight with ice crystal armour and an ice sword, pale blue',
 'bone knight, a skeleton inside rusty armour with a notched sword', 'shadow knight wrapped in purple smoke holding a scythe', 'thunder knight with a lightning lance, yellow sparks',
 'poison knight in green armour swinging a spiked flail, toxic drips', 'golden paladin boss with a halo and a huge golden greatsword', 'black knight boss with a giant greatsword and red glowing eyes',
 'mounted knight on a small armoured horse with a lance', 'knight captain holding a tall war banner', 'halberd knight with a long halberd', 'turtle knight hiding behind a huge round shield',
 'berserker knight with two swords and a torn cape', 'knight with a morning star and a round buckler', 'knight with a dragon-shaped helm and a fire sword', 'plague knight with a beaked helm and a lantern',
 'rust knight with rusty dented armour and a broken sword', 'crystal knight made of purple crystal with a crystal spear', 'desert knight in sand coloured armour with a curved scimitar',
 'moss knight covered in vines with a wooden shield', 'blood knight in crimson armour with a whip sword', 'ghost knight, translucent green spirit armour with a spectral blade',
 'tiny squire knight with a too-big helmet and a wooden sword', 'knight drummer with a war drum on the belly', 'knight torch bearer holding a burning torch and a short sword',
 'knight with a war hammer and an anvil shaped shield', 'lancer knight with a very long jousting lance', 'jailer knight with a giant iron key and chains', 'executioner knight with a huge cleaver',
 'royal guard with a tall pike and a red plume', 'knight commander with a long cape and a baton', 'star knight with dark cosmic armour and a glowing star sword',
 'storm knight with a wind swirling cape and a curved blade', 'obsidian lava knight with cracks of magma and a stone club', 'mirror knight with a shining reflective shield',
 'hunter knight with a skull mask helm and a longbow', 'hound helm knight with a wolf shaped helmet and claws', 'cursed knight bound in chains with a broken visor',
 'tiny knight king boss with a crown on the great helm and a big sword', 'twin knight pair standing back to back, swords crossed']
items, keys = [], []
for c in CL:
    for r in (1, 2, 3): items.append(f'human-tribe {K}, {HU}, {R[r]}, {CL[c]}, side view facing right, full body'); keys.append(f'hk_{c}_{r}')
for c in CL: items.append(f'human-tribe {K}, {HU}, {CL[c]}, {ATK[c]}, attacking pose, side view facing right, full body'); keys.append(f'hk_{c}_atk')
for i, e in enumerate(ENEMY): items.append(f'{K}, {e}, side view facing right, full body'); keys.append(f'ek_{i:02d}')
assert len(items) == 64 and len(set(items)) == 64, (len(items), len(set(items)))
style = [{'type': 'base64', 'base64': base64.b64encode(open(os.path.join(HERE, '../../art/incoming/clash/style32', f + '.png'), 'rb').read()).decode(), 'format': 'png'}
         for f in ['style_06_h_spear', 'style_10_g_angel', 'style_01_m_shield', 'style_09_d_brute', 'style_07_h_archer', 'style_00_m_saw', 'style_11_g_titan', 'style_08_d_imp']]
args = {'description': f'tiny {K}, pixel art game sprite, side view facing right, full body, dark outline', 'name': 'clash knights batch 2', 'view': 'sidescroller', 'style_images': style, 'item_descriptions': items}
os.makedirs(OUT, exist_ok=True); json.dump(keys, open(os.path.join(OUT, 'keys.json'), 'w'), indent=1); json.dump(items, open(os.path.join(OUT, 'items.json'), 'w'), indent=1)
if '--go' in sys.argv: r = call('create_1_direction_object', args); print(r); open(os.path.join(OUT, 'submit.txt'), 'w').write(r)
else: print(len(items), 'items, all different;', len(style), 'style images; dry run')
