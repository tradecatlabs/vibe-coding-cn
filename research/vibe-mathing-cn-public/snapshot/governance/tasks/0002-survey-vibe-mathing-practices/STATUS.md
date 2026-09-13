# Task Status

- Overall Status: `In Progress`
- Survey snapshot: `2026-09-01`
- First-round status: `Complete`

# Next Executable Leaves

- 无；TP-04 已处于 `In Progress`，下一次恢复时先核对其最新状态与输入，再继续执行。

# Task Package Status Table

| Node ID | Parent | Depth | Depends On | Ready | Status | Recent Evidence | Blocker | Unblock Needed |
|---|---|---:|---|---|---|---|---|---|
| TP-01 | ROOT | 1 | - | No | Done | 核心/邻接/背景范围和停止条件已冻结 | - | - |
| TP-02 | ROOT | 1 | TP-01 | No | Done | 来源账本覆盖论文、仓库、案例、批评与失败 | - | - |
| TP-03 | ROOT | 1 | TP-02 | No | Done | 综合报告与可执行工作流已形成 | - | - |
| TP-04 | ROOT | 1 | TP-03 | No | In Progress | 已确定候选复核案例与工具链 | 大型外部工程尚未本地复跑 | 固定 commit、工具链并运行验证 |

# Blockers

没有阻止第一轮交付的 blocker。付费墙、封闭社群、未索引内容和动态站点历史版本构成持续覆盖缺口。

# Runtime State

- 检索主流程：`math-discovery`。
- 任务与治理编排：`auto-tasks` + `auto-governance`。
- 研究形态：单 Agent、跨来源 Web 检索、人工证据分级。
- Public export 已补充 ProblemContract/ResearchBundle schema、候选隔离管线、工具成熟度契约和可移植测试；没有携带内部运行报告、候选 raw 或研究记录。

# Recent Evidence

- 原生术语材料显示 `vibe mathing` 从对话式探索扩展为研究协作方法。
- `vibe proving` 同时存在“漂亮但可能有错的自然语言证明”与“自然语言驱动 Lean、kernel 检查”的相反语用，报告已显式分流。
- 高价值案例共同采用候选生成、独立批判、版本化修补和可检查产物，而非信任单次模型输出。
- Erdős/First Proof 等公开记录同时包含成功、变体误解、重大缺口和错误尝试，证明失败状态必须是一等数据。
- 新增规范景观：当前未发现统一的 Vibe-Mathing 技术标准；可复用要求来自 Leiden Declaration、LMS/SIAM 出版政策、可审计案例工作流和 Etingof 研究指南。
- 已把九条候选要求按第一性原理压缩为三条不可约法则，并晋升到项目级 `VIBE-MATHING-SPEC v0.1`；现有 schema、校验器与 GATE-0002 执行核心不变量，代表案例复跑继续验证端到端工具链。

# First-Round Handoff Snapshot

第一轮全网深度调研已完成并落盘；总任务保持 `In Progress`，后续继续做代表案例的本地复跑。

## Core Conclusions

- `vibe mathing` 主要指开放式人机数学探索；`vibe proving` 同时指“可能有隐蔽错误的自然语言证明”和“自然语言驱动 Lean 形式化”，必须区分。
- 可靠实践的共同模式是：生成 → 严苛审稿 → 显式证明义务 → 局部修补 → 回归检查 → 独立验证。代表性可审计案例见 [Verbeken et al., arXiv:2602.18918](https://arxiv.org/abs/2602.18918)。
- Lean kernel check 只能证明形式化陈述，不能自动证明陈述忠实性、新颖性、可读性和数学价值。
- 当前真正稀缺的是验证与审稿能力。[First Proof](https://arxiv.org/abs/2602.05192) 与 [Erdős AI 贡献记录](https://github.com/teorth/erdosproblems/wiki/AI-contributions-to-Erd%C5%91s-problems) 均同时存在正确、部分、变体和错误结果。
- 优先复用成熟工具：[lean4-skills](https://github.com/cameronfreer/lean4-skills)、[lean-lsp-mcp](https://github.com/oOo0oOo/lean-lsp-mcp)、[Numina-Lean-Agent](https://github.com/project-numina/numina-lean-agent)。

## Primary Artifacts

- `SYNTHESIS.md`：术语谱系、案例矩阵、实践协议与项目建议。
- `MATH_TOOL_LANDSCAPE.md`：公开工具成熟度状态机、证据上限和 canary 边界；不引用内部运行盘点。
- `SOURCE_LEDGER.md`：来源、证据层级、可审计材料与局限。
- `SEARCH_PROTOCOL.md`：检索范围、来源优先级、失败策略与停止条件。
- `REVIEW.md`：审查结论、风险、未知项与总任务门禁。
- `STATUS.md`：任务状态、阶段证据与下一步恢复入口。

## Validation Snapshot

- `auto-tasks decompose` 校验：`PASS`，零占位符。
- `make check`：`PASS`。
- governance strict/health：`PASS`，0 issue、0 stale、0 placeholder。
- `git diff --check`：`PASS`。
- 审查裁决：`WARN`。外部 Lean 工程尚未固定版本本地复跑，动态聚合站状态可能漂移；限制已记录在 `REVIEW.md`。
- 交付状态：本轮公开导出待提交/推送；canonical/Attempt/Result 业务记录仍未新增，运行报告和私密材料未导出。

## Next Slice

固定一个 informal `generate-referee-repair` 案例和一个 Lean 案例，记录真实工具链、固定版本、构建命令、公理扫描、陈述忠实性与成本数据。
