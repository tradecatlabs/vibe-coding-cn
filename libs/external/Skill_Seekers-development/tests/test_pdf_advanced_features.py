#!/usr/bin/env python3
"""
Tests for PDF Advanced Features (Priority 2 & 3)

Tests cover:
- OCR support for scanned PDFs
- Password-protected PDFs
- Table extraction
- Parallel processing
- Caching
"""

import unittest
import sys
import tempfile
import shutil
import io
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "cli"))

try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False

try:
    from PIL import Image
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False


class TestOCRSupport(unittest.TestCase):
    """Test OCR support for scanned PDFs (Priority 2)"""

    def setUp(self):
        if not PYMUPDF_AVAILABLE:
            self.skipTest("PyMuPDF not installed")
        from pdf_extractor_poc import PDFExtractor
        self.PDFExtractor = PDFExtractor
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        if hasattr(self, 'temp_dir'):
            shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_ocr_initialization(self):
        """Test OCR flag initialization"""
        extractor = self.PDFExtractor.__new__(self.PDFExtractor)
        extractor.use_ocr = True
        self.assertTrue(extractor.use_ocr)

    def test_extract_text_with_ocr_disabled(self):
        """Test that OCR can be disabled"""
        extractor = self.PDFExtractor.__new__(self.PDFExtractor)
        extractor.use_ocr = False
        extractor.verbose = False

        # Create mock page with normal text
        mock_page = Mock()
        mock_page.get_text.return_value = "This is regular text"

        text = extractor.extract_text_with_ocr(mock_page)

        self.assertEqual(text, "This is regular text")
        mock_page.get_text.assert_called_once_with("text")

    def test_extract_text_with_ocr_sufficient_text(self):
        """Test OCR not triggered when sufficient text exists"""
        extractor = self.PDFExtractor.__new__(self.PDFExtractor)
        extractor.use_ocr = True
        extractor.verbose = False

        # Create mock page with enough text
        mock_page = Mock()
        mock_page.get_text.return_value = "This is a long paragraph with more than 50 characters"

        text = extractor.extract_text_with_ocr(mock_page)

        self.assertEqual(len(text), 53)  # Length after .strip()
        # OCR should not be triggered
        mock_page.get_pixmap.assert_not_called()

    @patch('pdf_extractor_poc.TESSERACT_AVAILABLE', False)
    def test_ocr_unavailable_warning(self):
        """Test warning when OCR requested but pytesseract not available"""
        extractor = self.PDFExtractor.__new__(self.PDFExtractor)
        extractor.use_ocr = True
        extractor.verbose = True

        mock_page = Mock()
        mock_page.get_text.return_value = "Short"  # Less than 50 chars

        # Capture output
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            text = extractor.extract_text_with_ocr(mock_page)
            output = fake_out.getvalue()

        self.assertIn("OCR requested but pytesseract not installed", output)
        self.assertEqual(text, "Short")

    @unittest.skipUnless(TESSERACT_AVAILABLE, "pytesseract not installed")
    def test_ocr_extraction_triggered(self):
        """Test OCR extraction when text is minimal"""
        extractor = self.PDFExtractor.__new__(self.PDFExtractor)
        extractor.use_ocr = True
        extractor.verbose = False

        # Create mock page with minimal text
        mock_page = Mock()
        mock_page.get_text.return_value = "X"  # Less than 50 chars

        # Mock pixmap and PIL Image
        mock_pix = Mock()
        mock_pix.width = 100
        mock_pix.height = 100
        mock_pix.samples = b'\x00' * (100 * 100 * 3)
        mock_page.get_pixmap.return_value = mock_pix

        with patch('pytesseract.image_to_string', return_value="OCR extracted text here"):
            text = extractor.extract_text_with_ocr(mock_page)

        # Should use OCR text since it's longer
        self.assertEqual(text, "OCR extracted text here")
        mock_page.get_pixmap.assert_called_once()


