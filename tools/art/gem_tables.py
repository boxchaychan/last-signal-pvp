#!/usr/bin/env python3
# Tables for gem.html (the match-3 battle): prints two JS literals to paste between the `/*MSH*/` and `/*FXT*/` markers.
#   python3 tools/art/gem_tables.py            -> prints them
#   python3 tools/art/gem_tables.py --write    -> rewrites the two marked lines in gem.html
# MSH = cell size + feet of every monster sheet in art/action/mobs_hr/ (rows walk / attack / death / hurt, 6 frames, facing right).
# FXT = the PVFX Foundry effects (CC0, art/pvfx/) the game plays: [path, w, h, pivot x, pivot y, frames, ms per frame or list].
import json, re, sys
FX = {
    'punch': 'impacts/punch-hit', 'crit': 'impacts/crit-hit', 'slam': 'impacts/ground-slam', 'ring': 'impacts/shockwave-ring', 'rock': 'impacts/rock-shatter',
    'spike': 'nature/earth-spike', 'fireball': 'fire/fireball-impact', 'meteor': 'fire/meteor-strike', 'boom': 'explosions/small-explosion', 'bigboom': 'explosions/big-explosion',
    'heal': 'holy/holy-heal', 'bubble': 'holy/shield-bubble', 'block': 'holy/barrier-block', 'shatter': 'arcane/shield-shatter', 'aura': 'status/power-up-aura',
    'firework': 'explosions/firework-burst', 'claw': 'melee/shadow-claw', 'blood': 'impacts/blood-splat', 'curse': 'shadow/curse', 'spore': 'nature/spore-burst',
    'poisoned': 'status/poisoned', 'burning': 'status/burning-aura', 'stun': 'status/stun-stars', 'bolt': 'lightning/lightning-strike', 'circle': 'arcane/magic-circle',
    'aburst': 'explosions/arcane-burst', 'dust': 'smoke/dust-puff'}
def tables():
    idx = json.load(open('art/action/mobs_hr/index.json'))
    msh = '{' + ','.join('%s:[%d,%d,%d,%d]' % (k, v['w'], v['h'], v['fx'], v['fy']) for k, v in idx.items()) + '}'
    out = []
    for k, p in FX.items():
        m = json.load(open('art/pvfx/%s/manifest.json' % p)); fr = m['frames']; w, h = m['source_size']
        ms = [round(f['duration']['numerator_ms'] / f['duration'].get('denominator', 1)) for f in fr]
        for i, f in enumerate(fr):
            s = f['sheet']; assert (s['x'], s['y']) == (i % 8 * w, i // 8 * h), (p, i)     # 8 columns, row by row
        d = str(ms[0]) if len(set(ms)) == 1 else '[' + ','.join(map(str, ms)) + ']'
        out.append("%s:['%s',%d,%d,%d,%d,%d,%s%s]" % (k, p, w, h, m['pivot'][0], m['pivot'][1], len(fr), d, ',1' if m['loop_mode'] != 'none' else ''))
    return msh, '{' + ','.join(out) + '}'
if __name__ == '__main__':
    msh, fxt = tables()
    if '--write' in sys.argv:
        s = open('gem.html', encoding='utf-8').read()
        s, a = re.subn(r'/\*MSH\*/.*?/\*\/MSH\*/', lambda _: '/*MSH*/' + msh + '/*/MSH*/', s, flags=re.S); s, b = re.subn(r'/\*FXT\*/.*?/\*\/FXT\*/', lambda _: '/*FXT*/' + fxt + '/*/FXT*/', s, flags=re.S)
        assert a == 1 and b == 1, (a, b); open('gem.html', 'w', encoding='utf-8').write(s); print('gem.html updated')
    else:
        print('const MSH = ' + msh + ';'); print('const FXT = ' + fxt + ';')
