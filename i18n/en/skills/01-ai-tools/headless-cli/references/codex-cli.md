```markdown
# Codex CLI Parameter Reference

> Source: [Official Documentation](https://developers.openai.com/codex/cli/reference)

## Installation

```bash
npm install -g @openai/codex
```

## Authentication

```bash
# Method 1: Browser OAuth (ChatGPT account)
codex login

# Method 2: API Key
printenv OPENAI_API_KEY | codex login --with-api-key

# Check login status
codex login status
```

## Core Commands

| Command | Description | Example |
|:---|:---|:---|
| `codex` | Starts interactive TUI | `codex` |
| `codex "prompt"` | Starts with a prompt | `codex "explain this"` |
| `codex exec` / `codex e` | Non-interactive mode | `codex exec "fix bugs"` |
| `codex resume` | Resumes session | `codex resume --last` |
| `codex apply` / `codex a` | Applies diff from Cloud task | `codex apply TASK_ID` |
| `codex mcp` | Manages MCP server | `codex mcp add server` |
| `codex completion` | Generates shell completion | `codex completion zsh` |

## Global Parameters

| Parameter | Description | Example |
|:---|:---|:---|
| `--model, -m` | Specifies model | `-m gpt-5-codex` |
| `--sandbox, -s` | Sandbox policy: `read-only`/`workspace-write`/`danger-full-access` | `-s workspace-write` |
| `--ask-for-approval, -a` | Approval mode: `untrusted`/`on-failure`/`on-request`/`never` | `-a on-failure` |
| `--full-auto` | Automatic preset (workspace-write + on-failure) | `--full-auto` |
| `--dangerously-bypass-approvals-and-sandbox` / `--yolo` | Bypasses all approvals and sandbox | `--yolo` |
| `--search` | Enables web search | `--search` |
| `--add-dir` | Adds extra write directory | `--add-dir ./other` |
| `--enable` | Enables feature flag | `--enable web_search_request` |
| `--disable` | Disables feature flag | `--disable feature_name` |
| `--config, -c` | Configuration override | `-c model_reasoning_effort="high"` |
| `--image, -i` | Attaches image | `-i image.png` |
| `--cd, -C` | Sets working directory | `-C /path/to/project` |
| `--profile, -p` | Profile configuration | `-p my-profile` |
| `--oss` | Uses local open-source model (Ollama) | `--oss` |

## `codex exec` Specific Parameters

| Parameter | Description | Example |
|:---|:---|:---|
| `--json` | Outputs JSONL format | `--json` |
| `--output-last-message, -o` | Saves final message to file | `-o result.txt` |
| `--output-schema` | JSON Schema validation output | `--output-schema schema.json` |
| `--color` | Color output: `always`/`never`/`auto` | `--color never` |
| `--skip-git-repo-check` | Allows running in non-Git directories | `--skip-git-repo-check` |

## Available Models

- `gpt-5-codex` - Standard model
- `gpt-5.3-codex` - Enhanced version
- `gpt-5.3-codex-max` - Strongest model

## Reasoning Strength Configuration

```bash
-c model_reasoning_effort="low"    # Fast
-c model_reasoning_effort="medium" # Balanced
-c model_reasoning_effort="high"   # Deep
```

## Headless Mode Usage

```bash
# Non-interactive execution
codex exec "fix all linting errors"

# Piped input
echo "explain this error" | codex exec -

# YOLO mode (skips all confirmations and sandbox)
codex --yolo "Your prompt"

# Or full syntax
codex --dangerously-bypass-approvals-and-sandbox "Your prompt"

# full-auto mode (recommended automated approach)
codex --full-auto "Your prompt"

# Full YOLO config alias
alias c='codex --enable web_search_request -m gpt-5.3-codex-max -c model_reasoning_effort="high" --yolo'

# Resume last session
codex resume --last
codex exec resume --last "continue"
```

## Configuration File

Configuration is stored in `~/.codex/config.toml`:

```toml
model = "gpt-5-codex"
sandbox = "workspace-write"
ask_for_approval = "on-failure"

[features]
web_search_request = true
```

## Frequently Asked Questions

1.  **Approval pop-ups**: Use `--yolo` or `--full-auto`
2.  **Internet connection required**: Use `--search` or `--enable web_search_request`
3.  **Insufficient reasoning depth**: Use `-c model_reasoning_effort="high"`
4.  **Non-Git directory**: Use `--skip-git-repo-check`
```