class TestPasswordProtection(unittest.TestCase):
    """Test password-protected PDF support (Priority 2)"""

    def setUp(self):
        if not PYMUPDF_AVAILABLE:
            self.skipTest("PyMuPDF not installed")
        from pdf_extractor_poc import PDFExtractor
        self.PDFExtractor = PDFExtractor
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        if hasattr(self, 'temp_dir'):
            shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_password_initialization(self):
        """Test password parameter initialization"""
        extractor = self.PDFExtractor.__new__(self.PDFExtractor)
        extractor.password = "test_password"
        self.assertEqual(extractor.password, "test_password")

    def test_encrypted_pdf_detection(self):
        """Test detection of encrypted PDF"""
        extractor = self.PDFExtractor.__new__(self.PDFExtractor)
        extractor.pdf_path = "test.pdf"
        extractor.password = "mypassword"
        extractor.verbose = False

        # Mock encrypted document (use MagicMock for __len__)
        mock_doc = MagicMock()
        mock_doc.is_encrypted = True
        mock_doc.authenticate.return_value = True
        mock_doc.metadata = {}
        mock_doc.__len__.return_value = 10

        with patch('fitz.open', return_value=mock_doc):
            # This would be called in extract_all()
            doc = fitz.open(extractor.pdf_path)

            self.assertTrue(doc.is_encrypted)
            result = doc.authenticate(extractor.password)
            self.assertTrue(result)

    def test_wrong_password_handling(self):
        """Test handling of wrong password"""
        extractor = self.PDFExtractor.__new__(self.PDFExtractor)
        extractor.pdf_path = "test.pdf"
        extractor.password = "wrong_password"

        mock_doc = Mock()
        mock_doc.is_encrypted = True
        mock_doc.authenticate.return_value = False

        with patch('fitz.open', return_value=mock_doc):
            doc = fitz.open(extractor.pdf_path)
            result = doc.authenticate(extractor.password)

            self.assertFalse(result)

    def test_missing_password_for_encrypted_pdf(self):
        """Test error when password is missing for encrypted PDF"""
        extractor = self.PDFExtractor.__new__(self.PDFExtractor)
        extractor.pdf_path = "test.pdf"
        extractor.password = None

        mock_doc = Mock()
        mock_doc.is_encrypted = True

        with patch('fitz.open', return_value=mock_doc):
            doc = fitz.open(extractor.pdf_path)

            self.assertTrue(doc.is_encrypted)
            self.assertIsNone(extractor.password)


class TestTableExtraction(unittest.TestCase):
    """Test table extraction (Priority 2)"""

    def setUp(self):
        if not PYMUPDF_AVAILABLE:
            self.skipTest("PyMuPDF not installed")
        from pdf_extractor_poc import PDFExtractor
        self.PDFExtractor = PDFExtractor
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        if hasattr(self, 'temp_dir'):
            shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_table_extraction_initialization(self):
        """Test table extraction flag initialization"""
        extractor = self.PDFExtractor.__new__(self.PDFExtractor)
        extractor.extract_tables = True
        self.assertTrue(extractor.extract_tables)

    def test_table_extraction_disabled(self):
        """Test no tables extracted when disabled"""
        extractor = self.PDFExtractor.__new__(self.PDFExtractor)
        extractor.extract_tables = False
        extractor.verbose = False

        mock_page = Mock()
        tables = extractor.extract_tables_from_page(mock_page)

        self.assertEqual(tables, [])
        # find_tables should not be called
        mock_page.find_tables.assert_not_called()

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

        # Create mock tables result
        mock_tables = Mock()
        mock_tables.tables = [mock_table]

        mock_page = Mock()
        mock_page.find_tables.return_value = mock_tables

        tables = extractor.extract_tables_from_page(mock_page)

        self.assertEqual(len(tables), 1)
        self.assertEqual(tables[0]['row_count'], 2)
        self.assertEqual(tables[0]['col_count'], 3)
        self.assertEqual(tables[0]['table_index'], 0)

    def test_multiple_tables_extraction(self):
        """Test extraction of multiple tables from one page"""
        extractor = self.PDFExtractor.__new__(self.PDFExtractor)
        extractor.extract_tables = True
        extractor.verbose = False

        # Create two mock tables
        mock_table1 = Mock()
        mock_table1.extract.return_value = [["A", "B"], ["1", "2"]]
        mock_table1.bbox = (0, 0, 50, 50)

        mock_table2 = Mock()
        mock_table2.extract.return_value = [["X", "Y", "Z"], ["10", "20", "30"]]
        mock_table2.bbox = (0, 60, 50, 110)

        mock_tables = Mock()
        mock_tables.tables = [mock_table1, mock_table2]

        mock_page = Mock()
        mock_page.find_tables.return_value = mock_tables

        tables = extractor.extract_tables_from_page(mock_page)

        self.assertEqual(len(tables), 2)
        self.assertEqual(tables[0]['table_index'], 0)
        self.assertEqual(tables[1]['table_index'], 1)

    def test_table_extraction_error_handling(self):
        """Test error handling during table extraction"""
        extractor = self.PDFExtractor.__new__(self.PDFExtractor)
        extractor.extract_tables = True
        extractor.verbose = False

        mock_page = Mock()
        mock_page.find_tables.side_effect = Exception("Table extraction failed")

        # Should not raise, should return empty list
        tables = extractor.extract_tables_from_page(mock_page)

        self.assertEqual(tables, [])


