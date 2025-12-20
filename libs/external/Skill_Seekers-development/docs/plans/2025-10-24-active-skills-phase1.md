# Active Skills Phase 1: Foundation Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Fix fundamental issues in llms.txt handling: rename .txt→.md, download all 3 variants, remove truncation.

**Architecture:** Modify existing llms.txt download/parse/build workflow to handle multiple variants correctly, store with proper extensions, and preserve complete content without truncation.

**Tech Stack:** Python 3.10+, requests, BeautifulSoup4, existing Skill_Seekers architecture

---

## Task 1: Add Multi-Variant Detection

**Files:**
- Modify: `cli/llms_txt_detector.py`
- Test: `tests/test_llms_txt_detector.py`

**Step 1: Write failing test for detect_all() method**

```python
# tests/test_llms_txt_detector.py (add new test)

def test_detect_all_variants():
    """Test detecting all llms.txt variants"""
    from unittest.mock import patch, Mock

    detector = LlmsTxtDetector("https://hono.dev/docs")

    with patch('cli.llms_txt_detector.requests.head') as mock_head:
        # Mock responses for different variants
        def mock_response(url, **kwargs):
            response = Mock()
            # All 3 variants exist for Hono
            if 'llms-full.txt' in url or 'llms.txt' in url or 'llms-small.txt' in url:
                response.status_code = 200
            else:
                response.status_code = 404
            return response

        mock_head.side_effect = mock_response

        variants = detector.detect_all()

        assert len(variants) == 3
        assert any(v['variant'] == 'full' for v in variants)
        assert any(v['variant'] == 'standard' for v in variants)
        assert any(v['variant'] == 'small' for v in variants)
        assert all('url' in v for v in variants)
```

**Step 2: Run test to verify it fails**

Run: `source .venv/bin/activate && pytest tests/test_llms_txt_detector.py::test_detect_all_variants -v`

Expected: FAIL with "AttributeError: 'LlmsTxtDetector' object has no attribute 'detect_all'"

**Step 3: Implement detect_all() method**

```python
# cli/llms_txt_detector.py (add new method)

def detect_all(self) -> List[Dict[str, str]]:
    """
    Detect all available llms.txt variants.

    Returns:
        List of dicts with 'url' and 'variant' keys for each found variant
    """
    found_variants = []

    for filename, variant in self.VARIANTS:
        parsed = urlparse(self.base_url)
        root_url = f"{parsed.scheme}://{parsed.netloc}"
        url = f"{root_url}/{filename}"

        if self._check_url_exists(url):
            found_variants.append({
                'url': url,
                'variant': variant
            })

    return found_variants
```

**Step 4: Add import for List and Dict at top of file**

```python
# cli/llms_txt_detector.py (add to imports)
from typing import Optional, Dict, List
```

**Step 5: Run test to verify it passes**

Run: `source .venv/bin/activate && pytest tests/test_llms_txt_detector.py::test_detect_all_variants -v`

Expected: PASS

**Step 6: Commit**

```bash
git add cli/llms_txt_detector.py tests/test_llms_txt_detector.py
git commit -m "feat: add detect_all() for multi-variant detection"
```

---

## Task 2: Add File Extension Renaming to Downloader

**Files:**
- Modify: `cli/llms_txt_downloader.py`
- Test: `tests/test_llms_txt_downloader.py`

**Step 1: Write failing test for get_proper_filename() method**

```python
# tests/test_llms_txt_downloader.py (add new test)

def test_get_proper_filename():
    """Test filename conversion from .txt to .md"""
    downloader = LlmsTxtDownloader("https://hono.dev/llms-full.txt")

    filename = downloader.get_proper_filename()

    assert filename == "llms-full.md"
    assert not filename.endswith('.txt')

def test_get_proper_filename_standard():
    """Test standard variant naming"""
    downloader = LlmsTxtDownloader("https://hono.dev/llms.txt")

    filename = downloader.get_proper_filename()

    assert filename == "llms.md"

def test_get_proper_filename_small():
    """Test small variant naming"""
    downloader = LlmsTxtDownloader("https://hono.dev/llms-small.txt")

    filename = downloader.get_proper_filename()

    assert filename == "llms-small.md"
```

**Step 2: Run test to verify it fails**

Run: `source .venv/bin/activate && pytest tests/test_llms_txt_downloader.py::test_get_proper_filename -v`

Expected: FAIL with "AttributeError: 'LlmsTxtDownloader' object has no attribute 'get_proper_filename'"

**Step 3: Implement get_proper_filename() method**

