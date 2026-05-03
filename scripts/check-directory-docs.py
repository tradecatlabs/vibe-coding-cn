#!/usr/bin/env python3
"""Check repository-owned directories have README.md and AGENTS.md."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_DIRS = [
    Path(".github"),
    Path(".github/ISSUE_TEMPLATE"),
    Path(".github/workflows"),
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
    Path("scripts/lib"),
    Path("skills"),
    Path("skills/auto-skill"),
    Path("skills/auto-skill/assets"),
    Path("skills/auto-skill/references"),
    Path("skills/auto-skill/scripts"),
    Path("tools"),
    Path("tools/chat-vault"),
    Path("tools/config"),
    Path("tools/config/.codex"),
    Path("tools/external"),
    Path("tools/prompts-library"),
    Path("tools/prompts-library/docs"),
    Path("tools/prompts-library/scripts"),
]
GENERATED_OR_VENDOR_DIRS = [
    Path("node_modules"),
]
SKIP_PARTS = {".git", ".history", "node_modules", "__pycache__"}
SKIP_PREFIXES = [
    Path(".github/wiki"),
]
VENDOR_SUBTREES = [
    Path("tools/external"),
    Path("tools/chat-vault"),
]


def should_skip(directory: Path) -> bool:
    rel = directory.relative_to(ROOT)
    if any(part in SKIP_PARTS for part in rel.parts):
        return True
    if directory.is_symlink():
        return True
    if any(rel == prefix or prefix in rel.parents for prefix in SKIP_PREFIXES):
        return True
    return any(vendor in rel.parents for vendor in VENDOR_SUBTREES)


def repository_owned_dirs() -> list[Path]:
    dirs = set(REQUIRED_DIRS)
    for directory in ROOT.rglob("*"):
        if not directory.is_dir():
            continue
        if should_skip(directory):
            continue
        dirs.add(directory.relative_to(ROOT))
    return sorted(dirs)


def main() -> int:
    errors: list[str] = []

    for rel_dir in repository_owned_dirs():
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

    print(f"OK directory README/AGENTS pairs checked: {len(repository_owned_dirs())} directories")
    return 0


if __name__ == "__main__":
    sys.exit(main())
