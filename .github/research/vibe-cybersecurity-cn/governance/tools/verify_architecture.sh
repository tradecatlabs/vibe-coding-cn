#!/usr/bin/env bash
# 做什么：运行治理包架构门禁（strict 校验 + 健康报告）。
# 怎么运行：bash governance/tools/verify_architecture.sh；失败时以非零退出。
# 需要什么：Python 3.10+ 标准库。
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$PROJECT_ROOT"

python3 governance/tools/validate_governance_package.py --project-root . --strict
python3 governance/tools/governance_health_report.py --project-root . --strict

echo "VERIFY_ARCHITECTURE: PASS"
