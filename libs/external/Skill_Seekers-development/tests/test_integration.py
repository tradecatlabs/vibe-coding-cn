#!/usr/bin/env python3
"""
Integration tests for doc_scraper
Tests complete workflows and dry-run mode
"""

import sys
import os
import unittest
import json
import tempfile
import shutil
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skill_seekers.cli.doc_scraper import DocToSkillConverter, load_config, validate_config


class TestDryRunMode(unittest.TestCase):
    """Test dry-run mode functionality"""

    def setUp(self):
        """Set up test configuration"""
        self.config = {
            'name': 'test-dry-run',
            'base_url': 'https://example.com/',
            'selectors': {
                'main_content': 'article',
                'title': 'h1',
                'code_blocks': 'pre code'
            },
            'url_patterns': {
                'include': [],
                'exclude': []
            },
            'rate_limit': 0.1,
            'max_pages': 10
        }

    def test_dry_run_no_directories_created(self):
        """Test that dry-run mode doesn't create directories"""
        converter = DocToSkillConverter(self.config, dry_run=True)

        # Check directories were NOT created
        data_dir = Path(f"output/{self.config['name']}_data")
        skill_dir = Path(f"output/{self.config['name']}")

        self.assertFalse(data_dir.exists(), "Dry-run should not create data directory")
        self.assertFalse(skill_dir.exists(), "Dry-run should not create skill directory")

    def test_dry_run_flag_set(self):
        """Test that dry_run flag is properly set"""
        converter = DocToSkillConverter(self.config, dry_run=True)
        self.assertTrue(converter.dry_run)

        converter_normal = DocToSkillConverter(self.config, dry_run=False)
        self.assertFalse(converter_normal.dry_run)

        # Clean up
        shutil.rmtree(f"output/{self.config['name']}_data", ignore_errors=True)
        shutil.rmtree(f"output/{self.config['name']}", ignore_errors=True)

    def test_normal_mode_creates_directories(self):
        """Test that normal mode creates directories"""
        converter = DocToSkillConverter(self.config, dry_run=False)

        # Check directories WERE created
        data_dir = Path(f"output/{self.config['name']}_data")
        skill_dir = Path(f"output/{self.config['name']}")

        self.assertTrue(data_dir.exists(), "Normal mode should create data directory")
        self.assertTrue(skill_dir.exists(), "Normal mode should create skill directory")

        # Clean up
        shutil.rmtree(data_dir, ignore_errors=True)
        shutil.rmtree(skill_dir, ignore_errors=True)


class TestConfigLoading(unittest.TestCase):
    """Test configuration loading and validation"""

    def setUp(self):
        """Set up temporary directory for test configs"""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up temporary directory"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_load_valid_config(self):
        """Test loading a valid configuration file"""
        config_data = {
            'name': 'test-config',
            'base_url': 'https://example.com/',
            'selectors': {
                'main_content': 'article',
                'title': 'h1',
                'code_blocks': 'pre code'
            },
            'rate_limit': 0.5,
            'max_pages': 100
        }

        config_path = Path(self.temp_dir) / 'test.json'
        with open(config_path, 'w') as f:
            json.dump(config_data, f)

        loaded_config = load_config(str(config_path))
        self.assertEqual(loaded_config['name'], 'test-config')
        self.assertEqual(loaded_config['base_url'], 'https://example.com/')

    def test_load_invalid_json(self):
        """Test loading an invalid JSON file"""
        config_path = Path(self.temp_dir) / 'invalid.json'
        with open(config_path, 'w') as f:
            f.write('{ invalid json }')

        with self.assertRaises(SystemExit):
            load_config(str(config_path))

    def test_load_nonexistent_file(self):
        """Test loading a nonexistent file"""
        config_path = Path(self.temp_dir) / 'nonexistent.json'

        with self.assertRaises(SystemExit):
            load_config(str(config_path))

    def test_load_config_with_validation_errors(self):
        """Test loading a config with validation errors"""
        config_data = {
            'name': 'invalid@name',  # Invalid name
            'base_url': 'example.com'  # Missing protocol
        }

        config_path = Path(self.temp_dir) / 'invalid_config.json'
        with open(config_path, 'w') as f:
            json.dump(config_data, f)

        with self.assertRaises(SystemExit):
            load_config(str(config_path))


