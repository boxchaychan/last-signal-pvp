"""Shorten the tail of the owner's Tripo tiger (free, no Blender: edits the GLB vertex buffer in place).

  python tools/art/tiger_tail_fix.py <raw.glb> <out.glb> cut  [keep] [cut]     take a piece out of the middle (owner "ตัดออกดิ ยาวไป")
  python tools/art/tiger_tail_fix.py <raw.glb> <out.glb> curl [k] [deg0] [deg1] shorten by k and bend it up (first try, not chosen)

The raw tail sticks straight out behind (0.55 long behind ROOT; the tiger is 0.81 tall). Every vertex behind z = ROOT is tail only (checked by
slices: fur / hood end before it). cut: the first `keep` (.04) stays, the next `cut` (.26) folds onto the ring at `keep` (zero-size faces, no hole), the rest
(the round curled tip, as Tripo made it) moves forward by `cut` and along the tail's slope, so the tail is 0.26 shorter with its own tip.
World = node rotation +90 deg about x: world (x, h, z) = local (x, -z, y); the tiger faces +z.
"""
import json, struct, sys
import numpy as np

src, dst, mode = sys.argv[1], sys.argv[2], sys.argv[3]
arg = [float(a) for a in sys.argv[4:]]
ROOT = -.245   # fur / hood reach back to z -.24; behind this only the tail (x +-.03, h .09-.26)

b = bytearray(open(src, 'rb').read())
jl = struct.unpack('<I', b[12:16])[0]
j = json.loads(b[20:20 + jl])
bin0 = 20 + jl + 8
prim = j['meshes'][0]['primitives'][0]


def view(acc_i):
    a = j['accessors'][acc_i]
    bv = j['bufferViews'][a['bufferView']]
    assert a['componentType'] == 5126 and not bv.get('byteStride')
    off = bin0 + bv.get('byteOffset', 0) + a.get('byteOffset', 0)
    return a, off, np.frombuffer(bytes(b[off:off + a['count'] * 12]), dtype='<f4').reshape(-1, 3).copy()


pa, poff, P = view(prim['attributes']['POSITION'])
na, noff, Nn = view(prim['attributes']['NORMAL'])
W = np.stack([P[:, 0], -P[:, 2], P[:, 1]], 1)            # x, h, z
Nw = np.stack([Nn[:, 0], -Nn[:, 2], Nn[:, 1]], 1)
tail = (W[:, 2] < ROOT) & (np.abs(W[:, 0]) < .06) & (W[:, 1] < .32)
assert (W[:, 2] < ROOT).sum() == tail.sum(), 'something besides the tail is behind ROOT'
t = ROOT - W[tail, 2]                                     # distance behind the root
L = t.max()
fit = t < .28                               # straight part: the centre height is a line
ca, cb = np.polyfit(t[fit], W[tail, 1][fit], 1)
oh = W[tail, 1] - (ca * t + cb)                           # offset across the tail (height); the x offset is x itself
W2, N2w = W.copy(), Nw.copy()

if mode == 'cut':
    A, CUT = (arg + [.04, .26][len(arg):])[:2]
    tt = np.where(t > A + CUT, t - CUT, np.minimum(t, A))
    W2[tail, 2] = ROOT - tt
    W2[tail, 1] = ca * tt + cb + oh
    newL = L - CUT
else:
    K, D0, D1 = (arg + [.6, 15, 95][len(arg):])[:3]
    S = np.linspace(0, K * L, 400)
    th = np.radians(D0 + (D1 - D0) * S / (K * L))
    ds = np.diff(S, prepend=0)
    ph, pz = cb + np.cumsum(np.sin(th) * ds), ROOT - np.cumsum(np.cos(th) * ds)
    s = K * t
    cth = np.interp(s, S, th)
    c, si = np.cos(cth), np.sin(cth)
    w = np.clip(t / .04, 0, 1)                            # the first few cm blend from the old place so the root does not kink
    W2[tail, 1] = W[tail, 1] * (1 - w) + (np.interp(s, S, ph) + oh * c) * w
    W2[tail, 2] = W[tail, 2] * (1 - w) + (np.interp(s, S, pz) + oh * si) * w
    n_h, n_z = Nw[tail, 1], Nw[tail, 2]                   # normals turn with it: back (0, -1) -> (sin, -cos)
    N2w[tail, 1], N2w[tail, 2] = c * n_h - si * n_z, si * n_h + c * n_z
    newL = K * L

P2 = np.stack([W2[:, 0], W2[:, 2], -W2[:, 1]], 1).astype('<f4')
N2 = np.stack([N2w[:, 0], N2w[:, 2], -N2w[:, 1]], 1).astype('<f4')
b[poff:poff + P2.nbytes] = P2.tobytes()
b[noff:noff + N2.nbytes] = N2.tobytes()
pa['min'], pa['max'] = P2.min(0).tolist(), P2.max(0).tolist()
js = json.dumps(j, separators=(',', ':')).encode()
js += b' ' * ((4 - len(js) % 4) % 4)
rest = bytes(b[20 + jl:])
open(dst, 'wb').write(struct.pack('<III', 0x46546C67, 2, 12 + 8 + len(js) + len(rest)) + struct.pack('<I', len(js)) + b'JSON' + js + rest)
print(f'{mode}: tail vertices {tail.sum()}, length {L:.3f} -> {newL:.3f}, tail end z {W2[tail, 2].min():.3f} -> {dst}')
