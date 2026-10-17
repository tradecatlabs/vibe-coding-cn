#!/usr/bin/env -S uv run --script
# 做什么：校验 Harness manifest、Operator Pack、参考库 Profile 与 Operator Runtime Core。
# 怎么运行：用 --self-test，传 manifest，或使用 --operator-pack/--operator-library/--operator-runtime。
# 需要什么：Python 3.11+、uv，以及同目录由 uv 生成的脚本锁文件。
# /// script
# requires-python = ">=3.11"
# dependencies = ["jsonschema==4.25.1"]
# ///

from __future__ import annotations

import argparse
import copy
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError

from validate_operator_library import (
    LibraryDocuments,
    LibraryValidationResult,
    catalog_path_issues,
    validate_operator_library,
    validate_operator_library_documents,
    validate_operator_pack_document,
)


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCHEMA = ROOT / "contracts" / "harness-manifest.schema.json"
VALID_EXAMPLE = ROOT / "contracts" / "examples" / "minimal-coding-harness.json"
INVALID_EXAMPLE = ROOT / "tests" / "fixtures" / "invalid-missing-stop-condition.json"
DEFAULT_OPERATOR_LIBRARY = ROOT / "operators" / "catalog.json"
DEFAULT_OPERATOR_SCHEMA = ROOT / "contracts" / "problem-solving-operator-pack.schema.json"
VALID_OPERATOR_PACK = ROOT / "contracts" / "examples" / "minimal-operator-pack.json"
DEFAULT_OPERATOR_RUNTIME_SCHEMA = ROOT / "contracts" / "operator-runtime.schema.json"
VALID_OPERATOR_RUNTIME_EXAMPLES = (
    ROOT / "contracts" / "examples" / "minimal-operator-binding.json",
    ROOT / "contracts" / "examples" / "minimal-operator-run-request.json",
    ROOT / "contracts" / "examples" / "minimal-operator-run-record.json",
)
INVALID_OPERATOR_RUNTIME_EXAMPLE = (
    ROOT / "tests" / "fixtures" / "invalid-operator-runtime-missing-binding-id.json"
)
MUTATING_RISKS = {"local_write", "external_write", "privileged", "destructive"}
HIGH_IMPACT_RISKS = {"external_write", "privileged", "destructive"}


@dataclass(frozen=True)
class Issue:
    path: str
    message: str


def load_json(path: Path) -> Any:
    try:
        with path.open("r", encoding="utf-8") as stream:
            return json.load(stream)
    except FileNotFoundError as exc:
        raise ValueError(f"文件不存在：{path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON 解析失败：{path}:{exc.lineno}:{exc.colno}: {exc.msg}") from exc


def format_path(parts: Iterable[Any]) -> str:
    rendered = "$"
    for part in parts:
        rendered += f"[{part}]" if isinstance(part, int) else f".{part}"
    return rendered


def schema_issues(instance: Any, schema: Any) -> list[Issue]:
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as exc:
        raise ValueError(f"Schema 自身无效：{exc.message}") from exc

    validator = Draft202012Validator(schema)
    return [
        Issue(format_path(error.absolute_path), error.message)
        for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.absolute_path))
    ]


