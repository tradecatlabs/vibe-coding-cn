#!/usr/bin/env python3
# 做什么：从 CLI 验证 SymPy Problem→Attempt→Result→Solution、恢复、幂等与失效闭环。
# 怎么运行：python3 scripts/test_vibe_mathing_pipeline.py
# 需要什么：Python 3、SymPy；所有状态写入隔离临时项目。

from __future__ import annotations

import json
import multiprocessing
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from vibe_mathing.pipeline import EXPECTED_STATEMENT, invalidate_sympy_result
from vibe_mathing.runtime import stable_run_id
from vibe_mathing.store import ResearchStore


ROOT = Path(__file__).resolve().parents[1]
NOW = "2026-08-13T00:00:00Z"


def prepare(base: Path) -> None:
    for relative in (
        "problem-library/schema/canonical-problem.schema.json",
        "research/schema/attempt.schema.json",
        "result-library/schema/result.schema.json",
        "research/verifiers.json",
        "research/schema/verifier-registry.schema.json",
        "research/schema/evidence-receipt.schema.json",
        "research/schema/run-state.schema.json",
    ):
        target = base / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / relative, target)
    (base / "result-library/indexes").mkdir(parents=True)
    (base / "result-library/indexes/solutions.json").write_text(
        json.dumps({"schema_version": "2.0.0", "generated_at": NOW, "result_ids": []}),
        encoding="utf-8",
    )


def invoke(base: Path, *arguments: str, expect: int = 0) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        [sys.executable, str(ROOT / "scripts/vibe_mathing_cli.py"), "--project-root", str(base), *arguments],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert completed.returncode == expect, completed.stderr
    return completed


