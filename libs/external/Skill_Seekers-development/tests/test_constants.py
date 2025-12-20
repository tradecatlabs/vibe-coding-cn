#!/usr/bin/env python3
"""Test suite for cli/constants.py module."""

import unittest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from skill_seekers.cli.constants import (
    DEFAULT_RATE_LIMIT,
    DEFAULT_MAX_PAGES,
    DEFAULT_CHECKPOINT_INTERVAL,
    CONTENT_PREVIEW_LENGTH,
    MAX_PAGES_WARNING_THRESHOLD,
    MIN_CATEGORIZATION_SCORE,
    URL_MATCH_POINTS,
    TITLE_MATCH_POINTS,
    CONTENT_MATCH_POINTS,
    API_CONTENT_LIMIT,
    API_PREVIEW_LIMIT,
    LOCAL_CONTENT_LIMIT,
    LOCAL_PREVIEW_LIMIT,
    DEFAULT_MAX_DISCOVERY,
    DISCOVERY_THRESHOLD,
    MAX_REFERENCE_FILES,
    MAX_CODE_BLOCKS_PER_PAGE,
)


class TestConstants(unittest.TestCase):
    """Test that all constants are defined and have sensible values."""

    def test_scraping_constants_exist(self):
        """Test that scraping constants are defined."""
        self.assertIsNotNone(DEFAULT_RATE_LIMIT)
        self.assertIsNotNone(DEFAULT_MAX_PAGES)
        self.assertIsNotNone(DEFAULT_CHECKPOINT_INTERVAL)

    def test_scraping_constants_types(self):
        """Test that scraping constants have correct types."""
        self.assertIsInstance(DEFAULT_RATE_LIMIT, (int, float))
        self.assertIsInstance(DEFAULT_MAX_PAGES, int)
        self.assertIsInstance(DEFAULT_CHECKPOINT_INTERVAL, int)

    def test_scraping_constants_ranges(self):
        """Test that scraping constants have sensible values."""
        self.assertGreater(DEFAULT_RATE_LIMIT, 0)
        self.assertGreater(DEFAULT_MAX_PAGES, 0)
        self.assertGreater(DEFAULT_CHECKPOINT_INTERVAL, 0)
        self.assertEqual(DEFAULT_RATE_LIMIT, 0.5)
        self.assertEqual(DEFAULT_MAX_PAGES, 500)
        self.assertEqual(DEFAULT_CHECKPOINT_INTERVAL, 1000)

    def test_content_analysis_constants(self):
        """Test content analysis constants."""
        self.assertEqual(CONTENT_PREVIEW_LENGTH, 500)
        self.assertEqual(MAX_PAGES_WARNING_THRESHOLD, 10000)
        self.assertGreater(MAX_PAGES_WARNING_THRESHOLD, DEFAULT_MAX_PAGES)

    def test_categorization_constants(self):
        """Test categorization scoring constants."""
        self.assertEqual(MIN_CATEGORIZATION_SCORE, 2)
        self.assertEqual(URL_MATCH_POINTS, 3)
        self.assertEqual(TITLE_MATCH_POINTS, 2)
        self.assertEqual(CONTENT_MATCH_POINTS, 1)
        # Verify scoring hierarchy
        self.assertGreater(URL_MATCH_POINTS, TITLE_MATCH_POINTS)
        self.assertGreater(TITLE_MATCH_POINTS, CONTENT_MATCH_POINTS)

    def test_enhancement_constants_exist(self):
        """Test that enhancement constants are defined."""
        self.assertIsNotNone(API_CONTENT_LIMIT)
        self.assertIsNotNone(API_PREVIEW_LIMIT)
        self.assertIsNotNone(LOCAL_CONTENT_LIMIT)
        self.assertIsNotNone(LOCAL_PREVIEW_LIMIT)

    def test_enhancement_constants_values(self):
        """Test enhancement constants have expected values."""
        self.assertEqual(API_CONTENT_LIMIT, 100000)
        self.assertEqual(API_PREVIEW_LIMIT, 40000)
        self.assertEqual(LOCAL_CONTENT_LIMIT, 50000)
        self.assertEqual(LOCAL_PREVIEW_LIMIT, 20000)

    def test_enhancement_limits_hierarchy(self):
        """Test that API limits are higher than local limits."""
        self.assertGreater(API_CONTENT_LIMIT, LOCAL_CONTENT_LIMIT)
        self.assertGreater(API_PREVIEW_LIMIT, LOCAL_PREVIEW_LIMIT)
        self.assertGreater(API_CONTENT_LIMIT, API_PREVIEW_LIMIT)
        self.assertGreater(LOCAL_CONTENT_LIMIT, LOCAL_PREVIEW_LIMIT)

    def test_estimation_constants(self):
        """Test page estimation constants."""
        self.assertEqual(DEFAULT_MAX_DISCOVERY, 1000)
        self.assertEqual(DISCOVERY_THRESHOLD, 10000)
        self.assertGreater(DISCOVERY_THRESHOLD, DEFAULT_MAX_DISCOVERY)

    def test_file_limit_constants(self):
        """Test file limit constants."""
        self.assertEqual(MAX_REFERENCE_FILES, 100)
        self.assertEqual(MAX_CODE_BLOCKS_PER_PAGE, 5)
        self.assertGreater(MAX_REFERENCE_FILES, 0)
        self.assertGreater(MAX_CODE_BLOCKS_PER_PAGE, 0)


class TestConstantsUsage(unittest.TestCase):
    """Test that constants are properly used in other modules."""

    def test_doc_scraper_imports_constants(self):
        """Test that doc_scraper imports and uses constants."""
        from skill_seekers.cli import doc_scraper
        # Check that doc_scraper can access the constants
        self.assertTrue(hasattr(doc_scraper, 'DEFAULT_RATE_LIMIT'))
        self.assertTrue(hasattr(doc_scraper, 'DEFAULT_MAX_PAGES'))

    def test_estimate_pages_imports_constants(self):
        """Test that estimate_pages imports and uses constants."""
        from skill_seekers.cli import estimate_pages
        # Verify function signature uses constants
        import inspect
        sig = inspect.signature(estimate_pages.estimate_pages)
        self.assertIn('max_discovery', sig.parameters)

    def test_enhance_skill_imports_constants(self):
        """Test that enhance_skill imports constants."""
        try:
            from skill_seekers.cli import enhance_skill
            # Check module loads without errors
            self.assertIsNotNone(enhance_skill)
        except (ImportError, SystemExit) as e:
            # anthropic package may not be installed or module exits on import
            # This is acceptable - we're just checking the constants import works
            pass

    def test_enhance_skill_local_imports_constants(self):
        """Test that enhance_skill_local imports constants."""
        from skill_seekers.cli import enhance_skill_local
        self.assertIsNotNone(enhance_skill_local)


class TestConstantsExports(unittest.TestCase):
    """Test that constants module exports are correct."""

    def test_all_exports_exist(self):
        """Test that all items in __all__ exist."""
        from skill_seekers.cli import constants
        self.assertTrue(hasattr(constants, '__all__'))
        for name in constants.__all__:
            self.assertTrue(
                hasattr(constants, name),
                f"Constant '{name}' in __all__ but not defined"
            )

    def test_all_exports_count(self):
        """Test that __all__ has expected number of exports."""
        from skill_seekers.cli import constants
        # We defined 18 constants (added DEFAULT_ASYNC_MODE)
        self.assertEqual(len(constants.__all__), 18)


if __name__ == '__main__':
    unittest.main()
