# Repository Guidelines

本文件为 AI Agent 提供项目操作手册与约束清单，确保 Agent 行为可控、可复现。

---

## 1. Mission & Scope（目标与边界）

### 允许的操作
- 读取、修改 `i18n/`、`libs/` 下的文档与代码
- 执行 `make lint`、备份脚本、prompts-library 转换工具
- 新增/修改提示词、技能、文档
- 提交符合规范的 commit

### 禁止的操作
- 修改 `.github/workflows/` 中的 CI 配置（除非任务明确要求）
- 删除或覆盖 `backups/gz/` 中的存档文件
- 修改 `LICENSE`、`CODE_OF_CONDUCT.md`
- 在代码中硬编码密钥、Token 或敏感凭证
- 未经确认的大范围重构

### 敏感区域（禁止自动修改）
- `.github/workflows/*.yml` - CI/CD 配置
- `backups/gz/` - 历史备份存档
- `.env*` 文件（如存在）

---

## 2. Golden Path（推荐执行路径）

```bash
# 1. 拉取最新代码
git pull origin main

# 2. 运行 lint 检查
make lint

# 3. 执行修改任务
# ...

# 4. 再次 lint 验证
make lint

# 5. 提交变更
git add -A
git commit -m "feat|fix|docs|chore: scope - summary"
git push
```

---

## 3. Must-Run Commands（必须执行的命令清单）

### 环境要求
- Node.js 16+（用于 markdownlint-cli）
- Python 3.8+（用于 prompts-library 工具）
- Git

### 核心命令

| 命令 | 用途 | 前置条件 |
|:---|:---|:---|
| `make help` | 列出所有 Make 目标 | 无 |
| `make lint` | 校验全仓库 Markdown | 需安装 markdownlint-cli |
| `bash backups/一键备份.sh` | 创建完整项目备份 | 无 |
| `python backups/快速备份.py` | Python 版备份脚本 | Python 3.8+ |
| `cd libs/external/prompts-library && python main.py` | 提示词格式转换 | pandas, openpyxl, PyYAML |

### prompts-library 支持的转换模式
1. Excel → Docs：将 Excel 工作簿转换为 Markdown 文档目录
2. Docs → Excel：将 Markdown 文档目录还原为 Excel 工作簿
3. Docs → JSONL：将 Markdown 文档转换为 JSONL 格式
4. JSONL → Excel：将 JSONL 转换为 Excel
5. Excel(JSONL) → JSONL：将内部 JSONL 格式的 Excel 转换为 JSONL 文件

---

## 4. Code Change Rules（修改约束）

### 架构原则
- 保持根目录扁平，避免巨石文件
- 多语言资产统一放在 `i18n/<lang>/` 下，遵循三层结构（documents / prompts / skills）
- 新增语言遵循现有目录层级

### 模块边界
- `i18n/zh/` - 中文主语料（默认）
- `i18n/en/` - 英文版本
- `libs/common/` - 通用模块
- `libs/external/` - 外部工具与依赖

### 依赖添加规则
- 新增工具或库时记录安装方式、最小版本与来源
- 外部依赖来源记录在 `libs/external/` 目录下
- 引入第三方脚本需标明许可证与来源

### 禁止行为
- 禁止"顺手重构/大范围改动"除非任务明确要求
- 禁止删除现有测试用例（除非任务要求）
- 禁止在代码中硬编码敏感信息

---

## 5. Style & Quality（风格与质量标准）

### 格式化工具
- Markdown：`markdownlint-cli`（通过 `make lint` 执行）
- CI 自动检查：`.github/workflows/ci.yml`

### 命名约定
- 文档、注释、日志使用中文
- 代码符号统一英文且语义直白
- 文件名小写加中划线或下划线

### 缩进与排版
- 全仓保持空格缩进（2 或 4 空格不混用）
- 行宽控制在 120 列内

### 设计品味
- 优先消除分支与重复
- 函数单一职责且短小

---

## 6. Project Map（项目结构速览）

