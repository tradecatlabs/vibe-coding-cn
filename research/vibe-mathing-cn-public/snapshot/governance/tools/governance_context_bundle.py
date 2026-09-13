#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path


GOV_ROOT = Path("governance")

DEFAULT_DOCS = [
    "INDEX.md",
    "context/AGENT-ENTRY.md",
    "context/PROJECT_OPERATING_MODEL.md",
    "context/PROJECT-TOPOLOGY.md",
    "context/CONTEXT-MAP.md",
    "context/CONTEXT-ROUTER.md",
]

DOCUMENT_DRIVEN_DOCS = [
    "context/PROJECT_OPERATING_MODEL.md",
    "processes/DOCUMENT_DRIVEN_DEVELOPMENT.md",
    "context/TOOLCHAIN_MODEL.md",
    "context/project_operating_model_contract.v1.yaml",
]

ROUTES = {
    "feature": {
        "label": "新功能",
        "required": [
            "standards/工程质量标准.md",
            "standards/非功能性需求标准.md",
            "processes/QA计划标准.md",
            "processes/代理协作协议.md",
        ],
        "optional": [
            "standards/优质代码定义.md",
            "standards/工程变更安全标准.md",
            "standards/术语表.md",
            "processes/工程变更安全审查流程.md",
            "decisions/adr/INDEX.md",
        ],
        "outputs": ["QA 计划或验证证据", "变更摘要", "风险等级", "副作用/兼容性/失败恢复说明", "回滚路径"],
    },
    "bugfix": {
        "label": "Bug 修复",
        "required": [
            "standards/劣质代码定义.md",
            "processes/本地工具与验证入口.md",
        ],
        "optional": [
            "evidence/postmortems/INDEX.md",
            "evidence/lessons/INDEX.md",
        ],
        "outputs": ["复现步骤", "根因结论", "回归测试或验证证据"],
    },
    "performance": {
        "label": "性能优化",
        "required": [
            "standards/非功能性需求标准.md",
            "architecture-gates/门禁与护栏.md",
        ],
        "optional": [
            "standards/性能效率优化标准.md",
            "evidence/postmortems/INDEX.md",
            "evidence/lessons/INDEX.md",
        ],
        "outputs": ["复杂度结论", "benchmark/profile 或指标证据", "性能收益与维护成本权衡"],
    },
    "architecture": {
        "label": "架构变更",
        "required": [
            "standards/工程质量标准.md",
            "standards/非功能性需求标准.md",
            "standards/架构设计原则.md",
            "decisions/adr/INDEX.md",
        ],
        "optional": [
            "evidence/tech-debt/INDEX.md",
            "processes/RPI研究计划实施流程.md",
        ],
        "outputs": ["ADR 或 ADR 更新", "边界与依赖说明", "迁移和回滚路径"],
    },
    "review": {
        "label": "代码审查",
        "required": [
            "architecture-gates/门禁与护栏.md",
        ],
        "optional": [
            "context/module-contexts/skills-auto-review/CONTEXT.md",
            "evidence/lessons/INDEX.md",
            "agent-governance/agent-feedback/INDEX.md",
        ],
        "outputs": ["PASS/WARN/BLOCK finding", "证据", "最小修复建议"],
    },
    "postmortem": {
        "label": "复盘",
        "required": [
            "architecture-gates/门禁与护栏.md",
            "evidence/postmortems/INDEX.md",
        ],
        "optional": [
            "processes/文档治理规则.md",
            "evidence/lessons/INDEX.md",
            "agent-governance/agent-feedback/INDEX.md",
        ],
        "outputs": ["根因", "防复发动作", "lesson/gate 转化判断"],
    },
    "governance": {
        "label": "治理包维护",
        "required": [
            "architecture-gates/门禁与护栏.md",
            "agent-governance/agent-feedback/INDEX.md",
        ],
        "optional": [
            "processes/文档治理规则.md",
            "evidence/lessons/INDEX.md",
            "decisions/adr/INDEX.md",
        ],
        "outputs": ["索引重建", "strict validate", "health report"],
    },
    "docs": {
        "label": "文档治理",
        "required": [
            "context/PROJECT_OPERATING_MODEL.md",
            "processes/DOCUMENT_DRIVEN_DEVELOPMENT.md",
            "context/TOOLCHAIN_MODEL.md",
            "context/CONTEXT-ROUTER.md",
        ],
        "optional": [
            "decisions/adr/INDEX.md",
            "context/module-contexts",
            "tasks/README.md",
            "tasks/lessons.md",
            "processes/文档治理规则.md",
        ],
        "outputs": ["文档同步证据", "受影响真相源清单", "无需更新的明确豁免理由", "strict validate 或缺口清单"],
    },
    "baseline": {
        "label": "基线治理",
        "required": [
            "control-plane/README.md",
            "evidence/baselines/INDEX.md",
            "evidence/verification/INDEX.md",
            "evidence/rollback/INDEX.md",
            "architecture-gates/GATE-INDEX.md",
        ],
        "optional": [
            "evidence/releases/INDEX.md",
            "evidence/compatibility/INDEX.md",
            "evidence/adoption/INDEX.md",
            "evidence/support/INDEX.md",
            "evidence/exceptions/INDEX.md",
        ],
        "outputs": ["基线证据包", "验证环境锁", "回滚验证", "例外状态", "晋级或阻断结论"],
    },
    "control": {
        "label": "控制项治理",
        "required": [
            "control-plane/README.md",
            "control-plane/controls/INDEX.md",
            "architecture-gates/GATE-INDEX.md",
        ],
        "optional": [
            "evidence/audit-exports/INDEX.md",
            "evidence/exceptions/INDEX.md",
            "risk-register/INDEX.md",
        ],
        "outputs": ["控制项覆盖", "检测方式", "证据路径", "planned/guarded/implemented 状态"],
    },
    "audit": {
        "label": "审计导出",
        "required": [
            "evidence/audit-exports/INDEX.md",
            "control-plane/README.md",
            "evidence/conformance/INDEX.md",
        ],
        "optional": [
            "evidence/verification/INDEX.md",
            "risk-register/INDEX.md",
            "evidence/exceptions/INDEX.md",
        ],
        "outputs": ["审计导出清单", "完整性证据", "provenance 或签名状态", "缺口清单"],
    },
    "risk": {
        "label": "风险治理",
        "required": [
            "risk-register/INDEX.md",
            "architecture-gates/GATE-INDEX.md",
            "evidence/exceptions/INDEX.md",
        ],
        "optional": [
            "decisions/adr/INDEX.md",
            "evidence/postmortems/INDEX.md",
            "control-plane/controls/INDEX.md",
        ],
        "outputs": ["风险记录", "缓解措施", "残余风险", "复审周期", "关联控制项"],
    },
}


