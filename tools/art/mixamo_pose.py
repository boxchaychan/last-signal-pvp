# Pose sheets from a 3D clip (owner 2026-11-13: "เราไปเอาท่าวิ่ง 3D จาก Mixamo มาเลยก็ได้ ... เลยให้ทำทูลขึ้นมา"): free, no jobs, no Blender.
# Reads a .glb with a Mixamo skeleton and named animations (ours: art/3d/storm_game.glb = idle, run, shoot, reload, throw, roll, hit,
# die, die2), plays a clip in code, and draws the skeleton as the colour-coded stick figure of pose_guide.py, 8 poses per sheet,
# from ANY camera direction (a 3D clip gives all 8 directions for free). Chibi look: a big head on the head joint.
#   python3 tools/art/mixamo_pose.py <file.glb> <clip> [--dir=east|south-east|south|...|north-east] [--tilt=0] [--out=dir]
#   -> <out>/<clip>_<dir>.png (1536x1024, 4x2 cells) + .json (2D joints per cell)
import json, math, os, struct, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
def opt(n, d):
    for a in sys.argv:
        if a.startswith('--' + n + '='): return a.split('=', 1)[1]
    return d
def load(path):
    b = open(path, 'rb').read(); l0 = struct.unpack('<I', b[12:16])[0]; J = json.loads(b[20:20 + l0]); bin_ = b[20 + l0 + 8:]
    def acc(i):
        a = J['accessors'][i]; v = J['bufferViews'][a['bufferView']]; n = {'SCALAR': 1, 'VEC3': 3, 'VEC4': 4, 'MAT4': 16}[a['type']]
        o = v.get('byteOffset', 0) + a.get('byteOffset', 0); return np.frombuffer(bin_, np.float32, a['count'] * n, o).reshape(a['count'], n)
    return J, acc
def quat_mat(q):
    x, y, z, w = q; return np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)], [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)], [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])
def sample(times, vals, t, rot):
    i = int(np.clip(np.searchsorted(times, t) - 1, 0, len(times) - 2)); u = float(np.clip((t - times[i]) / max(1e-9, times[i + 1] - times[i]), 0, 1)); a, b = vals[i], vals[i + 1]
    if not rot: return a + (b - a) * u
    if np.dot(a, b) < 0: b = -b
    q = a + (b - a) * u; return q / np.linalg.norm(q)
def poses(J, acc, clip, n=8):
    A = [a for a in J['animations'] if a['name'] == clip][0]; N = J['nodes']; parent = {c: i for i, nd in enumerate(N) for c in nd.get('children', [])}
    ch = {}; T = 0
    for c in A['channels']:
        s = A['samplers'][c['sampler']]; t = acc(s['input'])[:, 0]; ch[(c['target']['node'], c['target']['path'])] = (t, acc(s['output'])); T = max(T, float(t[-1]))
    out = []
    for f in range(n):
        tt = T * f / n; W = {}
        def world(i):
            if i in W: return W[i]
            nd = N[i]; tr = np.array(nd.get('translation', [0, 0, 0]), float); ro = np.array(nd.get('rotation', [0, 0, 0, 1]), float); sc = np.array(nd.get('scale', [1, 1, 1]), float)
            if (i, 'translation') in ch: tr = sample(*ch[(i, 'translation')], tt, 0)
            if (i, 'rotation') in ch: ro = sample(*ch[(i, 'rotation')], tt, 1)
            if (i, 'scale') in ch: sc = sample(*ch[(i, 'scale')], tt, 0)
            M = np.eye(4); M[:3, :3] = quat_mat(ro) * sc; M[:3, 3] = tr
            W[i] = (world(parent[i]) @ M) if i in parent else M; return W[i]
        out.append({nd['name'].split(':')[-1]: world(i)[:3, 3].copy() for i, nd in enumerate(N) if 'name' in nd and nd['name'].startswith('mixamorig')})
    return out, T
