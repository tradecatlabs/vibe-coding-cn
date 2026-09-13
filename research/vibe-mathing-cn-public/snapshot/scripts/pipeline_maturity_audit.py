#!/usr/bin/env python3
# 做什么：现场运行生产闭环 required capabilities，并从退出码派生 0–100 成熟度。
# 怎么运行：python3 scripts/pipeline_maturity_audit.py [--strict] [--output path]
# 需要什么：Python 3、项目依赖；严格模式要求 Lean/Mathlib fixture 可真实构建。

from __future__ import annotations

import argparse
import json
import os
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from vibe_mathing.runtime import RuntimeErrorBase, execute_bounded


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_BYTES = 4_000_000
CAPABILITIES = [
    ("trusted-evidence", 10, ["python3", "scripts/test_trusted_evidence.py"], 60, 512),
    ("evidence-attacks", 10, ["python3", "scripts/test_evidence_attacks.py"], 60, 512),
    ("research-space", 10, ["python3", "scripts/test_research_spaces.py"], 60, 512),
    ("atomic-store", 15, ["python3", "scripts/test_research_store.py"], 60, 512),
    ("bounded-runtime", 15, ["python3", "scripts/test_vibe_mathing_runtime.py"], 60, 512),
    ("sympy-e2e", 15, ["python3", "scripts/test_vibe_mathing_pipeline.py"], 120, 512),
    # The Lean runtime reserves virtual address space for its worker pool; the
    # inner adapter still enforces its own 8192 MiB ceiling and -j1 policy.
    ("lean-e2e", 15, ["python3", "scripts/test_lean_pipeline.py"], 900, 12288),
    ("portable-quality-gate", 10, ["make", "check"], 300, 512),
]


def _safe_environment() -> dict[str, str]:
    allowed = {"PATH", "HOME", "LANG", "LC_ALL", "TMPDIR"}
    environment = {key: value for key, value in os.environ.items() if key in allowed}
    environment["PATH"] = os.pathsep.join(
        [str(Path.home() / ".elan/bin"), environment.get("PATH", "/usr/local/bin:/usr/bin:/bin")]
    )
    return environment


def _redact_output(value: str) -> str:
    value = value.replace(str(ROOT), "<project-root>")
    value = value.replace(str(Path.home()), "<home>")
    value = re.sub(r"/tmp/[A-Za-z0-9._-]+", "<tmp>", value)
    return value[-4000:]


def _write_report(path: Path, data: bytes) -> None:
    root = ROOT.resolve()
    if path.is_absolute() or ".." in path.parts:
        raise RuntimeError("maturity report path must be repository-relative")
    candidate = root / path
    lexical = root
    for part in path.parts:
        lexical = lexical / part
        if lexical.is_symlink():
            raise RuntimeError("maturity report path cannot contain symlink")
    candidate.parent.mkdir(parents=True, exist_ok=True)
    nofollow = getattr(os, "O_NOFOLLOW", None)
    directory = getattr(os, "O_DIRECTORY", None)
    if nofollow is None or directory is None:
        raise RuntimeError("platform cannot safely publish maturity report")
    temporary = candidate.with_name(f".{candidate.name}.{os.getpid()}.tmp")
    try:
        descriptor = os.open(
            temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | nofollow, 0o600
        )
    except OSError as exc:
        raise RuntimeError("cannot create maturity report temporary file") from exc
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, candidate)
        directory_descriptor = os.open(
            candidate.parent, os.O_RDONLY | directory | nofollow
        )
        try:
            os.fsync(directory_descriptor)
        finally:
            os.close(directory_descriptor)
    finally:
        temporary.unlink(missing_ok=True)


def run_capability(
    capability_id: str,
    weight: int,
    argv: list[str],
    timeout: int,
    memory_budget_mb: int,
) -> dict[str, Any]:
    started = time.monotonic()
    resource_budget = {
        "memory_budget_mb": memory_budget_mb,
        "threads_max": 1,
        "max_output_bytes": DEFAULT_OUTPUT_BYTES,
    }
    stop_condition = "命令完成、退出码非零、超时或输出/资源预算触发"
    passed = False
    exit_code: int | None = None
    output = ""
    try:
        completed = execute_bounded(
            argv,
            cwd=ROOT,
            timeout_seconds=timeout,
            max_output_bytes=DEFAULT_OUTPUT_BYTES,
            memory_budget_mb=memory_budget_mb,
            threads_max=1,
            env=_safe_environment(),
        )
        exit_code = completed["exit_code"]
        output = completed["stdout"] + completed["stderr"]
        passed = exit_code == 0
        termination = {
            "status": "completed" if passed else "failed",
            "reason": "命令返回退出码 0" if passed else f"命令返回退出码 {exit_code}",
        }
    except (OSError, RuntimeErrorBase) as exc:
        output = str(exc)
        termination = {
            "status": "timed_out" if "超时" in str(exc) else "failed",
            "reason": str(exc),
        }
    duration = time.monotonic() - started
    return {
        "id": capability_id,
        "weight": weight,
        "status": "PASS" if passed else "FAIL",
        "argv": argv,
        "exit_code": exit_code,
        "duration_seconds": round(duration, 3),
        "execution_policy": {
            "timeout_seconds": timeout,
            "resource_budget": resource_budget,
            "stop_condition": stop_condition,
        },
        "termination": termination,
        "output_tail": _redact_output(output),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="审计 Vibe Mathing 单机生产闭环成熟度")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--output")
    args = parser.parse_args()
    results = [run_capability(*item) for item in CAPABILITIES]
    score = sum(item["weight"] for item in results if item["status"] == "PASS")
    maximum = sum(item["weight"] for item in results)
    payload = {
        "schema_version": "1.0.0",
        "scope": "single-host-single-agent-trusted-research-loop",
        "audited_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "score": score,
        "maximum": maximum,
        "readiness": f"{score}/{maximum}",
        "status": "PASS" if score == maximum else "FAIL",
        "capabilities": results,
        "excluded": [
            "distributed high availability",
            "external reviewer attestation issuance",
            "guaranteed solution of arbitrary open problems",
        ],
    }
    encoded = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    encoded_bytes = encoded.encode("utf-8")
    if len(encoded_bytes) > DEFAULT_OUTPUT_BYTES:
        raise RuntimeError("maturity report exceeds output budget")
    print(encoded, end="")
    if args.output:
        _write_report(Path(args.output), encoded_bytes)
    if args.strict and score != maximum:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
