# walkinglabs/learn-harness-engineering 研究分析

## 本轮结论

`walkinglabs/learn-harness-engineering` 的核心价值不是“又一个 AI 编程教程”，而是把 Harness
Engineering 拆成可复制的仓库控制面：入口指令、状态文件、验证命令、范围约束、会话生命周期、
评估器和审计工具。

本仓最应该迁移的是它的对象化交付方式：每个 Agent 可靠性问题都要落到仓库内 artifact，
而不是停留在经验句子或提示词技巧。对本仓而言，最有价值的迁移方向是：

- 把 `docs/research/harness/` 的概念研究补成可执行检查清单。
- 把 `feature_list.json` 的状态机思想迁移到任务治理、研究域推进和 Agent 工作包。
- 把 `init.sh` 的单入口验证思想迁移到本仓 `make test`、raw 拉取和文档门禁。
- 把 `evaluator-rubric.md` 的评分表思想迁移到重要产出的交叉审计。

## 本地证据

- 研究对象：`walkinglabs/learn-harness-engineering`
- 当前研究角色：Harness Engineering 课程、模板、Skill 与审计工具对标对象
- 原始仓库：`raw/repository/`
- 原始来源清单：`raw/sources.yml`
- 事实摘要：`domain.yml`
- 深度证据：`deep-dive.md`

## 对标拆解

| 项 | 内容 |
|:---|:---|
| 参考对象 | `walkinglabs/learn-harness-engineering` |
| 它解决的核心问题 | 强模型在真实仓库中仍会丢上下文、越界、提前宣告完成、跳过验证和无法跨会话延续 |
| 核心机制 | 12 讲课程、6 个递进项目、模板库、`skills/harness-creator`、`tools/audit-harness.sh` |
| 真正带来结果的动作 | 把经验变成仓库内可读、可执行、可验证、可交接的结构化 artifact |
| 可迁移做法 | 五子系统模型、fresh session test、feature list 状态机、pass-state gating、全链路验证、会话交接 |
| 不可迁移条件 | 不复制其 VitePress 站点、多语言工程和完整课程项目体量；本仓先保持轻量知识库和研究域结构 |
| 下一步试用动作 | 为本仓 Harness 研究域补一份“最小可执行 Harness 检查表”和一个研究任务状态机样例 |

## 改良迭代

| 改良目标 | 原模式 | 本仓版本 | 验证指标 |
|:---|:---|:---|:---|
| 概念落地 | 课程用模板和项目演示 Harness | 本仓在 `docs/research/harness/` 增加可执行检查表 | 读者能直接审计自己的仓库 |
| 状态治理 | `feature_list.json` 管理功能状态 | 研究域和任务包使用 `id / behavior / verification / status / evidence` | 新会话能知道下一步，不靠聊天记忆 |
| 验证闭环 | `init.sh` 统一安装、验证和启动 | 本仓继续收敛到 `make test` + raw 拉取 + 文档结构门禁 | 任何新增研究域都能一命令验收 |
| 审计沉淀 | `evaluator-rubric.md` 评分后验收 | 本仓重要产出用“正确性、证据、范围、可维护性、交接”审计 | 研究报告读完有可执行结论 |

## 可迁移清单

- 入口文件只做路由和硬约束，详细知识放到邻近文档中按需读取。
- 把仓库当成 Agent 的系统真相源，重要上下文不能只留在聊天记录或人脑里。
- 每个任务或功能都要有行为描述、验证方式、状态和证据，避免“差不多完成”。
- 验证失败信息要写给 Agent 看，包含问题、原因和修复方向。
- 会话结束前必须留下可恢复状态：做了什么、验证了什么、没做完什么、下一步是什么。
- 对 Harness 组件做 ablation 思维：移除某个组件后失败是否增加，用结果判断优先级。

## 不可迁移清单

- 不把本仓变成 15 语言 VitePress 课程站点。
- 不直接引入其 `harness-creator` 脚本作为本仓工具真相源，除非先完成安全、依赖和维护成本评估。
- 不把教学项目的 Electron 技术栈误认为 Harness Engineering 的必要条件。
- 不把 feature list 机械复制到所有文档；只有需要状态机和验证闭环的对象才引入。

## 验证动作

| 动作 | 成功信号 | 失败信号 |
|:---|:---|:---|
| 为本仓 Harness 研究域补最小检查表 | 能按五子系统审计一个仓库 | 仍只是概念解释，不能指导操作 |
| 把 feature list 思想用于一个真实任务包 | 新会话能从状态文件继续 | 仍需要翻聊天记录判断进度 |
| 抽取一条 Agent 错误反馈并转成门禁 | 同类错误下次能自动失败并提示修复 | 仍依赖人工反复提醒 |
| 试运行外部 `audit-harness.sh` 对本仓打分 | 能发现本仓 Harness 缺口 | 检查项与本仓结构不匹配且无法解释 |

## 沉淀判断

- 稳定概念进入 `docs/research/harness/` 和 `docs/workflow/`。
- 可执行检查表成熟后，可进入 `scripts/` 或 `skills/`。
- 本研究域保持 P2，对齐 Harness Engineering 课程和工具化对标对象。
