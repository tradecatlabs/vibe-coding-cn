# 跨领域问题求解方法证据与算子缺口矩阵

> 研究日期：2026-09-04
> 范围：前五波已落库的三十个领域，以及第六波六个领域（线性代数与谱方法、拓扑与几何、电磁场方法、量子算子方法、溶液热力学与相平衡、光谱结构解析）。
> 目的：从成熟领域抽取“专家面对未知问题时反复执行的程序”，而不是搬运领域知识。
> 边界：本文件只记录方法证据与迁移判断；不授予模型现实世界执行权限，不替代临床、生态、化学或安全专业人员。

## 结论先行

六轮研究都没有改变八类功能轴；各轮新增的是领域化前置对象、失败语义和证据契约。下表保留首轮六个来源面的总览，后续各波在独立章节追加：

| 母领域 | 反复出现的程序 | 主要补强的功能类 | 证据把握 |
| --- | --- | --- | --- |
| 因果推断 | 定义干预/结果、画因果结构、模拟目标试验、审查识别假设、做敏感性分析 | 表征、变换、验证/证伪、控制 | 高：Harvard CAUSALab/教材 |
| 经济学/博弈论 | 建战略互动模型、求最佳反应/均衡、检查承诺可信性、设计激励、分析信号与筛选 | 表征、搜索、构造、验证/证伪、控制 | 高：MIT/Stanford 课程材料 |
| 生态/生物学 | 分离生态过程与观测过程、做层级建模、扰动对照、分析资源权衡、检查网络韧性 | 表征、验证/证伪、控制 | 中高：USGS/National Academies |
| 认知科学 | 识别工作记忆负荷、分块、改写表征、迁移类比、在线监控策略 | 表征、构造、控制/元认知 | 中高：NASEM/同行评议综述 |
| 人因与可靠性 | 检查情境态势、跟踪程序状态、限制多任务、预设容差、设计检测与恢复 | 验证/证伪、诊断/修正、控制 | 高：NASA 官方手册/清单 |
| 医学决策 | 结构化临床问题、分级证据确定性、比较收益/伤害、纳入价值偏好、审查可行性/公平性 | 表征、验证/证伪、控制 | 高：WHO 指南/EtD |

## 证据与迁移明细

### 1. 因果推断

