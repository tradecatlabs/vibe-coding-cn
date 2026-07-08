#!/usr/bin/env python3
"""Check research domains have local raw fact snapshots."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESEARCH_DIR = ROOT / "research"
REQUIRED_RAW_FILES = [
    "README.md",
    "AGENTS.md",
    "sources.yml",
    "repository",
    "github-repo.raw.json",
    "github-readme.raw.md.txt",
    "github-root-contents.raw.json",
    "github-languages.raw.json",
]
REQUIRED_SOURCE_FIELDS = ["version: 1", "pulled_at:", "puller: scripts/fetch-research-raw.py", "files:"]
JSON_RAW_FILES = [
    "github-repo.raw.json",
    "github-root-contents.raw.json",
    "github-languages.raw.json",
]


def check_json(path: Path) -> str | None:
    try:
        json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        rel = path.relative_to(ROOT)
        return f"{rel}:{error.lineno}:{error.colno}: invalid JSON raw file"
    return None


def check_git_worktree(path: Path) -> str | None:
    result = subprocess.run(
        ["git", "-C", str(path), "rev-parse", "--is-inside-work-tree"],
        cwd=ROOT,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0 or result.stdout.strip() != "true":
        return f"{path.relative_to(ROOT)}: raw repository is not a valid Git working tree"
    return None


def main() -> int:
    errors: list[str] = []
    domain_files = sorted(RESEARCH_DIR.glob("*/domain.yml"))

    for domain_file in domain_files:
        domain_dir = domain_file.parent
        raw_dir = domain_dir / "raw"
        rel_raw = raw_dir.relative_to(ROOT)

        if not raw_dir.is_dir():
            errors.append(f"{rel_raw}: missing raw fact directory")
            continue

        for filename in REQUIRED_RAW_FILES:
            path = raw_dir / filename
            if filename == "repository":
                if not path.is_dir():
                    errors.append(f"{path.relative_to(ROOT)}: missing required raw repository directory")
                continue
            if not path.is_file():
                errors.append(f"{path.relative_to(ROOT)}: missing required raw fact file")

        sources = raw_dir / "sources.yml"
        if sources.is_file():
            text = sources.read_text(encoding="utf-8", errors="ignore")
            for field in REQUIRED_SOURCE_FIELDS:
                if field not in text:
                    errors.append(f"{sources.relative_to(ROOT)}: missing sources field '{field}'")
            if "path: repository/" not in text:
                errors.append(f"{sources.relative_to(ROOT)}: missing repository source record")

        raw_markdown = [
            path
            for path in raw_dir.glob("*.raw.md")
            if path.name not in {"README.md", "AGENTS.md"}
        ]
        for path in raw_markdown:
            errors.append(
                f"{path.relative_to(ROOT)}: raw external markdown must use '.raw.md.txt' to avoid local link checks"
            )

        for filename in JSON_RAW_FILES:
            path = raw_dir / filename
            if path.is_file():
                error = check_json(path)
                if error:
                    errors.append(error)

        repository = raw_dir / "repository"
        if repository.is_dir():
            error = check_git_worktree(repository)
            if error:
                errors.append(error)

    if errors:
        print("RESEARCH_RAW_ERRORS")
        for error in errors:
            print(error)
        print(f"TOTAL={len(errors)}")
        return 1

    print(f"OK research raw facts checked: {len(domain_files)} domains")
    return 0


if __name__ == "__main__":
    sys.exit(main())
