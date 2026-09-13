#!/usr/bin/env python3
"""Attack regressions for math tool maturity routing."""
from __future__ import annotations

import importlib.util
import json
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "scripts/validate_math_tool_maturity.py"


def load_module():
    spec = importlib.util.spec_from_file_location("tool_maturity", MODULE)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    module = load_module()
    baseline = json.loads(module.REGISTRY.read_text())
    assert module.validate() == []
    with tempfile.TemporaryDirectory(prefix="tool-maturity-") as directory:
        path = Path(directory) / "registry.json"
        value = json.loads(json.dumps(baseline))
        value["tools"][0]["runtime_route"] = "verifier"
        path.write_text(json.dumps(value))
        assert any("exceeds maturity" in error or "privileged route" in error for error in module.validate(path, module.SCHEMA, ROOT))
        value = json.loads(json.dumps(baseline))
        value["tools"] = value["tools"][1:]
        path.write_text(json.dumps(value))
        assert any("coverage mismatch" in error or "too short" in error for error in module.validate(path, module.SCHEMA, ROOT))
        value = json.loads(json.dumps(baseline))
        value["tools"][0]["evidence_refs"] = ["../secret"]
        path.write_text(json.dumps(value))
        assert any("unsafe evidence ref" in error for error in module.validate(path, module.SCHEMA, ROOT))
    print("math tool maturity attacks: PASS privilege, coverage, and path drift fail closed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
