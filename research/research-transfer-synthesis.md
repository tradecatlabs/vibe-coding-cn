# 研究迁移综合

## 字多不看

- 研究不是证明“我看过资料”，而是把成熟对象拆成可迁移机制、不可迁移边界和可验证动作。
- 本轮把 P1 研究对象合成为一条主线：Codex 负责执行控制面，Plugins/Skills 负责能力分发，Agents SDK 负责运行时编排，Cookbook 提供可复现示例，Spec Kit/OpenSpec 负责规格驱动，Gemini CLI/OpenHands/OpenCode/Goose 提供终端、工作区和配置对标，Aider 负责 Git 编辑闭环，Superpowers/Agent Skills/ECC 负责方法论与 Harness 资产化，Cline 负责多入口平台化。
- 当前 36 个研究域均已补齐 `deep-dive.md`，全量进入 L2 证据层。
- 本仓不应该复制任何一个外部项目，而应该杂交成“AI 原生知识库控制面”。
- 下一步最小试用动作是：补 `scripts` 风险登记、补研究域迁移表、补资源治理 schema、补工作流验证闭环。

## 研究质量问题

上一版研究读起来没有收获，根因不是材料不足，而是研究链条断在“观察”阶段：

| 缺口 | 表现 | 修正方式 |
|:---|:---|:---|
| 机制不足 | 只写目录结构和可借鉴点 | 明确哪个机制真正制造结果 |
| 迁移不足 | 只说“本仓可参考” | 写清能迁移什么、不能迁移什么 |
| 动作不足 | 只写“下一轮研究” | 写出下一步试用动作和验收指标 |
| 组合不足 | 单个仓库各说各话 | 把多个机制组合成本仓可执行方案 |
| 验证不足 | 结论像观点 | 给出证据来源、试用指标和失败条件 |

新的研究标准是：

> 每个深度研究必须回答：它为什么有效，我能抄哪里，不能抄哪里，怎么改成本仓版本，如何验证改完真的更好。

## 对标拆解

