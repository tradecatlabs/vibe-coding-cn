#!/usr/bin/env bash
# auto-tmux: safe tmux automation wrapper for Codex/AI operator workflows.
set -euo pipefail

PROG="${0##*/}"
DEFAULT_LINES=120
DEFAULT_RESCUE_PATTERN='(\(y/n\)|\[y/N\]|\[Y/n\]|continue\?|proceed\?|confirm|确认|是否继续)'
DANGEROUS_PATTERN='(^|[[:space:];|&])(rm[[:space:]]+-rf|mkfs|dd[[:space:]]+if=|shutdown|reboot|halt|poweroff|tmux[[:space:]]+kill-server|git[[:space:]]+reset[[:space:]]+--hard|git[[:space:]]+clean[[:space:]]+-fd|DROP[[:space:]]+(DATABASE|TABLE))'

usage() {
  cat <<'EOF'
auto-tmux: safe tmux automation wrapper

Usage:
  auto-tmux.sh help
  auto-tmux.sh doctor [--session NAME]
  auto-tmux.sh topology [--session NAME]
  auto-tmux.sh capture -t TARGET [-n LINES] [--save FILE] [--no-redact]
  auto-tmux.sh send -t TARGET (--text TEXT | --key KEY) [--enter] [--clear] [--force] [--dry-run]
  auto-tmux.sh broadcast --session NAME (--text TEXT | --key KEY) [--enter] [--clear] [--force] [--dry-run]
  auto-tmux.sh rescue -t TARGET [--pattern REGEX] [--reply TEXT] [-n LINES] [--force] [--dry-run]
  auto-tmux.sh scan [--session NAME] [-n LINES] [--pattern REGEX] [--rescue] [--reply TEXT] [--save-dir DIR]
  auto-tmux.sh record start -t TARGET [--dir DIR]
  auto-tmux.sh record stop -t TARGET
  auto-tmux.sh snapshot [--session NAME] [--dir DIR] [-n LINES]
  auto-tmux.sh hub [--session NAME] [--workers N] [--cmd CMD] [--commander-cmd CMD] [--attach]
  auto-tmux.sh wait -t TARGET --pattern REGEX [--timeout SEC] [--interval SEC] [-n LINES]

Target format:
  <session>:<window>.<pane>

Examples:
  auto-tmux.sh doctor --session ai-hub
  auto-tmux.sh topology
  auto-tmux.sh capture -t <target-from-topology> -n 80
  auto-tmux.sh send -t <target-from-topology> --text "make test" --enter
  auto-tmux.sh broadcast --session ai-hub --text "pwd" --enter --dry-run
  auto-tmux.sh rescue -t <target-from-topology> --pattern "(y/n)" --reply y
  auto-tmux.sh scan --session ai-hub --pattern "ERROR|Traceback"
  auto-tmux.sh snapshot --session ai-hub --dir /tmp/auto-tmux-snapshot
  auto-tmux.sh hub --session ai-hub --workers 3 --cmd "codex"
EOF
}

die() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

warn() {
  printf 'warn: %s\n' "$*" >&2
}

status_line() {
  local status="$1"
  local message="$2"
  printf '[%s] %s\n' "$status" "$message"
}

require_tmux() {
  command -v tmux >/dev/null 2>&1 || die "tmux is not installed or not in PATH"
  tmux list-sessions >/dev/null 2>&1 || die "no tmux server/session found"
}

target_exists() {
  local target="$1"
  tmux display-message -pt "$target" '#{pane_id}' >/dev/null 2>&1
}

require_target() {
  local target="$1"
  [[ -n "$target" ]] || die "missing -t TARGET"
  target_exists "$target" || die "tmux target not found: $target"
}

redact() {
  sed -E \
    -e 's/(OPENAI_API_KEY|ANTHROPIC_API_KEY|GITHUB_TOKEN|GH_TOKEN|API_KEY|TOKEN|PASSWORD|SECRET)=([^[:space:]]+)/\1=<redacted>/g' \
    -e 's/(Bearer[[:space:]]+)[A-Za-z0-9._~+\/=-]+/\1<redacted>/g' \
    -e 's/(sk-[A-Za-z0-9_-]{12,})/<redacted-openai-key>/g'
}

capture_raw() {
  local target="$1"
  local lines="$2"
  tmux capture-pane -t "$target" -p -S "-$lines"
}

