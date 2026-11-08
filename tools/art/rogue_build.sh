#!/bin/bash
# Rebuild the dagger rogue's sheets for action.html from both PixelLab downloads (see docs/action-game.md).
# Attack = attack_2hit_b; the lower diagonals and west play the clean east clip (owner found them odd).
# Upper attacks: north = attack_back (sideways slashes, she never faces the camera); north-west = attack_ul from the
# second account (two wide sideways sweeps seen from behind, owner chose "B"); north-east = north-west mirrored.
# Blade arcs are repainted on one colour ramp in every direction (act_sheet.py smear()).
# The vertical back-view chops (attack_back_v, N + NW) are kept as "chop" for a skill later.
R=art/incoming/action/rogue
python tools/art/act_sheet.py $R/pl2_dl/Idle art/action/rogue \
  "attack=@$R/pl_dl/Idle::attack_2hit_b,attack_back|@$R/pl2_dl/Idle::attack_ul" chop=@$R/pl_dl/Idle::attack_back_v \
  run=run idle=idle roll=roll hurt=hurt death=death \
  --skip=north-east "--alias=south-east:east,south-west:east~,west:east~" \
  "--hits=chop/north-west:6,9;chop/north:6,11" --arc=air --scale=4/5 "$@"
