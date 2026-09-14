# Vibe-Mathing Practices: First-Round Synthesis

检索截面：`2026-08-13`。

## Executive Findings

1. `Vibe mathing` 不是一个已有统一定义的成熟学术术语。当前至少包含两条主线：开放式 LLM 数学探索，以及自然语言驱动形式化证明工程。[S01, S05, S10-S16]
2. `Vibe proving` 有相反的两种语用：批评“看起来像证明但可能有洞”的 raw LLM 文本；也指用户不熟悉 Lean、通过对话让 Agent 产出 kernel-checkable proof。任何报告都必须先声明采用哪一种。[S10-S11, S20-S21]
3. 可审计成功不是“提示词技巧”单点胜利，而是把廉价候选生成接到昂贵验证链：明确陈述、文献 scaffold、反例搜索、独立 referee、版本化修补、计算/Lean 检查、专家忠实性审计。[S05-S19]
4. 当前最稀缺资源已经从候选生成转向验证、理解与治理。公开追踪器和 First Proof 同时记录 full、partial、variant、incorrect；模型能快速制造证明稿，也能快速制造审稿债务。[S07-S09, S19-S24]
5. Lean 能显著缩小“推导是否成立”的信任面，但不能自动回答“形式化的是不是原题”“公理是否允许”“证明是否有数学意义”“结果是否新颖”。kernel check 是必要证据能力之一，不是单一终局标签。[S10-S18, S23-S24]
6. 截至本轮检索截面，没有发现获得普遍承认的 `Vibe-Mathing Standard`，更没有发现 ISO、IEEE 或 AMS 意义上的统一技术标准。现有规范性材料形成三层事实标准：社区伦理声明、期刊出版政策和案例驱动的实践工作流。[S05, S25-S28]

## 1. Working Taxonomy

### Pattern A — Conversational exploration

人类提供兴趣、直觉或候选对象，LLM 扩展文献线索、生成代码、探索例子和提出证明方向。产物首先是研究候选，而不是结果。Ken Clements 的实践是这一语义的早期明确表述。[S01]

### Pattern B — Generate, referee, repair

先让模型构造全局路线或证明稿，再用同模型新会话、另一模型或人类专家做 hypercritical referee，把批评转成显式证明义务，最后局部修补并重新检查下游依赖。Verbeken 等人的七会话、四版本案例是目前最可审计的 informal workflow 样本。[S05]

### Pattern C — Vibe formalization

人类给出精确 statement、informal proof、局部接口和库上下文，Agent 写 Lean，编译器反馈驱动修复，kernel 检查最终 proof term。高质量工程还要固定工具链、扫描逃逸机制、检查公理、清警告和删除死 proof code。[S10-S18]

### Pattern D — Broad candidate/contradiction mining

对公开问题目录、OEIS 或结构化候选批量运行模型/agent，记录 full、partial、variant、incorrect 和 prior-art rediscovery。价值在于扩大搜索前沿；风险是把状态不明的候选洪水转嫁给专家。[S06-S09, S19]

## 2. Case Matrix

| Case | Human role | AI role | Verification | What is reusable | Main caveat |
|---|---|---|---|---|---|
| Spectral region Conjecture 20 | 定目标、给经典 scaffold、发现错误、闭合边界条件 | 提全局路线、代数候选、referee、结构化重写 | 版本稿 + 人工检查 + 独立新会话批评 | obligation list、局部 patch、Lamport-style 依赖 | 单例、早期交互重建、无 formal proof |
| Primitive-set / Erdős #1196 | 非专家选择问题，专家提炼与重写 | 跳出惯用路径，产生关键连接 | Tao/Lichtman 审阅；后续有 formalization 线索 | 模型可作异质路线生成器 | 媒体叙事压缩了专家闭环 |
| Sphere packing Lean project | 定义/蓝图、数学管理、人工检查 | 生成部分 Lean proof | kernel + definition/axiom/hack scan + lean4checker | 多层形式审计，不只“能编译” | 大型项目的可读性与忠实性成本高 |
| Sidon counterexamples | 人类发现候选并组织论文 | 将有限反例编码成 Lean | machine checked | 非 Lean 专家也能获得小核验证 | 不是 AI 原创数学；更早结果影响新颖性 |
| AI4SLT | 人类分解、供 proof 与接口、清理 | 大规模 formalization | human-verified, sorry-free, warning/dead-code clean | 小上下文、接口签名、增量修错 | 工程 recipe 的跨领域泛化未知 |
| Erdős tracker / First Proof | 社区选题与专家裁决 | 多系统生成 full/partial/variant/incorrect 尝试 | 专家评论、部分 Lean | 状态多维化、失败也入账 | 动态状态、不同系统预算不可直接横比 |

## 3. Minimum Reproducible Workflow

### Phase 0 — Freeze the problem

- 保存原问题、量词、定义、版本、来源与允许公理。
- 写明 `prove / disprove / characterize / compute evidence` 中哪一个才是目标。
- 为 statement faithfulness 单设验收人；禁止在证明过程中悄悄改弱陈述。

### Phase 1 — Discovery before proof

