#!/usr/bin/env bash
# swarm-timeline: render swarm status.log as a Markdown timeline.
set -euo pipefail

usage() {
  cat <<'EOF'
swarm-timeline: render auto-tmux status.log as Markdown

Usage:
  swarm-timeline.sh [--dir DIR] [--out FILE] [-n LINES]

Defaults:
  --dir AUTO_TMUX_SWARM_DIR or /tmp/ai_swarm
  --out stdout
  -n    100 recent status lines

This script is read-only. It does not mutate swarm state.
EOF
}

die() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

swarm_dir="${AUTO_TMUX_SWARM_DIR:-/tmp/ai_swarm}"
out_file=""
lines=100

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dir|--swarm-dir)
      swarm_dir="${2:-}"
      shift 2
      ;;
    --out)
      out_file="${2:-}"
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
status_log="$swarm_dir/status.log"
[[ -f "$status_log" ]] || die "status log not found: $status_log"

render_timeline() {
  printf '# auto-tmux Swarm Timeline\n\n'
  printf -- '- dir: `%s`\n' "$swarm_dir"
  printf -- '- created_at: `%s`\n' "$(date -Is)"
  printf -- '- lines: `%s`\n\n' "$lines"

  printf '## Summary\n\n'
  printf '| status | count |\n'
  printf '|:---|---:|\n'
  tail -n "$lines" "$status_log" |
    awk -F '[][]' '
      NF >= 6 {count[$6]++}
      END {
        if (length(count) == 0) {
          print "| - | 0 |"
        } else {
          for (status in count) print "| `" status "` | " count[status] " |"
        }
      }
    ' | sort

  printf '\n## Timeline\n\n'
  tail -n "$lines" "$status_log" |
    awk -F '[][]' '
      function esc(value) {
        gsub(/\|/, "\\|", value)
        return value
      }
      NF >= 6 {
        message = $7
        sub(/^ /, "", message)
        print "- `" $2 "` `" esc($4) "` **" esc($6) "** " esc(message)
        next
      }
      {print "- " esc($0)}
    '
}

if [[ -n "$out_file" ]]; then
  mkdir -p "$(dirname "$out_file")"
  render_timeline > "$out_file"
  printf 'swarm timeline written: %s\n' "$out_file"
else
  render_timeline
fi
