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

test_remote_readonly_package() {
  local tmp_dir fake_bin out_dir
  tmp_dir="$(mktemp -d)"
  fake_bin="$tmp_dir/bin"
  out_dir="$tmp_dir/out"
  mkdir -p "$fake_bin"
  cat > "$fake_bin/ssh" <<'EOF'
#!/usr/bin/env bash
cat >/dev/null
printf 'session: ai-hub windows=1 attached=0\n'
printf '===== [ai-hub:0.0] =====\n'
printf 'OPENAI_API_KEY=sk-testsecret000000\n'
EOF
  chmod +x "$fake_bin/ssh"
  PATH="$fake_bin:$PATH" "$script_dir/remote-readonly.sh" --host example.com --session ai-hub --out "$out_dir" >/dev/null
  grep -Fq 'metadata.jsonl' "$out_dir/index.md"
  grep -Fq '"read_only":true' "$out_dir/metadata.jsonl"
  grep -Fq '<redacted-openai-key>' "$out_dir/remote-tmux.txt"
  rm -rf "$tmp_dir"
}

scripts=(
  "$script_dir/auto-tmux.sh"
  "$script_dir/swarm-state.sh"
  "$script_dir/swarm-brief.sh"
  "$script_dir/swarm-watch.sh"
  "$script_dir/swarm-archive.sh"
  "$script_dir/swarm-board.sh"
  "$script_dir/swarm-deps-graph.sh"
  "$script_dir/swarm-export.sh"
  "$script_dir/swarm-timeline.sh"
  "$script_dir/swarm-blockers.sh"
  "$script_dir/swarm-results.sh"
  "$script_dir/swarm-report-pack.sh"
  "$script_dir/swarm-assign.sh"
  "$script_dir/swarm-health.sh"
  "$script_dir/remote-readonly.sh"
  "$script_dir/record-summary.sh"
  "$script_dir/check-jsonl.sh"
  "$script_dir/review-checklist.sh"
  "$script_dir/safety-check.sh"
  "$script_dir/render-swarm-prompt.sh"
  "$script_dir/swarm-dispatch.sh"
  "$script_dir/auto-tmux-smoke-test.sh"
)

for script in "${scripts[@]}"; do
  require_executable "$script"
  run_gate "bash syntax: ${script##*/}" bash -n "$script"
done

[[ -f "$script_dir/completion.bash" ]] && pass "completion file: skills/auto-tmux/scripts/completion.bash" || fail "missing completion.bash"
run_gate "bash syntax: completion.bash" bash -n "$script_dir/completion.bash"

run_gate "auto-tmux help" "$script_dir/auto-tmux.sh" help
run_gate "swarm-state help" "$script_dir/swarm-state.sh" help
run_gate "swarm-brief help" "$script_dir/swarm-brief.sh" --help
run_gate "swarm-watch help" "$script_dir/swarm-watch.sh" --help
run_gate "swarm-archive help" "$script_dir/swarm-archive.sh" --help
run_gate "swarm-board help" "$script_dir/swarm-board.sh" --help
run_gate "swarm-deps-graph help" "$script_dir/swarm-deps-graph.sh" --help
run_gate "swarm-export help" "$script_dir/swarm-export.sh" --help
run_gate "swarm-timeline help" "$script_dir/swarm-timeline.sh" --help
run_gate "swarm-blockers help" "$script_dir/swarm-blockers.sh" --help
run_gate "swarm-results help" "$script_dir/swarm-results.sh" --help
run_gate "swarm-results jsonl" bash -c '
  tmp="$(mktemp -d)"
  mkdir -p "$tmp/swarm/results"
  printf "id\tstatus\towner\ttext\tresult\n" > "$tmp/swarm/tasks.tsv"
  printf "t1\tDONE\tai-hub:1.0\tRun tests\tpassed\n" >> "$tmp/swarm/tasks.tsv"
  printf "passed\n" > "$tmp/swarm/results/t1.txt"
  "$1" --dir "$tmp/swarm" --out "$tmp/results.md" --jsonl "$tmp/results.jsonl" >/dev/null
  grep -Fq "t1" "$tmp/results.md"
  grep -Fq "\"type\":\"swarm-result\"" "$tmp/results.jsonl"
  "$2" "$tmp/results.jsonl" --require-key type --require-key id --require-key status >/dev/null
  rm -rf "$tmp"