| 证据事实 | 可迁移的算子 | 信心与缺口 |
| --- | --- | --- |
| Hernán 与 Robins 将观察性分析视为对一个明确“目标试验”的模拟，要求先写清资格、干预、分配、结局、随访和因果对比；并强调 exchangeability、positivity、consistency 等识别条件。[Harvard《Causal Inference: What If》](https://www.hsph.harvard.edu/miguel-hernan/wp-content/uploads/sites/1268/2024/04/hernanrobins_WhatIf_26apr24.pdf) | `causal-question-specification`、`target-trial-emulation` | 高；不能把“观察到相关”直接迁移成因果结论。 |
| Harvard CAUSALab 课程与研究材料把 DAG、混杂调整、负对照、目标试验和敏感性分析作为互相配合的研究设计，而不是事后套模型。[CAUSALab](https://hsph.harvard.edu/research/causalab/2025courses/) | `causal-dag-confounding`、`identification-assumption-audit` | 高；DAG 依赖领域知识，自动生成只能作为待审草图。 |
| What If 明确建议对不可检验假设做敏感性分析，并对未测混杂、选择偏差和模型错设分别说明替代假设。[What If 第 7 章](https://www.hsph.harvard.edu/miguel-hernan/wp-content/uploads/sites/1268/2024/01/hernanrobins_WhatIf_2jan24.pdf) | `sensitivity-to-unmeasured-confounding` | 高；敏感性范围本身需要有依据，不能用任意区间制造确定感。 |

**缺口判定**：现有库已有统计估计、贝叶斯更新和机器学习的因果特征消融，但没有把“干预定义—识别假设—目标试验—敏感性”串成一条因果专用链，因此新增一个因果 pack 是非重复补充。

### 2. 经济学 / 博弈论

| 证据事实 | 可迁移的算子 | 信心与缺口 |
| --- | --- | --- |
| MIT 课程将战略互动表示为玩家、策略和收益，并用最佳反应的固定点解释 Nash equilibrium：在他人策略给定时，任何一方都没有改变策略的动机。[MIT Networks Recitation 7](https://ocw.mit.edu/courses/14-15j-networks-spring-2018/pages/lecture-and-recitation-notes/recitation-7-notes/) | `strategic-interaction-model`、`best-response-equilibrium` | 高；均衡是模型内稳定性，不是现实预测的保证。 |
| MIT Game Theory for Managers 反复覆盖 sequential games、commitment、strategic substitutes/complements、auctions、uncertainty、signaling/screening、agency/moral hazard 和 reputation。[MIT 课程讲义目录](https://ocw.mit.edu/courses/15-040-game-theory-for-managers-spring-2004/pages/lecture-notes/) | `credible-commitment`、`signaling-screening` | 高；这些概念适合分析交互约束，不应把参与者默认成完全理性。 |
| MIT 机制设计讲义明确把 revelation principle、激励相容、individual rationality 和 optimal mechanisms作为“逆向设计”问题。[MIT Mechanism Design Lecture 19](https://ocw.mit.edu/courses/6-254-game-theory-with-engineering-applications-spring-2010/ce4daf120dcb728fc1fb128f6cd3b48f_MIT6_254S10_lec19.pdf) | `mechanism-incentive-alignment` | 高；激励相容需要明确私有信息、效用和可执行规则。 |

**缺口判定**：现有决策科学 pack 有期望效用与机会成本，但没有“他人会如何响应”和“规则如何改变激励”的算子；新增 pack 负责战略环境，不重复单主体决策。

### 3. 生态 / 生物学

| 证据事实 | 可迁移的算子 | 信心与缺口 |
| --- | --- | --- |
| USGS 强调生态数据同时包含真实种群变化和由抽样、观察者、空间覆盖、不完全检测造成的观测变化；层级模型把生态过程与观测过程分开建模。[USGS Hierarchical Modeling](https://www.usgs.gov/node/43499) | `hierarchical-observation-model` | 高；这是“别把测量误差当系统变化”的通用方法。 |
| USGS 的层级生态建模框架覆盖 occupancy、abundance、capture-recapture、population/metapopulation/community dynamics，并用链接子模型组织复杂似然。[USGS Hierarchical Modeling and Inference in Ecology](https://pubs.usgs.gov/publication/5200344) | `ecological-state-observation-separation`（在 pack 中以层级模型表达） | 中高；具体生态模型不能脱离数据生成过程和采样设计。 |
| National Academies 的进化教育材料强调生物演化具有概率性、历史偶然性，且性状之间常是成本—收益权衡，不应假设自然系统总是“最优”。[Thinking Evolutionarily](https://www.ncbi.nlm.nih.gov/books/NBK201233/) | `life-history-tradeoff` | 中高；迁移到 Agent 只能表达资源分配与权衡类比，不能把适应性叙事当因果证明。 |
| USGS 关于生态层级与自组织的材料把个体交互、群体、群落和尺度转换连起来，提示要检查跨尺度反馈与恢复。[Ecological hierarchies and self-organisation](https://www.usgs.gov/publications/ecological-hierarchies-and-self-organisation-pattern-analysis-modelling-and-process) | `ecological-network-resilience`、`perturbation-and-control` | 中；网络稳定性需要长期数据和扰动定义，本轮只沉淀静态方法。 |

**缺口判定**：现有系统科学/复杂性科学已有一般网络、反馈与韧性，但缺少“观测过程与真实过程分离”和“生物资源权衡”的具体方法；生态 pack 作为领域化实例保留。

### 4. 认知科学

| 证据事实 | 可迁移的算子 | 信心与缺口 |
| --- | --- | --- |
| 认知负荷研究把工作记忆容量和任务复杂度视为问题求解的限制条件；高复杂度可能诱发无效搜索，需要通过结构化和分块降低负荷。[Cognitive Load and Self-regulation 综述](https://pmc.ncbi.nlm.nih.gov/articles/PMC12204937/) | `cognitive-load-budget`、`working-memory-chunking` | 中高；研究多来自学习情境，迁移到 Agent 是工程类比而非效果证明。 |
| RAMPS/元推理研究把 metacognition 定义为对推理和问题求解的监控与控制，并强调工作记忆资源有限、需要抑制无关信息。[RAMPS Framework](https://pmc.ncbi.nlm.nih.gov/articles/PMC10302445/) | `metacognitive-monitoring`、`representational-recoding` | 中高；需要在 Agent 任务上单独做留出评估。 |
| 认知科学中类比迁移、重编码和策略监控共同说明：高手不是只拥有更多内容，还会改变表示、选择策略并检查当前策略是否仍有效。[National Academies Metacognition](https://www.nationalacademies.org/read/10024/chapter/3) | `analogical-transfer` | 中高；类比必须输出结构对应和不对应，防止表面相似误导。 |

**缺口判定**：现有通用问题求解 pack 有表征变换和元认知监控，但没有工作记忆负荷、分块和类比结构映射的专门契约；新增 pack 只承载认知控制视角，不做人格/智力分类。

### 5. 人因与可靠性

| 证据事实 | 可迁移的算子 | 信心与缺口 |
| --- | --- | --- |
| NASA Human Factors Checklist 建议做情境态势检查、限制多任务、提供测量目标与容差、减少心算，并把风险设计掉。[NASA Human Factors Checklist](https://ntrs.nasa.gov/api/citations/20160006485/downloads/20160006485.pdf?attachment=true) | `situation-awareness-check`、`workload-and-multitask-bounding` | 高；适合变成 Harness 的检查点，不等同于安全认证。 |
| 同一清单把损坏/错误的预防、检测和恢复作为完整链条，而不是只在事后找责任。[NASA Human Factors Checklist](https://ntrs.nasa.gov/api/citations/20160006485/downloads/20160006485.pdf?attachment=true) | `error-tolerant-recovery` | 高；恢复动作仍须由具体安全策略授权。 |
| NASA 飞行认知研究把 checklist 使用与记忆、态势感知、诊断、决策和工作负荷联系起来，并强调高压/时间关键场景的程序支持。[NASA Flight Cognition](https://humanfactors.arc.nasa.gov/flightcognition/Publications/NASA_TM_2014_218382.pdf) | `checklist-procedure-state`、`independent-cross-check` | 高；来源是航空场景，迁移到 Agent 需要保留“程序状态可见、独立交叉检查”的抽象。 |

**缺口判定**：现有工程 pack 有约束、压力测试、安全裕度，但没有把“情境感知—程序状态—负荷边界—错误恢复”组织为操作链；新增人因 pack 负责运行控制和可靠性护栏。

### 6. 医学决策

| 证据事实 | 可迁移的算子 | 信心与缺口 |
| --- | --- | --- |
| WHO 将 evidence-informed decision-making 定义为识别、评价并调动最佳可用证据，用于安全有效的健康政策与实践。[WHO EIDM Guide](https://www.who.int/publications/i/item/9789240039872) | `clinical-question-structuring`、`evidence-to-decision` | 高；只作为证据组织方法，不输出诊断或治疗。 |
| WHO Evidence-to-Decision 框架要求明确比较干预的利弊、关键决策标准、研究证据、分歧原因，并让决策依据透明。[WHO EtD Tables](https://www.who.int/publications-detail-redirect/9789240011908) | `benefits-harms-values-tradeoff` | 高；适合给 Agent 生成决策表，不允许自动代替临床人员。 |
| WHO 指南方法把证据确定性、收益/伤害、价值偏好、资源、可接受性、可行性、公平性等因素分开判断，并区分强推荐与条件推荐。[WHO Guideline Development](https://www.emro.who.int/images/stories/evidence-data/Generating-evidence-for-a-guideline-recommendation-systematic-reviews-of-evidence-economic-evaluation-and-critical-appraisal.pdf) | `evidence-certainty-grading`、`context-and-feasibility-adaptation` | 高；确定性等级和推荐强度不能被模型自报置信度替代。 |

**缺口判定**：现有决策科学能算效用与信息价值，但缺少医疗场景中“证据确定性—收益/伤害—价值—资源—公平/可行性”的结构化决策契约；新增 pack 严格标记 `reference_only` 与高风险。

## 第二轮六个领域：证据与迁移明细

第二轮选择历史推理、社会科学、教育学习、语言学、法律推理和伦理公共政策，是因为它们分别补上了
“来源如何解释”“群体如何取样”“能力如何形成”“语言证据如何隔离”“规则如何适用”和“影响如何负责”
六类现有库没有专门表达的程序。每个领域固定抓取五个 source entry，再组合一个 derived Method。

### 7. 法律推理

| 证据事实 | 可迁移的算子 | 信心与缺口 |
| --- | --- | --- |
| 法院意见把法律工作拆成识别争点、选择适用规则、解释规则、把规则应用到事实，并用实质事实相似性而非关键词做类比/区分。[Third Circuit Opinion](https://www2.ca3.uscourts.gov/opinarch/014535.pdf) | issue-spotting、authority-hierarchy、precedent-analogy-distinction | 高；仅沉淀研究程序，不提供个案法律意见。 |
| Federal Rule 401 用“提高或降低重要事实可能性”的倾向定义相关性；Rule 702 要求充分事实/数据、可靠方法和可靠适用。[Rule 401](https://www.law.cornell.edu/rules/fre/rule_401)、[Rule 702](https://www.law.cornell.edu/uscode/text/28a/courtrules-Evid/article-VII/courtrule-702) | burden-standard-of-proof、application-and-counterargument-audit | 高；证明标准、法域和程序阶段必须由专业人员核验。 |

**缺口判定**：既有统计、因果和决策条目会审查证据，却不表达法域/权威层级、先例实质类比和规则—事实适用，故新增 legal-reasoning。

### 8. 伦理与公共政策

| 证据事实 | 可迁移的算子 | 信心与缺口 |
| --- | --- | --- |
| UNESCO 原则要求比例与不伤害、安全、隐私、公平、透明、问责、人类监督和影响评估；OECD 进一步强调人权、公平、稳健安全和责任。[UNESCO AI Ethics](https://www.unesco.org/en/artificial-intelligence/recommendation-ethics?hub=66778)、[OECD AI Principles](https://www.oecd.org/en/topics/sub-issues/ai-principles.html) | stakeholder-impact-mapping、proportionality-and-do-no-harm | 高；价值冲突不能由模型自行裁决。 |
| NIST AI RMF 以 Govern、Map、Measure、Manage 组织风险治理；Belmont Report 用尊重人、善行/风险收益、公正约束研究决策。[NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework)、[Belmont Report](https://www.hhs.gov/ohrp/regulations-and-policy/belmont-report/read-the-belmont-report/index.html) | ethical-impact-assessment、human-oversight-accountability、rights-and-fairness-screen | 高；影响评估是治理证据，不等同法律合规或安全认证。 |

**缺口判定**：人因、工程和决策条目已有风险/权衡，但没有权利、群体公平、责任、申诉和人类接管的专门链，故新增 ethics-public-policy。

### 9. 教育与学习科学

| 证据事实 | 可迁移的算子 | 信心与缺口 |
| --- | --- | --- |
| How People Learn II 强调先备知识、迁移、情境、动机和文化；IES 指南总结间隔、交错、示例、主动提取、反馈和自我判断。[NASEM How People Learn II](https://nap.nationalacademies.org/resource/24783/How%20People%20Learn%202.pdf)、[IES WWC](https://ies.ed.gov/ncee/wwc/PracticeGuide/1) | learning-objective-operationalization、prior-knowledge-misconception-check、retrieval-and-application-practice | 高；学习效果仍需在目标任务上做留出评估。 |
| EEF 将反馈定义为对齐目标和差距的下一步行动，并建议显式教、示范、支架、监控、评价后逐步淡出。[EEF Feedback](https://educationendowmentfoundation.org.uk/education-evidence/guidance-reports/feedback/)、[EEF Metacognition](https://educationendowmentfoundation.org.uk/education-evidence/guidance-reports/metacognition) | scaffold-and-fade、formative-assessment-feedback | 中高；不能把完成课程或熟悉感当作迁移证据。 |

**缺口判定**：认知科学已有负荷和元认知，但缺少目标—起点诊断—练习—支架—反馈—迁移的学习设计闭环，故新增 education-learning-science。

### 10. 语言学

| 证据事实 | 可迁移的算子 | 信心与缺口 |
| --- | --- | --- |
| BLiMP 用大量最小成对刺激隔离句法、形态和语义现象，并与人类一致性对照。[BLiMP](https://aclanthology.org/2020.tacl-1.25/) | minimal-contrast-test | 高；最小对比不自动覆盖方言、语域和真实语用。 |
| TEI 语料指南强调代表性、上下文和标注方法；UD 规定词元化、形态、句法和结构化 CoNLL-U 表示。[TEI Language Corpora](https://tei-c.org/release/doc/tei-p5-doc/en/html/CC.html)、[UD Guidelines](https://universaldependencies.org/guidelines.html)、[UD Format](https://universaldependencies.org/format.html) | corpus-evidence-sampling、syntax-semantics-pragmatics-separation | 高；标注协议和样本边界必须随结论公开。 |
| 篇章研究把表达放入对话、篇章关系和语境，要求保留跨句证据。[ACL Discourse Proceedings](https://www.aclweb.org/anthology/P15-3.pdf) | discourse-context-analysis、ambiguity-resolution | 中高；模型偏好不能代替人类语言判断。 |

**缺口判定**：现有表征/验证算子与语言无关，缺少最小对比、语料代表性、句法—语义—语用分层和残余歧义语义，故新增 linguistics。

### 11. 历史推理

| 证据事实 | 可迁移的算子 | 信心与缺口 |
| --- | --- | --- |
| AHA 历史思维技能要求分析作者、目的、受众、媒介、上下文、可靠性与限制，并进行比较、因果、连续/变化、分期和论证。[AHA Historical Thinking Skills](https://www.historians.org/wp-content/uploads/2024/05/AP-Histories-Historical-Thinking-Skills.pdf) | source-provenance-criticism、contextualization-periodization、historiographical-perspective | 高；历史解释不是把档案数量相加。 |
| AHA 要求主张以可核验证据支撑并容纳多重解释；国家档案馆提示作者观点、矛盾、可靠性和缺失需要被显式检查。[AHA Criteria](https://www.historians.org/resource/criteria-for-standards-in-history-social-studies-social-sciences/)、[National Archives History in the Raw](https://www.archives.gov/education/research/history-in-the-raw.html) | corroboration-and-triangulation、historical-counterfactual-boundary | 高；反事实只能检验必要性/偶然性，不能冒充真实历史。 |

**缺口判定**：科研来源批判和因果推断已有一般证据链，但没有时间语境、分期、史学视角和受同期约束的反事实，故新增 historical-reasoning。

### 12. 社会科学方法

| 证据事实 | 可迁移的算子 | 信心与缺口 |
| --- | --- | --- |
| CDC 2024 评估框架要求理解情境、描述项目、聚焦问题、收集可信证据、支持结论并行动，同时强调严谨、独立、透明和伦理。[CDC Program Evaluation Framework](https://www.cdc.gov/mmwr/volumes/73/rr/rr7306a1.htm) | research-question-operationalization、sampling-and-representation-audit | 高；抽样和指标必须绑定目标总体与决策用途。 |
| CDC 证据指南要求问题、指标、来源、样本和质量对齐；国家科学院强调互补来源的三角互证；UKRI/ESRC 将访谈、观察、案例和叙事用于理解意义与情境。[CDC Gather Credible Evidence](https://www.cdc.gov/evaluation/php/evaluation-framework-action-guide/step-4-gather-credible-evidence.html)、[NASEM Mixed Methods](https://nap.nationalacademies.org/skim.php?chap=69-78&record_id=18739)、[UKRI Qualitative Research](https://www.ukri.org/who-we-are/esrc/what-is-social-science/qualitative-research/) | qualitative-coding-comparison、mixed-methods-triangulation、stakeholder-institutional-context | 高；三角互证不是多数票，制度情境和权力差异仍需解释。 |

**缺口判定**：统计、因果和研究 pack 已覆盖估计/因果/实验，却没有社会构念操作化、质性编码、混合方法综合和制度执行边界，故新增 social-science-methods。

## 第三波六个领域：证据与迁移明细

第三波优先选择能给 Agent 增加“形式可核验、解释克制、空间时间外推、观测模型、材料计量、证据检索”能力的领域。每个领域新增 5 个 source 和 1 个 derived Method；所有条目仍是 `experimental` / `reference_only`。

### 13. 形式逻辑与自动推理

| 证据事实 | 可迁移的算子 | 信心与缺口 |
| --- | --- | --- |
| Lean 以小型可信内核检查 proof term，tactic 只是生成证明项；证明状态由目标和局部假设组成，所有子目标完成后才算证明完成。[Lean Language Reference](https://lean-lang.org/doc/reference/latest/)、[Tactic Proofs](https://lean-lang.org/doc/reference/latest/Tactic-Proofs/) | formal-problem-specification、syntax-semantics-separation、proof-state-subgoal-decomposition、kernel-checked-proof-evidence | 高；迁移只保留“可检查见证”思想，不声称 Agent 自动产生形式证明。 |
| 经典逻辑区分语法、模型语义、可满足性、有效性与逻辑后承；复杂度研究把 SAT、有效性和模型检查作为不同判定/搜索问题。[SEP Classical Logic](https://plato.stanford.edu/entries/logic-classical/)、[SEP Computational Complexity](https://plato.stanford.edu/entries/computational-complexity/) | satisfiability-countermodel-search、formal-reasoning-loop | 高；有限搜索耗尽不能自动推出一般不可满足，需声明模型域和资源边界。 |

**缺口判定**：既有形式化方法与数学证明条目提供原则，但没有专门表达“语法—语义—反模型—子目标—内核证据”链，新增 `formal-logic-automated-reasoning`。

### 14. 科学哲学与认识论

| 证据事实 | 可迁移的算子 | 信心与缺口 |
| --- | --- | --- |
| 科学方法讨论观察、实验、模型、归纳/演绎和假设检验，并强调科学实践具有情境与方法多样性。[SEP Scientific Method](https://plato.stanford.edu/entries/scientific-method/) | observation-interpretation-separation、discriminating-evidence-design | 中高；SEP 是专业综述，项目迁移不是其原文的执行授权。 |
| 最佳解释推断比较解释力、简单性、一致性和范围；理论欠定性说明同一证据可能支持多个候选，失败还可能来自辅助假设。[SEP Scientific Realism](https://plato.stanford.edu/entries/scientific-realism/)、[SEP Theory and Observation](https://plato.stanford.edu/entries/science-theory-observation/)、[SEP Underdetermination](https://plato.stanford.edu/entries/scientific-underdetermination/index.html) | inference-to-best-explanation、auxiliary-assumption-audit、underdetermination-branching、epistemic-inquiry-loop | 高；“最佳”是相对比较，不是事实真值；需保留替代解释和区分性证据。 |

**缺口判定**：科研方法 pack 已有假设、证伪和重复，但没有专门审计观察/解释、辅助假设和欠定性，新增 `philosophy-science-epistemology`。

### 15. 地球科学与地质推理

| 证据事实 | 可迁移的算子 | 信心与缺口 |
| --- | --- | --- |
| USGS 地质图标准要求区分可观察、推断、遮蔽、位置误差和存在置信度，并把不确定性作为数据属性。[USGS Geologic Feature Accuracy](https://pubs.usgs.gov/of/2002/of02-370/soller1.html) | field-observation-uncertainty、geologic-map-cross-section | 高；地图精度与解释精度不是同一件事。 |
| 叠覆和切割关系建立相对时间；地层规范强调可观察特征与解释分离、相关关系和不确定年龄。[USGS Relative Time](https://pubs.usgs.gov/gip/geotime/relative.html)、[North American Stratigraphic Code](https://ngmdb.usgs.gov/Info/NACSN/Code2/code2.html) | stratigraphic-temporal-ordering | 高；相对排序不等于精确日期，变形区域要标注不适用规则。 |
| USGS 要求遥感解释做地面检查；储层物质平衡用边界、压力、体积和利用率做范围估计。[Remote Sensing Verification](https://www.usgs.gov/publications/verification-remotely-sensed-data)、[Material Balance](https://pubs.usgs.gov/publication/sir20255108/full) | remote-sensing-ground-truth、mass-balance-reservoir-accounting、geoscience-inference-loop | 中高；地面时差、空间稀疏和边界假设会限制外推。 |

**缺口判定**：既有物理、生态和系统科学条目没有表达地质空间/时间关系与稀疏观测外推，新增 `earth-science-geoscience`。

### 16. 天文学与天体物理

| 证据事实 | 可迁移的算子 | 信心与缺口 |
| --- | --- | --- |
| NASA 区分“检测到源”与“估计源参数”；后者核心是参数不确定度而非单纯信噪比。[NASA Detection versus Observation](https://ntrs.nasa.gov/api/citations/20080031653/downloads/20080031653.pdf) | signal-background-discrimination | 高；阈值越过只支持检测候选，不支持完整物理解释。 |
| Gaia 用观测模型、源参数和 nuisance 参数做加权拟合，并显式处理模型误差；HEASARC 要求按 Gaussian/Poisson 等数据分布做参数估计和拟合优度检查。[Gaia Calibration Models](https://gea.esac.esa.int/archive/documentation/GDR1/Data_processing/chap_cu3ast/sec_cu3ast_cali.html)、[XSPEC Statistics](https://heasarc.gsfc.nasa.gov/docs/software/xspec/manual/node340.html) | observation-model-separation、lightcurve-or-spectrum-model-fit、dimensional-scale-check | 高；拟合通过不能证明模型唯一正确，背景/校准误差必须保留。 |
| 天文分析指南提供背景扣除、信噪阈值、仪器校准和跨观测复核程序。[HEASARC Background](https://heasarc.gsfc.nasa.gov/docs/asca/background.html)、[NIST/HEASARC Detection](https://heasarc.gsfc.nasa.gov/docs/software/lheasoft/help/batcelldetect.html) | independent-observation-confirmation、astrophysical-inference-loop | 中高；不同观测若共享系统误差，不能当完全独立确认。 |

**缺口判定**：物理 pack 有一般残差/不确定度，但没有天文特有的背景、检测—观测分层和观测模型，新增 `astronomy-astrophysics`。

### 17. 材料科学与工程测量

| 证据事实 | 可迁移的算子 | 信心与缺口 |
| --- | --- | --- |
| NIST 材料科学以加工—结构—性能关系为核心，并结合测量、模型、数据和标准；结构计量强调过程中的原位演化、校准和资格确认。[NIST MSED](https://www.nist.gov/mml/materials-science-and-engineering-division)、[Structural Metrology](https://www.nist.gov/programs-projects/structural-metrology-advanced-manufacturing-processes) | processing-structure-property-map、microstructure-characterization、qualification-and-calibration | 高；过程—结构链是机制线索，不自动等同因果证明。 |
| NIST 材料测量实验室提供参考测量程序、标准物质和评估数据；数据评价区分可靠性、完整性、一致性、可重复性和可预测性。[NIST MML](https://www.nist.gov/mml/about-mml)、[Data Evaluation](https://www.nist.gov/publications/data-evaluation-theory-and-practice-materials-properties) | materials-metrology-traceability、data-quality-evaluation | 高；不同 measurand、样品状态和校准链的数据不能直接比较。 |
| NIST 微结构—性能工具把跨尺度模型、代理模型和主动学习用于结构—性能设计。[NIST Microstructure-Property Tools](https://www.nist.gov/programs-projects/microstructure-property-tools-structure-property-design) | materials-design-loop | 中高；代理模型和主动学习仍需独立验证与用途限定。 |

**缺口判定**：化学和工程 pack 已有守恒、约束和安全，但没有材料专属的加工—结构—性能、计量追溯和数据评价链，新增 `materials-science`。

### 18. 信息与知识组织科学

| 证据事实 | 可迁移的算子 | 信心与缺口 |
| --- | --- | --- |
| NIST TREC 以共享语料、查询、相关性判断、训练/评估分离和提交比较支撑大规模信息检索评价；RAG track 使用 recall、precision 和排序指标。[TREC Overview](https://trec.nist.gov/about.html)、[How To TREC](https://trec.nist.gov/howto.html)、[TREC RAG 2025](https://trec.nist.gov/pubs/trec34/papers/Overview_rag.pdf) | information-need-formulation、retrieval-query-expansion、relevance-precision-recall-audit | 高；指标反映预设判断集，不自动覆盖真实用户价值。 |
| W3C DCAT 用目录、持久标识、版本、许可、关联和血缘组织数据/服务；NIST FAIR 要求可发现、可访问、可互操作和可复用。[W3C DCAT 3](https://www.w3.org/TR/vocab-dcat-3/)、[NIST FAIR](https://www.nist.gov/itl/ssd/information-systems-group/configurable-data-curation-system-cdcs/cdcs-help-and-resources-1) | source-authority-and-provenance、metadata-and-fairness-check | 高；FAIR 是指导原则，不是自动合规认证。 |
| FAIR/知识组织原则强调唯一标识、丰富元数据、许可、责任和派生链，便于机器发现与复用。[NIH Data Management](https://www.grants.nih.gov/policy-and-compliance/policy-topics/sharing-policies/dms/data-management) | evidence-retrieval-loop | 中高；访问权限、语言偏差和元数据缺口仍需按具体群体审查。 |

**缺口判定**：既有 research/W3C PROV 只覆盖一般来源与血缘，没有把信息需求、检索评估和 FAIR 复用串为一条检索程序，新增 `information-knowledge-science`。

## 第四波六个领域：证据与迁移明细

第四波不是重复扩充已有母领域，而是补三个高价值空洞：Harness 缺少明确的反馈控制，数学/科学计算缺少误差与收敛审计，数学/物理/化学的专门方法还没有形成可调用链。每个领域抓取至少两类一手或权威来源，抽取 5 个 source 和 1 个 derived Method；新条目仍是 `experimental`、`reference_only`。

| 母领域 | 证据事实 | 可迁移算子 | 反向核验与边界 |
| --- | --- | --- | --- |
| 控制论与反馈系统 | MIT 状态空间材料把状态、输入、输出、可控性和可观测性作为统一模型，并给出秩条件；反馈课程说明利用当前/过去观测产生控制信号，开环误差不会自行修正。[MIT State Space](https://ocw.mit.edu/courses/16-30-feedback-control-systems-fall-2010/a2e9eccea56da4ba879a5a3e15cf8cde_MIT16_30F10_lec09.pdf)、[MIT Feedback/Observers](https://ocw.mit.edu/courses/6-011-introduction-to-communication-control-and-signal-processing-spring-2010/205766623e6e6edc42f9b6d129f18d30_MIT6_011S10_chap06.pdf) | 状态空间建模、可控/可观测审计、反馈误差修正、稳定裕度、滚动时域重规划 | 反馈能改善可观测闭环，不等同真实系统稳定保证；动作权限、延迟、饱和和独立验证必须由 Harness policy 接管。 |
| 数值分析与科学计算 | NIST 区分问题条件性与算法稳定性；SciPy 文档要求用绝对/相对误差估计控制自适应细分，并提醒异常区间会欺骗自适应程序；LAPACK提供条件估计和迭代精化。[NIST Numerical Stability](https://nvlpubs.nist.gov/nistpubs/Legacy/IR/nistir4763.pdf)、[SciPy Cubature](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.cubature.html)、[LAPACK Condition/Refinement](https://www.netlib.org/lapack/explore-html/d4/d1e/group__gesv__comp__grp.html) | 条件性/稳定性区分、离散化收敛、自适应误差、残差/后向误差、可复现实验 | 残差小不保证前向误差小；单点运行不证明收敛；数值方法包只产生审计证据，不替代领域模型确认。 |
| 离散组合数学 | MIT 离散数学系统覆盖双射、抽屉、容斥、递推和生成函数；概率组合课程补充随机方法、局部引理和随机图；Stanford课程覆盖图、匹配和枚举。[MIT Counting](https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-fall-2010/93cad640cf3ed0b23ef70688f452d4d5_MIT6_042JF10_notes.pdf)、[MIT Probabilistic Combinatorics](https://math.mit.edu/~shor/18.447/)、[Stanford Combinatorics](https://theory.stanford.edu/~jvondrak/MATH108-2016/MATH108.html) | 双射表示、碰撞搜索、容斥重叠、递推/生成函数、极值图界 | 有限搜索未找到不代表不存在；计数、剪枝和极值界必须公开对象域、边界和见证。 |
| 热力学与统计物理 | MIT课程用状态变量、熵、系综、自由能、平衡与变分方法连接宏观约束和微观概率；NIST提供常数、单位和不确定度表达。[MIT Statistical Mechanics](https://live.ocw.mit.edu/courses/8-333-statistical-mechanics-i-statistical-mechanics-of-particles-fall-2013/pages/lecture-notes/)、[MIT Thermodynamics](https://ocw.mit.edu/courses/res-8-010-introduction-to-statistical-physics-summer-2018/mitres_8_010su18_lec4.pdf)、[NIST CODATA](https://www.physics.nist.gov/cgi-bin/cuu/Info/index.html) | 系统边界/状态变量、熵与微观态、自由能界、平衡扰动、系综采样诊断 | 热力学可行不等于动力学必然；统计趋势不等于单次预测；非平衡、模型误差和抽样混合需显式标注。 |
| 有机化学反应设计 | IUPAC Gold Book 区分化学、区域、立体选择性与保护基术语；ACS机理资料强调电子流和反应步骤；Organic Syntheses以程序复现审查为边界。[IUPAC Chemoselectivity](https://goldbook.iupac.org/terms/view/C01051)、[IUPAC Regioselectivity](https://goldbook.iupac.org/terms/view/R05243)、[IUPAC Stereoselectivity](https://goldbook.iupac.org/terms/view/S05991)、[ACS Mechanisms](https://now.acs.org/public/detail/Documents/organic_reaction_mechanisms_a_practical_guide.pdf)、[Organic Syntheses](https://www.orgsyn.org/instructions.aspx) | 化学/区域/立体选择性筛查、保护基代价、机理箭推 | 只读路线推理，不授权合成、采购、放大或危险实验；底物差异、条件窗口和安全审查必须由资质人员确认。 |
| 分析化学与计量学 | NIST校准指南把信号与被测量的模型关系作为基础；IUPAC定义计量质量和检出限；IUPAC/EURACHEM要求方法验证与用途适配、不确定度预算。[NIST Calibration](https://www.nist.gov/publications/guidelines-calibration-analytical-chemistry-part-i-fundatmentals-and-single-component)、[IUPAC Metrology](https://iupac.org/recommendation/metrological-and-quality-concepts-in-analytical-chemistry/)、[IUPAC Method Validation](https://publications.iupac.org/pac/74/5/0835/index.html)、[EURACHEM Fitness](https://www.eurachem.org/images/stories/Guides/pdf/valid.pdf) | 校准模型、空白/检出限、基质干扰、用途验证、不确定度预算 | 检出限不等于可靠定量；相关系数不等于方法充分性；结果必须绑定量程、基质、校准链和报告不确定度。 |

**第四波缺口判定**：已有系统科学、数学、物理、化学和统计条目提供零散原则，但没有控制反馈、数值误差、组合计数、热力学势、选择性或分析计量的领域化程序；六个新 pack 是功能补齐，不改变八类功能轴，也不创建运行时 selector/planner。

## 第五波六个领域：动态科学方法与迁移明细

第五波继续按“领域知识与领域方法分开”的原则，补足前四波仍未拆开的六条程序链：随机状态下的界限与停止、连续动力系统的适定性与分岔、变分模型的结构保持、连续介质的尺度/边界、化学速率机理和电化学信号归因。每个领域只新增 5 个 source 与 1 个 derived Method；所有条目仍是 `experimental`、`reference_only`，不把公式或资料变成现实操作权限。

| 母领域 | 来源事实 | 可迁移算子 | 与既有库的缺口/交叉 | 反向核验与边界 |
| --- | --- | --- | --- | --- |
| 随机过程与概率过程 | MIT 随机过程课程系统覆盖 Markov 链、filtration/martingale、stopping time、收敛和集中不等式；离散过程课程补充随机游走、动态规划和停止过程。[MIT Advanced Stochastic Processes](https://ocw.mit.edu/courses/15-070j-advanced-stochastic-processes-fall-2013/pages/lecture-notes/)、[MIT Discrete Stochastic Processes](https://ocw.mit.edu/courses/6-262-discrete-stochastic-processes-spring-2011/video_galleries/video-lectures/) | 状态转移、鞅不变量、停止时刻边界、集中界、耦合敏感性 | 与 `statistics` 的估计/Bootstrap、`decision-science` 的价值信息相交，但新增“随机过程状态—停止合法性—共同扰动比较”的时间结构 | 概率界不是单次保证；停止规则不能偷看未来；依赖结构、预算和信息集必须显式记录。 |
| 微分方程与动力系统 | MIT 数值分析明确把 IVP 的存在性、唯一性、爆破和数值求解放在一起；非线性动力学课程覆盖相图、稳定性、分岔和 Lyapunov 指标。[MIT ODE Methods](https://ocw.mit.edu/courses/18-330-introduction-to-numerical-analysis-spring-2012/a9d2bd9be098f0ada172af40379a17cc_MIT18_330S12_Chapter5.pdf)、[MIT Nonlinear Dynamics](https://ocw.mit.edu/courses/12-006j-nonlinear-dynamics-chaos-fall-2022/resources/lecture-notes/) | 初值问题适定性、相空间定性分析、Lyapunov 稳定证书、分岔扫描、敏感性/鲁棒性 | 与 `physics` 的初值/边界/稳定性、`control-theory-cybernetics` 的稳定裕度相交，但新增连续系统的解存在性和参数导致的定性改变 | 局部稳定不等于全局稳定；单条仿真轨迹不覆盖相空间；分岔扫描受分辨率和模型域限制。 |
| 经典力学与变分方法 | MIT 经典力学把 Lagrangian/Hamiltonian、对称守恒、约束、变分和扰动作为统一结构；计算课程强调用计算表达作用量、相空间和守恒量。[MIT Classical Mechanics III](https://ocw.mit.edu/courses/8-09-classical-mechanics-iii-fall-2014/pages/lecture-notes/)、[MIT Classical Mechanics: A Computational Approach](https://ocw.mit.edu/courses/12-620j-classical-mechanics-a-computational-approach-fall-2008/) | 变分原理建模、Euler-Lagrange 推导、对称守恒审计、Hamilton 状态空间、扰动/相位稳定 | 与 `mathematics` 的优化/不变量、`physics` 的守恒/摄动相交，但新增“整体目标→局部方程→结构量→扰动”的推导链 | 形式推导不等于真实预测；边界项、约束自由度、耗散和外部输入必须保留。 |
| 流体与连续介质 | MIT 流体课程覆盖控制体守恒、Euler/Navier-Stokes、边界条件、相似、涡量和模型测试；MIT 量纲文章给出变量→无量纲群→物理尺度→主导平衡的程序。[MIT Marine Hydrodynamics](https://www.ocw.mit.edu/courses/2-20-marine-hydrodynamics-13-021-spring-2005/pages/lecture-notes/)、[MIT Dimensional Analysis](https://ocw.mit.edu/courses/res-12-001-topics-in-fluid-dynamics-fall-2024/pages/essay-2-dimensional-analysis-of-models-and-data-sets-similarity-solutions-and-scaling-analysis/) | 控制体守恒、无量纲相似、主导平衡区间、边界适定性、降阶模型测试 | 与 `physics` 的量纲/守恒、`numerical-analysis-scientific-computing` 的误差、`engineering` 的压力测试相交，但新增连续介质的尺度分区与边界闭合 | 主导平衡只在声明尺度域有效；降阶模型要对照基线、边界和分布外情景；不提供流体工程放行。 |
| 物理化学与化学动力学 | MIT 化学动力学课程要求从速率律、快慢步骤和稳态近似判断机理是否与数据一致；IUPAC 明确区分 rate-controlling step 与简单的“最慢步骤”；NIST 数据库提供反应、产物和速率参数的来源记录。[MIT Chemical Kinetics](https://ocw.mit.edu/courses/5-111sc-principles-of-chemical-science-fall-2014/pages/unit-v-chemical-kinetics/)、[IUPAC Rate Controlling Step](https://goldbook.iupac.org/terms/view/R05139)、[NIST Chemical Kinetics Database](https://kinetics.nist.gov/kinetics/welcome.jsp) | 速率律规格、机理假设、速率控制步骤、稳态近似、动力学参数敏感性 | 与 `chemistry` 的平衡/机理、`organic-chemistry-reaction-design` 的箭推、`statistics` 的拟合相交，但新增“时间尺度—控制转移—参数可辨识”的动力学证据链 | 速率拟合不等于机理确证；稳态近似不等于中间体恒定；只读分析不提供合成、投料或危险实验建议。 |
| 电化学与传质 | IUPAC Nernst 条目定义平衡电势与活度/计量关系，Butler–Volmer 资料把界面电荷转移与过电位联系起来，Cottrell 条目描述扩散控制电流的时间响应。[IUPAC Nernst](https://goldbook.iupac.org/terms/view/09068)、[MIT Butler–Volmer](https://ocw.mit.edu/courses/10-626-electrochemical-energy-systems-spring-2014/56cfa6e0f28bc8fc1a647cbe679384d1_MIT10_626S14_S11lec13.pdf)、[IUPAC Cottrell](https://goldbook.iupac.org/terms/view/09069/html) | 电化学电池模型、平衡电势检查、界面电荷转移动力学、扩散极限诊断、电流—电势交叉检查 | 与 `chemistry` 的氧化还原/平衡、`analytical-chemistry-metrology` 的校准/干扰相交，但新增电势—动力学—传质三层信号归因 | 平衡关系不能直接用于极化状态；单一读数不是独立证据；电化学条目只做信号审计，不驱动设备或给出专业放行。 |

**第五波缺口判定**：现有库已有“概率估计、初值/边界、守恒/稳定、化学平衡和分析计量”的片段，但缺少随机停止合法性、连续系统适定性/分岔、变分结构保持、连续介质主导平衡、动力学时间尺度和电化学传质归因这些可组合链条。上述六个 pack 是语义细化，不改变八类功能轴，也不创建 selector、planner 或运行时 Binding。

## 第五波反向核验与停止条件

第五波每个领域均达到“至少两类权威来源、五个可落地程序、一个组合 Method、明确失败/恢复边界”的入库门槛；与既有 44 个 pack 的同义动作已做交叉检查。下一步优先转向真实消费方、Binding 和留出评估，不再以堆叠来源数量替代效果证据。

## 当前落库快照

第四波新增 30 个 source、6 个 derived；总量从 `286/38/324` 变为 `316/44/360`，pack 数从 38 变为 44，reference framework 从 155 增至 190。实际库校验结果为 `source_coverage=316/316 derived_methods=44/44 total=360`。

第五波新增 30 个 source、6 个 derived；总量从 `316/44/360` 变为 `346/50/396`，pack 数从 44 变为 50，reference framework 从 190 增至 202。实际库校验结果为 `source_coverage=346/346 derived_methods=50/50 total=396`。

## 反向证伪与停止条件

第二轮停止继续扩展的理由：每个新增领域都至少有两类权威来源、五个可落地的程序抽取点、一个组合方法和明确迁移限制；继续搜集同义教材不会明显改变 pack 边界。以下问题保留为后续评估，而不是用更多资料掩盖：

1. 算子在真实 Agent 任务上的质量提升、成本和延迟尚未测量。
2. 生态、认知、人因、医学、法律、伦理、教育、语言、历史和社会科学条目的跨场景外推必须单独验证。
3. 医学、人因与生态条目不能自行触发现实操作；必须由 Harness policy 和专业 verifier 接管。
4. 因果与博弈条目依赖模型假设；若假设不可观察或参与者并非理性，结果只能标记为 `inconclusive` 或情景分析。

## 历史落库快照

第二轮为每个母领域建立 5 个 source 条目和 1 个 derived Method，共新增 30 个 source、6 个 derived；总量从
`196/20/216` 变为 `226/26/252`，pack 数从 20 变为 26。实际库校验结果为
`source_coverage=226/226 derived_methods=26/26 total=252`。

## 第六波六个领域：结构、场、算子与证据汇合

第六波先对 50 个既有 pack、346 个 source 和 50 个 derived Method 做语义去重，再选择六条仍缺少完整程序链的基础领域。目标不是重复已有的 `mathematics.linear-algebra-factorization`、一般 `physics.symmetry`、`chemistry.spectroscopy-assignment` 或 `operations-research.dual-sensitivity`，而是补齐“从前置表示到独立验证”的领域方法。

### 25. 线性代数与谱方法

| 证据事实 | 可迁移的算子 | 信心与边界 |
| --- | --- | --- |
| MIT 18.06 把 `Ax=b`、列空间/零空间、秩、基、投影、最小二乘、特征值和 SVD 组织成一条从可解性到表示变换的课程主线。[MIT 18.06 Goals](https://web.mit.edu/18.06/www/Fall02/goals.html) | `rank-nullspace-solvability-audit`、`basis-and-coordinate-selection`、`orthogonal-projection-least-squares` | 高；线性结构成立不等于业务模型正确，近秩亏还依赖容差。 |
| MIT 18.065 系统覆盖 SVD、矩阵范数、最小二乘和 Eckart–Young 最优低秩近似，支持把压缩与残差绑定，而非只保留主成分。[MIT Matrix Methods](https://ocw.mit.edu/courses/18-065-matrix-methods-in-data-analysis-signal-processing-and-machine-learning-spring-2018/download/) | `spectral-mode-decomposition`、`low-rank-approximation-residual` | 高；谱排序依赖目标，低能量方向仍可能承载稀有关键语义。 |

**缺口判定**：已有条目会“做矩阵分解”，但没有“先判可解性—再选基—不可达时投影—识别主导模式—审计压缩残差”的完整诊断链，故新增独立 pack。

### 26. 拓扑与几何方法

| 证据事实 | 可迁移的算子 | 信心与边界 |
| --- | --- | --- |
| MIT 18.901 把连续映射、连通性、紧致性、分离性和基本群作为判断结构保持与不可达性的核心工具。[MIT Introduction to Topology](https://ocw.mit.edu/courses/18-901-introduction-to-topology-fall-2004/) | `topological-space-continuity-model`、`connected-component-decomposition`、`compactness-finite-witness-check` | 高；拓扑抽象主动丢弃距离、角度和尺度，不能用于需要这些量的结论。 |
| MIT 18.905 讲义明确使用 homotopy invariance、局部性和 CW 复形等方法把空间归并、拆解并寻找全局障碍。[MIT Algebraic Topology I](https://ocw.mit.edu/courses/18-905-algebraic-topology-i-fall-2016/2dad3dd8354992d877fbeca4049817ee_MIT18_905F16_lecture_notes.pdf) | `homotopy-invariant-comparison`、`local-to-global-obstruction-audit` | 高；相同不变量通常只是必要证据，不自动构成同伦等价的充分证明。 |

**缺口判定**：既有 symmetry、graph 和 invariant 条目没有表达连续变形、连通分支、有限子覆盖与局部解拼接障碍，故新增结构保持专用链。

### 27. 电磁学与场方法

| 证据事实 | 可迁移的算子 | 信心与边界 |
| --- | --- | --- |
| MIT 电磁场边值问题材料从 `E=-∇V`、Poisson/Laplace 方程、边界条件和叠加构造场解，强调源与边界共同决定解。[MIT Boundary Value Problems](https://live.ocw.mit.edu/courses/6-641-electromagnetic-fields-forces-and-motion-spring-2005/7cd0d4244c96782a35a34ed41b6e85c6_05.pdf) | `source-field-boundary-model`、`superposition-component-analysis`、`potential-boundary-value-solution` | 高；边界缺失、多介质或非线性会使简化失效。 |
| MIT 8.02 问题求解材料把 Gauss/Ampere 对称面、势、感应、波和能量传输结合用于交叉核验。[MIT Electricity and Magnetism Problem Solving](https://ocw.mit.edu/courses/8-02-physics-ii-electricity-and-magnetism-spring-2007/pages/problem-solving/) | `symmetry-adapted-gaussian-surface`、`field-energy-flux-conservation-check` | 高；必须先证明源和边界对称，不能因曲面方便就倒推对称。 |

**缺口判定**：一般 physics pack 已有量纲、对称和守恒，但没有把源—场—介质—边界、势表示和能流收支串为场问题闭环，故新增 pack。

### 28. 量子力学与算子方法

| 证据事实 | 可迁移的算子 | 信心与边界 |
| --- | --- | --- |
| MIT 量子章节把状态、可观测算子、本征值、测量概率、对易子与相容可观测量分开定义，支持对“状态—查询—结果”做严格分层。[MIT Quantum States and Observables](https://ocw.mit.edu/courses/22-02-introduction-to-applied-nuclear-physics-spring-2012/0456d26b0767e6aab3bace1e6f86d78b_MIT22_02S12_lec_ch2.pdf) | `state-observable-separation`、`compatible-observables-commutator-check`、`measurement-probability-normalization` | 高；迁移到一般 Agent 时只能作为有声明的结构类比，不能冒充量子物理结论。 |
| MIT Quantum Physics III 的 readings 覆盖变分原理、简并/非简并微扰和适配基，要求近似绑定小参数、对称性、阶次或界。[MIT Quantum Physics III Readings](https://ocw.mit.edu/courses/8-06-quantum-physics-iii-spring-2016/pages/readings/) | `basis-adapted-representation`、`variational-perturbative-approximation` | 高；微扰不小、简并未处理或试探空间错误时必须停。 |

**缺口判定**：既有矩阵、概率和扰动条目没有“算子是否相容—状态和算子是否共同换基—近似是否在有效域内—概率是否完备归一”的形式自洽链，故新增 pack。

### 29. 溶液热力学与相平衡

| 证据事实 | 可迁移的算子 | 信心与边界 |
| --- | --- | --- |
| MIT Thermodynamics of Materials 把化学势、相律、自由能、溶液和相图用于判断相共存与稳定性。[MIT Thermodynamics of Materials](https://ocw.mit.edu/courses/3-00-thermodynamics-of-materials-fall-2002/pages/lecture-notes/) | `component-phase-degree-of-freedom-audit`、`chemical-potential-equilibrium-check`、`phase-stability-free-energy-test` | 高；热力学稳定不代表动力学上能在目标时间到达。 |
| MIT Chemical Engineering Thermodynamics 覆盖 partial molar properties、Gibbs-Duhem、activity/fugacity、phase rule 和 stability，支持对多组分模型做跨变量一致性审计。[MIT Chemical Engineering Thermodynamics](https://ocw.mit.edu/courses/10-40-chemical-engineering-thermodynamics-fall-2003/pages/readings/) | `activity-fugacity-nonideality-model`、`gibbs-duhem-consistency-check` | 高；参数必须绑定温压、组成、相态和参考态，不能无界外推。 |

**缺口判定**：已有 thermodynamics pack 处理一般自由能/熵，chemical-kinetics 处理速率；两者都没有多相多组分的自由度、化学势相等、非理想修正和 Gibbs-Duhem 整体约束，故新增 pack。

### 30. 光谱学与结构解析

| 证据事实 | 可迁移的算子 | 信心与边界 |
| --- | --- | --- |
| MIT Organic Chemistry II 的结构解析流程按分子式/不饱和度、功能团、片段、连接和“解释全部数据”推进，而不是以单峰命中定案。[MIT Structure Determination Protocol](https://ocw.mit.edu/courses/5-13-organic-chemistry-ii-fall-2003/c6fe40cdadfb1733da5045528cf44e9f_unit1_study_gd.pdf) | `molecular-formula-unsaturation-constraint`、`orthogonal-spectral-feature-extraction`、`fragment-connectivity-construction`、`all-evidence-structure-consistency` | 高；混合物、重叠峰和非唯一候选必须保留为未决。 |
| NIST Chemistry WebBook 提供有来源的 IR、MS、UV/Vis 等参考数据；IUPAC JCAMP-DX 协议说明光谱交换必须携带可解释的条件和元数据。[NIST Chemistry WebBook](https://webbook.nist.gov/)、[IUPAC JCAMP-DX](https://stats.iupac.org/jcamp/protocols.html) | `reference-spectrum-condition-audit` | 高；数据库相似不能替代样品身份、采集条件和独立证据。 |

**缺口判定**：已有 chemistry 的 `spectroscopy-assignment` 是单点归属思路，analytical chemistry 关注定量与计量；缺少从硬约束到多谱片段、全证据反证和参考条件审计的完整结构解析链，故新增 pack。

## 第六波重复审计与分类决策

| 候选语义 | 最相近既有条目 | 决策 | 理由 |
| --- | --- | --- | --- |
| 线性结构诊断 | `mathematics.linear-algebra-factorization`、`numerical-analysis-scientific-computing.conditioning-vs-algorithm-stability` | Add + crosswalk | 旧条目没有可解空间、基选择、投影和低秩任务残差的连续链。 |
| 拓扑结构分析 | `mathematics.invariant`、`complexity-science.network-structure` | Add + crosswalk | 拓扑连续性、连通分支、紧致有限见证和局部整体障碍是独立语义。 |
| 电磁场推理 | `physics.symmetry`、`physics.conservation-law`、`fluid-dynamics-continuum-mechanics.boundary-condition-well-posedness-audit` | Add + crosswalk | 新链明确源—场—介质—边界、势、通量和能流，不重复一般原则。 |
| 量子算子模型 | `linear-algebra-spectral-methods.basis-and-coordinate-selection`、`statistics.probability-model` | Add + crosswalk | 对易性、共同本征表示、测量完备性和近似有效域具有专门前提。 |
| 多组分相平衡 | `thermodynamics-statistical-mechanics.free-energy-potential-selection`、`physical-chemistry-chemical-kinetics.rate-law-specification` | Add + crosswalk | 平衡自由度、化学势、活度/逸度和 Gibbs-Duhem 不能由一般热力学或动力学替代。 |
| 光谱结构解析 | `chemistry.spectroscopy-assignment`、`analytical-chemistry-metrology.matrix-interference-selectivity` | Add + crosswalk | 新链负责完整候选构造、全证据一致性和参考条件，不是单峰归属或定量。 |

**反向核验**：若删去领域术语后只剩“分解、验证、比较”这种一般动作，就不新建；本轮保留的 30 个 source 均含现有条目没有的前置对象、失败语义或证据契约。权威来源只能证明这些程序存在于母领域，不能证明迁移后能提升 Agent；因此全部保持 `experimental` / `reference_only`。

**研究停止条件**：每个领域已有至少两条权威来源、五个可执行程序点、一个明确组合链、重复 crosswalk 和不适用边界；继续增加同类教材只会增加引用数量而不改变算子语义，本轮在此停止。

## 当前落库结果

第六波新增 30 个 source、6 个 derived；总量从 `346/50/396` 变为 `376/56/432`，pack 数从 50 变为 56，reference framework 从 202 增至 214。该轮机器校验摘要为 `source_coverage=376/376 derived_methods=56/56 total=432`。

## 数学专项：55 项过程方法的缺口闭合

数学专项以 Pólya 生命周期、Schoenfeld 的 Resources/Heuristics/Control/Beliefs 分层、Mason–Burton–Stacey 的 specialising/generalising/conjecturing/convincing、NCTM process standards 与 MIT 证明材料为证据入口。它不新增领域，只回答现有 mathematics 和跨领域条目是否完整覆盖用户点名的 55 个方法。

| 审计面 | 结果 | 反向证伪 |
| --- | --- | --- |
| 55 项名称覆盖 | `55/55` 有目标 ID | 任一名称无 crosswalk 即失败 |
| 语义去重 | `20 reuse / 35 add` | 与既有条目仅名称不同、前置条件/程序/证据相同则不得新增 |
| 组合方法 | 新增 `mathematical-discovery-proof-loop` | 机械固定十步、无法按前提和预算跳过则设计失败 |
| 证据等级 | 明确样例、计算实验、类比不等于证明 | 把“未找到反例”写成“证明为真”即失败 |
| 分类 | 八个数学过程组映射到既有八类功能 | 不得把项目综合分类冒充外部官方标准 |
| 契约边界 | Core Schema 无变更，内容保持 `experimental/reference_only` | 条目自行授权、裁决或声称真实效果即失败 |

完整逐项矩阵见 [`MATHEMATICAL_PROBLEM_SOLVING_RESEARCH.md`](MATHEMATICAL_PROBLEM_SOLVING_RESEARCH.md)。本专项新增 35 个 source、1 个 derived；总量从 `376/56/432` 变为 `411/57/468`，pack 数保持 56，reference framework 从 214 增至 216。当前机器校验摘要为 `source_coverage=411/411 derived_methods=57/57 total=468`。
