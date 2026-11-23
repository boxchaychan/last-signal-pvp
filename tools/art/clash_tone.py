#!/usr/bin/env python3
"""clash.html: give every unit of a tribe ONE colour tone (owner 2026-11-23 "ปรับสีโทนให้ไปทางเดียวกัน", picked A for the aliens).
Each pixel keeps its lightness; saturated pixels move to the tribe's MAIN hue, bright glows to its ACCENT hue, greys get a hint of
the main hue. The untoned picture is kept once as art/clash/orig/pretone_<anim|unit>_<key>.png and the tone is always made from it,
so running this again never tones twice. Run: python3 tools/art/clash_tone.py"""
import os, shutil
import numpy as np
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TONES = {'alien': (275, 105)}   # (main hue, accent hue) in degrees: A = dark purple + toxic green glow
TRIBE = {'alien': ['ax_tank', 'ax_hunter', 'ax_hound', 'ax_assassin', 'ax_eye', 'ax_priestess', 'ax_saucer', 'ax_tk']}
def hsv2rgb(h, s, v):
    i = np.floor(h * 6).astype(int) % 6; f = h * 6 - np.floor(h * 6); p = v * (1 - s); q = v * (1 - f * s); t = v * (1 - (1 - f) * s)
    return np.choose(i, [v, q, p, p, t, v]), np.choose(i, [t, v, v, q, p, p]), np.choose(i, [p, p, t, v, v, q])
def tone(path_in, path_out, main, accent):
    a = np.asarray(Image.open(path_in).convert('RGBA')).astype(float) / 255; rgb = a[..., :3]
    v = rgb.max(2); mn = rgb.min(2); s = np.where(v > 0, (v - mn) / np.maximum(v, 1e-6), 0)
    grey = s < .18; glow = (v > .72) & (s > .35) & ~grey
    h = np.where(glow, accent, main) / 360.0; s2 = np.where(grey, np.minimum(.35, s + .10 * (1 - v)), np.minimum(1, np.where(glow, s * 1.05, s)))
    r, g, b = hsv2rgb(h, s2, v); out = a.copy(); out[..., 0], out[..., 1], out[..., 2] = r, g, b
    Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8)).save(path_out)
for tribe, keys in TRIBE.items():
    main, acc = TONES[tribe]
    for k in keys:
        for kind, cur in (('anim', f'art/clash/anim/{k}.png'), ('unit', f'art/clash/units/{k}.png')):
            cur = os.path.join(ROOT, cur); keep = os.path.join(ROOT, f'art/clash/orig/pretone_{kind}_{k}.png')
            if not os.path.exists(cur): continue
            if not os.path.exists(keep): shutil.copy(cur, keep)
            tone(keep, cur, main, acc)
        print(tribe, k)
