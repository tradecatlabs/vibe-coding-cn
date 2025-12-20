"""Tests for configurable directory exclusions in GitHub scraper.

Tests Issue #203: Make EXCLUDED_DIRS configurable
"""

import unittest
from unittest.mock import patch, Mock
from skill_seekers.cli.github_scraper import GitHubScraper, EXCLUDED_DIRS


class TestExcludedDirsDefaults(unittest.TestCase):
    """Test default EXCLUDED_DIRS behavior (backward compatibility)."""

    @patch('skill_seekers.cli.github_scraper.Github')
    def test_defaults_when_no_config(self, mock_github):
        """Test that default exclusions are used when no config provided."""
        config = {
            'repo': 'owner/repo'
        }

        scraper = GitHubScraper(config)

        # Should use default EXCLUDED_DIRS
        self.assertEqual(scraper.excluded_dirs, EXCLUDED_DIRS)

    @patch('skill_seekers.cli.github_scraper.Github')
    def test_defaults_exclude_common_dirs(self, mock_github):
        """Test that default exclusions work correctly."""
        config = {
            'repo': 'owner/repo'
        }

        scraper = GitHubScraper(config)

        # Test common directories are excluded
        self.assertTrue(scraper.should_exclude_dir('venv'))
        self.assertTrue(scraper.should_exclude_dir('node_modules'))
        self.assertTrue(scraper.should_exclude_dir('__pycache__'))
        self.assertTrue(scraper.should_exclude_dir('.git'))
        self.assertTrue(scraper.should_exclude_dir('build'))

        # Test normal directories are not excluded
        self.assertFalse(scraper.should_exclude_dir('src'))
        self.assertFalse(scraper.should_exclude_dir('tests'))
        self.assertFalse(scraper.should_exclude_dir('docs'))

    @patch('skill_seekers.cli.github_scraper.Github')
    def test_dot_directories_always_excluded(self, mock_github):
        """Test that directories starting with '.' are always excluded."""
        config = {
            'repo': 'owner/repo'
        }

        scraper = GitHubScraper(config)

        # Dot directories should be excluded (even if not in EXCLUDED_DIRS)
        self.assertTrue(scraper.should_exclude_dir('.hidden'))
        self.assertTrue(scraper.should_exclude_dir('.cache'))
        self.assertTrue(scraper.should_exclude_dir('.vscode'))


class TestExcludedDirsAdditional(unittest.TestCase):
    """Test exclude_dirs_additional (extend mode)."""

    @patch('skill_seekers.cli.github_scraper.Github')
    def test_extend_with_additional_dirs(self, mock_github):
        """Test adding custom exclusions to defaults."""
        config = {
            'repo': 'owner/repo',
            'exclude_dirs_additional': ['proprietary', 'vendor', 'third_party']
        }

        scraper = GitHubScraper(config)

        # Should include both defaults and additional
        self.assertIn('venv', scraper.excluded_dirs)  # Default
        self.assertIn('node_modules', scraper.excluded_dirs)  # Default
        self.assertIn('proprietary', scraper.excluded_dirs)  # Additional
        self.assertIn('vendor', scraper.excluded_dirs)  # Additional
        self.assertIn('third_party', scraper.excluded_dirs)  # Additional

        # Verify total count
        self.assertEqual(
            len(scraper.excluded_dirs),
            len(EXCLUDED_DIRS) + 3
        )

    @patch('skill_seekers.cli.github_scraper.Github')
    def test_extend_excludes_additional_dirs(self, mock_github):
        """Test that additional directories are actually excluded."""
        config = {
            'repo': 'owner/repo',
            'exclude_dirs_additional': ['legacy', 'deprecated']
        }

        scraper = GitHubScraper(config)

        # Additional dirs should be excluded
        self.assertTrue(scraper.should_exclude_dir('legacy'))
        self.assertTrue(scraper.should_exclude_dir('deprecated'))

        # Default dirs still excluded
        self.assertTrue(scraper.should_exclude_dir('venv'))
        self.assertTrue(scraper.should_exclude_dir('node_modules'))

        # Normal dirs not excluded
        self.assertFalse(scraper.should_exclude_dir('src'))

    @patch('skill_seekers.cli.github_scraper.Github')
    def test_extend_with_empty_list(self, mock_github):
        """Test that empty additional list works correctly."""
        config = {
            'repo': 'owner/repo',
            'exclude_dirs_additional': []
        }

        scraper = GitHubScraper(config)

        # Should just have defaults
        self.assertEqual(scraper.excluded_dirs, EXCLUDED_DIRS)


