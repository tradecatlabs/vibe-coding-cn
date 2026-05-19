#!/usr/bin/env bash
# swarm-report-pack: build a portable read-only report pack for swarm state.
set -euo pipefail

usage() {
  cat <<'EOF'
swarm-report-pack: build an auto-tmux swarm report pack

Usage:
  swarm-report-pack.sh [--dir DIR] [--session NAME] [--out DIR]

Defaults:
  --dir AUTO_TMUX_SWARM_DIR or /tmp/ai_swarm
  --out /tmp/auto-tmux-report-pack-YYYYmmdd-HHMMSS

This script is read-only for tmux and swarm state. It writes only to --out.
EOF
}

die() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
swarm_dir="${AUTO_TMUX_SWARM_DIR:-/tmp/ai_swarm}"
session=""
out_dir="/tmp/auto-tmux-report-pack-$(date +%Y%m%d-%H%M%S)"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dir|--swarm-dir)
      swarm_dir="${2:-}"
      shift 2
      ;;
    --session)
      session="${2:-}"
      shift 2
      ;;
    --out)
      out_dir="${2:-}"
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

mkdir -p "$out_dir/export"

run_report() {
  local label="$1"
  shift
  if "$@" >/tmp/auto-tmux-report-pack.log 2>&1; then
    printf '[OK] %s\n' "$label"
  else
    printf '[WARN] %s failed\n' "$label" >&2
    sed -n '1,80p' /tmp/auto-tmux-report-pack.log >&2
  fi
}

run_report "board" "$script_dir/swarm-board.sh" --dir "$swarm_dir" --out "$out_dir/board.md"
run_report "dependency graph" "$script_dir/swarm-deps-graph.sh" --dir "$swarm_dir" --out "$out_dir/deps.md"
run_report "timeline" "$script_dir/swarm-timeline.sh" --dir "$swarm_dir" --out "$out_dir/timeline.md"
run_report "blockers" "$script_dir/swarm-blockers.sh" --dir "$swarm_dir" --out "$out_dir/blockers.md"
run_report "export" "$script_dir/swarm-export.sh" --dir "$swarm_dir" --out "$out_dir/export"

if [[ -n "$session" ]]; then
  run_report "assign" "$script_dir/swarm-assign.sh" --swarm-dir "$swarm_dir" --session "$session" --out "$out_dir/assign.md"
else
  run_report "assign" "$script_dir/swarm-assign.sh" --swarm-dir "$swarm_dir" --out "$out_dir/assign.md"
fi

cat > "$out_dir/index.md" <<EOF
# auto-tmux Swarm Report Pack

- created_at: \`$(date -Is)\`
- swarm_dir: \`$swarm_dir\`
- session: \`${session:-<not provided>}\`

## Files

- [board.md](./board.md)
- [deps.md](./deps.md)
- [timeline.md](./timeline.md)
- [blockers.md](./blockers.md)
- [assign.md](./assign.md)
- [export/manifest.json](./export/manifest.json)
EOF

rm -f /tmp/auto-tmux-report-pack.log
printf 'swarm report pack written: %s\n' "$out_dir"
