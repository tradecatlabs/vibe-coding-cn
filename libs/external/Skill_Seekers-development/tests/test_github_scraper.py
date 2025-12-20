#!/usr/bin/env python3
"""
Tests for GitHub Scraper (cli/github_scraper.py)

Tests cover:
- GitHubScraper initialization and configuration (C1.1)
- README extraction (C1.2)
- Language detection (C1.4)
- GitHub Issues extraction (C1.7)
- CHANGELOG extraction (C1.8)
- GitHub Releases extraction (C1.9)
- GitHubToSkillConverter and skill building (C1.10)
- Authentication handling
- Error handling and edge cases
"""

import unittest
import sys
import json
import tempfile
import shutil
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

try:
    from github import Github, GithubException
    PYGITHUB_AVAILABLE = True
except ImportError:
    PYGITHUB_AVAILABLE = False


class TestGitHubScraperInitialization(unittest.TestCase):
    """Test GitHubScraper initialization and configuration (C1.1)"""

    def setUp(self):
        if not PYGITHUB_AVAILABLE:
            self.skipTest("PyGithub not installed")
        from skill_seekers.cli.github_scraper import GitHubScraper
        self.GitHubScraper = GitHubScraper

        # Create temporary directory for test output
        self.temp_dir = tempfile.mkdtemp()
        self.output_dir = Path(self.temp_dir)

    def tearDown(self):
        # Clean up temporary directory
        if hasattr(self, 'temp_dir'):
            shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_init_with_repo_name(self):
        """Test initialization with repository name"""
        config = {
            'repo': 'facebook/react',
            'name': 'react',
            'github_token': None
        }

        scraper = self.GitHubScraper(config)

        self.assertEqual(scraper.repo_name, 'facebook/react')
        self.assertEqual(scraper.name, 'react')
        self.assertIsNotNone(scraper.github)

    def test_init_with_token_from_config(self):
        """Test initialization with token from config"""
        config = {
            'repo': 'facebook/react',
            'name': 'react',
            'github_token': 'test_token_123'
        }

        with patch('skill_seekers.cli.github_scraper.Github') as mock_github:
            scraper = self.GitHubScraper(config)
            mock_github.assert_called_once_with('test_token_123')

    def test_init_with_token_from_env(self):
        """Test initialization with token from environment variable"""
        config = {
            'repo': 'facebook/react',
            'name': 'react',
            'github_token': None
        }

        with patch.dict(os.environ, {'GITHUB_TOKEN': 'env_token_456'}):
            with patch('skill_seekers.cli.github_scraper.Github') as mock_github:
                scraper = self.GitHubScraper(config)
                mock_github.assert_called_once_with('env_token_456')

    def test_init_without_token(self):
        """Test initialization without authentication"""
        config = {
            'repo': 'facebook/react',
            'name': 'react',
            'github_token': None
        }

        with patch('skill_seekers.cli.github_scraper.Github') as mock_github:
            with patch.dict(os.environ, {}, clear=True):
                scraper = self.GitHubScraper(config)
                # Should create unauthenticated client
                self.assertIsNotNone(scraper.github)

    def test_token_priority_env_over_config(self):
        """Test that GITHUB_TOKEN env var takes priority over config"""
        config = {
            'repo': 'facebook/react',
            'name': 'react',
            'github_token': 'config_token'
        }

        with patch.dict(os.environ, {'GITHUB_TOKEN': 'env_token'}):
            scraper = self.GitHubScraper(config)
            token = scraper._get_token()
            self.assertEqual(token, 'env_token')


