---
id: GOV-PUBLICATION-README
type: publication-guide
status: current
owner: engineering
created: 2026-09-07
last_reviewed: 2026-09-07
review_cycle: P90D
---

# 公共发布资产

本目录保存公共 README、`llms.txt` 和 AI 引用资产使用的声明元数据。

- `public-claims.v1.json` 记录公共声明、验证日期、证据引用和允许出现的文档表面。
- 公共概念架构以 [`../standards/POINT-LINE-FACE-BODY-METAMODEL-v0.1.md`](../standards/POINT-LINE-FACE-BODY-METAMODEL-v0.1.md) 为入口；PLFB 是唯一概念根，PWTSJ 是 F05，OSPS 是 F04。该声明不表示相关 runtime 已实现。
- 具体开放问题、问题总库和网页版研究套件的只读入口见 [`../../problem-library/VIBEMATHING_PUBLIC_INDEX.md`](../../problem-library/VIBEMATHING_PUBLIC_INDEX.md)。
- 声明账本不是 Problem、Attempt、Result 或 Solution 真相源；数学事实仍由 schema、记录、证据和派生索引决定。
- 动态网页、私密运行状态、凭据、内部端点和未准入候选禁止进入这里。
- GEO 固定查询和机器报告模板位于 `assets/ai-citation/`；报告模板只记录文档理解反馈，不是数学证据。
- 修改声明或 AI 引用资产后运行 `python3 scripts/check_public_readme.py` 与 `python3 scripts/check_ai_citation_assets.py`。
