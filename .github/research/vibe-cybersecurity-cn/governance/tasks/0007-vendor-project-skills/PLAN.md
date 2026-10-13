# Planning Summary

把审计通过的 Web3/合约审计 skills 以 vendored 形式纳入项目供应链，
固定 commit 与许可，使用规则绑定授权求交，不安装全局。

# Lifecycle Gates

`SPEC -> PLAN -> BUILD -> TEST -> REVIEW -> SHIP`，任一 gate 不得跳过。

# Simplest Path

- 从沙盒复制选定 skill 到 `skills/`（tar 排除 .git）。
- 写 manifest + README + 入口同步。
- 校验与 closeout。

# Split Strategy

- TP-01：范围选择。
- TP-02：落地 + manifest。
- TP-03：治理同步。
- TP-04：closeout。

# Execution Waves

```text
TP-01 -> TP-02 -> TP-03 -> TP-04
```

# Next Executable Leaves

无。本任务已完成；下一任务按需抽查 skill 内容质量或扩展纳入范围。

# Dependency Graph

```text
0006 沙盒审计
    |
    v
TP-01 选范围 --> TP-02 vendored --> TP-03 治理 --> TP-04 closeout
```

# Runtime Workflow Contract

- Allowed：复制文件、写 manifest/文档、校验。
- Forbidden：执行 skill 脚本、安装全局、push。
- Stop：发现未审计内容混入。

# Rollback Protocol

- 删除 `skills/` 与 0007 目录即回滚；无外部状态。