class TestREADMEExtraction(unittest.TestCase):
    """Test README extraction (C1.2)"""

    def setUp(self):
        if not PYGITHUB_AVAILABLE:
            self.skipTest("PyGithub not installed")
        from skill_seekers.cli.github_scraper import GitHubScraper
        self.GitHubScraper = GitHubScraper

    def test_extract_readme_success(self):
        """Test successful README extraction"""
        config = {
            'repo': 'facebook/react',
            'name': 'react',
            'github_token': None
        }

        mock_content = Mock()
        mock_content.decoded_content = b'# React\n\nA JavaScript library'

        with patch('skill_seekers.cli.github_scraper.Github'):
            scraper = self.GitHubScraper(config)
            scraper.repo = Mock()
            scraper.repo.get_contents.return_value = mock_content

            scraper._extract_readme()

            self.assertIn('readme', scraper.extracted_data)
            self.assertEqual(scraper.extracted_data['readme'], '# React\n\nA JavaScript library')

    def test_extract_readme_tries_multiple_locations(self):
        """Test that README extraction tries multiple file locations"""
        config = {
            'repo': 'facebook/react',
            'name': 'react',
            'github_token': None
        }

        with patch('skill_seekers.cli.github_scraper.Github'):
            scraper = self.GitHubScraper(config)
            scraper.repo = Mock()

            # Make first attempts fail, succeed on third
            def side_effect(path):
                if path in ['README.md', 'README.rst']:
                    raise GithubException(404, 'Not found')
                mock_content = Mock()
                mock_content.decoded_content = b'# README'
                return mock_content

            scraper.repo.get_contents.side_effect = side_effect

            scraper._extract_readme()

            # Should have tried multiple paths
            self.assertGreaterEqual(scraper.repo.get_contents.call_count, 1)

    def test_extract_readme_not_found(self):
        """Test README extraction when no README exists"""
        config = {
            'repo': 'test/norepo',
            'name': 'norepo',
            'github_token': None
        }

        with patch('skill_seekers.cli.github_scraper.Github'):
            scraper = self.GitHubScraper(config)
            scraper.repo = Mock()
            scraper.repo.get_contents.side_effect = GithubException(404, 'Not found')

            scraper._extract_readme()

            # Should not crash, just log warning (readme initialized as empty string)
            self.assertEqual(scraper.extracted_data['readme'], '')


class TestLanguageDetection(unittest.TestCase):
    """Test language detection (C1.4)"""

    def setUp(self):
        if not PYGITHUB_AVAILABLE:
            self.skipTest("PyGithub not installed")
        from skill_seekers.cli.github_scraper import GitHubScraper
        self.GitHubScraper = GitHubScraper

    def test_extract_languages_success(self):
        """Test successful language detection"""
        config = {
            'repo': 'facebook/react',
            'name': 'react',
            'github_token': None
        }

        with patch('skill_seekers.cli.github_scraper.Github'):
            scraper = self.GitHubScraper(config)
            scraper.repo = Mock()
            scraper.repo.get_languages.return_value = {
                'JavaScript': 8000,
                'TypeScript': 2000
            }

            scraper._extract_languages()

            self.assertIn('languages', scraper.extracted_data)
            self.assertIn('JavaScript', scraper.extracted_data['languages'])
            self.assertIn('TypeScript', scraper.extracted_data['languages'])

            # Check percentages
            js_data = scraper.extracted_data['languages']['JavaScript']
            self.assertEqual(js_data['bytes'], 8000)
            self.assertEqual(js_data['percentage'], 80.0)

            ts_data = scraper.extracted_data['languages']['TypeScript']
            self.assertEqual(ts_data['bytes'], 2000)
            self.assertEqual(ts_data['percentage'], 20.0)

    def test_extract_languages_empty(self):
        """Test language detection with no languages"""
        config = {
            'repo': 'test/norepo',
            'name': 'norepo',
            'github_token': None
        }

        with patch('skill_seekers.cli.github_scraper.Github'):
            scraper = self.GitHubScraper(config)
            scraper.repo = Mock()
            scraper.repo.get_languages.return_value = {}

            scraper._extract_languages()

            self.assertIn('languages', scraper.extracted_data)
            self.assertEqual(scraper.extracted_data['languages'], {})