DIRS = {'east': 90, 'south-east': 45, 'south': 0, 'south-west': -45, 'west': -90, 'north-west': -135, 'north': 180, 'north-east': 135}   # yaw: the model faces +Z = toward the camera at 0
COL = dict(head=(250, 210, 60), torso=(60, 110, 230), aF1=(230, 50, 50), aF2=(250, 140, 40), aB1=(150, 70, 200), aB2=(240, 120, 200), lF1=(40, 170, 70), lF2=(150, 220, 60), lB1=(20, 140, 150), lB2=(90, 210, 230))
if __name__ == '__main__':
    path, clip = sys.argv[1], sys.argv[2]; dname = opt('dir', 'east'); tilt = math.radians(float(opt('tilt', 0))); O = opt('out', 'art/poses/mixamo/'); os.makedirs(O, exist_ok=True)
    J, acc = load(path); P, T = poses(J, acc, clip); yaw = math.radians(DIRS[dname]); CW, CH, GY = 384, 512, 452
    Ry = np.array([[math.cos(yaw), 0, math.sin(yaw)], [0, 1, 0], [-math.sin(yaw), 0, math.cos(yaw)]]); Rx = np.array([[1, 0, 0], [0, math.cos(tilt), -math.sin(tilt)], [0, math.sin(tilt), math.cos(tilt)]])
    V = [{k: Rx @ Ry @ v for k, v in p.items()} for p in P]
    hip0 = V[0]['Hips']; ymin = min(v[1] for p in V for v in p.values()); ymax = max(p['Head'][1] for p in V); S = 250 / (ymax - ymin)      # the body fills ~250 px; the head circle adds the chibi head
    xs = [p['Hips'][0] for p in V]; drift = max(xs) - min(xs)
    im = Image.new('RGB', (CW * 4, CH * 2), (255, 255, 255)); d = ImageDraw.Draw(im); F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 30); meta = []
    for i, p in enumerate(V):
        ox, oy = i % 4 * CW, i // 4 * CH; d.rectangle((ox, oy, ox + CW - 1, oy + CH - 1), outline=(190, 190, 190)); d.line((ox + 12, oy + GY + 2, ox + CW - 12, oy + GY + 2), fill=(150, 150, 150), width=3); d.text((ox + 12, oy + 8), str(i + 1), fill=(90, 90, 90), font=F)
        cx = p['Hips'][0] if drift < .6 * (ymax - ymin) or True else hip0[0]            # in place: the hips stay in the middle of the cell (a run clip that travels would walk out of it)
        def sc(k): v = p[k]; return (ox + CW / 2 + (v[0] - cx) * S, oy + GY - (v[1] - ymin) * S, v[2])
        Jn = {k: sc(k) for k in p}
        near = 'Left' if Jn['LeftUpLeg'][2] + Jn['LeftArm'][2] > Jn['RightUpLeg'][2] + Jn['RightArm'][2] else 'Right'; far = 'Right' if near == 'Left' else 'Left'
        def seg(a, b, c, w=16): d.line((*Jn[a][:2], *Jn[b][:2]), fill=(20, 20, 24), width=w + 6); d.line((*Jn[a][:2], *Jn[b][:2]), fill=COL[c], width=w)
        seg(far + 'Arm', far + 'ForeArm', 'aB1'); seg(far + 'ForeArm', far + 'Hand', 'aB2'); seg(far + 'UpLeg', far + 'Leg', 'lB1'); seg(far + 'Leg', far + 'Foot', 'lB2'); seg(far + 'Foot', far + 'ToeBase', 'lB2', 10)
        seg('Hips', 'Neck', 'torso', 40); seg(near + 'UpLeg', near + 'Leg', 'lF1'); seg(near + 'Leg', near + 'Foot', 'lF2'); seg(near + 'Foot', near + 'ToeBase', 'lF2', 10)
        hx, hy = (Jn['Head'][0] + Jn['HeadTop_End'][0]) / 2, (Jn['Head'][1] + Jn['HeadTop_End'][1]) / 2 - 22; fw = Rx @ Ry @ np.array([0, 0, 1.0])
        d.ellipse((hx - 69, hy - 69, hx + 69, hy + 69), fill=(20, 20, 24)); d.ellipse((hx - 64, hy - 64, hx + 64, hy + 64), fill=COL['head'])
        if abs(fw[0]) > .3: sgn = 1 if fw[0] > 0 else -1; d.polygon([(hx + sgn * 62, hy + 4), (hx + sgn * 92, hy + 16), (hx + sgn * 58, hy + 30)], fill=COL['head'], outline=(20, 20, 24))
        elif fw[2] > 0: d.ellipse((hx - 8, hy + 10, hx + 8, hy + 24), fill=(20, 20, 24))                    # facing the camera: a nose dot
        seg(near + 'Arm', near + 'ForeArm', 'aF1'); seg(near + 'ForeArm', near + 'Hand', 'aF2')
        meta.append({k: [round(v[0] - ox), round(v[1] - oy)] for k, v in Jn.items()})
    name = '%s_%s' % (clip, dname); im.save(O + name + '.png'); json.dump({'clip': clip, 'dir': dname, 'seconds': round(T, 3), 'cell': [CW, CH], 'ground': GY, 'poses': meta}, open(O + name + '.json', 'w')); print(name, 'clip %.2fs' % T, 'hip drift', round(float(drift), 2))