class TestRealConfigFiles(unittest.TestCase):
    """Test that real config files in the repository are valid"""

    def test_godot_config(self):
        """Test Godot config is valid"""
        config_path = 'configs/godot.json'
        if os.path.exists(config_path):
            config = load_config(config_path)
            errors, _ = validate_config(config)
            self.assertEqual(len(errors), 0, f"Godot config should be valid, got errors: {errors}")

    def test_react_config(self):
        """Test React config is valid"""
        config_path = 'configs/react.json'
        if os.path.exists(config_path):
            config = load_config(config_path)
            errors, _ = validate_config(config)
            self.assertEqual(len(errors), 0, f"React config should be valid, got errors: {errors}")

    def test_vue_config(self):
        """Test Vue config is valid"""
        config_path = 'configs/vue.json'
        if os.path.exists(config_path):
            config = load_config(config_path)
            errors, _ = validate_config(config)
            self.assertEqual(len(errors), 0, f"Vue config should be valid, got errors: {errors}")

    def test_django_config(self):
        """Test Django config is valid"""
        config_path = 'configs/django.json'
        if os.path.exists(config_path):
            config = load_config(config_path)
            errors, _ = validate_config(config)
            self.assertEqual(len(errors), 0, f"Django config should be valid, got errors: {errors}")

    def test_fastapi_config(self):
        """Test FastAPI config is valid"""
        config_path = 'configs/fastapi.json'
        if os.path.exists(config_path):
            config = load_config(config_path)
            errors, _ = validate_config(config)
            self.assertEqual(len(errors), 0, f"FastAPI config should be valid, got errors: {errors}")

    def test_steam_economy_config(self):
        """Test Steam Economy config is valid"""
        config_path = 'configs/steam-economy-complete.json'
        if os.path.exists(config_path):
            config = load_config(config_path)
            errors, _ = validate_config(config)
            self.assertEqual(len(errors), 0, f"Steam Economy config should be valid, got errors: {errors}")


class TestURLProcessing(unittest.TestCase):
    """Test URL processing and validation"""

    def test_url_normalization(self):
        """Test URL normalization in converter"""
        config = {
            'name': 'test',
            'base_url': 'https://example.com/',
            'selectors': {'main_content': 'article', 'title': 'h1', 'code_blocks': 'pre'},
            'url_patterns': {'include': [], 'exclude': []},
            'rate_limit': 0.1,
            'max_pages': 10
        }
        converter = DocToSkillConverter(config, dry_run=True)

        # Base URL should be stored correctly
        self.assertEqual(converter.base_url, 'https://example.com/')

    def test_start_urls_fallback(self):
        """Test that start_urls defaults to base_url"""
        config = {
            'name': 'test',
            'base_url': 'https://example.com/',
            'selectors': {'main_content': 'article', 'title': 'h1', 'code_blocks': 'pre'},
            'rate_limit': 0.1,
            'max_pages': 10
        }
        converter = DocToSkillConverter(config, dry_run=True)

        # Should have base_url in pending_urls
        self.assertEqual(len(converter.pending_urls), 1)
        self.assertEqual(converter.pending_urls[0], 'https://example.com/')

    def test_multiple_start_urls(self):
        """Test multiple start URLs"""
        config = {
            'name': 'test',
            'base_url': 'https://example.com/',
            'start_urls': [
                'https://example.com/guide/',
                'https://example.com/api/',
                'https://example.com/tutorial/'
            ],
            'selectors': {'main_content': 'article', 'title': 'h1', 'code_blocks': 'pre'},
            'rate_limit': 0.1,
            'max_pages': 10
        }
        converter = DocToSkillConverter(config, dry_run=True)

        # Should have all start URLs in pending_urls
        self.assertEqual(len(converter.pending_urls), 3)


