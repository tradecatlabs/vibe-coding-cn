#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path


GOV_ROOT = Path("governance")

KINDS = {
    "adr": ("ADR", Path("decisions/adr"), "record"),
    "review": ("REVIEW", Path("evidence/reviews"), "record"),
    "postmortem": ("POSTMORTEM", Path("evidence/postmortems"), "record"),
    "lesson": ("LESSON", Path("evidence/lessons"), "record"),
    "workorder": ("WO", Path("evidence/workorders"), "record"),
    "debt": ("DEBT", Path("evidence/tech-debt"), "record"),
    "gate": ("GATE", Path("architecture-gates/rules"), "gate"),
    "qa": ("QA", Path("evidence/qa-plans"), "record"),
    "agent-feedback": ("AF", Path("agent-governance/agent-feedback"), "record"),
    "baseline": ("BASELINE", Path("evidence/baselines"), "record"),
    "control": ("CONTROL", Path("control-plane/controls"), "record"),
    "exception": ("EXCEPTION", Path("evidence/exceptions"), "record"),
    "risk": ("RISK", Path("risk-register"), "record"),
    "conformance": ("CONFORMANCE", Path("evidence/conformance"), "record"),
    "audit-export": ("AUDIT", Path("evidence/audit-exports"), "record"),
    "release": ("RELEASE", Path("evidence/releases"), "record"),
}


def slugify(title: str) -> str:
    value = re.sub(r"[\\/:*?\"<>|]+", "", title.strip())
    value = re.sub(r"\s+", "-", value)
    return value[:80] or "记录"


def index_paths_for_kind(gov_root: Path, directory: Path, kind: str) -> list[Path]:
    indexes = [directory / "INDEX.md"]
    if kind == "gate":
        indexes.append(gov_root / "architecture-gates" / "GATE-INDEX.md")
    return indexes


def indexed_record_ids(gov_root: Path, directory: Path, kind: str, prefix: str) -> list[str]:
    pattern = re.compile(rf"^\|\s*`?({re.escape(prefix)}-\d{{4}})`?\s*\|")
    record_ids: list[str] = []
    for index in index_paths_for_kind(gov_root, directory, kind):
        if not index.exists():
            continue
        for line in index.read_text(encoding="utf-8").splitlines():
            match = pattern.match(line)
            if match:
                record_ids.append(match.group(1))
    return record_ids


def frontmatter_record_ids(gov_root: Path, prefix: str) -> list[str]:
    pattern = re.compile(rf"^{re.escape(prefix)}-\d{{4}}$")
    record_ids: list[str] = []
    for path in gov_root.rglob("*.md"):
        rel = path.relative_to(gov_root)
        if rel.parts and rel.parts[0] == "tasks":
            continue
        record_id = parse_frontmatter_id(path)
        if record_id and pattern.match(record_id):
            record_ids.append(record_id)
    return record_ids


def next_id(gov_root: Path, directory: Path, kind: str, prefix: str) -> str:
    highest = 0
    pattern = re.compile(rf"^{re.escape(prefix)}-(\d{{4}})")
    if directory.exists():
        for path in directory.glob(f"{prefix}-*.md"):
            match = pattern.match(path.name)
            if match:
                highest = max(highest, int(match.group(1)))
    for record_id in indexed_record_ids(gov_root, directory, kind, prefix):
        match = pattern.match(record_id)
        if match:
            highest = max(highest, int(match.group(1)))
    for record_id in frontmatter_record_ids(gov_root, prefix):
        match = pattern.match(record_id)
        if match:
            highest = max(highest, int(match.group(1)))
    return f"{prefix}-{highest + 1:04d}"


def validate_record_id(record_id: str, prefix: str) -> None:
    if not re.fullmatch(rf"{re.escape(prefix)}-\d{{4}}", record_id):
        raise SystemExit(f"Record id must match kind prefix: expected {prefix}-NNNN, got {record_id}")


def parse_frontmatter_id(path: Path) -> str | None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end == -1:
        return None
    for line in text[4:end].splitlines():
        key, _, value = line.partition(":")
        if key.strip() == "id":
            return value.strip() or None
    return None


def existing_record_paths(gov_root: Path, record_id: str) -> list[Path]:
    matches: list[Path] = []
    for path in gov_root.rglob("*.md"):
        rel = path.relative_to(gov_root)
        if rel.parts and rel.parts[0] == "tasks":
            continue
        if parse_frontmatter_id(path) == record_id:
            matches.append(path)
    return sorted(matches)


