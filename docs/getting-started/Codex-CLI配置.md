# Codex CLI 配置

> 默认 AI CLI 路线：假设你拿到的是一台全新电脑，从 0 安装系统依赖、Node.js、Codex CLI，然后用浏览器完成 Codex 登录。

## 定位

Codex CLI 是本教程默认推荐的 AI CLI。它适合承担从需求拆解、代码修改、命令执行、测试验证到 Git 提交的主流程。

OpenCode CLI 只作为备选方案保留在本文底部：当你暂时无法使用 OpenAI / Codex CLI，或只想接入免费、本地、多模型实验入口时，再使用 OpenCode。

## 不会操作？先让网页 AI 生成逐步执行版

如果你不确定该执行哪一段安装命令，打开 ChatGPT / Claude / Gemini 网页版，把下面提示词和本文档全文一起粘贴进去，让 AI 根据你的电脑情况生成专属安装步骤。

```text
我正在按下面这份 Codex CLI 安装文档配置一台新电脑。请你根据我的系统情况，生成一步一步执行流程。

我的系统是：____
我是否已经安装过 WSL / Node.js / npm / Git：____
我想使用的登录方式是：网页登录 codex login

要求：
1. 每一步只做一件事。
2. 明确告诉我在哪个终端执行：PowerShell、Ubuntu 终端、Linux shell 或 macOS Terminal。
3. 每条命令都必须单独放在代码块里，方便我直接复制。
4. 每一步执行后都给一个验证命令或验证方法。
5. 不要假设我已经安装任何前置依赖；按新电脑处理。
6. 如果我后续贴完整报错，请根据当前步骤给出最小修复命令。

下面是完整文档：

[把本文档全文粘贴到这里]
```

如果安装过程中已经报错，不要只复制最后一行错误。请把“你执行的命令 + 完整报错 + 本文档全文”一起发给 AI。

```text
我正在按下面这份 Codex CLI 安装文档配置一台新电脑，但遇到了报错。

我的系统是：____
我执行的命令是：____
完整报错如下：
____

请判断我卡在哪一步，给出最小修复命令，并说明修复后如何验证。

[把本文档全文粘贴到这里]
```

## 总流程

```text
新电脑
  -> 安装系统基础工具
  -> 安装 Node.js 22+
  -> npm 安装 Codex CLI
  -> codex --version 验证
  -> codex login 浏览器登录
  -> 复制本仓库 Codex 配置基线
  -> 进入项目运行 codex
```

推荐优先级：

1. Windows 11 用户优先使用 WSL2 + Ubuntu。
2. Linux 用户按 Ubuntu / Debian 路线安装。
3. macOS 用户使用 Homebrew 安装 Node.js。
4. Windows 原生 PowerShell 可用，但长期工程体验不如 WSL2 稳定。

## Windows 11：推荐 WSL2 + Ubuntu

### 第一步：安装 WSL2

在 Windows 开始菜单搜索 **PowerShell**，右键“以管理员身份运行”：

```powershell
wsl --install -d Ubuntu
```

安装完成后重启电脑，打开 Ubuntu，按提示创建 Linux 用户名和密码。

如果已经安装过 WSL，可执行：

```powershell
wsl --update
wsl --set-default-version 2
```

### 第二步：在 Ubuntu 中安装 Codex CLI

打开 Ubuntu 终端，执行：

```bash
sudo apt update && sudo apt install -y curl ca-certificates gnupg git build-essential
sudo install -d -m 0755 /etc/apt/keyrings
sudo rm -f /etc/apt/keyrings/nodesource.gpg
curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_22.x nodistro main" | sudo tee /etc/apt/sources.list.d/nodesource.list
sudo apt update && sudo apt install -y nodejs
sudo npm i -g @openai/codex@latest
node -v
npm -v
codex --version
```

### 第三步：网页登录

```bash
codex login
```

按终端提示打开浏览器完成登录。登录后检查状态：

```bash
codex login status
```

## Ubuntu / Debian Linux

全新 Ubuntu / Debian 机器直接执行：

```bash
sudo apt update && sudo apt install -y curl ca-certificates gnupg git build-essential
sudo install -d -m 0755 /etc/apt/keyrings
sudo rm -f /etc/apt/keyrings/nodesource.gpg
curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_22.x nodistro main" | sudo tee /etc/apt/sources.list.d/nodesource.list
sudo apt update && sudo apt install -y nodejs
sudo npm i -g @openai/codex@latest
node -v
npm -v
codex --version
codex login
```

