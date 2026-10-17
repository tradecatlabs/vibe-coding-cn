#!/usr/bin/env bash
# Audit auto-tmux package indexing consistency across scripts, references and gates.
set -euo pipefail

usage() {
  cat <<'EOF'
audit-package: check auto-tmux package indexing consistency

Usage:
  audit-package.sh

Checks:
  - 每个Extensions/auto-tmux/*.sh入口在Skill及本包README/AGENTS/validate-auto-tmux中登记
  - completion.bash is documented in the same package indexes
  - every references/*.md page is documented in SKILL.md and references/README.md
  - references/index.md remains a curated quick-link list; its local links are checked by the repository link checker
EOF
}

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
skill_dir="$(cd "$script_dir/../../skills/auto-tmux" && pwd)"
ref_dir="$skill_dir/references"

case "${1:-}" in
  -h|--help)
    usage
    exit 0
    ;;
  "")
    ;;
  *)
    printf 'error: unknown option: %s\n' "$1" >&2
    exit 1
    ;;
esac

failures=0

fail() {
  printf '[FAIL] %s\n' "$*" >&2
  failures=$((failures + 1))
}

pass() {
  printf '[OK] %s\n' "$*"
}

require_contains() {
  local file="$1"
  local pattern="$2"
  local label="$3"
  if grep -Fq "$pattern" "$file"; then
    pass "$label mentions $pattern"
  else
    fail "$label missing $pattern"
  fi
}

for script_path in "$script_dir"/*.sh; do
  script_name="$(basename "$script_path")"
  if [[ -x "$script_path" ]]; then
    pass "executable script: $script_name"
  else
    fail "script is not executable: $script_name"
  fi
  require_contains "$skill_dir/SKILL.md" ".github/extensions/auto-tmux/$script_name" "SKILL.md"
  require_contains "$script_dir/README.md" "$script_name" "scripts/README.md"
  require_contains "$script_dir/AGENTS.md" "$script_name" "scripts/AGENTS.md"
  require_contains "$script_dir/validate-auto-tmux.sh" "$script_name" "validate-auto-tmux.sh"
done

require_contains "$skill_dir/SKILL.md" ".github/extensions/auto-tmux/completion.bash" "SKILL.md"
require_contains "$script_dir/README.md" "completion.bash" "scripts/README.md"
require_contains "$script_dir/AGENTS.md" "completion.bash" "scripts/AGENTS.md"
require_contains "$script_dir/validate-auto-tmux.sh" "completion.bash" "validate-auto-tmux.sh"

for ref_path in "$ref_dir"/*.md; do
  ref_name="$(basename "$ref_path")"
  case "$ref_name" in
    AGENTS.md|README.md)
      continue
      ;;
    index.md)
      require_contains "$skill_dir/SKILL.md" "references/$ref_name" "SKILL.md"
      require_contains "$ref_dir/README.md" "$ref_name" "references/README.md"
      continue
      ;;
  esac
  require_contains "$skill_dir/SKILL.md" "references/$ref_name" "SKILL.md"
  require_contains "$ref_dir/README.md" "$ref_name" "references/README.md"
done

if (( failures > 0 )); then
  printf 'auto-tmux package audit failed: %s issue(s)\n' "$failures" >&2
  exit 1
fi

printf 'auto-tmux package audit ok\n'
