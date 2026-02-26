#!/usr/bin/env python3
"""
Tests for Unified Multi-Source Scraper

Covers:
- Config validation (unified vs legacy)
- Conflict detection
- Rule-based merging
- Skill building
"""

import os
import sys
import json
import pytest
import tempfile
from pathlib import Path

from skill_seekers.cli.config_validator import ConfigValidator, validate_config
from skill_seekers.cli.conflict_detector import ConflictDetector, Conflict
from skill_seekers.cli.merge_sources import RuleBasedMerger
from skill_seekers.cli.unified_skill_builder import UnifiedSkillBuilder


# ===========================
# Config Validation Tests
# ===========================

def test_detect_unified_format():
    """Test unified format detection"""
    import tempfile
    import json

    unified_config = {
        "name": "test",
        "description": "Test skill",
        "sources": [
            {"type": "documentation", "base_url": "https://example.com"}
        ]
    }

    legacy_config = {
        "name": "test",
        "description": "Test skill",
        "base_url": "https://example.com"
    }

    # Test unified detection
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(unified_config, f)
        config_path = f.name

    try:
        validator = ConfigValidator(config_path)
        assert validator.is_unified == True
    finally:
        os.unlink(config_path)

    # Test legacy detection
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(legacy_config, f)
        config_path = f.name

    try:
        validator = ConfigValidator(config_path)
        assert validator.is_unified == False
    finally:
        os.unlink(config_path)


def test_validate_unified_sources():
    """Test source type validation"""
    config = {
        "name": "test",
        "description": "Test",
        "sources": [
            {"type": "documentation", "base_url": "https://example.com"},
            {"type": "github", "repo": "user/repo"},
            {"type": "pdf", "path": "/path/to.pdf"}
        ]
    }

    validator = ConfigValidator(config)
    validator.validate()
    assert len(validator.config['sources']) == 3


def test_validate_invalid_source_type():
    """Test invalid source type raises error"""
    config = {
        "name": "test",
        "description": "Test",
        "sources": [
            {"type": "invalid_type", "url": "https://example.com"}
        ]
    }

    validator = ConfigValidator(config)
    with pytest.raises(ValueError, match="Invalid type"):
        validator.validate()


def test_needs_api_merge():
    """Test API merge detection"""
    # Config with both docs and GitHub code
    config_needs_merge = {
        "name": "test",
        "description": "Test",
        "sources": [
            {"type": "documentation", "base_url": "https://example.com", "extract_api": True},
            {"type": "github", "repo": "user/repo", "include_code": True}
        ]
    }

    validator = ConfigValidator(config_needs_merge)
    assert validator.needs_api_merge() == True

    # Config with only docs
    config_no_merge = {
        "name": "test",
        "description": "Test",
        "sources": [
            {"type": "documentation", "base_url": "https://example.com"}
        ]
    }

    validator = ConfigValidator(config_no_merge)
    assert validator.needs_api_merge() == False


def test_backward_compatibility():
    """Test legacy config conversion"""
    legacy_config = {
        "name": "test",
        "description": "Test skill",
        "base_url": "https://example.com",
        "selectors": {"main_content": "article"},
        "max_pages": 100
    }

    validator = ConfigValidator(legacy_config)
    unified = validator.convert_legacy_to_unified()

    assert 'sources' in unified
    assert len(unified['sources']) == 1
    assert unified['sources'][0]['type'] == 'documentation'
    assert unified['sources'][0]['base_url'] == 'https://example.com'


# ===========================
# Conflict Detection Tests
# ===========================

def test_detect_missing_in_docs():
    """Test detection of APIs missing in documentation"""
    docs_data = {
        'pages': [
            {
                'url': 'https://example.com/api',
                'apis': [
                    {
                        'name': 'documented_func',
                        'parameters': [{'name': 'x', 'type': 'int'}],
                        'return_type': 'str'
                    }
                ]
            }
        ]
    }

    github_data = {
        'code_analysis': {
            'analyzed_files': [
                {
                    'functions': [
                        {
                            'name': 'undocumented_func',
                            'parameters': [{'name': 'y', 'type_hint': 'float'}],
                            'return_type': 'bool'
                        }
                    ]
                }
            ]
        }
    }

    detector = ConflictDetector(docs_data, github_data)
    conflicts = detector._find_missing_in_docs()

    assert len(conflicts) > 0
    assert any(c.type == 'missing_in_docs' for c in conflicts)
    assert any(c.api_name == 'undocumented_func' for c in conflicts)


