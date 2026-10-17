# Repo Evidence
- 当前分支 `main`；任务开始时工作树 clean，HEAD 为 `5b8a191`，项目无 remote。
- 现有 PRD 将 PSOA 画成任务意图与 Harness Runtime 之间的独立 Semantic Plane。
- `docs/HARNESS_MODEL.md`、ADR-0003、根 README/AGENTS 与治理上下文复用了这一边界。
- 现有 Harness 模型已包含 loop、context、memory、tools、policy、verification 和 observability，适合把 Operator Library 归入同一运行时边界。

# Constraints Matrix
| 约束 | 处理 |
|---|---|
| 算子库属于 Harness | PRD 与总模型必须明确写入 Harness 组件树 |
| 元 Harness 不接管业务状态 | 只治理规范、目录、conformance、eval 和 lifecycle |
| 跨 Harness 复用 | `OperatorSpec` 与 Harness-specific `OperatorBinding` 分离 |
| 权限和完成裁决不可弱化 | Harness policy 裁权；Verifier 依据证据裁决 |
| 文档纠偏不提前编码 | 本轮不修改 contracts/scripts/tests 行为 |

# Change Boundary
- 允许：`docs/`、根 README/AGENTS、ADR-0003、项目操作模型、拓扑、docs module context 与 0007 任务证据。
- 禁止：`contracts/`、`scripts/`、`tests/`、上游 registry/lock/checkouts 和已完成任务 0006。
- 文档结构不新增平行组件；优先修正现有真相源。

# Risk Matrix
| 风险 | 等级 | 缓解 |
|---|---|---|
| 本地库存与中央目录出现双 owner | 高 | 明确规范/治理所有权与运行/执行所有权 |
| 把算子降级成 prompt 片段 | 中 | 保留前置条件、输入输出、证据、失败、预算和权限语义 |
| 把 Verifier 错画成必然外部服务 | 中 | 规定逻辑独立，不规定部署拓扑 |
| 文档只改一处造成漂移 | 中 | 全仓术语扫描、治理 strict 和 architecture gate |

# Assumptions and Falsification
- 假设：用户所说“属于 Harness”指运行时组件归属，不否定元 Harness 维护共享规范和治理目录。
- Proof point：读者能从组件树指出本地 Operator Library 位于 Harness 内，并能区分中央规范与本地 Binding。
- Falsifier：修订后仍需把算子作为 Harness 外部执行服务才能说明调用流程，或出现两个主体共同拥有运行状态。

# Critical Ambiguities
- 无关键歧义；Verifier 的进程部署和 selector 算法均不影响本轮所有权修正。

# Debug Evidence Contract
- 调试模式: Optional
- 回归证据契约: Optional
- 理由：本任务是架构文档纠偏，不修改可执行产品行为；使用结构检查、链接校验和项目门禁替代运行时 RED/GREEN。

# Task Package Context Map
## TP-01
- 输入：用户纠正、PSOA PRD、HARNESS_MODEL、Agent = LLM + Harness 定义。
- 输出：正确组件树、对象所有权和运行流程。

## TP-02
- 输入：TP-01 的稳定边界及现有 ADR/治理导航。
- 输出：一致的长期项目真相源。

## TP-03
- 输入：最终 diff、Task Intent 与 Verification Plan。
- 输出：自审、严格门禁和交付证据。
