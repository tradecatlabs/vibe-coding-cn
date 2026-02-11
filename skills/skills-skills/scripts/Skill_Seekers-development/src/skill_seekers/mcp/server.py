#!/usr/bin/env python3
"""
Skill Seeker MCP Server
Model Context Protocol server for generating Claude AI skills from documentation
"""

import asyncio
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

# Import external MCP package
# NOTE: Directory renamed from 'mcp/' to 'skill_seeker_mcp/' to avoid shadowing the external mcp package
MCP_AVAILABLE = False
Server = None
Tool = None
TextContent = None

try:
    from mcp.server import Server
    from mcp.types import Tool, TextContent
    MCP_AVAILABLE = True
except ImportError as e:
    if __name__ == "__main__":
        print("❌ Error: mcp package not installed")
        print("Install with: pip install mcp")
        print(f"Import error: {e}")
        sys.exit(1)


# Initialize MCP server (only if MCP is available)
app = Server("skill-seeker") if MCP_AVAILABLE and Server is not None else None

# Path to CLI tools
CLI_DIR = Path(__file__).parent.parent / "cli"

# Helper decorator that works even when app is None
def safe_decorator(decorator_func):
    """Returns the decorator if MCP is available, otherwise returns a no-op"""
    if MCP_AVAILABLE and app is not None:
        return decorator_func
    else:
        # Return a decorator that just returns the function unchanged
        def noop_decorator(func):
            return func
        return noop_decorator


def run_subprocess_with_streaming(cmd, timeout=None):
    """
    Run subprocess with real-time output streaming.
    Returns (stdout, stderr, returncode).

    This solves the blocking issue where long-running processes (like scraping)
    would cause MCP to appear frozen. Now we stream output as it comes.
    """
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,  # Line buffered
            universal_newlines=True
        )

        stdout_lines = []
        stderr_lines = []
        start_time = time.time()

        # Read output line by line as it comes
        while True:
            # Check timeout
            if timeout and (time.time() - start_time) > timeout:
                process.kill()
                stderr_lines.append(f"\n⚠️ Process killed after {timeout}s timeout")
                break

            # Check if process finished
            if process.poll() is not None:
                break

            # Read available output (non-blocking)
            try:
                import select
                readable, _, _ = select.select([process.stdout, process.stderr], [], [], 0.1)

                if process.stdout in readable:
                    line = process.stdout.readline()
                    if line:
                        stdout_lines.append(line)

                if process.stderr in readable:
                    line = process.stderr.readline()
                    if line:
                        stderr_lines.append(line)
            except:
                # Fallback for Windows (no select)
                time.sleep(0.1)

        # Get any remaining output
        remaining_stdout, remaining_stderr = process.communicate()
        if remaining_stdout:
            stdout_lines.append(remaining_stdout)
        if remaining_stderr:
            stderr_lines.append(remaining_stderr)

        stdout = ''.join(stdout_lines)
        stderr = ''.join(stderr_lines)
        returncode = process.returncode

        return stdout, stderr, returncode

    except Exception as e:
        return "", f"Error running subprocess: {str(e)}", 1


