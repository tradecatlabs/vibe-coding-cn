# PDF Parsing Libraries Research (Task B1.1)

**Date:** October 21, 2025
**Task:** B1.1 - Research PDF parsing libraries
**Purpose:** Evaluate Python libraries for extracting text and code from PDF documentation

---

## Executive Summary

After comprehensive research, **PyMuPDF (fitz)** is recommended as the primary library for Skill Seeker's PDF parsing needs, with **pdfplumber** as a secondary option for complex table extraction.

### Quick Recommendation:
- **Primary Choice:** PyMuPDF (fitz) - Fast, comprehensive, well-maintained
- **Secondary/Fallback:** pdfplumber - Better for tables, slower but more precise
- **Avoid:** PyPDF2 (deprecated, merged into pypdf)

---

## Library Comparison Matrix

| Library | Speed | Text Quality | Code Detection | Tables | Maintenance | License |
|---------|-------|--------------|----------------|--------|-------------|---------|
| **PyMuPDF** | ⚡⚡⚡⚡⚡ Fastest (42ms) | High | Excellent | Good | Active | AGPL/Commercial |
| **pdfplumber** | ⚡⚡ Slower (2.5s) | Very High | Excellent | Excellent | Active | MIT |
| **pypdf** | ⚡⚡⚡ Fast | Medium | Good | Basic | Active | BSD |
| **pdfminer.six** | ⚡ Slow | Very High | Good | Medium | Active | MIT |
| **pypdfium2** | ⚡⚡⚡⚡⚡ Very Fast (3ms) | Medium | Good | Basic | Active | Apache-2.0 |

---

## Detailed Analysis

### 1. PyMuPDF (fitz) ⭐ RECOMMENDED

**Performance:** 42 milliseconds (60x faster than pdfminer.six)

**Installation:**
```bash
pip install PyMuPDF
```

**Pros:**
- ✅ Extremely fast (C-based MuPDF backend)
- ✅ Comprehensive features (text, images, tables, metadata)
- ✅ Supports markdown output
- ✅ Can extract images and diagrams
- ✅ Well-documented and actively maintained
- ✅ Handles complex layouts well

**Cons:**
- ⚠️ AGPL license (requires commercial license for proprietary projects)
- ⚠️ Requires MuPDF binary installation (handled by pip)
- ⚠️ Slightly larger dependency footprint

**Code Example:**
```python
import fitz  # PyMuPDF

# Extract text from entire PDF
def extract_pdf_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ''
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

# Extract text from single page
def extract_page_text(pdf_path, page_num):
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_num)
    text = page.get_text()
    doc.close()
    return text

# Extract with markdown formatting
def extract_as_markdown(pdf_path):
    doc = fitz.open(pdf_path)
    markdown = ''
    for page in doc:
        markdown += page.get_text("markdown")
    doc.close()
    return markdown
```

**Use Cases for Skill Seeker:**
- Fast extraction of code examples from PDF docs
- Preserving formatting for code blocks
- Extracting diagrams and screenshots
- High-volume documentation scraping

---

### 2. pdfplumber ⭐ RECOMMENDED (for tables)

**Performance:** ~2.5 seconds (slower but more precise)

**Installation:**
```bash
pip install pdfplumber
```

**Pros:**
- ✅ MIT license (fully open source)
- ✅ Exceptional table extraction
- ✅ Visual debugging tool
- ✅ Precise layout preservation
- ✅ Built on pdfminer (proven text extraction)
- ✅ No binary dependencies

**Cons:**
- ⚠️ Slower than PyMuPDF
- ⚠️ Higher memory usage for large PDFs
- ⚠️ Requires more configuration for optimal results

**Code Example:**
```python
import pdfplumber

# Extract text from PDF
def extract_with_pdfplumber(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
        return text

# Extract tables
def extract_tables(pdf_path):
    tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_tables = page.extract_tables()
            tables.extend(page_tables)
    return tables

# Extract specific region (for code blocks)
def extract_region(pdf_path, page_num, bbox):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[page_num]
        cropped = page.crop(bbox)
        return cropped.extract_text()
```

**Use Cases for Skill Seeker:**
- Extracting API reference tables from PDFs
- Precise code block extraction with layout
- Documentation with complex table structures

