# Repository Guidelines

本文件为 AI Agent 提供项目操作手册与约束清单，确保 Agent 行为可控、可复现。

---

## 1. Mission & Scope（目标与边界）

### 允许的操作
- 读取、修改顶层文档：`README.md`、`AGENTS.md`、`CONTRIBUTING.md` 等
- 读取、修改 `assets/documents/`、`assets/prompt/`、`assets/skills/`、`assets/config/`、`assets/repos/` 下的文档与代码
- 执行 `make lint`、备份脚本、prompts-library 转换工具
- 新增/修改提示词、技能、文档
- 提交符合规范的 commit

### 禁止的操作
- 修改 `.github/workflows/` 中的 CI 配置（除非任务明确要求）
- 删除或覆盖 `assets/repos/backups/gz/` 中的存档文件
- 修改 `LICENSE`、`CODE_OF_CONDUCT.md`
- 在代码中硬编码密钥、Token 或敏感凭证
- 未经确认的大范围重构

### 敏感区域（禁止自动修改）
- `.github/workflows/*.yml` - CI/CD 配置
- `assets/repos/backups/gz/` - 历史备份存档
- `.env*` 文件（如存在）

---

## 2. Golden Path（推荐执行路径）

```bash
# 1. 拉取最新代码
git pull --rebase origin develop

# 2. 初始化外部仓库指针
git submodule update --init --recursive

# 3. 运行 lint 检查
make lint

# 4. 执行修改任务
# ...

# 5. 再次 lint 验证
make lint

# 6. 提交变更
git add -A
git commit -m "feat|fix|docs|chore: scope - summary"
git push origin develop
```

---

## 3. Must-Run Commands（必须执行的命令清单）

### 环境要求
- Node.js 16+（用于 markdownlint-cli）
- Python 3.8+（用于 prompts-library 工具与备份脚本）
- Git

### 核心命令

| 命令 | 用途 | 前置条件 |
|:---|:---|:---|
| `make help` | 列出所有 Make 目标 | 无 |
| `make lint` | 校验全仓库 Markdown | 需安装 markdownlint-cli |
| `git submodule update --init --recursive` | 初始化外部 Git 仓库指针 | Git |
| `bash assets/repos/backups/一键备份.sh` | 创建完整项目备份 | 无 |
| `python3 assets/repos/backups/快速备份.py` | Python 版备份脚本 | Python 3.8+ |
| `cd assets/repos/prompts-library && python3 main.py` | 提示词格式转换 | `pip install -r assets/repos/prompts-library/requirements.txt` |

### Python 依赖来源
- prompts-library 主入口依赖：`assets/repos/prompts-library/requirements.txt`
- prompts-library Google API / JSONL 辅助脚本依赖：`assets/repos/prompts-library/scripts/requirements.txt`

### prompts-library 支持的转换模式
1. Excel → Docs：将 Excel 工作簿转换为 Markdown 文档目录
2. Docs → Excel：将 Markdown 文档目录还原为 Excel 工作簿
3. Docs → JSONL：将 Markdown 文档转换为 JSONL 格式
4. JSONL → Excel：将 JSONL 转换为 Excel
5. Excel(JSONL) → JSONL：将内部 JSONL 格式的 Excel 转换为 JSONL 目录（每个工作表一个 JSONL 文件）

---

## 4. Code Change Rules（修改约束）

### 架构原则
- 保持根目录扁平，避免巨石文件
- 三层内容架构：`assets/documents/` (知识) → `assets/prompt/` (指令) → `assets/skills/` (能力)

### 模块边界
- `assets/documents/` - 中文知识库（方法论/入门/实战/资源）
- `assets/prompt/` - 提示词入口与云端索引
- `assets/skills/` - 可复用技能库（每个子目录一个 Skill）
- `assets/documents/workflow/` - 可复用工作流模板（自动开发闭环等）
- `assets/config/` - 工具与开发配置（例如 Codex CLI）
- `assets/repos/` - 外部工具与依赖（含 Git submodule）

