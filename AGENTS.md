# Repository Guidelines

本文件为 AI Agent 提供项目操作手册与约束清单，确保 Agent 行为可控、可复现。

---

## 1. Mission & Scope（目标与边界）

### 允许的操作
- 读取、修改顶层文档：`README.md`、`AGENTS.md`、`CONTRIBUTING.md` 等
- 读取、修改 `docs/`、`prompts/`、`skills/`、`tools/config/`、`tools/external/` 下的文档与代码
- 执行 `make lint`、`make check-links`、`make check-details`、`make check-doc-structure`、`make check-directory-docs`、`make check-metadata`、`make check-ai-citation`、`make sync-doc-toc`、`make sync-reference-readme`、prompts-library 转换工具
- 新增/修改提示词、技能、文档
- 提交符合规范的 commit

### 禁止的操作
- 修改 `.github/workflows/` 中的 CI 配置（除非任务明确要求）
- 修改 `LICENSE`、`CODE_OF_CONDUCT.md`
- 在代码中硬编码密钥、Token 或敏感凭证
- 未经确认的大范围重构

### 敏感区域（禁止自动修改）
- `.github/workflows/*.yml` - CI/CD 配置
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
- Node.js 22+（通过 `npx --yes markdownlint-cli@0.48.0` 运行固定版本 Markdown lint）
- Python 3.8+（用于 prompts-library 工具与链接检查脚本）
- Git

### 核心命令

| 命令 | 用途 | 前置条件 |
|:---|:---|:---|
| `make help` | 列出所有 Make 目标 | 无 |
| `make lint` | 校验全仓库 Markdown | Node.js 22+；通过 `npx --yes markdownlint-cli@0.48.0` 执行 |
| `make check-links` | 校验仓库内 Markdown 相对链接 | Python 3 |
| `make check-details` | 校验 Markdown 折叠块 `<details>/<summary>` 结构 | Python 3 |
| `make check-doc-structure` | 校验 docs 线性 README 主章节顺序、重复锚点与目录入口 | Python 3 |
| `make check-directory-docs` | 校验仓库自有目录 README/AGENTS 覆盖 | Python 3 |
| `make check-metadata` | 校验 metadata 路径与锚点 | Python 3 |
| `make check-ai-citation` | 校验 llms 与 AI 引用语料路径和锚点 | Python 3 |
| `make sync-doc-toc` | 根据 taxonomy 和文档锚点重建 docs 细粒度目录 | Python 3 |
| `make sync-reference-readme` | 从 `docs/references/sources/` 重建 references 线性总文档 | Python 3 |
| `make check-reference-readme` | 校验 references 线性总文档是否由源片段生成且无漂移 | Python 3 |
| `make test` | 执行本地质量门禁 | Node.js 22+、Python 3 |
| `git submodule update --init --recursive` | 初始化外部 Git 仓库指针 | Git |
| `cd tools/prompts-library && python3 main.py` | 提示词格式转换 | `pip install -r tools/prompts-library/requirements.txt` |

### Python 依赖来源
- prompts-library 主入口依赖：`tools/prompts-library/requirements.txt`
- prompts-library Google API / JSONL 辅助脚本依赖：`tools/prompts-library/scripts/requirements.txt`

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
- 三层内容架构：`docs/` (知识) → `prompts/` (指令) → `skills/` (能力)

### 模块边界
- `docs/` - 中文知识库（方法论/入门/实战/资源）
- `prompts/` - 提示词入口与云端索引
- `skills/` - 可复用技能库（每个子目录一个 Skill）
- `tools/config/` - 工具与开发配置（例如 Codex CLI）
- `tools/external/` - 外部工具与依赖（含 Git submodule）

### 依赖添加规则
- 新增工具或库时记录安装方式、最小版本与来源
- 外部依赖来源记录在 `tools/external/` 目录下
- 引入第三方脚本需标明许可证与来源

### 禁止行为
- 禁止"顺手重构/大范围改动"除非任务明确要求
- 禁止删除现有测试用例（除非任务要求）
- 禁止在代码中硬编码敏感信息

---

## 5. Style & Quality（风格与质量标准）

