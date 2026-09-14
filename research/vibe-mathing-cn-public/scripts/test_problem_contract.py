#!/usr/bin/env python3
# 做什么：验证 canonical ProblemContract v1 的完整字段、固定准入策略和可执行约束。
# 怎么运行：python3 scripts/test_problem_contract.py
# 需要什么：Python 3、jsonschema；只读取合成 fixture，不写业务记录。

from __future__ import annotations

import copy
import importlib.util
import json
import tempfile
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "problem-library/schema/canonical-problem.schema.json"
FIXTURE_PATH = ROOT / "fixtures/sympy-counterexample/problem.json"
TEMPLATE_PATH = ROOT / "problem-library/templates/problem-contract.template.json"
VALIDATOR_PATH = ROOT / "scripts/validate_research_spaces.py"


def rejected(validator: Draft202012Validator, record: dict[str, object]) -> bool:
    return bool(list(validator.iter_errors(record)))


def load_research_validator() -> Any:
    spec = importlib.util.spec_from_file_location(
        "validate_research_spaces", VALIDATOR_PATH
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"无法加载校验器：{VALIDATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def attempt(identifier: str, problem_id: str, method: str) -> dict[str, object]:
    return {
        "attempt_id": f"attempt:{identifier}",
        "problem_id": problem_id,
        "generator": "candidate-generator",
        "objective": "纯合成契约约束测试",
        "method": method,
        "lifecycle": "completed",
        "started_at": "2026-08-14T00:00:00Z",
        "completed_at": "2026-08-14T00:00:00Z",
        "inputs": [],
        "claims": [],
        "artifacts": [],
    }


def main() -> int:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    valid = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert not list(validator.iter_errors(valid)), "完整 ProblemContract fixture 必须通过"
    template = json.loads(TEMPLATE_PATH.read_text(encoding="utf-8"))
    assert not list(validator.iter_errors(template)), "ProblemContract draft template 必须通过 schema"
    assert template["problem_id"] == "problem:example-draft"
    assert template["lifecycle"] == "draft"

    for field in (
        "domain",
        "quantifiers",
        "definitions",
        "assumptions",
        "allowed_axioms",
        "acceptance",
        "constraints",
        "lifecycle",
    ):
        missing = copy.deepcopy(valid)
        del missing[field]
        assert rejected(validator, missing), f"缺少 {field} 必须拒绝"

    legacy = copy.deepcopy(valid)
    legacy["status"] = "open"
    assert rejected(validator, legacy), "canonical Problem 不得保留解题 status 双真相"

    weakened = copy.deepcopy(valid)
    weakened["acceptance"]["policy"] = "agent-self-report"
    assert rejected(validator, weakened), "调用者不得降低固定准入策略"

    invalid_budget = copy.deepcopy(valid)
    invalid_budget["constraints"]["runtime"]["timeout_seconds"] = 0
    assert rejected(validator, invalid_budget), "运行预算必须为正整数"

    invalid_adapter = copy.deepcopy(valid)
    invalid_adapter["constraints"]["allowed_adapters"] = ["../shell"]
    assert rejected(validator, invalid_adapter), "adapter ID 必须是稳定受限标识"

    manual_only = copy.deepcopy(valid)
    manual_only["constraints"]["allowed_adapters"] = []
    assert not list(validator.iter_errors(manual_only)), "纯人工研究可以不允许自动 adapter"

    missing_variable = copy.deepcopy(valid)
    missing_variable["quantifiers"][0]["variables"] = []
    assert rejected(validator, missing_variable), "全称量词必须冻结变量"

    research_validator = load_research_validator()
    active = copy.deepcopy(valid)
    active["problem_id"] = "problem:synthetic-contract-active"
    active["constraints"]["allowed_methods"] = ["computation"]
    active["constraints"]["max_attempts"] = 1
    draft = copy.deepcopy(active)
    draft["problem_id"] = "problem:synthetic-contract-draft"
    draft["lifecycle"] = "draft"
    attempts = [
        attempt("disallowed-method", active["problem_id"], "proof"),
        attempt("first", active["problem_id"], "computation"),
        attempt("over-budget", active["problem_id"], "computation"),
        attempt("draft", draft["problem_id"], "computation"),
    ]
    errors: list[str] = []
    with tempfile.TemporaryDirectory(prefix="vibe-mathing-contract-") as temporary:
        research_validator.validate_cross_references(
            [active, draft],
            {active["problem_id"], draft["problem_id"]},
            attempts,
            {item["attempt_id"] for item in attempts},
            [],
            errors,
            project_root=Path(temporary),
        )
    assert any("未被 ProblemContract 允许" in error for error in errors)
    assert any("超过 ProblemContract.max_attempts" in error for error in errors)
    assert any("draft ProblemContract" in error for error in errors)

    print("ProblemContract v1 测试通过：schema、生命周期、方法和 Attempt 预算全部 fail-closed。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
