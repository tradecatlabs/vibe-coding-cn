---
id: MODCTX-PROBLEM-LIBRARY
type: context
status: current
owner: engineering
created: 2026-08-13
last_reviewed: 2026-09-01
review_cycle: P90D
---

# Problem Library Context

- 职责：保存公开来源观察、隔离 CandidateObservation 和经确认的 ProblemContract。
- 真相源：本地可重建的 `records/problems.jsonl` 与公开可版本化的 `records/canonical-problems.jsonl`，两者语义不可混用。
- 上游：Wikipedia、UnsolvedMath、ErdősProblems 及 registry 中的候选来源；原始响应位于被忽略的 `raw/`。
- 下游：Attempt 只能引用 `lifecycle=active` 的 canonical ProblemContract；CandidateObservation 只能形成 discovery shortlist。
- 核心风险：同名误合并、来源 ID 冲突、不完整摘要冒充精确定理陈述、来源状态被误当作数学结论、候选路径逃逸或 parser 未绑定。
- 验证：`python3 scripts/validate_portable_problem_library.py`、`python3 scripts/test_validate_candidate_problem_library.py`；具备 raw 时再运行 candidate/full validator/test。