def test_detect_missing_in_code():
    """Test detection of APIs missing in code"""
    docs_data = {
        'pages': [
            {
                'url': 'https://example.com/api',
                'apis': [
                    {
                        'name': 'obsolete_func',
                        'parameters': [{'name': 'x', 'type': 'int'}],
                        'return_type': 'str'
                    }
                ]
            }
        ]
    }

    github_data = {
        'code_analysis': {
            'analyzed_files': []
        }
    }

    detector = ConflictDetector(docs_data, github_data)
    conflicts = detector._find_missing_in_code()

    assert len(conflicts) > 0
    assert any(c.type == 'missing_in_code' for c in conflicts)
    assert any(c.api_name == 'obsolete_func' for c in conflicts)


def test_detect_signature_mismatch():
    """Test detection of signature mismatches"""
    docs_data = {
        'pages': [
            {
                'url': 'https://example.com/api',
                'apis': [
                    {
                        'name': 'func',
                        'parameters': [{'name': 'x', 'type': 'int'}],
                        'return_type': 'str'
                    }
                ]
            }
        ]
    }

    github_data = {
        'code_analysis': {
            'analyzed_files': [
                {
                    'functions': [
                        {
                            'name': 'func',
                            'parameters': [
                                {'name': 'x', 'type_hint': 'int'},
                                {'name': 'y', 'type_hint': 'bool', 'default': 'False'}
                            ],
                            'return_type': 'str'
                        }
                    ]
                }
            ]
        }
    }

    detector = ConflictDetector(docs_data, github_data)
    conflicts = detector._find_signature_mismatches()

    assert len(conflicts) > 0
    assert any(c.type == 'signature_mismatch' for c in conflicts)
    assert any(c.api_name == 'func' for c in conflicts)


def test_conflict_severity():
    """Test conflict severity assignment"""
    # High severity: missing_in_code
    conflict_high = Conflict(
        type='missing_in_code',
        severity='high',
        api_name='test',
        docs_info={'name': 'test'},
        code_info=None,
        difference='API documented but not in code'
    )
    assert conflict_high.severity == 'high'

    # Medium severity: missing_in_docs
    conflict_medium = Conflict(
        type='missing_in_docs',
        severity='medium',
        api_name='test',
        docs_info=None,
        code_info={'name': 'test'},
        difference='API in code but not documented'
    )
    assert conflict_medium.severity == 'medium'


# ===========================
# Merge Tests
# ===========================

def test_rule_based_merge_docs_only():
    """Test rule-based merge for docs-only APIs"""
    docs_data = {
        'pages': [
            {
                'url': 'https://example.com/api',
                'apis': [
                    {
                        'name': 'docs_only_api',
                        'parameters': [{'name': 'x', 'type': 'int'}],
                        'return_type': 'str'
                    }
                ]
            }
        ]
    }

    github_data = {'code_analysis': {'analyzed_files': []}}

    detector = ConflictDetector(docs_data, github_data)
    conflicts = detector.detect_all_conflicts()

    merger = RuleBasedMerger(docs_data, github_data, conflicts)
    merged = merger.merge_all()

    assert 'apis' in merged
    assert 'docs_only_api' in merged['apis']
    assert merged['apis']['docs_only_api']['status'] == 'docs_only'


def test_rule_based_merge_code_only():
    """Test rule-based merge for code-only APIs"""
    docs_data = {'pages': []}

    github_data = {
        'code_analysis': {
            'analyzed_files': [
                {
                    'functions': [
                        {
                            'name': 'code_only_api',
                            'parameters': [{'name': 'y', 'type_hint': 'float'}],
                            'return_type': 'bool'
                        }
                    ]
                }
            ]
        }
    }

    detector = ConflictDetector(docs_data, github_data)
    conflicts = detector.detect_all_conflicts()

    merger = RuleBasedMerger(docs_data, github_data, conflicts)
    merged = merger.merge_all()

    assert 'apis' in merged
    assert 'code_only_api' in merged['apis']
    assert merged['apis']['code_only_api']['status'] == 'code_only'


def test_rule_based_merge_matched():
    """Test rule-based merge for matched APIs"""
    docs_data = {
        'pages': [
            {
                'url': 'https://example.com/api',
                'apis': [
                    {
                        'name': 'matched_api',
                        'parameters': [{'name': 'x', 'type': 'int'}],
                        'return_type': 'str'
                    }
                ]
            }
        ]
    }

    github_data = {
        'code_analysis': {
            'analyzed_files': [
                {
                    'functions': [
                        {
                            'name': 'matched_api',
                            'parameters': [{'name': 'x', 'type_hint': 'int'}],
                            'return_type': 'str'
                        }
                    ]
                }
            ]
        }
    }

    detector = ConflictDetector(docs_data, github_data)
    conflicts = detector.detect_all_conflicts()

    merger = RuleBasedMerger(docs_data, github_data, conflicts)
    merged = merger.merge_all()

    assert 'apis' in merged
    assert 'matched_api' in merged['apis']
    assert merged['apis']['matched_api']['status'] == 'matched'


