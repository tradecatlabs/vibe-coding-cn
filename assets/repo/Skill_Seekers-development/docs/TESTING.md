# Testing Guide for Skill Seeker

Comprehensive testing documentation for the Skill Seeker project.

## Quick Start

```bash
# Run all tests
python3 run_tests.py

# Run all tests with verbose output
python3 run_tests.py -v

# Run specific test suite
python3 run_tests.py --suite config
python3 run_tests.py --suite features
python3 run_tests.py --suite integration

# Stop on first failure
python3 run_tests.py --failfast

# List all available tests
python3 run_tests.py --list
```

## Test Structure

```
tests/
├── __init__.py                          # Test package marker
├── test_config_validation.py            # Config validation tests (30+ tests)
├── test_scraper_features.py             # Core feature tests (25+ tests)
├── test_integration.py                  # Integration tests (15+ tests)
├── test_pdf_extractor.py                # PDF extraction tests (23 tests)
├── test_pdf_scraper.py                  # PDF workflow tests (18 tests)
└── test_pdf_advanced_features.py        # PDF advanced features (26 tests) NEW
```

## Test Suites

### 1. Config Validation Tests (`test_config_validation.py`)

Tests the `validate_config()` function with comprehensive coverage.

**Test Categories:**
- ✅ Valid configurations (minimal and complete)
- ✅ Missing required fields (`name`, `base_url`)
- ✅ Invalid name formats (special characters)
- ✅ Valid name formats (alphanumeric, hyphens, underscores)
- ✅ Invalid URLs (missing protocol)
- ✅ Valid URL protocols (http, https)
- ✅ Selector validation (structure and recommended fields)
- ✅ URL patterns validation (include/exclude lists)
- ✅ Categories validation (structure and keywords)
- ✅ Rate limit validation (range 0-10, type checking)
- ✅ Max pages validation (range 1-10000, type checking)
- ✅ Start URLs validation (format and protocol)

**Example Test:**
```python
def test_valid_complete_config(self):
    """Test valid complete configuration"""
    config = {
        'name': 'godot',
        'base_url': 'https://docs.godotengine.org/en/stable/',
        'selectors': {
            'main_content': 'div[role="main"]',
            'title': 'title',
            'code_blocks': 'pre code'
        },
        'rate_limit': 0.5,
        'max_pages': 500
    }
    errors = validate_config(config)
    self.assertEqual(len(errors), 0)
```

**Running:**
```bash
python3 run_tests.py --suite config -v
```

---

### 2. Scraper Features Tests (`test_scraper_features.py`)

Tests core scraper functionality including URL validation, language detection, pattern extraction, and categorization.

**Test Categories:**

**URL Validation:**
- ✅ URL matching include patterns
- ✅ URL matching exclude patterns
- ✅ Different domain rejection
- ✅ No pattern configuration

