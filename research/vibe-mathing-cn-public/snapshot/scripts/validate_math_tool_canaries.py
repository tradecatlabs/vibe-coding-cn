#!/usr/bin/env python3
# 做什么：校验版本化数学工具 canary 报告的 schema、四类 case 和汇总计数。
# 怎么运行：python3 scripts/validate_math_tool_canaries.py
# 需要什么：Python 3 与 jsonschema；只读当前报告，不访问网络。

from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker, SchemaError


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "governance/operations/check-reports/math-tool-canaries.json"
SCHEMA = ROOT / "governance/control-plane/math-tool-canary.schema.json"
RUNNER = ROOT / "scripts/run_math_tool_canaries.py"
EXPECTED_KINDS = {"positive", "negative", "error", "timeout"}
MAX_REPORT_BYTES = 128_000_000
MAX_PATH_CHARS = 4_096


def _reject_json_constant(value: str) -> object:
    raise ValueError(f"invalid JSON constant: {value}")


def read_bounded(path: Path, max_bytes: int = MAX_REPORT_BYTES) -> bytes:
    if (
        not isinstance(max_bytes, int)
        or isinstance(max_bytes, bool)
        or max_bytes <= 0
        or max_bytes > MAX_REPORT_BYTES
        or len(str(path)) > MAX_PATH_CHARS
        or "\x00" in str(path)
        or "\\" in str(path)
        or any(part in {".", ".."} for part in Path(path).parts)
    ):
        raise ValueError("canary report read budget is invalid")
    nofollow = getattr(os, "O_NOFOLLOW", None)
    if nofollow is None:
        raise ValueError("platform cannot safely read canary report")
    if path.is_symlink() or path.resolve() != path:
        raise ValueError("canary report cannot be a symlink or non-canonical path")
    if any(parent.is_symlink() for parent in path.parents):
        raise ValueError("canary report parent cannot be a symlink")
    descriptor = os.open(path, os.O_RDONLY | nofollow)
    try:
        file_stat = os.fstat(descriptor)
        if not stat.S_ISREG(file_stat.st_mode) or file_stat.st_size > max_bytes:
            raise ValueError("canary report exceeds size budget or is not regular")
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(descriptor, min(64 * 1024, max_bytes - total + 1))
            if not chunk:
                return b"".join(chunks)
            total += len(chunk)
            if total > max_bytes:
                raise ValueError("canary report exceeds size budget")
            chunks.append(chunk)
    finally:
        os.close(descriptor)


def parse_json(path: Path) -> object:
    return json.loads(
        read_bounded(path).decode("utf-8"),
        parse_constant=_reject_json_constant,
    )


def validate(report: Path = REPORT, schema_path: Path = SCHEMA) -> list[str]:
    try:
        value = parse_json(report)
        schema = parse_json(schema_path)
        if not isinstance(schema, dict):
            return ["canary schema must be an object"]
        Draft202012Validator.check_schema(schema)
        errors = [
            error.message
            for error in Draft202012Validator(
                schema, format_checker=FormatChecker()
            ).iter_errors(value)
        ]
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError, TypeError, SchemaError) as exc:
        return [f"cannot read or validate report/schema: {exc}"]
    if not isinstance(value, dict):
        errors.append("canary report must be an object")
    if errors:
        return errors

    runner = value.get("runner", {})
    try:
        expected_runner_sha256 = hashlib.sha256(read_bounded(RUNNER)).hexdigest()
    except (OSError, ValueError) as exc:
        errors.append(f"cannot read canary runner: {exc}")
        expected_runner_sha256 = ""
    if runner.get("sha256") != expected_runner_sha256:
        errors.append("runner.sha256 does not match scripts/run_math_tool_canaries.py")

    tools = value.get("tools", [])
    results = value.get("results", [])
    summary = value.get("summary", {})
    execution_policy = value.get("execution_policy", {})
    if execution_policy.get("termination", {}).get("status") != "completed":
        errors.append("execution_policy termination did not complete")
    by_tool: dict[str, set[str]] = {tool_id: set() for tool_id in tools}
    for item in results:
        tool_id = item.get("tool_id")
        if tool_id in by_tool:
            by_tool[tool_id].add(item.get("kind"))
        if item.get("kind") == "timeout" and item.get("termination_status") != "timed_out":
            errors.append(f"{tool_id}: timeout case lacks timed_out termination")
        if item.get("kind") != "timeout" and item.get("termination_status") != "completed":
            errors.append(f"{tool_id}: non-timeout case did not complete")
    for tool_id, kinds in by_tool.items():
        missing = sorted(EXPECTED_KINDS - kinds)
        if missing:
            errors.append(f"{tool_id}: missing canary kinds {missing}")

    passed = sum(item.get("status") == "PASS" for item in results)
    failed = sum(item.get("status") != "PASS" for item in results)
    if summary.get("case_count") != len(results):
        errors.append("summary.case_count does not match results")
    if summary.get("passed") != passed or summary.get("failed") != failed:
        errors.append("summary pass/fail counts do not match results")
    if summary.get("all_passed") != (failed == 0):
        errors.append("summary.all_passed does not match result statuses")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a bounded math-tool canary report")
    parser.add_argument("--report", type=Path, default=REPORT)
    args = parser.parse_args()
    errors = validate(args.report)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"math tool canary report: BLOCK issues={len(errors)}")
        return 1
    try:
        value = parse_json(args.report)
        if not isinstance(value, dict):
            raise ValueError("canary report must be an object")
        print(f"math tool canary report: PASS cases={value['summary']['case_count']} tools={','.join(value['tools'])}")
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError, TypeError, KeyError) as exc:
        print(f"ERROR: cannot read validated canary report: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
