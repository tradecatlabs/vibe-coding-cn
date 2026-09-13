#!/usr/bin/env python3
# 做什么：验证 SymPy 命题 SAT/QF-LRA、精确 witness、真实回执和解库准入负例。
# 怎么运行：python3 scripts/test_smt_pipeline.py
# 需要什么：Python 3、SymPy 1.14、项目 evidence/Result validator；只写临时目录。

from __future__ import annotations

import json
import shutil
import tempfile
from pathlib import Path

from vibe_mathing.smt import BACKEND, verify_smt_fixture

import validate_research_spaces as validator


ROOT = Path(__file__).resolve().parents[1]
NOW = "2026-08-14T00:00:00Z"


def prepare(project_root: Path) -> None:
    (project_root / "research/schema").mkdir(parents=True)
    shutil.copy2(ROOT / "research/verifiers.json", project_root / "research/verifiers.json")
    for name in ("verifier-registry.schema.json", "evidence-receipt.schema.json"):
        shutil.copy2(
            ROOT / "research/schema" / name,
            project_root / "research/schema" / name,
        )


def make_result(result_id: str) -> dict:
    suffix = result_id.removeprefix("result:")
    return {
        "result_id": result_id,
        "problem_id": "problem:smt-lra-fixture",
        "attempt_id": f"attempt:{suffix}",
        "kind": "counterexample",
        "claim": "x=1/2 满足 0<=x<=1 且 x>0，因此原全称命题为假。",
        "scope": "QF-LRA + exact rational witness",
        "outcome": "refuted",
        "evidence": [],
        "created_at": NOW,
    }


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="vibe-mathing-smt-") as temporary:
        project_root = Path(temporary)
        prepare(project_root)
        result = make_result("result:smt-lra-fixture")
        result["evidence"] = verify_smt_fixture(
            project_root=project_root,
            fixture_root=ROOT / "fixtures/smt-lra",
            result=result,
        )
        attempts = {
            result["attempt_id"]: {
                "attempt_id": result["attempt_id"],
                "problem_id": result["problem_id"],
                "generator": "smt-generator",
            }
        }
        assert validator.qualifies_as_solution(
            result, attempts, project_root=project_root
        )
        assert {item["capability"] for item in result["evidence"]} == {
            "counterexample_check",
            "statement_faithfulness",
        }
        solver_evidence = next(
            item for item in result["evidence"] if item["capability"] == "counterexample_check"
        )
        receipt = json.loads(
            (project_root / solver_evidence["locator"]).read_text(encoding="utf-8")
        )
        output = json.loads(
            (project_root / receipt["output"]["locator"]).read_text(encoding="utf-8")
        )
        assert output["backend"] == BACKEND
        assert output["propositional_unsat"] is True
        assert output["qf_lra_contradiction_unsat"] is True
        assert output["exact_witness_ok"] is True
        assert output["verdict"] == "accept"

        without_faithfulness = {
            **result,
            "evidence": [
                item
                for item in result["evidence"]
                if item["capability"] != "statement_faithfulness"
            ],
        }
        assert not validator.qualifies_as_solution(
            without_faithfulness, attempts, project_root=project_root
        )
        output_path = project_root / receipt["output"]["locator"]
        output_path.write_text("{}\n", encoding="utf-8")
        assert not validator.qualifies_as_solution(
            result, attempts, project_root=project_root
        )

    print("SMT 垂直链测试通过：命题 SAT、QF-LRA、精确 witness 与回执攻击负例成立。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
