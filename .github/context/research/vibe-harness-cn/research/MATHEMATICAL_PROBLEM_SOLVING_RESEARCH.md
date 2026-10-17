# 数学问题求解方法论深度研究

> 状态：2026-09-04；本报告是研究证据与 55 项 crosswalk 的真相源，不是运行时效果证明。

## 结论

数学算子不应按代数、几何、分析等知识分支组织，而应按“面对未知问题时执行什么动作”组织：

```text
定义与表征
  -> 特化与实验
  -> 模式与猜想
  -> 变换与归约
  -> 构造与搜索
  -> 证明与界定
  -> 反例与压力检查
  -> 元认知控制与复盘
```

这八组是本项目对经典框架的功能性综合，不是任何单一机构发布的官方八分类。它们与库内统一
`functional_class` 是两个视图：前者描述数学求解过程，后者描述算子主要怎样改变问题空间。

本轮对用户点名的 55 个方法逐项审计后：

- `20` 项复用已有语义；
- `35` 项具有独立语义，新增到 `operators/packs/mathematics.json`；
- 新增 `1` 个 derived Method，组合发现、证明、反驳与复盘；
- 全库从 `376 source + 56 derived = 432` 更新为 `411 source + 57 derived = 468`；
- mathematics pack 从 `20 source + 1 derived` 更新为 `55 source + 2 derived`。

mathematics pack 的 `55 source` 与本报告的“55 项清单”只是数量巧合：清单中有 8 项复用其他领域算子，
而原 mathematics pack 另有本清单未点名的统计、误差和线性代数条目。

## 经典框架提供了什么

| 框架 | 可核验事实 | 本项目只借用什么 |
| --- | --- | --- |
| Pólya | 以 Understand、Plan、Carry out、Look back 组织陌生问题的生命周期 | 生命周期骨架与回看，不把具体启发式固定成唯一流程 |
| Schoenfeld | 将问题求解区分为 knowledge base、heuristics/strategies、metacognitive control 与 beliefs | 把领域知识、启发式算子、Harness 控制和证据政策分开 |
| Mason–Burton–Stacey | Open University 总结其四个数学思维要素：specialising、generalising、conjecturing、convincing | 发现循环：从例子到模式、猜想、检验和论证 |
| NCTM Process Standards | Problem Solving、Reasoning and Proof、Communication、Connections、Representations | 用作覆盖检查，不作为运行时封闭枚举 |
| MIT Mathematics for Computer Science | 系统展示反证、归纳、最小反例等证明义务和模板 | 证明类方法的程序、前提与可审计证据 |

权威入口：

