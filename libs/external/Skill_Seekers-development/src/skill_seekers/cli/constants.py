"""Configuration constants for Skill Seekers CLI.

This module centralizes all magic numbers and configuration values used
across the CLI tools to improve maintainability and clarity.
"""

# ===== SCRAPING CONFIGURATION =====

# Default scraping limits
DEFAULT_RATE_LIMIT = 0.5  # seconds between requests
DEFAULT_MAX_PAGES = 500   # maximum pages to scrape
DEFAULT_CHECKPOINT_INTERVAL = 1000  # pages between checkpoints
DEFAULT_ASYNC_MODE = False  # use async mode for parallel scraping (opt-in)

# Content analysis limits
CONTENT_PREVIEW_LENGTH = 500  # characters to check for categorization
MAX_PAGES_WARNING_THRESHOLD = 10000  # warn if config exceeds this

# Quality thresholds
MIN_CATEGORIZATION_SCORE = 2  # minimum score for category assignment
URL_MATCH_POINTS = 3  # points for URL keyword match
TITLE_MATCH_POINTS = 2  # points for title keyword match
CONTENT_MATCH_POINTS = 1  # points for content keyword match

# ===== ENHANCEMENT CONFIGURATION =====

# API-based enhancement limits (uses Anthropic API)
API_CONTENT_LIMIT = 100000  # max characters for API enhancement
API_PREVIEW_LIMIT = 40000   # max characters for preview

# Local enhancement limits (uses Claude Code Max)
LOCAL_CONTENT_LIMIT = 50000  # max characters for local enhancement
LOCAL_PREVIEW_LIMIT = 20000  # max characters for preview

# ===== PAGE ESTIMATION =====

# Estimation and discovery settings
DEFAULT_MAX_DISCOVERY = 1000  # default max pages to discover
DISCOVERY_THRESHOLD = 10000   # threshold for warnings

# ===== FILE LIMITS =====

# Output and processing limits
MAX_REFERENCE_FILES = 100  # maximum reference files per skill
MAX_CODE_BLOCKS_PER_PAGE = 5  # maximum code blocks to extract per page

# ===== EXPORT CONSTANTS =====

__all__ = [
    # Scraping
    'DEFAULT_RATE_LIMIT',
    'DEFAULT_MAX_PAGES',
    'DEFAULT_CHECKPOINT_INTERVAL',
    'DEFAULT_ASYNC_MODE',
    'CONTENT_PREVIEW_LENGTH',
    'MAX_PAGES_WARNING_THRESHOLD',
    'MIN_CATEGORIZATION_SCORE',
    'URL_MATCH_POINTS',
    'TITLE_MATCH_POINTS',
    'CONTENT_MATCH_POINTS',
    # Enhancement
    'API_CONTENT_LIMIT',
    'API_PREVIEW_LIMIT',
    'LOCAL_CONTENT_LIMIT',
    'LOCAL_PREVIEW_LIMIT',
    # Estimation
    'DEFAULT_MAX_DISCOVERY',
    'DISCOVERY_THRESHOLD',
    # Limits
    'MAX_REFERENCE_FILES',
    'MAX_CODE_BLOCKS_PER_PAGE',
]
