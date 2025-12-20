#!/usr/bin/env python3
"""
Tests for cli/package_skill.py functionality
"""

import unittest
import tempfile
import zipfile
from pathlib import Path
import sys

from skill_seekers.cli.package_skill import package_skill


class TestPackageSkill(unittest.TestCase):
    """Test package_skill function"""

    def create_test_skill_directory(self, tmpdir):
        """Helper to create a test skill directory structure"""
        skill_dir = Path(tmpdir) / "test-skill"
        skill_dir.mkdir()

        # Create SKILL.md
        (skill_dir / "SKILL.md").write_text("---\nname: test-skill\n---\n# Test Skill")

        # Create references directory
        refs_dir = skill_dir / "references"
        refs_dir.mkdir()
        (refs_dir / "index.md").write_text("# Index")
        (refs_dir / "getting_started.md").write_text("# Getting Started")

        # Create scripts directory (empty)
        (skill_dir / "scripts").mkdir()

        # Create assets directory (empty)
        (skill_dir / "assets").mkdir()

        return skill_dir

    def test_package_valid_skill_directory(self):
        """Test packaging a valid skill directory"""
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = self.create_test_skill_directory(tmpdir)

            success, zip_path = package_skill(skill_dir, open_folder_after=False, skip_quality_check=True)

            self.assertTrue(success)
            self.assertIsNotNone(zip_path)
            self.assertTrue(zip_path.exists())
            self.assertEqual(zip_path.suffix, '.zip')
            self.assertTrue(zipfile.is_zipfile(zip_path))

    def test_package_creates_correct_zip_structure(self):
        """Test that packaged zip contains correct files"""
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = self.create_test_skill_directory(tmpdir)

            success, zip_path = package_skill(skill_dir, open_folder_after=False, skip_quality_check=True)

            self.assertTrue(success)

            # Check zip contents
            with zipfile.ZipFile(zip_path, 'r') as zf:
                names = zf.namelist()

                # Should contain SKILL.md
                self.assertTrue(any('SKILL.md' in name for name in names))

                # Should contain references
                self.assertTrue(any('references/index.md' in name for name in names))
                self.assertTrue(any('references/getting_started.md' in name for name in names))

    def test_package_excludes_backup_files(self):
        """Test that .backup files are excluded from zip"""
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = self.create_test_skill_directory(tmpdir)

            # Add a backup file
            (skill_dir / "SKILL.md.backup").write_text("# Backup")

            success, zip_path = package_skill(skill_dir, open_folder_after=False, skip_quality_check=True)

            self.assertTrue(success)

            # Check that backup is NOT in zip
            with zipfile.ZipFile(zip_path, 'r') as zf:
                names = zf.namelist()
                self.assertFalse(any('.backup' in name for name in names))

    def test_package_nonexistent_directory(self):
        """Test packaging a nonexistent directory"""
        success, zip_path = package_skill("/nonexistent/path", open_folder_after=False, skip_quality_check=True)

        self.assertFalse(success)
        self.assertIsNone(zip_path)

    def test_package_directory_without_skill_md(self):
        """Test packaging directory without SKILL.md"""
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir) / "invalid-skill"
            skill_dir.mkdir()

            success, zip_path = package_skill(skill_dir, open_folder_after=False, skip_quality_check=True)

            self.assertFalse(success)
            self.assertIsNone(zip_path)

    def test_package_creates_zip_in_correct_location(self):
        """Test that zip is created in output/ directory"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create skill in output-like structure
            output_dir = Path(tmpdir) / "output"
            output_dir.mkdir()

            skill_dir = output_dir / "test-skill"
            skill_dir.mkdir()
            (skill_dir / "SKILL.md").write_text("# Test")
            (skill_dir / "references").mkdir()
            (skill_dir / "scripts").mkdir()
            (skill_dir / "assets").mkdir()

            success, zip_path = package_skill(skill_dir, open_folder_after=False, skip_quality_check=True)

            self.assertTrue(success)
            # Zip should be in output directory, not inside skill directory
            self.assertEqual(zip_path.parent, output_dir)
            self.assertEqual(zip_path.name, "test-skill.zip")

    def test_package_zip_name_matches_skill_name(self):
        """Test that zip filename matches skill directory name"""
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir) / "my-awesome-skill"
            skill_dir.mkdir()
            (skill_dir / "SKILL.md").write_text("# Test")
            (skill_dir / "references").mkdir()
            (skill_dir / "scripts").mkdir()
            (skill_dir / "assets").mkdir()

            success, zip_path = package_skill(skill_dir, open_folder_after=False, skip_quality_check=True)

            self.assertTrue(success)
            self.assertEqual(zip_path.name, "my-awesome-skill.zip")


class TestPackageSkillCLI(unittest.TestCase):
    """Test package_skill.py command-line interface"""

    def test_cli_help_output(self):
        """Test that skill-seekers package --help works"""
        import subprocess

        try:
            result = subprocess.run(
                ['skill-seekers', 'package', '--help'],
                capture_output=True,
                text=True,
                timeout=5
            )

            # argparse may return 0 or 2 for --help
            self.assertIn(result.returncode, [0, 2])
            output = result.stdout + result.stderr
            self.assertTrue('usage:' in output.lower() or 'package' in output.lower())
        except FileNotFoundError:
            self.skipTest("skill-seekers command not installed")

    def test_cli_executes_without_errors(self):
        """Test that skill-seekers-package entry point works"""
        import subprocess

        try:
            result = subprocess.run(
                ['skill-seekers-package', '--help'],
                capture_output=True,
                text=True,
                timeout=5
            )

            # argparse may return 0 or 2 for --help
            self.assertIn(result.returncode, [0, 2])
        except FileNotFoundError:
            self.skipTest("skill-seekers-package command not installed")


if __name__ == '__main__':
    unittest.main()
