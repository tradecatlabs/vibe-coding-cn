#!/usr/bin/env python3
"""
Test suite for doc_scraper core features
Tests URL validation, language detection, pattern extraction, and categorization
"""

import sys
import os
import unittest
from unittest.mock import Mock, MagicMock
from bs4 import BeautifulSoup

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skill_seekers.cli.doc_scraper import DocToSkillConverter


class TestURLValidation(unittest.TestCase):
    """Test URL validation logic"""

    def setUp(self):
        """Set up test converter"""
        self.config = {
            'name': 'test',
            'base_url': 'https://docs.example.com/',
            'url_patterns': {
                'include': ['/guide/', '/api/'],
                'exclude': ['/blog/', '/about/']
            },
            'selectors': {
                'main_content': 'article',
                'title': 'h1',
                'code_blocks': 'pre code'
            },
            'rate_limit': 0.1,
            'max_pages': 10
        }
        self.converter = DocToSkillConverter(self.config, dry_run=True)

    def test_valid_url_with_include_pattern(self):
        """Test URL matching include pattern"""
        url = 'https://docs.example.com/guide/getting-started'
        self.assertTrue(self.converter.is_valid_url(url))

    def test_valid_url_with_api_pattern(self):
        """Test URL matching API pattern"""
        url = 'https://docs.example.com/api/reference'
        self.assertTrue(self.converter.is_valid_url(url))

    def test_invalid_url_with_exclude_pattern(self):
        """Test URL matching exclude pattern"""
        url = 'https://docs.example.com/blog/announcement'
        self.assertFalse(self.converter.is_valid_url(url))

    def test_invalid_url_different_domain(self):
        """Test URL from different domain"""
        url = 'https://other-site.com/guide/tutorial'
        self.assertFalse(self.converter.is_valid_url(url))

    def test_invalid_url_no_include_match(self):
        """Test URL not matching any include pattern"""
        url = 'https://docs.example.com/download/installer'
        self.assertFalse(self.converter.is_valid_url(url))

    def test_url_validation_no_patterns(self):
        """Test URL validation with no include/exclude patterns"""
        config = {
            'name': 'test',
            'base_url': 'https://docs.example.com/',
            'url_patterns': {
                'include': [],
                'exclude': []
            },
            'selectors': {'main_content': 'article', 'title': 'h1', 'code_blocks': 'pre'},
            'rate_limit': 0.1,
            'max_pages': 10
        }
        converter = DocToSkillConverter(config, dry_run=True)

        # Should accept any URL under base_url
        self.assertTrue(converter.is_valid_url('https://docs.example.com/anything'))
        self.assertFalse(converter.is_valid_url('https://other.com/anything'))