ALIASES = {
    "new-feature": "feature",
    "新功能": "feature",
    "bug": "bugfix",
    "fix": "bugfix",
    "修复": "bugfix",
    "perf": "performance",
    "性能": "performance",
    "arch": "architecture",
    "架构": "architecture",
    "审查": "review",
    "复盘": "postmortem",
    "治理": "governance",
    "doc": "docs",
    "docs": "docs",
    "documentation": "docs",
    "文档": "docs",
    "文档治理": "docs",
    "baseline": "baseline",
    "基线": "baseline",
    "control": "control",
    "控制项": "control",
    "audit": "audit",
    "审计": "audit",
    "risk": "risk",
    "风险": "risk",
}


def slug_from_code_path(code_path: str) -> str:
    value = code_path.strip().strip("/").replace("\\", "/")
    chars = []
    for char in value:
        if char.isalnum() or "\u4e00" <= char <= "\u9fff":
            chars.append(char)
        else:
            chars.append("-")
    slug = "".join(chars).strip("-")
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug or "module"


def resolve_task_type(value: str) -> str:
    key = value.strip().lower()
    key = ALIASES.get(key, key)
    if key not in ROUTES:
        allowed = ", ".join(sorted(ROUTES))
        raise SystemExit(f"Unknown task type: {value}. Allowed: {allowed}")
    return key


def doc_entry(root: Path, rel: str, required: bool) -> dict[str, object]:
    path = root / rel
    return {
        "path": rel,
        "required": required,
        "exists": path.exists(),
    }


