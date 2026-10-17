#!/usr/bin/env python3
# 做什么：验证研究存储的幂等、并发、append-only 与 WAL 崩溃恢复。
# 怎么运行：python3 scripts/test_research_store.py
# 需要什么：Python 3、Linux fcntl；只写隔离临时目录。

from __future__ import annotations

import json
import multiprocessing
import shutil
import tempfile
from pathlib import Path

from vibe_mathing.store import ResearchStore, StoreError


ROOT = Path(__file__).resolve().parents[1]
NOW = "2026-08-13T00:00:00Z"


def prepare(base: Path) -> None:
    for relative in (
        "problem-library/schema/canonical-problem.schema.json",
        "research/schema/attempt.schema.json",
        "result-library/schema/result.schema.json",
    ):
        target = base / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / relative, target)


def problem(identifier: str) -> dict[str, object]:
    return {
        "schema_version": "1.0.0",
        "problem_id": f"problem:{identifier}",
        "title": identifier,
        "aliases": [],
        "statement": {"text": "测试问题", "language": "zh-CN", "version": 1},
        "domain": {"description": "纯合成测试对象", "objects": ["synthetic object"]},
        "quantifiers": [{"kind": "decide", "variables": [], "domain": "synthetic domain"}],
        "definitions": [],
        "assumptions": [],
        "allowed_axioms": [],
        "msc": [],
        "sources": [{"source": "fixture", "source_record_id": None, "url": "https://example.com/test", "retrieved_at": NOW}],
        "acceptance": {"policy": "solution-admission-v1"},
        "constraints": {
            "allowed_methods": ["computation"],
            "allowed_adapters": ["synthetic-test-v1"],
            "max_attempts": 1,
            "runtime": {
                "max_transitions": 16,
                "max_retries": 2,
                "timeout_seconds": 30,
                "max_output_bytes": 1_048_576,
                "memory_budget_mb": 256,
                "threads_max": 1,
            },
        },
        "lifecycle": "active",
        "created_at": NOW,
        "updated_at": NOW,
    }


def concurrent_write(root: str, identifier: str) -> None:
    ResearchStore(Path(root)).upsert("problems", problem(identifier))


def attempt(identifier: str, problem_id: str, method: str = "computation") -> dict[str, object]:
    return {
        "attempt_id": f"attempt:{identifier}",
        "problem_id": problem_id,
        "generator": "candidate-generator",
        "objective": "纯合成 lifecycle 测试",
        "method": method,
        "lifecycle": "completed",
        "started_at": NOW,
        "completed_at": NOW,
        "inputs": [],
        "claims": [],
        "artifacts": [],
    }


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="vibe-mathing-store-") as temporary:
        base = Path(temporary)
        prepare(base)
        store = ResearchStore(base)
        assert store.upsert("problems", problem("same")) is True
        assert store.upsert("problems", problem("same")) is False
        changed = problem("same")
        changed["title"] = "禁止覆盖"
        try:
            store.upsert("problems", changed)
        except StoreError:
            pass
        else:
            raise AssertionError("相同 ID 不同内容必须拒绝")

        workers = [
            multiprocessing.Process(target=concurrent_write, args=(temporary, f"p{index}"))
            for index in range(8)
        ]
        for worker in workers:
            worker.start()
        for worker in workers:
            worker.join(10)
            assert worker.exitcode == 0
        assert len(store.read("problems")) == 9

        try:
            store.commit(
                {
                    "problems": store.read("problems") + [problem("wal")],
                    "attempts": [],
                },
                fail_after_replace=1,
            )
        except StoreError as exc:
            assert "故障注入" in str(exc)
        else:
            raise AssertionError("故障注入必须中断")
        ResearchStore(base).recover()
        assert any(item["problem_id"] == "problem:wal" for item in store.read("problems"))
        assert not store.journal_path.exists()

        encoded = (base / "problem-library/records/canonical-problems.jsonl").read_text(encoding="utf-8")
        assert all(json.loads(line) for line in encoded.splitlines())

        dangling_attempt = {
            "attempt_id": "attempt:dangling",
            "problem_id": "problem:missing",
            "generator": "candidate-generator",
            "objective": "必须被完整性门拒绝",
            "method": "computation",
            "lifecycle": "completed",
            "started_at": NOW,
            "completed_at": NOW,
            "inputs": [],
            "claims": [],
            "artifacts": [],
        }
        try:
            store.upsert("attempts", dangling_attempt)
        except StoreError as exc:
            assert "跨记录完整性失败" in str(exc)
        else:
            raise AssertionError("唯一 writer 不得写入断链 Attempt")

    with tempfile.TemporaryDirectory(prefix="vibe-mathing-contract-lifecycle-") as temporary:
        base = Path(temporary)
        prepare(base)
        store = ResearchStore(base)
        draft = problem("lifecycle")
        draft["lifecycle"] = "draft"
        draft["constraints"]["max_attempts"] = 2
        store.upsert("problems", draft)
        first = attempt("lifecycle-first", draft["problem_id"])
        try:
            store.upsert("attempts", first)
        except StoreError as exc:
            assert "只有 active ProblemContract" in str(exc)
        else:
            raise AssertionError("draft ProblemContract 不得创建 Attempt")

        active = {**draft, "lifecycle": "active", "updated_at": "2026-08-14T00:00:01Z"}
        store.replace_problem(active)
        assert store.upsert("attempts", first) is True

        withdrawn = {
            **active,
            "lifecycle": "withdrawn",
            "updated_at": "2026-08-14T00:00:02Z",
        }
        store.replace_problem(withdrawn)
        assert store.read("attempts") == [first], "withdrawn 必须保留历史 Attempt"
        try:
            store.upsert("attempts", attempt("lifecycle-second", draft["problem_id"]))
        except StoreError as exc:
            assert "只有 active ProblemContract" in str(exc)
        else:
            raise AssertionError("withdrawn ProblemContract 不得创建新 Attempt")
        try:
            store.replace_problem(
                {**withdrawn, "lifecycle": "active", "updated_at": "2026-08-14T00:00:03Z"}
            )
        except StoreError as exc:
            assert "单向转换" in str(exc)
        else:
            raise AssertionError("withdrawn ProblemContract 不得重新激活")

    print("研究存储测试通过：幂等、并发唯一写入与 WAL 崩溃恢复均成立。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
