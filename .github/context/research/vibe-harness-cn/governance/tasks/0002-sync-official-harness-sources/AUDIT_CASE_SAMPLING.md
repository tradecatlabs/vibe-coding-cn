# Audit Case Sampling Decision

- Source: governance/tasks/0002-sync-official-harness-sources
- Fixed Problem: depth=1 checkout 在官方分支普通前进后缺少祖先边，导致 fetch 显示 forced update 且 ff-only merge 误失败。
- Decision: no-case
- Case ID: -
- Case Path: -
- Root Cause Class: shallow-history-ancestry-evidence-gap
- Trigger Signals: shallow clone, forced update, unrelated histories, fast-forward verification
- Evidence: governance/tasks/0002-sync-official-harness-sources/DEBUG.md；governance/tasks/0002-sync-official-harness-sources/REGRESSION_EVIDENCE.json；tests/test_sync_upstreams.sh。
- No-Case Reason: 当前只在本项目首次出现；项目回归已机械覆盖普通前进、真实改写、错误分支、脏树和 ignored 文件。尚无第二个跨项目实例证明需要新增全局案例，来源真实性规则已晋升为项目 LESSON-0002。
