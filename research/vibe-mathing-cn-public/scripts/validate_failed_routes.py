#!/usr/bin/env python3
"""Validate research/records/failed-routes.jsonl against failed-route.schema.json.

Rules:
- File is JSONL: every non-empty line must be valid JSON object.
- Every record must validate against the schema.
- route_id / problem_id must be unique (append-only ledger, no rewrites).
- recorded_at must parse as ISO8601.
Exit code: 0 = valid, 1 = any failure.
"""
import json
import os
import stat
import sys
from datetime import datetime

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(REPO, "research", "records", "failed-routes.jsonl")
SCHEMA_PATH = os.path.join(REPO, "research", "schema", "failed-route.schema.json")
MAX_FILE_BYTES = 128_000_000
MAX_RECORDS = 100_000
MAX_LINE_BYTES = 30_000_000
MAX_PATH_CHARS = 4_096
MAX_EVIDENCE_ITEMS = 10_000
MAX_FIELD_CHARS = 8_192

try:
    import jsonschema
except ImportError:
    jsonschema = None


def _nofollow_flag() -> int:
    value = getattr(os, "O_NOFOLLOW", None)
    if value is None:
        raise RuntimeError("O_NOFOLLOW unavailable; refusing failed-route validation")
    return value


def _safe_read(path: str, *, max_bytes: int = MAX_FILE_BYTES) -> bytes:
    if (
        not isinstance(max_bytes, int)
        or isinstance(max_bytes, bool)
        or max_bytes <= 0
        or max_bytes > MAX_FILE_BYTES
    ):
        raise ValueError("invalid failed-route read budget")
    if (
        not isinstance(path, str)
        or len(path) > MAX_PATH_CHARS
        or "\x00" in path
        or "\\" in path
        or any(part in {".", ".."} for part in path.replace("/", os.sep).split(os.sep))
    ):
        raise ValueError("invalid failed-route path")
    repo = os.path.abspath(REPO)
    candidate = os.path.abspath(path)
    if os.path.commonpath((repo, candidate)) != repo:
        raise ValueError(f"path escapes repository: {candidate}")
    current = repo
    relative = os.path.relpath(candidate, repo)
    for part in relative.split(os.sep):
        current = os.path.join(current, part)
        if os.path.islink(current):
            raise ValueError(f"path contains symlink: {candidate}")
    descriptor = os.open(candidate, os.O_RDONLY | _nofollow_flag())
    try:
        file_stat = os.fstat(descriptor)
        if not stat.S_ISREG(file_stat.st_mode):
            raise ValueError(f"path is not a regular file: {candidate}")
        if file_stat.st_size > max_bytes:
            raise ValueError(f"file exceeds size budget: {candidate}")
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(descriptor, min(64 * 1024, max_bytes - total + 1))
            if not chunk:
                return b"".join(chunks)
            total += len(chunk)
            if total > max_bytes:
                raise ValueError(f"file exceeds size budget: {candidate}")
            chunks.append(chunk)
    finally:
        os.close(descriptor)


def _reject_json_constant(value: str) -> object:
    raise ValueError(f"illegal JSON constant: {value}")


def load_schema():
    return json.loads(_safe_read(SCHEMA_PATH).decode("utf-8"), parse_constant=_reject_json_constant)


def parse_recorded_at(value: object) -> datetime:
    """Parse timezone-aware RFC3339 on Python versions where fromisoformat rejects Z."""
    if not isinstance(value, str) or not value or len(value) > MAX_FIELD_CHARS:
        raise ValueError("recorded_at must be a non-empty string")
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        raise ValueError("recorded_at must include a timezone")
    return parsed


def main() -> int:
    if os.path.islink(LEDGER):
        raise ValueError("failed-route ledger cannot be a symlink")
    if not os.path.lexists(LEDGER):
        print(f"OK: {LEDGER} missing (empty ledger allowed)")
        return 0
    if jsonschema is None:
        raise RuntimeError("jsonschema is required for failed-route validation")
    schema = load_schema()
    if not isinstance(schema, dict):
        raise ValueError("failed-route schema must be an object")
    try:
        jsonschema.Draft202012Validator.check_schema(schema)
    except (jsonschema.SchemaError, TypeError, ValueError) as exc:
        raise ValueError("failed-route schema is invalid") from exc
    errors = []
    seen_ids = set()
    line_no = 0
    nonempty_lines = 0
    data = _safe_read(LEDGER)
    if len(data) > MAX_FILE_BYTES:
        raise ValueError("failed-route ledger exceeds size budget")
    for raw_line in data.splitlines():
        line_no += 1
        if len(raw_line) > MAX_LINE_BYTES:
            errors.append(f"line {line_no}: line exceeds size budget")
            continue
        try:
            line = raw_line.decode("utf-8").strip()
        except UnicodeDecodeError as exc:
            errors.append(f"line {line_no}: invalid UTF-8: {exc}")
            continue
        if not line:
            continue
        nonempty_lines += 1
        if nonempty_lines > MAX_RECORDS:
            raise ValueError(f"failed-route records exceed limit {MAX_RECORDS}")
        try:
            rec = json.loads(line, parse_constant=_reject_json_constant)
        except (json.JSONDecodeError, ValueError) as e:
            errors.append(f"line {line_no}: invalid JSON: {e}")
            continue
        if not isinstance(rec, dict):
            errors.append(f"line {line_no}: not an object")
            continue
        try:
            jsonschema.validate(rec, schema)
        except jsonschema.ValidationError as e:
            errors.append(f"line {line_no}: schema: {e.message}")
            continue
        rid = rec.get("route_id")
        pid = rec.get("problem_id")
        if isinstance(rid, str) and isinstance(pid, str):
            key = (rid, pid)
            if key in seen_ids:
                errors.append(f"line {line_no}: duplicate (route_id, problem_id) {key}")
            seen_ids.add(key)
        try:
            parse_recorded_at(rec.get("recorded_at"))
        except ValueError:
            errors.append(f"line {line_no}: bad recorded_at: {rec.get('recorded_at')}")
        ev = rec.get("evidence", [])
        if not isinstance(ev, list) or len(ev) < 1 or len(ev) > MAX_EVIDENCE_ITEMS:
            errors.append(f"line {line_no}: evidence must be a bounded non-empty list")

    if errors:
        print(f"FAIL: {len(errors)} error(s) in {LEDGER}")
        for e in errors[:50]:
            print(f"  - {e}")
        return 1
    print(f"OK: {line_no} line(s), {len(seen_ids)} record(s) valid")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        sys.exit(1)
