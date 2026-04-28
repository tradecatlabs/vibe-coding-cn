#!/usr/bin/env python3
"""
Documentation to Claude Skill Converter
Single tool to scrape any documentation and create high-quality Claude skills.

Usage:
    skill-seekers scrape --interactive
    skill-seekers scrape --config configs/godot.json
    skill-seekers scrape --url https://react.dev/ --name react
"""

import os
import sys
import json
import time
import re
import argparse
import hashlib
import logging
import asyncio
import requests
import httpx
from pathlib import Path
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from collections import deque, defaultdict
from typing import Optional, Dict, List, Tuple, Set, Deque, Any

# Add parent directory to path for imports when run as script
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skill_seekers.cli.llms_txt_detector import LlmsTxtDetector
from skill_seekers.cli.llms_txt_parser import LlmsTxtParser
from skill_seekers.cli.llms_txt_downloader import LlmsTxtDownloader
from skill_seekers.cli.constants import (
    DEFAULT_RATE_LIMIT,
    DEFAULT_MAX_PAGES,
    DEFAULT_CHECKPOINT_INTERVAL,
    DEFAULT_ASYNC_MODE,
    CONTENT_PREVIEW_LENGTH,
    MAX_PAGES_WARNING_THRESHOLD,
    MIN_CATEGORIZATION_SCORE
)

# Configure logging
logger = logging.getLogger(__name__)


def setup_logging(verbose: bool = False, quiet: bool = False) -> None:
    """Configure logging based on verbosity level.

    Args:
        verbose: Enable DEBUG level logging
        quiet: Enable WARNING level logging only
    """
    if quiet:
        level = logging.WARNING
    elif verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO

    logging.basicConfig(
        level=level,
        format='%(message)s',
        force=True
    )


