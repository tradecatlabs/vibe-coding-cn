# Terminal Selection Guide

When using `--enhance-local`, Skill Seeker opens a new terminal window to run Claude Code. This guide explains how to control which terminal app is used.

## Priority Order

The script automatically detects which terminal to use in this order:

1. **`SKILL_SEEKER_TERMINAL` environment variable** (highest priority)
2. **`TERM_PROGRAM` environment variable** (inherit current terminal)
3. **Terminal.app** (fallback default)

## Setting Your Preferred Terminal

### Option 1: Set Environment Variable (Recommended)

Add this to your shell config (`~/.zshrc` or `~/.bashrc`):

```bash
# For Ghostty users
export SKILL_SEEKER_TERMINAL="Ghostty"

# For iTerm users
export SKILL_SEEKER_TERMINAL="iTerm"

# For WezTerm users
export SKILL_SEEKER_TERMINAL="WezTerm"
```

Then reload your shell:
```bash
source ~/.zshrc  # or source ~/.bashrc
```

### Option 2: Set Per-Session

Set the variable before running the command:

```bash
SKILL_SEEKER_TERMINAL="Ghostty" python3 cli/doc_scraper.py --config configs/react.json --enhance-local
```

### Option 3: Inherit Current Terminal (Automatic)

If you run the script from Ghostty, iTerm2, or WezTerm, it will automatically open the enhancement in the same terminal app.

**Note:** IDE terminals (VS Code, Zed, JetBrains) use unique `TERM_PROGRAM` values, so they fall back to Terminal.app unless you set `SKILL_SEEKER_TERMINAL`.

## Supported Terminals

- **Ghostty** (`ghostty`)
- **iTerm2** (`iTerm.app`)
- **Terminal.app** (`Apple_Terminal`)
- **WezTerm** (`WezTerm`)

## Example Output

When terminal detection works:
```
🚀 Launching Claude Code in new terminal...
   Using terminal: Ghostty (from SKILL_SEEKER_TERMINAL)
```

When running from an IDE terminal:
```
🚀 Launching Claude Code in new terminal...
⚠️  unknown TERM_PROGRAM (zed)
   → Using Terminal.app as fallback
```

**Tip:** Set `SKILL_SEEKER_TERMINAL` to avoid the fallback behavior.

## Troubleshooting

**Q: The wrong terminal opens even though I set `SKILL_SEEKER_TERMINAL`**

A: Make sure you reloaded your shell after editing `~/.zshrc`:
```bash
source ~/.zshrc
```

**Q: I want to use a different terminal temporarily**

A: Set the variable inline:
```bash
SKILL_SEEKER_TERMINAL="iTerm" python3 cli/doc_scraper.py --enhance-local ...
```

**Q: Can I use a custom terminal app?**

A: Yes! Just use the app name as it appears in `/Applications/`:
```bash
export SKILL_SEEKER_TERMINAL="Alacritty"
```