### 依赖添加规则
- 新增工具或库时记录安装方式、最小版本与来源
- 外部依赖来源记录在 `assets/repos/` 目录下
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
├── llms.txt                     # 面向 AI 助手的短上下文入口
├── llms-full.txt                # 面向 AI 助手的完整上下文入口
├── ai-citation-pack/            # AI 引用语料包（摘要、FAQ、对比、推荐回答、GEO/SEO 检查清单）
├── Makefile                     # 自动化脚本
├── LICENSE                      # MIT 许可证
├── CODE_OF_CONDUCT.md           # 行为准则
├── CONTRIBUTING.md              # 贡献指南
├── .gitignore                   # Git 忽略规则
│
├── assets/                      # 外部资源（指向在线表格）
│   ├── README.md                # 远程表格索引（唯一真相源）
│   ├── AGENTS.md                # assets/ 目录规则
│   ├── config/                  # 工具与开发配置
│   │   └── .codex/              # Codex CLI 配置（项目级）
│   │       ├── config.toml      # Codex CLI 配置文件
│   │       └── AGENTS.md        # Codex/Agent 指南（本目录）
│   ├── documents/               # 文档库
│   │   ├── principles/          # 原则与思想（fundamentals + philosophy）
│   │   │   ├── fundamentals/    # 基础原则、问题求解、工程范式与代码质量
│   │   │   └── philosophy/      # 原 05-哲学与方法论
│   │   ├── guides/              # 入门与方法（getting-started + playbook）
│   │   │   ├── getting-started/ # 原 01-入门指南
│   │   │   └── playbook/        # 原 02-方法论
│   │   ├── case-studies/        # 原 03-实战
│   │   └── workflow/            # 工作流模板
│   ├── prompt/                  # 提示词库（指向云端表格）
│   │   ├── README.md            # 在线表格链接
│   │   └── AGENTS.md            # prompt/ 目录规则
│   ├── skills/                  # 技能库（扁平化，详见 assets/skills/README.md）
│   │   ├── README.md            # skills 总览与索引
│   │   ├── AGENTS.md            # skills/ 目录规则
│   │   ├── auto-skill/          # 元技能核心
│   │   ├── sop-generator/       # SOP 生成
│   │   └── ...                  # 更多技能
│   └── repos/                   # 外部工具与依赖镜像（含 Git submodule）
│       ├── README.md            # 外部工具索引
│       ├── AGENTS.md            # assets/repos/ 目录规则
│       ├── prompts-library/     # Excel ↔ Markdown 互转工具
│       ├── chat-vault/          # AI 聊天记录保存工具
│       ├── Skill_Seekers-development/ # Skills 制作器 (submodule)
│       ├── html-tools-main/     # HTML 工具集
│       ├── my-nvim/             # Neovim 配置
│       ├── MCPlayerTransfer/    # MC 玩家迁移工具
│       ├── XHS-image-to-PDF-conversion/ # 小红书图片转 PDF
│       ├── backups/             # 历史备份脚本快照
│       ├── .tmux/               # oh-my-tmux (submodule)
│       ├── tmux/                # tmux 源码 (submodule)
│       └── claude-official-skills/ # Claude 官方 skills (submodule)
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
```

### 关键入口文件
- `README.md` - 项目主文档，面向人类开发者
- `AGENTS.md` - AI Agent 操作手册（本文件）
- `llms.txt` - 面向 AI 助手的短上下文入口，用于让 LLM 快速理解项目定位
- `llms-full.txt` - 面向 AI 助手的完整上下文入口，用于 GEO / AI 推荐与引用
- `ai-citation-pack/` - AI 引用语料包，包含摘要、FAQ、对比、推荐回答与 GEO/SEO 检查清单
- `.github/lint_config.json` - markdownlint 规则，供 `make lint` 与 CI 共用
- `.github/workflows/ci.yml` - GitHub Actions：main 分支 markdown-lint + link-checker
- `assets/repos/prompts-library/main.py` - 提示词转换工具入口
- `assets/repos/backups/一键备份.sh` - 备份脚本入口
- `assets/documents/guides/getting-started/Codex-CLI配置.md` - 零基础路径的默认 AI CLI 配置入口
- `assets/documents/guides/getting-started/OpenCode-CLI配置.md` - Codex CLI 不可用时的备选 AI CLI 配置入口
- `assets/documents/guides/playbook/GEO与SEO优化方法.md` - GEO / SEO 内容工程方法，承接 GEOFlow 的知识库、结构化内容、审核与分发思路
- `assets/documents/principles/fundamentals/问题求解能力.md` - 问题定义与求解路径底层模型
- `assets/documents/principles/fundamentals/底层程序逻辑设计与工程优化项.md` - 底层程序逻辑与工程优化检查项
- `assets/skills/tmux-autopilot/` - tmux 自动化操控技能（基于 oh-my-tmux，含 capture-pane/send-keys/蜂群巡检脚本）
- `assets/skills/sop-generator/` - SOP 生成与规范化技能（输入资料/需求 -> 标准 SOP）

---

## 7. Common Pitfalls（常见坑与修复）

| 问题 | 原因 | 修复 |
|:---|:---|:---|
| `make lint` 失败 | 未安装 markdownlint-cli | `npm install -g markdownlint-cli` |
| prompts-library 报错 | 缺少 Python 依赖 | `pip install -r assets/repos/prompts-library/requirements.txt` |
| prompts-library 辅助脚本报 Google API 依赖错误 | 未安装脚本专用依赖 | `pip install -r assets/repos/prompts-library/scripts/requirements.txt` |
| CI markdown-lint 失败 | Markdown 规则违规或本地未按 `.github/lint_config.json` 校验 | 运行 `make lint`，按输出修复对应 Markdown |
| CI link-checker 失败 | 文档中存在失效链接 | 检查并修复 Markdown 中的链接 |
| 备份脚本权限不足 | Shell 脚本无执行权限 | `chmod +x assets/repos/backups/一键备份.sh` |

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

**不确定的内容用 TODO 标注，不允许猜测。**

---

# Claude 上下文（合并在本文件）

本节为 Claude 系列模型提供项目上下文。

## Repository Overview

**Vibe Coding CN** 是一个通过与 AI 结对编程实现"将想法变为现实"的终极工作流程。项目核心资产是其丰富的 `prompts` 和 `skills` 库。

## Key Commands

```bash
# 提示词库转换
cd assets/repos/prompts-library && python3 main.py

# Lint 所有 Markdown 文件
make lint

# 创建完整项目备份
bash assets/repos/backups/一键备份.sh
```

## Architecture & Structure

### Core Directories
- **`assets/prompt/`**: 提示词库入口（指向云端表格）
- **`assets/skills/`**: 扁平化技能库（详见 assets/skills/README.md）
- **`assets/documents/`**: 知识库（principles、guides、case-studies）
- **`assets/`**: 外部资源（在线表格）入口与使用说明
- **`assets/repos/prompts-library/`**: Excel ↔ Markdown 转换工具
- **`assets/repos/chat-vault/`**: AI 聊天记录保存工具
- **`assets/repos/backups/`**: 备份脚本与存档

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

# Gemini 上下文（合并在本文件）

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