def document_driven_enabled(root: Path) -> bool:
    return any((root / rel).exists() for rel in DOCUMENT_DRIVEN_DOCS)


def unique_doc_entries(entries: list[dict[str, object]]) -> list[dict[str, object]]:
    merged: dict[str, dict[str, object]] = {}
    order: list[str] = []
    for entry in entries:
        path = str(entry["path"])
        if path not in merged:
            merged[path] = dict(entry)
            order.append(path)
            continue
        merged[path]["required"] = bool(merged[path]["required"] or entry["required"])
        merged[path]["exists"] = bool(merged[path]["exists"] or entry["exists"])
    return [merged[path] for path in order]


def module_context_entries(root: Path, code_paths: list[str]) -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    for code_path in code_paths:
        rel = Path("context/module-contexts") / slug_from_code_path(code_path) / "CONTEXT.md"
        path = root / rel
        entries.append(
            {
                "code_path": code_path,
                "path": rel.as_posix(),
                "exists": path.exists(),
            }
        )
    return entries


def build_bundle(project_root: Path, task_type: str, code_paths: list[str]) -> dict[str, object]:
    root = project_root / GOV_ROOT
    if not root.exists():
        raise SystemExit(f"Governance package not found: {root}")
    resolved = resolve_task_type(task_type)
    route = ROUTES[resolved]
    docs = [doc_entry(root, rel, True) for rel in DEFAULT_DOCS if (root / rel).exists() or rel not in DOCUMENT_DRIVEN_DOCS]
    if document_driven_enabled(root):
        docs.extend(doc_entry(root, rel, True) for rel in DOCUMENT_DRIVEN_DOCS)
    docs.extend(doc_entry(root, rel, True) for rel in route["required"])
    docs.extend(doc_entry(root, rel, False) for rel in route["optional"])
    docs = unique_doc_entries(docs)
    missing_required = [item["path"] for item in docs if item["required"] and not item["exists"]]
    module_contexts = module_context_entries(root, code_paths)
    return {
        "decision": "BLOCK" if missing_required else "PASS",
        "task_type": resolved,
        "label": route["label"],
        "root": str(root),
        "docs": docs,
        "module_contexts": module_contexts,
        "required_outputs": route["outputs"],
        "missing_required": missing_required,
        "non_invasive": "read-only; does not modify files",
    }


def render_markdown(bundle: dict[str, object]) -> str:
    lines = [
        "# Governance Context Bundle",
        "",
        f"- `decision`: {bundle['decision']}",
        f"- `task_type`: {bundle['task_type']}",
        f"- `label`: {bundle['label']}",
        f"- `root`: {bundle['root']}",
        "",
        "## Read These Documents",
        "",
    ]
    for item in bundle["docs"]:
        status = "OK" if item["exists"] else ("MISSING" if item["required"] else "optional-missing")
        required = "required" if item["required"] else "optional"
        lines.append(f"- [{status}] `{item['path']}` ({required})")
    lines.extend(["", "## Module Contexts", ""])
    module_contexts = bundle["module_contexts"]
    if module_contexts:
        for item in module_contexts:
            status = "OK" if item["exists"] else "MISSING"
            lines.append(f"- [{status}] `{item['path']}` for `{item['code_path']}`")
    else:
        lines.append("- none")
    lines.extend(["", "## Required Outputs", ""])
    for item in bundle["required_outputs"]:
        lines.append(f"- {item}")
    missing_required = bundle["missing_required"]
    if missing_required:
        lines.extend(["", "## Missing Required", ""])
        lines.extend(f"- `{item}`" for item in missing_required)
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render a governance context bundle for a task type.")
    parser.add_argument("--project-root", default=".", help="Target project root.")
    parser.add_argument("--task-type", required=True, help="feature, bugfix, performance, architecture, review, postmortem, governance.")
    parser.add_argument("--code-path", action="append", default=[], help="Relevant code path. Repeatable.")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    bundle = build_bundle(Path(args.project_root).resolve(), args.task_type, args.code_path)
    if args.format == "json":
        print(json.dumps(bundle, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(bundle))
    return 1 if bundle["decision"] == "BLOCK" else 0


if __name__ == "__main__":
    raise SystemExit(main())
