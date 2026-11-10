#!/bin/bash
# Rebuild the dagger rogue's sheets for action.html from both PixelLab downloads (see docs/action-game.md).
# Attack = attack_2hit_b; the lower diagonals and west play the clean east clip (owner found them odd).
# Upper attacks: north = attack_back (sideways slashes, she never faces the camera); north-west = attack_ul from the
# second account (two wide sideways sweeps seen from behind, owner chose "B"); north-east = north-west mirrored.
# Blade arcs are repainted on one colour ramp in every direction (act_sheet.py smear()).
# The vertical back-view chops (attack_back_v, N + NW) are kept as "chop" for a skill later.
R=art/incoming/action/rogue
# N128=1: full PixelLab size into art/action/n128/ (see hero_build.sh)
OUT=art/action/rogue; SC=--scale=2/3; [ -n "$N128" ] && { mkdir -p art/action/n128; OUT=art/action/n128/rogue; SC=; }
python3 tools/art/act_sheet.py $R/pl2_dl/Idle $OUT \
  "attack=@$R/pl_dl/Idle::attack_2hit_b,attack_back|@$R/pl2_dl/Idle::attack_ul" chop=@$R/pl_dl/Idle::attack_back_v \
  run=run idle=idle roll=roll hurt=hurt death=death spin=spin bomb=bomb dash=dash \
  --skip=north-east "--alias=south-east:east,south-west:east~,west:east~,bomb/south-east:east,bomb/south-west:east~,bomb/west:east~,dash/south-east:east,dash/south-west:east~,dash/west:east~,dash/south:east,dash/north:east~,dash/north-west:east~,dash/north-east:east" \
  "--hits=chop/north-west:6,9;chop/north:6,11;spin/south:6,7,8;bomb/east:5;bomb/south:5;bomb/north:4;bomb/north-west:5;dash/east:5" --arc=air $SC "$@"
# skill moves (2026-11-08): spin = skill 2 (south only, used for every direction: a spin looks the same from anywhere),
# bomb = skill 3 throw (E S N NW drawn; the bomb in flight is cut by dedust, the game draws its own)
