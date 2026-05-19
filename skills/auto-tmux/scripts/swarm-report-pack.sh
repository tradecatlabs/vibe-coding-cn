#!/usr/bin/env bash
# swarm-report-pack: build a portable read-only report pack for swarm state.
set -euo pipefail

usage() {
  cat <<'EOF'
swarm-report-pack: build an auto-tmux swarm report pack

Usage:
  swarm-report-pack.sh [--dir DIR] [--session NAME] [--out DIR] [--attach DIR ...] [--tar]

Defaults:
  --dir AUTO_TMUX_SWARM_DIR or /tmp/ai_swarm
  --out /tmp/auto-tmux-report-pack-YYYYmmdd-HHMMSS

This script is read-only for tmux and swarm state. It writes only to --out.
Use --attach to copy explicit external evidence directories into the report pack.
Use --tar to create OUT.tar.gz after the directory report pack is written.
EOF
}

die() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

json_escape() {
  local value="$1"
  value="${value//\\/\\\\}"
  value="${value//\"/\\\"}"
  value="${value//$'\n'/\\n}"
  value="${value//$'\r'/\\r}"
  value="${value//$'\t'/\\t}"
  printf '%s' "$value"
}

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
swarm_dir="${AUTO_TMUX_SWARM_DIR:-/tmp/ai_swarm}"
session=""
out_dir="/tmp/auto-tmux-report-pack-$(date +%Y%m%d-%H%M%S)"
attachments=()
created_at="$(date -Is)"
make_tar="0"

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
    --attach)
      attachments+=("${2:-}")
      shift 2
      ;;
    --tar)
      make_tar="1"
      shift
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
run_report "results" "$script_dir/swarm-results.sh" --dir "$swarm_dir" --out "$out_dir/results.md" --jsonl "$out_dir/results.jsonl"
run_report "export" "$script_dir/swarm-export.sh" --dir "$swarm_dir" --out "$out_dir/export"

if [[ -n "$session" ]]; then
  run_report "assign" "$script_dir/swarm-assign.sh" --swarm-dir "$swarm_dir" --session "$session" --out "$out_dir/assign.md"
else
  run_report "assign" "$script_dir/swarm-assign.sh" --swarm-dir "$swarm_dir" --out "$out_dir/assign.md"
fi

attachment_lines=""
attachment_json=""
attachment_count=0
if ((${#attachments[@]} > 0)); then
  mkdir -p "$out_dir/attachments"
  cat > "$out_dir/attachments.md" <<EOF
# Attachments

EOF
  for attachment in "${attachments[@]}"; do
    [[ -d "$attachment" ]] || die "attachment is not a directory: $attachment"
    name="$(basename "$attachment")"
    safe_name="$(printf '%s' "$name" | tr -c 'A-Za-z0-9._-' '_')"
    dest="$out_dir/attachments/$safe_name"
    suffix=1
    while [[ -e "$dest" ]]; do
      dest="$out_dir/attachments/${safe_name}_$suffix"
      suffix=$((suffix + 1))
    done
    cp -a "$attachment" "$dest"
    rel_path="attachments/$(basename "$dest")"
    printf -- '- [%s](./%s)\n' "$attachment" "$rel_path" >> "$out_dir/attachments.md"
    attachment_lines+="- [$rel_path](./$rel_path)"$'\n'
    if ((attachment_count > 0)); then
      attachment_json+=","$'\n'
    fi
    attachment_json+="    {\"source\":\"$(json_escape "$attachment")\",\"path\":\"$(json_escape "$rel_path")\"}"
    attachment_count=$((attachment_count + 1))
  done
fi

cat > "$out_dir/manifest.json" <<EOF
{
  "type": "auto-tmux-swarm-report-pack",
  "created_at": "$(json_escape "$created_at")",
  "swarm_dir": "$(json_escape "$swarm_dir")",
  "session": "$(json_escape "${session:-<not provided>}")",
  "files": [
    "index.md",
    "board.md",
    "deps.md",
    "timeline.md",
    "blockers.md",
    "results.md",
    "results.jsonl",
    "assign.md",
    "export/manifest.json"
  ],
  "attachments": [
$attachment_json
  ]
}
EOF

cat > "$out_dir/index.md" <<EOF
# auto-tmux Swarm Report Pack

- created_at: \`$created_at\`
- swarm_dir: \`$swarm_dir\`
- session: \`${session:-<not provided>}\`

## Files

- [board.md](./board.md)
- [deps.md](./deps.md)
- [timeline.md](./timeline.md)
- [blockers.md](./blockers.md)
- [results.md](./results.md)
- [results.jsonl](./results.jsonl)
- [assign.md](./assign.md)
- [manifest.json](./manifest.json)
- [export/manifest.json](./export/manifest.json)
$(if [[ -n "$attachment_lines" ]]; then printf '%s' "- [attachments.md](./attachments.md)"; fi)
EOF

rm -f /tmp/auto-tmux-report-pack.log
if [[ "$make_tar" == "1" ]]; then
  command -v tar >/dev/null 2>&1 || die "tar not found"
  parent_dir="$(cd "$(dirname "$out_dir")" && pwd)"
  base_dir="$(basename "$out_dir")"
  tar -C "$parent_dir" -czf "$out_dir.tar.gz" "$base_dir"
  printf 'swarm report archive written: %s\n' "$out_dir.tar.gz"
fi
printf 'swarm report pack written: %s\n' "$out_dir"