class TestIssuesExtraction(unittest.TestCase):
    """Test GitHub Issues extraction (C1.7)"""

    def setUp(self):
        if not PYGITHUB_AVAILABLE:
            self.skipTest("PyGithub not installed")
        from skill_seekers.cli.github_scraper import GitHubScraper
        self.GitHubScraper = GitHubScraper

    def test_extract_issues_success(self):
        """Test successful issues extraction"""
        config = {
            'repo': 'facebook/react',
            'name': 'react',
            'github_token': None,
            'max_issues': 10
        }

        # Create mock issues
        mock_label1 = Mock()
        mock_label1.name = 'bug'
        mock_label2 = Mock()
        mock_label2.name = 'high-priority'

        mock_milestone = Mock()
        mock_milestone.title = 'v18.0'

        mock_issue1 = Mock()
        mock_issue1.number = 123
        mock_issue1.title = 'Bug in useState'
        mock_issue1.state = 'open'
        mock_issue1.labels = [mock_label1, mock_label2]
        mock_issue1.milestone = mock_milestone
        mock_issue1.created_at = datetime(2023, 1, 1)
        mock_issue1.updated_at = datetime(2023, 1, 2)
        mock_issue1.closed_at = None
        mock_issue1.html_url = 'https://github.com/facebook/react/issues/123'
        mock_issue1.body = 'Issue description'
        mock_issue1.pull_request = None

        mock_label3 = Mock()
        mock_label3.name = 'enhancement'

        mock_issue2 = Mock()
        mock_issue2.number = 124
        mock_issue2.title = 'Feature request'
        mock_issue2.state = 'closed'
        mock_issue2.labels = [mock_label3]
        mock_issue2.milestone = None
        mock_issue2.created_at = datetime(2023, 1, 3)
        mock_issue2.updated_at = datetime(2023, 1, 4)
        mock_issue2.closed_at = datetime(2023, 1, 5)
        mock_issue2.html_url = 'https://github.com/facebook/react/issues/124'
        mock_issue2.body = 'Feature description'
        mock_issue2.pull_request = None

        with patch('skill_seekers.cli.github_scraper.Github'):
            scraper = self.GitHubScraper(config)
            scraper.repo = Mock()
            scraper.repo.get_issues.return_value = [mock_issue1, mock_issue2]

            scraper._extract_issues()

            self.assertIn('issues', scraper.extracted_data)
            issues = scraper.extracted_data['issues']
            self.assertEqual(len(issues), 2)

            # Check first issue
            self.assertEqual(issues[0]['number'], 123)
            self.assertEqual(issues[0]['title'], 'Bug in useState')
            self.assertEqual(issues[0]['state'], 'open')
            self.assertEqual(issues[0]['labels'], ['bug', 'high-priority'])
            self.assertEqual(issues[0]['milestone'], 'v18.0')

            # Check second issue
            self.assertEqual(issues[1]['number'], 124)
            self.assertEqual(issues[1]['state'], 'closed')
            self.assertIsNone(issues[1]['milestone'])

    def test_extract_issues_filters_pull_requests(self):
        """Test that pull requests are filtered out from issues"""
        config = {
            'repo': 'facebook/react',
            'name': 'react',
            'github_token': None,
            'max_issues': 10
        }

        # Create mock issue (need all required attributes)
        mock_issue = Mock()
        mock_issue.number = 123
        mock_issue.title = 'Real issue'
        mock_issue.state = 'open'
        mock_issue.labels = []
        mock_issue.milestone = None
        mock_issue.created_at = datetime(2023, 1, 1)
        mock_issue.updated_at = datetime(2023, 1, 2)
        mock_issue.closed_at = None
        mock_issue.html_url = 'https://github.com/test/repo/issues/123'
        mock_issue.body = 'Issue body'
        mock_issue.pull_request = None

        mock_pr = Mock()
        mock_pr.number = 124
        mock_pr.title = 'Pull request'
        mock_pr.pull_request = Mock()  # Has pull_request attribute

        with patch('skill_seekers.cli.github_scraper.Github'):
            scraper = self.GitHubScraper(config)
            scraper.repo = Mock()
            scraper.repo.get_issues.return_value = [mock_issue, mock_pr]

            scraper._extract_issues()

            issues = scraper.extracted_data['issues']
            # Should only have the real issue, not the PR
            self.assertEqual(len(issues), 1)
            self.assertEqual(issues[0]['number'], 123)

    def test_extract_issues_respects_max_limit(self):
        """Test that max_issues limit is respected"""
        config = {
            'repo': 'facebook/react',
            'name': 'react',
            'github_token': None,
            'max_issues': 2
        }

        # Create 5 mock issues
        mock_issues = []
        for i in range(5):
            mock_issue = Mock()
            mock_issue.number = i
            mock_issue.title = f'Issue {i}'
            mock_issue.state = 'open'
            mock_issue.labels = []
            mock_issue.milestone = None
            mock_issue.created_at = datetime(2023, 1, 1)
            mock_issue.updated_at = datetime(2023, 1, 2)
            mock_issue.closed_at = None
            mock_issue.html_url = f'https://github.com/test/repo/issues/{i}'
            mock_issue.body = None
            mock_issue.pull_request = None
            mock_issues.append(mock_issue)

        with patch('skill_seekers.cli.github_scraper.Github'):
            scraper = self.GitHubScraper(config)
            scraper.repo = Mock()
            scraper.repo.get_issues.return_value = mock_issues

            scraper._extract_issues()

            issues = scraper.extracted_data['issues']
            # Should only extract first 2 issues
            self.assertEqual(len(issues), 2)