class TestLanguageDetection(unittest.TestCase):
    """Test language detection from code blocks"""

    def setUp(self):
        """Set up test converter"""
        config = {
            'name': 'test',
            'base_url': 'https://example.com/',
            'selectors': {'main_content': 'article', 'title': 'h1', 'code_blocks': 'pre'},
            'rate_limit': 0.1,
            'max_pages': 10
        }
        self.converter = DocToSkillConverter(config, dry_run=True)

    def test_detect_language_from_class(self):
        """Test language detection from CSS class"""
        html = '<code class="language-python">print("hello")</code>'
        elem = BeautifulSoup(html, 'html.parser').find('code')
        lang = self.converter.detect_language(elem, 'print("hello")')
        self.assertEqual(lang, 'python')

    def test_detect_language_from_lang_class(self):
        """Test language detection from lang- prefix"""
        html = '<code class="lang-javascript">console.log("hello")</code>'
        elem = BeautifulSoup(html, 'html.parser').find('code')
        lang = self.converter.detect_language(elem, 'console.log("hello")')
        self.assertEqual(lang, 'javascript')

    def test_detect_language_from_parent(self):
        """Test language detection from parent pre element"""
        html = '<pre class="language-cpp"><code>int main() {}</code></pre>'
        elem = BeautifulSoup(html, 'html.parser').find('code')
        lang = self.converter.detect_language(elem, 'int main() {}')
        self.assertEqual(lang, 'cpp')

    def test_detect_python_from_heuristics(self):
        """Test Python detection from code content"""
        html = '<code>import os\nfrom pathlib import Path</code>'
        elem = BeautifulSoup(html, 'html.parser').find('code')
        code = elem.get_text()
        lang = self.converter.detect_language(elem, code)
        self.assertEqual(lang, 'python')

    def test_detect_python_from_def(self):
        """Test Python detection from def keyword"""
        html = '<code>def my_function():\n    pass</code>'
        elem = BeautifulSoup(html, 'html.parser').find('code')
        code = elem.get_text()
        lang = self.converter.detect_language(elem, code)
        self.assertEqual(lang, 'python')

    def test_detect_javascript_from_const(self):
        """Test JavaScript detection from const keyword"""
        html = '<code>const myVar = 10;</code>'
        elem = BeautifulSoup(html, 'html.parser').find('code')
        code = elem.get_text()
        lang = self.converter.detect_language(elem, code)
        self.assertEqual(lang, 'javascript')

    def test_detect_javascript_from_arrow(self):
        """Test JavaScript detection from arrow function"""
        html = '<code>const add = (a, b) => a + b;</code>'
        elem = BeautifulSoup(html, 'html.parser').find('code')
        code = elem.get_text()
        lang = self.converter.detect_language(elem, code)
        self.assertEqual(lang, 'javascript')

    def test_detect_gdscript(self):
        """Test GDScript detection"""
        html = '<code>func _ready():\n    var x = 5</code>'
        elem = BeautifulSoup(html, 'html.parser').find('code')
        code = elem.get_text()
        lang = self.converter.detect_language(elem, code)
        self.assertEqual(lang, 'gdscript')

    def test_detect_cpp(self):
        """Test C++ detection"""
        html = '<code>#include <iostream>\nint main() { return 0; }</code>'
        elem = BeautifulSoup(html, 'html.parser').find('code')
        code = elem.get_text()
        lang = self.converter.detect_language(elem, code)
        self.assertEqual(lang, 'cpp')

    def test_detect_unknown(self):
        """Test unknown language detection"""
        html = '<code>some random text without clear indicators</code>'
        elem = BeautifulSoup(html, 'html.parser').find('code')
        code = elem.get_text()
        lang = self.converter.detect_language(elem, code)
        self.assertEqual(lang, 'unknown')

    def test_detect_brush_pattern_in_pre(self):
        """Test brush: pattern in pre element"""
        html = '<pre class="brush: python"><code>x</code></pre>'
        elem = BeautifulSoup(html, 'html.parser').find('code')
        lang = self.converter.detect_language(elem, 'x')
        self.assertEqual(lang, 'python', 'Should detect python from brush: python pattern')

    def test_detect_bare_class_in_pre(self):
        """Test bare class name in pre element"""
        html = '<pre class="python"><code>x</code></pre>'
        elem = BeautifulSoup(html, 'html.parser').find('code')
        lang = self.converter.detect_language(elem, 'x')
        self.assertEqual(lang, 'python', 'Should detect python from bare class name')

    def test_detect_bare_class_in_code(self):
        """Test bare class name in code element"""
        html = '<code class="python">x</code>'
        elem = BeautifulSoup(html, 'html.parser').find('code')
        lang = self.converter.detect_language(elem, 'x')
        self.assertEqual(lang, 'python', 'Should detect python from bare class name')

    def test_detect_csharp_from_using_system(self):
        """Test C# detection from 'using System' keyword"""
        html = '<code>using System;\nnamespace MyApp { }</code>'
        elem = BeautifulSoup(html, 'html.parser').find('code')
        code = elem.get_text()
        lang = self.converter.detect_language(elem, code)
        self.assertEqual(lang, 'csharp', 'Should detect C# from using System')

    def test_detect_csharp_from_namespace(self):
        """Test C# detection from 'namespace' keyword"""
        html = '<code>namespace MyNamespace\n{\n    public class Test { }\n}</code>'
        elem = BeautifulSoup(html, 'html.parser').find('code')
        code = elem.get_text()
        lang = self.converter.detect_language(elem, code)
        self.assertEqual(lang, 'csharp', 'Should detect C# from namespace')

    def test_detect_csharp_from_property_syntax(self):
        """Test C# detection from property syntax"""
        html = '<code>public string Name { get; set; }</code>'
        elem = BeautifulSoup(html, 'html.parser').find('code')
        code = elem.get_text()
        lang = self.converter.detect_language(elem, code)
        self.assertEqual(lang, 'csharp', 'Should detect C# from { get; set; } syntax')

    def test_detect_csharp_from_public_class(self):
        """Test C# detection from 'public class' keyword"""
        html = '<code>public class MyClass\n{\n    private int value;\n}</code>'
        elem = BeautifulSoup(html, 'html.parser').find('code')
        code = elem.get_text()
        lang = self.converter.detect_language(elem, code)
        self.assertEqual(lang, 'csharp', 'Should detect C# from public class')

    def test_detect_csharp_from_private_class(self):
        """Test C# detection from 'private class' keyword"""
        html = '<code>private class Helper { }</code>'
        elem = BeautifulSoup(html, 'html.parser').find('code')
        code = elem.get_text()
        lang = self.converter.detect_language(elem, code)
        self.assertEqual(lang, 'csharp', 'Should detect C# from private class')

    def test_detect_csharp_from_public_static_void(self):
        """Test C# detection from 'public static void' keyword"""
        html = '<code>public static void Main(string[] args)\n{\n    Console.WriteLine("Test");\n}</code>'
        elem = BeautifulSoup(html, 'html.parser').find('code')
        code = elem.get_text()
        lang = self.converter.detect_language(elem, code)
        self.assertEqual(lang, 'csharp', 'Should detect C# from public static void')

    def test_detect_csharp_from_class_attribute(self):
        """Test C# detection from CSS class attribute"""
        html = '<code class="language-csharp">var x = 5;</code>'
        elem = BeautifulSoup(html, 'html.parser').find('code')
        code = elem.get_text()
        lang = self.converter.detect_language(elem, code)
        self.assertEqual(lang, 'csharp', 'Should detect C# from language-csharp class')


