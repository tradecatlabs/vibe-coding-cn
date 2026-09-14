"""确定性 SymPy 候选生成、独立验证与 Result 晋升流水线。"""

from __future__ import annotations

import json
import os
import re
import stat
import sys
from pathlib import Path
from typing import Any

from .evidence import create_evidence_receipt
from .runtime import (
    InjectedInterruption,
    RuntimeErrorBase,
    create_run,
    execute_bounded,
    locked_run,
    now,
    stable_run_id,
    transition,
)
from .store import ResearchStore, StoreError


SYMPY_ADAPTER = "sympy-counterexample-v1"
EXPECTED_STATEMENT = "对所有实数 x，x^2 >= x。"
SYMPY_MAX_OUTPUT_BYTES = 1_048_576


def _reject_json_constant(value: str) -> Any:
    raise StoreError(f"SymPy verifier JSON 含非法常量：{value}")


def _safe_component(value: str, label: str) -> str:
    if not isinstance(value, str) or len(value) > 256 or not re.fullmatch(
        r"[a-z0-9][a-z0-9.-]*", value
    ):
        raise StoreError(f"{label} 路径组件无效")
    return value


def _read_artifact(path: Path) -> bytes:
    nofollow = getattr(os, "O_NOFOLLOW", None)
    if nofollow is None:
        raise StoreError("当前平台无法安全读取 artifact")
    try:
        descriptor = os.open(path, os.O_RDONLY | nofollow)
    except OSError as exc:
        raise StoreError(f"无法读取确定性 artifact：{path}") from exc
    try:
        file_stat = os.fstat(descriptor)
        if not stat.S_ISREG(file_stat.st_mode):
            raise StoreError("artifact 不是普通文件")
        if file_stat.st_size > SYMPY_MAX_OUTPUT_BYTES:
            raise StoreError("已有 artifact 超过输出预算")
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(descriptor, min(64 * 1024, SYMPY_MAX_OUTPUT_BYTES - total + 1))
            if not chunk:
                return b"".join(chunks)
            total += len(chunk)
            if total > SYMPY_MAX_OUTPUT_BYTES:
                raise StoreError("已有 artifact 超过输出预算")
            chunks.append(chunk)
    except OSError as exc:
        raise StoreError(f"无法读取确定性 artifact：{path}") from exc
    finally:
        os.close(descriptor)


def _safe_artifact_path(project_root: Path, relative: str) -> Path:
    if (
        not isinstance(relative, str)
        or len(relative) > 4_096
        or "\x00" in relative
        or "\\" in relative
    ):
        raise StoreError("artifact 路径包含非法字符或超过大小预算")
    path = Path(relative)
    if path.is_absolute() or any(part in {".", ".."} for part in path.parts):
        raise StoreError(f"artifact 路径越界：{relative}")
    root = project_root.resolve()
    if project_root.is_symlink() or project_root.absolute() != root:
        raise StoreError("artifact project root 不能通过 symlink 访问")
    lexical = root
    for part in path.parts:
        lexical = lexical / part
        if lexical.is_symlink():
            raise StoreError(f"artifact 路径不能包含 symlink：{relative}")
    resolved = (root / path).resolve()
    if resolved != root and root not in resolved.parents:
        raise StoreError(f"artifact 路径越界：{relative}")
    if resolved.is_symlink():
        raise StoreError(f"artifact 路径不能是 symlink：{relative}")
    return resolved


