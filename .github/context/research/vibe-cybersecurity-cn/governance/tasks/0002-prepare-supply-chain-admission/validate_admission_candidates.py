#!/usr/bin/env python3
"""校验供应链准入候选并生成可读表。
运行：python3 governance/tasks/0002-prepare-supply-chain-admission/validate_admission_candidates.py
依赖：Python 3.10+ 标准库、同目录准入目录和 0001 研究目录。
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
ADMISSION_PATH = ROOT / "admission-candidates.json"
TABLE_PATH = ROOT / "ADMISSION_CANDIDATE_TABLE.md"
VALID_CLASSES = {"container", "data", "executable", "rules", "schema"}
VALID_STATES = {"admission-candidate", "pinned", "verified", "admitted", "suspended", "retired"}
VALID_CHECKS = {"pass", "pending", "block", "not-applicable"}
REQUIRED_CHECK_KEYS = (
    "research_source", "license_review", "immutable_pin",
    "integrity_verification", "security_review", "interface_contract",
    "isolation_policy", "behavior_test", "rollback_test",
)
EXPECTED_SOURCE_CATALOG = "../0001-survey-cybersecurity-supply-chain/supply-chain-candidates.json"
PROFILE_EFFECTS = {
    "schema-data": {"data-only"},
    "local-readonly": {"none"},
    "lab-active": {"data-only", "active-low", "active-medium"},
    "authorized-passive": {"passive"},
    "authorized-active": {"active-low", "active-medium"},
}
SAFE_RELATIVE_REF = re.compile(r"^(?!/)(?!.*(?:^|/)\.\.(?:/|$)).+\S$")
SHA256_DIGEST = re.compile(r"^sha256:[a-f0-9]{64}$")


def fail(message: str) -> None:
    raise ValueError(message)


def load_json(path: Path) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        fail(f"{path.name}: 顶层必须是对象")
    return payload


def validate() -> tuple[dict[str, object], list[dict[str, object]], dict[str, dict[str, object]]]:
    admission = load_json(ADMISSION_PATH)
    if admission.get("schema_version") != "1.0.0":
        fail("schema_version 必须为 1.0.0")
    if admission.get("source_catalog") != EXPECTED_SOURCE_CATALOG:
        fail("source_catalog 必须指向固定的 0001 研究目录")
    source_path = (ADMISSION_PATH.parent / EXPECTED_SOURCE_CATALOG).resolve()
    source = load_json(source_path)
    if admission.get("source_snapshot_date") != source.get("snapshot_date"):
        fail("source_snapshot_date 与研究目录不一致")

    source_candidates = source.get("candidates")
    if not isinstance(source_candidates, list):
        fail("研究目录 candidates 非法")
    source_by_id = {
        str(item["id"]): item for item in source_candidates if isinstance(item, dict)
    }

    check_keys = admission.get("check_keys")
    profiles = admission.get("profiles")
    waves = admission.get("waves")
    candidates = admission.get("candidates")
    if check_keys != list(REQUIRED_CHECK_KEYS):
        fail("check_keys 必须与校验器固定八门禁完全一致")
    if not isinstance(profiles, dict) or not profiles:
        fail("profiles 必须是非空对象")
    if not isinstance(waves, dict) or not waves:
        fail("waves 必须是非空对象")
    if not isinstance(candidates, list) or not candidates:
        fail("candidates 必须是非空数组")

    seen: set[str] = set()
    orders: set[int] = set()
    for index, item in enumerate(candidates):
        if not isinstance(item, dict):
            fail(f"candidates[{index}] 必须是对象")
        source_id = item.get("source_id")
        if not isinstance(source_id, str) or source_id not in source_by_id:
            fail(f"candidates[{index}].source_id 不在研究目录")
        if source_id in seen:
            fail(f"重复 source_id: {source_id}")
        seen.add(source_id)
        source_item = source_by_id[source_id]
        if source_item.get("disposition") != "mvp":
            fail(f"{source_id}: 只有研究状态 mvp 可进入准入候选")
        if source_item.get("network_effect") == "active-high":
            fail(f"{source_id}: active-high 不得进入当前准入候选")

        order = item.get("order")
        if not isinstance(order, int) or order < 0 or order in orders:
            fail(f"{source_id}: order 必须是唯一非负整数")
        orders.add(order)
        if item.get("wave") not in waves:
            fail(f"{source_id}: wave 未定义")
        if item.get("artifact_class") not in VALID_CLASSES:
            fail(f"{source_id}: artifact_class 非法")
        if item.get("profile") not in profiles:
            fail(f"{source_id}: profile 未定义")
        network_effect = str(source_item.get("network_effect"))
        if network_effect not in PROFILE_EFFECTS.get(str(item.get("profile")), set()):
            fail(f"{source_id}: profile 与 network_effect 不匹配")
        if item.get("admission_state") not in VALID_STATES:
            fail(f"{source_id}: admission_state 非法")
        if item.get("default_enabled") is not False:
            fail(f"{source_id}: 候选阶段必须 default_enabled=false")
        for field in ("planned_role", "owner_role"):
            if not isinstance(item.get(field), str) or not item[field].strip():
                fail(f"{source_id}: {field} 不能为空")

        pin = item.get("pin")
        if not isinstance(pin, dict) or set(pin) != {"ref", "digest", "status"}:
            fail(f"{source_id}: pin 字段不完整")
        if pin.get("status") not in {"pending", "verified"}:
            fail(f"{source_id}: pin.status 非法")
        if pin.get("status") == "verified" and (not pin.get("ref") or not pin.get("digest")):
            fail(f"{source_id}: verified pin 必须有 ref 和 digest")
        if pin.get("status") == "verified" and not SHA256_DIGEST.fullmatch(str(pin.get("digest"))):
            fail(f"{source_id}: verified pin.digest 必须是 sha256")

        checks = item.get("checks")
        if not isinstance(checks, dict) or set(checks) != set(check_keys):
            fail(f"{source_id}: checks 与 check_keys 不一致")
        if any(value not in VALID_CHECKS for value in checks.values()):
            fail(f"{source_id}: checks 状态非法")
        if checks.get("research_source") != "pass":
            fail(f"{source_id}: research_source 必须通过")
        evidence_refs = item.get("evidence_refs")
        if not isinstance(evidence_refs, dict) or not set(evidence_refs).issubset(
            set(REQUIRED_CHECK_KEYS) - {"research_source"}
        ):
            fail(f"{source_id}: evidence_refs 字段非法")
        for check_name in REQUIRED_CHECK_KEYS[1:]:
            refs = evidence_refs.get(check_name, [])
            if not isinstance(refs, list) or not all(
                isinstance(ref, str) and SAFE_RELATIVE_REF.fullmatch(ref) for ref in refs
            ):
                fail(f"{source_id}: evidence_refs.{check_name} 必须是安全相对引用数组")
            if checks[check_name] == "pass" and not refs:
                fail(f"{source_id}: {check_name}=pass 必须绑定 evidence_refs")
        if item["admission_state"] == "admitted":
            if pin.get("status") != "verified" or any(value != "pass" for value in checks.values()):
                fail(f"{source_id}: 未完成全部门禁不得 admitted")
        for field in ("extra_gates", "blocking_conditions"):
            values = item.get(field)
            if not isinstance(values, list) or not values or not all(
                isinstance(value, str) and value.strip() for value in values
            ):
                fail(f"{source_id}: {field} 必须是非空字符串数组")

    research_mvp_ids = {
        str(item["id"]) for item in source_candidates
        if isinstance(item, dict) and item.get("disposition") == "mvp"
    }
    if seen != research_mvp_ids:
        missing = sorted(research_mvp_ids - seen)
        extra = sorted(seen - research_mvp_ids)
        fail(f"准入候选必须完整覆盖研究 MVP；missing={missing}, extra={extra}")
    return admission, candidates, source_by_id


def render(
    admission: dict[str, object],
    candidates: list[dict[str, object]],
    source_by_id: dict[str, dict[str, object]],
) -> str:
    check_keys = list(admission["check_keys"])
    sorted_items = sorted(candidates, key=lambda item: int(item["order"]))
    lines = [
        "# 网络安全供应链准入候选表",
        "",
        f"快照：`{admission['snapshot_date']}`。本表由 `admission-candidates.json` 与 0001 研究目录联合生成，禁止手工修改。",
        "",
        "`准入候选` 不等于已安装、已纳入或已启用。当前所有候选默认禁用；版本、摘要和门禁未闭合前不得进入执行面。",
        "",
        "| 波次 | 候选 | 类型 | 计划职责 | 风险配置 | 网络副作用 | 门禁 | 固定版本 | 状态 | 主要阻塞 |",
        "|---|---|---|---|---|---|---:|---|---|---|",
    ]
    for item in sorted_items:
        source = source_by_id[str(item["source_id"])]
        checks = item["checks"]
        passed = sum(1 for key in check_keys if key != "research_source" and checks[key] == "pass")
        required = len(check_keys) - 1
        pin = item["pin"]
        pin_text = str(pin["ref"]) if pin["status"] == "verified" else "待固定"
        blockers = "；".join(str(value) for value in item["blocking_conditions"])
        lines.append(
            "| {wave} | [{name}]({url}) | {artifact_class} | {role} | {profile} | {effect} | "
            "{passed}/{required} | {pin} | {state} | {blockers} |".format(
                wave=item["wave"],
                name=str(source["name"]).replace("|", "\\|"),
                url=source["upstream_url"],
                artifact_class=item["artifact_class"],
                role=str(item["planned_role"]).replace("|", "\\|"),
                profile=item["profile"],
                effect=source["network_effect"],
                passed=passed,
                required=required,
                pin=pin_text,
                state=item["admission_state"],
                blockers=blockers.replace("|", "\\|"),
            )
        )

    wave_counts = Counter(str(item["wave"]) for item in candidates)
    class_counts = Counter(str(item["artifact_class"]) for item in candidates)
    lines.extend(["", "## 波次", ""])
    for wave, description in admission["waves"].items():
        lines.append(f"- `{wave}`（{wave_counts[wave]}）：{description}")
    lines.extend([
        "",
        "## 汇总",
        "",
        f"- 准入候选：{len(candidates)}",
        "- 已正式纳入：" + str(sum(1 for item in candidates if item["admission_state"] == "admitted")),
        "- 类型：" + "，".join(f"{key}={class_counts[key]}" for key in sorted(class_counts)),
        "",
        "## 门禁含义",
        "",
        "除研究来源外，每项需要完成 8 个正式门禁：许可、不可变版本、完整性、安全审查、接口契约、隔离策略、行为测试和回滚测试。",
        "",
    ])
    return "\n".join(lines)


def main() -> int:
    try:
        admission, candidates, source_by_id = validate()
        TABLE_PATH.write_text(render(admission, candidates, source_by_id), encoding="utf-8")
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"BLOCK: {exc}", file=sys.stderr)
        return 1
    print(f"PASS: {len(candidates)} admission candidates validated; rebuilt {TABLE_PATH.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
