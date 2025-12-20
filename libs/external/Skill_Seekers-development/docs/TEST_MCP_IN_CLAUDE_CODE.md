# Testing MCP Server in Claude Code

This guide shows you how to test the Skill Seeker MCP server **through actual Claude Code** using the MCP protocol (not just Python function calls).

## Important: What We Tested vs What You Need to Test

### What I Tested (Python Direct Calls) ✅
I tested the MCP server **functions** by calling them directly with Python:
```python
await server.list_configs_tool({})
await server.generate_config_tool({...})
```

This verified the **code works**, but didn't test the **MCP protocol integration**.

### What You Need to Test (Actual MCP Protocol) 🎯
You need to test via **Claude Code** using the MCP protocol:
```
In Claude Code:
> List all available configs
> mcp__skill-seeker__list_configs
```

This verifies the **full integration** works.

## Setup Instructions

### Step 1: Configure Claude Code

Create the MCP configuration file:

```bash
# Create config directory
mkdir -p ~/.config/claude-code

# Create/edit MCP configuration
nano ~/.config/claude-code/mcp.json
```

Add this configuration (replace `/path/to/` with your actual path):

```json
{
  "mcpServers": {
    "skill-seeker": {
      "command": "python3",
      "args": [
        "/mnt/1ece809a-2821-4f10-aecb-fcdf34760c0b/Git/Skill_Seekers/skill_seeker_mcp/server.py"
      ],
      "cwd": "/mnt/1ece809a-2821-4f10-aecb-fcdf34760c0b/Git/Skill_Seekers"
    }
  }
}
```

Or use the setup script:
```bash
./setup_mcp.sh
```

### Step 2: Restart Claude Code

