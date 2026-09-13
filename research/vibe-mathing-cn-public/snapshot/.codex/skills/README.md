# Project Skills

这里保存当前项目 active skills。每个目录只有一个稳定 owner；上游方法先进入 `vendor/`，经过 owner mapping、依赖适配和压力测试后才能进入本目录。

| Skill | 单一职责 |
|---|---|
| `vibe-mathing-router` | 根据当前瓶颈选择一个主流程 |
| `math-discovery` | 研究问题、检索、来源和证据图 |
| `math-derivation` | 公式推导与假设/近似边界 |
| `math-computation` | 符号、数值与反例计算 |
| `math-proof` | 自然语言证明与证明义务审计 |
| `math-formalization` | proof assistant 形式化与 kernel 验证 |

`CandidateObservation` 只归 `math-discovery`，且始终 `research_eligible=false`。工具调研按 `surveyed → source_locked → installed → smoke_checked → evidence_capable → verifier_admitted` 逐层准入；只有公开 registry 和 runtime probe 支持的能力才能进入 owner 路由。

## 方法层主线

Skill 路由遵循 [`governance/standards/FORMAL-METHODS-MAP.md`](../../governance/standards/FORMAL-METHODS-MAP.md) 的两层地图，而不是把 Lean 教程目录当作形式化方法总览：

```text
规格与语义
  → 演绎验证/定理证明（Lean 的主战场）
  → 模型检查 / 抽象解释 / SAT/SMT/符号推理（含符号执行）
  → 精化与程序综合

Lean 六层栈：类型理论与 Kernel → 语言与 elaboration → Proof Engineering
  → 自动化与决策过程 → Library Engineering → 应用形式化/验证
```

`ProblemContract` 负责规格与语义边界；`math-proof` 负责证明义务；`math-formalization` 负责 Lean 陈述、proof term、kernel/axiom/escape/faithfulness 分离；`math-computation` 负责有界计算和横向自动化。Lean kernel 检查证明项，但不替代原始命题的 statement-faithfulness 审查。

## 顶层生命周期中的 Skill 位置

项目按 `Project → Workflow → Task → Step → Job` 组织执行；skills 主要为具体 `Step` 提供 owner 操作，`Job` 只记录一次有界执行。Skill 路由不创建通用调度器，也不能用 Job/Workflow 完成状态替代 `ProblemContract → Attempt → Result` 的数学证据链。
