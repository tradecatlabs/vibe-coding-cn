#!/usr/bin/env bash
# record-summary: summarize auto-tmux pipe-pane record logs as Markdown.
set -euo pipefail

usage() {
  cat <<'EOF'
record-summary: summarize auto-tmux record logs

Usage:
  record-summary.sh [--dir DIR] [--out FILE] [-n LINES]

Defaults:
  --dir /tmp/auto-tmux-records
  --out stdout
  -n    40 tail lines per log

This script is read-only. It never modifies tmux sessions or record logs.
EOF
}

die() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

record_dir="/tmp/auto-tmux-records"
out_file=""
lines=40

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dir)
      record_dir="${2:-}"
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
[[ -d "$record_dir" ]] || die "record directory not found: $record_dir"

redact() {
  sed -E \
    -e 's/(OPENAI_API_KEY|ANTHROPIC_API_KEY|GITHUB_TOKEN|GH_TOKEN|API_KEY|TOKEN|PASSWORD|SECRET)=([^[:space:]]+)/\1=<redacted>/g' \
    -e 's/(Bearer[[:space:]]+)[A-Za-z0-9._~+\/=-]+/\1<redacted>/g' \
    -e 's/(sk-[A-Za-z0-9_-]{12,})/<redacted-openai-key>/g'
}

render_summary() {
  printf '# auto-tmux Record Summary\n\n'
  printf -- '- dir: `%s`\n' "$record_dir"
  printf -- '- created_at: `%s`\n\n' "$(date -Is)"

  printf '## Logs\n\n'
  printf '| file | bytes | lines | modified |\n'
  printf '|:---|---:|---:|:---|\n'
  find "$record_dir" -maxdepth 1 -type f -name '*.log' -print | sort | while read -r file; do
    printf '| `%s` | %s | %s | %s |\n' \
      "$(basename "$file")" \
      "$(wc -c < "$file" | tr -d ' ')" \
      "$(wc -l < "$file" | tr -d ' ')" \
      "$(date -r "$file" -Is 2>/dev/null || printf unknown)"
  done

  if ! find "$record_dir" -maxdepth 1 -type f -name '*.log' -print -quit | grep -q .; then
    printf '| - | 0 | 0 | - |\n'
    return 0
  fi

  printf '\n## Recent Output\n\n'
  find "$record_dir" -maxdepth 1 -type f -name '*.log' -print | sort | while read -r file; do
    printf '### `%s`\n\n' "$(basename "$file")"
    printf '```text\n'
    tail -n "$lines" "$file" | redact
    printf '\n```\n\n'
  done
}

if [[ -n "$out_file" ]]; then
  mkdir -p "$(dirname "$out_file")"
  render_summary > "$out_file"
  printf 'record summary written: %s\n' "$out_file"
else
  render_summary
fi
