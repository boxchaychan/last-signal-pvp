#!/usr/bin/env python3
"""horde.html monsters: cut the chosen Monster Catalog monsters (art/incoming/monster_catalog, 2x pages + atlas.json)
into uniform-grid sheets like art/action/mobs (row 0 = walk, row 1 = attack, foot point fx / fy from the top-left of a cell)
and write ONE index (art/horde/mobs/index.json) that also lists the older pixel monsters of art/action/mobs.
Run: python3 tools/art/horde_mobs.py        (free: only cuts and packs pictures we already have)"""
import json, os, sys
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CAT = os.path.join(ROOT, 'art/incoming/monster_catalog'); OUT = os.path.join(ROOT, 'art/horde/mobs'); OLD = os.path.join(ROOT, 'art/action/mobs')
# catalog monsters per map (id without the mob_ / boss_ prefix is looked up in both)
PICK = {
  'forest': ['meadow_larva', 'meadow_beetle', 'meadow_hopper', 'meadow_fuzzfly', 'vale_bee', 'vale_frog', 'vale_cap', 'vale_stump', 'forest_bristleback_hedgehog', 'forest_acorn_squirrel', 'forest_coilfang', 'forest_tusker_boar',
             'forest_ringtail', 'forest_pollenwing', 'forest_pitcher_maw', 'forest_gapebloom', 'forest_hornshell_beetle', 'forest_tusklet', 'forest_mask_goblin', 'forest_greymane_wolf', 'forest_thornpaw_cat', 'forest_mistail_fox',
             'forest_spotted_stalker', 'forest_bladearm_mantis', 'forest_tusk_warrior', 'forest_petal_wraith', 'forest_logbound_giant', 'forest_lone_packlord', 'forest_barkmaiden', 'meadow_bighopper',
             'vale_tiger', 'forest_tusk_champion', 'forest_rampage_beast', 'forest_tusk_overlord', 'forest_blazing_serpent'],
  'grave': ['graveyard_shadehound', 'graveyard_sheetghost', 'graveyard_gravegnaw', 'graveyard_shambler', 'graveyard_bone_guard', 'graveyard_rattlebones', 'graveyard_bone_archer', 'graveyard_chainbound', 'graveyard_grave_warden',
            'graveyard_broken_oath', 'graveyard_phantom_drop', 'graveyard_severed_knight', 'graveyard_gallows_tree', 'graveyard_bone_paladin', 'graveyard_veilshade', 'ruins_chestmaw', 'ruins_smogwraith', 'ruins_horned_imp',
            'ruins_lanternhead', 'ruins_haunted_frame', 'ruins_hollow_armour', 'ruins_echo_knight', 'ruins_dread_shade', 'ruins_grinning_jester', 'ruins_iron_marauder',
            'graveyard_fallen_prelate', 'ruins_crimson_swordlady', 'ruins_mirror_knight', 'graveyard_night_sovereign', 'ruins_crimson_count'],
  'volcano': ['desert_sandburrower', 'desert_dune_viper', 'desert_frillneck', 'desert_stingclaw_scorpion', 'desert_dune_wolf', 'desert_sandchick', 'desert_spinewalker', 'desert_linenwalker', 'desert_strider_bird', 'desert_fortress_tortoise',
              'desert_serpent_dancer', 'desert_gust_phantom', 'desert_sandstone_colossus', 'desert_jackal_priest', 'volcano_flamefist', 'volcano_magma_blob', 'volcano_lava_scorpion', 'volcano_emberwisp', 'volcano_kindle_imp',
              'volcano_cinder_skull', 'volcano_pyre_fiend', 'volcano_magma_hulk', 'volcano_hellfire_steed', 'volcano_flamecrest_lizard', 'volcano_pyre_dancer', 'volcano_threefold_beast',
              'desert_dune_emperor', 'desert_tomb_king', 'desert_sandfiend_sovereign', 'volcano_inferno_sovereign', 'desert_solar_tomb_lord'],
  'snow': ['snow_goldbristle_boar', 'snow_icicle_imp', 'snow_puff', 'snow_frost_pup', 'snow_snowseal', 'snow_rime_stalker', 'snow_snowhulk', 'snow_snowveil_sprite', 'snow_frost_ape', 'snow_frost_bear', 'snow_mortar_witch', 'snow_glacier_titan',
           'sky_pebble_puff', 'sky_bigbeak', 'sky_needlewing_lancer', 'sky_puffseed', 'sky_false_seraph', 'sky_crag_goat', 'sky_wyrmkit', 'sky_gale_hawk', 'sky_cloudsage', 'sky_gustfang', 'sky_haven_warden', 'sky_spear_maiden', 'sky_stormtalon',
           'snow_frostfang_alpha', 'sky_gale_knight', 'snow_tri_crown_wyrm', 'sky_winged_arbiter'],
}
OLDNAME = { 'kasa_obake': 'ร่มผี', 'tengu': 'นกเทงงู', 'ice_wraith': 'วิญญาณน้ำแข็ง', 'shroom': 'เห็ดพิษ', 'wisp': 'ภูตตะเกียง', 'monkey': 'ลิงโจร', 'kappa': 'กัปปะ', 'paper_doll': 'ตุ๊กตากระดาษ', 'goblin_archer': 'ก็อบลิน', 'wolf': 'หมาป่าเงา',
  'skeleton': 'โครงกระดูก', 'boar_guard': 'นักรบหมูป่า', 'draugr': 'ดรากร์', 'jackal_warrior': 'นักรบหมาใน', 'nekomata': 'แมวสองหาง', 'fox_spirit': 'ปีศาจจิ้งจอก', 'golem': 'โกเลมหิน', 'troll': 'โทรล', 'oni': 'ยักษ์โอนิ', 'croc_guard': 'ทหารจระเข้',
  'terracotta_general': 'นายพลดินเผา', 'ice_golem': 'โกเลมน้ำแข็ง', 'boss_treant': 'ต้นไม้อสูร', 'boss_nian': 'เหนียนโซ่ว', 'boss_orochi': 'โอโรจิแปดหัว', 'boss_jotun': 'ยักษ์โยตุน', 'jiangshi': 'ผีดิบกระโดด', 'mummy': 'มัมมี่', 'pret': 'เปรต',
  'phrai': 'ผีพราย', 'krahang': 'กระหัง', 'frost_wolf': 'หมาป่าน้ำแข็ง', 'sand_golem': 'โกเลมทราย', 'sand_scorpion': 'แมงป่องทราย', 'scarab': 'ด้วงทอง', 'cobra_priest': 'นักบวชงูเห่า', 'dwarf_berserker': 'คนแคระคลั่ง', 'khamot': 'ผีโขมด',
  'rokurokubi': 'ผีคอยาว', 'terracotta_archer': 'พลธนูดินเผา', 'toad_demon': 'ปีศาจคางคก', 'boss_chalawan': 'ชาละวัน', 'boss_sphinx': 'สฟิงซ์' }
