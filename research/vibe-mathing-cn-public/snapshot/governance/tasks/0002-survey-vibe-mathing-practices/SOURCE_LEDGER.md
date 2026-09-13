# Vibe-Mathing Source Ledger

检索截面：`2026-08-13`。`Primary` 表示原论文、原仓库、作者材料或直接项目记录；它不自动代表数学结论正确。`Local replay` 均为本轮是否在本机复跑，而非作者是否运行过。

## A. Terminology and Practice Narratives

| ID | Layer / type | Source | Auditable material | Practice signal | Limits |
|---|---|---|---|---|---|
| S01 | Core / Primary | [Ken Clements, “Vibe Mathing”](https://kenclements.substack.com/p/beyond-binary-claims-mathematical-170), 2025-07-20 | 连续系列文章、作者描述的对话与计算实践 | 将其定义为与 LLM 反复讨论、沿想法探索、寻找证明；包含代码生成和分布式序列搜索 | 个人叙事；部分数学主张和投稿状态未在本轮独立复核 |
| S02 | Core / Primary | [Patrick White, “Two Months of Vibe Mathing”](https://pwhite.org/vibe-mathing), 2026-07 | 16 项作者自报结果、部分公开论文/代码、two-seat reasoner/checker 方法 | 展示非数学专业用户组织批量案例、独立 checker 和结果追踪 | 多数 checker 在私有仓库；具体案例需逐项回到公开论文/代码，不能接受作者“checked”标签本身 |
| S03 | Core / Secondary | [Scientific American: 60-year-old primitive-set problem](https://www.scientificamerican.com/article/amateur-armed-with-chatgpt-vibe-maths-a-60-year-old-problem/), 2026-04-24 | 对 Liam Price、Kevin Barreto、Tao、Lichtman 的采访 | 一次候选生成可以跳出人类惯用路径，但原始输出需要专家提炼和重写 | 媒体报道；应继续回溯原证明、专家稿与 formalization |
| S04 | Core / Aggregator | [VibeMathed](https://vibemathed.com/)（[methodology](https://vibemathed.com/methodology)、[GitHub](https://github.com/mrconter1/vibemathed)） | 动态案例目录、验证标签、来源链接、CC BY 4.0 数据集 | 适合发现候选案例和观察“声明数 vs 验证数”差距 | 首页与标签小时级变化；定义、历史快照和单项来源需分别审计，不作数学真相源 |

## B. Auditable Informal-Proof Workflows

| ID | Layer / type | Source | Auditable material | Practice signal | Limits |
|---|---|---|---|---|---|
| S05 | Core / Primary | [Verbeken et al., arXiv:2602.18918](https://arxiv.org/abs/2602.18918), 2026-02-21 | 7 个公开会话、4 个版本稿、角色分工和错误清单 | `generate → referee → repair`；把批评转成 branch/sign/endpoint 等证明义务；版本化防回归 | 单个结构良好、已有经典模板的问题；早期交互部分为重建；未形式化 |
| S06 | Adjacent / Institutional | [Google DeepMind: Gemini Deep Think scientific discovery](https://deepmind.google/blog/accelerating-mathematical-and-scientific-discovery-with-gemini-deep-think/), 2026-02-11 | 论文链接、案例分类、Aletheia 架构与协作 recipe | natural-language verifier、允许承认失败、balanced prompting（同时求证与求反例）、Advisor 协作 | 公司第一方总结；案例正确性仍应回到论文与专家审查 |
| S07 | Background / Primary | [First Proof](https://arxiv.org/abs/2602.05192) 与 [solutions/comments](https://1stproof.org/documents/FirstProofSolutionsComments.pdf), 2026-02 | 10 个研究问题、官方解答和逐项评论 | 用未公开研究问题测试长链证明；专家评论揭示“像证明”与出版级证明的差距 | 小样本，领域覆盖有限；不同系统交互预算未必可比 |
| S08 | Background / Institutional | [OpenAI First Proof submissions](https://openai.com/index/first-proof-submissions/), 2026-02-20 | 全部尝试、prompt appendix、后续纠错说明 | 明确撤回此前认为可能正确的 Problem 2 尝试；支持证据可失效模型 | 公司自报；“high chance”不是独立 PASS |
| S09 | Adjacent / Primary | [Aletheia tackles FirstProof autonomously, arXiv:2602.21201](https://arxiv.org/abs/2602.21201) | 论文与公开 raw prompts/outputs 链接 | 生成—验证—修订 agent loop，可与专家基准对照 | 需逐项检查原始输出和官方评论；本轮未本地重跑 |

## C. Lean / Formal Vibe-Proving

| ID | Layer / type | Source | Auditable material | Practice signal | Limits |
|---|---|---|---|---|---|
| S10 | Core / Primary | [Lean community Sphere Packing Project](https://leanprover-community.github.io/blog/posts/SpherePacking-1/), 2026 | Lean 代码、项目叙事、definition/axiom/metaprogramming 检查、lean4checker 复核 | AI 生成 Lean 后仍做定义冻结、公理审计、hack 扫描与外部 checker | 形式化项目的完整数学忠实性和可维护性仍需持续人工审阅 |
| S11 | Core / Primary | [Alexeev & Mixon, “Forbidden Sidon subsets…”](https://borisalexeev.com/pdf/erdos707.pdf), 2026 | 论文与机器检查的反例形式化 | 非 Lean 专家可用 ChatGPT “vibe code” 验证有限反例；kernel 将信任面缩小 | 机器检查反例不等于 AI 发现新数学；论文也发现更早人类反例，归因需谨慎 |
| S12 | Adjacent / Primary | [Numina-Lean-Agent](https://github.com/project-numina/numina-lean-agent) / [arXiv:2601.14027](https://arxiv.org/abs/2601.14027) | MIT 仓库、setup、prompts、skills、run outputs、论文 | coding-agent + Lean LSP/MCP + 搜索/验证技能；适合交互式 formalization 和 proof engineering | 多个外部 API/凭据与较重环境；结果声明需固定 commit 和复跑 |
| S13 | Adjacent / Institutional | [中科院数学院：Numina-Lean-Agent](https://www.amss.ac.cn/kyjz1/202602/t20260205_8140300.html), 2026-02-05 | 中文机构说明、代码和论文链接 | 报告两周完成 Effective Brascamp–Lieb inequalities 论文级形式化 | 机构项目说明，非独立评测；具体形式化应回到仓库与论文 |
| S14 | Adjacent / Primary | [AI4SLT / lean-stat-learning-theory](https://github.com/YuanheZ/lean-stat-learning-theory) | ~30k 行 human-verified Lean、`vibe-recipe/`、unused-have detector | 小引理分解、只给接口签名与高质量 informal proof、清 warning、删死 `have`；记录长证明剧烈重写失败模式 | 特定统计学习理论工程；经验是否泛化到所有领域需验证 |
| S15 | Adjacent / Primary | [cameronfreer/lean4-skills](https://github.com/cameronfreer/lean4-skills) | MIT 仓库、prove/review/refactor/golf/checkpoint 工作流、axiom guardrails | 成熟的 draft→prove→review→refactor→checkpoint 路径；支持 disprove 与预算停止 | 工具仍依赖目标声明和库上下文质量；kernel PASS 不自动审计 statement faithfulness |
| S16 | Adjacent / Primary | [lean-lsp-mcp](https://github.com/oOo0oOo/lean-lsp-mcp) | Lean LSP 的 MCP 接口、版本匹配说明 | 给 agent 结构化目标、诊断、搜索和编译反馈，是“写→编译→修复”闭环基础 | 需要匹配 Lean 版本与安全配置；只是接口，不保证证明策略质量 |
| S17 | Background / Primary | [OpenAI cdc-lean verification record](https://github.com/openai/cdc-lean/blob/main/VERIFICATION.md), 2026-07-09 | toolchain commit、build 命令、escape-hatch scan、`#print axioms` | 优质形式化发布应携带可复跑 verification record，而非只说“Lean checked” | 仍需独立 statement-faithfulness 和数学价值审查；本轮未本地复跑 |
| S18 | Background / Primary | [Leo de Moura, “Machine-Checked Mathematics in the Age of AI”](https://leodemoura.github.io/static/icml2026/), 2026-07-10 | 公开演讲、Lean proof 示例、可独立检查理念 | proof assistant 是人机共享环境；AI 改变生成方式，不改变小 kernel 与独立检查的价值 | 演讲为观点与案例概述，不替代每个项目的审计 |

## D. Trackers, Failures, Norms, and Criticism

| ID | Layer / type | Source | Auditable material | Practice signal | Limits |
|---|---|---|---|---|---|
| S19 | Adjacent / Primary community record | [AI contributions to Erdős problems](https://github.com/teorth/erdosproblems/wiki/AI-contributions-to-Erd%C5%91s-problems) | 逐问题来源、模型、日期、full/partial/variant/incorrect 状态、文献先例 | 失败、变体、旧结果重发现和部分进展必须与成功一起记录 | Wiki 动态更新；状态可能变化，应保存检索日期并回到每个问题页 |
| S20 | Background / Primary | [Emily Riehl, Hardy Lecture on professional norms](https://emilyriehl.github.io/files/norms-hardy.pdf), 2025 | 带微妙错误的生成证明样例、职业规范讨论 | 流畅文本降低错误可见性；审稿负担和数学文献污染是系统性成本 | 规范性演讲，不是能力 benchmark |
| S21 | Background / Primary | [Kevin Buzzard, “Where is mathematics going?”](https://leanprover.zulipchat.com/user_uploads/3121/0VmATIJSpRi9aTbnedDsqLje/talk.pdf), 2025 | 演讲幻灯片 | 将 raw LLM “vibeproving” 的逻辑缺口与 Lean 检查闭环明确对照 | 高层概述；不提供单一模型的系统实验 |
| S22 | Background / Institutional | [ICARM: Neural Proving](https://icarm.io/neural-theorem-proving/) | 研究机构对 autoformalization、工具和数学共同体中介角色的说明 | 工具评估、社区中介、可理解性与规范治理和模型能力同等重要 | 项目概览，具体性能应回到论文/代码 |
| S23 | Background / Primary commentary | [Xena: Mathematicians learning Lean by doing](https://xenaproject.wordpress.com/) | Lean 社区实践评论 | 指出大多数现代研究对象尚未形式化；“能 formalize 某个例子”不能推广为研究数学普遍可用 | 博客观点；需结合 mathlib 覆盖的定量研究 |
| S24 | Background / Primary commentary | [ProofJudge: Can we align vibe-proving with human taste?](https://hackbot.dad/writing/proofjudge-and-taste/) | 对形式正确但不可读/无用 proof 的案例与实验 | correctness 之外还有证明品味、可维护性和教学/研究价值 | 个人实验，评价函数与样本覆盖有限 |

## E. Ethics, Publishing, and Research Norms

| ID | Layer / type | Source | Auditable material | Practice signal | Limits |
|---|---|---|---|---|---|
| S25 | Background / Community declaration | [Leiden Declaration on Artificial Intelligence and Mathematics](https://leidendeclaration.ai/), 2026-06-02 | 声明正文、DOI、签署与 endorsement 信息；页面明确标注获 IMU 背书 | 披露自动化工具；人类作者保留正确性与引用责任；开放可验证；AI 不承担作者身份 | 伦理倡议和社区规范，不是 ISO/IEEE/AMS 意义上的技术标准，也不直接定义机器可验收字段 |
| S26 | Background / Publisher policy | [London Mathematical Society: Artificial Intelligence](https://www.lms.ac.uk/publications/policies/AI), updated 2026-06 | LMS 期刊伦理政策节选，覆盖作者、审稿人与编辑 | AI 不得署名；作者必须检查准确性、引用和抄袭风险，披露工具名称及其用途；审稿不得上传稿件给 AI | LMS 出版范围内的政策，不等于全数学共同体统一标准 |
| S27 | Background / Publisher policy | [SIAM: Artificial Intelligence](https://epubs.siam.org/artificial-intelligence) | SIAM 官方政策入口 | 用户提供的政策摘要指向工具披露、人类责任与计算/数据过程可评估性 | 本轮直接访问返回 HTTP 403，正文条款尚未完成一手复核；后续需通过可访问的 SIAM 官方版本核对措辞 |
| S28 | Background / Primary guidance | [Pavel Etingof, “Use of AI in mathematical research: A guide for young mathematicians”](https://math.mit.edu/~etingof/aiuse.pdf), 2026-05 | MIT 托管作者 PDF | 采用的 AI 数学内容必须由研究者完整理解、逐项检查、以自己的方式重写，并能现场解释；AI 输出至多是起点或中间步骤 | 个人研究指南，不是期刊政策或正式技术标准；内容会随技术发展更新 |

## F. Formal Methods Map and Lean Sources

| ID | Layer / type | Source | Auditable material | Practice signal | Limits |
|---|---|---|---|---|---|
| S29 | Formal methods / Institutional | [NASA NTRS: Formal Methods Case Studies for DO-333](https://ntrs.nasa.gov/citations/20140004055) | DO-333 case studies for one avionics example | Directly illustrates theorem proving, model checking and abstract interpretation as different formal-method classes, with attention to produced verification evidence | Case studies are not a complete certification effort and do not define this project's admission rules |
| S30 | Lean / Official reference | [Lean Language Reference](https://lean-lang.org/doc/reference/latest/) | Official positioning, dependent type theory, minimal kernel and tactic-produced proof terms | Supports placing Lean in dependent-type-theory interactive theorem proving for mathematics and software verification | Reference-version details change; current fixture toolchain must be checked independently |
| S31 | Lean foundations / Official documentation | [Dependent Type Theory](https://lean-lang.org/theorem_proving_in_lean4/Dependent-Type-Theory/) | Dependent type theory, inductive types and Lean's foundational language model | Supports the first layers of the Lean stack: logic/kernel and language/elaboration | Educational foundation, not a statement that Lean covers every formal-methods technique |
| S32 | Lean automation / Release record | [Lean 4.22.0 release notes](https://lean-lang.org/doc/reference/latest/releases/v4.22.0/) | Release note for the SMT-style `grind` tactic and theory-specific solvers | Supports treating automation/decision procedures as a layer around proof construction, not as a replacement for kernel checking | Historical release note; it is not evidence of this repository's installed or verifier-admitted capability |
| S33 | Mathematical formalization / Community text | [Mathematics in Lean — Introduction](https://leanprover-community.github.io/mathematics_in_lean/C01_Introduction.html) | Interactive formalization workflow and Mathlib relationship | Supports treating library engineering and interactive practice as distinct Lean layers | Tutorial scope; it does not replace the project's ProblemContract or evidence gates |
| S34 | Model checking / Classic textbook | [Baier & Katoen, Principles of Model Checking](https://mitpress.mit.edu/9780262026499/principles-of-model-checking/) | Canonical textbook entry for model-checking concepts and algorithms | Supports keeping state-space verification conceptually separate from deductive proof and SMT automation | Publisher page is a bibliographic entry; specific claims require reading the book or a primary source |

## G. Excluded or Downgraded Materials

- `vibemath.app` 等教育/动画产品：同名但不属于研究型 vibe-mathing。
- 无真实 GitHub 仓库或引用不可解析的 RL “vibe prover” 教程：不能作为可重跑实践。
- 小说、营销转载、社交平台口号：只可用于传播语义研究，不进入实践核心证据。
- 中文聚合文章的“模型独立证明”“一个提示词解决”等说法：若与原论文中人类 scaffold、审稿和修补记录冲突，以原始材料为准。

## H. Verification Status

- 本轮完成：网页正文、论文 HTML/摘要、仓库 README、公开验证记录和社区索引的交叉阅读。
- 本轮未完成：外部 Lean 仓库固定 commit 构建、全部聊天链接逐条归档、每个数学结论的领域专家独立复核，以及 SIAM AI 政策正文的一手复核。
- 因此本账本证明“来源和实践描述可追溯”，不证明所有被报道数学结论已成立。
