---
id: GOV-PROJECT-TOPOLOGY
type: index
status: current
owner: engineering
created: 2026-08-13
last_reviewed: 2026-09-04
review_cycle: P90D
---

# Project Topology

## 项目结构

| 路径 | 职责 | 禁止事项 | 主要验证 |
|---|---|---|---|
| `governance/` | 项目工程治理包、上下文路由、标准、门禁和证据记录 | 不覆盖项目原有 README、AGENTS、CI 或模块文档 | `validate_governance_package.py --strict` |
| `governance/tasks/` | 任务树、任务包和执行状态 | 不把任务执行期状态直接当成长期标准 | `validate_tasks_tree.py` |
| `docs/` | Harness 领域模型、PSOA 需求、Core/Profile 规范与目标架构 | 不复制字段级机器契约，不把计划冒充已实现能力 | 文档链接与治理审查 |
| `research/` | 官方 Harness 上游来源、revision lock 与研究边界 | 不提交第三方 checkout，不把公开扩展仓库冒充核心源码 | `bash scripts/sync_upstreams.sh` |
| `contracts/` | Harness manifest、Operator Pack 与 Operator Runtime Core 的机器 Schema | 不把特定库内容完整度写成公共契约，不保存运行状态 | `validate_harness.py --self-test` |
| `operators/` | Reference Profile、411 个原始方法、57 个派生 Method、来源清单、catalog 与双轴 taxonomy | 不执行方法，不把本地 Profile 冒充 Core | `validate_harness.py --operator-library operators/catalog.json` |
| `examples/` | 具体 Harness 的非生产协议消费方与无副作用运行证明 | 不成为中央 Runtime，不执行真实模型或工具 | `python3 -m unittest tests.test_reference_operator_harness` |
| `scripts/` | 连接成熟工具与项目策略的薄验证入口 | 不反向定义领域语义，不输出敏感内容 | Pack/Runtime Core、Reference Profile 与 self-test |
| `tests/` | 结构、策略和参考 Harness 行为反例 | 不保存生产 prompt、凭据或客户数据 | `validate_harness.py --self-test` 与标准库 `unittest` |
| `governance/control-plane/` | 项目 Verification Policy 与 capability registry | 不保存业务状态，不接受调用者降级 required gate | verification policy strict validator |

## 依赖方向

`research/` 固定官方上游输入，`docs/` 和 ADR 定义语义，`contracts/` 固化结构，`operators/` 保存静态参考内容，`scripts/` 消费契约并输出准入结果，
`examples/` 证明具体 Harness 可消费共享协议，`tests/` 证明拒绝能力；`governance/` 约束所有变更。控制面只通过稳定记录消费
受管 runtime 的证据，不反向接管其业务状态。PSOA 定义 Harness 内的 Operator Library；共享
OperatorSpec 与 Runtime Core 由元 Harness 治理，本地库存、Binding、权限和业务运行状态由具体 Harness 拥有。
