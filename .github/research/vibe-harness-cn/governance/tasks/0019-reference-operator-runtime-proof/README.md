# Task Overview
- Task ID: `0019`
- Slug: `reference-operator-runtime-proof`
- Objective: `建立可移植 Operator Runtime 契约，并以无副作用参考 Harness 验证 Selector、Binding、Execute、Verify、Trace 闭环`
- Status: `In Progress`

## In Scope
- 定义宽松的 OperatorBinding、OperatorRunRequest 与 OperatorRunRecord 互操作契约
- 实现确定性、无模型、无工具副作用的参考 Harness 闭环
- 为正常路径和失败关闭路径补齐自动化测试
- 把统一验证入口、PRD、ADR、架构文档和治理上下文同步到当前事实

## Out of Scope
- 中央运行时、通用 Planner、数据库、服务、队列或插件系统
- 真实模型调用、工具执行、生产 Harness 适配或外部写入
- 宣称 instruction materialization 等同于问题解决或方法有效

## Task Package Tree
- ROOT
  ├─ TP-01 [leaf] [P0] 定义运行时互操作契约
  ├─ TP-02 [leaf] [P0] 实现参考 Harness 闭环
  ├─ TP-03 [leaf] [P0] 建立失败关闭证据
  ├─ TP-04 [leaf] [P0] 同步架构与治理真相
  └─ TP-05 [leaf] [P0] 验证、审查与交付

## Requirement Alignment
- 目标: 建立可移植 Operator Runtime 契约，并以无副作用参考 Harness 验证 Selector、Binding、Execute、Verify、Trace 闭环
- approved plan 顶层步骤数: 5
- 编译后节点总数: 5
- 编译后叶子节点数: 5
- 对齐项: 用户在完整算子库汇报后要求执行下一阶段
- 对齐项: 当前静态库已有 468 条方法，但尚无 Selector、Binding、Execute、Verify、Trace 可运行闭环
- 对齐项: 项目边界要求执行能力由具体 Harness 本地拥有
- 计划摘要: 先冻结共享运行时信封与 Harness 本地职责，再做单文件参考 Harness，随后用反例和摘要重算证明 fail-closed，最后同步文档治理并运行项目门禁。

## Task Package Overview
| Task Package ID | Parent | Depth | Priority | Type | Leaf | Depends On | Wave | Ready | Parallelizable | Objective |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | P0 | action | Yes | - | 1 | Yes | No | 定义三个宽松 envelope、最小例子和静态验证入口 |
| TP-02 | ROOT | 1 | P0 | action | Yes | TP-01 | 2 | No | No | 实现确定性 Select、Bind、Materialize、Verify 与 Trace |
| TP-03 | ROOT | 1 | P0 | action | Yes | TP-02 | 3 | No | No | 覆盖未知绑定、策略不匹配、预算超限、循环/未知引用和摘要篡改 |
| TP-04 | ROOT | 1 | P0 | action | Yes | TP-03 | 4 | No | No | 更新 PRD、Operator Spec、Harness Model、ADR、README、AGENTS 和 module context |
| TP-05 | ROOT | 1 | P0 | action | Yes | TP-04 | 5 | No | No | 运行所有 required gates、strict governance、任务 closeout 和本地提交 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