```python
# cli/llms_txt_downloader.py (add new method)

def get_proper_filename(self) -> str:
    """
    Extract filename from URL and convert .txt to .md

    Returns:
        Proper filename with .md extension

    Examples:
        https://hono.dev/llms-full.txt -> llms-full.md
        https://hono.dev/llms.txt -> llms.md
        https://hono.dev/llms-small.txt -> llms-small.md
    """
    # Extract filename from URL
    from urllib.parse import urlparse
    parsed = urlparse(self.url)
    filename = parsed.path.split('/')[-1]

    # Replace .txt with .md
    if filename.endswith('.txt'):
        filename = filename[:-4] + '.md'

    return filename
```

**Step 4: Run test to verify it passes**

Run: `source .venv/bin/activate && pytest tests/test_llms_txt_downloader.py::test_get_proper_filename -v`

Expected: PASS (all 3 tests)

**Step 5: Commit**

```bash
git add cli/llms_txt_downloader.py tests/test_llms_txt_downloader.py
git commit -m "feat: add get_proper_filename() for .txt to .md conversion"
```

---

## Task 3: Update _try_llms_txt() to Download All Variants

**Files:**
- Modify: `cli/doc_scraper.py:337-384` (_try_llms_txt method)
- Test: `tests/test_integration.py`

**Step 1: Write failing test for multi-variant download**

```python
# tests/test_integration.py (add to TestFullLlmsTxtWorkflow class)

def test_multi_variant_download(self):
    """Test downloading all 3 llms.txt variants"""
    from unittest.mock import patch, Mock
    import tempfile
    import os

    config = {
        'name': 'test-multi-variant',
        'base_url': 'https://hono.dev/docs'
    }

    # Mock all 3 variants
    sample_full = "# Full\n" + "x" * 1000
    sample_standard = "# Standard\n" + "x" * 200
    sample_small = "# Small\n" + "x" * 500

    with tempfile.TemporaryDirectory() as tmpdir:
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
                return response

            mock_get.side_effect = mock_download

            # Run scraper
            scraper = DocumentationScraper(config, dry_run=False)
            result = scraper._try_llms_txt()

            # Verify all 3 files created
            refs_dir = os.path.join(scraper.skill_dir, 'references')

            assert os.path.exists(os.path.join(refs_dir, 'llms-full.md'))
            assert os.path.exists(os.path.join(refs_dir, 'llms.md'))
            assert os.path.exists(os.path.join(refs_dir, 'llms-small.md'))

            # Verify content not truncated
            with open(os.path.join(refs_dir, 'llms-full.md')) as f:
                content = f.read()
                assert len(content) == len(sample_full)
```

**Step 2: Run test to verify it fails**

Run: `source .venv/bin/activate && pytest tests/test_integration.py::TestFullLlmsTxtWorkflow::test_multi_variant_download -v`

Expected: FAIL - only one file created, not all 3

**Step 3: Modify _try_llms_txt() to use detect_all()**

```python
# cli/doc_scraper.py (replace _try_llms_txt method, lines 337-384)

def _try_llms_txt(self) -> bool:
    """
    Try to use llms.txt instead of HTML scraping.
    Downloads ALL available variants and stores with .md extension.

    Returns:
        True if llms.txt was found and processed successfully
    """
    print(f"\n🔍 Checking for llms.txt at {self.base_url}...")

    # Check for explicit config URL first
    explicit_url = self.config.get('llms_txt_url')
    if explicit_url:
        print(f"\n📌 Using explicit llms_txt_url from config: {explicit_url}")

        downloader = LlmsTxtDownloader(explicit_url)
        content = downloader.download()

        if content:
            # Save with proper .md extension
            filename = downloader.get_proper_filename()
            filepath = os.path.join(self.skill_dir, "references", filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  💾 Saved {filename} ({len(content)} chars)")

            # Parse and save pages
            parser = LlmsTxtParser(content)
            pages = parser.parse()

            if pages:
                for page in pages:
                    self.save_page(page)
                    self.pages.append(page)

                self.llms_txt_detected = True
                self.llms_txt_variant = 'explicit'
                return True

    # Auto-detection: Find ALL variants
    detector = LlmsTxtDetector(self.base_url)
    variants = detector.detect_all()

    if not variants:
        print("ℹ️  No llms.txt found, using HTML scraping")
        return False

    print(f"✅ Found {len(variants)} llms.txt variant(s)")

    # Download ALL variants
    downloaded = {}
    for variant_info in variants:
        url = variant_info['url']
        variant = variant_info['variant']

        print(f"  📥 Downloading {variant}...")
        downloader = LlmsTxtDownloader(url)
        content = downloader.download()

        if content:
            filename = downloader.get_proper_filename()
            downloaded[variant] = {
                'content': content,
                'filename': filename,
                'size': len(content)
            }
            print(f"     ✓ {filename} ({len(content)} chars)")

    if not downloaded:
        print("⚠️  Failed to download any variants, falling back to HTML scraping")
        return False

    # Save ALL variants to references/
    os.makedirs(os.path.join(self.skill_dir, "references"), exist_ok=True)

    for variant, data in downloaded.items():
        filepath = os.path.join(self.skill_dir, "references", data['filename'])
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(data['content'])
        print(f"  💾 Saved {data['filename']}")

    # Parse LARGEST variant for skill building
    largest = max(downloaded.items(), key=lambda x: x[1]['size'])
    print(f"\n📄 Parsing {largest[1]['filename']} for skill building...")

    parser = LlmsTxtParser(largest[1]['content'])
    pages = parser.parse()

    if not pages:
        print("⚠️  Failed to parse llms.txt, falling back to HTML scraping")
        return False

    print(f"  ✓ Parsed {len(pages)} sections")

    # Save pages for skill building
    for page in pages:
        self.save_page(page)
        self.pages.append(page)

    self.llms_txt_detected = True
    self.llms_txt_variants = list(downloaded.keys())

    return True
```

