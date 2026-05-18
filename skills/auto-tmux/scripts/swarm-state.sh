#!/usr/bin/env bash
# swarm-state: minimal state, task and lock manager for tmux AI swarm workflows.
set -euo pipefail

SWARM_DIR="${AUTO_TMUX_SWARM_DIR:-/tmp/ai_swarm}"
STATUS_LOG="$SWARM_DIR/status.log"
TASKS_TSV="$SWARM_DIR/tasks.tsv"
LOCKS_DIR="$SWARM_DIR/locks"
RESULTS_DIR="$SWARM_DIR/results"
STATE_LOCK_DIR="$SWARM_DIR/.state.lock.d"

usage() {
  cat <<'EOF'
swarm-state: tmux AI swarm state/task/lock helper

Usage:
  swarm-state.sh init [--dir DIR]
  swarm-state.sh log --target TARGET --status STATUS --message TEXT [--dir DIR]
  swarm-state.sh status [--dir DIR]
  swarm-state.sh task-add --text TEXT [--id ID] [--dir DIR]
  swarm-state.sh task-list [--dir DIR]
  swarm-state.sh task-next --owner TARGET [--dir DIR]
  swarm-state.sh task-claim --id ID --owner TARGET [--dir DIR]
  swarm-state.sh task-done --id ID --owner TARGET [--result TEXT] [--dir DIR]
  swarm-state.sh task-block --id ID --owner TARGET --reason TEXT [--dir DIR]
  swarm-state.sh task-fail --id ID --owner TARGET --reason TEXT [--dir DIR]
  swarm-state.sh lock-acquire --name NAME --owner TARGET [--dir DIR]
  swarm-state.sh lock-release --name NAME --owner TARGET [--dir DIR] [--force]
  swarm-state.sh lock-list [--dir DIR]
  swarm-state.sh lock-prune --older-than SEC [--dir DIR] [--dry-run]
  swarm-state.sh report [--dir DIR]

Environment:
  AUTO_TMUX_SWARM_DIR overrides the default /tmp/ai_swarm.
EOF
}

die() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

sanitize() {
  tr '\t\r\n' '   ' | sed -E 's/[[:space:]]+/ /g; s/^ //; s/ $//'
}

set_dir() {
  local dir="$1"
  SWARM_DIR="$dir"
  STATUS_LOG="$SWARM_DIR/status.log"
  TASKS_TSV="$SWARM_DIR/tasks.tsv"
  LOCKS_DIR="$SWARM_DIR/locks"
  RESULTS_DIR="$SWARM_DIR/results"
  STATE_LOCK_DIR="$SWARM_DIR/.state.lock.d"
}

ensure_init() {
  mkdir -p "$LOCKS_DIR" "$RESULTS_DIR"
  touch "$STATUS_LOG" "$TASKS_TSV"
  if [[ ! -s "$TASKS_TSV" ]]; then
    printf 'id\tstatus\towner\ttext\tresult\n' > "$TASKS_TSV"
  fi
}

acquire_state_lock() {
  local timeout="${1:-10}"
  local start now
  start="$(date +%s)"
  while ! mkdir "$STATE_LOCK_DIR" 2>/dev/null; do
    now="$(date +%s)"
    if (( now - start >= timeout )); then
      die "timeout waiting for swarm state lock: $STATE_LOCK_DIR"
    fi
    sleep 0.2
  done
  printf '%s\n' "$$" > "$STATE_LOCK_DIR/pid"
  printf '%s\n' "$(date -Is)" > "$STATE_LOCK_DIR/created_at"
}

release_state_lock() {
  rm -rf "$STATE_LOCK_DIR"
}

cmd_init() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --dir) set_dir "${2:-}"; shift 2 ;;
      *) die "unknown init option: $1" ;;
    esac
  done
  ensure_init
  printf 'swarm initialized: %s\n' "$SWARM_DIR"
}

