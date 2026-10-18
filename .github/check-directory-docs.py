#!/usr/bin/env python3
"""Check repository-owned directories have README.md and AGENTS.md."""

from __future__ import annotations

import sys
from pathlib import Path
from source_boundaries import SOURCE_PREFIXES, VENDOR_SUBTREES, is_research_repository_snapshot


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_DIRS = list(map(Path, (
    '.github', '.github/ISSUE_TEMPLATE',
    '.github/context', '.github/context/assets', '.github/context/ai-citation',
    '.github/context/assets/datasets', '.github/context/assets/images', '.github/context/assets/templates',
    '.github/context/getting-started', '.github/context/gongfa', '.github/context/faqi',
    '.github/context/research', '.github/context/metadata', '.github/context/prompts',
    '.github/extensions',
    '.github/skills', '.github/skills/auto-skill', '.github/skills/auto-skill/assets',
    '.github/skills/auto-skill/references', '.github/skills/auto-tmux',
    '.github/extensions/prompts-library', '.github/extensions/prompts-library/docs',
    '.github/extensions/prompts-library/scripts',
)))
COLLECTION_DIRS = {Path('.github/context/gongfa'), Path('.github/context/faqi')}
RETIRED_DIRS = (Path('.github/workflows'), Path('.github/lib'))
README_OPTIONAL_DIRS = {
    # GitHub repository pages can surface `.github/README.md` as an overview file.
    # Keep the root project README authoritative and use `.github/AGENTS.md` only.
    Path(".github"),
}
GENERATED_OR_VENDOR_DIRS = [
    Path("build"),
    Path("node_modules"),
]
SKIP_PARTS = {".git", ".history", "build", "node_modules", "__pycache__"}
SKIP_PREFIXES = SOURCE_PREFIXES


def should_skip(directory: Path) -> bool:
    rel = directory.relative_to(ROOT)
    if any(part in SKIP_PARTS for part in rel.parts):
        return True
    if is_research_repository_snapshot(rel):
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

    for rel_dir in RETIRED_DIRS:
        directory = ROOT / rel_dir
        if directory.exists() or directory.is_symlink():
            errors.append(f'{rel_dir}: 已退役目录不得重新创建')

    for rel_dir in repository_owned_dirs():
        directory = ROOT / rel_dir
        if not directory.is_dir():
            errors.append(f"{rel_dir}: required directory is missing")
            continue
        if rel_dir in COLLECTION_DIRS:
            if ({entry.name for entry in directory.iterdir()} != {'data.json', 'README.md'}
                    or any(entry.is_symlink() for entry in directory.iterdir())):
                errors.append(f'{rel_dir}: 文集必须且只能包含data.json和生成的README.md')
            if not (ROOT / '.github/context/AGENTS.md').is_file():
                errors.append(f'{rel_dir}: missing inherited context rules')
            continue
        required_files = ['AGENTS.md'] if rel_dir in README_OPTIONAL_DIRS else ['README.md', 'AGENTS.md']
        for filename in required_files:
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
