#!/usr/bin/env bash
# Smoke-test auto-tmux scripts without touching user tmux sessions.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AUTO_TMUX="$SCRIPT_DIR/auto-tmux.sh"
SWARM_STATE="$SCRIPT_DIR/swarm-state.sh"
RENDER_PROMPT="$SCRIPT_DIR/render-swarm-prompt.sh"
SWARM_BRIEF="$SCRIPT_DIR/swarm-brief.sh"
SESSION="auto-tmux-smoke-$$"
SWARM_DIR="/tmp/auto-tmux-smoke-swarm-$$"
SNAPSHOT_DIR="/tmp/auto-tmux-smoke-snapshot-$$"
RECORD_DIR="/tmp/auto-tmux-smoke-record-$$"
BRIEF_DIR="/tmp/auto-tmux-smoke-brief-$$"

cleanup() {
  tmux kill-session -t "$SESSION" 2>/dev/null || true
  rm -rf "$SWARM_DIR" "$SNAPSHOT_DIR" "$RECORD_DIR" "$BRIEF_DIR"
}
trap cleanup EXIT

command -v tmux >/dev/null 2>&1 || {
  echo "SKIP: tmux is not installed"
  exit 0
}

bash -n "$AUTO_TMUX"
bash -n "$SWARM_STATE"
bash -n "$RENDER_PROMPT"
bash -n "$SWARM_BRIEF"

"$AUTO_TMUX" hub --session "$SESSION" --workers 1 --cmd bash
"$AUTO_TMUX" doctor --session "$SESSION" >/tmp/auto-tmux-smoke-doctor.txt
"$AUTO_TMUX" topology --session "$SESSION" >/tmp/auto-tmux-smoke-topology.txt

commander_target="$(tmux list-panes -t "$SESSION:commander" -F '#S:#I.#P' | head -n 1)"
worker_target="$(tmux list-panes -t "$SESSION:worker1" -F '#S:#I.#P' | head -n 1)"

"$AUTO_TMUX" capture -t "$commander_target" -n 10 >/tmp/auto-tmux-smoke-capture.txt
"$AUTO_TMUX" broadcast --session "$SESSION" --text "pwd" --enter --dry-run >/tmp/auto-tmux-smoke-broadcast.txt
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
"$SWARM_STATE" task-add --dir "$SWARM_DIR" --id smoke-next --text "claim next task" >/tmp/auto-tmux-smoke-task-next-add.txt
"$SWARM_STATE" task-next --dir "$SWARM_DIR" --owner "$worker_target" >/tmp/auto-tmux-smoke-task-next.txt
grep -q 'smoke-next' /tmp/auto-tmux-smoke-task-next.txt
"$SWARM_STATE" task-block --dir "$SWARM_DIR" --id smoke-next --owner "$worker_target" --reason "waiting for input"
"$SWARM_STATE" task-add --dir "$SWARM_DIR" --id smoke-fail --text "fail task" >/tmp/auto-tmux-smoke-task-fail-add.txt
"$SWARM_STATE" task-fail --dir "$SWARM_DIR" --id smoke-fail --owner "$worker_target" --reason "expected failure"
"$SWARM_STATE" report --dir "$SWARM_DIR" >/tmp/auto-tmux-smoke-report.txt
grep -q 'smoke-task' /tmp/auto-tmux-smoke-report.txt
grep -q 'BLOCKED' /tmp/auto-tmux-smoke-report.txt
grep -q 'FAIL' /tmp/auto-tmux-smoke-report.txt
"$SWARM_BRIEF" --session "$SESSION" --swarm-dir "$SWARM_DIR" --out "$BRIEF_DIR" -n 10 >/tmp/auto-tmux-smoke-brief.txt
grep -q 'auto-tmux Swarm Brief' "$BRIEF_DIR/brief.md"
"$RENDER_PROMPT" commander --session "$SESSION" --swarm-dir "$SWARM_DIR" --task "smoke" >/tmp/auto-tmux-smoke-commander-prompt.md
"$RENDER_PROMPT" worker --session "$SESSION" --target "$worker_target" --swarm-dir "$SWARM_DIR" --task "smoke" >/tmp/auto-tmux-smoke-worker-prompt.md
grep -q 'Commander Prompt' /tmp/auto-tmux-smoke-commander-prompt.md
grep -q 'Worker Prompt' /tmp/auto-tmux-smoke-worker-prompt.md

printf 'auto-tmux smoke test ok: session=%s worker=%s\n' "$SESSION" "$worker_target"
