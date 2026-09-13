#!/usr/bin/env python3
# 做什么：验证状态机非法转换、预算、超时、输出上限与 CLI 恢复语义。
# 怎么运行：python3 scripts/test_vibe_mathing_runtime.py
# 需要什么：Python 3；只写隔离临时目录。

from __future__ import annotations

import sys
import shutil
import tempfile
from pathlib import Path

from vibe_mathing.runtime import RuntimeErrorBase, cancel_run, create_run, execute_bounded, record_retry, transition


def expect_error(action: object, message: str) -> None:
    try:
        action()  # type: ignore[operator]
    except RuntimeErrorBase:
        return
    raise AssertionError(message)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="vibe-mathing-runtime-") as temporary:
        root = Path(temporary)
        schema = root / "research/schema/run-state.schema.json"
        schema.parent.mkdir(parents=True)
        shutil.copy2(
            Path(__file__).resolve().parents[1] / "research/schema/run-state.schema.json",
            schema,
        )
        state = create_run(root, "problem:test", "test-adapter", {"max_transitions": 2})
        expect_error(lambda: transition(root, state, "accepted"), "非法转换必须拒绝")
        state = transition(root, state, "routed")
        state = transition(root, state, "running")
        expect_error(lambda: transition(root, state, "candidate_ready"), "转换预算必须生效")
        state = record_retry(root, state, "第一次失败")
        state = record_retry(root, state, "第二次失败")
        expect_error(lambda: record_retry(root, state, "第三次失败"), "重试预算必须生效")
        cancelled = cancel_run(root, state["run_id"])
        assert cancelled["status"] == "cancelled"
        assert cancel_run(root, state["run_id"])["status"] == "cancelled"
        expect_error(
            lambda: execute_bounded(
                [sys.executable, "-c", "import time; time.sleep(2)"],
                cwd=root,
                timeout_seconds=1,
                max_output_bytes=100,
            ),
            "超时必须 fail-closed",
        )
        expect_error(
            lambda: execute_bounded(
                [sys.executable, "-c", "print('x' * 1000)"],
                cwd=root,
                timeout_seconds=2,
                max_output_bytes=100,
            ),
            "输出预算必须 fail-closed",
        )
        business_output = root / "business-output.bin"
        completed = execute_bounded(
            [
                sys.executable,
                "-c",
                "from pathlib import Path; Path('business-output.bin').write_bytes(b'x' * 4096)",
            ],
            cwd=root,
            timeout_seconds=2,
            max_output_bytes=100,
        )
        assert completed["exit_code"] == 0
        assert business_output.stat().st_size == 4096
    print("运行时测试通过：状态、转换、超时和输出预算均 fail-closed。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