**Language Detection:**
- ✅ Detection from CSS classes (`language-*`, `lang-*`)
- ✅ Detection from parent elements
- ✅ Python detection (import, from, def)
- ✅ JavaScript detection (const, let, arrow functions)
- ✅ GDScript detection (func, var)
- ✅ C++ detection (#include, int main)
- ✅ Unknown language fallback

**Pattern Extraction:**
- ✅ Extraction with "Example:" marker
- ✅ Extraction with "Usage:" marker
- ✅ Pattern limit (max 5)

**Categorization:**
- ✅ Categorization by URL keywords
- ✅ Categorization by title keywords
- ✅ Categorization by content keywords
- ✅ Fallback to "other" category
- ✅ Empty category removal

**Text Cleaning:**
- ✅ Multiple spaces normalization
- ✅ Newline normalization
- ✅ Tab normalization
- ✅ Whitespace stripping

**Example Test:**
```python
def test_detect_python_from_heuristics(self):
    """Test Python detection from code content"""
    html = '<code>import os\nfrom pathlib import Path</code>'
    elem = BeautifulSoup(html, 'html.parser').find('code')
    lang = self.converter.detect_language(elem, elem.get_text())
    self.assertEqual(lang, 'python')
```

**Running:**
```bash
python3 run_tests.py --suite features -v
```

---

### 3. Integration Tests (`test_integration.py`)

Tests complete workflows and interactions between components.

**Test Categories:**

**Dry-Run Mode:**
- ✅ No directories created in dry-run mode
- ✅ Dry-run flag properly set
- ✅ Normal mode creates directories

**Config Loading:**
- ✅ Load valid configuration files
- ✅ Invalid JSON error handling
- ✅ Nonexistent file error handling
- ✅ Validation errors during load

**Real Config Validation:**
- ✅ Godot config validation
- ✅ React config validation
- ✅ Vue config validation
- ✅ Django config validation
- ✅ FastAPI config validation
- ✅ Steam Economy config validation

**URL Processing:**
- ✅ URL normalization
- ✅ Start URLs fallback to base_url
- ✅ Multiple start URLs handling

**Content Extraction:**
- ✅ Empty content handling
- ✅ Basic content extraction
- ✅ Code sample extraction with language detection

**Example Test:**
```python
def test_dry_run_no_directories_created(self):
    """Test that dry-run mode doesn't create directories"""
    converter = DocToSkillConverter(self.config, dry_run=True)

    data_dir = Path(f"output/{self.config['name']}_data")
    skill_dir = Path(f"output/{self.config['name']}")

    self.assertFalse(data_dir.exists())
    self.assertFalse(skill_dir.exists())
```

**Running:**
```bash
python3 run_tests.py --suite integration -v
```

---

### 4. PDF Extraction Tests (`test_pdf_extractor.py`) **NEW**

Tests PDF content extraction functionality (B1.2-B1.5).

**Note:** These tests require PyMuPDF (`pip install PyMuPDF`). They will be skipped if not installed.

**Test Categories:**

**Language Detection (5 tests):**
- ✅ Python detection with confidence scoring
- ✅ JavaScript detection with confidence
- ✅ C++ detection with confidence
- ✅ Unknown language returns low confidence
- ✅ Confidence always between 0 and 1

**Syntax Validation (5 tests):**
- ✅ Valid Python syntax validation
- ✅ Invalid Python indentation detection
- ✅ Unbalanced brackets detection
- ✅ Valid JavaScript syntax validation
- ✅ Natural language fails validation

**Quality Scoring (4 tests):**
- ✅ Quality score between 0 and 10
- ✅ High-quality code gets good score (>7)
- ✅ Low-quality code gets low score (<4)
- ✅ Quality considers multiple factors

**Chapter Detection (4 tests):**
- ✅ Detect chapters with numbers
- ✅ Detect uppercase chapter headers
- ✅ Detect section headings (e.g., "2.1")
- ✅ Normal text not detected as chapter

**Code Block Merging (2 tests):**
- ✅ Merge code blocks split across pages
- ✅ Don't merge different languages

**Code Detection Methods (2 tests):**
- ✅ Pattern-based detection (keywords)
- ✅ Indent-based detection

**Quality Filtering (1 test):**
- ✅ Filter by minimum quality threshold

**Example Test:**
```python
def test_detect_python_with_confidence(self):
    """Test Python detection returns language and confidence"""
    extractor = self.PDFExtractor.__new__(self.PDFExtractor)
    code = "def hello():\n    print('world')\n    return True"

    language, confidence = extractor.detect_language_from_code(code)

    self.assertEqual(language, "python")
    self.assertGreater(confidence, 0.7)
    self.assertLessEqual(confidence, 1.0)
```

**Running:**
```bash
python3 -m pytest tests/test_pdf_extractor.py -v
```

---

### 5. PDF Workflow Tests (`test_pdf_scraper.py`) **NEW**

Tests PDF to skill conversion workflow (B1.6).

**Note:** These tests require PyMuPDF (`pip install PyMuPDF`). They will be skipped if not installed.

**Test Categories:**

**PDFToSkillConverter (3 tests):**
- ✅ Initialization with name and PDF path
- ✅ Initialization with config file
- ✅ Requires name or config_path

**Categorization (3 tests):**
- ✅ Categorize by keywords
- ✅ Categorize by chapters
- ✅ Handle missing chapters

**Skill Building (3 tests):**
- ✅ Create required directory structure
- ✅ Create SKILL.md with metadata
- ✅ Create reference files for categories

**Code Block Handling (2 tests):**
- ✅ Include code blocks in references
- ✅ Prefer high-quality code

**Image Handling (2 tests):**
- ✅ Save images to assets directory
- ✅ Reference images in markdown

**Error Handling (3 tests):**
- ✅ Handle missing PDF files
- ✅ Handle invalid config JSON
- ✅ Handle missing required config fields

**JSON Workflow (2 tests):**
- ✅ Load from extracted JSON
- ✅ Build from JSON without extraction

**Example Test:**
```python
def test_build_skill_creates_structure(self):
    """Test that build_skill creates required directory structure"""
    converter = self.PDFToSkillConverter(
        name="test_skill",
        pdf_path="test.pdf",
        output_dir=self.temp_dir
    )

    converter.extracted_data = {
        "pages": [{"page_number": 1, "text": "Test", "code_blocks": [], "images": []}],
        "total_pages": 1
    }
    converter.categories = {"test": [converter.extracted_data["pages"][0]]}

    converter.build_skill()

    skill_dir = Path(self.temp_dir) / "test_skill"
    self.assertTrue(skill_dir.exists())
    self.assertTrue((skill_dir / "references").exists())
    self.assertTrue((skill_dir / "scripts").exists())
    self.assertTrue((skill_dir / "assets").exists())
```

**Running:**
```bash
python3 -m pytest tests/test_pdf_scraper.py -v
```

---

### 6. PDF Advanced Features Tests (`test_pdf_advanced_features.py`) **NEW**

Tests advanced PDF features (Priority 2 & 3).

**Note:** These tests require PyMuPDF (`pip install PyMuPDF`). OCR tests also require pytesseract and Pillow. They will be skipped if not installed.

**Test Categories:**

**OCR Support (5 tests):**
- ✅ OCR flag initialization
- ✅ OCR disabled behavior
- ✅ OCR only triggers for minimal text
- ✅ Warning when pytesseract unavailable
- ✅ OCR extraction triggered correctly

**Password Protection (4 tests):**
- ✅ Password parameter initialization
- ✅ Encrypted PDF detection
- ✅ Wrong password handling
- ✅ Missing password error

**Table Extraction (5 tests):**
- ✅ Table extraction flag initialization
- ✅ No extraction when disabled
- ✅ Basic table extraction
- ✅ Multiple tables per page
- ✅ Error handling during extraction

**Caching (5 tests):**
- ✅ Cache initialization
- ✅ Set and get cached values
- ✅ Cache miss returns None
- ✅ Caching can be disabled
- ✅ Cache overwrite

**Parallel Processing (4 tests):**
- ✅ Parallel flag initialization
- ✅ Disabled by default
- ✅ Worker count auto-detection
- ✅ Custom worker count

**Integration (3 tests):**
- ✅ Full initialization with all features
- ✅ Various feature combinations
- ✅ Page data includes tables

**Example Test:**
```python
def test_table_extraction_basic(self):
    """Test basic table extraction"""
    extractor = self.PDFExtractor.__new__(self.PDFExtractor)
    extractor.extract_tables = True
    extractor.verbose = False

    # Create mock table
    mock_table = Mock()
    mock_table.extract.return_value = [
        ["Header 1", "Header 2", "Header 3"],
        ["Data 1", "Data 2", "Data 3"]
    ]
    mock_table.bbox = (0, 0, 100, 100)

    mock_tables = Mock()
    mock_tables.tables = [mock_table]

    mock_page = Mock()
    mock_page.find_tables.return_value = mock_tables

    tables = extractor.extract_tables_from_page(mock_page)

    self.assertEqual(len(tables), 1)
    self.assertEqual(tables[0]['row_count'], 2)
    self.assertEqual(tables[0]['col_count'], 3)
```

**Running:**
```bash
python3 -m pytest tests/test_pdf_advanced_features.py -v
```

---

## Test Runner Features

The custom test runner (`run_tests.py`) provides:

### Colored Output
- 🟢 Green for passing tests
- 🔴 Red for failures and errors
- 🟡 Yellow for skipped tests

### Detailed Summary
```
======================================================================
TEST SUMMARY
======================================================================

Total Tests: 70
✓ Passed: 68
✗ Failed: 2
⊘ Skipped: 0

Success Rate: 97.1%

Test Breakdown by Category:
  TestConfigValidation: 28/30 passed
  TestURLValidation: 6/6 passed
  TestLanguageDetection: 10/10 passed
  TestPatternExtraction: 3/3 passed
  TestCategorization: 5/5 passed
  TestDryRunMode: 3/3 passed
  TestConfigLoading: 4/4 passed
  TestRealConfigFiles: 6/6 passed
  TestContentExtraction: 3/3 passed

======================================================================
```

### Command-Line Options

```bash
# Verbose output (show each test name)
python3 run_tests.py -v

# Quiet output (minimal)
python3 run_tests.py -q

# Stop on first failure
python3 run_tests.py --failfast

# Run specific suite
python3 run_tests.py --suite config

# List all tests
python3 run_tests.py --list
```

---

## Running Individual Tests

### Run Single Test File
```bash
python3 -m unittest tests.test_config_validation
python3 -m unittest tests.test_scraper_features
python3 -m unittest tests.test_integration
```

### Run Single Test Class
```bash
python3 -m unittest tests.test_config_validation.TestConfigValidation
python3 -m unittest tests.test_scraper_features.TestLanguageDetection
```

### Run Single Test Method
```bash
python3 -m unittest tests.test_config_validation.TestConfigValidation.test_valid_complete_config
python3 -m unittest tests.test_scraper_features.TestLanguageDetection.test_detect_python_from_heuristics
```

---

## Test Coverage

### Current Coverage

| Component | Tests | Coverage |
|-----------|-------|----------|
| Config Validation | 30+ | 100% |
| URL Validation | 6 | 95% |
| Language Detection | 10 | 90% |
| Pattern Extraction | 3 | 85% |
| Categorization | 5 | 90% |
| Text Cleaning | 4 | 100% |
| Dry-Run Mode | 3 | 100% |
| Config Loading | 4 | 95% |
| Real Configs | 6 | 100% |
| Content Extraction | 3 | 80% |
| **PDF Extraction** | **23** | **90%** |
| **PDF Workflow** | **18** | **85%** |
| **PDF Advanced Features** | **26** | **95%** |

**Total: 142 tests (75 passing + 67 PDF tests)**

**Note:** PDF tests (67 total) require PyMuPDF and will be skipped if not installed. When PyMuPDF is available, all 142 tests run.

### Not Yet Covered
- Network operations (actual scraping)
- Enhancement scripts (`enhance_skill.py`, `enhance_skill_local.py`)
- Package creation (`package_skill.py`)
- Interactive mode
- SKILL.md generation
- Reference file creation
- PDF extraction with real PDF files (tests use mocked data)

---

## Writing New Tests

### Test Template

```python
#!/usr/bin/env python3
"""
Test suite for [feature name]
Tests [description of what's being tested]
"""

import sys
import os
import unittest

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from doc_scraper import DocToSkillConverter


class TestYourFeature(unittest.TestCase):
    """Test [feature] functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.config = {
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
        self.converter = DocToSkillConverter(self.config, dry_run=True)

    def tearDown(self):
        """Clean up after tests"""
        pass

    def test_your_feature(self):
        """Test description"""
        # Arrange
        test_input = "something"

        # Act
        result = self.converter.some_method(test_input)

        # Assert
        self.assertEqual(result, expected_value)


if __name__ == '__main__':
    unittest.main()
```

### Best Practices

1. **Use descriptive test names**: `test_valid_name_formats` not `test1`
2. **Follow AAA pattern**: Arrange, Act, Assert
3. **One assertion per test** when possible
4. **Test edge cases**: empty inputs, invalid inputs, boundary values
5. **Use setUp/tearDown**: for common initialization and cleanup
6. **Mock external dependencies**: don't make real network calls
7. **Keep tests independent**: tests should not depend on each other
8. **Use dry_run=True**: for converter tests to avoid file creation

---

## Continuous Integration

### GitHub Actions (Future)

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.7'
      - run: pip install requests beautifulsoup4
      - run: python3 run_tests.py
```

---

## Troubleshooting

### Tests Fail with Import Errors
```bash
# Make sure you're in the repository root
cd /path/to/Skill_Seekers

# Run tests from root directory
python3 run_tests.py
```

### Tests Create Output Directories
```bash
# Clean up test artifacts
rm -rf output/test-*

# Make sure tests use dry_run=True
# Check test setUp methods
```

### Specific Test Keeps Failing
```bash
# Run only that test with verbose output
python3 -m unittest tests.test_config_validation.TestConfigValidation.test_name -v

# Check the error message carefully
# Verify test expectations match implementation
```

---

## Performance

Test execution times:
- **Config Validation**: ~0.1 seconds (30 tests)
- **Scraper Features**: ~0.3 seconds (25 tests)
- **Integration Tests**: ~0.5 seconds (15 tests)
- **Total**: ~1 second (70 tests)

---

## Contributing Tests

When adding new features:

1. Write tests **before** implementing the feature (TDD)
2. Ensure tests cover:
   - ✅ Happy path (valid inputs)
   - ✅ Edge cases (empty, null, boundary values)
   - ✅ Error cases (invalid inputs)
3. Run tests before committing:
   ```bash
   python3 run_tests.py
   ```
4. Aim for >80% coverage for new code

---

## Additional Resources

- **unittest documentation**: https://docs.python.org/3/library/unittest.html
- **pytest** (alternative): https://pytest.org/ (more powerful, but requires installation)
- **Test-Driven Development**: https://en.wikipedia.org/wiki/Test-driven_development

---

## Summary

✅ **142 comprehensive tests** covering all major features (75 + 67 PDF)
✅ **PDF support testing** with 67 tests for B1 tasks + Priority 2 & 3
✅ **Colored test runner** with detailed summaries
✅ **Fast execution** (~1 second for full suite)
✅ **Easy to extend** with clear patterns and templates
✅ **Good coverage** of critical paths

**PDF Tests Status:**
- 23 tests for PDF extraction (language detection, syntax validation, quality scoring, chapter detection)
- 18 tests for PDF workflow (initialization, categorization, skill building, code/image handling)
- **26 tests for advanced features (OCR, passwords, tables, parallel, caching)** NEW!
- Tests are skipped gracefully when PyMuPDF is not installed
- Full test coverage when PyMuPDF + optional dependencies are available

**Advanced PDF Features Tested:**
- ✅ OCR support for scanned PDFs (5 tests)
- ✅ Password-protected PDFs (4 tests)
- ✅ Table extraction (5 tests)
- ✅ Parallel processing (4 tests)
- ✅ Caching (5 tests)
- ✅ Integration (3 tests)

Run tests frequently to catch bugs early! 🚀
