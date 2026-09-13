#!/usr/bin/env python3
# 做什么：运行真实 Lean/Mathlib fixture 并验证 kernel、axiom、faithfulness 三证据准入。
# 怎么运行：python3 scripts/test_lean_pipeline.py
# 需要什么：固定 elan/Lean/lake 与 Mathlib cache；只写隔离临时项目。

from __future__ import annotations

import json
import os
import shutil
import tempfile
from pathlib import Path

from vibe_mathing.lean import verify_lean_fixture

import validate_research_spaces as validator


ROOT = Path(__file__).resolve().parents[1]
NOW = "2026-08-13T00:00:00Z"


def main() -> int:
    original_path = os.environ.get("PATH", "")
    elan_bin = str(Path.home() / ".elan" / "bin")
    os.environ["PATH"] = os.pathsep.join(
        entry for entry in original_path.split(os.pathsep) if entry != elan_bin
    )
    with tempfile.TemporaryDirectory(prefix="vibe-mathing-lean-") as temporary:
        project_root = Path(temporary)
        registry = project_root / "research/verifiers.json"
        registry.parent.mkdir(parents=True)
        shutil.copy2(ROOT / "research/verifiers.json", registry)
        schema_root = project_root / "research/schema"
        schema_root.mkdir(parents=True)
        for name in ("verifier-registry.schema.json", "evidence-receipt.schema.json"):
            shutil.copy2(ROOT / "research/schema" / name, schema_root / name)
        result = {
            "result_id": "result:lean-fixture",
            "problem_id": "problem:lean-fixture",
            "attempt_id": "attempt:lean-fixture",
            "kind": "proof",
            "claim": "自然数中 2 + 2 = 4。",
            "scope": "Lean Nat",
            "outcome": "established",
            "evidence": [],
            "created_at": NOW,
        }
        result["evidence"] = verify_lean_fixture(
            project_root=project_root,
            fixture_root=ROOT / "fixtures/lean-proof",
            result=result,
        )
        attempts = {
            "attempt:lean-fixture": {
                "attempt_id": "attempt:lean-fixture",
                "problem_id": "problem:lean-fixture",
                "generator": "lean-generator",
            }
        }
        assert validator.qualifies_as_solution(
            result, attempts, project_root=project_root
        )
        without_axioms = {**result, "evidence": [item for item in result["evidence"] if item["capability"] != "axiom_escape_audit"]}
        assert not validator.qualifies_as_solution(
            without_axioms, attempts, project_root=project_root
        )
        without_faithfulness = {**result, "evidence": [item for item in result["evidence"] if item["capability"] != "statement_faithfulness"]}
        assert not validator.qualifies_as_solution(
            without_faithfulness, attempts, project_root=project_root
        )
        audit = next(
            item for item in result["evidence"] if item["capability"] == "axiom_escape_audit"
        )
        kernel = next(
            item for item in result["evidence"] if item["capability"] == "kernel_check"
        )
        kernel_receipt = json.loads(
            (project_root / kernel["locator"]).read_text(encoding="utf-8")
        )
        kernel_argv = kernel_receipt["command"]["argv"]
        assert kernel_argv[1:3] == ["-j1", "-o"]
        assert kernel_argv[-1] == "VibeMathingFixture.lean"
        assert audit["verdict"] == "accept"
        print(json.dumps({"result_id": result["result_id"], "capabilities": [item["capability"] for item in result["evidence"]]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
