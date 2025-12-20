# ABOUTME: Detects and validates llms.txt file availability at documentation URLs
# ABOUTME: Supports llms-full.txt, llms.txt, and llms-small.txt variants

import requests
from typing import Optional, Dict, List
from urllib.parse import urlparse

class LlmsTxtDetector:
    """Detect llms.txt files at documentation URLs"""

    VARIANTS = [
        ('llms-full.txt', 'full'),
        ('llms.txt', 'standard'),
        ('llms-small.txt', 'small')
    ]

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')

    def detect(self) -> Optional[Dict[str, str]]:
        """
        Detect available llms.txt variant.

        Returns:
            Dict with 'url' and 'variant' keys, or None if not found
        """
        parsed = urlparse(self.base_url)
        root_url = f"{parsed.scheme}://{parsed.netloc}"

        for filename, variant in self.VARIANTS:
            url = f"{root_url}/{filename}"

            if self._check_url_exists(url):
                return {'url': url, 'variant': variant}

        return None

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

    def _check_url_exists(self, url: str) -> bool:
        """Check if URL returns 200 status"""
        try:
            response = requests.head(url, timeout=5, allow_redirects=True)
            return response.status_code == 200
        except requests.RequestException:
            return False
