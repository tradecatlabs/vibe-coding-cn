#!/usr/bin/env bash
# Run finite read-only watch cycles for a tmux AI swarm session.
set -euo pipefail

usage() {
  cat <<'EOF'
swarm-watch: collect repeated read-only scan/report snapshots for a tmux AI swarm

Usage:
  swarm-watch.sh [--session NAME] [--swarm-dir DIR] [--out DIR] [--interval SEC] [--iterations N] [-n LINES] [--pattern REGEX]

Examples:
  swarm-watch.sh --session ai-hub --swarm-dir /tmp/ai_swarm --iterations 3 --interval 10
  swarm-watch.sh --session ai-hub --pattern "ERROR|Traceback|failed" --iterations 1
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
out_dir="/tmp/auto-tmux-watch-$(date +%Y%m%d-%H%M%S)"
interval=10
iterations=3
lines=80
pattern=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --session) session="${2:-}"; shift 2 ;;
    --swarm-dir) swarm_dir="${2:-}"; shift 2 ;;
    --out) out_dir="${2:-}"; shift 2 ;;
    --interval) interval="${2:-}"; shift 2 ;;
    --iterations) iterations="${2:-}"; shift 2 ;;
    -n|--lines) lines="${2:-}"; shift 2 ;;
    --pattern) pattern="${2:-}"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) die "unknown option: $1" ;;
  esac
done

[[ "$iterations" =~ ^[0-9]+$ ]] || die "--iterations must be a positive integer"
[[ "$interval" =~ ^[0-9]+$ ]] || die "--interval must be a non-negative integer"
[[ "$lines" =~ ^[0-9]+$ ]] || die "--lines must be a positive integer"
(( iterations > 0 )) || die "--iterations must be > 0"

mkdir -p "$out_dir"
index="$out_dir/index.md"

{
  printf '# auto-tmux Swarm Watch\n\n'
  printf '%s\n' "- created_at: \`$(date -Is)\`"
  printf '%s\n' "- session: \`${session:-<all>}\`"
  printf '%s\n' "- swarm_dir: \`$swarm_dir\`"
  printf '%s\n' "- iterations: \`$iterations\`"
  printf '%s\n' "- interval: \`$interval\`"
  printf '%s\n' "- lines_per_pane: \`$lines\`"
  printf '%s\n\n' "- pattern: \`${pattern:-<none>}\`"
} > "$index"

scan_args=(scan -n "$lines")
if [[ -n "$session" ]]; then
  scan_args+=(--session "$session")
fi
if [[ -n "$pattern" ]]; then
  scan_args+=(--pattern "$pattern")
fi

for ((i = 1; i <= iterations; i++)); do
  stamp="$(date +%Y%m%d-%H%M%S)"
  scan_file="$out_dir/${i}-${stamp}-scan.log"
  report_file="$out_dir/${i}-${stamp}-report.md"

  printf 'watch iteration %s/%s\n' "$i" "$iterations"
  "$auto_tmux" "${scan_args[@]}" > "$scan_file" 2>&1 || true

  if [[ -d "$swarm_dir" ]]; then
    "$swarm_state" report --dir "$swarm_dir" > "$report_file" 2>&1 || true
  else
    printf 'swarm state dir not found: %s\n' "$swarm_dir" > "$report_file"
  fi

  {
    printf '## Iteration %s\n\n' "$i"
    printf '%s\n' "- scan: [$(basename "$scan_file")](./$(basename "$scan_file"))"
    printf '%s\n\n' "- report: [$(basename "$report_file")](./$(basename "$report_file"))"
  } >> "$index"

  if (( i < iterations )); then
    sleep "$interval"
  fi
done

printf 'watch written: %s\n' "$out_dir"
