#!/usr/bin/env python3
# 做什么：用纯合成记录验证 ResearchBundle 的 solved/refuted/open/conflict 四象限与 CLI 契约。
# 怎么运行：python3 scripts/test_research_bundle.py
# 需要什么：Python 3；所有记录和证据只写隔离临时目录。

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

from vibe_mathing.bundle import derive_research_bundle
from vibe_mathing.evidence import create_evidence_receipt
from vibe_mathing.store import ResearchStore, StoreError


ROOT = Path(__file__).resolve().parents[1]
NOW = "2026-08-14T00:00:00Z"


def prepare(base: Path) -> None:
    for relative in (
        "problem-library/schema/canonical-problem.schema.json",
        "research/schema/attempt.schema.json",
        "research/schema/evidence-receipt.schema.json",
        "research/schema/research-bundle.schema.json",
        "research/schema/verifier-registry.schema.json",
        "result-library/schema/result.schema.json",
    ):
        target = base / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / relative, target)
    registry = json.loads((ROOT / "research/verifiers.json").read_text(encoding="utf-8"))
    registry["principals"].append(
        {
            "id": "synthetic-bundle-verifier",
            "role": "verifier",
            "trust_domain": "synthetic-bundle-verification",
            "policy": "test-fixture-v1",
            "capabilities": [
                "human_review",
                "counterexample_check",
                "statement_faithfulness",
            ],
        }
    )
    registry_path = base / "research/verifiers.json"
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    registry_path.write_text(json.dumps(registry), encoding="utf-8")


def problem(identifier: str) -> dict[str, Any]:
    return {
        "schema_version": "1.0.0",
        "problem_id": f"problem:{identifier}",
        "title": f"纯合成契约 {identifier}",
        "aliases": [],
        "statement": {"text": "判断合成谓词 Q 是否成立。", "language": "zh-CN", "version": 1},
        "domain": {"description": "不承载真实数学含义的合成域", "objects": ["synthetic object"]},
        "quantifiers": [{"kind": "decide", "variables": [], "domain": "synthetic domain"}],
        "definitions": [{"term": "Q", "definition": "测试专用未解释谓词"}],
        "assumptions": [],
        "allowed_axioms": [],
        "msc": [],
        "sources": [
            {
                "source": "synthetic test fixture",
                "source_record_id": None,
                "url": "https://example.com/synthetic-bundle-fixture",
                "retrieved_at": NOW,
            }
        ],
        "acceptance": {"policy": "solution-admission-v1"},
        "constraints": {
            "allowed_methods": ["proof", "computation"],
            "allowed_adapters": ["synthetic-bundle-v1"],
            "max_attempts": 2,
            "runtime": {
                "max_transitions": 16,
                "max_retries": 2,
                "timeout_seconds": 30,
                "max_output_bytes": 1_048_576,
                "memory_budget_mb": 256,
                "threads_max": 1,
            },
        },
        "lifecycle": "active",
        "created_at": NOW,
        "updated_at": NOW,
    }


def attempt(identifier: str, problem_id: str, method: str) -> dict[str, Any]:
    return {
        "attempt_id": f"attempt:{identifier}",
        "problem_id": problem_id,
        "generator": "candidate-generator",
        "objective": "构造测试专用候选",
        "method": method,
        "lifecycle": "completed",
        "started_at": NOW,
        "completed_at": NOW,
        "inputs": [problem_id],
        "claims": ["测试专用候选"],
        "artifacts": [],
    }


def result(
    identifier: str,
    problem_id: str,
    attempt_id: str,
    kind: str,
    outcome: str,
) -> dict[str, Any]:
    return {
        "result_id": f"result:{identifier}",
        "problem_id": problem_id,
        "attempt_id": attempt_id,
        "kind": kind,
        "claim": "测试专用原子声明",
        "scope": "synthetic domain",
        "outcome": outcome,
        "evidence": [],
        "created_at": NOW,
    }


def add_evidence(base: Path, record: dict[str, Any], capability: str) -> None:
    safe_capability = capability.replace("_", "-")
    evidence_id = f"evidence:{record['result_id'].removeprefix('result:')}.{safe_capability}"
    locator = f"research/artifacts/outputs/{record['result_id'].removeprefix('result:')}/{capability}.json"
    output = base / locator
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps({"capability": capability, "verdict": "accept"}),
        encoding="utf-8",
    )
    record["evidence"].append(
        create_evidence_receipt(
            project_root=base,
            result=record,
            generator="candidate-generator",
            evidence_id=evidence_id,
            capability=capability,
            verdict="accept",
            verifier="synthetic-bundle-verifier",
            checked_at=NOW,
            output_locator=locator,
            command=["synthetic-verifier", capability],
            timeout_seconds=30,
            resource_budget={"memory_budget_mb": 256, "threads_max": 1, "max_output_bytes": 1_048_576},
            stop_condition="合成能力检查完成",
            termination_status="completed",
            termination_reason="synthetic verifier returned",
            executor="in_process",
            notes="纯合成 ResearchBundle 测试回执",
        )
    )


