#!/bin/bash
# Build the Berserker (class 2 of the swordsman) for action.html from what we already have, no new PixelLab jobs
# (owner 2026-11-10 "เบอร์เซิร์กเกอร์ทำยัง"): base moves + chain throw from the paid download, the three south-east attacks
# from the trial download; every missing direction plays the south-east one, mirrored for the left.
#   bash tools/art/berserker_build.sh     -> art/action/n128/berserker.* (full size) + art/action/berserker.* (2/3, menu card)
set -e
B=art/incoming/action/berserker
T=$(mktemp -d)/Idle; mkdir -p $T/animations
cp -r $B/pl_dl_paid/Idle/rotations $T/
for a in idle run roll hurt death chain; do cp -r $B/pl_dl_paid/Idle/animations/$a $T/animations/; done
put() { local a=$1 d=$2; shift 2; mkdir -p $T/animations/$a/$d; local i=0
  for f in "$@"; do cp "$f" $(printf "$T/animations/$a/$d/frame_%03d.png" $i); i=$((i+1)); done; }
seqf() { ls $1 | sort | sed "s|^|$1/|"; }
P=$B/pl_dl/Idle/animations
put attack south-east $(seqf $P/bz_sweep/south-east) $(seqf $P/bz_slam/south-east)   # sweep, then the overhead slam
put leap south-east $(seqf $P/bz_slam/south-east)
put charge south-east $(seqf $P/bz_slam/south-east)
put spin south $(seqf $P/bz_spin/south-east)                                           # E: the swordsman's whirl plays the 360 spin
AL=""; for m in attack leap charge chain; do
  AL="$AL,$m/east:south-east,$m/south:south-east,$m/south-west:south-east~,$m/west:south-east~,$m/north-east:south-east,$m/north:south-east,$m/north-west:south-east~"; done
AL=${AL#,}; AL="${AL/attack\/south:south-east,/south:south-east,}"
H="south-east:2,13;leap/south-east:4;charge/south-east:4;spin/south:2,3"
ARGS=(attack=attack run=run idle=idle roll=roll hurt=hurt death=death leap=leap charge=charge spin=spin chain=chain "--alias=$AL" "--hits=$H" --arc=air)
mkdir -p art/action/n128
python3 tools/art/act_sheet.py $T art/action/n128/berserker "${ARGS[@]}"
python3 tools/art/act_sheet.py $T art/action/berserker "${ARGS[@]}" --scale=2/3
