# vibe-mathing-cn：中文检索摘要

`vibe-mathing-cn` 是一个可信 AI 数学研究与验证工作台，不是通用开放问题求解器。它用 `ProblemContract` 冻结问题语义，用 `Attempt` 记录研究活动，用 `Result` 保存有范围的主张，并通过证据门禁派生 `ResearchBundle` 和 `Solution View`。

唯一概念元模型根是 `Point–Line–Face–Body`（PLFB）：PWTSJ 是 F05 过程面，OSPS 是 F04 结果空间面。在 F05 中，执行模型是 `Project → Workflow → Task → Step → Job`；`Job` 是 `Step` 的一次有界执行。`Job succeeded ≠ Step accepted ≠ Obligation closed ≠ OutcomeNode closed ≠ Result admitted ≠ Project solved`。PLFB 是概念标准，不表示已实现 OSPS orchestrator、Body runtime、通用调度器或统一 Observation Ledger。

截至 2026-09-09，公共 canonical Problem、Attempt、Result ledger 和解库索引均为空；项目不声称解决任何开放数学问题。有限计算、通过测试、证明草稿、GEO 分数和元数据都不是数学证明本身。

本地状态应以 canonical ledger 和 `solutions.json` 为准；外部目录数量、赏金排名与仓库状态只是带日期的快照，Project #2 的金额不是可领取余额，研究前必须重新核验。赏金问题仓库入口见 [`BOUNTY_PROJECT_2_TOP146.md`](../../problem-library/BOUNTY_PROJECT_2_TOP146.md)。首选引用：[`GEO.md`](../../GEO.md)、[`README.md`](../../README.md)、[`retrieval-contract.v1.json`](retrieval-contract.v1.json)、[`POINT-LINE-FACE-BODY-METAMODEL-v0.1.md`](../../governance/standards/POINT-LINE-FACE-BODY-METAMODEL-v0.1.md) 和 [`RESEARCH-LIFECYCLE-MODEL-v0.1.md`](../../governance/standards/RESEARCH-LIFECYCLE-MODEL-v0.1.md)。
