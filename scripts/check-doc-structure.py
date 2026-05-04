#!/usr/bin/env python3
"""Check docs README standard blocks, stable anchors and duplicate manual anchors."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from lib.taxonomy import doc_readmes_from_taxonomy, taxonomy_sections

ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {".git", ".history", "node_modules"}
SKIP_PREFIXES = [
    Path(".github/wiki"),
    Path("tools/external"),
]
ANCHOR_PATTERN = re.compile(r"<a\s+id=[\"']([^\"']+)[\"']")
SUMMARY_LINE = "<summary><strong>完整细粒度目录（点击展开/收起）</strong></summary>"
STANDARD_README_BLOCKS = [
    ("顶部标题块", re.compile(r"^#\s+.+$", re.MULTILINE)),
    ("字多不看", re.compile(r"^##\s+字多不看\s*$", re.MULTILINE)),
    ("快速导航", re.compile(r"^##\s+快速导航\s*$", re.MULTILINE)),
    ("完整细粒度目录", re.compile(re.escape(SUMMARY_LINE))),
    ("使用方式", re.compile(r"^##\s+使用方式\s*$", re.MULTILINE)),
]


def strip_fenced_code(text: str) -> str:
    lines: list[str] = []
    in_fence = False
    fence_marker = ""

    for line in text.splitlines():
        stripped = line.lstrip()
        if stripped.startswith(("```", "~~~")):
            marker = stripped[:3]
            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif marker == fence_marker:
                in_fence = False
                fence_marker = ""
            lines.append("")
            continue
        lines.append("" if in_fence else line)

    return "\n".join(lines)


def should_skip(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    if any(part in SKIP_PARTS for part in rel.parts):
        return True
    return any(rel == prefix or prefix in rel.parents for prefix in SKIP_PREFIXES)


def duplicate_manual_anchors(path: Path) -> list[str]:
    text = strip_fenced_code(path.read_text(encoding="utf-8", errors="ignore"))
    seen: dict[str, int] = {}
    errors: list[str] = []

    for lineno, line in enumerate(text.splitlines(), start=1):
        for anchor in ANCHOR_PATTERN.findall(line):
            if anchor in seen:
                rel = path.relative_to(ROOT)
                errors.append(f"{rel}:{lineno}: duplicate manual anchor '{anchor}', first seen at line {seen[anchor]}")
            else:
                seen[anchor] = lineno

    return errors


def check_linear_readme(path: Path, expected_anchors: list[str]) -> list[str]:
    rel = path.relative_to(ROOT)
    text = strip_fenced_code(path.read_text(encoding="utf-8", errors="ignore"))
    errors: list[str] = []

    errors.extend(check_standard_readme_blocks(path, text))

    if "完整细粒度目录（点击展开/收起）" not in text:
        errors.append(f"{rel}: missing collapsible full fine-grained table of contents")

    if "<details>" not in text or "</details>" not in text:
        errors.append(f"{rel}: missing details block for long-form navigation")

    anchor_lines: dict[str, int] = {}
    for lineno, line in enumerate(text.splitlines(), start=1):
        for anchor in ANCHOR_PATTERN.findall(line):
            anchor_lines.setdefault(anchor, lineno)

    previous_line = 0
    for anchor in expected_anchors:
        line = anchor_lines.get(anchor)
        if line is None:
            errors.append(f"{rel}: missing required main anchor '{anchor}'")
            continue
        if line <= previous_line:
            errors.append(f"{rel}:{line}: main anchor '{anchor}' is out of expected section order")
        previous_line = line

    toc_text = active_toc_text(text)
    if not toc_text:
        errors.append(f"{rel}: missing active collapsible fine-grained TOC block")

    for anchor in expected_anchors:
        if f"#{anchor}" not in toc_text:
            errors.append(f"{rel}: top navigation or fine-grained TOC does not link to '#{anchor}'")

    required_prefixes = tuple(f"{anchor}-" for anchor in expected_anchors)
    for anchor in anchor_lines:
        if anchor in expected_anchors or anchor.startswith(required_prefixes):
            if f"#{anchor}" not in toc_text:
                errors.append(f"{rel}: fine-grained TOC does not link to manual anchor '#{anchor}'")

    return errors


def check_standard_readme_blocks(path: Path, text: str) -> list[str]:
    """Validate the standard top-level README block order used under docs/."""
    rel = path.relative_to(ROOT)
    errors: list[str] = []
    positions: list[tuple[str, int]] = []

    for block_name, pattern in STANDARD_README_BLOCKS:
        match = pattern.search(text)
        if match is None:
            errors.append(f"{rel}: missing standard README block '{block_name}'")
            continue
        positions.append((block_name, match.start()))

    if len(positions) != len(STANDARD_README_BLOCKS):
        return errors

    title_end = positions[0][1] + text[positions[0][1] :].find("\n")
    if title_end < positions[0][1]:
        title_end = len(text)
    between_title_and_summary = text[title_end:positions[1][1]].strip()
    if between_title_and_summary:
        errors.append(f"{rel}: standard README block '字多不看' must immediately follow the top title")

    previous_name, previous_pos = positions[0]
    for block_name, position in positions[1:]:
        if position <= previous_pos:
            errors.append(
                f"{rel}: standard README block '{block_name}' must appear after '{previous_name}'"
            )
        previous_name, previous_pos = block_name, position

    return errors


def active_toc_text(text: str) -> str:
    in_fence = False
    fence_marker = ""
    collecting = False
    collected: list[str] = []

    for line in text.splitlines():
        stripped = line.lstrip()
        if stripped.startswith(("```", "~~~")):
            marker = stripped[:3]
            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif marker == fence_marker:
                in_fence = False
                fence_marker = ""

        if in_fence:
            continue
        if SUMMARY_LINE in line:
            collecting = True
        if collecting:
            collected.append(line)
        if collecting and line.strip() == "</details>":
            break

    return "\n".join(collected)


def check_docs_index() -> list[str]:
    errors: list[str] = []
    docs_index = ROOT / "docs/README.md"
    rel = docs_index.relative_to(ROOT)

    if not docs_index.exists():
        return [f"{rel}: missing docs index"]

    text = docs_index.read_text(encoding="utf-8", errors="ignore")
    for name, fields in taxonomy_sections().items():
        for field in ("path", "entry", "agent_guide"):
            value = fields.get(field)
            if not value:
                errors.append(f"metadata/taxonomy.yml: section '{name}' missing '{field}'")
                continue
            docs_relative = value.removeprefix("docs/")
            candidates = {value, f"./{docs_relative}", docs_relative}
            if not any(candidate in text for candidate in candidates):
                errors.append(f"{rel}: missing taxonomy {field} reference for '{name}': {value}")

    return errors


def main() -> int:
    errors: list[str] = []
    checked_files = 0

    for markdown_file in sorted(ROOT.rglob("*.md")):
        if should_skip(markdown_file):
            continue
        checked_files += 1
        errors.extend(duplicate_manual_anchors(markdown_file))

    doc_readmes = doc_readmes_from_taxonomy()
    if not doc_readmes:
        errors.append("metadata/taxonomy.yml: no docs README anchors found under documents")

    for rel_path, expected_anchors in doc_readmes.items():
        path = ROOT / rel_path
        if not path.exists():
            errors.append(f"{rel_path}: missing docs README")
            continue
        errors.extend(check_linear_readme(path, expected_anchors))

    docs_index = ROOT / "docs" / "README.md"
    if docs_index.exists():
        text = strip_fenced_code(docs_index.read_text(encoding="utf-8", errors="ignore"))
        errors.extend(check_standard_readme_blocks(docs_index, text))

    errors.extend(check_docs_index())

    if errors:
        print("DOC_STRUCTURE_ERRORS")
        for error in errors:
            print(error)
        print(f"TOTAL={len(errors)}")
        return 1

    print(f"OK docs structure checked: {checked_files} markdown files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
