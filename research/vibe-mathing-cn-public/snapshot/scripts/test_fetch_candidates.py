#!/usr/bin/env python3
"""Safety regressions for the candidate source fetcher."""
from __future__ import annotations

import fcntl
import importlib.util
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts/fetch_candidates.py"


def load_module():
    spec = importlib.util.spec_from_file_location("fetch_candidates", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load fetcher")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    text = MODULE_PATH.read_text(encoding="utf-8")
    assert "reset\", \"--hard" not in text
    module = load_module()
    assert module.source_coverage_errors() == []
    assert module.REGISTRY_ONLY_SOURCES == {"awesome_solved_index"}

    fetcher = module.Fetcher(timeout=1, delay=0, retries=1)
    try:
        fetcher.fetch("http://example.test")
    except module.FetchError:
        pass
    else:
        raise AssertionError("non-HTTPS candidate URL must fail closed")

    class FakeHeaders:
        def get(self, _name):
            return None

    class OversizedResponse:
        headers = FakeHeaders()

        def read(self, _size):
            return b"xxxx"

    try:
        module.Fetcher._read_limited(OversizedResponse(), 3)
    except module.ResponseTooLarge:
        pass
    else:
        raise AssertionError("oversized response must fail before unbounded buffering")

    old_argv = sys.argv
    with tempfile.TemporaryDirectory(prefix="candidate-fetch-") as directory:
        raw = Path(directory) / "raw"
        module.ROOT = Path(directory)
        module.RAW = raw
        module.INVENTORY_PATH = raw / "inventory.json"
        module.LOCK_PATH = raw / ".fetch.lock"
        module.SOURCES = {"fixture": lambda fetcher, sink, refresh=False: sink.fail("fixture", "https://example.test", "expected")}
        sink = module.Sink({"sources": {}}, "fixture")
        outside = Path(directory) / "outside"
        outside.mkdir()
        (raw / "fixture").mkdir(parents=True)
        (raw / "fixture" / "link").symlink_to(outside, target_is_directory=True)
        try:
            sink.save("link/escape", "https://example.test", b"x")
        except ValueError:
            pass
        else:
            raise AssertionError("candidate artifact symlink must fail closed")
        for unsafe_name in ("../escape", "/absolute"):
            try:
                sink.save(unsafe_name, "https://example.test", b"x")
            except ValueError:
                pass
            else:
                raise AssertionError("candidate artifact path must remain inside raw root")
        sys.argv = [str(MODULE_PATH), "--only", "fixture"]
        assert module.main() == 1
        sys.argv = [str(MODULE_PATH), "--only", "fixture", "--allow-partial"]
        assert module.main() == 0
        raw.mkdir(parents=True, exist_ok=True)
        descriptor = os.open(module.LOCK_PATH, os.O_WRONLY | os.O_CREAT, 0o600)
        fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        sys.argv = [str(MODULE_PATH), "--only", "fixture"]
        assert module.main() == 1
        os.close(descriptor)
    sys.argv = old_argv
    print("candidate fetcher safety tests: PASS failures and concurrent writers fail closed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
