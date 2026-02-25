# Skill Seeker MCP Server

Model Context Protocol (MCP) server for Skill Seeker - enables Claude Code to generate documentation skills directly.

## What is This?

This MCP server allows Claude Code to use Skill Seeker's tools directly through natural language commands. Instead of running CLI commands manually, you can ask Claude Code to:

- Generate config files for any documentation site
- Estimate page counts before scraping
- Scrape documentation and build skills
- Package skills into `.zip` files
- List and validate configurations
- Split large documentation (10K-40K+ pages) into focused sub-skills
- Generate intelligent router/hub skills for split documentation
- **NEW:** Scrape PDF documentation and extract code/images

## Quick Start

### 1. Install Dependencies

```bash
# From repository root
pip3 install -r mcp/requirements.txt
pip3 install requests beautifulsoup4
```

### 2. Quick Setup (Automated)

```bash
# Run the setup script
./setup_mcp.sh

# Follow the prompts - it will:
# - Install dependencies
# - Test the server
# - Generate configuration
# - Guide you through Claude Code setup
```

### 3. Manual Setup

Add to `~/.config/claude-code/mcp.json`:

```json
{
  "mcpServers": {
    "skill-seeker": {
      "command": "python3",
      "args": [
        "/path/to/Skill_Seekers/mcp/server.py"
      ],
      "cwd": "/path/to/Skill_Seekers"
    }
  }
}
```

**Replace `/path/to/Skill_Seekers`** with your actual repository path!

### 4. Restart Claude Code