class TestChangelogExtraction(unittest.TestCase):
    """Test CHANGELOG extraction (C1.8)"""

    def setUp(self):
        if not PYGITHUB_AVAILABLE:
            self.skipTest("PyGithub not installed")
        from skill_seekers.cli.github_scraper import GitHubScraper
        self.GitHubScraper = GitHubScraper

    def test_extract_changelog_success(self):
        """Test successful CHANGELOG extraction"""
        config = {
            'repo': 'facebook/react',
            'name': 'react',
            'github_token': None
        }

        mock_content = Mock()
        mock_content.decoded_content = b'# Changelog\n\n## v1.0.0\n- Initial release'

        with patch('skill_seekers.cli.github_scraper.Github'):
            scraper = self.GitHubScraper(config)
            scraper.repo = Mock()
            scraper.repo.get_contents.return_value = mock_content

            scraper._extract_changelog()

            self.assertIn('changelog', scraper.extracted_data)
            self.assertIn('Initial release', scraper.extracted_data['changelog'])

    def test_extract_changelog_tries_multiple_locations(self):
        """Test that CHANGELOG extraction tries multiple file locations"""
        config = {
            'repo': 'facebook/react',
            'name': 'react',
            'github_token': None
        }

        with patch('skill_seekers.cli.github_scraper.Github'):
            scraper = self.GitHubScraper(config)
            scraper.repo = Mock()

            # Make first attempts fail
            call_count = {'count': 0}

            def side_effect(path):
                call_count['count'] += 1
                if path in ['CHANGELOG.md', 'CHANGES.md']:
                    raise GithubException(404, 'Not found')
                mock_content = Mock()
                mock_content.decoded_content = b'# History'
                return mock_content

            scraper.repo.get_contents.side_effect = side_effect

            scraper._extract_changelog()

            # Should have tried multiple paths
            self.assertGreaterEqual(call_count['count'], 1)

    def test_extract_changelog_not_found(self):
        """Test CHANGELOG extraction when no changelog exists"""
        config = {
            'repo': 'test/norepo',
            'name': 'norepo',
            'github_token': None
        }

        with patch('skill_seekers.cli.github_scraper.Github'):
            scraper = self.GitHubScraper(config)
            scraper.repo = Mock()
            scraper.repo.get_contents.side_effect = GithubException(404, 'Not found')

            scraper._extract_changelog()

            # Should not crash, just log warning (changelog initialized as empty string)
            self.assertEqual(scraper.extracted_data['changelog'], '')