OLDFLY = {'wisp', 'kasa_obake', 'tengu', 'ice_wraith', 'krahang', 'khamot'}
OLDSHOOT = {'goblin_archer', 'terracotta_archer', 'cobra_priest'}

def cut(m):
    d = os.path.join(CAT, m['sprite']); A = json.load(open(os.path.join(d, m['id'] + '.atlas.json'))); S = A['scales']['2x']
    pages = [Image.open(os.path.join(d, p['file'])).convert('RGBA') for p in S['pages']]; px, py = S['pivot']
    rows = [(a, A['animations'][a]['w' if 'w' in A['animations'][a] else list(A['animations'][a])[0]]) for a in ('walk', 'attack') if a in A['animations']]
    fr = [[A['frames'][k]['2x'] for k in ks] for _, ks in rows]
    x0 = min(f['ox'] for r in fr for f in r); y0 = min(f['oy'] for r in fr for f in r); x1 = max(f['ox'] + f['w'] for r in fr for f in r); y1 = max(max(f['oy'] + f['h'] for r in fr for f in r), py)
    w, h, n = x1 - x0 + 2, y1 - y0 + 2, max(len(r) for r in fr); sheet = Image.new('RGBA', (w * n, h * len(fr)))
    for j, r in enumerate(fr):
        for i in range(n):
            f = r[i % len(r)]; sheet.paste(pages[f['p']].crop((f['x'], f['y'], f['x'] + f['w'], f['y'] + f['h'])), (i * w + f['ox'] - x0 + 1, j * h + f['oy'] - y0 + 1))
    if A.get('drawnSide') == 'right':   # everything in the index faces LEFT
        out = Image.new('RGBA', sheet.size)
        for j in range(len(fr)):
            for i in range(n): out.paste(sheet.crop((i * w, j * h, i * w + w, j * h + h)).transpose(Image.FLIP_LEFT_RIGHT), (i * w, j * h))
        sheet = out; fx = w - (px - x0 + 1)
    else: fx = px - x0 + 1
    # small files: hard alpha (the card shader cuts at 45% anyway) + a 255-colour palette; transparent = BLACK so the shader can divide the
    # filtered colour by the filtered alpha (no dark fringe when the card is drawn small)
    al = sheet.getchannel('A').point(lambda v: 255 if v >= 115 else 0); q = sheet.convert('RGB').quantize(255, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    q.paste(255, mask=al.point(lambda v: 255 - v)); pal = q.getpalette()[:765] + [0, 0, 0]; q.putpalette(pal); q.save(os.path.join(OUT, m['id'] + '.png'), optimize=True, transparency=255)
    return {'f': 'art/horde/mobs/' + m['id'] + '.png', 'w': w, 'h': h, 'fx': fx, 'fy': py - y0 + 1, 'n': n, 'rows': {a: j for j, (a, _) in enumerate(rows)}, 'px': 2, 'hw': m['heightWorld'], 'fly': m['motion'] == 'fly',
            'name': m['nameTH'], 'tier': m['tier'], 'boss': m['kind'] == 'boss', 'el': m['element'], 'role': m['role']}

def main():
    C = json.load(open(os.path.join(CAT, 'catalog.json'))); by = {m['id']: m for m in C['monsters']}; idx = {}; maps = {}
    for mp, ids in PICK.items():
        maps[mp] = []
        for s in ids:
            m = by.get('mob_' + s) or by.get('boss_' + s)
            if not m: print('MISSING', s); continue
            if 'walk' not in m['actions']: print('no walk', s); continue
            idx[m['id']] = cut(m); maps[mp].append(m['id'])
    for f in sorted(os.listdir(OLD)):
        if not f.endswith('.json') or f == 'index.json': continue
        k = f[:-5]; J = json.load(open(os.path.join(OLD, f)))
        idx[k] = {'f': 'art/action/mobs/' + k + '.png', 'w': J['w'], 'h': J['h'], 'fx': J['fx'], 'fy': J['fy'], 'n': J['n'], 'rows': J['rows'], 'px': 1, 'hw': J.get('size', J['h']), 'fly': k in OLDFLY, 'name': OLDNAME.get(k, k), 'boss': k.startswith('boss_'), 'role': 'ranged' if k in OLDSHOOT else 'melee'}
    json.dump({'mobs': idx, 'maps': maps}, open(os.path.join(OUT, 'index.json'), 'w'), ensure_ascii=False, separators=(',', ':'))
    tot = sum(os.path.getsize(os.path.join(OUT, f)) for f in os.listdir(OUT)); print(len(idx), 'monsters,', round(tot / 1e6, 1), 'MB in art/horde/mobs')
if __name__ == '__main__': main()
