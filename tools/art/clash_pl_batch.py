"""clash.html: the PixelLab batch order prepared 2026-11-23 and NOT sent (paid call blocked; owner then chose the free GPT route).
create_1_direction_object, sidescroller, 64 slots of 32 x 32 for 10 generations (16-32 px band); the 8 style pictures (32 x 32, cut from the owner's
GPT sheet, art/incoming/clash/style32/) set the slot size. 27 small / medium units x 2 versions + 10 attack-pose tries.
Dry run by default; `--go` sends it (ONLY after the owner says "เจน" and the price is said). PixelLab key: the cloud proxy (PL_KEY=proxy-injected)."""
import json, base64, sys, os, glob
sys.path.insert(0, '/home/user/last-signal-pvp/tools')
os.environ.setdefault('PL_KEY', 'proxy-injected')
from pl_rpc import call
U = {
 'saw':      'small machine-tribe robot warrior with a spinning circular saw blade arm, steel grey with orange warning stripes, yellow visor light',
 'drone':    'small flying machine-tribe blade drone hovering in the air, two spinning blades, steel grey with orange warning stripes, yellow eye light',
 'turret':   'machine-tribe walking gun turret robot on short legs with a long cannon barrel, steel grey with orange warning stripes, cyan light',
 'tesla':    'machine-tribe tesla robot mage with a glowing electric coil on its head and crackling blue sparks, steel grey with orange warning stripes',
 'repair':   'small machine-tribe repair robot holding a big wrench, green cross light on its chest, steel grey with orange warning stripes',
 'wolf':     'animal-tribe wolf warrior on four legs, snarling, brown and cream fur, leather straps, green war paint',
 'leopard':  'animal-tribe leopard assassin crouching on four legs, spotted golden fur, leather straps, green war paint',
 'porcupine':'animal-tribe porcupine archer on four legs with big quills raised, brown fur, cream quills, green war paint',
 'owl':      'animal-tribe owl shaman standing, holding a small bone staff with feathers, brown and cream feathers, green war paint, glowing green eyes',
 'deer':     'animal-tribe deer healer standing on four legs, glowing green antlers, brown and cream fur, leather straps',
 'tentacle': 'alien-tribe tentacle warrior, squid-like head, long whip tentacle arm, teal skin, purple armour suit, pink glowing eyes',
 'cloaker':  'alien-tribe stealth assassin, slim body with a half-transparent shimmer, long claws, teal skin, purple suit, pink glowing eyes',
 'laser':    'alien-tribe laser gunner holding a ray gun, big head, teal skin, purple suit, pink glowing eyes',
 'psychic':  'alien-tribe big-headed psychic floating above the ground holding a glowing pink orb, teal skin, purple robe',
 'ufo':      'small alien-tribe flying saucer with a glass dome and a pink tractor beam light underneath, purple and teal metal',
 'blob':     'small alien-tribe jelly blob with one big eye, translucent teal green',
 'shield':   'human-tribe shield soldier with a big tower shield and a short sword, steel helmet with red plume, blue tunic',
 'spear':    'human-tribe spearman with helmet and long spear, steel armour, blue tunic, red plume',
 'hood':     'human-tribe hooded assassin with two daggers, dark blue hood and cloak, brown leather',
 'archer':   'human-tribe archer drawing a bow, blue and white cloth, brown leather hood',
 'firemage': 'human-tribe fire mage in a blue and white robe with a pointed hat, holding a staff with a fire orb',
 'priest':   'human-tribe priest in a white and blue robe holding a golden staff with a glowing light',
 'horned':   'demon-tribe horned demon warrior with a curved blade, crimson skin, black horns, orange glowing eyes, glowing lava cracks',
 'imp':      'small demon-tribe flying imp with bat wings and a pitchfork, crimson skin, black horns, orange fire eyes',
 'breather': 'demon-tribe fire-breathing demon with a big jaw breathing orange flames, dark red skin, black horns',
 'witch':    'demon-tribe hell witch in a black and crimson robe with horns, holding a staff with a cursed orange flame',
 'bloodghost':'demon-tribe blood ghost floating, ragged crimson cloak, red glowing eyes, dripping blood wisps',
}
ATK = ['spear', 'archer', 'wolf', 'saw', 'turret', 'imp', 'horned', 'laser', 'tentacle', 'firemage']
items, keys = [], []
for k, d in U.items():
    for v in (1, 2): items.append(d + ', side view facing right, full body'); keys.append(f'{k}_{v}')
for k in ATK: items.append(U[k] + ', ATTACKING pose mid-strike, side view facing right, full body'); keys.append(f'{k}_atk')
assert len(items) == 64, len(items)
style = []
for f in ['style_00_m_saw', 'style_02_a_wolf', 'style_04_e_psychic', 'style_06_h_spear', 'style_07_h_archer', 'style_08_d_imp', 'style_09_d_brute', 'style_10_g_angel']:
    style.append({'type': 'base64', 'base64': base64.b64encode(open(os.path.join(os.path.dirname(__file__), '../../art/incoming/clash/style32', f + '.png'), 'rb').read()).decode(), 'format': 'png'})
args = {'description': 'tiny chibi fantasy army unit, pixel art game sprite, side view facing right, full body, dark outline, bright colours',
        'name': 'clash small units v1', 'view': 'sidescroller', 'style_images': style, 'item_descriptions': items}
if '--go' in sys.argv:
    r = call('create_1_direction_object', args); print(r)
else:
    print(len(items), 'items;', len(style), 'style images; dry run')
