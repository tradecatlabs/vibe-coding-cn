#!/usr/bin/env bash
# safety-check: inspect text/file payloads before tmux send, paste or dispatch.
set -euo pipefail

usage() {
  cat <<'EOF'
safety-check: inspect an auto-tmux payload before sending it to a pane

Usage:
  safety-check.sh --text TEXT [--strict]
  safety-check.sh --file FILE [--strict]
  safety-check.sh --stdin [--strict]

Checks:
  - dangerous shell/database/tmux commands that require explicit review
  - common secret patterns that should not be pasted into shared panes
  - oversized payloads that should use paste/archive instead of send

Exit codes:
  0: no issue found
  1: warning found
  2: blocking issue found
EOF
}

die() {
  printf 'error: %s\n' "$*" >&2
  exit 2
}

input=""
label=""
strict="0"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --text)
      input="${2:-}"
      label="<text>"
      shift 2
      ;;
    --file)
      [[ -f "${2:-}" ]] || die "file not found: ${2:-}"
      input="$(cat "$2")"
      label="$2"
      shift 2
      ;;
    --stdin)
      input="$(cat)"
      label="<stdin>"
      shift
      ;;
    --strict)
      strict="1"
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

[[ -n "$label" ]] || die "one input source is required: --text, --file or --stdin"

dangerous_pattern='(^|[[:space:];|&])(rm[[:space:]]+-rf|mkfs|dd[[:space:]]+if=|shutdown|reboot|halt|poweroff|tmux[[:space:]]+kill-server|git[[:space:]]+reset[[:space:]]+--hard|git[[:space:]]+clean[[:space:]]+-fd|DROP[[:space:]]+(DATABASE|TABLE))'
secret_pattern='(OPENAI_API_KEY|ANTHROPIC_API_KEY|GITHUB_TOKEN|GH_TOKEN|API_KEY|TOKEN|PASSWORD|SECRET)=|Bearer[[:space:]]+[A-Za-z0-9._~+/=-]+|sk-[A-Za-z0-9_-]{12,}'

failures=0
warnings=0

if printf '%s\n' "$input" | grep -Eiq "$dangerous_pattern"; then
  printf '[FAIL] dangerous command pattern detected in %s\n' "$label" >&2
  failures=$((failures + 1))
fi

if printf '%s\n' "$input" | grep -Eiq "$secret_pattern"; then
  if [[ "$strict" == "1" ]]; then
    printf '[FAIL] possible secret detected in %s\n' "$label" >&2
    failures=$((failures + 1))
  else
    printf '[WARN] possible secret detected in %s\n' "$label" >&2
    warnings=$((warnings + 1))
  fi
fi

byte_count="$(printf '%s' "$input" | wc -c | tr -d ' ')"
line_count="$(printf '%s\n' "$input" | wc -l | tr -d ' ')"
if (( byte_count > 8192 )); then
  printf '[WARN] payload is large: %s bytes; prefer paste-buffer or archive handoff\n' "$byte_count" >&2
  warnings=$((warnings + 1))
fi

printf 'safety-check target=%s bytes=%s lines=%s strict=%s\n' "$label" "$byte_count" "$line_count" "$strict"

if (( failures > 0 )); then
  exit 2
fi
if (( warnings > 0 )); then
  exit 1
fi
printf '[OK] no safety issue found\n'
