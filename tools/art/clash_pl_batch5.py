"""clash.html batch 5 (owner 2026-11-23 "ทำเผ่าสัตว์มาเลยนะ64ตัว"): 64 DIFFERENT fierce ANIMAL tribe units, one a slot, no tiers.
Fierce look like the alien batch (owner: cute = "ไม่เท่"). Style pictures = 8 of our own 32 x 32 sprites (batch 3 animal fighters, the
GPT wolf / rhino, the brute, the bat-helm knight). create_1_direction_object, sidescroller, 64 x 32 px = 10 generations. `--go` sends it."""
import json, base64, sys, os, glob
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')); os.environ.setdefault('PL_KEY', 'proxy-injected')
from pl_rpc import call
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, '../..'); OUT = os.path.join(R, 'art/incoming/clash/batch5')
K = 'fierce chibi beast warrior of the animal tribe, tribal war paint, bone and leather armour, glowing eyes, sharp claws, aggressive stance'
AN = ['dire wolf alpha on four legs with a scarred face', 'wolf berserker standing on two legs with two hand axes', 'jackal archer with a short bow', 'hyena scavenger with a bone club and a cackling grin',
 'fox assassin with two curved daggers', 'tiger warrior with huge claws and stripes', 'black panther stalker crouching low', 'lion chieftain with a big mane and a greatsword', 'lynx scout with tufted ears and a bow',
 'sabertooth beast on four legs with long fangs', 'armoured grizzly bear brute', 'polar bear shieldbearer with an ice shield', 'panda monk with a bamboo staff', 'bear shaman holding a totem pole',
 'bull warrior with a giant hammer and a nose ring', 'armoured rhino charger on four legs', 'bison charger with a shaggy mane', 'ram knight with curled horns and a round shield', 'stag druid with glowing antlers and a staff',
 'elk spearman with wide antlers', 'shaggy yak warrior with a heavy axe', 'boar brute with big tusks and a spiked club', 'warthog berserker with a cleaver', 'gorilla smasher with huge fists',
 'orangutan shaman with a gourd and feathers', 'baboon slinger with a sling', 'monkey trickster with a staff', 'crocodile warrior with a heavy club', 'komodo dragon spearman', 'turtle guardian with a big shell shield',
 'cobra mystic with a hooded head and a staff', 'chameleon assassin half camouflaged', 'eagle archer with a longbow and spread wings', 'owl sage with a lantern', 'raven scout with a dagger and black feathers',
 'hawk knight with wing armour and a spear', 'vulture scavenger with a hooked blade', 'rooster duelist with a rapier', 'peacock mystic with a glowing tail fan', 'mantis blade fighter with scythe arms',
 'scorpion warrior with a raised stinger', 'beetle knight with a horn and shell armour', 'hornet queen with a stinger spear', 'shark brute walking on land with a jaw full of teeth', 'frog shaman with a poison staff',
 'axolotl healer with glowing gills', 'otter fighter with a trident', 'walrus tank with long tusks and a club', 'rat rogue with a rusty dagger', 'porcupine quill shooter', 'hedgehog roller with spikes',
 'badger berserker with claws', 'wolverine claw fighter', 'squirrel scout with a slingshot', 'battle-scarred rabbit swordsman', 'kangaroo boxer with gloves', 'tribal warrior riding a wild boar',
 'lizard warrior riding a raptor', 'monkey riding a grey wolf', 'small warrior riding a war elephant', 'warrior riding a giant eagle', 'goat rider with a lance', 'beastmaster with two small wolves', 'gecko climber with sticky hands and a knife']
assert len(AN) == 64 and len(set(AN)) == 64, (len(AN), len(set(AN)))
items = [f'{K}, {a}, side view facing right, full body' for a in AN]; keys = [f'b5_{i:02d}' for i in range(64)]
SP = [os.path.join(R, f'art/incoming/clash/batch3/raw/k3_{n}.png') for n in ('24', '26', '27', '28', '20')] + [os.path.join(R, 'art/incoming/clash/style32', f) for f in ('style_02_a_wolf.png', 'style_03_a_rhino.png', 'style_09_d_brute.png')]
style = [{'type': 'base64', 'base64': base64.b64encode(open(f, 'rb').read()).decode(), 'format': 'png'} for f in SP]
args = {'description': f'tiny {K}, pixel art game sprite, side view facing right, full body, dark outline', 'name': 'clash animal tribe batch 5', 'view': 'sidescroller', 'style_images': style, 'item_descriptions': items}
os.makedirs(OUT, exist_ok=True); json.dump(keys, open(os.path.join(OUT, 'keys.json'), 'w'), indent=1); json.dump(dict(zip(keys, AN)), open(os.path.join(OUT, 'items.json'), 'w'), indent=1)
if '--go' in sys.argv: r = call('create_1_direction_object', args); print(r); open(os.path.join(OUT, 'submit.txt'), 'w').write(r)
else: print(len(items), 'animals, all different; style:', [os.path.basename(f) for f in SP])
