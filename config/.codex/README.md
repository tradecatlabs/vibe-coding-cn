# `config/.codex/` 用法说明

本目录用于在仓库内版本化管理 Codex CLI 的“全局配置基线”，便于多人同步、审阅与回滚。

你只需要把本目录里的两个文件复制到 **Codex Home**（默认 `~/.codex/`）即可生效：

- `config/.codex/config.toml` → `~/.codex/config.toml`
- `config/.codex/AGENTS.md` → `~/.codex/AGENTS.md`

## 1. 一键安装（推荐）

在仓库根目录执行：

```bash
mkdir -p ~/.codex
cp -f config/.codex/config.toml ~/.codex/config.toml
cp -f config/.codex/AGENTS.md ~/.codex/AGENTS.md
```

## 2. 路径示例

### Linux / WSL（实际生效位置）

- `\\wsl.localhost\\Ubuntu\\home\\<你的用户名>\\.codex\\config.toml`
- `\\wsl.localhost\\Ubuntu\\home\\<你的用户名>\\.codex\\AGENTS.md`

（在 WSL 内对应：`~/.codex/config.toml` 与 `~/.codex/AGENTS.md`）

### Windows（原生）

Codex Home 默认是 `~/.codex/`；在 Windows 上 `~` 通常展开为用户目录：

- `C:\\Users\\<你的用户名>\\.codex\\config.toml`
- `C:\\Users\\<你的用户名>\\.codex\\AGENTS.md`

如果你自己的 Codex Home 被改到了其它位置（例如 `C:\\Users\\<你的用户名>\\.config\\...`），请把两份文件复制到你实际的 Codex Home。

## 3. 配置优先级（重要）

- **全局配置**：`~/.codex/config.toml`
- **项目覆盖**：在项目根目录创建 `.codex/config.toml`（仅对当前项目生效）

如果你想把某些配置“只对本仓库生效”，建议使用项目覆盖（`.codex/config.toml`），全局配置只保留你长期通用的习惯与安全策略。

## 4. 参考（官方文档）

- Configuration / Config file：说明 `~/.codex/config.toml` 与项目级 `.codex/config.toml` 的优先级
- Custom instructions / Global instructions：说明 `~/.codex/AGENTS.md` 的全局指令加载方式

