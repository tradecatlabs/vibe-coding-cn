"""MCP tools subpackage.

This package will contain modularized MCP tool implementations.

Planned structure (for future refactoring):
    - scraping_tools.py: Tools for scraping (estimate_pages, scrape_docs)
    - building_tools.py: Tools for building (package_skill, validate_config)
    - deployment_tools.py: Tools for deployment (upload_skill)
    - config_tools.py: Tools for configs (list_configs, generate_config)
    - advanced_tools.py: Advanced tools (split_config, generate_router)

Current state:
    All tools are currently implemented in mcp/server.py
    This directory is a placeholder for future modularization.
"""

__version__ = "2.0.0"

__all__ = []
