# Repo Evidence
- 基线分支 `main`，任务开始时 HEAD `056f5ce`，工作树 clean，项目无 remote。
- `docs/HARNESS_MODEL.md` 已定义元 Harness 控制面，但此前没有 Operator/Method 需求真相源。
- `contracts/harness-manifest.schema.json` 只拥有 Harness 声明结构，不应承载问题求解算子定义。
- 架构 context bundle 要求 ADR、边界/依赖和回滚路径，并发现 `docs` module context 缺失。
- 用户提供了跨学科方法地图及 STRIPS/PDDL、HTN、TEVV、BPMN/CMMN、DMN、PROV、Essence 等参考。

# Constraints Matrix
| 类别 | 约束 |
|---|---|
| 语义 | 领域知识与问题求解方法分离；JSON 不反向决定领域模型 |
| 边界 | Operator 不等于 Tool/Prompt/Skill/Workflow；Harness 执行，Verifier 裁决 |
| 状态 | world、knowledge、governance 三类效果必须独立表达 |
| 风险 | Operator 只能声明所需 capability，不能授予权限或自证成功 |
| 架构 | operator/method 契约未来独立于 Harness manifest，不建设统一 runtime |
| 工程 | 最小充分文档变更；不引入依赖、服务、Schema 或运行行为 |

# Change Boundary
- 允许：PSOA PRD、HARNESS_MODEL 链接、README/AGENTS 导航、ADR-0003、docs module context、
  PROJECT_OPERATING_MODEL/TOPOLOGY/CONTEXT-MAP、0006 任务证据与治理索引。
- 只读：现有 contracts、scripts、tests、research 和历史任务。
- 禁止：修改 Harness Schema、执行上游、引入运行时、读取凭据、使用破坏性 Git 操作。

# Risk Matrix
| 风险 | 等级 | 控制 |
|---|---|---|
| 把 JSON Schema 当作需求本体 | 高 | 本轮只定义语义和验收，Schema 留给 prototype 后任务 |
| Operator/Tool/Harness 职责混淆 | 高 | PRD 提供相邻概念责任表和生命周期 owner |
| 把非确定性结果写成确定事实 | 高 | Observation/Evidence/Outcome 分层，明确 inconclusive |
| 大而全标准拼盘 | 中 | 只借鉴语义，拒绝完整兼容声明和首版平台化 |
| 文档新增但项目入口漂移 | 中 | 同步两级 AGENTS、README、操作模型、拓扑、module context、ADR |

# Assumptions and Falsification
- 假设：跨 Harness 可移植的问题求解方法值得拥有独立语义层，而非继续作为 prompt/skill 私有实现。
- Proof point：同一 Operator 可被两个独立 Harness adapter 执行和验证，无供应商自由文本特例。
- Falsifier：第二个 adapter 必须改写核心语义、隐藏关键状态或绕过 evidence contract 才能接入。
- 若 falsifier 命中，应重塑 Operator/Harness/Verifier 边界，不增加长期兼容壳。

# Critical Ambiguities
- 无阻塞性歧义；用户已确认要先整理需求文档。
- 非关键待决策：predicate/effect DSL、Method 图结构、Verifier 实现、PROV profile 和 registry ID。
  这些需要 semantic prototype 证据，本轮以 open questions 保留。

# Debug Evidence Contract
- 调试模式: `Optional`
- 回归证据契约: `Optional`
- 本任务不修复行为缺陷；若校验暴露实现 bug，再另行升级为 `Required` 并转调试闭环。

# Task Package Context Map
## TP-01
- 输入：用户提供的方法论地图、上一轮全局景观分析、HARNESS_MODEL 和架构标准。
- 输出：可供后续 Schema/原型任务消费的 PSOA PRD。

## TP-02
- 输入：TP-01 中稳定的系统边界与所有权判断。
- 输出：ADR-0003、docs context 和项目级导航/操作模型同步。

## TP-03
- 输入：最终文档 diff、Task Intent、Verification Plan 和项目门禁。
- 输出：review、closeout 文档、校验证据与本地交付。
