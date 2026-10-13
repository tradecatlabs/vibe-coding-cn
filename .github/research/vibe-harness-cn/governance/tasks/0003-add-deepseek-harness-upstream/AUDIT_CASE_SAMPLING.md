# Audit Case Sampling Decision

- Source: governance/tasks/0003-add-deepseek-harness-upstream
- Fixed Problem: 原则扫描器把表示不保证兼容的 `compatibility-breaking` / `破坏性兼容变更` 外部事实误判为兼容层并 BLOCK architecture gate。
- Decision: no-case
- Case ID: -
- Case Path: -
- Root Cause Class: negated-compatibility-lexical-false-positive
- Trigger Signals: compatibility-breaking, 破坏性兼容变更, future-optimal lexical scanner, architecture gate false positive
- Evidence: governance/tasks/0003-add-deepseek-harness-upstream/DEBUG.md；governance/tasks/0003-add-deepseek-harness-upstream/REGRESSION_EVIDENCE.json；tests/test_verify_project.py。
- No-Case Reason: 当前是项目专用词法扫描器的首次误报，已用正反控回归机械覆盖并修复 owning boundary；尚无第二个跨项目实例证明需要新增全局案例，且现有 Future-Optimal Gate 已覆盖真正 compatibility shim 的审计问题。

## Decision Values

- `case-created`
- `case-updated`
- `project-overlay`
- `promoted-to-gate`
- `no-case`

## Rule

每次问题修复后都必须填写采样判定。`no-case` 不是跳过；它必须给出明确理由。
