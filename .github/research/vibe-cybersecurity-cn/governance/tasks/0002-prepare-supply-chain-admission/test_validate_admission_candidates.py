#!/usr/bin/env python3
"""回归验证供应链准入状态机的 fail-closed 行为。
运行：python3 -m unittest governance/tasks/0002-prepare-supply-chain-admission/test_validate_admission_candidates.py
依赖：Python 3.10+ 标准库和 0001/0002 的真实 JSON fixture。
"""

from __future__ import annotations

import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


TASK_ROOT = Path(__file__).resolve().parent
SOURCE_PATH = TASK_ROOT.parent / "0001-survey-cybersecurity-supply-chain" / "supply-chain-candidates.json"
ADMISSION_PATH = TASK_ROOT / "admission-candidates.json"
SPEC = importlib.util.spec_from_file_location(
    "validate_admission_candidates",
    TASK_ROOT / "validate_admission_candidates.py",
)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("无法加载准入校验器")
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class AdmissionValidationTest(unittest.TestCase):
    def setUp(self) -> None:
        self.source = json.loads(SOURCE_PATH.read_text(encoding="utf-8"))
        self.admission = json.loads(ADMISSION_PATH.read_text(encoding="utf-8"))

    def validate(self, admission: dict[str, object], source: dict[str, object] | None = None) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source_dir = root / "0001-survey-cybersecurity-supply-chain"
            admission_dir = root / "0002-prepare-supply-chain-admission"
            source_dir.mkdir()
            admission_dir.mkdir()
            source_path = source_dir / "supply-chain-candidates.json"
            admission_path = admission_dir / "admission-candidates.json"
            source_path.write_text(
                json.dumps(source or self.source, ensure_ascii=False),
                encoding="utf-8",
            )
            admission_path.write_text(
                json.dumps(admission, ensure_ascii=False),
                encoding="utf-8",
            )
            with patch.object(VALIDATOR, "ADMISSION_PATH", admission_path):
                VALIDATOR.validate()

    def test_real_catalog_passes(self) -> None:
        self.validate(self.admission)

    def test_default_enabled_candidate_is_rejected(self) -> None:
        payload = copy.deepcopy(self.admission)
        payload["candidates"][0]["default_enabled"] = True
        with self.assertRaisesRegex(ValueError, "default_enabled=false"):
            self.validate(payload)

    def test_admitted_candidate_with_pending_gates_is_rejected(self) -> None:
        payload = copy.deepcopy(self.admission)
        payload["candidates"][0]["admission_state"] = "admitted"
        with self.assertRaisesRegex(ValueError, "未完成全部门禁"):
            self.validate(payload)

    def test_missing_research_mvp_is_rejected(self) -> None:
        payload = copy.deepcopy(self.admission)
        payload["candidates"].pop()
        with self.assertRaisesRegex(ValueError, "完整覆盖研究 MVP"):
            self.validate(payload)

    def test_active_high_research_candidate_is_rejected(self) -> None:
        source = copy.deepcopy(self.source)
        subfinder = next(
            item for item in source["candidates"] if item["id"] == "subfinder"
        )
        subfinder["network_effect"] = "active-high"
        with self.assertRaisesRegex(ValueError, "active-high"):
            self.validate(self.admission, source)

    def test_source_snapshot_drift_is_rejected(self) -> None:
        payload = copy.deepcopy(self.admission)
        payload["source_snapshot_date"] = "1970-01-01"
        with self.assertRaisesRegex(ValueError, "source_snapshot_date"):
            self.validate(payload)

    def test_required_check_keys_cannot_be_deleted(self) -> None:
        payload = copy.deepcopy(self.admission)
        payload["check_keys"].remove("security_review")
        for candidate in payload["candidates"]:
            candidate["checks"].pop("security_review")
        with self.assertRaisesRegex(ValueError, "固定八门禁"):
            self.validate(payload)

    def test_passed_gate_requires_evidence(self) -> None:
        payload = copy.deepcopy(self.admission)
        payload["candidates"][0]["checks"]["security_review"] = "pass"
        with self.assertRaisesRegex(ValueError, "必须绑定 evidence_refs"):
            self.validate(payload)

    def test_verified_pin_requires_sha256_digest(self) -> None:
        payload = copy.deepcopy(self.admission)
        payload["candidates"][0]["pin"] = {
            "ref": "v1.0.0", "digest": "trusted", "status": "verified"
        }
        with self.assertRaisesRegex(ValueError, "必须是 sha256"):
            self.validate(payload)


if __name__ == "__main__":
    unittest.main()
