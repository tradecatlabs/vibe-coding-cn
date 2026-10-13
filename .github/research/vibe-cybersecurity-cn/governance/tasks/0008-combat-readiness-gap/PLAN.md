# Planning Summary

盘点 0001-0007 全部交付物，量化"真实授权协议 fork 级审计"就绪度，
输出综合评分、P0/P1/P2 差距清单与 M1-M4 里程碑路径，并同步治理文档。

# Lifecycle Gates

`SPEC -> PLAN -> BUILD -> TEST -> REVIEW -> SHIP`，任一 gate 不得跳过。

# Simplest Path

- 复用既有证据（INDEX、ADMISSION_TABLE、web3-lab/evidence、SKILLS_MANIFEST），
  不重新运行工具。
- 评分直接落盘 `governance/context/COMBAT_READINESS.md`，一次到位。
- 治理同步只改 6 个既有文档，不新建抽象。

# Split Strategy

- TP-01：现状盘点与证据核实。
- TP-02：就绪度评分与差距清单（COMBAT_READINESS.md）。
- TP-03：治理文档同步（拓扑/操作模型/context-map/README/INDEX/AGENTS）。
- TP-04：closeout 校验。

# Execution Waves

```text
TP-01 -> TP-02 -> TP-03 -> TP-04
```

# Runtime Workflow Contract

- Allowed：只读盘点、文档编辑、本地校验命令。
- Forbidden：拉取真实协议仓库、接入 RPC、执行扫描、push、破坏性 git。
- Evidence：现状表、评分表、差距清单、strict/health 输出。
- Stop：证据与现状不符或校验失败且无法定位时停止。

# Next Executable Leaves

无。本任务已完成；下一任务（M1）在用户提供授权协议仓库后启动管线骨架。

# Dependency Graph

```text
0001-0007 交付物与证据
        |
        v
TP-01 现状盘点 --> TP-02 就绪度评分 --> TP-03 治理同步 --> TP-04 closeout
```

# Rollback Protocol

- 恢复 `INDEX.md` 当前任务行
- 恢复本任务目录到初始化状态
- 不得影响其他任务目录