- [Berkeley：Schoenfeld 问题求解框架](https://gsi.berkeley.edu/programs-services/hsl-project/hsl-speakers/schoenfeld/)
- [Open University：Thinking Mathematically](https://www.open.edu/openlearn/mod/oucontent/view.php?id=47878&printable=1)
- [NCTM：Process Standards 所在数学实践标准](https://www.nctm.org/uploadedFiles/Standards_and_Positions/Common_Core_State_Standards/Math_Standards.pdf)
- [MIT OCW：Mathematics for Computer Science](https://ocw.mit.edu/courses/6-1200j-mathematics-for-computer-science-spring-2024/)
- [MIT OCW：Probabilistic Methods in Combinatorics](https://ocw.mit.edu/courses/18-226-probabilistic-methods-in-combinatorics-fall-2022/)
- [Toronto CS：Pólya 四阶段教学摘要](https://www.teach.cs.toronto.edu/~ajr/104/diary/01/polya.html)

## 八组方法的职责

| 数学过程组 | 根本问题 | 主要产物 | 与统一功能类的关系 |
| --- | --- | --- | --- |
| 定义与表征 | 问题到底在说什么，表达是否合适？ | 定义域、量词、类型、标准形和等价表示 | 以 `representation` 为主 |
| 特化与实验 | 小规模、边界、退化和极端情况下发生什么？ | 实例表、计算记录、失败样例 | 横跨 `search` 与 `verification-falsification` |
| 模式与猜想 | 实例之间能提出什么可证伪规律？ | 模式、猜想版本、参数族 | 横跨 `representation`、`transformation`、`diagnosis-revision` |
| 变换与归约 | 能否把陌生问题变成更熟悉的问题？ | 等价链、归约、类比、辅助对象和对偶 | 以 `transformation` 为主 |
| 构造与搜索 | 如何产生候选、见证或证明路径？ | 子目标树、候选对象、分支记录 | 横跨 `construction`、`search`、`decomposition` |
| 证明与界定 | 怎样把经验支持升级为必然结论或有界结论？ | 证明链、不变量、上下界和存在性证据 | 以 `verification-falsification` 为主 |
| 反例与压力检查 | 猜想哪里会失败，假设和界是否必要？ | 反例、消融矩阵、紧性与等号分类 | 横跨 `verification-falsification` 与 `diagnosis-revision` |
| 元认知控制与复盘 | 何时继续、停止、回退、切换或总结？ | 进展指标、策略日志、证明审计和复盘 | 以 `control-metacognition` 为主 |

## 55 项逐项 crosswalk

`reuse` 表示库中已有同义且足够完整的语义；`add` 表示本轮新增。功能类只表示主作用，不否认次级作用。

| # | 用户方法 | 数学过程组 | 主功能类 | 决策 | 目标算子 ID |
| ---: | --- | --- | --- | --- | --- |
| 1 | Definition First | 定义与表征 | representation | reuse | `psoa.mathematics.definition-first` |
| 2 | Quantifier Unpacking | 定义与表征 | representation | add | `psoa.mathematics.quantifier-unpacking` |
| 3 | Change Representation | 定义与表征 | transformation | reuse | `psoa.problem-solving-methodology.representational-change` |
| 4 | Canonicalization | 定义与表征 | representation | add | `psoa.mathematics.canonicalization` |
| 5 | Dimensional / Type Check | 定义与表征 | representation | add | `psoa.mathematics.dimensional-type-check` |
| 6 | Specialization | 特化与实验 | search | add | `psoa.mathematics.specialization` |
| 7 | Small Cases | 特化与实验 | search | add | `psoa.mathematics.small-cases` |
| 8 | Boundary Cases | 特化与实验 | verification-falsification | add | `psoa.mathematics.boundary-cases` |
| 9 | Degenerate Cases | 特化与实验 | verification-falsification | add | `psoa.mathematics.degenerate-cases` |
| 10 | Extremal Cases | 特化与实验 | search | add | `psoa.mathematics.extremal-case-probe` |
| 11 | Computational Experiment | 特化与实验 | search | add | `psoa.mathematics.computational-experiment` |
| 12 | Pattern Extraction | 模式与猜想 | representation | add | `psoa.mathematics.pattern-extraction` |
| 13 | Generalization | 模式与猜想 | transformation | add | `psoa.mathematics.generalization` |
| 14 | Conjecture–Test–Revise | 模式与猜想 | diagnosis-revision | add | `psoa.mathematics.conjecture-test-revise` |
| 15 | Strengthen the Conclusion | 模式与猜想 | verification-falsification | add | `psoa.mathematics.strengthen-conclusion` |
| 16 | Weaken the Assumptions | 模式与猜想 | diagnosis-revision | add | `psoa.mathematics.weaken-assumptions` |
| 17 | Parameterization | 模式与猜想 | representation | add | `psoa.mathematics.parameterization` |
| 18 | Equivalent Reformulation | 变换与归约 | transformation | add | `psoa.mathematics.equivalent-reformulation` |
| 19 | Reduction | 变换与归约 | transformation | reuse | `psoa.computer-science.reduction` |
| 20 | Analogy | 变换与归约 | transformation | reuse | `psoa.cognitive-science.analogical-transfer` |
| 21 | Auxiliary Construction | 变换与归约 | construction | add | `psoa.mathematics.auxiliary-construction` |
| 22 | Change of Variables | 变换与归约 | transformation | add | `psoa.mathematics.change-of-variables` |
| 23 | Symmetry | 变换与归约 | transformation | reuse | `psoa.mathematics.symmetry` |
| 24 | Duality / Complement | 变换与归约 | transformation | add | `psoa.mathematics.duality-complement` |
| 25 | Relaxation | 变换与归约 | transformation | reuse | `psoa.mathematics.optimization-relaxation` |
| 26 | Work Backwards | 构造与搜索 | search | add | `psoa.mathematics.work-backwards` |
| 27 | Forward Chaining | 构造与搜索 | search | add | `psoa.mathematics.forward-chaining` |
| 28 | Subgoal Decomposition | 构造与搜索 | decomposition | reuse | `psoa.formal-logic-automated-reasoning.proof-state-subgoal-decomposition` |
| 29 | Constructive Witness | 构造与搜索 | construction | reuse | `psoa.problem-solving-methodology.constructive-witness` |
| 30 | Case Analysis | 构造与搜索 | decomposition | add | `psoa.mathematics.case-analysis` |
| 31 | Backtracking | 构造与搜索 | search | reuse | `psoa.computer-science.backtracking` |
| 32 | Direct Proof | 证明与界定 | verification-falsification | reuse | `psoa.mathematics.direct-proof` |
| 33 | Contrapositive | 证明与界定 | verification-falsification | reuse | `psoa.mathematics.contrapositive` |
| 34 | Proof by Contradiction | 证明与界定 | verification-falsification | reuse | `psoa.mathematics.proof-by-contradiction` |
| 35 | Induction | 证明与界定 | verification-falsification | reuse | `psoa.mathematics.induction` |
| 36 | Strong / Structural Induction | 证明与界定 | verification-falsification | add | `psoa.mathematics.strong-structural-induction` |
| 37 | Invariant | 证明与界定 | verification-falsification | reuse | `psoa.mathematics.invariant` |
| 38 | Monovariant | 证明与界定 | verification-falsification | reuse | `psoa.mathematics.monovariant` |
| 39 | Extremal Principle | 证明与界定 | verification-falsification | reuse | `psoa.mathematics.extremal-principle` |
| 40 | Minimal Counterexample | 证明与界定 | verification-falsification | add | `psoa.mathematics.minimal-counterexample` |
| 41 | Upper–Lower Bounds | 证明与界定 | verification-falsification | add | `psoa.mathematics.upper-lower-bounds` |
| 42 | Probabilistic Method | 证明与界定 | verification-falsification | reuse | `psoa.mathematics.probabilistic-method` |
| 43 | Counterexample Search | 反例与压力检查 | verification-falsification | reuse | `psoa.mathematics.counterexample` |
| 44 | Assumption Ablation | 反例与压力检查 | diagnosis-revision | add | `psoa.mathematics.assumption-ablation` |
| 45 | Conclusion Stress Test | 反例与压力检查 | verification-falsification | add | `psoa.mathematics.conclusion-stress-test` |
| 46 | Tightness Analysis | 反例与压力检查 | verification-falsification | add | `psoa.mathematics.tightness-analysis` |
| 47 | Equality Case Analysis | 反例与压力检查 | verification-falsification | add | `psoa.mathematics.equality-case-analysis` |
| 48 | Independent Derivation | 反例与压力检查 | verification-falsification | add | `psoa.mathematics.independent-derivation` |
| 49 | Relevance Check | 元认知控制与复盘 | control-metacognition | add | `psoa.mathematics.relevance-check` |
| 50 | Progress Measure | 元认知控制与复盘 | control-metacognition | add | `psoa.mathematics.progress-measure` |
| 51 | Strategy Switching | 元认知控制与复盘 | control-metacognition | add | `psoa.mathematics.strategy-switching` |
| 52 | Budgeted Exploration | 元认知控制与复盘 | control-metacognition | reuse | `psoa.programming.resource-bounded-loop` |
| 53 | Proof Audit | 元认知控制与复盘 | verification-falsification | add | `psoa.mathematics.proof-audit` |
| 54 | Look Back | 元认知控制与复盘 | verification-falsification | reuse | `psoa.problem-solving-methodology.look-back-evaluation` |
| 55 | Multiple-Proof Comparison | 元认知控制与复盘 | verification-falsification | add | `psoa.mathematics.multiple-proof-comparison` |

## 新增组合 Method

`psoa.mathematics.mathematical-discovery-proof-loop` 组合：

```text
Definition First
  -> Change Representation
  -> Specialization
  -> Generalization
  -> Conjecture-Test-Revise
  -> Equivalent Reformulation
  -> Auxiliary Construction
  -> Direct Proof
  -> Counterexample
  -> Look Back
```

这不是强制每次执行十步。Harness 必须按前置条件、证据缺口、信息增益和预算跳过或切换；任何原子步骤
不能衔接、关键证据缺失或连续无进展时，组合方法应返回 `inconclusive` 或停止，而不是继续生成文字。

## 证据等级与边界

- 定义展开、等价变换和证明链可以支撑逻辑结论，但仍受前提与定义域限制。
- 特化、小规模枚举、计算实验、模式提取和类比只提供发现证据，不能替代一般证明。
- 反例可以推翻全称命题，但找不到反例不能证明命题为真。
- 假设消融找不到反例，只能说明“在当前搜索范围未发现必要性”，不能自动删除安全或契约硬边界。
- 独立推导只有在依赖图真正不同的情况下才增加信心；共享错误前提不会因重复而消失。
- taxonomy 的主功能类是项目推断；调用次序、权限、成本、工具与最终结论仍由具体 Harness 和 verifier 决定。

## 暂缓进入通用算子层

傅里叶分析、生成函数、留数法、Gröbner 基、范畴论、代数几何、微分拓扑、强迫法和证明助手内核等，
先作为领域资源或执行工具看待。升级为通用算子的触发条件是：能从具体知识中剥离出稳定跨领域程序，并且
能够写出适用条件、反例、证据契约和至少两个真实消费场景。

## Claim-to-source ledger

| 主张 | 来源 | 证据性质 |
| --- | --- | --- |
| 问题求解需要区分知识、启发式、元认知控制与信念 | Berkeley Schoenfeld 页面 | 大学官方人物/教学资料，对原研究的概括 |
| specializing、generalising、conjecturing、convincing 是 Mason 等人的核心数学思维动作 | Open University 课程 | 官方大学课程对著作的明确转述 |
| Problem Solving、Reasoning and Proof、Communication、Connections、Representations 是 NCTM process standards | NCTM PDF | 专业组织发布材料 |
| 反证、归纳、最小反例等可写成不同证明义务与模板 | MIT Mathematics for Computer Science | 大学官方课程资料 |
| 概率方法通过正概率事件建立存在性 | MIT Probabilistic Methods in Combinatorics | 大学官方课程资料 |
| 本项目八组过程与每项 functional_class | 本报告综合与 taxonomy | 项目推断，不冒充外部标准 |
| 20 reuse / 35 add / 1 derived | 当前 inventory、pack 与 crosswalk | 仓库确定性审计结果 |

## 未验证项

- 尚未用真实 Agent 任务比较新增算子与基础 prompting 的效果、成本和失败率。
- 尚未建立 selector 的调用精度、跨方法冲突解决或自动组合评测。
- 数学专家独立审查尚未完成；当前证据只证明来源和静态结构可审计。
- 后续应从 representative task set 中测量选择正确率、无效调用率、证据完整度与 token/latency 成本，再决定哪些条目晋升为 `verified`。
