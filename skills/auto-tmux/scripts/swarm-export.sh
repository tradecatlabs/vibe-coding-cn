#!/usr/bin/env bash
# swarm-export: export swarm state as machine-readable JSONL files.
set -euo pipefail

usage() {
  cat <<'EOF'
swarm-export: export auto-tmux swarm state as JSONL

Usage:
  swarm-export.sh [--dir DIR] [--out DIR]

Defaults:
  --dir AUTO_TMUX_SWARM_DIR or /tmp/ai_swarm
  --out /tmp/auto-tmux-export-YYYYmmdd-HHMMSS

Outputs:
  tasks.jsonl
  deps.jsonl
  locks.jsonl
  manifest.json

This script is read-only. It does not mutate swarm state.
EOF
}

die() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

swarm_dir="${AUTO_TMUX_SWARM_DIR:-/tmp/ai_swarm}"
out_dir="/tmp/auto-tmux-export-$(date +%Y%m%d-%H%M%S)"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dir|--swarm-dir)
      swarm_dir="${2:-}"
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

tasks_tsv="$swarm_dir/tasks.tsv"
deps_tsv="$swarm_dir/deps.tsv"
locks_dir="$swarm_dir/locks"
[[ -f "$tasks_tsv" ]] || die "tasks file not found: $tasks_tsv"
[[ -f "$deps_tsv" ]] || die "deps file not found: $deps_tsv"
mkdir -p "$out_dir"

json_escape() {
  printf '%s' "$1" | sed -e 's/\\/\\\\/g' -e 's/"/\\"/g' -e 's/\r/\\r/g' -e 's/\n/\\n/g'
}

awk -F '\t' '
  function json(value) {
    gsub(/\\/, "\\\\", value)
    gsub(/"/, "\\\"", value)
    gsub(/\r/, "\\r", value)
    gsub(/\n/, "\\n", value)
    return value
  }
  NR > 1 {
    print "{\"id\":\"" json($1) "\",\"status\":\"" json($2) "\",\"owner\":\"" json($3) "\",\"text\":\"" json($4) "\",\"result\":\"" json($5) "\"}"
  }
' "$tasks_tsv" > "$out_dir/tasks.jsonl"

awk -F '\t' '
  function json(value) {
    gsub(/\\/, "\\\\", value)
    gsub(/"/, "\\\"", value)
    return value
  }
  NR > 1 {
    print "{\"task_id\":\"" json($1) "\",\"blocked_by\":\"" json($2) "\"}"
  }
' "$deps_tsv" > "$out_dir/deps.jsonl"

if [[ -d "$locks_dir" ]]; then
  find "$locks_dir" -mindepth 1 -maxdepth 1 -type d -name '*.lock.d' -print | sort | while read -r path; do
    name="$(basename "$path" .lock.d)"
    owner="$(cat "$path/owner" 2>/dev/null || printf unknown)"
    created_at="$(cat "$path/created_at" 2>/dev/null || printf unknown)"
    printf '{"name":"%s","owner":"%s","created_at":"%s"}\n' \
      "$(json_escape "$name")" "$(json_escape "$owner")" "$(json_escape "$created_at")"
  done > "$out_dir/locks.jsonl"
else
  : > "$out_dir/locks.jsonl"
fi

printf '{"type":"auto-tmux-swarm-export","created_at":"%s","swarm_dir":"%s","files":["tasks.jsonl","deps.jsonl","locks.jsonl"]}\n' \
  "$(date -Is)" "$(json_escape "$swarm_dir")" > "$out_dir/manifest.json"

printf 'swarm export written: %s\n' "$out_dir"
