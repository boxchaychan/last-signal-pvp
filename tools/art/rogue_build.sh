#!/bin/bash
# Rebuild the dagger rogue's sheets for action.html from both PixelLab downloads (see docs/action-game.md).
# Attack = attack_2hit_b; the lower diagonals and west play the clean east clip (owner found them odd).
# Upper attacks (owner 2026-11-08 "ฟันบน ... อีกแบบ ไม่หันหน้ามา"): north = attack_back (sideways slashes, she never
# faces the camera), north-east = north-west mirrored (attack_2hit_b NW keeps her back to the camera).
# The vertical back-view chops (attack_back_v, N + NW) are kept as "chop" for a skill later.
R=art/incoming/action/rogue
python tools/art/act_sheet.py $R/pl2_dl/Idle art/action/rogue \
  attack=@$R/pl_dl/Idle::attack_2hit_b,attack_back chop=@$R/pl_dl/Idle::attack_back_v \
  run=run idle=idle roll=roll hurt=hurt death=death \
  --skip=north-east "--alias=south-east:east,south-west:east~,west:east~" \
  "--hits=north-west:3,5;chop/north-west:6,9;chop/north:6,11"