def policy_issues(instance: Any) -> list[Issue]:
    """执行 JSON Schema 难以清晰表达的少量跨字段治理规则。"""
    if not isinstance(instance, dict) or not isinstance(instance.get("spec"), dict):
        return []

    spec = instance["spec"]
    issues: list[Issue] = []

    def find_duplicate_ids(items: Any, path: str) -> None:
        if not isinstance(items, list):
            return
        seen: set[str] = set()
        for index, item in enumerate(items):
            if not isinstance(item, dict) or not isinstance(item.get("id"), str):
                continue
            item_id = item["id"]
            if item_id in seen:
                issues.append(Issue(f"{path}[{index}].id", f"标识符重复：{item_id}"))
            seen.add(item_id)

    instructions = spec.get("instructions")
    if isinstance(instructions, dict):
        find_duplicate_ids(instructions.get("sources"), "$.spec.instructions.sources")
    context = spec.get("context")
    if isinstance(context, dict):
        find_duplicate_ids(context.get("sources"), "$.spec.context.sources")

    tools = spec.get("tools")
    if isinstance(tools, list):
        names: set[str] = set()
        for index, tool in enumerate(tools):
            if not isinstance(tool, dict):
                continue
            name = tool.get("name")
            if isinstance(name, str):
                if name in names:
                    issues.append(Issue(f"$.spec.tools[{index}].name", f"工具名重复：{name}"))
                names.add(name)

            risk = tool.get("risk")
            approval = tool.get("approval")
            contract = tool.get("contract")
            if isinstance(contract, dict):
                for field in ("input_schema", "output_schema", "error_schema"):
                    candidate_schema = contract.get(field)
                    if not isinstance(candidate_schema, dict):
                        continue
                    try:
                        Draft202012Validator.check_schema(candidate_schema)
                    except SchemaError as exc:
                        issues.append(
                            Issue(
                                f"$.spec.tools[{index}].contract.{field}",
                                f"工具子 Schema 无效：{exc.message}",
                            )
                        )
                input_schema = contract.get("input_schema")
                if isinstance(input_schema, dict) and (
                    input_schema.get("type") != "object"
                    or input_schema.get("additionalProperties") is not False
                ):
                    issues.append(
                        Issue(
                            f"$.spec.tools[{index}].contract.input_schema",
                            "工具输入 Schema 必须是 object 且拒绝未知属性",
                        )
                    )
            if risk in HIGH_IMPACT_RISKS and approval == "never":
                issues.append(
                    Issue(
                        f"$.spec.tools[{index}].approval",
                        f"{risk} 工具不能声明为永不审批",
                    )
                )
            if risk == "destructive" and approval != "always":
                issues.append(
                    Issue(
                        f"$.spec.tools[{index}].approval",
                        "destructive 工具必须每次审批",
                    )
                )
            if risk in MUTATING_RISKS and tool.get("idempotency") == "non_idempotent" and approval != "always":
                issues.append(
                    Issue(
                        f"$.spec.tools[{index}]",
                        "非幂等写操作必须每次审批",
                    )
                )
            if tool.get("idempotency") == "non_idempotent" and tool.get("retry_policy") != "never":
                issues.append(
                    Issue(
                        f"$.spec.tools[{index}].retry_policy",
                        "非幂等工具不得自动重试",
                    )
                )

    autonomy = spec.get("autonomy")
    checkpoint = spec.get("loop", {}).get("checkpoint") if isinstance(spec.get("loop"), dict) else None
    if autonomy in {"L4", "L5"} and isinstance(checkpoint, dict) and not checkpoint.get("enabled"):
        issues.append(Issue("$.spec.loop.checkpoint.enabled", f"{autonomy} 自治必须启用 checkpoint"))

    risk_level = spec.get("risk_level")
    required_gates = []
    validation = spec.get("validation")
    if isinstance(validation, dict) and isinstance(validation.get("gates"), list):
        required_gates = [gate for gate in validation["gates"] if isinstance(gate, dict) and gate.get("required")]
    if risk_level in {"high", "critical"} and not required_gates:
        issues.append(Issue("$.spec.validation.gates", "高风险 harness 至少需要一个 required gate"))
    if risk_level in {"high", "critical"} and not any(gate.get("type") == "eval" for gate in required_gates):
        issues.append(Issue("$.spec.validation.gates", "高风险 harness 至少需要一个 required eval gate"))
    if isinstance(validation, dict):
        find_duplicate_ids(validation.get("gates"), "$.spec.validation.gates")

    observability = spec.get("observability")
    if (
        risk_level in {"high", "critical"}
        and isinstance(observability, dict)
        and observability.get("tracing") != "required"
    ):
        issues.append(Issue("$.spec.observability.tracing", "高风险 harness 必须启用 tracing"))
    if (
        isinstance(observability, dict)
        and isinstance(observability.get("redact"), list)
        and "credentials" not in observability["redact"]
    ):
        issues.append(Issue("$.spec.observability.redact", "观测脱敏必须包含 credentials"))

    if risk_level in {"high", "critical"} and isinstance(environment := spec.get("environment"), dict):
        if environment.get("filesystem") == "unrestricted":
            issues.append(Issue("$.spec.environment.filesystem", "高风险 harness 不允许 unrestricted filesystem"))
        if environment.get("network") == "unrestricted":
            issues.append(Issue("$.spec.environment.network", "高风险 harness 不允许 unrestricted network"))

    permissions = spec.get("permissions")
    environment = spec.get("environment")
    if isinstance(permissions, dict) and isinstance(environment, dict):
        network_policy = permissions.get("network")
        if isinstance(network_policy, dict):
            allowed = network_policy.get("allow")
            network_mode = environment.get("network")
            if network_mode == "none" and isinstance(allowed, list) and allowed:
                issues.append(Issue("$.spec.permissions.network.allow", "network=none 时 allow 必须为空"))
            if network_mode == "allowlist" and isinstance(allowed, list) and not allowed:
                issues.append(Issue("$.spec.permissions.network.allow", "network=allowlist 时必须声明至少一个目标"))

    return issues


