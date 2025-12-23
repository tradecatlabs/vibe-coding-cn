# Repository Guidelines

## Project Structure & Module Organization
- 根目录：`README.md` 给出全貌，`Makefile` 封装日常命令，`CONTRIBUTING.md` 说明贡献流程，`LICENSE` 载明协议。保持根目录扁平，避免巨石文件。
- 多语言 i18n：`i18n/<lang>/` 统一三层结构（documents / prompts / skills）。现有语言：中文 `zh`、英文 `en`、希伯来语 `he`，以及 `es`、`hi`、`ar`、`pt`、`ru`、`fr`、`de`、`ja`、`ko`、`it`、`tr`、`nl`、`pl`、`id`、`vi`、`th`、`fa`、`uk`、`bn`、`ta`、`ur`、`ms`、`sw`、`ha`；新增语言遵循同样层级。
- 文档库：`i18n/zh/documents/` 是默认中文方法论入口，含子目录：`方法论与原则/`、`模板与资源/`、`教程与指南/`、`外部资源聚合/`、`胶水编程/`、`从零开始vibecoding/` 等。
- 提示词资产：`i18n/zh/prompts/` 按角色拆分（`system_prompts/`、`assistant_prompts/`、`coding_prompts/`、`user_prompts/`、`meta_prompts/`），`libs/external/prompts-library/` 提供 Excel ↔ Markdown 互转工具。
- 技能库：`i18n/zh/skills/` 包含模块化技能集，如 `ccxt/`、`postgresql/`、`telegram-dev/`、`claude-code-guide/`、`ddd-doc-steward/`、`claude-skills/` 等 17+ 个技能目录。
- 代码与集成：`libs/` 预留核心实现骨架，`common/`（含 `models/`、`utils/`）、`database/`、`external/` 分别对应通用模型、存储适配与外部依赖。
- 外部工具：`libs/external/` 含 `prompts-library/`、`l10n-tool/`、`my-nvim/`、`MCPlayerTransfer/`、`XHS-image-to-PDF-conversion/` 等。
- 备份：`backups/` 内含 `一键备份.sh`、`快速备份.py` 和 `gz/` 存档目录。
- 脚本：`scripts/` 目录预留项目脚本。
- GitHub 配置：`.github/` 含 `ISSUE_TEMPLATE/`、`PULL_REQUEST_TEMPLATE.md`、`SECURITY.md`、`FUNDING.yml`。

## Build, Test, and Development Commands
- `make help`：列出所有 Make 目标。
- `make lint`：使用 `markdownlint-cli` 校验全仓库 Markdown。
- `make build` / `make test` / `make clean`：目前为占位。
- 提示词转换：`cd libs/external/prompts-library && python main.py`。
- JSONL 批处理（Gemini）：`python libs/external/prompts-library/scripts/gemini_jsonl_batch.py --input 2 --output 2/prompts.jsonl`。
- 备份：`bash backups/一键备份.sh` 或 `python backups/快速备份.py`。

## Coding Style & Naming Conventions
- 文字层：文档、注释、日志使用中文；代码符号统一英文且语义直白。
- 缩进与排版：全仓保持空格缩进（2 或 4 空格不混用）；行宽控制在 120 列内。
- 设计品味：优先消除分支与重复；函数单一职责且短小；命名小写加中划线或下划线。
- 依赖管理：新增工具或库时记录安装方式、最小版本与来源。

## Testing Guidelines
- 当前无实测用例；引入代码时请至少提供最小可复现测试。
- 文档与提示词改动：提交前运行 `make lint`。
- 覆盖率基线由模块维护者设定。

## Commit & Pull Request Guidelines
- Commit 遵循简化 Conventional Commits：`feat|fix|docs|chore|refactor|test: scope – summary`。
- PR 必填：变更摘要、动机或关联 Issue、测试与验证步骤。
- 提交前清单：跑通 `make lint`；更新对应文档与 `Makefile` 目标；确认不携带临时文件或机密数据。