@safe_decorator(app.list_tools() if app else lambda: lambda f: f)
async def list_tools() -> list[Tool]:
    """List available tools"""
    return [
        Tool(
            name="generate_config",
            description="Generate a config file for documentation scraping. Interactively creates a JSON config for any documentation website.",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Skill name (lowercase, alphanumeric, hyphens, underscores)",
                    },
                    "url": {
                        "type": "string",
                        "description": "Base documentation URL (must include http:// or https://)",
                    },
                    "description": {
                        "type": "string",
                        "description": "Description of when to use this skill",
                    },
                    "max_pages": {
                        "type": "integer",
                        "description": "Maximum pages to scrape (default: 100, use -1 for unlimited)",
                        "default": 100,
                    },
                    "unlimited": {
                        "type": "boolean",
                        "description": "Remove all limits - scrape all pages (default: false). Overrides max_pages.",
                        "default": False,
                    },
                    "rate_limit": {
                        "type": "number",
                        "description": "Delay between requests in seconds (default: 0.5)",
                        "default": 0.5,
                    },
                },
                "required": ["name", "url", "description"],
            },
        ),
        Tool(
            name="estimate_pages",
            description="Estimate how many pages will be scraped from a config. Fast preview without downloading content.",
            inputSchema={
                "type": "object",
                "properties": {
                    "config_path": {
                        "type": "string",
                        "description": "Path to config JSON file (e.g., configs/react.json)",
                    },
                    "max_discovery": {
                        "type": "integer",
                        "description": "Maximum pages to discover during estimation (default: 1000, use -1 for unlimited)",
                        "default": 1000,
                    },
                    "unlimited": {
                        "type": "boolean",
                        "description": "Remove discovery limit - estimate all pages (default: false). Overrides max_discovery.",
                        "default": False,
                    },
                },
                "required": ["config_path"],
            },
        ),
        Tool(
            name="scrape_docs",
            description="Scrape documentation and build Claude skill. Supports both single-source (legacy) and unified multi-source configs. Creates SKILL.md and reference files. Automatically detects llms.txt files for 10x faster processing. Falls back to HTML scraping if not available.",
            inputSchema={
                "type": "object",
                "properties": {
                    "config_path": {
                        "type": "string",
                        "description": "Path to config JSON file (e.g., configs/react.json or configs/godot_unified.json)",
                    },
                    "unlimited": {
                        "type": "boolean",
                        "description": "Remove page limit - scrape all pages (default: false). Overrides max_pages in config.",
                        "default": False,
                    },
                    "enhance_local": {
                        "type": "boolean",
                        "description": "Open terminal for local enhancement with Claude Code (default: false)",
                        "default": False,
                    },
                    "skip_scrape": {
                        "type": "boolean",
                        "description": "Skip scraping, use cached data (default: false)",
                        "default": False,
                    },
                    "dry_run": {
                        "type": "boolean",
                        "description": "Preview what will be scraped without saving (default: false)",
                        "default": False,
                    },
                    "merge_mode": {
                        "type": "string",
                        "description": "Override merge mode for unified configs: 'rule-based' or 'claude-enhanced' (default: from config)",
                    },
                },
                "required": ["config_path"],
            },
        ),
        Tool(
            name="package_skill",
            description="Package a skill directory into a .zip file ready for Claude upload. Automatically uploads if ANTHROPIC_API_KEY is set.",
            inputSchema={
                "type": "object",
                "properties": {
                    "skill_dir": {
                        "type": "string",
                        "description": "Path to skill directory (e.g., output/react/)",
                    },
                    "auto_upload": {
                        "type": "boolean",
                        "description": "Try to upload automatically if API key is available (default: true). If false, only package without upload attempt.",
                        "default": True,
                    },
                },
                "required": ["skill_dir"],
            },
        ),
        Tool(
            name="upload_skill",
            description="Upload a skill .zip file to Claude automatically (requires ANTHROPIC_API_KEY)",
            inputSchema={
                "type": "object",
                "properties": {
                    "skill_zip": {
                        "type": "string",
                        "description": "Path to skill .zip file (e.g., output/react.zip)",
                    },
                },
                "required": ["skill_zip"],
            },
        ),
        Tool(
            name="list_configs",
            description="List all available preset configurations.",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="validate_config",
            description="Validate a config file for errors.",
            inputSchema={
                "type": "object",
                "properties": {
                    "config_path": {
                        "type": "string",
                        "description": "Path to config JSON file",
                    },
                },
                "required": ["config_path"],
            },
        ),
        Tool(
            name="split_config",
            description="Split large documentation config into multiple focused skills. For 10K+ page documentation.",
            inputSchema={
                "type": "object",
                "properties": {
                    "config_path": {
                        "type": "string",
                        "description": "Path to config JSON file (e.g., configs/godot.json)",
                    },
                    "strategy": {
                        "type": "string",
                        "description": "Split strategy: auto, none, category, router, size (default: auto)",
                        "default": "auto",
                    },
                    "target_pages": {
                        "type": "integer",
                        "description": "Target pages per skill (default: 5000)",
                        "default": 5000,
                    },
                    "dry_run": {
                        "type": "boolean",
                        "description": "Preview without saving files (default: false)",
                        "default": False,
                    },
                },
                "required": ["config_path"],
            },
        ),
        Tool(
            name="generate_router",
            description="Generate router/hub skill for split documentation. Creates intelligent routing to sub-skills.",
            inputSchema={
                "type": "object",
                "properties": {
                    "config_pattern": {
                        "type": "string",
                        "description": "Config pattern for sub-skills (e.g., 'configs/godot-*.json')",
                    },
                    "router_name": {
                        "type": "string",
                        "description": "Router skill name (optional, inferred from configs)",
                    },
                },
                "required": ["config_pattern"],
            },
        ),
        Tool(
            name="scrape_pdf",
            description="Scrape PDF documentation and build Claude skill. Extracts text, code, and images from PDF files.",
            inputSchema={
                "type": "object",
                "properties": {
                    "config_path": {
                        "type": "string",
                        "description": "Path to PDF config JSON file (e.g., configs/manual_pdf.json)",
                    },
                    "pdf_path": {
                        "type": "string",
                        "description": "Direct PDF path (alternative to config_path)",
                    },
                    "name": {
                        "type": "string",
                        "description": "Skill name (required with pdf_path)",
                    },
                    "description": {
                        "type": "string",
                        "description": "Skill description (optional)",
                    },
                    "from_json": {
                        "type": "string",
                        "description": "Build from extracted JSON file (e.g., output/manual_extracted.json)",
                    },
                },
                "required": [],
            },
        ),
        Tool(
            name="scrape_github",
            description="Scrape GitHub repository and build Claude skill. Extracts README, Issues, Changelog, Releases, and code structure.",
            inputSchema={
                "type": "object",
                "properties": {
                    "repo": {
                        "type": "string",
                        "description": "GitHub repository (owner/repo, e.g., facebook/react)",
                    },
                    "config_path": {
                        "type": "string",
                        "description": "Path to GitHub config JSON file (e.g., configs/react_github.json)",
                    },
                    "name": {
                        "type": "string",
                        "description": "Skill name (default: repo name)",
                    },
                    "description": {
                        "type": "string",
                        "description": "Skill description",
                    },
                    "token": {
                        "type": "string",
                        "description": "GitHub personal access token (or use GITHUB_TOKEN env var)",
                    },
                    "no_issues": {
                        "type": "boolean",
                        "description": "Skip GitHub issues extraction (default: false)",
                        "default": False,
                    },
                    "no_changelog": {
                        "type": "boolean",
                        "description": "Skip CHANGELOG extraction (default: false)",
                        "default": False,
                    },
                    "no_releases": {
                        "type": "boolean",
                        "description": "Skip releases extraction (default: false)",
                        "default": False,
                    },
                    "max_issues": {
                        "type": "integer",
                        "description": "Maximum issues to fetch (default: 100)",
                        "default": 100,
                    },
                    "scrape_only": {
                        "type": "boolean",
                        "description": "Only scrape, don't build skill (default: false)",
                        "default": False,
                    },
                },
                "required": [],
            },
        ),
    ]


