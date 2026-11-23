"""clash.html batch 3 (owner 2026-11-23 "เอาคาแรคมาอย่างละตัว 64 เลย เจนใหม่" + "อัศวินทั้งหมด 64 แบบ"): 64 DIFFERENT chibi knights,
one character a slot, NO star tiers, NO repeats of batch 2's 40 enemy knights. Look in words only (other artists' pictures never uploaded).
Style pictures = 8 of our own 32 x 32 units. create_1_direction_object, sidescroller, 64 x 32 px = 10 generations. `--go` sends it."""
import json, base64, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')); os.environ.setdefault('PL_KEY', 'proxy-injected')
from pl_rpc import call
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, '../../art/incoming/clash/batch3')
K = 'chibi knight with an oversized helm and glowing eyes in the visor'
KN = ['winged-helm silver knight with a thin rapier', 'crimson knight with a huge two-handed claymore', 'bronze heavy knight with a tall tower shield and a short gladius',
 'white templar knight with a red cross tabard and a longsword', 'teal knight with a trident', 'violet knight with two sickles', 'bell-helm knight swinging a war bell on a chain',
 'forest ranger knight with a longbow and a leaf cloak', 'navy blue knight with a heavy crossbow on the shoulder', 'black and gold knight with a flanged mace and a kite shield',
 'silver knight with a unicorn horn on the helm and a glaive', 'knight wearing a grey wolf pelt over the armour with a bearded axe', 'copper clockwork knight with a gear shield and a hammer',
 'pearl white holy knight with a feathered helm and a shining spear', 'sapphire mage knight with a crystal staff', 'ruby knight with a flaming rapier',
 'emerald knight with a leaf staff and small leaf wings', 'sand and gold pharaoh knight with a khopesh sword', 'red lacquered samurai knight with a katana',
 'viking knight with a round wooden shield and a short sword, fur collar', 'bat-wing helm knight with two daggers', 'owl helm knight with a small crossbow',
 'golden lion helm knight with a sword and a lion shield', 'eagle helm knight with a spear and a feather cape', 'bear pelt heavy knight with a giant maul',
 'snake helm knight with a serpent shaped spear', 'fox helm agile knight with a short sword and an orange cape', 'boar tusk helm knight with a spiked club',
 'stag antler helm knight with a wooden staff', 'rose knight with pink petals on the armour and a thin sword', 'moon knight with a crescent helm and a crescent blade',
 'arc knight with crackling blue armour and a lightning hammer', 'deep sea knight with a round diving helm and a harpoon', 'mushroom cap helm knight with a wooden club',
 'candle knight with a melted wax helm and a candle staff', 'clockwork knight with a swinging pendulum blade', 'horse-head helm chess knight with a sword',
 'scarecrow knight with straw sticking out and a pitchfork', 'pumpkin head knight with a lantern sword', 'zombie knight with a green rotting face and a cracked shield',
 'vampire knight with a high collar cape and a bat shaped axe', 'mummy knight wrapped in bandages with a golden staff', 'small winged white knight with a holy lantern',
 'demon horned knight with bat wings and a hellfire chain', 'dwarf knight, short with a big braided beard and a double axe', 'slim elf knight with a leaf shaped blade and a green cape',
 'giant knight with a tree trunk club', 'tiny knight riding a mountain goat', 'knight riding a grey wolf', 'knight with a small cannon on the shoulder',
 'knight with a clockwork drill lance', 'mimic knight carrying a treasure chest with teeth', 'knight with a spiked shield on each arm', 'bard knight playing a lute',
 'alchemist knight with potion flasks on the belt and a flask in hand', 'monk knight with a quarterstaff and prayer beads', 'beastmaster knight with a falcon on the arm',
 'ninja knight with a chain sickle', 'yeti fur knight with an ice pick', 'void knight with a black hole in the visor holding a dark orb',
 'gardener knight with giant shears', 'blacksmith knight with tongs and a glowing hot sword', 'jester knight with a striped helm and juggling daggers', 'banker knight with a sack of gold coins and a club']
assert len(KN) == 64 and len(set(KN)) == 64
items = [f'{K}, {k}, side view facing right, full body' for k in KN]; keys = [f'k3_{i:02d}' for i in range(64)]
style = [{'type': 'base64', 'base64': base64.b64encode(open(os.path.join(HERE, '../../art/incoming/clash/style32', f + '.png'), 'rb').read()).decode(), 'format': 'png'}
         for f in ['style_06_h_spear', 'style_10_g_angel', 'style_01_m_shield', 'style_09_d_brute', 'style_07_h_archer', 'style_00_m_saw', 'style_11_g_titan', 'style_08_d_imp']]
args = {'description': f'tiny {K}, pixel art game sprite, side view facing right, full body, dark outline', 'name': 'clash knights batch 3', 'view': 'sidescroller', 'style_images': style, 'item_descriptions': items}
os.makedirs(OUT, exist_ok=True); json.dump(keys, open(os.path.join(OUT, 'keys.json'), 'w'), indent=1); json.dump(dict(zip(keys, KN)), open(os.path.join(OUT, 'items.json'), 'w'), indent=1, ensure_ascii=False)
if '--go' in sys.argv: r = call('create_1_direction_object', args); print(r); open(os.path.join(OUT, 'submit.txt'), 'w').write(r)
else: print(len(items), 'knights, all different; dry run')