| 参考对象 | 核心机制 | 真正带来结果的动作 | 可迁移做法 | 不可迁移条件 | 下一步试用动作 |
|:---|:---|:---|:---|:---|:---|
| `openai/codex` | 执行控制面 | 把配置、沙箱、执行策略、工具、技能和项目上下文显式建模 | `scripts` 风险分级、Agent 执行边界、技能输入输出契约 | 不复制 Rust/Bazel/CLI runtime，本仓不是 coding agent 产品 | 建立 `scripts/manifest.yml`，记录 owner、风险、输入、输出、dry-run 和 CI 状态 |
| `openai/plugins` | 插件与能力分发 | 用 manifest、marketplace 和 skill-only plugin 组织可安装能力 | 为 skill/工具增加来源、安装、权限、版本和回滚字段 | 不把可安装等同于可信，不复制官方插件全集 | 为一个本地 skill 写安装前审查清单 |
| `openai/skills` | 技能目录迁移 | 展示 Skills Catalog 向 Plugins 的弃用与迁移边界 | 为 skill 建立触发、输入输出、验证和弃用规则 | 不把 deprecated catalog 当作现行安装入口 | 对本仓高频 skill 做生命周期标记 |
| `openai/openai-agents-python` | Agent 运行时 | 将 Agent、Tools、Handoffs、Guardrails、Sessions 和 Tracing 组合成闭环 | 把任务执行、工具副作用、护栏和证据分层 | 不为文档仓库引入完整 SDK 运行时 | 写一个“计划 -> 工具 -> 验证”最小实验 |
| `openai/openai-agents-js` | TypeScript Agent 运行时 | 将 runner、工具审批、session、sandbox 和 tracing 组合成可观察生命周期 | 为本仓工具与任务契约补充状态所有权和审批边界 | 不复制 SDK、实时能力或完整 sandbox | 写一个“工具意图 -> 审批 -> 执行 -> trace”最小实验 |
| `openai/openai-cookbook` | 官方示例资产层 | 用 registry、示例目录和评估材料组织可复现方法 | 为研究结论补充复现前置条件、命令和验证输出 | 不把示例默认当生产架构，不复制凭据和外部副作用 | 选择一个 Codex 示例建立本仓复现记录 |
| `github/spec-kit` | 规格驱动开发 | 用规格、计划、任务、实现和测试阶段化推进变更 | 把复杂文档/代码任务拆成有产物的阶段契约 | 不复制其 CLI、模板或完整项目脚手架 | 为一个文档重构任务写规格到验收链 |
| `Fission-AI/OpenSpec` | 变更与规格生命周期 | 分离 changes、specs、schema、skills 和 archive | 把临时任务状态与稳定知识分开 | 不为本仓引入完整 openspec 运行时 | 选择一次目录变更试做变更提案与归档记录 |
| `google-gemini/gemini-cli` | 终端 Agent 与安全评估 | 将上下文、MCP、扩展、沙箱、checkpoint 和负例评估放入 CLI | 增加非交互入口、上下文层级和安全负例 | 不复制供应商账号、模型默认值和完整 CLI | 用一个只读任务验证输入、输出和退出码 |
| `OpenHands/OpenHands` | Agent 控制中心与工作区 | 把 Agent 后端、workspace、自动化和用户接管分离 | 将研究任务状态、工作区和恢复入口显式化 | 不复制 Agent Canvas、云平台或多租户服务 | 为 raw 刷新任务增加可恢复状态记录 |
| `anomalyco/opencode` | 模型无关配置与权限 | 将 provider、model、agent、permission、plugin 和 reload 生命周期分离 | 先 plan 再执行，配置变更可备份、验证和回滚 | 不把 v2 spec 当稳定 API，不复制完整 monorepo | 为 CLI 配置变更设计 dry-run 和回滚检查 |
| `obra/superpowers` | Skill 化开发方法论 | 把头脑风暴、计划、TDD、审查和分支收尾做成可触发能力包 | 为本仓 skill 补触发、阶段和完成前验证契约 | 不把第三方流程无条件强加给简单任务 | 选一个高频任务补最小 Skill 触发和验证表 |
| `addyosmani/agent-skills` | 生命周期导航与技能评估 | 用短命令连接 spec、plan、build、test、review 和 ship，并用 eval 验证 | 为已有能力建立目标到 owner skill 的路由 | 不复制其 harness 绑定路径或个人偏好 | 抽样验证一个入口是否能指向唯一验证命令 |
| `aaif-goose/goose` | 跨模型 Agent 平台 | 分离 provider、MCP、上下文、工作区、recipe 和 eval | 明确外部模型、工具、上下文和验证的边界 | 不为知识库自建 provider 或 MCP runtime | 为一个研究任务补 provider/工具/证据边界表 |
| `continuedev/continue` | 生命周期与迁移案例 | 以只读项目状态说明架构价值与继续采用风险必须同时判断 | 将维护状态、最终版本和替代路径纳入研究域 | 不作为现行安装或推荐主线 | 对一个历史项目执行状态、引用和替代路径检查 |
| `SWE-agent/mini-SWE-agent` | 极简问题修复 Agent | 用 Bash 工具、线性轨迹和有界预算完成 issue 修复 | 为自动化脚本明确工具面、退出码、超时和输出上限 | 不牺牲验证，不把极简当作无边界执行 | 运行一个只读检查任务并记录轨迹与退出码 |
| `affaan-m/ECC` | 多 Agent Harness 资产 | 将记忆、技能、安全、评估和 hooks 组织成跨工具 Harness | 为本仓补 Harness 资产清单、权限边界和评估入口 | 不直接导入外部配置、秘密或未经审查的 hooks | 抽取一个安全/评估 skill 做来源和行为审查 |
| `Aider-AI/aider` | Git 驱动编辑闭环 | 让每次 AI 修改都进入 diff、lint/test、commit、回滚和审查链路 | 研究域和文档修改必须保留 diff 证据、门禁命令和失败修复记录 | 不复制 Python 实现、repo map 算法和完整交互式终端产品 | 建立“AI 修改 -> diff 审查 -> make test -> commit”工作流模板 |
| `cline/cline` | 多入口 agent 平台 | 同一套能力暴露为 IDE、CLI、SDK、rules、skills、examples 和测试平台 | 为人类入口、AI 入口、脚本入口、skill 入口、资源入口和 metadata 入口写清协议 | 不提前做 SDK、服务端 hub 或复杂 UI | 梳理本仓入口矩阵，记录每个入口的输入、输出、owner 和验证命令 |
| `shanraisshan/claude-code-best-practice` | 方法论资产化 | 把经验拆成 best practice、implementation、workflow、reports、config | 把经验短句下沉为概念、模板、流程、skill 或检查项 | 不照搬 Claude Code 生态绑定配置，不把个人偏好当通用标准 | 建立“经验 -> 产物类型 -> 验证方式”的分流表 |
| `hesreallyhim/awesome-claude-code` | 资源治理系统 | 用结构化主表、状态字段、脚本、测试和模板治理外部资源 | 外部资源本地化、生命周期字段、去重和失效检查 | 不复制其分类体系，本仓聚焦中文 Vibe Coding | 为 `assets/external-resources` 增加字段契约和过期检查策略 |
| `tradecatlabs/vibe-coding-cn` | AI 原生知识库雏形 | 把 docs、skills、scripts、metadata、assets、research 和 llms 入口工程化 | 用外部样本反向校准本仓，持续把研究下沉到稳定层 | 不因自我研究陷入自我确认 | 对 P1 研究结论做跨对象组合和下游落地 |

