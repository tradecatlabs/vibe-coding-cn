#!/usr/bin/env python3
"""Validate the fail-closed 41-family math tool maturity registry."""
from __future__ import annotations

import json
import os
import stat
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker, SchemaError

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "governance/control-plane/math-tool-maturity.v1.json"
SCHEMA = ROOT / "governance/control-plane/math-tool-maturity.schema.json"
STATES = ["surveyed", "source_locked", "installed", "smoke_checked", "evidence_capable", "verifier_admitted"]
ROUTE_MINIMUM = {"none": "surveyed", "candidate-generation": "smoke_checked", "evidence": "evidence_capable", "verifier": "verifier_admitted"}
MAX_FILE_BYTES = 5_000_000
MAX_PATH_CHARS = 4_096


def _nofollow_flag() -> int:
    value = getattr(os, "O_NOFOLLOW", None)
    if value is None:
        raise RuntimeError("O_NOFOLLOW unavailable; refusing maturity validation")
    return value


def _safe_path(path: Path, root: Path) -> Path:
    path = Path(path)
    root_input = Path(root)
    if (
        len(str(path)) > MAX_PATH_CHARS
        or any(part in {".", ".."} for part in path.parts)
        or "\x00" in str(path)
        or "\\" in str(path)
    ):
        raise ValueError(f"path contains an invalid component: {path}")
    root = root_input.resolve()
    if (
        not root_input.is_absolute()
        or root_input.absolute() != root
        or not root.is_dir()
    ):
        raise ValueError(f"project root is not canonical: {root_input}")
    candidate = Path(os.path.abspath(path if path.is_absolute() else root / path))
    try:
        relative = candidate.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"path escapes project root: {candidate}") from exc
    current = root
    for part in relative.parts:
        current /= part
        if current.is_symlink():
            raise ValueError(f"path contains symlink: {candidate}")
    return candidate


def _reject_json_constant(value: str) -> object:
    raise ValueError(f"illegal JSON constant: {value}")


def _read_json(path: Path, root: Path) -> object:
    candidate = _safe_path(path, root)
    descriptor = os.open(candidate, os.O_RDONLY | _nofollow_flag())
    try:
        file_stat = os.fstat(descriptor)
        if not stat.S_ISREG(file_stat.st_mode) or file_stat.st_size > MAX_FILE_BYTES:
            raise ValueError(f"file exceeds size budget: {candidate}")
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(descriptor, min(64 * 1024, MAX_FILE_BYTES - total + 1))
            if not chunk:
                break
            total += len(chunk)
            if total > MAX_FILE_BYTES:
                raise ValueError(f"file exceeds size budget: {candidate}")
            chunks.append(chunk)
    finally:
        os.close(descriptor)
    return json.loads(
        b"".join(chunks).decode("utf-8"),
        parse_constant=_reject_json_constant,
    )


def _regular_file(path: Path, root: Path) -> bool:
    candidate = _safe_path(path, root)
    descriptor = os.open(candidate, os.O_RDONLY | _nofollow_flag())
    try:
        file_stat = os.fstat(descriptor)
        return stat.S_ISREG(file_stat.st_mode) and file_stat.st_size <= MAX_FILE_BYTES
    finally:
        os.close(descriptor)


def validate(registry: Path = REGISTRY, schema_path: Path = SCHEMA, root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    try:
        # The test/API permits an explicitly supplied temporary registry; it is
        # still opened no-follow and bounded, while evidence references remain
        # confined to the declared project root.
        value = _read_json(registry, registry.parent)
        schema = _read_json(schema_path, root)
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        return [f"cannot read registry/schema: {exc}"]
    try:
        Draft202012Validator.check_schema(schema)
    except (SchemaError, TypeError, ValueError) as exc:
        return [f"invalid registry schema: {exc}"]
    for error in Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(value):
        where = "/".join(str(part) for part in error.absolute_path) or "<root>"
        errors.append(f"schema {where}: {error.message}")
    tools = value.get("tools") if isinstance(value, dict) else None
    if not isinstance(tools, list):
        return errors + ["tools is not a list"]
    expected = {f"T{index:02d}" for index in range(1, 42)}
    actual = [item.get("tool_id") for item in tools if isinstance(item, dict) and isinstance(item.get("tool_id"), str)]
    actual_set = set(actual)
    if actual_set != expected:
        errors.append(f"tool ID coverage mismatch: missing={sorted(expected-actual_set)} extra={sorted(actual_set-expected)}")
    if len(actual) != len(set(actual)):
        errors.append("duplicate tool IDs")
    for item in tools:
        if not isinstance(item, dict):
            continue
        tool_id_value = item.get("tool_id")
        if not isinstance(tool_id_value, str):
            errors.append("tool entry has invalid tool_id type")
            continue
        tool_id = tool_id_value
        maturity = item.get("maturity")
        route = item.get("runtime_route")
        if isinstance(maturity, str) and isinstance(route, str) and maturity in STATES and route in ROUTE_MINIMUM:
            if STATES.index(maturity) < STATES.index(ROUTE_MINIMUM[route]):
                errors.append(f"{tool_id}: route {route} exceeds maturity {maturity}")
        if isinstance(maturity, str) and maturity in {"evidence_capable", "verifier_admitted"} and not item.get("admitted_components"):
            errors.append(f"{tool_id}: admitted components required at {maturity}")
        if isinstance(maturity, str) and maturity not in {"evidence_capable", "verifier_admitted"} and isinstance(route, str) and route in {"evidence", "verifier"}:
            errors.append(f"{tool_id}: unadmitted tool has privileged route")
        references = item.get("evidence_refs", [])
        if not isinstance(references, list) or len(references) > 10_000:
            errors.append(f"{tool_id}: evidence_refs must be a list")
            references = []
        for reference in references:
            if (
                not isinstance(reference, str)
                or len(reference) > MAX_PATH_CHARS
                or "\x00" in reference
            ):
                errors.append(f"{tool_id}: invalid evidence ref {reference}")
                continue
            path_text = reference.split("#", 1)[0]
            path = Path(path_text)
            if (
                path.is_absolute()
                or any(part in {".", ".."} for part in path.parts)
                or "\x00" in path_text
                or "\\" in path_text
            ):
                errors.append(f"{tool_id}: unsafe evidence ref {reference}")
                continue
            lexical = root
            unsafe_symlink = False
            for part in path.parts:
                lexical = lexical / part
                if lexical.is_symlink():
                    unsafe_symlink = True
                    break
            try:
                resolved = _safe_path(root / path, root)
            except ValueError:
                errors.append(f"{tool_id}: evidence ref escapes project root {reference}")
                continue
            if unsafe_symlink:
                errors.append(f"{tool_id}: evidence ref contains symlink {reference}")
                continue
            try:
                if not _regular_file(resolved, root):
                    errors.append(f"{tool_id}: missing evidence ref {reference}")
            except (OSError, ValueError):
                errors.append(f"{tool_id}: missing evidence ref {reference}")
    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"math tool maturity registry: BLOCK issues={len(errors)}")
        return 1
    value = _read_json(REGISTRY, ROOT)
    if not isinstance(value, dict) or not isinstance(value.get("tools"), list):
        print("ERROR: invalid registry after validation")
        return 1
    counts = {state: sum(item.get("maturity") == state for item in value["tools"] if isinstance(item, dict)) for state in STATES}
    print(f"math tool maturity registry: PASS tools=41 states={counts}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, TypeError, ValueError, KeyError, UnicodeError) as exc:
        print(f"ERROR: {exc}")
        raise SystemExit(1) from exc
