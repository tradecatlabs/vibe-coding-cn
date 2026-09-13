---
id: MODCTX-RESULT-LIBRARY
type: context
status: current
owner: engineering
created: 2026-08-13
last_reviewed: 2026-08-13
review_cycle: P90D
---

# Result Library Context

- 职责：保存候选、验证和拒绝的数学成果，并派生完整解视图。
- 真相源：`result-library/records/results.jsonl`；`indexes/solutions.json` 不是第二写入面。
- 上游：canonical Problem、Attempt 和真实证据产物。
- 下游：面向用户的解库查询和未来 `/vibe-mathing` 总控。
- 核心风险：证据越权、自我审查、陈述失真、手工制造解库条目。
- 验证：`python3 scripts/validate_research_spaces.py` 与 `python3 scripts/test_research_spaces.py`。
