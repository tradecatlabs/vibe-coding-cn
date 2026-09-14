#!/usr/bin/env python3
# 做什么：在已配置的数学运行时中执行有限、可重放的工具正/负/错误与超时 canary。
# 怎么运行：python3 scripts/run_math_tool_canaries.py --tools T13,T15,T16 --json --strict。
# 需要什么：显式运行时环境；所有子进程都有短 timeout，不访问网络、不写项目目录。

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

from vibe_mathing.runtime import RuntimeErrorBase, execute_bounded


CaseKind = Literal["positive", "negative", "error", "timeout"]
DEFAULT_TIMEOUT = float(os.environ.get("MATH_CANARY_TIMEOUT_SECONDS", "8"))
PYTHON_TIMEOUT = float(os.environ.get("MATH_CANARY_PYTHON_TIMEOUT_SECONDS", "3"))
MAX_OUTPUT_BYTES = int(os.environ.get("MATH_CANARY_MAX_OUTPUT_BYTES", "1048576"))
MEMORY_BUDGET_MB = int(os.environ.get("MATH_CANARY_MEMORY_BUDGET_MB", "256"))
THREADS_MAX = int(os.environ.get("MATH_CANARY_THREADS_MAX", "1"))
MAX_TIMEOUT_SECONDS = 86_400
MAX_OUTPUT_LIMIT = 128_000_000
MAX_MEMORY_MB = 131_072
MAX_THREADS = 1_024


class CanaryProcessFailure(RuntimeError):
    pass


def _safe_environment() -> dict[str, str]:
    """Keep credentials and unrelated agent configuration out of canary children."""
    allowed = {"PATH", "HOME", "LANG", "LC_ALL", "TMPDIR"}
    environment = {key: value for key, value in os.environ.items() if key in allowed}
    environment["PATH"] = environment.get("PATH", "/usr/local/bin:/usr/bin:/bin")
    return environment


def run_bounded(argv: list[str], *, timeout: float) -> dict[str, object]:
    """Run a canary with a process-group timeout and combined output cap."""
    if (
        not math.isfinite(timeout)
        or timeout <= 0
        or timeout > MAX_TIMEOUT_SECONDS
        or MAX_OUTPUT_BYTES <= 0
        or MAX_OUTPUT_BYTES > MAX_OUTPUT_LIMIT
        or MEMORY_BUDGET_MB <= 0
        or MEMORY_BUDGET_MB > MAX_MEMORY_MB
        or THREADS_MAX <= 0
        or THREADS_MAX > MAX_THREADS
    ):
        raise CanaryProcessFailure("invalid canary execution budget")
    try:
        return execute_bounded(
            argv,
            cwd=Path.cwd(),
            timeout_seconds=timeout,
            max_output_bytes=MAX_OUTPUT_BYTES,
            memory_budget_mb=MEMORY_BUDGET_MB,
            threads_max=THREADS_MAX,
            env=_safe_environment(),
        )
    except RuntimeErrorBase as exc:
        message = str(exc)
        if "超时" in message:
            raise subprocess.TimeoutExpired(argv, timeout) from exc
        raise CanaryProcessFailure(message) from exc


@dataclass(frozen=True)
class CanaryResult:
    tool_id: str
    component: str
    kind: CaseKind
    status: str
    detail: str
    duration_seconds: float
    termination_status: str


def resolve_executable(value: str) -> str | None:
    path = shutil.which(value)
    if path:
        return path
    candidate = Path(value)
    return str(candidate) if candidate.is_file() and os.access(candidate, os.X_OK) else None


def read_bounded_output(path: Path) -> str:
    nofollow = getattr(os, "O_NOFOLLOW", None)
    if nofollow is None:
        raise CanaryProcessFailure("O_NOFOLLOW unavailable for canary output")
    descriptor = os.open(path, os.O_RDONLY | nofollow)
    try:
        file_stat = os.fstat(descriptor)
        if not stat.S_ISREG(file_stat.st_mode) or file_stat.st_size > MAX_OUTPUT_BYTES:
            raise CanaryProcessFailure("canary result file exceeds output budget")
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(descriptor, min(64 * 1024, MAX_OUTPUT_BYTES - total + 1))
            if not chunk:
                return b"".join(chunks).decode("ascii", errors="replace")
            total += len(chunk)
            if total > MAX_OUTPUT_BYTES:
                raise CanaryProcessFailure("canary result file exceeds output budget")
            chunks.append(chunk)
    finally:
        os.close(descriptor)


