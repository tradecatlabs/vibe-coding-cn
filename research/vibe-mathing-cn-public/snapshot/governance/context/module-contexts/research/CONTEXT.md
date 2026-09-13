---
id: MODCTX-RESEARCH
type: context
status: current
owner: engineering
created: 2026-08-13
last_reviewed: 2026-08-13
review_cycle: P90D
---

# Research Context

- 职责：记录一次具体数学研究活动的目标、方法、输入、声明和产物。
- 真相源：`research/records/attempts.jsonl`。
- 上游：canonical Problem、文献目录和 active math skills。
- 下游：Result 必须引用一个存在的 Attempt。
- 核心风险：把运行完成、模型回答或有限实验误标为问题解决。
- 验证：`python3 scripts/validate_research_spaces.py`。
