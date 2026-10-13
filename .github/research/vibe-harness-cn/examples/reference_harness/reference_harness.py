#!/usr/bin/env python3
# 做什么：以无副作用参考 Harness 物化问题求解算子并独立验证结果。
# 怎么运行：python3 examples/reference_harness/reference_harness.py --request <json> --binding <json>。
# 需要什么：Python 3.11+、本仓库 operator catalog、taxonomy 与 Harness 本地 Binding。

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CATALOG = ROOT / "operators" / "catalog.json"
DEFAULT_TAXONOMY = ROOT / "operators" / "taxonomy" / "problem-solving-methodology.json"
DEFAULT_BINDING = Path(__file__).resolve().parent / "bindings" / "instruction-packet.json"
DEFAULT_REQUEST = Path(__file__).resolve().parent / "requests" / "definition-first.json"
RUNTIME_API_VERSION = "vibe-harness-cn.dev/operator-runtime/v1alpha1"
CLAIM_SCOPE = "instruction_materialization_only"
EXECUTOR_ID = "vibe-harness-cn.reference.executor"
VERIFIER_ID = "vibe-harness-cn.reference.verifier"


class RuntimeViolation(ValueError):
    """表示请求、Binding、目录或物化结果违反参考 Harness 的硬边界。"""


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RuntimeViolation(f"文件不存在：{path}") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeViolation(f"JSON 解析失败：{path}:{exc.lineno}:{exc.colno}: {exc.msg}") from exc
    if not isinstance(value, dict):
        raise RuntimeViolation(f"JSON 顶层必须是对象：{path}")
    return value


def canonical_digest(value: Any) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def require_object(parent: dict[str, Any], key: str) -> dict[str, Any]:
    value = parent.get(key)
    if not isinstance(value, dict):
        raise RuntimeViolation(f"{key} 必须是对象")
    return value


def require_string(parent: dict[str, Any], key: str) -> str:
    value = parent.get(key)
    if not isinstance(value, str) or not value.strip():
        raise RuntimeViolation(f"{key} 必须是非空字符串")
    return value


def string_list(parent: dict[str, Any], key: str) -> list[str]:
    value = parent.get(key, [])
    if not isinstance(value, list) or any(not isinstance(item, str) or not item for item in value):
        raise RuntimeViolation(f"{key} 必须是非空字符串数组")
    return value


def _safe_child(base: Path, relative: str) -> Path:
    candidate = (base / relative).resolve()
    base = base.resolve()
    if not candidate.is_relative_to(base):
        raise RuntimeViolation(f"目录路径越界：{relative}")
    return candidate


