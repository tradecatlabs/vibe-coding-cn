#!/usr/bin/env python3
"""Check docs README structure, stable anchors and duplicate manual anchors."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC_READMES: dict[Path, list[str]] = {
    Path("docs/getting-started/README.md"): [
        "vibe-coding-experience",
        "learning-map",
        "network-environment",
        "cli-setup",
        "development-environment",
    ],
    Path("docs/concepts/README.md"): [
        "concept-problem-solving",
        "concept-glue-coding",
        "concept-system-building",
        "concept-development-paradigms",
        "concept-language-layers",
        "concept-recursive-self-optimizing-system",
    ],
    Path("docs/philosophy/README.md"): [
        "philosophy-thinking-models",
        "philosophy-compositional-description-model",
        "philosophy-programming-dao",
        "philosophy-methodology-toolbox",
    ],
    Path("docs/references/README.md"): [
        "reference-engineering-practice",
        "reference-technology-stack",
    ],
    Path("docs/research/README.md"): [
        "research-harness-engineering",
    ],
}
SKIP_PARTS = {".git", ".history", "node_modules"}
SKIP_PREFIXES = [
    Path(".github/wiki"),
    Path("tools/external"),
]
ANCHOR_PATTERN = re.compile(r"<a\s+id=[\"']([^\"']+)[\"']")


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

    toc_boundary = min((anchor_lines.get(anchor, len(text.splitlines()) + 1) for anchor in expected_anchors), default=0)
    toc_text = "\n".join(text.splitlines()[:toc_boundary])
    for anchor in expected_anchors:
        if f"#{anchor}" not in toc_text:
            errors.append(f"{rel}: top navigation or fine-grained TOC does not link to '#{anchor}'")

    return errors


def main() -> int:
    errors: list[str] = []
    checked_files = 0

    for markdown_file in sorted(ROOT.rglob("*.md")):
        if should_skip(markdown_file):
            continue
        checked_files += 1
        errors.extend(duplicate_manual_anchors(markdown_file))

    for rel_path, expected_anchors in DOC_READMES.items():
        path = ROOT / rel_path
        if not path.exists():
            errors.append(f"{rel_path}: missing docs README")
            continue
        errors.extend(check_linear_readme(path, expected_anchors))

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