@safe_decorator(app.call_tool() if app else lambda: lambda f: f)
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls"""

    try:
        if name == "generate_config":
            return await generate_config_tool(arguments)
        elif name == "estimate_pages":
            return await estimate_pages_tool(arguments)
        elif name == "scrape_docs":
            return await scrape_docs_tool(arguments)
        elif name == "package_skill":
            return await package_skill_tool(arguments)
        elif name == "upload_skill":
            return await upload_skill_tool(arguments)
        elif name == "list_configs":
            return await list_configs_tool(arguments)
        elif name == "validate_config":
            return await validate_config_tool(arguments)
        elif name == "split_config":
            return await split_config_tool(arguments)
        elif name == "generate_router":
            return await generate_router_tool(arguments)
        elif name == "scrape_pdf":
            return await scrape_pdf_tool(arguments)
        elif name == "scrape_github":
            return await scrape_github_tool(arguments)
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]

    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def generate_config_tool(args: dict) -> list[TextContent]:
    """Generate a config file"""
    name = args["name"]
    url = args["url"]
    description = args["description"]
    max_pages = args.get("max_pages", 100)
    unlimited = args.get("unlimited", False)
    rate_limit = args.get("rate_limit", 0.5)

    # Handle unlimited mode
    if unlimited:
        max_pages = None
        limit_msg = "unlimited (no page limit)"
    elif max_pages == -1:
        max_pages = None
        limit_msg = "unlimited (no page limit)"
    else:
        limit_msg = str(max_pages)

    # Create config
    config = {
        "name": name,
        "description": description,
        "base_url": url,
        "selectors": {
            "main_content": "article",
            "title": "h1",
            "code_blocks": "pre code"
        },
        "url_patterns": {
            "include": [],
            "exclude": []
        },
        "categories": {},
        "rate_limit": rate_limit,
        "max_pages": max_pages
    }

    # Save to configs directory
    config_path = Path("configs") / f"{name}.json"
    config_path.parent.mkdir(exist_ok=True)

    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)

    result = f"""✅ Config created: {config_path}

