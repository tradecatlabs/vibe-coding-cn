"""Tests for skip_llms_txt configuration option.

This config option allows users to explicitly skip llms.txt detection and fetching,
which is useful when:
- A site's llms.txt is incomplete or incorrect
- You need specific pages not in llms.txt
- You want to force HTML scraping
"""

import os
import tempfile
import unittest
import logging
from unittest.mock import patch, Mock, MagicMock

from skill_seekers.cli.doc_scraper import DocToSkillConverter


class TestSkipLlmsTxtConfig(unittest.TestCase):
    """Test skip_llms_txt configuration option."""

    def test_default_skip_llms_txt_is_false(self):
        """Test that skip_llms_txt defaults to False when not specified."""
        config = {
            'name': 'test',
            'base_url': 'https://example.com/',
            'selectors': {'main_content': 'article'}
        }

        converter = DocToSkillConverter(config, dry_run=True)
        self.assertFalse(converter.skip_llms_txt)

    def test_skip_llms_txt_can_be_set_true(self):
        """Test that skip_llms_txt can be explicitly set to True."""
        config = {
            'name': 'test',
            'base_url': 'https://example.com/',
            'selectors': {'main_content': 'article'},
            'skip_llms_txt': True
        }

        converter = DocToSkillConverter(config, dry_run=True)
        self.assertTrue(converter.skip_llms_txt)

    def test_skip_llms_txt_can_be_set_false(self):
        """Test that skip_llms_txt can be explicitly set to False."""
        config = {
            'name': 'test',
            'base_url': 'https://example.com/',
            'selectors': {'main_content': 'article'},
            'skip_llms_txt': False
        }

        converter = DocToSkillConverter(config, dry_run=True)
        self.assertFalse(converter.skip_llms_txt)


class TestSkipLlmsTxtSyncBehavior(unittest.TestCase):
    """Test skip_llms_txt behavior in sync scraping mode."""

    def test_llms_txt_tried_when_not_skipped(self):
        """Test that _try_llms_txt is called when skip_llms_txt is False."""
        config = {
            'name': 'test',
            'base_url': 'https://example.com/',
            'selectors': {'main_content': 'article'},
            'skip_llms_txt': False
        }

        original_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                os.chdir(tmpdir)
                converter = DocToSkillConverter(config, dry_run=False)

                with patch.object(converter, '_try_llms_txt', return_value=False) as mock_try:
                    with patch.object(converter, 'scrape_page'):
                        with patch.object(converter, 'save_summary'):
                            converter.scrape_all()
                            mock_try.assert_called_once()
            finally:
                os.chdir(original_cwd)

    def test_llms_txt_skipped_when_skip_true(self):
        """Test that _try_llms_txt is NOT called when skip_llms_txt is True."""
        config = {
            'name': 'test',
            'base_url': 'https://example.com/',
            'selectors': {'main_content': 'article'},
            'skip_llms_txt': True
        }

        original_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                os.chdir(tmpdir)
                converter = DocToSkillConverter(config, dry_run=False)

                with patch.object(converter, '_try_llms_txt') as mock_try:
                    with patch.object(converter, 'scrape_page'):
                        with patch.object(converter, 'save_summary'):
                            converter.scrape_all()
                            mock_try.assert_not_called()
            finally:
                os.chdir(original_cwd)

    def test_llms_txt_skipped_in_dry_run_mode(self):
        """Test that _try_llms_txt is NOT called in dry-run mode regardless of skip setting."""
        config = {
            'name': 'test',
            'base_url': 'https://example.com/',
            'selectors': {'main_content': 'article'},
            'skip_llms_txt': False  # Even when False
        }

        original_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                os.chdir(tmpdir)
                converter = DocToSkillConverter(config, dry_run=True)

                with patch.object(converter, '_try_llms_txt') as mock_try:
                    with patch.object(converter, 'save_summary'):
                        converter.scrape_all()
                        mock_try.assert_not_called()
            finally:
                os.chdir(original_cwd)


class TestSkipLlmsTxtAsyncBehavior(unittest.TestCase):
    """Test skip_llms_txt behavior in async scraping mode."""

    def test_async_llms_txt_tried_when_not_skipped(self):
        """Test that _try_llms_txt is called in async mode when skip_llms_txt is False."""
        config = {
            'name': 'test',
            'base_url': 'https://example.com/',
            'selectors': {'main_content': 'article'},
            'async_mode': True,
            'skip_llms_txt': False
        }

        original_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                os.chdir(tmpdir)
                converter = DocToSkillConverter(config, dry_run=False)

                with patch.object(converter, '_try_llms_txt', return_value=False) as mock_try:
                    with patch.object(converter, 'scrape_page_async', return_value=None):
                        with patch.object(converter, 'save_summary'):
                            converter.scrape_all()
                            mock_try.assert_called_once()
            finally:
                os.chdir(original_cwd)

    def test_async_llms_txt_skipped_when_skip_true(self):
        """Test that _try_llms_txt is NOT called in async mode when skip_llms_txt is True."""
        config = {
            'name': 'test',
            'base_url': 'https://example.com/',
            'selectors': {'main_content': 'article'},
            'async_mode': True,
            'skip_llms_txt': True
        }

        original_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                os.chdir(tmpdir)
                converter = DocToSkillConverter(config, dry_run=False)

                with patch.object(converter, '_try_llms_txt') as mock_try:
                    with patch.object(converter, 'scrape_page_async', return_value=None):
                        with patch.object(converter, 'save_summary'):
                            converter.scrape_all()
                            mock_try.assert_not_called()
            finally:
                os.chdir(original_cwd)


