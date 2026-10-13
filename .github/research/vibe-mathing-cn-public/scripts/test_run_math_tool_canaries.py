#!/usr/bin/env python3
# 做什么：回归验证数学工具 canary 的选择、超时分类和输出边界。
# 怎么运行：python3 scripts/test_run_math_tool_canaries.py
# 需要什么：Python 3 标准库；不启动外部数学工具，不访问网络。

from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_math_tool_canaries as canaries  # noqa: E402


class MathToolCanaryTests(unittest.TestCase):
    def test_tool_selection_is_deduplicated_and_ordered(self) -> None:
        self.assertEqual(canaries.parse_tool_ids("t15,T13,t15"), ["T15", "T13"])
        with self.assertRaises(ValueError):
            canaries.parse_tool_ids("T99")

    def test_expected_timeout_is_pass_only_after_timeout(self) -> None:
        timed_out = canaries.run_python(
            "T15",
            "bounded subprocess",
            "timeout",
            sys.executable,
            "while True: pass",
            "timeout",
            timeout=0.05,
        )
        self.assertEqual(timed_out.status, "PASS")
        self.assertEqual(timed_out.kind, "timeout")

    def test_expected_success_requires_marker(self) -> None:
        completed = {"exit_code": 0, "stdout": "no marker\n", "stderr": ""}
        with patch.object(canaries, "resolve_executable", return_value=sys.executable):
            with patch.object(canaries, "run_bounded", return_value=completed):
                checked = canaries.run_python(
                    "T13", "fixture", "positive", sys.executable, "pass", "success"
                )
        self.assertEqual(checked.status, "FAIL")

    def test_detail_does_not_include_command_paths(self) -> None:
        text = Path(canaries.__file__).read_text(encoding="utf-8")
        self.assertNotIn("print(completed.stdout", text)
        self.assertIn("detail[:160]", text)


if __name__ == "__main__":
    unittest.main()
