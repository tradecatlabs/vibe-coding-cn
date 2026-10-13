# Audit Case Sampling Decision

- Source: governance/tasks/0007-reposition-operator-library-in-harness
- Fixed Problem: 原需求把 Operator Library 画成 Harness 外部的独立执行平面，造成共享规范治理与业务运行时所有权混淆。
- Decision: no-case
- Case ID: -
- Case Path: -
- Root Cause Class: architecture-ownership-confusion
- Trigger Signals: 文档出现中央 Operator Runtime、双运行状态 owner，或把 Catalog、Library、Binding 混为一体。
- Evidence: docs/PROBLEM_SOLVING_OPERATOR_ARCHITECTURE_PRD.md；governance/decisions/adr/ADR-0003-引入问题求解算子语义层.md；governance/standards/架构设计原则.md；governance/tasks/0007-reposition-operator-library-in-harness/REVIEW.md。
- No-Case Reason: 这是首次发现的项目领域边界错误，已直接固化为 ADR 和 Harness 架构不变量；现有 agent-harness ownership 审查已覆盖同类问题，当前没有第二次复发或新增机械检测条件，单独建案例只会重复规则。

## Decision Values

- `case-created`
- `case-updated`
- `project-overlay`
- `promoted-to-gate`
- `no-case`

## Rule

每次问题修复后都必须填写采样判定。`no-case` 不是跳过；它必须给出明确理由。
