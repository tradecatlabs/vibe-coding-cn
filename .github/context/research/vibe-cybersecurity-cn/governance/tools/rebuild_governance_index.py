#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path


GOV_ROOT = Path("governance")

RECORD_DIRS = {
    "ADR": Path("decisions/adr"),
    "REVIEW": Path("evidence/reviews"),
    "POSTMORTEM": Path("evidence/postmortems"),
    "LESSON": Path("evidence/lessons"),
    "WO": Path("evidence/workorders"),
    "DEBT": Path("evidence/tech-debt"),
    "GATE": Path("architecture-gates/rules"),
    "QA": Path("evidence/qa-plans"),
    "AF": Path("agent-governance/agent-feedback"),
    "BASELINE": Path("evidence/baselines"),
    "CONTROL": Path("control-plane/controls"),
    "EXCEPTION": Path("evidence/exceptions"),
    "RISK": Path("risk-register"),
    "CONFORMANCE": Path("evidence/conformance"),
    "AUDIT": Path("evidence/audit-exports"),
    "RELEASE": Path("evidence/releases"),
}


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}
    data: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip()
    return data


def title_from_markdown(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def strip_record_id_prefix(title: str, record_id: str) -> str:
    prefix = f"{record_id} "
    if not title.startswith(prefix):
        return title
    stripped = title[len(prefix) :].strip()
    return stripped or title


def fallback_id(path: Path, prefix: str) -> str:
    match = re.match(rf"^({re.escape(prefix)}-\d{{4}})", path.stem)
    return match.group(1) if match else path.stem


def is_record_file(path: Path, prefix: str, fm: dict[str, str]) -> bool:
    if path.name == "INDEX.md":
        return False
    if "id" in fm and not re.fullmatch(rf"{re.escape(prefix)}-\d{{4}}", fm["id"]):
        raise SystemExit(f"Record id prefix mismatch in {path}: expected {prefix}-NNNN, got {fm['id'] or '<empty>'}")
    record_id = fm.get("id", fallback_id(path, prefix))
    return bool(re.fullmatch(rf"{re.escape(prefix)}-\d{{4}}", record_id))


def escape_table_cell(value: str) -> str:
    return value.replace("|", r"\|")


def record_rows(directory: Path, prefix: str) -> list[tuple[str, str, str, str]]:
    rows = []
    if not directory.exists():
        return rows
    for path in sorted(directory.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        if not is_record_file(path, prefix, fm):
            continue
        record_id = fm.get("id", fallback_id(path, prefix))
        rows.append(
            (
                record_id,
                strip_record_id_prefix(title_from_markdown(text, path.stem), record_id),
                fm.get("status", "unknown"),
                path.name,
            )
        )
    return rows


def gate_rows(root: Path) -> list[tuple[str, str, str, str, str, str, str]]:
    directory = root / "architecture-gates" / "rules"
    rows = []
    for path in sorted(directory.glob("*.md")) if directory.exists() else []:
        text = path.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        if not is_record_file(path, "GATE", fm):
            continue
        record_id = fm.get("id", fallback_id(path, "GATE"))
        rows.append(
            (
                record_id,
                fm.get("severity", "UNKNOWN"),
                strip_record_id_prefix(title_from_markdown(text, path.stem), record_id),
                fm.get("detectability", "manual"),
                fm.get("source", ""),
                fm.get("status", "unknown"),
                path.name,
            )
        )
    return rows


def assert_unique_record_ids(label: str, rows: list[tuple[str, ...]]) -> None:
    seen: dict[str, str] = {}
    for row in rows:
        record_id = row[0]
        filename = row[-1]
        if record_id in seen:
            raise SystemExit(f"Duplicate governance record id in {label}: {record_id} ({seen[record_id]}, {filename})")
        seen[record_id] = filename


def write_record_index(directory: Path, title: str, rows: list[tuple[str, str, str, str]], dry_run: bool) -> Path:
    index = directory / "INDEX.md"
    today = date.today().isoformat()
    lines = [
        "---",
        f"id: IDX-{title.upper().replace(' ', '-')}",
        "type: index",
        "status: current",
        "owner: engineering",
        f"last_reviewed: {today}",
        "---",
        "",
        f"# {title}",
        "",
        "| ID | 标题 | 状态 | 文件 |",
        "|---|---|---|---|",
    ]
    for record_id, title_text, status, filename in rows:
        lines.append(
            f"| `{escape_table_cell(record_id)}` | {escape_table_cell(title_text)} | "
            f"{escape_table_cell(status)} | `{escape_table_cell(filename)}` |"
        )
    content = "\n".join(lines) + "\n"
    if not dry_run:
        directory.mkdir(parents=True, exist_ok=True)
        index.write_text(content, encoding="utf-8")
    return index


def write_gate_index(root: Path, rows: list[tuple[str, str, str, str, str, str, str]], dry_run: bool) -> Path:
    index = root / "architecture-gates" / "GATE-INDEX.md"
    today = date.today().isoformat()
    lines = [
        "---",
        "id: GATE-INDEX",
        "type: gate-index",
        "status: current",
        "owner: engineering",
        f"last_reviewed: {today}",
        "---",
        "",
        "# Gate Index",
        "",
        "| Gate ID | 严重级别 | 标题 | 检测方式 | 来源 | 状态 | 文件 |",
        "|---|---|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| `{escape_table_cell(row[0])}` | {escape_table_cell(row[1])} | "
            f"{escape_table_cell(row[2])} | {escape_table_cell(row[3])} | "
            f"{escape_table_cell(row[4])} | {escape_table_cell(row[5])} | "
            f"`{escape_table_cell(row[6])}` |"
        )
    if not dry_run:
        index.parent.mkdir(parents=True, exist_ok=True)
        index.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return index


def write_root_index(root: Path, dry_run: bool) -> Path:
    index = root / "INDEX.md"
    sections = [
        (
            "启动入口",
            [
                ("context/AGENT-ENTRY.md", True),
                ("context/CONTEXT-MAP.md", True),
                ("context/CONTEXT-ROUTER.md", True),
                ("context/PROJECT-TOPOLOGY.md", True),
            ],
        ),
        (
            "当前标准",
            [
                ("standards/工程质量标准.md", True),
                ("standards/劣质代码定义.md", True),
                ("standards/非功能性需求标准.md", True),
                ("standards/优质代码定义.md", False),
                ("standards/性能效率优化标准.md", False),
                ("standards/可靠性标准.md", False),
                ("standards/架构设计原则.md", True),
                ("standards/工程变更安全标准.md", False),
            ],
        ),
        (
            "流程",
            [
                ("processes/代理协作协议.md", True),
                ("processes/RPI研究计划实施流程.md", True),
                ("processes/QA计划标准.md", True),
                ("processes/本地工具与验证入口.md", True),
                ("processes/代码评审标准.md", False),
                ("processes/工程变更安全审查流程.md", False),
                ("processes/文档治理规则.md", False),
            ],
        ),
        (
            "门禁",
            [
                ("architecture-gates/门禁与护栏.md", True),
                ("architecture-gates/GATE-INDEX.md", True),
                ("architecture-gates/rules/INDEX.md", True),
            ],
        ),
        (
            "记录与证据",
            [
                (str(path / "INDEX.md"), prefix in {"ADR", "POSTMORTEM", "LESSON", "QA", "AF", "BASELINE", "CONTROL", "EXCEPTION", "RISK"})
                for prefix, path in RECORD_DIRS.items()
            ],
        ),
    ]
    lines = [
        "---",
        "id: GOV-INDEX",
        "type: index",
        "status: current",
        "owner: engineering",
        f"last_reviewed: {date.today().isoformat()}",
        "---",
        "",
        "# 治理包索引",
        "",
    ]
    for heading, rels in sections:
        lines.extend([f"## {heading}", ""])
        for rel, required in rels:
            if (root / rel).exists():
                status = "OK"
            elif required:
                status = "REQUIRED-MISSING"
            else:
                status = "optional"
            lines.append(f"- [{status}] `{rel}`")
        lines.append("")
    while lines and lines[-1] == "":
        lines.pop()
    if not dry_run:
        index.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return index


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Rebuild governance package indexes.")
    parser.add_argument("--project-root", default=".", help="Target project root.")
    parser.add_argument("--dry-run", action="store_true", help="Preview index targets without writing.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.project_root).resolve() / GOV_ROOT
    if not root.exists():
        raise SystemExit(f"Governance package not found: {root}")
    rows_by_prefix = {}
    for prefix, rel_dir in RECORD_DIRS.items():
        rows = record_rows(root / rel_dir, prefix)
        assert_unique_record_ids(rel_dir.as_posix(), rows)
        rows_by_prefix[prefix] = (rel_dir, rows)
    gate_index_rows = gate_rows(root)
    assert_unique_record_ids("architecture-gates/GATE-INDEX.md", gate_index_rows)

    gate_index = write_gate_index(root, gate_index_rows, args.dry_run)
    record_indexes = []
    for prefix, (rel_dir, rows) in rows_by_prefix.items():
        record_indexes.append(write_record_index(root / rel_dir, f"{prefix} Index", rows, args.dry_run))
    root_index = write_root_index(root, args.dry_run)
    touched = [root_index, gate_index, *record_indexes]
    for path in touched:
        print(path)
    print("non_invasive: wrote only inside governance/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