cmd_log() {
  local target="" status="" message=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --dir) set_dir "${2:-}"; shift 2 ;;
      --target) target="${2:-}"; shift 2 ;;
      --status) status="${2:-}"; shift 2 ;;
      --message) message="${2:-}"; shift 2 ;;
      *) die "unknown log option: $1" ;;
    esac
  done
  [[ -n "$target" ]] || die "missing --target"
  [[ -n "$status" ]] || die "missing --status"
  [[ -n "$message" ]] || die "missing --message"
  ensure_init
  message="$(printf '%s' "$message" | sanitize)"
  printf '[%s] [%s] [%s] %s\n' "$(date +%H:%M:%S)" "$target" "$status" "$message" >> "$STATUS_LOG"
}

cmd_status() {
  local lines=30
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --dir) set_dir "${2:-}"; shift 2 ;;
      -n|--lines) lines="${2:-}"; shift 2 ;;
      *) die "unknown status option: $1" ;;
    esac
  done
  ensure_init
  tail -n "$lines" "$STATUS_LOG"
}

cmd_task_add() {
  local id="" text=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --dir) set_dir "${2:-}"; shift 2 ;;
      --id) id="${2:-}"; shift 2 ;;
      --text) text="${2:-}"; shift 2 ;;
      *) die "unknown task-add option: $1" ;;
    esac
  done
  [[ -n "$text" ]] || die "missing --text"
  ensure_init
  if [[ -z "$id" ]]; then
    id="task-$(date +%Y%m%d%H%M%S)-$$"
  fi
  text="$(printf '%s' "$text" | sanitize)"
  printf '%s\tTODO\t-\t%s\t-\n' "$id" "$text" >> "$TASKS_TSV"
  printf 'task added: %s\n' "$id"
}

cmd_task_list() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --dir) set_dir "${2:-}"; shift 2 ;;
      *) die "unknown task-list option: $1" ;;
    esac
  done
  ensure_init
  column -t -s $'\t' "$TASKS_TSV" 2>/dev/null || cat "$TASKS_TSV"
}

update_task() {
  local id="$1" status="$2" owner="$3" result="$4"
  local tmp
  tmp="$(mktemp)"
  awk -F '\t' -v OFS='\t' -v id="$id" -v status="$status" -v owner="$owner" -v result="$result" '
    NR == 1 {print; next}
    $1 == id {$2 = status; $3 = owner; if (result != "") $5 = result; found = 1}
    {print}
    END {if (!found) exit 42}
  ' "$TASKS_TSV" > "$tmp" || {
    local code=$?
    rm -f "$tmp"
    if [[ "$code" == "42" ]]; then
      die "task not found: $id"
    fi
    exit "$code"
  }
  mv "$tmp" "$TASKS_TSV"
}

cmd_task_claim() {
  local id="" owner=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --dir) set_dir "${2:-}"; shift 2 ;;
      --id) id="${2:-}"; shift 2 ;;
      --owner) owner="${2:-}"; shift 2 ;;
      *) die "unknown task-claim option: $1" ;;
    esac
  done
  [[ -n "$id" ]] || die "missing --id"
  [[ -n "$owner" ]] || die "missing --owner"
  ensure_init
  update_task "$id" "DOING" "$owner" ""
  cmd_log --target "$owner" --status "START" --message "claimed $id"
}

cmd_task_next() {
  local owner=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --dir) set_dir "${2:-}"; shift 2 ;;
      --owner) owner="${2:-}"; shift 2 ;;
      *) die "unknown task-next option: $1" ;;
    esac
  done
  [[ -n "$owner" ]] || die "missing --owner"
  ensure_init

  acquire_state_lock
  local id tmp
  id="$(awk -F '\t' 'NR > 1 && $2 == "TODO" {print $1; exit}' "$TASKS_TSV")"
  if [[ -z "$id" ]]; then
    release_state_lock
    printf 'no TODO task available\n'
    return 1
  fi

  tmp="$(mktemp)"
  awk -F '\t' -v OFS='\t' -v id="$id" -v owner="$owner" '
    NR == 1 {print; next}
    $1 == id {$2 = "DOING"; $3 = owner}
    {print}
  ' "$TASKS_TSV" > "$tmp"
  mv "$tmp" "$TASKS_TSV"
  release_state_lock

  cmd_log --target "$owner" --status "START" --message "claimed next $id"
  printf 'task claimed: %s\n' "$id"
}

