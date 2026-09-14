# Task-Level Acceptance

- [x] 已冻结工作定义、关键词族、来源层级、时间截面和停止条件。
- [x] 已覆盖术语原生材料、个人实践、研究论文、代码工具、形式化案例、聚合索引、批评与失败材料。
- [x] 每个核心来源都有稳定 URL、来源类型、可审计产物、实践价值与限制。
- [x] 综合报告明确区分生成能力、数学正确性、形式化正确性、陈述忠实性、可读性和数学意义。
- [x] 已形成可执行的最小 vibe-mathing 工作流与 fail-closed 门禁。
- [x] 已将规范候选压缩为三条不可约法则，并晋升为项目级 `VIBE-MATHING-SPEC v0.1`。
- [ ] 对选定的代表案例做本地可重跑复核，并持续吸收新材料。

# Validation Plan

- 运行任务文档 decompose 校验，确保无占位符、任务树和状态一致。
- 运行 Markdown 链接与治理包 strict/health 校验。
- 抽查来源 URL、发布日期、论文/仓库/验证记录之间的引用关系。
- 对综合报告中的强结论逐条回指 `SOURCE_LEDGER.md`。

# Review Gate

- BLOCK：把未核验作者声明写成已证实事实；把搜索未命中写成不存在；把二手摘要当原始证据。
- BLOCK：把 kernel check 当 statement faithfulness，或把自然语言漂亮程度当证明正确性。
- WARN：仅有公司/作者自报、动态聚合状态、缺少公开会话或无法本地复跑。

# Runtime Verification Gate

- 第一轮只证明“材料发现与综合可追溯”，不证明账本内全部数学结论正确。
- 外部代码/Lean 项目尚未逐个本地构建；相应条目明确标记为未本地复核。
- 后续本地复跑必须固定 commit、Lean/Mathlib 版本、命令、axiom scan 和 statement-faithfulness review。

# Ship Readiness

第一轮证据包在文档校验、治理 strict/health 和来源抽查通过后可交付；总任务保持 `In Progress`，因为持续增量检索与代表案例复跑尚未完成。

# Task Package Acceptance

- TP-01：检索协议可由另一名研究者复用，不依赖聊天上下文。
- TP-02：来源账本同时收录成功、失败、争议、工具和聚合材料。
- TP-03：综合结论不越过证据等级，并给出具体可执行协议。
- TP-04：新增材料只有在稳定来源、状态与限制齐全后进入核心账本。

# Anti-Goals

- 不建立新的通用数据库、爬虫框架或 skill。
- 不把材料数量当质量，不追求堆满转载链接。
- 不为任何公司、模型或工具做能力背书。
