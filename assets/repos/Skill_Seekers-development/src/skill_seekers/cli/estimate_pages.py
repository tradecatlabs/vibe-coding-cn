#!/usr/bin/env python3
"""
Page Count Estimator for Skill Seeker
Quickly estimates how many pages a config will scrape without downloading content
"""

import sys
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import json

# Add parent directory to path for imports when run as script
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skill_seekers.cli.constants import (
    DEFAULT_RATE_LIMIT,
    DEFAULT_MAX_DISCOVERY,
    DISCOVERY_THRESHOLD
)


def estimate_pages(config, max_discovery=DEFAULT_MAX_DISCOVERY, timeout=30):
    """
    Estimate total pages that will be scraped

    Args:
        config: Configuration dictionary
        max_discovery: Maximum pages to discover (safety limit, use -1 for unlimited)
        timeout: Timeout for HTTP requests in seconds

    Returns:
        dict with estimation results
    """
    base_url = config['base_url']
    start_urls = config.get('start_urls', [base_url])
    url_patterns = config.get('url_patterns', {'include': [], 'exclude': []})
    rate_limit = config.get('rate_limit', DEFAULT_RATE_LIMIT)

    visited = set()
    pending = list(start_urls)
    discovered = 0

    include_patterns = url_patterns.get('include', [])
    exclude_patterns = url_patterns.get('exclude', [])

    # Handle unlimited mode
    unlimited = (max_discovery == -1 or max_discovery is None)

    print(f"🔍 Estimating pages for: {config['name']}")
    print(f"📍 Base URL: {base_url}")
    print(f"🎯 Start URLs: {len(start_urls)}")
    print(f"⏱️  Rate limit: {rate_limit}s")

    if unlimited:
        print(f"🔢 Max discovery: UNLIMITED (will discover all pages)")
        print(f"⚠️  WARNING: This may take a long time!")
    else:
        print(f"🔢 Max discovery: {max_discovery}")

    print()

    start_time = time.time()

    # Loop condition: stop if no more URLs, or if limit reached (when not unlimited)
    while pending and (unlimited or discovered < max_discovery):
        url = pending.pop(0)

        # Skip if already visited
        if url in visited:
            continue

        visited.add(url)
        discovered += 1

        # Progress indicator
        if discovered % 10 == 0:
            elapsed = time.time() - start_time
            rate = discovered / elapsed if elapsed > 0 else 0
            print(f"⏳ Discovered: {discovered} pages ({rate:.1f} pages/sec)", end='\r')

        try:
            # HEAD request first to check if page exists (faster)
            head_response = requests.head(url, timeout=timeout, allow_redirects=True)

            # Skip non-HTML content
            content_type = head_response.headers.get('Content-Type', '')
            if 'text/html' not in content_type:
                continue

            # Now GET the page to find links
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all links
            for link in soup.find_all('a', href=True):
                href = link['href']
                full_url = urljoin(url, href)

                # Normalize URL
                parsed = urlparse(full_url)
                full_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

                # Check if URL is valid
                if not is_valid_url(full_url, base_url, include_patterns, exclude_patterns):
                    continue

                # Add to pending if not visited
                if full_url not in visited and full_url not in pending:
                    pending.append(full_url)

            # Rate limiting
            time.sleep(rate_limit)

        except requests.RequestException as e:
            # Silently skip errors during estimation
            pass
        except Exception as e:
            # Silently skip other errors
            pass

    elapsed = time.time() - start_time

    # Results
    results = {
        'discovered': discovered,
        'pending': len(pending),
        'estimated_total': discovered + len(pending),
        'elapsed_seconds': round(elapsed, 2),
        'discovery_rate': round(discovered / elapsed if elapsed > 0 else 0, 2),
        'hit_limit': (not unlimited) and (discovered >= max_discovery),
        'unlimited': unlimited
    }

    return results


