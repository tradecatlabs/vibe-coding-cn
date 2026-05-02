#!/usr/bin/env python3
"""Check local Markdown links that should resolve inside this repository."""

from __future__ import annotations

import re
import sys
import urllib.parse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {".git", ".history"}
SKIP_PREFIXES = [
    Path(".github/wiki"),
    Path("tools/external"),
    Path("tools/chat-vault"),
]
LINK_PATTERNS = [
    re.compile(r"!??\[[^\]]*\]\(([^)]+)\)"),
    re.compile(r"\b(?:href|src)=[\"']([^\"']+)[\"']"),
]
EXTERNAL_PREFIXES = (
    "#",
    "http://",
    "https://",
    "wss://",
    "ws://",
    "mailto:",
    "tel:",
    "data:",
)


def should_skip(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    if any(part in SKIP_PARTS for part in rel.parts):
        return True
    return any(rel == prefix or prefix in rel.parents for prefix in SKIP_PREFIXES)


def normalize_target(raw: str) -> str:
    raw = raw.strip()
    if not raw or raw.startswith(EXTERNAL_PREFIXES):
        return ""
    target = raw.split()[0] if " " in raw and not raw.startswith("<") else raw
    target = target.strip("<>").split("#", 1)[0]
    return urllib.parse.unquote(target)


def main() -> int:
    missing: list[tuple[Path, str, Path]] = []
    checked_files = 0

    for markdown_file in sorted(ROOT.rglob("*.md")):
        if should_skip(markdown_file):
            continue
        checked_files += 1
        text = markdown_file.read_text(encoding="utf-8", errors="ignore")

        for pattern in LINK_PATTERNS:
            for match in pattern.finditer(text):
                raw = match.group(1)
                target = normalize_target(raw)
                if not target or target.startswith(("/", "\\")):
                    continue

                destination = (markdown_file.parent / target).resolve()
                try:
                    destination.relative_to(ROOT)
                except ValueError:
                    continue

                if not destination.exists():
                    missing.append((markdown_file.relative_to(ROOT), raw, markdown_file.parent / target))

    if missing:
        print("MISSING_LINKS")
        for source, raw, resolved in missing:
            print(f"{source} -> {raw} => {resolved.relative_to(ROOT)}")
        print(f"TOTAL={len(missing)}")
        return 1

    print(f"OK local links checked: {checked_files} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
