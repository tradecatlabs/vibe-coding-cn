#!/usr/bin/env python3
"""校验 Web3 工具链准入目录并重建可读表。
运行：python3 governance/tasks/0005-admit-web3-toolchain/validate_web3_admission.py
依赖：Python 3.10+ 标准库、同目录准入目录和 0004 Web3 研究目录。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
ADMISSION_PATH = ROOT / "web3-admission-candidates.json"
TABLE_PATH = ROOT / "ADMISSION_TABLE.md"
SOURCE_CATALOG = (
    ROOT.parent / "0004-web3-vertical-proof" / "web3-supply-chain-candidates.json"
).resolve()

EXPECTED_SOURCE_CATALOG = "../0004-web3-vertical-proof/web3-supply-chain-candidates.json"
CHECK_KEYS = {
    "research_source",
    "license_review",
    "immutable_pin",
    "integrity_verification",
    "security_review",
    "interface_contract",
    "isolation_policy",
    "behavior_test",
    "rollback_test",
}
ALLOWED_STATES = {"admission-candidate", "pinned", "verified", "admitted", "suspended", "retired"}
VALID_CLASSES = {"executable", "library", "schema", "data", "rules", "container"}


def fail(message: str) -> None:
    raise ValueError(message)


def main() -> int:
    try:
        admission = json.loads(ADMISSION_PATH.read_text(encoding="utf-8"))
        source = json.loads(SOURCE_CATALOG.read_text(encoding="utf-8"))
        if admission.get("schema_version") != "1.0.0":
            fail("schema_version 必须为 1.0.0")
        if admission.get("source_catalog") != EXPECTED_SOURCE_CATALOG:
            fail("source_catalog 必须指向固定的 0004 Web3 研究目录")

        source_by_id = {item["id"]: item for item in source["candidates"]}
        seen: set[str] = set()
        admitted = 0

        for index, item in enumerate(admission["candidates"]):
            prefix = f"candidates[{index}]"
            source_id = item.get("source_id")
            if not isinstance(source_id, str) or source_id not in source_by_id:
                fail(f"{prefix}.source_id 不在 0004 研究目录")
            if source_id in seen:
                fail(f"重复 source_id: {source_id}")
            seen.add(source_id)
            source_item = source_by_id[source_id]
            if source_item.get("disposition") not in {"mvp", "pilot"}:
                fail(f"{source_id}: 只有 mvp/pilot 研究候选可进入 Web3 准入")
            if not isinstance(item.get("order"), int) or item["order"] < 0:
                fail(f"{source_id}: order 必须是唯一非负整数")
            if item.get("artifact_class") not in VALID_CLASSES:
                fail(f"{source_id}: artifact_class 非法")
            if item.get("admission_state") not in ALLOWED_STATES:
                fail(f"{source_id}: admission_state 非法")

            checks = item.get("checks")
            if not isinstance(checks, dict) or set(checks) != CHECK_KEYS:
                fail(f"{source_id}: checks 必须恰好覆盖 9 项门禁")
            for key, value in checks.items():
                if value not in {"pass", "pending", "fail", "n-a"}:
                    fail(f"{source_id}: checks.{key} 非法")

            if item["admission_state"] == "admitted":
                admitted += 1
                if item.get("default_enabled") is not True:
                    fail(f"{source_id}: admitted 必须 default_enabled=true")
                for key in CHECK_KEYS:
                    if checks[key] != "pass":
                        fail(f"{source_id}: admitted 但门禁 {key} 未 pass")
                pin = item.get("pin") or {}
                if not pin.get("ref") or pin.get("status") != "pinned":
                    fail(f"{source_id}: admitted 必须已 pinned（含 ref）")
                if item.get("blocking_conditions"):
                    fail(f"{source_id}: admitted 但存在 blocking_conditions")

        lines = [
            "# Web3 工具链准入表",
            "",
            f"快照：`{admission['snapshot_date']}`。本表由 `web3-admission-candidates.json` 生成，禁止手工修改。",
            "",
            "`admitted` 表示已完成 9 项门禁（含 research_source）并固定版本；运行权仍由 ScopeGrant 和运行时策略决定。",
            "",
            "| 状态 | 工具 | 角色 | 固定版本 | 门禁 | 行为证据 |",
            "|---|---|---|---|---|---|",
        ]
        for item in sorted(admission["candidates"], key=lambda x: x["order"]):
            name = source_by_id[item["source_id"]]["name"]
            checks = item["checks"]
            passed = sum(1 for v in checks.values() if v == "pass")
            behavior = checks.get("behavior_test")
            behavior_evidence = item["evidence_refs"].get("behavior_test", "-")
            lines.append(
                f"| {item['admission_state']} | {name} | {item['planned_role']} | "
                f"{item['pin']['ref']} | {passed}/9 | {behavior_evidence} |"
            )
        lines.extend(
            [
                "",
                "## 汇总",
                "",
                f"- 准入候选：{len(admission['candidates'])}",
                f"- 已正式纳入（admitted）：{admitted}",
                "",
                "## 门禁含义",
                "",
                "research_source / license_review / immutable_pin / integrity_verification / "
                "security_review / interface_contract / isolation_policy / behavior_test / rollback_test：",
                "9 项全部 pass 才允许 admitted。",
                "",
            ]
        )
        TABLE_PATH.write_text("\n".join(lines), encoding="utf-8")
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"BLOCK: {exc}", file=sys.stderr)
        return 1

    print(f"PASS: {admitted} admitted / {len(admission['candidates'])} candidates; rebuilt {TABLE_PATH.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
