#!/usr/bin/env bash
# swarm-assign: generate read-only task-to-pane dispatch suggestions.
set -euo pipefail

usage() {
  cat <<'EOF'
swarm-assign: suggest ready task assignments for auto-tmux workers

Usage:
  swarm-assign.sh [--swarm-dir DIR] [--session NAME] [--out FILE] [--limit N]

Defaults:
  --swarm-dir AUTO_TMUX_SWARM_DIR or /tmp/ai_swarm
  --session   omitted; use placeholder targets
  --out       stdout
  --limit     20 suggestions

This script is read-only. It does not claim tasks and does not send prompts.
EOF
}

die() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

swarm_dir="${AUTO_TMUX_SWARM_DIR:-/tmp/ai_swarm}"
session=""
out_file=""
limit=20

while [[ $# -gt 0 ]]; do
  case "$1" in
    --swarm-dir|--dir)
      swarm_dir="${2:-}"
      shift 2
      ;;
    --session)
      session="${2:-}"
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
[[ -f "$tasks_tsv" ]] || die "tasks file not found: $tasks_tsv"
[[ -f "$deps_tsv" ]] || die "deps file not found: $deps_tsv"

tmp_dir="$(mktemp -d)"
cleanup() {
  rm -rf "$tmp_dir"
}
trap cleanup EXIT

ready_tsv="$tmp_dir/ready.tsv"
panes_tsv="$tmp_dir/panes.tsv"

awk -F '\t' -v limit="$limit" '
  FILENAME == ARGV[1] {
    if (FNR == 1) next
    status[$1] = $2
    owner[$1] = $3
    text[$1] = $4
    order[++n] = $1
    next
  }
  FILENAME == ARGV[2] {
    if (FNR == 1) next
    if (status[$2] != "DONE") blocked[$1] = 1
    next
  }
  END {
    shown = 0
    for (i = 1; i <= n; i++) {
      id = order[i]
      if (status[id] == "TODO" && blocked[id] != 1) {
        print id "\t" owner[id] "\t" text[id]
        shown++
        if (shown >= limit) break
      }
    }
  }
' "$tasks_tsv" "$deps_tsv" > "$ready_tsv"

if [[ -n "$session" ]]; then
  command -v tmux >/dev/null 2>&1 || die "tmux is required when --session is used"
  tmux has-session -t "$session" 2>/dev/null || die "session not found: $session"
  tmux list-panes -t "$session" -F '#S:#{window_index}.#{pane_index}\t#{window_name}\t#{pane_current_command}' |
    awk -F '\t' 'tolower($2) ~ /worker/ {print; next} {other[++n] = $0} END {for (i = 1; i <= n; i++) print other[i]}' > "$panes_tsv"
else
  printf '<target-pane>\tworker\tunknown\n' > "$panes_tsv"
fi

render_assignments() {
  printf '# auto-tmux Swarm Assignment Suggestions\n\n'
  printf -- '- swarm_dir: `%s`\n' "$swarm_dir"
  printf -- '- session: `%s`\n' "${session:-<not provided>}"
  printf -- '- created_at: `%s`\n\n' "$(date -Is)"
  printf 'This is a read-only planning report. It does not claim tasks and does not send prompts.\n\n'

  printf '## Suggestions\n\n'
  printf '| task | current owner | target | command |\n'
  printf '|:---|:---|:---|:---|\n'

  if [[ ! -s "$ready_tsv" ]]; then
    printf '| - | - | - | no ready TODO task |\n'
    return 0
  fi

  awk -F '\t' -v swarm_dir="$swarm_dir" '
    FILENAME == ARGV[1] {
      pane[++pane_count] = $1
      next
    }
    FILENAME == ARGV[2] {
      task_count++
      idx = ((task_count - 1) % pane_count) + 1
      target = pane[idx]
      task_text = $3
      gsub(/"/, "\\\"", task_text)
      cmd = "skills/auto-tmux/scripts/swarm-dispatch.sh --role worker --target " target " --swarm-dir " swarm_dir " --task \"" $1 ": " task_text "\" --send --dry-run"
      gsub(/\|/, "\\|", $3)
      gsub(/\|/, "\\|", cmd)
      print "| `" $1 "` | `" $2 "` | `" target "` | `" cmd "` |"
    }
  ' "$panes_tsv" "$ready_tsv"

  printf '\n## Ready Tasks\n\n'
  printf '| id | owner | text |\n'
  printf '|:---|:---|:---|\n'
  awk -F '\t' '{gsub(/\|/, "\\|", $3); print "| `" $1 "` | `" $2 "` | " $3 " |"}' "$ready_tsv"
}

if [[ -n "$out_file" ]]; then
  mkdir -p "$(dirname "$out_file")"
  render_assignments > "$out_file"
  printf 'swarm assignments written: %s\n' "$out_file"
else
  render_assignments
fi
