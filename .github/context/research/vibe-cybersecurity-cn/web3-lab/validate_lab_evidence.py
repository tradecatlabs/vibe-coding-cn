#!/usr/bin/env python3
"""校验靶场 ground truth 与证据账本的一致性。
运行：python3 web3-lab/validate_lab_evidence.py
依赖：Python 3.10+ 标准库；需要 web3-lab/ground-truth.json 与 evidence/findings-*.json。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
GT_PATH = ROOT / "ground-truth.json"
EVIDENCE_DIR = ROOT / "evidence"


def fail(message: str) -> None:
    raise ValueError(message)


def main() -> int:
    try:
        gt = json.loads(GT_PATH.read_text(encoding="utf-8"))
        gt_items = {item["id"]: item for item in gt["vulnerabilities"]}

        finding_files = sorted(EVIDENCE_DIR.glob("findings-*.json"))
        if not finding_files:
            fail("缺少 findings-*.json 证据账本")

        for path in finding_files:
            evidence = json.loads(path.read_text(encoding="utf-8"))
            findings = {item["id"]: item for item in evidence["findings"]}

            if set(findings) != set(gt_items):
                missing = set(gt_items) - set(findings)
                extra = set(findings) - set(gt_items)
                fail(f"{path.name}: ground truth 与 findings 不一致 missing={missing} extra={extra}")

            for finding_id, item in findings.items():
                if item["ground_truth"] != gt_items[finding_id].get("ground_truth", True):
                    fail(f"{finding_id}: ground_truth 标志不一致")
                if item["status"] != "confirmed":
                    fail(f"{finding_id}: 靶场证据账本必须全部 confirmed")
                if item["verification"]["method"] not in {"foundry attack test"}:
                    fail(f"{finding_id}: 验证方法不在允许集")
                artifact = item["verification"].get("artifact")
                if artifact:
                    artifact_path = ROOT / artifact
                    if not artifact_path.exists() or artifact_path.stat().st_size == 0:
                        fail(f"{finding_id}: 验证 artifact 缺失或为空 {artifact}")

        print(f"PASS: ground truth {len(gt_items)} == findings 全部 confirmed，artifacts 存在")
        return 0
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"BLOCK: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
