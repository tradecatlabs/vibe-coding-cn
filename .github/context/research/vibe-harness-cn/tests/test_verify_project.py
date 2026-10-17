"""验证项目 gate runner 对架构扫描与回滚契约的真实行为。"""

from __future__ import annotations

import importlib.util
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]


def load_principle_scanner():
    path = ROOT / "governance/tools/scan_principle_gates.py"
    spec = importlib.util.spec_from_file_location("scan_principle_gates", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"无法加载原则扫描器：{path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ProjectGateRegressionTest(unittest.TestCase):
    def test_breaking_change_notice_is_not_compatibility_shim(self) -> None:
        scanner = load_principle_scanner()
        external_fact = (
            "Developer preview: there will be compatibility-breaking changes; "
            "当前 revision 可能发生破坏性兼容变更。"
        )
        self.assertEqual([], scanner.scan_future_optimal("upstream-lock.json", external_fact))
        self.assertTrue(
            scanner.scan_future_optimal(
                "implementation.md",
                "Keep a temporary compatibility shim for now.",
            )
        )

    def test_architecture_and_rollback_gates(self) -> None:
        for gate in ("architecture", "rollback"):
            with self.subTest(gate=gate):
                completed = subprocess.run(
                    [sys.executable, "scripts/verify_project.py", "--gate", gate],
                    cwd=ROOT,
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    check=False,
                )
                self.assertEqual(0, completed.returncode, completed.stdout)


if __name__ == "__main__":
    unittest.main()
