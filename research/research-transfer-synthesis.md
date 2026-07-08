# 研究迁移综合

## 字多不看

- 研究不是证明“我看过资料”，而是把成熟对象拆成可迁移机制、不可迁移边界和可验证动作。
- 本轮把 P1 研究对象合成为一条主线：Codex 负责执行控制面，Aider 负责 Git 编辑闭环，Cline 负责多入口平台化，Claude Code Best Practice 负责方法论资产化。
- 当前 17 个研究域均已补齐 `deep-dive.md`，全量进入 L2 证据层。
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
| `Aider-AI/aider` | Git 驱动编辑闭环 | 让每次 AI 修改都进入 diff、lint/test、commit、回滚和审查链路 | 研究域和文档修改必须保留 diff 证据、门禁命令和失败修复记录 | 不复制 Python 实现、repo map 算法和完整交互式终端产品 | 建立“AI 修改 -> diff 审查 -> make test -> commit”工作流模板 |
| `cline/cline` | 多入口 agent 平台 | 同一套能力暴露为 IDE、CLI、SDK、rules、skills、examples 和测试平台 | 为人类入口、AI 入口、脚本入口、skill 入口、资源入口和 metadata 入口写清协议 | 不提前做 SDK、服务端 hub 或复杂 UI | 梳理本仓入口矩阵，记录每个入口的输入、输出、owner 和验证命令 |
| `shanraisshan/claude-code-best-practice` | 方法论资产化 | 把经验拆成 best practice、implementation、workflow、reports、config | 把经验短句下沉为概念、模板、流程、skill 或检查项 | 不照搬 Claude Code 生态绑定配置，不把个人偏好当通用标准 | 建立“经验 -> 产物类型 -> 验证方式”的分流表 |
| `hesreallyhim/awesome-claude-code` | 资源治理系统 | 用结构化主表、状态字段、脚本、测试和模板治理外部资源 | 外部资源本地化、生命周期字段、去重和失效检查 | 不复制其分类体系，本仓聚焦中文 Vibe Coding | 为 `assets/external-resources` 增加字段契约和过期检查策略 |
| `tradecatlabs/vibe-coding-cn` | AI 原生知识库雏形 | 把 docs、skills、scripts、metadata、assets、research 和 llms 入口工程化 | 用外部样本反向校准本仓，持续把研究下沉到稳定层 | 不因自我研究陷入自我确认 | 对 P1 研究结论做跨对象组合和下游落地 |

## 全量研究域迁移矩阵

| 研究域 | 类型 | 最有价值机制 | 本仓迁移位置 | 下一步动作 |
|:---|:---|:---|:---|:---|
| `openai-codex` | coding-agent-tooling | 执行控制面 | `scripts/`、`workflow/`、`references/` | 建脚本风险登记表 |
| `aider-ai-aider` | coding-agent-tooling | Git 驱动编辑闭环 | `workflow/` | 建 AI 修改到提交的证据模板 |
| `cline-cline` | coding-agent-tooling | 多入口 agent 平台 | `metadata/`、`llms.txt`、`skills/` | 建入口矩阵 |
| `shanraisshan-claude-code-best-practice` | agentic-engineering-methodology | 方法论资产化 | `concepts/`、`workflow/`、`skills/` | 建经验分流表 |
| `hesreallyhim-awesome-claude-code` | ecosystem-index | 资源治理系统 | `assets/external-resources/` | 强化资源 schema |
| `tradecatlabs-vibe-coding-cn` | workflow-methodology | AI 原生知识库控制面 | 全仓 | 建自我审计和下沉任务 |
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

## 改良迭代

### 第一轮：让研究从“结论”变成“动作”

目标结果：用户打开研究文档后，能直接知道下一步怎么改自己的仓库。

| 改动点 | 原模式 | 本仓改良 | 验证指标 |
|:---|:---|:---|:---|
| 研究域分析 | 结构观察和可借鉴点 | 对标拆解、迁移边界、试用动作 | 17 个研究域 `analysis.md` 都有可执行动作 |
| 深度研究 | L2 证据和关键机制 | 保留证据链，另写迁移综合 | 17 个研究域均有 `deep-dive.md` |
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
