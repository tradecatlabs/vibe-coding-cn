# Skills 目录 Agent 指南

本目录用于收纳可复用的 **Skills（技能模块）**：每个子目录代表一个“可触发、可复用、可交付”的能力包，通常包含入口文档 `SKILL.md`，以及可选的脚本/参考资料/资产文件。

## 目录结构（约定）

```text
skills/
├── AGENTS.md                     # 本文件（目录级行为准则）
├── README.md                     # skills 总览与索引
├── <skill-name>/                 # 一个技能 = 一个目录
│   ├── SKILL.md                  # 入口：触发条件/边界/交付物/流程
│   ├── references/               # (可选) 参考资料与索引
│   ├── scripts/                  # (可选) 可执行脚本/自动化
│   ├── assets/                   # (可选) 模板/样例/静态资源
│   └── agents/                   # (可选) Agent 元数据（如 openai.yaml）
└── auto-skill/                   # 元技能：生成/校验/脚手架化其它技能
```

## 外部仓库引用（约定）

- 允许在 `skills/` 下放置“只读引用”的软链接，用于引入外部权威仓库的内容（便于统一索引与检索）。
- 为保证可复现性：软链接目标必须落在仓库内，并优先使用 Git submodule 管理（避免链接到个人机器的绝对路径）。

## 模块职责与边界

- 每个 `<skill-name>/` 必须以 `SKILL.md` 作为入口，明确：
  - 触发条件（何时用）
  - 不适用/边界（何时不用）
  - 交付物（要产出什么文件/结论）
  - 最小可复现流程（命令/步骤/输入输出）
- 技能目录之间尽量 **无隐式耦合**：不要依赖别的技能目录中的“隐式文件路径/脚本副作用”。
- 通用逻辑优先下沉到仓库的通用库目录（如后续引入），技能目录只保留“该领域必要的最薄封装”。

## 操作规范

### 允许
- 新增技能目录（优先复用现有模板与规范）
- 迭代现有 `SKILL.md` 的触发条件、边界与交付物定义
- 为技能补齐 `references/` 索引或 `scripts/` 自动化

### 禁止 / 不推荐
- 在 `skills/` 下按“编号分类目录”拆层级（保持扁平，靠 `README.md` 建索引）
- 让脚本默认写入不可审计的全局路径（优先输出到技能目录内或明确的 `artifacts/`）

## 快速定位（常用技能）

- `skills/tmux-autopilot/`：tmux 自动化操控与多 Agent 协作
- `skills/sop-generator/`：SOP 生成与规范化
- `skills/markdown-to-epub/`：Markdown → EPUB 稳定构建
- `skills/auto-skill/`：元技能（技能生成/校验/脚手架）
- `skills/claude-official-skills/`：Claude 官方 skills 仓库（Anthropic）的软链接入口
- `skills/auto-skill/scripts/Skill_Seekers-development`：Skill Seekers submodule 的软链接入口
- `skills/tmux-autopilot/assets/oh-my-tmux`：oh-my-tmux submodule 的软链接入口
- `skills/tmux-autopilot/assets/tmux-src`：tmux submodule 的软链接入口
