#!/usr/bin/env python3
"""Validate the conceptual Point-Line-Face-Body registry fail-closed."""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = Path("governance/control-plane/plfb-metamodel.v0.1.json")
SCHEMA = Path("governance/control-plane/plfb-metamodel.schema.json")
EXPECTED_FACES = {f"F{i:02d}" for i in range(1, 14)}
EXPECTED_BODIES = {f"B{i}" for i in range(5)}
EXPECTED_PRIMITIVES = {"point", "line", "face", "body"}


def schema_errors(instance: Any, schema: dict[str, Any]) -> list[str]:
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [
        f"schema: {error.message}"
        for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.path))
    ]


def duplicates(values: list[str]) -> list[str]:
    return sorted(value for value, count in Counter(values).items() if count > 1)


def validate(registry: dict[str, Any], schema: dict[str, Any], root: Path) -> list[str]:
    errors = schema_errors(registry, schema)

    primitives = [item.get("id") for item in registry.get("primitives", []) if isinstance(item, dict)]
    if set(primitives) != EXPECTED_PRIMITIVES or len(primitives) != len(EXPECTED_PRIMITIVES):
        errors.append("primitives must be exactly point, line, face, body")

    points = [item for item in registry.get("point_types", []) if isinstance(item, dict)]
    lines = [item for item in registry.get("line_types", []) if isinstance(item, dict)]
    faces = [item for item in registry.get("faces", []) if isinstance(item, dict)]
    bodies = [item for item in registry.get("body_types", []) if isinstance(item, dict)]
    point_ids = [str(item.get("id")) for item in points]
    line_ids = [str(item.get("id")) for item in lines]
    face_ids = [str(item.get("id")) for item in faces]
    body_ids = [str(item.get("id")) for item in bodies]

    for label, values in (("point type", point_ids), ("line type", line_ids), ("face", face_ids), ("body type", body_ids)):
        dupes = duplicates(values)
        if dupes:
            errors.append(f"duplicate {label} IDs: {', '.join(dupes)}")

    if len(point_ids) != 61:
        errors.append(f"public v0.1 registry must contain exactly 61 point types, observed {len(point_ids)}")
    if len(line_ids) != 58:
        errors.append(f"public v0.1 registry must contain exactly 58 line types, observed {len(line_ids)}")

    if set(face_ids) != EXPECTED_FACES or len(face_ids) != len(EXPECTED_FACES):
        errors.append("faces must be exactly F01 through F13")
    if set(body_ids) != EXPECTED_BODIES or len(body_ids) != len(EXPECTED_BODIES):
        errors.append("body types must be exactly B0 through B4")

    point_set, line_set, face_set = set(point_ids), set(line_ids), set(face_ids)
    point_usage: Counter[str] = Counter()
    line_usage: Counter[str] = Counter()
    faces_by_id = {str(item.get("id")): item for item in faces}

    for face in faces:
        face_id = str(face.get("id"))
        for point_id in face.get("point_types", []):
            point_usage[str(point_id)] += 1
            if point_id not in point_set:
                errors.append(f"face {face_id} references unknown point type: {point_id}")
        for line_id in face.get("line_types", []):
            line_usage[str(line_id)] += 1
            if line_id not in line_set:
                errors.append(f"face {face_id} references unknown line type: {line_id}")
        for owner_path in face.get("owner_paths", []):
            if not (root / str(owner_path)).exists():
                errors.append(f"face {face_id} owner path does not exist: {owner_path}")

    for point in points:
        point_id = str(point.get("id"))
        primary_face = str(point.get("primary_face"))
        if primary_face not in face_set:
            errors.append(f"point {point_id} has unknown primary face: {primary_face}")
        elif point_id not in faces_by_id[primary_face].get("point_types", []):
            errors.append(f"point {point_id} is absent from primary face {primary_face}")
        if point_usage[point_id] != 1:
            errors.append(f"point {point_id} must be owned by exactly one face, observed {point_usage[point_id]}")

    for line_id in line_ids:
        if line_usage[line_id] == 0:
            errors.append(f"line type is not used by any face: {line_id}")

    for body in bodies:
        body_id = str(body.get("id"))
        for face_id in body.get("required_faces", []):
            if face_id not in face_set:
                errors.append(f"body {body_id} references unknown face: {face_id}")

    f04, f05 = faces_by_id.get("F04", {}), faces_by_id.get("F05", {})
    model_bindings = sorted(
        (str(face.get("id")), str(face.get("model")))
        for face in faces
        if face.get("model") is not None
    )
    if model_bindings != [("F04", "OSPS"), ("F05", "PWTSJ")]:
        errors.append("model bindings must be exactly F04=OSPS and F05=PWTSJ")
    if f04.get("model") != "OSPS" or f04.get("implementation_status") != "conceptual":
        errors.append("F04 must be OSPS and remain conceptual until runtime evidence exists")
    if f05.get("model") != "PWTSJ":
        errors.append("F05 must be the PWTSJ process face")
    expected_face_points = {
        "F04": {"point.outcome_node", "point.outcome_frontier", "point.obstruction"},
        "F05": {"point.project", "point.workflow", "point.task", "point.step", "point.job", "point.checkpoint"},
    }
    for face_id, expected in expected_face_points.items():
        observed = set(faces_by_id.get(face_id, {}).get("point_types", []))
        if observed != expected:
            errors.append(f"{face_id} point types do not match its fixed public model")

    for kind, objects in (("point", points), ("line", lines), ("face", faces), ("body", bodies)):
        for item in objects:
            if item.get("implementation_status") != "conceptual":
                errors.append(f"public conceptual registry cannot claim implemented {kind}: {item.get('id')}")

    for doc in registry.get("document_refs", []):
        path = root / str(doc)
        if not path.is_file():
            errors.append(f"document_ref does not exist: {doc}")

    claims = registry.get("capability_claims", {})
    for key in (
        "body_manifest_implemented",
        "outcome_graph_runtime_implemented",
        "osps_orchestrator_implemented",
        "pwtsj_general_scheduler_implemented",
        "mathematical_truth_changed",
    ):
        if claims.get(key) is not False:
            errors.append(f"unsupported capability claim must remain false: {key}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the PLFB conceptual metamodel registry.")
    parser.add_argument("--project-root", type=Path, default=ROOT)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    root = args.project_root.resolve()
    try:
        registry = json.loads((root / REGISTRY).read_text(encoding="utf-8"))
        schema = json.loads((root / SCHEMA).read_text(encoding="utf-8"))
        errors = validate(registry, schema, root)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        registry = {}
        errors = [str(exc)]
    report = {
        "decision": "PASS" if not errors else "BLOCK",
        "point_types": len(registry.get("point_types", [])),
        "line_types": len(registry.get("line_types", [])),
        "faces": len(registry.get("faces", [])),
        "body_types": len(registry.get("body_types", [])),
        "errors": errors,
    }
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(
            "PLFB metamodel: "
            f"{report['decision']} points={report['point_types']} lines={report['line_types']} "
            f"faces={report['faces']} bodies={report['body_types']}"
        )
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
