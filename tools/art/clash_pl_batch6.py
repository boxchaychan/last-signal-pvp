"""clash.html batch 6 (owner 2026-11-23 "เอาสัตว์ดึกดำบรรพ์ เจน64ตัว", after "สัตว์ไม่น่าจะสู้กับเผ่าอื่นได้เลย"): the animal tribe becomes
PREHISTORIC beasts. 64 DIFFERENT, one a slot, no tiers: theropods, armoured / horned, long necks + crests, flyers, ice-age megafauna, giant
reptiles + bugs, 12 tribal riders. Style pictures = 8 of the fierce batch 5 sprites. create_1_direction_object, 64 x 32 px = 10 generations."""
import json, base64, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')); os.environ.setdefault('PL_KEY', 'proxy-injected')
from pl_rpc import call
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, '../..'); OUT = os.path.join(R, 'art/incoming/clash/batch6')
K = 'fierce chibi prehistoric beast of the animal tribe, battle scars, tribal war paint and bone armour, glowing eyes, aggressive stance'
AN = ['tyrannosaurus rex roaring', 'velociraptor pack hunter with sickle claws', 'spinosaurus with a tall back sail', 'allosaurus with jagged teeth', 'carnotaurus with two short horns', 'baryonyx with long hooked claws',
 'dilophosaurus with an open neck frill spitting venom', 'giganotosaurus huge hunter', 'utahraptor with feathers', 'tiny compsognathus swarm biter',
 'triceratops with three horns', 'styracosaurus with a spiked frill', 'pachyrhinosaurus with a thick nose boss', 'ankylosaurus with a club tail', 'stegosaurus with back plates and tail spikes',
 'kentrosaurus covered in spikes', 'pachycephalosaurus head butter with a dome skull', 'small protoceratops with a beak', 'nodosaurus with heavy armour plates', 'euoplocephalus with a spiked back',
 'brachiosaurus with a long neck', 'diplodocus with a whip tail', 'parasaurolophus with a hollow head crest calling', 'iguanodon with thumb spikes', 'therizinosaurus with giant scythe claws', 'gallimimus fast runner',
 'pteranodon with a long crest', 'quetzalcoatlus giant flyer', 'dimorphodon with a big beak', 'rhamphorhynchus with a long tail', 'archaeopteryx feathered glider', 'meganeura giant dragonfly',
 'woolly mammoth with long tusks', 'woolly rhinoceros with a huge horn', 'smilodon sabertooth cat', 'dire wolf with a thick mane', 'cave bear standing tall', 'giant ground sloth with long claws',
 'glyptodon with a domed armour shell', 'terror bird with a huge hooked beak', 'megaloceros giant deer with huge antlers', 'entelodont hell pig with big jaws', 'short-faced bear running', 'cave lion with a short mane',
 'deinosuchus giant crocodile', 'titanoboa giant snake coiled', 'megalania giant monitor lizard', 'dimetrodon with a sail back', 'arthropleura giant millipede', 'small trilobite crawler',
 'sarcosuchus with a long snout', 'postosuchus walking upright',
 'caveman warrior riding a raptor', 'tribal warrior riding a triceratops', 'shaman riding a woolly mammoth', 'hunter riding a pteranodon', 'warrior riding a sabertooth cat', 'archer riding a woolly rhinoceros',
 'spear rider on a gallimimus', 'war drummer riding a stegosaurus', 'chieftain riding a tyrannosaurus rex', 'warrior riding a terror bird', 'scout riding a dire wolf', 'slinger riding a glyptodon']
assert len(AN) == 64 and len(set(AN)) == 64, (len(AN), len(set(AN)))
items = [f'{K}, {a}, side view facing right, full body' for a in AN]; keys = [f'p6_{i:02d}' for i in range(64)]
SP = [os.path.join(R, f'art/incoming/clash/batch5/raw/b5_{n}.png') for n in ('09', '57', '15', '10', '00', '59', '27', '23')]
style = [{'type': 'base64', 'base64': base64.b64encode(open(f, 'rb').read()).decode(), 'format': 'png'} for f in SP]
args = {'description': f'tiny {K}, pixel art game sprite, side view facing right, full body, dark outline', 'name': 'clash prehistoric batch 6', 'view': 'sidescroller', 'style_images': style, 'item_descriptions': items}
os.makedirs(OUT, exist_ok=True); json.dump(keys, open(os.path.join(OUT, 'keys.json'), 'w'), indent=1); json.dump(dict(zip(keys, AN)), open(os.path.join(OUT, 'items.json'), 'w'), indent=1)
if '--go' in sys.argv: r = call('create_1_direction_object', args); print(r); open(os.path.join(OUT, 'submit.txt'), 'w').write(r)
else: print(len(items), 'prehistoric beasts, all different')