def concurrent_run(base: str, problem_id: str, queue: multiprocessing.Queue[int]) -> None:
    completed = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/vibe_mathing_cli.py"),
            "--project-root",
            base,
            "run",
            "--problem-id",
            problem_id,
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    queue.put(completed.returncode)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="vibe-mathing-problem-lifecycle-") as temporary:
        base = Path(temporary)
        prepare(base)
        problem_id = "problem:sympy-counterexample-fixture"
        draft_file = base / "draft-problem.json"
        draft = json.loads(
            (ROOT / "fixtures/sympy-counterexample/problem.json").read_text(
                encoding="utf-8"
            )
        )
        draft["lifecycle"] = "draft"
        draft_file.write_text(json.dumps(draft), encoding="utf-8")
        invoke(base, "register-problem", "--file", str(draft_file))
        assert "lifecycle=active" in invoke(
            base, "run", "--problem-id", problem_id, expect=1
        ).stderr
        activated = json.loads(
            invoke(
                base,
                "set-problem-lifecycle",
                "--problem-id",
                problem_id,
                "--lifecycle",
                "active",
            ).stdout
        )
        assert activated == {"problem_id": problem_id, "lifecycle": "active"}
        withdrawn = json.loads(
            invoke(
                base,
                "set-problem-lifecycle",
                "--problem-id",
                problem_id,
                "--lifecycle",
                "withdrawn",
            ).stdout
        )
        assert withdrawn == {"problem_id": problem_id, "lifecycle": "withdrawn"}
        assert "单向转换" in invoke(
            base,
            "set-problem-lifecycle",
            "--problem-id",
            problem_id,
            "--lifecycle",
            "active",
            expect=2,
        ).stderr

    with tempfile.TemporaryDirectory(prefix="vibe-mathing-pipeline-") as temporary:
        base = Path(temporary)
        prepare(base)
        store = ResearchStore(base)
        problem_id = "problem:sympy-counterexample-fixture"
        problem_file = base / "fixture-problem.json"
        shutil.copy2(ROOT / "fixtures/sympy-counterexample/problem.json", problem_file)
        registered = json.loads(
            invoke(base, "register-problem", "--file", str(problem_file)).stdout
        )
        assert registered == {"problem_id": problem_id, "created": True}
        assert json.loads(
            invoke(base, "register-problem", "--file", str(problem_file)).stdout
        )["created"] is False
        interrupted = invoke(
            base,
            "run",
            "--problem-id",
            problem_id,
            "--fail-after",
            "candidate_ready",
            expect=1,
        )
        assert "candidate_ready" in interrupted.stderr
        run_id = stable_run_id(problem_id, "sympy-counterexample-v1")
        resumed = json.loads(invoke(base, "resume", "--run-id", run_id).stdout)
        assert resumed["status"] == "accepted"
        assert json.loads(invoke(base, "status", "--run-id", run_id).stdout)["status"] == "accepted"
        invoke(base, "verify", "--run-id", run_id)
        assert len(store.read("attempts")) == 1
        assert len(store.read("results")) == 1

        rerun = json.loads(invoke(base, "run", "--problem-id", problem_id).stdout)
        assert rerun["status"] == "accepted"
        assert len(store.read("attempts")) == 1 and len(store.read("results")) == 1
        result_id = f"result:{run_id.removeprefix('run:')}"
        assert result_id in store.rebuild_solution_view()
        assert result_id not in invalidate_sympy_result(base, run_id)
        assert result_id not in invalidate_sympy_result(base, run_id)
        invalidated_rerun = invoke(
            base, "run", "--problem-id", problem_id, expect=1
        )
        assert "当前 Result 已失效" in invalidated_rerun.stderr

    with tempfile.TemporaryDirectory(prefix="vibe-mathing-result-resume-") as temporary:
        base = Path(temporary)
        prepare(base)
        store = ResearchStore(base)
        problem_id = "problem:sympy-counterexample-fixture"
        store.upsert(
            "problems",
            {
                "schema_version": "1.0.0",
                "problem_id": problem_id,
                "title": "确定性反例 fixture",
                "aliases": [],
                "statement": {"text": EXPECTED_STATEMENT, "language": "zh-CN", "version": 1},
                "domain": {"description": "实数上的一元全称不等式", "objects": ["real number"]},
                "quantifiers": [{"kind": "forall", "variables": ["x"], "domain": "x ∈ ℝ"}],
                "definitions": [],
                "assumptions": [],
                "allowed_axioms": ["ordered-field"],
                "msc": [],
                "sources": [{"source": "fixture", "source_record_id": None, "url": "https://example.com/sympy-fixture", "retrieved_at": NOW}],
                "acceptance": {"policy": "solution-admission-v1"},
                "constraints": {
                    "allowed_methods": ["computation"],
                    "allowed_adapters": ["sympy-counterexample-v1"],
                    "max_attempts": 1,
                    "runtime": {"max_transitions": 16, "max_retries": 2, "timeout_seconds": 30, "max_output_bytes": 1_048_576, "memory_budget_mb": 256, "threads_max": 1},
                },
                "lifecycle": "active",
                "created_at": NOW,
                "updated_at": NOW,
            },
        )
        interrupted = invoke(
            base,
            "run",
            "--problem-id",
            problem_id,
            "--fail-after",
            "result_written",
            expect=1,
        )
        assert "result_written" in interrupted.stderr
        run_id = stable_run_id(problem_id, "sympy-counterexample-v1")
        resumed = json.loads(invoke(base, "resume", "--run-id", run_id).stdout)
        assert resumed["status"] == "accepted"
        assert len(store.read("attempts")) == 1 and len(store.read("results")) == 1

    with tempfile.TemporaryDirectory(prefix="vibe-mathing-concurrent-run-") as temporary:
        base = Path(temporary)
        prepare(base)
        store = ResearchStore(base)
        problem_id = "problem:sympy-counterexample-fixture"
        store.upsert(
            "problems",
            {
                "schema_version": "1.0.0",
                "problem_id": problem_id,
                "title": "确定性反例 fixture",
                "aliases": [],
                "statement": {"text": EXPECTED_STATEMENT, "language": "zh-CN", "version": 1},
                "domain": {"description": "实数上的一元全称不等式", "objects": ["real number"]},
                "quantifiers": [{"kind": "forall", "variables": ["x"], "domain": "x ∈ ℝ"}],
                "definitions": [],
                "assumptions": [],
                "allowed_axioms": ["ordered-field"],
                "msc": [],
                "sources": [{"source": "fixture", "source_record_id": None, "url": "https://example.com/sympy-fixture", "retrieved_at": NOW}],
                "acceptance": {"policy": "solution-admission-v1"},
                "constraints": {
                    "allowed_methods": ["computation"],
                    "allowed_adapters": ["sympy-counterexample-v1"],
                    "max_attempts": 1,
                    "runtime": {"max_transitions": 16, "max_retries": 2, "timeout_seconds": 30, "max_output_bytes": 1_048_576, "memory_budget_mb": 256, "threads_max": 1},
                },
                "lifecycle": "active",
                "created_at": NOW,
                "updated_at": NOW,
            },
        )
        queue: multiprocessing.Queue[int] = multiprocessing.Queue()
        workers = [
            multiprocessing.Process(target=concurrent_run, args=(temporary, problem_id, queue))
            for _ in range(4)
        ]
        for worker in workers:
            worker.start()
        for worker in workers:
            worker.join(20)
            assert worker.exitcode == 0
        assert [queue.get(timeout=2) for _ in workers] == [0, 0, 0, 0]
        assert len(store.read("attempts")) == 1 and len(store.read("results")) == 1

    print("SymPy 垂直闭环测试通过：CLI 恢复、幂等、准入与 append-only 失效均成立。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
