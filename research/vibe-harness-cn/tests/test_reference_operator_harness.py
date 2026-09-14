"""验证参考 Harness 的选择、物化、独立验证、溯源与失败关闭行为。"""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "examples" / "reference_harness" / "reference_harness.py"
REQUEST_PATH = ROOT / "examples" / "reference_harness" / "requests" / "definition-first.json"
BINDING_PATH = ROOT / "examples" / "reference_harness" / "bindings" / "instruction-packet.json"


def load_reference_harness():
    spec = importlib.util.spec_from_file_location("reference_operator_harness", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"无法加载参考 Harness：{MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ReferenceOperatorHarnessTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.harness = load_reference_harness()

    def request(self) -> dict:
        return json.loads(REQUEST_PATH.read_text(encoding="utf-8"))

    def binding(self) -> dict:
        return json.loads(BINDING_PATH.read_text(encoding="utf-8"))

    def test_full_loop_is_deterministic_and_minimally_disclosed(self) -> None:
        first = self.harness.run_reference_harness(self.request(), self.binding())
        second = self.harness.run_reference_harness(self.request(), self.binding())

        self.assertEqual(first, second)
        record = first["record"]
        packet = first["instruction_packet"]
        self.assertEqual("completed", record["metadata"]["status"])
        self.assertEqual("accepted", record["spec"]["result"]["verification_verdict"])
        self.assertEqual("instruction_materialization_only", record["spec"]["result"]["claim_scope"])
        self.assertEqual(468, record["spec"]["selection"]["considered_count"])
        self.assertEqual(4, len(packet["spec"]["instructions"]))
        self.assertEqual(
            self.harness.canonical_digest(packet),
            record["spec"]["result"]["instruction_packet_digest"],
        )
        serialized_trace = json.dumps(record["spec"]["provenance"], ensure_ascii=False)
        self.assertNotIn("需要明确 AI 算子", serialized_trace)
        self.assertNotIn("problem", record["spec"]["provenance"])

    def test_three_operator_kinds_and_recursive_model_application(self) -> None:
        cases = (
            ("psoa.research.intervene", {"perform"}),
            ("psoa.computer-science.abstraction", {"ask", "interpret"}),
            ("psoa.mathematics.rigorous-reasoning-loop", {"perform", "ask", "interpret"}),
        )
        for operator_id, expected_actions in cases:
            with self.subTest(operator_id=operator_id):
                request = self.request()
                request["spec"]["selection"] = {"requested_operator_ids": [operator_id]}
                request["spec"]["budgets"]["max_steps"] = 32
                bundle = self.harness.run_reference_harness(request, self.binding())
                actions = {
                    item["action"] for item in bundle["instruction_packet"]["spec"]["instructions"]
                }
                self.assertTrue(expected_actions.issubset(actions))
                self.assertEqual(
                    operator_id,
                    bundle["record"]["spec"]["selection"]["selected_operator"]["id"],
                )

    def test_selector_can_use_domain_class_and_query_without_explicit_id(self) -> None:
        request = self.request()
        request["spec"]["selection"] = {
            "domains": ["mathematics"],
            "functional_classes": ["representation"],
            "query_terms": ["量词拆解"],
        }
        bundle = self.harness.run_reference_harness(request, self.binding())
        selected = bundle["record"]["spec"]["selection"]["selected_operator"]
        self.assertEqual("psoa.mathematics.quantifier-unpacking", selected["id"])
        self.assertIn("domain_match", selected["reasons"])
        self.assertIn("functional_class_match", selected["reasons"])

        request = self.request()
        request["spec"]["selection"] = {"domains": ["mathematics"]}
        request["spec"]["budgets"]["max_candidates"] = 2
        selection = self.harness.run_reference_harness(request, self.binding())["record"]["spec"][
            "selection"
        ]
        self.assertEqual(2, selection["candidate_count"])
        self.assertGreater(selection["rejection_summary"]["candidate_budget_truncated"], 0)
        self.assertEqual(
            selection["considered_count"],
            selection["candidate_count"] + sum(selection["rejection_summary"].values()),
        )

    def test_unknown_binding_and_policy_escalation_fail_closed(self) -> None:
        request = self.request()
        request["spec"]["binding_id"] = "missing.binding"
        with self.assertRaisesRegex(self.harness.RuntimeViolation, "未知 Binding"):
            self.harness.run_reference_harness(request, self.binding())

        request = self.request()
        request["spec"]["required_effect_scope"] = "local_write"
        with self.assertRaisesRegex(self.harness.RuntimeViolation, "effect scope"):
            self.harness.run_reference_harness(request, self.binding())

    def test_step_budget_is_enforced_before_success_record(self) -> None:
        request = self.request()
        request["spec"]["budgets"]["max_steps"] = 2
        with self.assertRaisesRegex(self.harness.RuntimeViolation, "超过 max_steps=2"):
            self.harness.run_reference_harness(request, self.binding())

        request = self.request()
        request["spec"]["budgets"]["max_steps"] = True
        with self.assertRaisesRegex(self.harness.RuntimeViolation, "必须是正整数"):
            self.harness.run_reference_harness(request, self.binding())

    def test_verifier_rejects_tampered_instruction_packet(self) -> None:
        request = self.request()
        binding = self.binding()
        bundle = self.harness.run_reference_harness(request, binding)
        packet = copy.deepcopy(bundle["instruction_packet"])
        reported_digest = bundle["record"]["spec"]["result"]["instruction_packet_digest"]
        packet["spec"]["instructions"][0]["content"] = "被篡改的指令"

        failures = self.harness.verify_materialization(
            request,
            binding,
            self.harness.DEFAULT_CATALOG,
            self.harness.DEFAULT_TAXONOMY,
            packet,
            reported_digest,
        )
        self.assertIn("reported_instruction_packet_digest_mismatch", failures)
        self.assertIn("instruction_packet_content_mismatch", failures)
        record = self.harness.verify_and_record(
            request,
            binding,
            self.harness.DEFAULT_CATALOG,
            self.harness.DEFAULT_TAXONOMY,
            packet,
            reported_digest,
        )
        self.assertEqual("rejected", record["metadata"]["status"])
        self.assertEqual("completed", record["spec"]["result"]["materialization_status"])
        self.assertEqual("rejected", record["spec"]["result"]["verification_verdict"])

    def test_unknown_and_cyclic_method_references_fail_closed(self) -> None:
        for case, target in (("missing", "psoa.test.missing"), ("cycle", "psoa.test.method")):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as raw:
                directory = Path(raw)
                entry = {
                    "id": "psoa.test.method",
                    "version": "1.0.0",
                    "kind": "MethodSpec",
                    "status": "experimental",
                    "domain": "test-domain",
                    "governance": {"risk_level": "low"},
                    "semantics": {"steps": [{"order": 1, "use": target}]},
                }
                catalog = {
                    "api_version": "vibe-harness-cn.dev/v1alpha1",
                    "spec": {
                        "conformance_profile": "vibe-harness-cn/reference-library-v1",
                        "packs": [{"path": "pack.json"}],
                    },
                }
                taxonomy = {
                    "spec": {
                        "domain_defaults": [
                            {"domain": "test-domain", "functional_class": "search"}
                        ],
                        "entry_overrides": [],
                    }
                }
                (directory / "catalog.json").write_text(json.dumps(catalog), encoding="utf-8")
                (directory / "pack.json").write_text(
                    json.dumps({"entries": [entry]}), encoding="utf-8"
                )
                (directory / "taxonomy.json").write_text(json.dumps(taxonomy), encoding="utf-8")
                request = self.request()
                request["spec"]["selection"] = {
                    "requested_operator_ids": ["psoa.test.method"]
                }

                expected = "引用不存在" if case == "missing" else "引用形成循环"
                with self.assertRaisesRegex(self.harness.RuntimeViolation, expected):
                    self.harness.run_reference_harness(
                        request,
                        self.binding(),
                        directory / "catalog.json",
                        directory / "taxonomy.json",
                    )

    def test_cli_returns_nonzero_without_printing_a_success_bundle(self) -> None:
        request = self.request()
        request["spec"]["binding_id"] = "missing.binding"
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "request.json"
            path.write_text(json.dumps(request), encoding="utf-8")
            completed = subprocess.run(
                [
                    sys.executable,
                    str(MODULE_PATH),
                    "--request",
                    str(path),
                    "--binding",
                    str(BINDING_PATH),
                ],
                cwd=ROOT,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
        self.assertEqual(2, completed.returncode)
        self.assertEqual("", completed.stdout)
        error = json.loads(completed.stderr)
        self.assertEqual("rejected", error["status"])

    def test_generated_record_conforms_to_runtime_core(self) -> None:
        record = self.harness.run_reference_harness(self.request(), self.binding())["record"]
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "record.json"
            path.write_text(json.dumps(record), encoding="utf-8")
            completed = subprocess.run(
                [
                    "uv",
                    "run",
                    "--locked",
                    "--script",
                    "scripts/validate_harness.py",
                    "--operator-runtime",
                    str(path),
                ],
                cwd=ROOT,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                check=False,
            )
        self.assertEqual(0, completed.returncode, completed.stdout)


if __name__ == "__main__":
    unittest.main()
