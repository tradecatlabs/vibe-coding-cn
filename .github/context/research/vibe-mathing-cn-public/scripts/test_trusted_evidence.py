#!/usr/bin/env python3
# 做什么：证明不存在的证据文件和调用者自报摘要不能让 Result 进入解库。
# 怎么运行：python3 scripts/test_trusted_evidence.py
# 需要什么：Python 3；只读取研究空间校验器，不写业务记录。

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts" / "validate_research_spaces.py"


def load_validator() -> Any:
    spec = importlib.util.spec_from_file_location("validate_research_spaces", VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"无法加载校验器：{VALIDATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    validator = load_validator()
    attempts = {
        "attempt:forged": {
            "attempt_id": "attempt:forged",
            "problem_id": "problem:forged",
            "generator": "candidate-generator",
        }
    }
    forged_result = {
        "result_id": "result:forged",
        "problem_id": "problem:forged",
        "attempt_id": "attempt:forged",
        "kind": "proof",
        "outcome": "established",
        "evidence": [
            {
                "evidence_id": "evidence:forged-review",
                "capability": "human_review",
                "verdict": "accept",
                "verifier": "forged-reviewer",
                "independent": True,
                "locator": "research/artifacts/does-not-exist-review.txt",
                "sha256": "0" * 64,
                "invalidates": [],
            },
            {
                "evidence_id": "evidence:forged-faithfulness",
                "capability": "statement_faithfulness",
                "verdict": "accept",
                "verifier": "forged-reviewer",
                "independent": True,
                "locator": "research/artifacts/does-not-exist-faithfulness.txt",
                "sha256": "1" * 64,
                "invalidates": [],
            },
        ],
    }

    assert not validator.qualifies_as_solution(forged_result, attempts), (
        "安全缺陷：不存在 artifact、伪摘要和自报 independent 仍可让 Result 晋升解库"
    )
    print("可信证据回归测试通过：伪证据未进入解库。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
