#!/usr/bin/env python3
"""Check required repository-owned directories have README.md and AGENTS.md."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_DIRS = [
    Path("assets"),
    Path("assets/ai-citation"),
    Path("assets/datasets"),
    Path("assets/images"),
    Path("assets/templates"),
    Path("docs"),
    Path("docs/concepts"),
    Path("docs/getting-started"),
    Path("docs/philosophy"),
    Path("docs/references"),
    Path("docs/research"),
    Path("metadata"),
    Path("prompts"),
    Path("scripts"),
    Path("skills"),
    Path("skills/auto-skill"),
    Path("tools"),
    Path("tools/chat-vault"),
    Path("tools/config"),
    Path("tools/config/.codex"),
    Path("tools/external"),
    Path("tools/prompts-library"),
]
GENERATED_OR_VENDOR_DIRS = [
    Path("node_modules"),
]


def main() -> int:
    errors: list[str] = []

    for rel_dir in REQUIRED_DIRS:
        directory = ROOT / rel_dir
        if not directory.is_dir():
            errors.append(f"{rel_dir}: required directory is missing")
            continue
        for filename in ("README.md", "AGENTS.md"):
            if not (directory / filename).is_file():
                errors.append(f"{rel_dir}/{filename}: missing required directory document")

    for rel_dir in GENERATED_OR_VENDOR_DIRS:
        directory = ROOT / rel_dir
        if directory.exists() and not (ROOT / ".gitignore").read_text(encoding="utf-8").count(str(rel_dir)):
            errors.append(f"{rel_dir}: generated directory exists but is not ignored")

    if errors:
        print("DIRECTORY_DOC_ERRORS")
        for error in errors:
            print(error)
        print(f"TOTAL={len(errors)}")
        return 1

    print(f"OK directory README/AGENTS pairs checked: {len(REQUIRED_DIRS)} directories")
    return 0


if __name__ == "__main__":
    sys.exit(main())