如果你是在 root 用户下配置新服务器，可以去掉 `sudo`：

```bash
apt update && apt install -y curl ca-certificates gnupg git build-essential && install -d -m 0755 /etc/apt/keyrings && rm -f /etc/apt/keyrings/nodesource.gpg && curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg && echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_22.x nodistro main" > /etc/apt/sources.list.d/nodesource.list && apt update && apt install -y nodejs && npm i -g @openai/codex@latest && node -v && npm -v && codex --version
```

然后执行：

```bash
codex login
```

## macOS

### 第一步：安装命令行工具

```bash
xcode-select --install
```

如果系统提示已经安装，可继续下一步。

### 第二步：安装 Homebrew

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

安装结束后，按 Homebrew 终端输出把 `brew` 加入 shell 环境。

Apple Silicon 常见配置：

```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

Intel Mac 常见配置：

```bash
echo 'eval "$(/usr/local/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/usr/local/bin/brew shellenv)"
```

### 第三步：安装 Node.js 和 Codex CLI

```bash
brew install git node
npm i -g @openai/codex@latest
node -v
npm -v
codex --version
codex login
```

## Windows 11：原生 PowerShell 备选

如果你暂时不想使用 WSL2，可以在 Windows 原生 PowerShell 中安装。

打开 PowerShell：

```powershell
winget source update
winget install --id Git.Git -e --source winget
winget install --id OpenJS.NodeJS.LTS -e --source winget
```

关闭并重新打开 PowerShell，然后执行：

```powershell
node -v
npm -v
npm i -g @openai/codex@latest
codex --version
codex login
```

如果 `winget` 不存在，先在 Microsoft Store 更新或安装 **App Installer**。

## API Key 模式（可选）

默认推荐 `codex login` 浏览器登录。不要把占位 API Key 写进环境变量，否则可能干扰认证排查。

如果你明确要使用 API Key 模式，再执行：

```bash
mkdir -p ~/.config
grep -q "OPENAI_API_KEY" ~/.bashrc || echo 'export OPENAI_API_KEY="sk-替换成你的OpenAI_API_KEY"' >> ~/.bashrc
source ~/.bashrc
printenv OPENAI_API_KEY | codex login --with-api-key
```

Windows PowerShell 的 API Key 配置：

```powershell
[Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "sk-替换成你的OpenAI_API_KEY", "User")
$env:OPENAI_API_KEY="sk-替换成你的OpenAI_API_KEY"
$env:OPENAI_API_KEY | codex login --with-api-key
```

## 使用仓库配置基线

本仓库已经提供 Codex CLI 配置基线：

- `tools/config/.codex/config.toml`
- `tools/config/.codex/AGENTS.md`

在仓库根目录执行：

```bash
mkdir -p ~/.codex
cp -f tools/config/.codex/config.toml ~/.codex/config.toml
cp -f tools/config/.codex/AGENTS.md ~/.codex/AGENTS.md
```

详细说明见：[Codex 配置基线](../../../config/.codex/README.md)。

## 推荐启动方式

日常使用：

```bash
codex --search -m gpt-5.5 -c model_reasoning_effort="xhigh"
```

在完全可信的本地仓库中，需要减少确认弹窗时使用：

```bash
codex --search -m gpt-5.5 -c model_reasoning_effort="xhigh" --dangerously-bypass-approvals-and-sandbox
```

高权限模式会放开确认与沙箱限制，只能在你确认可信的目录中使用。

## 推荐别名

Linux / WSL / macOS：

```bash
cat >> ~/.bashrc <<'EOF'
alias c='codex --search -m gpt-5.5 -c model_reasoning_effort="xhigh"'
alias cy='codex --search -m gpt-5.5 -c model_reasoning_effort="xhigh" --dangerously-bypass-approvals-and-sandbox'
EOF
source ~/.bashrc
```

如果你使用的是 macOS 默认 zsh，把 `~/.bashrc` 换成 `~/.zshrc`：

```bash
cat >> ~/.zshrc <<'EOF'
alias c='codex --search -m gpt-5.5 -c model_reasoning_effort="xhigh"'
alias cy='codex --search -m gpt-5.5 -c model_reasoning_effort="xhigh" --dangerously-bypass-approvals-and-sandbox'
EOF
source ~/.zshrc
```

## 第一次使用

进入你的项目目录：

```bash
cd /path/to/project
codex
```

然后让 Codex 先建立项目上下文：

```text
请阅读当前仓库结构，说明这个项目是什么、关键入口在哪里、下一步最小可执行任务是什么。先给计划，不要直接改文件。
```

确认计划后，再让 Codex 执行。

## 常见问题

### `codex: command not found`

检查 npm 全局安装目录是否在 `PATH` 中：

```bash
npm config get prefix
echo "$(npm config get prefix)/bin"
```

重新打开终端后再执行：

```bash
codex --version
```

### `sudo npm i -g` 权限问题

Linux / WSL 用 NodeSource 安装的 Node.js 通常需要 `sudo npm i -g`。如果你使用 nvm 管理 Node.js，则不要使用 `sudo`。

### 浏览器登录失败

先确认网络环境可访问 OpenAI 登录页面，再执行：

```bash
codex login
```

如果你是在无桌面的远程服务器上登录，按终端输出的设备码或链接，在本机浏览器完成授权。

## Codex 不可用时：OpenCode 备选方案

OpenCode 是开源 AI 编程代理，支持终端、桌面应用和 IDE 扩展。本文仍然以 Codex CLI 为默认路线；只有当 Codex CLI 暂时不可用、账号不可用，或你明确需要接入免费/本地模型时，才切到 OpenCode。

官网：[opencode.ai](https://opencode.ai/)

### 不会操作？先让网页 AI 生成逐步执行版

如果你要用 OpenCode 作为备选路线，先打开网页版 AI，把下面提示词和本节内容一起复制进去，让 AI 按你的系统和模型来源生成逐步执行方案：

```text
你是一个面向零基础用户的 OpenCode CLI 配置助手。