## 全量研究域迁移矩阵

| 研究域 | 类型 | 最有价值机制 | 本仓迁移位置 | 下一步动作 |
|:---|:---|:---|:---|:---|
| `openai-codex` | coding-agent-tooling | 执行控制面 | `scripts/`、`workflow/`、`references/` | 建脚本风险登记表 |
| `openai-plugins` | coding-agent-tooling | 插件 manifest、marketplace 和 skill-only plugin 分发 | `skills/`、`assets/`、`metadata/` | 建插件来源、权限和回滚检查清单 |
| `openai-skills` | coding-agent-tooling | Skills Catalog 到 Plugins 的迁移边界 | `skills/`、`docs/workflow/` | 为现有 Skill 标记生命周期和弃用路径 |
| `openai-agents-python` | agent-runtime | Agent、Tools、Handoffs、Guardrails、Sessions 和 Tracing | `workflow/`、`references/` | 建计划、工具、副作用和验证的生命周期表 |
| `openai-agents-js` | agent-runtime | TypeScript runner、工具审批和状态追踪 | `workflow/`、`skills/` | 建工具意图到证据的生命周期表 |
| `openai-cookbook` | agent-development-guides | 可复现 API、Codex、Agent 和评估示例 | `getting-started/`、`references/` | 建示例复现记录模板 |
| `github-spec-kit` | spec-driven-development | 规格到实现的阶段化流程 | `workflow/`、`references/` | 建规格/计划/任务/验收模板 |
| `fission-ai-openspec` | spec-driven-development | 变更、规格、schema 和归档分层 | `workflow/`、`references/` | 建临时变更与稳定知识分流表 |
| `google-gemini-gemini-cli` | coding-agent-tooling | 终端上下文、MCP、扩展、checkpoint 和安全评估 | `getting-started/`、`workflow/` | 建非交互入口和安全负例检查 |
| `openhands-openhands` | agent-runtime | Agent 控制中心、工作区和后端适配 | `workflow/`、`references/` | 建 Agent、工作区、后端和恢复状态边界表 |
| `anomalyco-opencode` | coding-agent-tooling | provider、model、permission、plugin 和 reload 生命周期 | `getting-started/`、`references/` | 建配置 dry-run、备份、验证和回滚检查 |
| `aider-ai-aider` | coding-agent-tooling | Git 驱动编辑闭环 | `workflow/` | 建 AI 修改到提交的证据模板 |
| `cline-cline` | coding-agent-tooling | 多入口 agent 平台 | `metadata/`、`llms.txt`、`skills/` | 建入口矩阵 |
| `shanraisshan-claude-code-best-practice` | agentic-engineering-methodology | 方法论资产化 | `concepts/`、`workflow/`、`skills/` | 建经验分流表 |
| `hesreallyhim-awesome-claude-code` | ecosystem-index | 资源治理系统 | `assets/external-resources/` | 强化资源 schema |
| `tradecatlabs-vibe-coding-cn` | workflow-methodology | AI 原生知识库控制面 | 全仓 | 建自我审计和下沉任务 |
| `vibe-mathing-cn-public` | research-infrastructure | 问题契约、证据闭环和有界工具运行时 | `workflow/`、`references/`、未来 skills | 抽取候选/结果分层、失败回执和工具边界，验证能否跨领域复用 |
| `datawhalechina-easy-vibe` | cn-onboarding | 目标分流课程路径 | `getting-started/` | 重构学习地图分流 |
| `datawhalechina-vibe-vibe` | cn-onboarding | demo 驱动零基础课程 | `getting-started/`、未来 practice | 给概念补最小练习 |
| `liyupi-ai-guide` | cn-onboarding | 大众解释和项目实战入口 | `getting-started/`、`assets/` | 抽取低门槛表达和工具候选 |
| `wendy7756-vibe-coding-guide` | cn-onboarding | 非程序员视角 | `getting-started/`、`prompts/` | 增加非程序员入口说明 |
| `luzhenqian-ai-coding-lab` | project-practice | 项目实验室矩阵 | `workflow/`、未来 practice | 建最小实践项目模板 |
| `shouzhengai-cs146s-cn` | project-practice | assignments 验证层 | `getting-started/`、`workflow/` | 建练习任务模板 |
| `filipecalegario-awesome-vibe-coding` | ecosystem-index | 国际工具族和术语雷达 | `assets/`、`concepts/keyword-system.md` | 抽取工具族和术语对照 |
| `ai-for-developers-awesome-vibe-coding` | ecosystem-index | 轻量工具分类雷达 | `assets/external-resources/` | 对照资源分类缺口 |
| `daotin-ai-coding` | workflow-methodology | 中文 AI Coding 主题雷达 | `concepts/keyword-system.md`、`assets/` | 抽取中文高频主题 |
| `earyantle-vibe-coding-skill` | workflow-methodology | 最小 Skill 骨架 | `skills/` | 建 Skill 发布检查清单 |
| `roocodeinc-roo-code` | coding-agent-tooling | 归档工具生命周期样本 | `research/`、`assets/` | 明确 archived 降级规则 |
| `obra-superpowers` | agent-workflow-methodology | 可组合 Skill 与 TDD/审查阶段门禁 | `skills/`、`workflow/` | 建 Skill 触发和完成前验证清单 |
| `addyosmani-agent-skills` | skill-governance | 生命周期命令与独立 eval | `skills/`、`workflow/` | 建入口到 owner skill 的路由表 |
| `aaif-goose-goose` | coding-agent-tooling | provider、MCP、上下文和工作区分层 | `workflow/`、`references/` | 建外部能力边界表 |
| `continuedev-continue` | lifecycle-reference | 只读项目的维护状态和迁移风险 | `research/`、`references/` | 建历史项目降级规则 |
| `swe-agent-mini-swe-agent` | issue-solving-agent | 极简工具面和有界轨迹 | `workflow/`、`references/` | 建命令、预算和退出码检查 |
| `affaan-m-ecc` | harness-engineering | Harness、记忆、安全和评估资产 | `skills/`、`workflow/` | 建 Harness 来源与权限审查清单 |

