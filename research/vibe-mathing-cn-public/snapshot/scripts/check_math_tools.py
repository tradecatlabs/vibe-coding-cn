#!/usr/bin/env python3
# 做什么：按数学领域探测工具存在性、运行时和最小真实行为，输出文本或 JSON 证据。
# 怎么运行：python3 scripts/check_math_tools.py --profile millennium --strict [--json]。
# 需要什么：Python 3 标准库；被选 profile 的 required 工具必须已安装。

from __future__ import annotations

import argparse
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable

from vibe_mathing.runtime import RuntimeErrorBase, execute_bounded

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SYSTEM_PYTHON = Path(os.environ.get("MATH_TOOLS_SYSTEM_PYTHON", "/usr/bin/python3"))
FENICS_PYTHON = Path(os.environ.get("MATH_TOOLS_FENICS_PYTHON", str(SYSTEM_PYTHON)))
TIMEOUT_SECONDS = int(os.environ.get("MATH_TOOLS_TIMEOUT_SECONDS", "30"))
MAX_OUTPUT_BYTES = int(os.environ.get("MATH_TOOLS_MAX_OUTPUT_BYTES", "1048576"))
MEMORY_BUDGET_MB = int(os.environ.get("MATH_TOOLS_MEMORY_BUDGET_MB", "512"))
THREADS_MAX = int(os.environ.get("MATH_TOOLS_THREADS_MAX", "1"))
MAX_TIMEOUT_SECONDS = 300
MAX_OUTPUT_LIMIT = 128_000_000
MAX_MEMORY_MB = 131_072
MAX_THREADS = 1_024


def _safe_environment() -> dict[str, str]:
    """Do not pass unrelated credentials or agent configuration to probed tools."""
    allowed = {"PATH", "HOME", "LANG", "LC_ALL", "TMPDIR"}
    environment = {key: value for key, value in os.environ.items() if key in allowed}
    environment["PATH"] = environment.get("PATH", "/usr/local/bin:/usr/bin:/bin")
    return environment


def configured_command(env_name: str, default: str) -> str:
    return os.environ.get(env_name, default)


def read_bounded_result(path: Path) -> str:
    nofollow = getattr(os, "O_NOFOLLOW", None)
    if nofollow is None:
        raise OSError("O_NOFOLLOW unavailable for verifier output")
    descriptor = os.open(path, os.O_RDONLY | nofollow)
    try:
        file_stat = os.fstat(descriptor)
        if not stat.S_ISREG(file_stat.st_mode) or file_stat.st_size > MAX_OUTPUT_BYTES:
            raise OSError("verifier output exceeds size budget or is not regular")
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(descriptor, min(64 * 1024, MAX_OUTPUT_BYTES - total + 1))
            if not chunk:
                return b"".join(chunks).decode("ascii")
            total += len(chunk)
            if total > MAX_OUTPUT_BYTES:
                raise OSError("verifier output exceeds size budget")
            chunks.append(chunk)
    finally:
        os.close(descriptor)


@dataclass(frozen=True)
class CheckResult:
    capability: str
    runtime: str
    required: bool
    status: str
    detail: str


def run_process(
    command: list[str],
    *,
    input_text: str | None = None,
) -> subprocess.CompletedProcess[str]:
    if (
        TIMEOUT_SECONDS <= 0
        or TIMEOUT_SECONDS > MAX_TIMEOUT_SECONDS
        or MAX_OUTPUT_BYTES <= 0
        or MAX_OUTPUT_BYTES > MAX_OUTPUT_LIMIT
        or MEMORY_BUDGET_MB <= 0
        or MEMORY_BUDGET_MB > MAX_MEMORY_MB
        or THREADS_MAX <= 0
        or THREADS_MAX > MAX_THREADS
    ):
        raise OSError("math tool probe budgets exceed the platform bound")
    try:
        bounded = execute_bounded(
            command,
            cwd=PROJECT_ROOT,
            timeout_seconds=TIMEOUT_SECONDS,
            max_output_bytes=MAX_OUTPUT_BYTES,
            memory_budget_mb=MEMORY_BUDGET_MB,
            threads_max=THREADS_MAX,
            env=_safe_environment(),
            input_text=input_text,
        )
    except RuntimeErrorBase as exc:
        if "超时" in str(exc):
            raise subprocess.TimeoutExpired(command, TIMEOUT_SECONDS) from exc
        raise OSError(str(exc)) from exc
    return subprocess.CompletedProcess(
        command,
        bounded["exit_code"],
        bounded["stdout"],
        bounded["stderr"],
    )


