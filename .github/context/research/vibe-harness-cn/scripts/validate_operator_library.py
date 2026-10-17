#!/usr/bin/env python3
# 做什么：校验 Operator Pack Core Schema，以及参考库 Profile 的完整清单、引用和治理不变量。
# 怎么运行：由 validate_harness.py --operator-library 或 --self-test 调用。
# 需要什么：Python 3.11+、jsonschema，以及 operators/catalog.json 指向的本地文件。

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError


EXPECTED_GOVERNANCE = {
    "permission_decision": "harness_policy",
    "outcome_decision": "verifier",
    "sensitive_values": "reference_only",
}
REFERENCE_LIBRARY_PROFILE = "vibe-harness-cn/reference-library-v1"
REFERENCE_ENTRY_FIELDS = (
    "id",
    "version",
    "kind",
    "origin",
    "name",
    "name_zh",
    "domain",
    "status",
    "summary",
    "core_question",
    "operation",
    "agent_use",
    "applicability",
    "source_refs",
    "governance",
    "semantics",
)
REFERENCE_SEMANTIC_FIELDS = {
    "MentalModelSpec": ("questions", "interpretation_rules", "limitations"),
    "OperatorSpec": (
        "preconditions",
        "inputs",
        "procedure",
        "effect",
        "outcomes",
        "evidence_required",
        "failure_modes",
        "recovery",
    ),
    "MethodSpec": (
        "preconditions",
        "steps",
        "stop_conditions",
        "success_conditions",
        "evidence_required",
        "failure_modes",
    ),
}


@dataclass(frozen=True)
class Issue:
    path: str
    message: str


@dataclass(frozen=True)
class LibrarySummary:
    expected_source_entries: int = 0
    source_entries: int = 0
    expected_derived_entries: int = 0
    derived_entries: int = 0
    entries: int = 0


@dataclass
class LibraryDocuments:
    catalog: dict[str, Any]
    inventory: dict[str, Any]
    packs: dict[str, dict[str, Any]]
    schema: dict[str, Any]


@dataclass(frozen=True)
class LibraryValidationResult:
    issues: list[Issue]
    summary: LibrarySummary
    documents: LibraryDocuments | None = None


def _format_path(parts: Iterable[Any]) -> str:
    rendered = "$"
    for part in parts:
        rendered += f"[{part}]" if isinstance(part, int) else f".{part}"
    return rendered


def _schema_issues(instance: Any, schema: Any, prefix: str) -> list[Issue]:
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as exc:
        raise ValueError(f"Operator Schema 自身无效：{exc.message}") from exc

    validator = Draft202012Validator(schema)
    return [
        Issue(prefix + _format_path(error.absolute_path)[1:], error.message)
        for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.absolute_path))
    ]


def validate_operator_pack_document(pack: Any, schema: Any) -> list[Issue]:
    """只执行公共 Core Contract；内容质量与完整度交给显式 Profile。"""
    return _schema_issues(pack, schema, "$")