class TestExcludedDirsReplace(unittest.TestCase):
    """Test exclude_dirs (replace mode)."""

    @patch('skill_seekers.cli.github_scraper.Github')
    def test_replace_with_custom_list(self, mock_github):
        """Test replacing default exclusions entirely."""
        config = {
            'repo': 'owner/repo',
            'exclude_dirs': ['node_modules', 'custom_vendor']
        }

        scraper = GitHubScraper(config)

        # Should ONLY have specified dirs
        self.assertEqual(scraper.excluded_dirs, {'node_modules', 'custom_vendor'})
        self.assertEqual(len(scraper.excluded_dirs), 2)

    @patch('skill_seekers.cli.github_scraper.Github')
    def test_replace_excludes_only_specified_dirs(self, mock_github):
        """Test that only specified directories are excluded in replace mode."""
        config = {
            'repo': 'owner/repo',
            'exclude_dirs': ['node_modules', '.git']
        }

        scraper = GitHubScraper(config)

        # Specified dirs should be excluded
        self.assertTrue(scraper.should_exclude_dir('node_modules'))
        # Note: .git would be excluded anyway due to dot prefix
        self.assertTrue(scraper.should_exclude_dir('.git'))

        # Default dirs NOT in our list should NOT be excluded
        self.assertFalse(scraper.should_exclude_dir('venv'))
        self.assertFalse(scraper.should_exclude_dir('__pycache__'))
        self.assertFalse(scraper.should_exclude_dir('build'))

        # Normal dirs still not excluded
        self.assertFalse(scraper.should_exclude_dir('src'))

    @patch('skill_seekers.cli.github_scraper.Github')
    def test_replace_with_empty_list(self, mock_github):
        """Test that empty replace list allows all directories (except dot-prefixed)."""
        config = {
            'repo': 'owner/repo',
            'exclude_dirs': []
        }

        scraper = GitHubScraper(config)

        # No explicit exclusions
        self.assertEqual(scraper.excluded_dirs, set())

        # Nothing explicitly excluded
        self.assertFalse(scraper.should_exclude_dir('venv'))
        self.assertFalse(scraper.should_exclude_dir('node_modules'))
        self.assertFalse(scraper.should_exclude_dir('build'))

        # But dot dirs still excluded (different logic)
        self.assertTrue(scraper.should_exclude_dir('.git'))
        self.assertTrue(scraper.should_exclude_dir('.hidden'))


class TestExcludedDirsPrecedence(unittest.TestCase):
    """Test precedence when both options provided."""

    @patch('skill_seekers.cli.github_scraper.Github')
    def test_replace_takes_precedence_over_additional(self, mock_github):
        """Test that exclude_dirs takes precedence over exclude_dirs_additional."""
        config = {
            'repo': 'owner/repo',
            'exclude_dirs': ['only', 'these'],  # Replace mode
            'exclude_dirs_additional': ['ignored']  # Should be ignored
        }

        scraper = GitHubScraper(config)

        # Should use replace mode (exclude_dirs), ignore additional
        self.assertEqual(scraper.excluded_dirs, {'only', 'these'})
        self.assertNotIn('ignored', scraper.excluded_dirs)
        self.assertNotIn('venv', scraper.excluded_dirs)  # Defaults also ignored


class TestExcludedDirsEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""

    @patch('skill_seekers.cli.github_scraper.Github')
    def test_duplicate_exclusions_in_additional(self, mock_github):
        """Test that duplicates in additional list are handled (set deduplication)."""
        config = {
            'repo': 'owner/repo',
            'exclude_dirs_additional': ['venv', 'custom', 'venv']  # venv is duplicate (default + listed)
        }

        scraper = GitHubScraper(config)

        # Should deduplicate automatically (using set)
        self.assertIn('venv', scraper.excluded_dirs)
        self.assertIn('custom', scraper.excluded_dirs)
        # Count should account for deduplication
        self.assertEqual(
            len(scraper.excluded_dirs),
            len(EXCLUDED_DIRS) + 1  # Only 'custom' is truly additional
        )

    @patch('skill_seekers.cli.github_scraper.Github')
    def test_case_sensitive_exclusions(self, mock_github):
        """Test that exclusions are case-sensitive."""
        config = {
            'repo': 'owner/repo',
            'exclude_dirs': ['Venv', 'NODE_MODULES']
        }

        scraper = GitHubScraper(config)

        # Case-sensitive matching
        self.assertTrue(scraper.should_exclude_dir('Venv'))
        self.assertTrue(scraper.should_exclude_dir('NODE_MODULES'))
        self.assertFalse(scraper.should_exclude_dir('venv'))  # Different case
        self.assertFalse(scraper.should_exclude_dir('node_modules'))  # Different case


