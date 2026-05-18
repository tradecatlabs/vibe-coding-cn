#!/usr/bin/env bash
# Render a swarm prompt and optionally dispatch it to a tmux pane.
set -euo pipefail

usage() {
  cat <<'EOF'
swarm-dispatch: render and optionally send commander/worker/reviewer prompts

Usage:
  swarm-dispatch.sh --role ROLE --target TARGET [--session NAME] [--swarm-dir DIR] [--task TEXT] [--out FILE] [--send] [--dry-run]

Roles:
  commander
  worker
  reviewer

Examples:
  swarm-dispatch.sh --role worker --target ai-hub:2.1 --task "只运行 make test" --out /tmp/worker.md
  swarm-dispatch.sh --role worker --target ai-hub:2.1 --task "只运行 make test" --send --dry-run
  swarm-dispatch.sh --role commander --target ai-hub:1.1 --task "拆分并推进 README 重构" --send
EOF
}

die() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
render="$script_dir/render-swarm-prompt.sh"
auto_tmux="$script_dir/auto-tmux.sh"

role=""
target=""
session="ai-hub"
swarm_dir="${AUTO_TMUX_SWARM_DIR:-/tmp/ai_swarm}"
task="未指定；请等待 commander 分配具体任务。"
out_file=""
send="0"
dry_run="0"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --role) role="${2:-}"; shift 2 ;;
    --target) target="${2:-}"; shift 2 ;;
    --session) session="${2:-}"; shift 2 ;;
    --swarm-dir) swarm_dir="${2:-}"; shift 2 ;;
    --task) task="${2:-}"; shift 2 ;;
    --out) out_file="${2:-}"; shift 2 ;;
    --send) send="1"; shift ;;
    --dry-run) dry_run="1"; shift ;;
    -h|--help) usage; exit 0 ;;
    *) die "unknown option: $1" ;;
  esac
done

[[ -n "$role" ]] || die "missing --role"
[[ -n "$target" ]] || die "missing --target"

case "$role" in
  commander|reviewer) ;;
  worker) ;;
  *) die "unknown role: $role" ;;
esac

prompt_file="$out_file"
if [[ -z "$prompt_file" ]]; then
  prompt_file="$(mktemp "/tmp/auto-tmux-${role}-prompt.XXXXXX.md")"
fi

render_args=("$role" --session "$session" --swarm-dir "$swarm_dir" --task "$task")
if [[ "$role" == "worker" ]]; then
  render_args+=(--target "$target")
fi

"$render" "${render_args[@]}" > "$prompt_file"
printf 'prompt written: %s\n' "$prompt_file"

if [[ "$send" != "1" ]]; then
  printf 'send skipped; add --send to dispatch to %s\n' "$target"
  exit 0
fi

send_args=(-t "$target" --text "$(cat "$prompt_file")" --enter)
if [[ "$dry_run" == "1" ]]; then
  send_args+=(--dry-run)
fi

"$auto_tmux" send "${send_args[@]}"
