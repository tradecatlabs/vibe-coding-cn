#!/usr/bin/env python3
"""Regression tests for the read-only vibemathing public index."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module():
    path = ROOT / "scripts/query_vibemathing_public.py"
    spec = importlib.util.spec_from_file_location("query_vibemathing_public", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load public index module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def repository(name: str, *, private: bool = False, fork: bool = False, archived: bool = False) -> dict:
    return {
        "name": name,
        "full_name": f"vibemathing/{name}",
        "html_url": f"https://github.com/vibemathing/{name}",
        "description": "example",
        "private": private,
        "fork": fork,
        "archived": archived,
        "default_branch": "main",
        "updated_at": "2026-09-07T00:00:00Z",
        "topics": ["vibe-mathing"],
    }


def main() -> int:
    module = load_module()
    items = module.load_repositories(
        [
            repository("problem-opg-example"),
            repository("problem-um-example"),
            repository("vibe-mathing-problem-public-template"),
            repository("vibe-mathing-problem-library-public"),
        ]
    )
    assert [item["name"] for item in module.select_repositories(items, "concrete")] == [
        "problem-opg-example",
        "problem-um-example",
    ]
    assert [item["name"] for item in module.select_repositories(items, "candidate")] == [
        "problem-um-example"
    ]
    assert [item["name"] for item in module.select_repositories(items, "library")] == [
        "vibe-mathing-problem-library-public"
    ]
    catalog = module.validate_catalog(
        {
            "schema_version": "1.0.0",
            "count": 1,
            "records": [
                {
                    "problem_id": "problem:opg-example",
                    "lifecycle": "active",
                    "path": "catalog/problems/opg-example.json",
                    "contract_sha256": "a" * 64,
                }
            ],
        }
    )
    assert catalog["records"][0]["contract_url"].endswith("catalog/problems/opg-example.json")
    for bad in (
        repository("problem-opg-private", private=True),
        repository("problem-opg-fork", fork=True),
        repository("problem-opg-archived", archived=True),
    ):
        try:
            module.validate_repository(bad)
        except module.PublicIndexError:
            pass
        else:
            raise AssertionError("unsafe repository metadata was accepted")
    print("vibemathing public index tests: PASS namespace, catalog, and safety boundaries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
