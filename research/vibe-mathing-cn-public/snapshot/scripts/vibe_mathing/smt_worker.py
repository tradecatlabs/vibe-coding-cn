#!/usr/bin/env python3
"""Bounded worker for the fixed SymPy SAT/QF-LRA fixture."""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Make the public scripts package importable when this file is executed directly.
SCRIPTS_ROOT = Path(__file__).resolve().parents[1]
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))

from vibe_mathing.smt import _evaluate_fixture  # noqa: E402


MAX_INPUT_BYTES = 1_048_576


def _reject_json_constant(value: str) -> object:
    raise RuntimeError(f"fixture JSON contains invalid constant: {value}")


def _read_stdin_bounded() -> bytes:
    chunks: list[bytes] = []
    total = 0
    while True:
        chunk = sys.stdin.buffer.read(min(64 * 1024, MAX_INPUT_BYTES - total + 1))
        if not chunk:
            return b"".join(chunks)
        total += len(chunk)
        if total > MAX_INPUT_BYTES:
            raise RuntimeError("fixture stdin exceeds size budget")
        chunks.append(chunk)


def main() -> int:
    if len(sys.argv) != 1:
        print("fixture must be provided on bounded stdin", file=sys.stderr)
        return 2
    try:
        raw = _read_stdin_bounded()
        fixture = json.loads(
            raw.decode("utf-8"), parse_constant=_reject_json_constant
        )
        if not isinstance(fixture, dict):
            raise RuntimeError("fixture must be an object")
        payload = _evaluate_fixture(fixture)
    except (OSError, json.JSONDecodeError, RuntimeError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    try:
        encoded = json.dumps(
            payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
        )
    except (TypeError, ValueError, UnicodeEncodeError) as exc:
        print(f"worker output is not portable JSON: {exc}", file=sys.stderr)
        return 1
    if len(encoded.encode("utf-8")) > MAX_INPUT_BYTES:
        print("worker output exceeds size budget", file=sys.stderr)
        return 1
    print(encoded)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
