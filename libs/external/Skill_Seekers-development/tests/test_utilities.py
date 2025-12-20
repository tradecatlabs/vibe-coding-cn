#!/usr/bin/env python3
"""
Tests for cli/utils.py utility functions
"""

import unittest
import tempfile
import os
import zipfile
from pathlib import Path
import sys

from skill_seekers.cli.utils import (
    has_api_key,
    get_api_key,
    get_upload_url,
    format_file_size,
    validate_skill_directory,
    validate_zip_file,
    print_upload_instructions
)


class TestAPIKeyFunctions(unittest.TestCase):
    """Test API key utility functions"""

    def setUp(self):
        """Store original API key state"""
        self.original_api_key = os.environ.get('ANTHROPIC_API_KEY')

    def tearDown(self):
        """Restore original API key state"""
        if self.original_api_key:
            os.environ['ANTHROPIC_API_KEY'] = self.original_api_key
        elif 'ANTHROPIC_API_KEY' in os.environ:
            del os.environ['ANTHROPIC_API_KEY']

    def test_has_api_key_when_set(self):
        """Test has_api_key returns True when key is set"""
        os.environ['ANTHROPIC_API_KEY'] = 'sk-ant-test-key'
        self.assertTrue(has_api_key())

    def test_has_api_key_when_not_set(self):
        """Test has_api_key returns False when key is not set"""
        if 'ANTHROPIC_API_KEY' in os.environ:
            del os.environ['ANTHROPIC_API_KEY']
        self.assertFalse(has_api_key())

    def test_has_api_key_when_empty_string(self):
        """Test has_api_key returns False when key is empty string"""
        os.environ['ANTHROPIC_API_KEY'] = ''
        self.assertFalse(has_api_key())

    def test_has_api_key_when_whitespace_only(self):
        """Test has_api_key returns False when key is whitespace"""
        os.environ['ANTHROPIC_API_KEY'] = '   '
        self.assertFalse(has_api_key())

    def test_get_api_key_returns_key(self):
        """Test get_api_key returns the actual key"""
        os.environ['ANTHROPIC_API_KEY'] = 'sk-ant-test-key'
        self.assertEqual(get_api_key(), 'sk-ant-test-key')

    def test_get_api_key_returns_none_when_not_set(self):
        """Test get_api_key returns None when not set"""
        if 'ANTHROPIC_API_KEY' in os.environ:
            del os.environ['ANTHROPIC_API_KEY']
        self.assertIsNone(get_api_key())

    def test_get_api_key_strips_whitespace(self):
        """Test get_api_key strips whitespace from key"""
        os.environ['ANTHROPIC_API_KEY'] = '  sk-ant-test-key  '
        self.assertEqual(get_api_key(), 'sk-ant-test-key')


class TestGetUploadURL(unittest.TestCase):
    """Test get_upload_url function"""

    def test_get_upload_url_returns_correct_url(self):
        """Test get_upload_url returns the correct Claude skills URL"""
        url = get_upload_url()
        self.assertEqual(url, "https://claude.ai/skills")

    def test_get_upload_url_returns_string(self):
        """Test get_upload_url returns a string"""
        url = get_upload_url()
        self.assertIsInstance(url, str)


class TestFormatFileSize(unittest.TestCase):
    """Test format_file_size function"""

    def test_format_bytes_below_1kb(self):
        """Test formatting bytes below 1 KB"""
        self.assertEqual(format_file_size(500), "500 bytes")
        self.assertEqual(format_file_size(1023), "1023 bytes")

    def test_format_kilobytes(self):
        """Test formatting KB sizes"""
        self.assertEqual(format_file_size(1024), "1.0 KB")
        self.assertEqual(format_file_size(1536), "1.5 KB")
        self.assertEqual(format_file_size(10240), "10.0 KB")

    def test_format_megabytes(self):
        """Test formatting MB sizes"""
        self.assertEqual(format_file_size(1048576), "1.0 MB")
        self.assertEqual(format_file_size(1572864), "1.5 MB")
        self.assertEqual(format_file_size(10485760), "10.0 MB")

    def test_format_zero_bytes(self):
        """Test formatting zero bytes"""
        self.assertEqual(format_file_size(0), "0 bytes")

    def test_format_large_files(self):
        """Test formatting large file sizes"""
        # 100 MB
        self.assertEqual(format_file_size(104857600), "100.0 MB")
        # 1 GB (still shows as MB)
        self.assertEqual(format_file_size(1073741824), "1024.0 MB")


