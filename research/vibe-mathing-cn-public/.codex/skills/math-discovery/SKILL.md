---
name: math-discovery
description: "数学问题发现与证据检索。用于界定研究问题、查定义/定理谱系、检索 arXiv/Scholar/OpenAlex/Crossref、建立来源账本、证据图、查新或从证据缺口生成可证伪猜想。"
---

# Math Discovery

把模糊兴趣变成可界定、可检索、可证伪的数学问题，并产出来源可追溯的证据图。

## Position in the Method Map

本 skill 负责方法地图第一层的“规格与语义”前置：在选择 Lean、SMT、model checking 或 abstract interpretation 之前，先冻结对象、定义域、量词、来源和可接受结论。对应的机器边界是 `ProblemContract`；地图总览见 [`FORMAL-METHODS-MAP.md`](../../../governance/standards/FORMAL-METHODS-MAP.md)。

## When to Use This Skill

- 需要查询某个定义、定理、证明技术或问题的前人工作。
- 需要从本地 admitted/candidate 问题语料发现研究方向，并判断来源成熟度或准入缺口。
- 需要建立关键词、别名、MSC/领域分类和检索式。
- 需要判断“是否已有类似结果”，或从冲突/空白形成候选猜想。
- 需要阅读论文并区分作者原始主张、证明依赖和当前综合判断。

## Not For / Boundaries

- “没搜到”不等于“从未有人研究”。
- 搜索摘要不能替代读取定理陈述与证明正文。
- 不把博客、搜索摘要或模型总结当作原始证据。
- 不在没有证明/计算证据时把候选猜想提升为结果。
- CandidateObservation 是来源发现材料，`research_eligible=false`；不得直接创建 Attempt，也不得把来源的 `answered/resolved/solved` 当作数学 Result。
- 默认只查询 admitted；只有用户明确需要扩展发现面时才使用 `--collection candidates|all`，并在输出中保留 collection、来源和许可边界。

## Quick Reference

```text
1. 固定对象、领域、问题和非目标。
2. 先查 `query_problem_library.py --collection admitted`；需要扩面时再显式查 candidates。
3. 建立术语：正式名、别名、旧名、符号、MSC、相邻领域术语。
4. 冻结检索式、来源、日期、语言和停止条件。
5. 优先原始论文、正式出版物、arXiv 原文和官方数据库记录。
6. 为每个来源记录稳定 ID、URL/DOI/arXiv ID、版本、raw locator 和证据位置。
7. 将关系标为 supports / contradicts / limits / extends / unknown；候选身份匹配只进入 review queue。
8. 输出已知事实、冲突、空白、候选猜想和下一步取证。
```

默认 provider 顺序：项目资源/MCP → SearXNG `arxiv,semantic scholar,openalex,crossref` →通用 Web。429/CAPTCHA 时记录失败并切换 provider；不无限重试。

## Examples

### Example 1：定理谱系
- 输入：“找 Szemerédi 正则性引理的主要变体。”
- 动作：冻结术语与范围，检索原论文和后续正式变体，构建依赖图。
- 验收：每项结论带稳定来源和定理位置；未读全文项标记未核验。

### Example 2：序列查新
- 输入：一组整数项和生成规则。
- 动作：先确认规则与索引，再用 OEIS/论文检索，区分序列匹配与定理匹配。
- 验收：不会因 OEIS 命中直接声称生成机制相同。

### Example 3：候选问题库选题
- 输入：“从新增问题库里找适合图论计算的开放问题。”
- 动作：显式查询 candidates，保留 source status、许可和 admission 状态；只生成待审 shortlist，不启动计算。
- 验收：每项均标为 `research_eligible=false`，唯一下一步是来源/陈述准入或 ProblemContract 冻结。

## References

- `references/source-map.md`：研究方法与检索供应链映射。
- `references/pressure-tests.md`：查新与摘要误用压力场景。

## Maintenance

- Sources：`rw-research-skill`、`wentor-research-plugins`、`kdense-scientific-skills`。
- Last updated：2026-08-13。
- Verification：供应链检查 + 搜索 provider smoke；外部数据库状态每次使用时重新核验。
