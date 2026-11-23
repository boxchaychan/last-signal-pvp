"""clash.html batch 4 (owner 2026-11-23 "ดูไม่ดุเลยไม่เท่" -> "ลองเอามาเจน64ตัวสิ"): 64 DIFFERENT FIERCE aliens, one a slot, no tiers.
Our own designs in words (movie MOOD only, no film creature copied). Style pictures = 8 of our darkest 32 x 32 sprites (knights + demons)
so the look comes out menacing. create_1_direction_object, sidescroller, 64 x 32 px = 10 generations. `--go` sends it."""
import json, base64, sys, os, glob
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')); os.environ.setdefault('PL_KEY', 'proxy-injected')
from pl_rpc import call
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, '../..'); OUT = os.path.join(R, 'art/incoming/clash/batch4')
K = 'fierce menacing chibi alien monster with a dark carapace, glowing eyes, sharp claws and spikes, aggressive crouched stance'
AL = ['bone-white mask hunter with an energy spear, black and crimson', 'cloaked stealth hunter with wrist blades, shimmering purple', 'hunter with a heavy energy rifle, dark green armour',
 'tracker with a long barbed tongue and hooks, black and red', 'spear-tailed stalker crouching on all fours, purple glow', 'sniper with a long glowing rifle and a visor, black and cyan',
 'gladiator with a curved energy glaive, crimson plates', 'eyeless alien hound with huge jaws, black and toxic green',
 'mantis warrior with scythe arms, dark green', 'acid spitting beetle soldier, black shell with green acid', 'hive drone with buzzing wings and a stinger, purple', 'burrowing worm alien with a ring of teeth, pale flesh',
 'armoured hive brute with crab claws, dark red shell', 'spider alien with eight legs and a glowing abdomen, black and neon green', 'small tick parasite swarmling, red glow', 'hive queen with a huge crest and an egg sac, purple and gold',
 'centipede alien warrior with many legs, black and orange', 'scorpion tailed alien with a glowing stinger, black and violet', 'hive bomber with a glowing explosive sac on its back, green glow', 'hive priestess with long antennae and a glowing staff, violet',
 'bio-armour trooper with a plasma rifle, black and cyan', 'heavy cyborg brute with a minigun arm, gunmetal and red lights', 'cyborg commander with a spiked helmet and an energy whip, black and gold', 'jetpack alien soldier with blue flames, dark armour',
 'shield trooper with a glowing energy barrier, black and teal', 'cyborg medic with injector needle arms, white and toxic green', 'alien engineer with a small drone on the shoulder, gunmetal', 'power armour juggernaut, huge fists, black and purple',
 'grenadier alien holding glowing grenades, dark armour', 'cyborg assassin with twin energy blades, black and magenta',
 'small leaping parasite with long legs and a tail, pale and red', 'writhing tentacle mass with many mouths, dark purple', 'bloated flesh blob with a huge mouth, sickly green', 'brain parasite riding a stolen host body, glowing pink brain',
 'shadow tentacle horror with one huge glowing eye', 'acid slime with bones floating inside, toxic green', 'spore pod walker puffing toxic spores, purple and yellow', 'symbiote warrior covered in black goo armour with white eyes',
 'infected mutant with glowing veins, grey and green', 'egg carrying crawler with glowing eggs on its back',
 'three-eyed psychic priest floating with glowing hands, purple robes', 'floating brain with dangling tentacles, pink and violet glow', 'grey alien overlord with huge black eyes and a glowing rod', 'twin grey aliens floating, linked by an energy beam',
 'void seer with a cracked glowing skull, black and cyan', 'telekinetic alien lifting floating rocks, purple aura', 'moth alien with hypnotic eye-pattern wings, dark violet', 'star mage alien with a floating crystal halo, black and white glow',
 'alien riding a giant armoured beetle', 'alien on a blade-winged hover bike', 'alien riding a six-legged beast', 'alien inside a spider-legged walker pod', 'small tripod walker machine with a heat ray', 'alien riding a flying manta creature',
 'alien riding a crawling armoured worm', 'alien in a spiked saucer chariot',
 'hulking alien warlord with a giant energy axe', 'hive titan with huge claws and a crest', 'living cannon guardian with a glowing core', 'abyssal larva boss with rows of teeth', 'alien emperor on a floating throne',
 'crystal armoured alien juggernaut', 'plague bringer alien swinging a toxic censer', 'obsidian shadow reaper alien with a scythe arm']
assert len(AL) == 64 and len(set(AL)) == 64
items = [f'{K}, {a}, side view facing right, full body' for a in AL]; keys = [f'a4_{i:02d}' for i in range(64)]
SP = [os.path.join(R, 'art/incoming/clash/batch3/raw/k3_20.png'), glob.glob(os.path.join(R, 'art/incoming/clash/batch2/raw/44_*.png'))[0], os.path.join(R, 'art/incoming/clash/batch3/raw/k3_14.png'),
      os.path.join(R, 'art/incoming/clash/batch3/raw/k3_59.png'), glob.glob(os.path.join(R, 'art/incoming/clash/batch2/raw/27_*.png'))[0], glob.glob(os.path.join(R, 'art/incoming/clash/batch2/raw/29_*.png'))[0],
      os.path.join(R, 'art/incoming/clash/style32/style_09_d_brute.png'), os.path.join(R, 'art/incoming/clash/style32/style_08_d_imp.png')]
style = [{'type': 'base64', 'base64': base64.b64encode(open(f, 'rb').read()).decode(), 'format': 'png'} for f in SP]
args = {'description': f'tiny {K}, pixel art game sprite, side view facing right, full body, dark outline', 'name': 'clash fierce aliens batch 4', 'view': 'sidescroller', 'style_images': style, 'item_descriptions': items}
os.makedirs(OUT, exist_ok=True); json.dump(keys, open(os.path.join(OUT, 'keys.json'), 'w'), indent=1); json.dump(dict(zip(keys, AL)), open(os.path.join(OUT, 'items.json'), 'w'), indent=1)
if '--go' in sys.argv: r = call('create_1_direction_object', args); print(r); open(os.path.join(OUT, 'submit.txt'), 'w').write(r)
else: print(len(items), 'aliens, all different; style:', [os.path.basename(f) for f in SP])