cmd_task_done() {
  local id="" owner="" result="done"
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --dir) set_dir "${2:-}"; shift 2 ;;
      --id) id="${2:-}"; shift 2 ;;
      --owner) owner="${2:-}"; shift 2 ;;
      --result) result="${2:-}"; shift 2 ;;
      *) die "unknown task-done option: $1" ;;
    esac
  done
  [[ -n "$id" ]] || die "missing --id"
  [[ -n "$owner" ]] || die "missing --owner"
  ensure_init
  result="$(printf '%s' "$result" | sanitize)"
  update_task "$id" "DONE" "$owner" "$result"
  printf '%s\n' "$result" > "$RESULTS_DIR/$id.txt"
  cmd_log --target "$owner" --status "DONE" --message "$id $result"
}

cmd_task_terminal() {
  local status="$1"
  shift
  local id="" owner="" reason=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --dir) set_dir "${2:-}"; shift 2 ;;
      --id) id="${2:-}"; shift 2 ;;
      --owner) owner="${2:-}"; shift 2 ;;
      --reason) reason="${2:-}"; shift 2 ;;
      *) die "unknown task-$status option: $1" ;;
    esac
  done
  [[ -n "$id" ]] || die "missing --id"
  [[ -n "$owner" ]] || die "missing --owner"
  [[ -n "$reason" ]] || die "missing --reason"
  ensure_init
  reason="$(printf '%s' "$reason" | sanitize)"
  update_task "$id" "$status" "$owner" "$reason"
  printf '%s\n' "$reason" > "$RESULTS_DIR/$id.txt"
  cmd_log --target "$owner" --status "$status" --message "$id $reason"
}

lock_path() {
  local name="$1"
  name="$(printf '%s' "$name" | sed -E 's#[^A-Za-z0-9_.-]+#_#g')"
  printf '%s/%s.lock.d' "$LOCKS_DIR" "$name"
}

cmd_lock_acquire() {
  local name="" owner=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --dir) set_dir "${2:-}"; shift 2 ;;
      --name) name="${2:-}"; shift 2 ;;
      --owner) owner="${2:-}"; shift 2 ;;
      *) die "unknown lock-acquire option: $1" ;;
    esac
  done
  [[ -n "$name" ]] || die "missing --name"
  [[ -n "$owner" ]] || die "missing --owner"
  ensure_init
  local path
  path="$(lock_path "$name")"
  if mkdir "$path" 2>/dev/null; then
    printf '%s\n' "$owner" > "$path/owner"
    printf '%s\n' "$(date -Is)" > "$path/created_at"
    cmd_log --target "$owner" --status "LOCK" --message "acquired $name"
    printf 'lock acquired: %s\n' "$name"
  else
    printf 'lock busy: %s owner=' "$name" >&2
    cat "$path/owner" >&2 2>/dev/null || printf 'unknown\n' >&2
    exit 2
  fi
}

cmd_lock_release() {
  local name="" owner="" force="0"
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --dir) set_dir "${2:-}"; shift 2 ;;
      --name) name="${2:-}"; shift 2 ;;
      --owner) owner="${2:-}"; shift 2 ;;
      --force) force="1"; shift ;;
      *) die "unknown lock-release option: $1" ;;
    esac
  done
  [[ -n "$name" ]] || die "missing --name"
  [[ -n "$owner" ]] || die "missing --owner"
  ensure_init
  local path current_owner
  path="$(lock_path "$name")"
  [[ -d "$path" ]] || die "lock not found: $name"
  current_owner="$(cat "$path/owner" 2>/dev/null || true)"
  if [[ "$force" != "1" && "$current_owner" != "$owner" ]]; then
    die "lock owner mismatch: current=$current_owner requested=$owner"
  fi
  rm -rf "$path"
  cmd_log --target "$owner" --status "UNLOCK" --message "released $name"
  printf 'lock released: %s\n' "$name"
}

