#!/usr/bin/env python3
"""Attack tests for the PLFB conceptual metamodel registry."""
from __future__ import annotations

import copy
import json
from pathlib import Path

from validate_plfb_metamodel import validate

ROOT = Path(__file__).resolve().parents[1]
CONTROL = ROOT / "governance/control-plane"


def load(name: str) -> dict:
    return json.loads((CONTROL / name).read_text(encoding="utf-8"))


def must_fail(registry: dict, schema: dict, needle: str) -> None:
    errors = validate(registry, schema, ROOT)
    assert errors, f"attack unexpectedly passed: {needle}"
    assert any(needle in error for error in errors), (needle, errors)


def main() -> int:
    registry = load("plfb-metamodel.v0.1.json")
    schema = load("plfb-metamodel.schema.json")
    assert validate(registry, schema, ROOT) == []

    duplicate = copy.deepcopy(registry)
    duplicate["point_types"].append(copy.deepcopy(duplicate["point_types"][0]))
    must_fail(duplicate, schema, "duplicate point type")

    missing_line = copy.deepcopy(registry)
    missing_line["line_types"].pop()
    must_fail(missing_line, schema, "exactly 58 line types")

    unknown_face = copy.deepcopy(registry)
    unknown_face["point_types"][0]["primary_face"] = "F99"
    must_fail(unknown_face, schema, "unknown primary face")

    missing_ownership = copy.deepcopy(registry)
    missing_ownership["faces"][0]["point_types"].remove("point.body")
    must_fail(missing_ownership, schema, "absent from primary face")

    unknown_line = copy.deepcopy(registry)
    unknown_line["faces"][0]["line_types"].append("line.unknown")
    must_fail(unknown_line, schema, "unknown line type")

    wrong_osps = copy.deepcopy(registry)
    wrong_osps["faces"][3]["model"] = "PWTSJ"
    must_fail(wrong_osps, schema, "F04 must be OSPS")

    extra_root_model = copy.deepcopy(registry)
    extra_root_model["faces"][0]["model"] = "OSPS"
    must_fail(extra_root_model, schema, "model bindings must be exactly")

    status_escalation = copy.deepcopy(registry)
    status_escalation["point_types"][0]["implementation_status"] = "implemented"
    must_fail(status_escalation, schema, "cannot claim implemented point")

    capability_escalation = copy.deepcopy(registry)
    capability_escalation["capability_claims"]["osps_orchestrator_implemented"] = True
    must_fail(capability_escalation, schema, "osps_orchestrator_implemented")

    missing_doc = copy.deepcopy(registry)
    missing_doc["document_refs"][0] = "governance/strategy/DOES_NOT_EXIST.md"
    must_fail(missing_doc, schema, "document_ref does not exist")

    missing_owner = copy.deepcopy(registry)
    missing_owner["faces"][0]["owner_paths"][0] = "missing/owner/path"
    must_fail(missing_owner, schema, "owner path does not exist")

    print("PLFB metamodel tests: PASS duplicate, count, cross-reference, ownership, face-model, status, capability and path attacks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