- 建关键词、别名、旧名、领域分类和 prior-art ledger。
- 同时搜索证明、反例、等价形式和已知边界。
- 对开放问题先建立 novelty status：`unknown`，不是 `novel`。

### Phase 2 — Balanced candidate generation

- 让模型分别扮演 prover、disprover、literature scout 和 skeptical referee。
- 同时要求“给证明路径”和“找最小反例/失败条件”，降低确认偏差。[S06]
- 所有输出标记为 candidate；记录模型、配置、输入摘要和时间。

### Phase 3 — Turn prose criticism into obligations

- 把“这里不对”改写成有限检查项：domain、sign、branch、endpoint、compactness、measurability、dependency、hidden axiom。
- 优先局部 patch；每次 patch 后重跑受影响依赖，不让模型整篇重写掩盖根因。[S05, S14]
- 保存 A/B/C 版本和变更原因。

### Phase 4 — Mechanize the bottleneck

- 代数恒等式、有限搜索、数值边界交给 CAS/高精度/反例搜索。
- 可形式化核心进入 Lean；小引理分解，给局部接口签名与高质量 informal proof，不把整个代码库塞进上下文。[S14]
- 对 Lean 运行 build、`sorry/admit/unsafe/axiom` scan、`#print axioms`，必要时用独立 checker。[S10, S17]

### Phase 5 — Independent closure

- 生成主体不得为唯一 verifier。
- 独立检查 statement faithfulness、数学正确性、prior art、归因和结果重要性。
- 若证据失败，追加 invalidation 记录；不覆盖历史，不静默降级。

### Phase 6 — Publish an audit bundle

最小包应包含：

- 原陈述与来源；
- prompts/会话或至少输入摘要；
- 版本化 proof drafts；
- 计算/Lean 代码和固定依赖；
- 实际验证命令与输出摘要；
- 已知失败、剩余 obligations、人工贡献和模型贡献；
- verification status 与 novelty status 分开表达。

## 4. Verification Ladder Is Not a Ladder

应使用证据能力集合，而不是 `unverified < checked < Lean = true` 的单线等级：

| Capability | It establishes | It does not establish |
|---|---|---|
| Numeric check | 有限样本/精度下未发现失败 | 一般定理、无舍入误差 |
| Symbolic check | 指定恒等式/变换在系统语义下成立 | 前提覆盖、完整证明 |
| Human review | 专家认为论证可接受 | 绝对无错、独立复现 |
| Kernel check | proof term 证明了 formal statement | 原题忠实性、新颖性、可读性 |
| Axiom/escape audit | 没有禁止的信任捷径 | statement 正确表达现实目标 |
| Statement faithfulness | formal statement 对应原问题 | proof term 正确；需与 kernel check 组合 |
| Prior-art review | 归因与新颖性更可信 | 数学推导本身正确 |

## 5. Recurrent Failure Modes

1. **Problem drift**：模型证明较弱命题、变体或漏掉条件；Lean 仍可能完美通过。[S19]
2. **Polished gap**：文本整体专业，局部 branch/sign/endpoint 错误难以被非专家发现。[S05, S20]
3. **Prior-art rediscovery**：结果早已存在，甚至问题目录本身有误；形式正确不代表新贡献。[S11, S19]
4. **Confirmation loops**：连续让同一模型“继续修”容易保留共同盲点；需要 balanced prompting 和独立 session/model/human。[S05-S06]
5. **Rewrite regression**：长 Lean proof 出现多错误时，Agent 倾向抛弃大体正确结构进行剧烈重写。[S14]
6. **Proof bloat**：kernel-checkable 代码可能巨大、不可读、难以人工审计或维护。[S23-S24]
7. **Verification debt externalization**：发布大量 candidate，把甄别成本转嫁给少数专家。[S07-S09, S20-S23]
8. **Attribution compression**：媒体把“模型候选 + 专家数轮重写/复核”简化为“一个提示词独立解决”。[S03, S05]

## 6. Mature Tools Worth Reusing

### Immediate candidates

- `cameronfreer/lean4-skills`：成熟的 prove/review/refactor/golf/checkpoint 和 disprove 路径。[S15]
- `lean-lsp-mcp`：结构化 Lean 编译、目标和诊断接口。[S16]
- `Numina-Lean-Agent`：完整 agent scaffold、prompts、skills 和 run layout；适合做代表案例而非直接照搬全部依赖。[S12]
- AI4SLT `vibe-recipe/`：小引理、接口签名、warning/dead-code 清理的实践基线。[S14]
- `teorth/erdosproblems` AI wiki：动态发现成功、错误、变体和 prior-art 案例。[S19]

### Do not build yet

- 新的通用 proof agent、Lean kernel、文献搜索引擎或案例数据库。
- 在没有真实消费量和查询瓶颈前，把 Markdown 账本迁移到知识图谱/向量库。
- 仅靠模型互评给出独立验证标签。

## 7. Implications for `vibe-mathing-cn`

当前项目的 `Problem → Attempt → Result` 与二维 `outcome × evidence` 模型方向正确，且比许多公开案例的单标签更严格。下一切片应是三个垂直样例，而不是先造总控：

