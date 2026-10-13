# Planning Summary

把 14 个社区安全 skills 候选拉进隔离沙盒，用静态审计确认无投毒模式与许可风险，
输出准入评估，为后续按需安装/采纳提供证据基线。

# Lifecycle Gates

`SPEC -> PLAN -> BUILD -> TEST -> REVIEW -> SHIP`，任一 gate 不得跳过。

# Simplest Path

- 沙盒：`.sandbox/skill-audit/`（gitignore 排除）。
- 拉取：`git clone --depth 1`，逐仓库超时与大小控制。
- 审计：一个 Python 脚本做统计 + 恶意模式 + 嵌入指令 + 许可核验。
- 报告：Markdown 落盘 0006。

# Split Strategy

- TP-01：沙盒与拉取。
- TP-02：审计扫描。
- TP-03：报告与准入建议。
- TP-04：治理同步与 closeout。

# Execution Waves

```text
TP-01 -> TP-02 -> TP-03 -> TP-04
```

# Next Executable Leaves

无。本任务已完成；下一任务按报告采纳优先项并做逐 skill 复核。

# Dependency Graph

```text
社区候选清单（上一轮扫描）
        |
        v
TP-01 沙盒拉取 --> TP-02 审计 --> TP-03 报告 --> TP-04 治理
```

# Runtime Workflow Contract

- Allowed：浅克隆、只读分析、写审计报告。
- Forbidden：执行仓库脚本、安装 skills、运行安装器、push。
- Evidence：克隆日志、扫描输出、报告、校验结果。
- Stop：发现高危投毒立即隔离并记录，不继续使用该仓库。

# Rollback Protocol

- 删除 `.sandbox/skill-audit/` 与 0006 目录即回滚；无外部状态。