capture_print() {
  local target="$1"
  local lines="$2"
  local no_redact="$3"
  if [[ "$no_redact" == "1" ]]; then
    capture_raw "$target" "$lines"
  else
    capture_raw "$target" "$lines" | redact
  fi
}

is_dangerous_text() {
  local text="$1"
  echo "$text" | grep -Eiq "$DANGEROUS_PATTERN"
}

cancel_copy_mode_if_needed() {
  local target="$1"
  local in_mode
  in_mode="$(tmux display-message -pt "$target" '#{pane_in_mode}' 2>/dev/null || echo 0)"
  if [[ "$in_mode" == "1" ]]; then
    tmux send-keys -t "$target" -X cancel
  fi
}

pane_list() {
  local session="$1"
  if [[ -n "$session" ]]; then
    tmux list-panes -a -F '#S:#I.#P' | awk -F: -v s="$session" '$1 == s {print}'
  else
    tmux list-panes -a -F '#S:#I.#P'
  fi
}

cmd_doctor() {
  local session=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --session) session="${2:-}"; shift 2 ;;
      -h|--help) usage; exit 0 ;;
      *) die "unknown doctor option: $1" ;;
    esac
  done

  local failures=0
  local script_dir
  script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

  if command -v tmux >/dev/null 2>&1; then
    status_line "OK" "tmux found: $(tmux -V)"
  else
    status_line "FAIL" "tmux not found in PATH"
    failures=$((failures + 1))
  fi

  if tmux list-sessions >/dev/null 2>&1; then
    status_line "OK" "tmux server is reachable"
  else
    status_line "WARN" "tmux server has no reachable session yet"
  fi

  for script in auto-tmux.sh swarm-state.sh swarm-brief.sh render-swarm-prompt.sh swarm-dispatch.sh auto-tmux-smoke-test.sh validate-auto-tmux.sh; do
    if [[ -x "$script_dir/$script" ]]; then
      status_line "OK" "script executable: $script"
    else
      status_line "FAIL" "script missing or not executable: $script"
      failures=$((failures + 1))
    fi
  done

  local root
  root="$(git -C "$script_dir" rev-parse --show-toplevel 2>/dev/null || true)"
  if [[ -n "$root" ]]; then
    for rel in skills/auto-tmux/assets/oh-my-tmux skills/auto-tmux/assets/tmux-src; do
      if [[ -e "$root/$rel" ]]; then
        status_line "OK" "asset exists: $rel"
      else
        status_line "WARN" "asset missing: $rel (run git submodule update --init --recursive)"
      fi
    done
  else
    status_line "WARN" "not inside a git worktree; skipped asset checks"
  fi

  if [[ -n "$session" ]]; then
    if tmux has-session -t "$session" 2>/dev/null; then
      status_line "OK" "session exists: $session"
      tmux list-panes -t "$session" -F '  pane #S:#{window_index}.#{pane_index} cmd=#{pane_current_command}'
    else
      status_line "FAIL" "session not found: $session"
      failures=$((failures + 1))
    fi
  fi

  if (( failures > 0 )); then
    return 1
  fi
}

cmd_topology() {
  local session=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --session) session="${2:-}"; shift 2 ;;
      -h|--help) usage; exit 0 ;;
      *) die "unknown topology option: $1" ;;
    esac
  done

  require_tmux
  if [[ -n "$session" ]]; then
    tmux has-session -t "$session" 2>/dev/null || die "session not found: $session"
    printf 'session: %s\n' "$session"
    tmux list-windows -t "$session" -F '  window #{window_index}: #{window_name} #{window_flags}'
    tmux list-panes -a -F '#S #S:#{window_index}.#{pane_index} #{pane_current_command} #{pane_current_path}' |
      awk -v s="$session" '$1 == s {print "  pane target=" $2 " cmd=" $3 " path=" $4}'
  else
    tmux list-sessions -F 'session: #{session_name} windows=#{session_windows} attached=#{session_attached}'
    tmux list-windows -a -F '  window #S:#{window_index}: #{window_name} #{window_flags}'
    tmux list-panes -a -F '    pane #S:#{window_index}.#{pane_index} cmd=#{pane_current_command} path=#{pane_current_path}'
  fi
}