请根据我的电脑环境、可用模型和目标，生成适合我的逐步安装与配置流程。

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

### 何时选择 OpenCode

- 没有可用的 OpenAI / Codex CLI 账号或环境。
- 需要接入 Z.AI、MiniMax、Hugging Face、本地 Ollama 等模型。
- 想保留一条不依赖单一模型提供商的备份路线。

### 安装

```bash
# 一键安装（推荐）
curl -fsSL https://opencode.ai/install | bash

# 或使用 npm
npm install -g opencode-ai

# 或使用 Homebrew（macOS/Linux）
brew install anomalyco/tap/opencode
```

Windows 可用 Scoop 或 Chocolatey：

```powershell
scoop bucket add extras
scoop install extras/opencode

choco install opencode
```

### 模型配置

OpenCode 支持多个模型提供商。进入 OpenCode 后，用 `/connect` 添加模型提供商，用 `/models` 切换模型。

常见备选：

1. Z.AI：注册 API Key 后，`/connect` 搜索 Z.AI，再用 `/models` 选择 GLM 模型。
2. MiniMax：注册 API Key 后，`/connect` 搜索 MiniMax，再用 `/models` 选择可用模型。
3. Hugging Face：创建 Token 后，`/connect` 搜索 Hugging Face，再用 `/models` 选择可用模型。
4. Ollama：本地安装 Ollama 后，在 `opencode.json` 中配置 OpenAI-compatible base URL。

Ollama 最小安装示例：

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama2
```

### 核心命令

| 命令 | 功能 |
|:---|:---|
| `/models` | 切换模型 |
| `/connect` | 添加 API Key |
| `/init` | 初始化项目，生成 AGENTS.md |
| `/undo` | 撤销上次修改 |
| `/redo` | 重做 |
| `/share` | 分享对话链接 |
| `Tab` | 切换 Plan 模式 |

### 推荐工作流

```bash
cd /path/to/project
opencode
```

进入后先初始化项目，再切换模型：

```text
/init
/models
```

建议先用 Plan 模式让 AI 规划，确认方案后再执行。

### 配置文件位置

- 全局配置：`~/.config/opencode/opencode.json`
- 项目配置：`./opencode.json`
- 认证信息：`~/.local/share/opencode/auth.json`

### 相关资源

- [OpenCode 官方文档](https://opencode.ai/docs/)
- [OpenCode GitHub 仓库](https://github.com/opencode-ai/opencode)
- [Models.dev 模型目录](https://models.dev)

## 下一步

→ [开发环境搭建](开发环境搭建.md) - 回看基础环境
