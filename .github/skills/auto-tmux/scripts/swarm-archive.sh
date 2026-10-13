#!/usr/bin/env bash
# Build a portable archive for a tmux AI swarm handoff.
set -euo pipefail

usage() {
  cat <<'EOF'
swarm-archive: build a portable auto-tmux handoff archive

Usage:
  swarm-archive.sh [--session NAME] [--swarm-dir DIR] [--out FILE] [-n LINES]

Examples:
  swarm-archive.sh --session ai-hub --swarm-dir /tmp/ai_swarm
  swarm-archive.sh --session ai-hub --out /tmp/ai-hub-handoff.tar.gz -n 120
EOF
}

die() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
auto_tmux="$script_dir/auto-tmux.sh"
swarm_brief="$script_dir/swarm-brief.sh"

session=""
swarm_dir="${AUTO_TMUX_SWARM_DIR:-/tmp/ai_swarm}"
out_file="/tmp/auto-tmux-archive-$(date +%Y%m%d-%H%M%S).tar.gz"
lines=120

while [[ $# -gt 0 ]]; do
  case "$1" in
    --session) session="${2:-}"; shift 2 ;;
    --swarm-dir) swarm_dir="${2:-}"; shift 2 ;;
    --out) out_file="${2:-}"; shift 2 ;;
    -n|--lines) lines="${2:-}"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) die "unknown option: $1" ;;
  esac
done

[[ "$lines" =~ ^[0-9]+$ ]] || die "--lines must be a positive integer"
command -v tar >/dev/null 2>&1 || die "tar is not installed or not in PATH"

work_dir="$(mktemp -d /tmp/auto-tmux-archive.XXXXXX)"
cleanup() {
  rm -rf "$work_dir"
}
trap cleanup EXIT

mkdir -p "$work_dir"
{
  printf '# auto-tmux archive manifest\n\n'
  printf '%s\n' "- created_at: \`$(date -Is)\`"
  printf '%s\n' "- session: \`${session:-<all>}\`"
  printf '%s\n' "- swarm_dir: \`$swarm_dir\`"
  printf '%s\n' "- lines_per_pane: \`$lines\`"
} > "$work_dir/MANIFEST.md"

brief_args=(--swarm-dir "$swarm_dir" --out "$work_dir/brief" -n "$lines")
snapshot_args=(snapshot --dir "$work_dir/snapshot" -n "$lines")
if [[ -n "$session" ]]; then
  brief_args=(--session "$session" "${brief_args[@]}")
  snapshot_args=(snapshot --session "$session" --dir "$work_dir/snapshot" -n "$lines")
fi

"$swarm_brief" "${brief_args[@]}" > "$work_dir/brief.log" 2>&1 || true
"$auto_tmux" "${snapshot_args[@]}" > "$work_dir/snapshot.log" 2>&1 || true

if [[ -d "$swarm_dir" ]]; then
  mkdir -p "$work_dir/state"
  cp -a "$swarm_dir/." "$work_dir/state/"
else
  printf 'swarm state dir not found: %s\n' "$swarm_dir" > "$work_dir/state-missing.txt"
fi

mkdir -p "$(dirname "$out_file")"
tar -czf "$out_file" -C "$work_dir" .
printf 'archive written: %s\n' "$out_file"
