#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path


GOV_ROOT = Path("governance")


def slug_from_code_path(code_path: str) -> str:
    value = code_path.strip().strip("/").replace("\\", "/")
    value = re.sub(r"[^A-Za-z0-9\u4e00-\u9fff]+", "-", value).strip("-")
    return value or "module"


def frontmatter(module_id: str, today: str, code_path: str) -> str:
    return (
        "---\n"
        f"id: {module_id}\n"
        "type: module-context\n"
        "status: current\n"
        "owner: engineering\n"
        f"created: {today}\n"
        f"last_reviewed: {today}\n"
        f"code_path: {code_path}\n"
        "---\n\n"
    )


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


def existing_context_paths(gov_root: Path, module_id: str) -> list[Path]:
    matches: list[Path] = []
    for path in gov_root.rglob("*.md"):
        rel = path.relative_to(gov_root)
        if rel.parts and rel.parts[0] == "tasks":
            continue
        if parse_frontmatter_id(path) == module_id:
            matches.append(path)
    return sorted(matches)


def context_body(name: str, code_path: str, validations: list[str], adrs: list[str]) -> str:
    validation_lines = "\n".join(f"- `{item}`" for item in validations) or "- 待补充。"
    adr_lines = "\n".join(f"- `{item}`" for item in adrs) or "- 待补充。"
    return f"""# {name} Context

## 代码路径

`{code_path}`

## 模块职责

待补充。

## 非职责

待补充。

## 禁止事项

- 待补充。

## 单一真相源

待补充。

## 常用验证

{validation_lines}

## 相关治理文档

{adr_lines}

## Agent Rules

- 不要把本模块上下文散落到代码目录。
- 如需引用原模块 README，只在这里链接，不复制覆盖。
"""


def ensure_context_map(gov_root: Path) -> Path:
    path = gov_root / "context" / "CONTEXT-MAP.md"
    if not path.exists():
        today = date.today().isoformat()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "---\n"
            "id: GOV-CONTEXT-MAP\n"
            "type: index\n"
            "status: current\n"
            "owner: engineering\n"
            f"created: {today}\n"
            f"last_reviewed: {today}\n"
            "---\n\n"
            "# Context Map\n\n"
            "| 领域 | 代码目录 | 上下文文件 | 相关 ADR | 常用验证 |\n"
            "|---|---|---|---|---|\n",
            encoding="utf-8",
        )
    return path


def table_cells(line: str) -> list[str]:
    value = line.strip()
    if not value.startswith("|") or not value.endswith("|"):
        return []
    cells: list[str] = []
    current: list[str] = []
    escaped = False
    for char in value[1:-1]:
        if char == "|" and not escaped:
            cells.append("".join(current).strip())
            current = []
            continue
        current.append(char)
        escaped = char == "\\" and not escaped
        if char != "\\":
            escaped = False
    cells.append("".join(current).strip())
    return cells


def unquote_cell(value: str) -> str:
    value = value.strip()
    if value.startswith("`") and value.endswith("`"):
        value = value[1:-1]
    return value.replace(r"\|", "|")


def escape_table_cell(value: str) -> str:
    return value.replace("|", r"\|")


def context_map_has_entry(content: str, code_path: str, context_rel: str) -> bool:
    for line in content.splitlines():
        cells = table_cells(line)
        if len(cells) < 3:
            continue
        if unquote_cell(cells[1]) == code_path or unquote_cell(cells[2]) == context_rel:
            return True
    return False


def append_context_map_row(content: str, line: str) -> str:
    lines = content.rstrip().splitlines()
    insert_at: int | None = None
    for index, current in enumerate(lines):
        cells = table_cells(current)
        if len(cells) >= 3 and cells[0] == "领域" and cells[1] == "代码目录" and cells[2] == "上下文文件":
            insert_at = index + 1
            while insert_at < len(lines) and table_cells(lines[insert_at]):
                insert_at += 1
            break
    if insert_at is None:
        return content.rstrip() + "\n" + line
    lines.insert(insert_at, line.rstrip("\n"))
    return "\n".join(lines) + "\n"


def append_context_map(path: Path, name: str, code_path: str, context_rel: str, validations: list[str], adrs: list[str]) -> None:
    content = path.read_text(encoding="utf-8")
    if context_map_has_entry(content, code_path, context_rel):
        return
    validation_text = "<br>".join(f"`{escape_table_cell(item)}`" for item in validations) if validations else "待补充"
    adr_text = "<br>".join(f"`{escape_table_cell(item)}`" for item in adrs) if adrs else "待补充"
    line = (
        f"| {escape_table_cell(name)} | `{escape_table_cell(code_path)}` | "
        f"`{escape_table_cell(context_rel)}` | {adr_text} | {validation_text} |\n"
    )
    path.write_text(append_context_map_row(content, line), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a governance-owned module context.")
    parser.add_argument("--project-root", default=".", help="Target project root.")
    parser.add_argument("--code-path", required=True, help="Code module path, e.g. src/domains/payment.")
    parser.add_argument("--name", help="Human-readable module/domain name.")
    parser.add_argument("--validation", action="append", default=[], help="Validation command. Repeatable.")
    parser.add_argument("--adr", action="append", default=[], help="Related ADR path. Repeatable.")
    parser.add_argument("--dry-run", action="store_true", help="Preview target without writing.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project_root = Path(args.project_root).resolve()
    gov_root = project_root / GOV_ROOT
    if not gov_root.exists():
        raise SystemExit(f"Governance package not found: {gov_root}. Run init_governance_package.py first.")
    slug = slug_from_code_path(args.code_path)
    name = args.name or slug.replace("-", " ")
    rel = Path("context") / "module-contexts" / slug / "CONTEXT.md"
    path = gov_root / rel
    if path.exists():
        raise SystemExit(f"Module context already exists: {path}")
    module_id = f"CTX-{slug.upper()}"
    existing_paths = existing_context_paths(gov_root, module_id)
    if existing_paths:
        existing = ", ".join(str(path) for path in existing_paths)
        raise SystemExit(f"Module context id already exists: {module_id} ({existing})")
    if args.dry_run:
        print(path)
        return 0
    today = date.today().isoformat()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        frontmatter(module_id, today, args.code_path)
        + context_body(name, args.code_path, args.validation, args.adr),
        encoding="utf-8",
    )
    context_map = ensure_context_map(gov_root)
    append_context_map(context_map, name, args.code_path, str(rel), args.validation, args.adr)
    print(path)
    print(f"updated: {context_map}")
    print("non_invasive: wrote only inside governance/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