### 格式化工具
- Markdown：`Makefile` 固定调用 `markdownlint-cli@0.48.0`（通过 `make lint` 执行）
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
├── Makefile                     # 自动化脚本
├── LICENSE                      # MIT 许可证
├── CODE_OF_CONDUCT.md           # 行为准则
├── CONTRIBUTING.md              # 贡献指南
├── .gitattributes               # GitHub Linguist 语言统计规则
├── .gitignore                   # Git 忽略规则
│
├── docs/                        # 核心知识库
│   ├── README.md                # docs 总索引
│   ├── getting-started/         # 从零开始、学习地图、环境与 AI CLI 配置
│   ├── concepts/                # 核心概念、方法论与工程思想
│   ├── philosophy/              # 哲学方法论、思维模型与底层认知模型
│   ├── references/              # 清单、约束、常见坑、模板（README 由 sources/ 生成）
│   └── research/                # 新技术、优秀 repo 与工程范式研究
│
├── prompts/                     # 提示词库入口（指向云端表格）
│   ├── README.md                # 在线表格链接
│   └── AGENTS.md                # prompts/ 目录规则
│
├── skills/                      # 技能库（每个子目录一个 Skill）
│   ├── README.md                # skills 总览与索引
│   ├── AGENTS.md                # skills/ 目录规则
│   ├── auto-skill/              # 元技能核心
│   └── claude-official-skills/  # Claude 官方 skills 软链接入口
│
├── assets/                      # 静态资产与外部资源入口
│   ├── README.md                # 外部资源在线表格入口
│   ├── AGENTS.md                # assets/ 目录规则
│   ├── ai-citation/             # AI 引用语料包与 llms-full
│   ├── images/                  # 图片资产
│   ├── templates/               # 模板附件
│   └── datasets/                # 示例数据或数据说明
│
├── scripts/                     # 自动化脚本
│   ├── README.md                # scripts 目录说明
│   ├── AGENTS.md                # scripts 目录规则
│   └── check-local-links.py     # Markdown 相对链接检查
│
├── tools/                       # 工具、本地配置与外部仓库
│   ├── README.md                # tools 目录说明
│   ├── AGENTS.md                # tools 目录规则
│   ├── config/                  # 工具与开发配置（含 Codex CLI）
│   ├── prompts-library/         # Excel ↔ Markdown 互转工具
│   ├── chat-vault/              # AI 聊天记录保存工具
│   └── external/                # 外部工具与 Git submodule
│       ├── AGENTS.md            # external 目录规则
│       ├── README.md            # 外部工具索引
│       ├── Skill_Seekers-development/ # Skills 制作器 (submodule)
│       ├── .tmux/               # oh-my-tmux (submodule)
│       ├── tmux/                # tmux 源码 (submodule)
│       └── claude-official-skills/ # Claude 官方 skills (submodule)
│
├── metadata/                    # 机器可读索引
│   ├── README.md                # metadata 目录说明
│   ├── AGENTS.md                # metadata 目录规则
│   ├── taxonomy.yml             # 分类体系
│   ├── glossary.yml             # 术语表
│   └── redirects.yml            # 重命名/迁移映射
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
│   └── WIKI.md                  # GitHub Wiki 独立仓库说明
```

### 关键入口文件
- `README.md` - 项目主文档，面向人类开发者
- `AGENTS.md` - AI Agent 操作手册（本文件）
- `llms.txt` - 面向 AI 助手的短上下文入口，用于让 LLM 快速理解项目定位
- `assets/ai-citation/llms-full.txt` - 面向 AI 助手的完整上下文入口，用于 GEO / AI 推荐与引用
- `assets/ai-citation/` - AI 引用语料包，包含摘要、FAQ、对比、推荐回答与 GEO/SEO 检查清单
- `.gitattributes` - GitHub Linguist 语言统计规则，当前将 `tools/external/**` 标记为 vendored
- `.github/lint_config.json` - markdownlint 规则，供 `make lint` 与 CI 共用
- `.github/workflows/ci.yml` - GitHub Actions：develop/master 分支 markdown-lint + link-checker
- `scripts/check-local-links.py` - 仓库内 Markdown 相对链接与锚点检查脚本，供 `make check-links` 与 CI 使用
- `scripts/check-markdown-details.py` - 仓库内 Markdown 折叠块结构检查脚本，供 `make check-details` 与 CI 使用
- `scripts/check-doc-structure.py` - docs 线性 README 主章节顺序、重复锚点与目录入口检查脚本，供 `make check-doc-structure` 与 CI 使用
- `scripts/check-directory-docs.py` - 仓库自有目录 README/AGENTS 覆盖检查脚本，供 `make check-directory-docs` 与 CI 使用
- `scripts/check-metadata.py` - metadata 路径与锚点检查脚本，供 `make check-metadata` 与 CI 使用
- `scripts/check-ai-citation.py` - llms 与 AI 引用语料路径和锚点检查脚本，供 `make check-ai-citation` 与 CI 使用
- `scripts/sync-doc-toc.py` - docs 线性 README 细粒度目录重建脚本，供 `make sync-doc-toc` 使用
- `scripts/build-reference-readme.py` - references 线性总文档生成与漂移检查脚本，供 `make sync-reference-readme` 与 `make check-reference-readme` 使用
- `tools/prompts-library/main.py` - 提示词转换工具入口
- `docs/getting-started/README.md` - 从零开始完整入门，包含学习地图、Vibe Coding 经验、网络配置、CLI 配置与开发环境搭建
- `docs/concepts/README.md#concept-problem-solving` - 问题定义与求解路径底层模型
- `docs/references/README.md#reference-engineering-practice` - 项目架构、代码组织、开发经验、底层程序逻辑、AI 编程质量门禁与常见坑的统一入口
- `docs/references/README.md#reference-technology-stack` - 常见软件系统技术栈、选型维度、组合案例与初学者学习路径
- `skills/auto-skill/` - Skills 生成、重构与校验的元技能

---

## 7. Common Pitfalls（常见坑与修复）

| 问题 | 原因 | 修复 |
|:---|:---|:---|
| `make lint` 失败 | Node.js 不可用、npx 无法拉取 markdownlint-cli 或 Markdown 规则违规 | 先确认 `node -v` 为 22+，再运行 `make lint` |
| prompts-library 报错 | 缺少 Python 依赖 | `pip install -r tools/prompts-library/requirements.txt` |
| prompts-library 辅助脚本报 Google API 依赖错误 | 未安装脚本专用依赖 | `pip install -r tools/prompts-library/scripts/requirements.txt` |
| CI markdown-lint 失败 | Markdown 规则违规或本地未按 `.github/lint_config.json` 校验 | 运行 `make lint`，按输出修复对应 Markdown |
| CI link-checker 失败 | 文档中存在失效链接 | 检查并修复 Markdown 中的链接 |

---

## 8. PR / Commit Rules（提交与 CI 规则）

### Commit 规范
遵循简化 Conventional Commits：
```
feat|fix|docs|chore|refactor|test: scope - summary
```

示例：
- `docs: prompts - add new coding prompt`
- `feat: skills - add custom skill`
- `fix: readme - correct broken link`

### PR 必填内容
- 变更摘要
- 动机或关联 Issue
- 测试与验证步骤

### CI 触发条件
- `push` 到 `develop` 或 `master` 分支
- `pull_request` 到 `develop` 或 `master` 分支
- 手动触发 `workflow_dispatch`

### CI 检查项
1. `markdown-lint` - Markdown 格式检查
2. `check local markdown links and anchors` - 仓库内相对链接与锚点检查
3. `check markdown details and summaries` - Markdown 折叠块结构检查
4. `check references README generated state` - references 总文档生成状态检查
5. `check docs README structure` - docs 线性 README 主章节顺序、重复锚点与目录入口检查
6. `check required directory README and AGENTS files` - 仓库自有目录 README/AGENTS 覆盖检查
7. `check metadata paths and anchors` - metadata 路径与锚点检查
8. `check llms and AI citation paths and anchors` - llms 与 AI 引用语料路径和锚点检查
9. `link-checker` - 链接有效性检查

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
cd tools/prompts-library && python3 main.py

# Lint 所有 Markdown 文件
make lint

# 本地质量门禁
make test

```

## Architecture & Structure

### Core Directories
- **`prompts/`**: 提示词库入口（指向云端表格）
- **`skills/`**: 扁平化技能库（详见 skills/README.md）
- **`docs/`**: 知识库（getting-started、concepts、philosophy、references）
- **`assets/`**: 外部资源（在线表格）入口与使用说明
- **`assets/ai-citation/`**: AI 引用语料包与 `llms-full.txt`
- **`tools/prompts-library/`**: Excel ↔ Markdown 转换工具
- **`tools/chat-vault/`**: AI 聊天记录保存工具

### Key Technical Details
1. **Prompt Organization**: 提示词使用 `(row,col)_` 前缀进行分类
2. **Conversion Tool**: 使用 Python + pandas + openpyxl
3. **Documentation Standard**: 用户文档使用中文；代码/文件名使用英文
4. **Skills**: 每个技能有独立的 `SKILL.md`
5. **Quality Gates**: `make test` 执行 Markdown lint、本地相对链接/锚点检查、折叠块结构检查、references 生成状态检查、metadata 路径检查与 AI 引用路径检查

## Development Workflow

1. 遵循现有的提示词和技能分类系统
2. 使用 `prompts-library` 工具进行提示词更新
3. Markdown 修改后运行 `make test`
4. 重大重构前先确认 Git 状态，并必要时创建 checkpoint commit

---

# Gemini 上下文（合并在本文件）

## 项目概述

`vibe-coding-cn` 是一个通过与 AI 结对编程实现"将想法变为现实"的中文 Vibe Coding 从入门到精通教程。强调"规划驱动"、"模块化"、"上下文固定"与"质量门禁"。

## 技术栈

- **核心形态:** Markdown 知识库 + Python 工具脚本
- **提示词转换工具:** `tools/prompts-library/`
- **数据处理:** `pandas`, `openpyxl`（prompts-library）
- **配置管理:** `PyYAML`（prompts-library）
- **文档规范:** `Makefile` 固定调用的 `markdownlint-cli@0.48.0`
- **版本控制:** Git
- **自动化:** Makefile

## 文件结构

详见上方 Project Map 章节。