def validate_file(path: Path, schema: Any) -> list[Issue]:
    instance = load_json(path)
    return schema_issues(instance, schema) + policy_issues(instance)


def print_result(path: Path, issues: list[Issue]) -> None:
    if not issues:
        print(f"PASS {path}")
        return

    print(f"BLOCK {path}")
    for issue in issues:
        print(f"  - {issue.path}: {issue.message}")


def print_operator_result(path: Path, result: LibraryValidationResult) -> None:
    if result.issues:
        print(f"BLOCK {path}")
        for issue in result.issues:
            print(f"  - {issue.path}: {issue.message}")
        return
    summary = result.summary
    print(
        f"PASS {path} source_coverage={summary.source_entries}/"
        f"{summary.expected_source_entries} derived_methods={summary.derived_entries}/"
        f"{summary.expected_derived_entries} "
        f"total={summary.entries}"
    )


def _copy_operator_documents(documents: LibraryDocuments) -> LibraryDocuments:
    return LibraryDocuments(
        copy.deepcopy(documents.catalog),
        copy.deepcopy(documents.inventory),
        copy.deepcopy(documents.packs),
        copy.deepcopy(documents.schema),
    )


def run_operator_library_self_test() -> int:
    operator_schema = load_json(DEFAULT_OPERATOR_SCHEMA)
    core_pack = load_json(VALID_OPERATOR_PACK)
    core_issues = validate_operator_pack_document(core_pack, operator_schema)
    print_result(VALID_OPERATOR_PACK, core_issues)
    if core_issues:
        print("SELF-TEST BLOCK：最小 Core Operator Pack 被错误拒绝")
        return 1

    empty_pack = copy.deepcopy(core_pack)
    empty_pack["entries"] = []
    empty_issues = validate_operator_pack_document(empty_pack, operator_schema)
    if empty_issues:
        print("SELF-TEST BLOCK：空 Core Operator Pack 被内容数量规则错误拒绝")
        return 1
    print("PASS synthetic://empty-core-operator-pack")

    misspelled = copy.deepcopy(core_pack)
    misspelled["entries"][0]["summmary"] = "拼写错误不能静默进入稳定字段"
    misspelled_issues = validate_operator_pack_document(misspelled, operator_schema)
    if not any("Additional properties are not allowed" in issue.message for issue in misspelled_issues):
        print("SELF-TEST BLOCK：Core Pack 未知稳定字段未被拒绝")
        return 1
    print("EXPECTED-BLOCK synthetic://unknown-core-field")
    for issue in misspelled_issues:
        print(f"  - {issue.path}: {issue.message}")

    wrong_type = copy.deepcopy(core_pack)
    wrong_type["metadata"]["version"] = 1
    wrong_type_issues = validate_operator_pack_document(wrong_type, operator_schema)
    if not any("is not of type 'string'" in issue.message for issue in wrong_type_issues):
        print("SELF-TEST BLOCK：Core Pack 错误字段类型未被拒绝")
        return 1
    print("EXPECTED-BLOCK synthetic://wrong-core-field-type")
    for issue in wrong_type_issues:
        print(f"  - {issue.path}: {issue.message}")

    positive = validate_operator_library(DEFAULT_OPERATOR_LIBRARY, load_json)
    print_operator_result(DEFAULT_OPERATOR_LIBRARY, positive)
    if positive.issues or positive.documents is None:
        print("SELF-TEST BLOCK：canonical 算子库未通过")
        return 1

    cases: list[tuple[str, LibraryDocuments, str]] = []

    wrong_profile = _copy_operator_documents(positive.documents)
    wrong_profile.catalog["spec"]["conformance_profile"] = "example.org/custom-profile-v1"
    cases.append(("wrong-reference-profile", wrong_profile, "参考库必须显式声明"))

    missing = _copy_operator_documents(positive.documents)
    first_pack = next(iter(missing.packs.values()))
    first_source_index = next(
        index for index, entry in enumerate(first_pack["entries"]) if entry["origin"] == "source"
    )
    first_pack["entries"].pop(first_source_index)
    cases.append(("missing-source-entry", missing, "缺少 source 条目"))

    duplicate = _copy_operator_documents(positive.documents)
    duplicate_pack = next(iter(duplicate.packs.values()))
    duplicate_pack["entries"][1]["id"] = duplicate_pack["entries"][0]["id"]
    cases.append(("duplicate-entry-id", duplicate, "entry id 重复"))

    incomplete_profile = _copy_operator_documents(positive.documents)
    incomplete_entry = next(entry for pack in incomplete_profile.packs.values() for entry in pack["entries"])
    incomplete_entry.pop("core_question")
    cases.append(("reference-profile-missing-content", incomplete_profile, "Reference Library Profile 缺少字段"))

    bad_reference = _copy_operator_documents(positive.documents)
    derived_method = next(
        entry
        for pack in bad_reference.packs.values()
        for entry in pack["entries"]
        if entry["origin"] == "derived"
    )
    derived_method["semantics"]["steps"][0]["use"] = "psoa.missing.operator"
    cases.append(("unresolved-method-reference", bad_reference, "Method 引用不存在"))

    disguised_model = _copy_operator_documents(positive.documents)
    mental_model = next(
        entry
        for pack in disguised_model.packs.values()
        for entry in pack["entries"]
        if entry["kind"] == "MentalModelSpec"
    )
    mental_model["semantics"]["effect"] = {
        "state": "world_state",
        "statement": "伪装成现实世界副作用",
    }
    cases.append(("mental-model-with-effect", disguised_model, "Additional properties are not allowed"))

    wrong_model_edge = _copy_operator_documents(positive.documents)
    target_method = next(
        entry
        for pack in wrong_model_edge.packs.values()
        for entry in pack["entries"]
        if entry["origin"] == "derived" and "use" in entry["semantics"]["steps"][0]
    )
    model_id = next(
        entry["id"]
        for pack in wrong_model_edge.packs.values()
        for entry in pack["entries"]
        if entry["kind"] == "MentalModelSpec"
    )
    target_method["semantics"]["steps"][0]["use"] = model_id
    cases.append(("mental-model-used-as-action", wrong_model_edge, "必须通过 apply_model 应用"))

    cyclic_method = _copy_operator_documents(positive.documents)
    cycle_target = next(
        entry
        for pack in cyclic_method.packs.values()
        for entry in pack["entries"]
        if entry["origin"] == "derived" and "use" in entry["semantics"]["steps"][0]
    )
    cycle_target["semantics"]["steps"][0]["use"] = cycle_target["id"]
    cases.append(("cyclic-method-reference", cyclic_method, "Method 引用形成循环"))

    self_authorized = _copy_operator_documents(positive.documents)
    first_entry = next(entry for pack in self_authorized.packs.values() for entry in pack["entries"])
    first_entry["governance"]["permission_decision"] = "model"
    cases.append(("operator-self-authorization", self_authorized, "必须是 harness_policy"))

    for case_id, documents, expected_message in cases:
        result = validate_operator_library_documents(documents)
        if not any(expected_message in issue.message for issue in result.issues):
            print(f"SELF-TEST BLOCK：{case_id} 未被预期规则拒绝")
            for issue in result.issues:
                print(f"  - {issue.path}: {issue.message}")
            return 1
        print(f"EXPECTED-BLOCK synthetic://{case_id}")
        for issue in result.issues:
            print(f"  - {issue.path}: {issue.message}")

    escaped = copy.deepcopy(positive.documents.catalog)
    escaped["spec"]["packs"][0]["path"] = "../outside.json"
    escaped_issues, _ = catalog_path_issues(DEFAULT_OPERATOR_LIBRARY, escaped)
    if not any("路径逃逸" in issue.message for issue in escaped_issues):
        print("SELF-TEST BLOCK：pack 路径逃逸未被拒绝")
        return 1
    print("EXPECTED-BLOCK synthetic://escaped-pack-path")
    for issue in escaped_issues:
        print(f"  - {issue.path}: {issue.message}")

    print("OPERATOR-LIBRARY SELF-TEST PASS：Core 宽松正例通过，格式与 Reference Profile 负例被拒绝")
    return 0


