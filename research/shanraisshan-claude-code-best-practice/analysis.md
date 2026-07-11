# shanraisshan/claude-code-best-practice 研究分析

## 本轮结论

`shanraisshan/claude-code-best-practice` 的核心价值不是“Claude Code 资料多”，而是展示了方法论如何
变成文件系统、配置、workflow、reports 和 agent teams。它说明经验如果不能落到文件、流程、
示例或检查项，就只是口号。

本仓最应该迁移的是方法论资产化：把经验短句分流到 concepts、references、workflow、skills、
research 或 reports，而不是长期堆在一个经验清单里。

## 本地证据

- 研究对象：`shanraisshan/claude-code-best-practice`
- 当前研究角色：Claude Code / Agentic Engineering 最强对标
- 原始仓库：`raw/repository/`
- 原始来源清单：`raw/sources.yml`
- 事实摘要：`domain.yml`
- 深度证据：`deep-dive.md`

## 对标拆解

| 项 | 内容 |
|:---|:---|
| 参考对象 | `shanraisshan/claude-code-best-practice` |
| 它解决的核心问题 | 把 Claude Code / Agentic Engineering 经验变成可复用操作资产 |
| 核心机制 | `best-practice/` 放原则，`implementation/` 放实现，`orchestration-workflow/` 放流程，`reports/` 放复盘，配置文件放运行入口 |
| 真正带来结果的动作 | 让方法论进入文件、配置、示例、报告和工作流，而不是停留在聊天记录 |
| 可迁移做法 | 经验分流、agent teams 契约、harness 报告、配置治理、报告层沉淀 |
| 不可迁移条件 | 不照搬 Claude 生态绑定配置，不把个人实践当通用事实 |
| 下一步试用动作 | 建立“经验 -> 产物类型 -> 验证方式”的分流表 |

## 改良迭代

| 改良目标 | 原模式 | 本仓版本 | 验证指标 |
|:---|:---|:---|:---|
| 方法论分流 | best-practice / implementation / workflow / reports 分层 | concepts / references / workflow / skills / research 分层 | 每条经验能找到落点 |
| 复杂任务编排 | agent teams 和 orchestration workflow | 本仓任务树、子 Agent、tmux 协作和验收标准 | 多 Agent 任务有职责、输入、输出、依赖、验收 |
| 报告层沉淀 | reports 承载复盘和比较 | 本仓 research 和 references 承载阶段判断 | 重要结论不只留在对话里 |

## 可迁移清单

- 对经验短句做分流：概念、模板、流程、skill、检查项、归档。
- 对复杂研究任务写清角色、输入、输出、依赖和验收标准。
- 对重要失败或纠偏产出独立报告，避免同类问题反复出现。
- 把 hooks、settings、MCP、skills 等配置视为 AI 工程系统的一部分，而不是私人工具偏好。

## 不可迁移清单

- 不把 Claude Code 专属配置当作所有 Agent 的通用标准。
- 不直接复制命名结构；本仓已有 docs、skills、scripts、assets、metadata，需要按自身结构吸收。
- 不把未经验证的个人经验写成硬规则。

## 验证动作

| 动作 | 成功信号 | 失败信号 |
|:---|:---|:---|
| 抽样 10 条经验做分流 | 每条经验进入概念、流程、模板或 skill | 经验仍只是短句 |
| 为一次复杂研究任务写 agent teams 契约 | 子任务边界清楚、可验收 | 多 Agent 只是并行堆上下文 |
| 把一次失败研究写成复盘规则 | 同类失败有前置检查 | 下次继续产出空泛研究 |

## 沉淀判断

- 稳定结论应下沉到 `docs/getting-started/`、`docs/workflow/`、`docs/references/` 和 `skills/`。
- `deep-dive.md` 保留证据；本文件负责把证据转成迁移动作。