def _artifact(project_root: Path, run_id: str, name: str, payload: dict[str, Any]) -> str:
    if not isinstance(payload, dict):
        raise StoreError("artifact payload 必须是 object")
    if not isinstance(run_id, str):
        raise StoreError("run 路径组件无效")
    run_component = _safe_component(run_id.removeprefix("run:"), "run")
    name_component = _safe_component(name, "artifact")
    relative = f"research/artifacts/outputs/{run_component}/{name_component}.json"
    path = _safe_artifact_path(project_root, relative)
    path.parent.mkdir(parents=True, exist_ok=True)
    _safe_artifact_path(project_root, str(path.relative_to(project_root.resolve())))
    try:
        encoded = (
            json.dumps(
                payload, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False
            )
            + "\n"
        )
    except (TypeError, ValueError) as exc:
        raise StoreError("artifact 不是可移植 JSON") from exc
    if len(encoded.encode("utf-8")) > SYMPY_MAX_OUTPUT_BYTES:
        raise StoreError("artifact 超过输出预算")
    if path.is_symlink():
        raise StoreError(f"确定性 artifact 不能是 symlink：{relative}")
    encoded_bytes = encoded.encode("utf-8")
    if path.is_file():
        nofollow = getattr(os, "O_NOFOLLOW", None)
        if nofollow is None:
            raise StoreError("当前平台无法安全读取 artifact")
        try:
            existing = _read_artifact(path)
        except StoreError as exc:
            raise StoreError(f"无法读取确定性 artifact：{relative}") from exc
        if existing == encoded_bytes:
            return relative
        raise StoreError(f"确定性 artifact 内容漂移：{relative}")
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    nofollow = getattr(os, "O_NOFOLLOW", None)
    directory = getattr(os, "O_DIRECTORY", None)
    if nofollow is None or directory is None:
        raise StoreError("当前平台无法安全耐久写入 artifact")
    try:
        descriptor = os.open(
            temporary,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | nofollow,
            0o600,
        )
    except OSError as exc:
        raise StoreError(f"无法创建 artifact 暂存文件：{relative}") from exc
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(encoded_bytes)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        directory_descriptor = os.open(
            path.parent, os.O_RDONLY | directory | nofollow
        )
        try:
            os.fsync(directory_descriptor)
        finally:
            os.close(directory_descriptor)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise
    return relative


def _bounded_counterexample(
    project_root: Path, runtime_budget: dict[str, Any]
) -> tuple[dict[str, Any], list[str]]:
    worker = Path(__file__).with_name("sympy_counterexample_worker.py")
    if (
        worker.is_symlink()
        or worker.resolve() != worker
        or not worker.is_file()
        or not os.access(worker, os.R_OK)
    ):
        raise StoreError("bounded SymPy verifier worker path is invalid")
    environment = {
        key: value
        for key, value in os.environ.items()
        if key in {"PATH", "HOME", "LANG", "LC_ALL", "TMPDIR"}
    }
    environment["PATH"] = environment.get("PATH", "/usr/local/bin:/usr/bin:/bin")
    command = [sys.executable, str(worker)]
    try:
        completed = execute_bounded(
            command,
            cwd=project_root,
            timeout_seconds=runtime_budget["timeout_seconds"],
            max_output_bytes=runtime_budget["max_output_bytes"],
            memory_budget_mb=runtime_budget["memory_budget_mb"],
            threads_max=runtime_budget["threads_max"],
            env=environment,
        )
    except RuntimeErrorBase as exc:
        raise StoreError(f"bounded SymPy verifier failed: {exc}") from exc
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
        raise StoreError(f"bounded SymPy verifier failed: {detail[:240]}")
    try:
        payload = json.loads(
            completed["stdout"], parse_constant=_reject_json_constant
        )
    except (json.JSONDecodeError, ValueError) as exc:
        raise StoreError("bounded SymPy verifier returned invalid JSON") from exc
    if (
        not isinstance(payload, dict)
        or payload.get("backend") != "sympy-exact-rational-v1"
        or payload.get("x") != "1/2"
        or payload.get("x_squared") != "1/4"
        or payload.get("x_squared_lt_x") is not True
    ):
        raise StoreError("bounded SymPy verifier output identity mismatch")
    return payload, command


def _problem(store: ResearchStore, problem_id: str) -> dict[str, Any]:
    for item in store.read("problems"):
        if item["problem_id"] == problem_id:
            return item
    raise StoreError(f"Problem 不存在：{problem_id}")


def run_sympy_pipeline(
    project_root: Path,
    problem_id: str,
    *,
    fail_after: str | None = None,
) -> dict[str, Any]:
    run_id = stable_run_id(problem_id, SYMPY_ADAPTER)
    with locked_run(project_root, run_id):
        return _run_sympy_pipeline_locked(
            project_root, problem_id, fail_after=fail_after
        )


