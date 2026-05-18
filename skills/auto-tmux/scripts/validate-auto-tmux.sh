#!/usr/bin/env bash
# Validate the auto-tmux skill package with script, docs and optional smoke gates.
set -euo pipefail

usage() {
  cat <<'EOF'
validate-auto-tmux: run auto-tmux package quality gates

Usage:
  validate-auto-tmux.sh [--no-smoke]

Checks:
  - required scripts exist and are executable
  - shell syntax is valid
  - help commands render without failure
  - SKILL.md and reference indexes mention the current script set
  - auto-skill strict validation passes
  - smoke test passes unless --no-smoke is used
EOF
}

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
skill_dir="$(cd "$script_dir/.." && pwd)"
repo_root="$(git -C "$skill_dir" rev-parse --show-toplevel 2>/dev/null || true)"
if [[ -z "$repo_root" ]]; then
  repo_root="$(cd "$skill_dir/../.." && pwd)"
fi

run_smoke="1"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --no-smoke) run_smoke="0"; shift ;;
    -h|--help) usage; exit 0 ;;
    *) printf 'error: unknown option: %s\n' "$1" >&2; exit 1 ;;
  esac
done

failures=0

pass() {
  printf '[OK] %s\n' "$*"
}

fail() {
  printf '[FAIL] %s\n' "$*" >&2
  failures=$((failures + 1))
}

require_executable() {
  local path="$1"
  if [[ -x "$path" ]]; then
    pass "executable: ${path#$repo_root/}"
  else
    fail "missing or not executable: ${path#$repo_root/}"
  fi
}

require_contains() {
  local file="$1"
  local pattern="$2"
  if grep -Fq "$pattern" "$file"; then
    pass "$(basename "$file") mentions $pattern"
  else
    fail "$(basename "$file") missing $pattern"
  fi
}

run_gate() {
  local name="$1"
  shift
  if "$@" >/tmp/auto-tmux-validate-gate.log 2>&1; then
    pass "$name"
  else
    fail "$name"
    sed -n '1,80p' /tmp/auto-tmux-validate-gate.log >&2
  fi
}

scripts=(
  "$script_dir/auto-tmux.sh"
  "$script_dir/swarm-state.sh"
  "$script_dir/swarm-brief.sh"
  "$script_dir/render-swarm-prompt.sh"
  "$script_dir/auto-tmux-smoke-test.sh"
)

for script in "${scripts[@]}"; do
  require_executable "$script"
  run_gate "bash syntax: ${script##*/}" bash -n "$script"
done

run_gate "auto-tmux help" "$script_dir/auto-tmux.sh" help
run_gate "swarm-state help" "$script_dir/swarm-state.sh" help
run_gate "swarm-brief help" "$script_dir/swarm-brief.sh" --help
run_gate "render-swarm-prompt help" "$script_dir/render-swarm-prompt.sh" --help

require_contains "$skill_dir/SKILL.md" "scripts/validate-auto-tmux.sh"
require_contains "$skill_dir/SKILL.md" "scripts/swarm-brief.sh"
require_contains "$skill_dir/references/index.md" "automation.md"
require_contains "$skill_dir/references/README.md" "swarm-state.md"
require_contains "$script_dir/README.md" "validate-auto-tmux.sh"
require_contains "$script_dir/AGENTS.md" "validate-auto-tmux.sh"

if [[ -x "$repo_root/skills/auto-skill/scripts/validate-skill.sh" ]]; then
  run_gate "auto-skill strict validation" "$repo_root/skills/auto-skill/scripts/validate-skill.sh" "$skill_dir" --strict
else
  fail "auto-skill validator not found"
fi

if [[ "$run_smoke" == "1" ]]; then
  run_gate "auto-tmux smoke test" "$script_dir/auto-tmux-smoke-test.sh"
else
  pass "smoke test skipped by --no-smoke"
fi

rm -f /tmp/auto-tmux-validate-gate.log

if (( failures > 0 )); then
  printf 'auto-tmux validation failed: %s issue(s)\n' "$failures" >&2
  exit 1
fi

printf 'auto-tmux validation ok\n'
