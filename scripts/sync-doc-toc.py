#!/usr/bin/env python3
"""Regenerate collapsible fine-grained TOC blocks in docs linear README files."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from lib.taxonomy import doc_readmes_from_taxonomy

ROOT = Path(__file__).resolve().parents[1]
SUMMARY_LINE = "<summary><strong>完整细粒度目录（点击展开/收起）</strong></summary>"
ANCHOR_PATTERN = re.compile(r"<a\s+id=[\"']([^\"']+)[\"']")
HEADING_PATTERN = re.compile(r"^(#{2,6})\s+(.+?)\s*#*\s*$")


def heading_after(lines: list[str], start: int) -> tuple[int, str] | None:
    for line in lines[start + 1 : start + 8]:
        stripped = line.strip()
        if not stripped:
            continue
        match = HEADING_PATTERN.match(stripped)
        if not match:
            return None
        return len(match.group(1)), match.group(2).strip()
    return None


def title_from_anchor(anchor: str, main_anchors: list[str]) -> str:
    for main_anchor in sorted(main_anchors, key=len, reverse=True):
        if anchor == main_anchor:
            return main_anchor
        prefix = f"{main_anchor}-"
        if anchor.startswith(prefix):
            return anchor.removeprefix(prefix).replace("-", " ")
    return anchor.replace("-", " ")


def collect_toc_entries(text: str, main_anchors: list[str]) -> list[tuple[int, str, str]]:
    lines = text.splitlines()
    required_prefixes = tuple(f"{anchor}-" for anchor in main_anchors)
    entries: list[tuple[int, str, str]] = []
    seen: set[str] = set()

    for idx, line in enumerate(lines):
        for anchor in ANCHOR_PATTERN.findall(line):
            if anchor in seen:
                continue
            if anchor not in main_anchors and not anchor.startswith(required_prefixes):
                continue
            seen.add(anchor)

            heading = heading_after(lines, idx)
            if heading:
                level, title = heading
            else:
                level, title = 3, title_from_anchor(anchor, main_anchors)
            entries.append((level, title, anchor))

    return entries


def render_toc(entries: list[tuple[int, str, str]]) -> str:
    rendered = [
        "<details>",
        SUMMARY_LINE,
        "",
        "### 细粒度目录",
        "",
    ]

    for level, title, anchor in entries:
        indent = "  " * max(level - 2, 0)
        rendered.append(f"{indent}- [{title}](#{anchor})")

    rendered.extend(["", "</details>"])
    return "\n".join(rendered)


def active_toc_bounds(text: str) -> tuple[int, int] | None:
    in_fence = False
    fence_marker = ""
    offset = 0
    details_start: int | None = None

    for line in text.splitlines(keepends=True):
        stripped = line.lstrip()
        if stripped.startswith(("```", "~~~")):
            marker = stripped[:3]
            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif marker == fence_marker:
                in_fence = False
                fence_marker = ""

        if not in_fence:
            if "<details>" in line:
                details_start = offset + line.index("<details>")
            if SUMMARY_LINE in line and details_start is not None:
                end = text.find("</details>", offset)
                if end == -1:
                    return None
                return details_start, end + len("</details>")

        offset += len(line)

    return None


def replace_toc_block(text: str, toc: str) -> tuple[str, bool]:
    bounds = active_toc_bounds(text)
    if bounds is None:
        return text, False

    details_start, details_end = bounds
    return f"{text[:details_start]}{toc}{text[details_end:]}", True


def main() -> int:
    changed: list[str] = []
    errors: list[str] = []

    for rel_path, main_anchors in doc_readmes_from_taxonomy().items():
        path = ROOT / rel_path
        if not path.exists():
            errors.append(f"{rel_path}: missing docs README")
            continue

        text = path.read_text(encoding="utf-8")
        entries = collect_toc_entries(text, main_anchors)
        if not entries:
            errors.append(f"{rel_path}: no TOC entries generated")
            continue

        new_text, replaced = replace_toc_block(text, render_toc(entries))
        if not replaced:
            errors.append(f"{rel_path}: missing standard collapsible TOC block")
            continue

        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            changed.append(str(rel_path))

    if errors:
        print("SYNC_DOC_TOC_ERRORS")
        for error in errors:
            print(error)
        return 1

    for rel_path in changed:
        print(f"updated {rel_path}")
    print(f"OK synced docs TOC blocks: {len(changed)} changed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