' _ "$script_dir/swarm-results.sh" "$script_dir/check-jsonl.sh"
run_gate "swarm-report-pack help" "$script_dir/swarm-report-pack.sh" --help
run_gate "swarm-report-pack attachment" bash -c '
  tmp="$(mktemp -d)"
  mkdir -p "$tmp/swarm" "$tmp/remote"
  printf "id\ttext\tstatus\towner\tupdated_at\tresult\n" > "$tmp/swarm/tasks.tsv"
  printf "remote evidence\n" > "$tmp/remote/remote-tmux.txt"
  "$1" --dir "$tmp/swarm" --out "$tmp/out" --attach "$tmp/remote" >/dev/null
  grep -Fq "attachments.md" "$tmp/out/index.md"
  grep -Fq "results.md" "$tmp/out/index.md"
  grep -Fq "results.jsonl" "$tmp/out/index.md"
  grep -Fq "review-checklist.md" "$tmp/out/index.md"
  grep -Fq "manifest.json" "$tmp/out/index.md"
  grep -Fq "\"type\": \"auto-tmux-swarm-report-pack\"" "$tmp/out/manifest.json"
  grep -Fq "\"attachments\"" "$tmp/out/manifest.json"
  grep -Fq "remote-tmux.txt" "$tmp/out/attachments/remote/remote-tmux.txt"
  "$1" --dir "$tmp/swarm" --out "$tmp/out-tar" --attach "$tmp/remote" --tar >/dev/null
  test -f "$tmp/out-tar.tar.gz"
  rm -rf "$tmp"
' _ "$script_dir/swarm-report-pack.sh"
run_gate "swarm-assign help" "$script_dir/swarm-assign.sh" --help
run_gate "swarm-health help" "$script_dir/swarm-health.sh" --help
run_gate "remote-readonly help" "$script_dir/remote-readonly.sh" --help
run_gate "remote-readonly dry-run" "$script_dir/remote-readonly.sh" --host example.com --dry-run
run_gate "remote-readonly package with fake ssh" test_remote_readonly_package
run_gate "record-summary help" "$script_dir/record-summary.sh" --help
run_gate "check-jsonl help" "$script_dir/check-jsonl.sh" --help
run_gate "check-jsonl required keys" bash -c '
  tmp="$(mktemp)"
  printf "{\"type\":\"swarm-result\",\"id\":\"t1\",\"status\":\"DONE\"}\n" > "$tmp"
  "$1" "$tmp" --require-key type --require-key id --require-key status >/dev/null
  rm -f "$tmp"
' _ "$script_dir/check-jsonl.sh"
run_gate "review-checklist help" "$script_dir/review-checklist.sh" --help
run_gate "safety-check help" "$script_dir/safety-check.sh" --help
run_gate "safety-check clean text" "$script_dir/safety-check.sh" --text "make test"
if "$script_dir/safety-check.sh" --text "rm -rf /tmp/example" >/tmp/auto-tmux-validate-gate.log 2>&1; then
  fail "safety-check should reject dangerous text"
else
  pass "safety-check rejects dangerous text"
fi
run_gate "render-swarm-prompt help" "$script_dir/render-swarm-prompt.sh" --help
run_gate "swarm-dispatch help" "$script_dir/swarm-dispatch.sh" --help

