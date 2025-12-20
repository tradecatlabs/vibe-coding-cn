#!/usr/bin/env python3
"""
Test suite for configuration validation
Tests the validate_config() function with various valid and invalid configs
"""

import sys
import os
import unittest

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skill_seekers.cli.doc_scraper import validate_config


class TestConfigValidation(unittest.TestCase):
    """Test configuration validation"""

    def test_valid_minimal_config(self):
        """Test valid minimal configuration"""
        config = {
            'name': 'test-skill',
            'base_url': 'https://example.com/'
        }
        errors, _ = validate_config(config)
        # Should have warnings about missing selectors, but no critical errors
        self.assertIsInstance(errors, list)

    def test_valid_complete_config(self):
        """Test valid complete configuration"""
        config = {
            'name': 'godot',
            'base_url': 'https://docs.godotengine.org/en/stable/',
            'description': 'Godot Engine documentation',
            'selectors': {
                'main_content': 'div[role="main"]',
                'title': 'title',
                'code_blocks': 'pre code'
            },
            'url_patterns': {
                'include': ['/guide/', '/api/'],
                'exclude': ['/blog/']
            },
            'categories': {
                'getting_started': ['intro', 'tutorial'],
                'api': ['api', 'reference']
            },
            'rate_limit': 0.5,
            'max_pages': 500
        }
        errors, _ = validate_config(config)
        self.assertEqual(len(errors), 0, f"Valid config should have no errors, got: {errors}")

    def test_missing_name(self):
        """Test missing required field 'name'"""
        config = {
            'base_url': 'https://example.com/'
        }
        errors, _ = validate_config(config)
        self.assertTrue(any('name' in error.lower() for error in errors))

    def test_missing_base_url(self):
        """Test missing required field 'base_url'"""
        config = {
            'name': 'test'
        }
        errors, _ = validate_config(config)
        self.assertTrue(any('base_url' in error.lower() for error in errors))

    def test_invalid_name_special_chars(self):
        """Test invalid name with special characters"""
        config = {
            'name': 'test@skill!',
            'base_url': 'https://example.com/'
        }
        errors, _ = validate_config(config)
        self.assertTrue(any('invalid name' in error.lower() for error in errors))

    def test_valid_name_formats(self):
        """Test various valid name formats"""
        valid_names = ['test', 'test-skill', 'test_skill', 'TestSkill123', 'my-awesome-skill_v2']
        for name in valid_names:
            config = {
                'name': name,
                'base_url': 'https://example.com/'
            }
            errors, _ = validate_config(config)
            name_errors = [e for e in errors if 'invalid name' in e.lower()]
            self.assertEqual(len(name_errors), 0, f"Name '{name}' should be valid")

    def test_invalid_base_url_no_protocol(self):
        """Test invalid base_url without protocol"""
        config = {
            'name': 'test',
            'base_url': 'example.com'
        }
        errors, _ = validate_config(config)
        self.assertTrue(any('base_url' in error.lower() for error in errors))

    def test_valid_url_protocols(self):
        """Test valid URL protocols"""
        for protocol in ['http://', 'https://']:
            config = {
                'name': 'test',
                'base_url': f'{protocol}example.com/'
            }
            errors, _ = validate_config(config)
            url_errors = [e for e in errors if 'base_url' in e.lower() and 'invalid' in e.lower()]
            self.assertEqual(len(url_errors), 0, f"Protocol '{protocol}' should be valid")

    def test_invalid_selectors_not_dict(self):
        """Test invalid selectors (not a dictionary)"""
        config = {
            'name': 'test',
            'base_url': 'https://example.com/',
            'selectors': 'invalid'
        }
        errors, _ = validate_config(config)
        self.assertTrue(any('selectors' in error.lower() and 'dictionary' in error.lower() for error in errors))

    def test_missing_recommended_selectors(self):
        """Test warning for missing recommended selectors"""
        config = {
            'name': 'test',
            'base_url': 'https://example.com/',
            'selectors': {
                'main_content': 'article'
                # Missing 'title' and 'code_blocks'
            }
        }
        _, warnings = validate_config(config)
        self.assertTrue(any('title' in warning.lower() for warning in warnings))
        self.assertTrue(any('code_blocks' in warning.lower() for warning in warnings))

    def test_invalid_url_patterns_not_dict(self):
        """Test invalid url_patterns (not a dictionary)"""
        config = {
            'name': 'test',
            'base_url': 'https://example.com/',
            'url_patterns': []
        }
        errors, _ = validate_config(config)
        self.assertTrue(any('url_patterns' in error.lower() and 'dictionary' in error.lower() for error in errors))

    def test_invalid_url_patterns_include_not_list(self):
        """Test invalid url_patterns.include (not a list)"""
        config = {
            'name': 'test',
            'base_url': 'https://example.com/',
            'url_patterns': {
                'include': 'not-a-list'
            }
        }
        errors, _ = validate_config(config)
        self.assertTrue(any('include' in error.lower() and 'list' in error.lower() for error in errors))

    def test_invalid_categories_not_dict(self):
        """Test invalid categories (not a dictionary)"""
        config = {
            'name': 'test',
            'base_url': 'https://example.com/',
            'categories': []
        }
        errors, _ = validate_config(config)
        self.assertTrue(any('categories' in error.lower() and 'dictionary' in error.lower() for error in errors))

    def test_invalid_category_keywords_not_list(self):
        """Test invalid category keywords (not a list)"""
        config = {
            'name': 'test',
            'base_url': 'https://example.com/',
            'categories': {
                'getting_started': 'not-a-list'
            }
        }
        errors, _ = validate_config(config)
        self.assertTrue(any('getting_started' in error.lower() and 'list' in error.lower() for error in errors))

    def test_invalid_rate_limit_negative(self):
        """Test invalid rate_limit (negative)"""
        config = {
            'name': 'test',
            'base_url': 'https://example.com/',
            'rate_limit': -1
        }
        errors, _ = validate_config(config)
        self.assertTrue(any('rate_limit' in error.lower() for error in errors))

    def test_invalid_rate_limit_too_high(self):
        """Test invalid rate_limit (too high)"""
        config = {
            'name': 'test',
            'base_url': 'https://example.com/',
            'rate_limit': 20
        }
        _, warnings = validate_config(config)
        self.assertTrue(any('rate_limit' in warning.lower() for warning in warnings))

    def test_invalid_rate_limit_not_number(self):
        """Test invalid rate_limit (not a number)"""
        config = {
            'name': 'test',
            'base_url': 'https://example.com/',
            'rate_limit': 'fast'
        }
        errors, _ = validate_config(config)
        self.assertTrue(any('rate_limit' in error.lower() for error in errors))

    def test_valid_rate_limit_range(self):
        """Test valid rate_limit range"""
        for rate in [0, 0.1, 0.5, 1, 5, 10]:
            config = {
                'name': 'test',
                'base_url': 'https://example.com/',
                'rate_limit': rate
            }
            errors, _ = validate_config(config)
            rate_errors = [e for e in errors if 'rate_limit' in e.lower()]
            self.assertEqual(len(rate_errors), 0, f"Rate limit {rate} should be valid")

    def test_invalid_max_pages_zero(self):
        """Test invalid max_pages (zero)"""
        config = {
            'name': 'test',
            'base_url': 'https://example.com/',
            'max_pages': 0
        }
        errors, _ = validate_config(config)
        self.assertTrue(any('max_pages' in error.lower() for error in errors))

    def test_invalid_max_pages_too_high(self):
        """Test invalid max_pages (too high)"""
        config = {
            'name': 'test',
            'base_url': 'https://example.com/',
            'max_pages': 20000
        }
        _, warnings = validate_config(config)
        self.assertTrue(any('max_pages' in warning.lower() for warning in warnings))

    def test_invalid_max_pages_not_int(self):
        """Test invalid max_pages (not an integer)"""
        config = {
            'name': 'test',
            'base_url': 'https://example.com/',
            'max_pages': 'many'
        }
        errors, _ = validate_config(config)
        self.assertTrue(any('max_pages' in error.lower() for error in errors))

    def test_valid_max_pages_range(self):
        """Test valid max_pages range"""
        for max_p in [1, 10, 100, 500, 5000, 10000]:
            config = {
                'name': 'test',
                'base_url': 'https://example.com/',
                'max_pages': max_p
            }
            errors, _ = validate_config(config)
            max_errors = [e for e in errors if 'max_pages' in e.lower()]
            self.assertEqual(len(max_errors), 0, f"Max pages {max_p} should be valid")

    def test_invalid_start_urls_not_list(self):
        """Test invalid start_urls (not a list)"""
        config = {
            'name': 'test',
            'base_url': 'https://example.com/',
            'start_urls': 'https://example.com/page1'
        }
        errors, _ = validate_config(config)
        self.assertTrue(any('start_urls' in error.lower() and 'list' in error.lower() for error in errors))

    def test_invalid_start_urls_bad_protocol(self):
        """Test invalid start_urls (bad protocol)"""
        config = {
            'name': 'test',
            'base_url': 'https://example.com/',
            'start_urls': ['ftp://example.com/page1']
        }
        errors, _ = validate_config(config)
        self.assertTrue(any('start_url' in error.lower() for error in errors))

    def test_valid_start_urls(self):
        """Test valid start_urls"""
        config = {
            'name': 'test',
            'base_url': 'https://example.com/',
            'start_urls': [
                'https://example.com/page1',
                'http://example.com/page2',
                'https://example.com/api/docs'
            ]
        }
        errors, _ = validate_config(config)
        url_errors = [e for e in errors if 'start_url' in e.lower()]
        self.assertEqual(len(url_errors), 0, "Valid start_urls should pass validation")

    def test_config_with_llms_txt_url(self):
        """Test config validation with explicit llms_txt_url"""
        config = {
            'name': 'test',
            'llms_txt_url': 'https://example.com/llms-full.txt',
            'base_url': 'https://example.com/docs'
        }

        # Should be valid
        self.assertEqual(config.get('llms_txt_url'), 'https://example.com/llms-full.txt')

    def test_config_with_skip_llms_txt(self):
        """Test config validation accepts skip_llms_txt"""
        config = {
            'name': 'test',
            'base_url': 'https://example.com/docs',
            'skip_llms_txt': True
        }

        errors, warnings = validate_config(config)
        self.assertEqual(errors, [])
        self.assertTrue(config.get('skip_llms_txt'))

    def test_config_with_skip_llms_txt_false(self):
        """Test config validation accepts skip_llms_txt as False"""
        config = {
            'name': 'test',
            'base_url': 'https://example.com/docs',
            'skip_llms_txt': False
        }

        errors, warnings = validate_config(config)
        self.assertEqual(errors, [])
        self.assertFalse(config.get('skip_llms_txt'))


if __name__ == '__main__':
    unittest.main()