cmd_broadcast() {
  local session=""
  local text=""
  local key=""
  local enter="0"
  local clear="0"
  local force="0"
  local dry_run="0"
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --session) session="${2:-}"; shift 2 ;;
      --text) text="${2:-}"; shift 2 ;;
      --key) key="${2:-}"; shift 2 ;;
      --enter) enter="1"; shift ;;
      --clear) clear="1"; shift ;;
      --force) force="1"; shift ;;
      --dry-run) dry_run="1"; shift ;;
      -h|--help) usage; exit 0 ;;
      *) die "unknown broadcast option: $1" ;;
    esac
  done

  require_tmux
  [[ -n "$session" ]] || die "broadcast requires --session NAME"
  tmux has-session -t "$session" 2>/dev/null || die "session not found: $session"
  [[ -n "$text" || -n "$key" ]] || die "broadcast requires --text TEXT or --key KEY"
  [[ -z "$text" || -z "$key" ]] || die "broadcast accepts only one of --text or --key"
  if [[ -n "$text" && "$force" != "1" ]] && is_dangerous_text "$text"; then
    die "refusing dangerous broadcast text without --force: $text"
  fi

  local panes=()
  mapfile -t panes < <(pane_list "$session")
  [[ "${#panes[@]}" -gt 0 ]] || die "no panes found in session: $session"
  printf 'broadcast targets (%s):\n' "${#panes[@]}"
  printf '  %s\n' "${panes[@]}"

  local pane
  for pane in "${panes[@]}"; do
    if [[ "$dry_run" == "1" ]]; then
      printf '[dry-run] would send to %s\n' "$pane"
      continue
    fi
    if [[ -n "$text" ]]; then
      local args=(-t "$pane" --text "$text")
      [[ "$enter" == "1" ]] && args+=(--enter)
      [[ "$clear" == "1" ]] && args+=(--clear)
      [[ "$force" == "1" ]] && args+=(--force)
      cmd_send "${args[@]}"
    else
      local args=(-t "$pane" --key "$key")
      [[ "$enter" == "1" ]] && args+=(--enter)
      [[ "$clear" == "1" ]] && args+=(--clear)
      [[ "$force" == "1" ]] && args+=(--force)
      cmd_send "${args[@]}"
    fi
  done
}

cmd_capture() {
  local target=""
  local lines="$DEFAULT_LINES"
  local save_file=""
  local no_redact="0"
  while [[ $# -gt 0 ]]; do
    case "$1" in
      -t|--target) target="${2:-}"; shift 2 ;;
      -n|--lines) lines="${2:-}"; shift 2 ;;
      --save) save_file="${2:-}"; shift 2 ;;
      --no-redact) no_redact="1"; shift ;;
      -h|--help) usage; exit 0 ;;
      *) die "unknown capture option: $1" ;;
    esac
  done

  require_tmux
  require_target "$target"
  if [[ -n "$save_file" ]]; then
    mkdir -p "$(dirname "$save_file")"
    capture_print "$target" "$lines" "$no_redact" | tee "$save_file"
  else
    capture_print "$target" "$lines" "$no_redact"
  fi
}

cmd_send() {
  local target=""
  local text=""
  local key=""
  local enter="0"
  local clear="0"
  local force="0"
  local dry_run="0"
  while [[ $# -gt 0 ]]; do
    case "$1" in
      -t|--target) target="${2:-}"; shift 2 ;;
      --text) text="${2:-}"; shift 2 ;;
      --key) key="${2:-}"; shift 2 ;;
      --enter) enter="1"; shift ;;
      --clear) clear="1"; shift ;;
      --force) force="1"; shift ;;
      --dry-run) dry_run="1"; shift ;;
      -h|--help) usage; exit 0 ;;
      *) die "unknown send option: $1" ;;
    esac
  done

  require_tmux
  require_target "$target"
  [[ -n "$text" || -n "$key" ]] || die "send requires --text TEXT or --key KEY"
  [[ -z "$text" || -z "$key" ]] || die "send accepts only one of --text or --key"

  printf -- '--- current context: %s ---\n' "$target" >&2
  capture_print "$target" 40 0 >&2 || true

  if [[ -n "$text" && "$force" != "1" ]] && is_dangerous_text "$text"; then
    die "refusing dangerous text without --force: $text"
  fi

  if [[ "$dry_run" == "1" ]]; then
    printf '[dry-run] target=%s clear=%s text=%q key=%q enter=%s\n' "$target" "$clear" "$text" "$key" "$enter"
    return 0
  fi

  cancel_copy_mode_if_needed "$target"
  if [[ "$clear" == "1" ]]; then
    tmux send-keys -t "$target" C-u
  fi
  if [[ -n "$text" ]]; then
    tmux send-keys -t "$target" -l "$text"
  else
    tmux send-keys -t "$target" "$key"
  fi
  if [[ "$enter" == "1" ]]; then
    tmux send-keys -t "$target" Enter
  fi
}

