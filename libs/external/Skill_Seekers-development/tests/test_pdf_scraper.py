#!/usr/bin/env python3
"""
Tests for PDF Scraper (cli/pdf_scraper.py)

Tests cover:
- Config-based PDF extraction
- Direct PDF path conversion
- JSON-based workflow
- Skill structure generation
- Categorization
- Error handling
"""

import unittest
import sys
import json
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False


class TestPDFToSkillConverter(unittest.TestCase):
    """Test PDFToSkillConverter initialization and basic functionality"""

    def setUp(self):
        if not PYMUPDF_AVAILABLE:
            self.skipTest("PyMuPDF not installed")
        from skill_seekers.cli.pdf_scraper import PDFToSkillConverter
        self.PDFToSkillConverter = PDFToSkillConverter

        # Create temporary directory for test output
        self.temp_dir = tempfile.mkdtemp()
        self.output_dir = Path(self.temp_dir)

    def tearDown(self):
        # Clean up temporary directory
        if hasattr(self, 'temp_dir'):
            shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_init_with_name_and_pdf_path(self):
        """Test initialization with name and PDF path"""
        config = {
            "name": "test_skill",
            "pdf_path": "test.pdf"
        }
        converter = self.PDFToSkillConverter(config)

        self.assertEqual(converter.name, "test_skill")
        self.assertEqual(converter.pdf_path, "test.pdf")

    def test_init_with_config(self):
        """Test initialization with config file"""
        # Create test config
        config = {
            "name": "config_skill",
            "description": "Test skill",
            "pdf_path": "docs/test.pdf",
            "extract_options": {
                "chunk_size": 10,
                "min_quality": 5.0
            }
        }

        converter = self.PDFToSkillConverter(config)

        self.assertEqual(converter.name, "config_skill")
        self.assertEqual(converter.config.get("description"), "Test skill")

    def test_init_requires_name_or_config(self):
        """Test that initialization requires config dict with 'name' field"""
        with self.assertRaises((ValueError, TypeError, KeyError)):
            self.PDFToSkillConverter({})


class TestCategorization(unittest.TestCase):
    """Test content categorization functionality"""

    def setUp(self):
        if not PYMUPDF_AVAILABLE:
            self.skipTest("PyMuPDF not installed")
        from skill_seekers.cli.pdf_scraper import PDFToSkillConverter
        self.PDFToSkillConverter = PDFToSkillConverter
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_categorize_by_keywords(self):
        """Test categorization using keyword matching"""
        config = {
            "name": "test",
            "pdf_path": "test.pdf",
            "categories": {
                "getting_started": ["introduction", "getting started"],
                "api": ["api", "reference", "function"]
            }
        }

        converter = self.PDFToSkillConverter(config)

        # Mock extracted data with different content
        converter.extracted_data = {
            "pages": [
                {
                    "page_number": 1,
                    "text": "Introduction to the API",
                    "chapter": "Chapter 1: Getting Started"
                },
                {
                    "page_number": 2,
                    "text": "API reference for functions",
                    "chapter": None
                }
            ]
        }

        categories = converter.categorize_content()

        # Should have both categories
        self.assertIn("getting_started", categories)
        self.assertIn("api", categories)

    def test_categorize_by_chapters(self):
        """Test categorization using chapter information"""
        config = {
            "name": "test",
            "pdf_path": "test.pdf"
        }
        converter = self.PDFToSkillConverter(config)

        # Mock data with chapters
        converter.extracted_data = {
            "pages": [
                {
                    "page_number": 1,
                    "text": "Content here",
                    "chapter": "Chapter 1: Introduction"
                },
                {
                    "page_number": 2,
                    "text": "More content",
                    "chapter": "Chapter 1: Introduction"
                },
                {
                    "page_number": 3,
                    "text": "New chapter",
                    "chapter": "Chapter 2: Advanced Topics"
                }
            ]
        }

        categories = converter.categorize_content()

        # Should create categories based on chapters
        self.assertIsInstance(categories, dict)
        self.assertGreater(len(categories), 0)

    def test_categorize_handles_no_chapters(self):
        """Test categorization when no chapters are detected"""
        config = {
            "name": "test",
            "pdf_path": "test.pdf"
        }
        converter = self.PDFToSkillConverter(config)

        # Mock data without chapters
        converter.extracted_data = {
            "pages": [
                {
                    "page_number": 1,
                    "text": "Some content",
                    "chapter": None
                }
            ]
        }

        categories = converter.categorize_content()

        # Should still create categories (fallback to "other")
        self.assertIsInstance(categories, dict)