class TestValidateSkillDirectory(unittest.TestCase):
    """Test validate_skill_directory function"""

    def test_valid_skill_directory(self):
        """Test validation of valid skill directory"""
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir) / "test-skill"
            skill_dir.mkdir()
            (skill_dir / "SKILL.md").write_text("# Test Skill")

            is_valid, error = validate_skill_directory(skill_dir)
            self.assertTrue(is_valid)
            self.assertIsNone(error)

    def test_nonexistent_directory(self):
        """Test validation of nonexistent directory"""
        is_valid, error = validate_skill_directory("/nonexistent/path")
        self.assertFalse(is_valid)
        self.assertIn("not found", error.lower())

    def test_file_instead_of_directory(self):
        """Test validation when path is a file"""
        with tempfile.NamedTemporaryFile() as tmpfile:
            is_valid, error = validate_skill_directory(tmpfile.name)
            self.assertFalse(is_valid)
            self.assertIn("not a directory", error.lower())

    def test_directory_without_skill_md(self):
        """Test validation of directory without SKILL.md"""
        with tempfile.TemporaryDirectory() as tmpdir:
            is_valid, error = validate_skill_directory(tmpdir)
            self.assertFalse(is_valid)
            self.assertIn("SKILL.md not found", error)


class TestValidateZipFile(unittest.TestCase):
    """Test validate_zip_file function"""

    def test_valid_zip_file(self):
        """Test validation of valid .zip file"""
        with tempfile.TemporaryDirectory() as tmpdir:
            zip_path = Path(tmpdir) / "test-skill.zip"

            # Create a real zip file
            with zipfile.ZipFile(zip_path, 'w') as zf:
                zf.writestr("SKILL.md", "# Test")

            is_valid, error = validate_zip_file(zip_path)
            self.assertTrue(is_valid)
            self.assertIsNone(error)

    def test_nonexistent_file(self):
        """Test validation of nonexistent file"""
        is_valid, error = validate_zip_file("/nonexistent/file.zip")
        self.assertFalse(is_valid)
        self.assertIn("not found", error.lower())

    def test_directory_instead_of_file(self):
        """Test validation when path is a directory"""
        with tempfile.TemporaryDirectory() as tmpdir:
            is_valid, error = validate_zip_file(tmpdir)
            self.assertFalse(is_valid)
            self.assertIn("not a file", error.lower())

    def test_wrong_extension(self):
        """Test validation of file with wrong extension"""
        with tempfile.NamedTemporaryFile(suffix='.txt') as tmpfile:
            is_valid, error = validate_zip_file(tmpfile.name)
            self.assertFalse(is_valid)
            self.assertIn("not a .zip file", error.lower())


class TestPrintUploadInstructions(unittest.TestCase):
    """Test print_upload_instructions function"""

    def test_print_upload_instructions_runs(self):
        """Test that print_upload_instructions executes without error"""
        with tempfile.TemporaryDirectory() as tmpdir:
            zip_path = Path(tmpdir) / "test.zip"
            zip_path.write_text("")

            # Should not raise exception
            try:
                print_upload_instructions(zip_path)
            except Exception as e:
                self.fail(f"print_upload_instructions raised {e}")

    def test_print_upload_instructions_accepts_string_path(self):
        """Test print_upload_instructions accepts string path"""
        with tempfile.TemporaryDirectory() as tmpdir:
            zip_path = str(Path(tmpdir) / "test.zip")
            Path(zip_path).write_text("")

            try:
                print_upload_instructions(zip_path)
            except Exception as e:
                self.fail(f"print_upload_instructions raised {e}")


if __name__ == '__main__':
    unittest.main()