def hash_runner_source(path: Path) -> str:
    nofollow = getattr(os, "O_NOFOLLOW", None)
    if nofollow is None:
        raise CanaryProcessFailure("O_NOFOLLOW unavailable for canary source")
    descriptor = os.open(path, os.O_RDONLY | nofollow)
    digest = hashlib.sha256()
    try:
        file_stat = os.fstat(descriptor)
        if not stat.S_ISREG(file_stat.st_mode) or file_stat.st_size > 5_000_000:
            raise CanaryProcessFailure("canary source exceeds source budget")
        total = 0
        while True:
            chunk = os.read(descriptor, min(64 * 1024, 5_000_000 - total + 1))
            if not chunk:
                return digest.hexdigest()
            total += len(chunk)
            if total > 5_000_000:
                raise CanaryProcessFailure("canary source exceeds source budget")
            digest.update(chunk)
    finally:
        os.close(descriptor)


def runtime_path(name: str, fallback: str) -> str:
    return os.environ.get(name, fallback)


def first_line(text: str) -> str:
    return next((line.strip() for line in text.splitlines() if line.strip()), "")[:120]


def result(
    tool_id: str,
    component: str,
    kind: CaseKind,
    status: str,
    detail: str,
    started: float,
    termination_status: str = "completed",
) -> CanaryResult:
    return CanaryResult(
        tool_id,
        component,
        kind,
        status,
        detail[:160],
        round(time.monotonic() - started, 3),
        termination_status,
    )


def run_python(
    tool_id: str,
    component: str,
    kind: CaseKind,
    python: str,
    program: str,
    expected: Literal["success", "nonzero", "timeout"],
    timeout: float = PYTHON_TIMEOUT,
) -> CanaryResult:
    started = time.monotonic()
    executable = resolve_executable(python)
    if executable is None:
        return result(tool_id, component, kind, "FAIL", "Python runtime missing", started, "failed")
    try:
        completed = run_bounded([executable, "-c", program], timeout=timeout)
    except subprocess.TimeoutExpired:
        status = "PASS" if expected == "timeout" else "FAIL"
        detail = f"timeout expected={expected == 'timeout'}"
        return result(tool_id, component, kind, status, detail, started, "timed_out")
    except (OSError, CanaryProcessFailure) as exc:
        return result(tool_id, component, kind, "FAIL", type(exc).__name__, started, "failed")

    if expected == "success":
        passed = completed["exit_code"] == 0 and "CANARY_PASS" in str(completed["stdout"])
        detail = f"exit={completed['exit_code']} marker={passed}"
    elif expected == "nonzero":
        passed = completed["exit_code"] != 0
        detail = f"expected nonzero exit={completed['exit_code']}"
    else:
        passed = False
        detail = f"completed-before-timeout exit={completed['exit_code']}"
    return result(tool_id, component, kind, "PASS" if passed else "FAIL", detail, started)


def python_probe(python: str, label: str, program: str) -> str:
    executable = resolve_executable(python)
    if executable is None:
        return f"{label}:missing"
    try:
        completed = run_bounded([executable, "-c", program], timeout=PYTHON_TIMEOUT)
    except (OSError, CanaryProcessFailure, subprocess.TimeoutExpired):
        return f"{label}:error"
    return f"{label}:{first_line(str(completed['stdout'])) or 'unknown'}"


def python_version(python: str, label: str) -> str:
    return python_probe(python, label, "import platform; print(platform.python_version())")


def command_probe(command: str, args: list[str], label: str) -> str:
    executable = resolve_executable(command)
    if executable is None:
        return f"{label}:missing"
    try:
        completed = run_bounded([executable, *args], timeout=PYTHON_TIMEOUT)
    except (OSError, CanaryProcessFailure, subprocess.TimeoutExpired):
        return f"{label}:error"
    combined = str(completed["stdout"]) + chr(10) + str(completed["stderr"])
    return f"{label}:{first_line(combined) or 'unknown'}"


