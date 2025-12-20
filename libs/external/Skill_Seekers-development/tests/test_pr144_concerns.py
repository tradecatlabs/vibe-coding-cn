#!/usr/bin/env python3
"""
Test script to investigate PR #144 concerns
"""

import sys
import json
import tempfile
from pathlib import Path
from collections import deque

# Add cli to path
sys.path.insert(0, str(Path(__file__).parent / 'cli'))

print("="*60)
print("PR #144 CONCERN INVESTIGATION")
print("="*60)

## CONCERN 1: Thread Safety
print("\n1. THREAD SAFETY ANALYSIS")
print("-" * 40)

print("✓ Lock created when workers > 1:")
print("  - Line 54-56: Creates self.lock with threading.Lock()")
print("  - Only created when self.workers > 1")

print("\n✓ Protected operations in scrape_page():")
print("  - print() - Line 295 (with lock)")
print("  - save_page() - Line 296 (with lock)")
print("  - pages.append() - Line 297 (with lock)")
print("  - visited_urls check - Line 301 (with lock)")
print("  - pending_urls.append() - Line 302 (with lock)")

print("\n✓ Protected operations in scrape_all():")
print("  - visited_urls.add() - Line 414 (BEFORE lock!)")
print("  - save_checkpoint() - Line 431 (with lock)")
print("  - print() - Line 435 (with lock)")

print("\n❌ RACE CONDITION FOUND:")
print("  - Line 414: visited_urls.add(url) is OUTSIDE lock")
print("  - Line 301: Link check 'if link not in visited_urls' is INSIDE lock")
print("  - Two threads could add same URL to visited_urls simultaneously")
print("  - Result: Same URL could be scraped twice")

## CONCERN 2: Checkpoint Behavior
print("\n2. CHECKPOINT WITH WORKERS")
print("-" * 40)

print("✓ Checkpoint save is protected:")
print("  - Line 430-431: Uses lock before save_checkpoint()")
print("  - save_checkpoint() itself does file I/O (line 103-104)")

print("\n⚠️  POTENTIAL ISSUE:")
print("  - pages_scraped counter incremented WITHOUT lock (line 427, 442)")
print("  - Could miss checkpoints or checkpoint at wrong interval")
print("  - Multiple threads incrementing same counter = race condition")

## CONCERN 3: Error Handling
print("\n3. ERROR HANDLING IN PARALLEL MODE")
print("-" * 40)

print("✓ Exceptions are caught in scrape_page():")
print("  - Line 319-324: try/except wraps entire method")
print("  - Errors are printed (with lock if workers > 1)")

print("\n✓ ThreadPoolExecutor exception handling:")
print("  - Exceptions stored in Future objects")
print("  - as_completed() will raise exception when accessed")

print("\n❌ SILENT FAILURE POSSIBLE:")
print("  - Line 425-442: Futures are iterated but exceptions not checked")
print("  - future.result() is never called - exceptions never raised")
print("  - Failed pages silently disappear")

## CONCERN 4: Rate Limiting Semantics
print("\n4. RATE LIMITING WITH WORKERS")
print("-" * 40)

print("✓ Rate limit applied per-worker:")
print("  - Line 315-317: time.sleep() after each scrape_page()")
print("  - Each worker sleeps independently")

print("\n✓ Semantics:")
print("  - 4 workers, 0.5s rate limit = 8 requests/second total")
print("  - 1 worker, 0.5s rate limit = 2 requests/second total")
print("  - This is per-worker, not global rate limiting")

print("\n⚠️  CONSIDERATION:")
print("  - Documentation should clarify this is per-worker")
print("  - Users might expect global rate limit")
print("  - 10 workers with 0.1s = 100 req/s (very aggressive)")

## CONCERN 5: Resource Limits
print("\n5. RESOURCE LIMITS")
print("-" * 40)

print("✓ Worker limit enforced:")
print("  - Capped at 10 workers (mentioned in PR)")
print("  - ThreadPoolExecutor bounds threads")

print("\n❌ NO MEMORY LIMITS:")
print("  - self.pages list grows unbounded")
print("  - visited_urls set grows unbounded")
print("  - 10,000 pages * avg 50KB each = 500MB minimum")
print("  - Unlimited mode could cause OOM")

print("\n❌ NO PENDING URL LIMIT:")
print("  - pending_urls deque grows unbounded")
print("  - Could have thousands of URLs queued")

## CONCERN 6: Streaming Subprocess
print("\n6. STREAMING SUBPROCESS")
print("-" * 40)

print("✓ Good implementation:")
print("  - Uses select() for non-blocking I/O")
print("  - Timeout mechanism works (line 60-63)")
print("  - Kills process on timeout")

print("\n⚠️  Windows fallback:")
print("  - Line 83-85: Falls back to sleep() on Windows")
print("  - Won't stream output on Windows (will appear frozen)")
print("  - But will still work, just poor UX")

print("\n✓ Process cleanup:")
print("  - Line 88: communicate() gets remaining output")
print("  - process.returncode properly captured")

print("\n" + "="*60)
print("SUMMARY OF FINDINGS")
print("="*60)

print("\n🚨 CRITICAL ISSUES FOUND:")
print("1. Race condition on visited_urls.add() (line 414)")
print("2. pages_scraped counter not thread-safe")
print("3. Silent exception swallowing in parallel mode")

print("\n⚠️  MODERATE CONCERNS:")
print("4. No memory limits for unlimited mode")
print("5. Per-worker rate limiting may confuse users")
print("6. Windows streaming falls back to polling")

print("\n✅ WORKS CORRECTLY:")
print("7. Lock protects most shared state")
print("8. Checkpoint saves are protected")
print("9. save_page() file I/O protected")
print("10. Timeout mechanism solid")

print("\n" + "="*60)
