# Planning Summary

用最少的三个对象表达问题、研究和成果；用 JSON Schema 管结构、Python 管跨记录不变量、GitHub Actions 复用同一 `make check`。数学内容保持空，先证明错误成果不能晋升。

# Lifecycle Gates

SPEC → PLAN → BUILD → TEST → REVIEW → SHIP。任何 Schema、引用、晋升负例、治理、公开仓库卫生或远端 CI BLOCK 都不得跳过。

# Simplest Path

复用标准文件格式、jsonschema、现有 Python 依赖、Git/GitHub Actions 和现有验证脚本；不引入服务、数据库、框架或新 Agent。

# Split Strategy

按契约、空间/治理、CI、交付四个串行叶子拆分。它们共享同一工作区，但每步均有独立校验信号。

# Execution Waves

1. TP-01：对象契约和晋升负例。
2. TP-02：目录、文档、治理、ADR/Gate。
3. TP-03：portable/full 检查和 CI。
4. TP-04：repo hygiene、Git、push、Actions 核验与 closeout。

# Runtime Workflow Contract

- 主 Agent 串行执行，不使用子代理。
- 所有脚本默认只读；`--write-index` 只修改派生 `solutions.json`。
- Git 不使用 reset/clean/stash/force，远端非空时停止直接初始推送。
- 凭据只由 `gh` 内建凭据管理器运行时使用，不写入仓库或日志。

# Next Executable Leaves

- TP-04：初始化 Git、审计 staged 清单、提交推送和核验 Actions。

# Dependency Graph

`TP-01 -> TP-02 -> TP-03 -> TP-04`

# Proof Point and Falsifier

- Proof point：本地 `make check` / `make check-full` PASS，模拟公开克隆 PASS，远端 Actions PASS。
- Falsifier：公开仓库包含 ignored/private/unknown-license 内容，或任一错误成果进入解库。

# Rollback Protocol

公开前删除新文件即可；公开后使用普通 Git revert。远端为空，不允许强推重写；派生索引可随时从 Result 重算。
