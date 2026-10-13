#!/usr/bin/env bash
# check-jsonl: lightweight JSONL field gate without jq dependency.
set -euo pipefail

usage() {
  cat <<'EOF'
check-jsonl: validate JSONL-like lines contain required fields

Usage:
  check-jsonl.sh FILE [--require-key KEY ...]

Defaults:
  Requires no fixed keys unless --require-key is provided.

This is a lightweight gate: it checks non-empty lines look like JSON objects and
contain required top-level key names. It does not replace a full JSON parser.
EOF
}

die() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

file=""
required_keys=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --require-key)
      required_keys+=("${2:-}")
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      if [[ -z "$file" ]]; then
        file="$1"
        shift
      else
        die "unknown option: $1"
      fi
      ;;
  esac
done

[[ -n "$file" ]] || die "missing FILE"
[[ -f "$file" ]] || die "file not found: $file"

line_no=0
checked=0
while IFS= read -r line || [[ -n "$line" ]]; do
  line_no=$((line_no + 1))
  [[ -n "$line" ]] || continue
  [[ "$line" =~ ^\{.*\}$ ]] || die "line $line_no is not a JSON object"
  for key in "${required_keys[@]}"; do
    [[ "$line" == *"\"$key\""* ]] || die "line $line_no missing key: $key"
  done
  checked=$((checked + 1))
done < "$file"

((checked > 0)) || die "no JSONL records found"
printf 'jsonl ok: %s records=%s\n' "$file" "$checked"
