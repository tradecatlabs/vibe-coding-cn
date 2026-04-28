"""Skill Seekers MCP (Model Context Protocol) server package.

This package provides MCP server integration for Claude Code, allowing
natural language interaction with Skill Seekers tools.

Main modules:
    - server: MCP server implementation with 9 tools

Available MCP Tools:
    - list_configs: List all available preset configurations
    - generate_config: Generate a new config file for any docs site
    - validate_config: Validate a config file structure
    - estimate_pages: Estimate page count before scraping
    - scrape_docs: Scrape and build a skill
    - package_skill: Package skill into .zip file (with auto-upload)
    - upload_skill: Upload .zip to Claude
    - split_config: Split large documentation configs
    - generate_router: Generate router/hub skills

Usage:
    The MCP server is typically run by Claude Code via configuration
    in ~/.config/claude-code/mcp.json
"""

__version__ = "2.0.0"

__all__ = []
