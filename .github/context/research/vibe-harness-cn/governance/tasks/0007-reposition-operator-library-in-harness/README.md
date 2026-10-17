# Task Overview
- Task ID: `0007`
- Slug: `reposition-operator-library-in-harness`
- Objective: `把问题求解算子库重新定位为 Harness 内部能力层，并同步需求、架构与治理边界`
- Status: `Done`

## In Scope
- 修正 Operator Library 在总体架构中的归属。
- 区分共享 Operator 规范、Harness 本地库存、执行 Binding 与元 Harness 治理目录。
- 更新 PRD、Harness 领域模型、ADR-0003、项目入口和治理上下文。
- 完成文档漂移审查与项目门禁。

## Out of Scope
- 不实现 Schema、算子 corpus、selector、runtime、adapter 或 registry service。
- 不修改 Harness manifest 契约和验证脚本。
- 不改写已完成任务 0006 的历史证据。
- 不引入数据库、UI、服务或新依赖。

## Task Package Tree
```text
TP-01 修正算子库的领域归属
  -> TP-02 同步架构决策与项目真相源
      -> TP-03 自审、验证与交付
```

## Requirement Alignment
- 用户确认：算子库存储思维模型与方法论，用于增强 Agent，属于 Harness 的内部组成。
- `Agent = LLM + Harness`；Operator Library 是 Harness 提供给 LLM 的问题求解能力之一。
- 元 Harness 不替代具体 Harness 执行算子，只制定共享规范并治理登记、分发、评测和生命周期。
- 保留执行与验证分离、权限由 Harness 裁决、跨 Harness 互操作等既有正确约束。

## Task Package Overview
| ID | 目标 | 主要输出 | Depends On |
|---|---|---|---|
| TP-01 | 修正组件归属、对象和运行流程 | PRD、HARNESS_MODEL | - |
| TP-02 | 同步长期架构真相 | ADR、README/AGENTS、治理上下文 | TP-01 |
| TP-03 | 检查一致性并形成证据 | REVIEW、校验与提交证据 | TP-02 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