def load_library(catalog_path: Path, taxonomy_path: Path) -> dict[str, Any]:
    catalog = load_json(catalog_path)
    taxonomy = load_json(taxonomy_path)
    spec = require_object(catalog, "spec")
    pack_rows = spec.get("packs")
    if not isinstance(pack_rows, list) or not pack_rows:
        raise RuntimeViolation("catalog.spec.packs 必须是非空数组")

    entries: dict[str, dict[str, Any]] = {}
    pack_documents: list[dict[str, Any]] = []
    base = catalog_path.resolve().parent
    for index, row in enumerate(pack_rows):
        if not isinstance(row, dict):
            raise RuntimeViolation(f"catalog.spec.packs[{index}] 必须是对象")
        relative = require_string(row, "path")
        pack = load_json(_safe_child(base, relative))
        pack_documents.append(pack)
        pack_entries = pack.get("entries")
        if not isinstance(pack_entries, list):
            raise RuntimeViolation(f"pack {relative} 缺少 entries")
        for entry in pack_entries:
            if not isinstance(entry, dict):
                raise RuntimeViolation(f"pack {relative} 包含非对象 entry")
            entry_id = require_string(entry, "id")
            if entry_id in entries:
                raise RuntimeViolation(f"算子 ID 重复：{entry_id}")
            entries[entry_id] = entry

    taxonomy_spec = require_object(taxonomy, "spec")
    domain_rows = taxonomy_spec.get("domain_defaults")
    override_rows = taxonomy_spec.get("entry_overrides")
    if not isinstance(domain_rows, list) or not domain_rows:
        raise RuntimeViolation("taxonomy.spec.domain_defaults 必须是非空数组")
    if not isinstance(override_rows, list):
        raise RuntimeViolation("taxonomy.spec.entry_overrides 必须是数组")

    domain_defaults: dict[str, str] = {}
    for index, row in enumerate(domain_rows):
        if not isinstance(row, dict):
            raise RuntimeViolation(f"taxonomy.spec.domain_defaults[{index}] 必须是对象")
        domain_defaults[require_string(row, "domain")] = require_string(
            row, "functional_class"
        )

    overrides: dict[str, str] = {}
    for index, row in enumerate(override_rows):
        if not isinstance(row, dict):
            raise RuntimeViolation(f"taxonomy.spec.entry_overrides[{index}] 必须是对象")
        overrides[require_string(row, "entry")] = require_string(row, "functional_class")
    functional_classes: dict[str, str] = {}
    for entry_id, entry in entries.items():
        domain = require_string(entry, "domain")
        functional_class = overrides.get(entry_id, domain_defaults.get(domain))
        if not functional_class:
            raise RuntimeViolation(f"算子缺少 functional_class 映射：{entry_id}")
        functional_classes[entry_id] = functional_class

    library_document = {
        "catalog": catalog,
        "packs": pack_documents,
        "taxonomy": taxonomy,
    }
    return {
        "catalog": catalog,
        "entries": entries,
        "functional_classes": functional_classes,
        "digest": canonical_digest(library_document),
    }


def validate_binding(request: dict[str, Any], binding: dict[str, Any], library: dict[str, Any]) -> None:
    if request.get("api_version") != RUNTIME_API_VERSION or request.get("kind") != "OperatorRunRequest":
        raise RuntimeViolation("请求不是受支持的 OperatorRunRequest v1alpha1")
    if binding.get("api_version") != RUNTIME_API_VERSION or binding.get("kind") != "OperatorBinding":
        raise RuntimeViolation("Binding 不是受支持的 OperatorBinding v1alpha1")

    request_spec = require_object(request, "spec")
    binding_metadata = require_object(binding, "metadata")
    binding_spec = require_object(binding, "spec")
    contract = require_object(binding_spec, "operator_contract")
    execution = require_object(binding_spec, "execution")
    policy = require_object(binding_spec, "policy")
    catalog = library["catalog"]

    if require_string(request_spec, "harness_id") != require_string(binding_metadata, "harness_id"):
        raise RuntimeViolation("请求 harness_id 与 Binding 所有者不匹配")
    if require_string(request_spec, "binding_id") != require_string(binding_metadata, "id"):
        raise RuntimeViolation("请求引用了未知 Binding")
    if require_string(contract, "api_version") != require_string(catalog, "api_version"):
        raise RuntimeViolation("Binding 支持的 Operator API 与目录不匹配")
    catalog_spec = require_object(catalog, "spec")
    if require_string(contract, "library_profile") != require_string(catalog_spec, "conformance_profile"):
        raise RuntimeViolation("Binding 支持的 library profile 与目录不匹配")
    if require_string(request_spec, "required_effect_scope") != require_string(execution, "effect_scope"):
        raise RuntimeViolation("请求 effect scope 超出 Binding")
    modes = set(string_list(execution, "modes"))
    default_mode = require_string(execution, "default_mode")
    if default_mode not in modes:
        raise RuntimeViolation("Binding default_mode 未包含在 modes 中")
    if default_mode != "instruction_materialization":
        raise RuntimeViolation("参考 Harness 只支持 instruction_materialization")
    if execution.get("effect_scope") != "none":
        raise RuntimeViolation("参考 Harness 只允许 effect_scope=none")
    if any(policy.get(field) is not False for field in ("model_access", "tool_access", "external_write")):
        raise RuntimeViolation("参考 Harness 禁止模型、工具和外部写入")

    budgets = require_object(request_spec, "budgets")
    for key in ("max_candidates", "max_steps"):
        requested = budgets.get(key)
        allowed = policy.get(key)
        if type(requested) is not int or requested < 1:
            raise RuntimeViolation(f"请求预算 {key} 必须是正整数")
        if type(allowed) is not int or allowed < 1:
            raise RuntimeViolation(f"Binding 策略 {key} 必须是正整数")
        if requested > allowed:
            raise RuntimeViolation(f"请求预算 {key}={requested} 超出 Binding 上限 {allowed}")


