#!/usr/bin/env python3
"""
Test suite for modern CLI command patterns
Tests that all CLI scripts use correct unified CLI commands in usage messages and print statements
"""

import sys
import os
import unittest
import subprocess
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestModernCLICommands(unittest.TestCase):
    """Test that all CLI scripts use modern unified CLI commands"""

    def test_doc_scraper_uses_modern_commands(self):
        """Test doc_scraper.py uses skill-seekers commands"""
        script_path = Path(__file__).parent.parent / 'src' / 'skill_seekers' / 'cli' / 'doc_scraper.py'

        with open(script_path, 'r') as f:
            content = f.read()

        # Should use modern commands
        self.assertIn('skill-seekers scrape', content)

        # Should NOT use old python3 cli/ pattern
        self.assertNotIn('python3 cli/doc_scraper.py', content)

    def test_enhance_skill_local_uses_modern_commands(self):
        """Test enhance_skill_local.py uses skill-seekers commands"""
        script_path = Path(__file__).parent.parent / 'src' / 'skill_seekers' / 'cli' / 'enhance_skill_local.py'

        with open(script_path, 'r') as f:
            content = f.read()

        # Should use modern commands
        self.assertIn('skill-seekers', content)

        # Should NOT use old python3 cli/ pattern
        self.assertNotIn('python3 cli/enhance_skill_local.py', content)

    def test_estimate_pages_uses_modern_commands(self):
        """Test estimate_pages.py uses skill-seekers commands"""
        script_path = Path(__file__).parent.parent / 'src' / 'skill_seekers' / 'cli' / 'estimate_pages.py'

        with open(script_path, 'r') as f:
            content = f.read()

        # Should use modern commands
        self.assertIn('skill-seekers estimate', content)

        # Should NOT use old python3 cli/ pattern
        self.assertNotIn('python3 cli/estimate_pages.py', content)

    def test_package_skill_uses_modern_commands(self):
        """Test package_skill.py uses skill-seekers commands"""
        script_path = Path(__file__).parent.parent / 'src' / 'skill_seekers' / 'cli' / 'package_skill.py'

        with open(script_path, 'r') as f:
            content = f.read()

        # Should use modern commands
        self.assertIn('skill-seekers package', content)

        # Should NOT use old python3 cli/ pattern
        self.assertNotIn('python3 cli/package_skill.py', content)

    def test_github_scraper_uses_modern_commands(self):
        """Test github_scraper.py uses skill-seekers commands"""
        script_path = Path(__file__).parent.parent / 'src' / 'skill_seekers' / 'cli' / 'github_scraper.py'

        with open(script_path, 'r') as f:
            content = f.read()

        # Should use modern commands
        self.assertIn('skill-seekers', content)

        # Should NOT use old python3 cli/ pattern
        self.assertNotIn('python3 cli/github_scraper.py', content)


class TestUnifiedCLIEntryPoints(unittest.TestCase):
    """Test that unified CLI entry points work correctly"""

    def test_main_cli_help_output(self):
        """Test skill-seekers --help works"""
        try:
            result = subprocess.run(
                ['skill-seekers', '--help'],
                capture_output=True,
                text=True,
                timeout=5
            )

            # Should return successfully
            self.assertIn(result.returncode, [0, 2],
                         f"skill-seekers --help failed with code {result.returncode}")

            # Should show subcommands
            output = result.stdout + result.stderr
            self.assertIn('scrape', output)
            self.assertIn('github', output)
            self.assertIn('package', output)

        except FileNotFoundError:
            # If skill-seekers is not installed, skip this test
            self.skipTest("skill-seekers command not found - install package first")

    def test_main_cli_version_output(self):
        """Test skill-seekers --version works"""
        try:
            result = subprocess.run(
                ['skill-seekers', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )

            # Should return successfully
            self.assertEqual(result.returncode, 0,
                           f"skill-seekers --version failed: {result.stderr}")

            # Should show version
            output = result.stdout + result.stderr
            self.assertIn('2.1.1', output)

        except FileNotFoundError:
            # If skill-seekers is not installed, skip this test
            self.skipTest("skill-seekers command not found - install package first")


class TestNoHardcodedPaths(unittest.TestCase):
    """Test that no scripts have hardcoded absolute paths"""

    def test_no_hardcoded_paths_in_cli_scripts(self):
        """Test that CLI scripts don't have hardcoded paths"""
        cli_dir = Path(__file__).parent.parent / 'src' / 'skill_seekers' / 'cli'

        hardcoded_paths = [
            '/mnt/skills/examples/skill-creator/scripts/',
            '/home/',
            '/Users/',
        ]

        for script_path in cli_dir.glob('*.py'):
            with open(script_path, 'r') as f:
                content = f.read()

            for hardcoded_path in hardcoded_paths:
                self.assertNotIn(hardcoded_path, content,
                               f"{script_path.name} contains hardcoded path: {hardcoded_path}")


class TestPackageStructure(unittest.TestCase):
    """Test that package structure is correct"""

    def test_src_layout_exists(self):
        """Test that src/ layout directory exists"""
        src_dir = Path(__file__).parent.parent / 'src' / 'skill_seekers'
        self.assertTrue(src_dir.exists(), "src/skill_seekers/ directory should exist")

    def test_cli_package_exists(self):
        """Test that CLI package exists in src/"""
        cli_dir = Path(__file__).parent.parent / 'src' / 'skill_seekers' / 'cli'
        self.assertTrue(cli_dir.exists(), "src/skill_seekers/cli/ directory should exist")

        init_file = cli_dir / '__init__.py'
        self.assertTrue(init_file.exists(), "src/skill_seekers/cli/__init__.py should exist")

    def test_mcp_package_exists(self):
        """Test that MCP package exists in src/"""
        mcp_dir = Path(__file__).parent.parent / 'src' / 'skill_seekers' / 'mcp'
        self.assertTrue(mcp_dir.exists(), "src/skill_seekers/mcp/ directory should exist")

        init_file = mcp_dir / '__init__.py'
        self.assertTrue(init_file.exists(), "src/skill_seekers/mcp/__init__.py should exist")

    def test_main_cli_file_exists(self):
        """Test that main.py unified CLI exists"""
        main_file = Path(__file__).parent.parent / 'src' / 'skill_seekers' / 'cli' / 'main.py'
        self.assertTrue(main_file.exists(), "src/skill_seekers/cli/main.py should exist")


if __name__ == '__main__':
    unittest.main()
