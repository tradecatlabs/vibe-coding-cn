# Task Lessons Candidate Pool

本文件是任务级候选教训整理池，只记录尚未拆分、晋升或拒绝的原始经验材料。

## 使用规则

- 任务执行中发现的纠偏、失败复盘、可复用验收标准或防复发经验，可以先追加到这里。
- 写入后必须拆成原子事实：事实、来源、影响、通用规则、建议目标位置。
- 通用规则最终应晋升到 `governance/evidence/lessons/`、`governance/architecture-gates/rules/`、`governance/standards/`、`governance/processes/`、`governance/decisions/adr/` 或 `governance/context/module-contexts/`。
- 已晋升或拒绝晋升的条目，应保留简短处理记录，避免同一教训长期堆积在候选池。

## Candidate Lessons

- 2026-08-14：验证器不得猜测 owner 输出结构。已原子化晋升到
  `evidence/lessons/LESSON-0001-验证器必须消费-owner-契约.md`，不在候选池重复保留。
- 2026-08-14：上游源码研究必须绑定官方 revision 与可见性证据。已原子化晋升到
  `evidence/lessons/LESSON-0002-上游源码研究必须绑定官方-revision-与可见性证据.md`。
- 2026-09-03：问题求解算子库应作为 Harness 内部能力，而非 Harness 外部执行平面；共享规范治理
  与本地库存/Binding/运行状态必须分开。已晋升到 `standards/架构设计原则.md` 和 ADR-0003。
