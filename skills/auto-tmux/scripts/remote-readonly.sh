#!/usr/bin/env bash
# remote-readonly: collect read-only tmux evidence over SSH.
set -euo pipefail

usage() {
  cat <<'EOF'
remote-readonly: collect read-only tmux topology/capture evidence over SSH

Usage:
  remote-readonly.sh --host HOST [--session NAME] [--out DIR] [-n LINES] [--dry-run]

Defaults:
  --out /tmp/auto-tmux-remote-YYYYmmdd-HHMMSS
  -n    80 capture lines per pane

This script is read-only. It runs tmux list/capture commands on the remote host.
It never sends keys and never mutates remote tmux state.
Outputs:
  - remote-tmux.txt: redacted tmux topology and pane output
  - metadata.jsonl: machine-readable evidence metadata
  - index.md: human-readable evidence index
EOF
}

die() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

host=""
session=""
out_dir="/tmp/auto-tmux-remote-$(date +%Y%m%d-%H%M%S)"
lines=80
dry_run="0"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --host)
      host="${2:-}"
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
    -n|--lines)
      lines="${2:-}"
      shift 2
      ;;
    --dry-run)
      dry_run="1"
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

[[ -n "$host" ]] || die "missing --host"
[[ "$lines" =~ ^[0-9]+$ ]] || die "--lines must be a number"

redact() {
  sed -E \
    -e 's/(OPENAI_API_KEY|ANTHROPIC_API_KEY|GITHUB_TOKEN|GH_TOKEN|API_KEY|TOKEN|PASSWORD|SECRET)=([^[:space:]]+)/\1=<redacted>/g' \
    -e 's/(Bearer[[:space:]]+)[A-Za-z0-9._~+\/=-]+/\1<redacted>/g' \
    -e 's/(sk-[A-Za-z0-9_-]{12,})/<redacted-openai-key>/g'
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

remote_script='
set -e
session_filter="$1"
lines="$2"
if ! command -v tmux >/dev/null 2>&1; then
  echo "tmux not found" >&2
  exit 2
fi
if [ -n "$session_filter" ]; then
  tmux has-session -t "$session_filter"
  tmux list-windows -t "$session_filter" -F "window #S:#{window_index}: #{window_name} #{window_flags}"
  tmux list-panes -t "$session_filter" -F "#S:#{window_index}.#{pane_index}" |
    while read -r pane; do
      echo "===== [$pane] ====="
      tmux capture-pane -t "$pane" -p -S "-$lines"
    done
else
  tmux list-sessions -F "session: #{session_name} windows=#{session_windows} attached=#{session_attached}"
  tmux list-panes -a -F "#S:#{window_index}.#{pane_index}" |
    while read -r pane; do
      echo "===== [$pane] ====="
      tmux capture-pane -t "$pane" -p -S "-$lines"
    done
fi
'

if [[ "$dry_run" == "1" ]]; then
  printf 'ssh %q %q -- %q %q\n' "$host" "bash -s" "$session" "$lines"
  exit 0
fi

mkdir -p "$out_dir"
created_at="$(date -Is)"
ssh "$host" "bash -s" -- "$session" "$lines" <<EOF | redact > "$out_dir/remote-tmux.txt"
$remote_script
EOF

evidence_file="$out_dir/remote-tmux.txt"
evidence_bytes="$(wc -c < "$evidence_file" | tr -d '[:space:]')"
evidence_lines="$(wc -l < "$evidence_file" | tr -d '[:space:]')"
if command -v sha256sum >/dev/null 2>&1; then
  evidence_sha256="$(sha256sum "$evidence_file" | awk '{print $1}')"
else
  evidence_sha256=""
fi

cat > "$out_dir/metadata.jsonl" <<EOF
{"type":"remote-readonly","created_at":"$(json_escape "$created_at")","host":"$(json_escape "$host")","session":"$(json_escape "${session:-<all>}")","lines":$lines,"evidence_file":"remote-tmux.txt","evidence_bytes":$evidence_bytes,"evidence_lines":$evidence_lines,"evidence_sha256":"$(json_escape "$evidence_sha256")","read_only":true,"redacted":true}
EOF

cat > "$out_dir/index.md" <<EOF
# auto-tmux Remote Readonly

- created_at: \`$created_at\`
- host: \`$host\`
- session: \`${session:-<all>}\`
- lines: \`$lines\`
- evidence: [remote-tmux.txt](./remote-tmux.txt)
- metadata: [metadata.jsonl](./metadata.jsonl)
EOF

printf 'remote readonly evidence written: %s\n' "$out_dir"
