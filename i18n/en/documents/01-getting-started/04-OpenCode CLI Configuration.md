# OpenCode CLI Configuration

> Free AI programming assistant, supporting 75+ models, no credit card required

OpenCode is an open-source AI programming agent that supports terminal, desktop applications, and IDE extensions. Free models can be used without an account.

Official website: [opencode.ai](https://opencode.ai/)

---

## Installation

```bash
# One-click installation (recommended)
curl -fsSL https://opencode.ai/install | bash

# Or use npm
npm install -g opencode-ai

# Or use Homebrew (macOS/Linux)
brew install anomalyco/tap/opencode

# Windows - Scoop
scoop bucket add extras && scoop install extras/opencode

# Windows - Chocolatey
choco install opencode
```

---

## Free Model Configuration

OpenCode supports multiple free model providers that can be used without payment.

### Option 1: Z.AI (Recommended, GLM-4.7)

1. Visit [Z.AI API Console](https://z.ai/manage-apikey/apikey-list) to register and create an API Key
2. Run the `/connect` command, search for **Z.AI**
3. Enter your API Key
4. Run `/models` and select **GLM-4.7**

```bash
opencode
# After entering, type
/connect
# Select Z.AI, enter API Key
/models
# Select GLM-4.7
```

### Option 2: MiniMax (M2.1)

1. Visit [MiniMax API Console](https://platform.minimax.io/login) to register and create an API Key
2. Run `/connect`, search for **MiniMax**
3. Enter your API Key
4. Run `/models` and select **M2.1**

### Option 3: Hugging Face (Multiple Free Models)

1. Visit [Hugging Face Settings](https://huggingface.co/settings/tokens/new?ownUserPermissions=inference.serverless.write&tokenType=fineGrained) to create a Token
2. Run `/connect`, search for **Hugging Face**
3. Enter your Token
4. Run `/models` and select **Kimi-K2-Instruct** or **GLM-4.6**

### Option 4: Local Models (Ollama)

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull a model
ollama pull llama2
```

Configure in `opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "ollama": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Ollama (local)",
      "options": {
        "baseURL": "http://localhost:11434/v1"
      },
      "models": {
        "llama2": {
          "name": "Llama 2"
        }
      }
    }
  }
}
```

---

## Core Commands

| Command | Function |
|:---|:---|
| `/models` | Switch models |
| `/connect` | Add API Key |
| `/init` | Initialize project (generate AGENTS.md) |
| `/undo` | Undo last modification |
| `/redo` | Redo |
| `/share` | Share conversation link |
| `Tab` | Toggle Plan mode (plan only, no execution) |

---

## Let AI Handle All Configuration Tasks

The core philosophy of OpenCode: **Delegate all configuration tasks to AI**.

### Example: Install MCP Server

```
Help me install the filesystem MCP server and configure it for opencode
```

### Example: Deploy GitHub Open Source Project

```
Clone the https://github.com/xxx/yyy project, read the README, and help me complete all dependency installation and environment configuration
```

### Example: Configure Skills

```
Read the project structure and create an appropriate AGENTS.md rules file for this project
```

### Example: Configure Environment Variables

```
Check what environment variables the project needs, help me create a .env file template and explain the purpose of each variable
```

### Example: Install Dependencies

```
Analyze package.json / requirements.txt, install all dependencies, and resolve version conflicts
```

---

## Recommended Workflow

1. **Enter project directory**
   ```bash
   cd /path/to/project
   opencode
   ```

2. **Initialize project**
   ```
   /init
   ```

3. **Switch to free model**
   ```
   /models
   # Select GLM-4.7 or MiniMax M2.1
   ```

4. **Start working**
   - First use `Tab` to switch to Plan mode, let AI plan
   - Confirm the plan before letting AI execute

---

## Configuration File Locations

- Global config: `~/.config/opencode/opencode.json`
- Project config: `./opencode.json` (project root)
- Auth info: `~/.local/share/opencode/auth.json`

---

## Related Resources

- [OpenCode Official Documentation](https://opencode.ai/docs/)
- [GitHub Repository](https://github.com/opencode-ai/opencode)
- [Models.dev - Model Directory](https://models.dev)
