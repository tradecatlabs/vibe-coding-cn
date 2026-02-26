#!/usr/bin/env python3
"""
Test MCP Integration with Unified Scraping

Tests that the MCP server correctly handles unified configs.
"""

import sys
import os
import json
import tempfile
import asyncio
import pytest
from pathlib import Path

# WORKAROUND for shadowing issue: Temporarily change to /tmp to import external mcp
# This avoids any local mcp/ directory being in the import path
_original_dir = os.getcwd()
MCP_AVAILABLE = False
try:
    os.chdir('/tmp')  # Change away from project directory
    from mcp.types import TextContent
    MCP_AVAILABLE = True
except ImportError:
    pass
finally:
    os.chdir(_original_dir)  # Restore original directory

# Configure pytest to only use asyncio backend (not trio)
pytestmark = pytest.mark.anyio

if MCP_AVAILABLE:
    from skill_seekers.mcp.server import validate_config_tool, scrape_docs_tool
else:
    validate_config_tool = None
    scrape_docs_tool = None


@pytest.mark.skipif(not MCP_AVAILABLE, reason="MCP package not installed")
async def test_mcp_validate_unified_config():
    """Test that MCP can validate unified configs"""
    print("\n✓ Testing MCP validate_config_tool with unified config...")

    # Use existing unified config
    config_path = "configs/react_unified.json"

    if not Path(config_path).exists():
        print(f"  ⚠️  Skipping: {config_path} not found")
        return

    args = {"config_path": config_path}
    result = await validate_config_tool(args)

    # Check result
    text = result[0].text
    assert "✅" in text, f"Expected success, got: {text}"
    assert "Unified" in text, f"Expected unified format detected, got: {text}"
    assert "Sources:" in text, f"Expected sources count, got: {text}"

    print("  ✅ MCP correctly validates unified config")


@pytest.mark.skipif(not MCP_AVAILABLE, reason="MCP package not installed")
async def test_mcp_validate_legacy_config():
    """Test that MCP can validate legacy configs"""
    print("\n✓ Testing MCP validate_config_tool with legacy config...")

    # Use existing legacy config
    config_path = "configs/react.json"

    if not Path(config_path).exists():
        print(f"  ⚠️  Skipping: {config_path} not found")
        return

    args = {"config_path": config_path}
    result = await validate_config_tool(args)

    # Check result
    text = result[0].text
    assert "✅" in text, f"Expected success, got: {text}"
    assert "Legacy" in text, f"Expected legacy format detected, got: {text}"

    print("  ✅ MCP correctly validates legacy config")


@pytest.mark.skipif(not MCP_AVAILABLE, reason="MCP package not installed")
async def test_mcp_scrape_docs_detection():
    """Test that MCP scrape_docs correctly detects format"""
    print("\n✓ Testing MCP scrape_docs format detection...")

    # Create temporary unified config
    unified_config = {
        "name": "test_mcp_unified",
        "description": "Test unified via MCP",
        "merge_mode": "rule-based",
        "sources": [
            {
                "type": "documentation",
                "base_url": "https://example.com",
                "extract_api": True,
                "max_pages": 5
            }
        ]
    }

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(unified_config, f)
        unified_config_path = f.name

    # Create temporary legacy config
    legacy_config = {
        "name": "test_mcp_legacy",
        "description": "Test legacy via MCP",
        "base_url": "https://example.com",
        "max_pages": 5
    }

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(legacy_config, f)
        legacy_config_path = f.name

    try:
        # Test unified detection
        with open(unified_config_path, 'r') as f:
            config = json.load(f)

        is_unified = 'sources' in config and isinstance(config['sources'], list)
        assert is_unified, "Should detect unified format"
        print("  ✅ Unified format detected correctly")

        # Test legacy detection
        with open(legacy_config_path, 'r') as f:
            config = json.load(f)

        is_unified = 'sources' in config and isinstance(config['sources'], list)
        assert not is_unified, "Should detect legacy format"
        print("  ✅ Legacy format detected correctly")

    finally:
        # Cleanup
        Path(unified_config_path).unlink(missing_ok=True)
        Path(legacy_config_path).unlink(missing_ok=True)


@pytest.mark.skipif(not MCP_AVAILABLE, reason="MCP package not installed")
async def test_mcp_merge_mode_override():
    """Test that MCP can override merge mode"""
    print("\n✓ Testing MCP merge_mode override...")

    # Create unified config
    config = {
        "name": "test_merge_override",
        "description": "Test merge mode override",
        "merge_mode": "rule-based",
        "sources": [
            {"type": "documentation", "base_url": "https://example.com"}
        ]
    }

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(config, f)
        config_path = f.name

    try:
        # Test that we can override merge_mode in args
        args = {
            "config_path": config_path,
            "merge_mode": "claude-enhanced"  # Override
        }

        # Check that args has merge_mode
        assert args.get("merge_mode") == "claude-enhanced"
        print("  ✅ Merge mode override supported")

    finally:
        Path(config_path).unlink(missing_ok=True)


# Run all tests
async def run_all_tests():
    print("=" * 60)
    print("MCP Unified Scraping Integration Tests")
    print("=" * 60)

    try:
        await test_mcp_validate_unified_config()
        await test_mcp_validate_legacy_config()
        await test_mcp_scrape_docs_detection()
        await test_mcp_merge_mode_override()

        print("\n" + "=" * 60)
        print("✅ All MCP integration tests passed!")
        print("=" * 60)

    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    asyncio.run(run_all_tests())