def select_operator(
    request: dict[str, Any],
    binding: dict[str, Any],
    library: dict[str, Any],
) -> dict[str, Any]:
    request_spec = require_object(request, "spec")
    selection = require_object(request_spec, "selection")
    binding_spec = require_object(binding, "spec")
    contract = require_object(binding_spec, "operator_contract")
    policy = require_object(binding_spec, "policy")
    budgets = require_object(request_spec, "budgets")

    requested_ids = set(string_list(selection, "requested_operator_ids"))
    requested_domains = set(string_list(selection, "domains"))
    requested_classes = set(string_list(selection, "functional_classes"))
    requested_kinds = set(string_list(selection, "kinds"))
    query_terms = [term.casefold() for term in string_list(selection, "query_terms")]
    if not any((requested_ids, requested_domains, requested_classes, requested_kinds, query_terms)):
        raise RuntimeViolation("selection 至少需要一种确定性选择条件")

    supported_kinds = set(string_list(contract, "supported_kinds"))
    supported_statuses = set(string_list(contract, "supported_statuses"))
    allowed_risks = set(string_list(policy, "allowed_risk_levels"))
    allowed_domains = set(string_list(policy, "allowed_domains"))
    allowed_classes = set(string_list(policy, "allowed_functional_classes"))
    entries: dict[str, dict[str, Any]] = library["entries"]
    functional_classes: dict[str, str] = library["functional_classes"]

    missing_ids = sorted(requested_ids - set(entries))
    if missing_ids:
        raise RuntimeViolation("请求的算子不存在：" + ", ".join(missing_ids))

    candidates: list[dict[str, Any]] = []
    rejections: Counter[str] = Counter()
    for entry_id, entry in entries.items():
        kind = require_string(entry, "kind")
        status = require_string(entry, "status")
        domain = require_string(entry, "domain")
        functional_class = functional_classes[entry_id]
        governance = require_object(entry, "governance")
        risk = require_string(governance, "risk_level")

        rejection = ""
        if kind not in supported_kinds:
            rejection = "unsupported_kind"
        elif status not in supported_statuses:
            rejection = "unsupported_status"
        elif risk not in allowed_risks:
            rejection = "risk_not_allowed"
        elif allowed_domains and domain not in allowed_domains:
            rejection = "domain_not_allowed"
        elif allowed_classes and functional_class not in allowed_classes:
            rejection = "functional_class_not_allowed"
        elif requested_ids and entry_id not in requested_ids:
            rejection = "not_requested"
        elif requested_domains and domain not in requested_domains:
            rejection = "domain_mismatch"
        elif requested_classes and functional_class not in requested_classes:
            rejection = "functional_class_mismatch"
        elif requested_kinds and kind not in requested_kinds:
            rejection = "kind_mismatch"

        searchable = " ".join(
            str(entry.get(field, ""))
            for field in ("id", "name", "name_zh", "summary", "core_question", "operation", "agent_use")
        ).casefold()
        matched_terms = [term for term in query_terms if term in searchable]
        if not rejection and query_terms and not matched_terms:
            rejection = "query_miss"
        if rejection:
            rejections[rejection] += 1
            continue

        score = 0
        reasons: list[str] = []
        if requested_ids:
            score += 10_000
            reasons.append("explicit_operator_id")
        if requested_classes:
            score += 500
            reasons.append("functional_class_match")
        if requested_domains:
            score += 250
            reasons.append("domain_match")
        if requested_kinds:
            score += 100
            reasons.append("kind_match")
        if matched_terms:
            score += 10 * len(matched_terms)
            reasons.extend(f"query_term:{term}" for term in matched_terms)
        candidates.append(
            {
                "id": entry_id,
                "version": require_string(entry, "version"),
                "kind": kind,
                "functional_class": functional_class,
                "score": score,
                "reasons": reasons,
            }
        )

    candidates.sort(key=lambda item: (-item["score"], item["id"]))
    max_candidates = budgets["max_candidates"]
    if len(candidates) > max_candidates:
        rejections["candidate_budget_truncated"] += len(candidates) - max_candidates
    candidates = candidates[:max_candidates]
    if not candidates:
        raise RuntimeViolation("没有算子同时满足请求、Binding 与 Harness policy")
    return {
        "selected_operator": candidates[0],
        "candidate_count": len(candidates),
        "considered_count": len(entries),
        "candidates": candidates,
        "rejection_summary": dict(sorted(rejections.items())),
    }


