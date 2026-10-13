#!/usr/bin/env python3
"""Regression tests for the read-only public status auditor."""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_public_status as audit  # noqa: E402


ROOT = Path(__file__).resolve().parents[1]


def test_public_snapshot_is_empty_and_digest_bound() -> None:
    report = audit.build_status(ROOT)
    assert report["schema_version"] == "public-status.v1"
    assert report["repository"] == "vibemathing/vibe-mathing-cn-public"
    assert report["status"] == "empty"
    assert report["counts"] == {
        "canonical_problem_records": 0,
        "attempt_records": 0,
        "result_records": 0,
        "solution_result_ids": 0,
    }
    assert report["source_digests"]["algorithm"] == "sha256"
    assert all(len(value) == 64 for value in report["source_digests"]["files"].values())
    assert report["not_mathematical_evidence"] is True


def test_non_empty_snapshot_is_reported_without_admission() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        for relative in audit.LEDGER_PATHS.values():
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("", encoding="utf-8")
        index = root / audit.SOLUTION_INDEX_PATH
        index.parent.mkdir(parents=True, exist_ok=True)
        index.write_text(json.dumps({"schema_version": "2.0.0", "result_ids": ["result:test"]}), encoding="utf-8")
        report = audit.build_status(root)
        assert report["status"] == "non-empty"
        assert report["counts"]["solution_result_ids"] == 1
        assert report["not_mathematical_evidence"] is True


def test_malformed_jsonl_fails_closed() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        for field, relative in audit.LEDGER_PATHS.items():
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("not-json\n" if field == "attempt_records" else "", encoding="utf-8")
        index = root / audit.SOLUTION_INDEX_PATH
        index.parent.mkdir(parents=True, exist_ok=True)
        index.write_text(json.dumps({"result_ids": []}), encoding="utf-8")
        try:
            audit.build_status(root)
        except audit.StatusAuditError as exc:
            assert "attempts.jsonl:1" in str(exc)
        else:
            raise AssertionError("malformed JSONL must fail closed")


if __name__ == "__main__":
    test_public_snapshot_is_empty_and_digest_bound()
    test_non_empty_snapshot_is_reported_without_admission()
    test_malformed_jsonl_fails_closed()
    print("Public status auditor tests: PASS read-only, bounded, and fail-closed")