def closing_result(
    base: Path,
    identifier: str,
    problem_id: str,
    attempt_id: str,
    kind: str,
) -> dict[str, Any]:
    outcome = "established" if kind == "proof" else "refuted"
    record = result(identifier, problem_id, attempt_id, kind, outcome)
    add_evidence(base, record, "human_review" if kind == "proof" else "counterexample_check")
    add_evidence(base, record, "statement_faithfulness")
    return record


def invoke(base: Path, problem_id: str, expected: int = 0) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/vibe_mathing_cli.py"),
            "--project-root",
            str(base),
            "export-bundle",
            "--problem-id",
            problem_id,
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert completed.returncode == expected, completed.stderr
    return completed


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="vibe-mathing-bundle-") as temporary:
        base = Path(temporary)
        prepare(base)
        store = ResearchStore(base)

        solved = problem("synthetic-solved")
        solved_attempt = attempt("synthetic-solved", solved["problem_id"], "proof")
        store.upsert("problems", solved)
        store.upsert("attempts", solved_attempt)
        store.upsert(
            "results",
            closing_result(
                base,
                "synthetic-solved",
                solved["problem_id"],
                solved_attempt["attempt_id"],
                "proof",
            ),
        )
        solved_bundle = json.loads(invoke(base, solved["problem_id"]).stdout)
        assert solved_bundle["disposition"] == "solved"
        assert solved_bundle["solution_view"] == ["result:synthetic-solved"]
        assert solved_bundle == derive_research_bundle(base, solved["problem_id"])
        assert invoke(base, solved["problem_id"]).stdout == invoke(base, solved["problem_id"]).stdout

        refuted = problem("synthetic-refuted")
        refuted_attempt = attempt("synthetic-refuted", refuted["problem_id"], "computation")
        store.upsert("problems", refuted)
        store.upsert("attempts", refuted_attempt)
        store.upsert(
            "results",
            closing_result(
                base,
                "synthetic-refuted",
                refuted["problem_id"],
                refuted_attempt["attempt_id"],
                "counterexample",
            ),
        )
        refuted_bundle = json.loads(invoke(base, refuted["problem_id"]).stdout)
        assert refuted_bundle["disposition"] == "refuted"
        assert refuted_bundle["solution_view"] == ["result:synthetic-refuted"]

        open_problem = problem("synthetic-open")
        store.upsert("problems", open_problem)
        open_bundle = json.loads(invoke(base, open_problem["problem_id"]).stdout)
        assert open_bundle["disposition"] == "open"
        assert open_bundle["solution_view"] == []
        assert open_bundle["unresolved_obligations"] == [
            {"code": "no_closing_candidate", "missing": [], "result_id": None}
        ]

        unknown = invoke(base, "problem:synthetic-missing", expected=2)
        assert "Problem 不存在" in unknown.stderr

        conflict = problem("synthetic-conflict")
        proof_attempt = attempt("synthetic-conflict-proof", conflict["problem_id"], "proof")
        counter_attempt = attempt("synthetic-conflict-counter", conflict["problem_id"], "computation")
        store.upsert("problems", conflict)
        store.upsert("attempts", proof_attempt)
        store.upsert("attempts", counter_attempt)
        proof = closing_result(
            base,
            "synthetic-conflict-proof",
            conflict["problem_id"],
            proof_attempt["attempt_id"],
            "proof",
        )
        counterexample = closing_result(
            base,
            "synthetic-conflict-counter",
            conflict["problem_id"],
            counter_attempt["attempt_id"],
            "counterexample",
        )
        store.upsert("results", proof)
        try:
            store.upsert("results", counterexample)
        except StoreError as exc:
            assert "同时存在通过准入" in str(exc)
        else:
            raise AssertionError("唯一 writer 必须拒绝 proof/counterexample 冲突")

        results_path = base / "result-library/records/results.jsonl"
        existing = store.read("results")
        results_path.write_text(
            "".join(
                json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n"
                for item in [*existing, counterexample]
            ),
            encoding="utf-8",
        )
        try:
            store.rebuild_solution_view()
        except StoreError as exc:
            assert "同时存在通过准入" in str(exc)
        else:
            raise AssertionError("Solution View 重建不得绕过冲突门")
        conflict_cli = invoke(base, conflict["problem_id"], expected=2)
        assert "同时存在通过准入" in conflict_cli.stderr

    print("ResearchBundle v1 测试通过：solved/refuted/open 稳定派生，未知问题和矛盾闭合均 fail-closed。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
