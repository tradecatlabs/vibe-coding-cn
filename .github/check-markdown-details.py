#!/usr/bin/env python3
"""Check Markdown details/summary blocks for balanced collapsible sections."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from lib import SOURCE_PREFIXES, is_research_repository_snapshot


ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {".git", ".history", "node_modules"}
# 保留原折叠块检查对chat-vault的覆盖。
SKIP_PREFIXES = tuple(path for path in SOURCE_PREFIXES if path != Path('.github/extensions/chat-vault'))
TAG_PATTERN = re.compile(r"<details\b[^>]*>|</details>|<summary>.*?</summary>")


def strip_fenced_code(text: str) -> str:
    lines: list[str] = []
    in_fence = False
    fence_marker = ""

    for line in text.splitlines():
        stripped = line.lstrip()
        match = re.match(r"(`{3,}|~{3,})(.*)$", stripped)
        if match:
            marker, suffix = match.groups()
            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif (
                marker[0] == fence_marker[0]
                and len(marker) >= len(fence_marker)
                and not suffix.strip(" \t")
            ):
                in_fence = False
                fence_marker = ""
            lines.append("")
            continue
        lines.append("" if in_fence else line)

    return "\n".join(lines)


def strip_inline_code(text: str) -> str:
    return re.sub(r"`[^`\n]*`", "", text)


def should_skip(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    if any(part in SKIP_PARTS for part in rel.parts):
        return True
    if is_research_repository_snapshot(rel):
        return True
    return any(rel == prefix or prefix in rel.parents for prefix in SKIP_PREFIXES)


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def main() -> int:
    errors: list[str] = []
    checked_files = 0

    for markdown_file in sorted(ROOT.rglob("*.md")):
        if should_skip(markdown_file):
            continue
        checked_files += 1
        raw_text = markdown_file.read_text(encoding="utf-8", errors="ignore")
        text = strip_inline_code(strip_fenced_code(raw_text))
        rel = markdown_file.relative_to(ROOT)
        stack: list[dict[str, int | bool]] = []

        for match in TAG_PATTERN.finditer(text):
            tag = match.group(0)
            line = line_number(text, match.start())
            if tag.startswith("<details"):
                stack.append({"line": line, "summary": False})
                continue

            if tag == "</details>":
                if not stack:
                    errors.append(f"{rel}:{line}: closing </details> without opening <details>")
                    continue
                block = stack.pop()
                if not block["summary"]:
                    errors.append(f"{rel}:{block['line']}: <details> block missing <summary>")
                continue

            if tag.startswith("<summary>"):
                if not stack:
                    continue
                if stack[-1]["summary"]:
                    errors.append(f"{rel}:{line}: duplicate <summary> in same <details> block")
                    continue
                stack[-1]["summary"] = True

        for block in stack:
            errors.append(f"{rel}:{block['line']}: opening <details> without closing </details>")

    if errors:
        print("MARKDOWN_DETAILS_ERRORS")
        for error in errors:
            print(error)
        print(f"TOTAL={len(errors)}")
        return 1

    print(f"OK markdown details checked: {checked_files} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