def check_command(
    capability: str,
    command: str,
    smoke_args: list[str],
    *,
    required: bool = True,
    accepted_codes: tuple[int, ...] = (0,),
    input_text: str | None = None,
    expected: str | None = None,
    runtime_label: str | None = None,
) -> CheckResult:
    runtime = runtime_label or Path(command).name
    executable = shutil.which(command)
    if executable is None:
        return CheckResult(capability, runtime, required, "missing", "命令不存在")
    try:
        completed = run_process([executable, *smoke_args], input_text=input_text)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return CheckResult(capability, runtime, required, "error", type(exc).__name__)
    combined = f"{completed.stdout}\n{completed.stderr}"
    if completed.returncode not in accepted_codes:
        return CheckResult(
            capability, runtime, required, "error", f"退出码 {completed.returncode}"
        )
    if expected is not None and expected not in combined:
        return CheckResult(capability, runtime, required, "error", "行为断言未满足")
    first_line = next((line.strip() for line in combined.splitlines() if line.strip()), "PASS")
    return CheckResult(capability, runtime, required, "ready", first_line[:160])


def check_python(
    capability: str,
    python: Path,
    imports: list[str],
    assertion: str,
    *,
    required: bool = True,
    runtime_label: str | None = None,
) -> CheckResult:
    runtime = runtime_label or (
        "project-python" if python.resolve() == Path(sys.executable).resolve() else "system-python"
    )
    if not python.is_file():
        return CheckResult(capability, runtime, required, "missing", "Python 运行时不存在")
    program = ";".join([*(f"import {name}" for name in imports), assertion, "print('PASS')"])
    try:
        completed = run_process([str(python), "-c", program])
    except (OSError, subprocess.TimeoutExpired) as exc:
        return CheckResult(capability, runtime, required, "error", type(exc).__name__)
    if completed.returncode != 0 or "PASS" not in completed.stdout:
        detail = completed.stderr.strip().splitlines()[-1] if completed.stderr.strip() else f"退出码 {completed.returncode}"
        return CheckResult(capability, runtime, required, "error", detail[:160])
    return CheckResult(capability, runtime, required, "ready", "最小行为 PASS")


def check_minisat() -> CheckResult:
    executable = shutil.which("minisat")
    if executable is None:
        return CheckResult("sat-solving", "minisat", True, "missing", "命令不存在")
    with tempfile.TemporaryDirectory(prefix="math-tools-") as directory:
        source = Path(directory) / "input.cnf"
        result = Path(directory) / "result.txt"
        source.write_text("p cnf 2 2\n1 0\n-1 2 0\n", encoding="ascii")
        try:
            completed = run_process([executable, str(source), str(result)])
        except (OSError, subprocess.TimeoutExpired) as exc:
            return CheckResult("sat-solving", "minisat", True, "error", type(exc).__name__)
        if result.is_symlink():
            return CheckResult("sat-solving", "minisat", True, "error", "结果文件不能是 symlink")
        try:
            result_text = read_bounded_result(result) if result.exists() else ""
        except (OSError, UnicodeError) as exc:
            return CheckResult("sat-solving", "minisat", True, "error", type(exc).__name__)
        result_lines = result_text.splitlines()
        if completed.returncode != 10 or not result_lines or result_lines[0] != "SAT":
            return CheckResult("sat-solving", "minisat", True, "error", f"协议退出码 {completed.returncode}")
    return CheckResult("sat-solving", "minisat", True, "ready", "SAT 协议 PASS")


def project_python_checks() -> dict[str, CheckResult]:
    return {
        "project-python-portable": check_python(
            "portable-symbolic-numeric",
            Path(sys.executable),
            ["sympy", "numpy", "scipy", "mpmath"],
            "assert sympy.factor(sympy.Symbol('x')**2-1)==(sympy.Symbol('x')-1)*(sympy.Symbol('x')+1)",
        ),
        "project-python-core": check_python(
            "core-symbolic-numeric",
            Path(sys.executable),
            ["sympy", "numpy", "scipy", "mpmath", "flint", "gmpy2"],
            "assert sympy.factor(sympy.Symbol('x')**2-1)==(sympy.Symbol('x')-1)*(sympy.Symbol('x')+1)",
        ),
        "project-python-graph": check_python(
            "graph-combinatorics",
            Path(sys.executable),
            ["networkx", "igraph"],
            "assert sum(networkx.triangles(networkx.complete_graph(3)).values())//3==1 and igraph.Graph.Full(4).ecount()==6",
        ),
        "project-python-smt": check_python(
            "smt-sat-python",
            Path(sys.executable),
            ["cvc5", "pysat.solvers"],
            (
                "s=cvc5.Solver();s.setLogic('QF_LIA');"
                "x=s.mkConst(s.getIntegerSort(),'x');"
                "s.assertFormula(s.mkTerm(cvc5.Kind.GT,x,s.mkInteger(0)));"
                "assert s.checkSat().isSat() and "
                "pysat.solvers.Solver(name='m22',bootstrap_with=[[1]]).solve()"
            ),
        ),
    }