class TestReleasesExtraction(unittest.TestCase):
    """Test GitHub Releases extraction (C1.9)"""

    def setUp(self):
        if not PYGITHUB_AVAILABLE:
            self.skipTest("PyGithub not installed")
        from skill_seekers.cli.github_scraper import GitHubScraper
        self.GitHubScraper = GitHubScraper

    def test_extract_releases_success(self):
        """Test successful releases extraction"""
        config = {
            'repo': 'facebook/react',
            'name': 'react',
            'github_token': None
        }

        # Create mock releases
        mock_release1 = Mock()
        mock_release1.tag_name = 'v18.0.0'
        mock_release1.title = 'React 18.0.0'
        mock_release1.body = 'New features:\n- Concurrent rendering'
        mock_release1.draft = False
        mock_release1.prerelease = False
        mock_release1.created_at = datetime(2023, 3, 1)
        mock_release1.published_at = datetime(2023, 3, 1)
        mock_release1.html_url = 'https://github.com/facebook/react/releases/tag/v18.0.0'
        mock_release1.tarball_url = 'https://github.com/facebook/react/archive/v18.0.0.tar.gz'
        mock_release1.zipball_url = 'https://github.com/facebook/react/archive/v18.0.0.zip'

        mock_release2 = Mock()
        mock_release2.tag_name = 'v18.0.0-rc.0'
        mock_release2.title = 'React 18.0.0 RC'
        mock_release2.body = 'Release candidate'
        mock_release2.draft = False
        mock_release2.prerelease = True
        mock_release2.created_at = datetime(2023, 2, 1)
        mock_release2.published_at = datetime(2023, 2, 1)
        mock_release2.html_url = 'https://github.com/facebook/react/releases/tag/v18.0.0-rc.0'
        mock_release2.tarball_url = 'https://github.com/facebook/react/archive/v18.0.0-rc.0.tar.gz'
        mock_release2.zipball_url = 'https://github.com/facebook/react/archive/v18.0.0-rc.0.zip'

        with patch('skill_seekers.cli.github_scraper.Github'):
            scraper = self.GitHubScraper(config)
            scraper.repo = Mock()
            scraper.repo.get_releases.return_value = [mock_release1, mock_release2]

            scraper._extract_releases()

            self.assertIn('releases', scraper.extracted_data)
            releases = scraper.extracted_data['releases']
            self.assertEqual(len(releases), 2)

            # Check first release
            self.assertEqual(releases[0]['tag_name'], 'v18.0.0')
            self.assertEqual(releases[0]['name'], 'React 18.0.0')
            self.assertFalse(releases[0]['draft'])
            self.assertFalse(releases[0]['prerelease'])
            self.assertIn('Concurrent rendering', releases[0]['body'])

            # Check second release (prerelease)
            self.assertEqual(releases[1]['tag_name'], 'v18.0.0-rc.0')
            self.assertTrue(releases[1]['prerelease'])

    def test_extract_releases_empty(self):
        """Test releases extraction with no releases"""
        config = {
            'repo': 'test/norepo',
            'name': 'norepo',
            'github_token': None
        }

        with patch('skill_seekers.cli.github_scraper.Github'):
            scraper = self.GitHubScraper(config)
            scraper.repo = Mock()
            scraper.repo.get_releases.return_value = []

            scraper._extract_releases()

            self.assertIn('releases', scraper.extracted_data)
            self.assertEqual(scraper.extracted_data['releases'], [])