def run_operator_runtime_self_test() -> int:
    runtime_schema = load_json(DEFAULT_OPERATOR_RUNTIME_SCHEMA)
    for path in VALID_OPERATOR_RUNTIME_EXAMPLES:
        issues = schema_issues(load_json(path), runtime_schema)
        print_result(path, issues)
        if issues:
            print("SELF-TEST BLOCK：有效 Operator Runtime 样例被错误拒绝")
            return 1

    invalid_issues = schema_issues(load_json(INVALID_OPERATOR_RUNTIME_EXAMPLE), runtime_schema)
    if not invalid_issues:
        print("SELF-TEST BLOCK：缺失 binding_id 的 Runtime 请求被错误接受")
        return 1
    print(f"EXPECTED-BLOCK {INVALID_OPERATOR_RUNTIME_EXAMPLE}")
    for issue in invalid_issues:
        print(f"  - {issue.path}: {issue.message}")

    extension_case = copy.deepcopy(load_json(VALID_OPERATOR_RUNTIME_EXAMPLES[0]))
    extension_case["metadata"]["extensions"] = {"example.org": {"deployment": "local"}}
    extension_issues = schema_issues(extension_case, runtime_schema)
    if extension_issues:
        print("SELF-TEST BLOCK：显式 Runtime extensions 被错误拒绝")
        return 1
    print("PASS synthetic://operator-runtime-explicit-extension")

    misspelled = copy.deepcopy(load_json(VALID_OPERATOR_RUNTIME_EXAMPLES[0]))
    misspelled["metadata"]["harnes_id"] = misspelled["metadata"]["harness_id"]
    misspelled_issues = schema_issues(misspelled, runtime_schema)
    if not misspelled_issues:
        print("SELF-TEST BLOCK：Runtime 未知稳定字段被错误接受")
        return 1
    print("EXPECTED-BLOCK synthetic://operator-runtime-unknown-stable-field")

    nested_unknown = copy.deepcopy(load_json(VALID_OPERATOR_RUNTIME_EXAMPLES[2]))
    nested_unknown["spec"]["provenance"]["events"][0]["unexpected"] = True
    nested_unknown_issues = schema_issues(nested_unknown, runtime_schema)
    if not nested_unknown_issues:
        print("SELF-TEST BLOCK：Runtime 嵌套未知稳定字段被错误接受")
        return 1
    print("EXPECTED-BLOCK synthetic://operator-runtime-unknown-nested-stable-field")

    invalid_timestamp = copy.deepcopy(load_json(VALID_OPERATOR_RUNTIME_EXAMPLES[1]))
    invalid_timestamp["metadata"]["requested_at"] = "not-a-date"
    invalid_timestamp_issues = schema_issues(invalid_timestamp, runtime_schema)
    if not invalid_timestamp_issues:
        print("SELF-TEST BLOCK：Runtime 非法 requested_at 被错误接受")
        return 1
    print("EXPECTED-BLOCK synthetic://operator-runtime-invalid-requested-at")

    print("OPERATOR-RUNTIME SELF-TEST PASS：三个 Core 对象和扩展通过，缺失/未知稳定字段被拒绝")
    return 0


