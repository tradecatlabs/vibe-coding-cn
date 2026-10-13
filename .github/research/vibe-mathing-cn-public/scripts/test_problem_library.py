#!/usr/bin/env python3
# 从原始快照重算关键事实，防止解析容器和第三方源 ID 主键假设回归。
# 运行：python3 scripts/test_problem_library.py
# 依赖：Python 3、beautifulsoup4、lxml 与已完成抓取的问题库；不访问网络。

from __future__ import annotations

import importlib.util
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FETCHER_PATH = ROOT / "scripts" / "fetch_problem_library.py"
LIBRARY = ROOT / "problem-library"
MANIFEST_PATH = LIBRARY / "manifest.json"
RECORDS_PATH = LIBRARY / "records" / "problems.jsonl"
WIKIPEDIA_RAW_PATH = LIBRARY / "raw" / "wikipedia" / "list-of-unsolved-problems.json"


def load_fetcher_module() -> Any:
    spec = importlib.util.spec_from_file_location("fetch_problem_library", FETCHER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"无法加载抓取器：{FETCHER_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_records() -> list[dict[str, Any]]:
    with RECORDS_PATH.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def main() -> int:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    raw_wikipedia = json.loads(WIKIPEDIA_RAW_PATH.read_text(encoding="utf-8"))
    fetcher = load_fetcher_module()
    wikipedia_records, wikipedia_metadata = fetcher.parse_wikipedia(
        raw_wikipedia,
        retrieved_at=raw_wikipedia["retrieved_at"],
    )
    expected_wikipedia = manifest["sources"]["wikipedia"]
    assert wikipedia_metadata["record_count"] == expected_wikipedia["record_count"]
    assert wikipedia_metadata["status_counts"] == expected_wikipedia["status_counts"]
    assert any(record["categories"] == ["Algebra"] for record in wikipedia_records)
    assert any(record["categories"][:1] == ["Uncategorised"] for record in wikipedia_records)

    records = load_records()
    assert len(records) == manifest["record_count"]
    assert len({record["id"] for record in records}) == len(records)
    unsolvedmath_records = [record for record in records if record["source"] == "unsolvedmath"]
    assert len(unsolvedmath_records) == manifest["sources"]["unsolvedmath"]["expected_record_count"]

    by_native_id: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in unsolvedmath_records:
        by_native_id[record["source_native_id"]].append(record)
    conflicts = {native_id: items for native_id, items in by_native_id.items() if len(items) > 1}
    reported = manifest["sources"]["unsolvedmath"]["identity_anomalies"]
    assert set(conflicts) == set(reported["conflicts"])
    assert len(conflicts) == reported["conflicting_native_id_count"]
    assert sum(len(items) - 1 for items in conflicts.values()) == reported["excess_rows_over_distinct_native_ids"]
    assert "COMB-001" in conflicts
    assert len({record["title"] for record in conflicts["COMB-001"]}) > 1

    print(
        "问题库回归测试通过："
        f"Wikipedia 原始快照重算 {len(wikipedia_records)} 条；"
        f"统一记录 {len(records)} 条；"
        f"UnsolvedMath 冲突源 ID {len(conflicts)} 组。"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, OSError, RuntimeError, KeyError, json.JSONDecodeError) as exc:
        print(f"ERROR: 问题库回归测试失败：{exc}", file=sys.stderr)
        raise SystemExit(1) from exc
