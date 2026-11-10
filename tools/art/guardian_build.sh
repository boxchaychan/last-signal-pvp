#!/bin/bash
# Build the Guardian (shield knight, class 2 of the swordsman) for action.html from what we already have, no new
# PixelLab jobs (owner 2026-11-10 "ทำอัศวินโล่ให้เสร็จ ... แค่กลับด้าน"): base moves from the paid download, attacks
# from the trial download (south-east) and the knight-pose copies (east); every missing direction plays a drawn one,
# mirrored for the left side.
#   bash tools/art/guardian_build.sh            -> art/action/n128/guardian.* (full size) + art/action/guardian.* (2/3)
set -e
G=art/incoming/action/guardian
T=$(mktemp -d)/Idle; mkdir -p $T/animations
cp -r $G/pl_dl_paid/Idle/rotations $T/
for a in idle run roll hurt death; do cp -r $G/pl_dl_paid/Idle/animations/$a $T/animations/; done
put() {   # put <anim> <dir> <frame files...>: copies them in order as frame_NNN.png
  local a=$1 d=$2; shift 2; mkdir -p $T/animations/$a/$d; local i=0
  for f in "$@"; do cp "$f" $(printf "$T/animations/$a/$d/frame_%03d.png" $i); i=$((i+1)); done; }
seqf() { ls $1 | sort | sed "s|^|$1/|"; }
K=$G/pose_copy_knight; P=$G/pl_dl/Idle/animations
rs() { for i in $(seq 0 $(( $(ls $1/r*.png | wc -l) - 1 ))); do echo $1/r$i.png; done; }
# normal attack: two cuts (east = knight attack 1 + 2, south-east = PixelLab slash + shield bash)
put attack east $(rs $K/ATTACK_1) $(rs $K/ATTACK_2)
put attack south-east $(seqf $P/gd_slash/south-east) $(seqf $P/gd_bash/south-east)
# the leap slam / charged strike: knight attack 3 (east) and the overhead chop (south-east)
put leap east $(rs $K/ATTACK_3); put leap south-east $(seqf $P/gd_overhead/south-east)
put charge east $(rs $K/ATTACK_3); put charge south-east $(seqf $P/gd_overhead/south-east)
put guard east $(rs $K/BLOCK)
A="south:south-east,south-west:south-east~,west:east~,north-east:east,north:east,north-west:east~"
AL="$A"; for m in leap charge; do AL="$AL,$m/south:south-east,$m/south-west:south-east~,$m/west:east~,$m/north-east:east,$m/north:east,$m/north-west:east~"; done
AL="$AL,guard/south-east:east,guard/south:east,guard/south-west:east~,guard/west:east~,guard/north-east:east,guard/north:east,guard/north-west:east~"
H="east:3,12;south-east:4,13;leap/east:4;leap/south-east:4;charge/east:4;charge/south-east:4"
ARGS=(attack=attack run=run idle=idle roll=roll hurt=hurt death=death leap=leap charge=charge guard=guard "--alias=$AL" "--hits=$H" --arc=air)
mkdir -p art/action/n128
python3 tools/art/act_sheet.py $T art/action/n128/guardian "${ARGS[@]}"
python3 tools/art/act_sheet.py $T art/action/guardian "${ARGS[@]}" --scale=2/3
