#!/usr/bin/env python3
# 做什么：验证 git-reference 冷缓存的命令、路径、许可证和 fail-closed 行为。
# 怎么运行：python3 scripts/test_sync_supply_chain.py
# 需要什么：Python 3；测试使用 mock，不访问网络、不创建或删除真实仓库。

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch


SCRIPT = Path(__file__).with_name("sync_supply_chain.py")
SPEC = importlib.util.spec_from_file_location("sync_supply_chain", SCRIPT)
assert SPEC and SPEC.loader
sync = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(sync)


def reference_source() -> dict[str, object]:
    return {
        "id": "fixture-reference",
        "kind": "git-reference",
        "url": "https://github.com/example/fixture.git",
        "branch": "main",
        "commit": "a" * 40,
        "license_path": "LICENSE",
        "license_sha256": "b" * 64,
        "path": "vendor/upstream/reference/fixture-reference",
    }


class ReferenceCacheTests(unittest.TestCase):
    def test_reference_source_rejects_untrusted_git_fields(self) -> None:
        invalid = {
            "url": "ssh://example.invalid/repo.git",
            "branch": "--upload-pack=bad",
            "commit": "HEAD",
            "license_path": "docs/LICENSE",
            "license_sha256": "bad",
        }
        for field, value in invalid.items():
            with self.subTest(field=field):
                source = reference_source()
                source[field] = value
                with self.assertRaises(RuntimeError):
                    sync.validate_git_reference_source(source)

    def test_reference_path_must_stay_in_reference_root(self) -> None:
        source = reference_source()
        source["path"] = "vendor/upstream/not-reference"
        with self.assertRaisesRegex(RuntimeError, "路径越界"):
            sync.reference_repo_path(source)

    def test_reference_path_must_be_direct_child(self) -> None:
        source = reference_source()
        source["path"] = "vendor/upstream/reference/nested/fixture"
        with self.assertRaisesRegex(RuntimeError, "直接子项"):
            sync.reference_repo_path(source)

    def test_reference_shape_rejects_materialized_worktree(self) -> None:
        root = MagicMock(spec=Path)
        git_dir = MagicMock(spec=Path)
        git_dir.is_dir.return_value = True
        root.__truediv__.return_value = git_dir
        worktree_file = MagicMock(spec=Path)
        worktree_file.name = "README.md"
        root.iterdir.return_value = iter([git_dir, worktree_file])
        git_dir.name = ".git"
        with self.assertRaisesRegex(RuntimeError, "意外包含工作树"):
            sync.ensure_reference_shape(root)

    @patch.object(sync, "reference_license_sha256", return_value="b" * 64)
    @patch.object(sync, "ensure_reference_shape")
    @patch.object(sync, "run")
    @patch.object(sync, "reference_repo_path")
    def test_sync_fetches_only_pinned_commit_without_branch_clone(
        self,
        mock_path: MagicMock,
        mock_run: MagicMock,
        _mock_shape: MagicMock,
        _mock_license: MagicMock,
    ) -> None:
        source = reference_source()
        path = MagicMock(spec=Path)
        path.exists.return_value = False
        path.parent = MagicMock(spec=Path)
        mock_path.return_value = path
        mock_run.side_effect = [
            "",  # git init
            "",  # remote add
            "",  # initial fetch
            "",  # pin ref
            "",  # set symbolic HEAD
            source["url"],  # remote get-url
            "c" * 40,  # initial HEAD differs
            "",  # pinned fetch
            "",  # pin ref
            "",  # set symbolic HEAD
            source["commit"],  # final HEAD
        ]

        sync.sync_git_reference(source)

        calls = [item.args[0] for item in mock_run.call_args_list]
        self.assertEqual(calls[0], ["git", "init", str(path)])
        self.assertIn(
            ["git", "fetch", "--no-tags", "--depth", "1", "--filter=blob:none", "origin", source["commit"]],
            calls,
        )
        self.assertIn(
            ["git", "update-ref", "refs/heads/reference-pin", source["commit"]],
            calls,
        )
        self.assertFalse(any(args[:2] == ["git", "clone"] for args in calls))
        self.assertFalse(any("--branch" in args for args in calls))
        self.assertFalse(any("checkout" in args for args in calls))

    @patch.object(sync, "reference_license_sha256", return_value="d" * 64)
    @patch.object(sync, "ensure_reference_shape")
    @patch.object(sync, "run")
    @patch.object(sync, "reference_repo_path")
    def test_sync_rejects_license_drift(
        self,
        mock_path: MagicMock,
        mock_run: MagicMock,
        _mock_shape: MagicMock,
        _mock_license: MagicMock,
    ) -> None:
        source = reference_source()
        path = MagicMock(spec=Path)
        path.exists.return_value = True
        mock_path.return_value = path
        mock_run.side_effect = [source["url"], source["commit"], source["commit"]]
        with self.assertRaisesRegex(RuntimeError, "许可证哈希漂移"):
            sync.sync_git_reference(source)

    @patch.object(sync, "reference_license_sha256", return_value="b" * 64)
    @patch.object(sync, "ensure_reference_shape")
    @patch.object(sync, "run")
    @patch.object(sync, "reference_repo_path")
    def test_check_preserves_native_commit_and_remote_failures(
        self,
        mock_path: MagicMock,
        mock_run: MagicMock,
        _mock_shape: MagicMock,
        _mock_license: MagicMock,
    ) -> None:
        source = reference_source()
        path = MagicMock(spec=Path)
        path.is_dir.return_value = True
        mock_path.return_value = path
        mock_run.side_effect = ["https://github.com/other/repo.git", "e" * 40]
        errors = sync.check_git_reference(source)
        self.assertEqual(2, len(errors))
        self.assertTrue(any("远端漂移" in error for error in errors))
        self.assertTrue(any("commit 漂移" in error for error in errors))


if __name__ == "__main__":
    unittest.main(verbosity=2)
