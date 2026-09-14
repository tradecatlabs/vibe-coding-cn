#!/usr/bin/env python3
# 做什么：回归验证数学能力探针的退出码、MiniSat 协议和 profile 聚合语义。
# 怎么运行：python3 scripts/test_check_math_tools.py
# 需要什么：Python 3 标准库；测试使用 mock，不要求安装外部数学工具。

from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path
from subprocess import CompletedProcess
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_math_tools  # noqa: E402


class MathToolCheckTests(unittest.TestCase):
    def test_missing_command_is_explicit(self) -> None:
        with patch.object(check_math_tools.shutil, "which", return_value=None):
            result = check_math_tools.check_command("test", "missing", [])
        self.assertEqual(result.status, "missing")
        self.assertTrue(result.required)

    def test_command_accepts_tool_specific_exit_code(self) -> None:
        completed = CompletedProcess(["solver"], 10, "SAT\n", "")
        with patch.object(check_math_tools.shutil, "which", return_value="/usr/bin/solver"):
            with patch.object(check_math_tools, "run_process", return_value=completed):
                result = check_math_tools.check_command(
                    "sat", "solver", [], accepted_codes=(10,), expected="SAT"
                )
        self.assertEqual(result.status, "ready")

    def test_portable_profile_uses_declared_core_dependencies(self) -> None:
        self.assertEqual(check_math_tools.PROFILE_KEYS["portable"], ["project-python-portable"])

    def test_millennium_profile_deduplicates_shared_runtimes(self) -> None:
        keys = check_math_tools.PROFILE_KEYS["millennium"]
        self.assertEqual(len(keys), len(set(keys)))
        self.assertIn("project-python-core", keys)
        self.assertIn("project-python-graph", keys)
        self.assertIn("project-python-smt", keys)
        self.assertIn("system-python-pde", keys)
        self.assertIn("lean", keys)

    def test_python_failure_preserves_error(self) -> None:
        completed = CompletedProcess(["python"], 1, "", "ImportError: bad")
        with patch.object(check_math_tools, "run_process", return_value=completed):
            result = check_math_tools.check_python(
                "test", Path(sys.executable), ["missing"], "assert True"
            )
        self.assertEqual(result.status, "error")
        self.assertIn("ImportError", result.detail)

    def test_runtime_label_does_not_expose_executable_path(self) -> None:
        completed = CompletedProcess(["tool"], 0, "PASS\n", "")
        with patch.object(check_math_tools.shutil, "which", return_value="/private/tool"):
            with patch.object(check_math_tools, "run_process", return_value=completed):
                result = check_math_tools.check_command(
                    "test", "/private/tool", [], runtime_label="stable-tool"
                )
        self.assertEqual(result.status, "ready")
        self.assertEqual(result.runtime, "stable-tool")

    def test_command_override_is_explicit(self) -> None:
        with patch.dict(os.environ, {"MATH_TOOLS_SAGE": "/opt/sage"}):
            self.assertEqual(
                check_math_tools.configured_command("MATH_TOOLS_SAGE", "sage"),
                "/opt/sage",
            )

    def test_current_dolfinx_api_is_used(self) -> None:
        source = Path(check_math_tools.__file__).read_text(encoding="utf-8")
        self.assertIn("dolfinx.mesh.create_unit_square", source)
        self.assertNotIn("dolfinx.mesh.UnitSquareMesh", source)


if __name__ == "__main__":
    unittest.main()