**IMPORTANT:** Completely quit and restart Claude Code (don't just close the window).

### Step 3: Verify MCP Server Loaded

In Claude Code, check if the server loaded:

```
Show me all available MCP tools
```

You should see 6 tools with the prefix `mcp__skill-seeker__`:
- `mcp__skill-seeker__list_configs`
- `mcp__skill-seeker__generate_config`
- `mcp__skill-seeker__validate_config`
- `mcp__skill-seeker__estimate_pages`
- `mcp__skill-seeker__scrape_docs`
- `mcp__skill-seeker__package_skill`

## Testing All 6 MCP Tools

### Test 1: list_configs

**In Claude Code, type:**
```
List all available Skill Seeker configs
```

**Or explicitly:**
```
Use mcp__skill-seeker__list_configs
```

**Expected Output:**
```
📋 Available Configs:

  • django.json
  • fastapi.json
  • godot.json
  • react.json
  • vue.json
  ...
```

### Test 2: generate_config

**In Claude Code, type:**
```
Generate a config for Astro documentation at https://docs.astro.build with max 15 pages
```

**Or explicitly:**
```
Use mcp__skill-seeker__generate_config with:
- name: astro-test
- url: https://docs.astro.build
- description: Astro framework testing
- max_pages: 15
```

**Expected Output:**
```
✅ Config created: configs/astro-test.json
```

### Test 3: validate_config

**In Claude Code, type:**
```
Validate the astro-test config
```

**Or explicitly:**
```
Use mcp__skill-seeker__validate_config for configs/astro-test.json
```

**Expected Output:**
```
✅ Config is valid!
  Name: astro-test
  Base URL: https://docs.astro.build
  Max pages: 15
```

### Test 4: estimate_pages

**In Claude Code, type:**
```
Estimate pages for the astro-test config
```

**Or explicitly:**
```
Use mcp__skill-seeker__estimate_pages for configs/astro-test.json
```

**Expected Output:**
```
📊 ESTIMATION RESULTS
Estimated Total: ~25 pages
Recommended max_pages: 75
```

### Test 5: scrape_docs

**In Claude Code, type:**
```
Scrape docs using the astro-test config
```

**Or explicitly:**
```
Use mcp__skill-seeker__scrape_docs with configs/astro-test.json
```

**Expected Output:**
```
✅ Skill built: output/astro-test/
Scraped X pages
Created Y categories
```

### Test 6: package_skill

**In Claude Code, type:**
```
Package the astro-test skill
```

**Or explicitly:**
```
Use mcp__skill-seeker__package_skill for output/astro-test/
```

**Expected Output:**
```
✅ Package created: output/astro-test.zip
Size: X KB
```

## Complete Workflow Test

Test the entire workflow in Claude Code with natural language:

```
Step 1:
> List all available configs

Step 2:
> Generate config for Svelte at https://svelte.dev/docs with description "Svelte framework" and max 20 pages

Step 3:
> Validate configs/svelte.json

Step 4:
> Estimate pages for configs/svelte.json

Step 5:
> Scrape docs using configs/svelte.json

Step 6:
> Package skill at output/svelte/
```

Expected result: `output/svelte.zip` ready to upload to Claude!

## Troubleshooting

### Issue: Tools Not Appearing

**Symptoms:**
- Claude Code doesn't recognize skill-seeker commands
- No `mcp__skill-seeker__` tools listed

**Solutions:**

1. Check configuration exists:
   ```bash
   cat ~/.config/claude-code/mcp.json
   ```

2. Verify server can start:
   ```bash
   cd /path/to/Skill_Seekers
   python3 skill_seeker_mcp/server.py
   # Should start without errors (Ctrl+C to exit)
   ```

3. Check dependencies installed:
   ```bash
   pip3 list | grep mcp
   # Should show: mcp x.x.x
   ```

4. Completely restart Claude Code (quit and reopen)

5. Check Claude Code logs:
   - macOS: `~/Library/Logs/Claude Code/`
   - Linux: `~/.config/claude-code/logs/`

### Issue: "Permission Denied"

```bash
chmod +x skill_seeker_mcp/server.py
```

### Issue: "Module Not Found"

```bash
pip3 install -r skill_seeker_mcp/requirements.txt
pip3 install requests beautifulsoup4
```

## Verification Checklist

Use this checklist to verify MCP integration:

- [ ] Configuration file created at `~/.config/claude-code/mcp.json`
- [ ] Repository path in config is absolute and correct
- [ ] Python dependencies installed (`mcp`, `requests`, `beautifulsoup4`)
- [ ] Server starts without errors when run manually
- [ ] Claude Code completely restarted (quit and reopened)
- [ ] Tools appear when asking "show me all MCP tools"
- [ ] Tools have `mcp__skill-seeker__` prefix
- [ ] Can list configs successfully
- [ ] Can generate a test config
- [ ] Can scrape and package a small skill

## What Makes This Different from My Tests

| What I Tested | What You Should Test |
|---------------|---------------------|
| Python function calls | Claude Code MCP protocol |
| `await server.list_configs_tool({})` | Natural language in Claude Code |
| Direct Python imports | Full MCP server integration |
| Validates code works | Validates Claude Code integration |
| Quick unit testing | Real-world usage testing |

## Success Criteria

✅ **MCP Integration is Working When:**

1. You can ask Claude Code to "list all available configs"
2. Claude Code responds with the actual config list
3. You can generate, validate, scrape, and package skills
4. All through natural language commands in Claude Code
5. No Python code needed - just conversation!

## Next Steps After Successful Testing

Once MCP integration works:

1. **Create your first skill:**
   ```
   > Generate config for TailwindCSS at https://tailwindcss.com/docs
   > Scrape docs using configs/tailwind.json
   > Package skill at output/tailwind/
   ```

2. **Upload to Claude:**
   - Take the generated `.zip` file
   - Upload to Claude.ai
   - Start using your new skill!

3. **Share feedback:**
   - Report any issues on GitHub
   - Share successful skills created
   - Suggest improvements

## Reference

- **Full Setup Guide:** [docs/MCP_SETUP.md](docs/MCP_SETUP.md)
- **MCP Documentation:** [mcp/README.md](mcp/README.md)
- **Main README:** [README.md](README.md)
- **Setup Script:** `./setup_mcp.sh`

---

**Important:** This document is for testing the **actual MCP protocol integration** with Claude Code, not just the Python functions. Make sure you're testing through Claude Code's UI, not Python scripts!
