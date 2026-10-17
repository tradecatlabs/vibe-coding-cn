# 通用问题求解方法论：八类功能与母领域双轴研究

> 研究日期：2026-09-04
> 研究对象：Vibe Harness CN 的静态 Operator Reference Library
> 研究状态：`experimental`；本文不声称 selector、planner、Binding 或真实任务效果已经实现。

## 一句话结论

算子库的上位对象不是学科知识，而是专家面对未知问题时反复使用的**启发式动作**与**元认知控制**。
每个条目要说明何时做、改变什么、留下什么证据、失败后怎么走；母领域只说明动作从哪里来，功能分类才说明
它在问题求解链上承担什么作用。

## 一、先把两个轴分开

```text
问题求解内容
├── source_domain 母领域：方法的出生地
│   ├── 数学、计算机科学、科学/研究方法
│   ├── 软件调试、软件设计、统计、机器学习
│   ├── 工程、系统思维、决策科学、运筹学、设计方法
│   └── 物理、化学、深度学习、信息论、复杂性科学等扩展来源
└── functional_class 功能类：方法改变问题空间的方式
    ├── representation 表征：换一种方式看清对象、边界和变量
    ├── decomposition 分解：把大问题拆成依赖可见的子问题
    ├── transformation 变换：把陌生问题改写成已有结构
    ├── search 搜索：在候选空间中排序、探索、剪枝或回退
    ├── construction 构造：做出候选、见证、原型或最小可行物
    ├── verification-falsification 验证/证伪：让主张面对独立证据
    ├── diagnosis-revision 诊断/修正：定位失效并做可归因改动
    └── control-metacognition 控制/元认知：选择策略、分配预算、停止或升级
```

同一个母领域可以贡献多个功能类；同一个功能类也应吸收多个母领域。比如“压力测试”来自工程学，
在功能轴上属于验证/证伪；“信息价值”来自决策科学，在功能轴上属于控制/元认知。这个映射是本项目的
工作性推断，不是任何学科的官方分类。

## 二、上位理论依据

### 1. Schoenfeld：知识、启发式和控制不是一层东西

