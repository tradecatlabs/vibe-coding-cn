#!/usr/bin/env python3
"""
Tests for cli/upload_skill.py functionality
"""

import unittest
import tempfile
import zipfile
import os
from pathlib import Path
import sys

from skill_seekers.cli.upload_skill import upload_skill_api


class TestUploadSkillAPI(unittest.TestCase):
    """Test upload_skill_api function"""

    def setUp(self):
        """Store original API key state"""
        self.original_api_key = os.environ.get('ANTHROPIC_API_KEY')

    def tearDown(self):
        """Restore original API key state"""
        if self.original_api_key:
            os.environ['ANTHROPIC_API_KEY'] = self.original_api_key
        elif 'ANTHROPIC_API_KEY' in os.environ:
            del os.environ['ANTHROPIC_API_KEY']

    def create_test_zip(self, tmpdir):
        """Helper to create a test .zip file"""
        zip_path = Path(tmpdir) / "test-skill.zip"

        with zipfile.ZipFile(zip_path, 'w') as zf:
            zf.writestr("SKILL.md", "---\nname: test\n---\n# Test Skill")
            zf.writestr("references/index.md", "# Index")

        return zip_path

    def test_upload_without_api_key(self):
        """Test that upload fails gracefully without API key"""
        # Remove API key
        if 'ANTHROPIC_API_KEY' in os.environ:
            del os.environ['ANTHROPIC_API_KEY']

        with tempfile.TemporaryDirectory() as tmpdir:
            zip_path = self.create_test_zip(tmpdir)

            success, message = upload_skill_api(zip_path)

            self.assertFalse(success)
            # Check for api_key (with underscore) in message
            self.assertTrue('api_key' in message.lower() or 'api key' in message.lower())

    def test_upload_with_nonexistent_file(self):
        """Test upload with nonexistent file"""
        os.environ['ANTHROPIC_API_KEY'] = 'sk-ant-test-key'

        success, message = upload_skill_api("/nonexistent/file.zip")

        self.assertFalse(success)
        self.assertIn('not found', message.lower())

    def test_upload_with_invalid_zip(self):
        """Test upload with invalid zip file (not a zip)"""
        os.environ['ANTHROPIC_API_KEY'] = 'sk-ant-test-key'

        with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as tmpfile:
            tmpfile.write(b"Not a valid zip file")
            tmpfile.flush()

            try:
                success, message = upload_skill_api(tmpfile.name)

                # Should either fail validation or detect invalid zip
                self.assertFalse(success)
            finally:
                os.unlink(tmpfile.name)

    def test_upload_accepts_path_object(self):
        """Test that upload_skill_api accepts Path objects"""
        os.environ['ANTHROPIC_API_KEY'] = 'sk-ant-test-key'

        with tempfile.TemporaryDirectory() as tmpdir:
            zip_path = self.create_test_zip(tmpdir)

            # This should not raise TypeError
            try:
                success, message = upload_skill_api(Path(zip_path))
            except TypeError:
                self.fail("upload_skill_api should accept Path objects")


class TestUploadSkillCLI(unittest.TestCase):
    """Test upload_skill.py command-line interface"""

    def test_cli_help_output(self):
        """Test that skill-seekers upload --help works"""
        import subprocess

        try:
            result = subprocess.run(
                ['skill-seekers', 'upload', '--help'],
                capture_output=True,
                text=True,
                timeout=5
            )

            # argparse may return 0 or 2 for --help
            self.assertIn(result.returncode, [0, 2])
            output = result.stdout + result.stderr
            self.assertTrue('usage:' in output.lower() or 'upload' in output.lower())
        except FileNotFoundError:
            self.skipTest("skill-seekers command not installed")

    def test_cli_executes_without_errors(self):
        """Test that skill-seekers-upload entry point works"""
        import subprocess

        try:
            result = subprocess.run(
                ['skill-seekers-upload', '--help'],
                capture_output=True,
                text=True,
                timeout=5
            )

            # argparse may return 0 or 2 for --help
            self.assertIn(result.returncode, [0, 2])
        except FileNotFoundError:
            self.skipTest("skill-seekers-upload command not installed")

    def test_cli_requires_zip_argument(self):
        """Test that CLI requires zip file argument"""
        import subprocess

        result = subprocess.run(
            ['python3', 'cli/upload_skill.py'],
            capture_output=True,
            text=True
        )

        # Should fail or show usage
        self.assertTrue(
            result.returncode != 0 or 'usage' in result.stderr.lower() or 'usage' in result.stdout.lower()
        )


if __name__ == '__main__':
    unittest.main()