def frontmatter(record_id: str, record_type: str, status: str, today: str) -> str:
    fields = {
        "id": record_id,
        "type": record_type,
        "status": status,
        "owner": "engineering",
        "created": today,
        "last_reviewed": today,
        "source": "manual" if record_type == "gate" else "",
    }
    if record_type == "gate":
        fields["severity"] = "BLOCK"
        fields["detectability"] = "manual"
    lines = ["---"]
    for key, value in fields.items():
        lines.append(f"{key}: {value}")
    lines.append("related_gates: []")
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def body(kind: str, record_id: str, title: str) -> str:
    heading = f"# {record_id} {title}\n\n"
    if kind == "gate":
        return heading + (
            "## 阻止条件\n\n待补充。\n\n"
            "## 原因\n\n待补充。\n\n"
            "## 检查方式\n\n- manual: 待补充。\n\n"
            "## 可操作错误提示\n\n待补充。\n\n"
            "## 最小修复\n\n- [ ] 待补充。\n"
        )
    if kind == "postmortem":
        return heading + (
            "## 事件背景\n\n待补充。\n\n"
            "## 影响范围\n\n待补充。\n\n"
            "## 根因\n\n待补充。\n\n"
            "## 修复过程\n\n待补充。\n\n"
            "## 防复发动作\n\n- [ ] 待补充。\n\n"
            "## 是否需要新增 Gate\n\n待判定。\n"
        )
    if kind == "qa":
        return heading + (
            "## 功能范围\n\n待补充。\n\n"
            "## 用户旅程\n\n待补充。\n\n"
            "## 验收场景\n\n- [ ] 成功路径。\n- [ ] 失败路径。\n- [ ] 边界输入。\n\n"
            "## 验证证据\n\n待补充。\n"
        )
    if kind == "agent-feedback":
        return heading + (
            "## 反馈来源\n\n待补充。\n\n"
            "## 代理失败模式\n\n待补充。\n\n"
            "## 期望行为\n\n待补充。\n\n"
            "## 处理状态\n\nnew\n\n"
            "## 转化结果\n\n- [ ] lesson\n- [ ] gate\n- [ ] rejected\n"
        )
    return heading + (
        "## 背景\n\n待补充。\n\n"
        "## 决策或结论\n\n待补充。\n\n"
        "## 证据\n\n待补充。\n\n"
        "## 影响范围\n\n待补充。\n\n"
        "## 后续动作\n\n- [ ] 待补充。\n"
    )


def ensure_index(directory: Path, title: str) -> Path:
    index = directory / "INDEX.md"
    if not index.exists():
        today = date.today().isoformat()
        index.write_text(
            "---\n"
            f"id: IDX-{slugify(title).upper()}\n"
            "type: index\n"
            "status: current\n"
            "owner: engineering\n"
            f"created: {today}\n"
            f"last_reviewed: {today}\n"
            "---\n\n"
            f"# {title}\n\n| ID | 标题 | 状态 | 文件 |\n|---|---|---|---|\n",
            encoding="utf-8",
        )
    else:
        content = index.read_text(encoding="utf-8")
        normalized = normalize_record_index_content(content)
        if normalized != content:
            index.write_text(normalized, encoding="utf-8")
    return index


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