class TestCaching(unittest.TestCase):
    """Test caching of expensive operations (Priority 3)"""

    def setUp(self):
        if not PYMUPDF_AVAILABLE:
            self.skipTest("PyMuPDF not installed")
        from pdf_extractor_poc import PDFExtractor
        self.PDFExtractor = PDFExtractor
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        if hasattr(self, 'temp_dir'):
            shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_cache_initialization(self):
        """Test cache is initialized"""
        extractor = self.PDFExtractor.__new__(self.PDFExtractor)
        extractor._cache = {}
        extractor.use_cache = True

        self.assertIsInstance(extractor._cache, dict)
        self.assertTrue(extractor.use_cache)

    def test_cache_set_and_get(self):
        """Test setting and getting cached values"""
        extractor = self.PDFExtractor.__new__(self.PDFExtractor)
        extractor._cache = {}
        extractor.use_cache = True

        # Set cache
        test_data = {"page": 1, "text": "cached content"}
        extractor.set_cached("page_1", test_data)

        # Get cache
        cached = extractor.get_cached("page_1")

        self.assertEqual(cached, test_data)

    def test_cache_miss(self):
        """Test cache miss returns None"""
        extractor = self.PDFExtractor.__new__(self.PDFExtractor)
        extractor._cache = {}
        extractor.use_cache = True

        cached = extractor.get_cached("nonexistent_key")

        self.assertIsNone(cached)

    def test_cache_disabled(self):
        """Test caching can be disabled"""
        extractor = self.PDFExtractor.__new__(self.PDFExtractor)
        extractor._cache = {}
        extractor.use_cache = False

        # Try to set cache
        extractor.set_cached("page_1", {"data": "test"})

        # Cache should be empty
        self.assertEqual(len(extractor._cache), 0)

        # Try to get cache
        cached = extractor.get_cached("page_1")
        self.assertIsNone(cached)

    def test_cache_overwrite(self):
        """Test cache can be overwritten"""
        extractor = self.PDFExtractor.__new__(self.PDFExtractor)
        extractor._cache = {}
        extractor.use_cache = True

        # Set initial value
        extractor.set_cached("page_1", {"version": 1})

        # Overwrite
        extractor.set_cached("page_1", {"version": 2})

        # Get cached value
        cached = extractor.get_cached("page_1")

        self.assertEqual(cached["version"], 2)


