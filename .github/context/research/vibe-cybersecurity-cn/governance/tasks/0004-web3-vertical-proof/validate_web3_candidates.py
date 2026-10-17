#!/usr/bin/env python3
"""校验 Web3/EVM 供应链候选目录并重建可读表。
运行：python3 governance/tasks/0004-web3-vertical-proof/validate_web3_candidates.py
依赖：Python 3.10+ 标准库，以及同目录 web3-supply-chain-candidates.json。
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parent
CATALOG_PATH = ROOT / "web3-supply-chain-candidates.json"
TABLE_PATH = ROOT / "WEB3_CANDIDATE_TABLE.md"

VALID_CATEGORIES = {
    "static-analysis",
    "fuzzing-property",
    "formal-verification",
    "toolchain-stdlib",
    "benchmarks-labs",
    "vulnerability-intel",
    "intelligence-standards",
}
VALID_DISPOSITIONS = {"mvp", "pilot", "reference", "hold"}
VALID_EFFECTS = {"none", "data-only", "passive", "active-low", "active-medium", "active-high"}
SCORE_KEYS = ("fit", "evidence", "safety", "operability", "maturity")


def fail(message: str) -> None:
    raise ValueError(message)


def valid_url(value: object) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)


def validate(catalog: dict[str, object]) -> list[dict[str, object]]:
    if catalog.get("schema_version") != "1.0.0":
        fail("schema_version 必须为 1.0.0")
    if not isinstance(catalog.get("snapshot_date"), str):
        fail("缺少 snapshot_date")
    if catalog.get("ecosystem") != "evm-solidity":
        fail("ecosystem 必须为 evm-solidity")

    candidates = catalog.get("candidates")
    if not isinstance(candidates, list) or not candidates:
        fail("candidates 必须是非空数组")

    seen: set[str] = set()
    for index, candidate in enumerate(candidates):
        prefix = f"candidates[{index}]"
        if not isinstance(candidate, dict):
            fail(f"{prefix} 必须是对象")

        candidate_id = candidate.get("id")
        if not isinstance(candidate_id, str) or not candidate_id:
            fail(f"{prefix}.id 缺失")
        if candidate_id in seen:
            fail(f"重复 id: {candidate_id}")
        seen.add(candidate_id)

        if candidate.get("category") not in VALID_CATEGORIES:
            fail(f"{candidate_id}: category 非法")
        if candidate.get("disposition") not in VALID_DISPOSITIONS:
            fail(f"{candidate_id}: disposition 非法")
        if candidate.get("network_effect") not in VALID_EFFECTS:
            fail(f"{candidate_id}: network_effect 非法")
        if not valid_url(candidate.get("upstream_url")):
            fail(f"{candidate_id}: upstream_url 必须是 HTTPS")

        source_urls = candidate.get("fact_sources")
        if not isinstance(source_urls, list) or not source_urls:
            fail(f"{candidate_id}: 至少需要一个 fact_sources")
        if not all(valid_url(url) for url in source_urls):
            fail(f"{candidate_id}: fact_sources 必须全部是 HTTPS")

        for field in ("name", "license", "role", "rationale", "evidence_ceiling", "isolation"):
            if not isinstance(candidate.get(field), str) or not candidate[field].strip():
                fail(f"{candidate_id}: {field} 不能为空")

        for field in ("interfaces", "machine_outputs", "supply_chain_controls", "blockers"):
            if not isinstance(candidate.get(field), list):
                fail(f"{candidate_id}: {field} 必须是数组")

        scores = candidate.get("scores")
        if not isinstance(scores, dict) or set(scores) != set(SCORE_KEYS):
            fail(f"{candidate_id}: scores 字段不完整")
        for score_name, value in scores.items():
            if not isinstance(value, int) or not 0 <= value <= 5:
                fail(f"{candidate_id}: scores.{score_name} 必须为 0..5 整数")

        if candidate["disposition"] == "mvp" and candidate["network_effect"] == "active-high":
            fail(f"{candidate_id}: active-high 不得直接进入 mvp")
        if candidate["disposition"] in {"mvp", "pilot"} and not candidate["machine_outputs"]:
            fail(f"{candidate_id}: mvp/pilot 必须有机器输出")
        if candidate["network_effect"].startswith("active") and candidate["isolation"] == "none":
            fail(f"{candidate_id}: 主动工具必须声明隔离")

    return candidates


def total_score(candidate: dict[str, object]) -> int:
    scores = candidate["scores"]
    assert isinstance(scores, dict)
    return sum(int(scores[key]) for key in SCORE_KEYS)


def render(catalog: dict[str, object], candidates: list[dict[str, object]]) -> str:
    sorted_candidates = sorted(
        candidates,
        key=lambda item: (
            {"mvp": 0, "pilot": 1, "reference": 2, "hold": 3}[str(item["disposition"])],
            -total_score(item),
            str(item["name"]).lower(),
        ),
    )
    lines = [
        "# Web3/EVM 供应链候选表",
        "",
        f"检索截面：`{catalog['snapshot_date']}`。本表由 `web3-supply-chain-candidates.json` 生成，请勿手工编辑。",
        "",
        "评分是本项目的选型判断，不是上游官方声明，也不代表已完成本地能力验证。",
        "",
        "| 状态 | 候选 | 类别 | 角色 | 接口 / 输出 | 网络副作用 | 许可 | 分数 | 主要门禁 |",
        "|---|---|---|---|---|---|---|---:|---|",
    ]
    for candidate in sorted_candidates:
        interfaces = ", ".join(str(value) for value in candidate["interfaces"]) or "-"
        outputs = ", ".join(str(value) for value in candidate["machine_outputs"]) or "-"
        blockers = "；".join(str(value) for value in candidate["blockers"]) or "无"
        lines.append(
            "| {disposition} | [{name}]({url}) | {category} | {role} | {interfaces} / {outputs} | "
            "{effect} | {license} | {score}/25 | {blockers} |".format(
                disposition=candidate["disposition"],
                name=str(candidate["name"]).replace("|", "\\|"),
                url=candidate["upstream_url"],
                category=candidate["category"],
                role=str(candidate["role"]).replace("|", "\\|"),
                interfaces=interfaces.replace("|", "\\|"),
                outputs=outputs.replace("|", "\\|"),
                effect=candidate["network_effect"],
                license=str(candidate["license"]).replace("|", "\\|"),
                score=total_score(candidate),
                blockers=blockers.replace("|", "\\|"),
            )
        )

    disposition_counts = Counter(str(candidate["disposition"]) for candidate in candidates)
    category_counts = Counter(str(candidate["category"]) for candidate in candidates)
    lines.extend(
        [
            "",
            "## 汇总",
            "",
            f"- 总候选：{len(candidates)}",
            "- 状态：" + "，".join(f"{key}={disposition_counts[key]}" for key in ("mvp", "pilot", "reference", "hold")),
            "- 类别：" + "，".join(f"{key}={category_counts[key]}" for key in sorted(category_counts)),
            "",
            "## 状态语义",
            "",
            "- `mvp`：允许进入本地隔离纵向样例；仍需固定版本和真实复跑。",
            "- `pilot`：价值明确，但部署、许可、动作风险或运维成本需要先校准。",
            "- `reference`：仅用于架构、方法、数据或评测研究，不进入默认执行工具面。",
            "- `hold`：当前阻塞未闭合，不进入实施计划。",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    try:
        catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
        if not isinstance(catalog, dict):
            fail("catalog 顶层必须是对象")
        candidates = validate(catalog)
        rendered = render(catalog, candidates)
        TABLE_PATH.write_text(rendered, encoding="utf-8")
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"BLOCK: {exc}", file=sys.stderr)
        return 1

    print(f"PASS: {len(candidates)} candidates validated; rebuilt {TABLE_PATH.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
