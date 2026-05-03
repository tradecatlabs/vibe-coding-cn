#!/usr/bin/env python3
"""Build docs/references/README.md from ordered source fragments."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "docs" / "references" / "sources"
TARGET = ROOT / "docs" / "references" / "README.md"
EXCLUDED_SOURCE_NAMES = {"README.md", "AGENTS.md"}


def iter_source_files() -> list[Path]:
    if not SOURCE_DIR.exists():
        raise FileNotFoundError(f"source directory not found: {SOURCE_DIR}")

    files = sorted(
        path
        for path in SOURCE_DIR.glob("*.md")
        if path.name not in EXCLUDED_SOURCE_NAMES
    )
    if not files:
        raise FileNotFoundError(f"no source fragments found in: {SOURCE_DIR}")
    return files


def build_content() -> str:
    parts: list[str] = []
    for path in iter_source_files():
        content = path.read_text(encoding="utf-8").strip()
        if content:
            parts.append(content)
    return "\n\n".join(parts).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build docs/references/README.md from docs/references/sources/*.md."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail if docs/references/README.md is not synced with source fragments.",
    )
    args = parser.parse_args()

    expected = build_content()
    if args.check:
        actual = TARGET.read_text(encoding="utf-8") if TARGET.exists() else ""
        if actual != expected:
            print(
                "docs/references/README.md is out of sync. "
                "Run `make sync-reference-readme`.",
                file=sys.stderr,
            )
            return 1
        print("docs/references/README.md is synced with source fragments.")
        return 0

    TARGET.write_text(expected, encoding="utf-8")
    print(f"wrote {TARGET.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
