#!/usr/bin/env bash
# Build a read-only handoff brief for a tmux AI swarm session.
set -euo pipefail

usage() {
  cat <<'EOF'
swarm-brief: export tmux AI swarm topology, pane output and state report into one brief

Usage:
  swarm-brief.sh [--session NAME] [--swarm-dir DIR] [--out DIR] [-n LINES]

Examples:
  swarm-brief.sh --session ai-hub --swarm-dir /tmp/ai_swarm
  swarm-brief.sh --session ai-hub --out /tmp/auto-tmux-brief -n 80
EOF
}

die() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
auto_tmux="$script_dir/auto-tmux.sh"
swarm_state="$script_dir/swarm-state.sh"

session=""
swarm_dir="${AUTO_TMUX_SWARM_DIR:-/tmp/ai_swarm}"
out_dir="/tmp/auto-tmux-brief-$(date +%Y%m%d-%H%M%S)"
lines=80

while [[ $# -gt 0 ]]; do
  case "$1" in
    --session) session="${2:-}"; shift 2 ;;
    --swarm-dir) swarm_dir="${2:-}"; shift 2 ;;
    --out) out_dir="${2:-}"; shift 2 ;;
    -n|--lines) lines="${2:-}"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) die "unknown option: $1" ;;
  esac
done

mkdir -p "$out_dir"
brief="$out_dir/brief.md"

run_block() {
  local title="$1"
  shift
  {
    printf '## %s\n\n' "$title"
    printf '```text\n'
    "$@" 2>&1 || printf '[command failed: %s]\n' "$*"
    printf '```\n\n'
  } >> "$brief"
}

{
  printf '# auto-tmux Swarm Brief\n\n'
  printf '%s\n' "- created_at: \`$(date -Is)\`"
  printf '%s\n' "- session: \`${session:-<all>}\`"
  printf '%s\n' "- swarm_dir: \`$swarm_dir\`"
  printf '%s\n\n' "- lines_per_pane: \`$lines\`"
  printf '本报告是只读交接快照，用于让 commander、reviewer 或新会话快速恢复上下文。\n\n'
} > "$brief"

doctor_args=(doctor)
topology_args=(topology)
scan_args=(scan -n "$lines")
if [[ -n "$session" ]]; then
  doctor_args+=(--session "$session")
  topology_args+=(--session "$session")
  scan_args+=(--session "$session")
fi

run_block "Doctor" "$auto_tmux" "${doctor_args[@]}"
run_block "Topology" "$auto_tmux" "${topology_args[@]}"
run_block "Recent Pane Output" "$auto_tmux" "${scan_args[@]}"

if [[ -d "$swarm_dir" ]]; then
  run_block "Swarm State Report" "$swarm_state" report --dir "$swarm_dir"
else
  {
    printf '## Swarm State Report\n\n'
    printf '```text\n'
    printf 'swarm state dir not found: %s\n' "$swarm_dir"
    printf 'initialize with: %s init --dir %s\n' "$swarm_state" "$swarm_dir"
    printf '```\n\n'
  } >> "$brief"
fi

printf 'brief written: %s\n' "$brief"
