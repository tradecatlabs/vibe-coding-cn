# Audit Case Sampling Decision

- Source: governance/tasks/0009-define-permissive-operator-contract
- Fixed Problem: 公共 Schema 把当前参考库的领域、内容字段和集合数量误当成所有第三方 Pack 的强制标准。
- Decision: no-case
- Case ID: -
- Case Path: -
- Root Cause Class: core-profile-contract-boundary-drift
- Trigger Signals: 公共交换 Schema 出现单一实现专属枚举、固定内容数量或发布完整度要求。
- Evidence: docs/OPERATOR_SPEC.md；contracts/problem-solving-operator-pack.schema.json；governance/decisions/adr/ADR-0004-问题求解算子采用宽松核心与可选加严-Profile.md；governance/tasks/0009-define-permissive-operator-contract/REVIEW.md。
- No-Case Reason: 这是首次出现的项目契约分层问题，已经原子化沉淀到 ADR-0004、架构标准、QA-0003 和 Core/Profile 负例；现有 contract、future-optimal 与 document-drift review 能机械发现复发信号，另建 audit case 会重复已生效的项目规则。

## Decision Values

- `case-created`
- `case-updated`
- `project-overlay`
- `promoted-to-gate`
- `no-case`

## Rule

每次问题修复后都必须填写采样判定。`no-case` 不是跳过；它必须给出明确理由。
