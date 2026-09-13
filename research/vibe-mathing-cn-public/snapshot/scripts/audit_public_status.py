#!/usr/bin/env python3
"""Read-only, bounded audit of the public canonical ledgers and solution index.

This command reports the current repository snapshot only.  Its output is not a
Problem, Attempt, Result, proof, or mathematical evidence receipt.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import sys
from pathlib import Path
from typing import Any

PUBLIC_REPOSITORY = "vibemathing/vibe-mathing-cn-public"
STATUS_SCHEMA = "public-status.v1"
MAX_SOURCE_BYTES = 4_000_000
LEDGER_PATHS = {
    "canonical_problem_records": "problem-library/records/canonical-problems.jsonl",
    "attempt_records": "research/records/attempts.jsonl",
    "result_records": "result-library/records/results.jsonl",
}
SOLUTION_INDEX_PATH = "result-library/indexes/solutions.json"


class StatusAuditError(RuntimeError):
    """Raised when the public status snapshot cannot be read safely."""


def _read_regular(root: Path, relative: str) -> bytes:
    path = root / relative
    if path.is_symlink():
        raise StatusAuditError(f"source path is a symlink: {relative}")
    try:
        file_stat = path.stat()
    except OSError as exc:
        raise StatusAuditError(f"cannot stat {relative}: {exc}") from exc
    if not stat.S_ISREG(file_stat.st_mode):
        raise StatusAuditError(f"source path is not a regular file: {relative}")
    if file_stat.st_size > MAX_SOURCE_BYTES:
        raise StatusAuditError(f"source exceeds {MAX_SOURCE_BYTES} bytes: {relative}")
    try:
        data = path.read_bytes()
    except OSError as exc:
        raise StatusAuditError(f"cannot read {relative}: {exc}") from exc
    if len(data) > MAX_SOURCE_BYTES:
        raise StatusAuditError(f"source exceeds {MAX_SOURCE_BYTES} bytes: {relative}")
    return data


def _count_jsonl(data: bytes, relative: str) -> int:
    count = 0
    for line_number, raw_line in enumerate(data.splitlines(), start=1):
        if not raw_line.strip():
            continue
        try:
            value = json.loads(raw_line.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise StatusAuditError(f"invalid JSONL at {relative}:{line_number}: {exc}") from exc
        if not isinstance(value, dict):
            raise StatusAuditError(f"JSONL record at {relative}:{line_number} is not an object")
        count += 1
    return count


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def build_status(project_root: Path) -> dict[str, Any]:
    """Return a bounded status snapshot without writing to the repository."""
    root = Path(os.path.abspath(project_root))
    if (
        root.is_symlink()
        or not root.is_dir()
        or root.resolve() != root
        or any(parent.is_symlink() for parent in (root.parent, *root.parents))
    ):
        raise StatusAuditError("project root must be a regular directory")

    counts: dict[str, int] = {}
    digests: dict[str, str] = {}
    for field, relative in LEDGER_PATHS.items():
        data = _read_regular(root, relative)
        counts[field] = _count_jsonl(data, relative)
        digests[relative] = _digest(data)

    index_data = _read_regular(root, SOLUTION_INDEX_PATH)
    try:
        index = json.loads(index_data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise StatusAuditError(f"invalid JSON in {SOLUTION_INDEX_PATH}: {exc}") from exc
    if not isinstance(index, dict) or not isinstance(index.get("result_ids"), list):
        raise StatusAuditError(f"{SOLUTION_INDEX_PATH} must contain a result_ids list")
    result_ids = index["result_ids"]
    if any(not isinstance(result_id, str) or not result_id for result_id in result_ids):
        raise StatusAuditError(f"{SOLUTION_INDEX_PATH} contains an invalid result ID")
    if len(set(result_ids)) != len(result_ids):
        raise StatusAuditError(f"{SOLUTION_INDEX_PATH} contains duplicate result IDs")
    counts["solution_result_ids"] = len(result_ids)
    digests[SOLUTION_INDEX_PATH] = _digest(index_data)

    empty = all(value == 0 for value in counts.values())
    return {
        "schema_version": STATUS_SCHEMA,
        "repository": PUBLIC_REPOSITORY,
        "status": "empty" if empty else "non-empty",
        "counts": counts,
        "source_digests": {
            "algorithm": "sha256",
            "files": digests,
        },
        "source_paths": [*LEDGER_PATHS.values(), SOLUTION_INDEX_PATH],
        "not_mathematical_evidence": True,
    }


def _print_human(report: dict[str, Any]) -> None:
    print(f"Public status snapshot: {report['status']}")
    for field, count in report["counts"].items():
        print(f"- {field}: {count}")
    print("- source digests: sha256 (repository-relative files)")
    print("- not mathematical evidence: true")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument(
        "--expect-empty",
        action="store_true",
        help="fail if any canonical ledger or solution-index result ID exists",
    )
    args = parser.parse_args(argv)
    try:
        report = build_status(Path(args.project_root))
    except StatusAuditError as exc:
        print(f"Public status snapshot: BLOCK - {exc}", file=sys.stderr)
        return 1
    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        _print_human(report)
    if args.expect_empty and report["status"] != "empty":
        print("Public status snapshot: BLOCK - expected an empty public status", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