def run_command(
    tool_id: str,
    component: str,
    kind: CaseKind,
    command: str,
    args: list[str],
    expected_code: set[int],
    expected_text: str | None = None,
    timeout: float = DEFAULT_TIMEOUT,
) -> CanaryResult:
    started = time.monotonic()
    executable = resolve_executable(command)
    if executable is None:
        return result(tool_id, component, kind, "FAIL", "command missing", started, "failed")
    try:
        completed = run_bounded([executable, *args], timeout=timeout)
    except subprocess.TimeoutExpired:
        return result(tool_id, component, kind, "FAIL", "unexpected timeout", started, "timed_out")
    except (OSError, CanaryProcessFailure) as exc:
        return result(tool_id, component, kind, "FAIL", type(exc).__name__, started, "failed")
    combined = f"{completed['stdout']}\n{completed['stderr']}"
    passed = completed["exit_code"] in expected_code and (
        expected_text is None or expected_text in combined
    )
    return result(
        tool_id,
        component,
        kind,
        "PASS" if passed else "FAIL",
        f"exit={completed['exit_code']} text={expected_text is None or expected_text in combined}",
        started,
    )


def run_minisat(
    tool_id: str,
    component: str,
    kind: CaseKind,
    executable: str,
    dimacs: str,
    expected_code: set[int],
    expected_text: str | None,
) -> CanaryResult:
    started = time.monotonic()
    command = resolve_executable(executable)
    if command is None:
        return result(tool_id, component, kind, "FAIL", "command missing", started, "failed")
    try:
        with tempfile.TemporaryDirectory(prefix="math-canary-") as directory:
            source = Path(directory) / "input.cnf"
            output = Path(directory) / "result.txt"
            source.write_text(dimacs, encoding="ascii")
            completed = run_bounded(
                [command, str(source), str(output)], timeout=DEFAULT_TIMEOUT
            )
            if output.is_symlink():
                raise CanaryProcessFailure("canary result file cannot be a symlink")
            output_text = read_bounded_output(output) if output.exists() else ""
    except subprocess.TimeoutExpired:
        return result(tool_id, component, kind, "FAIL", "unexpected timeout", started, "timed_out")
    except (OSError, CanaryProcessFailure) as exc:
        return result(tool_id, component, kind, "FAIL", type(exc).__name__, started, "failed")
    passed = completed["exit_code"] in expected_code and (
        expected_text is None or expected_text in output_text
    )
    return result(
        tool_id,
        component,
        kind,
        "PASS" if passed else "FAIL",
        f"exit={completed['exit_code']} output={expected_text is None or expected_text in output_text}",
        started,
    )


def t13(project_python: str) -> tuple[list[CanaryResult], dict[str, str]]:
    positive = """
from flint import arb, fmpq, fmpz
assert fmpz(91).factor() == [(7, 1), (13, 1)]
assert fmpq(1, 3) + fmpq(1, 6) == fmpq(1, 2)
assert ((arb(1) / 3) * 3).contains(arb(1))
print('CANARY_PASS')
"""
    negative = """
from flint import fmpz
assert fmpz(91).factor() == [(7, 1), (13, 2)]
"""
    error = """
from flint import arb
arb('not-a-number')
"""
    return [
        run_python("T13", "python-flint + Arb", "positive", project_python, positive, "success"),
        run_python("T13", "python-flint + Arb", "negative", project_python, negative, "nonzero"),
        run_python("T13", "python-flint + Arb", "error", project_python, error, "nonzero"),
        run_python("T13", "bounded subprocess", "timeout", sys.executable, "while True: pass", "timeout", timeout=0.2),
    ], {
        "project_python": python_version(project_python, "project-python"),
        "python_flint": python_probe(project_python, "python-flint", "import flint; print(getattr(flint, '__version__', 'unknown'))"),
    }