class TestSkipLlmsTxtWithRealConfig(unittest.TestCase):
    """Test skip_llms_txt with real-world config patterns."""

    def test_telegram_bots_config_pattern(self):
        """Test the telegram-bots config pattern which uses skip_llms_txt."""
        config = {
            'name': 'telegram-bots',
            'description': 'Telegram bot documentation',
            'base_url': 'https://core.telegram.org/bots',
            'skip_llms_txt': True,  # Telegram doesn't have useful llms.txt
            'start_urls': [
                'https://core.telegram.org/bots',
                'https://core.telegram.org/bots/api'
            ],
            'selectors': {
                'main_content': '#dev_page_content, main, article',
                'title': 'h1, title',
                'code_blocks': 'pre code, pre'
            }
        }

        converter = DocToSkillConverter(config, dry_run=True)
        self.assertTrue(converter.skip_llms_txt)
        self.assertEqual(converter.name, 'telegram-bots')

    def test_skip_llms_txt_with_multiple_start_urls(self):
        """Test skip_llms_txt works correctly with multiple start URLs."""
        config = {
            'name': 'test-multi',
            'base_url': 'https://example.com/',
            'selectors': {'main_content': 'article'},
            'skip_llms_txt': True,
            'start_urls': [
                'https://example.com/docs/',
                'https://example.com/api/',
                'https://example.com/guide/'
            ]
        }

        converter = DocToSkillConverter(config, dry_run=True)
        self.assertTrue(converter.skip_llms_txt)
        # start_urls are stored in pending_urls deque
        self.assertEqual(len(converter.pending_urls), 3)


class TestSkipLlmsTxtEdgeCases(unittest.TestCase):
    """Test edge cases for skip_llms_txt."""

    def test_skip_llms_txt_with_int_zero_logs_warning(self):
        """Test that integer 0 logs warning and defaults to False."""
        config = {
            'name': 'test',
            'base_url': 'https://example.com/',
            'selectors': {'main_content': 'article'},
            'skip_llms_txt': 0  # Invalid type
        }

        with self.assertLogs('skill_seekers.cli.doc_scraper', level='WARNING') as cm:
            converter = DocToSkillConverter(config, dry_run=True)
            self.assertFalse(converter.skip_llms_txt)
            self.assertTrue(any('Invalid value' in log and '0' in log for log in cm.output))

    def test_skip_llms_txt_with_int_one_logs_warning(self):
        """Test that integer 1 logs warning and defaults to False."""
        config = {
            'name': 'test',
            'base_url': 'https://example.com/',
            'selectors': {'main_content': 'article'},
            'skip_llms_txt': 1  # Invalid type
        }

        with self.assertLogs('skill_seekers.cli.doc_scraper', level='WARNING') as cm:
            converter = DocToSkillConverter(config, dry_run=True)
            self.assertFalse(converter.skip_llms_txt)
            self.assertTrue(any('Invalid value' in log and '1' in log for log in cm.output))

    def test_skip_llms_txt_with_string_logs_warning(self):
        """Test that string values log warning and default to False."""
        config = {
            'name': 'test',
            'base_url': 'https://example.com/',
            'selectors': {'main_content': 'article'},
            'skip_llms_txt': "true"  # Invalid type
        }

        with self.assertLogs('skill_seekers.cli.doc_scraper', level='WARNING') as cm:
            converter = DocToSkillConverter(config, dry_run=True)
            self.assertFalse(converter.skip_llms_txt)
            self.assertTrue(any('Invalid value' in log and 'true' in log for log in cm.output))

    def test_skip_llms_txt_with_none_logs_warning(self):
        """Test that None logs warning and defaults to False."""
        config = {
            'name': 'test',
            'base_url': 'https://example.com/',
            'selectors': {'main_content': 'article'},
            'skip_llms_txt': None  # Invalid type
        }

        with self.assertLogs('skill_seekers.cli.doc_scraper', level='WARNING') as cm:
            converter = DocToSkillConverter(config, dry_run=True)
            self.assertFalse(converter.skip_llms_txt)
            self.assertTrue(any('Invalid value' in log and 'None' in log for log in cm.output))

    def test_scraping_proceeds_when_llms_txt_skipped(self):
        """Test that HTML scraping proceeds normally when llms.txt is skipped."""
        config = {
            'name': 'test',
            'base_url': 'https://example.com/',
            'selectors': {'main_content': 'article'},
            'skip_llms_txt': True
        }

        original_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                os.chdir(tmpdir)
                converter = DocToSkillConverter(config, dry_run=False)

                # Track if scrape_page was called
                scrape_called = []

                def mock_scrape(url):
                    scrape_called.append(url)
                    return None

                with patch.object(converter, 'scrape_page', side_effect=mock_scrape):
                    with patch.object(converter, 'save_summary'):
                        converter.scrape_all()
                        # Should have attempted to scrape the base URL
                        self.assertTrue(len(scrape_called) > 0)
            finally:
                os.chdir(original_cwd)


if __name__ == '__main__':
    unittest.main()