## Security & Configuration Tips
- 运行备份或转换脚本前，确认输出目录不会覆盖私有数据。
- 外部依赖来源记录在 `libs/external/` 目录下，引入第三方脚本需标明许可证与来源。

## Architecture Overview & Workflow
- 工作流倡导「规划 → 上下文固定 → 分步实现 → 自测 → 复盘」。
- 设计决策与目录结构更新后，请同步修订本文件与相关文档。

---

# CLAUDE.md

This file provides guidance to Claude series models when working with code in this repository.

## Repository Overview

This is the **Vibe Coding CN** repository, a workflow, toolset, and knowledge base for advanced AI-assisted programming. The project's core assets are its extensive `prompts` and `skills` libraries.

## Key Commands

```bash
# Prompt library conversion
cd libs/external/prompts-library && python3 main.py

# Lint all markdown files
make lint

# Create a full project backup
bash backups/一键备份.sh
```

## Architecture & Structure

### Core Directories
- **`i18n/zh/prompts/`**: Core prompt library (`coding_prompts/`, `system_prompts/`, `user_prompts/`, `assistant_prompts/`, `meta_prompts/`)
- **`i18n/zh/skills/`**: Modular skills library (16+ skills including `ccxt`, `postgresql`, `telegram-dev`, `claude-skills`)
- **`i18n/zh/documents/`**: Knowledge base (`方法论与原则/`, `模板与资源/`, `教程与指南/`, `胶水编程/`, `从零开始vibecoding/`)
- **`libs/external/prompts-library/`**: Excel ↔ Markdown conversion tool
- **`libs/external/`**: External tools (`l10n-tool/`, `my-nvim/`, `MCPlayerTransfer/`)
- **`backups/`**: Backup scripts and archives
- **`scripts/`**: Project scripts placeholder

### Key Technical Details
1. **Prompt Organization**: Prompts use `(row,col)_` prefix for categorization.
2. **Conversion Tool**: Uses Python with `pandas` and `openpyxl`.
3. **Documentation Standard**: User-facing docs in Chinese; code/filenames in English.
4. **Skills**: Each skill has its own `SKILL.md`.

## Development Workflow

1. Follow existing prompt and skill categorization systems.
2. Use `prompts-library` tool for prompt updates.
3. Run `make lint` after Markdown changes.
4. Run backup before major refactoring.

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

```
.
├── .github/                     # GitHub 配置 (Issue/PR 模板, SECURITY, FUNDING)
├── AGENTS.md                    # AI Agent 行为准则
├── CLAUDE.md                    # Claude 模型上下文
├── GEMINI.md                    # Gemini 模型上下文
├── CODE_OF_CONDUCT.md           # 行为准则
├── CONTRIBUTING.md              # 贡献指南
├── LICENSE                      # MIT 许可证
├── Makefile                     # 自动化脚本
├── README.md                    # 项目主文档
│
├── i18n/                        # 多语言资产 (29 种语言)
│   ├── zh/                      # 中文主语料
│   │   ├── documents/           # 文档库 (方法论/模板/教程/胶水编程等)
│   │   ├── prompts/             # 提示词库 (system/coding/user/assistant/meta)
│   │   └── skills/              # 技能库 (16+ 技能)
│   ├── en/                      # 英文版本
│   └── ...                      # 其他语言骨架
│
├── libs/                        # 核心库代码
│   ├── common/                  # 通用模块 (models/, utils/)
│   ├── database/                # 数据库模块
│   └── external/                # 外部工具
│       ├── prompts-library/     # Excel-Markdown 互转工具
│       ├── l10n-tool/           # 多语言翻译脚本
│       ├── my-nvim/             # Neovim 配置
│       ├── MCPlayerTransfer/    # MC 玩家迁移工具
│       └── XHS-image-to-PDF-conversion/
│
├── backups/                     # 备份脚本与存档
│   ├── 一键备份.sh
│   ├── 快速备份.py
│   └── gz/                      # 压缩存档
│
└── scripts/                     # 项目脚本
```