def _run_sympy_pipeline_locked(
    project_root: Path,
    problem_id: str,
    *,
    fail_after: str | None,
) -> dict[str, Any]:
    store = ResearchStore(project_root)
    problem = _problem(store, problem_id)
    if problem["lifecycle"] != "active":
        raise StoreError("只有 lifecycle=active 的 ProblemContract 可以运行")
    constraints = problem["constraints"]
    runtime_budget = constraints["runtime"]
    evidence_resource_budget = {
        "memory_budget_mb": runtime_budget["memory_budget_mb"],
        "threads_max": runtime_budget["threads_max"],
        "max_output_bytes": runtime_budget["max_output_bytes"],
    }
    if SYMPY_ADAPTER not in constraints["allowed_adapters"]:
        raise StoreError(f"ProblemContract 未允许 adapter={SYMPY_ADAPTER}")
    if "computation" not in constraints["allowed_methods"]:
        raise StoreError("ProblemContract 未允许 computation 研究方法")
    state = create_run(
        project_root,
        problem_id,
        SYMPY_ADAPTER,
        budgets=constraints["runtime"],
    )
    if state["status"] in {"accepted", "rejected"}:
        if state["status"] == "accepted":
            run_suffix = state["run_id"].removeprefix("run:")
            result_id = f"result:{run_suffix}"
            if result_id not in store.rebuild_solution_view():
                raise StoreError(
                    f"运行曾被接受，但当前 Result 已失效：{result_id}"
                )
        return state
    if problem["statement"]["text"] != EXPECTED_STATEMENT:
        raise StoreError("SymPy fixture adapter 拒绝未注册的问题陈述")
    if state["status"] == "planned":
        state = transition(project_root, state, "routed")
    if state["status"] == "routed":
        state = transition(project_root, state, "running")
    run_suffix = state["run_id"].removeprefix("run:")
    attempt_id = f"attempt:{run_suffix}"
    result_id = f"result:{run_suffix}"
    existing_attempts = [
        item for item in store.read("attempts") if item["problem_id"] == problem_id
    ]
    if not any(item["attempt_id"] == attempt_id for item in existing_attempts) and len(
        existing_attempts
    ) >= constraints["max_attempts"]:
        raise StoreError("ProblemContract 的 max_attempts 预算耗尽")
    if state["status"] == "running":
        candidate_locator = _artifact(
            project_root,
            state["run_id"],
            "candidate",
            {"candidate": {"x": "1/2"}, "claim": "x^2 < x"},
        )
        started = state["created_at"]
        attempt = {
            "attempt_id": attempt_id,
            "problem_id": problem_id,
            "generator": "sympy-generator",
            "objective": "寻找全称命题的精确反例",
            "method": "computation",
            "lifecycle": "completed",
            "started_at": started,
            "completed_at": started,
            "inputs": [problem_id],
            "claims": ["x=1/2 是候选反例"],
            "artifacts": [candidate_locator],
        }
        store.upsert("attempts", attempt)
        state = transition(project_root, state, "candidate_ready")
        if fail_after == "candidate_ready":
            raise InjectedInterruption("故障注入：candidate_ready")
    if state["status"] == "candidate_ready":
        state = transition(project_root, state, "verifying")
    if state["status"] == "verifying":
        verification_at = state["updated_at"]
        counterexample_payload, counterexample_command = _bounded_counterexample(
            project_root, runtime_budget
        )
        counterexample_ok = counterexample_payload["x_squared_lt_x"] is True
        check_locator = _artifact(
            project_root,
            state["run_id"],
            "counterexample-check",
            {
                "x": counterexample_payload["x"],
                "x_squared": counterexample_payload["x_squared"],
                "x_squared_lt_x": counterexample_payload["x_squared_lt_x"],
            },
        )
        faithfulness_ok = problem["statement"]["text"] == EXPECTED_STATEMENT
        faithfulness_locator = _artifact(
            project_root,
            state["run_id"],
            "statement-faithfulness",
            {"expected": EXPECTED_STATEMENT, "actual": problem["statement"]["text"], "match": faithfulness_ok},
        )
        result = {
            "result_id": result_id,
            "problem_id": problem_id,
            "attempt_id": attempt_id,
            "kind": "counterexample",
            "claim": "x=1/2 时 x^2=1/4<1/2，因此原全称命题为假。",
            "scope": "实数域上的精确有理数反例",
            "outcome": "refuted",
            "evidence": [],
            "created_at": verification_at,
        }
        if not (counterexample_ok and faithfulness_ok):
            result["outcome"] = "inconclusive"
        result["evidence"] = [
            create_evidence_receipt(
                project_root=project_root,
                result=result,
                generator="sympy-generator",
                evidence_id=f"evidence:{run_suffix}.counterexample",
                capability="counterexample_check",
                verdict="accept" if counterexample_ok else "reject",
                verifier="sympy-counterexample-verifier",
                checked_at=verification_at,
                output_locator=check_locator,
                command=counterexample_command,
                timeout_seconds=runtime_budget["timeout_seconds"],
                resource_budget=evidence_resource_budget,
                stop_condition="固定有理数 witness 检查完成或 verifier 返回失败",
                termination_status="completed",
                termination_reason="fixture verifier returned",
                executor="subprocess",
                notes="bounded worker 中的 SymPy exact Rational 独立复算",
            ),
            create_evidence_receipt(
                project_root=project_root,
                result=result,
                generator="sympy-generator",
                evidence_id=f"evidence:{run_suffix}.faithfulness",
                capability="statement_faithfulness",
                verdict="accept" if faithfulness_ok else "reject",
                verifier="statement-faithfulness-verifier",
                checked_at=verification_at,
                output_locator=faithfulness_locator,
                command=["fixture-verifier", "fixture-statement-contract-v1"],
                timeout_seconds=runtime_budget["timeout_seconds"],
                resource_budget=evidence_resource_budget,
                stop_condition="固定 ProblemContract 陈述逐字比较完成",
                termination_status="completed",
                termination_reason="fixture verifier returned",
                executor="in_process",
                notes="固定 fixture 的陈述逐字契约",
            ),
        ]
        store.upsert("results", result)
        if fail_after == "result_written":
            raise InjectedInterruption("故障注入：result_written")
        solution_ids = store.rebuild_solution_view()
        state = transition(
            project_root,
            state,
            "accepted" if result_id in solution_ids else "rejected",
        )
    return state