cmd_lock_list() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --dir) set_dir "${2:-}"; shift 2 ;;
      *) die "unknown lock-list option: $1" ;;
    esac
  done
  ensure_init
  find "$LOCKS_DIR" -mindepth 1 -maxdepth 1 -type d -name '*.lock.d' -print | sort | while read -r path; do
    printf '%s\towner=%s\tcreated_at=%s\n' \
      "$(basename "$path" .lock.d)" \
      "$(cat "$path/owner" 2>/dev/null || printf unknown)" \
      "$(cat "$path/created_at" 2>/dev/null || printf unknown)"
  done
}

cmd_lock_prune() {
  local older_than="" dry_run="0"
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --dir) set_dir "${2:-}"; shift 2 ;;
      --older-than) older_than="${2:-}"; shift 2 ;;
      --dry-run) dry_run="1"; shift ;;
      *) die "unknown lock-prune option: $1" ;;
    esac
  done
  [[ -n "$older_than" ]] || die "missing --older-than SEC"
  [[ "$older_than" =~ ^[0-9]+$ ]] || die "--older-than must be seconds"
  ensure_init

  local now path created_at created_epoch age name
  now="$(date +%s)"
  find "$LOCKS_DIR" -mindepth 1 -maxdepth 1 -type d -name '*.lock.d' -print | sort | while read -r path; do
    created_at="$(cat "$path/created_at" 2>/dev/null || true)"
    created_epoch="$(date -d "$created_at" +%s 2>/dev/null || printf '0')"
    [[ "$created_epoch" != "0" ]] || continue
    age=$((now - created_epoch))
    name="$(basename "$path" .lock.d)"
    if (( age >= older_than )); then
      if [[ "$dry_run" == "1" ]]; then
        printf '[dry-run] would prune lock: %s age=%ss\n' "$name" "$age"
      else
        rm -rf "$path"
        cmd_log --target "swarm-state" --status "UNLOCK" --message "pruned stale lock $name age=${age}s"
        printf 'lock pruned: %s age=%ss\n' "$name" "$age"
      fi
    fi
  done
}

cmd_report() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --dir) set_dir "${2:-}"; shift 2 ;;
      *) die "unknown report option: $1" ;;
    esac
  done
  ensure_init
  printf '# swarm report\n\n'
  printf 'dir: %s\n\n' "$SWARM_DIR"
  printf '## tasks\n\n'
  cmd_task_list
  printf '\n## locks\n\n'
  cmd_lock_list || true
  printf '\n## recent status\n\n'
  cmd_status -n 20
}

main() {
  local cmd="${1:-help}"
  shift || true
  case "$cmd" in
    help|-h|--help) usage ;;
    init) cmd_init "$@" ;;
    log) cmd_log "$@" ;;
    status) cmd_status "$@" ;;
    task-add) cmd_task_add "$@" ;;
    task-list) cmd_task_list "$@" ;;
    task-next) cmd_task_next "$@" ;;
    task-claim) cmd_task_claim "$@" ;;
    task-done) cmd_task_done "$@" ;;
    task-block) cmd_task_terminal "BLOCKED" "$@" ;;
    task-fail) cmd_task_terminal "FAIL" "$@" ;;
    lock-acquire) cmd_lock_acquire "$@" ;;
    lock-release) cmd_lock_release "$@" ;;
    lock-list) cmd_lock_list "$@" ;;
    lock-prune) cmd_lock_prune "$@" ;;
    report) cmd_report "$@" ;;
    *) die "unknown command: $cmd" ;;
  esac
}

main "$@"
