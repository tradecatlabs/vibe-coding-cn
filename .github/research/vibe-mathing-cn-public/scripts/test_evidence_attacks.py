#!/usr/bin/env python3
# 做什么：攻击可信证据入口，覆盖伪 hash、路径逃逸、symlink、自验证和 registry 越权。
# 怎么运行：python3 scripts/test_evidence_attacks.py
# 需要什么：Python 3；只写隔离临时目录。

from __future__ import annotations

import json
import os
import shutil
import tempfile
from pathlib import Path

from vibe_mathing.evidence import (
    EvidenceError,
    create_evidence_receipt,
    sha256_file,
    verify_evidence_receipt,
)


ROOT = Path(__file__).resolve().parents[1]
NOW = "2026-08-13T00:00:00Z"


def expect_rejection(action: object, label: str) -> None:
    try:
        action()  # type: ignore[operator]
    except EvidenceError:
        return
    raise AssertionError(f"攻击未被拒绝：{label}")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="vibe-mathing-evidence-attacks-") as temporary:
        root = Path(temporary)
        registry = root / "research/verifiers.json"
        registry.parent.mkdir(parents=True)
        shutil.copy2(ROOT / "research/verifiers.json", registry)
        schema_root = root / "research/schema"
        schema_root.mkdir(parents=True)
        for name in ("verifier-registry.schema.json", "evidence-receipt.schema.json"):
            shutil.copy2(ROOT / "research/schema" / name, schema_root / name)
        output = root / "research/artifacts/outputs/test/check.txt"
        output.parent.mkdir(parents=True)
        output.write_text(
            json.dumps({"x": "1/2", "x_squared": "1/4", "x_squared_lt_x": True}),
            encoding="utf-8",
        )
        result = {
            "result_id": "result:attack-test",
            "problem_id": "problem:attack-test",
            "attempt_id": "attempt:attack-test",
        }
        receipt = create_evidence_receipt(
            project_root=root,
            result=result,
            generator="sympy-generator",
            evidence_id="evidence:attack-test",
            capability="counterexample_check",
            verdict="accept",
            verifier="sympy-counterexample-verifier",
            checked_at=NOW,
            output_locator="research/artifacts/outputs/test/check.txt",
            command=["sympy", "verify"],
            timeout_seconds=30,
            resource_budget={"memory_budget_mb": 256, "threads_max": 1, "max_output_bytes": 1_048_576},
            stop_condition="攻击 fixture 的精确检查完成",
            termination_status="completed",
            termination_reason="attack fixture verifier returned",
            executor="in_process",
            notes="attack fixture",
        )
        assert verify_evidence_receipt(
            project_root=root, result=result, evidence=receipt, generator="sympy-generator"
        ) == "counterexample_check"
        receipt_path = root / receipt["locator"]
        original_receipt = receipt_path.read_bytes()
        mutated_receipt = json.loads(original_receipt.decode("utf-8"))
        mutated_receipt["verdict"] = "reject"
        receipt_path.write_text(
            json.dumps(mutated_receipt, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
        mismatch = {**receipt, "sha256": sha256_file(receipt_path)}
        expect_rejection(
            lambda: verify_evidence_receipt(
                project_root=root, result=result, evidence=mismatch, generator="sympy-generator"
            ),
            "回执 verdict 篡改",
        )
        receipt_path.write_bytes(original_receipt)
        changed_output = root / "research/artifacts/outputs/test/changed.txt"
        changed_output.write_text(
            json.dumps({"x": "1/2", "x_squared": "1/4", "x_squared_lt_x": True}),
            encoding="utf-8",
        )
        expect_rejection(
            lambda: create_evidence_receipt(
                project_root=root,
                result=result,
                generator="sympy-generator",
                evidence_id="evidence:attack-test",
                capability="counterexample_check",
                verdict="accept",
                verifier="sympy-counterexample-verifier",
                checked_at=NOW,
                output_locator="research/artifacts/outputs/test/changed.txt",
                command=["sympy", "verify"],
                timeout_seconds=30,
                resource_budget={"memory_budget_mb": 256, "threads_max": 1, "max_output_bytes": 1_048_576},
                stop_condition="覆盖攻击检查完成",
                termination_status="completed",
                termination_reason="attack fixture verifier returned",
                executor="in_process",
                notes="禁止覆盖既有回执",
            ),
            "回执覆盖",
        )

        forged_hash = {**receipt, "sha256": "0" * 64}
        expect_rejection(
            lambda: verify_evidence_receipt(project_root=root, result=result, evidence=forged_hash, generator="sympy-generator"),
            "伪 hash",
        )
        escaped = {**receipt, "locator": "../outside.json"}
        expect_rejection(
            lambda: verify_evidence_receipt(project_root=root, result=result, evidence=escaped, generator="sympy-generator"),
            "路径逃逸",
        )
        symlink = root / "research/artifacts/symlink.json"
        symlink.symlink_to(root / receipt["locator"])
        linked = {**receipt, "locator": "research/artifacts/symlink.json"}
        expect_rejection(
            lambda: verify_evidence_receipt(project_root=root, result=result, evidence=linked, generator="sympy-generator"),
            "symlink",
        )
        self_review = {**receipt, "verifier": "sympy-generator", "independent": False}
        expect_rejection(
            lambda: verify_evidence_receipt(project_root=root, result=result, evidence=self_review, generator="sympy-generator"),
            "自验证",
        )
        unauthorized = {**receipt, "capability": "kernel_check"}
        expect_rejection(
            lambda: verify_evidence_receipt(project_root=root, result=result, evidence=unauthorized, generator="sympy-generator"),
            "未注册 capability",
        )
        output.write_text(json.dumps({"x": "0", "x_squared": "0", "x_squared_lt_x": False}), encoding="utf-8")
        expect_rejection(
            lambda: verify_evidence_receipt(project_root=root, result=result, evidence=receipt, generator="sympy-generator"),
            "底层输出篡改",
        )
        assert not os.path.exists(root / "outside.json")

    print("可信证据攻击矩阵通过：路径、摘要、symlink、主体与能力伪造均 fail-closed。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