cmd_rescue() {
  local target=""
  local pattern="$DEFAULT_RESCUE_PATTERN"
  local reply="y"
  local lines=80
  local force="0"
  local dry_run="0"
  while [[ $# -gt 0 ]]; do
    case "$1" in
      -t|--target) target="${2:-}"; shift 2 ;;
      --pattern) pattern="${2:-}"; shift 2 ;;
      --reply) reply="${2:-}"; shift 2 ;;
      -n|--lines) lines="${2:-}"; shift 2 ;;
      --force) force="1"; shift ;;
      --dry-run) dry_run="1"; shift ;;
      -h|--help) usage; exit 0 ;;
      *) die "unknown rescue option: $1" ;;
    esac
  done

  require_tmux
  require_target "$target"
  local output
  output="$(capture_raw "$target" "$lines")"
  printf '%s\n' "$output" | redact
  if printf '%s\n' "$output" | grep -Eiq "$pattern"; then
    printf '[match] target=%s pattern=%s reply=%q\n' "$target" "$pattern" "$reply" >&2
    if [[ "$dry_run" == "1" ]]; then
      printf '[dry-run] would send reply to %s\n' "$target"
    else
      if [[ "$force" == "1" ]]; then
        cmd_send -t "$target" --text "$reply" --enter --force
      else
        cmd_send -t "$target" --text "$reply" --enter
      fi
    fi
  else
    printf '[skip] no rescue pattern matched for %s\n' "$target" >&2
  fi
}

cmd_scan() {
  local session=""
  local lines=80
  local pattern=""
  local rescue="0"
  local reply="y"
  local save_dir=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --session) session="${2:-}"; shift 2 ;;
      -n|--lines) lines="${2:-}"; shift 2 ;;
      --pattern) pattern="${2:-}"; shift 2 ;;
      --rescue) rescue="1"; shift ;;
      --reply) reply="${2:-}"; shift 2 ;;
      --save-dir) save_dir="${2:-}"; shift 2 ;;
      -h|--help) usage; exit 0 ;;
      *) die "unknown scan option: $1" ;;
    esac
  done

  require_tmux
  if [[ -n "$save_dir" ]]; then
    mkdir -p "$save_dir"
  fi

  local pane output safe_name
  while IFS= read -r pane; do
    [[ -n "$pane" ]] || continue
    printf '\n===== [%s] =====\n' "$pane"
    output="$(capture_raw "$pane" "$lines")"
    printf '%s\n' "$output" | redact
    if [[ -n "$save_dir" ]]; then
      safe_name="${pane//[:.]/-}.log"
      printf '%s\n' "$output" | redact > "$save_dir/$safe_name"
    fi
    if [[ -n "$pattern" ]] && printf '%s\n' "$output" | grep -Eiq "$pattern"; then
      printf '[match] %s matched %s\n' "$pane" "$pattern" >&2
      if [[ "$rescue" == "1" ]]; then
        cmd_send -t "$pane" --text "$reply" --enter
      fi
    fi
  done < <(pane_list "$session")
}

cmd_record() {
  local action="${1:-}"
  [[ -n "$action" ]] || die "record requires start or stop"
  shift || true

  local target=""
  local dir="/tmp/auto-tmux-records"
  while [[ $# -gt 0 ]]; do
    case "$1" in
      -t|--target) target="${2:-}"; shift 2 ;;
      --dir) dir="${2:-}"; shift 2 ;;
      -h|--help) usage; exit 0 ;;
      *) die "unknown record option: $1" ;;
    esac
  done

  require_tmux
  require_target "$target"
  case "$action" in
    start)
      mkdir -p "$dir"
      local safe_name="${target//[:.]/-}.log"
      local file="$dir/$safe_name"
      tmux pipe-pane -t "$target" -o "cat >> '$file'"
      printf 'recording %s -> %s\n' "$target" "$file"
      ;;
    stop)
      tmux pipe-pane -t "$target"
      printf 'recording stopped for %s\n' "$target"
      ;;
    *)
      die "record action must be start or stop"
      ;;
  esac
}