def t15(project_python: str, system_python: str, z3_command: str) -> tuple[list[CanaryResult], dict[str, str]]:
    cvc5_positive = """
from cvc5 import Kind, Solver
s=Solver(); s.setLogic('QF_LIA')
x=s.mkConst(s.getIntegerSort(), 'x')
s.assertFormula(s.mkTerm(Kind.GT, x, s.mkInteger(0)))
assert s.checkSat().isSat()
print('CANARY_PASS')
"""
    cvc5_negative = """
from cvc5 import Kind, Solver
s=Solver(); s.setLogic('QF_LIA')
x=s.mkConst(s.getIntegerSort(), 'x')
s.assertFormula(s.mkTerm(Kind.GT, x, s.mkInteger(0)))
s.assertFormula(s.mkTerm(Kind.LEQ, x, s.mkInteger(0)))
assert s.checkSat().isSat()
"""
    cvc5_error = """
from cvc5 import Solver
Solver().setLogic('NO_SUCH_LOGIC')
"""
    z3_positive = """
import z3
x=z3.Int('x'); s=z3.Solver(); s.add(x > 0, x < 2)
assert s.check() == z3.sat
print('CANARY_PASS')
"""
    z3_negative = """
import z3
x=z3.Int('x'); s=z3.Solver(); s.add(x > 0, x <= 0)
assert s.check() == z3.sat
"""
    z3_error = """
import z3
z3.parse_smt2_string('(assert')
"""
    timeout_program = "while True: pass"
    smt_sat = """(set-logic QF_LIA)\n(declare-const x Int)\n(assert (> x 0))\n(assert (< x 2))\n(check-sat)\n(exit)\n"""
    smt_unsat = """(set-logic QF_LIA)\n(declare-const x Int)\n(assert (> x 0))\n(assert (<= x 0))\n(check-sat)\n(exit)\n"""
    results = [
        run_python("T15", "cvc5 Python API", "positive", project_python, cvc5_positive, "success"),
        run_python("T15", "cvc5 Python API", "negative", project_python, cvc5_negative, "nonzero"),
        run_python("T15", "cvc5 Python API", "error", project_python, cvc5_error, "nonzero"),
        run_python("T15", "Z3 Python API", "positive", system_python, z3_positive, "success"),
        run_python("T15", "Z3 Python API", "negative", system_python, z3_negative, "nonzero"),
        run_python("T15", "Z3 Python API", "error", system_python, z3_error, "nonzero"),
        run_python("T15", "bounded subprocess", "timeout", system_python, timeout_program, "timeout", timeout=0.2),
    ]
    with tempfile.TemporaryDirectory(prefix="math-canary-") as directory:
        sat_file = Path(directory) / "sat.smt2"
        unsat_file = Path(directory) / "unsat.smt2"
        sat_file.write_text(smt_sat, encoding="ascii")
        unsat_file.write_text(smt_unsat, encoding="ascii")
        results.append(run_command("T15", "Z3 SMT-LIB syntax", "positive", z3_command, [str(sat_file)], {0}, "sat"))
        results.append(run_command("T15", "Z3 SMT-LIB syntax", "negative", z3_command, [str(unsat_file)], {0}, "unsat"))
    versions = {
        "project_python": python_version(project_python, "project-python"),
        "system_python": python_version(system_python, "system-python"),
        "cvc5": python_probe(project_python, "cvc5", "import cvc5; print(getattr(cvc5, '__version__', 'unknown'))"),
        "z3": python_probe(system_python, "z3-python", "import z3; print(z3.get_version_string())"),
        "z3_cli": command_probe(z3_command, ["--version"], "z3-cli"),
    }
    return results, versions


def t16(minisat_command: str) -> tuple[list[CanaryResult], dict[str, str]]:
    sat = "p cnf 2 2\n1 0\n-1 2 0\n"
    unsat = "p cnf 1 2\n1 0\n-1 0\n"
    malformed = "not dimacs\n"
    return [
        run_minisat("T16", "MiniSat DIMACS CLI", "positive", minisat_command, sat, {10}, "SAT"),
        run_minisat("T16", "MiniSat DIMACS CLI", "negative", minisat_command, unsat, {20}, "UNSAT"),
        run_minisat("T16", "MiniSat DIMACS CLI", "error", minisat_command, malformed, {1, 2, 3, 4}, None),
        run_python("T16", "bounded subprocess", "timeout", sys.executable, "while True: pass", "timeout", timeout=0.2),
    ], {"cli": "MiniSat DIMACS protocol"}