Quit and reopen Claude Code (don't just close the window).

### 5. Test

In Claude Code, type:
```
List all available configs
```

You should see a list of preset configurations (Godot, React, Vue, etc.).

## Available Tools

The MCP server exposes 10 tools:

### 1. `generate_config`
Create a new configuration file for any documentation website.

**Parameters:**
- `name` (required): Skill name (e.g., "tailwind")
- `url` (required): Documentation URL (e.g., "https://tailwindcss.com/docs")
- `description` (required): When to use this skill
- `max_pages` (optional): Maximum pages to scrape (default: 100)
- `rate_limit` (optional): Delay between requests in seconds (default: 0.5)

**Example:**
```
Generate config for Tailwind CSS at https://tailwindcss.com/docs
```

### 2. `estimate_pages`
Estimate how many pages will be scraped from a config (fast, no data downloaded).

**Parameters:**
- `config_path` (required): Path to config file (e.g., "configs/react.json")
- `max_discovery` (optional): Maximum pages to discover (default: 1000)

**Example:**
```
Estimate pages for configs/react.json
```

### 3. `scrape_docs`
Scrape documentation and build Claude skill.

**Parameters:**
- `config_path` (required): Path to config file
- `enhance_local` (optional): Open terminal for local enhancement (default: false)
- `skip_scrape` (optional): Use cached data (default: false)
- `dry_run` (optional): Preview without saving (default: false)

**Example:**
```
Scrape docs using configs/react.json
```

### 4. `package_skill`
Package a skill directory into a `.zip` file ready for Claude upload. Automatically uploads if ANTHROPIC_API_KEY is set.

**Parameters:**
- `skill_dir` (required): Path to skill directory (e.g., "output/react/")
- `auto_upload` (optional): Try to upload automatically if API key is available (default: true)

**Example:**
```
Package skill at output/react/
```

### 5. `upload_skill`
Upload a skill .zip file to Claude automatically (requires ANTHROPIC_API_KEY).

**Parameters:**
- `skill_zip` (required): Path to skill .zip file (e.g., "output/react.zip")

**Example:**
```
Upload output/react.zip using upload_skill
```

### 6. `list_configs`
List all available preset configurations.

**Parameters:** None

**Example:**
```
List all available configs
```

### 7. `validate_config`
Validate a config file for errors.

**Parameters:**
- `config_path` (required): Path to config file

**Example:**
```
Validate configs/godot.json
```

### 8. `split_config`
Split large documentation config into multiple focused skills. For 10K+ page documentation.

**Parameters:**
- `config_path` (required): Path to config JSON file (e.g., "configs/godot.json")
- `strategy` (optional): Split strategy - "auto", "none", "category", "router", "size" (default: "auto")
- `target_pages` (optional): Target pages per skill (default: 5000)
- `dry_run` (optional): Preview without saving files (default: false)

**Example:**
```
Split configs/godot.json using router strategy with 5000 pages per skill
```

**Strategies:**
- **auto** - Intelligently detects best strategy based on page count and config
- **category** - Split by documentation categories (creates focused sub-skills)
- **router** - Create router/hub skill + specialized sub-skills (RECOMMENDED for 10K+ pages)
- **size** - Split every N pages (for docs without clear categories)

### 9. `generate_router`
Generate router/hub skill for split documentation. Creates intelligent routing to sub-skills.

**Parameters:**
- `config_pattern` (required): Config pattern for sub-skills (e.g., "configs/godot-*.json")
- `router_name` (optional): Router skill name (inferred from configs if not provided)

**Example:**
```
Generate router for configs/godot-*.json
```

**What it does:**
- Analyzes all sub-skill configs
- Extracts routing keywords from categories and names
- Creates router SKILL.md with intelligent routing logic
- Users can ask questions naturally, router directs to appropriate sub-skill

### 10. `scrape_pdf`
Scrape PDF documentation and build Claude skill. Extracts text, code blocks, images, and tables from PDF files with advanced features.

**Parameters:**
- `config_path` (optional): Path to PDF config JSON file (e.g., "configs/manual_pdf.json")
- `pdf_path` (optional): Direct PDF path (alternative to config_path)
- `name` (optional): Skill name (required with pdf_path)
- `description` (optional): Skill description
- `from_json` (optional): Build from extracted JSON file (e.g., "output/manual_extracted.json")
- `use_ocr` (optional): Use OCR for scanned PDFs (requires pytesseract)
- `password` (optional): Password for encrypted PDFs
- `extract_tables` (optional): Extract tables from PDF
- `parallel` (optional): Process pages in parallel for faster extraction
- `max_workers` (optional): Number of parallel workers (default: CPU count)

**Examples:**
```
Scrape PDF at docs/manual.pdf and create skill named api-docs
Create skill from configs/example_pdf.json
Build skill from output/manual_extracted.json
Scrape scanned PDF with OCR: --pdf docs/scanned.pdf --ocr
Scrape encrypted PDF: --pdf docs/manual.pdf --password mypassword
Extract tables: --pdf docs/data.pdf --extract-tables
Fast parallel processing: --pdf docs/large.pdf --parallel --workers 8
```

**What it does:**
- Extracts text and markdown from PDF pages
- Detects code blocks using 3 methods (font, indent, pattern)
- Detects programming language with confidence scoring (19+ languages)
- Validates syntax and scores code quality (0-10 scale)
- Extracts images with size filtering
- **NEW:** Extracts tables from PDFs (Priority 2)
- **NEW:** OCR support for scanned PDFs (Priority 2, requires pytesseract + Pillow)
- **NEW:** Password-protected PDF support (Priority 2)
- **NEW:** Parallel page processing for faster extraction (Priority 3)
- **NEW:** Intelligent caching of expensive operations (Priority 3)
- Detects chapters and creates page chunks
- Categorizes content automatically
- Generates complete skill structure (SKILL.md + references)

**Performance:**
- Sequential: ~30-60 seconds per 100 pages
- Parallel (8 workers): ~10-20 seconds per 100 pages (3x faster)

**See:** `docs/PDF_SCRAPER.md` for complete PDF documentation guide

## Example Workflows

### Generate a New Skill from Scratch

```
User: Generate config for Svelte at https://svelte.dev/docs

Claude: ✅ Config created: configs/svelte.json

User: Estimate pages for configs/svelte.json

Claude: 📊 Estimated pages: 150

User: Scrape docs using configs/svelte.json

Claude: ✅ Skill created at output/svelte/

User: Package skill at output/svelte/

Claude: ✅ Created: output/svelte.zip
      Ready to upload to Claude!
```

### Use Existing Preset

```
User: List all available configs

Claude: [Shows all configs: godot, react, vue, django, fastapi, etc.]

User: Scrape docs using configs/react.json

Claude: ✅ Skill created at output/react/

User: Package skill at output/react/

Claude: ✅ Created: output/react.zip
```

### Validate Before Scraping

```
User: Validate configs/godot.json

Claude: ✅ Config is valid!
        Name: godot
        Base URL: https://docs.godotengine.org/en/stable/
        Max pages: 500
        Rate limit: 0.5s

User: Scrape docs using configs/godot.json

Claude: [Starts scraping...]
```

### PDF Documentation - NEW

```
User: Scrape PDF at docs/api-manual.pdf and create skill named api-docs

Claude: 📄 Scraping PDF documentation...
        ✅ Extracted 120 pages
        ✅ Found 45 code blocks (Python, JavaScript, C++)
        ✅ Extracted 12 images
        ✅ Created skill at output/api-docs/
        📦 Package with: python3 cli/package_skill.py output/api-docs/

User: Package skill at output/api-docs/

Claude: ✅ Created: output/api-docs.zip
        Ready to upload to Claude!
```

### Large Documentation (40K Pages)

```
User: Estimate pages for configs/godot.json

Claude: 📊 Estimated pages: 40,000
        ⚠️  Large documentation detected!
        💡 Recommend splitting into multiple skills

User: Split configs/godot.json using router strategy

Claude: ✅ Split complete!
        Created 5 sub-skills:
        - godot-scripting.json (5,000 pages)
        - godot-2d.json (8,000 pages)
        - godot-3d.json (10,000 pages)
        - godot-physics.json (6,000 pages)
        - godot-shaders.json (11,000 pages)

User: Scrape all godot sub-skills in parallel

Claude: [Starts scraping all 5 configs in parallel...]
        ✅ All skills created in 4-8 hours instead of 20-40!

User: Generate router for configs/godot-*.json

Claude: ✅ Router skill created at output/godot/
        Routing logic:
        - "scripting", "gdscript" → godot-scripting
        - "2d", "sprites", "tilemap" → godot-2d
        - "3d", "meshes", "camera" → godot-3d
        - "physics", "collision" → godot-physics
        - "shaders", "visual shader" → godot-shaders

User: Package all godot skills

Claude: ✅ 6 skills packaged:
        - godot.zip (router)
        - godot-scripting.zip
        - godot-2d.zip
        - godot-3d.zip
        - godot-physics.zip
        - godot-shaders.zip

        Upload all to Claude!
        Users just ask questions naturally - router handles routing!
```

## Architecture

### Server Structure

```
mcp/
├── server.py           # Main MCP server
├── requirements.txt    # MCP dependencies
└── README.md          # This file
```

### How It Works

1. **Claude Code** sends MCP requests to the server
2. **Server** routes requests to appropriate tool functions
3. **Tools** call CLI scripts (`doc_scraper.py`, `estimate_pages.py`, etc.)
4. **CLI scripts** perform actual work (scraping, packaging, etc.)
5. **Results** returned to Claude Code via MCP protocol

### Tool Implementation

Each tool is implemented as an async function:

```python
async def generate_config_tool(args: dict) -> list[TextContent]:
    """Generate a config file"""
    # Create config JSON
    # Save to configs/
    # Return success message
```

Tools use `subprocess.run()` to call CLI scripts:

```python
result = subprocess.run([
    sys.executable,
    str(CLI_DIR / "doc_scraper.py"),
    "--config", config_path
], capture_output=True, text=True)
```

## Testing

The MCP server has comprehensive test coverage:

```bash
# Run MCP server tests (25 tests)
python3 -m pytest tests/test_mcp_server.py -v

# Expected output: 25 passed in ~0.3s
```

### Test Coverage

- **Server initialization** (2 tests)
- **Tool listing** (2 tests)
- **generate_config** (3 tests)
- **estimate_pages** (3 tests)
- **scrape_docs** (4 tests)
- **package_skill** (3 tests)
- **upload_skill** (2 tests)
- **list_configs** (3 tests)
- **validate_config** (3 tests)
- **split_config** (3 tests)
- **generate_router** (3 tests)
- **Tool routing** (2 tests)
- **Integration** (1 test)

**Total: 34 tests | Pass rate: 100%**

## Troubleshooting

### MCP Server Not Loading

**Symptoms:**
- Tools don't appear in Claude Code
- No response to skill-seeker commands

**Solutions:**

1. Check configuration:
   ```bash
   cat ~/.config/claude-code/mcp.json
   ```

2. Verify server can start:
   ```bash
   python3 mcp/server.py
   # Should start without errors (Ctrl+C to exit)
   ```

3. Check dependencies:
   ```bash
   pip3 install -r mcp/requirements.txt
   ```

4. Completely restart Claude Code (quit and reopen)

5. Check Claude Code logs:
   - macOS: `~/Library/Logs/Claude Code/`
   - Linux: `~/.config/claude-code/logs/`

### "ModuleNotFoundError: No module named 'mcp'"

```bash
pip3 install -r mcp/requirements.txt
```

### Tools Appear But Don't Work

**Solutions:**

1. Verify `cwd` in config points to repository root
2. Check CLI tools exist:
   ```bash
   ls cli/doc_scraper.py
   ls cli/estimate_pages.py
   ls cli/package_skill.py
   ```

3. Test CLI tools directly:
   ```bash
   python3 cli/doc_scraper.py --help
   ```

### Slow Operations

1. Check rate limit in configs (increase if needed)
2. Use smaller `max_pages` for testing
3. Use `skip_scrape` to avoid re-downloading data

## Advanced Configuration

### Using Virtual Environment

```bash
# Create venv
python3 -m venv venv
source venv/bin/activate
pip install -r mcp/requirements.txt
pip install requests beautifulsoup4
which python3  # Copy this path
```

Configure Claude Code to use venv Python:

```json
{
  "mcpServers": {
    "skill-seeker": {
      "command": "/path/to/Skill_Seekers/venv/bin/python3",
      "args": ["/path/to/Skill_Seekers/mcp/server.py"],
      "cwd": "/path/to/Skill_Seekers"
    }
  }
}
```

### Debug Mode

Enable verbose logging:

```json
{
  "mcpServers": {
    "skill-seeker": {
      "command": "python3",
      "args": ["-u", "/path/to/Skill_Seekers/mcp/server.py"],
      "cwd": "/path/to/Skill_Seekers",
      "env": {
        "DEBUG": "1"
      }
    }
  }
}
```

### With API Enhancement

For API-based enhancement (requires Anthropic API key):

```json
{
  "mcpServers": {
    "skill-seeker": {
      "command": "python3",
      "args": ["/path/to/Skill_Seekers/mcp/server.py"],
      "cwd": "/path/to/Skill_Seekers",
      "env": {
        "ANTHROPIC_API_KEY": "sk-ant-your-key-here"
      }
    }
  }
}
```

## Performance

| Operation | Time | Notes |
|-----------|------|-------|
| List configs | <1s | Instant |
| Generate config | <1s | Creates JSON file |
| Validate config | <1s | Quick validation |
| Estimate pages | 1-2min | Fast, no data download |
| Split config | 1-3min | Analyzes and creates sub-configs |
| Generate router | 10-30s | Creates router SKILL.md |
| Scrape docs | 15-45min | First time only |
| Scrape docs (40K pages) | 20-40hrs | Sequential |
| Scrape docs (40K pages, parallel) | 4-8hrs | 5 skills in parallel |
| Scrape (cached) | <1min | With `skip_scrape` |
| Package skill | 5-10s | Creates .zip |
| Package multi | 30-60s | Packages 5-10 skills |

## Documentation

- **Full Setup Guide**: [docs/MCP_SETUP.md](../docs/MCP_SETUP.md)
- **Main README**: [README.md](../README.md)
- **Usage Guide**: [docs/USAGE.md](../docs/USAGE.md)
- **Testing Guide**: [docs/TESTING.md](../docs/TESTING.md)

## Support

- **Issues**: [GitHub Issues](https://github.com/yusufkaraaslan/Skill_Seekers/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yusufkaraaslan/Skill_Seekers/discussions)

## License

MIT License - See [LICENSE](../LICENSE) for details