def _mapping(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _require_profile_fields(
    value: dict[str, Any],
    fields: Iterable[str],
    path: str,
    issues: list[Issue],
) -> None:
    for field in fields:
        if field not in value:
            issues.append(Issue(f"{path}.{field}", "Reference Library Profile 缺少字段"))


def _reference_entry_issues(entry: dict[str, Any], path: str) -> list[Issue]:
    """保留本仓库参考内容的完整写法，不把它提升成公共 Schema。"""
    issues: list[Issue] = []
    _require_profile_fields(entry, REFERENCE_ENTRY_FIELDS, path, issues)
    applicability = _mapping(entry.get("applicability"))
    _require_profile_fields(applicability, ("when", "not_when"), f"{path}.applicability", issues)
    governance = _mapping(entry.get("governance"))
    _require_profile_fields(
        governance,
        ("risk_level", *EXPECTED_GOVERNANCE),
        f"{path}.governance",
        issues,
    )
    semantics = _mapping(entry.get("semantics"))
    semantic_fields = REFERENCE_SEMANTIC_FIELDS.get(entry.get("kind"), ())
    _require_profile_fields(semantics, semantic_fields, f"{path}.semantics", issues)

    for field in ("source_refs",):
        if field in entry and not _list(entry.get(field)):
            issues.append(Issue(f"{path}.{field}", "Reference Library Profile 要求至少一项"))
    for field in ("when", "not_when"):
        if field in applicability and not _list(applicability.get(field)):
            issues.append(Issue(f"{path}.applicability.{field}", "Reference Library Profile 要求至少一项"))
    for field in semantic_fields:
        if field == "effect":
            continue
        if field in semantics and not _list(semantics.get(field)):
            issues.append(Issue(f"{path}.semantics.{field}", "Reference Library Profile 要求至少一项"))
    if entry.get("kind") == "OperatorSpec" and len(_list(semantics.get("outcomes"))) < 2:
        issues.append(Issue(f"{path}.semantics.outcomes", "Reference Library Profile 要求至少两个结果"))
    if entry.get("kind") == "MethodSpec" and len(_list(semantics.get("steps"))) < 2:
        issues.append(Issue(f"{path}.semantics.steps", "Reference Library Profile 要求至少两个步骤"))
    return issues


def _safe_relative_path(
    base: Path,
    scope: Path,
    value: Any,
    path: str,
    issues: list[Issue],
) -> Path | None:
    if not isinstance(value, str) or not value.strip():
        issues.append(Issue(path, "必须是非空相对路径"))
        return None
    relative = Path(value)
    if relative.is_absolute():
        issues.append(Issue(path, "不允许绝对路径"))
        return None
    resolved = (base / relative).resolve()
    try:
        resolved.relative_to(scope.resolve())
    except ValueError:
        issues.append(Issue(path, f"路径逃逸允许范围：{value}"))
        return None
    return resolved


def catalog_path_issues(catalog_path: Path, catalog: dict[str, Any]) -> tuple[list[Issue], dict[str, Path]]:
    """解析 catalog 引用；pack/inventory 必须留在库内，Schema 必须留在项目内。"""
    issues: list[Issue] = []
    paths: dict[str, Path] = {}
    library_root = catalog_path.resolve().parent
    project_root = library_root.parent
    spec = _mapping(catalog.get("spec"))

    schema_path = _safe_relative_path(
        library_root,
        project_root,
        spec.get("schema"),
        "$.spec.schema",
        issues,
    )
    if schema_path is not None:
        paths["schema"] = schema_path

    inventory_path = _safe_relative_path(
        library_root,
        library_root,
        spec.get("source_inventory"),
        "$.spec.source_inventory",
        issues,
    )
    if inventory_path is not None:
        paths["inventory"] = inventory_path

    seen_pack_paths: set[str] = set()
    for index, item in enumerate(_list(spec.get("packs"))):
        item_path = _mapping(item).get("path")
        issue_path = f"$.spec.packs[{index}].path"
        resolved = _safe_relative_path(library_root, library_root, item_path, issue_path, issues)
        if resolved is None or not isinstance(item_path, str):
            continue
        if item_path in seen_pack_paths:
            issues.append(Issue(issue_path, f"pack 路径重复：{item_path}"))
        else:
            seen_pack_paths.add(item_path)
            paths[f"pack:{item_path}"] = resolved
    return issues, paths


def validate_operator_library(catalog_path: Path, load_json: Any) -> LibraryValidationResult:
    catalog = load_json(catalog_path.resolve())
    if not isinstance(catalog, dict):
        return LibraryValidationResult([Issue("$", "catalog 必须是 object")], LibrarySummary())
    path_issues, paths = catalog_path_issues(catalog_path, catalog)
    if path_issues:
        return LibraryValidationResult(path_issues, LibrarySummary())
    try:
        inventory = load_json(paths["inventory"])
        schema = load_json(paths["schema"])
        packs = {
            key.removeprefix("pack:"): load_json(path)
            for key, path in paths.items()
            if key.startswith("pack:")
        }
    except KeyError as exc:
        return LibraryValidationResult(
            [Issue("$.spec", f"缺少必要路径：{exc.args[0]}")],
            LibrarySummary(),
        )
    if not isinstance(inventory, dict) or not isinstance(schema, dict) or any(
        not isinstance(pack, dict) for pack in packs.values()
    ):
        return LibraryValidationResult(
            [Issue("$", "catalog、inventory、Schema 和 pack 都必须是 JSON object")],
            LibrarySummary(),
        )
    documents = LibraryDocuments(catalog, inventory, packs, schema)
    result = validate_operator_library_documents(documents)
    return LibraryValidationResult(result.issues, result.summary, documents)


def validate_operator_library_documents(documents: LibraryDocuments) -> LibraryValidationResult:
    issues: list[Issue] = []
    catalog = documents.catalog
    inventory = documents.inventory
    packs = documents.packs

    if catalog.get("api_version") != "vibe-harness-cn.dev/v1alpha1":
        issues.append(Issue("$.api_version", "catalog api_version 不受支持"))
    if catalog.get("kind") != "OperatorLibraryCatalog":
        issues.append(Issue("$.kind", "catalog kind 必须是 OperatorLibraryCatalog"))
    if inventory.get("kind") != "OperatorSourceInventory":
        issues.append(Issue("inventory:$.kind", "inventory kind 必须是 OperatorSourceInventory"))

    catalog_spec = _mapping(catalog.get("spec"))
    inventory_spec = _mapping(inventory.get("spec"))
    catalog_packs = _list(catalog_spec.get("packs"))
    domains = _list(inventory_spec.get("domains"))
    expected_total = inventory_spec.get("expected_source_entries")
    if catalog_spec.get("conformance_profile") != REFERENCE_LIBRARY_PROFILE:
        issues.append(
            Issue(
                "$.spec.conformance_profile",
                f"参考库必须显式声明 {REFERENCE_LIBRARY_PROFILE}",
            )
        )
    if not isinstance(expected_total, int) or isinstance(expected_total, bool) or expected_total < 1:
        issues.append(Issue("inventory:$.spec.expected_source_entries", "必须是正整数"))
        expected_total = 0

    expected_by_key: dict[str, tuple[str, dict[str, Any]]] = {}
    inventory_domain_counts: dict[str, int] = {}
    for domain_index, domain_value in enumerate(domains):
        domain = _mapping(domain_value)
        domain_id = domain.get("id")
        entries = _list(domain.get("entries"))
        prefix = f"inventory:$.spec.domains[{domain_index}]"
        if not isinstance(domain_id, str) or not domain_id:
            issues.append(Issue(f"{prefix}.id", "domain id 必须是非空字符串"))
            continue
        if domain_id in inventory_domain_counts:
            issues.append(Issue(f"{prefix}.id", f"inventory domain 重复：{domain_id}"))
        inventory_domain_counts[domain_id] = len(entries)
        declared_domain_count = domain.get("expected_count")
        if type(declared_domain_count) is not int or declared_domain_count != len(entries):
            issues.append(Issue(f"{prefix}.expected_count", "声明计数与 entries 实际数量不一致"))
        for entry_index, entry_value in enumerate(entries):
            entry = _mapping(entry_value)
            source_key = entry.get("source_key")
            entry_path = f"{prefix}.entries[{entry_index}]"
            if not isinstance(source_key, str) or not source_key:
                issues.append(Issue(f"{entry_path}.source_key", "source_key 必须是非空字符串"))
                continue
            if not source_key.startswith(f"{domain_id}."):
                issues.append(Issue(f"{entry_path}.source_key", "source_key 必须使用所属 domain 前缀"))
            if source_key in expected_by_key:
                issues.append(Issue(f"{entry_path}.source_key", f"inventory source_key 重复：{source_key}"))
            else:
                expected_by_key[source_key] = (domain_id, entry)
    if expected_total != len(expected_by_key):
        issues.append(
            Issue(
                "inventory:$.spec.expected_source_entries",
                f"声明 {expected_total}，唯一 source 条目实际为 {len(expected_by_key)}",
            )
        )

    reference_ids: set[str] = set()
    for index, value in enumerate(_list(inventory_spec.get("reference_frameworks"))):
        reference_id = _mapping(value).get("id")
        path = f"inventory:$.spec.reference_frameworks[{index}].id"
        if not isinstance(reference_id, str) or not reference_id:
            issues.append(Issue(path, "reference id 必须是非空字符串"))
        elif reference_id in reference_ids:
            issues.append(Issue(path, f"reference id 重复：{reference_id}"))
        else:
            reference_ids.add(reference_id)

    actual_by_key: dict[str, tuple[str, dict[str, Any]]] = {}
    all_ids: set[str] = set()
    entries_by_id: dict[str, dict[str, Any]] = {}
    all_entries: list[tuple[str, int, dict[str, Any]]] = []
    source_count = 0
    derived_count = 0
    catalog_domains: set[str] = set()

    for catalog_index, catalog_item_value in enumerate(catalog_packs):
        catalog_item = _mapping(catalog_item_value)
        domain_id = catalog_item.get("domain")
        relative_path = catalog_item.get("path")
        prefix = f"$.spec.packs[{catalog_index}]"
        if not isinstance(domain_id, str) or not domain_id:
            issues.append(Issue(f"{prefix}.domain", "domain 必须是非空字符串"))
            continue
        if domain_id in catalog_domains:
            issues.append(Issue(f"{prefix}.domain", f"catalog domain 重复：{domain_id}"))
        catalog_domains.add(domain_id)
        if not isinstance(relative_path, str) or relative_path not in packs:
            issues.append(Issue(f"{prefix}.path", f"pack 未装载：{relative_path}"))
            continue
        pack = packs[relative_path]
        pack_prefix = f"pack:{relative_path}:$"
        issues.extend(_schema_issues(pack, documents.schema, pack_prefix))
        metadata = _mapping(pack.get("metadata"))
        entries = _list(pack.get("entries"))
        _require_profile_fields(
            metadata,
            ("id", "version", "domain", "title", "summary", "source_entry_count", "derived_entry_count"),
            f"{pack_prefix}.metadata",
            issues,
        )
        if metadata.get("domain") != domain_id:
            issues.append(Issue(f"{pack_prefix}.metadata.domain", "pack domain 与 catalog 不一致"))
        pack_source_count = 0
        pack_derived_count = 0
        for entry_index, entry_value in enumerate(entries):
            entry = _mapping(entry_value)
            all_entries.append((relative_path, entry_index, entry))
            entry_path = f"{pack_prefix}.entries[{entry_index}]"
            issues.extend(_reference_entry_issues(entry, entry_path))
            entry_id = entry.get("id")
            if isinstance(entry_id, str):
                if entry_id in all_ids:
                    issues.append(Issue(f"{entry_path}.id", f"entry id 重复：{entry_id}"))
                else:
                    all_ids.add(entry_id)
                    entries_by_id[entry_id] = entry
            if entry.get("domain") != domain_id:
                issues.append(Issue(f"{entry_path}.domain", "entry domain 与 pack 不一致"))
            origin = entry.get("origin")
            if origin == "source":
                pack_source_count += 1
                source_count += 1
                source_key = entry.get("source_key")
                if isinstance(source_key, str):
                    if source_key in actual_by_key:
                        issues.append(Issue(f"{entry_path}.source_key", f"库中 source_key 重复：{source_key}"))
                    else:
                        actual_by_key[source_key] = (domain_id, entry)
            elif origin == "derived":
                pack_derived_count += 1
                derived_count += 1
                if entry.get("kind") != "MethodSpec":
                    issues.append(Issue(f"{entry_path}.kind", "derived 条目只能是 MethodSpec"))
            else:
                issues.append(Issue(f"{entry_path}.origin", "Reference Library Profile 只接受 source 或 derived"))
            governance = _mapping(entry.get("governance"))
            for field, expected in EXPECTED_GOVERNANCE.items():
                if governance.get(field) != expected:
                    issues.append(Issue(f"{entry_path}.governance.{field}", f"必须是 {expected}"))
            for ref_index, reference_id in enumerate(_list(entry.get("source_refs"))):
                if reference_id not in reference_ids:
                    issues.append(
                        Issue(
                            f"{entry_path}.source_refs[{ref_index}]",
                            f"来源引用不存在：{reference_id}",
                        )
                    )
        for owner, field, declared, actual in (
            ("catalog", "source_entry_count", catalog_item.get("source_entry_count"), pack_source_count),
            ("catalog", "derived_entry_count", catalog_item.get("derived_entry_count"), pack_derived_count),
            ("pack", "source_entry_count", metadata.get("source_entry_count"), pack_source_count),
            ("pack", "derived_entry_count", metadata.get("derived_entry_count"), pack_derived_count),
        ):
            if type(declared) is not int or declared != actual:
                location = prefix if owner == "catalog" else f"{pack_prefix}.metadata"
                issues.append(Issue(f"{location}.{field}", f"声明 {declared}，实际 {actual}"))

    registered_pack_paths = {
        path
        for item in map(_mapping, catalog_packs)
        if isinstance(path := item.get("path"), str)
    }
    unloaded = sorted(set(packs) - registered_pack_paths)
    for path in unloaded:
        issues.append(Issue("$.spec.packs", f"装载了 catalog 未登记的 pack：{path}"))
    missing_domains = sorted(set(inventory_domain_counts) - catalog_domains)
    extra_domains = sorted(catalog_domains - set(inventory_domain_counts))
    if missing_domains:
        issues.append(Issue("$.spec.packs", f"缺少 inventory domain：{', '.join(missing_domains)}"))
    if extra_domains:
        issues.append(Issue("$.spec.packs", f"存在 inventory 未登记 domain：{', '.join(extra_domains)}"))

    missing_keys = sorted(set(expected_by_key) - set(actual_by_key))
    extra_keys = sorted(set(actual_by_key) - set(expected_by_key))
    if missing_keys:
        issues.append(Issue("$.source_coverage", f"缺少 source 条目：{', '.join(missing_keys)}"))
    if extra_keys:
        issues.append(Issue("$.source_coverage", f"存在清单外 source 条目：{', '.join(extra_keys)}"))
    for source_key in sorted(set(expected_by_key) & set(actual_by_key)):
        expected_domain, expected = expected_by_key[source_key]
        actual_domain, actual = actual_by_key[source_key]
        for field, actual_value in (
            ("domain", actual_domain),
            ("name", actual.get("name")),
            ("name_zh", actual.get("name_zh")),
            ("expected_kind", actual.get("kind")),
            ("id", actual.get("id")),
        ):
            if field == "domain":
                expected_value = expected_domain
            elif field == "id":
                expected_value = f"psoa.{source_key}"
            else:
                expected_value = expected.get(field)
            if actual_value != expected_value:
                issues.append(
                    Issue(
                        f"source:{source_key}.{field}",
                        f"inventory={expected_value!r}，library={actual_value!r}",
                    )
                )

    method_graph: dict[str, set[str]] = {}
    for relative_path, entry_index, entry in all_entries:
        if entry.get("kind") != "MethodSpec":
            continue
        entry_id = entry.get("id")
        if isinstance(entry_id, str):
            method_graph.setdefault(entry_id, set())
        steps = _list(_mapping(entry.get("semantics")).get("steps"))
        orders = [_mapping(step).get("order") for step in steps]
        if orders != list(range(1, len(steps) + 1)):
            issues.append(
                Issue(
                    f"pack:{relative_path}:$.entries[{entry_index}].semantics.steps",
                    "Method step order 必须从 1 连续递增",
                )
            )
        for step_index, step_value in enumerate(steps):
            use = _mapping(step_value).get("use")
            step_path = f"pack:{relative_path}:$.entries[{entry_index}].semantics.steps[{step_index}]"
            if isinstance(use, str):
                target = entries_by_id.get(use)
                if target is None:
                    issues.append(Issue(f"{step_path}.use", f"Method 引用不存在：{use}"))
                elif target.get("kind") == "MentalModelSpec":
                    issues.append(Issue(f"{step_path}.use", "MentalModelSpec 必须通过 apply_model 应用"))
                elif target.get("kind") == "MethodSpec" and isinstance(entry_id, str):
                    method_graph[entry_id].add(use)
            apply_model = _mapping(step_value).get("apply_model")
            if isinstance(apply_model, str):
                target = entries_by_id.get(apply_model)
                if target is None:
                    issues.append(Issue(f"{step_path}.apply_model", f"思维模型引用不存在：{apply_model}"))
                elif target.get("kind") != "MentalModelSpec":
                    issues.append(Issue(f"{step_path}.apply_model", "apply_model 只能引用 MentalModelSpec"))

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(method_id: str, trail: list[str]) -> None:
        if method_id in visiting:
            start = trail.index(method_id)
            cycle = trail[start:]
            issues.append(Issue("$.method_graph", f"Method 引用形成循环：{' -> '.join(cycle)}"))
            return
        if method_id in visited:
            return
        visiting.add(method_id)
        for target in sorted(method_graph.get(method_id, set())):
            visit(target, trail + [target])
        visiting.remove(method_id)
        visited.add(method_id)

    for method_id in sorted(method_graph):
        visit(method_id, [method_id])

    totals = _mapping(catalog_spec.get("totals"))
    actual_total = source_count + derived_count
    expected_derived = totals.get("derived_entries")
    if type(expected_derived) is not int:
        expected_derived = 0
    for field, actual in (
        ("source_entries", source_count),
        ("derived_entries", derived_count),
        ("entries", actual_total),
    ):
        if type(totals.get(field)) is not int or totals.get(field) != actual:
            issues.append(Issue(f"$.spec.totals.{field}", f"声明 {totals.get(field)}，实际 {actual}"))
    invariants = _mapping(catalog_spec.get("invariants"))
    for field, expected in {
        "source_coverage": "exact",
        "unique_ids": True,
        "references_must_resolve": True,
        **EXPECTED_GOVERNANCE,
    }.items():
        if invariants.get(field) != expected:
            issues.append(Issue(f"$.spec.invariants.{field}", f"必须是 {expected!r}"))

    return LibraryValidationResult(
        issues,
        LibrarySummary(
            expected_source_entries=expected_total,
            source_entries=source_count,
            expected_derived_entries=expected_derived,
            derived_entries=derived_count,
            entries=actual_total,
        ),
        documents,
    )