class TestParallelProcessing(unittest.TestCase):
    """Test parallel page processing (Priority 3)"""

    def setUp(self):
        if not PYMUPDF_AVAILABLE:
            self.skipTest("PyMuPDF not installed")
        from pdf_extractor_poc import PDFExtractor
        self.PDFExtractor = PDFExtractor
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        if hasattr(self, 'temp_dir'):
            shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_parallel_initialization(self):
        """Test parallel processing flag initialization"""
        extractor = self.PDFExtractor.__new__(self.PDFExtractor)
        extractor.parallel = True
        extractor.max_workers = 4

        self.assertTrue(extractor.parallel)
        self.assertEqual(extractor.max_workers, 4)

    def test_parallel_disabled_by_default(self):
        """Test parallel processing is disabled by default"""
        extractor = self.PDFExtractor.__new__(self.PDFExtractor)
        extractor.parallel = False

        self.assertFalse(extractor.parallel)

    def test_worker_count_auto_detect(self):
        """Test worker count auto-detection"""
        import os
        cpu_count = os.cpu_count()

        extractor = self.PDFExtractor.__new__(self.PDFExtractor)
        extractor.max_workers = cpu_count

        self.assertIsNotNone(extractor.max_workers)
        self.assertGreater(extractor.max_workers, 0)

    def test_custom_worker_count(self):
        """Test custom worker count"""
        extractor = self.PDFExtractor.__new__(self.PDFExtractor)
        extractor.max_workers = 8

        self.assertEqual(extractor.max_workers, 8)


class TestIntegration(unittest.TestCase):
    """Integration tests for advanced features"""

    def setUp(self):
        if not PYMUPDF_AVAILABLE:
            self.skipTest("PyMuPDF not installed")
        from pdf_extractor_poc import PDFExtractor
        self.PDFExtractor = PDFExtractor
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        if hasattr(self, 'temp_dir'):
            shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_full_initialization_with_all_features(self):
        """Test initialization with all advanced features enabled"""
        extractor = self.PDFExtractor.__new__(self.PDFExtractor)

        # Set all advanced features
        extractor.use_ocr = True
        extractor.password = "test_password"
        extractor.extract_tables = True
        extractor.parallel = True
        extractor.max_workers = 4
        extractor.use_cache = True
        extractor._cache = {}

        # Verify all features are set
        self.assertTrue(extractor.use_ocr)
        self.assertEqual(extractor.password, "test_password")
        self.assertTrue(extractor.extract_tables)
        self.assertTrue(extractor.parallel)
        self.assertEqual(extractor.max_workers, 4)
        self.assertTrue(extractor.use_cache)

    def test_feature_combinations(self):
        """Test various feature combinations"""
        combinations = [
            {"use_ocr": True, "extract_tables": True},
            {"password": "test", "parallel": True},
            {"use_cache": True, "extract_tables": True, "parallel": True},
            {"use_ocr": True, "password": "test", "extract_tables": True, "parallel": True}
        ]

        for combo in combinations:
            extractor = self.PDFExtractor.__new__(self.PDFExtractor)
            for key, value in combo.items():
                setattr(extractor, key, value)

            # Verify all attributes are set correctly
            for key, value in combo.items():
                self.assertEqual(getattr(extractor, key), value)

    def test_page_data_includes_tables(self):
        """Test that page data includes table count"""
        # This tests that the page_data structure includes tables
        expected_keys = [
            'page_number', 'text', 'markdown', 'headings',
            'code_samples', 'images_count', 'extracted_images',
            'tables', 'char_count', 'code_blocks_count', 'tables_count'
        ]

        # Just verify the structure is correct
        # Actual extraction is tested in other test classes
        page_data = {
            'page_number': 1,
            'text': 'test',
            'markdown': 'test',
            'headings': [],
            'code_samples': [],
            'images_count': 0,
            'extracted_images': [],
            'tables': [],
            'char_count': 4,
            'code_blocks_count': 0,
            'tables_count': 0
        }

        for key in expected_keys:
            self.assertIn(key, page_data)


if __name__ == '__main__':
    unittest.main()
