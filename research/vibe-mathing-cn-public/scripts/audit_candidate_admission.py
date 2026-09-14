#!/usr/bin/env python3
"""Produce a source-level admission audit; never writes admitted or canonical records."""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from validate_candidate_problem_library import (
    MAX_RECORDS,
    _reject_json_constant,
    iter_text_lines_nofollow,
    read_json,
    safe_relative_path,
)

ROOT = Path(__file__).resolve().parents[1]
LIBRARY = ROOT / "problem-library"
LATEST = LIBRARY / "derived/candidate-observations/latest.json"
REGISTRY = LIBRARY / "registry/candidate-sources.json"
ADMITTED = LIBRARY / "records/problems.jsonl"


def norm(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip().casefold()


def read_jsonl(path: Path):
    count = 0
    for _line_number, line in iter_text_lines_nofollow(path):
        if not line.strip():
            continue
        count += 1
        if count > MAX_RECORDS:
            raise ValueError(f"JSONL records exceed limit {MAX_RECORDS}")
        yield json.loads(line, parse_constant=_reject_json_constant)


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit one candidate source without promoting records.")
    parser.add_argument("--source", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if not isinstance(args.source, str) or not re.fullmatch(
        r"[a-z][a-z0-9_]{1,63}", args.source
    ):
        parser.error("source is invalid")
    registry = read_json(REGISTRY)
    if not isinstance(registry, dict) or not isinstance(registry.get("sources"), list):
        raise ValueError("candidate source registry is invalid")
    policies: dict[str, dict[str, Any]] = {}
    for item in registry["sources"]:
        if not isinstance(item, dict) or not isinstance(
            item.get("source_id"), str
        ) or not re.fullmatch(r"[a-z][a-z0-9_]{1,63}", item["source_id"]):
            raise ValueError("candidate source registry entry is invalid")
        source_id = item["source_id"]
        if source_id in policies:
            raise ValueError("candidate source registry contains duplicate IDs")
        policies[source_id] = item
    policy = policies.get(args.source)
    if policy is None:
        parser.error("source is not registered")
    latest = read_json(LATEST)
    if not isinstance(latest, dict):
        raise ValueError("candidate latest pointer is invalid")
    observations_path = safe_relative_path(
        ROOT,
        latest.get("observations_path"),
        prefix="problem-library/derived/candidate-observations/",
        label="latest observations path",
    )
    observations = []
    for value in read_jsonl(observations_path):
        if not isinstance(value, dict):
            raise ValueError("candidate observation is not an object")
        if value.get("source") == args.source:
            if value.get("admission") != {
                "state": "candidate",
                "research_eligible": False,
            }:
                raise ValueError("candidate observation has unsafe admission state")
            observations.append(value)
    admitted_keys: set[tuple[str, str]] = set()
    if ADMITTED.is_file():
        for value in read_jsonl(ADMITTED):
            if not isinstance(value, dict):
                raise ValueError("admitted source record is not an object")
            title = value.get("title", "")
            statement = value.get("statement_excerpt", "")
            if isinstance(title, str) and isinstance(statement, str):
                admitted_keys.add((norm(title), norm(statement)))
    blockers: list[str] = []
    warnings: list[str] = []
    if not observations:
        blockers.append("source has no CandidateObservation records")
    if policy["ingestion_role"] != "parsed-candidate":
        blockers.append(f"ingestion_role={policy['ingestion_role']} is not parsed-candidate")
    if policy["admission_policy"] in {"discovery-only", "never-auto-admit"}:
        blockers.append(f"admission_policy={policy['admission_policy']}")
    if policy["license"]["review"] != "reviewed":
        blockers.append("source license review is not complete")
    if "query" not in policy["license"]["allowed_uses"]:
        blockers.append("source is not approved for query use")
    truncated = sum(value.get("excerpt_truncated") is True for value in observations)
    short = sum(
        isinstance(value.get("statement_excerpt"), str)
        and len(value["statement_excerpt"]) < 40
        for value in observations
    )
    unknown_status = sum(value.get("source_status_class") == "unknown" for value in observations)
    exact_existing = sum(
        isinstance(value.get("title"), str)
        and isinstance(value.get("statement_excerpt"), str)
        and (norm(value["title"]), norm(value["statement_excerpt"])) in admitted_keys
        for value in observations
    )
    if truncated:
        warnings.append(f"{truncated} excerpts are truncated and require source-level reparse")
    if short:
        warnings.append(f"{short} excerpts are shorter than 40 characters")
    if unknown_status:
        warnings.append(f"{unknown_status} records have unknown source status")
    if exact_existing:
        warnings.append(f"{exact_existing} records exactly overlap admitted title/statement pairs")
    report: dict[str, Any] = {
        "schema_version": "candidate-admission-audit.v1",
        "source": args.source,
        "decision": "BLOCK" if blockers else "READY_FOR_HUMAN_SOURCE_REVIEW",
        "candidate_count": len(observations),
        "status_counts": dict(sorted(Counter(value["source_status_class"] for value in observations).items())),
        "blockers": blockers,
        "warnings": warnings,
        "mathematical_effect": "No SourceRecord, ProblemContract, Attempt, Result, or Solution is created.",
    }
    if args.json:
        print(
            json.dumps(
                report, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False
            )
        )
    else:
        print(f"{args.source}: {report['decision']} candidates={len(observations)}")
        for blocker in blockers:
            print(f"  BLOCK: {blocker}")
        for warning in warnings:
            print(f"  WARN: {warning}")
    return 0 if not blockers else 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, TypeError, KeyError, AttributeError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
