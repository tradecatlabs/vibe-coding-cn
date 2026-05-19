#!/usr/bin/env bash
# swarm-deps-graph: render swarm task dependencies as Markdown + Mermaid.
set -euo pipefail

usage() {
  cat <<'EOF'
swarm-deps-graph: render auto-tmux task dependencies

Usage:
  swarm-deps-graph.sh [--dir DIR] [--out FILE]

Defaults:
  --dir AUTO_TMUX_SWARM_DIR or /tmp/ai_swarm
  --out stdout

This script is read-only. It does not mutate swarm state.
EOF
}

die() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

swarm_dir="${AUTO_TMUX_SWARM_DIR:-/tmp/ai_swarm}"
out_file=""

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
    -h|--help)
      usage
      exit 0
      ;;
    *)
      die "unknown option: $1"
      ;;
  esac
done

tasks_tsv="$swarm_dir/tasks.tsv"
deps_tsv="$swarm_dir/deps.tsv"
[[ -f "$tasks_tsv" ]] || die "tasks file not found: $tasks_tsv"
[[ -f "$deps_tsv" ]] || die "deps file not found: $deps_tsv"

render_graph() {
  printf '# auto-tmux Swarm Dependency Graph\n\n'
  printf -- '- dir: `%s`\n' "$swarm_dir"
  printf -- '- created_at: `%s`\n\n' "$(date -Is)"

  printf '## Mermaid\n\n'
  printf '```mermaid\n'
  printf 'flowchart TD\n'
  awk -F '\t' '
    function node_id(id) {
      gsub(/[^A-Za-z0-9_]/, "_", id)
      return "task_" id
    }
    function label(value) {
      gsub(/"/, "\\\"", value)
      return value
    }
    FILENAME == ARGV[1] {
      if (FNR == 1) next
      id = $1
      status[id] = $2
      text[id] = $4
      print "  " node_id(id) "[\"" label(id ": " $2) "\"]"
      next
    }
    FILENAME == ARGV[2] {
      if (FNR == 1) next
      print "  " node_id($2) " --> " node_id($1)
      has_dep = 1
      next
    }
    END {
      if (!has_dep) print "  empty[\"no dependencies\"]"
    }
  ' "$tasks_tsv" "$deps_tsv"
  printf '```\n\n'

  printf '## Dependencies\n\n'
  printf '| task | blocked_by |\n'
  printf '|:---|:---|\n'
  awk -F '\t' '
    NR == 1 {next}
    {print "| `" $1 "` | `" $2 "` |"; found = 1}
    END {if (!found) print "| - | - |"}
  ' "$deps_tsv"
}

if [[ -n "$out_file" ]]; then
  mkdir -p "$(dirname "$out_file")"
  render_graph > "$out_file"
  printf 'swarm dependency graph written: %s\n' "$out_file"
else
  render_graph
fi
