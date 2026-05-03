#!/usr/bin/env python3
"""Check AI citation entry files for local path and anchor drift."""

from __future__ import annotations

import re
import sys
import urllib.parse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AI_ENTRY_FILES = [
    Path("llms.txt"),
    Path("assets/ai-citation/llms-full.txt"),
]
AI_MARKDOWN_DIR = Path("assets/ai-citation")
PATH_PATTERN = re.compile(
    r"(?<![\w./-])("
    r"(?:README|AGENTS)\.md"
    r"|(?:docs|assets|skills|prompts|metadata|scripts|tools)/[^\s`，。；：、)）]+"
    r"|[A-Za-z0-9_.-]+\.(?:md|txt|yml)"
    r"|llms\.txt"
    r")"
)
MARKDOWN_LINK_PATTERN = re.compile(r"!??\[[^\]]*\]\(([^)]+)\)")
EXTERNAL_PREFIXES = ("http://", "https://", "mailto:", "tel:", "data:")


def github_slug(title: str) -> str:
    title = re.sub(r"<[^>]+>", "", title.strip().lower())
    title = re.sub(r"[`*_~]", "", title)
    title = re.sub(r"[^\w\u4e00-\u9fff\- ]+", "", title)
    title = re.sub(r"\s+", "-", title).strip("-")
    return title


def markdown_anchors(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    anchors = set(re.findall(r"<a\s+id=[\"']([^\"']+)[\"']", text))
    used: dict[str, int] = {}
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
            continue
        if in_fence:
            continue

        heading = re.match(r"^(#{1,6})\s+(.+?)\s*#*\s*$", line)
        if not heading:
            continue
        slug = github_slug(heading.group(2))
        if not slug:
            continue
        count = used.get(slug, 0)
        used[slug] = count + 1
        anchors.add(slug if count == 0 else f"{slug}-{count}")

    return anchors


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


def candidate_files() -> list[Path]:
    files = list(AI_ENTRY_FILES)
    if AI_MARKDOWN_DIR.exists():
        files.extend(sorted(AI_MARKDOWN_DIR.glob("*.md")))
    return sorted(set(files))


def extract_targets(path: Path) -> list[tuple[int, str]]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    scan_text = strip_fenced_code(text)
    targets: list[tuple[int, str]] = []

    for lineno, line in enumerate(scan_text.splitlines(), start=1):
        for match in MARKDOWN_LINK_PATTERN.finditer(line):
            targets.append((lineno, match.group(1).strip()))
        for match in PATH_PATTERN.finditer(line):
            targets.append((lineno, match.group(1).strip().strip("<>")))

    return targets


def validate_target(source: Path, lineno: int, raw: str, anchor_cache: dict[Path, set[str]]) -> str | None:
    if not raw or raw.startswith(EXTERNAL_PREFIXES):
        return None

    target = urllib.parse.unquote(raw.strip("<>").rstrip(".,;"))
    path_part, _, anchor = target.partition("#")
    if not path_part:
        return None

    destination = (ROOT / path_part).resolve()
    if "/" not in path_part and source.parent == AI_MARKDOWN_DIR and not destination.exists():
        destination = (ROOT / source.parent / path_part).resolve()

    try:
        destination.relative_to(ROOT)
    except ValueError:
        return None

    if not destination.exists():
        return f"{source}:{lineno}: missing AI citation target: {raw}"

    if anchor and destination.suffix.lower() == ".md":
        if destination not in anchor_cache:
            anchor_cache[destination] = markdown_anchors(destination)
        if anchor not in anchor_cache[destination]:
            rel = destination.relative_to(ROOT)
            return f"{source}:{lineno}: missing AI citation anchor: {rel}#{anchor}"

    return None


def main() -> int:
    errors: list[str] = []
    anchor_cache: dict[Path, set[str]] = {}

    for rel_path in candidate_files():
        path = ROOT / rel_path
        if not path.exists():
            errors.append(f"{rel_path}: missing AI citation file")
            continue
        for lineno, target in extract_targets(path):
            error = validate_target(rel_path, lineno, target, anchor_cache)
            if error:
                errors.append(error)

    if errors:
        print("AI_CITATION_ERRORS")
        for error in errors:
            print(error)
        print(f"TOTAL={len(errors)}")
        return 1

    print("OK AI citation paths and anchors checked")
    return 0


if __name__ == "__main__":
    sys.exit(main())