class TestPatternExtraction(unittest.TestCase):
    """Test pattern extraction from documentation"""

    def setUp(self):
        """Set up test converter"""
        config = {
            'name': 'test',
            'base_url': 'https://example.com/',
            'selectors': {'main_content': 'article', 'title': 'h1', 'code_blocks': 'pre'},
            'rate_limit': 0.1,
            'max_pages': 10
        }
        self.converter = DocToSkillConverter(config, dry_run=True)

    def test_extract_pattern_with_example_marker(self):
        """Test pattern extraction with 'Example:' marker"""
        html = '''
        <article>
            <p>Example: Here's how to use it</p>
            <pre><code>print("hello")</code></pre>
        </article>
        '''
        soup = BeautifulSoup(html, 'html.parser')
        main = soup.find('article')
        patterns = self.converter.extract_patterns(main, [])

        self.assertGreater(len(patterns), 0)
        self.assertIn('example', patterns[0]['description'].lower())

    def test_extract_pattern_with_usage_marker(self):
        """Test pattern extraction with 'Usage:' marker"""
        html = '''
        <article>
            <p>Usage: Call this function like so</p>
            <pre><code>my_function(arg)</code></pre>
        </article>
        '''
        soup = BeautifulSoup(html, 'html.parser')
        main = soup.find('article')
        patterns = self.converter.extract_patterns(main, [])

        self.assertGreater(len(patterns), 0)
        self.assertIn('usage', patterns[0]['description'].lower())

    def test_extract_pattern_limit(self):
        """Test pattern extraction limits to 5 patterns"""
        html = '<article>'
        for i in range(10):
            html += f'<p>Example {i}: Test</p><pre><code>code_{i}</code></pre>'
        html += '</article>'

        soup = BeautifulSoup(html, 'html.parser')
        main = soup.find('article')
        patterns = self.converter.extract_patterns(main, [])

        self.assertLessEqual(len(patterns), 5, "Should limit to 5 patterns max")


