#!/usr/bin/env python3
"""Check metadata path references resolve to real repository paths and anchors."""

from __future__ import annotations

import re
import sys
import urllib.parse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
METADATA_FILES = [
    Path("metadata/taxonomy.yml"),
    Path("metadata/redirects.yml"),
]


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


def metadata_targets(path: Path) -> list[tuple[int, str]]:
    targets: list[tuple[int, str]] = []
    text = path.read_text(encoding="utf-8", errors="ignore")

    for lineno, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith(("path:", "entry:", "agent_guide:", "to:")):
            _, value = stripped.split(":", 1)
            targets.append((lineno, value.strip().strip("\"'")))
            continue
        if stripped.startswith("- "):
            value = stripped[2:].strip().strip("\"'")
            if value.startswith("from:"):
                continue
            if value.startswith(("path:", "entry:", "agent_guide:", "to:")):
                _, value = value.split(":", 1)
                targets.append((lineno, value.strip().strip("\"'")))
                continue
            if value.startswith((".", "/")) or "/" in value or value.endswith(".md"):
                targets.append((lineno, value))

    return targets


def validate_target(source: Path, lineno: int, raw: str, anchor_cache: dict[Path, set[str]]) -> str | None:
    if not raw or raw.startswith(("http://", "https://", "mailto:", "tel:")):
        return None
    if " 或 " in raw:
        return f"{source}:{lineno}: ambiguous metadata target: {raw}"

    target = urllib.parse.unquote(raw.strip("<>"))
    path_part, _, anchor = target.partition("#")
    destination = (ROOT / path_part).resolve()

    try:
        destination.relative_to(ROOT)
    except ValueError:
        return None

    if not destination.exists():
        return f"{source}:{lineno}: missing metadata target: {raw}"
    if anchor and destination.suffix.lower() == ".md":
        if destination not in anchor_cache:
            anchor_cache[destination] = markdown_anchors(destination)
        if anchor not in anchor_cache[destination]:
            rel = destination.relative_to(ROOT)
            return f"{source}:{lineno}: missing metadata anchor: {rel}#{anchor}"

    return None


def main() -> int:
    errors: list[str] = []
    anchor_cache: dict[Path, set[str]] = {}

    for rel_path in METADATA_FILES:
        path = ROOT / rel_path
        if not path.exists():
            errors.append(f"{rel_path}: missing metadata file")
            continue
        for lineno, target in metadata_targets(path):
            error = validate_target(rel_path, lineno, target, anchor_cache)
            if error:
                errors.append(error)

    if errors:
        print("METADATA_ERRORS")
        for error in errors:
            print(error)
        print(f"TOTAL={len(errors)}")
        return 1

    print("OK metadata paths checked")
    return 0


if __name__ == "__main__":
    sys.exit(main())
