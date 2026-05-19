#!/usr/bin/env bash
# swarm-results: render terminal worker results as a delivery summary.
set -euo pipefail

usage() {
  cat <<'EOF'
swarm-results: summarize DONE/FAIL/BLOCKED worker results

Usage:
  swarm-results.sh [--dir DIR] [--out FILE] [--limit N]

Defaults:
  --dir   AUTO_TMUX_SWARM_DIR or /tmp/ai_swarm
  --out   stdout
  --limit 80 result rows

This script is read-only. It does not mutate swarm state.
EOF
}

die() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

swarm_dir="${AUTO_TMUX_SWARM_DIR:-/tmp/ai_swarm}"
out_file=""
limit=80

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
    --limit)
      limit="${2:-}"
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

[[ "$limit" =~ ^[0-9]+$ ]] || die "--limit must be a number"

tasks_tsv="$swarm_dir/tasks.tsv"
results_dir="$swarm_dir/results"
status_log="$swarm_dir/status.log"
[[ -f "$tasks_tsv" ]] || die "tasks file not found: $tasks_tsv"

render_results() {
  printf '# auto-tmux Swarm Results\n\n'
  printf -- '- dir: `%s`\n' "$swarm_dir"
  printf -- '- created_at: `%s`\n\n' "$(date -Is)"

  printf '## Summary\n\n'
  awk -F '\t' '
    NR > 1 {count[$2]++}
    END {
      print "| status | count |"
      print "|:---|---:|"
      n = split("DONE FAIL BLOCKED DOING TODO", order, " ")
      for (i = 1; i <= n; i++) {
        status = order[i]
        print "| `" status "` | " (count[status] + 0) " |"
      }
    }
  ' "$tasks_tsv"

  printf '\n## Terminal Results\n\n'
  printf '| status | id | owner | text | result |\n'
  printf '|:---|:---|:---|:---|:---|\n'
  awk -F '\t' -v limit="$limit" '
    function esc(value) {
      gsub(/\|/, "\\|", value)
      return value
    }
    NR > 1 && ($2 == "DONE" || $2 == "FAIL" || $2 == "BLOCKED") {
      print "| `" esc($2) "` | `" esc($1) "` | `" esc($3) "` | " esc($4) " | " esc($5) " |"
      shown++
      if (shown >= limit) exit
    }
    END {if (shown == 0) print "| - | - | - | - | - |"}
  ' "$tasks_tsv"

  printf '\n## Result Files\n\n'
  if [[ -d "$results_dir" ]] && find "$results_dir" -mindepth 1 -maxdepth 1 -type f -name '*.txt' -print -quit | grep -q .; then
    find "$results_dir" -mindepth 1 -maxdepth 1 -type f -name '*.txt' -print | sort | while read -r path; do
      printf -- '- `%s`: %s\n' "$(basename "$path")" "$(head -n 1 "$path")"
    done
  else
    printf -- '- no result files\n'
  fi

  printf '\n## Recent Terminal Status\n\n'
  if [[ -s "$status_log" ]]; then
    tail -n 30 "$status_log" | grep -E '\[(DONE|FAIL|BLOCKED)\]' | sed 's/^/- /' || printf -- '- no recent terminal status\n'
  else
    printf -- '- no status log\n'
  fi
}

if [[ -n "$out_file" ]]; then
  mkdir -p "$(dirname "$out_file")"
  render_results > "$out_file"
  printf 'swarm results written: %s\n' "$out_file"
else
  render_results
fi
