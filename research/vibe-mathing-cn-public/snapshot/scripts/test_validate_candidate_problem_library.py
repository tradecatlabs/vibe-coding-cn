#!/usr/bin/env python3
"""Self-contained attack tests for candidate snapshot isolation."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "validate_candidate_problem_library.py"


def load_module():
    spec = importlib.util.spec_from_file_location("candidate_validator", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load candidate validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def make_fixture(root: Path) -> None:
    for relative in (
        "problem-library/schema/candidate-observation.schema.json",
        "problem-library/schema/candidate-source.schema.json",
        "scripts/consolidate_candidates.py",
    ):
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / relative, target)

    raw = root / "problem-library/raw/candidates/fixture/data.json"
    raw.parent.mkdir(parents=True, exist_ok=True)
    raw_bytes = b"fixture distribution\n"
    raw.write_bytes(raw_bytes)
    parser = root / "scripts/consolidate_candidates.py"
    registry = {
        "schema_version": "1.0.0",
        "sources": [
            {
                "source_id": "fixture",
                "ingestion_role": "parsed-candidate",
                "record_scope": "problem_page",
                "parser": "fixture-v1",
                "license": {
                    "review": "reviewed",
                    "allowed_uses": ["local-reference", "query"],
                    "url": None,
                    "attribution": "synthetic fixture",
                },
                "admission_policy": "source-review-required",
                "status_map": {"open": "open_claimed"},
            }
        ],
    }
    registry_path = root / "problem-library/registry/candidate-sources.json"
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    registry_path.write_text(json.dumps(registry), encoding="utf-8")
    inventory = {
        "schema_version": "candidate-inventory.v1",
        "generated_at": "2026-09-01T00:00:00Z",
        "sources": {
            "fixture": {
                "files": [
                    {
                        "name": "data.json",
                        "url": "https://example.invalid/data.json",
                        "path": "problem-library/raw/candidates/fixture/data.json",
                        "sha256": hashlib.sha256(raw_bytes).hexdigest(),
                        "bytes": len(raw_bytes),
                    }
                ]
            }
        },
        "failures": [],
    }
    inventory_path = root / "problem-library/raw/candidates/inventory.json"
    inventory_path.parent.mkdir(parents=True, exist_ok=True)
    inventory_path.write_text(json.dumps(inventory), encoding="utf-8")
    parser_digest = digest(parser)
    observation = {
        "observation_id": "candidate:" + "a" * 64,
        "collection": "candidate",
        "source": "fixture",
        "source_native_id": "1",
        "source_url": "https://example.invalid/problem/1",
        "record_scope": "problem_page",
        "title": "Synthetic candidate",
        "statement_excerpt": "A synthetic candidate statement.",
        "excerpt_truncated": False,
        "excerpt_original_chars": 31,
        "source_status_raw": "open",
        "source_status_class": "open_claimed",
        "raw_artifact": {
            "path": "problem-library/raw/candidates/fixture/data.json",
            "sha256": hashlib.sha256(raw_bytes).hexdigest(),
            "locator": "1",
        },
        "parser": {"name": "fixture-v1", "version": "sha256:" + parser_digest},
        "retrieved_at": "2026-09-01T00:00:00Z",
        "license": registry["sources"][0]["license"],
        "categories": [],
        "extra": {},
        "admission": {"state": "candidate", "research_eligible": False},
    }
    lines = (json.dumps(observation, sort_keys=True, separators=(",", ":")) + "\n").encode()
    snapshot_dir = root / "problem-library/derived/candidate-observations/synthetic"
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    observations_path = snapshot_dir / "observations.jsonl"
    observations_path.write_bytes(lines)
    snapshot = {
        "schema_version": "candidate-snapshot.v1",
        "snapshot_id": "candidate-snapshot:synthetic",
        "decision": "PASS",
        "candidate_count": 1,
        "duplicate_observation_ids": 0,
        "source_counts": {"fixture": 1},
        "source_errors": [],
        "upstream_failures": [],
        "inputs": {
            "inventory_sha256": digest(inventory_path),
            "parser_sha256": parser_digest,
            "candidate_schema_sha256": digest(root / "problem-library/schema/candidate-observation.schema.json"),
            "source_registry_sha256": digest(registry_path),
        },
        "output": {
            "path": "problem-library/derived/candidate-observations/synthetic/observations.jsonl",
            "sha256": hashlib.sha256(lines).hexdigest(),
            "bytes": len(lines),
        },
    }
    (snapshot_dir / "snapshot.json").write_text(json.dumps(snapshot), encoding="utf-8")
    latest = {
        "schema_version": "candidate-latest.v1",
        "snapshot_id": "candidate-snapshot:synthetic",
        "snapshot_path": "problem-library/derived/candidate-observations/synthetic/snapshot.json",
        "observations_path": "problem-library/derived/candidate-observations/synthetic/observations.jsonl",
        "inputs": snapshot["inputs"],
        "output": snapshot["output"],
    }
    latest_path = root / "problem-library/derived/candidate-observations/latest.json"
    latest_path.write_text(json.dumps(latest), encoding="utf-8")


def main() -> int:
    module = load_module()
    with tempfile.TemporaryDirectory(prefix="candidate-validation-") as directory:
        root = Path(directory)
        make_fixture(root)
        assert module.validate_paths(root=root) == []
        latest = json.loads(
            (root / "problem-library/derived/candidate-observations/latest.json").read_text()
        )
        observations = root / latest["observations_path"]
        first = observations.read_text(encoding="utf-8")
        observations.write_text(first + first, encoding="utf-8")
        assert any("duplicate observation_id" in error for error in module.validate_paths(root=root))

        make_fixture(root)
        registry_path = root / "problem-library/registry/candidate-sources.json"
        registry = json.loads(registry_path.read_text())
        registry["sources"][0]["parser"] = "other-v1"
        registry_path.write_text(json.dumps(registry), encoding="utf-8")
        errors = module.validate_paths(root=root)
        assert any("parser disagrees" in error or "input digests" in error for error in errors)

        make_fixture(root)
        latest_path = root / "problem-library/derived/candidate-observations/latest.json"
        latest = json.loads(latest_path.read_text())
        latest["observations_path"] = "problem-library/derived/candidate-observations/../escape.jsonl"
        latest_path.write_text(json.dumps(latest), encoding="utf-8")
        assert any("unsafe latest observations path" in error for error in module.validate_paths(root=root))
    print("candidate snapshot attacks: PASS duplicate, parser, and path drift fail closed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
