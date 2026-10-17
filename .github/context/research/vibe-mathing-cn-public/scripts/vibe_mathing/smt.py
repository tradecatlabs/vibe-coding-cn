"""固定 SymPy SAT/QF-LRA fixture 的有限 theory verifier。"""

from __future__ import annotations

import json
import os
import re
import stat
import sys
from pathlib import Path
from typing import Any

from .evidence import create_evidence_receipt
from .runtime import RuntimeErrorBase, execute_bounded, now


EXPECTED_SYMPY_VERSION = "1.14.0"
EXPECTED_STATEMENT = "对所有实数 x，若 0 <= x <= 1，则 x <= 0。"
BACKEND = "sympy-1.14-sat-qf-lra"
SMT_TIMEOUT_SECONDS = 30
SMT_RESOURCE_BUDGET = {
    "memory_budget_mb": 256,
    "threads_max": 1,
    "max_output_bytes": 1_048_576,
}
MAX_FIXTURE_BYTES = 1_048_576
MAX_OUTPUT_BYTES = SMT_RESOURCE_BUDGET["max_output_bytes"]
MAX_WITNESS_ABS = 1_000_000_000


def _reject_json_constant(value: str) -> Any:
    raise RuntimeError(f"SMT JSON 含非法常量：{value}")


def _read_fixture(fixture_root: Path) -> dict[str, Any]:
    root = fixture_root.resolve()
    if fixture_root.is_symlink() or fixture_root.absolute() != root or not root.is_dir():
        raise RuntimeError("SMT fixture root 不能通过 symlink 访问")
    path = root / "case.json"
    if path.is_symlink():
        raise RuntimeError("SMT fixture 不能是 symlink")
    nofollow = getattr(os, "O_NOFOLLOW", None)
    if nofollow is None:
        raise RuntimeError("当前平台无法安全读取 SMT fixture")
    descriptor = os.open(path, os.O_RDONLY | nofollow)
    try:
        file_stat = os.fstat(descriptor)
        if not stat.S_ISREG(file_stat.st_mode) or file_stat.st_size > MAX_FIXTURE_BYTES:
            raise RuntimeError("SMT fixture 文件超过大小预算或不是普通文件")
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(descriptor, min(64 * 1024, MAX_FIXTURE_BYTES - total + 1))
            if not chunk:
                break
            total += len(chunk)
            if total > MAX_FIXTURE_BYTES:
                raise RuntimeError("SMT fixture 文件超过大小预算")
            chunks.append(chunk)
        raw = b"".join(chunks)
    finally:
        os.close(descriptor)
    if len(raw) > MAX_FIXTURE_BYTES:
        raise RuntimeError("SMT fixture 文件超过大小预算")
    try:
        fixture = json.loads(raw.decode("utf-8"), parse_constant=_reject_json_constant)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RuntimeError("无法读取 SMT/LRA fixture") from exc
    if not isinstance(fixture, dict):
        raise RuntimeError("SMT/LRA fixture 必须是 object")
    return fixture


