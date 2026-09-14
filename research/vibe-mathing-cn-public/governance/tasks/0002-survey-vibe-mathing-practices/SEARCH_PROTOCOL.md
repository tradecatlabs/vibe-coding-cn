# Vibe-Mathing Search Protocol

## 1. Research Question

截至 `2026-08-13`，公开网络上有哪些可追溯的 vibe-mathing / vibe-proving 实践、工具、案例、验证方法、失败模式与争议？哪些做法能被本项目复用？

## 2. Working Definitions

### Core

来源明确使用 `vibe mathing`、`vibe mathematics`、`vibe maths` 或 `vibe proving`，并描述真实数学探索、证明或形式化活动。

### Adjacent

没有使用上述术语，但展示同一闭环：人类给目标或直觉，模型生成候选，计算机/专家批判，失败反馈驱动修补，最终产物可复核。

### Background

用于校准能力边界、验证瓶颈、职业规范、评测或传播风险的材料。背景材料不得冒充 vibe-mathing 原生案例。

## 3. Non-Goals

- AI 数学教育、题目讲解、动画生成和同名消费产品。
- 泛化的“AI 会不会取代数学家”评论，除非包含可检验案例或规范建议。
- 无原始链接、无真实仓库、无作者/日期或只有转载摘要的材料。

## 4. Keyword Families

### Exact terms

- `"vibe mathing"`, `"vibe-mathing"`, `"vibe mathematics"`, `"vibe maths"`
- `"vibe proving"`, `"vibe-proving"`, `"vibe proof"`

### Workflow terms

- `AI-assisted mathematics`, `LLM mathematical discovery`, `human AI proof collaboration`
- `generate referee repair mathematics`, `AI proof audit trail`, `AI formalization Lean`
- `natural language to Lean`, `agentic theorem proving`, `proof repair compiler feedback`

### Evidence and failure terms

- `incorrect AI proof`, `solution to variant problem`, `statement faithfulness`
- `Lean axiom audit`, `lean4checker`, `sorry-free`, `proof verification record`
- `AI contributions Erdős problems`, `First Proof comments`, `vibe proving criticism`

### Chinese/Japanese variants

- `氛围证明`, `氛围数学`, `vibe proving 实践`, `vibe mathing 数学`
- `バイブ証明`, `vibe-proving 数学`

## 5. Source Priority

1. 论文正文、正式出版物、作者公开会话与版本稿。
2. 官方代码仓库、proof artifacts、verification record、Lean 社区项目记录。
3. 数学家、研究机构、会议或社区的第一方说明。
4. 有署名、有原始链接的专业媒体。
5. 聚合站、社交平台和转载，只用于发现、传播分析或状态线索。

## 6. Evidence Fields

每项核心来源至少记录：

- stable ID、标题、作者/机构、日期、URL；
- core / adjacent / background；
- primary / institutional / secondary / aggregator；
- 可审计产物：会话、版本稿、代码、Lean 文件、验证记录、专家评论；
- 当前 verification status 与是否本地复跑；
- 可复用实践；
- 局限、冲突、潜在偏差。

## 7. Verification Semantics

证据不得压成单一“正确等级”。至少分开：

1. 候选是否生成；
2. 数值/符号检查是否覆盖关键子命题；
3. 自然语言证明是否经领域专家审阅；
4. 形式化代码是否由 Lean kernel 接受；
5. 是否只使用允许公理、无 `sorry/admit/unsafe` 等逃逸；
6. 形式化陈述是否忠实于原问题；
7. 证明是否可读、可维护、有数学解释价值；
8. 新颖性、重要性和归因是否经独立判断。

## 8. Search Providers and Failure Policy

- 首选：项目资源 → arXiv/GitHub/Lean 社区/机构站点 → 通用 Web。
- 搜索摘要只用于发现，随后打开正文或仓库。
- 429、CAPTCHA、付费墙最多合理重试并切换 provider；记录覆盖缺口。
- 动态聚合状态以检索日期为准，不推断历史版本。

## 9. Saturation / Stop Conditions

第一轮满足以下条件后停止广搜并进入增量模式：

- exact-term 关键词族均有命中或明确噪声结论；
- 论文、仓库、个人实践、机构说明、聚合索引、批评/失败六类来源均覆盖；
- 至少覆盖 informal 与 Lean-formal 两条实践链；
- 新一轮查询主要重复已登记案例，不再产生新实践范式；
- 重要强结论均有第一方或可审计产物支撑。

停止只表示“当前检索饱和”，不表示全网材料已穷尽。

## 10. Incremental Update Triggers

- 新的研究级公开案例附会话、代码或专家复核；
- 已登记案例发生撤回、纠错、同行评审或形式化状态变化；
- 出现新验证范式、公开工具链或大规模可复现实验；
- 每月一次轻量精确词检索，或重大 AI4Math 事件后专项检索。