**Step 4: Add llms_txt_variants attribute to __init__**

```python
# cli/doc_scraper.py (in __init__ method, after llms_txt_variant line)

self.llms_txt_variants = []  # Track all downloaded variants
```

**Step 5: Run test to verify it passes**

Run: `source .venv/bin/activate && pytest tests/test_integration.py::TestFullLlmsTxtWorkflow::test_multi_variant_download -v`

Expected: PASS

**Step 6: Commit**

```bash
git add cli/doc_scraper.py tests/test_integration.py
git commit -m "feat: download all llms.txt variants with proper .md extension"
```

---

## Task 4: Remove Content Truncation

**Files:**
- Modify: `cli/doc_scraper.py:714-730` (create_reference_file method)

**Step 1: Write failing test for no truncation**

```python
# tests/test_integration.py (add new test)

def test_no_content_truncation():
    """Test that content is NOT truncated in reference files"""
    from unittest.mock import Mock
    import tempfile
    import os

    config = {
        'name': 'test-no-truncate',
        'base_url': 'https://example.com/docs'
    }

    # Create scraper with long content
    scraper = DocumentationScraper(config, dry_run=False)

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
    ref_file = os.path.join(scraper.skill_dir, 'references', 'test.md')
    with open(ref_file, 'r') as f:
        content = f.read()

    assert long_content in content  # Full content included
    assert long_code in content     # Full code included
    assert '[Content truncated]' not in content
    assert '...' not in content or content.count('...') == 0
```

**Step 2: Run test to verify it fails**

Run: `source .venv/bin/activate && pytest tests/test_integration.py::test_no_content_truncation -v`

Expected: FAIL - content contains "[Content truncated]" or "..."

**Step 3: Remove truncation from create_reference_file()**

```python
# cli/doc_scraper.py (modify create_reference_file method, lines 712-731)

# OLD (line 714-716):
#     if page.get('content'):
#         content = page['content'][:2500]
#         if len(page['content']) > 2500:
#             content += "\n\n*[Content truncated]*"

# NEW (replace with):
    if page.get('content'):
        content = page['content']  # NO TRUNCATION
        lines.append(content)
        lines.append("")

# OLD (line 728-730):
#     lines.append(code[:600])
#     if len(code) > 600:
#         lines.append("...")

# NEW (replace with):
    lines.append(code)  # NO TRUNCATION
    # No "..." suffix
```

**Complete replacement of lines 712-731:**

```python
# cli/doc_scraper.py:712-731 (complete replacement)

        # Content (NO TRUNCATION)
        if page.get('content'):
            lines.append(page['content'])
            lines.append("")

        # Code examples with language (NO TRUNCATION)
        if page.get('code_samples'):
            lines.append("**Examples:**\n")
            for i, sample in enumerate(page['code_samples'][:4], 1):
                lang = sample.get('language', 'unknown')
                code = sample.get('code', sample if isinstance(sample, str) else '')
                lines.append(f"Example {i} ({lang}):")
                lines.append(f"```{lang}")
                lines.append(code)  # Full code, no truncation
                lines.append("```\n")
