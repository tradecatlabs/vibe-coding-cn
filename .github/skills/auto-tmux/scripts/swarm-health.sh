#!/usr/bin/env bash
# swarm-health: build a read-only health report for an auto-tmux swarm.
set -euo pipefail

usage() {
  cat <<'EOF'
swarm-health: build an auto-tmux swarm health report

Usage:
  swarm-health.sh [--session NAME] [--swarm-dir DIR] [--out DIR] [-n LINES]

Defaults:
  --swarm-dir AUTO_TMUX_SWARM_DIR or /tmp/ai_swarm
  --out       /tmp/auto-tmux-health-YYYYmmdd-HHMMSS
  -n          80 pane output lines

This script is read-only. It does not send keys, claim tasks or mutate state.
EOF
}

die() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
auto_tmux="$script_dir/auto-tmux.sh"
swarm_state="$script_dir/swarm-state.sh"
swarm_board="$script_dir/swarm-board.sh"
swarm_assign="$script_dir/swarm-assign.sh"

session=""
swarm_dir="${AUTO_TMUX_SWARM_DIR:-/tmp/ai_swarm}"
out_dir="/tmp/auto-tmux-health-$(date +%Y%m%d-%H%M%S)"
lines=80

while [[ $# -gt 0 ]]; do
  case "$1" in
    --session)
      session="${2:-}"
      shift 2
      ;;
    --swarm-dir|--dir)
      swarm_dir="${2:-}"
      shift 2
      ;;
    --out)
      out_dir="${2:-}"
      shift 2
      ;;
    -n|--lines)
      lines="${2:-}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      die "unknown option: $1"
      ;;
  esac
done

[[ "$lines" =~ ^[0-9]+$ ]] || die "--lines must be a number"
mkdir -p "$out_dir"

run_optional() {
  local label="$1"
  local file="$2"
  shift 2
  if "$@" > "$out_dir/$file" 2>&1; then
    printf '[OK] %s\n' "$label"
  else
    printf '[WARN] %s failed; see %s\n' "$label" "$file"
  fi
}

{
  printf '# auto-tmux Swarm Health\n\n'
  printf -- '- created_at: `%s`\n' "$(date -Is)"
  printf -- '- session: `%s`\n' "${session:-<not provided>}"
  printf -- '- swarm_dir: `%s`\n' "$swarm_dir"
  printf -- '- output_dir: `%s`\n\n' "$out_dir"
  printf '## Files\n\n'
  printf -- '- `doctor.txt`\n'
  printf -- '- `topology.txt`\n'
  printf -- '- `scan.txt`\n'
  printf -- '- `state-validate.txt`\n'
  printf -- '- `metrics.md`\n'
  printf -- '- `board.md`\n'
  printf -- '- `assign.md`\n'
} > "$out_dir/index.md"

if [[ -n "$session" ]]; then
  run_optional "doctor" "doctor.txt" "$auto_tmux" doctor --session "$session"
  run_optional "topology" "topology.txt" "$auto_tmux" topology --session "$session"
  run_optional "scan" "scan.txt" "$auto_tmux" scan --session "$session" -n "$lines"
else
  printf 'session not provided; skipped tmux doctor/topology/scan\n' > "$out_dir/doctor.txt"
  : > "$out_dir/topology.txt"
  : > "$out_dir/scan.txt"
fi

if [[ -f "$swarm_dir/tasks.tsv" && -f "$swarm_dir/deps.tsv" ]]; then
  run_optional "state validate" "state-validate.txt" "$swarm_state" validate --dir "$swarm_dir"
  run_optional "metrics" "metrics.md" "$swarm_state" metrics --dir "$swarm_dir"
  run_optional "board" "board.md" "$swarm_board" --dir "$swarm_dir"
  if [[ -n "$session" ]]; then
    run_optional "assign" "assign.md" "$swarm_assign" --swarm-dir "$swarm_dir" --session "$session"
  else
    run_optional "assign" "assign.md" "$swarm_assign" --swarm-dir "$swarm_dir"
  fi
else
  printf 'swarm state files not found: %s\n' "$swarm_dir" > "$out_dir/state-validate.txt"
  printf '# swarm metrics\n\nstate files not found: `%s`\n' "$swarm_dir" > "$out_dir/metrics.md"
  printf '# auto-tmux Swarm Board\n\nstate files not found: `%s`\n' "$swarm_dir" > "$out_dir/board.md"
  printf '# auto-tmux Swarm Assignment Suggestions\n\nstate files not found: `%s`\n' "$swarm_dir" > "$out_dir/assign.md"
  printf '[WARN] swarm state files not found; skipped state checks\n'
fi

printf 'swarm health written: %s\n' "$out_dir"
