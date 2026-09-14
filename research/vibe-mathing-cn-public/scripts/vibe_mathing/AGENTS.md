# Runtime Package Agent Guide

本目录只实现单机可信研究闭环的连接层：证据解析、原子存储、状态机、确定性 adapter 与 CLI。数学事实仍由三张 JSONL 真相源和派生 Solution View 管理。

## 目录结构

```text
scripts/vibe_mathing/
├── AGENTS.md      # 包边界与维护规则
├── __init__.py    # 稳定公共入口
├── evidence.py    # 可信根、回执、摘要和 verifier registry
├── store.py       # JSONL 唯一 writer、flock、WAL 与原子恢复
├── runtime.py     # 有限状态机、预算、checkpoint 与有界子进程
├── pipeline.py    # 确定性 SymPy 候选、验证和晋升编排
└── lean.py        # 固定 Lean/Mathlib kernel、逃逸与公理审计
```

## 边界

- 上游：`research/verifiers.json`、Problem/Attempt/Result schema。
- 下游：`validate_research_spaces.py`、runtime CLI 与自动化测试。
- caller 自报的 locator、hash、verifier、independent 都不是事实；必须由本包现场重算。
- 不在此包内实现模型、CAS、证明内核、数据库或分布式调度器。
- 新增模块时同步更新本文件、`scripts/README.md` 和根 `AGENTS.md`。
