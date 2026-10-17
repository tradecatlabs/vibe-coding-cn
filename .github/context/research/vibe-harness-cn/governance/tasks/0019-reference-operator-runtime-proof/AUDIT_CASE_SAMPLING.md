# Audit Case Sampling Decision

- Source: governance/tasks/0019-reference-operator-runtime-proof
- Fixed Problem: 本地深审发现 Runtime 嵌套稳定字段过宽、布尔值可穿透整数预算，以及验证拒绝时物化状态被错误改写；现已收紧 Schema、精确检查整数，并分开 materialization 与 verification 状态。
- Decision: no-case
- Case ID: CASE-0008
- Case Path: skills/workflow/modules/review/audit-cases/cases/CASE-0008-declared-marker-substitutes-for-derived-proof/CASE.md
- Root Cause Class: declared_marker_substitutes_for_derived_proof
- Trigger Signals: unknown field、schema validation、artifact digest、verification verdict 与 caller-supplied typed value。
- Evidence: Runtime Core self-test、`tests/test_reference_operator_harness.py` 的预算和 packet 篡改负例、任务 `REVIEW.md`。
- No-Case Reason: CASE-0008 已明确覆盖“Schema 禁止的未知字段是否也被运行时拒绝”、摘要是否重算、调用者声明是否穿透 validator 等审计问题；本轮没有新的根因类别或缺失的通用审计问题，因此不重复建案。

## Decision Values

- `case-created`
- `case-updated`
- `project-overlay`
- `promoted-to-gate`
- `no-case`
