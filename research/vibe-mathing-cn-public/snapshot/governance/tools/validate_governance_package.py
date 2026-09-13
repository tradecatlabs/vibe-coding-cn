#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote

sys.dont_write_bytecode = True

from governance_context_bundle import ROUTES

GOV_ROOT = Path("governance")

REQUIRED = [
    "README.md",
    "INDEX.md",
    "CHANGELOG.md",
    "context/AGENT-ENTRY.md",
    "context/CONTEXT-MAP.md",
    "context/CONTEXT-ROUTER.md",
    "context/PROJECT-TOPOLOGY.md",
    "standards/工程质量标准.md",
    "standards/劣质代码定义.md",
    "standards/非功能性需求标准.md",
    "processes/代理协作协议.md",
    "processes/RPI研究计划实施流程.md",
    "processes/QA计划标准.md",
    "processes/本地工具与验证入口.md",
    "architecture-gates/门禁与护栏.md",
    "architecture-gates/GATE-INDEX.md",
    "architecture-gates/rules/INDEX.md",
    "decisions/adr/INDEX.md",
    "evidence/postmortems/INDEX.md",
    "evidence/lessons/INDEX.md",
    "evidence/qa-plans/INDEX.md",
    "agent-governance/agent-feedback/INDEX.md",
    "templates/ADR.template.md",
    "templates/GATE.template.md",
    "templates/QA.template.md",
    "templates/AGENT-FEEDBACK.template.md",
    "tools/README.md",
    "tasks/README.md",
    "tasks/lessons.md",
    "runtime/README.md",
    "archive/README.md",
]

DOCUMENT_DRIVEN_REQUIRED = [
    "context/PROJECT_OPERATING_MODEL.md",
    "processes/DOCUMENT_DRIVEN_DEVELOPMENT.md",
    "context/TOOLCHAIN_MODEL.md",
    "context/project_operating_model_contract.v1.yaml",
]

PROJECT_OPERATING_MODEL_SECTIONS = [
    "项目一句话定义",
    "业务模型",
    "技术模型",
    "工具链模型",
    "目录和真相源地图",
    "验证入口",
    "最近一次 review",
]

DOCUMENT_DRIVEN_SECTIONS = [
    "适用范围",
    "执行顺序",
    "文档影响分类",
    "Closeout 必填判断",
    "不接受的做法",
]

TOOLCHAIN_MODEL_SECTIONS = [
    "成熟工具优先",
    "项目命令",
    "禁止或谨慎使用",
    "工具链变更流程",
]

CONTRACT_REQUIRED_KEYS = [
    "version:",
    "required_documents:",
    "closeout_required_fields:",
    "validation:",
]

REQUIRED_DIRS = [
    "context/module-contexts",
    "architecture-gates/rules",
    "tasks",
    "runtime/runs",
    "runtime/tmp",
]

EMBEDDED_TOOLS = [
    "tools/init_governance_package.py",
    "tools/new_governance_record.py",
    "tools/new_module_context.py",
    "tools/rebuild_governance_index.py",
    "tools/validate_governance_package.py",
    "tools/governance_health_report.py",
    "tools/governance_context_bundle.py",
    "tools/scan_principle_gates.py",
]

FRONTMATTER_REQUIRED = {"id", "type", "status", "owner", "last_reviewed"}
DATE_FIELDS = {"created", "last_reviewed"}
VALID_STATUSES = {"draft", "active", "current", "deprecated", "archived", "converted", "rejected"}
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
TASKS_DOC_ROOTS = {"tasks"}
RECORD_DIR_PREFIXES = {
    Path("decisions/adr"): "ADR",
    Path("evidence/reviews"): "REVIEW",
    Path("evidence/postmortems"): "POSTMORTEM",
    Path("evidence/lessons"): "LESSON",
    Path("evidence/workorders"): "WO",
    Path("evidence/tech-debt"): "DEBT",
    Path("architecture-gates/rules"): "GATE",
    Path("evidence/qa-plans"): "QA",
    Path("agent-governance/agent-feedback"): "AF",
    Path("evidence/baselines"): "BASELINE",
    Path("control-plane/controls"): "CONTROL",
    Path("evidence/exceptions"): "EXCEPTION",
    Path("risk-register"): "RISK",
    Path("evidence/conformance"): "CONFORMANCE",
    Path("evidence/audit-exports"): "AUDIT",
    Path("evidence/releases"): "RELEASE",
}


def parse_frontmatter(text: str) -> dict[str, str] | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end == -1:
        return None
    raw = text[4:end].splitlines()
    data: dict[str, str] = {}
    for line in raw:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip()
    return data


