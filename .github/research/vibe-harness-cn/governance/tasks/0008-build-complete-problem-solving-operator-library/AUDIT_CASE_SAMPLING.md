# Audit Case Sampling Decision

- Source: governance/tasks/0008-build-complete-problem-solving-operator-library
- Fixed Problem: 首版实现暴露了状态类型漂移和 MentalModel/Operator 执行边混淆，随后以 Schema、引用规则和负例修复。
- Decision: no-case
- Case ID: -
- Case Path: -
- Root Cause Class: operator-contract-type-boundary-drift
- Trigger Signals: Operator Schema 新增未批准状态类型，或 Method 把 MentalModelSpec 作为可执行 `use` 边。
- Evidence: contracts/problem-solving-operator-pack.schema.json；scripts/validate_operator_library.py；scripts/validate_harness.py；governance/tasks/0008-build-complete-problem-solving-operator-library/REVIEW.md。
- No-Case Reason: 两个问题均为首次出现的项目私有契约设计问题，已由 `control_state` 移除、`apply_model` 类型边、循环检测和负例机械阻断；现有 contract/agent-harness review 已覆盖其通用类别，当前没有跨项目复发证据，新增全局或项目案例会重复已落地 Gate。

## Decision Values

- `case-created`
- `case-updated`
- `project-overlay`
- `promoted-to-gate`
- `no-case`

## Rule

每次问题修复后都必须填写采样判定。`no-case` 不是跳过；它必须给出明确理由。