class DocToSkillConverter:
    def __init__(self, config: Dict[str, Any], dry_run: bool = False, resume: bool = False) -> None:
        self.config = config
        self.name = config['name']
        self.base_url = config['base_url']
        self.dry_run = dry_run
        self.resume = resume

        # Paths
        self.data_dir = f"output/{self.name}_data"
        self.skill_dir = f"output/{self.name}"
        self.checkpoint_file = f"{self.data_dir}/checkpoint.json"

        # Checkpoint config
        checkpoint_config = config.get('checkpoint', {})
        self.checkpoint_enabled = checkpoint_config.get('enabled', False)
        self.checkpoint_interval = checkpoint_config.get('interval', DEFAULT_CHECKPOINT_INTERVAL)

        # llms.txt detection state
        skip_llms_txt_value = config.get('skip_llms_txt', False)
        if not isinstance(skip_llms_txt_value, bool):
            logger.warning(
                "Invalid value for 'skip_llms_txt': %r (expected bool). Defaulting to False.",
                skip_llms_txt_value
            )
            self.skip_llms_txt = False
        else:
            self.skip_llms_txt = skip_llms_txt_value
        self.llms_txt_detected = False
        self.llms_txt_variant = None
        self.llms_txt_variants: List[str] = []  # Track all downloaded variants

        # Parallel scraping config
        self.workers = config.get('workers', 1)
        self.async_mode = config.get('async_mode', DEFAULT_ASYNC_MODE)

        # State
        self.visited_urls: set[str] = set()
        # Support multiple starting URLs
        start_urls = config.get('start_urls', [self.base_url])
        self.pending_urls = deque(start_urls)
        self.pages: List[Dict[str, Any]] = []
        self.pages_scraped = 0

        # Thread-safe lock for parallel scraping
        if self.workers > 1:
            import threading
            self.lock = threading.Lock()

        # Create directories (unless dry-run)
        if not dry_run:
            os.makedirs(f"{self.data_dir}/pages", exist_ok=True)
            os.makedirs(f"{self.skill_dir}/references", exist_ok=True)
            os.makedirs(f"{self.skill_dir}/scripts", exist_ok=True)
            os.makedirs(f"{self.skill_dir}/assets", exist_ok=True)

        # Load checkpoint if resuming
        if resume and not dry_run:
            self.load_checkpoint()
    
    def is_valid_url(self, url: str) -> bool:
        """Check if URL should be scraped based on patterns.

        Args:
            url (str): URL to validate

        Returns:
            bool: True if URL matches include patterns and doesn't match exclude patterns
        """
        if not url.startswith(self.base_url):
            return False

        # Include patterns
        includes = self.config.get('url_patterns', {}).get('include', [])
        if includes and not any(pattern in url for pattern in includes):
            return False

        # Exclude patterns
        excludes = self.config.get('url_patterns', {}).get('exclude', [])
        if any(pattern in url for pattern in excludes):
            return False

        return True

    def save_checkpoint(self) -> None:
        """Save progress checkpoint"""
        if not self.checkpoint_enabled or self.dry_run:
            return

        checkpoint_data = {
            "config": self.config,
            "visited_urls": list(self.visited_urls),
            "pending_urls": list(self.pending_urls),
            "pages_scraped": self.pages_scraped,
            "last_updated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "checkpoint_interval": self.checkpoint_interval
        }

        try:
            with open(self.checkpoint_file, 'w') as f:
                json.dump(checkpoint_data, f, indent=2)
            logger.info("  💾 Checkpoint saved (%d pages)", self.pages_scraped)
        except Exception as e:
            logger.warning("  ⚠️  Failed to save checkpoint: %s", e)

    def load_checkpoint(self) -> None:
        """Load progress from checkpoint"""
        if not os.path.exists(self.checkpoint_file):
            logger.info("ℹ️  No checkpoint found, starting fresh")
            return

        try:
            with open(self.checkpoint_file, 'r') as f:
                checkpoint_data = json.load(f)

            self.visited_urls = set(checkpoint_data["visited_urls"])
            self.pending_urls = deque(checkpoint_data["pending_urls"])
            self.pages_scraped = checkpoint_data["pages_scraped"]

            logger.info("✅ Resumed from checkpoint")
            logger.info("   Pages already scraped: %d", self.pages_scraped)
            logger.info("   URLs visited: %d", len(self.visited_urls))
            logger.info("   URLs pending: %d", len(self.pending_urls))
            logger.info("   Last updated: %s", checkpoint_data['last_updated'])
            logger.info("")

        except Exception as e:
            logger.warning("⚠️  Failed to load checkpoint: %s", e)
            logger.info("   Starting fresh")

    def clear_checkpoint(self) -> None:
        """Remove checkpoint file"""
        if os.path.exists(self.checkpoint_file):
            try:
                os.remove(self.checkpoint_file)
                logger.info("✅ Checkpoint cleared")
            except Exception as e:
                logger.warning("⚠️  Failed to clear checkpoint: %s", e)

    def extract_content(self, soup: Any, url: str) -> Dict[str, Any]:
        """Extract content with improved code and pattern detection"""
        page = {
            'url': url,
            'title': '',
            'content': '',
            'headings': [],
            'code_samples': [],
            'patterns': [],  # NEW: Extract common patterns
            'links': []
        }
        
        selectors = self.config.get('selectors', {})
        
        # Extract title
        title_elem = soup.select_one(selectors.get('title', 'title'))
        if title_elem:
            page['title'] = self.clean_text(title_elem.get_text())
        
        # Find main content
        main_selector = selectors.get('main_content', 'div[role="main"]')
        main = soup.select_one(main_selector)
        
        if not main:
            logger.warning("⚠ No content: %s", url)
            return page
        
        # Extract headings with better structure
        for h in main.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            text = self.clean_text(h.get_text())
            if text:
                page['headings'].append({
                    'level': h.name,
                    'text': text,
                    'id': h.get('id', '')
                })
        
        # Extract code with language detection
        code_selector = selectors.get('code_blocks', 'pre code')
        for code_elem in main.select(code_selector):
            code = code_elem.get_text()
            if len(code.strip()) > 10:
                # Try to detect language
                lang = self.detect_language(code_elem, code)
                page['code_samples'].append({
                    'code': code.strip(),
                    'language': lang
                })
        
        # Extract patterns (NEW: common code patterns)
        page['patterns'] = self.extract_patterns(main, page['code_samples'])
        
        # Extract paragraphs
        paragraphs = []
        for p in main.find_all('p'):
            text = self.clean_text(p.get_text())
            if text and len(text) > 20:  # Skip very short paragraphs
                paragraphs.append(text)
        
        page['content'] = '\n\n'.join(paragraphs)

        # Extract links from entire page (not just main content)
        # This allows discovery of navigation links outside the main content area
        for link in soup.find_all('a', href=True):
            href = urljoin(url, link['href'])
            # Strip anchor fragments to avoid treating #anchors as separate pages
            href = href.split('#')[0]
            if self.is_valid_url(href) and href not in page['links']:
                page['links'].append(href)

        return page

    def _extract_language_from_classes(self, classes):
        """Extract language from class list

        Supports multiple patterns:
        - language-{lang} (e.g., "language-python")
        - lang-{lang} (e.g., "lang-javascript")
        - brush: {lang} (e.g., "brush: java")
        - bare language name (e.g., "python", "java")

        """
        # Define common programming languages
        known_languages = [
            "javascript", "java", "xml", "html", "python", "bash", "cpp", "typescript",
            "go", "rust", "php", "ruby", "swift", "kotlin", "csharp", "c", "sql",
            "yaml", "json", "markdown", "css", "scss", "sass", "jsx", "tsx", "vue",
            "shell", "powershell", "r", "scala", "dart", "perl", "lua", "elixir"
        ]

        for cls in classes:
            # Clean special characters (except word chars and hyphens)
            cls = re.sub(r'[^\w-]', '', cls)

            if 'language-' in cls:
                return cls.replace('language-', '')

            if 'lang-' in cls:
                return cls.replace('lang-', '')

            # Check for brush: pattern (e.g., "brush: java")
            if 'brush' in cls.lower():
                lang = cls.lower().replace('brush', '').strip()
                if lang in known_languages:
                    return lang

            # Check for bare language name
            if cls in known_languages:
                return cls

        return None

    def detect_language(self, elem, code):
        """Detect programming language from code block"""

        # Check element classes
        lang = self._extract_language_from_classes(elem.get('class', []))
        if lang:
            return lang

        # Check parent pre element
        parent = elem.parent
        if parent and parent.name == 'pre':
            lang = self._extract_language_from_classes(parent.get('class', []))
            if lang:
                return lang

        # Heuristic detection
        if 'import ' in code and 'from ' in code:
            return 'python'
        if 'const ' in code or 'let ' in code or '=>' in code:
            return 'javascript'
        if 'func ' in code and 'var ' in code:
            return 'gdscript'
        if 'def ' in code and ':' in code:
            return 'python'
        if '#include' in code or 'int main' in code:
            return 'cpp'
        # C# detection
        if 'using System' in code or 'namespace ' in code:
            return 'csharp'
        if '{ get; set; }' in code:
            return 'csharp'
        if any(keyword in code for keyword in ['public class ', 'private class ', 'internal class ', 'public static void ']):
            return 'csharp'

        return 'unknown'
    
    def extract_patterns(self, main: Any, code_samples: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Extract common coding patterns (NEW FEATURE)"""
        patterns = []
        
        # Look for "Example:" or "Pattern:" sections
        for elem in main.find_all(['p', 'div']):
            text = elem.get_text().lower()
            if any(word in text for word in ['example:', 'pattern:', 'usage:', 'typical use']):
                # Get the code that follows
                next_code = elem.find_next(['pre', 'code'])
                if next_code:
                    patterns.append({
                        'description': self.clean_text(elem.get_text()),
                        'code': next_code.get_text().strip()
                    })
        
        return patterns[:5]  # Limit to 5 most relevant patterns
    
    def clean_text(self, text: str) -> str:
        """Clean text content"""
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def save_page(self, page: Dict[str, Any]) -> None:
        """Save page data"""
        url_hash = hashlib.md5(page['url'].encode()).hexdigest()[:10]
        safe_title = re.sub(r'[^\w\s-]', '', page['title'])[:50]
        safe_title = re.sub(r'[-\s]+', '_', safe_title)
        
        filename = f"{safe_title}_{url_hash}.json"
        filepath = os.path.join(self.data_dir, "pages", filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(page, f, indent=2, ensure_ascii=False)
    
    def scrape_page(self, url: str) -> None:
        """Scrape a single page with thread-safe operations.

        Args:
            url (str): URL to scrape

        Returns:
            dict or None: Page data dict on success, None on failure

        Note:
            Uses threading locks when workers > 1 for thread safety
        """
        try:
            # Scraping part (no lock needed - independent)
            headers = {'User-Agent': 'Mozilla/5.0 (Documentation Scraper)'}
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            page = self.extract_content(soup, url)

            # Thread-safe operations (lock required)
            if self.workers > 1:
                with self.lock:
                    logger.info("  %s", url)
                    self.save_page(page)
                    self.pages.append(page)

                    # Add new URLs
                    for link in page['links']:
                        if link not in self.visited_urls and link not in self.pending_urls:
                            self.pending_urls.append(link)
            else:
                # Single-threaded mode (no lock needed)
                logger.info("  %s", url)
                self.save_page(page)
                self.pages.append(page)

                # Add new URLs
                for link in page['links']:
                    if link not in self.visited_urls and link not in self.pending_urls:
                        self.pending_urls.append(link)

            # Rate limiting
            rate_limit = self.config.get('rate_limit', DEFAULT_RATE_LIMIT)
            if rate_limit > 0:
                time.sleep(rate_limit)

        except Exception as e:
            if self.workers > 1:
                with self.lock:
                    logger.error("  ✗ Error scraping %s: %s: %s", url, type(e).__name__, e)
            else:
                logger.error("  ✗ Error scraping page: %s: %s", type(e).__name__, e)
                logger.error("     URL: %s", url)

    async def scrape_page_async(self, url: str, semaphore: asyncio.Semaphore, client: httpx.AsyncClient) -> None:
        """Scrape a single page asynchronously.

        Args:
            url: URL to scrape
            semaphore: Asyncio semaphore for concurrency control
            client: Shared httpx AsyncClient for connection pooling

        Note:
            Uses asyncio.Lock for async-safe operations instead of threading.Lock
        """
        async with semaphore:  # Limit concurrent requests
            try:
                # Async HTTP request
                headers = {'User-Agent': 'Mozilla/5.0 (Documentation Scraper)'}
                response = await client.get(url, headers=headers, timeout=30.0)
                response.raise_for_status()

                # BeautifulSoup parsing (still synchronous, but fast)
                soup = BeautifulSoup(response.content, 'html.parser')
                page = self.extract_content(soup, url)

                # Async-safe operations (no lock needed - single event loop)
                logger.info("  %s", url)
                self.save_page(page)
                self.pages.append(page)

                # Add new URLs
                for link in page['links']:
                    if link not in self.visited_urls and link not in self.pending_urls:
                        self.pending_urls.append(link)

                # Rate limiting
                rate_limit = self.config.get('rate_limit', DEFAULT_RATE_LIMIT)
                if rate_limit > 0:
                    await asyncio.sleep(rate_limit)

            except Exception as e:
                logger.error("  ✗ Error scraping %s: %s: %s", url, type(e).__name__, e)

    def _try_llms_txt(self) -> bool:
        """
        Try to use llms.txt instead of HTML scraping.
        Downloads ALL available variants and stores with .md extension.

        Returns:
            True if llms.txt was found and processed successfully
        """
        logger.info("\n🔍 Checking for llms.txt at %s...", self.base_url)

        # Check for explicit config URL first
        explicit_url = self.config.get('llms_txt_url')
        if explicit_url:
            logger.info("\n📌 Using explicit llms_txt_url from config: %s", explicit_url)

            # Download explicit file first
            downloader = LlmsTxtDownloader(explicit_url)
            content = downloader.download()

            if content:
                # Save explicit file with proper .md extension
                filename = downloader.get_proper_filename()
                filepath = os.path.join(self.skill_dir, "references", filename)
                os.makedirs(os.path.dirname(filepath), exist_ok=True)

                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                logger.info("  💾 Saved %s (%d chars)", filename, len(content))

                # Also try to detect and download ALL other variants
                detector = LlmsTxtDetector(self.base_url)
                variants = detector.detect_all()

                if variants:
                    logger.info("\n🔍 Found %d total variant(s), downloading remaining...", len(variants))
                    for variant_info in variants:
                        url = variant_info['url']
                        variant = variant_info['variant']

                        # Skip the explicit one we already downloaded
                        if url == explicit_url:
                            continue

                        logger.info("  📥 Downloading %s...", variant)
                        extra_downloader = LlmsTxtDownloader(url)
                        extra_content = extra_downloader.download()

                        if extra_content:
                            extra_filename = extra_downloader.get_proper_filename()
                            extra_filepath = os.path.join(self.skill_dir, "references", extra_filename)
                            with open(extra_filepath, 'w', encoding='utf-8') as f:
                                f.write(extra_content)
                            logger.info("     ✓ %s (%d chars)", extra_filename, len(extra_content))

                # Parse explicit file for skill building
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
            logger.info("ℹ️  No llms.txt found, using HTML scraping")
            return False

        logger.info("✅ Found %d llms.txt variant(s)", len(variants))

        # Download ALL variants
        downloaded = {}
        for variant_info in variants:
            url = variant_info['url']
            variant = variant_info['variant']

            logger.info("  📥 Downloading %s...", variant)
            downloader = LlmsTxtDownloader(url)
            content = downloader.download()

            if content:
                filename = downloader.get_proper_filename()
                downloaded[variant] = {
                    'content': content,
                    'filename': filename,
                    'size': len(content)
                }
                logger.info("     ✓ %s (%d chars)", filename, len(content))

        if not downloaded:
            logger.warning("⚠️  Failed to download any variants, falling back to HTML scraping")
            return False

        # Save ALL variants to references/
        os.makedirs(os.path.join(self.skill_dir, "references"), exist_ok=True)

        for variant, data in downloaded.items():
            filepath = os.path.join(self.skill_dir, "references", data['filename'])
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(data['content'])
            logger.info("  💾 Saved %s", data['filename'])

        # Parse LARGEST variant for skill building
        largest = max(downloaded.items(), key=lambda x: x[1]['size'])
        logger.info("\n📄 Parsing %s for skill building...", largest[1]['filename'])

        parser = LlmsTxtParser(largest[1]['content'])
        pages = parser.parse()

        if not pages:
            logger.warning("⚠️  Failed to parse llms.txt, falling back to HTML scraping")
            return False

        logger.info("  ✓ Parsed %d sections", len(pages))

        # Save pages for skill building
        for page in pages:
            self.save_page(page)
            self.pages.append(page)

        self.llms_txt_detected = True
        self.llms_txt_variants = list(downloaded.keys())

        return True

    def scrape_all(self) -> None:
        """Scrape all pages (supports llms.txt and HTML scraping)

        Routes to async version if async_mode is enabled in config.
        """
        # Route to async version if enabled
        if self.async_mode:
            asyncio.run(self.scrape_all_async())
            return

        # Try llms.txt first (unless dry-run or explicitly disabled)
        if not self.dry_run and not self.skip_llms_txt:
            llms_result = self._try_llms_txt()
            if llms_result:
                logger.info("\n✅ Used llms.txt (%s) - skipping HTML scraping", self.llms_txt_variant)
                self.save_summary()
                return

        # HTML scraping (sync/thread-based logic)
        logger.info("\n" + "=" * 60)
        if self.dry_run:
            logger.info("DRY RUN: %s", self.name)
        else:
            logger.info("SCRAPING: %s", self.name)
        logger.info("=" * 60)
        logger.info("Base URL: %s", self.base_url)

        if self.dry_run:
            logger.info("Mode: Preview only (no actual scraping)\n")
        else:
            logger.info("Output: %s", self.data_dir)
            if self.workers > 1:
                logger.info("Workers: %d parallel threads", self.workers)
            logger.info("")

        max_pages = self.config.get('max_pages', DEFAULT_MAX_PAGES)

        # Handle unlimited mode
        if max_pages is None or max_pages == -1:
            logger.warning("⚠️  UNLIMITED MODE: No page limit (will scrape all pages)\n")
            unlimited = True
        else:
            unlimited = False

        # Dry run: preview first 20 URLs
        preview_limit = 20 if self.dry_run else max_pages

        # Single-threaded mode (original sequential logic)
        if self.workers <= 1:
            while self.pending_urls and (unlimited or len(self.visited_urls) < preview_limit):
                url = self.pending_urls.popleft()

                if url in self.visited_urls:
                    continue

                self.visited_urls.add(url)

                if self.dry_run:
                    # Just show what would be scraped
                    logger.info("  [Preview] %s", url)
                    try:
                        headers = {'User-Agent': 'Mozilla/5.0 (Documentation Scraper - Dry Run)'}
                        response = requests.get(url, headers=headers, timeout=10)
                        soup = BeautifulSoup(response.content, 'html.parser')

                        main_selector = self.config.get('selectors', {}).get('main_content', 'div[role="main"]')
                        main = soup.select_one(main_selector)

                        if main:
                            for link in main.find_all('a', href=True):
                                href = urljoin(url, link['href'])
                                if self.is_valid_url(href) and href not in self.visited_urls:
                                    self.pending_urls.append(href)
                    except Exception as e:
                        # Failed to extract links in fast mode, continue anyway
                        logger.warning("⚠️  Warning: Could not extract links from %s: %s", url, e)
                else:
                    self.scrape_page(url)
                    self.pages_scraped += 1

                    if self.checkpoint_enabled and self.pages_scraped % self.checkpoint_interval == 0:
                        self.save_checkpoint()

                if len(self.visited_urls) % 10 == 0:
                    logger.info("  [%d pages]", len(self.visited_urls))

        # Multi-threaded mode (parallel scraping)
        else:
            from concurrent.futures import ThreadPoolExecutor, as_completed

            logger.info("🚀 Starting parallel scraping with %d workers\n", self.workers)

            with ThreadPoolExecutor(max_workers=self.workers) as executor:
                futures = []

                while self.pending_urls and (unlimited or len(self.visited_urls) < preview_limit):
                    # Get next batch of URLs (thread-safe)
                    batch = []
                    batch_size = min(self.workers * 2, len(self.pending_urls))

                    with self.lock:
                        for _ in range(batch_size):
                            if not self.pending_urls:
                                break
                            url = self.pending_urls.popleft()

                            if url not in self.visited_urls:
                                self.visited_urls.add(url)
                                batch.append(url)

                    # Submit batch to executor
                    for url in batch:
                        if unlimited or len(self.visited_urls) <= preview_limit:
                            future = executor.submit(self.scrape_page, url)
                            futures.append(future)

                    # Wait for some to complete before submitting more
                    completed = 0
                    for future in as_completed(futures[:batch_size]):
                        # Check for exceptions
                        try:
                            future.result()  # Raises exception if scrape_page failed
                        except Exception as e:
                            with self.lock:
                                logger.warning("  ⚠️  Worker exception: %s", e)

                        completed += 1

                        with self.lock:
                            self.pages_scraped += 1

                            if self.checkpoint_enabled and self.pages_scraped % self.checkpoint_interval == 0:
                                self.save_checkpoint()

                            if self.pages_scraped % 10 == 0:
                                logger.info("  [%d pages scraped]", self.pages_scraped)

                    # Remove completed futures
                    futures = [f for f in futures if not f.done()]

                # Wait for remaining futures
                for future in as_completed(futures):
                    # Check for exceptions
                    try:
                        future.result()
                    except Exception as e:
                        with self.lock:
                            logger.warning("  ⚠️  Worker exception: %s", e)

                    with self.lock:
                        self.pages_scraped += 1

        if self.dry_run:
            logger.info("\n✅ Dry run complete: would scrape ~%d pages", len(self.visited_urls))
            if len(self.visited_urls) >= preview_limit:
                logger.info("   (showing first %d, actual scraping may find more)", preview_limit)
            logger.info("\n💡 To actually scrape, run without --dry-run")
        else:
            logger.info("\n✅ Scraped %d pages", len(self.visited_urls))
            self.save_summary()

    async def scrape_all_async(self) -> None:
        """Scrape all pages asynchronously (async/await version).

        This method provides significantly better performance for parallel scraping
        compared to thread-based scraping, with lower memory overhead and better
        CPU utilization.

        Performance: ~2-3x faster than sync mode with same worker count.
        """
        # Try llms.txt first (unless dry-run or explicitly disabled)
        if not self.dry_run and not self.skip_llms_txt:
            llms_result = self._try_llms_txt()
            if llms_result:
                logger.info("\n✅ Used llms.txt (%s) - skipping HTML scraping", self.llms_txt_variant)
                self.save_summary()
                return

        # HTML scraping (async version)
        logger.info("\n" + "=" * 60)
        if self.dry_run:
            logger.info("DRY RUN (ASYNC): %s", self.name)
        else:
            logger.info("SCRAPING (ASYNC): %s", self.name)
        logger.info("=" * 60)
        logger.info("Base URL: %s", self.base_url)

        if self.dry_run:
            logger.info("Mode: Preview only (no actual scraping)\n")
        else:
            logger.info("Output: %s", self.data_dir)
            logger.info("Workers: %d concurrent tasks (async)", self.workers)
            logger.info("")

        max_pages = self.config.get('max_pages', DEFAULT_MAX_PAGES)

        # Handle unlimited mode
        if max_pages is None or max_pages == -1:
            logger.warning("⚠️  UNLIMITED MODE: No page limit (will scrape all pages)\n")
            unlimited = True
            preview_limit = float('inf')
        else:
            unlimited = False
            preview_limit = 20 if self.dry_run else max_pages

        # Create semaphore for concurrency control
        semaphore = asyncio.Semaphore(self.workers)

        # Create shared HTTP client with connection pooling
        async with httpx.AsyncClient(
            timeout=30.0,
            limits=httpx.Limits(max_connections=self.workers * 2)
        ) as client:
            tasks = []

            while self.pending_urls and (unlimited or len(self.visited_urls) < preview_limit):
                # Get next batch of URLs
                batch = []
                batch_size = min(self.workers * 2, len(self.pending_urls))

                for _ in range(batch_size):
                    if not self.pending_urls:
                        break
                    url = self.pending_urls.popleft()

                    if url not in self.visited_urls:
                        self.visited_urls.add(url)
                        batch.append(url)

                # Create async tasks for batch
                for url in batch:
                    if unlimited or len(self.visited_urls) <= preview_limit:
                        if self.dry_run:
                            logger.info("  [Preview] %s", url)
                        else:
                            task = asyncio.create_task(
                                self.scrape_page_async(url, semaphore, client)
                            )
                            tasks.append(task)

                # Wait for batch to complete before continuing
                if tasks:
                    await asyncio.gather(*tasks, return_exceptions=True)
                    tasks = []
                    self.pages_scraped = len(self.visited_urls)

                    # Progress indicator
                    if self.pages_scraped % 10 == 0 and not self.dry_run:
                        logger.info("  [%d pages scraped]", self.pages_scraped)

                    # Checkpoint saving
                    if not self.dry_run and self.checkpoint_enabled:
                        if self.pages_scraped % self.checkpoint_interval == 0:
                            self.save_checkpoint()

            # Wait for any remaining tasks
            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)

        if self.dry_run:
            logger.info("\n✅ Dry run complete: would scrape ~%d pages", len(self.visited_urls))
            if len(self.visited_urls) >= preview_limit:
                logger.info("   (showing first %d, actual scraping may find more)", int(preview_limit))
            logger.info("\n💡 To actually scrape, run without --dry-run")
        else:
            logger.info("\n✅ Scraped %d pages (async mode)", len(self.visited_urls))
            self.save_summary()

    def save_summary(self) -> None:
        """Save scraping summary"""
        summary = {
            'name': self.name,
            'total_pages': len(self.pages),
            'base_url': self.base_url,
            'llms_txt_detected': self.llms_txt_detected,
            'llms_txt_variant': self.llms_txt_variant,
            'pages': [{'title': p['title'], 'url': p['url']} for p in self.pages]
        }

        with open(f"{self.data_dir}/summary.json", 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
    
    def load_scraped_data(self) -> List[Dict[str, Any]]:
        """Load previously scraped data"""
        pages = []
        pages_dir = Path(self.data_dir) / "pages"
        
        if not pages_dir.exists():
            return []
        
        for json_file in pages_dir.glob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    pages.append(json.load(f))
            except Exception as e:
                logger.error("⚠️  Error loading scraped data file %s: %s: %s", json_file, type(e).__name__, e)
                logger.error("   Suggestion: File may be corrupted, consider re-scraping with --fresh")
        
        return pages
    
    def smart_categorize(self, pages: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Improved categorization with better pattern matching"""
        category_defs = self.config.get('categories', {})
        
        # Default smart categories if none provided
        if not category_defs:
            category_defs = self.infer_categories(pages)

        categories: Dict[str, List[Dict[str, Any]]] = {cat: [] for cat in category_defs.keys()}
        categories['other'] = []
        
        for page in pages:
            url = page['url'].lower()
            title = page['title'].lower()
            content = page.get('content', '').lower()[:CONTENT_PREVIEW_LENGTH]  # Check first N chars for categorization
            
            categorized = False
            
            # Match against keywords
            for cat, keywords in category_defs.items():
                score = 0
                for keyword in keywords:
                    keyword = keyword.lower()
                    if keyword in url:
                        score += 3
                    if keyword in title:
                        score += 2
                    if keyword in content:
                        score += 1
                
                if score >= MIN_CATEGORIZATION_SCORE:  # Threshold for categorization
                    categories[cat].append(page)
                    categorized = True
                    break
            
            if not categorized:
                categories['other'].append(page)
        
        # Remove empty categories
        categories = {k: v for k, v in categories.items() if v}
        
        return categories
    
    def infer_categories(self, pages: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """Infer categories from URL patterns (IMPROVED)"""
        url_segments: defaultdict[str, int] = defaultdict(int)
        
        for page in pages:
            path = urlparse(page['url']).path
            segments = [s for s in path.split('/') if s and s not in ['en', 'stable', 'latest', 'docs']]
            
            for seg in segments:
                url_segments[seg] += 1
        
        # Top segments become categories
        top_segments = sorted(url_segments.items(), key=lambda x: x[1], reverse=True)[:8]
        
        categories = {}
        for seg, count in top_segments:
            if count >= 3:  # At least 3 pages
                categories[seg] = [seg]
        
        # Add common defaults
        if 'tutorial' not in categories and any('tutorial' in url for url in [p['url'] for p in pages]):
            categories['tutorials'] = ['tutorial', 'guide', 'getting-started']
        
        if 'api' not in categories and any('api' in url or 'reference' in url for url in [p['url'] for p in pages]):
            categories['api'] = ['api', 'reference', 'class']
        
        return categories
    
    def generate_quick_reference(self, pages: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Generate quick reference from common patterns (NEW FEATURE)"""
        quick_ref = []
        
        # Collect all patterns
        all_patterns = []
        for page in pages:
            all_patterns.extend(page.get('patterns', []))
        
        # Get most common code patterns
        seen_codes = set()
        for pattern in all_patterns:
            code = pattern['code']
            if code not in seen_codes and len(code) < 300:
                quick_ref.append(pattern)
                seen_codes.add(code)
                if len(quick_ref) >= 15:
                    break
        
        return quick_ref
    
    def create_reference_file(self, category: str, pages: List[Dict[str, Any]]) -> None:
        """Create enhanced reference file"""
        if not pages:
            return
        
        lines = []
        lines.append(f"# {self.name.title()} - {category.replace('_', ' ').title()}\n")
        lines.append(f"**Pages:** {len(pages)}\n")
        lines.append("---\n")
        
        for page in pages:
            lines.append(f"## {page['title']}\n")
            lines.append(f"**URL:** {page['url']}\n")
            
            # Table of contents from headings
            if page.get('headings'):
                lines.append("**Contents:**")
                for h in page['headings'][:10]:
                    level = int(h['level'][1]) if len(h['level']) > 1 else 1
                    indent = "  " * max(0, level - 2)
                    lines.append(f"{indent}- {h['text']}")
                lines.append("")
            
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
            
            lines.append("---\n")
        
        filepath = os.path.join(self.skill_dir, "references", f"{category}.md")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

        logger.info("  ✓ %s.md (%d pages)", category, len(pages))
    
    def create_enhanced_skill_md(self, categories: Dict[str, List[Dict[str, Any]]], quick_ref: List[Dict[str, str]]) -> None:
        """Create SKILL.md with actual examples (IMPROVED)"""
        description = self.config.get('description', f'Comprehensive assistance with {self.name}')
        
        # Extract actual code examples from docs
        example_codes = []
        for pages in categories.values():
            for page in pages[:3]:  # First 3 pages per category
                for sample in page.get('code_samples', [])[:2]:  # First 2 samples per page
                    code = sample.get('code', sample if isinstance(sample, str) else '')
                    lang = sample.get('language', 'unknown')
                    if len(code) < 200 and lang != 'unknown':
                        example_codes.append((lang, code))
                    if len(example_codes) >= 10:
                        break
                if len(example_codes) >= 10:
                    break
            if len(example_codes) >= 10:
                break
        
        content = f"""---
name: {self.name}
description: {description}
---

# {self.name.title()} Skill

Comprehensive assistance with {self.name} development, generated from official documentation.

## When to Use This Skill

This skill should be triggered when:
- Working with {self.name}
- Asking about {self.name} features or APIs
- Implementing {self.name} solutions
- Debugging {self.name} code
- Learning {self.name} best practices

## Quick Reference

### Common Patterns

"""
        
        # Add actual quick reference patterns
        if quick_ref:
            for i, pattern in enumerate(quick_ref[:8], 1):
                content += f"**Pattern {i}:** {pattern.get('description', 'Example pattern')}\n\n"
                content += "```\n"
                content += pattern.get('code', '')[:300]
                content += "\n```\n\n"
        else:
            content += "*Quick reference patterns will be added as you use the skill.*\n\n"
        
        # Add example codes from docs
        if example_codes:
            content += "### Example Code Patterns\n\n"
            for i, (lang, code) in enumerate(example_codes[:5], 1):
                content += f"**Example {i}** ({lang}):\n```{lang}\n{code}\n```\n\n"
        
        content += f"""## Reference Files

This skill includes comprehensive documentation in `references/`:

"""
        
        for cat in sorted(categories.keys()):
            content += f"- **{cat}.md** - {cat.replace('_', ' ').title()} documentation\n"
        
        content += """
Use `view` to read specific reference files when detailed information is needed.

## Working with This Skill

### For Beginners
Start with the getting_started or tutorials reference files for foundational concepts.

### For Specific Features
Use the appropriate category reference file (api, guides, etc.) for detailed information.

### For Code Examples
The quick reference section above contains common patterns extracted from the official docs.

## Resources

### references/
Organized documentation extracted from official sources. These files contain:
- Detailed explanations
- Code examples with language annotations
- Links to original documentation
- Table of contents for quick navigation

### scripts/
Add helper scripts here for common automation tasks.

### assets/
Add templates, boilerplate, or example projects here.

## Notes

- This skill was automatically generated from official documentation
- Reference files preserve the structure and examples from source docs
- Code examples include language detection for better syntax highlighting
- Quick reference patterns are extracted from common usage examples in the docs

## Updating

To refresh this skill with updated documentation:
1. Re-run the scraper with the same configuration
2. The skill will be rebuilt with the latest information
"""
        
        filepath = os.path.join(self.skill_dir, "SKILL.md")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        logger.info("  ✓ SKILL.md (enhanced with %d examples)", len(example_codes))
    
    def create_index(self, categories: Dict[str, List[Dict[str, Any]]]) -> None:
        """Create navigation index"""
        lines = []
        lines.append(f"# {self.name.title()} Documentation Index\n")
        lines.append("## Categories\n")
        
        for cat, pages in sorted(categories.items()):
            lines.append(f"### {cat.replace('_', ' ').title()}")
            lines.append(f"**File:** `{cat}.md`")
            lines.append(f"**Pages:** {len(pages)}\n")
        
        filepath = os.path.join(self.skill_dir, "references", "index.md")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

        logger.info("  ✓ index.md")
    
    def build_skill(self) -> bool:
        """Build the skill from scraped data.

        Loads scraped JSON files, categorizes pages, extracts patterns,
        and generates SKILL.md and reference files.

        Returns:
            bool: True if build succeeded, False otherwise
        """
        logger.info("\n" + "=" * 60)
        logger.info("BUILDING SKILL: %s", self.name)
        logger.info("=" * 60 + "\n")

        # Load data
        logger.info("Loading scraped data...")
        pages = self.load_scraped_data()

        if not pages:
            logger.error("✗ No scraped data found!")
            return False

        logger.info("  ✓ Loaded %d pages\n", len(pages))

        # Categorize
        logger.info("Categorizing pages...")
        categories = self.smart_categorize(pages)
        logger.info("  ✓ Created %d categories\n", len(categories))

        # Generate quick reference
        logger.info("Generating quick reference...")
        quick_ref = self.generate_quick_reference(pages)
        logger.info("  ✓ Extracted %d patterns\n", len(quick_ref))

        # Create reference files
        logger.info("Creating reference files...")
        for cat, cat_pages in categories.items():
            self.create_reference_file(cat, cat_pages)

        # Create index
        self.create_index(categories)
        logger.info("")

        # Create enhanced SKILL.md
        logger.info("Creating SKILL.md...")
        self.create_enhanced_skill_md(categories, quick_ref)

        logger.info("\n✅ Skill built: %s/", self.skill_dir)
        return True


def validate_config(config: Dict[str, Any]) -> Tuple[List[str], List[str]]:
    """Validate configuration structure and values.

    Args:
        config (dict): Configuration dictionary to validate

    Returns:
        tuple: (errors, warnings) where each is a list of strings

    Example:
        >>> errors, warnings = validate_config({'name': 'test', 'base_url': 'https://example.com'})
        >>> if errors:
        ...     print("Invalid config:", errors)
    """
    errors = []
    warnings = []

    # Required fields
    required_fields = ['name', 'base_url']
    for field in required_fields:
        if field not in config:
            errors.append(f"Missing required field: '{field}'")

    # Validate name (alphanumeric, hyphens, underscores only)
    if 'name' in config:
        if not re.match(r'^[a-zA-Z0-9_-]+$', config['name']):
            errors.append(f"Invalid name: '{config['name']}' (use only letters, numbers, hyphens, underscores)")

    # Validate base_url
    if 'base_url' in config:
        if not config['base_url'].startswith(('http://', 'https://')):
            errors.append(f"Invalid base_url: '{config['base_url']}' (must start with http:// or https://)")

    # Validate selectors structure
    if 'selectors' in config:
        if not isinstance(config['selectors'], dict):
            errors.append("'selectors' must be a dictionary")
        else:
            recommended_selectors = ['main_content', 'title', 'code_blocks']
            for selector in recommended_selectors:
                if selector not in config['selectors']:
                    warnings.append(f"Missing recommended selector: '{selector}'")
    else:
        warnings.append("Missing 'selectors' section (recommended)")

    # Validate url_patterns
    if 'url_patterns' in config:
        if not isinstance(config['url_patterns'], dict):
            errors.append("'url_patterns' must be a dictionary")
        else:
            for key in ['include', 'exclude']:
                if key in config['url_patterns']:
                    if not isinstance(config['url_patterns'][key], list):
                        errors.append(f"'url_patterns.{key}' must be a list")

    # Validate categories
    if 'categories' in config:
        if not isinstance(config['categories'], dict):
            errors.append("'categories' must be a dictionary")
        else:
            for cat_name, keywords in config['categories'].items():
                if not isinstance(keywords, list):
                    errors.append(f"'categories.{cat_name}' must be a list of keywords")

    # Validate rate_limit
    if 'rate_limit' in config:
        try:
            rate = float(config['rate_limit'])
            if rate < 0:
                errors.append(f"'rate_limit' must be non-negative (got {rate})")
            elif rate > 10:
                warnings.append(f"'rate_limit' is very high ({rate}s) - this may slow down scraping significantly")
        except (ValueError, TypeError):
            errors.append(f"'rate_limit' must be a number (got {config['rate_limit']})")

    # Validate max_pages
    if 'max_pages' in config:
        max_p_value = config['max_pages']

        # Allow None for unlimited
        if max_p_value is None:
            warnings.append("'max_pages' is None (unlimited) - this will scrape ALL pages. Use with caution!")
        else:
            try:
                max_p = int(max_p_value)
                # Allow -1 for unlimited
                if max_p == -1:
                    warnings.append("'max_pages' is -1 (unlimited) - this will scrape ALL pages. Use with caution!")
                elif max_p < 1:
                    errors.append(f"'max_pages' must be at least 1 or -1 for unlimited (got {max_p})")
                elif max_p > MAX_PAGES_WARNING_THRESHOLD:
                    warnings.append(f"'max_pages' is very high ({max_p}) - scraping may take a very long time")
            except (ValueError, TypeError):
                errors.append(f"'max_pages' must be an integer, -1, or null (got {config['max_pages']})")

    # Validate start_urls if present
    if 'start_urls' in config:
        if not isinstance(config['start_urls'], list):
            errors.append("'start_urls' must be a list")
        else:
            for url in config['start_urls']:
                if not url.startswith(('http://', 'https://')):
                    errors.append(f"Invalid start_url: '{url}' (must start with http:// or https://)")

    return errors, warnings


def load_config(config_path: str) -> Dict[str, Any]:
    """Load and validate configuration from JSON file.

    Args:
        config_path (str): Path to JSON configuration file

    Returns:
        dict: Validated configuration dictionary

    Raises:
        SystemExit: If config is invalid or file not found

    Example:
        >>> config = load_config('configs/react.json')
        >>> print(config['name'])
        'react'
    """
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        logger.error("❌ Error: Invalid JSON in config file: %s", config_path)
        logger.error("   Details: %s", e)
        logger.error("   Suggestion: Check syntax at line %d, column %d", e.lineno, e.colno)
        sys.exit(1)
    except FileNotFoundError:
        logger.error("❌ Error: Config file not found: %s", config_path)
        logger.error("   Suggestion: Create a config file or use an existing one from configs/")
        logger.error("   Available configs: react.json, vue.json, django.json, godot.json")
        sys.exit(1)

    # Validate config
    errors, warnings = validate_config(config)

    # Show warnings (non-blocking)
    if warnings:
        logger.warning("⚠️  Configuration warnings in %s:", config_path)
        for warning in warnings:
            logger.warning("   - %s", warning)
        logger.info("")

    # Show errors (blocking)
    if errors:
        logger.error("❌ Configuration validation errors in %s:", config_path)
        for error in errors:
            logger.error("   - %s", error)
        logger.error("\n   Suggestion: Fix the above errors or check configs/ for working examples")
        sys.exit(1)

    return config


def interactive_config() -> Dict[str, Any]:
    """Interactive configuration wizard for creating new configs.

    Prompts user for all required configuration fields step-by-step
    and returns a complete configuration dictionary.

    Returns:
        dict: Complete configuration dictionary with user-provided values

    Example:
        >>> config = interactive_config()
        # User enters: name=react, url=https://react.dev, etc.
        >>> config['name']
        'react'
    """
    logger.info("\n" + "="*60)
    logger.info("Documentation to Skill Converter")
    logger.info("="*60 + "\n")

    config: Dict[str, Any] = {}
    
    # Basic info
    config['name'] = input("Skill name (e.g., 'react', 'godot'): ").strip()
    config['description'] = input("Skill description: ").strip()
    config['base_url'] = input("Base URL (e.g., https://docs.example.com/): ").strip()
    
    if not config['base_url'].endswith('/'):
        config['base_url'] += '/'
    
    # Selectors
    logger.info("\nCSS Selectors (press Enter for defaults):")
    selectors = {}
    selectors['main_content'] = input("  Main content [div[role='main']]: ").strip() or "div[role='main']"
    selectors['title'] = input("  Title [title]: ").strip() or "title"
    selectors['code_blocks'] = input("  Code blocks [pre code]: ").strip() or "pre code"
    config['selectors'] = selectors
    
    # URL patterns
    logger.info("\nURL Patterns (comma-separated, optional):")
    include = input("  Include: ").strip()
    exclude = input("  Exclude: ").strip()
    config['url_patterns'] = {
        'include': [p.strip() for p in include.split(',') if p.strip()],
        'exclude': [p.strip() for p in exclude.split(',') if p.strip()]
    }
    
    # Settings
    rate = input(f"\nRate limit (seconds) [{DEFAULT_RATE_LIMIT}]: ").strip()
    config['rate_limit'] = float(rate) if rate else DEFAULT_RATE_LIMIT

    max_p = input(f"Max pages [{DEFAULT_MAX_PAGES}]: ").strip()
    config['max_pages'] = int(max_p) if max_p else DEFAULT_MAX_PAGES
    
    return config


def check_existing_data(name: str) -> Tuple[bool, int]:
    """Check if scraped data already exists for a skill.

    Args:
        name (str): Skill name to check

    Returns:
        tuple: (exists, page_count) where exists is bool and page_count is int

    Example:
        >>> exists, count = check_existing_data('react')
        >>> if exists:
        ...     print(f"Found {count} existing pages")
    """
    data_dir = f"output/{name}_data"
    if os.path.exists(data_dir) and os.path.exists(f"{data_dir}/summary.json"):
        with open(f"{data_dir}/summary.json", 'r') as f:
            summary = json.load(f)
        return True, summary.get('total_pages', 0)
    return False, 0


def setup_argument_parser() -> argparse.ArgumentParser:
    """Setup and configure command-line argument parser.

    Creates an ArgumentParser with all CLI options for the doc scraper tool,
    including configuration, scraping, enhancement, and performance options.

    Returns:
        argparse.ArgumentParser: Configured argument parser

    Example:
        >>> parser = setup_argument_parser()
        >>> args = parser.parse_args(['--config', 'configs/react.json'])
        >>> print(args.config)
        configs/react.json
    """
    parser = argparse.ArgumentParser(
        description='Convert documentation websites to Claude skills',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('--interactive', '-i', action='store_true',
                       help='Interactive configuration mode')
    parser.add_argument('--config', '-c', type=str,
                       help='Load configuration from file (e.g., configs/godot.json)')
    parser.add_argument('--name', type=str,
                       help='Skill name')
    parser.add_argument('--url', type=str,
                       help='Base documentation URL')
    parser.add_argument('--description', '-d', type=str,
                       help='Skill description')
    parser.add_argument('--skip-scrape', action='store_true',
                       help='Skip scraping, use existing data')
    parser.add_argument('--dry-run', action='store_true',
                       help='Preview what will be scraped without actually scraping')
    parser.add_argument('--enhance', action='store_true',
                       help='Enhance SKILL.md using Claude API after building (requires API key)')
    parser.add_argument('--enhance-local', action='store_true',
                       help='Enhance SKILL.md using Claude Code (no API key needed, runs in background)')
    parser.add_argument('--interactive-enhancement', action='store_true',
                       help='Open terminal window for enhancement (use with --enhance-local)')
    parser.add_argument('--api-key', type=str,
                       help='Anthropic API key for --enhance (or set ANTHROPIC_API_KEY)')
    parser.add_argument('--resume', action='store_true',
                       help='Resume from last checkpoint (for interrupted scrapes)')
    parser.add_argument('--fresh', action='store_true',
                       help='Clear checkpoint and start fresh')
    parser.add_argument('--rate-limit', '-r', type=float, metavar='SECONDS',
                       help=f'Override rate limit in seconds (default: from config or {DEFAULT_RATE_LIMIT}). Use 0 for no delay.')
    parser.add_argument('--workers', '-w', type=int, metavar='N',
                       help='Number of parallel workers for faster scraping (default: 1, max: 10)')
    parser.add_argument('--async', dest='async_mode', action='store_true',
                       help='Enable async mode for better parallel performance (2-3x faster than threads)')
    parser.add_argument('--no-rate-limit', action='store_true',
                       help='Disable rate limiting completely (same as --rate-limit 0)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose output (DEBUG level logging)')
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='Minimize output (WARNING level logging only)')

    return parser


def get_configuration(args: argparse.Namespace) -> Dict[str, Any]:
    """Load or create configuration from command-line arguments.

    Handles three configuration modes:
    1. Load from JSON file (--config)
    2. Interactive configuration wizard (--interactive or missing args)
    3. Quick mode from command-line arguments (--name, --url)

    Also applies CLI overrides for rate limiting and worker count.

    Args:
        args: Parsed command-line arguments from argparse

    Returns:
        dict: Configuration dictionary with all required fields

    Example:
        >>> args = parser.parse_args(['--name', 'react', '--url', 'https://react.dev'])
        >>> config = get_configuration(args)
        >>> print(config['name'])
        react
    """
    # Get base configuration
    if args.config:
        config = load_config(args.config)
    elif args.interactive or not (args.name and args.url):
        config = interactive_config()
    else:
        config = {
            'name': args.name,
            'description': args.description or f'Comprehensive assistance with {args.name}',
            'base_url': args.url,
            'selectors': {
                'main_content': "div[role='main']",
                'title': 'title',
                'code_blocks': 'pre code'
            },
            'url_patterns': {'include': [], 'exclude': []},
            'rate_limit': DEFAULT_RATE_LIMIT,
            'max_pages': DEFAULT_MAX_PAGES
        }

    # Apply CLI overrides for rate limiting
    if args.no_rate_limit:
        config['rate_limit'] = 0
        logger.info("⚡ Rate limiting disabled")
    elif args.rate_limit is not None:
        config['rate_limit'] = args.rate_limit
        if args.rate_limit == 0:
            logger.info("⚡ Rate limiting disabled")
        else:
            logger.info("⚡ Rate limit override: %ss per page", args.rate_limit)

    # Apply CLI overrides for worker count
    if args.workers:
        # Validate workers count
        if args.workers < 1:
            logger.error("❌ Error: --workers must be at least 1 (got %d)", args.workers)
            logger.error("   Suggestion: Use --workers 1 (default) or omit the flag")
            sys.exit(1)
        if args.workers > 10:
            logger.warning("⚠️  Warning: --workers capped at 10 (requested %d)", args.workers)
            args.workers = 10
        config['workers'] = args.workers
        if args.workers > 1:
            logger.info("🚀 Parallel scraping enabled: %d workers", args.workers)

    # Apply CLI override for async mode
    if args.async_mode:
        config['async_mode'] = True
        if config.get('workers', 1) > 1:
            logger.info("⚡ Async mode enabled (2-3x faster than threads)")
        else:
            logger.warning("⚠️  Async mode enabled but workers=1. Consider using --workers 4 for better performance")

    return config


def execute_scraping_and_building(config: Dict[str, Any], args: argparse.Namespace) -> Optional['DocToSkillConverter']:
    """Execute the scraping and skill building process.

    Handles dry run mode, existing data checks, scraping with checkpoints,
    keyboard interrupts, and skill building. This is the core workflow
    orchestration for the scraping phase.

    Args:
        config (dict): Configuration dictionary with scraping parameters
        args: Parsed command-line arguments

    Returns:
        DocToSkillConverter: The converter instance after scraping/building,
                            or None if process was aborted

    Example:
        >>> config = {'name': 'react', 'base_url': 'https://react.dev'}
        >>> converter = execute_scraping_and_building(config, args)
        >>> if converter:
        ...     print("Scraping complete!")
    """
    # Dry run mode - preview only
    if args.dry_run:
        logger.info("\n" + "=" * 60)
        logger.info("DRY RUN MODE")
        logger.info("=" * 60)
        logger.info("This will show what would be scraped without saving anything.\n")

        converter = DocToSkillConverter(config, dry_run=True)
        converter.scrape_all()

        logger.info("\n📋 Configuration Summary:")
        logger.info("   Name: %s", config['name'])
        logger.info("   Base URL: %s", config['base_url'])
        logger.info("   Max pages: %d", config.get('max_pages', DEFAULT_MAX_PAGES))
        logger.info("   Rate limit: %ss", config.get('rate_limit', DEFAULT_RATE_LIMIT))
        logger.info("   Categories: %d", len(config.get('categories', {})))
        return None

    # Check for existing data
    exists, page_count = check_existing_data(config['name'])

    if exists and not args.skip_scrape and not args.fresh:
        # Check force_rescrape flag from config
        if config.get('force_rescrape', False):
            # Auto-delete cached data and rescrape
            logger.info("\n✓ Found existing data: %d pages", page_count)
            logger.info("  force_rescrape enabled - deleting cached data and rescaping")
            import shutil
            data_dir = f"output/{config['name']}_data"
            if os.path.exists(data_dir):
                shutil.rmtree(data_dir)
                logger.info(f"  Deleted: {data_dir}")
        else:
            # Only prompt if force_rescrape is False
            logger.info("\n✓ Found existing data: %d pages", page_count)
            response = input("Use existing data? (y/n): ").strip().lower()
            if response == 'y':
                args.skip_scrape = True
    elif exists and args.fresh:
        logger.info("\n✓ Found existing data: %d pages", page_count)
        logger.info("  --fresh flag set, will re-scrape from scratch")

    # Create converter
    converter = DocToSkillConverter(config, resume=args.resume)

    # Handle fresh start (clear checkpoint)
    if args.fresh:
        converter.clear_checkpoint()

    # Scrape or skip
    if not args.skip_scrape:
        try:
            converter.scrape_all()
            # Save final checkpoint
            if converter.checkpoint_enabled:
                converter.save_checkpoint()
                logger.info("\n💾 Final checkpoint saved")
                # Clear checkpoint after successful completion
                converter.clear_checkpoint()
                logger.info("✅ Scraping complete - checkpoint cleared")
        except KeyboardInterrupt:
            logger.warning("\n\nScraping interrupted.")
            if converter.checkpoint_enabled:
                converter.save_checkpoint()
                logger.info("💾 Progress saved to checkpoint")
                logger.info("   Resume with: --config %s --resume", args.config if args.config else 'config.json')
            response = input("Continue with skill building? (y/n): ").strip().lower()
            if response != 'y':
                return None
    else:
        logger.info("\n⏭️  Skipping scrape, using existing data")

    # Build skill
    success = converter.build_skill()

    if not success:
        sys.exit(1)

    return converter


def execute_enhancement(config: Dict[str, Any], args: argparse.Namespace) -> None:
    """Execute optional SKILL.md enhancement with Claude.

    Supports two enhancement modes:
    1. API-based enhancement (requires ANTHROPIC_API_KEY)
    2. Local enhancement using Claude Code (no API key needed)

    Prints appropriate messages and suggestions based on whether
    enhancement was requested and whether it succeeded.

    Args:
        config (dict): Configuration dictionary with skill name
        args: Parsed command-line arguments with enhancement flags

    Example:
        >>> execute_enhancement(config, args)
        # Runs enhancement if --enhance or --enhance-local flag is set
    """
    import subprocess

    # Optional enhancement with Claude API
    if args.enhance:
        logger.info("\n" + "=" * 60)
        logger.info("ENHANCING SKILL.MD WITH CLAUDE API")
        logger.info("=" * 60 + "\n")

        try:
            enhance_cmd = ['python3', 'cli/enhance_skill.py', f'output/{config["name"]}/']
            if args.api_key:
                enhance_cmd.extend(['--api-key', args.api_key])

            result = subprocess.run(enhance_cmd, check=True)
            if result.returncode == 0:
                logger.info("\n✅ Enhancement complete!")
        except subprocess.CalledProcessError:
            logger.warning("\n⚠ Enhancement failed, but skill was still built")
        except FileNotFoundError:
            logger.warning("\n⚠ enhance_skill.py not found. Run manually:")
            logger.info("  skill-seekers-enhance output/%s/", config['name'])

    # Optional enhancement with Claude Code (local, no API key)
    if args.enhance_local:
        logger.info("\n" + "=" * 60)
        if args.interactive_enhancement:
            logger.info("ENHANCING SKILL.MD WITH CLAUDE CODE (INTERACTIVE)")
        else:
            logger.info("ENHANCING SKILL.MD WITH CLAUDE CODE (HEADLESS)")
        logger.info("=" * 60 + "\n")

        try:
            enhance_cmd = ['skill-seekers-enhance', f'output/{config["name"]}/']
            if args.interactive_enhancement:
                enhance_cmd.append('--interactive-enhancement')

            result = subprocess.run(enhance_cmd, check=True)

            if result.returncode == 0:
                logger.info("\n✅ Enhancement complete!")
        except subprocess.CalledProcessError:
            logger.warning("\n⚠ Enhancement failed, but skill was still built")
        except FileNotFoundError:
            logger.warning("\n⚠ skill-seekers-enhance command not found. Run manually:")
            logger.info("  skill-seekers-enhance output/%s/", config['name'])

    # Print packaging instructions
    logger.info("\n📦 Package your skill:")
    logger.info("  skill-seekers-package output/%s/", config['name'])

    # Suggest enhancement if not done
    if not args.enhance and not args.enhance_local:
        logger.info("\n💡 Optional: Enhance SKILL.md with Claude:")
        logger.info("  Local (recommended):  skill-seekers-enhance output/%s/", config['name'])
        logger.info("                        or re-run with: --enhance-local")
        logger.info("  API-based:            skill-seekers-enhance-api output/%s/", config['name'])
        logger.info("                        or re-run with: --enhance")
        logger.info("\n💡 Tip: Use --interactive-enhancement with --enhance-local to open terminal window")


def main() -> None:
    parser = setup_argument_parser()
    args = parser.parse_args()

    # Setup logging based on verbosity flags
    setup_logging(verbose=args.verbose, quiet=args.quiet)

    config = get_configuration(args)

    # Execute scraping and building
    converter = execute_scraping_and_building(config, args)

    # Exit if dry run or aborted
    if converter is None:
        return

    # Execute enhancement and print instructions
    execute_enhancement(config, args)


if __name__ == "__main__":
    main()