def system_python_checks() -> list[CheckResult]:
    return [
        check_python(
            "smt-z3-python",
            SYSTEM_PYTHON,
            ["z3"],
            "x=z3.Int('x');s=z3.Solver();s.add(x>0,x<2);assert s.check()==z3.sat",
            runtime_label="system-python",
        ),
        check_python(
            "pde-fem",
            FENICS_PYTHON,
            ["dolfinx", "dolfinx.mesh", "petsc4py", "slepc4py", "mpi4py", "ufl"],
            "m=dolfinx.mesh.create_unit_square(mpi4py.MPI.COMM_SELF,2,2);assert m.topology.dim==2",
            runtime_label="fenics-python",
        ),
    ]


def cli_checks() -> dict[str, Callable[[], CheckResult]]:
    return {
        "sage": lambda: check_command(
            "number-theory",
            configured_command("MATH_TOOLS_SAGE", "sage"),
            ["-c", "assert list(ZZ(91).factor())==[(ZZ(7),1),(ZZ(13),1)];print('PASS')"],
            expected="PASS",
            runtime_label="sage",
        ),
        "gap": lambda: check_command("finite-algebra", "gap", ["-q"], input_text='if Size(SymmetricGroup(4)) <> 24 then Error("bad"); fi; Print("PASS"); QUIT;\n', expected="PASS"),
        "pari": lambda: check_command("number-theory", "gp", ["-fq"], input_text='if(factor(91) != [7,1;13,1], error("bad")); print("PASS")\n', expected="PASS"),
        "singular": lambda: check_command("computer-algebra", "Singular", ["-q"], input_text='ring r=0,(x,y),dp; ideal i=x2-y; if(size(std(i))<1){exit(1);} print("PASS"); quit;\n', expected="PASS"),
        "macaulay2": lambda: check_command("algebraic-geometry", "M2", ["--script", "/dev/stdin"], input_text='R=QQ[x,y]; assert(dim R==2); print "PASS"; exit 0\n', expected="PASS"),
        "z3": lambda: check_command("smt-solving", "z3", ["-version"]),
        "minisat": check_minisat,
        "polymake": lambda: check_command("polyhedral-geometry", "polymake", ["--version"]),
        "4ti2": lambda: check_command("integer-algebra", "4ti2-zsolve", ["--help"]),
        "topcom": lambda: check_command("triangulations", "topcom-points2chiro", ["--help"]),
        "nauty": lambda: check_command("graph-generation", "nauty-geng", ["-q", "3"]),
        "mpi": lambda: check_command("parallel-runtime", "mpirun", ["--version"]),
        "lean": lambda: check_command(
            "kernel-check",
            configured_command("MATH_TOOLS_LEAN", "lean"),
            ["--version"],
            runtime_label="lean",
        ),
        "lake": lambda: check_command(
            "lean-build",
            configured_command("MATH_TOOLS_LAKE", "lake"),
            ["--version"],
            runtime_label="lake",
        ),
    }


PROFILE_KEYS = {
    "portable": ["project-python-portable"],
    "core": ["project-python-core"],
    "number-theory": ["project-python-core", "sage", "pari", "gap"],
    "complexity": ["project-python-smt", "system-python-z3", "z3", "minisat"],
    "algebraic-geometry": ["sage", "singular", "macaulay2", "polymake", "4ti2", "topcom"],
    "combinatorics": ["project-python-graph", "gap", "nauty", "polymake"],
    "pde": ["system-python-pde", "mpi"],
    "formalization": ["lean", "lake"],
}
PROFILE_KEYS["millennium"] = list(
    dict.fromkeys(key for name in PROFILE_KEYS for key in PROFILE_KEYS[name])
)


def collect(profile: str) -> list[CheckResult]:
    selected = PROFILE_KEYS[profile]
    project = project_python_checks()
    system = system_python_checks()
    results: list[CheckResult] = [project[key] for key in selected if key in project]
    if "system-python-z3" in selected:
        results.append(system[0])
    if "system-python-pde" in selected:
        results.append(system[1])
    commands = cli_checks()
    results.extend(commands[key]() for key in selected if key in commands)
    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="探测数学工具能力")
    parser.add_argument("--profile", choices=sorted(PROFILE_KEYS), default="core")
    parser.add_argument("--json", action="store_true", help="输出机器可读 JSON")
    parser.add_argument("--strict", action="store_true", help="required 能力缺失时非零退出")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    results = collect(args.profile)
    failed = [result for result in results if result.required and result.status != "ready"]
    payload = {
        "schema_version": 1,
        "profile": args.profile,
        "ready": not failed,
        "results": [asdict(result) for result in results],
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        for result in results:
            print(f"{result.status.upper():7} {result.capability:24} {result.runtime:16} {result.detail}")
        print(f"Math tool profile {args.profile}: {'PASS' if not failed else 'BLOCK'}")
    return 1 if args.strict and failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
