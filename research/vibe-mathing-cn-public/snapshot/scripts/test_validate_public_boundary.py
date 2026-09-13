#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).with_name("validate_public_boundary.py")
SPEC = importlib.util.spec_from_file_location("validate_public_boundary", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class PublicBoundaryTests(unittest.TestCase):
    def test_exact_public_origin_forms(self) -> None:
        self.assertIn("https://github.com/vibemathing/vibe-mathing-cn-public", MODULE.PUBLIC_ORIGINS)
        self.assertIn("https://github.com/vibemathing/vibe-mathing-cn-public.git", MODULE.PUBLIC_ORIGINS)
        self.assertNotIn("https://github.com/example/vibe-mathing-cn-public", MODULE.PUBLIC_ORIGINS)

    def test_forbidden_paths(self) -> None:
        blocked = [
            "governance/tasks/0010-millennium-rh/result.json",
            "governance/tasks/millennium-goals/GOAL-RH.md",
            "governance/verification/ledger/VR-001.md",
            "research/artifacts/candidate.zip",
            "research/runs/live/state.json",
            "fixture/Proof.olean",
            "RECOVERY_MANIFEST.json",
        ]
        allowed = [
            "research/schema/result.schema.json",
            "research/artifacts/README.md",
            "fixtures/lean-proof/Proof.lean",
            "governance/processes/PUBLIC_REPOSITORY_BOUNDARY.md",
        ]
        for path in blocked:
            self.assertTrue(MODULE.forbidden_path(path), path)
        for path in allowed:
            self.assertFalse(MODULE.forbidden_path(path), path)

    def test_sensitive_content_patterns(self) -> None:
        private_name = b"vibe-mathing-cn-" + b"internal"
        absolute_path = b"/" + b"home" + b"/alice/.projects/vibe-mathing-cn/task"
        session_identifier = b"01" + b"a0123456-1234-5678-9abc-def012345678"
        self.assertIn("private_repository_name", MODULE.content_findings(private_name))
        self.assertIn("absolute_user_project_path", MODULE.content_findings(absolute_path))
        self.assertIn("session_identifier", MODULE.content_findings(session_identifier))
        self.assertEqual(MODULE.content_findings(b"portable public fixture"), [])

    def test_non_repository_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            issues = MODULE.validate(Path(temporary))
        self.assertEqual(issues[0]["code"], "not_git_repository")


if __name__ == "__main__":
    unittest.main(verbosity=2)