class TestGitHubToSkillConverter(unittest.TestCase):
    """Test GitHubToSkillConverter and skill building (C1.10)"""

    def setUp(self):
        if not PYGITHUB_AVAILABLE:
            self.skipTest("PyGithub not installed")
        from skill_seekers.cli.github_scraper import GitHubToSkillConverter
        self.GitHubToSkillConverter = GitHubToSkillConverter

        # Create temporary directory for test output
        self.temp_dir = tempfile.mkdtemp()
        self.output_dir = Path(self.temp_dir)

        # Create mock data file
        self.data_file = self.output_dir / "test_github_data.json"
        self.mock_data = {
            'repo_info': {
                'name': 'react',
                'full_name': 'facebook/react',
                'description': 'A JavaScript library',
                'stars': 200000,
                'language': 'JavaScript'
            },
            'readme': '# React\n\nA JavaScript library for building user interfaces.',
            'languages': {
                'JavaScript': {'bytes': 8000, 'percentage': 80.0},
                'TypeScript': {'bytes': 2000, 'percentage': 20.0}
            },
            'issues': [
                {
                    'number': 123,
                    'title': 'Bug in useState',
                    'state': 'open',
                    'labels': ['bug'],
                    'milestone': 'v18.0',
                    'created_at': '2023-01-01T10:00:00',
                    'updated_at': '2023-01-02T10:00:00',
                    'closed_at': None,
                    'url': 'https://github.com/facebook/react/issues/123',
                    'body': 'Issue description'
                }
            ],
            'changelog': '# Changelog\n\n## v18.0.0\n- New features',
            'releases': [
                {
                    'tag_name': 'v18.0.0',
                    'name': 'React 18.0.0',
                    'body': 'Release notes',
                    'published_at': '2023-03-01T10:00:00',
                    'prerelease': False,
                    'draft': False,
                    'url': 'https://github.com/facebook/react/releases/tag/v18.0.0'
                }
            ]
        }

        with open(self.data_file, 'w') as f:
            json.dump(self.mock_data, f)

    def tearDown(self):
        # Clean up temporary directory
        if hasattr(self, 'temp_dir'):
            shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_init_loads_data(self):
        """Test that converter loads data file on initialization"""
        config = {
            'repo': 'facebook/react',
            'name': 'test',
            'description': 'Test skill'
        }

        # Override data file path
        with patch('skill_seekers.cli.github_scraper.GitHubToSkillConverter.__init__') as mock_init:
            mock_init.return_value = None
            converter = self.GitHubToSkillConverter(config)
            converter.data_file = str(self.data_file)
            converter.data = converter._load_data()

            self.assertIn('repo_info', converter.data)
            self.assertEqual(converter.data['repo_info']['name'], 'react')

    def test_build_skill_creates_directory_structure(self):
        """Test that build_skill creates proper directory structure"""
        # Create data file in expected location
        data_file_path = self.output_dir / 'test_github_data.json'
        with open(data_file_path, 'w') as f:
            json.dump(self.mock_data, f)

        config = {
            'repo': 'facebook/react',
            'name': 'test',
            'description': 'Test skill'
        }

        # Patch the paths to use our temp directory
        with patch('skill_seekers.cli.github_scraper.GitHubToSkillConverter._load_data') as mock_load:
            mock_load.return_value = self.mock_data
            converter = self.GitHubToSkillConverter(config)
            converter.skill_dir = str(self.output_dir / 'test_skill')
            converter.data = self.mock_data

            converter.build_skill()

            skill_dir = Path(converter.skill_dir)
            self.assertTrue(skill_dir.exists())
            self.assertTrue((skill_dir / 'SKILL.md').exists())
            self.assertTrue((skill_dir / 'references').exists())


class TestErrorHandling(unittest.TestCase):
    """Test error handling and edge cases"""

    def setUp(self):
        if not PYGITHUB_AVAILABLE:
            self.skipTest("PyGithub not installed")
        from skill_seekers.cli.github_scraper import GitHubScraper
        self.GitHubScraper = GitHubScraper

    def test_invalid_repo_name(self):
        """Test handling of invalid repository name"""
        config = {
            'repo': 'invalid_repo_format',
            'name': 'test',
            'github_token': None
        }

        with patch('skill_seekers.cli.github_scraper.Github'):
            scraper = self.GitHubScraper(config)
            scraper.repo = None
            scraper.github.get_repo = Mock(side_effect=GithubException(404, 'Not found'))

            # Should raise ValueError with helpful message
            with self.assertRaises(ValueError) as context:
                scraper._fetch_repository()

            self.assertIn('Repository not found', str(context.exception))

    def test_rate_limit_error(self):
        """Test handling of rate limit errors"""
        config = {
            'repo': 'facebook/react',
            'name': 'react',
            'github_token': None,
            'max_issues': 10
        }

        with patch('skill_seekers.cli.github_scraper.Github'):
            scraper = self.GitHubScraper(config)
            scraper.repo = Mock()
            scraper.repo.get_issues.side_effect = GithubException(403, 'Rate limit exceeded')

            # Should handle gracefully and log warning
            scraper._extract_issues()
            # Should not crash, just log warning


if __name__ == '__main__':
    unittest.main()
