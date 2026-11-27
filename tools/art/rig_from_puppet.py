"""art/divine/puppet.json (the 9-piece Zeus drawn as separate pieces by Codex, cut by tools/art/divine_puppet.py) -> a rig of the new tool,
art/rigs/zeus.json (rig.html?char=zeus, rig2d/bones.js). Free, nothing redrawn. A front-facing chibi like the heroes of the owner's recording.
  python3 tools/art/rig_from_puppet.py"""
import json, math, os
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'); P = json.load(open(os.path.join(R, 'art/divine/puppet.json')))['zeus']
by = {q['n']: q for q in P['parts']}; W, H, FX, FY = 250, 236, 125, 222   # the rig's own picture space: feet at (FX, FY)
def world(n):   # (x, y, angle) of the piece's turning point: parent . translate(lx, ly) . rotate(rot)
    q = by[n]; px, py, pa = world(q['p']) if q['p'] else (0.0, 0.0, 0.0); c, s = math.cos(pa), math.sin(pa)
    return px + c * q['lx'] - s * q['ly'], py + s * q['lx'] + c * q['ly'], pa + q['rot']
ROLE = dict(torso='body', head='head', armW='armF', handW='foreF', bolt='weapon', armF='armB', handF='foreB', legL='legB', legR='legF')
NAME = dict(torso='ลำตัว', head='หัว', armW='แขนถืออาวุธ', handW='มือถืออาวุธ', bolt='สายฟ้า', armF='แขนว่าง', handF='มือว่าง', legL='ขาซ้าย', legR='ขาขวา')
parts = {}
for q in P['parts']:
    x, y, a = world(q['n']); parts[q['n']] = dict(img=f"pup_zeus_{q['n']}.png", n=NAME[q['n']], role=ROLE[q['n']], pv=[round(-q['ox'], 1), round(-q['oy'], 1)], at=[round(FX + x, 1), round(FY + y, 1)], s=1, r=round(math.degrees(a), 1), p=q['p'] or '')
parts['handW']['g'] = parts['handF']['g'] = .15; parts['armW']['g'] = parts['armF']['g'] = .9   # his arms bend outward at the elbow: a full raise would put both fists before his face
parts['torso']['pv'][1] += 26; parts['torso']['at'][1] += 26   # the body turns at the HIP line (where the legs join), so a lean does not swing the skirt off the legs
rig = dict(v=2, name='zeus', title='ซุส (9 ชิ้น หันหน้าตรง)', dir='art/divine/', ref='../rigs/zeus_ref.png', size=[W, H], feet=[FX, FY], view='front', flip=True, parts=parts, order=[q['n'] for q in P['parts']])   # flip: his weapon arm is on the left of the picture
json.dump(rig, open(os.path.join(R, 'art/rigs/zeus.json'), 'w'), ensure_ascii=False, indent=1); print('art/rigs/zeus.json', len(parts), 'pieces')