Schoenfeld 将问题求解拆为 resources、heuristics、control/monitoring/self-regulation 和 beliefs。
对本库而言，resources 是领域知识的输入，heuristics 是算子库主体，control 是 Harness 的调度与停机
边界，beliefs 则决定什么被视为证据。来源：[Berkeley 对 Schoenfeld 工作的介绍](https://gsi.berkeley.edu/programs-services/hsl-project/hsl-speakers/schoenfeld/)。

### 2. Pólya：把解题变成可回看的循环

Understand → Plan → Carry out → Look back 不是僵硬流水线，而是一组可往返的检查点。它告诉我们：
生成答案之后仍要回看目标、边界、替代解和可推广性。来源：[University of Toronto 的 Pólya 四阶段说明](https://www.teach.cs.toronto.edu/~ajr/104/diary/01/polya.html)。

### 3. Newell–Simon：算子是在问题空间里改变状态

问题由状态、允许的 operators、目标状态和搜索路径构成；改变表示、选择性搜索和缩小候选空间，往往比
单纯增加推理文字更有效。来源：[CMU 保存的 Human Problem Solving 原始材料](https://iiif.library.cmu.edu/file/Newell_box00018_fld01306_doc0001/Newell_box00018_fld01306_doc0001.pdf)。

### 4. 元认知：监控理解、策略和停止点

元认知不仅是“想一想”，而是计划、监控理解、选择策略、评价结果并在证据不足时改路。来源：[National Academies 关于 metacognition 的章节](https://www.nationalacademies.org/read/10024/chapter/3)。

由此得到项目原则：**算子负责推进状态，Harness 负责决定何时用它；Verifer 负责裁决证据是否够。**

## 三、按八类功能分别开采方法

### 3.1 Representation 表征

**核心问题**：当前卡住是因为答案难，还是因为问题表示错了？

**母领域来源**：

- 计算机科学的 abstraction、state model、interface contract；Newell–Simon 说明更好的表示可让搜索规模显著下降。
- 数学的 definition-first、case analysis、specialization/generalization。
- 系统思维的 system boundary；工程学的 constraint budget；设计方法的 reframe user need。
- 统计学的 sampling frame；物理学的 boundary/initial conditions 与 dimensional analysis。

**迁移成算子程序**：列对象、边界、变量和不变量 → 生成文字/图/表/方程/状态图等替代表征 → 检查语义是否
保持 → 比较变量数、约束可见性和搜索负担 → 选择当前表示并留下回译记录。

**证据与边界**：必须有原表示、替表示、保持的不变量、信息损失和适用范围；换表示不等于解决问题，不能把
更漂亮的图当作真实性证明。相关资料：[ODU 对问题重构的研究](https://digitalcommons.odu.edu/psychology_fac_pubs/62/)、[NIST 抽样与统计方法](https://itl.nist.gov/div898/handbook/eda/section3/eda35.htm)。

### 3.2 Decomposition 分解

**核心问题**：怎样把一个大目标拆成可以独立检查、再组合的子目标？

**母领域来源**：

- 算法的 divide-and-conquer、dynamic programming、dependency graph 和 topological order。
- 软件工程的 requirements traceability、architecture decomposition。
- 研究方法的实验因素拆分；运筹学的优化模型变量、约束和子问题分解。
- 数学的分情况、归纳和辅助命题；工程学的需求到验证链。

**迁移成算子程序**：写出目标和依赖图 → 划定每个子问题的输入/输出/验收 → 判断可并行、串行、复用还是需要共享状态 → 先解决边界最清楚的子问题 → 组合并重新检查全局不变量。

**证据与边界**：产物是依赖图、子目标契约、组合规则和遗漏项；拆分如果改变了原目标或隐藏跨子问题耦合，
必须回退到整体表示。来源：[ACM/IEEE/AAAI CS2023](https://csed.acm.org/)、[MIT 算法设计与分析](https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/)。

### 3.3 Transformation 变换

**核心问题**：能否把陌生问题转成一个已有方法能处理的问题？

**母领域来源**：

- 计算机科学的 reduction、relaxation、abstraction。
- Pólya 的 analogy、solve a simpler problem、specialization/generalization。
- 运筹学的 relaxation and bound；物理学的 nondimensionalization、symmetry reduction、linearization。
- 化学的 retrosynthetic disconnection；信息论的 compression/rate-distortion。

**迁移成算子程序**：声明原问题与目标问题 → 写出映射规则和保持条件 → 变换或松弛 → 在熟悉空间求解/估计 → 将结果回译并检查变换引入的误差、丢失和不可逆点。

**证据与边界**：必须提供映射、保持的不变量、松弛造成的上下界和回译检查；近似解不能被写成原问题的精确解。
来源：[MIT AI 问题求解章节](https://courses.csail.mit.edu/6.034f/ai3/ch3.pdf)、[INFORMS 松弛与割平面教程](https://pubsonline.informs.org/doi/10.1287/educ.1090.0064)。

### 3.4 Search 搜索

**核心问题**：候选很多、预算有限时，下一条路径为什么值得先走？

**母领域来源**：

- 算法的 greedy、backtracking、branch-and-bound、randomized search、online/competitive analysis。
- Newell–Simon 的 selective search；机器学习的 active learning、hyperparameter search。
- 决策科学的 value of information；运筹学的 simulation optimization；设计方法的 divergent/convergent。

**迁移成算子程序**：定义候选空间、目标测试、希望度/信息价值和预算 → 生成或扩展有限分支 → 记录排序、剪枝、
回退和未搜索区域 → 周期性比较替代策略 → 在收益低于成本或遗漏风险过高时停止/换路。

**证据与边界**：需要候选队列、评价函数、访问顺序、剪枝理由、覆盖声明和预算消耗；启发式排序不是全局最优
证明，必须保留可恢复分支或独立抽查。来源：[Stanford 决策理论资料](https://ai.stanford.edu/~koller/BNtut/index.html)、[INFORMS 仿真优化](https://pubsonline.informs.org/doi/pdf/10.1287/educ.2013.0118?download=true)。

### 3.5 Construction 构造

**核心问题**：怎样把“应该可行”变成别人能检查的东西？

**母领域来源**：

- 数学的 constructive proof、witness、prototype。
- 设计和工程的 prototype/test article；化学的 mechanism hypothesis、retrosynthesis candidate。
- 机器学习/深度学习的 transfer、distillation、architecture search；编程的 minimal reproduction。

**迁移成算子程序**：选择决定成败的最小假设 → 构造候选、样例、原型或见证 → 只覆盖当前问题的关键约束 → 由独立检查读取产物 → 根据结果保留、修改或淘汰。

**证据与边界**：产物必须可复现、带输入/版本/假设和检查结果；一个样例通过不代表普遍成立，原型通过不代表生产验收。
来源：[Stanford ME113 Design Thinking](https://web.stanford.edu/class/me113/d_thinking.html)、[NASA Systems Engineering Handbook](https://www.nasa.gov/reference/system-engineering-handbook-appendix/)。

### 3.6 Verification / Falsification 验证/证伪

**核心问题**：什么证据足以支持、限制或推翻当前主张？

**母领域来源**：

- 数学的 direct proof、contrapositive、contradiction、counterexample、invariant、extremal principle。
- 科学/研究方法的 hypothesis、control、randomization、blinding、replication、falsification。
- 统计学的 interval estimation、hypothesis testing、effect size；机器学习的 holdout、cross-validation、calibration、ablation。
- 物理学的 dimensional/conservation/limit/residual checks；工程学的 V&V、qualification、stress test 和 safety margin。

**迁移成算子程序**：先写主张、基线和可证伪条件 → 选择独立对照或边界情景 → 执行测量/推导/测试 → 区分通过、
未判定和失败 → 只在证据契约满足时支持结论，发现反例时回退或缩小范围。

**证据与边界**：证据必须含数据来源、基线、指标、不确定度、留出边界和失败解释；“没有发现反例”不等于“已经证明”。
来源：[NIST 统计方法](https://itl.nist.gov/div898/handbook/eda/section3/eda35.htm)、[NIH 严谨性与可重复性](https://www.grants.nih.gov/policy-and-compliance/policy-topics/reproducibility)、[NASA 系统工程](https://www.nasa.gov/reference/system-engineering-handbook-appendix/)。

### 3.7 Diagnosis / Revision 诊断/修正

**核心问题**：失败首次发生在哪里，什么最小改动能区分根因？

**母领域来源**：

- 软件调试的 reproduce、localize、bisect、trace、root cause、regression、fuzzing 和 minimal reproduction。
- 统计学的 missingness/confounding audit、误差分析；物理学的 residual analysis；机器学习的 error analysis、OOD check、feature ablation。
- 系统思维的 feedback loop、bottleneck、second-order effect；设计方法的 feedback iteration。

**迁移成算子程序**：冻结失败输入和版本 → 建立最小复现 → 逐段定位首次偏离 → 只改变一个可归因变量 → 重测原失败与反事实对照 → 记录修正、回退和回归范围。

**证据与边界**：必须保存失败前后状态、定位探针、变更差异和回归结果；一次通过但不能在未修复条件下失败的测试只算
post-fix regression，不能证明因果。来源：[Python Debugging and Profiling](https://docs.python.org/3/library/debug.html)、[scikit-learn Common Pitfalls](https://scikit-learn.org/stable/common_pitfalls.html)。

### 3.8 Control / Metacognition 控制/元认知

**核心问题**：什么时候继续、停止、切换、回退、追加信息或请求人工？

**母领域来源**：

- Schoenfeld 的 control/monitoring/self-regulation；Pólya 的 look back。
- 决策科学的 expected utility、opportunity cost、value of information、regret/robustness。
- 统计/工程的 uncertainty、sensitivity、safety margin；系统思维的反馈、稳态和韧性。
- 软件工程的预算、checkpoint、review、traceability；机器学习的 learning curve 和 confidence escalation。

**迁移成算子程序**：声明进展指标、风险阈值、时间/token/工具预算和升级通道 → 在检查点比较当前策略与替代策略的预期收益 → 继续、切换、回退、停机或升级 → 将控制决定写入 trace。

**证据与边界**：需要预算轨迹、阈值来源、策略比较、停止理由和人工决定；活动量、模型自报信心或循环次数都不能单独证明进展。
来源：[National Academies metacognition](https://www.nationalacademies.org/read/10024/chapter/3)、[MIT Value of Information](https://ocw.mit.edu/courses/ids-333-risk-and-decision-analysis-fall-2021/resources/unit-9-value-of-info-video-4/)、[INFORMS Sensitivity Analysis](https://pubsonline.informs.org/doi/abs/10.1287/educ.2023.0259)。

## 四、用户列出的母领域如何落库

下表只回答“从哪里挖”和“已落到哪个 pack”，不把母领域名称当作功能分类。

| 母领域 | 反复使用的方法 | 当前 pack / 状态 | 主要功能类（项目映射） |
| --- | --- | --- | --- |
| 数学 Problem Solving | 定义、证明、反例、不变量、归纳、构造、极值 | `mathematics` 已有；`problem-solving-methodology` 新增通用层 | 验证/证伪、表征 |
| CS Algorithmic Thinking | 分解、归约、分治、DP、贪心、回溯、剪枝、复杂度 | `computer-science`、`algorithms` 已有 | 分解、变换、搜索 |
| Scientific Reasoning | 假设、操作化、干预、对照、证伪、重复、敏感性 | `scientific-methodology`、`research` 已有 | 验证/证伪、控制 |
| Software Debugging | 复现、定位、二分、跟踪、根因、回归 | `programming`、`software-engineering` 已有 | 诊断/修正 |
| Software Design | 抽象、模块化、分离、权衡、重构、追踪 | `software-engineering` 已有 | 表征、分解、诊断/修正 |
| Statistics | 抽样、估计、比较、不确定性、更新、混杂审计 | `statistics` 新增 | 验证/证伪、诊断/修正 |
| Machine Learning | baseline、holdout、ablation、正则化、CV、误差分析 | `machine-learning` 已有 | 验证/证伪、搜索 |
| Engineering | 约束、权衡、原型、压力测试、安全裕度 | `engineering` 新增 | 构造、验证/证伪、控制 |
| Systems Thinking | 边界、反馈回路、瓶颈、二阶效应、涌现 | `systems-science`、`complexity-science` 已有 | 表征、控制、诊断/修正 |
| Decision Science | 期望值、机会成本、信息价值、贝叶斯更新、鲁棒决策 | `decision-science` 新增 | 控制/元认知、搜索 |
| Operations Research | 优化、松弛、界、敏感性、仿真、排队 | `operations-research` 新增 | 搜索、变换、诊断/修正 |
| Design Methods | 重构、发散、收敛、原型、迭代 | `design-methods` 新增 | 表征、构造、搜索、诊断/修正 |
| Research Methods | 预注册、随机化、盲法、样本量、重复、透明报告 | `research`、`scientific-methodology` 已有 | 验证/证伪、控制 |
| Physics | 量纲、守恒、极限、尺度、对称、稳定、残差 | `physics` 已有 | 表征、变换、验证/证伪 |
| Chemistry | 物料/电荷/电子平衡、平衡、机理、谱学、绿色筛查 | `chemistry` 已有 | 变换、构造、验证/证伪 |
| Deep Learning | 迁移、蒸馏、剪枝、量化、分布式、扩展 | `deep-learning` 已有 | 构造、搜索、控制 |
| Information Theory | 熵、互信息、压缩、率失真、信道容量 | `information-theory` 已有 | 表征、变换、搜索 |
| Complexity Science | 网络、涌现、临界、粗粒化、混沌、突变 | `complexity-science` 已有 | 表征、验证/证伪、控制 |

## 四点一、本轮新增六个母领域的深挖结果

本轮继续从六个母领域抓取一手/官方资料，并把“来源事实、项目迁移、限制条件”分开记录在
[`research/DOMAIN_EVIDENCE_MATRIX.md`](DOMAIN_EVIDENCE_MATRIX.md)。结论不是增加六组知识名词，而是补上六种
Harness 在陌生问题中常缺的动作边界：

| 母领域 | 可复用动作 | 新增 pack | 主要功能类 | 关键限制 |
| --- | --- | --- | --- | --- |
| 因果推断 | 定义干预和目标试验、画 DAG、审查识别假设、做敏感性分析 | `causal-inference` | 表征、变换、验证/证伪、控制 | 相关不能直接写成因果；DAG 和交换性假设须人工审查 |
| 经济学/博弈论 | 建战略互动、求最佳反应/均衡、检查承诺可信性、设计激励与信号 | `economics-game-theory` | 表征、搜索、构造、验证/证伪、控制 | 均衡是模型内稳定性，不保证现实预测；参与者未必完全理性 |
| 生态/生物学 | 分离真实生态状态与观测过程、层级建模、扰动对照、权衡与韧性分析 | `ecology-biology` | 表征、验证/证伪、控制 | 观测误差、尺度和长期数据决定可识别性，不能自动执行现实干预 |
| 认知科学 | 识别工作记忆负荷、分块、重编码、类比迁移、元认知监控 | `cognitive-science` | 表征、构造、控制/元认知 | 研究情境到 Agent 的迁移是工程假设，不是效果证明 |
| 人因与可靠性 | 情境态势检查、程序状态、负荷边界、独立交叉检查、错误恢复 | `human-factors-reliability` | 验证/证伪、诊断/修正、控制 | 高影响动作仍须人工审批、停止和恢复策略 |
| 医学决策 | 结构化问题、证据确定性、收益/伤害、价值偏好、资源/公平/可行性 | `medical-decision` | 表征、验证/证伪、控制 | 仅作证据组织参考，不能替代诊疗、处方或临床流程 |

六个 pack 均保持 `experimental`，权限归具体 Harness policy，结果归独立 verifier，敏感值为
`reference_only`。本轮没有修改公共 Core，也没有把这些方法注册成 selector、planner 或现实操作授权。

## 四点二、第二轮六个母领域的深挖结果

第二轮把历史、社会、教育、语言、法律和伦理领域的“专家程序”抽取为 6 个 pack；每个 pack 含 5 个 source 条目和 1 个 derived Method。逐条证据、来源链接、迁移限制和停止理由见 [`research/DOMAIN_EVIDENCE_MATRIX.md`](DOMAIN_EVIDENCE_MATRIX.md)。

| 母领域 | 可复用动作 | 新增 pack | 主要功能类 | 关键限制 |
| --- | --- | --- | --- | --- |
| 法律推理 | 争点识别、权威层级、先例类比/区分、证明标准、规则—事实反方审计 | `legal-reasoning` | 表征、变换、验证/证伪 | 高风险，仅作研究参考，法域和专业复核不可省略 |
| 伦理与公共政策 | 利益相关者影响、比例/不伤害、权利公平、影响评估、人类监督与责任 | `ethics-public-policy` | 表征、验证/证伪、控制 | 不能替代伦理审查、法律判断或责任主体 |
| 教育与学习科学 | 目标操作化、先备/误解诊断、提取应用、支架淡出、形成性反馈 | `education-learning-science` | 表征、构造、诊断、控制 | 熟悉感和课程完成不等于迁移学习 |
| 语言学 | 语料采样、最小对比、句法—语义—语用分层、篇章语境、歧义消解 | `linguistics` | 表征、验证/证伪、诊断 | 结论必须绑定语言变体、语域、标注和上下文 |
| 历史推理 | 来源出处批判、语境分期、交叉印证、史学视角、受约束反事实 | `historical-reasoning` | 表征、变换、验证/证伪 | 反事实是分析工具，不是另一段事实历史 |
| 社会科学方法 | 构念/问题操作化、抽样代表性、质性编码、混合方法、制度情境 | `social-science-methods` | 表征、验证/证伪、诊断、控制 | 不把样本、叙事或相关性写成普遍因果 |

第二轮仍保持 `experimental`、`reference_only`、`harness_policy` 和 `verifier`；没有新增运行时 selector、planner、数据库或工具授权。

## 四点三、第三波六个母领域的深挖结果

第三波继续沿“领域知识”和“领域方法”分离的原则，选择能补足形式核验、解释克制、空间外推、观测建模、材料计量和证据检索的六个来源域。每个领域形成 5 个 source 条目和 1 个 derived Method，详细来源与缺口见 [`research/DOMAIN_EVIDENCE_MATRIX.md`](DOMAIN_EVIDENCE_MATRIX.md)。

| 母领域 | 可复用动作 | 新增 pack | 主要功能类 | 关键限制 |
| --- | --- | --- | --- | --- |
| 形式逻辑与自动推理 | 形式规约、语法/语义分离、反模型搜索、子目标分解、内核核验 | `formal-logic-automated-reasoning` | 表征、分解、搜索、验证、控制 | 有限搜索不能自动推出一般定理；证明项和模型域必须固定 |
| 科学哲学与认识论 | 观察/解释分离、最佳解释、辅助假设审计、欠定分支、区分性证据 | `philosophy-science-epistemology` | 表征、搜索、诊断、构造、控制 | “最佳”是相对比较，不是事实真值 |
| 地球科学与地质推理 | 观察不确定性、地层排序、地图/剖面、物质平衡、地面验证 | `earth-science-geoscience` | 表征、变换、验证、控制 | 稀疏观测、空间误差和边界假设限制外推 |
| 天文学与天体物理 | 观测模型、背景扣除、信号检测、尺度检查、拟合与独立确认 | `astronomy-astrophysics` | 表征、验证、控制 | 检测不等于参数观测，拟合通过不等于模型唯一正确 |
| 材料科学与工程测量 | 加工—结构—性能、微结构表征、计量追溯、数据质量、资格校准 | `materials-science` | 表征、变换、验证、控制 | 样品状态、measurand 和校准链决定可比性 |
| 信息与知识组织科学 | 信息需求、查询扩展、来源血缘、精确率/召回率、FAIR 检查 | `information-knowledge-science` | 表征、搜索、验证、控制 | 检索指标依赖判断集，FAIR 不是自动合规证明 |

第三波仍保持 `experimental`、`reference_only`、`harness_policy` 和 `verifier`；没有新增运行时 selector、planner、数据库或工具授权。

## 四点四、第四波六个母领域的深挖结果

第四波沿“领域方法而非领域知识”的原则补齐控制、误差、离散搜索、物理状态、化学选择性和测量可信度六个缺口。每个领域落成 5 个 source 和 1 个 derived Method，全部仍是 reference-only。

| 母领域 | 可复用动作 | 新增 pack | 主要功能类 | 关键限制 |
| --- | --- | --- | --- | --- |
| 控制论与反馈系统 | 状态空间、可控/可观测审计、反馈误差修正、稳定裕度、滚动重规划 | `control-theory-cybernetics` | 表征、验证、控制 | 闭环改善不等于真实稳定；延迟、饱和、权限和独立验证不可省略 |
| 数值分析与科学计算 | 条件性/稳定性区分、收敛、误差分配、残差/后向误差、复现实验 | `numerical-analysis-scientific-computing` | 验证、诊断、控制 | 残差小不保证前向误差小；单点输出不证明收敛 |
| 离散组合数学 | 双射表示、抽屉碰撞、容斥、递推/生成函数、极值图界 | `discrete-combinatorics` | 表征、搜索、构造、验证 | 有限搜索未找到不代表不存在；对象域和剪枝界必须公开 |
| 热力学与统计物理 | 系统边界/状态变量、熵、自由能界、扰动响应、系综采样 | `thermodynamics-statistical-mechanics` | 表征、验证、控制 | 热力学可行不等于动力学必然；统计趋势不等于单次预测 |
| 有机化学反应设计 | 化学/区域/立体选择性、保护基代价、机理箭推、路线复现审查 | `organic-chemistry-reaction-design` | 表征、验证、诊断 | 只读路线推理，不授权合成、采购、放大或危险实验 |
| 分析化学与计量学 | 校准、LOD/LOQ、基质干扰、用途验证、不确定度预算 | `analytical-chemistry-metrology` | 表征、验证、控制 | 检出限不等于可靠定量；结果必须绑定量程、基质和不确定度 |

第四波继续证明：八类功能轴足以承载新增方法，新增的是领域化语义和证据契约，不是新的运行时权限或执行系统。

## 四点五、第五波六个动态科学领域的深挖结果

第五波不再扩展泛化的“学科名录”，而是把六条仍缺少时间结构和连续状态的程序链拆开：随机过程负责不确定状态、概率界和停止；微分方程负责适定性、相图、稳定性和分岔；经典力学负责变分目标、局部方程、守恒结构和扰动；流体负责控制体、尺度、主导平衡、边界和降阶；化学动力学负责速率律、机理、时间尺度和参数可辨识；电化学负责平衡、界面动力学、传质和多通道归因。每个领域新增 5 个 source 和 1 个 derived Method。

| 母领域 | 可复用动作 | 新增 pack | 主要功能类 | 关键限制 |
| --- | --- | --- | --- | --- |
| 随机过程与概率过程 | Markov 状态、鞅不变量、停止边界、集中界、耦合比较 | `stochastic-processes-probability` | 控制/元认知 | 概率范围不等于单次保证，停止规则不能偷看未来 |
| 微分方程与动力系统 | 适定性、相图、Lyapunov、分岔、敏感性 | `differential-equations-dynamical-systems` | 验证/证伪 | 局部稳定不等于全局稳定，仿真不等于证明 |
| 经典力学与变分方法 | 变分建模、Euler-Lagrange、对称守恒、Hamilton 状态、扰动 | `classical-mechanics-variational-methods` | 表征 | 形式推导不等于真实预测，边界/耗散必须显式保留 |
| 流体与连续介质 | 控制体守恒、无量纲相似、主导平衡、边界适定性、降阶测试 | `fluid-dynamics-continuum-mechanics` | 表征 | 简化只在声明尺度域有效，不提供工程放行 |
| 物理化学与化学动力学 | 速率律、机理假设、速率控制、稳态近似、参数敏感性 | `physical-chemistry-chemical-kinetics` | 验证/证伪 | 拟合不等于机理确证，只读分析不授权化学操作 |
| 电化学与传质 | 电池模型、Nernst、界面动力学、扩散极限、电流/电势交叉检查 | `electrochemistry-mass-transport` | 诊断/修正 | 平衡关系不能直接用于极化状态，不驱动设备 |

第五波继续验证了一个设计结论：八类功能轴仍然足够，新增的是“状态如何演化、假设在哪个尺度成立、什么证据能区分瓶颈”的领域化语义，不是新的权限或运行时类型。来源事实、迁移推断和未验证项已在 [`DOMAIN_EVIDENCE_MATRIX.md`](DOMAIN_EVIDENCE_MATRIX.md) 分开列出。

## 四点六、第六波六个基础领域的深挖结果

第六波优先补数学、物理、化学中的“结构与证据链”，不是继续扩充一般名词。入库前先与现有 396 个条目做 crosswalk；每个领域只保留 5 个具有独立前置对象、失败语义或证据契约的 source，再组合 1 个 derived Method。

| 母领域 | 可复用动作 | 新增 pack | 主要功能类 | 关键限制 |
| --- | --- | --- | --- | --- |
| 线性代数与谱方法 | 秩/零空间可解性、基选择、投影最小二乘、谱模式、低秩残差 | `linear-algebra-spectral-methods` | 表征 | 低秩和小残差不等于任务语义正确；病态性与稀有方向必须检查 |
| 拓扑与几何方法 | 连续性、连通分支、紧致有限见证、同伦不变量、局部整体障碍 | `topology-geometry` | 变换 | 拓扑抽象丢失度量；相同不变量通常不是等价的充分证明 |
| 电磁学与场方法 | 源—场—边界、对称面、叠加、势边值、能流收支 | `electromagnetism-field-methods` | 表征 | 对称、线性和势表示必须先验证，经典场模型不覆盖所有尺度 |
| 量子力学与算子方法 | 状态/可观测量分离、对易检查、基适配、受界近似、概率归一 | `quantum-mechanics-operator-methods` | 表征 | 一般 Agent 中只可作显式结构类比，不能伪装成量子物理效果 |
| 溶液热力学与相平衡 | 相律自由度、化学势、活度/逸度、相稳定、Gibbs-Duhem | `solution-thermodynamics-phase-equilibria` | 验证/证伪 | 平衡不等于动力学可达；模型参数必须绑定温压、组成与参考态 |
| 光谱学与结构解析 | 分子式硬约束、正交谱证据、片段连接、全证据一致性、参考条件 | `spectroscopy-structure-elucidation` | 诊断/修正 | 谱归属可能非唯一；数据库命中不等于样品身份或专业放行 |

第六波仍保持 `experimental`、`reference_only`、`harness_policy` 和 `verifier`。详细一手来源、重复审计、迁移限制与停止条件见 [`DOMAIN_EVIDENCE_MATRIX.md`](DOMAIN_EVIDENCE_MATRIX.md)。新增内容不修改公共 Core，不创建 selector、planner、Binding、现实实验步骤或专业授权。

## 四点七、数学问题求解的过程级深挖

数学专项不再增加母领域，而是把用户点名的 55 个方法按“定义与表征 → 特化与实验 → 模式与猜想 → 变换与归约 → 构造与搜索 → 证明与界定 → 反例与压力检查 → 元认知控制与复盘”逐项对账。20 项已有稳定同义语义，35 项是可区分缺口；后者补入现有 mathematics pack，并由 1 个 derived Method 连接发现、证明、反驳和复盘。

专项结果进一步确认 Schoenfeld 的分层：数学知识与定理属于 Resources；本轮条目属于 Heuristics；Relevance Check、Progress Measure 与 Strategy Switching 属于 Control；什么算证明、反例或计算证据属于 Beliefs/Epistemic policy。详细 55 行 crosswalk 和证据等级见 [`MATHEMATICAL_PROBLEM_SOLVING_RESEARCH.md`](MATHEMATICAL_PROBLEM_SOLVING_RESEARCH.md)。

## 五、从方法到可调用条目的抽取规约

领域资料只提供“出生地和方法事实”；进入算子库前按下列步骤再写一遍：

```text
来源事实
  → 它反复解决的核心问题
  → 当前状态/目标/约束
  → 最小可执行 procedure 或 Method steps
  → effect：知识、候选、治理或现实状态如何改变
  → evidence_required：别人如何复核
  → outcomes：成功、失败、未判定、阻塞或预算耗尽
  → failure_modes + recovery：哪里会误导，如何回退/换路
```

对应 Core 字段：

- `MentalModelSpec`：只写 questions、interpretation_rules、limitations，表达“怎么看”。
- `OperatorSpec`：写 preconditions、inputs、procedure、effect、outcomes、evidence_required、failure_modes、recovery，表达“做一次什么”。
- `MethodSpec`：用有序 `steps` 组合 Operator 或 `apply_model`，写 stop/success/evidence/failure，表达“如何组成一条方法”。
- `extensions.vibe-harness-cn.functional_class` 与本目录 taxonomy 只表达项目分类，不改写 Core 语义。

条目不能授权工具、批准自身结果、内联秘密或把来源链接冒充实验效果。高风险动作必须由具体 Harness
policy、隔离环境和独立 verifier 接管。

## 六、历史阶段快照与当前落库结果

| 指标 | 上一历史阶段 | 第二历史阶段完成后 |
| --- | ---: | ---: |
| source 条目 | 196 | 226 |
| derived Method | 20 | 26 |
| 总条目 | 216 | 252 |
| domain pack | 20 | 26 |
| reference framework | 63 | 87 |

第三波完成后的当前快照：286 个 source、38 个 derived、324 个总条目、38 个 domain pack、155 个 reference framework。

第四波完成后的当前快照：316 个 source、44 个 derived、360 个总条目、44 个 domain pack、190 个 reference framework。

第五波完成后的快照：346 个 source、50 个 derived、396 个总条目、50 个 domain pack、202 个 reference framework；机器校验摘要为 `source_coverage=346/346 derived_methods=50/50 total=396`。

第六波完成后的历史快照：376 个 source、56 个 derived、432 个总条目、56 个 domain pack、214 个 reference framework；机器校验摘要为 `source_coverage=376/376 derived_methods=56/56 total=432`。

数学专项完成后的当前快照：411 个 source、57 个 derived、468 个总条目、56 个 domain pack、216 个 reference framework；机器校验摘要为 `source_coverage=411/411 derived_methods=57/57 total=468`。

上一阶段新增 pack 为 `problem-solving-methodology`、`statistics`、`decision-science`、
`operations-research`、`design-methods`、`engineering`；本轮再新增 `causal-inference`、
`economics-game-theory`、`ecology-biology`、`cognitive-science`、`human-factors-reliability`、
`medical-decision`。机器清单见
[`operators/source-inventory.json`](../operators/source-inventory.json)、[`operators/catalog.json`](../operators/catalog.json)，
双轴索引见 [`operators/taxonomy/problem-solving-methodology.json`](../operators/taxonomy/problem-solving-methodology.json)。

第二轮新增 pack 为 `legal-reasoning`、`ethics-public-policy`、`education-learning-science`、`linguistics`、`historical-reasoning`、`social-science-methods`；第三波再加入 `formal-logic-automated-reasoning`、`philosophy-science-epistemology`、`earth-science-geoscience`、`astronomy-astrophysics`、`materials-science`、`information-knowledge-science`，把形式核验、认识论克制、地学外推、天文观测、材料计量和证据检索纳入同一套八类功能轴。

## 七、已知边界与下一阶段

1. 来源权威只能证明方法存在及其原始目的，不能证明它迁移到 Agent 后一定有效。
2. 功能类是本项目按“主要改变问题空间的动作”做的归类；一个条目可以有交叉类，但必须有一个主类。
3. 目前只完成静态内容、引用和计数校验，没有实现在线检索、selector、planner、运行时 binding、真实化学/工程实验或跨模型评估。
4. `experimental` 不能升级为 `verified`，除非有固定任务集、正负例、留出评估、重复运行、成本/延迟、独立 verifier、恢复和版本绑定证据。
5. 下一阶段不再以“继续堆数量”为目标；数学专项已把用户点名的 55 个方法逐项闭合。后续优先补真实消费方、Binding、负例和留出评估；只有出现明确缺口，才继续扩展。扩展前仍须先证明新语义不重复、证据可追溯且能写出失败契约。

最终边界可以压成一句话：**母领域提供矿石，八类功能提供切面，算子契约把切面变成可审计动作，Harness 决定是否调用，Verifier 决定是否相信。**
