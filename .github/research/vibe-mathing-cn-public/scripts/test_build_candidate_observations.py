#!/usr/bin/env python3
"""Regression tests for artifact binding, stable IDs, truncation, and publication."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import tempfile
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parent / "build_candidate_observations.py"


def load_module():
    spec = importlib.util.spec_from_file_location("candidate_builder", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load candidate builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    module = load_module()
    with tempfile.TemporaryDirectory(prefix="candidate-builder-") as directory:
        root = Path(directory)
        raw = root / "problem-library/raw/candidates/fixture"
        derived = root / "problem-library/derived/candidate-observations"
        (raw / "api").mkdir(parents=True)
        derived.mkdir(parents=True)
        module.ROOT = root
        module.RAW = root / "problem-library/raw/candidates"
        module.DERIVED = derived

        first = raw / "api/questions-page-01.json"
        first_bytes = b'{"items":[{"question_id":42,"title":"Synthetic"}]}'
        first.write_bytes(first_bytes)
        second = raw / "api/questions-page-02.json"
        second_bytes = b'{"items":[{"question_id":43,"title":"Other"}]}'
        second.write_bytes(second_bytes)
        files = [
            {
                "name": first.name,
                "url": "https://example.invalid/page-1",
                "path": str(first.relative_to(root)),
                "sha256": hashlib.sha256(first_bytes).hexdigest(),
                "bytes": len(first_bytes),
            },
            {
                "name": second.name,
                "url": "https://example.invalid/page-2",
                "path": str(second.relative_to(root)),
                "sha256": hashlib.sha256(second_bytes).hexdigest(),
                "bytes": len(second_bytes),
            },
        ]
        record = {
            "title": "Synthetic",
            "statement": "A synthetic statement.",
            "url": "https://mathoverflow.net/questions/42",
            "extra": {"question_id": 42},
            "status": "open",
        }
        artifact = module.choose_artifact("mathoverflow", record, files)
        assert artifact["path"] == files[0]["path"]
        assert artifact["locator"] == "question-id:42"

        unrelated = {**record, "extra": {"question_id": 999}, "title": "Missing"}
        try:
            module.choose_artifact("mathoverflow", unrelated, files)
        except ValueError as exc:
            assert "cannot bind" in str(exc) or "matches" in str(exc)
        else:
            raise AssertionError("unbound record must fail closed")

        unrelated_single = {**record, "title": "No matching single distribution", "extra": {"question_id": 999}}
        try:
            module.choose_artifact("mathoverflow", unrelated_single, [files[1]])
        except ValueError as exc:
            assert "cannot bind" in str(exc) or "matches" in str(exc)
        else:
            raise AssertionError("a single unrelated artifact must fail closed")

        source = {
            "source_id": "mathoverflow",
            "record_scope": "forum_question",
            "parser": "mathoverflow-v1",
            "status_map": {"open": "open_claimed"},
            "license": {
                "review": "reviewed",
                "allowed_uses": ["local-reference"],
                "url": None,
                "attribution": "synthetic",
            },
        }
        long_record = {**record, "statement": "x" * (module.MAX_EXCERPT_CHARS + 10)}
        one = module.build_observation(
            long_record,
            ordinal=1,
            source=source,
            files=files,
            retrieved_at="2026-09-01T00:00:00Z",
            parser_digest="a" * 64,
        )
        two = module.build_observation(
            long_record,
            ordinal=2,
            source=source,
            files=files,
            retrieved_at="2026-09-01T00:00:00Z",
            parser_digest="a" * 64,
        )
        assert one["observation_id"] == two["observation_id"]
        assert one["excerpt_truncated"] is True
        assert one["statement_excerpt"].endswith(module.TRUNCATION_MARKER)
        assert one["excerpt_original_chars"] == module.MAX_EXCERPT_CHARS + 10

        output_dir = derived / "snapshot"
        snapshot = {
            "schema_version": "candidate-snapshot.v1",
            "snapshot_id": "candidate-snapshot:test",
            "inputs": {"inventory_sha256": "a" * 64},
            "output": {
                "path": "problem-library/derived/candidate-observations/snapshot/observations.jsonl",
                "sha256": hashlib.sha256(b"{}\n").hexdigest(),
                "bytes": 3,
            },
            "decision": "PASS",
        }
        module.publish_snapshot(output_dir, snapshot, b"{}\n", update_latest=True)
        latest = json.loads((derived / "latest.json").read_text(encoding="utf-8"))
        assert latest["inputs"] == snapshot["inputs"]
        assert latest["output"] == snapshot["output"]
        assert (output_dir / "snapshot.json").is_file()

    print("candidate builder tests: PASS binding, stable IDs, truncation, and atomic latest publication")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