def _write_output(
    project_root: Path, run_key: str, name: str, payload: dict[str, Any]
) -> str:
    if (
        not isinstance(run_key, str)
        or len(run_key) > 256
        or not re.fullmatch(r"[a-z0-9][a-z0-9.-]*", run_key)
        or not isinstance(name, str)
        or len(name) > 256
        or not re.fullmatch(r"[a-z0-9][a-z0-9.-]*", name)
    ):
        raise RuntimeError("SMT verifier 输出组件无效")
    relative = f"research/artifacts/outputs/{run_key}/{name}.json"
    root = project_root.resolve()
    if project_root.is_symlink() or project_root.absolute() != root:
        raise RuntimeError("SMT verifier project root 不能通过 symlink 访问")
    path = root / relative
    lexical = root
    for part in Path(relative).parts:
        lexical = lexical / part
        if lexical.is_symlink():
            raise RuntimeError(f"SMT verifier 输出路径不能包含 symlink：{relative}")
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        encoded = (
            json.dumps(
                payload, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False
            )
            + "\n"
        )
    except (TypeError, ValueError) as exc:
        raise RuntimeError("SMT verifier 输出不是可移植 JSON") from exc
    encoded_bytes = encoded.encode("utf-8")
    if len(encoded_bytes) > SMT_RESOURCE_BUDGET["max_output_bytes"]:
        raise RuntimeError("SMT verifier 输出超过大小预算")
    if path.is_symlink():
        raise RuntimeError(f"SMT verifier 输出不能是 symlink：{relative}")
    if path.is_file():
        nofollow = getattr(os, "O_NOFOLLOW", None)
        if nofollow is None:
            raise RuntimeError("当前平台无法安全读取 SMT verifier 输出")
        descriptor = os.open(path, os.O_RDONLY | nofollow)
        try:
            file_stat = os.fstat(descriptor)
            if not stat.S_ISREG(file_stat.st_mode):
                raise RuntimeError("已有 SMT verifier 输出不是普通文件")
            if file_stat.st_size > MAX_OUTPUT_BYTES:
                raise RuntimeError("已有 SMT verifier 输出超过大小预算")
            chunks: list[bytes] = []
            total = 0
            while True:
                chunk = os.read(descriptor, min(64 * 1024, MAX_OUTPUT_BYTES - total + 1))
                if not chunk:
                    break
                total += len(chunk)
                if total > MAX_OUTPUT_BYTES:
                    raise RuntimeError("已有 SMT verifier 输出超过大小预算")
                chunks.append(chunk)
            existing = b"".join(chunks)
        finally:
            os.close(descriptor)
        if existing != encoded_bytes:
            raise RuntimeError(f"SMT verifier 输出已存在且内容不同：{relative}")
        return relative
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    nofollow = getattr(os, "O_NOFOLLOW", None)
    directory = getattr(os, "O_DIRECTORY", None)
    if nofollow is None or directory is None:
        raise RuntimeError("当前平台无法安全耐久写入 SMT verifier 输出")
    try:
        descriptor = os.open(
            temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | nofollow, 0o600
        )
    except OSError as exc:
        raise RuntimeError("无法创建 SMT verifier 输出暂存文件") from exc
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(encoded_bytes)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        directory_descriptor = os.open(path.parent, os.O_RDONLY | directory | nofollow)
        try:
            os.fsync(directory_descriptor)
        finally:
            os.close(directory_descriptor)
    finally:
        temporary.unlink(missing_ok=True)
    return relative


def _serialize_model(model: dict[Any, Any] | bool) -> dict[str, bool] | bool:
    if model is False:
        return False
    return {str(key): bool(value) for key, value in sorted(model.items(), key=lambda item: str(item[0]))}


