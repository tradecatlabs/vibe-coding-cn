#!/usr/bin/env python3
# 做什么：用真实证据回执和攻击性反例验证二维状态与完整解派生规则。
# 怎么运行：python3 scripts/test_research_spaces.py
# 需要什么：Python 3；所有产物写入隔离临时目录，不读写业务记录。

from __future__ import annotations

import importlib.util
import json
import tempfile
from pathlib import Path
from typing import Any

from vibe_mathing.evidence import create_evidence_receipt


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts" / "validate_research_spaces.py"
CHECKED_AT = "2026-08-13T00:00:00Z"


def load_validator() -> Any:
    spec = importlib.util.spec_from_file_location("validate_research_spaces", VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"无法加载校验器：{VALIDATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def prepare_project_root(base: Path) -> None:
    registry = json.loads((ROOT / "research" / "verifiers.json").read_text(encoding="utf-8"))
    registry["principals"].append(
        {
            "id": "independent-test-verifier",
            "role": "verifier",
            "trust_domain": "test-verification",
            "policy": "test-fixture-v1",
            "capabilities": [
                "human_review",
                "kernel_check",
                "axiom_escape_audit",
                "counterexample_check",
                "statement_faithfulness",
                "numeric_check",
            ],
        }
    )
    registry_path = base / "research" / "verifiers.json"
    registry_path.parent.mkdir(parents=True)
    registry_path.write_text(json.dumps(registry), encoding="utf-8")
    schema_root = base / "research/schema"
    schema_root.mkdir(parents=True, exist_ok=True)
    for name in ("verifier-registry.schema.json", "evidence-receipt.schema.json"):
        (schema_root / name).write_text(
            (ROOT / "research/schema" / name).read_text(encoding="utf-8"),
            encoding="utf-8",
        )


def result_record(
    *, result_id: str, kind: str, outcome: str
) -> dict[str, Any]:
    return {
        "result_id": result_id,
        "problem_id": "problem:test",
        "attempt_id": "attempt:test",
        "kind": kind,
        "claim": "测试声明",
        "scope": "测试定义域",
        "outcome": outcome,
        "evidence": [],
        "created_at": CHECKED_AT,
    }


def add_evidence(
    validator: Any,
    project_root: Path,
    result: dict[str, Any],
    evidence_id: str,
    capability: str,
    *,
    verdict: str = "accept",
    invalidates: list[str] | None = None,
) -> dict[str, Any]:
    output_locator = (
        f"research/artifacts/outputs/{result['result_id'].removeprefix('result:')}/"
        f"{evidence_id.removeprefix('evidence:')}.txt"
    )
    output_path = project_root / output_locator
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_payload: dict[str, Any] = {"capability": capability, "verdict": verdict}
    if invalidates:
        output_payload["invalidates"] = invalidates
    output_path.write_text(json.dumps(output_payload), encoding="utf-8")
    item = create_evidence_receipt(
        project_root=project_root,
        result=result,
        generator="candidate-generator",
        evidence_id=evidence_id,
        capability=capability,
        verdict=verdict,
        verifier="independent-test-verifier",
        checked_at=CHECKED_AT,
        output_locator=output_locator,
        command=["test-verifier", capability],
        timeout_seconds=30,
        resource_budget={"memory_budget_mb": 256, "threads_max": 1, "max_output_bytes": 1_048_576},
        stop_condition="测试 verifier 完成单个能力检查",
        termination_status="completed",
        termination_reason="test verifier returned",
        executor="in_process",
        notes="真实回执晋升规则测试",
        invalidates=invalidates,
    )
    result["evidence"].append(item)
    return item


def main() -> int:
    validator = load_validator()
    attempts_by_id = {
        "attempt:test": {
            "attempt_id": "attempt:test",
            "problem_id": "problem:test",
            "generator": "candidate-generator",
        }
    }
    with tempfile.TemporaryDirectory(prefix="vibe-mathing-research-test-") as temporary:
        project_root = Path(temporary)
        prepare_project_root(project_root)

        valid_proof = result_record(
            result_id="result:valid-proof", kind="proof", outcome="established"
        )
        add_evidence(validator, project_root, valid_proof, "evidence:valid-proof-review", "human_review")
        add_evidence(validator, project_root, valid_proof, "evidence:valid-proof-faithfulness", "statement_faithfulness")
        valid_proof["evidence"].append(
            {
                "evidence_id": "evidence:forged-invalidation",
                "capability": "human_review",
                "verdict": "reject",
                "verifier": "independent-test-verifier",
                "independent": True,
                "locator": "research/artifacts/does-not-exist.json",
                "sha256": "0" * 64,
                "checked_at": CHECKED_AT,
                "invalidates": ["evidence:valid-proof-review"],
                "notes": "伪造的失效记录不得拥有撤销权",
            }
        )

        valid_counterexample = result_record(
            result_id="result:valid-counterexample", kind="counterexample", outcome="refuted"
        )
        add_evidence(validator, project_root, valid_counterexample, "evidence:valid-counterexample-check", "counterexample_check")
        add_evidence(validator, project_root, valid_counterexample, "evidence:valid-counterexample-faithfulness", "statement_faithfulness")

        valid_kernel_proof = result_record(
            result_id="result:valid-kernel-proof", kind="proof", outcome="established"
        )
        add_evidence(validator, project_root, valid_kernel_proof, "evidence:valid-kernel-proof-check", "kernel_check")
        add_evidence(validator, project_root, valid_kernel_proof, "evidence:valid-kernel-proof-axioms", "axiom_escape_audit")
        add_evidence(validator, project_root, valid_kernel_proof, "evidence:valid-kernel-proof-faithfulness", "statement_faithfulness")

        finite_evidence = result_record(
            result_id="result:finite-evidence", kind="numerical_evidence", outcome="supported"
        )
        add_evidence(validator, project_root, finite_evidence, "evidence:finite-numeric", "numeric_check")

        false_numeric_solution = result_record(
            result_id="result:false-numeric-solution", kind="numerical_evidence", outcome="established"
        )
        add_evidence(validator, project_root, false_numeric_solution, "evidence:false-numeric", "numeric_check")

        self_reviewed_proof = result_record(
            result_id="result:self-reviewed-proof", kind="proof", outcome="established"
        )
        self_review = add_evidence(validator, project_root, self_reviewed_proof, "evidence:self-review", "human_review")
        self_review["verifier"] = "candidate-generator"
        add_evidence(validator, project_root, self_reviewed_proof, "evidence:self-review-faithfulness", "statement_faithfulness")

        unfaithful_formalization = result_record(
            result_id="result:unfaithful-formalization", kind="proof", outcome="established"
        )
        add_evidence(validator, project_root, unfaithful_formalization, "evidence:unfaithful-kernel", "kernel_check")
        add_evidence(validator, project_root, unfaithful_formalization, "evidence:unfaithful-statement", "statement_faithfulness", verdict="reject")

        unaudited_formalization = result_record(
            result_id="result:unaudited-formalization", kind="proof", outcome="established"
        )
        add_evidence(validator, project_root, unaudited_formalization, "evidence:unaudited-kernel", "kernel_check")
        add_evidence(validator, project_root, unaudited_formalization, "evidence:unaudited-faithfulness", "statement_faithfulness")

        invalidated_proof = result_record(
            result_id="result:invalidated-proof", kind="proof", outcome="established"
        )
        add_evidence(validator, project_root, invalidated_proof, "evidence:invalidated-review", "human_review")
        add_evidence(validator, project_root, invalidated_proof, "evidence:invalidated-faithfulness", "statement_faithfulness")
        add_evidence(
            validator,
            project_root,
            invalidated_proof,
            "evidence:invalidation-review",
            "human_review",
            verdict="reject",
            invalidates=["evidence:invalidated-review"],
        )

        derived = validator.derive_solution_ids(
            [
                valid_proof,
                valid_counterexample,
                valid_kernel_proof,
                finite_evidence,
                false_numeric_solution,
                self_reviewed_proof,
                unfaithful_formalization,
                unaudited_formalization,
                invalidated_proof,
            ],
            attempts_by_id,
            project_root=project_root,
        )
        assert derived == [
            "result:valid-counterexample",
            "result:valid-kernel-proof",
            "result:valid-proof",
        ]
        assert validator.qualifies_as_solution(
            valid_proof, attempts_by_id, project_root=project_root
        ), "未通过受信校验的 invalidation 不得撤销真实证据"
        cross_capability = result_record(
            result_id="result:cross-capability-invalidation",
            kind="proof",
            outcome="established",
        )
        add_evidence(validator, project_root, cross_capability, "evidence:cross-review", "human_review")
        add_evidence(validator, project_root, cross_capability, "evidence:cross-faithfulness", "statement_faithfulness")
        add_evidence(
            validator,
            project_root,
            cross_capability,
            "evidence:cross-invalidates",
            "statement_faithfulness",
            verdict="reject",
            invalidates=["evidence:cross-review"],
        )
        ledger_errors: list[str] = []
        validator.validate_evidence_ledger(cross_capability, ledger_errors)
        assert any("只能撤销同 capability" in error for error in ledger_errors)

        errors: list[str] = []
        validator.validate_cross_references(
            [{"problem_id": "problem:test", "sources": []}],
            {"problem:test"},
            [
                {
                    "attempt_id": "attempt:test",
                    "problem_id": "problem:test",
                    "generator": "candidate-generator",
                    "lifecycle": "completed",
                    "completed_at": CHECKED_AT,
                }
            ],
            {"attempt:test"},
            [
                false_numeric_solution,
                self_reviewed_proof,
                unfaithful_formalization,
                unaudited_formalization,
                invalidated_proof,
            ],
            errors,
            project_root=project_root,
        )
        assert any("不能成为原问题的完整结论" in error for error in errors)
        assert sum("缺少独立直接验证" in error for error in errors) >= 4
        assert any("未注册 verifier" in error for error in errors)

    print("研究空间晋升规则回归测试通过：只有真实、独立、完整且未失效的证据进入解库。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
