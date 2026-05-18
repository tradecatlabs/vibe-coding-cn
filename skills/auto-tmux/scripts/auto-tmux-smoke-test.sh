#!/usr/bin/env bash
# Smoke-test auto-tmux scripts without touching user tmux sessions.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AUTO_TMUX="$SCRIPT_DIR/auto-tmux.sh"
SWARM_STATE="$SCRIPT_DIR/swarm-state.sh"
RENDER_PROMPT="$SCRIPT_DIR/render-swarm-prompt.sh"
SWARM_BRIEF="$SCRIPT_DIR/swarm-brief.sh"
SWARM_WATCH="$SCRIPT_DIR/swarm-watch.sh"
SWARM_ARCHIVE="$SCRIPT_DIR/swarm-archive.sh"
SWARM_BOARD="$SCRIPT_DIR/swarm-board.sh"
SWARM_ASSIGN="$SCRIPT_DIR/swarm-assign.sh"
SWARM_HEALTH="$SCRIPT_DIR/swarm-health.sh"
RECORD_SUMMARY="$SCRIPT_DIR/record-summary.sh"
COMPLETION="$SCRIPT_DIR/completion.bash"
SAFETY_CHECK="$SCRIPT_DIR/safety-check.sh"
SWARM_DISPATCH="$SCRIPT_DIR/swarm-dispatch.sh"
SESSION="auto-tmux-smoke-$$"
SWARM_DIR="/tmp/auto-tmux-smoke-swarm-$$"
DEP_SWARM_DIR="/tmp/auto-tmux-smoke-dep-swarm-$$"
SNAPSHOT_DIR="/tmp/auto-tmux-smoke-snapshot-$$"
RECORD_DIR="/tmp/auto-tmux-smoke-record-$$"
RECORD_SUMMARY_FILE="/tmp/auto-tmux-smoke-record-summary-$$.md"
BRIEF_DIR="/tmp/auto-tmux-smoke-brief-$$"
WATCH_DIR="/tmp/auto-tmux-smoke-watch-$$"
ARCHIVE_FILE="/tmp/auto-tmux-smoke-archive-$$.tar.gz"
BOARD_FILE="/tmp/auto-tmux-smoke-board-$$.md"
ASSIGN_FILE="/tmp/auto-tmux-smoke-assign-$$.md"
HEALTH_DIR="/tmp/auto-tmux-smoke-health-$$"
DISPATCH_PROMPT="/tmp/auto-tmux-smoke-dispatch-$$.md"
TASK_IMPORT_FILE="/tmp/auto-tmux-smoke-tasks-$$.txt"
PASTE_FILE="/tmp/auto-tmux-smoke-paste-$$.txt"