class TestLlmsTxtIntegration(unittest.TestCase):
    """Test llms.txt integration into scraping workflow"""

    def test_scraper_has_llms_txt_attributes(self):
        """Test that scraper has llms.txt detection attributes"""
        config = {
            'name': 'test-llms',
            'base_url': 'https://hono.dev/docs',
            'selectors': {
                'main_content': 'article',
                'title': 'h1',
                'code_blocks': 'pre code'
            },
            'max_pages': 50
        }

        scraper = DocToSkillConverter(config, dry_run=True)

        # Should have llms.txt attributes
        self.assertFalse(scraper.llms_txt_detected)
        self.assertIsNone(scraper.llms_txt_variant)

    def test_scraper_has_try_llms_txt_method(self):
        """Test that scraper has _try_llms_txt method"""
        config = {
            'name': 'test-llms',
            'base_url': 'https://hono.dev/docs',
            'selectors': {
                'main_content': 'article',
                'title': 'h1',
                'code_blocks': 'pre code'
            },
            'max_pages': 50
        }

        scraper = DocToSkillConverter(config, dry_run=True)

        # Should have _try_llms_txt method
        self.assertTrue(hasattr(scraper, '_try_llms_txt'))
        self.assertTrue(callable(getattr(scraper, '_try_llms_txt')))


class TestContentExtraction(unittest.TestCase):
    """Test content extraction functionality"""

    def setUp(self):
        """Set up test converter"""
        config = {
            'name': 'test',
            'base_url': 'https://example.com/',
            'selectors': {
                'main_content': 'article',
                'title': 'h1',
                'code_blocks': 'pre code'
            },
            'rate_limit': 0.1,
            'max_pages': 10
        }
        self.converter = DocToSkillConverter(config, dry_run=True)

    def test_extract_empty_content(self):
        """Test extracting from empty HTML"""
        from bs4 import BeautifulSoup
        html = '<html><body></body></html>'
        soup = BeautifulSoup(html, 'html.parser')

        page = self.converter.extract_content(soup, 'https://example.com/test')

        self.assertEqual(page['url'], 'https://example.com/test')
        self.assertEqual(page['title'], '')
        self.assertEqual(page['content'], '')
        self.assertEqual(len(page['code_samples']), 0)

    def test_extract_basic_content(self):
        """Test extracting basic content"""
        from bs4 import BeautifulSoup
        html = '''
        <html>
        <head><title>Test Page</title></head>
        <body>
            <article>
                <h1>Page Title</h1>
                <p>This is some content.</p>
                <p>This is more content with sufficient length to be included.</p>
                <pre><code class="language-python">print("hello")</code></pre>
            </article>
        </body>
        </html>
        '''
        soup = BeautifulSoup(html, 'html.parser')

        page = self.converter.extract_content(soup, 'https://example.com/test')

        self.assertEqual(page['url'], 'https://example.com/test')
        self.assertIn('Page Title', page['title'])
        self.assertIn('content', page['content'].lower())
        self.assertGreater(len(page['code_samples']), 0)
        self.assertEqual(page['code_samples'][0]['language'], 'python')