def is_table_row(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("|") and stripped.count("|") >= 2


def format_table_row(cells: list[str]) -> str:
    return "| " + " | ".join(cells) + " |"


def normalize_record_index_content(content: str) -> str:
    lines: list[str] = []
    in_record_table = False
    for line in content.splitlines():
        stripped = line.strip()
        if stripped in {"| 名称 | 说明 |", "| ID | 标题 | 状态 |"}:
            lines.append("| ID | 标题 | 状态 | 文件 |")
            in_record_table = True
            continue
        if in_record_table and stripped in {"|---|---|", "|---|---|---|"}:
            lines.append("|---|---|---|---|")
            continue
        if in_record_table and is_table_row(line):
            cells = table_cells(line)
            if len(cells) == 2:
                cells = [cells[0], cells[1], "unknown", "-"]
            elif len(cells) == 3:
                cells = [cells[0], cells[1], cells[2], "-"]
            lines.append(format_table_row(cells))
            continue
        if in_record_table and not stripped:
            in_record_table = False
        lines.append(line)
    return "\n".join(lines) + ("\n" if content.endswith("\n") else "")


def normalize_gate_index_content(content: str) -> str:
    old_header = "| Gate ID | 严重级别 | 类型 | 检测方式 | 来源 | 当前状态 |"
    new_header = "| Gate ID | 严重级别 | 标题 | 检测方式 | 来源 | 状态 | 文件 |"
    lines: list[str] = []
    in_gate_table = False
    for line in content.splitlines():
        stripped = line.strip()
        if stripped == old_header:
            lines.append(new_header)
            in_gate_table = True
            continue
        if stripped == new_header:
            lines.append(line)
            in_gate_table = True
            continue
        if in_gate_table and stripped in {"|---|---|---|---|---|---|", "|---|---|---|---|---|---|---|"}:
            lines.append("|---|---|---|---|---|---|---|")
            continue
        if in_gate_table and is_table_row(line):
            cells = table_cells(line)
            if cells and "无 active gate" in cells[0]:
                continue
            if len(cells) == 6:
                if cells[2] in {"待补充", "-"} and cells[4] not in {"", "-"}:
                    cells = [cells[0], cells[1], cells[4], cells[3], "manual", cells[5], "-"]
                else:
                    cells = [cells[0], cells[1], cells[2], cells[3], cells[4], cells[5], "-"]
            lines.append(format_table_row(cells))
            continue
        if in_gate_table and not stripped:
            in_gate_table = False
        lines.append(line)
    return "\n".join(lines) + ("\n" if content.endswith("\n") else "")


def escape_table_cell(value: str) -> str:
    return value.replace("|", r"\|")


def index_has_record_id(content: str, record_id: str) -> bool:
    pattern = re.compile(rf"^\|\s*`?{re.escape(record_id)}`?\s*\|")
    return any(pattern.match(line) for line in content.splitlines())


def existing_index_paths(gov_root: Path, directory: Path, kind: str, record_id: str) -> list[Path]:
    matches: list[Path] = []
    for index in index_paths_for_kind(gov_root, directory, kind):
        if index.exists() and index_has_record_id(index.read_text(encoding="utf-8"), record_id):
            matches.append(index)
    return sorted(matches)


def append_index(index: Path, record_id: str, title: str, status: str, filename: str) -> None:
    content = index.read_text(encoding="utf-8")
    line = (
        f"| `{escape_table_cell(record_id)}` | {escape_table_cell(title)} | "
        f"{escape_table_cell(status)} | `{escape_table_cell(filename)}` |\n"
    )
    if not index_has_record_id(content, record_id):
        index.write_text(content.rstrip() + "\n" + line, encoding="utf-8")


def append_gate_index(gov_root: Path, record_id: str, title: str, status: str, filename: str) -> None:
    index = gov_root / "architecture-gates" / "GATE-INDEX.md"
    index.parent.mkdir(parents=True, exist_ok=True)
    if not index.exists():
        today = date.today().isoformat()
        index.write_text(
            "---\n"
            "id: GATE-INDEX\n"
            "type: gate-index\n"
            "status: current\n"
            "owner: engineering\n"
            f"created: {today}\n"
            f"last_reviewed: {today}\n"
            "---\n\n"
            "# Gate Index\n\n"
            "| Gate ID | 严重级别 | 标题 | 检测方式 | 来源 | 状态 | 文件 |\n"
            "|---|---|---|---|---|---|---|\n",
            encoding="utf-8",
        )
    else:
        content = index.read_text(encoding="utf-8")
        normalized = normalize_gate_index_content(content)
        if normalized != content:
            index.write_text(normalized, encoding="utf-8")
    content = index.read_text(encoding="utf-8")
    line = (
        f"| `{escape_table_cell(record_id)}` | BLOCK | {escape_table_cell(title)} | manual | "
        f"manual | {escape_table_cell(status)} | `{escape_table_cell(filename)}` |\n"
    )
    if not index_has_record_id(content, record_id):
        index.write_text(content.rstrip() + "\n" + line, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a numbered governance record.")
    parser.add_argument("--project-root", default=".", help="Target project root.")
    parser.add_argument("--kind", choices=sorted(KINDS), required=True, help="Record kind.")
    parser.add_argument("--title", required=True, help="Record title.")
    parser.add_argument("--id", help="Explicit record id, e.g. ADR-0007.")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project_root = Path(args.project_root).resolve()
    gov_root = project_root / GOV_ROOT
    if not gov_root.exists():
        raise SystemExit(f"Governance package not found: {gov_root}. Run init_governance_package.py first.")

    prefix, rel_dir, record_type = KINDS[args.kind]
    directory = gov_root / rel_dir
    record_id = args.id or next_id(gov_root, directory, args.kind, prefix)
    validate_record_id(record_id, prefix)
    existing_paths = existing_record_paths(gov_root, record_id)
    if existing_paths:
        existing = ", ".join(str(path) for path in existing_paths)
        raise SystemExit(f"Record id already exists: {record_id} ({existing})")
    existing_indexes = existing_index_paths(gov_root, directory, args.kind, record_id)
    if existing_indexes:
        existing = ", ".join(str(path) for path in existing_indexes)
        raise SystemExit(f"Record id already exists in index: {record_id} ({existing})")
    filename = f"{record_id}-{slugify(args.title)}.md"
    path = directory / filename
    if path.exists():
        raise SystemExit(f"Record already exists: {path}")

    today = date.today().isoformat()
    record_status = "draft" if record_type != "gate" else "active"
    content = frontmatter(record_id, record_type, record_status, today)
    content += body(args.kind, record_id, args.title)

    if args.dry_run:
        print(path)
        return 0

    directory.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    index = ensure_index(directory, f"{args.kind} Index")
    append_index(index, record_id, args.title, record_status, path.name)
    if args.kind == "gate":
        append_gate_index(gov_root, record_id, args.title, record_status, path.name)

    print(path)
    print(f"updated: {index}")
    if args.kind == "gate":
        print(f"updated: {gov_root / 'architecture-gates' / 'GATE-INDEX.md'}")
    print("non_invasive: wrote only inside governance/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