```

**Step 4: Run test to verify it passes**

Run: `source .venv/bin/activate && pytest tests/test_integration.py::test_no_content_truncation -v`

Expected: PASS

**Step 5: Run full test suite to check for regressions**

Run: `source .venv/bin/activate && pytest tests/ -v`

Expected: All 201+ tests pass

**Step 6: Commit**

```bash
git add cli/doc_scraper.py tests/test_integration.py
git commit -m "feat: remove content truncation in reference files"
```

---

## Task 5: Update Documentation

**Files:**
- Modify: `docs/plans/2025-10-24-active-skills-design.md`
- Modify: `CHANGELOG.md`

**Step 1: Update design doc status**

```markdown
# docs/plans/2025-10-24-active-skills-design.md (update header)

**Status:** Phase 1 Implemented ✅
```

**Step 2: Add CHANGELOG entry**

```markdown
# CHANGELOG.md (add new section at top)

## [Unreleased]

### Added - Phase 1: Active Skills Foundation
- Multi-variant llms.txt detection: downloads all 3 variants (full, standard, small)
- Automatic .txt → .md file extension conversion
- No content truncation: preserves complete documentation
- `detect_all()` method for finding all llms.txt variants
- `get_proper_filename()` for correct .md naming

### Changed
- `_try_llms_txt()` now downloads all available variants instead of just one
- Reference files now contain complete content (no 2500 char limit)
- Code samples now include full code (no 600 char limit)

### Fixed
- File extension bug: llms.txt files now saved as .md
- Content loss: 0% truncation (was 36%)
```

**Step 3: Commit**

```bash
git add docs/plans/2025-10-24-active-skills-design.md CHANGELOG.md
git commit -m "docs: update status for Phase 1 completion"
```

---

## Task 6: Manual Verification

**Files:**
- None (manual testing)

**Step 1: Test with Hono config**

Run: `source .venv/bin/activate && python3 cli/doc_scraper.py --config configs/hono.json`

**Expected output:**
```
🔍 Checking for llms.txt at https://hono.dev/docs...
📌 Using explicit llms_txt_url from config: https://hono.dev/llms-full.txt
  💾 Saved llms-full.md (319000 chars)
📄 Parsing llms-full.md for skill building...
  ✓ Parsed 93 sections
✅ Used llms.txt (explicit) - skipping HTML scraping
```

**Step 2: Verify all 3 files exist with correct extensions**

Run: `ls -lah output/hono/references/llms*.md`

Expected:
```
llms-full.md    319k
llms.md         5.4k
llms-small.md   176k
```

**Step 3: Verify no truncation in reference files**

Run: `grep -c "Content truncated" output/hono/references/*.md`

Expected: 0 matches (no truncation messages)

**Step 4: Check file sizes are correct**

Run: `wc -c output/hono/references/llms-full.md`

Expected: Should match original download size (~319k), not reduced to 203k

**Step 5: Verify all tests still pass**

Run: `source .venv/bin/activate && pytest tests/ -v`

Expected: All tests pass (201+)

---

## Completion Checklist

- [ ] Task 1: Multi-variant detection (detect_all)
- [ ] Task 2: File extension renaming (get_proper_filename)
- [ ] Task 3: Download all variants (_try_llms_txt)
- [ ] Task 4: Remove truncation (create_reference_file)
- [ ] Task 5: Update documentation
- [ ] Task 6: Manual verification
- [ ] All tests passing
- [ ] No regressions in existing functionality

---

## Success Criteria

**Technical:**
- ✅ All 3 variants downloaded when available
- ✅ Files saved with .md extension (not .txt)
- ✅ 0% content truncation (was 36%)
- ✅ All existing tests pass
- ✅ New tests cover all changes

**User Experience:**
- ✅ Hono skill has all 3 files: llms-full.md, llms.md, llms-small.md
- ✅ Reference files contain complete documentation
- ✅ No "[Content truncated]" messages in output

---

## Related Skills

- @superpowers:test-driven-development - Used throughout for TDD approach
- @superpowers:verification-before-completion - Used in Task 6 for manual verification

---

## Notes

- This plan implements Phase 1 from `docs/plans/2025-10-24-active-skills-design.md`
- Phase 2 (Catalog System) and Phase 3 (Active Scripts) will be separate plans
- All changes maintain backward compatibility with existing HTML scraping
- File extension fix (.txt → .md) is critical for proper skill functionality

---

## Estimated Time

- Task 1: 15 minutes
- Task 2: 15 minutes
- Task 3: 30 minutes
- Task 4: 20 minutes
- Task 5: 10 minutes
- Task 6: 15 minutes

**Total: ~1.5 hours**