Configuration:
  Name: {name}
  URL: {url}
  Max pages: {limit_msg}
  Rate limit: {rate_limit}s

Next steps:
  1. Review/edit config: cat {config_path}
  2. Estimate pages: Use estimate_pages tool
  3. Scrape docs: Use scrape_docs tool

Note: Default selectors may need adjustment for your documentation site.
"""

    return [TextContent(type="text", text=result)]


async def estimate_pages_tool(args: dict) -> list[TextContent]:
    """Estimate page count"""
    config_path = args["config_path"]
    max_discovery = args.get("max_discovery", 1000)
    unlimited = args.get("unlimited", False)

    # Handle unlimited mode
    if unlimited or max_discovery == -1:
        max_discovery = -1
        timeout = 1800  # 30 minutes for unlimited discovery
    else:
        # Estimate: 0.5s per page discovered
        timeout = max(300, max_discovery // 2)  # Minimum 5 minutes

    # Run estimate_pages.py
    cmd = [
        sys.executable,
        str(CLI_DIR / "estimate_pages.py"),
        config_path,
        "--max-discovery", str(max_discovery)
    ]

    progress_msg = f"🔄 Estimating page count...\n"
    progress_msg += f"⏱️ Maximum time: {timeout // 60} minutes\n\n"

    stdout, stderr, returncode = run_subprocess_with_streaming(cmd, timeout=timeout)

    output = progress_msg + stdout

    if returncode == 0:
        return [TextContent(type="text", text=output)]
    else:
        return [TextContent(type="text", text=f"{output}\n\n❌ Error:\n{stderr}")]


async def scrape_docs_tool(args: dict) -> list[TextContent]:
    """Scrape documentation - auto-detects unified vs legacy format"""
    config_path = args["config_path"]
    unlimited = args.get("unlimited", False)
    enhance_local = args.get("enhance_local", False)
    skip_scrape = args.get("skip_scrape", False)
    dry_run = args.get("dry_run", False)
    merge_mode = args.get("merge_mode")

    # Load config to detect format
    with open(config_path, 'r') as f:
        config = json.load(f)

    # Detect if unified format (has 'sources' array)
    is_unified = 'sources' in config and isinstance(config['sources'], list)

    # Handle unlimited mode by modifying config temporarily
    if unlimited:
        # Set max_pages to None (unlimited)
        if is_unified:
            # For unified configs, set max_pages on documentation sources
            for source in config.get('sources', []):
                if source.get('type') == 'documentation':
                    source['max_pages'] = None
        else:
            # For legacy configs
            config['max_pages'] = None

        # Create temporary config file
        temp_config_path = config_path.replace('.json', '_unlimited_temp.json')
        with open(temp_config_path, 'w') as f:
            json.dump(config, f, indent=2)

        config_to_use = temp_config_path
    else:
        config_to_use = config_path

    # Choose scraper based on format
    if is_unified:
        scraper_script = "unified_scraper.py"
        progress_msg = f"🔄 Starting unified multi-source scraping...\n"
        progress_msg += f"📦 Config format: Unified (multiple sources)\n"
    else:
        scraper_script = "doc_scraper.py"
        progress_msg = f"🔄 Starting scraping process...\n"
        progress_msg += f"📦 Config format: Legacy (single source)\n"

    # Build command
    cmd = [
        sys.executable,
        str(CLI_DIR / scraper_script),
        "--config", config_to_use
    ]

    # Add merge mode for unified configs
    if is_unified and merge_mode:
        cmd.extend(["--merge-mode", merge_mode])

    # Add --fresh to avoid user input prompts when existing data found
    if not skip_scrape:
        cmd.append("--fresh")

    if enhance_local:
        cmd.append("--enhance-local")
    if skip_scrape:
        cmd.append("--skip-scrape")
    if dry_run:
        cmd.append("--dry-run")

    # Determine timeout based on operation type
    if dry_run:
        timeout = 300  # 5 minutes for dry run
    elif skip_scrape:
        timeout = 600  # 10 minutes for building from cache
    elif unlimited:
        timeout = None  # No timeout for unlimited mode (user explicitly requested)
    else:
        # Read config to estimate timeout
        try:
            if is_unified:
                # For unified configs, estimate based on all sources
                total_pages = 0
                for source in config.get('sources', []):
                    if source.get('type') == 'documentation':
                        total_pages += source.get('max_pages', 500)
                max_pages = total_pages or 500
            else:
                max_pages = config.get('max_pages', 500)

            # Estimate: 30s per page + buffer
            timeout = max(3600, max_pages * 35)  # Minimum 1 hour, or 35s per page
        except:
            timeout = 14400  # Default: 4 hours

    # Add progress message
    if timeout:
        progress_msg += f"⏱️ Maximum time allowed: {timeout // 60} minutes\n"
    else:
        progress_msg += f"⏱️ Unlimited mode - no timeout\n"
    progress_msg += f"📝 Progress will be shown below:\n\n"

    # Run scraper with streaming
    stdout, stderr, returncode = run_subprocess_with_streaming(cmd, timeout=timeout)

    # Clean up temporary config
    if unlimited and Path(config_to_use).exists():
        Path(config_to_use).unlink()

    output = progress_msg + stdout

    if returncode == 0:
        return [TextContent(type="text", text=output)]
    else:
        error_output = output + f"\n\n❌ Error:\n{stderr}"
        return [TextContent(type="text", text=error_output)]


async def package_skill_tool(args: dict) -> list[TextContent]:
    """Package skill to .zip and optionally auto-upload"""
    skill_dir = args["skill_dir"]
    auto_upload = args.get("auto_upload", True)

    # Check if API key exists - only upload if available
    has_api_key = os.environ.get('ANTHROPIC_API_KEY', '').strip()
    should_upload = auto_upload and has_api_key

    # Run package_skill.py
    cmd = [
        sys.executable,
        str(CLI_DIR / "package_skill.py"),
        skill_dir,
        "--no-open",  # Don't open folder in MCP context
        "--skip-quality-check"  # Skip interactive quality checks in MCP context
    ]

    # Add upload flag only if we have API key
    if should_upload:
        cmd.append("--upload")

    # Timeout: 5 minutes for packaging + upload
    timeout = 300

    progress_msg = "📦 Packaging skill...\n"
    if should_upload:
        progress_msg += "📤 Will auto-upload if successful\n"
    progress_msg += f"⏱️ Maximum time: {timeout // 60} minutes\n\n"

    stdout, stderr, returncode = run_subprocess_with_streaming(cmd, timeout=timeout)

    output = progress_msg + stdout

    if returncode == 0:
        if should_upload:
            # Upload succeeded
            output += "\n\n✅ Skill packaged and uploaded automatically!"
            output += "\n   Your skill is now available in Claude!"
        elif auto_upload and not has_api_key:
            # User wanted upload but no API key
            output += "\n\n📝 Skill packaged successfully!"
            output += "\n"
            output += "\n💡 To enable automatic upload:"
            output += "\n   1. Get API key from https://console.anthropic.com/"
            output += "\n   2. Set: export ANTHROPIC_API_KEY=sk-ant-..."
            output += "\n"
            output += "\n📤 Manual upload:"
            output += "\n   1. Find the .zip file in your output/ folder"
            output += "\n   2. Go to https://claude.ai/skills"
            output += "\n   3. Click 'Upload Skill' and select the .zip file"
        else:
            # auto_upload=False, just packaged
            output += "\n\n✅ Skill packaged successfully!"
            output += "\n   Upload manually to https://claude.ai/skills"

        return [TextContent(type="text", text=output)]
    else:
        return [TextContent(type="text", text=f"{output}\n\n❌ Error:\n{stderr}")]


async def upload_skill_tool(args: dict) -> list[TextContent]:
    """Upload skill .zip to Claude"""
    skill_zip = args["skill_zip"]

    # Run upload_skill.py
    cmd = [
        sys.executable,
        str(CLI_DIR / "upload_skill.py"),
        skill_zip
    ]

    # Timeout: 5 minutes for upload
    timeout = 300

    progress_msg = "📤 Uploading skill to Claude...\n"
    progress_msg += f"⏱️ Maximum time: {timeout // 60} minutes\n\n"

    stdout, stderr, returncode = run_subprocess_with_streaming(cmd, timeout=timeout)

    output = progress_msg + stdout

    if returncode == 0:
        return [TextContent(type="text", text=output)]
    else:
        return [TextContent(type="text", text=f"{output}\n\n❌ Error:\n{stderr}")]


async def list_configs_tool(args: dict) -> list[TextContent]:
    """List available configs"""
    configs_dir = Path("configs")

    if not configs_dir.exists():
        return [TextContent(type="text", text="No configs directory found")]

    configs = list(configs_dir.glob("*.json"))

    if not configs:
        return [TextContent(type="text", text="No config files found")]

    result = "📋 Available Configs:\n\n"

    for config_file in sorted(configs):
        try:
            with open(config_file) as f:
                config = json.load(f)
                name = config.get("name", config_file.stem)
                desc = config.get("description", "No description")
                url = config.get("base_url", "")

                result += f"  • {config_file.name}\n"
                result += f"    Name: {name}\n"
                result += f"    URL: {url}\n"
                result += f"    Description: {desc}\n\n"
        except Exception as e:
            result += f"  • {config_file.name} - Error reading: {e}\n\n"

    return [TextContent(type="text", text=result)]


async def validate_config_tool(args: dict) -> list[TextContent]:
    """Validate a config file - supports both legacy and unified formats"""
    config_path = args["config_path"]

    # Import validation classes
    sys.path.insert(0, str(CLI_DIR))

    try:
        # Check if file exists
        if not Path(config_path).exists():
            return [TextContent(type="text", text=f"❌ Error: Config file not found: {config_path}")]

        # Try unified config validator first
        try:
            from config_validator import validate_config
            validator = validate_config(config_path)

            result = f"✅ Config is valid!\n\n"

            # Show format
            if validator.is_unified:
                result += f"📦 Format: Unified (multi-source)\n"
                result += f"  Name: {validator.config['name']}\n"
                result += f"  Sources: {len(validator.config.get('sources', []))}\n"

                # Show sources
                for i, source in enumerate(validator.config.get('sources', []), 1):
                    result += f"\n  Source {i}: {source['type']}\n"
                    if source['type'] == 'documentation':
                        result += f"    URL: {source.get('base_url', 'N/A')}\n"
                        result += f"    Max pages: {source.get('max_pages', 'Not set')}\n"
                    elif source['type'] == 'github':
                        result += f"    Repo: {source.get('repo', 'N/A')}\n"
                        result += f"    Code depth: {source.get('code_analysis_depth', 'surface')}\n"
                    elif source['type'] == 'pdf':
                        result += f"    Path: {source.get('path', 'N/A')}\n"

                # Show merge settings if applicable
                if validator.needs_api_merge():
                    merge_mode = validator.config.get('merge_mode', 'rule-based')
                    result += f"\n  Merge mode: {merge_mode}\n"
                    result += f"  API merging: Required (docs + code sources)\n"

            else:
                result += f"📦 Format: Legacy (single source)\n"
                result += f"  Name: {validator.config['name']}\n"
                result += f"  Base URL: {validator.config.get('base_url', 'N/A')}\n"
                result += f"  Max pages: {validator.config.get('max_pages', 'Not set')}\n"
                result += f"  Rate limit: {validator.config.get('rate_limit', 'Not set')}s\n"

            return [TextContent(type="text", text=result)]

        except ImportError:
            # Fall back to legacy validation
            from doc_scraper import validate_config
            import json

            with open(config_path, 'r') as f:
                config = json.load(f)

            # Validate config - returns (errors, warnings) tuple
            errors, warnings = validate_config(config)

            if errors:
                result = f"❌ Config validation failed:\n\n"
                for error in errors:
                    result += f"  • {error}\n"
            else:
                result = f"✅ Config is valid!\n\n"
                result += f"📦 Format: Legacy (single source)\n"
                result += f"  Name: {config['name']}\n"
                result += f"  Base URL: {config['base_url']}\n"
                result += f"  Max pages: {config.get('max_pages', 'Not set')}\n"
                result += f"  Rate limit: {config.get('rate_limit', 'Not set')}s\n"

                if warnings:
                    result += f"\n⚠️  Warnings:\n"
                    for warning in warnings:
                        result += f"  • {warning}\n"

            return [TextContent(type="text", text=result)]

    except Exception as e:
        return [TextContent(type="text", text=f"❌ Error: {str(e)}")]


async def split_config_tool(args: dict) -> list[TextContent]:
    """Split large config into multiple focused configs"""
    config_path = args["config_path"]
    strategy = args.get("strategy", "auto")
    target_pages = args.get("target_pages", 5000)
    dry_run = args.get("dry_run", False)

    # Run split_config.py
    cmd = [
        sys.executable,
        str(CLI_DIR / "split_config.py"),
        config_path,
        "--strategy", strategy,
        "--target-pages", str(target_pages)
    ]

    if dry_run:
        cmd.append("--dry-run")

    # Timeout: 5 minutes for config splitting
    timeout = 300

    progress_msg = "✂️ Splitting configuration...\n"
    progress_msg += f"⏱️ Maximum time: {timeout // 60} minutes\n\n"

    stdout, stderr, returncode = run_subprocess_with_streaming(cmd, timeout=timeout)

    output = progress_msg + stdout

    if returncode == 0:
        return [TextContent(type="text", text=output)]
    else:
        return [TextContent(type="text", text=f"{output}\n\n❌ Error:\n{stderr}")]


async def generate_router_tool(args: dict) -> list[TextContent]:
    """Generate router skill for split documentation"""
    import glob

    config_pattern = args["config_pattern"]
    router_name = args.get("router_name")

    # Expand glob pattern
    config_files = glob.glob(config_pattern)

    if not config_files:
        return [TextContent(type="text", text=f"❌ No config files match pattern: {config_pattern}")]

    # Run generate_router.py
    cmd = [
        sys.executable,
        str(CLI_DIR / "generate_router.py"),
    ] + config_files

    if router_name:
        cmd.extend(["--name", router_name])

    # Timeout: 5 minutes for router generation
    timeout = 300

    progress_msg = "🧭 Generating router skill...\n"
    progress_msg += f"⏱️ Maximum time: {timeout // 60} minutes\n\n"

    stdout, stderr, returncode = run_subprocess_with_streaming(cmd, timeout=timeout)

    output = progress_msg + stdout

    if returncode == 0:
        return [TextContent(type="text", text=output)]
    else:
        return [TextContent(type="text", text=f"{output}\n\n❌ Error:\n{stderr}")]


async def scrape_pdf_tool(args: dict) -> list[TextContent]:
    """Scrape PDF documentation and build skill"""
    config_path = args.get("config_path")
    pdf_path = args.get("pdf_path")
    name = args.get("name")
    description = args.get("description")
    from_json = args.get("from_json")

    # Build command
    cmd = [sys.executable, str(CLI_DIR / "pdf_scraper.py")]

    # Mode 1: Config file
    if config_path:
        cmd.extend(["--config", config_path])

    # Mode 2: Direct PDF
    elif pdf_path and name:
        cmd.extend(["--pdf", pdf_path, "--name", name])
        if description:
            cmd.extend(["--description", description])

    # Mode 3: From JSON
    elif from_json:
        cmd.extend(["--from-json", from_json])

    else:
        return [TextContent(type="text", text="❌ Error: Must specify --config, --pdf + --name, or --from-json")]

    # Run pdf_scraper.py with streaming (can take a while)
    timeout = 600  # 10 minutes for PDF extraction

    progress_msg = "📄 Scraping PDF documentation...\n"
    progress_msg += f"⏱️ Maximum time: {timeout // 60} minutes\n\n"

    stdout, stderr, returncode = run_subprocess_with_streaming(cmd, timeout=timeout)

    output = progress_msg + stdout

    if returncode == 0:
        return [TextContent(type="text", text=output)]
    else:
        return [TextContent(type="text", text=f"{output}\n\n❌ Error:\n{stderr}")]


async def scrape_github_tool(args: dict) -> list[TextContent]:
    """Scrape GitHub repository to Claude skill (C1.11)"""
    repo = args.get("repo")
    config_path = args.get("config_path")
    name = args.get("name")
    description = args.get("description")
    token = args.get("token")
    no_issues = args.get("no_issues", False)
    no_changelog = args.get("no_changelog", False)
    no_releases = args.get("no_releases", False)
    max_issues = args.get("max_issues", 100)
    scrape_only = args.get("scrape_only", False)

    # Build command
    cmd = [sys.executable, str(CLI_DIR / "github_scraper.py")]

    # Mode 1: Config file
    if config_path:
        cmd.extend(["--config", config_path])

    # Mode 2: Direct repo
    elif repo:
        cmd.extend(["--repo", repo])
        if name:
            cmd.extend(["--name", name])
        if description:
            cmd.extend(["--description", description])
        if token:
            cmd.extend(["--token", token])
        if no_issues:
            cmd.append("--no-issues")
        if no_changelog:
            cmd.append("--no-changelog")
        if no_releases:
            cmd.append("--no-releases")
        if max_issues != 100:
            cmd.extend(["--max-issues", str(max_issues)])
        if scrape_only:
            cmd.append("--scrape-only")

    else:
        return [TextContent(type="text", text="❌ Error: Must specify --repo or --config")]

    # Run github_scraper.py with streaming (can take a while)
    timeout = 600  # 10 minutes for GitHub scraping

    progress_msg = "🐙 Scraping GitHub repository...\n"
    progress_msg += f"⏱️ Maximum time: {timeout // 60} minutes\n\n"

    stdout, stderr, returncode = run_subprocess_with_streaming(cmd, timeout=timeout)

    output = progress_msg + stdout

    if returncode == 0:
        return [TextContent(type="text", text=output)]
    else:
        return [TextContent(type="text", text=f"{output}\n\n❌ Error:\n{stderr}")]


async def main():
    """Run the MCP server"""
    if not MCP_AVAILABLE or app is None:
        print("❌ Error: MCP server cannot start - MCP package not available")
        sys.exit(1)

    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
