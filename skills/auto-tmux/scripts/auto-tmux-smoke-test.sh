#!/usr/bin/env bash
# Smoke-test auto-tmux scripts without touching user tmux sessions.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AUTO_TMUX="$SCRIPT_DIR/auto-tmux.sh"
SWARM_STATE="$SCRIPT_DIR/swarm-state.sh"
SESSION="auto-tmux-smoke-$$"
SWARM_DIR="/tmp/auto-tmux-smoke-swarm-$$"
SNAPSHOT_DIR="/tmp/auto-tmux-smoke-snapshot-$$"
RECORD_DIR="/tmp/auto-tmux-smoke-record-$$"

cleanup() {
  tmux kill-session -t "$SESSION" 2>/dev/null || true
  rm -rf "$SWARM_DIR" "$SNAPSHOT_DIR" "$RECORD_DIR"
}
trap cleanup EXIT

command -v tmux >/dev/null 2>&1 || {
  echo "SKIP: tmux is not installed"
  exit 0
}

bash -n "$AUTO_TMUX"
bash -n "$SWARM_STATE"

"$AUTO_TMUX" hub --session "$SESSION" --workers 1 --cmd bash
"$AUTO_TMUX" topology --session "$SESSION" >/tmp/auto-tmux-smoke-topology.txt

commander_target="$(tmux list-panes -t "$SESSION:commander" -F '#S:#I.#P' | head -n 1)"
worker_target="$(tmux list-panes -t "$SESSION:worker1" -F '#S:#I.#P' | head -n 1)"

"$AUTO_TMUX" capture -t "$commander_target" -n 10 >/tmp/auto-tmux-smoke-capture.txt
"$AUTO_TMUX" send -t "$worker_target" --text "echo AUTO_TMUX_SMOKE_OK" --enter
"$AUTO_TMUX" wait -t "$worker_target" --pattern "AUTO_TMUX_SMOKE_OK" --timeout 10 >/tmp/auto-tmux-smoke-wait.txt
"$AUTO_TMUX" snapshot --session "$SESSION" --dir "$SNAPSHOT_DIR" -n 20 >/tmp/auto-tmux-smoke-snapshot.txt
test -s "$SNAPSHOT_DIR/topology.txt"

"$AUTO_TMUX" record start -t "$worker_target" --dir "$RECORD_DIR" >/tmp/auto-tmux-smoke-record-start.txt
"$AUTO_TMUX" record stop -t "$worker_target" >/tmp/auto-tmux-smoke-record-stop.txt

"$SWARM_STATE" init --dir "$SWARM_DIR" >/tmp/auto-tmux-smoke-swarm-init.txt
"$SWARM_STATE" task-add --dir "$SWARM_DIR" --id smoke-task --text "run smoke task" >/tmp/auto-tmux-smoke-task-add.txt
"$SWARM_STATE" task-claim --dir "$SWARM_DIR" --id smoke-task --owner "$worker_target"
"$SWARM_STATE" lock-acquire --dir "$SWARM_DIR" --name smoke-file --owner "$worker_target" >/tmp/auto-tmux-smoke-lock.txt
"$SWARM_STATE" lock-release --dir "$SWARM_DIR" --name smoke-file --owner "$worker_target" >/tmp/auto-tmux-smoke-unlock.txt
"$SWARM_STATE" task-done --dir "$SWARM_DIR" --id smoke-task --owner "$worker_target" --result "ok"
"$SWARM_STATE" report --dir "$SWARM_DIR" >/tmp/auto-tmux-smoke-report.txt
grep -q 'smoke-task' /tmp/auto-tmux-smoke-report.txt

printf 'auto-tmux smoke test ok: session=%s worker=%s\n' "$SESSION" "$worker_target"