def check_gate(path: Path, text: str, issues: list[dict[str, str]]) -> None:
    required_sections = ["阻止条件", "原因", "检查方式", "可操作错误提示", "最小修复"]
    for section in required_sections:
        if f"## {section}" not in text:
            issues.append({"severity": "BLOCK", "path": str(path), "message": f"gate missing section: {section}"})
    fm = parse_frontmatter(text) or {}
    for field in ["severity", "detectability", "source"]:
        if not fm.get(field, "").strip():
            issues.append({"severity": "BLOCK", "path": str(path), "message": f"gate missing field: {field}"})


def is_valid_date(value: str) -> bool:
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return False
    return True


def check_frontmatter_values(path: Path, fm: dict[str, str], issues: list[dict[str, str]]) -> None:
    doc_id = fm.get("id", "")
    if doc_id and not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", doc_id):
        issues.append({"severity": "WARN", "path": str(path), "message": f"frontmatter id has unstable characters: {doc_id}"})

    status = fm.get("status", "")
    if status and status not in VALID_STATUSES:
        issues.append({"severity": "WARN", "path": str(path), "message": f"unknown status: {status}"})

    for field in DATE_FIELDS:
        value = fm.get(field)
        if value and not is_valid_date(value):
            issues.append({"severity": "WARN", "path": str(path), "message": f"{field} must use YYYY-MM-DD"})

    review_cycle = fm.get("review_cycle")
    if review_cycle and not re.fullmatch(r"P\d+D", review_cycle):
        issues.append({"severity": "WARN", "path": str(path), "message": "review_cycle must use ISO day duration like P90D"})


def check_record_location(rel: Path, fm: dict[str, str], issues: list[dict[str, str]]) -> None:
    if rel.name == "INDEX.md":
        return
    prefix = RECORD_DIR_PREFIXES.get(rel.parent)
    if not prefix:
        return
    doc_id = fm.get("id", "")
    expected = f"{prefix}-NNNN"
    if not re.fullmatch(rf"{re.escape(prefix)}-\d{{4}}", doc_id):
        issues.append(
            {
                "severity": "BLOCK",
                "path": str(rel),
                "message": f"record id must match directory prefix: expected {expected}, got {doc_id or '<empty>'}",
            }
        )


def target_is_external(target: str) -> bool:
    return bool(re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target)) or target.startswith("#")


def markdown_link_destination(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<"):
        end = target.find(">")
        if end != -1:
            return target[1:end].strip()
    parts = target.split(None, 1)
    return parts[0].strip() if parts else ""


def resolve_markdown_link(project_root: Path, root: Path, current_file: Path, target: str) -> Path | None:
    target = unquote(markdown_link_destination(target))
    if not target or target_is_external(target):
        return None
    target = target.split("#", 1)[0].strip()
    if not target:
        return None
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1].strip()
    if target.startswith(str(GOV_ROOT) + "/"):
        return (project_root / target).resolve()
    if target.startswith("/"):
        return (project_root / target.lstrip("/")).resolve()
    return (current_file.parent / target).resolve()


def check_markdown_links(project_root: Path, root: Path, rel: Path, text: str, issues: list[dict[str, str]]) -> None:
    current_file = root / rel
    for match in MARKDOWN_LINK_RE.finditer(text):
        raw_target = match.group(1).strip()
        target_path = resolve_markdown_link(project_root, root, current_file, raw_target)
        if target_path is None:
            continue
        try:
            target_path.relative_to(project_root.resolve())
        except ValueError:
            issues.append({"severity": "WARN", "path": str(rel), "message": f"markdown link escapes project root: {raw_target}"})
            continue
        if not target_path.exists():
            issues.append({"severity": "WARN", "path": str(rel), "message": f"broken markdown link: {raw_target}"})


def table_cells(line: str) -> list[str]:
    cells: list[str] = []
    cell: list[str] = []
    escaped = False
    for char in line.strip():
        if char == "|" and not escaped:
            cells.append("".join(cell).strip())
            cell = []
        else:
            cell.append(char)
        if char == "\\" and not escaped:
            escaped = True
        else:
            escaped = False
    cells.append("".join(cell).strip())
    if cells and cells[0] == "":
        cells = cells[1:]
    if cells and cells[-1] == "":
        cells = cells[:-1]
    return cells


