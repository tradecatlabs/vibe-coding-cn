# Task Overview
- Task ID: `0003`
- Slug: `production-research-pipeline`
- Objective: `实现可恢复、可审计、可信证据驱动的 Vibe-Mathing 自动研究流水线，并以机器门禁证明生产闭环成熟度`
- Status: `In Progress`（实现节点全 Done；Git delivery、Verification Plan、复用资产交接与外部复盘 provenance 尚未通过 owner closeout）

## In Scope
- 可信 artifact root、verifier registry、现场哈希重算与防路径逃逸
- Problem/Attempt/Result 的唯一原子写入器、幂等键与并发锁
- 可恢复单 Agent 状态机、预算、超时、重试、取消和结构化 trace
- 统一 run/resume/verify/status CLI 与确定性 SymPy 垂直样例
- 固定 Lean 4/Mathlib 工具链、无 sorry 样例、公理/逃逸审计和忠实性回执
- 端到端、恢复、并发、伪造证据与成熟度攻击性测试及 CI

## Out of Scope
- 多 Agent 或分布式 worker 调度
- 自研模型、proof kernel、向量数据库或通用工作流平台
- 把实现者自签的 reviewer receipt 冒充外部独立审查
- 自动解决任意开放数学问题的能力承诺
- 提交、推送、部署或外部消息发送

## Task Package Tree
- ROOT
  ├─ TP-01 [leaf] [P0] 可信证据根与不可伪造回执
  ├─ TP-02 [leaf] [P0] 原子研究存储与唯一写入器
  ├─ TP-03 [leaf] [P0] 可恢复运行状态机与统一 CLI
  ├─ TP-04 [leaf] [P0] 确定性 SymPy 垂直闭环
  ├─ TP-05 [leaf] [P0] 固定 Lean/Mathlib 形式化闭环
  └─ TP-06 [leaf] [P0] 生产成熟度审计、CI、文档与最终审查

## Requirement Alignment
- 目标: 实现可恢复、可审计、可信证据驱动的 Vibe-Mathing 自动研究流水线，并以机器门禁证明生产闭环成熟度达到 100/100
- approved plan 顶层步骤数: 6
- 编译后节点总数: 6
- 编译后叶子节点数: 6
- 对齐项: 用户要求先设计推进到 100% 的计划，再按 tasks 容器完整实现
- 对齐项: 100% 定义为 required capabilities 和攻击性门禁全部通过，不是主观进度
- 对齐项: 当前审计基线为 MVP 35%-40%、生产闭环 15%-20%
- 计划摘要: 先封闭信任根，再建立单一存储和可恢复状态机；随后用确定性 adapter 证明主链，用 Lean 证明形式化链，最后以攻击性测试、CI、成熟度审计和文档审查收口。

## Task Package Overview
| Task Package ID | Parent | Depth | Priority | Type | Leaf | Depends On | Wave | Ready | Parallelizable | Objective |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | P0 | security-contract | Yes | - | 1 | Yes | No | 封住伪 locator、伪 hash、自报 independent 和 verifier 身份伪造路径 |
| TP-02 | ROOT | 1 | P0 | data-reliability | Yes | TP-01 | 2 | No | No | 为 Problem/Attempt/Result 和派生索引建立 schema-first、幂等、并发安全的唯一写入路径 |
| TP-03 | ROOT | 1 | P0 | agent-runtime | Yes | TP-02 | 3 | No | No | 实现 run/resume/verify/status、预算、超时、重试、取消、checkpoint 和 trace |
| TP-04 | ROOT | 1 | P0 | end-to-end-testing | Yes | TP-03 | 4 | No | No | 用无网络、无模型依赖的固定数学问题证明整条生产主链 |
| TP-05 | ROOT | 1 | P0 | formal-verification | Yes | TP-04 | 5 | No | No | 安装固定官方工具链并完成无 sorry 的最小 kernel/axiom/faithfulness 垂直链 |
| TP-06 | ROOT | 1 | P0 | release-gate | Yes | TP-05 | 6 | No | No | 把所有 required capability 编译为不可自报的 100/100 门禁并完成项目文档同步 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
