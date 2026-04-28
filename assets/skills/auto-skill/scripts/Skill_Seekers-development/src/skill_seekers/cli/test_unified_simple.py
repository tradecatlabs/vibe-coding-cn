#!/usr/bin/env python3
"""
Simple Integration Tests for Unified Multi-Source Scraper

Focuses on real-world usage patterns rather than unit tests.
"""

import os
import sys
import json
import tempfile
from pathlib import Path

# Add CLI to path
sys.path.insert(0, str(Path(__file__).parent))

from .config_validator import validate_config

def test_validate_existing_unified_configs():
    """Test that all existing unified configs are valid"""
    configs_dir = Path(__file__).parent.parent / 'configs'

    unified_configs = [
        'godot_unified.json',
        'react_unified.json',
        'django_unified.json',
        'fastapi_unified.json'
    ]

    for config_name in unified_configs:
        config_path = configs_dir / config_name
        if config_path.exists():
            print(f"\n✓ Validating {config_name}...")
            validator = validate_config(str(config_path))
            assert validator.is_unified, f"{config_name} should be unified format"
            assert validator.needs_api_merge(), f"{config_name} should need API merging"
            print(f"  Sources: {len(validator.config['sources'])}")
            print(f"  Merge mode: {validator.config.get('merge_mode')}")


def test_backward_compatibility():
    """Test that legacy configs still work"""
    configs_dir = Path(__file__).parent.parent / 'configs'

    legacy_configs = [
        'react.json',
        'godot.json',
        'django.json'
    ]

    for config_name in legacy_configs:
        config_path = configs_dir / config_name
        if config_path.exists():
            print(f"\n✓ Validating legacy {config_name}...")
            validator = validate_config(str(config_path))
            assert not validator.is_unified, f"{config_name} should be legacy format"
            print(f"  Format: Legacy")


def test_create_temp_unified_config():
    """Test creating a unified config from scratch"""
    config = {
        "name": "test_unified",
        "description": "Test unified config",
        "merge_mode": "rule-based",
        "sources": [
            {
                "type": "documentation",
                "base_url": "https://example.com/docs",
                "extract_api": True,
                "max_pages": 50
            },
            {
                "type": "github",
                "repo": "test/repo",
                "include_code": True,
                "code_analysis_depth": "surface"
            }
        ]
    }

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(config, f)
        config_path = f.name

    try:
        print("\n✓ Validating temp unified config...")
        validator = validate_config(config_path)
        assert validator.is_unified
        assert validator.needs_api_merge()
        assert len(validator.config['sources']) == 2
        print("  ✓ Config is valid unified format")
        print(f"  Sources: {len(validator.config['sources'])}")
    finally:
        os.unlink(config_path)


def test_mixed_source_types():
    """Test config with documentation, GitHub, and PDF sources"""
    config = {
        "name": "test_mixed",
        "description": "Test mixed sources",
        "merge_mode": "rule-based",
        "sources": [
            {
                "type": "documentation",
                "base_url": "https://example.com"
            },
            {
                "type": "github",
                "repo": "test/repo"
            },
            {
                "type": "pdf",
                "path": "/path/to/manual.pdf"
            }
        ]
    }

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(config, f)
        config_path = f.name

    try:
        print("\n✓ Validating mixed source types...")
        validator = validate_config(config_path)
        assert validator.is_unified
        assert len(validator.config['sources']) == 3

        # Check each source type
        source_types = [s['type'] for s in validator.config['sources']]
        assert 'documentation' in source_types
        assert 'github' in source_types
        assert 'pdf' in source_types
        print("  ✓ All 3 source types validated")
    finally:
        os.unlink(config_path)


def test_config_validation_errors():
    """Test that invalid configs are rejected"""
    # Invalid source type
    config = {
        "name": "test",
        "description": "Test",
        "sources": [
            {"type": "invalid_type", "url": "https://example.com"}
        ]
    }

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(config, f)
        config_path = f.name

    try:
        print("\n✓ Testing invalid source type...")
        try:
            # validate_config() calls .validate() automatically
            validator = validate_config(config_path)
            assert False, "Should have raised error for invalid source type"
        except ValueError as e:
            assert "Invalid" in str(e) or "invalid" in str(e)
            print("  ✓ Invalid source type correctly rejected")
    finally:
        os.unlink(config_path)


# Run tests
if __name__ == '__main__':
    print("=" * 60)
    print("Running Unified Scraper Integration Tests")
    print("=" * 60)

    try:
        test_validate_existing_unified_configs()
        test_backward_compatibility()
        test_create_temp_unified_config()
        test_mixed_source_types()
        test_config_validation_errors()

        print("\n" + "=" * 60)
        print("✅ All integration tests passed!")
        print("=" * 60)

    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