---

### 3. pypdf (formerly PyPDF2)

**Performance:** Fast (medium speed)

**Installation:**
```bash
pip install pypdf
```

**Pros:**
- ✅ BSD license
- ✅ Simple API
- ✅ Can modify PDFs (merge, split, encrypt)
- ✅ Actively maintained (PyPDF2 merged back)
- ✅ No external dependencies

**Cons:**
- ⚠️ Limited complex layout support
- ⚠️ Basic text extraction only
- ⚠️ Poor with scanned/image PDFs
- ⚠️ No table extraction

**Code Example:**
```python
from pypdf import PdfReader

# Extract text
def extract_with_pypdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text
```

**Use Cases for Skill Seeker:**
- Simple text extraction
- Fallback when PyMuPDF licensing is an issue
- Basic PDF manipulation tasks

---

### 4. pdfminer.six

**Performance:** Slow (~2.5 seconds)

**Installation:**
```bash
pip install pdfminer.six
```

**Pros:**
- ✅ MIT license
- ✅ Excellent text quality (preserves formatting)
- ✅ Handles complex layouts
- ✅ Pure Python (no binaries)

**Cons:**
- ⚠️ Slowest option
- ⚠️ Complex API
- ⚠️ Poor documentation
- ⚠️ Limited table support

**Use Cases for Skill Seeker:**
- Not recommended (pdfplumber is built on this with better API)

---

### 5. pypdfium2

**Performance:** Very fast (3ms - fastest tested)

**Installation:**
```bash
pip install pypdfium2
```

**Pros:**
- ✅ Extremely fast
- ✅ Apache 2.0 license
- ✅ Lightweight
- ✅ Clean output

**Cons:**
- ⚠️ Basic features only
- ⚠️ Limited documentation
- ⚠️ No table extraction
- ⚠️ Newer/less proven

**Use Cases for Skill Seeker:**
- High-speed basic extraction
- Potential future optimization

---

## Licensing Considerations

### Open Source Projects (Skill Seeker):
- **PyMuPDF:** ✅ AGPL license is fine for open-source projects
- **pdfplumber:** ✅ MIT license (most permissive)
- **pypdf:** ✅ BSD license (permissive)

### Important Note:
PyMuPDF requires AGPL compliance (source code must be shared) OR a commercial license for proprietary use. Since Skill Seeker is open source on GitHub, AGPL is acceptable.

---

## Performance Benchmarks

Based on 2025 testing:

| Library | Time (single page) | Time (100 pages) |
|---------|-------------------|------------------|
| pypdfium2 | 0.003s | 0.3s |
| PyMuPDF | 0.042s | 4.2s |
| pypdf | 0.1s | 10s |
| pdfplumber | 2.5s | 250s |
| pdfminer.six | 2.5s | 250s |

**Winner:** pypdfium2 (speed) / PyMuPDF (features + speed balance)

---

## Recommendations for Skill Seeker

### Primary Approach: PyMuPDF (fitz)

**Why:**
1. **Speed** - 60x faster than alternatives
2. **Features** - Text, images, markdown output, metadata
3. **Quality** - High-quality text extraction
4. **Maintained** - Active development, good docs
5. **License** - AGPL is fine for open source

**Implementation Strategy:**
```python
import fitz  # PyMuPDF

def extract_pdf_documentation(pdf_path):
    """
    Extract documentation from PDF with code block detection
    """
    doc = fitz.open(pdf_path)
    pages = []

    for page_num, page in enumerate(doc):
        # Get text with layout info
        text = page.get_text("text")

        # Get markdown (preserves code blocks)
        markdown = page.get_text("markdown")

        # Get images (for diagrams)
        images = page.get_images()

        pages.append({
            'page_number': page_num,
            'text': text,
            'markdown': markdown,
            'images': images
        })

    doc.close()
    return pages
```

### Fallback Approach: pdfplumber

**When to use:**
- PDF has complex tables that PyMuPDF misses
- Need visual debugging
- License concerns (use MIT instead of AGPL)

