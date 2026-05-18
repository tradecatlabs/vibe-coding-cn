#!/usr/bin/env bash
# swarm-board: render swarm tasks, dependencies and locks as a Markdown board.
set -euo pipefail

usage() {
  cat <<'EOF'
swarm-board: render an auto-tmux swarm state directory as Markdown

Usage:
  swarm-board.sh [--dir DIR] [--out FILE] [--limit N]

Defaults:
  --dir   AUTO_TMUX_SWARM_DIR or /tmp/ai_swarm
  --out   stdout
  --limit 50 rows per section
EOF
}

die() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

swarm_dir="${AUTO_TMUX_SWARM_DIR:-/tmp/ai_swarm}"
out_file=""
limit=50

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dir)
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
deps_tsv="$swarm_dir/deps.tsv"
locks_dir="$swarm_dir/locks"
status_log="$swarm_dir/status.log"

[[ -f "$tasks_tsv" ]] || die "tasks file not found: $tasks_tsv"
[[ -f "$deps_tsv" ]] || die "deps file not found: $deps_tsv"

render_summary() {
  awk -F '\t' '
    NR > 1 {count[$2]++}
    END {
      print "| status | count |"
      print "|:---|---:|"
      n = split("TODO DOING DONE BLOCKED FAIL", order, " ")
      for (i = 1; i <= n; i++) {
        status = order[i]
        print "| `" status "` | " (count[status] + 0) " |"
      }
    }
  ' "$tasks_tsv"
}

render_ready() {
  awk -F '\t' -v limit="$limit" '
    function esc(value) {
      gsub(/\|/, "\\|", value)
      return value
    }
    FILENAME == ARGV[1] {
      if (FNR == 1) next
      status[$1] = $2
      owner[$1] = $3
      text[$1] = $4
      result[$1] = $5
      order[++n] = $1
      next
    }
    FILENAME == ARGV[2] {
      if (FNR == 1) next
      if (status[$2] != "DONE") {
        blocked[$1] = blocked[$1] ? blocked[$1] ", " $2 : $2
      }
      next
    }
    END {
      print "| id | owner | text |"
      print "|:---|:---|:---|"
      shown = 0
      for (i = 1; i <= n; i++) {
        id = order[i]
        if (status[id] == "TODO" && blocked[id] == "") {
          print "| `" esc(id) "` | `" esc(owner[id]) "` | " esc(text[id]) " |"
          shown++
          if (shown >= limit) break
        }
      }
      if (shown == 0) print "| - | - | - |"
    }
  ' "$tasks_tsv" "$deps_tsv"
}

render_status_section() {
  local status="$1"
  awk -F '\t' -v wanted="$status" -v limit="$limit" '
    function esc(value) {
      gsub(/\|/, "\\|", value)
      return value
    }
    BEGIN {
      print "| id | owner | text | result |"
      print "|:---|:---|:---|:---|"
    }
    NR > 1 && $2 == wanted {
      print "| `" esc($1) "` | `" esc($3) "` | " esc($4) " | " esc($5) " |"
      shown++
      if (shown >= limit) exit
    }
    END {
      if (shown == 0) print "| - | - | - | - |"
    }
  ' "$tasks_tsv"
}

render_locks() {
  printf '| lock | owner | created_at |\n'
  printf '|:---|:---|:---|\n'
  if [[ ! -d "$locks_dir" ]] || ! find "$locks_dir" -mindepth 1 -maxdepth 1 -type d -name '*.lock.d' -print -quit | grep -q .; then
    printf '| - | - | - |\n'
    return 0
  fi
  find "$locks_dir" -mindepth 1 -maxdepth 1 -type d -name '*.lock.d' -print | sort | while read -r path; do
    printf '| `%s` | `%s` | %s |\n' \
      "$(basename "$path" .lock.d)" \
      "$(cat "$path/owner" 2>/dev/null || printf unknown)" \
      "$(cat "$path/created_at" 2>/dev/null || printf unknown)"
  done
}

render_recent_status() {
  if [[ -s "$status_log" ]]; then
    tail -n 20 "$status_log" | sed 's/^/- /'
  else
    printf -- '- no status log\n'
  fi
}

render_board() {
  printf '# auto-tmux Swarm Board\n\n'
  printf -- '- dir: `%s`\n' "$swarm_dir"
  printf -- '- created_at: `%s`\n\n' "$(date -Is)"

  printf '## Summary\n\n'
  render_summary
  printf '\n## Ready TODO\n\n'
  render_ready

  local status
  for status in TODO DOING BLOCKED FAIL DONE; do
    printf '\n## %s\n\n' "$status"
    render_status_section "$status"
  done

  printf '\n## Locks\n\n'
  render_locks
  printf '\n## Recent Status\n\n'
  render_recent_status
}

if [[ -n "$out_file" ]]; then
  mkdir -p "$(dirname "$out_file")"
  render_board > "$out_file"
  printf 'swarm board written: %s\n' "$out_file"
else
  render_board
fi
