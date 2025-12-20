# Troubleshooting Guide

Common issues and solutions when using Skill Seeker.

---

## Installation Issues

### Python Not Found

**Error:**
```
python3: command not found
```

**Solutions:**
1. **Check if Python is installed:**
   ```bash
   which python3
   python --version  # Try without the 3
   ```

2. **Install Python:**
   - **macOS:** `brew install python3`
   - **Linux:** `sudo apt install python3 python3-pip`
   - **Windows:** Download from python.org, check "Add to PATH"

3. **Use python instead of python3:**
   ```bash
   python cli/doc_scraper.py --help
   ```

### Module Not Found

**Error:**
```
ModuleNotFoundError: No module named 'requests'
ModuleNotFoundError: No module named 'bs4'
ModuleNotFoundError: No module named 'mcp'
```

**Solutions:**
1. **Install dependencies:**
   ```bash
   pip3 install requests beautifulsoup4
   pip3 install -r mcp/requirements.txt  # For MCP
   ```

2. **Use --user flag if permission denied:**
   ```bash
   pip3 install --user requests beautifulsoup4
   ```

3. **Check pip is working:**
   ```bash
   pip3 --version
   ```

### Permission Denied

**Error:**
```
Permission denied: '/usr/local/lib/python3.x/...'
```

**Solutions:**
1. **Use --user flag:**
   ```bash
   pip3 install --user requests beautifulsoup4
   ```

2. **Use sudo (not recommended):**
   ```bash
   sudo pip3 install requests beautifulsoup4
   ```

3. **Use virtual environment (best practice):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install requests beautifulsoup4
   ```

---

## Runtime Issues

### File Not Found

**Error:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'cli/doc_scraper.py'
```

**Solutions:**
1. **Check you're in the Skill_Seekers directory:**
   ```bash
   pwd
   # Should show: .../Skill_Seekers

   ls
   # Should show: README.md, cli/, mcp/, configs/
   ```

2. **Change to the correct directory:**
   ```bash
   cd ~/Projects/Skill_Seekers  # Adjust path
   ```

### Config File Not Found

**Error:**
```
FileNotFoundError: configs/react.json
```

**Solutions:**
1. **Check config exists:**
   ```bash
   ls configs/
   # Should show: godot.json, react.json, vue.json, etc.
   ```

2. **Use full path:**
   ```bash
   skill-seekers scrape --config $(pwd)/configs/react.json
   ```

3. **Create missing config:**
   ```bash
   skill-seekers scrape --interactive
   ```

---

## MCP Setup Issues

### MCP Server Not Loading

**Symptoms:**
- Tools don't appear in Claude Code
- "List all available configs" doesn't work

**Solutions:**

1. **Check configuration file:**
   ```bash
   cat ~/.config/claude-code/mcp.json
   ```

2. **Verify paths are ABSOLUTE (not placeholders):**
   ```json
   {
     "mcpServers": {
       "skill-seeker": {
         "args": [
           "/Users/yourname/Projects/Skill_Seekers/mcp/server.py"
         ]
       }
     }
   }
   ```
   ❌ **Bad:** `$REPO_PATH` or `/path/to/Skill_Seekers`
   ✅ **Good:** `/Users/john/Projects/Skill_Seekers`

3. **Test server manually:**
   ```bash
   cd ~/Projects/Skill_Seekers
   python3 mcp/server.py
   # Should start without errors (Ctrl+C to stop)
   ```

4. **Re-run setup script:**
   ```bash
   ./setup_mcp.sh
   # Select "y" for auto-configure
   ```

