#!/usr/bin/env bash
# 做什么：运行 Web3 靶场全套测试与校验（候选表、证据账本、Foundry 攻击测试）。
# 怎么运行：bash web3-lab/verify_tests.sh；失败时以非零退出。
# 需要什么：PATH 含 forge 与项目 venv（脚本会自动补齐）。
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PATH="$HOME/.foundry/bin:$PROJECT_ROOT/.venv-web3/bin:$PATH"

python3 "$PROJECT_ROOT/governance/tasks/0004-web3-vertical-proof/validate_web3_candidates.py"
python3 "$PROJECT_ROOT/web3-lab/validate_lab_evidence.py"
cd "$PROJECT_ROOT/web3-lab"
forge test

echo "VERIFY_TESTS: PASS"
