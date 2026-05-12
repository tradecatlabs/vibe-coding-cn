# Codex CLI 配置基线

本目录把 Codex CLI 全局配置做成可审阅、可安装、可回滚的公开基线。

## 字多不看

- 默认安装 `safe` 配置：不写入本机路径，不启用 `danger-full-access`，不设置 `approval_policy = "never"`。
- 需要全自动高权限体验时，显式安装 `power` 配置。
- 安装前会备份用户现有 `~/.codex/config.toml` 和 `~/.codex/AGENTS.md`。
- 每次安装都会生成恢复脚本，误覆盖后可以一键恢复。
- 支持通过 `CODEX_HOME` 指定 Codex Home。

## 一键安装

安全默认版：

```bash
curl -fsSL https://raw.githubusercontent.com/tukuaiai/vibe-coding-cn/develop/tools/config/.codex/install.sh | bash
```

高权限版：

```bash
curl -fsSL https://raw.githubusercontent.com/tukuaiai/vibe-coding-cn/develop/tools/config/.codex/install.sh | bash -s -- --profile power
```

指定 Codex Home：

```bash
curl -fsSL https://raw.githubusercontent.com/tukuaiai/vibe-coding-cn/develop/tools/config/.codex/install.sh | CODEX_HOME="$HOME/.codex" bash
```

## 恢复

恢复最近一次安装前的配置：

```bash
bash ~/.codex/backups/vibe-coding-cn/LATEST/restore.sh
```

也可以恢复某一次具体备份：

```bash
bash ~/.codex/backups/vibe-coding-cn/YYYYMMDD-HHMMSS/restore.sh
```

备份目录包含：

- `config.toml`：安装前的用户原配置；如果原文件不存在，会写入 `.missing-config.toml` 标记。
- `AGENTS.md`：安装前的用户原指令；如果原文件不存在，会写入 `.missing-AGENTS.md` 标记。
- `MANIFEST.txt`：安装来源、profile、目标路径和恢复脚本位置。
- `restore.sh`：恢复脚本。

## 文件说明

| 文件 | 用途 |
|:---|:---|
| `install.sh` | 一键安装、备份和恢复入口 |
| `config.toml` | 公开安全默认配置 |
| `config.power.toml` | 高权限配置，显式 `--profile power` 才安装 |
| `AGENTS.safe.md` | 公开安全默认全局指令 |
| `AGENTS.md` | 高强度个人工作流指令，配合 `power` profile 使用 |

## 安全边界

`safe` profile 适合新手和公共分发：

- 不自动信任任何本机项目路径。
- 不放开全盘读写和命令执行权限。
- 不关闭审批确认。

`power` profile 只适合完全可信的本地环境：

- 会写入 `sandbox_mode = "danger-full-access"`。
- 会写入 `approval_policy = "never"`。
- 会安装更强势的全局 `AGENTS.md`。

如果你不确定该选哪个，使用默认 `safe`。

## 本地仓库内安装

如果你已经 clone 本仓库，也可以在仓库根目录执行：

```bash
bash tools/config/.codex/install.sh
```

安装高权限版：

```bash
bash tools/config/.codex/install.sh --profile power
```

## 路径示例

Linux / WSL：

- `~/.codex/config.toml`
- `~/.codex/AGENTS.md`

Windows 原生：

- `C:\Users\<你的用户名>\.codex\config.toml`
- `C:\Users\<你的用户名>\.codex\AGENTS.md`

如果你自己的 Codex Home 被改到了其它位置，请通过 `CODEX_HOME` 或 `--codex-home` 指定。
