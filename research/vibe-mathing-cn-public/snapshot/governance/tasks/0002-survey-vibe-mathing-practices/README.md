# Task Overview

- Task ID: `0002`
- Slug: `survey-vibe-mathing-practices`
- Objective: 深度检索并建立全网 vibe-mathing 实践材料的可追溯证据包。
- Status: `In Progress`
- Survey snapshot: `2026-08-13`

## In Scope

- 明确使用 `vibe mathing`、`vibe mathematics`、`vibe proving` 的原生材料。
- 邻接的 LLM 数学探索、研究级证明、Lean 形式化与人机协作实践。
- 原始论文、公开会话、版本稿、代码仓库、验证记录、专家复核和失败案例。
- 可直接复用的工作流、工具链、验证门和传播风险。

## Out of Scope

- AI 数学教育、解题 App 和同名 `VibeMath` 产品。
- 只有宣传摘要、无法回溯原始声明或虚构仓库的“教程”。
- 对每项数学成果重新做独立数学审稿或本地复跑全部大型 Lean 工程。
- 声称“全网穷尽”“首次发现”或把搜索未命中解释为材料不存在。

## Task Package Tree

- TP-01：冻结术语、检索协议、来源层级和停止条件。
- TP-02：检索案例、工具、论文、批评与中文材料，建立来源账本。
- TP-03：综合实践谱系、可执行工作流、风险门和项目落地建议。
- TP-04：持续增量检索、来源复核和高价值案例本地复跑。

## Requirement Alignment

用户要求“开始深度调研检索全网 vibe-mathing 实践材料”。本任务先完成可审计的第一轮广搜与综合，再保留增量入口；“全网”被解释为跨关键词族、语言、来源类型和证据等级的系统覆盖，而不是无法证明的绝对穷尽。

## Evidence Assets

- [SEARCH_PROTOCOL.md](SEARCH_PROTOCOL.md)：冻结检索范围、关键词、来源优先级和停止条件。
- [SOURCE_LEDGER.md](SOURCE_LEDGER.md)：逐项记录来源、证据层级、可审计产物、实践启示和限制。
- [SYNTHESIS.md](SYNTHESIS.md)：术语谱系、案例矩阵、可执行工作流、风险与项目建议。

## Task Package Overview

| ID | Parent | Depth | Priority | Type | Leaf | Depends On | Ready | Objective |
|---|---|---:|---|---|---|---|---|---|
| TP-01 | ROOT | 1 | P0 | discovery-contract | Yes | - | No | 冻结检索协议与证据等级 |
| TP-02 | ROOT | 1 | P0 | evidence-search | Yes | TP-01 | No | 建立跨来源实践材料账本 |
| TP-03 | ROOT | 1 | P0 | synthesis | Yes | TP-02 | No | 形成可执行实践协议与项目建议 |
| TP-04 | ROOT | 1 | P1 | continuous-research | Yes | TP-03 | No | 增量检索并复核高价值案例 |

## Reading Order

1. `SYNTHESIS.md`
2. `SOURCE_LEDGER.md`
3. `SEARCH_PROTOCOL.md`
4. `CONTEXT.md`
5. `PLAN.md`
6. `STATUS.md`
