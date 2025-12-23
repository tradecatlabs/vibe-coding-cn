# 💡 AI 提示词库 (Prompts)

> ⚠️ **最新提示词请访问网页版表格**：[📋 提示词在线表格](https://docs.google.com/spreadsheets/d/1Ifk_dLF25ULSxcfGem1hXzJsi7_RBUNAki8SBCuvkJA/edit?gid=1254297203#gid=1254297203)
>
> 本目录为离线备份，网页版表格持续更新，内容更全面。

---

`i18n/zh/prompts/` 存放本仓库的提示词资产：用 **01-系统提示词** 约束 AI 的边界与品味，用 **任务提示词** 驱动「需求澄清 → 计划 → 执行 → 复盘」的开发流水线。

## 推荐使用路径（从 0 到可控）

1. **先定边界**：选择一个01-系统提示词版本（推荐 `v8` 或 `v10`）。
2. **再跑流程**：在具体任务里按阶段选用 `02-编程提示词/`（澄清 / 计划 / 执行 / 复盘）。
3. **最后产品化**：当你在某领域反复做同类工作，把「提示词 + 资料」升级为 `skills/` 里的 Skill（更可复用、更稳定）。

## 目录结构（以仓库真实目录为准）

```
i18n/zh/prompts/
├── README.md
├── 02-编程提示词/                 # 编程/研发提示词（当前 41 个 .md）
│   ├── index.md                    # 自动生成的索引与版本矩阵（请勿手改）
│   ├── 标准化流程.md
│   ├── 项目上下文文档生成.md
│   ├── 智能需求理解与研发导航引擎.md
│   └── ...
├── 01-系统提示词/                 # 01-系统提示词（CLAUDE 多版本 + 其他收集）
│   ├── CLAUDE.md/                  # 1~10 版本目录（v9 目前仅占位）
│   │   ├── 1/CLAUDE.md
│   │   ├── 2/CLAUDE.md
│   │   ├── ...
│   │   ├── 9/AGENTS.md             # v9 当前没有 CLAUDE.md
│   │   └── 10/CLAUDE.md
│   └── system-prompts-and-models-of-ai-tools-main-cn/  # AI 工具01-系统提示词（中文翻译版）
│       ├── Anthropic/              # Claude Code 等
│       ├── Cursor Prompts/         # Cursor Agent/Chat
│       ├── Windsurf/               # Windsurf Wave 11
│       ├── VSCode Agent/           # VS Code Copilot
│       ├── Kiro/                   # Kiro Vibe/Spec 模式
│       └── ...                     # 更多 AI 工具提示词
└── 03-用户提示词/                   # 用户自用/一次性提示词
    ├── ASCII图生成.md
    ├── 数据管道.md
    └── 项目变量与工具统一维护.md
```

## `01-系统提示词/`：系统级提示词（先把 AI 变“可控”）

01-系统提示词用于定义 **工作模式、代码品味、输出格式、安全边界**。目录采用版本化结构：

- 路径约定：`i18n/zh/prompts/01-系统提示词/CLAUDE.md/<版本号>/CLAUDE.md`
- 推荐版本：
  - `v8`：综合版，适合通用 Vibe Coding
  - `v10`：偏 Augment/上下文引擎的规范化约束
- 注意：`v9` 目录目前仅占位（无 `CLAUDE.md`）

### AI 工具01-系统提示词集合（中文翻译版）

`01-系统提示词/system-prompts-and-models-of-ai-tools-main-cn/` 收录了主流 AI 编程工具的01-系统提示词，**由 [x1xhlol/system-prompts-and-models-of-ai-tools](https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools) 翻译为中文**，包括：

| 工具 | 目录 | 说明 |
|:---|:---|:---|
| Claude Code | `Anthropic/` | Claude Code 2.0 01-系统提示词 |
| Cursor | `Cursor Prompts/` | Agent/Chat 多版本提示词 |
| Windsurf | `Windsurf/` | Wave 11 提示词与工具定义 |
| VS Code Copilot | `VSCode Agent/` | GPT-4/5、Gemini、Claude 等模型配置 |
| Kiro | `Kiro/` | Vibe/Spec 模式提示词 |
| Devin | `Devin AI/` | 自主 AI 工程师提示词 |
| Lovable | `Lovable/` | Agent 提示词与工具 |
| Replit | `Replit/` | Agent 提示词 |
| 更多... | 见目录 | Bolt、Cline、Gemini CLI 等 |

> 📌 原仓库：[x1xhlol/system-prompts-and-models-of-ai-tools](https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools)

## `02-编程提示词/`：任务级提示词（把流程跑通）

`02-编程提示词/` 面向「一次任务」：从需求澄清、计划拆解到交付与复盘。建议把它当作工作流脚本库：

- **入口级**（新会话/新项目必用）
  - `项目上下文文档生成.md`：固化上下文，降低跨会话漂移
  - `智能需求理解与研发导航引擎.md`：把模糊需求拆成可执行任务
- **交付级**（保证输出可审计）
  - `标准化流程.md`：把“先做什么、后做什么”写死，减少失控
  - `系统架构可视化生成Mermaid.md`：把架构输出成可视化（图胜千言）

### 关于 `index.md`（重要）

[`02-编程提示词/index.md`](./02-编程提示词/index.md) 是自动生成的索引（包含版本矩阵与跳转链接），**不要手工编辑**。如果你批量增删/调整版本，建议通过工具链生成索引再同步。

## `03-用户提示词/`：个人工作台（不追求体系化）

放一些个人习惯、临时脚手架提示词，原则是 **能用、别烂、别污染主库**。

## 快速使用（复制即用）

```bash
# 查看一个任务提示词
sed -n '1,160p' i18n/zh/prompts/02-编程提示词/标准化流程.md

# 选定01-系统提示词版本（建议先备份你当前的 CLAUDE.md）
cp i18n/zh/prompts/01-系统提示词/CLAUDE.md/10/CLAUDE.md ./CLAUDE.md
```

## 维护与批量管理（可选）

如果你需要 Excel ↔ Markdown 的批量维护能力，仓库内置了第三方工具：`libs/external/prompts-library/`。建议把它视为“提示词资产的生产工具”，而把 `i18n/zh/prompts/` 视为“日常开发的精选集”。

## 相关资源

- [`../skills/`](../skills/)：把高频领域能力沉淀为 Skills（更强复用）
- [`../documents/`](../documents/)：方法论与最佳实践（提示词设计与工作流原则）
- [`../libs/external/prompts-library/`](../libs/external/prompts-library/)：提示词 Excel ↔ Markdown 管理工具