**Implementation Strategy:**
```python
import pdfplumber

def extract_pdf_tables(pdf_path):
    """
    Extract tables from PDF documentation
    """
    with pdfplumber.open(pdf_path) as pdf:
        tables = []
        for page in pdf.pages:
            page_tables = page.extract_tables()
            if page_tables:
                tables.extend(page_tables)
        return tables
```

---

## Code Block Detection Strategy

PDFs don't have semantic "code block" markers like HTML. Detection strategies:

### 1. Font-based Detection
```python
# PyMuPDF can detect font changes
def detect_code_by_font(page):
    blocks = page.get_text("dict")["blocks"]
    code_blocks = []

    for block in blocks:
        if 'lines' in block:
            for line in block['lines']:
                for span in line['spans']:
                    font = span['font']
                    # Monospace fonts indicate code
                    if 'Courier' in font or 'Mono' in font:
                        code_blocks.append(span['text'])

    return code_blocks
```

### 2. Indentation-based Detection
```python
def detect_code_by_indent(text):
    lines = text.split('\n')
    code_blocks = []
    current_block = []

    for line in lines:
        # Code often has consistent indentation
        if line.startswith('    ') or line.startswith('\t'):
            current_block.append(line)
        elif current_block:
            code_blocks.append('\n'.join(current_block))
            current_block = []

    return code_blocks
```

### 3. Pattern-based Detection
```python
import re

def detect_code_by_pattern(text):
    # Look for common code patterns
    patterns = [
        r'(def \w+\(.*?\):)',  # Python functions
        r'(function \w+\(.*?\) \{)',  # JavaScript
        r'(class \w+:)',  # Python classes
        r'(import \w+)',  # Import statements
    ]

    code_snippets = []
    for pattern in patterns:
        matches = re.findall(pattern, text)
        code_snippets.extend(matches)

    return code_snippets
```

---

## Next Steps (Task B1.2+)

### Immediate Next Task: B1.2 - Create Simple PDF Text Extractor

**Goal:** Proof of concept using PyMuPDF

**Implementation Plan:**
1. Create `cli/pdf_extractor_poc.py`
2. Extract text from sample PDF
3. Detect code blocks using font/pattern matching
4. Output to JSON (similar to web scraper)

**Dependencies:**
```bash
pip install PyMuPDF
```

**Expected Output:**
```json
{
  "pages": [
    {
      "page_number": 1,
      "text": "...",
      "code_blocks": ["def main():", "import sys"],
      "images": []
    }
  ]
}
```

### Future Tasks:
- **B1.3:** Add page chunking (split large PDFs)
- **B1.4:** Improve code block detection
- **B1.5:** Extract images/diagrams
- **B1.6:** Create full `pdf_scraper.py` CLI
- **B1.7:** Add MCP tool integration
- **B1.8:** Create PDF config format

---

## Additional Resources

### Documentation:
- PyMuPDF: https://pymupdf.readthedocs.io/
- pdfplumber: https://github.com/jsvine/pdfplumber
- pypdf: https://pypdf.readthedocs.io/

### Comparison Studies:
- 2025 Comparative Study: https://arxiv.org/html/2410.09871v1
- Performance Benchmarks: https://github.com/py-pdf/benchmarks

### Example Use Cases:
- Extracting API docs from PDF manuals
- Converting PDF guides to markdown
- Building skills from PDF-only documentation

---

## Conclusion

**For Skill Seeker's PDF documentation extraction:**

1. **Use PyMuPDF (fitz)** as primary library
2. **Add pdfplumber** for complex table extraction
3. **Detect code blocks** using font + pattern matching
4. **Preserve formatting** with markdown output
5. **Extract images** for diagrams/screenshots

**Estimated Implementation Time:**
- B1.2 (POC): 2-3 hours
- B1.3-B1.5 (Features): 5-8 hours
- B1.6 (CLI): 3-4 hours
- B1.7 (MCP): 2-3 hours
- B1.8 (Config): 1-2 hours
- **Total: 13-20 hours** for complete PDF support

**License:** AGPL (PyMuPDF) is acceptable for Skill Seeker (open source)

---

**Research completed:** ✅ October 21, 2025
**Next task:** B1.2 - Create simple PDF text extractor (proof of concept)
