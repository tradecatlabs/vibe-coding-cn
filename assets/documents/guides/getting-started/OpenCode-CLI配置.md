# OpenCode CLI 配置（备选方案）

> 备选 AI CLI 路线：当你暂时无法使用 Codex CLI，或希望接入免费/本地模型时使用。

本教程默认推荐 [Codex CLI](./Codex-CLI配置.md)。OpenCode 是开源 AI 编程代理，支持终端、桌面应用和 IDE 扩展，适合用作免费模型、本地模型或多模型实验入口。

官网：[opencode.ai](https://opencode.ai/)

---

## 不会操作？先让网页 AI 生成逐步执行版

如果你暂时无法使用 Codex CLI，或想把 OpenCode 作为备选路线，先打开网页版 AI（ChatGPT / Claude / Gemini 均可），把下面这段提示词和本文件全文一起复制进去，让 AI 按你的系统和模型来源生成逐步执行方案：

```text
你是一个面向零基础用户的 OpenCode CLI 配置助手。

我会把一份 OpenCode CLI 配置文档发给你。请你根据我的电脑环境、可用模型和目标，生成适合我的逐步安装与配置流程。

我的当前情况是：
- 操作系统：[填写 Windows 11 / WSL2 / macOS / Linux]
- 是否已经安装 Node.js / npm / Homebrew / Scoop / Chocolatey：[填写没有 / 已安装 / 不确定]
- 想使用的模型来源：[填写 Z.AI / MiniMax / Hugging Face / Ollama / 不确定]
- 是否已经有 API Key：[填写有 / 没有 / 不确定]
- 卡住的位置：[如果已经卡住，填写具体问题；如果没有，写“还没开始”]

要求：
1. 每一步只做一件事。
2. 每一步都说明我要在哪个终端执行、输入什么、观察什么、如何判断成功。
3. 每条命令都必须单独放在代码块里。
4. 不要跳步；默认我是第一次配置新电脑。
5. 如果我后续贴报错，请根据当前步骤给出最小修复方案。
```

## 何时选择 OpenCode

- 没有可用的 OpenAI / Codex CLI 账号或环境
- 需要接入 Z.AI、MiniMax、Hugging Face、本地 Ollama 等模型
- 想保留一条不依赖单一模型提供商的备份路线

如果 Codex CLI 可用，优先完成：[Codex-CLI配置](./Codex-CLI配置.md)。

## 安装

```bash
# 一键安装（推荐）
curl -fsSL https://opencode.ai/install | bash

# 或使用 npm
npm install -g opencode-ai

# 或使用 Homebrew (macOS/Linux)
brew install anomalyco/tap/opencode

# Windows - Scoop
scoop bucket add extras && scoop install extras/opencode

# Windows - Chocolatey
choco install opencode
```

---

## 免费模型配置

OpenCode 支持多个模型提供商。以下配置适合作为 Codex CLI 不可用时的备选入口。

### 方式一：Z.AI（推荐，GLM-4.7）

1. 访问 [Z.AI API 控制台](https://z.ai/manage-apikey/apikey-list) 注册并创建 API Key
2. 运行 `/connect` 命令，搜索 **Z.AI**
3. 输入 API Key
4. 运行 `/models` 选择 **GLM-4.7**

```bash
opencode
# 进入后输入
/connect
# 选择 Z.AI，输入 API Key
/models
# 选择 GLM-4.7
```

### 方式二：MiniMax（M2.1）

1. 访问 [MiniMax API 控制台](https://platform.minimax.io/login) 注册并创建 API Key
2. 运行 `/connect`，搜索 **MiniMax**
3. 输入 API Key
4. 运行 `/models` 选择 **M2.1**

### 方式三：Hugging Face（多种免费模型）

1. 访问 [Hugging Face 设置](https://huggingface.co/settings/tokens/new?ownUserPermissions=inference.serverless.write&tokenType=fineGrained) 创建 Token
2. 运行 `/connect`，搜索 **Hugging Face**
3. 输入 Token
4. 运行 `/models` 选择 **Kimi-K2-Instruct** 或 **GLM-4.6**

### 方式四：本地模型（Ollama）

```bash
# 安装 Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 拉取模型
ollama pull llama2
```

在 `opencode.json` 中配置：

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

## 核心命令

| 命令 | 功能 |
|:---|:---|
| `/models` | 切换模型 |
| `/connect` | 添加 API Key |
| `/init` | 初始化项目（生成 AGENTS.md） |
| `/undo` | 撤销上次修改 |
| `/redo` | 重做 |
| `/share` | 分享对话链接 |
| `Tab` | 切换 Plan 模式（只规划不执行） |

---

## 让 AI 执行一切配置任务

OpenCode 的核心思维：**把配置任务交给 AI 执行，把选择权和验收权留给你**。

### 示例：安装 MCP 服务器

```
帮我安装 filesystem MCP 服务器，配置到 opencode
```

### 示例：部署 GitHub 开源项目

```
克隆 https://github.com/xxx/yyy 项目，阅读 README，帮我完成所有依赖安装和环境配置
```

### 示例：配置 Skills

```
阅读项目结构，为这个项目创建合适的 AGENTS.md 规则文件
```

### 示例：配置环境变量

```
检查项目需要哪些环境变量，帮我创建 .env 文件模板并说明每个变量的用途
```

### 示例：安装依赖

```
分析 package.json / requirements.txt，安装所有依赖，解决版本冲突
```

---

## 推荐工作流

1. **进入项目目录**
   ```bash
   cd /path/to/project
   opencode
   ```

2. **初始化项目**
   ```
   /init
   ```

3. **切换免费模型**
   ```
   /models
   # 选择 GLM-4.7 或 MiniMax M2.1
   ```

4. **开始工作**
   - 先用 `Tab` 切换到 Plan 模式，让 AI 规划
   - 确认方案后再让 AI 执行

---

## 配置文件位置

- 全局配置：`~/.config/opencode/opencode.json`
- 项目配置：`./opencode.json`（项目根目录）
- 认证信息：`~/.local/share/opencode/auth.json`

---

## 相关资源

- [OpenCode 官方文档](https://opencode.ai/docs/)
- [GitHub 仓库](https://github.com/opencode-ai/opencode)
- [Models.dev - 模型目录](https://models.dev)