class TestSkillBuilding(unittest.TestCase):
    """Test skill structure generation"""

    def setUp(self):
        if not PYMUPDF_AVAILABLE:
            self.skipTest("PyMuPDF not installed")
        from skill_seekers.cli.pdf_scraper import PDFToSkillConverter
        self.PDFToSkillConverter = PDFToSkillConverter
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_build_skill_creates_structure(self):
        """Test that build_skill creates required directory structure"""
        config = {
            "name": "test_skill",
            "pdf_path": "test.pdf"
        }
        converter = self.PDFToSkillConverter(config)

        # Override skill_dir to use temp directory
        converter.skill_dir = str(Path(self.temp_dir) / "test_skill")

        # Mock extracted data
        converter.extracted_data = {
            "pages": [
                {
                    "page_number": 1,
                    "text": "Test content",
                    "code_blocks": [],
                    "images": []
                }
            ],
            "total_pages": 1
        }

        # Mock categorization
        converter.categories = {
            "getting_started": [converter.extracted_data["pages"][0]]
        }

        converter.build_skill()

        # Check directory structure
        skill_dir = Path(self.temp_dir) / "test_skill"
        self.assertTrue(skill_dir.exists())
        self.assertTrue((skill_dir / "references").exists())
        self.assertTrue((skill_dir / "scripts").exists())
        self.assertTrue((skill_dir / "assets").exists())

    def test_build_skill_creates_skill_md(self):
        """Test that SKILL.md is created"""
        config = {
            "name": "test_skill",
            "pdf_path": "test.pdf",
            "description": "Test description"
        }
        converter = self.PDFToSkillConverter(config)

        # Override skill_dir to use temp directory
        converter.skill_dir = str(Path(self.temp_dir) / "test_skill")

        converter.extracted_data = {
            "pages": [{"page_number": 1, "text": "Test", "code_blocks": [], "images": []}],
            "total_pages": 1
        }
        converter.categories = {"test": [converter.extracted_data["pages"][0]]}

        converter.build_skill()

        skill_md = Path(self.temp_dir) / "test_skill" / "SKILL.md"
        self.assertTrue(skill_md.exists())

        # Check content
        content = skill_md.read_text()
        self.assertIn("test_skill", content)
        self.assertIn("Test description", content)

    def test_build_skill_creates_reference_files(self):
        """Test that reference files are created for categories"""
        config = {
            "name": "test_skill",
            "pdf_path": "test.pdf"
        }
        converter = self.PDFToSkillConverter(config)

        # Override skill_dir to use temp directory
        converter.skill_dir = str(Path(self.temp_dir) / "test_skill")

        converter.extracted_data = {
            "pages": [
                {"page_number": 1, "text": "Getting started", "code_blocks": [], "images": []},
                {"page_number": 2, "text": "API reference", "code_blocks": [], "images": []}
            ],
            "total_pages": 2
        }

        converter.categories = {
            "getting_started": [converter.extracted_data["pages"][0]],
            "api": [converter.extracted_data["pages"][1]]
        }

        converter.build_skill()

        # Check reference files exist
        refs_dir = Path(self.temp_dir) / "test_skill" / "references"
        self.assertTrue((refs_dir / "getting_started.md").exists())
        self.assertTrue((refs_dir / "api.md").exists())
        self.assertTrue((refs_dir / "index.md").exists())


