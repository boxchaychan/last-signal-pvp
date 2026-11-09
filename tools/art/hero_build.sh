#!/bin/bash
# Build an action-game hero's sheets (swordsman / mage, 2026-11-09) from its PixelLab download, like rogue_build.sh.
#   bash tools/art/hero_build.sh <swordsman|mage> [extra act_sheet options]
# Attack was made in E S N NE NW: the lower diagonals and west play east (mirrored where needed). Skill moves were made
# in E S N NW (spin only S): the same aliases, north-east mirrors north-west by itself in the game (animRow).
# Only the moves that are downloaded go in, so it can be rerun as the skill moves arrive.
K=$1; shift
D=art/incoming/action/$K/pl_dl/Idle
A=$D/animations
args=(attack=attack run=run idle=idle roll=roll hurt=hurt death=death)
# the archer: a crit shot row, and the hurt / death moves came in two groups (her queue was restarted)
[ "$K" = archer ] && args=(attack=attack crit=crit run=run idle=idle roll=roll hurt=hurt,hurt-ba62d0b0 death=death,death-e16f77cc)
# keep only the moves that have arrived (a hero whose queue is still running can be tried early)
keep=(); for x in "${args[@]}"; do f=${x#*=}; [ -d "$A/${f%%,*}" ] && keep+=("$x"); done
alias="south-east:east,south-west:east~,west:east~"
[ "$K" = archer ] && alias="$alias,crit/south-east:east,crit/south-west:east~,crit/west:east~"
args=(); for x in "${keep[@]}"; do args+=("$x"); done
for m in leap guard charge cast_up staff_slam pray bless; do
  [ -d $A/$m ] || continue
  args+=($m=$m); alias="$alias,$m/south-east:east,$m/south-west:east~,$m/west:east~"
done
[ -d $A/spin ] && args+=(spin=spin)
# hit frames read off the sheets by eye (the widest-frame guess picks the follow-through):
# swordsman = sideways sweep, then the overhead slam; mage = the two staff casts (a white orb at the crystal)
case $K in
  swordsman) hits="east:3,9;south:4,10;north-west:4,9;north:4,9;north-east:2,7;leap/east:7;leap/south:4;leap/north-west:7;leap/north:6";;
  mage) hits="east:4,12;south:5,7;north-west:4,12;north:5,10;north-east:4,11";;
  priest) hits="";;
  archer) hits="east:10;south:11;north-west:9;north:10;north-east:11;crit/east:10;crit/south:11;crit/north-west:12;crit/north:11;crit/north-east:10";;
esac
extra=(); [ "$K" = archer ] && extra=(--detach=attack,crit)   # her own arrow only (the drawn one flew off its own way)
python tools/art/act_sheet.py $D art/action/$K "${args[@]}" "--alias=$alias" "--hits=$hits" --arc=air --scale=2/3 "${extra[@]}" "$@"