def test_merge_summary():
    """Test merge summary statistics"""
    docs_data = {
        'pages': [
            {
                'url': 'https://example.com/api',
                'apis': [
                    {'name': 'api1', 'parameters': [], 'return_type': 'str'},
                    {'name': 'api2', 'parameters': [], 'return_type': 'int'}
                ]
            }
        ]
    }

    github_data = {
        'code_analysis': {
            'analyzed_files': [
                {
                    'functions': [
                        {'name': 'api3', 'parameters': [], 'return_type': 'bool'}
                    ]
                }
            ]
        }
    }

    detector = ConflictDetector(docs_data, github_data)
    conflicts = detector.detect_all_conflicts()

    merger = RuleBasedMerger(docs_data, github_data, conflicts)
    merged = merger.merge_all()

    assert 'summary' in merged
    assert merged['summary']['total_apis'] == 3
    assert merged['summary']['docs_only'] == 2
    assert merged['summary']['code_only'] == 1


# ===========================
# Skill Builder Tests
# ===========================

def test_skill_builder_basic():
    """Test basic skill building"""
    config = {
        'name': 'test_skill',
        'description': 'Test skill description',
        'sources': [
            {'type': 'documentation', 'base_url': 'https://example.com'}
        ]
    }

    scraped_data = {
        'documentation': {
            'pages': [],
            'data_file': '/tmp/test.json'
        }
    }

    with tempfile.TemporaryDirectory() as tmpdir:
        # Override output directory
        builder = UnifiedSkillBuilder(config, scraped_data)
        builder.skill_dir = tmpdir

        builder._generate_skill_md()

        # Check SKILL.md was created
        skill_md = Path(tmpdir) / 'SKILL.md'
        assert skill_md.exists()

        content = skill_md.read_text()
        assert 'test_skill' in content.lower()
        assert 'Test skill description' in content


def test_skill_builder_with_conflicts():
    """Test skill building with conflicts"""
    config = {
        'name': 'test_skill',
        'description': 'Test',
        'sources': [
            {'type': 'documentation', 'base_url': 'https://example.com'},
            {'type': 'github', 'repo': 'user/repo'}
        ]
    }

    scraped_data = {}

    conflicts = [
        Conflict(
            type='missing_in_code',
            severity='high',
            api_name='test_api',
            docs_info={'name': 'test_api'},
            code_info=None,
            difference='Test difference'
        )
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        builder = UnifiedSkillBuilder(config, scraped_data, conflicts=conflicts)
        builder.skill_dir = tmpdir

        builder._generate_skill_md()

        skill_md = Path(tmpdir) / 'SKILL.md'
        content = skill_md.read_text()

        assert '1 conflicts detected' in content
        assert 'missing_in_code' in content


def test_skill_builder_merged_apis():
    """Test skill building with merged APIs"""
    config = {
        'name': 'test',
        'description': 'Test',
        'sources': []
    }

    scraped_data = {}

    merged_data = {
        'apis': {
            'test_api': {
                'name': 'test_api',
                'status': 'matched',
                'merged_signature': 'test_api(x: int) -> str',
                'merged_description': 'Test API',
                'source': 'both'
            }
        }
    }

    with tempfile.TemporaryDirectory() as tmpdir:
        builder = UnifiedSkillBuilder(config, scraped_data, merged_data=merged_data)
        builder.skill_dir = tmpdir

        content = builder._format_merged_apis()

        assert '✅ Verified APIs' in content
        assert 'test_api' in content


# ===========================
# Integration Tests
# ===========================

def test_full_workflow_unified_config():
    """Test complete workflow with unified config"""
    # Create test config
    config = {
        "name": "test_unified",
        "description": "Test unified workflow",
        "merge_mode": "rule-based",
        "sources": [
            {
                "type": "documentation",
                "base_url": "https://example.com",
                "extract_api": True
            },
            {
                "type": "github",
                "repo": "user/repo",
                "include_code": True,
                "code_analysis_depth": "surface"
            }
        ]
    }

    # Validate config
    validator = ConfigValidator(config)
    validator.validate()
    assert validator.is_unified == True
    assert validator.needs_api_merge() == True


def test_config_file_validation():
    """Test validation from config file"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        config = {
            "name": "test",
            "description": "Test",
            "sources": [
                {"type": "documentation", "base_url": "https://example.com"}
            ]
        }
        json.dump(config, f)
        config_path = f.name

    try:
        validator = validate_config(config_path)
        assert validator.is_unified == True
    finally:
        os.unlink(config_path)


# Run tests
if __name__ == '__main__':
    pytest.main([__file__, '-v'])