def _evaluate_fixture(fixture: dict[str, Any]) -> dict[str, Any]:
    """Evaluate the fixed formulas; callers must run this in a bounded worker."""
    import sympy as sp
    from sympy.logic.inference import satisfiable

    statement = fixture.get("statement")
    witness_spec = fixture.get("witness", {})
    if (
        fixture.get("schema_version") != "1.0.0"
        or statement != EXPECTED_STATEMENT
        or not isinstance(witness_spec, dict)
        or not isinstance(witness_spec.get("numerator"), int)
        or isinstance(witness_spec.get("numerator"), bool)
        or not isinstance(witness_spec.get("denominator"), int)
        or isinstance(witness_spec.get("denominator"), bool)
        or witness_spec["denominator"] == 0
        or abs(witness_spec["numerator"]) > MAX_WITNESS_ABS
        or abs(witness_spec["denominator"]) > MAX_WITNESS_ABS
    ):
        raise RuntimeError("SMT/LRA fixture 契约漂移")

    p, q = sp.symbols("p q", boolean=True)
    propositional_sat = satisfiable(
        sp.And(sp.Or(p, q), sp.Or(sp.Not(p), q), sp.Or(p, sp.Not(q))),
        algorithm="dpll2",
    )
    propositional_unsat = satisfiable(sp.And(p, sp.Not(p)), algorithm="dpll2")

    x = sp.symbols("x", real=True)
    lra_formula = sp.And(x >= 0, x <= 1, x > 0)
    lra_contradiction = sp.And(x > 1, x < 0)
    lra_sat = satisfiable(lra_formula, use_lra_theory=True)
    lra_unsat = satisfiable(lra_contradiction, use_lra_theory=True)
    witness = sp.Rational(witness_spec["numerator"], witness_spec["denominator"])
    exact_witness_ok = bool(witness >= 0 and witness <= 1 and witness > 0)
    counterexample_ok = bool(
        propositional_sat is not False
        and propositional_unsat is False
        and lra_sat is not False
        and lra_unsat is False
        and exact_witness_ok
    )
    return {
        "backend": BACKEND,
        "sympy_version": sp.__version__,
        "propositional_sat": _serialize_model(propositional_sat),
        "propositional_unsat": propositional_unsat is False,
        "qf_lra_formula": str(lra_formula),
        "qf_lra_sat": _serialize_model(lra_sat),
        "qf_lra_contradiction_unsat": lra_unsat is False,
        "witness": str(witness),
        "exact_witness_ok": exact_witness_ok,
        "verdict": "accept" if counterexample_ok else "reject",
    }


def _bounded_smt_evaluation(
    fixture: dict[str, Any], runtime_root: Path
) -> tuple[dict[str, Any], list[str]]:
    worker = Path(__file__).with_name("smt_worker.py")
    if (
        worker.is_symlink()
        or worker.resolve() != worker
        or not worker.is_file()
        or not os.access(worker, os.R_OK)
    ):
        raise RuntimeError("bounded SMT verifier worker path is invalid")
    command = [sys.executable, str(worker)]
    try:
        fixture_text = json.dumps(
            fixture, ensure_ascii=False, sort_keys=True, allow_nan=False
        )
    except (TypeError, ValueError) as exc:
        raise RuntimeError("SMT fixture 不是可移植 JSON") from exc
    environment = {
        key: value
        for key, value in os.environ.items()
        if key in {"PATH", "HOME", "LANG", "LC_ALL", "TMPDIR"}
    }
    environment["PATH"] = environment.get("PATH", "/usr/local/bin:/usr/bin:/bin")
    try:
        completed = execute_bounded(
            command,
            cwd=runtime_root,
            timeout_seconds=SMT_TIMEOUT_SECONDS,
            max_output_bytes=SMT_RESOURCE_BUDGET["max_output_bytes"],
            memory_budget_mb=SMT_RESOURCE_BUDGET["memory_budget_mb"],
            threads_max=SMT_RESOURCE_BUDGET["threads_max"],
            env=environment,
            input_text=fixture_text,
        )
    except RuntimeErrorBase as exc:
        raise RuntimeError(f"bounded SMT verifier failed: {exc}") from exc
    if (
        not isinstance(completed, dict)
        or completed.get("exit_code") != 0
        or not isinstance(completed.get("stdout"), str)
        or not isinstance(completed.get("stderr"), str)
    ):
        detail = completed.get("stderr", "") if isinstance(completed, dict) else "worker returned malformed result"
        if not isinstance(detail, str):
            detail = "worker returned malformed result"
        detail = detail.strip() or "worker returned non-zero"
        raise RuntimeError(f"bounded SMT verifier failed: {detail[:240]}")
    try:
        payload = json.loads(
            completed["stdout"], parse_constant=_reject_json_constant
        )
    except (json.JSONDecodeError, ValueError) as exc:
        raise RuntimeError("bounded SMT verifier returned invalid JSON") from exc
    if not isinstance(payload, dict):
        raise RuntimeError("bounded SMT verifier output must be an object")
    if payload.get("backend") != BACKEND or payload.get("sympy_version") != EXPECTED_SYMPY_VERSION:
        raise RuntimeError("bounded SMT verifier output identity mismatch")
    if payload.get("verdict") not in {"accept", "reject"}:
        raise RuntimeError("bounded SMT verifier output verdict invalid")
    return payload, command


