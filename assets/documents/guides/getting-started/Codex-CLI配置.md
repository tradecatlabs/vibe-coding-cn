# Codex CLI 配置

> 默认 AI CLI 路线：假设你拿到的是一台全新电脑，从 0 安装系统依赖、Node.js、Codex CLI，然后用浏览器完成 Codex 登录。

## 定位

Codex CLI 是本教程默认推荐的 AI CLI。它适合承担从需求拆解、代码修改、命令执行、测试验证到 Git 提交的主流程。

OpenCode CLI 保留为备选方案：当你暂时无法使用 OpenAI / Codex CLI，或只想接入免费模型时，再使用 [OpenCode-CLI配置](./OpenCode-CLI配置.md)。

## 遇到问题先这样问 AI

如果安装过程中报错，不要只复制最后一行错误。请把以下三部分一起发给 AI（可以用 ChatGPT / Claude / Gemini 网页版）：

1. 你的系统：Windows 11 / WSL2 Ubuntu / Ubuntu / Debian / macOS。
2. 完整报错：从你执行的命令开始，到错误结束，全部复制。
3. 本文档全文：把本页从标题到末尾完整复制给 AI，让它基于本文档判断你卡在哪一步。

推荐提问模板：

```text
我正在按下面这份 Codex CLI 安装文档配置一台新电脑，但遇到了报错。

我的系统是：____
我执行的命令是：____
完整报错如下：
____

下面是我正在遵循的完整安装文档。请你判断我卡在哪一步，给出最小修复命令，并说明修复后如何验证。

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

- `assets/config/.codex/config.toml`
- `assets/config/.codex/AGENTS.md`

在仓库根目录执行：

```bash
mkdir -p ~/.codex
cp -f assets/config/.codex/config.toml ~/.codex/config.toml
cp -f assets/config/.codex/AGENTS.md ~/.codex/AGENTS.md
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

## 下一步

→ [开发环境搭建](./开发环境搭建.md) - 回看基础环境

→ [OpenCode-CLI配置](./OpenCode-CLI配置.md) - Codex CLI 不可用时的备选方案
