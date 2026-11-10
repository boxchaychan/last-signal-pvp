#!/bin/bash
# Guardian v2 (long sword, owner 2026-11-10 "ทำมาดิ"): the 3 long-sword moves (side view, 132 px PixMiniMax tests) as a
# 3-step combo attack / attack2 / attack3, every direction plays them (mirrored for the left); idle / run are the new
# character's 8 stills (no base moves made yet), drawn on the same 132 canvas and spot as the moves.
#   bash tools/art/guardian2_build.sh   -> art/action/n128/guardian.* + art/action/guardian.* (2/3, menu card)
set -e
G=art/incoming/action/guardian2
T=$(mktemp -d)/Idle; mkdir -p $T/rotations $T/animations
for d in east south-east south south-west west north-west north north-east; do
  python3 -c "
from PIL import Image
im=Image.open('$G/dl/Idle/rotations/$d.png').convert('RGBA'); c=Image.new('RGBA',(132,132)); c.paste(im,(2,4)); c.save('$T/rotations/$d.png')
import os
for a in ('idle','run'):
    os.makedirs('$T/animations/'+a+'/$d',exist_ok=True); c.save('$T/animations/'+a+'/$d/frame_000.png')"
done
i=0; for a in combo1 combo2 combo3; do n=attack; [ $a = combo2 ] && n=attack2; [ $a = combo3 ] && n=attack3
  mkdir -p $T/animations/$n/east; cp $G/test_$a/f*.png $T/animations/$n/east/; (cd $T/animations/$n/east && for f in f*.png; do mv $f frame_${f#f}; done); done
AL=""; for m in attack attack2 attack3; do AL="$AL,$m/south-east:east,$m/south:east,$m/south-west:east~,$m/west:east~,$m/north-east:east,$m/north:east,$m/north-west:east~"; done
python3 tools/art/act_sheet.py $T art/action/n128/guardian attack=attack attack2=attack2 attack3=attack3 idle=idle run=run "--alias=${AL#,}" "--hits=east:4,7;attack2/east:3,8;attack3/east:7"
python3 tools/art/act_sheet.py $T art/action/guardian attack=attack attack2=attack2 attack3=attack3 idle=idle run=run "--alias=${AL#,}" "--hits=east:4,7;attack2/east:3,8;attack3/east:7" --scale=2/3
