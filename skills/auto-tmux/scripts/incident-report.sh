#!/usr/bin/env bash
# incident-report: generate an auto-tmux incident report template.
set -euo pipefail

usage() {
  cat <<'EOF'
incident-report: generate an auto-tmux incident report template

Usage:
  incident-report.sh --type TYPE [--out FILE]

Examples:
  incident-report.sh --type mis-send --out /tmp/auto-tmux-incident.md
  incident-report.sh --type broadcast
  incident-report.sh --type remote-readonly
  incident-report.sh --type secret-risk
EOF
}

die() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

incident_type=""
out_file=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --type)
      incident_type="${2:-}"
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

[[ -n "$incident_type" ]] || die "missing --type"

case "$incident_type" in
  mis-send|broadcast|remote-readonly|secret-risk) ;;
  *) die "unsupported incident type: $incident_type" ;;
esac

render_report() {
  cat <<EOF
# auto-tmux Incident Report

- type: \`$incident_type\`
- created_at: \`$(date -Is)\`
- operator:
- target_expected:
- target_actual:
- command_or_payload:
- impact:

## Evidence

- pane_capture:
- snapshot:
- report_pack:

## Mitigation

- immediate_action:
- rollback_or_cleanup:
- user_visible_impact:

## Prevention

- missing_gate:
- doc_or_script_update:
- follow_up_owner:

## Closeout

- [ ] Evidence captured.
- [ ] Sensitive output redacted.
- [ ] Affected task marked DONE/FAIL/BLOCKED.
- [ ] Prevention rule added to docs or scripts.
EOF
}

if [[ -n "$out_file" ]]; then
  mkdir -p "$(dirname "$out_file")"
  render_report > "$out_file"
  printf 'incident report written: %s\n' "$out_file"
else
  render_report
fi