def is_valid_url(url, base_url, include_patterns, exclude_patterns):
    """Check if URL should be crawled"""
    # Must be same domain
    if not url.startswith(base_url.rstrip('/')):
        return False

    # Check exclude patterns first
    if exclude_patterns:
        for pattern in exclude_patterns:
            if pattern in url:
                return False

    # Check include patterns (if specified)
    if include_patterns:
        for pattern in include_patterns:
            if pattern in url:
                return True
        return False

    # If no include patterns, accept by default
    return True


def print_results(results, config):
    """Print estimation results"""
    print()
    print("=" * 70)
    print("📊 ESTIMATION RESULTS")
    print("=" * 70)
    print()
    print(f"Config: {config['name']}")
    print(f"Base URL: {config['base_url']}")
    print()
    print(f"✅ Pages Discovered: {results['discovered']}")
    print(f"⏳ Pages Pending: {results['pending']}")
    print(f"📈 Estimated Total: {results['estimated_total']}")
    print()
    print(f"⏱️  Time Elapsed: {results['elapsed_seconds']}s")
    print(f"⚡ Discovery Rate: {results['discovery_rate']} pages/sec")

    if results.get('unlimited', False):
        print()
        print("✅ UNLIMITED MODE - Discovered all reachable pages")
        print(f"   Total pages: {results['estimated_total']}")
    elif results['hit_limit']:
        print()
        print("⚠️  Hit discovery limit - actual total may be higher")
        print("   Increase max_discovery parameter for more accurate estimate")

    print()
    print("=" * 70)
    print("💡 RECOMMENDATIONS")
    print("=" * 70)
    print()

    estimated = results['estimated_total']
    current_max = config.get('max_pages', 100)

    if estimated <= current_max:
        print(f"✅ Current max_pages ({current_max}) is sufficient")
    else:
        recommended = min(estimated + 50, DISCOVERY_THRESHOLD)  # Add 50 buffer, cap at threshold
        print(f"⚠️  Current max_pages ({current_max}) may be too low")
        print(f"📝 Recommended max_pages: {recommended}")
        print(f"   (Estimated {estimated} + 50 buffer)")

    # Estimate time for full scrape
    rate_limit = config.get('rate_limit', DEFAULT_RATE_LIMIT)
    estimated_time = (estimated * rate_limit) / 60  # in minutes

    print()
    print(f"⏱️  Estimated full scrape time: {estimated_time:.1f} minutes")
    print(f"   (Based on rate_limit: {rate_limit}s)")

    print()


def load_config(config_path):
    """Load configuration from JSON file"""
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print(f"❌ Error: Config file not found: {config_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in config file: {e}")
        sys.exit(1)


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Estimate page count for Skill Seeker configs',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Estimate pages for a config
  skill-seekers estimate configs/react.json

  # Estimate with higher discovery limit
  skill-seekers estimate configs/godot.json --max-discovery 2000

  # Quick estimate (stop at 100 pages)
  skill-seekers estimate configs/vue.json --max-discovery 100
        """
    )

    parser.add_argument('config', help='Path to config JSON file')
    parser.add_argument('--max-discovery', '-m', type=int, default=DEFAULT_MAX_DISCOVERY,
                       help=f'Maximum pages to discover (default: {DEFAULT_MAX_DISCOVERY}, use -1 for unlimited)')
    parser.add_argument('--unlimited', '-u', action='store_true',
                       help='Remove discovery limit - discover all pages (same as --max-discovery -1)')
    parser.add_argument('--timeout', '-t', type=int, default=30,
                       help='HTTP request timeout in seconds (default: 30)')

    args = parser.parse_args()

    # Handle unlimited flag
    max_discovery = -1 if args.unlimited else args.max_discovery

    # Load config
    config = load_config(args.config)

    # Run estimation
    try:
        results = estimate_pages(config, max_discovery, args.timeout)
        print_results(results, config)

        # Return exit code based on results
        if results['hit_limit']:
            return 2  # Warning: hit limit
        return 0  # Success

    except KeyboardInterrupt:
        print("\n\n⚠️  Estimation interrupted by user")
        return 1
    except Exception as e:
        print(f"\n\n❌ Error during estimation: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