class Materializer:
    def __init__(self, entries: dict[str, dict[str, Any]], max_steps: int) -> None:
        self.entries = entries
        self.max_steps = max_steps
        self.instructions: list[dict[str, Any]] = []
        self.preconditions: list[str] = []
        self.evidence_required: list[str] = []
        self.stop_conditions: list[str] = []
        self.failure_modes: list[str] = []

    @staticmethod
    def _append_unique(target: list[str], values: Any) -> None:
        if not isinstance(values, list):
            return
        for value in values:
            if isinstance(value, str) and value and value not in target:
                target.append(value)

    def _add_instruction(self, operator_id: str, kind: str, action: str, content: str) -> None:
        if len(self.instructions) >= self.max_steps:
            raise RuntimeViolation(f"物化步骤超过 max_steps={self.max_steps}")
        self.instructions.append(
            {
                "sequence": len(self.instructions) + 1,
                "source_operator_id": operator_id,
                "source_kind": kind,
                "action": action,
                "content": content,
            }
        )

    def visit(self, operator_id: str, stack: tuple[str, ...] = ()) -> None:
        if operator_id in stack:
            raise RuntimeViolation("Method 引用形成循环：" + " -> ".join((*stack, operator_id)))
        entry = self.entries.get(operator_id)
        if entry is None:
            raise RuntimeViolation(f"Method 引用不存在：{operator_id}")
        kind = require_string(entry, "kind")
        semantics = require_object(entry, "semantics")
        self._append_unique(self.preconditions, semantics.get("preconditions"))
        self._append_unique(self.evidence_required, semantics.get("evidence_required"))
        self._append_unique(self.stop_conditions, semantics.get("stop_conditions"))
        self._append_unique(self.failure_modes, semantics.get("failure_modes"))

        if kind == "OperatorSpec":
            procedure = semantics.get("procedure")
            if not isinstance(procedure, list) or not procedure:
                raise RuntimeViolation(f"OperatorSpec 缺少 procedure：{operator_id}")
            for instruction in procedure:
                if not isinstance(instruction, str) or not instruction:
                    raise RuntimeViolation(f"OperatorSpec procedure 非法：{operator_id}")
                self._add_instruction(operator_id, kind, "perform", instruction)
            return

        if kind == "MentalModelSpec":
            questions = semantics.get("questions")
            rules = semantics.get("interpretation_rules")
            if not isinstance(questions, list) or not questions or not isinstance(rules, list) or not rules:
                raise RuntimeViolation(f"MentalModelSpec 缺少 questions 或 interpretation_rules：{operator_id}")
            for question in questions:
                self._add_instruction(operator_id, kind, "ask", require_text(question, operator_id))
            for rule in rules:
                self._add_instruction(operator_id, kind, "interpret", require_text(rule, operator_id))
            self._append_unique(self.failure_modes, semantics.get("limitations"))
            return

        if kind != "MethodSpec":
            raise RuntimeViolation(f"不支持的算子 kind：{kind}")
        steps = semantics.get("steps")
        if not isinstance(steps, list) or not steps:
            raise RuntimeViolation(f"MethodSpec 缺少 steps：{operator_id}")
        for step in sorted(steps, key=lambda item: item.get("order", 0) if isinstance(item, dict) else 0):
            if not isinstance(step, dict):
                raise RuntimeViolation(f"MethodSpec step 非法：{operator_id}")
            if "instruction" in step:
                self._add_instruction(
                    operator_id,
                    kind,
                    "perform",
                    require_text(step["instruction"], operator_id),
                )
            elif "use" in step:
                self.visit(require_text(step["use"], operator_id), (*stack, operator_id))
            elif "apply_model" in step:
                self.visit(require_text(step["apply_model"], operator_id), (*stack, operator_id))
            else:
                raise RuntimeViolation(f"MethodSpec step 缺少 instruction/use/apply_model：{operator_id}")


