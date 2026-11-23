"""clash.html: ONE PixelLab order for the 24 missing units (owner 2026-11-23 "ยืนยันเจน", 10 credits).
create_1_direction_object, sidescroller, 64 slots of 32 x 32 for 10 generations (16-32 px band); the 8 style pictures (32 x 32, cut from the
owner's GPT sheet, art/incoming/clash/style32/) set the slot size and the look. 24 units x 2 versions + baby jelly x 2 + buffalo x 2 + a third
try of the 12 hardest designs. Slot names in art/incoming/clash/batch1/keys.json.
Dry run by default; `--go` sends it (ONLY after the owner says "เจน" and the price is said). PixelLab key: the cloud proxy (PL_KEY=proxy-injected)."""
import json, base64, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
os.environ.setdefault('PL_KEY', 'proxy-injected')
from pl_rpc import call
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, '../../art/incoming/clash/batch1')
M = 'steel grey with orange warning stripes'; A = 'brown and cream fur, leather straps, green war paint'; E = 'teal skin, purple suit, pink glowing eyes'
H = 'blue tunic, steel armour'; D = 'crimson skin, black horns, orange glowing eyes'; G = 'white and gold armour, light blue glow, golden halo'
U = {
 'm_drone':   f'small flying machine-tribe blade drone hovering in the air, two spinning blades, {M}, yellow eye light',
 'm_turret':  f'machine-tribe walking gun turret robot on short legs with a long cannon barrel pointing right, {M}, cyan light',
 'm_tesla':   f'machine-tribe tesla robot mage with a glowing electric coil on its head and crackling blue sparks, {M}',
 'm_repair':  f'small machine-tribe repair robot holding a big wrench, green cross light on its chest, {M}',
 'a_leopard': 'animal-tribe leopard assassin crouching on four legs, spotted golden fur, leather straps, green war paint',
 'a_porcupine': 'animal-tribe porcupine archer on four legs with big quills raised, brown fur, cream quills, green war paint',
 'a_owl':     'animal-tribe owl shaman standing, holding a small bone staff with feathers, brown and cream feathers, green war paint, glowing green eyes',
 'a_deer':    f'animal-tribe deer healer standing on four legs, glowing green antlers, {A}',
 'e_tentacle': f'alien-tribe tentacle warrior, squid-like head, long whip tentacle arm, {E}',
 'e_cloaker': f'alien-tribe stealth assassin, slim body with a half-transparent shimmer, long claws, {E}',
 'e_laser':   f'alien-tribe laser gunner holding a ray gun, big head, {E}',
 'e_ufo':     'small alien-tribe flying saucer with a glass dome and a pink tractor beam light underneath, purple and teal metal',
 'h_shield':  f'human-tribe shield soldier with a big tower shield and a short sword, steel helmet with red plume, {H}',
 'h_hood':    'human-tribe hooded assassin with two daggers, dark blue hood and cloak, brown leather',
 'h_firemage': 'human-tribe fire mage in a blue and white robe with a pointed hat, holding a staff with a fire orb',
 'h_priest':  'human-tribe priest in a white and blue robe holding a golden staff with a glowing light',
 'd_horned':  f'demon-tribe horned demon warrior with a curved blade, {D}, glowing lava cracks',
 'd_breather': 'demon-tribe fire-breathing demon with a big jaw breathing orange flames, dark red skin, black horns',
 'd_witch':   'demon-tribe hell witch in a black and crimson robe with horns, holding a staff with a cursed orange flame',
 'd_bloodghost': 'demon-tribe blood ghost floating, ragged crimson cloak, red glowing eyes, dripping blood wisps',
 'g_lightwar': f'god-tribe light warrior with a glowing light-blue greatsword, {G}',
 'g_lightarcher': f'god-tribe light archer drawing a glowing golden bow, small white wings, {G}',
 'g_oracle':  'god-tribe oracle in a long white and gold robe holding a staff topped with a glowing blue crystal, floating slightly, golden halo',
 'g_healer':  'god-tribe healing angel with white feathered wings and a white and gold dress holding a glowing green-gold light, golden halo',
}
EXTRA = {'e_babyjelly': 'small alien-tribe baby jelly blob with one big eye, translucent teal green',
         'a_buffalo': 'animal-tribe wild buffalo charging, big curved horns, dark brown fur, green war paint'}
THIRD = ['e_cloaker', 'm_tesla', 'd_bloodghost', 'e_ufo', 'm_repair', 'g_oracle', 'a_owl', 'd_witch', 'm_turret', 'm_drone', 'g_healer', 'e_tentacle']
items, keys = [], []
for k, d in U.items():
    for v in (1, 2): items.append(d + ', side view facing right, full body'); keys.append(f'{k}_{v}')
for k, d in EXTRA.items():
    for v in (1, 2): items.append(d + ', side view facing right, full body'); keys.append(f'{k}_{v}')
for k in THIRD: items.append(U[k] + ', side view facing right, full body'); keys.append(f'{k}_3')
assert len(items) == 64, len(items)
style = []
for f in ['style_00_m_saw', 'style_02_a_wolf', 'style_04_e_psychic', 'style_06_h_spear', 'style_07_h_archer', 'style_08_d_imp', 'style_09_d_brute', 'style_10_g_angel']:
    style.append({'type': 'base64', 'base64': base64.b64encode(open(os.path.join(HERE, '../../art/incoming/clash/style32', f + '.png'), 'rb').read()).decode(), 'format': 'png'})
args = {'description': 'tiny chibi fantasy army unit, pixel art game sprite, side view facing right, full body, dark outline, bright colours',
        'name': 'clash units batch 1', 'view': 'sidescroller', 'style_images': style, 'item_descriptions': items}
os.makedirs(OUT, exist_ok=True); json.dump(keys, open(os.path.join(OUT, 'keys.json'), 'w'), indent=1)
if '--go' in sys.argv:
    r = call('create_1_direction_object', args); print(r); open(os.path.join(OUT, 'submit.txt'), 'w').write(r)
else:
    print(len(items), 'items;', len(style), 'style images; dry run')