def verify_smt_fixture(
    *,
    project_root: Path,
    fixture_root: Path,
    result: dict[str, Any],
) -> list[dict[str, Any]]:
    """验证固定命题 SAT、QF-LRA 与精确 witness，返回两类独立证据。"""
    fixture = _read_fixture(fixture_root)
    statement = fixture.get("statement")
    witness_spec = fixture.get("witness", {}) if isinstance(fixture, dict) else {}
    if (
        not isinstance(fixture, dict)
        or fixture.get("schema_version") != "1.0.0"
        or statement != EXPECTED_STATEMENT
        or not isinstance(witness_spec, dict)
        or not isinstance(witness_spec.get("numerator"), int)
        or isinstance(witness_spec.get("numerator"), bool)
        or not isinstance(witness_spec.get("denominator"), int)
        or isinstance(witness_spec.get("denominator"), bool)
        or witness_spec.get("denominator") == 0
        or abs(witness_spec["numerator"]) > MAX_WITNESS_ABS
        or abs(witness_spec["denominator"]) > MAX_WITNESS_ABS
    ):
        raise RuntimeError("SMT/LRA fixture 契约漂移")

    solver_payload, solver_command = _bounded_smt_evaluation(fixture, project_root)
    counterexample_ok = solver_payload.get("verdict") == "accept"
    faithfulness_ok = statement == EXPECTED_STATEMENT
    run_key = result["result_id"].removeprefix("result:")
    solver_locator = _write_output(
        project_root,
        run_key,
        "smt-counterexample",
        solver_payload,
    )
    faithfulness_locator = _write_output(
        project_root,
        run_key,
        "smt-statement-faithfulness",
        {
            "expected": EXPECTED_STATEMENT,
            "actual": statement,
            "match": faithfulness_ok,
        },
    )
    checked_at = now()
    return [
        create_evidence_receipt(
            project_root=project_root,
            result=result,
            generator="smt-generator",
            evidence_id=f"evidence:{run_key}.smt-counterexample",
            capability="counterexample_check",
            verdict="accept" if counterexample_ok else "reject",
            verifier="sympy-smt-verifier",
            checked_at=checked_at,
            output_locator=solver_locator,
            command=solver_command,
            timeout_seconds=SMT_TIMEOUT_SECONDS,
            resource_budget=SMT_RESOURCE_BUDGET,
            stop_condition="固定 SAT/QF-LRA 公式和 witness 检查完成",
            termination_status="completed",
            termination_reason="fixture verifier returned",
            executor="subprocess",
            notes="bounded worker 中的 SymPy 命题 SAT、QF-LRA 与精确有理数 witness 复核",
        ),
        create_evidence_receipt(
            project_root=project_root,
            result=result,
            generator="smt-generator",
            evidence_id=f"evidence:{run_key}.faithfulness",
            capability="statement_faithfulness",
            verdict="accept" if faithfulness_ok else "reject",
            verifier="smt-statement-faithfulness-verifier",
            checked_at=checked_at,
            output_locator=faithfulness_locator,
            command=["fixture-verifier", "smt-statement-fixture-v1"],
            timeout_seconds=SMT_TIMEOUT_SECONDS,
            resource_budget=SMT_RESOURCE_BUDGET,
            stop_condition="固定 SMT fixture 陈述逐字比较完成",
            termination_status="completed",
            termination_reason="fixture verifier returned",
            executor="in_process",
            notes="固定 SMT fixture 的陈述逐字契约",
        ),
    ]
