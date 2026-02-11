```
name: headless-cli
description: "Headless Mode AI CLI Calling Skill: Supports non-interactive batch calling of Gemini/Claude/Codex CLIs, including YOLO mode and safe mode. Used for scenarios like batch translation, code review, multi-model orchestration, etc."
---

# Headless CLI Skill

Non-interactive batch calling of AI CLI tools, supporting stdin/stdout pipes to achieve automated workflows.

## When to Use This Skill

Trigger conditions:
- Need to process files in batches (translate, review, format)
- Need to call AI models in scripts
- Need to chain/parallelize multiple models
- Need unattended AI task execution

## Not For / Boundaries

Not applicable for:
- Scenarios requiring interactive conversation
- Tasks requiring real-time feedback
- Sensitive operations (YOLO mode requires caution)

Required inputs:
- Corresponding CLI tools installed
- Identity authentication completed
- Network proxy configuration (if needed)

## Quick Reference

### 🔴 YOLO Mode (Full permissions, skips confirmation)

**Codex CLI**
```bash
# --yolo is an alias for --dangerously-bypass-approvals-and-sandbox
alias c='codex --enable web_search_request -m gpt-5.3-codex-max -c model_reasoning_effort="high" --yolo'
```

**Claude Code**
```bash
alias cc='claude --dangerously-skip-permissions'
```

**Gemini CLI**
```bash
# --yolo or --approval-mode yolo
alias g='gemini --yolo'
```

### 🟡 Full-Auto Mode (Recommended automation method)

**Codex CLI**
```bash
# workspace-write sandbox + approval only on failure
codex --full-auto "Your prompt"
```

**Gemini CLI**
```bash
# Automatically approve edit tools
gemini --approval-mode auto_edit "Your prompt"
```

### 🟢 Safe Mode (Headless but with limitations)

**Gemini CLI (Disable tool calls)**
```bash
cat input.md | gemini -p "prompt" --output-format text --allowed-tools '' > output.md
```

**Claude Code (Print Mode)**
```bash
cat input.md | claude -p "prompt" --output-format text > output.md
```

**Codex CLI (Non-interactive execution)**
```bash
codex exec "prompt" --json -o result.txt
```

### 📋 Common Command Templates

**Batch Translation**
```bash
# Set proxy (if needed)
export http_proxy=http://127.0.0.1:9910
export https_proxy=http://127.0.0.1:9910

# Gemini Translation
cat zh.md | gemini -p "Translate to English. Keep code/links unchanged." \
  --output-format text --allowed-tools '' > en.md
```

**Code Review**
```bash
cat code.py | claude --dangerously-skip-permissions -p \
  "Review this code for bugs and security issues. Output markdown." > review.md
```

**Multi-Model Orchestration**
```bash
# Model A generates → Model B reviews
cat spec.md | gemini -p "Generate code" --output-format text | \
  claude -p "Review and improve this code" --output-format text > result.md
```

### ⚙️ Key Parameter Comparison Table

| Feature | Gemini CLI | Claude Code | Codex CLI |
|:---|:---|:---|:---|
| YOLO Mode | `--yolo` | `--dangerously-skip-permissions` | `--yolo` |
| Specify Model | `-m <model>` | `--model <model>` | `-m <model>` |
| Non-interactive | `-p "prompt"` | `-p "prompt"` | `exec "prompt"` |
| Output Format | `--output-format text` | `--output-format text` | `--json` |
| Disable Tools | `--allowed-tools ''` | `--disallowedTools` | N/A |
| Continue Conversation | N/A | `-c` / `--continue` | `resume --last` |

## Examples

### Example 1: Batch Translating Documents

**Input**: Chinese Markdown file
**Steps**:
```bash
export http_proxy=http://127.0.0.1:9910
export https_proxy=http://127.0.0.1:9910

for f in docs/*.md; do
  cat "$f" | timeout 120 gemini -p \
    "Translate to English. Keep code fences unchanged." \
    --output-format text --allowed-tools '' 2>/dev/null > "en_$(basename $f)"
done
```
**Expected output**: Translated English file

### Example 2: Code Review Pipeline

**Input**: Python code file
**Steps**:
```bash
cat src/*.py | claude --dangerously-skip-permissions -p \
  "Review for: 1) Bugs 2) Security 3) Performance. Output markdown table." > review.md
```
**Expected output**: Markdown formatted review report

### Example 3: Multi-Model Comparison and Verification

**Input**: Technical question
**Steps**:
```bash
question="How to implement rate limiting in Python?"

echo "$question" | gemini -p "$question" --output-format text > gemini_answer.md
echo "$question" | claude -p "$question" --output-format text > claude_answer.md

# Compare the two answers
diff gemini_answer.md claude_answer.md
```
**Expected output**: Comparison of answers from two models

## References

- `references/gemini-cli.md` - Gemini CLI complete parameters
- `references/claude-cli.md` - Claude Code CLI parameters
- `references/codex-cli.md` - Codex CLI parameters
- [Gemini CLI Official Documentation](https://geminicli.com/docs/)
- [Claude Code Official Documentation](https://docs.anthropic.com/en/docs/claude-code/)
- [Codex CLI Official Documentation](https://developers.openai.com/codex/cli/reference)

## Maintenance

- Source: Official CLI documentation for each
- Updated: 2025-12-19
- Limitations: Requires network connection and valid authentication; YOLO mode has security risks
```
