# AGENTS.md

AI Agent 操作手册 - Chat Vault Monorepo

---

## 1. Mission & Scope（目标与边界）

### 允许操作
- 修改 `services/chat-vault/src/` 下的 Python 代码
- 添加新的解析器到 `services/chat-vault/src/parsers/`
- 更新文档 (`README.md`, `AGENTS.md`, `docs/`)
- 修改配置示例 `.env.example`

### 禁止操作
- **禁止修改** `output/` 目录下的任何文件（数据库、日志）
- **禁止修改** `.env` 文件（包含用户敏感配置）
- **禁止修改** `libs/external/` 下的外部依赖镜像
- **禁止删除** 现有解析器，除非明确要求

### 敏感区域
| 路径 | 说明 |
|------|------|
| `services/chat-vault/.env` | 用户配置，不得读取或修改 |
| `services/chat-vault/output/` | 运行时数据，不得修改 |
| `libs/external/` | 外部镜像，只读 |

---

## 2. Golden Path（推荐执行路径）

```bash
# 1. 进入服务目录
cd services/chat-vault

# 2. 首次运行（自动创建 venv 并安装依赖）
python src/main.py

# 3. 验证功能
python src/main.py --stats

# 4. 修改代码后测试
python src/main.py              # 同步测试
python src/main.py --search "test"  # 搜索测试

# 5. 更新文档（如有变更）
# 编辑 README.md, AGENTS.md, docs/schema.md
```

---

## 3. Must-Run Commands（必须执行的命令）

### 环境准备
```bash
cd services/chat-vault
python src/main.py  # 首次运行自动安装依赖
```

### 依赖文件
- `services/chat-vault/requirements.txt`
  ```
  python-dotenv>=1.0.0
  watchdog>=3.0.0
  tiktoken>=0.5.0
  ```

### 功能验证
```bash
# 同步一次
python src/main.py

# 查看统计
python src/main.py --stats

# 监控模式
python src/main.py --watch
```

---

## 4. Code Change Rules（修改约束）

### 架构原则
- 解析器必须继承 `parsers/base.py` 的 `SessionData` 数据结构
- 新增 CLI 支持需在 `parsers/__init__.py` 中导出
- 配置项通过 `config.py` 的 `CONFIG` 字典访问

### 模块边界
| 模块 | 职责 | 禁止 |
|------|------|------|
| `main.py` | CLI 入口、命令分发 | 不含业务逻辑 |
| `config.py` | 路径检测、配置加载 | 不含 I/O 操作 |
| `storage.py` | SQLite 读写、Token 计数 | 不含解析逻辑 |
| `watcher.py` | 文件监控 | 不含存储逻辑 |
| `parsers/*.py` | 各 CLI 格式解析 | 不含存储逻辑 |

### 依赖添加规则
- 新依赖必须添加到 `requirements.txt`
- 优先使用标准库
- 避免引入大型框架

### 兼容性要求
- Python 3.8+ 兼容
- 跨平台：Linux / macOS / Windows (WSL)
- WSL 路径格式：`\\wsl.localhost\Ubuntu\...`

---

## 5. Style & Quality（风格与质量）

### 代码风格
- 文件头：`#!/usr/bin/env python3` + `# -*- coding: utf-8 -*-`
- 缩进：4 空格
- 行宽：建议 100 字符
- 命名：snake_case（函数/变量），PascalCase（类）

### 文档要求
- 每个模块需有 docstring 说明用途
- 公开函数需有参数/返回值说明
- 复杂逻辑需有行内注释

### 错误处理
- 解析失败记录到日志，不中断流程
- 使用 `logger.py` 的 `get_logger()` 记录

---

## 6. Project Map（项目结构速览）

```
chat-vault/
├── services/chat-vault/       # 核心服务
│   ├── src/
│   │   ├── main.py           # 入口：CLI 命令分发
│   │   ├── config.py         # 配置：路径检测、环境变量
│   │   ├── storage.py        # 存储：SQLite + tiktoken
│   │   ├── watcher.py        # 监控：watchdog 封装
│   │   ├── logger.py         # 日志：统一日志配置
│   │   └── parsers/
│   │       ├── __init__.py   # 导出所有解析器
│   │       ├── base.py       # SessionData 数据结构
│   │       ├── codex.py      # Codex CLI 解析
│   │       ├── kiro.py       # Kiro CLI 解析
│   │       ├── gemini.py     # Gemini CLI 解析
│   │       └── claude.py     # Claude CLI 解析
│   ├── docs/
│   │   ├── schema.md         # 数据库结构文档
│   │   ├── roadmap.md        # 开发路线图
│   │   └── AI_PROMPT.md      # AI 助手指南
│   ├── requirements.txt      # Python 依赖
│   ├── .env.example          # 配置示例
│   ├── start.sh              # Linux/macOS 启动脚本
│   └── start.bat             # Windows 启动脚本
├── libs/                      # 共享库（预留）
├── monitoring/                # 监控配置（预留）
├── scripts/                   # 全局脚本
├── README.md                  # 项目说明
└── AGENTS.md                  # 本文件
```

### 关键入口
- **CLI 入口**: `services/chat-vault/src/main.py`
- **配置加载**: `services/chat-vault/src/config.py` → `CONFIG` 字典
- **数据库**: `services/chat-vault/output/chat_history.db`

---

## 7. Common Pitfalls（常见问题）

| 问题 | 原因 | 解决 |
|------|------|------|
| `ModuleNotFoundError` | 未在 venv 中运行 | 运行 `python src/main.py` 自动创建 venv |
| 路径未检测到 | 默认路径不存在 | 在 `.env` 中配置 `CODEX_PATHS` 等 |
| WSL 路径失败 | 格式错误 | 使用 `\\wsl.localhost\Ubuntu\...` 格式 |
| Token 计数为 0 | tiktoken 未安装 | 检查 `requirements.txt` 是否包含 tiktoken |
| 数据库锁定 | 多进程同时写入 | 确保只有一个实例运行 |

---

## 8. PR / Commit Rules（提交规则）

### Commit Message 格式
```
<type>(<scope>): <description>

type: feat|fix|docs|refactor|test|chore
scope: chat-vault|parsers|storage|config|docs
```

示例：
```
feat(parsers): add support for new CLI format
fix(storage): handle empty message array
docs(readme): update quick start section
```

### 分支策略
- `main`: 稳定版本
- `dev`: 开发分支
- `feature/*`: 功能分支

---

## 9. Documentation Sync Rule（文档同步规则）

### 强制同步
以下变更必须同步更新文档：

| 变更类型 | 需更新文档 |
|----------|-----------|
| 新增命令行参数 | README.md, AGENTS.md |
| 新增解析器 | README.md (功能特性), AGENTS.md (Project Map) |
| 数据库结构变更 | docs/schema.md |
| 配置项变更 | README.md (配置说明), .env.example |
| 目录结构变更 | README.md, AGENTS.md |

### 不确定时
- 使用 `TODO: 需确认 <具体问题>` 标注
- 不允许猜测或编造

---

## 10. Quick Reference（速查）

```bash
# 同步
python src/main.py

# 监控
python src/main.py --watch

# 统计
python src/main.py --stats

# 搜索
python src/main.py --search "关键词"

# 导出
python src/main.py --export json
python src/main.py --export csv --source codex

# 清理
python src/main.py --prune
```
