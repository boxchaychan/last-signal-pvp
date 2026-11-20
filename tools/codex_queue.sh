#!/usr/bin/env bash
# Run Codex picture jobs one after another on the owner's PC (owner 2026-11-20 "สั่งไปเรื่อยๆ codex").
#   bash tools/codex_queue.sh <log dir> "<phrase 1>" "<phrase 2>" ...
# Optional: WAIT_FOR=<file> waits until that file has a line starting with "exit" (the job already running) before starting.
# Each job runs in its own Codex worktree (--worktree, from the current main), so this folder's branch is never switched.
# Every phrase must be listed in AGENTS.md (it points Codex to the brief). Logs: <log dir>/job<N>.log, last message job<N>.last.txt.
set -u
LOGDIR="$1"; shift; mkdir -p "$LOGDIR"
if [ -n "${WAIT_FOR:-}" ]; then until grep -q '^exit' "$WAIT_FOR" 2>/dev/null; do sleep 30; done; fi
n=0
for phrase in "$@"; do
  n=$((n + 1)); echo "$(date +%H:%M) start job $n: $phrase"
  codex exec --worktree --approve-for-me -C "C:/last-signal-pvp" -o "$LOGDIR/job$n.last.txt" \
    "$phrase — follow the brief AGENTS.md points to for this phrase. Make the pictures with image generation, painted 2D, NOT pixel art. Commit after each picture on the brief's branch. Write REPORT_TH.txt at the end." \
    > "$LOGDIR/job$n.log" 2>&1
  echo "$(date +%H:%M) end job $n: exit $?"
done
echo "queue done"
