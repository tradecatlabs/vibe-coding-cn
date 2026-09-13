#!/usr/bin/env python3
"""Regression tests for admitted/candidate query isolation."""
from __future__ import annotations

import importlib.util
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]


def load_module():
    path = ROOT / "scripts/query_problem_library.py"
    spec = importlib.util.spec_from_file_location("query_problem_library", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load query module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def args(**changes):
    value = dict(source=None, status=None, status_class=None, category=None, text=None)
    value.update(changes)
    return SimpleNamespace(**value)


def main() -> int:
    module = load_module()
    admitted = module.admitted_view(
        {
            "id": "source:1",
            "source": "wikipedia",
            "status": "open",
            "title": "Example",
            "statement_excerpt": "Riemann example",
            "categories": ["Number Theory"],
            "detail_url": "https://example.test/1",
        }
    )
    candidate = module.candidate_view(
        {
            "observation_id": "candidate:" + "a" * 64,
            "source": "theoremdb",
            "source_status_raw": "resolved",
            "source_status_class": "closed_claimed",
            "title": "Candidate",
            "statement_excerpt": "A candidate statement",
            "categories": ["Algebra"],
            "source_url": "https://example.test/2",
            "admission": {"state": "candidate", "research_eligible": False},
        }
    )
    assert admitted["_research_eligible"] is False
    assert candidate["_research_eligible"] is False
    assert module.matches(admitted, args(text="riemann"))
    assert module.matches(candidate, args(status_class="closed_claimed"))
    assert not module.matches(admitted, args(status_class="open_claimed"))
    assert not module.matches(candidate, args(status="open"))
    print("problem query federation tests: PASS candidates remain explicit and research-ineligible")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