1. **Informal case**：复现 generate-referee-repair，保存版本稿和 obligation ledger。
2. **Computation case**：候选猜想 + 精确/高精度交叉检查 + 有限反例搜索，明确证据天花板。
3. **Lean case**：formal statement + proof + axiom/escape audit + statement-faithfulness review。

每个样例都应允许 `inconclusive/refuted/withdrawn`，并验证失败证据能让旧结论失效。只有这些垂直样例证明 schema 与 gate 足够，才实现 `/vibe-mathing` 总控。

## 8. Evidence Gaps and Next Search

- 缺少跨领域、预注册、可复现的“普通个人使用消费级 LLM 做研究数学”样本；S05 仍是单案例。
- 缺少 formal proof 的 statement-faithfulness 独立评测数据集。
- 缺少 proof bloat、审稿时间、token/API 成本、返工次数和失败率的统一统计。
- 中文公开的一手实践材料稀少，现有内容多为机构说明或二手报道。
- 需固定版本本地复跑一个 informal audit bundle 和一个 Lean bundle，验证公开说明是否足以复现。

## 9. Performance and Cost Review

本任务是文档检索，无运行时 hot path。当前 Markdown 账本的查询成本为线性扫描，但材料规模仅几十项，可读性与审计性优先，暂不优化。若增长到数千来源且出现高频交叉查询，再用 benchmark 比较 JSONL/SQLite；在此之前引入数据库只会增加所有权面。

外部实践的真正成本热点是：长上下文、重复模型调用、Lean 重编译和专家审阅。后续复跑应记录每轮调用数、token/API 成本、wall time、Lean build time、修补次数、人工审阅时长和最终未闭合 obligations，而不是只报告“成功”。

## 10. Normative Landscape

截至 `2026-08-13`，本轮检索没有发现获得普遍承认的 Vibe-Mathing 技术标准。当前更准确的描述是三层事实规范，而非单一标准：

1. **社区伦理规范**：Leiden Declaration 要求披露 AI、证明助手和数学软件的使用；正确性、引用与归因责任仍由人类承担；数学证据应尽可能开放并可独立验证；自动系统不能承担作者责任。该声明获 IMU 背书，但仍是社区倡议，不是技术接口标准。[S25]
2. **期刊出版规则**：LMS 明确要求人类作者检查内容、披露工具名称和用途、禁止 AI 署名，并限制在审稿中使用 AI。SIAM 也提供官方 AI 政策入口，但本轮因 HTTP 403 未直接核验正文，因此具体条款暂按待复核处理。[S26-S27]
3. **实践工作流**：最接近操作规范的是案例归纳，而非正式标准。Verbeken 等人的流程强调明确陈述、显式证明义务、竞争性修补、版本控制、回归检查与机械验证；Etingof 要求研究者完全理解、检查、重写并能解释采用的 AI 数学内容。[S05, S28]

因此，“外部已有伦理、出版和局部工作流规范，但尚缺统一、机器可验证的 Vibe-Mathing 技术规范”是当前证据支持的最准确结论。“没有统一标准”只表示本轮系统检索未发现，不是对所有未索引、付费或未来材料的绝对不存在证明。

## 11. Three Irreducible Laws

从“候选不得冒充事实、事实必须通过验证、事实必须可追溯且可撤销”三个不可再删的必要条件出发，九条候选要求最终压缩为三条基本法则：

1. **R1 — 候选隔离**：事实链是 `Problem → Attempt → Result`。Agent 只能产生 Attempt 和候选 Result；解库是合格 Result 的派生视图，不是第二套真相源。
2. **R2 — 验证准入**：只有独立验证链可以改变系统“真正知道什么”。Result 使用 `outcome × evidence`；证据是能力集合，不是线性等级；解库只收 `proof + established` 和 `counterexample + refuted`，并要求独立直接验证与 `statement_faithfulness=accept`。
3. **R3 — 证据守恒**：每项结论必须形成 `Problem → Attempt → Result → Verification Artifacts` 完整链条。证据与失效记录只追加，当前结论从有效证据重算；断链或证据失效时自动退出解库。

三条分别阻止身份污染、错误准入和历史失真，任何一条删除都会让不可信候选有路径污染解库。项目级规范真相源现为 [`VIBE-MATHING-SPEC v0.1`](../../standards/VIBE-MATHING-SPEC-v0.1.md)。

## 12. Operational Consequences

原九条候选要求不再作为九条并列基本法则；其中 Candidate-Only、Multidimensional Evidence、Independent Closure、Fail-Closed Formalization 和 Append-Only Invalidation 是三条法则的直接落实，Problem Contract、Tool Disclosure、Balanced Search 和 Versioned Repair 是可审计研究运行的操作层要求。

下一步用一个 informal 案例和一个 Lean 案例验证标准能否被真实运行记录、schema、校验器和审查门端到端执行；在完成前，本项目可以声明“规范 v0.1 当前生效”，但不能声明“完整工具链认证”或“外部标准符合性认证”。