cmd_snapshot() {
  local session=""
  local dir="/tmp/auto-tmux-snapshot-$(date +%Y%m%d-%H%M%S)"
  local lines=120
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --session) session="${2:-}"; shift 2 ;;
      --dir) dir="${2:-}"; shift 2 ;;
      -n|--lines) lines="${2:-}"; shift 2 ;;
      -h|--help) usage; exit 0 ;;
      *) die "unknown snapshot option: $1" ;;
    esac
  done

  require_tmux
  mkdir -p "$dir/panes"
  {
    printf 'auto-tmux snapshot\n'
    printf 'created_at=%s\n' "$(date -Is)"
    printf 'session=%s\n\n' "${session:-<all>}"
    cmd_topology ${session:+--session "$session"}
  } > "$dir/topology.txt"

  local pane safe_name
  while IFS= read -r pane; do
    [[ -n "$pane" ]] || continue
    safe_name="${pane//[:.]/-}.log"
    capture_print "$pane" "$lines" 0 > "$dir/panes/$safe_name"
  done < <(pane_list "$session")

  printf 'snapshot written: %s\n' "$dir"
}

cmd_hub() {
  local session="ai-hub"
  local workers=3
  local worker_cmd="bash"
  local commander_cmd="bash"
  local attach="0"
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --session) session="${2:-}"; shift 2 ;;
      --workers) workers="${2:-}"; shift 2 ;;
      --cmd) worker_cmd="${2:-}"; shift 2 ;;
      --commander-cmd) commander_cmd="${2:-}"; shift 2 ;;
      --attach) attach="1"; shift ;;
      -h|--help) usage; exit 0 ;;
      *) die "unknown hub option: $1" ;;
    esac
  done

  command -v tmux >/dev/null 2>&1 || die "tmux is not installed or not in PATH"
  if tmux has-session -t "$session" 2>/dev/null; then
    warn "session already exists: $session"
    tmux list-windows -t "$session" -F '#S:#I #{window_name}'
  else
    tmux new-session -d -s "$session" -n commander "$commander_cmd"
    local i
    for i in $(seq 1 "$workers"); do
      tmux new-window -t "$session" -n "worker$i" "$worker_cmd"
    done
    tmux select-window -t "$session:commander"
    printf 'created tmux AI hub: %s workers=%s cmd=%q\n' "$session" "$workers" "$worker_cmd"
  fi
  if [[ "$attach" == "1" ]]; then
    tmux attach -t "$session"
  fi
}

cmd_wait() {
  local target=""
  local pattern=""
  local timeout=60
  local interval=2
  local lines=80
  while [[ $# -gt 0 ]]; do
    case "$1" in
      -t|--target) target="${2:-}"; shift 2 ;;
      --pattern) pattern="${2:-}"; shift 2 ;;
      --timeout) timeout="${2:-}"; shift 2 ;;
      --interval) interval="${2:-}"; shift 2 ;;
      -n|--lines) lines="${2:-}"; shift 2 ;;
      -h|--help) usage; exit 0 ;;
      *) die "unknown wait option: $1" ;;
    esac
  done

  require_tmux
  require_target "$target"
  [[ -n "$pattern" ]] || die "wait requires --pattern REGEX"

  local start now output
  start="$(date +%s)"
  while true; do
    output="$(capture_raw "$target" "$lines")"
    if printf '%s\n' "$output" | grep -Eiq "$pattern"; then
      printf '%s\n' "$output" | redact
      printf '[matched] target=%s pattern=%s\n' "$target" "$pattern" >&2
      return 0
    fi
    now="$(date +%s)"
    if (( now - start >= timeout )); then
      printf '%s\n' "$output" | redact
      die "timeout waiting for pattern: $pattern"
    fi
    sleep "$interval"
  done
}

main() {
  local cmd="${1:-help}"
  shift || true
  case "$cmd" in
    help|-h|--help) usage ;;
    doctor) cmd_doctor "$@" ;;
    topology) cmd_topology "$@" ;;
    capture) cmd_capture "$@" ;;
    send) cmd_send "$@" ;;
    broadcast) cmd_broadcast "$@" ;;
    rescue) cmd_rescue "$@" ;;
    scan) cmd_scan "$@" ;;
    record) cmd_record "$@" ;;
    snapshot) cmd_snapshot "$@" ;;
    hub) cmd_hub "$@" ;;
    wait) cmd_wait "$@" ;;
    *) die "unknown command: $cmd" ;;
  esac
}

main "$@"
