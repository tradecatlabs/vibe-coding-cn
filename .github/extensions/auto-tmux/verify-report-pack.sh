#!/usr/bin/env bash
# verify-report-pack: verify an auto-tmux report pack with local gates.
set -euo pipefail

usage() {
  cat <<'EOF'
verify-report-pack: verify an auto-tmux report pack

Usage:
  verify-report-pack.sh --pack DIR

Checks:
  - required report pack files via review-checklist --strict
  - root manifest type
  - results.jsonl required fields
EOF
}

die() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
pack_dir=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --pack)
      pack_dir="${2:-}"
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

"$script_dir/review-checklist.sh" --pack "$pack_dir" --strict >/dev/null
grep -Fq '"type": "auto-tmux-swarm-report-pack"' "$pack_dir/manifest.json" || die "invalid manifest type"
"$script_dir/check-jsonl.sh" "$pack_dir/results.jsonl" --require-key type --require-key id --require-key status >/dev/null

printf 'report pack ok: %s\n' "$pack_dir"