def parse_tool_ids(raw: str) -> list[str]:
    selected = [item.strip().upper() for item in raw.split(",") if item.strip()]
    supported = {"T13", "T15", "T16"}
    unknown = sorted(set(selected) - supported)
    if unknown:
        raise ValueError(f"unsupported tool IDs: {','.join(unknown)}")
    result = list(dict.fromkeys(selected))
    if not result:
        raise ValueError("at least one tool ID is required")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="运行有界数学工具 canary")
    parser.add_argument("--tools", default="T13,T15,T16")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    try:
        selected = parse_tool_ids(args.tools)
    except ValueError as exc:
        parser.error(str(exc))
    if (
        not math.isfinite(DEFAULT_TIMEOUT)
        or not math.isfinite(PYTHON_TIMEOUT)
        or DEFAULT_TIMEOUT <= 0
        or PYTHON_TIMEOUT <= 0
        or DEFAULT_TIMEOUT > MAX_TIMEOUT_SECONDS
        or PYTHON_TIMEOUT > MAX_TIMEOUT_SECONDS
    ):
        parser.error("canary timeout budgets exceed the platform bound")
    if (
        MAX_OUTPUT_BYTES <= 0
        or MAX_OUTPUT_BYTES > MAX_OUTPUT_LIMIT
        or MEMORY_BUDGET_MB <= 0
        or MEMORY_BUDGET_MB > MAX_MEMORY_MB
        or THREADS_MAX <= 0
        or THREADS_MAX > MAX_THREADS
    ):
        parser.error("canary resource budgets exceed the platform bound")

    project_python = runtime_path(
        "MATH_CANARY_PROJECT_PYTHON",
        os.environ.get("MATH_TOOLS_PYTHON", sys.executable),
    )
    system_python = runtime_path(
        "MATH_CANARY_SYSTEM_PYTHON",
        os.environ.get("MATH_TOOLS_SYSTEM_PYTHON", sys.executable),
    )
    z3_command = runtime_path("MATH_CANARY_Z3", "z3")
    minisat_command = runtime_path("MATH_CANARY_MINISAT", "minisat")
    all_results: list[CanaryResult] = []
    identities: dict[str, dict[str, str]] = {}
    if "T13" in selected:
        cases, identity = t13(project_python)
        all_results.extend(cases)
        identities["T13"] = identity
    if "T15" in selected:
        cases, identity = t15(project_python, system_python, z3_command)
        all_results.extend(cases)
        identities["T15"] = identity
    if "T16" in selected:
        cases, identity = t16(minisat_command)
        all_results.extend(cases)
        identities["T16"] = identity

    failed = [item for item in all_results if item.status != "PASS"]
    runner_sha256 = os.environ.get("MATH_CANARY_SOURCE_SHA256", "")
    try:
        actual_runner_sha256 = hash_runner_source(Path(__file__))
    except (OSError, CanaryProcessFailure):
        actual_runner_sha256 = ""
    runner_bound = bool(runner_sha256) and runner_sha256 == actual_runner_sha256
    payload = {
        "schema_version": "math-tool-canary.v1",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "scope": "synthetic-bounded-runtime",
        "runner": {
            "source": "scripts/run_math_tool_canaries.py",
            "sha256": runner_sha256 or "unbound",
            "runtime_binding": "explicit-environment",
        },
        "execution_policy": {
            "timeout_seconds": max(DEFAULT_TIMEOUT, PYTHON_TIMEOUT),
            "memory_budget_mb": MEMORY_BUDGET_MB,
            "threads_max": THREADS_MAX,
            "max_output_bytes": MAX_OUTPUT_BYTES,
            "stop_condition": "每个选定 case 返回预期结果，或达到其 bounded timeout/错误边界",
            "termination": {
                "status": "completed" if all_results else "failed",
                "reason": "所有选定 canary case 均已返回终止状态" if all_results else "没有选定 canary case",
            },
        },
        "tools": selected,
        "identities": identities,
        "results": [asdict(item) for item in all_results],
        "summary": {
            "case_count": len(all_results),
            "passed": len(all_results) - len(failed),
            "failed": len(failed),
            "all_passed": not failed,
        },
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False))
    else:
        for item in all_results:
            print(f"{item.status:4} {item.tool_id} {item.component} {item.kind} {item.detail}")
        print(f"math tool canaries: {'PASS' if not failed else 'BLOCK'} cases={len(all_results)}")
    return 1 if args.strict and (failed or not runner_bound) else 0


if __name__ == "__main__":
    raise SystemExit(main())