class TestCodeBlockHandling(unittest.TestCase):
    """Test code block extraction and inclusion in references"""

    def setUp(self):
        if not PYMUPDF_AVAILABLE:
            self.skipTest("PyMuPDF not installed")
        from skill_seekers.cli.pdf_scraper import PDFToSkillConverter
        self.PDFToSkillConverter = PDFToSkillConverter
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_code_blocks_included_in_references(self):
        """Test that code blocks are included in reference files"""
        config = {
            "name": "test_skill",
            "pdf_path": "test.pdf"
        }
        converter = self.PDFToSkillConverter(config)

        # Override skill_dir to use temp directory
        converter.skill_dir = str(Path(self.temp_dir) / "test_skill")

        # Mock data with code blocks
        converter.extracted_data = {
            "pages": [
                {
                    "page_number": 1,
                    "text": "Example code",
                    "code_blocks": [
                        {
                            "code": "def hello():\n    print('world')",
                            "language": "python",
                            "quality": 8.0
                        }
                    ],
                    "images": []
                }
            ],
            "total_pages": 1
        }

        converter.categories = {
            "examples": [converter.extracted_data["pages"][0]]
        }

        converter.build_skill()

        # Check code block in reference file
        ref_file = Path(self.temp_dir) / "test_skill" / "references" / "examples.md"
        content = ref_file.read_text()

        self.assertIn("```python", content)
        self.assertIn("def hello()", content)
        self.assertIn("print('world')", content)

    def test_high_quality_code_preferred(self):
        """Test that high-quality code blocks are prioritized"""
        config = {
            "name": "test_skill",
            "pdf_path": "test.pdf"
        }
        converter = self.PDFToSkillConverter(config)

        # Override skill_dir to use temp directory
        converter.skill_dir = str(Path(self.temp_dir) / "test_skill")

        # Mock data with varying quality
        converter.extracted_data = {
            "pages": [
                {
                    "page_number": 1,
                    "text": "Code examples",
                    "code_blocks": [
                        {"code": "x = 1", "language": "python", "quality": 2.0},
                        {"code": "def process():\n    return result", "language": "python", "quality": 9.0}
                    ],
                    "images": []
                }
            ],
            "total_pages": 1
        }

        converter.categories = {"examples": [converter.extracted_data["pages"][0]]}
        converter.build_skill()

        ref_file = Path(self.temp_dir) / "test_skill" / "references" / "examples.md"
        content = ref_file.read_text()

        # High quality code should be included
        self.assertIn("def process()", content)


class TestImageHandling(unittest.TestCase):
    """Test image extraction and handling"""

    def setUp(self):
        if not PYMUPDF_AVAILABLE:
            self.skipTest("PyMuPDF not installed")
        from skill_seekers.cli.pdf_scraper import PDFToSkillConverter
        self.PDFToSkillConverter = PDFToSkillConverter
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_images_saved_to_assets(self):
        """Test that images are saved to assets directory"""
        config = {
            "name": "test_skill",
            "pdf_path": "test.pdf"
        }
        converter = self.PDFToSkillConverter(config)

        # Override skill_dir to use temp directory
        converter.skill_dir = str(Path(self.temp_dir) / "test_skill")

        # Mock image data (1x1 white PNG)
        mock_image_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'

        converter.extracted_data = {
            "pages": [
                {
                    "page_number": 1,
                    "text": "See diagram",
                    "code_blocks": [],
                    "images": [
                        {
                            "page": 1,
                            "index": 0,
                            "width": 100,
                            "height": 100,
                            "data": mock_image_bytes
                        }
                    ]
                }
            ],
            "total_pages": 1
        }

        converter.categories = {"diagrams": [converter.extracted_data["pages"][0]]}
        converter.build_skill()

        # Check assets directory has image
        assets_dir = Path(self.temp_dir) / "test_skill" / "assets"
        image_files = list(assets_dir.glob("*.png"))
        self.assertGreater(len(image_files), 0)

    def test_image_references_in_markdown(self):
        """Test that images are referenced in markdown files"""
        config = {
            "name": "test_skill",
            "pdf_path": "test.pdf"
        }
        converter = self.PDFToSkillConverter(config)

        # Override skill_dir to use temp directory
        converter.skill_dir = str(Path(self.temp_dir) / "test_skill")

        mock_image_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'

        converter.extracted_data = {
            "pages": [
                {
                    "page_number": 1,
                    "text": "Architecture diagram",
                    "code_blocks": [],
                    "images": [
                        {
                            "page": 1,
                            "index": 0,
                            "width": 200,
                            "height": 150,
                            "data": mock_image_bytes
                        }
                    ]
                }
            ],
            "total_pages": 1
        }

        converter.categories = {"architecture": [converter.extracted_data["pages"][0]]}
        converter.build_skill()

        # Check markdown has image reference
        ref_file = Path(self.temp_dir) / "test_skill" / "references" / "architecture.md"
        content = ref_file.read_text()

        self.assertIn("![", content)  # Markdown image syntax
        self.assertIn("../assets/", content)  # Relative path to assets