## 改良迭代

### 第一轮：让研究从“结论”变成“动作”

目标结果：用户打开研究文档后，能直接知道下一步怎么改自己的仓库。

| 改动点 | 原模式 | 本仓改良 | 验证指标 |
|:---|:---|:---|:---|
| 研究域分析 | 结构观察和可借鉴点 | 对标拆解、迁移边界、试用动作 | 36 个研究域 `analysis.md` 都有可执行动作 |
| 深度研究 | L2 证据和关键机制 | 保留证据链，另写迁移综合 | 36 个研究域均有 `deep-dive.md` |
| 价值地图 | 用户价值说明 | 增加组合方案和验收指标 | 能回答“看完有什么用” |

### 第二轮：让研究进入仓库控制面

目标结果：研究结论不再停在 research，而是进入 `scripts`、`workflow`、`assets`、`skills` 和 `references`。

| 迁移方向 | 来源机制 | 本仓目标产物 | 验证指标 |
|:---|:---|:---|:---|
| `scripts` 控制面 | Codex exec policy / sandbox | 脚本登记表、风险等级、dry-run 和审批边界 | 每个脚本有 owner、风险、输入输出和 CI 状态 |
| Git 编辑闭环 | Aider repo editing loop | AI 修改工作流和提交前证据模板 | 每次提交说明验证命令和 diff 范围 |
| 多入口契约 | Cline IDE / CLI / SDK / rules | 人类入口、AI 入口、脚本入口、skill 入口矩阵 | 每个入口有输入、输出、更新策略 |
| 方法论分流 | Claude best practice | 经验到 concepts/references/workflow/skills 的分流规则 | 经验短句不再孤立堆放 |
| 资源治理 | awesome-claude-code CSV | 资源 schema、状态字段、过期检查 | 资源表能被脚本校验 |

