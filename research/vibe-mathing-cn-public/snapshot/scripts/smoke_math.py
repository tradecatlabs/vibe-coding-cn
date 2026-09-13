#!/usr/bin/env python3
# 做什么：在有界 disposable worker 中验证精确符号计算与高精度数值后端。
# 怎么运行：python3 scripts/smoke_math.py
# 需要什么：Python 3、SymPy 1.14+、mpmath；失败时非零退出。

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from vibe_mathing.runtime import RuntimeErrorBase, execute_bounded


ROOT = Path(__file__).resolve().parents[1]


def _reject_json_constant(value: str) -> object:
    raise ValueError(f"invalid JSON constant: {value}")
WORKER = Path(__file__).with_name("smoke_math_worker.py")
TIMEOUT_SECONDS = 30
MAX_OUTPUT_BYTES = 1_048_576
MEMORY_BUDGET_MB = 512
THREADS_MAX = 1


def main() -> int:
    if (
        WORKER.is_symlink()
        or WORKER.resolve() != WORKER
        or not WORKER.is_file()
        or not os.access(WORKER, os.R_OK)
    ):
        print("ERROR: smoke worker path is invalid", file=sys.stderr)
        return 1
    environment = {
        key: value
        for key, value in os.environ.items()
        if key in {"PATH", "HOME", "LANG", "LC_ALL", "TMPDIR"}
    }
    environment["PATH"] = environment.get("PATH", "/usr/local/bin:/usr/bin:/bin")
    try:
        completed = execute_bounded(
            [sys.executable, str(WORKER)],
            cwd=ROOT,
            timeout_seconds=TIMEOUT_SECONDS,
            max_output_bytes=MAX_OUTPUT_BYTES,
            memory_budget_mb=MEMORY_BUDGET_MB,
            threads_max=THREADS_MAX,
            env=environment,
        )
    except RuntimeErrorBase as exc:
        print(f"ERROR: bounded smoke worker failed: {exc}", file=sys.stderr)
        return 1
    if (
        not isinstance(completed, dict)
        or completed.get("exit_code") != 0
        or not isinstance(completed.get("stdout"), str)
        or not isinstance(completed.get("stderr"), str)
    ):
        detail = completed.get("stderr", "") if isinstance(completed, dict) else "worker returned malformed result"
        if not isinstance(detail, str):
            detail = "worker returned malformed result"
        detail = detail.strip() or "worker returned non-zero"
        print(f"ERROR: bounded smoke worker failed: {detail[:240]}", file=sys.stderr)
        return 1
    try:
        payload = json.loads(
            completed["stdout"], parse_constant=_reject_json_constant
        )
    except (json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: bounded smoke worker returned invalid JSON: {exc}", file=sys.stderr)
        return 1
    if not isinstance(payload, dict) or payload.get("status") != "PASS":
        print("ERROR: bounded smoke worker returned an invalid result", file=sys.stderr)
        return 1
    print(json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
