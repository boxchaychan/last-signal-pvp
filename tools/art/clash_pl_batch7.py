"""clash.html batch 7 (owner 2026-11-23 "เอาพวกสัตว์ในเทพนิยายมาดิ มังกร ม้ายูนิคอร์นพวกนี้"): 64 DIFFERENT mythical beasts, one a slot,
no tiers: dragons, horses / horned, mythic birds, mythic beasts, Thai Himmapan creatures, serpents, elemental spirits, 6 riders.
Public-domain myths only, own designs. Style pictures = 8 fierce sprites from batches 5 + 6. 64 x 32 px = 10 generations."""
import json, base64, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')); os.environ.setdefault('PL_KEY', 'proxy-injected')
from pl_rpc import call
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, '../..'); OUT = os.path.join(R, 'art/incoming/clash/batch7')
K = 'fierce chibi mythical beast, majestic and dangerous, glowing eyes, bold silhouette, battle ready stance'
AN = ['red fire dragon breathing flames', 'frost dragon with ice crystal spikes', 'storm dragon crackling with lightning', 'poison swamp dragon dripping venom', 'wyvern with two legs and big wings',
 'three-headed hydra', 'long eastern dragon flying with whiskers', 'small baby dragon with stubby wings', 'skeletal bone dragon', 'dragon turtle with a spiked shell',
 'white unicorn with a glowing horn', 'pegasus with white feathered wings', 'nightmare horse with a flaming mane', 'kirin with scales and a single antler', 'eight-legged warhorse',
 'kelpie water horse with a seaweed mane', 'hippogriff half eagle half horse', 'karkadann with one huge horn',
 'phoenix wreathed in fire', 'griffin with an eagle head and lion body', 'thunderbird with storm clouds', 'roc giant bird with huge talons', 'garuda bird warrior with a golden crown', 'hamsa sacred swan with golden feathers',
 'cockatrice rooster serpent', 'simurgh with rainbow tail feathers',
 'chimera with lion, goat and snake heads', 'manticore with a scorpion tail', 'three-headed guard dog cerberus', 'giant chained wolf with glowing eyes', 'golden lion with impenetrable hide', 'sphinx with a lion body and human head',
 'basilisk serpent lizard with a deadly gaze', 'nine-tailed fox with blue fox fire', 'hellhound wreathed in black flames', 'behemoth huge horned beast', 'baku dream eater with a trunk', 'jackalope rabbit with antlers',
 'naga serpent king with a jeweled crown and many heads', 'rajasi royal lion of the himmapan forest', 'kotchasi elephant-headed lion', 'makara sea dragon with an elephant trunk', 'kinnaree half bird half woman dancer',
 'hera crocodile dragon', 'lion with a naga serpent tail', 'erawan three-headed white elephant',
 'kraken tentacle beast crawling on land', 'leviathan sea serpent rising', 'world serpent biting its tail', 'sea serpent with fins', 'two-headed serpent', 'golden scarab beast',
 'will-o-wisp fox made of blue light', 'lava salamander', 'frost wolf spirit', 'thunder tiger with lightning stripes', 'forest spirit stag with mossy antlers', 'shadow panther made of smoke',
 'tribal warrior riding a griffin', 'rider on a pegasus with a lance', 'warrior riding a small dragon', 'shaman riding a unicorn', 'warrior riding a three-headed hellhound', 'archer riding a phoenix']
assert len(AN) == 64 and len(set(AN)) == 64, (len(AN), len(set(AN)))
items = [f'{K}, {a}, side view facing right, full body' for a in AN]; keys = [f'm7_{i:02d}' for i in range(64)]
SP = [os.path.join(R, f'art/incoming/clash/batch6/raw/p6_{n}.png') for n in ('00', '08', '19', '33', '26')] + [os.path.join(R, f'art/incoming/clash/batch5/raw/b5_{n}.png') for n in ('09', '18', '32')]
style = [{'type': 'base64', 'base64': base64.b64encode(open(f, 'rb').read()).decode(), 'format': 'png'} for f in SP]
args = {'description': f'tiny {K}, pixel art game sprite, side view facing right, full body, dark outline', 'name': 'clash mythical batch 7', 'view': 'sidescroller', 'style_images': style, 'item_descriptions': items}
os.makedirs(OUT, exist_ok=True); json.dump(keys, open(os.path.join(OUT, 'keys.json'), 'w'), indent=1); json.dump(dict(zip(keys, AN)), open(os.path.join(OUT, 'items.json'), 'w'), indent=1)
if '--go' in sys.argv: r = call('create_1_direction_object', args); print(r); open(os.path.join(OUT, 'submit.txt'), 'w').write(r)
else: print(len(items), 'mythical beasts, all different')