```
.
├── README.md                    # 项目主文档
├── AGENTS.md                    # AI Agent 行为准则（本文件）
├── CLAUDE.md                    # Claude 模型上下文（合并在本文件末尾）
├── GEMINI.md                    # Gemini 模型上下文
├── Makefile                     # 自动化脚本
├── LICENSE                      # MIT 许可证
├── CODE_OF_CONDUCT.md           # 行为准则
├── CONTRIBUTING.md              # 贡献指南
├── .gitignore                   # Git 忽略规则
│
├── .github/                     # GitHub 配置
│   ├── workflows/               # CI/CD 工作流
│   │   ├── ci.yml               # Markdown lint + link checker
│   │   ├── labeler.yml          # 自动标签
│   │   └── welcome.yml          # 欢迎新贡献者
│   ├── ISSUE_TEMPLATE/          # Issue 模板
│   ├── PULL_REQUEST_TEMPLATE.md # PR 模板
│   ├── SECURITY.md              # 安全政策
│   ├── FUNDING.yml              # 赞助配置
│   └── wiki/                    # GitHub Wiki 内容
│
├── i18n/                        # 多语言资产 (27 种语言)
│   ├── README.md                # 多语言索引
│   ├── zh/                      # 中文主语料
│   │   ├── documents/           # 文档库
│   │   │   ├── -01-哲学与方法论/ # 最高思想纲领与方法论
│   │   │   ├── 00-基础指南/     # 核心原则与底层逻辑
│   │   │   ├── 01-入门指南/     # 从零开始教程
│   │   │   ├── 02-方法论/       # 具体工具与技巧
│   │   │   ├── 03-实战/         # 项目实战案例
│   │   │   └── 04-资源/         # 外部资源聚合
│   │   ├── prompts/             # 提示词库
│   │   │   ├── 00-元提示词/     # 生成提示词的提示词
│   │   │   ├── 01-系统提示词/   # AI 系统级提示词
│   │   │   ├── 02-编程提示词/   # 编程相关提示词
│   │   │   └── 03-用户提示词/   # 用户自定义提示词
│   │   └── skills/              # 技能库
│   │       ├── 00-元技能/       # 生成技能的元技能
│   │       │   ├── claude-skills/ # 元技能核心
│   │       │   └── sop-generator/ # SOP 生成与规范化技能
│   │       ├── 01-AI工具/       # AI CLI 和工具
│   │       ├── 02-数据库/       # 数据库技能
│   │       ├── 03-加密货币/     # 加密货币/量化交易
│   │       └── 04-开发工具/     # 通用开发工具
│   ├── en/                      # 英文版本（结构同 zh/）
│   └── ...                      # 其他语言骨架
│
├── libs/                        # 核心库代码
│   ├── common/                  # 通用模块
│   │   ├── models/              # 模型定义
│   │   └── utils/               # 工具函数
│   ├── database/                # 数据库模块（预留）
│   └── external/                # 外部工具
│       ├── prompts-library/     # Excel ↔ Markdown 互转工具
│       ├── chat-vault/          # AI 聊天记录保存工具
│       ├── Skill_Seekers-development/ # Skills 制作器
│       ├── html-tools-main/     # HTML 工具集（Markdown 编辑器、任务卡片生成等）
│       ├── l10n-tool/           # 多语言翻译脚本
│       ├── my-nvim/             # Neovim 配置
│       ├── MCPlayerTransfer/    # MC 玩家迁移工具
│       └── XHS-image-to-PDF-conversion/ # 小红书图片转 PDF
│
└── backups/                     # 备份脚本与存档
    ├── 一键备份.sh              # Shell 备份脚本
    ├── 快速备份.py              # Python 备份脚本
    ├── README.md                # 备份说明
    └── gz/                      # 压缩存档目录
```

### 关键入口文件
- `README.md` - 项目主文档，面向人类开发者
- `AGENTS.md` - AI Agent 操作手册（本文件）
- `libs/external/prompts-library/main.py` - 提示词转换工具入口
- `backups/一键备份.sh` - 备份脚本入口
- `i18n/zh/skills/04-开发工具/tmux-autopilot/` - tmux 自动化操控技能（基于 oh-my-tmux，含 capture-pane/send-keys/蜂群巡检脚本）
- `i18n/zh/skills/00-元技能/sop-generator/` - SOP 生成与规范化技能（输入资料/需求 -> 标准 SOP）

