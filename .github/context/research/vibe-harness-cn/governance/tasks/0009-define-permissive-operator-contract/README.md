# Task Overview
- Task ID: `0009`
- Slug: `define-permissive-operator-contract`
- Objective: `建立结构严格、语义宽松、可由 Profile 加严的问题求解算子规范与契约`
- Status: `Blocked`

## In Scope
- 定义 Core Contract、Reference Library Profile 和 extensions 边界
- 放宽 Operator Pack Schema 的内容必填与封闭领域枚举
- 增加 Core Pack 校验入口和宽松/拒绝回归用例
- 同步规范、目录文档、ADR、QA 与治理上下文

## Out of Scope
- 修改 75+7 个既有条目内容
- 实现 OperatorBinding、selector、planner、运行时服务或外部标准完整版
- 放宽路径、安全 owner、类型判别或引用完整性边界

## Task Package Tree
- ROOT
  ├─ TP-01 [leaf] [P0] 定义宽松核心与 Profile 边界
  ├─ TP-02 [leaf] [P0] 放宽 Schema 并标注参考库 Profile
  ├─ TP-03 [leaf] [P0] 实现 Core 与 Reference 回归
  └─ TP-04 [leaf] [P0] 同步文档治理并完成验证

## Requirement Alignment
- 目标: 建立结构严格、语义宽松、可由 Profile 加严的问题求解算子规范与契约
- approved plan 顶层步骤数: 4
- 编译后节点总数: 4
- 编译后叶子节点数: 4
- 对齐项: 用户明确要求只把字段格式契约做严格，方法内容不能被模板锁死
- 对齐项: 现有 Schema 已完整承载 82 个条目，但把七个领域、语义字段和数量写成公共强约束
- 对齐项: 正确分层是 Core Contract 管互操作形状，Profile 管特定库质量和完整性
- 计划摘要: 先确定宽松核心与加严 Profile 的规范边界，再改 Schema/校验器和回归，最后同步长期项目真相并验证。

## Task Package Overview
| Task Package ID | Parent | Depth | Priority | Type | Leaf | Depends On | Wave | Ready | Parallelizable | Objective |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | P0 | documentation | Yes | - | 1 | Yes | No | 把规范性 MUST 与内容建议 SHOULD 分开 |
| TP-02 | ROOT | 1 | P0 | feature | Yes | TP-01 | 2 | No | No | 让新领域和渐进式定义可被结构契约表达 |
| TP-03 | ROOT | 1 | P0 | testing | Yes | TP-02 | 3 | No | No | 证明宽松不等于失去格式和安全门禁 |
| TP-04 | ROOT | 1 | P0 | delivery | Yes | TP-03 | 4 | No | No | 让所有长期真相源和任务证据与新分层一致 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md

## Closeout Blocker

- 规范、Schema、Profile、回归、文档和本地项目门禁已完成。
- owner 派生的高风险 retrospective 必须由仓库外受信 reviewer 签发 PASS receipt；当前只有通过
  strict validation 的 sealed draft，未生成或伪造 `RETROSPECTIVE_HANDOFF.json`。