cleanup() {
  tmux kill-session -t "$SESSION" 2>/dev/null || true
  rm -rf "$SWARM_DIR" "$DEP_SWARM_DIR" "$SNAPSHOT_DIR" "$RECORD_DIR" "$RECORD_SUMMARY_FILE" "$BRIEF_DIR" "$WATCH_DIR" "$ARCHIVE_FILE" "$BOARD_FILE" "$ASSIGN_FILE" "$HEALTH_DIR" "$DISPATCH_PROMPT" "$TASK_IMPORT_FILE" "$PASTE_FILE"
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
bash -n "$SWARM_WATCH"
bash -n "$SWARM_ARCHIVE"
bash -n "$SWARM_BOARD"
bash -n "$SWARM_ASSIGN"
bash -n "$SWARM_HEALTH"
bash -n "$RECORD_SUMMARY"
bash -n "$COMPLETION"
bash -n "$SAFETY_CHECK"
bash -n "$SWARM_DISPATCH"

"$AUTO_TMUX" hub --session "$SESSION" --workers 1 --cmd bash
"$AUTO_TMUX" doctor --session "$SESSION" >/tmp/auto-tmux-smoke-doctor.txt
"$AUTO_TMUX" topology --session "$SESSION" >/tmp/auto-tmux-smoke-topology.txt
"$AUTO_TMUX" cleanup --session "$SESSION" --dry-run >/tmp/auto-tmux-smoke-cleanup-dry-run.txt

commander_target="$(tmux list-panes -t "$SESSION:commander" -F '#S:#I.#P' | head -n 1)"
worker_target="$(tmux list-panes -t "$SESSION:worker1" -F '#S:#I.#P' | head -n 1)"

"$AUTO_TMUX" capture -t "$commander_target" -n 10 >/tmp/auto-tmux-smoke-capture.txt
"$AUTO_TMUX" inspect -t "$commander_target" -n 10 >/tmp/auto-tmux-smoke-inspect.txt
grep -q 'pane inspect' /tmp/auto-tmux-smoke-inspect.txt
printf '%s\n' 'echo AUTO_TMUX_PASTE_OK' > "$PASTE_FILE"
"$SAFETY_CHECK" --text "make test" >/tmp/auto-tmux-smoke-safety-clean.txt
if "$SAFETY_CHECK" --text "rm -rf /tmp/example" >/tmp/auto-tmux-smoke-safety-danger.txt 2>&1; then
  echo "expected safety-check to reject dangerous text" >&2
  exit 1
fi
"$SAFETY_CHECK" --file "$PASTE_FILE" --strict >/tmp/auto-tmux-smoke-safety-file.txt
"$AUTO_TMUX" paste -t "$worker_target" --file "$PASTE_FILE" --enter --dry-run >/tmp/auto-tmux-smoke-paste-dry-run.txt
"$AUTO_TMUX" broadcast --session "$SESSION" --text "pwd" --enter --dry-run >/tmp/auto-tmux-smoke-broadcast.txt
"$AUTO_TMUX" send -t "$worker_target" --text "echo AUTO_TMUX_SMOKE_OK" --enter
"$AUTO_TMUX" wait -t "$worker_target" --pattern "AUTO_TMUX_SMOKE_OK" --timeout 10 >/tmp/auto-tmux-smoke-wait.txt
"$AUTO_TMUX" snapshot --session "$SESSION" --dir "$SNAPSHOT_DIR" -n 20 >/tmp/auto-tmux-smoke-snapshot.txt
test -s "$SNAPSHOT_DIR/topology.txt"

"$AUTO_TMUX" record start -t "$worker_target" --dir "$RECORD_DIR" >/tmp/auto-tmux-smoke-record-start.txt
"$AUTO_TMUX" send -t "$worker_target" --text "echo AUTO_TMUX_RECORD_OK" --enter
"$AUTO_TMUX" wait -t "$worker_target" --pattern "AUTO_TMUX_RECORD_OK" --timeout 10 >/tmp/auto-tmux-smoke-record-wait.txt
"$AUTO_TMUX" record stop -t "$worker_target" >/tmp/auto-tmux-smoke-record-stop.txt
"$RECORD_SUMMARY" --dir "$RECORD_DIR" --out "$RECORD_SUMMARY_FILE" -n 20 >/tmp/auto-tmux-smoke-record-summary.txt
grep -q 'auto-tmux Record Summary' "$RECORD_SUMMARY_FILE"
grep -q 'AUTO_TMUX_RECORD_OK' "$RECORD_SUMMARY_FILE"

"$SWARM_STATE" init --dir "$SWARM_DIR" >/tmp/auto-tmux-smoke-swarm-init.txt
"$SWARM_STATE" task-add --dir "$SWARM_DIR" --id smoke-task --text "run smoke task" >/tmp/auto-tmux-smoke-task-add.txt
printf '%s\n' "- import task one" "- import task two" > "$TASK_IMPORT_FILE"
"$SWARM_STATE" task-import --dir "$SWARM_DIR" --file "$TASK_IMPORT_FILE" --prefix imported >/tmp/auto-tmux-smoke-task-import.txt
"$SWARM_STATE" task-add --dir "$SWARM_DIR" --id dep-a --text "dependency root" >/tmp/auto-tmux-smoke-dep-a.txt
"$SWARM_STATE" task-add --dir "$SWARM_DIR" --id dep-b --text "dependency child" >/tmp/auto-tmux-smoke-dep-b.txt
"$SWARM_STATE" task-depend --dir "$SWARM_DIR" --id dep-b --blocked-by dep-a >/tmp/auto-tmux-smoke-depend.txt
"$SWARM_STATE" task-ready --dir "$SWARM_DIR" >/tmp/auto-tmux-smoke-ready-before.txt
! grep -q 'dep-b' /tmp/auto-tmux-smoke-ready-before.txt
"$SWARM_STATE" init --dir "$DEP_SWARM_DIR" >/tmp/auto-tmux-smoke-dep-only-init.txt
"$SWARM_STATE" task-add --dir "$DEP_SWARM_DIR" --id dep-only-a --text "dependency root" >/tmp/auto-tmux-smoke-dep-only-a.txt
"$SWARM_STATE" task-add --dir "$DEP_SWARM_DIR" --id dep-only-b --text "dependency child" >/tmp/auto-tmux-smoke-dep-only-b.txt
"$SWARM_STATE" task-depend --dir "$DEP_SWARM_DIR" --id dep-only-b --blocked-by dep-only-a >/tmp/auto-tmux-smoke-dep-only-link.txt
"$SWARM_STATE" task-next --dir "$DEP_SWARM_DIR" --owner "$worker_target" >/tmp/auto-tmux-smoke-dep-only-next-a.txt
grep -q 'dep-only-a' /tmp/auto-tmux-smoke-dep-only-next-a.txt
! grep -q 'dep-only-b' /tmp/auto-tmux-smoke-dep-only-next-a.txt
"$SWARM_STATE" task-done --dir "$DEP_SWARM_DIR" --id dep-only-a --owner "$worker_target" --result "dep root done"
"$SWARM_STATE" task-next --dir "$DEP_SWARM_DIR" --owner "$worker_target" >/tmp/auto-tmux-smoke-dep-only-next-b.txt
grep -q 'dep-only-b' /tmp/auto-tmux-smoke-dep-only-next-b.txt
"$SWARM_STATE" task-done --dir "$SWARM_DIR" --id dep-a --owner "$worker_target" --result "dep ok"
"$SWARM_STATE" task-ready --dir "$SWARM_DIR" >/tmp/auto-tmux-smoke-ready-after.txt
grep -q 'dep-b' /tmp/auto-tmux-smoke-ready-after.txt
"$SWARM_STATE" task-claim --dir "$SWARM_DIR" --id smoke-task --owner "$worker_target"
"$SWARM_STATE" lock-acquire --dir "$SWARM_DIR" --name smoke-file --owner "$worker_target" >/tmp/auto-tmux-smoke-lock.txt
"$SWARM_STATE" lock-release --dir "$SWARM_DIR" --name smoke-file --owner "$worker_target" >/tmp/auto-tmux-smoke-unlock.txt
"$SWARM_STATE" lock-acquire --dir "$SWARM_DIR" --name stale-file --owner "$worker_target" >/tmp/auto-tmux-smoke-stale-lock.txt
"$SWARM_STATE" lock-prune --dir "$SWARM_DIR" --older-than 0 --dry-run >/tmp/auto-tmux-smoke-lock-prune-dry-run.txt
"$SWARM_STATE" lock-prune --dir "$SWARM_DIR" --older-than 0 >/tmp/auto-tmux-smoke-lock-prune.txt
grep -q 'stale-file' /tmp/auto-tmux-smoke-lock-prune.txt
"$SWARM_STATE" task-done --dir "$SWARM_DIR" --id smoke-task --owner "$worker_target" --result "ok"
"$SWARM_STATE" task-next --dir "$SWARM_DIR" --owner "$worker_target" >/tmp/auto-tmux-smoke-task-next.txt
grep -q 'imported-001' /tmp/auto-tmux-smoke-task-next.txt
"$SWARM_STATE" task-block --dir "$SWARM_DIR" --id imported-001 --owner "$worker_target" --reason "waiting for input"
"$SWARM_STATE" task-add --dir "$SWARM_DIR" --id smoke-fail --text "fail task" >/tmp/auto-tmux-smoke-task-fail-add.txt
"$SWARM_STATE" task-fail --dir "$SWARM_DIR" --id smoke-fail --owner "$worker_target" --reason "expected failure"
"$SWARM_STATE" task-list --dir "$SWARM_DIR" --status FAIL >/tmp/auto-tmux-smoke-task-list-fail.txt
grep -q 'smoke-fail' /tmp/auto-tmux-smoke-task-list-fail.txt
"$SWARM_STATE" metrics --dir "$SWARM_DIR" >/tmp/auto-tmux-smoke-metrics.txt
grep -q 'FAIL' /tmp/auto-tmux-smoke-metrics.txt
"$SWARM_STATE" report --dir "$SWARM_DIR" >/tmp/auto-tmux-smoke-report.txt
"$SWARM_STATE" validate --dir "$SWARM_DIR" >/tmp/auto-tmux-smoke-state-validate.txt
grep -q 'smoke-task' /tmp/auto-tmux-smoke-report.txt
grep -q 'imported-001' /tmp/auto-tmux-smoke-report.txt
grep -q 'BLOCKED' /tmp/auto-tmux-smoke-report.txt
grep -q 'FAIL' /tmp/auto-tmux-smoke-report.txt
"$SWARM_STATE" task-reopen --dir "$SWARM_DIR" --id smoke-fail --owner "$worker_target" --reason "retry after failure"
"$SWARM_STATE" task-list --dir "$SWARM_DIR" --status TODO >/tmp/auto-tmux-smoke-task-list-todo.txt
grep -q 'smoke-fail' /tmp/auto-tmux-smoke-task-list-todo.txt
"$SWARM_BRIEF" --session "$SESSION" --swarm-dir "$SWARM_DIR" --out "$BRIEF_DIR" -n 10 >/tmp/auto-tmux-smoke-brief.txt
grep -q 'auto-tmux Swarm Brief' "$BRIEF_DIR/brief.md"
"$SWARM_WATCH" --session "$SESSION" --swarm-dir "$SWARM_DIR" --out "$WATCH_DIR" --iterations 1 --interval 0 -n 10 >/tmp/auto-tmux-smoke-watch.txt
grep -q 'auto-tmux Swarm Watch' "$WATCH_DIR/index.md"
"$SWARM_ARCHIVE" --session "$SESSION" --swarm-dir "$SWARM_DIR" --out "$ARCHIVE_FILE" -n 10 >/tmp/auto-tmux-smoke-archive.txt
test -s "$ARCHIVE_FILE"
"$SWARM_BOARD" --dir "$SWARM_DIR" --out "$BOARD_FILE" --limit 20 >/tmp/auto-tmux-smoke-board.txt
grep -q 'auto-tmux Swarm Board' "$BOARD_FILE"
grep -q '## Ready TODO' "$BOARD_FILE"
grep -q 'smoke-fail' "$BOARD_FILE"
"$SWARM_ASSIGN" --swarm-dir "$SWARM_DIR" --session "$SESSION" --out "$ASSIGN_FILE" --limit 20 >/tmp/auto-tmux-smoke-assign.txt
grep -q 'auto-tmux Swarm Assignment Suggestions' "$ASSIGN_FILE"
grep -q 'swarm-dispatch.sh' "$ASSIGN_FILE"
"$SWARM_HEALTH" --session "$SESSION" --swarm-dir "$SWARM_DIR" --out "$HEALTH_DIR" -n 10 >/tmp/auto-tmux-smoke-health.txt
grep -q 'auto-tmux Swarm Health' "$HEALTH_DIR/index.md"
test -s "$HEALTH_DIR/state-validate.txt"
test -s "$HEALTH_DIR/board.md"
"$RENDER_PROMPT" commander --session "$SESSION" --swarm-dir "$SWARM_DIR" --task "smoke" >/tmp/auto-tmux-smoke-commander-prompt.md
"$RENDER_PROMPT" worker --session "$SESSION" --target "$worker_target" --swarm-dir "$SWARM_DIR" --task "smoke" >/tmp/auto-tmux-smoke-worker-prompt.md
"$SWARM_DISPATCH" --role worker --target "$worker_target" --session "$SESSION" --swarm-dir "$SWARM_DIR" --task "smoke" --out "$DISPATCH_PROMPT" >/tmp/auto-tmux-smoke-dispatch-render.txt
"$SWARM_DISPATCH" --role worker --target "$worker_target" --session "$SESSION" --swarm-dir "$SWARM_DIR" --task "smoke" --send --dry-run >/tmp/auto-tmux-smoke-dispatch-dry-run.txt
grep -q 'Commander Prompt' /tmp/auto-tmux-smoke-commander-prompt.md
grep -q 'Worker Prompt' /tmp/auto-tmux-smoke-worker-prompt.md
grep -q 'Worker Prompt' "$DISPATCH_PROMPT"

printf 'auto-tmux smoke test ok: session=%s worker=%s\n' "$SESSION" "$worker_target"
