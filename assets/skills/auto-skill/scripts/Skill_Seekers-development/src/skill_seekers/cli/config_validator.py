#!/usr/bin/env python3
"""
Unified Config Validator

Validates unified config format that supports multiple sources:
- documentation (website scraping)
- github (repository scraping)
- pdf (PDF document scraping)

Also provides backward compatibility detection for legacy configs.
"""

import json
import logging
from typing import Dict, Any, List, Optional, Union
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ConfigValidator:
    """
    Validates unified config format and provides backward compatibility.
    """

    # Valid source types
    VALID_SOURCE_TYPES = {'documentation', 'github', 'pdf'}

    # Valid merge modes
    VALID_MERGE_MODES = {'rule-based', 'claude-enhanced'}

    # Valid code analysis depth levels
    VALID_DEPTH_LEVELS = {'surface', 'deep', 'full'}

    def __init__(self, config_or_path: Union[Dict[str, Any], str]):
        """
        Initialize validator with config dict or file path.

        Args:
            config_or_path: Either a config dict or path to config JSON file
        """
        if isinstance(config_or_path, dict):
            self.config_path = None
            self.config = config_or_path
        else:
            self.config_path = config_or_path
            self.config = self._load_config()
        self.is_unified = self._detect_format()

    def _load_config(self) -> Dict[str, Any]:
        """Load JSON config file."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise ValueError(f"Config file not found: {self.config_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in config file: {e}")

    def _detect_format(self) -> bool:
        """
        Detect if config is unified format or legacy.

        Returns:
            True if unified format (has 'sources' array)
            False if legacy format
        """
        return 'sources' in self.config and isinstance(self.config['sources'], list)

    def validate(self) -> bool:
        """
        Validate config based on detected format.

        Returns:
            True if valid

        Raises:
            ValueError if invalid with detailed error message
        """
        if self.is_unified:
            return self._validate_unified()
        else:
            return self._validate_legacy()

    def _validate_unified(self) -> bool:
        """Validate unified config format."""
        logger.info("Validating unified config format...")

        # Required top-level fields
        if 'name' not in self.config:
            raise ValueError("Missing required field: 'name'")

        if 'description' not in self.config:
            raise ValueError("Missing required field: 'description'")

        if 'sources' not in self.config:
            raise ValueError("Missing required field: 'sources'")

        # Validate sources array
        sources = self.config['sources']

        if not isinstance(sources, list):
            raise ValueError("'sources' must be an array")

        if len(sources) == 0:
            raise ValueError("'sources' array cannot be empty")

        # Validate merge_mode (optional)
        merge_mode = self.config.get('merge_mode', 'rule-based')
        if merge_mode not in self.VALID_MERGE_MODES:
            raise ValueError(f"Invalid merge_mode: '{merge_mode}'. Must be one of {self.VALID_MERGE_MODES}")

        # Validate each source
        for i, source in enumerate(sources):
            self._validate_source(source, i)

        logger.info(f"✅ Unified config valid: {len(sources)} sources")
        return True

    def _validate_source(self, source: Dict[str, Any], index: int):
        """Validate individual source configuration."""
        # Check source has 'type' field
        if 'type' not in source:
            raise ValueError(f"Source {index}: Missing required field 'type'")

        source_type = source['type']

        if source_type not in self.VALID_SOURCE_TYPES:
            raise ValueError(
                f"Source {index}: Invalid type '{source_type}'. "
                f"Must be one of {self.VALID_SOURCE_TYPES}"
            )

        # Type-specific validation
        if source_type == 'documentation':
            self._validate_documentation_source(source, index)
        elif source_type == 'github':
            self._validate_github_source(source, index)
        elif source_type == 'pdf':
            self._validate_pdf_source(source, index)

    def _validate_documentation_source(self, source: Dict[str, Any], index: int):
        """Validate documentation source configuration."""
        if 'base_url' not in source:
            raise ValueError(f"Source {index} (documentation): Missing required field 'base_url'")

        # Optional but recommended fields
        if 'selectors' not in source:
            logger.warning(f"Source {index} (documentation): No 'selectors' specified, using defaults")

        if 'max_pages' in source and not isinstance(source['max_pages'], int):
            raise ValueError(f"Source {index} (documentation): 'max_pages' must be an integer")

    def _validate_github_source(self, source: Dict[str, Any], index: int):
        """Validate GitHub source configuration."""
        if 'repo' not in source:
            raise ValueError(f"Source {index} (github): Missing required field 'repo'")

        # Validate repo format (owner/repo)
        repo = source['repo']
        if '/' not in repo:
            raise ValueError(
                f"Source {index} (github): Invalid repo format '{repo}'. "
                f"Must be 'owner/repo' (e.g., 'facebook/react')"
            )

        # Validate code_analysis_depth if specified
        if 'code_analysis_depth' in source:
            depth = source['code_analysis_depth']
            if depth not in self.VALID_DEPTH_LEVELS:
                raise ValueError(
                    f"Source {index} (github): Invalid code_analysis_depth '{depth}'. "
                    f"Must be one of {self.VALID_DEPTH_LEVELS}"
                )

        # Validate max_issues if specified
        if 'max_issues' in source and not isinstance(source['max_issues'], int):
            raise ValueError(f"Source {index} (github): 'max_issues' must be an integer")

    def _validate_pdf_source(self, source: Dict[str, Any], index: int):
        """Validate PDF source configuration."""
        if 'path' not in source:
            raise ValueError(f"Source {index} (pdf): Missing required field 'path'")

        # Check if file exists
        pdf_path = source['path']
        if not Path(pdf_path).exists():
            logger.warning(f"Source {index} (pdf): File not found: {pdf_path}")

    def _validate_legacy(self) -> bool:
        """
        Validate legacy config format (backward compatibility).

        Legacy configs are the old format used by doc_scraper, github_scraper, pdf_scraper.
        """
        logger.info("Detected legacy config format (backward compatible)")

        # Detect which legacy type based on fields
        if 'base_url' in self.config:
            logger.info("Legacy type: documentation")
        elif 'repo' in self.config:
            logger.info("Legacy type: github")
        elif 'pdf' in self.config or 'path' in self.config:
            logger.info("Legacy type: pdf")
        else:
            raise ValueError("Cannot detect legacy config type (missing base_url, repo, or pdf)")

        return True

    def convert_legacy_to_unified(self) -> Dict[str, Any]:
        """
        Convert legacy config to unified format.

        Returns:
            Unified config dict
        """
        if self.is_unified:
            logger.info("Config already in unified format")
            return self.config

        logger.info("Converting legacy config to unified format...")

        # Detect legacy type and convert
        if 'base_url' in self.config:
            return self._convert_legacy_documentation()
        elif 'repo' in self.config:
            return self._convert_legacy_github()
        elif 'pdf' in self.config or 'path' in self.config:
            return self._convert_legacy_pdf()
        else:
            raise ValueError("Cannot convert: unknown legacy format")

    def _convert_legacy_documentation(self) -> Dict[str, Any]:
        """Convert legacy documentation config to unified."""
        unified = {
            'name': self.config.get('name', 'unnamed'),
            'description': self.config.get('description', 'Documentation skill'),
            'merge_mode': 'rule-based',
            'sources': [
                {
                    'type': 'documentation',
                    **{k: v for k, v in self.config.items()
                       if k not in ['name', 'description']}
                }
            ]
        }
        return unified

    def _convert_legacy_github(self) -> Dict[str, Any]:
        """Convert legacy GitHub config to unified."""
        unified = {
            'name': self.config.get('name', 'unnamed'),
            'description': self.config.get('description', 'GitHub repository skill'),
            'merge_mode': 'rule-based',
            'sources': [
                {
                    'type': 'github',
                    **{k: v for k, v in self.config.items()
                       if k not in ['name', 'description']}
                }
            ]
        }
        return unified

    def _convert_legacy_pdf(self) -> Dict[str, Any]:
        """Convert legacy PDF config to unified."""
        unified = {
            'name': self.config.get('name', 'unnamed'),
            'description': self.config.get('description', 'PDF document skill'),
            'merge_mode': 'rule-based',
            'sources': [
                {
                    'type': 'pdf',
                    **{k: v for k, v in self.config.items()
                       if k not in ['name', 'description']}
                }
            ]
        }
        return unified

    def get_sources_by_type(self, source_type: str) -> List[Dict[str, Any]]:
        """
        Get all sources of a specific type.

        Args:
            source_type: 'documentation', 'github', or 'pdf'

        Returns:
            List of sources matching the type
        """
        if not self.is_unified:
            # For legacy, convert and get sources
            unified = self.convert_legacy_to_unified()
            sources = unified['sources']
        else:
            sources = self.config['sources']

        return [s for s in sources if s.get('type') == source_type]

    def has_multiple_sources(self) -> bool:
        """Check if config has multiple sources (requires merging)."""
        if not self.is_unified:
            return False
        return len(self.config['sources']) > 1

    def needs_api_merge(self) -> bool:
        """
        Check if config needs API merging.

        Returns True if both documentation and github sources exist
        with API extraction enabled.
        """
        if not self.has_multiple_sources():
            return False

        has_docs_api = any(
            s.get('type') == 'documentation' and s.get('extract_api', True)
            for s in self.config['sources']
        )

        has_github_code = any(
            s.get('type') == 'github' and s.get('include_code', False)
            for s in self.config['sources']
        )

        return has_docs_api and has_github_code


def validate_config(config_path: str) -> ConfigValidator:
    """
    Validate config file and return validator instance.

    Args:
        config_path: Path to config JSON file

    Returns:
        ConfigValidator instance

    Raises:
        ValueError if config is invalid
    """
    validator = ConfigValidator(config_path)
    validator.validate()
    return validator


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python config_validator.py <config.json>")
        sys.exit(1)

    config_file = sys.argv[1]

    try:
        validator = validate_config(config_file)

        print(f"\n✅ Config valid!")
        print(f"   Format: {'Unified' if validator.is_unified else 'Legacy'}")
        print(f"   Name: {validator.config.get('name')}")

        if validator.is_unified:
            sources = validator.config['sources']
            print(f"   Sources: {len(sources)}")
            for i, source in enumerate(sources):
                print(f"     {i+1}. {source['type']}")

            if validator.needs_api_merge():
                merge_mode = validator.config.get('merge_mode', 'rule-based')
                print(f"   ⚠️  API merge required (mode: {merge_mode})")

    except ValueError as e:
        print(f"\n❌ Config invalid: {e}")
        sys.exit(1)