class TestExcludedDirsWithLocalRepo(unittest.TestCase):
    """Test exclude_dirs integration with local_repo_path."""

    @patch('skill_seekers.cli.github_scraper.Github')
    def test_exclude_dirs_with_local_repo_path(self, mock_github):
        """Test that exclude_dirs works when local_repo_path is provided."""
        config = {
            'repo': 'owner/repo',
            'local_repo_path': '/tmp/test/repo',
            'exclude_dirs_additional': ['proprietary', 'internal']
        }

        scraper = GitHubScraper(config)

        # Should have both defaults and additional
        self.assertIn('venv', scraper.excluded_dirs)
        self.assertIn('proprietary', scraper.excluded_dirs)
        self.assertIn('internal', scraper.excluded_dirs)

        # Test exclusion works
        self.assertTrue(scraper.should_exclude_dir('proprietary'))
        self.assertTrue(scraper.should_exclude_dir('internal'))
        self.assertTrue(scraper.should_exclude_dir('venv'))

    @patch('skill_seekers.cli.github_scraper.Github')
    def test_replace_mode_with_local_repo_path(self, mock_github):
        """Test that replace mode works with local_repo_path."""
        config = {
            'repo': 'owner/repo',
            'local_repo_path': '/tmp/test/repo',
            'exclude_dirs': ['only_this']
        }

        scraper = GitHubScraper(config)

        # Should ONLY have specified dir
        self.assertEqual(scraper.excluded_dirs, {'only_this'})
        self.assertTrue(scraper.should_exclude_dir('only_this'))
        self.assertFalse(scraper.should_exclude_dir('venv'))


class TestExcludedDirsLogging(unittest.TestCase):
    """Test logging output for exclude_dirs configuration."""

    @patch('skill_seekers.cli.github_scraper.Github')
    @patch('skill_seekers.cli.github_scraper.logger')
    def test_extend_mode_logs_info(self, mock_logger, mock_github):
        """Test that extend mode logs INFO level message."""
        config = {
            'repo': 'owner/repo',
            'exclude_dirs_additional': ['custom1', 'custom2']
        }

        scraper = GitHubScraper(config)

        # Should have logged INFO message
        # Check that info was called with a message about adding custom exclusions
        info_calls = [str(call) for call in mock_logger.info.call_args_list]
        self.assertTrue(any('Added 2 custom directory exclusions' in call for call in info_calls))

    @patch('skill_seekers.cli.github_scraper.Github')
    @patch('skill_seekers.cli.github_scraper.logger')
    def test_replace_mode_logs_warning(self, mock_logger, mock_github):
        """Test that replace mode logs WARNING level message."""
        config = {
            'repo': 'owner/repo',
            'exclude_dirs': ['only', 'these']
        }

        scraper = GitHubScraper(config)

        # Should have logged WARNING message
        warning_calls = [str(call) for call in mock_logger.warning.call_args_list]
        self.assertTrue(any('Using custom directory exclusions' in call and 'defaults overridden' in call for call in warning_calls))

    @patch('skill_seekers.cli.github_scraper.Github')
    @patch('skill_seekers.cli.github_scraper.logger')
    def test_no_config_no_logging(self, mock_logger, mock_github):
        """Test that default mode doesn't log exclude_dirs messages."""
        config = {
            'repo': 'owner/repo'
        }

        scraper = GitHubScraper(config)

        # Should NOT have logged any exclude_dirs messages
        info_calls = [str(call) for call in mock_logger.info.call_args_list]
        warning_calls = [str(call) for call in mock_logger.warning.call_args_list]

        # Filter for exclude_dirs related messages
        exclude_info = [c for c in info_calls if 'directory exclusion' in c]
        exclude_warnings = [c for c in warning_calls if 'directory exclusion' in c]

        self.assertEqual(len(exclude_info), 0)
        self.assertEqual(len(exclude_warnings), 0)


class TestExcludedDirsTypeHandling(unittest.TestCase):
    """Test type handling for exclude_dirs configuration."""

    @patch('skill_seekers.cli.github_scraper.Github')
    def test_exclude_dirs_with_tuple(self, mock_github):
        """Test that tuples are converted to sets correctly."""
        config = {
            'repo': 'owner/repo',
            'exclude_dirs': ('node_modules', 'build')  # Tuple instead of list
        }

        scraper = GitHubScraper(config)

        # Should work with tuples (set() accepts tuples)
        self.assertEqual(scraper.excluded_dirs, {'node_modules', 'build'})

    @patch('skill_seekers.cli.github_scraper.Github')
    def test_exclude_dirs_additional_with_set(self, mock_github):
        """Test that sets work correctly for exclude_dirs_additional."""
        config = {
            'repo': 'owner/repo',
            'exclude_dirs_additional': {'custom1', 'custom2'}  # Set instead of list
        }

        scraper = GitHubScraper(config)

        # Should work with sets
        self.assertIn('custom1', scraper.excluded_dirs)
        self.assertIn('custom2', scraper.excluded_dirs)
        self.assertIn('venv', scraper.excluded_dirs)  # Defaults still there


if __name__ == '__main__':
    unittest.main()
