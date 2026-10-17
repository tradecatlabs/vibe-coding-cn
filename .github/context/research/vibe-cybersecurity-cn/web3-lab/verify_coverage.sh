#!/usr/bin/env bash
# 做什么：生成 Web3 靶场 Foundry 覆盖率摘要。
# 怎么运行：bash web3-lab/verify_coverage.sh；失败时以非零退出。
# 需要什么：PATH 含 forge（脚本会自动补齐）。
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PATH="$HOME/.foundry/bin:$PATH"

cd "$PROJECT_ROOT/web3-lab"
forge coverage --report summary

echo "VERIFY_COVERAGE: PASS"