class TestCategorization(unittest.TestCase):
    """Test smart categorization logic"""

    def setUp(self):
        """Set up test converter"""
        config = {
            'name': 'test',
            'base_url': 'https://example.com/',
            'categories': {
                'getting_started': ['intro', 'tutorial', 'getting-started'],
                'api': ['api', 'reference', 'class'],
                'guides': ['guide', 'how-to']
            },
            'selectors': {'main_content': 'article', 'title': 'h1', 'code_blocks': 'pre'},
            'rate_limit': 0.1,
            'max_pages': 10
        }
        self.converter = DocToSkillConverter(config, dry_run=True)

    def test_categorize_by_url(self):
        """Test categorization based on URL"""
        pages = [{
            'url': 'https://example.com/api/reference',
            'title': 'Some Title',
            'content': 'Some content'
        }]
        categories = self.converter.smart_categorize(pages)

        # Should categorize to 'api' based on URL containing 'api'
        self.assertIn('api', categories)
        self.assertEqual(len(categories['api']), 1)

    def test_categorize_by_title(self):
        """Test categorization based on title"""
        pages = [{
            'url': 'https://example.com/docs/page',
            'title': 'API Reference Documentation',
            'content': 'Some content'
        }]
        categories = self.converter.smart_categorize(pages)

        self.assertIn('api', categories)
        self.assertEqual(len(categories['api']), 1)

    def test_categorize_by_content(self):
        """Test categorization based on content (lower priority)"""
        pages = [{
            'url': 'https://example.com/docs/page',
            'title': 'Some Page',
            'content': 'This is a tutorial for beginners. An intro to the system.'
        }]
        categories = self.converter.smart_categorize(pages)

        # Should categorize based on 'tutorial' and 'intro' in content
        self.assertIn('getting_started', categories)

    def test_categorize_to_other(self):
        """Test pages that don't match any category go to 'other'"""
        pages = [{
            'url': 'https://example.com/random/page',
            'title': 'Random Page',
            'content': 'Random content with no keywords'
        }]
        categories = self.converter.smart_categorize(pages)

        self.assertIn('other', categories)
        self.assertEqual(len(categories['other']), 1)

    def test_empty_categories_removed(self):
        """Test empty categories are removed"""
        pages = [{
            'url': 'https://example.com/api/reference',
            'title': 'API Reference',
            'content': 'API documentation'
        }]
        categories = self.converter.smart_categorize(pages)

        # Only 'api' should exist, not empty 'guides' or 'getting_started'
        # (categories with no pages are removed)
        self.assertIn('api', categories)
        self.assertNotIn('guides', categories)