def require_text(value: Any, context: str) -> str:
    if not isinstance(value, str) or not value:
        raise RuntimeViolation(f"{context} 包含空文本")
    return value


def materialize_operator(
    request: dict[str, Any],
    selection: dict[str, Any],
    library: dict[str, Any],
) -> dict[str, Any]:
    budgets = require_object(require_object(request, "spec"), "budgets")
    selected = require_object(selection, "selected_operator")
    materializer = Materializer(library["entries"], budgets["max_steps"])
    materializer.visit(require_string(selected, "id"))
    problem = require_object(require_object(request, "spec"), "problem")
    return {
        "api_version": RUNTIME_API_VERSION,
        "kind": "InstructionPacket",
        "metadata": {
            "request_id": require_string(require_object(request, "metadata"), "id"),
            "operator_id": selected["id"],
            "operator_version": selected["version"],
        },
        "spec": {
            "claim_scope": CLAIM_SCOPE,
            "problem_digest": canonical_digest(problem),
            "instructions": materializer.instructions,
            "checks": {
                "preconditions": materializer.preconditions,
                "evidence_required": materializer.evidence_required,
                "stop_conditions": materializer.stop_conditions,
                "failure_modes": materializer.failure_modes,
            },
            "execution_constraints": {
                "effect_scope": "none",
                "model_access": False,
                "tool_access": False,
                "external_write": False,
            },
        },
    }


def _verify_materialization(
    request: dict[str, Any],
    binding: dict[str, Any],
    library: dict[str, Any],
    instruction_packet: dict[str, Any],
    reported_packet_digest: str,
) -> tuple[list[str], dict[str, Any]]:
    failures: list[str] = []
    try:
        validate_binding(request, binding, library)
        expected_selection = select_operator(request, binding, library)
        expected_packet = materialize_operator(request, expected_selection, library)
    except RuntimeViolation as exc:
        return [f"verifier_recompute_failed:{exc}"], {}

    expected_digest = canonical_digest(expected_packet)
    actual_digest = canonical_digest(instruction_packet)
    if reported_packet_digest != actual_digest:
        failures.append("reported_instruction_packet_digest_mismatch")
    if actual_digest != expected_digest:
        failures.append("instruction_packet_content_mismatch")
    if instruction_packet.get("spec", {}).get("claim_scope") != CLAIM_SCOPE:
        failures.append("claim_scope_mismatch")
    return failures, expected_selection


def verify_materialization(
    request: dict[str, Any],
    binding: dict[str, Any],
    catalog_path: Path,
    taxonomy_path: Path,
    instruction_packet: dict[str, Any],
    reported_packet_digest: str,
) -> list[str]:
    library = load_library(catalog_path, taxonomy_path)
    failures, _ = _verify_materialization(
        request,
        binding,
        library,
        instruction_packet,
        reported_packet_digest,
    )
    return failures


