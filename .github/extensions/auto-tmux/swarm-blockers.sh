#!/usr/bin/env bash
# swarm-blockers: render blocked/failed tasks and active locks as Markdown.
set -euo pipefail

usage() {
  cat <<'EOF'
swarm-blockers: summarize auto-tmux blockers

Usage:
  swarm-blockers.sh [--dir DIR] [--out FILE] [-n LINES]

Defaults:
  --dir AUTO_TMUX_SWARM_DIR or /tmp/ai_swarm
  --out stdout
  -n    50 recent status lines

This script is read-only. It does not mutate swarm state.
EOF
}

die() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

swarm_dir="${AUTO_TMUX_SWARM_DIR:-/tmp/ai_swarm}"
out_file=""
lines=50

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
tasks_tsv="$swarm_dir/tasks.tsv"
locks_dir="$swarm_dir/locks"
status_log="$swarm_dir/status.log"
[[ -f "$tasks_tsv" ]] || die "tasks file not found: $tasks_tsv"

render_blockers() {
  printf '# auto-tmux Swarm Blockers\n\n'
  printf -- '- dir: `%s`\n' "$swarm_dir"
  printf -- '- created_at: `%s`\n\n' "$(date -Is)"

  printf '## BLOCKED / FAIL Tasks\n\n'
  printf '| status | id | owner | text | result |\n'
  printf '|:---|:---|:---|:---|:---|\n'
  awk -F '\t' '
    function esc(value) {
      gsub(/\|/, "\\|", value)
      return value
    }
    NR > 1 && ($2 == "BLOCKED" || $2 == "FAIL") {
      print "| `" esc($2) "` | `" esc($1) "` | `" esc($3) "` | " esc($4) " | " esc($5) " |"
      found = 1
    }
    END {if (!found) print "| - | - | - | - | - |"}
  ' "$tasks_tsv"

  printf '\n## Active Locks\n\n'
  printf '| lock | owner | created_at |\n'
  printf '|:---|:---|:---|\n'
  if [[ -d "$locks_dir" ]] && find "$locks_dir" -mindepth 1 -maxdepth 1 -type d -name '*.lock.d' -print -quit | grep -q .; then
    find "$locks_dir" -mindepth 1 -maxdepth 1 -type d -name '*.lock.d' -print | sort | while read -r path; do
      printf '| `%s` | `%s` | %s |\n' \
        "$(basename "$path" .lock.d)" \
        "$(cat "$path/owner" 2>/dev/null || printf unknown)" \
        "$(cat "$path/created_at" 2>/dev/null || printf unknown)"
    done
  else
    printf '| - | - | - |\n'
  fi

  printf '\n## Recent Risk Status\n\n'
  if [[ -s "$status_log" ]]; then
    tail -n "$lines" "$status_log" | grep -E '\[(BLOCKED|FAIL|ERROR|HELP)\]' | sed 's/^/- /' || printf -- '- no recent risk status\n'
  else
    printf -- '- no status log\n'
  fi
}

if [[ -n "$out_file" ]]; then
  mkdir -p "$(dirname "$out_file")"
  render_blockers > "$out_file"
  printf 'swarm blockers written: %s\n' "$out_file"
else
  render_blockers
fi