class TestFullLlmsTxtWorkflow(unittest.TestCase):
    """Test complete llms.txt workflow with mocked HTTP requests"""

    def setUp(self):
        """Set up test configuration and temporary directory"""
        self.temp_dir = tempfile.mkdtemp()
        self.config = {
            'name': 'test-e2e-llms',
            'base_url': 'https://hono.dev/docs',
            'llms_txt_url': 'https://hono.dev/llms-full.txt',
            'selectors': {
                'main_content': 'article',
                'title': 'h1',
                'code_blocks': 'pre code'
            },
            'max_pages': 50
        }

        # Sample llms.txt content for testing
        self.sample_llms_content = """# Getting Started

Welcome to the framework documentation. This is the introduction section.

## Installation

To install the framework, run the following command:

```bash
npm install hono
```

## Quick Start

Create a simple application:

```javascript
import { Hono } from 'hono'

const app = new Hono()

app.get('/', (c) => {
  return c.text('Hello World!')
})

export default app
```

# API Reference

This section covers the API documentation for the framework.

## Context

The context object provides request and response handling:

```typescript
interface Context {
  req: Request
  res: Response
  text: (text: string) => Response
}
```

# Middleware

Middleware functions run before route handlers.

## Built-in Middleware

The framework provides several built-in middleware functions:

```javascript
import { logger, cors } from 'hono/middleware'

app.use('*', logger())
app.use('*', cors())
```
"""

    def tearDown(self):
        """Clean up temporary directory and test output"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        # Clean up test output directories
        shutil.rmtree(f"output/{self.config['name']}_data", ignore_errors=True)
        shutil.rmtree(f"output/{self.config['name']}", ignore_errors=True)

    def test_full_llms_txt_workflow(self):
        """Test complete workflow: config -> scrape (llms.txt) -> build -> verify"""
        from unittest.mock import patch, MagicMock
        import requests

        # Mock the requests.get call for downloading llms.txt
        with patch('cli.llms_txt_downloader.requests.get') as mock_get:
            # Configure mock response
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.text = self.sample_llms_content
            mock_response.raise_for_status = MagicMock()
            mock_get.return_value = mock_response

            # Create scraper and scrape
            scraper = DocToSkillConverter(self.config, dry_run=False)
            scraper.scrape_all()

            # Verify llms.txt was detected
            self.assertTrue(scraper.llms_txt_detected,
                          "llms.txt should be detected")
            self.assertEqual(scraper.llms_txt_variant, 'explicit',
                           "Should use explicit variant from config")

            # Verify pages were parsed
            self.assertGreater(len(scraper.pages), 0,
                             "Should have parsed pages from llms.txt")

            # Verify page structure
            self.assertTrue(all('title' in page for page in scraper.pages),
                          "All pages should have titles")
            self.assertTrue(all('content' in page for page in scraper.pages),
                          "All pages should have content")
            self.assertTrue(any(len(page.get('code_samples', [])) > 0
                              for page in scraper.pages),
                          "At least one page should have code samples")

            # Verify code samples have language detection
            pages_with_code = [p for p in scraper.pages
                             if len(p.get('code_samples', [])) > 0]
            if pages_with_code:
                sample = pages_with_code[0]['code_samples'][0]
                self.assertIn('language', sample,
                            "Code samples should have language field")
                self.assertIn('code', sample,
                            "Code samples should have code field")

            # Build skill
            scraper.build_skill()

            # Verify SKILL.md exists
            skill_md_path = Path(f"output/{self.config['name']}/SKILL.md")
            self.assertTrue(skill_md_path.exists(),
                          "SKILL.md should be created")

            # Verify SKILL.md content
            skill_content = skill_md_path.read_text()
            self.assertIn(self.config['name'], skill_content,
                        "SKILL.md should contain skill name")
            self.assertGreater(len(skill_content), 100,
                             "SKILL.md should have substantial content")

            # Verify references directory exists
            refs_dir = Path(f"output/{self.config['name']}/references")
            self.assertTrue(refs_dir.exists(),
                          "references directory should exist")

            # Verify at least index.md was created
            index_md = refs_dir / 'index.md'
            self.assertTrue(index_md.exists(),
                          "references/index.md should exist")

            # Verify reference files have content
            ref_files = list(refs_dir.glob('*.md'))
            self.assertGreater(len(ref_files), 0,
                             "Should have at least one reference file")

            # Verify data directory was created and has summary
            data_dir = Path(f"output/{self.config['name']}_data")
            self.assertTrue(data_dir.exists(),
                          "Data directory should exist")

            summary_path = data_dir / 'summary.json'
            self.assertTrue(summary_path.exists(),
                          "summary.json should exist")

            # Verify summary content
            with open(summary_path) as f:
                summary = json.load(f)
                self.assertEqual(summary['name'], self.config['name'])
                self.assertGreater(summary['total_pages'], 0)
                self.assertIn('llms_txt_detected', summary)
                self.assertTrue(summary['llms_txt_detected'])

    def test_multi_variant_download(self):
        """Test downloading all 3 llms.txt variants"""
        from unittest.mock import patch, Mock

        config = {
            'name': 'test-multi-variant',
            'base_url': 'https://hono.dev/docs',
            'selectors': {
                'main_content': 'article',
                'title': 'h1',
                'code_blocks': 'pre code'
            },
            'max_pages': 50
        }

        # Mock all 3 variants
        sample_full = "# Full\n" + "x" * 1000
        sample_standard = "# Standard\n" + "x" * 200
        sample_small = "# Small\n" + "x" * 500

        with patch('cli.llms_txt_detector.requests.head') as mock_head, \
             patch('cli.llms_txt_downloader.requests.get') as mock_get:

            # Mock detection (all exist)
            mock_head_response = Mock()
            mock_head_response.status_code = 200
            mock_head.return_value = mock_head_response

            # Mock downloads
            def mock_download(url, **kwargs):
                response = Mock()
                response.status_code = 200
                if 'llms-full.txt' in url:
                    response.text = sample_full
                elif 'llms-small.txt' in url:
                    response.text = sample_small
                else:  # llms.txt
                    response.text = sample_standard
                response.raise_for_status = Mock()
                return response

            mock_get.side_effect = mock_download

            # Run scraper
            from skill_seekers.cli.doc_scraper import DocToSkillConverter as DocumentationScraper
            scraper = DocumentationScraper(config, dry_run=False)
            result = scraper._try_llms_txt()

            # Verify all 3 files created
            refs_dir = Path(f"output/{config['name']}/references")

            self.assertTrue(refs_dir.exists(), "references directory should exist")
            self.assertTrue((refs_dir / 'llms-full.md').exists(), "llms-full.md should exist")
            self.assertTrue((refs_dir / 'llms.md').exists(), "llms.md should exist")
            self.assertTrue((refs_dir / 'llms-small.md').exists(), "llms-small.md should exist")

            # Verify content not truncated
            full_content = (refs_dir / 'llms-full.md').read_text()
            self.assertEqual(len(full_content), len(sample_full))

        # Clean up
        shutil.rmtree(f"output/{config['name']}_data", ignore_errors=True)
        shutil.rmtree(f"output/{config['name']}", ignore_errors=True)

def test_no_content_truncation():
    """Test that content is NOT truncated in reference files"""
    from unittest.mock import Mock
    import tempfile

    config = {
        'name': 'test-no-truncate',
        'base_url': 'https://example.com/docs',
        'selectors': {
            'main_content': 'article',
            'title': 'h1',
            'code_blocks': 'pre code'
        },
        'max_pages': 50
    }

    # Create scraper with long content
    from skill_seekers.cli.doc_scraper import DocToSkillConverter
    scraper = DocToSkillConverter(config, dry_run=False)

    # Create page with content > 2500 chars
    long_content = "x" * 5000
    long_code = "y" * 1000

    pages = [{
        'title': 'Long Page',
        'url': 'https://example.com/long',
        'content': long_content,
        'code_samples': [
            {'code': long_code, 'language': 'python'}
        ],
        'headings': []
    }]

    # Create reference file
    scraper.create_reference_file('test', pages)

    # Verify no truncation
    ref_file = Path(f"output/{config['name']}/references/test.md")
    with open(ref_file, 'r') as f:
        content = f.read()

    assert long_content in content  # Full content included
    assert long_code in content     # Full code included
    assert '[Content truncated]' not in content
    assert '...' not in content or content.count('...') == 0

    # Clean up
    shutil.rmtree(f"output/{config['name']}_data", ignore_errors=True)
    shutil.rmtree(f"output/{config['name']}", ignore_errors=True)


if __name__ == '__main__':
    unittest.main()
