# Complete MCP Setup Guide for Claude Code

Step-by-step guide to set up the Skill Seeker MCP server with Claude Code.

**✅ Fully Tested and Working**: All 9 MCP tools verified in production use with Claude Code
- ✅ 34 comprehensive unit tests (100% pass rate)
- ✅ Integration tested via actual Claude Code MCP protocol
- ✅ All 9 tools working with natural language commands (includes upload support!)

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Verification](#verification)
- [Usage Examples](#usage-examples)
- [Troubleshooting](#troubleshooting)
- [Advanced Configuration](#advanced-configuration)

---

## Prerequisites

### Required Software

1. **Python 3.10 or higher**
   ```bash
   python3 --version
   # Should show: Python 3.10.x or higher
   ```

2. **Claude Code installed**
   - Download from [claude.ai/code](https://claude.ai/code)
   - Requires Claude Pro or Claude Code Max subscription

3. **Skill Seeker repository cloned**
   ```bash
   git clone https://github.com/yusufkaraaslan/Skill_Seekers.git
   cd Skill_Seekers
   ```

### System Requirements

- **Operating System**: macOS, Linux, or Windows (WSL)
- **Disk Space**: 100 MB for dependencies + space for generated skills
- **Network**: Internet connection for documentation scraping

---

## Installation

### Step 1: Install Python Dependencies

```bash
# Navigate to repository root
cd /path/to/Skill_Seekers

# Install MCP server dependencies
pip3 install -r skill_seeker_mcp/requirements.txt

# Install CLI tool dependencies (for scraping)
pip3 install requests beautifulsoup4
```

**Expected output:**
```
Successfully installed mcp-0.9.0 requests-2.31.0 beautifulsoup4-4.12.3
```

### Step 2: Verify Installation

```bash
# Test MCP server can start
timeout 3 python3 skill_seeker_mcp/server.py || echo "Server OK (timeout expected)"

# Should exit cleanly or timeout (both are normal)
```

**Optional: Run Tests**

```bash
# Install test dependencies
pip3 install pytest

# Run MCP server tests (25 tests)
python3 -m pytest tests/test_mcp_server.py -v

# Expected: 25 passed in ~0.3s
```

### Step 3: Note Your Repository Path

```bash
# Get absolute path
pwd

# Example output: /Users/username/Projects/Skill_Seekers
# or: /home/username/Skill_Seekers
```

**Save this path** - you'll need it for configuration!

---

## Configuration

### Step 1: Locate Claude Code MCP Configuration

Claude Code stores MCP configuration in:

- **macOS**: `~/.config/claude-code/mcp.json`
- **Linux**: `~/.config/claude-code/mcp.json`
- **Windows (WSL)**: `~/.config/claude-code/mcp.json`

### Step 2: Create/Edit Configuration File

```bash
# Create config directory if it doesn't exist
mkdir -p ~/.config/claude-code

# Edit the configuration
nano ~/.config/claude-code/mcp.json
```

### Step 3: Add Skill Seeker MCP Server

**Full Configuration Example:**

```json
{
  "mcpServers": {
    "skill-seeker": {
      "command": "python3",
      "args": [
        "/Users/username/Projects/Skill_Seekers/skill_seeker_mcp/server.py"
      ],
      "cwd": "/Users/username/Projects/Skill_Seekers",
      "env": {}
    }
  }
}
```

**IMPORTANT:** Replace `/Users/username/Projects/Skill_Seekers` with YOUR actual repository path!

**If you already have other MCP servers:**

```json
{
  "mcpServers": {
    "existing-server": {
      "command": "node",
      "args": ["/path/to/existing/server.js"]
    },
    "skill-seeker": {
      "command": "python3",
      "args": [
        "/Users/username/Projects/Skill_Seekers/skill_seeker_mcp/server.py"
      ],
      "cwd": "/Users/username/Projects/Skill_Seekers"
    }
  }
}
```

### Step 4: Save and Restart Claude Code

1. Save the file (`Ctrl+O` in nano, then `Enter`)
2. Exit editor (`Ctrl+X` in nano)
3. **Completely restart Claude Code** (quit and reopen)

---

## Verification

### Step 1: Check MCP Server Loaded

In Claude Code, type:
```
List all available MCP tools
```

You should see 9 Skill Seeker tools:
- `generate_config`
- `estimate_pages`
- `scrape_docs`
- `package_skill`
- `upload_skill`
- `list_configs`
- `validate_config`
- `split_config`
- `generate_router`

### Step 2: Test a Simple Command

```
List all available configs
```

**Expected response:**
```
Available configurations:
1. godot - Godot Engine documentation
2. react - React framework
3. vue - Vue.js framework
4. django - Django web framework
5. fastapi - FastAPI Python framework
6. kubernetes - Kubernetes documentation
7. steam-economy-complete - Steam Economy API
```

### Step 3: Test Config Generation

```
Generate a config for Tailwind CSS at https://tailwindcss.com/docs
```

**Expected response:**
```
✅ Config created: configs/tailwind.json
```

**Verify the file exists:**
```bash
ls configs/tailwind.json
```

---

## Usage Examples

### Example 1: Generate Skill from Scratch

```
User: Generate config for Svelte docs at https://svelte.dev/docs

Claude: ✅ Config created: configs/svelte.json

User: Estimate pages for configs/svelte.json

Claude: 📊 Estimated pages: 150
        Recommended max_pages: 180

User: Scrape docs using configs/svelte.json

Claude: ✅ Skill created at output/svelte/
        Run: python3 cli/package_skill.py output/svelte/

User: Package skill at output/svelte/

Claude: ✅ Created: output/svelte.zip
        Ready to upload to Claude!
```

### Example 2: Use Existing Config

```
User: List all available configs

Claude: [Shows 7 configs]

User: Scrape docs using configs/react.json with max 50 pages

Claude: ✅ Skill created at output/react/

User: Package skill at output/react/

Claude: ✅ Created: output/react.zip
```

### Example 3: Validate Before Scraping

```
User: Validate configs/godot.json

Claude: ✅ Config is valid
        - Base URL: https://docs.godotengine.org/en/stable/
        - Max pages: 500
        - Rate limit: 0.5s
        - Categories: 3

User: Estimate pages for configs/godot.json

Claude: 📊 Estimated pages: 450
        Current max_pages (500) is sufficient

User: Scrape docs using configs/godot.json

Claude: [Scraping starts...]
```

---

## Troubleshooting

### Issue: MCP Server Not Loading

**Symptoms:**
- Skill Seeker tools don't appear in Claude Code
- No response when asking about configs

**Solutions:**

1. **Check configuration path:**
   ```bash
   cat ~/.config/claude-code/mcp.json
   ```

2. **Verify Python path:**
   ```bash
   which python3
   # Should show: /usr/bin/python3 or /usr/local/bin/python3
   ```

3. **Test server manually:**
   ```bash
   cd /path/to/Skill_Seekers
   python3 skill_seeker_mcp/server.py
   # Should start without errors
   ```

4. **Check Claude Code logs:**
   - macOS: `~/Library/Logs/Claude Code/`
   - Linux: `~/.config/claude-code/logs/`

5. **Completely restart Claude Code:**
   - Quit Claude Code (don't just close window)
   - Reopen Claude Code

### Issue: "ModuleNotFoundError: No module named 'mcp'"

**Solution:**
```bash
pip3 install -r skill_seeker_mcp/requirements.txt
```

### Issue: "Permission denied" when running server

**Solution:**
```bash
chmod +x skill_seeker_mcp/server.py
```

### Issue: Tools appear but don't work

**Symptoms:**
- Tools listed but commands fail
- "Error executing tool" messages

**Solutions:**

1. **Check working directory in config:**
   ```json
   {
     "cwd": "/FULL/PATH/TO/Skill_Seekers"
   }
   ```

2. **Verify CLI tools exist:**
   ```bash
   ls cli/doc_scraper.py
   ls cli/estimate_pages.py
   ls cli/package_skill.py
   ```

3. **Test CLI tools directly:**
   ```bash
   python3 cli/doc_scraper.py --help
   ```

### Issue: Slow or hanging operations

**Solutions:**

1. **Check rate limit in config:**
   - Default: 0.5 seconds
   - Increase if needed: 1.0 or 2.0 seconds

2. **Use smaller max_pages for testing:**
   ```
   Generate config with max_pages=20 for testing
   ```

3. **Check network connection:**
   ```bash
   curl -I https://docs.example.com
   ```

---

## Advanced Configuration

### Custom Environment Variables

```json
{
  "mcpServers": {
    "skill-seeker": {
      "command": "python3",
      "args": ["/path/to/Skill_Seekers/skill_seeker_mcp/server.py"],
      "cwd": "/path/to/Skill_Seekers",
      "env": {
        "ANTHROPIC_API_KEY": "sk-ant-...",
        "PYTHONPATH": "/custom/path"
      }
    }
  }
}
```

### Multiple Python Versions

If you have multiple Python versions:

```json
{
  "mcpServers": {
    "skill-seeker": {
      "command": "/usr/local/bin/python3.11",
      "args": ["/path/to/Skill_Seekers/skill_seeker_mcp/server.py"],
      "cwd": "/path/to/Skill_Seekers"
    }
  }
}
```

### Virtual Environment

To use a Python virtual environment:

```bash
# Create venv
cd /path/to/Skill_Seekers
python3 -m venv venv
source venv/bin/activate
pip install -r skill_seeker_mcp/requirements.txt
pip install requests beautifulsoup4
which python3
# Copy this path for config
```

```json
{
  "mcpServers": {
    "skill-seeker": {
      "command": "/path/to/Skill_Seekers/venv/bin/python3",
      "args": ["/path/to/Skill_Seekers/skill_seeker_mcp/server.py"],
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
      "args": [
        "-u",
        "/path/to/Skill_Seekers/skill_seeker_mcp/server.py"
      ],
      "cwd": "/path/to/Skill_Seekers",
      "env": {
        "DEBUG": "1"
      }
    }
  }
}
```

---

## Complete Example Configuration

**Minimal (recommended for most users):**

```json
{
  "mcpServers": {
    "skill-seeker": {
      "command": "python3",
      "args": [
        "/Users/username/Projects/Skill_Seekers/skill_seeker_mcp/server.py"
      ],
      "cwd": "/Users/username/Projects/Skill_Seekers"
    }
  }
}
```

**With API enhancement:**

```json
{
  "mcpServers": {
    "skill-seeker": {
      "command": "python3",
      "args": [
        "/Users/username/Projects/Skill_Seekers/skill_seeker_mcp/server.py"
      ],
      "cwd": "/Users/username/Projects/Skill_Seekers",
      "env": {
        "ANTHROPIC_API_KEY": "sk-ant-your-key-here"
      }
    }
  }
}
```

---

## End-to-End Workflow

### Complete Setup and First Skill

```bash
# 1. Install
cd ~/Projects
git clone https://github.com/yusufkaraaslan/Skill_Seekers.git
cd Skill_Seekers
pip3 install -r skill_seeker_mcp/requirements.txt
pip3 install requests beautifulsoup4

# 2. Configure
mkdir -p ~/.config/claude-code
cat > ~/.config/claude-code/mcp.json << 'EOF'
{
  "mcpServers": {
    "skill-seeker": {
      "command": "python3",
      "args": [
        "/Users/username/Projects/Skill_Seekers/skill_seeker_mcp/server.py"
      ],
      "cwd": "/Users/username/Projects/Skill_Seekers"
    }
  }
}
EOF
# (Replace paths with your actual paths!)

# 3. Restart Claude Code

# 4. Test in Claude Code:
```

**In Claude Code:**
```
User: List all available configs
User: Scrape docs using configs/react.json with max 50 pages
User: Package skill at output/react/
```

**Result:** `output/react.zip` ready to upload!

---

## Next Steps

After successful setup:

1. **Try preset configs:**
   - React: `scrape docs using configs/react.json`
   - Vue: `scrape docs using configs/vue.json`
   - Django: `scrape docs using configs/django.json`

2. **Create custom configs:**
   - `generate config for [framework] at [url]`

3. **Test with small limits first:**
   - Use `max_pages` parameter: `scrape docs using configs/test.json with max 20 pages`

4. **Explore enhancement:**
   - Use `--enhance-local` flag for AI-powered SKILL.md improvement

---

## Getting Help

- **Documentation**: See [mcp/README.md](../mcp/README.md)
- **Issues**: [GitHub Issues](https://github.com/yusufkaraaslan/Skill_Seekers/issues)
- **Examples**: See [.github/ISSUES_TO_CREATE.md](../.github/ISSUES_TO_CREATE.md) for test cases

---

## Quick Reference Card

```
SETUP:
1. Install dependencies: pip3 install -r skill_seeker_mcp/requirements.txt
2. Configure: ~/.config/claude-code/mcp.json
3. Restart Claude Code

VERIFY:
- "List all available configs"
- "Validate configs/react.json"

GENERATE SKILL:
1. "Generate config for [name] at [url]"
2. "Estimate pages for configs/[name].json"
3. "Scrape docs using configs/[name].json"
4. "Package skill at output/[name]/"

TROUBLESHOOTING:
- Check: cat ~/.config/claude-code/mcp.json
- Test: python3 skill_seeker_mcp/server.py
- Logs: ~/Library/Logs/Claude Code/
```

---

Happy skill creating! 🚀
