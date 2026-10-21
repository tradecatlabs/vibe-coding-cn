#!/usr/bin/env python3
"""Verify that research materials stay local and are excluded from Git."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESEARCH_PATH = ".github/context/research"
IGNORED_PATHS = (
    f"{RESEARCH_PATH}/README.md",
    f"{RESEARCH_PATH}/facts/sources.yml",
    f"{RESEARCH_PATH}/raw/repository/.git",
)


def main() -> int:
    tracked = subprocess.run(
        ["git", "ls-files", "-z", "--", RESEARCH_PATH],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
    ).stdout.split(b"\0")
    tracked = [path for path in tracked if path]
    errors: list[str] = []
    if tracked:
        errors.append(f"仍有 {len(tracked)} 个研究文件被 Git 跟踪")

    for path in IGNORED_PATHS:
        result = subprocess.run(
            ["git", "check-ignore", "--no-index", "--quiet", "--", path],
            cwd=ROOT,
            check=False,
        )
        if result.returncode != 0:
            errors.append(f"本地研究路径未被忽略：{path}")

    if errors:
        print("RESEARCH_DISTRIBUTION_ERRORS")
        for error in errors:
            print(error)
        return 1

    print("OK local research archive is untracked and ignored")
    return 0


if __name__ == "__main__":
    sys.exit(main())
