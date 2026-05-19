#!/usr/bin/env bash
# review-checklist: render a reviewer checklist for an auto-tmux report pack.
set -euo pipefail

usage() {
  cat <<'EOF'
review-checklist: render a reviewer checklist for an auto-tmux report pack

Usage:
  review-checklist.sh --pack DIR [--out FILE]

Defaults:
  --out stdout

This script is read-only for the report pack. It writes only when --out is set.
EOF
}

die() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

pack_dir=""
out_file=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --pack)
      pack_dir="${2:-}"
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

[[ -n "$pack_dir" ]] || die "missing --pack"
[[ -d "$pack_dir" ]] || die "pack dir not found: $pack_dir"

exists_mark() {
  local path="$1"
  if [[ -e "$pack_dir/$path" ]]; then
    printf 'x'
  else
    printf ' '
  fi
}

render_checklist() {
  printf '# auto-tmux Report Review Checklist\n\n'
  printf -- '- pack_dir: `%s`\n' "$pack_dir"
  printf -- '- created_at: `%s`\n\n' "$(date -Is)"

  printf '## Required Files\n\n'
  local file
  for file in index.md manifest.json board.md deps.md timeline.md blockers.md results.md results.jsonl assign.md export/manifest.json; do
    printf -- '- [%s] `%s`\n' "$(exists_mark "$file")" "$file"
  done

  printf '\n## Review Gates\n\n'
  printf -- '- [ ] `manifest.json` type is `auto-tmux-swarm-report-pack`.\n'
  printf -- '- [ ] `results.md` clearly lists DONE/FAIL/BLOCKED worker outcomes.\n'
  printf -- '- [ ] `blockers.md` has no unresolved blocker that prevents handoff.\n'
  printf -- '- [ ] `assign.md` does not imply an unclaimed task was silently executed.\n'
  printf -- '- [ ] Attachments, if present, are explicit evidence directories and do not contain secrets.\n'
  printf -- '- [ ] Reviewer can reproduce the key conclusion from files in this pack only.\n'

  printf '\n## Suggested Commands\n\n'
  printf '```bash\n'
  printf 'skills/auto-tmux/scripts/check-jsonl.sh %q --require-key type --require-key id --require-key status\n' "$pack_dir/results.jsonl"
  printf 'grep -F "\"type\": \"auto-tmux-swarm-report-pack\"" %q\n' "$pack_dir/manifest.json"
  printf '```\n'
}

if [[ -n "$out_file" ]]; then
  mkdir -p "$(dirname "$out_file")"
  render_checklist > "$out_file"
  printf 'review checklist written: %s\n' "$out_file"
else
  render_checklist
fi
