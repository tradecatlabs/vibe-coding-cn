# Chat Vault Monorepo

AI 聊天记录集中存储与管理平台。

## 项目概述

本项目是一个 monorepo，包含 AI 聊天记录同步工具及相关基础设施。核心功能是将多个 AI CLI 工具（Codex、Kiro、Gemini、Claude）的聊天记录统一存储到 SQLite 数据库。

## 功能特性

- 多 CLI 支持：Codex、Kiro、Gemini、Claude
- 实时监控：基于 watchdog 的文件变更检测
- Token 统计：使用 tiktoken (cl100k_base) 精确计数
- 搜索导出：支持关键词搜索、JSON/CSV 导出
- 零配置：自动检测默认路径，开箱即用

## 快速开始

### 环境要求

- Python 3.8+
- Linux / macOS / Windows (WSL)

### 启动服务

```bash
cd services/chat-vault

# Linux/macOS
./start.sh

# Windows
start.bat
```

首次运行会自动创建虚拟环境并安装依赖。

## 目录结构

```
chat-vault/
├── services/
│   └── chat-vault/          # 核心同步服务
│       ├── src/
│       │   ├── main.py      # CLI 入口
│       │   ├── config.py    # 配置与路径检测
│       │   ├── storage.py   # SQLite 存储
│       │   ├── watcher.py   # 文件监控
│       │   └── parsers/     # 各 CLI 解析器
│       ├── docs/            # 服务文档
│       ├── scripts/         # 辅助脚本
│       ├── requirements.txt
│       ├── start.sh
│       └── .env.example
├── libs/
│   ├── common/              # 共享库（预留）
│   ├── database/            # 数据库工具（预留）
│   └── external/            # 外部依赖镜像
├── monitoring/
│   ├── grafana/             # Grafana 配置
│   ├── prometheus/          # Prometheus 配置（预留）
│   └── alertmanager/        # 告警配置（预留）
├── scripts/                 # 全局脚本
│   ├── build_all.sh
│   ├── test_all.sh
│   └── deploy.sh
├── docs/                    # 全局文档
├── AGENTS.md
├── README.md
└── LICENSE
```

## 常用命令

在 `services/chat-vault/` 目录下执行：

| 命令 | 说明 |
|------|------|
| `python src/main.py` | 同步一次 |
| `python src/main.py -w` | 持续监控模式 |
| `python src/main.py --stats` | 显示统计信息 |
| `python src/main.py --search "关键词"` | 搜索消息 |
| `python src/main.py --export json` | 导出 JSON |
| `python src/main.py --export csv --source codex` | 导出指定来源 |
| `python src/main.py --prune` | 清理孤立记录 |

## 配置说明

### 环境变量（可选）

参考 `services/chat-vault/.env.example`：

```bash
# 自定义路径（逗号分隔多个）
CODEX_PATHS=~/.codex/sessions
KIRO_PATHS=~/.local/share/kiro-cli
GEMINI_PATHS=~/.gemini/tmp
CLAUDE_PATHS=~/.claude

# WSL 路径支持
CODEX_PATHS=\\wsl.localhost\Ubuntu\home\user\.codex\sessions
```

默认自动检测以下路径：
- Codex: `~/.codex/sessions`, `~/.codex`
- Kiro: `~/.local/share/kiro-cli`
- Gemini: `~/.gemini/tmp`, `~/.gemini`
- Claude: `~/.claude`

### 输出位置

- 数据库：`services/chat-vault/output/chat_history.db`
- 日志：`services/chat-vault/output/logs/`

## 数据库结构

详见 `services/chat-vault/docs/schema.md`

主表 `sessions`：
- `file_path` (PK): 源文件路径
- `session_id`: 会话 ID
- `source`: 来源 (codex/kiro/gemini/claude)
- `messages`: JSON 消息数组
- `token_count`: Token 数量

## FAQ

**Q: 需要配置吗？**
A: 不需要，自动检测默认路径。

**Q: 支持 WSL 吗？**
A: 支持，`\\wsl.localhost\Ubuntu\...` 格式路径会自动转换。

**Q: 数据安全吗？**
A: 只读取 AI 工具的文件，不修改原始数据。

## 贡献

欢迎提交 Issue 和 Pull Request。

## 许可证

MIT License
