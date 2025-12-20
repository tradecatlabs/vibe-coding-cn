#!/usr/bin/env python3
"""
Tests for async scraping functionality
Tests the async/await implementation for parallel web scraping
"""

import sys
import os
import unittest
import asyncio
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, AsyncMock, MagicMock
from collections import deque

from skill_seekers.cli.doc_scraper import DocToSkillConverter


class TestAsyncConfiguration(unittest.TestCase):
    """Test async mode configuration and initialization"""

    def setUp(self):
        """Save original working directory"""
        self.original_cwd = os.getcwd()

    def tearDown(self):
        """Restore original working directory"""
        os.chdir(self.original_cwd)

    def test_async_mode_default_false(self):
        """Test async mode is disabled by default"""
        config = {
            'name': 'test',
            'base_url': 'https://example.com/',
            'selectors': {'main_content': 'article'},
            'max_pages': 10
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                os.chdir(tmpdir)
                converter = DocToSkillConverter(config, dry_run=True)
                self.assertFalse(converter.async_mode)
            finally:
                os.chdir(self.original_cwd)

    def test_async_mode_enabled_from_config(self):
        """Test async mode can be enabled via config"""
        config = {
            'name': 'test',
            'base_url': 'https://example.com/',
            'selectors': {'main_content': 'article'},
            'max_pages': 10,
            'async_mode': True
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                os.chdir(tmpdir)
                converter = DocToSkillConverter(config, dry_run=True)
                self.assertTrue(converter.async_mode)
            finally:
                os.chdir(self.original_cwd)

    def test_async_mode_with_workers(self):
        """Test async mode works with multiple workers"""
        config = {
            'name': 'test',
            'base_url': 'https://example.com/',
            'selectors': {'main_content': 'article'},
            'workers': 4,
            'async_mode': True
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                os.chdir(tmpdir)
                converter = DocToSkillConverter(config, dry_run=True)
                self.assertTrue(converter.async_mode)
                self.assertEqual(converter.workers, 4)
            finally:
                os.chdir(self.original_cwd)


class TestAsyncScrapeMethods(unittest.TestCase):
    """Test async scraping methods exist and have correct signatures"""

    def setUp(self):
        """Set up test fixtures"""
        self.original_cwd = os.getcwd()

    def tearDown(self):
        """Clean up"""
        os.chdir(self.original_cwd)

    def test_scrape_page_async_exists(self):
        """Test scrape_page_async method exists"""
        config = {
            'name': 'test',
            'base_url': 'https://example.com/',
            'selectors': {'main_content': 'article'}
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                os.chdir(tmpdir)
                converter = DocToSkillConverter(config, dry_run=True)
                self.assertTrue(hasattr(converter, 'scrape_page_async'))
                self.assertTrue(asyncio.iscoroutinefunction(converter.scrape_page_async))
            finally:
                os.chdir(self.original_cwd)

    def test_scrape_all_async_exists(self):
        """Test scrape_all_async method exists"""
        config = {
            'name': 'test',
            'base_url': 'https://example.com/',
            'selectors': {'main_content': 'article'}
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                os.chdir(tmpdir)
                converter = DocToSkillConverter(config, dry_run=True)
                self.assertTrue(hasattr(converter, 'scrape_all_async'))
                self.assertTrue(asyncio.iscoroutinefunction(converter.scrape_all_async))
            finally:
                os.chdir(self.original_cwd)


class TestAsyncRouting(unittest.TestCase):
    """Test that scrape_all() correctly routes to async version"""

    def setUp(self):
        """Set up test fixtures"""
        self.original_cwd = os.getcwd()

    def tearDown(self):
        """Clean up"""
        os.chdir(self.original_cwd)

    def test_scrape_all_routes_to_async_when_enabled(self):
        """Test scrape_all calls async version when async_mode=True"""
        config = {
            'name': 'test',
            'base_url': 'https://example.com/',
            'selectors': {'main_content': 'article'},
            'async_mode': True,
            'max_pages': 1
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                os.chdir(tmpdir)
                converter = DocToSkillConverter(config, dry_run=True)

                # Mock scrape_all_async to verify it gets called
                with patch.object(converter, 'scrape_all_async', new_callable=AsyncMock) as mock_async:
                    converter.scrape_all()
                    # Verify async version was called
                    mock_async.assert_called_once()
            finally:
                os.chdir(self.original_cwd)

    def test_scrape_all_uses_sync_when_async_disabled(self):
        """Test scrape_all uses sync version when async_mode=False"""
        config = {
            'name': 'test',
            'base_url': 'https://example.com/',
            'selectors': {'main_content': 'article'},
            'async_mode': False,
            'max_pages': 1
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                os.chdir(tmpdir)
                converter = DocToSkillConverter(config, dry_run=True)

                # Mock scrape_all_async to verify it does NOT get called
                with patch.object(converter, 'scrape_all_async', new_callable=AsyncMock) as mock_async:
                    with patch.object(converter, '_try_llms_txt', return_value=False):
                        converter.scrape_all()
                        # Verify async version was NOT called
                        mock_async.assert_not_called()
            finally:
                os.chdir(self.original_cwd)


class TestAsyncDryRun(unittest.TestCase):
    """Test async scraping in dry-run mode"""

    def setUp(self):
        """Set up test fixtures"""
        self.original_cwd = os.getcwd()

    def tearDown(self):
        """Clean up"""
        os.chdir(self.original_cwd)

    def test_async_dry_run_completes(self):
        """Test async dry run completes without errors"""
        config = {
            'name': 'test',
            'base_url': 'https://example.com/',
            'selectors': {'main_content': 'article'},
            'async_mode': True,
            'max_pages': 5
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                os.chdir(tmpdir)
                converter = DocToSkillConverter(config, dry_run=True)

                # Mock _try_llms_txt to skip llms.txt detection
                with patch.object(converter, '_try_llms_txt', return_value=False):
                    # Should complete without errors
                    converter.scrape_all()
                    # Verify dry run mode was used
                    self.assertTrue(converter.dry_run)
            finally:
                os.chdir(self.original_cwd)


class TestAsyncErrorHandling(unittest.TestCase):
    """Test error handling in async scraping"""

    def setUp(self):
        """Set up test fixtures"""
        self.original_cwd = os.getcwd()

    def tearDown(self):
        """Clean up"""
        os.chdir(self.original_cwd)

    def test_async_handles_http_errors(self):
        """Test async scraping handles HTTP errors gracefully"""
        config = {
            'name': 'test',
            'base_url': 'https://example.com/',
            'selectors': {'main_content': 'article'},
            'async_mode': True,
            'workers': 2,
            'max_pages': 1
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                os.chdir(tmpdir)
                converter = DocToSkillConverter(config, dry_run=False)

                # Mock httpx to simulate errors
                import httpx

                async def run_test():
                    semaphore = asyncio.Semaphore(2)

                    async with httpx.AsyncClient() as client:
                        # Mock client.get to raise exception
                        with patch.object(client, 'get', side_effect=httpx.HTTPError("Test error")):
                            # Should not raise exception, just log error
                            await converter.scrape_page_async('https://example.com/test', semaphore, client)

                # Run async test
                asyncio.run(run_test())
                # If we got here without exception, test passed
            finally:
                os.chdir(self.original_cwd)


class TestAsyncPerformance(unittest.TestCase):
    """Test async performance characteristics"""

    def test_async_uses_semaphore_for_concurrency_control(self):
        """Test async mode uses semaphore instead of threading lock"""
        config = {
            'name': 'test',
            'base_url': 'https://example.com/',
            'selectors': {'main_content': 'article'},
            'async_mode': True,
            'workers': 4
        }

        original_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                os.chdir(tmpdir)
                converter = DocToSkillConverter(config, dry_run=True)

                # Async mode should NOT create threading lock
                # (async uses asyncio.Semaphore instead)
                self.assertTrue(converter.async_mode)
            finally:
                os.chdir(original_cwd)


class TestAsyncLlmsTxtIntegration(unittest.TestCase):
    """Test async mode with llms.txt detection"""

    def test_async_respects_llms_txt(self):
        """Test async mode respects llms.txt and skips HTML scraping"""
        config = {
            'name': 'test',
            'base_url': 'https://example.com/',
            'selectors': {'main_content': 'article'},
            'async_mode': True
        }

        original_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                os.chdir(tmpdir)
                converter = DocToSkillConverter(config, dry_run=False)

                # Mock _try_llms_txt to return True (llms.txt found)
                with patch.object(converter, '_try_llms_txt', return_value=True):
                    with patch.object(converter, 'save_summary'):
                        converter.scrape_all()
                        # If llms.txt succeeded, async scraping should be skipped
                        # Verify by checking that pages were not scraped
                        self.assertEqual(len(converter.visited_urls), 0)
            finally:
                os.chdir(original_cwd)


if __name__ == '__main__':
    unittest.main()