def build_record(
    request: dict[str, Any],
    binding: dict[str, Any],
    library: dict[str, Any],
    selection: dict[str, Any],
    instruction_packet: dict[str, Any],
    failures: list[str],
) -> dict[str, Any]:
    request_metadata = require_object(request, "metadata")
    binding_metadata = require_object(binding, "metadata")
    packet_digest = canonical_digest(instruction_packet)
    accepted = not failures
    record_seed = {
        "request": request_metadata["id"],
        "binding": binding_metadata["id"],
        "packet": packet_digest,
    }
    record_id = "run-record." + canonical_digest(record_seed).split(":", 1)[1][:16]
    return {
        "api_version": RUNTIME_API_VERSION,
        "kind": "OperatorRunRecord",
        "metadata": {
            "id": record_id,
            "version": "0.1.0",
            "harness_id": binding_metadata["harness_id"],
            "status": "completed" if accepted else "rejected",
        },
        "spec": {
            "request_id": request_metadata["id"],
            "binding_id": binding_metadata["id"],
            "selection": selection,
            "result": {
                "materialization_status": "completed",
                "verification_verdict": "accepted" if accepted else "rejected",
                "claim_scope": CLAIM_SCOPE,
                "instruction_count": len(instruction_packet["spec"]["instructions"]),
                "instruction_packet_digest": packet_digest,
                "failures": failures,
            },
            "provenance": {
                "actors": [EXECUTOR_ID, VERIFIER_ID],
                "artifacts": {
                    "request": canonical_digest(request),
                    "binding": canonical_digest(binding),
                    "library": library["digest"],
                    "instruction_packet": packet_digest,
                },
                "events": [
                    {"sequence": 1, "stage": "select", "status": "completed", "actor": EXECUTOR_ID},
                    {"sequence": 2, "stage": "bind", "status": "completed", "actor": EXECUTOR_ID},
                    {"sequence": 3, "stage": "materialize", "status": "completed", "actor": EXECUTOR_ID},
                    {
                        "sequence": 4,
                        "stage": "verify",
                        "status": "accepted" if accepted else "rejected",
                        "actor": VERIFIER_ID,
                    },
                    {"sequence": 5, "stage": "trace", "status": "completed", "actor": VERIFIER_ID},
                ],
                "disclosure": "digests_and_metadata_only",
            },
        },
    }


def verify_and_record(
    request: dict[str, Any],
    binding: dict[str, Any],
    catalog_path: Path,
    taxonomy_path: Path,
    instruction_packet: dict[str, Any],
    reported_packet_digest: str,
) -> dict[str, Any]:
    """从原始输入重载目录并生成 verifier 拥有的最终记录。"""
    library = load_library(catalog_path, taxonomy_path)
    failures, selection = _verify_materialization(
        request,
        binding,
        library,
        instruction_packet,
        reported_packet_digest,
    )
    if not selection:
        raise RuntimeViolation("Verifier 无法生成可记录的确定性选择结果：" + "; ".join(failures))
    return build_record(
        request,
        binding,
        library,
        selection,
        instruction_packet,
        failures,
    )


def run_reference_harness(
    request: dict[str, Any],
    binding: dict[str, Any],
    catalog_path: Path = DEFAULT_CATALOG,
    taxonomy_path: Path = DEFAULT_TAXONOMY,
) -> dict[str, Any]:
    library = load_library(catalog_path, taxonomy_path)
    validate_binding(request, binding, library)
    selection = select_operator(request, binding, library)
    instruction_packet = materialize_operator(request, selection, library)
    reported_digest = canonical_digest(instruction_packet)
    record = verify_and_record(
        request,
        binding,
        catalog_path,
        taxonomy_path,
        instruction_packet,
        reported_digest,
    )
    return {
        "api_version": RUNTIME_API_VERSION,
        "kind": "OperatorRunBundle",
        "record": record,
        "instruction_packet": instruction_packet,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="运行无副作用 Reference Operator Harness。")
    parser.add_argument("--request", type=Path, default=DEFAULT_REQUEST)
    parser.add_argument("--binding", type=Path, default=DEFAULT_BINDING)
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--taxonomy", type=Path, default=DEFAULT_TAXONOMY)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        bundle = run_reference_harness(
            load_json(args.request.resolve()),
            load_json(args.binding.resolve()),
            args.catalog.resolve(),
            args.taxonomy.resolve(),
        )
    except (OSError, RuntimeViolation, KeyError, TypeError) as exc:
        print(
            json.dumps(
                {
                    "api_version": RUNTIME_API_VERSION,
                    "kind": "OperatorRunError",
                    "status": "rejected",
                    "error": str(exc),
                },
                ensure_ascii=False,
                sort_keys=True,
            ),
            file=sys.stderr,
        )
        return 2
    print(json.dumps(bundle, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