### 第三轮：让研究可以被证伪

目标结果：研究不再是“写得像对”，而是能通过小实验判断是否有效。

| 假设 | 最小实验 | 成功信号 | 失败信号 |
|:---|:---|:---|:---|
| `scripts` manifest 能降低脚本风险 | 选 5 个脚本补 owner、风险、输入输出和自动执行边界 | Agent 能判断哪些脚本可自动跑 | 仍需要人工逐个解释脚本用途 |
| 文档地图能降低索引漂移 | 为 research 建生成或校验入口 | README、metadata、llms 路径一致 | 新文档漏进索引 |
| 资源 schema 能提升资源质量 | 抽样 30 条资源做字段校验 | 能发现缺 license、last_checked 或重复 ID | 仍靠肉眼维护 |
| 经验分流能提升学习效果 | 将 10 条经验分别落到概念、流程或 skill | 用户能按目的找到对应动作 | 经验仍只是口号 |

## 杂交创新

本仓最优路线不是学习某一个外部仓库，而是把多个成熟机制组合成一个更适合中文 Vibe Coding 的系统：

```text
AI 原生知识库控制面
├── research/   # 发现和验证外部机制
├── assets/     # 治理外部资源和引用材料
├── metadata/   # 提供机器可读索引
├── scripts/    # 执行质量门禁和同步任务
├── workflow/   # 约束 AI 修改、验证和交付过程
├── skills/     # 沉淀可复用 Agent 能力
└── docs/       # 面向人类的稳定知识层
```

组合逻辑：

- Codex 给出“执行必须有控制面”的底线。
- Aider 给出“修改必须进入 Git 和测试闭环”的底线。
- Cline 给出“入口必须平台化和契约化”的方向。
- Claude Code Best Practice 给出“方法论必须文件系统化”的方向。
- Awesome 生态给出“资源必须结构化治理”的方向。
- 本仓负责把这些机制压成中文学习路径、工程模板和 Agent 可执行规则。

## 下一步落地清单

| 优先级 | 动作 | 目标位置 | 完成标准 |
|:---|:---|:---|:---|
| P0 | 更新 P1 研究域 `analysis.md` | `research/*/analysis.md` | 每个样板有对标拆解、改良迭代和试用动作 |
| P0 | 升级研究域治理契约 | `research/research-domain-contract.md` | L2/L3 明确要求迁移动作和验证指标 |
| P1 | 建立 scripts 控制面 | `scripts/` | manifest、风险等级、自动/人工边界 |
| P1 | 建立入口矩阵 | `docs/references/` 或 `docs/workflow/` | 人类、AI、脚本、skill、资源入口边界清楚 |
| P1 | 建立资源 schema | `assets/external-resources/` | 字段、生命周期、过期检查和去重规则 |
| P2 | 建立经验分流规则 | `docs/getting-started/`、`docs/workflow/`、`skills/` | 经验短句能下沉成可执行产物 |

## 验收标准

研究文档以后必须满足以下标准，否则就只是资料整理：

- 能说清参考对象的核心机制。
- 能指出哪些机制真正带来结果。
- 能列出可迁移做法和不可迁移条件。
- 能给出本仓改良版本，而不是照搬原模式。
- 能给出最小试用动作和验证指标。
- 能说明失败信号，允许研究结论被证伪。
