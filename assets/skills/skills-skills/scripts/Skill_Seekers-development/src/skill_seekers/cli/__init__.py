"""Skill Seekers CLI tools package.

This package provides command-line tools for converting documentation
websites into Claude AI skills.

Main modules:
    - doc_scraper: Main documentation scraping and skill building tool
    - llms_txt_detector: Detect llms.txt files at documentation URLs
    - llms_txt_downloader: Download llms.txt content
    - llms_txt_parser: Parse llms.txt markdown content
    - pdf_scraper: Extract documentation from PDF files
    - enhance_skill: AI-powered skill enhancement (API-based)
    - enhance_skill_local: AI-powered skill enhancement (local)
    - estimate_pages: Estimate page count before scraping
    - package_skill: Package skills into .zip files
    - upload_skill: Upload skills to Claude
    - utils: Shared utility functions
"""

from .llms_txt_detector import LlmsTxtDetector
from .llms_txt_downloader import LlmsTxtDownloader
from .llms_txt_parser import LlmsTxtParser

try:
    from .utils import open_folder, read_reference_files
except ImportError:
    # utils.py might not exist in all configurations
    open_folder = None
    read_reference_files = None

__version__ = "2.0.0"

__all__ = [
    "LlmsTxtDetector",
    "LlmsTxtDownloader",
    "LlmsTxtParser",
    "open_folder",
    "read_reference_files",
]