5. **RESTART Claude Code completely:**
   - Quit (don't just close window)
   - Reopen

### Placeholder Paths in Config

**Problem:** Config has `$REPO_PATH` or `/Users/username/` instead of real paths

**Solution:**
```bash
# Get your actual path
cd ~/Projects/Skill_Seekers
pwd
# Copy this path

# Edit config
nano ~/.config/claude-code/mcp.json

# Replace ALL instances of placeholders with your actual path
# Save (Ctrl+O, Enter, Ctrl+X)

# Restart Claude Code
```

### Tools Appear But Don't Work

**Symptoms:**
- Tools listed but commands fail
- "Error executing tool" messages

**Solutions:**

1. **Check working directory:**
   ```json
   {
     "cwd": "/FULL/PATH/TO/Skill_Seekers"
   }
   ```

2. **Verify files exist:**
   ```bash
   ls cli/doc_scraper.py
   ls mcp/server.py
   ```

3. **Test CLI tools directly:**
   ```bash
   skill-seekers scrape --help
   ```

---

## Scraping Issues

### Slow or Hanging

**Solutions:**

1. **Check network connection:**
   ```bash
   ping google.com
   curl -I https://docs.yoursite.com
   ```

2. **Use smaller max_pages for testing:**
   ```bash
   skill-seekers scrape --config configs/test.json --max-pages 5
   ```

3. **Increase rate_limit in config:**
   ```json
   {
     "rate_limit": 1.0  // Increase from 0.5
   }
   ```

### No Content Extracted

**Problem:** Pages scraped but content is empty

**Solutions:**

1. **Check selector in config:**
   ```bash
   # Test with browser dev tools
   # Look for: article, main, div[role="main"], div.content
   ```

2. **Verify website is accessible:**
   ```bash
   curl https://docs.example.com
   ```

3. **Try different selectors:**
   ```json
   {
     "selectors": {
       "main_content": "article"  // Try: main, div.content, etc.
     }
   }
   ```

### Rate Limiting / 429 Errors

**Error:**
```
HTTP Error 429: Too Many Requests
```

**Solutions:**

1. **Increase rate_limit:**
   ```json
   {
     "rate_limit": 2.0  // Wait 2 seconds between requests
   }
   ```

2. **Reduce max_pages:**
   ```json
   {
     "max_pages": 50  // Scrape fewer pages
   }
   ```

3. **Try again later:**
   ```bash
   # Wait an hour and retry
   ```

---

## Platform-Specific Issues

### macOS

**Issue:** Can't run `./setup_mcp.sh`

**Solution:**
```bash
chmod +x setup_mcp.sh
./setup_mcp.sh
```

**Issue:** Homebrew not installed

**Solution:**
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Linux

**Issue:** pip3 not found

**Solution:**
```bash
sudo apt update
sudo apt install python3-pip
```

**Issue:** Permission errors

**Solution:**
```bash
# Use --user flag
pip3 install --user requests beautifulsoup4
```

### Windows (WSL)

**Issue:** Python not in PATH

**Solution:**
1. Reinstall Python
2. Check "Add Python to PATH"
3. Or add manually to PATH

**Issue:** Line ending errors

**Solution:**
```bash
dos2unix setup_mcp.sh
./setup_mcp.sh
```

---

## Verification Commands

Use these to check your setup:

```bash
# 1. Check Python
python3 --version  # Should be 3.10+

# 2. Check dependencies
pip3 list | grep requests
pip3 list | grep beautifulsoup4
pip3 list | grep mcp

# 3. Check files exist
ls cli/doc_scraper.py
ls mcp/server.py
ls configs/

# 4. Check MCP config
cat ~/.config/claude-code/mcp.json

# 5. Test scraper
skill-seekers scrape --help

# 6. Test MCP server
timeout 3 python3 mcp/server.py || echo "Server OK"

# 7. Check git repo
git status
git log --oneline -5
```

---

## Getting Help

If none of these solutions work:

1. **Check existing issues:**
   https://github.com/yusufkaraaslan/Skill_Seekers/issues

2. **Open a new issue with:**
   - Your OS (macOS 13, Ubuntu 22.04, etc.)
   - Python version (`python3 --version`)
   - Full error message
   - What command you ran
   - Output of verification commands above

3. **Include this debug info:**
   ```bash
   # System info
   uname -a
   python3 --version
   pip3 --version

   # Skill Seeker info
   cd ~/Projects/Skill_Seekers  # Your path
   pwd
   git log --oneline -1
   ls -la cli/ mcp/ configs/

   # MCP config (if using MCP)
   cat ~/.config/claude-code/mcp.json
   ```

---

## Quick Fixes Checklist

- [ ] In the Skill_Seekers directory? (`pwd`)
- [ ] Python 3.10+ installed? (`python3 --version`)
- [ ] Dependencies installed? (`pip3 list | grep requests`)
- [ ] Config file exists? (`ls configs/yourconfig.json`)
- [ ] Internet connection working? (`ping google.com`)
- [ ] For MCP: Config uses absolute paths? (not `$REPO_PATH`)
- [ ] For MCP: Claude Code restarted? (quit and reopen)

---

**Still stuck?** Open an issue: https://github.com/yusufkaraaslan/Skill_Seekers/issues/new
