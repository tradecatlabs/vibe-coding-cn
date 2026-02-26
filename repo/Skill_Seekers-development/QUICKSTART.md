# Quick Start Guide

## 🚀 3 Steps to Create a Skill

### Step 1: Install Dependencies

```bash
pip3 install requests beautifulsoup4
```

> **Note:** Skill_Seekers automatically checks for llms.txt files first, which is 10x faster when available.

### Step 2: Run the Tool

**Option A: Use a Preset (Easiest)**
```bash
skill-seekers scrape --config configs/godot.json
```

**Option B: Interactive Mode**
```bash
skill-seekers scrape --interactive
```

**Option C: Quick Command**
```bash
skill-seekers scrape --name react --url https://react.dev/
```

**Option D: Unified Multi-Source (NEW - v2.0.0)**
```bash
# Combine documentation + GitHub code in one skill
skill-seekers unified --config configs/react_unified.json
```
*Detects conflicts between docs and code automatically!*

### Step 3: Enhance SKILL.md (Recommended)

```bash
# LOCAL enhancement (no API key, uses Claude Code Max)
skill-seekers enhance output/godot/
```

**This takes 60 seconds and dramatically improves the SKILL.md quality!**

### Step 4: Package the Skill

```bash
skill-seekers package output/godot/
```

**Done!** You now have `godot.zip` ready to use.

---

## 📋 Available Presets

```bash
# Godot Engine
skill-seekers scrape --config configs/godot.json

# React
skill-seekers scrape --config configs/react.json

# Vue.js
skill-seekers scrape --config configs/vue.json

# Django
skill-seekers scrape --config configs/django.json

# FastAPI
skill-seekers scrape --config configs/fastapi.json

# Unified Multi-Source (NEW!)
skill-seekers unified --config configs/react_unified.json
skill-seekers unified --config configs/django_unified.json
skill-seekers unified --config configs/fastapi_unified.json
skill-seekers unified --config configs/godot_unified.json
```

---

## ⚡ Using Existing Data (Fast!)

If you already scraped once:

```bash
skill-seekers scrape --config configs/godot.json

# When prompted:
✓ Found existing data: 245 pages
Use existing data? (y/n): y

# Builds in seconds!
```

Or use `--skip-scrape`:
```bash
skill-seekers scrape --config configs/godot.json --skip-scrape
```

---

## 🎯 Complete Example (Recommended Workflow)

```bash
# 1. Install (once)
pip3 install requests beautifulsoup4

# 2. Scrape React docs with LOCAL enhancement
skill-seekers scrape --config configs/react.json --enhance-local
# Wait 15-30 minutes (scraping) + 60 seconds (enhancement)

# 3. Package
skill-seekers package output/react/

# 4. Use react.zip in Claude!
```

**Alternative: Enhancement after scraping**
```bash
# 2a. Scrape only (no enhancement)
skill-seekers scrape --config configs/react.json

# 2b. Enhance later
skill-seekers enhance output/react/

# 3. Package
skill-seekers package output/react/
```

---

## 💡 Pro Tips

### Test with Small Pages First
Edit config file:
```json
{
  "max_pages": 20  // Test with just 20 pages
}
```

### Rebuild Instantly
```bash
# After first scrape, you can rebuild instantly:
skill-seekers scrape --config configs/react.json --skip-scrape
```

### Create Custom Config
```bash
# Copy a preset
cp configs/react.json configs/myframework.json

# Edit it
nano configs/myframework.json

# Use it
skill-seekers scrape --config configs/myframework.json
```

---

## 📁 What You Get

```
output/
├── godot_data/          # Raw scraped data (reusable!)
└── godot/               # The skill
    ├── SKILL.md        # With real code examples!
    └── references/     # Organized docs
```

---

## ❓ Need Help?

See **README.md** for:
- Complete documentation
- Config file structure
- Troubleshooting
- Advanced usage

---

## 🎮 Let's Go!

```bash
# Godot
skill-seekers scrape --config configs/godot.json

# Or interactive
skill-seekers scrape --interactive
```

That's it! 🚀