---

## 7. Common Pitfalls（常见坑与修复）

| 问题 | 原因 | 修复 |
|:---|:---|:---|
| `make lint` 失败 | 未安装 markdownlint-cli | `npm install -g markdownlint-cli` |
| prompts-library 报错 | 缺少 Python 依赖 | `pip install pandas openpyxl PyYAML rich InquirerPy` |
| CI link-checker 失败 | 文档中存在失效链接 | 检查并修复 Markdown 中的链接 |
| 备份脚本权限不足 | Shell 脚本无执行权限 | `chmod +x backups/一键备份.sh` |

---

## 8. PR / Commit Rules（提交与 CI 规则）

### Commit 规范
遵循简化 Conventional Commits：
```
feat|fix|docs|chore|refactor|test: scope - summary
```

示例：
- `docs: prompts - add new coding prompt`
- `feat: skills - add postgresql skill`
- `fix: readme - correct broken link`

### PR 必填内容
- 变更摘要
- 动机或关联 Issue
- 测试与验证步骤

### CI 触发条件
- `push` 到 `main` 分支
- `pull_request` 到 `main` 分支

### CI 检查项
1. `markdown-lint` - Markdown 格式检查
2. `link-checker` - 链接有效性检查

### 提交前清单
- [ ] 运行 `make lint` 通过
- [ ] 更新对应文档
- [ ] 确认不携带临时文件或机密数据

---

## 9. Documentation Sync Rule（强制同步规则）

**任何功能/命令/配置/目录/工作流变化必须同步更新：**
- `README.md` - 面向人类开发者
- `AGENTS.md` - 面向 AI Agent（本文件）
- `GEMINI.md` - Gemini 模型上下文

**不确定的内容用 TODO 标注，不允许猜测。**

---

# CLAUDE.md

本节为 Claude 系列模型提供项目上下文。

## Repository Overview

**Vibe Coding CN** 是一个通过与 AI 结对编程实现"将想法变为现实"的终极工作流程。项目核心资产是其丰富的 `prompts` 和 `skills` 库。

## Key Commands

```bash
# 提示词库转换
cd libs/external/prompts-library && python3 main.py

# Lint 所有 Markdown 文件
make lint

# 创建完整项目备份
bash backups/一键备份.sh
```

## Architecture & Structure

### Core Directories
- **`i18n/zh/prompts/`**: 核心提示词库（00-元提示词、01-系统提示词、02-编程提示词、03-用户提示词）
- **`i18n/zh/skills/`**: 模块化技能库（00-元技能、01-AI工具、02-数据库、03-加密货币、04-开发工具）
- **`i18n/zh/documents/`**: 知识库（-01-哲学与方法论、00-基础指南、01-入门指南、02-方法论、03-实战、04-资源）
- **`libs/external/prompts-library/`**: Excel ↔ Markdown 转换工具
- **`libs/external/chat-vault/`**: AI 聊天记录保存工具
- **`backups/`**: 备份脚本与存档

### Key Technical Details
1. **Prompt Organization**: 提示词使用 `(row,col)_` 前缀进行分类
2. **Conversion Tool**: 使用 Python + pandas + openpyxl
3. **Documentation Standard**: 用户文档使用中文；代码/文件名使用英文
4. **Skills**: 每个技能有独立的 `SKILL.md`

## Development Workflow

1. 遵循现有的提示词和技能分类系统
2. 使用 `prompts-library` 工具进行提示词更新
3. Markdown 修改后运行 `make lint`
4. 重大重构前运行备份脚本

---

# GEMINI.md - 项目上下文文档

## 项目概述

`vibe-coding-cn` 是一个通过与 AI 结对编程实现"将想法变为现实"的终极工作流程。强调"规划驱动"和"模块化"核心理念。

## 技术栈

- **核心语言:** Python
- **CLI 交互:** `rich`, `InquirerPy`
- **数据处理:** `pandas`, `openpyxl`
- **配置管理:** `PyYAML`
- **文档规范:** `markdownlint-cli`
- **版本控制:** Git
- **自动化:** Makefile

## 文件结构

详见上方 Project Map 章节。
