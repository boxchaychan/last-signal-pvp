"""Game-size sprites for divine.html from the cut pictures (art/incoming/divine_game/cut, made by divine_cut.py). Free.
Stored at 2x the size they are drawn on the 585 x 1266 game canvas (sharp on phones). -> art/divine/<name>.png"""
import os
from PIL import Image
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'); CUT = os.path.join(R, 'art/incoming/divine_game/cut'); OUT = os.path.join(R, 'art/divine')
H = {'zeus_boy': ('hero_greek', 200), 'thor': ('hero_norse', 200), 'anubis': ('hero_egypt', 214), 'monkey': ('hero_asia', 200), 'soldier': ('soldier', 176),
     'zeus_spirit': ('spirit_greek', 300), 'robot_a': ('mob_robot_a', 150), 'robot_b': ('mob_robot_b', 156), 'robot_c': ('mob_robot_c', 118),
     'ghoul_a': ('mob_ghoul', 166), 'ghoul_b': ('boss_ghoul', 300)}
os.makedirs(OUT, exist_ok=True)
for src, (dst, h) in H.items():
    a = Image.open(os.path.join(CUT, src + '.png')).convert('RGBA'); w = round(a.width * h / a.height)
    a.resize((w, h), Image.LANCZOS).save(os.path.join(OUT, dst + '.png'), optimize=True); print(dst, w, h)