def invalidate_sympy_result(project_root: Path, run_id: str) -> list[str]:
    store = ResearchStore(project_root)
    result_id = f"result:{run_id.removeprefix('run:')}"
    result = next(item for item in store.read("results") if item["result_id"] == result_id)
    runtime_budget = _problem(store, result["problem_id"])["constraints"]["runtime"]
    evidence_resource_budget = {
        "memory_budget_mb": runtime_budget["memory_budget_mb"],
        "threads_max": runtime_budget["threads_max"],
        "max_output_bytes": runtime_budget["max_output_bytes"],
    }
    invalidation_id = f"evidence:{run_id.removeprefix('run:')}.invalidation"
    if any(item["evidence_id"] == invalidation_id for item in result["evidence"]):
        return store.rebuild_solution_view()
    target = result["evidence"][0]["evidence_id"]
    invalidation_locator = _artifact(
        project_root,
        run_id,
        "invalidation",
        {"invalidates": [target], "reason": "regression-test"},
    )
    result["evidence"].append(
        create_evidence_receipt(
            project_root=project_root,
            result=result,
            generator="sympy-generator",
            evidence_id=invalidation_id,
            capability="counterexample_check",
            verdict="reject",
            verifier="sympy-counterexample-verifier",
            checked_at=now(),
            output_locator=invalidation_locator,
            command=["fixture-verifier", "append-only-invalidation-v1"],
            timeout_seconds=runtime_budget["timeout_seconds"],
            resource_budget=evidence_resource_budget,
            stop_condition="append-only 失效目标检查完成",
            termination_status="completed",
            termination_reason="fixture verifier returned",
            executor="in_process",
            notes="append-only 失效记录",
            invalidates=[target],
        )
    )
    result["outcome"] = "withdrawn"
    store.replace_result(result)
    return store.rebuild_solution_view()
