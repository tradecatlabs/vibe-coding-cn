# Codex CLI 配置

> 默认 AI CLI 路线：用 Codex CLI 作为主要编程代理，把本仓库的配置基线复制到本机 Codex Home。

## 定位

Codex CLI 是本教程默认推荐的 AI CLI。它适合承担从需求拆解、代码修改、命令执行、测试验证到 Git 提交的主流程。

OpenCode CLI 保留为备选方案：当你暂时无法使用 OpenAI / Codex CLI，或只想接入免费模型时，再使用 [OpenCode-CLI配置](./OpenCode-CLI配置.md)。

## 前置条件

请先完成：

1. [网络环境配置](./网络环境配置.md)
2. [开发环境搭建](./开发环境搭建.md)
3. [IDE 配置](./IDE配置.md)

在终端验证 Codex CLI 是否可用：

```bash
codex --help
```

如果命令不存在，先按你当前系统的 Codex CLI 安装方式完成安装，再回到本页继续。

## 登录

```bash
codex login
```

登录完成后，再次运行：

```bash
codex --help
```

能看到命令说明，就说明 CLI 已可用。

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

在 `~/.bashrc` 中添加：

```bash
alias c='codex --search -m gpt-5.5 -c model_reasoning_effort="xhigh"'
alias cy='codex --search -m gpt-5.5 -c model_reasoning_effort="xhigh" --dangerously-bypass-approvals-and-sandbox'
```

生效：

```bash
source ~/.bashrc
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

## 下一步

→ [开发环境搭建](./开发环境搭建.md) - 回看基础环境

→ [IDE 配置](./IDE配置.md) - 配置编辑器

→ [OpenCode-CLI配置](./OpenCode-CLI配置.md) - Codex CLI 不可用时的备选方案