class TestErrorHandling(unittest.TestCase):
    """Test error handling for invalid inputs"""

    def setUp(self):
        if not PYMUPDF_AVAILABLE:
            self.skipTest("PyMuPDF not installed")
        from skill_seekers.cli.pdf_scraper import PDFToSkillConverter
        self.PDFToSkillConverter = PDFToSkillConverter
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_missing_pdf_file(self):
        """Test error when PDF file doesn't exist"""
        config = {
            "name": "test",
            "pdf_path": "nonexistent.pdf"
        }
        converter = self.PDFToSkillConverter(config)

        with self.assertRaises((FileNotFoundError, RuntimeError)):
            converter.extract_pdf()

    def test_invalid_config_file(self):
        """Test error when config dict is invalid"""
        invalid_config = "invalid string not a dict"

        with self.assertRaises((ValueError, TypeError, AttributeError)):
            self.PDFToSkillConverter(invalid_config)

    def test_missing_required_config_fields(self):
        """Test error when config is missing required fields"""
        config = {"description": "Missing name and pdf_path"}

        with self.assertRaises((ValueError, KeyError)):
            converter = self.PDFToSkillConverter(config)
            converter.extract_pdf()


class TestJSONWorkflow(unittest.TestCase):
    """Test building skills from extracted JSON"""

    def setUp(self):
        if not PYMUPDF_AVAILABLE:
            self.skipTest("PyMuPDF not installed")
        from skill_seekers.cli.pdf_scraper import PDFToSkillConverter
        self.PDFToSkillConverter = PDFToSkillConverter
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_load_from_json(self):
        """Test loading extracted data from JSON file"""
        # Create mock extracted JSON
        extracted_data = {
            "pages": [
                {
                    "page_number": 1,
                    "text": "Test content",
                    "code_blocks": [],
                    "images": []
                }
            ],
            "total_pages": 1,
            "metadata": {
                "title": "Test PDF"
            }
        }

        json_path = Path(self.temp_dir) / "extracted.json"
        json_path.write_text(json.dumps(extracted_data, indent=2))

        config = {
            "name": "test_skill",
            "pdf_path": "test.pdf"
        }
        converter = self.PDFToSkillConverter(config)
        converter.load_extracted_data(str(json_path))

        self.assertEqual(converter.extracted_data["total_pages"], 1)
        self.assertEqual(len(converter.extracted_data["pages"]), 1)

    def test_build_from_json_without_extraction(self):
        """Test that from_json workflow skips PDF extraction"""
        extracted_data = {
            "pages": [{"page_number": 1, "text": "Content", "code_blocks": [], "images": []}],
            "total_pages": 1
        }

        json_path = Path(self.temp_dir) / "extracted.json"
        json_path.write_text(json.dumps(extracted_data))

        config = {
            "name": "test_skill",
            "pdf_path": "test.pdf"
        }
        converter = self.PDFToSkillConverter(config)
        converter.load_extracted_data(str(json_path))

        # Should have data loaded without calling extract_pdf()
        self.assertIsNotNone(converter.extracted_data)
        self.assertEqual(converter.extracted_data["total_pages"], 1)


if __name__ == '__main__':
    unittest.main()
