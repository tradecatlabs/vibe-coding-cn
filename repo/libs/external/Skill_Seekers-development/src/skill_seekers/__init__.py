"""
Skill Seekers - Convert documentation, GitHub repos, and PDFs into Claude AI skills.

This package provides tools for automatically scraping, organizing, and packaging
documentation from various sources into uploadable Claude AI skills.
"""

__version__ = "2.0.0"
__author__ = "Yusuf Karaaslan"
__license__ = "MIT"

# Expose main components for easier imports
from skill_seekers.cli import __version__ as cli_version
from skill_seekers.mcp import __version__ as mcp_version

__all__ = [
    "__version__",
    "__author__",
    "__license__",
    "cli_version",
    "mcp_version",
]