def run_self_test(schema: Any) -> int:
    positive = validate_file(VALID_EXAMPLE, schema)
    negative = validate_file(INVALID_EXAMPLE, schema)
    print_result(VALID_EXAMPLE, positive)

    if positive:
        print("SELF-TEST BLOCK：有效样例被错误拒绝")
        return 1
    if not negative:
        print_result(INVALID_EXAMPLE, negative)
        print("SELF-TEST BLOCK：无效样例被错误接受")
        return 1

    print(f"EXPECTED-BLOCK {INVALID_EXAMPLE}")
    for issue in negative:
        print(f"  - {issue.path}: {issue.message}")

    policy_negative = copy.deepcopy(load_json(VALID_EXAMPLE))
    policy_negative["spec"]["tools"][2]["approval"] = "never"
    policy_issues_found = schema_issues(policy_negative, schema) + policy_issues(policy_negative)
    expected_policy_path = "$.spec.tools[2].approval"
    if not any(issue.path == expected_policy_path for issue in policy_issues_found):
        print("SELF-TEST BLOCK：高风险工具绕过审批未被策略门禁拒绝")
        return 1

    print("EXPECTED-BLOCK synthetic://high-risk-tool-without-approval")
    for issue in policy_issues_found:
        print(f"  - {issue.path}: {issue.message}")

    version_negative = copy.deepcopy(load_json(VALID_EXAMPLE))
    version_negative["metadata"]["version"] = "01.0.0"
    version_issues = schema_issues(version_negative, schema)
    expected_version_path = "$.metadata.version"
    if not any(issue.path == expected_version_path for issue in version_issues):
        print("SELF-TEST BLOCK：非法 SemVer 被错误接受")
        return 1

    print("EXPECTED-BLOCK synthetic://invalid-semver")
    for issue in version_issues:
        print(f"  - {issue.path}: {issue.message}")

    tracing_negative = copy.deepcopy(load_json(VALID_EXAMPLE))
    tracing_negative["spec"]["observability"]["tracing"] = "disabled"
    tracing_issues = schema_issues(tracing_negative, schema) + policy_issues(tracing_negative)
    expected_tracing_path = "$.spec.observability.tracing"
    if not any(issue.path == expected_tracing_path for issue in tracing_issues):
        print("SELF-TEST BLOCK：高风险 harness 关闭 tracing 未被拒绝")
        return 1

    print("EXPECTED-BLOCK synthetic://high-risk-without-tracing")
    for issue in tracing_issues:
        print(f"  - {issue.path}: {issue.message}")

    lifecycle_negative = copy.deepcopy(load_json(VALID_EXAMPLE))
    lifecycle_negative["spec"]["lifecycle"]["stage"] = "approved"
    lifecycle_issues = schema_issues(lifecycle_negative, schema)
    expected_lifecycle_path = "$.spec.lifecycle.stage"
    if not any(issue.path == expected_lifecycle_path for issue in lifecycle_issues):
        print("SELF-TEST BLOCK：manifest 作者自报 approved 未被拒绝")
        return 1

    print("EXPECTED-BLOCK synthetic://author-self-approved")
    for issue in lifecycle_issues:
        print(f"  - {issue.path}: {issue.message}")

    approval_negative = copy.deepcopy(load_json(VALID_EXAMPLE))
    approval_negative["spec"]["permissions"]["approvals"]["model_self_approval"] = True
    approval_issues = schema_issues(approval_negative, schema)
    expected_approval_path = "$.spec.permissions.approvals.model_self_approval"
    if not any(issue.path == expected_approval_path for issue in approval_issues):
        print("SELF-TEST BLOCK：模型自我审批未被拒绝")
        return 1

    print("EXPECTED-BLOCK synthetic://model-self-approval")
    for issue in approval_issues:
        print(f"  - {issue.path}: {issue.message}")

    tool_schema_negative = copy.deepcopy(load_json(VALID_EXAMPLE))
    tool_schema_negative["spec"]["tools"][0]["contract"]["input_schema"] = {"type": "not-a-json-type"}
    tool_schema_issues = schema_issues(tool_schema_negative, schema) + policy_issues(tool_schema_negative)
    expected_tool_schema_path = "$.spec.tools[0].contract.input_schema"
    if not any(issue.path == expected_tool_schema_path for issue in tool_schema_issues):
        print("SELF-TEST BLOCK：无效工具子 Schema 未被拒绝")
        return 1

    print("EXPECTED-BLOCK synthetic://invalid-tool-input-schema")
    for issue in tool_schema_issues:
        print(f"  - {issue.path}: {issue.message}")
    print("HARNESS-MANIFEST SELF-TEST PASS：正例通过，负例被拒绝")
    operator_status = run_operator_library_self_test()
    if operator_status:
        return operator_status
    runtime_status = run_operator_runtime_self_test()
    if runtime_status:
        return runtime_status
    print("SELF-TEST PASS：Harness manifest、Operator Library 与 Operator Runtime 回归全部通过")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="校验 Harness manifest、Operator Pack、参考算子库或 Operator Runtime 对象。"
    )
    parser.add_argument("paths", nargs="*", type=Path, help="待校验的 JSON manifest 路径。")
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA, help="JSON Schema 路径。")
    parser.add_argument("--operator-pack", type=Path, help="按公共 Core Contract 校验单个 Operator Pack。")
    parser.add_argument(
        "--operator-schema",
        type=Path,
        default=DEFAULT_OPERATOR_SCHEMA,
        help="Operator Pack Core JSON Schema 路径。",
    )
    parser.add_argument("--operator-library", type=Path, help="待校验的 Operator Library catalog。")
    parser.add_argument(
        "--operator-runtime",
        nargs="+",
        type=Path,
        help="按 Operator Runtime Core 校验一个或多个 JSON 对象。",
    )
    parser.add_argument(
        "--operator-runtime-schema",
        type=Path,
        default=DEFAULT_OPERATOR_RUNTIME_SCHEMA,
        help="Operator Runtime Core JSON Schema 路径。",
    )
    parser.add_argument("--self-test", action="store_true", help="运行内置正反例回归。")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    modes = (
        int(args.self_test)
        + int(bool(args.paths))
        + int(args.operator_pack is not None)
        + int(args.operator_library is not None)
        + int(args.operator_runtime is not None)
    )
    if modes != 1:
        print(
            "参数错误：manifest 路径、--operator-pack、--operator-library、--operator-runtime 与 --self-test 必须且只能选择一种",
            file=sys.stderr,
        )
        return 2

    try:
        if args.self_test:
            schema = load_json(args.schema.resolve())
            return run_self_test(schema)
        if args.operator_pack is not None:
            operator_schema = load_json(args.operator_schema.resolve())
            operator_pack = load_json(args.operator_pack.resolve())
            issues = validate_operator_pack_document(operator_pack, operator_schema)
            print_result(args.operator_pack, issues)
            return 1 if issues else 0
        if args.operator_library is not None:
            result = validate_operator_library(args.operator_library.resolve(), load_json)
            print_operator_result(args.operator_library, result)
            return 1 if result.issues else 0
        if args.operator_runtime is not None:
            runtime_schema = load_json(args.operator_runtime_schema.resolve())
            blocked = False
            for path in args.operator_runtime:
                issues = schema_issues(load_json(path.resolve()), runtime_schema)
                print_result(path, issues)
                blocked = blocked or bool(issues)
            return 1 if blocked else 0

        schema = load_json(args.schema.resolve())
        blocked = False
        for path in args.paths:
            issues = validate_file(path.resolve(), schema)
            print_result(path, issues)
            blocked = blocked or bool(issues)
        return 1 if blocked else 0
    except ValueError as exc:
        print(f"BLOCK {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