require_contains "$skill_dir/SKILL.md" "scripts/validate-auto-tmux.sh"
require_contains "$skill_dir/SKILL.md" "scripts/swarm-brief.sh"
require_contains "$skill_dir/SKILL.md" "scripts/swarm-watch.sh"
require_contains "$skill_dir/SKILL.md" "scripts/swarm-archive.sh"
require_contains "$skill_dir/SKILL.md" "scripts/swarm-board.sh"
require_contains "$skill_dir/SKILL.md" "scripts/swarm-deps-graph.sh"
require_contains "$skill_dir/SKILL.md" "scripts/swarm-export.sh"
require_contains "$skill_dir/SKILL.md" "scripts/swarm-timeline.sh"
require_contains "$skill_dir/SKILL.md" "scripts/swarm-blockers.sh"
require_contains "$skill_dir/SKILL.md" "scripts/swarm-results.sh"
require_contains "$skill_dir/SKILL.md" "scripts/swarm-report-pack.sh"
require_contains "$skill_dir/SKILL.md" "scripts/swarm-assign.sh"
require_contains "$skill_dir/SKILL.md" "scripts/swarm-health.sh"
require_contains "$skill_dir/SKILL.md" "scripts/remote-readonly.sh"
require_contains "$skill_dir/SKILL.md" "scripts/record-summary.sh"
require_contains "$skill_dir/SKILL.md" "scripts/check-jsonl.sh"
require_contains "$skill_dir/SKILL.md" "scripts/review-checklist.sh"
require_contains "$skill_dir/SKILL.md" "scripts/completion.bash"
require_contains "$skill_dir/SKILL.md" "scripts/safety-check.sh"
require_contains "$skill_dir/SKILL.md" "scripts/swarm-dispatch.sh"
require_contains "$skill_dir/references/index.md" "automation.md"
require_contains "$skill_dir/references/index.md" "safety-policy.md"
require_contains "$skill_dir/references/index.md" "session-safety.md"
require_contains "$skill_dir/references/index.md" "jsonl-schema.md"
require_contains "$skill_dir/references/README.md" "swarm-state.md"
require_contains "$skill_dir/references/README.md" "safety-policy.md"
require_contains "$skill_dir/references/README.md" "session-safety.md"
require_contains "$skill_dir/references/README.md" "jsonl-schema.md"
require_contains "$skill_dir/references/jsonl-schema.md" "swarm-result"
require_contains "$skill_dir/references/jsonl-schema.md" "remote-readonly"
require_contains "$skill_dir/references/session-safety.md" "remote-readonly.sh"
require_contains "$skill_dir/references/session-safety.md" "远程默认只读"
require_contains "$skill_dir/references/session-safety.md" "metadata.jsonl"
require_contains "$script_dir/README.md" "validate-auto-tmux.sh"
require_contains "$script_dir/README.md" "swarm-dispatch.sh"
require_contains "$script_dir/README.md" "swarm-watch.sh"
require_contains "$script_dir/README.md" "swarm-archive.sh"
require_contains "$script_dir/README.md" "swarm-board.sh"
require_contains "$script_dir/README.md" "swarm-deps-graph.sh"
require_contains "$script_dir/README.md" "swarm-export.sh"
require_contains "$script_dir/README.md" "swarm-timeline.sh"
require_contains "$script_dir/README.md" "swarm-blockers.sh"
require_contains "$script_dir/README.md" "swarm-results.sh"
require_contains "$script_dir/README.md" "swarm-report-pack.sh"
require_contains "$script_dir/README.md" "swarm-assign.sh"
require_contains "$script_dir/README.md" "swarm-health.sh"
require_contains "$script_dir/README.md" "remote-readonly.sh"
require_contains "$script_dir/README.md" "metadata.jsonl"
require_contains "$script_dir/README.md" "record-summary.sh"
require_contains "$script_dir/README.md" "check-jsonl.sh"
require_contains "$script_dir/README.md" "review-checklist.sh"
require_contains "$script_dir/README.md" "completion.bash"
require_contains "$script_dir/README.md" "safety-check.sh"
require_contains "$script_dir/AGENTS.md" "validate-auto-tmux.sh"
require_contains "$script_dir/AGENTS.md" "swarm-dispatch.sh"
require_contains "$script_dir/AGENTS.md" "swarm-watch.sh"
require_contains "$script_dir/AGENTS.md" "swarm-archive.sh"
require_contains "$script_dir/AGENTS.md" "swarm-board.sh"
require_contains "$script_dir/AGENTS.md" "swarm-deps-graph.sh"
require_contains "$script_dir/AGENTS.md" "swarm-export.sh"
require_contains "$script_dir/AGENTS.md" "swarm-timeline.sh"
require_contains "$script_dir/AGENTS.md" "swarm-blockers.sh"
require_contains "$script_dir/AGENTS.md" "swarm-results.sh"
require_contains "$script_dir/AGENTS.md" "swarm-report-pack.sh"
require_contains "$script_dir/AGENTS.md" "swarm-assign.sh"
require_contains "$script_dir/AGENTS.md" "swarm-health.sh"
require_contains "$script_dir/AGENTS.md" "remote-readonly.sh"
require_contains "$script_dir/AGENTS.md" "record-summary.sh"
require_contains "$script_dir/AGENTS.md" "check-jsonl.sh"
require_contains "$script_dir/AGENTS.md" "review-checklist.sh"
require_contains "$script_dir/AGENTS.md" "completion.bash"
require_contains "$script_dir/AGENTS.md" "safety-check.sh"

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
