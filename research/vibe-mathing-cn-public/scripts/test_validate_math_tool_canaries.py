#!/usr/bin/env python3
"""Self-contained attack tests for the bounded canary report validator."""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts/validate_math_tool_canaries.py"


def load_module():
    spec = importlib.util.spec_from_file_location("canary_validator", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load canary validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def report(module) -> dict:
    results = [
        {
            "tool_id": "T13",
            "component": "synthetic",
            "kind": kind,
            "status": "PASS",
            "detail": "bounded fixture",
            "duration_seconds": 0.001,
            "termination_status": "timed_out" if kind == "timeout" else "completed",
        }
        for kind in ("positive", "negative", "error", "timeout")
    ]
    return {
        "schema_version": "math-tool-canary.v1",
        "generated_at": "2026-09-01T00:00:00Z",
        "scope": "synthetic-bounded-runtime",
        "runner": {
            "source": "scripts/run_math_tool_canaries.py",
            "sha256": hashlib.sha256(module.RUNNER.read_bytes()).hexdigest(),
            "runtime_binding": "explicit-environment",
        },
        "execution_policy": {
            "timeout_seconds": 8,
            "memory_budget_mb": 256,
            "threads_max": 1,
            "max_output_bytes": 1048576,
            "stop_condition": "每个 bounded fixture 返回预期结果",
            "termination": {
                "status": "completed",
                "reason": "synthetic report assembled",
            },
        },
        "tools": ["T13"],
        "identities": {},
        "results": results,
        "summary": {"case_count": 4, "passed": 4, "failed": 0, "all_passed": True},
    }


def check(module, value: dict) -> list[str]:
    with tempfile.TemporaryDirectory(prefix="math-tool-canary-validation-") as directory:
        report_path = Path(directory) / "report.json"
        report_path.write_text(json.dumps(value), encoding="utf-8")
        return module.validate(report_path, module.SCHEMA)


def main() -> int:
    module = load_module()
    baseline = report(module)
    assert check(module, baseline) == []

    missing_timeout = copy.deepcopy(baseline)
    missing_timeout["results"] = [
        item for item in missing_timeout["results"] if item["kind"] != "timeout"
    ]
    missing_timeout["summary"] = {"case_count": 3, "passed": 3, "failed": 0, "all_passed": True}
    assert any("missing canary kinds" in error for error in check(module, missing_timeout))

    tampered_runner = copy.deepcopy(baseline)
    tampered_runner["runner"]["sha256"] = "0" * 64
    assert any("runner.sha256" in error for error in check(module, tampered_runner))

    extra = copy.deepcopy(baseline)
    extra["results"][0]["raw_output"] = "must not be persisted"
    assert check(module, extra)
    print("math tool canary attacks: PASS timeout, runner, and output-boundary checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