class TestLinkExtraction(unittest.TestCase):
    """Test link extraction and anchor fragment handling"""

    def setUp(self):
        """Set up test converter"""
        config = {
            'name': 'test',
            'base_url': 'https://example.com/',
            'selectors': {'main_content': 'article', 'title': 'h1', 'code_blocks': 'pre code'},
            'url_patterns': {
                'include': [],
                'exclude': []
            },
            'rate_limit': 0.1,
            'max_pages': 10
        }
        self.converter = DocToSkillConverter(config, dry_run=True)

    def test_extract_links_strips_anchor_fragments(self):
        """Test that anchor fragments (#anchor) are stripped from extracted links"""
        html = '''
        <article>
            <h1>Test Page</h1>
            <p>Content with links</p>
            <a href="https://example.com/docs/page.html#section1">Link 1</a>
            <a href="https://example.com/docs/page.html#section2">Link 2</a>
            <a href="https://example.com/docs/other.html">Link 3</a>
        </article>
        '''
        soup = BeautifulSoup(html, 'html.parser')
        page = self.converter.extract_content(soup, 'https://example.com/')

        # Should have 2 unique URLs (page.html and other.html), not 3
        # The two links with different anchors should be deduplicated
        self.assertEqual(len(page['links']), 2)
        self.assertIn('https://example.com/docs/page.html', page['links'])
        self.assertIn('https://example.com/docs/other.html', page['links'])

    def test_extract_links_no_anchor_duplicates(self):
        """Test that multiple anchor links to same page don't create duplicates"""
        html = '''
        <article>
            <h1>Test Page</h1>
            <a href="https://example.com/docs/api.html#cb1-1">Anchor 1</a>
            <a href="https://example.com/docs/api.html#cb1-2">Anchor 2</a>
            <a href="https://example.com/docs/api.html#cb1-3">Anchor 3</a>
            <a href="https://example.com/docs/api.html#cb1-4">Anchor 4</a>
            <a href="https://example.com/docs/api.html#cb1-5">Anchor 5</a>
        </article>
        '''
        soup = BeautifulSoup(html, 'html.parser')
        page = self.converter.extract_content(soup, 'https://example.com/')

        # All 5 links point to the same page, should result in only 1 URL
        self.assertEqual(len(page['links']), 1)
        self.assertEqual(page['links'][0], 'https://example.com/docs/api.html')

    def test_extract_links_preserves_query_params(self):
        """Test that query parameters are preserved when stripping anchors"""
        html = '''
        <article>
            <h1>Test Page</h1>
            <a href="https://example.com/search?q=test#result1">Search Result</a>
        </article>
        '''
        soup = BeautifulSoup(html, 'html.parser')
        page = self.converter.extract_content(soup, 'https://example.com/')

        # Query params should be preserved, only anchor stripped
        self.assertEqual(len(page['links']), 1)
        self.assertEqual(page['links'][0], 'https://example.com/search?q=test')

    def test_extract_links_relative_urls_with_anchors(self):
        """Test that relative URLs with anchors are handled correctly"""
        html = '''
        <article>
            <h1>Test Page</h1>
            <a href="/docs/guide.html#intro">Relative Link 1</a>
            <a href="/docs/guide.html#advanced">Relative Link 2</a>
            <a href="/docs/tutorial.html#start">Relative Link 3</a>
        </article>
        '''
        soup = BeautifulSoup(html, 'html.parser')
        page = self.converter.extract_content(soup, 'https://example.com/')

        # Should have 2 unique URLs (guide.html and tutorial.html)
        self.assertEqual(len(page['links']), 2)
        self.assertIn('https://example.com/docs/guide.html', page['links'])
        self.assertIn('https://example.com/docs/tutorial.html', page['links'])


class TestTextCleaning(unittest.TestCase):
    """Test text cleaning utility"""

    def setUp(self):
        """Set up test converter"""
        config = {
            'name': 'test',
            'base_url': 'https://example.com/',
            'selectors': {'main_content': 'article', 'title': 'h1', 'code_blocks': 'pre'},
            'rate_limit': 0.1,
            'max_pages': 10
        }
        self.converter = DocToSkillConverter(config, dry_run=True)

    def test_clean_multiple_spaces(self):
        """Test cleaning multiple spaces"""
        text = "Hello    world     test"
        cleaned = self.converter.clean_text(text)
        self.assertEqual(cleaned, "Hello world test")

    def test_clean_newlines(self):
        """Test cleaning newlines"""
        text = "Hello\n\nworld\ntest"
        cleaned = self.converter.clean_text(text)
        self.assertEqual(cleaned, "Hello world test")

    def test_clean_tabs(self):
        """Test cleaning tabs"""
        text = "Hello\t\tworld\ttest"
        cleaned = self.converter.clean_text(text)
        self.assertEqual(cleaned, "Hello world test")

    def test_clean_strip_whitespace(self):
        """Test stripping leading/trailing whitespace"""
        text = "   Hello world   "
        cleaned = self.converter.clean_text(text)
        self.assertEqual(cleaned, "Hello world")


if __name__ == '__main__':
    unittest.main()