def is_table_line(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("|") and stripped.count("|") >= 2


def is_table_separator(line: str) -> bool:
    cells = table_cells(line)
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


def check_markdown_tables(rel: Path, text: str, issues: list[dict[str, str]]) -> None:
    lines = text.splitlines()
    in_fence = False
    index = 0
    while index < len(lines):
        stripped = lines[index].strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            index += 1
            continue
        if in_fence or not is_table_line(lines[index]):
            index += 1
            continue
        if index + 1 >= len(lines) or not is_table_separator(lines[index + 1]):
            index += 1
            continue
        expected = len(table_cells(lines[index]))
        row_index = index + 1
        while row_index < len(lines) and is_table_line(lines[row_index]):
            actual = len(table_cells(lines[row_index]))
            if actual != expected:
                issues.append(
                    {
                        "severity": "BLOCK",
                        "path": str(rel),
                        "message": f"markdown table row has {actual} cells, expected {expected} at line {row_index + 1}",
                    }
                )
            row_index += 1
        index = row_index


def clean_table_cell_id(value: str) -> str:
    return value.strip().strip("`").strip()


def check_duplicate_index_table_ids(rel: Path, text: str, issues: list[dict[str, str]]) -> None:
    lines = text.splitlines()
    in_fence = False
    index = 0
    while index < len(lines):
        stripped = lines[index].strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            index += 1
            continue
        if in_fence or not is_table_line(lines[index]):
            index += 1
            continue
        if index + 1 >= len(lines) or not is_table_separator(lines[index + 1]):
            index += 1
            continue
        header = [clean_table_cell_id(cell) for cell in table_cells(lines[index])]
        row_index = index + 2
        seen: dict[str, int] = {}
        if header and header[0] in {"ID", "Gate ID"}:
            while row_index < len(lines) and is_table_line(lines[row_index]):
                cells = table_cells(lines[row_index])
                if cells:
                    record_id = clean_table_cell_id(cells[0])
                    if re.fullmatch(r"[A-Z][A-Z0-9-]*-\d{4}", record_id):
                        if record_id in seen:
                            issues.append(
                                {
                                    "severity": "BLOCK",
                                    "path": str(rel),
                                    "message": f"duplicate index id: {record_id} at lines {seen[record_id]} and {row_index + 1}",
                                }
                            )
                        else:
                            seen[record_id] = row_index + 1
                row_index += 1
        else:
            while row_index < len(lines) and is_table_line(lines[row_index]):
                row_index += 1
        index = row_index


def check_duplicate_ids(ids: dict[str, list[str]], issues: list[dict[str, str]]) -> None:
    for doc_id, paths in sorted(ids.items()):
        if len(paths) > 1:
            issues.append({"severity": "BLOCK", "path": ", ".join(paths), "message": f"duplicate frontmatter id: {doc_id}"})


def is_task_doc(rel: Path) -> bool:
    return bool(rel.parts) and rel.parts[0] in TASKS_DOC_ROOTS


def document_driven_enabled(root: Path) -> bool:
    return any((root / rel).exists() for rel in DOCUMENT_DRIVEN_REQUIRED)


def check_required_sections(
    root: Path,
    rel: str,
    sections: list[str],
    issues: list[dict[str, str]],
) -> None:
    path = root / rel
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    for section in sections:
        if f"## {section}" not in text:
            issues.append({"severity": "BLOCK", "path": rel, "message": f"document-driven doc missing section: {section}"})


def check_contract_keys(root: Path, rel: str, keys: list[str], issues: list[dict[str, str]]) -> None:
    path = root / rel
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    for key in keys:
        if key not in text:
            issues.append({"severity": "BLOCK", "path": rel, "message": f"operating model contract missing key: {key}"})


def check_route_index_contract(root: Path, issues: list[dict[str, str]]) -> None:
    index_path = root / "INDEX.md"
    if not index_path.is_file():
        return
    index_text = index_path.read_text(encoding="utf-8")
    classifications: dict[str, str] = {}
    for status, rel in re.findall(r"- \[(OK|optional)\] `([^`]+)`", index_text):
        classifications[rel] = status

    for route_name, route in ROUTES.items():
        for rel in route["required"]:
            classification = classifications.get(rel)
            if classification == "optional":
                issues.append(
                    {
                        "severity": "BLOCK",
                        "path": "INDEX.md",
                        "message": f"route {route_name} requires a document classified optional: {rel}",
                    }
                )
            if classification == "OK" and not (root / rel).exists():
                issues.append(
                    {
                        "severity": "BLOCK",
                        "path": rel,
                        "message": f"route {route_name} requires an indexed document that is missing",
                    }
                )


def validate(project_root: Path, strict: bool) -> dict[str, object]:
    root = project_root / GOV_ROOT
    issues: list[dict[str, str]] = []
    ids: dict[str, list[str]] = {}
    if not root.exists():
        return {
            "decision": "BLOCK",
            "root": str(root),
            "issues": [{"severity": "BLOCK", "path": str(root), "message": "governance package missing"}],
        }

    for rel in REQUIRED:
        path = root / rel
        if not path.exists():
            issues.append({"severity": "BLOCK", "path": str(path), "message": "required file missing"})

    if document_driven_enabled(root):
        for rel in DOCUMENT_DRIVEN_REQUIRED:
            path = root / rel
            if not path.exists():
                issues.append({"severity": "BLOCK", "path": str(path), "message": "document-driven operating model file missing"})
        if strict:
            check_required_sections(root, "context/PROJECT_OPERATING_MODEL.md", PROJECT_OPERATING_MODEL_SECTIONS, issues)
            check_required_sections(root, "processes/DOCUMENT_DRIVEN_DEVELOPMENT.md", DOCUMENT_DRIVEN_SECTIONS, issues)
            check_required_sections(root, "context/TOOLCHAIN_MODEL.md", TOOLCHAIN_MODEL_SECTIONS, issues)
            check_contract_keys(root, "context/project_operating_model_contract.v1.yaml", CONTRACT_REQUIRED_KEYS, issues)

    for rel in REQUIRED_DIRS:
        path = root / rel
        if not path.exists():
            issues.append({"severity": "WARN", "path": str(path), "message": "recommended directory missing"})

    if strict:
        for rel in EMBEDDED_TOOLS:
            path = root / rel
            if not path.exists():
                issues.append({"severity": "WARN", "path": str(path), "message": "embedded maintenance tool missing"})

    for path in root.rglob("*.md"):
        rel = path.relative_to(root)
        text = path.read_text(encoding="utf-8")
        if is_task_doc(rel):
            if strict:
                check_markdown_links(project_root, root, rel, text, issues)
            continue
        fm = parse_frontmatter(text)
        if fm is None:
            severity = "WARN" if "template" in path.name.lower() or path.name == "INDEX.md" else "BLOCK"
            issues.append({"severity": severity, "path": str(rel), "message": "missing frontmatter"})
        elif strict:
            if fm.get("id"):
                ids.setdefault(fm["id"], []).append(str(rel))
            missing = sorted(field for field in FRONTMATTER_REQUIRED if not fm.get(field, "").strip())
            if missing:
                issues.append({"severity": "BLOCK", "path": str(rel), "message": f"frontmatter missing: {', '.join(missing)}"})
            check_frontmatter_values(rel, fm, issues)
            check_record_location(rel, fm, issues)
            check_markdown_links(project_root, root, rel, text, issues)
            check_markdown_tables(rel, text, issues)
            check_duplicate_index_table_ids(rel, text, issues)
        if "/architecture-gates/rules/" in f"/{rel.as_posix()}/" and path.name.startswith("GATE-"):
            check_gate(rel, text, issues)

    if strict:
        check_duplicate_ids(ids, issues)
        check_route_index_contract(root, issues)

    index = root / "INDEX.md"
    if index.exists():
        content = index.read_text(encoding="utf-8")
        for rel in ["context/AGENT-ENTRY.md", "architecture-gates/GATE-INDEX.md", "standards/工程质量标准.md"]:
            if rel not in content:
                issues.append({"severity": "WARN", "path": "INDEX.md", "message": f"index does not mention {rel}"})

    gate_index = root / "architecture-gates" / "GATE-INDEX.md"
    if gate_index.exists() and "Gate ID" not in gate_index.read_text(encoding="utf-8"):
        issues.append({"severity": "WARN", "path": str(gate_index.relative_to(root)), "message": "GATE-INDEX missing table header"})

    decision = "PASS"
    if any(issue["severity"] == "BLOCK" for issue in issues):
        decision = "BLOCK"
    elif issues:
        decision = "WARN"
    return {"decision": decision, "root": str(root), "issue_count": len(issues), "issues": issues}


def render_markdown(result: dict[str, object]) -> str:
    lines = [
        "# Governance Package Validation",
        "",
        f"- `decision`: {result['decision']}",
        f"- `root`: {result['root']}",
        f"- `issue_count`: {result.get('issue_count', len(result['issues']))}",
        "",
        "## Issues",
    ]
    issues = result["issues"]
    if not issues:
        lines.append("- none")
    else:
        for issue in issues:
            lines.append(f"- `{issue['severity']}` `{issue['path']}`: {issue['message']}")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate an governance package.")
    parser.add_argument("--project-root", default=".", help="Target project root.")
    parser.add_argument("--strict", action="store_true", help="Enable stricter frontmatter checks.")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = validate(Path(args.project_root).resolve(), args.strict)
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(result))
    return 1 if result["decision"] == "BLOCK" else 0


if __name__ == "__main__":
    raise SystemExit(main())
