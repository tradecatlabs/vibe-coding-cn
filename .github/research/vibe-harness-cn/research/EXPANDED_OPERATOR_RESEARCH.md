# 跨学科问题求解算子深度调研

> 研究日期：2026-09-04
> 研究对象：Vibe Harness CN 的静态 Operator Reference Library
> 研究状态：`experimental`，仅作方法参考，不代表运行时已验证

## 一句话结论

算子库不是“知识百科”，也不是提示词集合；它把成熟学科中反复使用的**问题求解动作**压缩成可检索、可组合、可审计的参考条目。条目回答“什么时候用、怎么做、产生什么证据、何时停止/回退”，具体 Harness 再决定是否调用、如何授权和怎样执行。

本报告的上位方法论与双轴分类见
[`HEURISTIC_METACOGNITIVE_RESEARCH.md`](HEURISTIC_METACOGNITIVE_RESEARCH.md)：母领域记录方法出处，
八类功能记录它在问题空间中承担的动作，二者不混用。

## 研究边界与方法

本轮只做只读资料研究和结构化沉淀，不运行任何上游代码，不把网页中的指令当作本项目指令。优先使用大学课程、国家实验室/政府机构、专业标准组织和官方项目文档；每个算子仍需经过本项目实际 Harness Binding、负例和评估后，才可能从 `experimental` 晋升。

抽取规则固定为：

```text
问题/状态/目标
    → 适用前提
    → 最小操作步骤
    → 状态或认知效果
    → 成功/失败证据
    → 停止、回退或升级
```

`MentalModelSpec` 只提供观察角度；`OperatorSpec` 描述一次动作；`MethodSpec` 组合多个动作。它们不拥有工具权限，不批准自身结果，也不替代领域专家或 verifier。

## 证据矩阵

| 领域 | 采用的成熟方法 | 可迁移的算子族 | 主要证据 |
| --- | --- | --- | --- |
| 数学 | 定义、证明、反例、不变量、逼近、概率推断、误差和尺度 | 松弛、敏感性、极限、误差界、贝叶斯更新、假设检验、矩阵分解、归一化 | [MIT Mathematics for Computer Science](https://ocw.mit.edu/courses/6-1200j-mathematics-for-computer-science-spring-2024/)、[MIT Probability](https://ocw.mit.edu/courses/6-041sc-probabilistic-systems-analysis-and-applied-probability-fall-2013/pages/unit-iv/)、[MIT Approximation](https://ocw.mit.edu/courses/6-055j-the-art-of-approximation-in-science-and-engineering-spring-2008/) |
| 物理学 | 量纲、守恒、极限、数量级、对称、摄动、边界/初值、稳定性、残差、不确定度 | 量纲检查、守恒检查、极限分析、数量级估计、对称约简、线性化、边界条件、稳定性、残差、不确定度传播 | [MIT Dimensional Analysis](https://ocw.mit.edu/courses/2-25-advanced-fluid-mechanics-fall-2013/pages/dimensional-analysis/)、[MIT Classical Mechanics](https://ocw.mit.edu/courses/8-09-classical-mechanics-iii-fall-2014/)、[NIST Measurement Uncertainty](https://www.nist.gov/itl/sed/topic-areas/measurement-uncertainty) |
| 化学 | 物料/电荷/电子守恒、质量作用定律、酸碱平衡、动力学、机理、光谱和绿色化学 | 原子电荷平衡、限量试剂、酸碱形态、氧化还原、化学平衡、速率诊断、机理假设、光谱指派、逆合成、绿色筛选 | [IUPAC Gold Book](https://goldbook.iupac.org/)、[IUPAC Mass Action](https://goldbook.iupac.org/terms/view/08184)、[IUPAC Acid Dissociation](https://goldbook.iupac.org/terms/view/15441)、[NIST Chemistry WebBook](https://webbook.nist.gov/)、[ACS 12 Principles](https://www.acs.org/green-chemistry-sustainability/principles/12-principles-of-green-chemistry.html) |
| 计算机科学 | 抽象、分解、归约、状态转移、不变量、契约、缓存、依赖图 | 状态建模、不变量检查、接口契约、记忆化、依赖图 | [ACM CS2023](https://csed.acm.org/)、[NIST Formal Methods](https://csrc.nist.gov/glossary/term/formal_methods) |
| 算法 | 复杂度、近似、随机化、图、拓扑序、在线竞争分析 | 摊还分析、近似、随机搜索、图建模、拓扑排序、在线/竞争分析 | [MIT Algorithms](https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/) |
| 科学方法论 | 假设、随机化、盲法、实验设计、功效、重复和透明报告 | 假设操作化、随机化、盲法、实验设计、样本量/功效、重复研究 | [NIH Reproducibility](https://www.grants.nih.gov/policy-and-compliance/policy-topics/reproducibility)、[NINDS Rigorous Study Design](https://www.ninds.nih.gov/funding/preparing-your-application/preparing-research-plan/rigorous-study-design-and-transparent-reporting)、[National Academies](https://nap.nationalacademies.org/resource/25303/R%26R.pdf) |
| 系统科学/控制 | 边界、库存-流量、因果回路、反馈、稳态、必要多样性、韧性 | 系统边界、因果回路、库存流、反馈控制、稳态、必要多样性、鲁棒性 | [MIT System Dynamics](https://ocw.mit.edu/courses/15-871-introduction-to-system-dynamics-fall-2013/)、[MIT Feedback Control](https://ocw.mit.edu/courses/16-30-feedback-control-systems-fall-2010/)、[ANU Cybernetics](https://cybernetics.anu.edu.au/news/2024/07/08/understanding-cybernetics/) |
| 信息论 | 熵、互信息、压缩、率失真、信道容量 | 不确定性、信息增益、信息瓶颈、率失真、信道容量 | [MIT Information Theory](https://ocw.mit.edu/courses/6-441-information-theory-spring-2016/pages/lecture-notes/) |
| 复杂性科学 | 网络、涌现、敏感性、临界转变、多尺度、耗散、协同、突变 | 涌现、网络映射、敏感性/混沌、相变、多尺度粗粒化、耗散结构、序参量、突变边界 | [Complexity Explorer Networks](https://www.complexityexplorer.org/courses/117-introduction-to-networks)、[MIT Nonlinear Dynamics](https://ocw.mit.edu/courses/12-006j-nonlinear-dynamics-chaos-fall-2022/pages/lecture-notes/) |
| 软件工程/编程 | 需求追踪、V&V、风险测试、可观测性、调试、模糊/性质/差分测试 | 风险测试、接口隔离、事故复盘、可观测性设计、性质测试、差分测试、插桩、依赖最小化、资源有界循环 | [SWEBOK](https://www.computer.org/education/bodies-of-knowledge/software-engineering)、[ISO 29119](https://committee.iso.org/sites/jtc1sc7/home/projects/flagship-standards/isoiecieee-29119-series.html)、[Python Debugging](https://docs.python.org/3/library/debug.html) |
| 机器学习 | 切分、交叉验证、校准、学习曲线、泄漏控制、泛化 | 主动学习、漂移检测、分布外检查、因果特征消融、置信度升级 | [scikit-learn Model Selection](https://scikit-learn.org/stable/model_selection)、[Validation Curves](https://scikit-learn.org/stable/modules/learning_curve.html)、[Calibration](https://scikit-learn.org/stable/modules/calibration.html) |
| 深度学习 | 迁移、压缩、精度、分布式、检查点、激活/梯度稳定性 | 混合精度、分布式训练、检查点恢复、激活检查点、梯度裁剪 | [PyTorch Tutorials](https://docs.pytorch.org/tutorials/)、[PyTorch Distributed](https://docs.pytorch.org/tutorials/distributed.html)、[OpenAI Scaling Laws](https://openai.com/index/scaling-laws-for-neural-language-models/) |

## 第三波新增领域

| 领域 | 采用的成熟方法 | 可迁移的算子族 | 主要证据 |
| --- | --- | --- | --- |
| 形式逻辑与自动推理 | 形式规约、语法/语义分离、可满足性/反模型、证明状态、可信内核 | 形式问题规约、反模型搜索、子目标分解、内核证据 | [Lean Reference](https://lean-lang.org/doc/reference/latest/)、[SEP Classical Logic](https://plato.stanford.edu/entries/logic-classical/) |
| 科学哲学与认识论 | 观察/解释、最佳解释、辅助假设、欠定性、区分性证据 | 解释比较、辅助假设审计、理论分支、区分性证据设计 | [SEP Scientific Method](https://plato.stanford.edu/entries/scientific-method/)、[SEP Underdetermination](https://plato.stanford.edu/entries/scientific-underdetermination/index.html) |
| 地球科学与地质推理 | 观察位置不确定性、叠覆/切割、地图剖面、物质平衡、地面验证 | 观察不确定性、时间排序、地图/剖面一致性、收支、遥感地面真值 | [USGS Geologic Accuracy](https://pubs.usgs.gov/of/2002/of02-370/soller1.html)、[USGS Relative Time](https://pubs.usgs.gov/gip/geotime/relative.html) |
| 天文学与天体物理 | 观测模型、背景扣除、源检测、统计拟合、校准与独立观测 | 检测/观测分层、背景区分、尺度检查、光谱/光变拟合、独立确认 | [NASA Detection vs Observation](https://ntrs.nasa.gov/api/citations/20080031653/downloads/20080031653.pdf)、[HEASARC XSPEC](https://heasarc.gsfc.nasa.gov/docs/software/xspec/manual/node340.html) |
| 材料科学与工程测量 | 加工—结构—性能、结构计量、微结构、数据评价、资格校准 | 过程映射、计量追溯、微结构表征、数据质量、资格/校准 | [NIST MSED](https://www.nist.gov/mml/materials-science-and-engineering-division)、[NIST Data Evaluation](https://www.nist.gov/publications/data-evaluation-theory-and-practice-materials-properties) |
| 信息与知识组织科学 | 信息需求、共享检索评估、来源血缘、目录/元数据、FAIR | 需求规约、查询扩展、来源审计、精确率/召回率、FAIR 检查 | [NIST TREC](https://trec.nist.gov/about.html)、[W3C DCAT 3](https://www.w3.org/TR/vocab-dcat-3/)、[NIST FAIR](https://www.nist.gov/itl/ssd/information-systems-group/configurable-data-curation-system-cdcs/cdcs-help-and-resources-1) |

## 第四波新增领域

第四波从历史清单继续向“缺什么程序”推进，而不是重复增加领域名：控制论补 Harness 的反馈控制，数值分析补误差/收敛审计，离散组合数学补计数与剪枝，热力学补状态/势/概率视角，有机化学补选择性与机理，分析化学补校准、检测能力和计量不确定度。每个领域仍是 5 个 source + 1 个 derived Method。

| 领域 | 采用的成熟方法 | 可迁移的算子族 | 主要证据 |
| --- | --- | --- | --- |
| 控制论与反馈系统 | 状态空间、可控性/可观测性、反馈、稳定裕度、滚动时域 | 状态建模、覆盖审计、误差修正、稳定边界、滚动重规划 | [MIT State Space](https://ocw.mit.edu/courses/16-30-feedback-control-systems-fall-2010/a2e9eccea56da4ba879a5a3e15cf8cde_MIT16_30F10_lec09.pdf)、[MIT Feedback](https://ocw.mit.edu/courses/6-011-introduction-to-communication-control-and-signal-processing-spring-2010/205766623e6e6edc42f9b6d129f18d30_MIT6_011S10_chap06.pdf) |
| 数值分析与科学计算 | 条件性/稳定性、收敛、误差估计、残差/后向误差、复现 | 条件审计、离散化收敛、自适应误差、残差审计、数值复现 | [NIST Numerical Stability](https://nvlpubs.nist.gov/nistpubs/Legacy/IR/nistir4763.pdf)、[SciPy Cubature](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.cubature.html)、[LAPACK](https://www.netlib.org/lapack/explore-html/d4/d1e/group__gesv__comp__grp.html) |
| 离散组合数学 | 双射、抽屉、容斥、递推/生成函数、极值和概率方法 | 表示变换、碰撞见证、重叠审计、递推缓存、极值界 | [MIT Counting](https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-fall-2010/93cad640cf3ed0b23ef70688f452d4d5_MIT6_042JF10_notes.pdf)、[MIT Probabilistic Combinatorics](https://math.mit.edu/~shor/18.447/)、[Stanford Combinatorics](https://theory.stanford.edu/~jvondrak/MATH108-2016/MATH108.html) |
| 热力学与统计物理 | 状态变量、熵、系综、自由能、平衡和扰动响应 | 系统定义、微观态审计、可行性界、扰动响应、采样诊断 | [MIT Statistical Mechanics](https://live.ocw.mit.edu/courses/8-333-statistical-mechanics-i-statistical-mechanics-of-particles-fall-2013/pages/lecture-notes/)、[MIT Thermodynamics](https://ocw.mit.edu/courses/res-8-010-introduction-to-statistical-physics-summer-2018/mitres_8_010su18_lec4.pdf) |
| 有机化学反应设计 | 化学/区域/立体选择性、保护基、电子箭推、程序复现 | 选择性筛查、路线代价、机理审计、路线组合 | [IUPAC Gold Book](https://goldbook.iupac.org/)、[ACS Mechanisms](https://now.acs.org/public/detail/Documents/organic_reaction_mechanisms_a_practical_guide.pdf)、[Organic Syntheses](https://www.orgsyn.org/instructions.aspx) |
| 分析化学与计量学 | 校准模型、检出限、基质干扰、用途验证、不确定度 | 校准建模、LOD/LOQ审计、选择性检查、方法验证、不确定度预算 | [NIST Calibration](https://www.nist.gov/publications/guidelines-calibration-analytical-chemistry-part-i-fundatmentals-and-single-component)、[IUPAC Metrology](https://iupac.org/recommendation/metrological-and-quality-concepts-in-analytical-chemistry/)、[EURACHEM Fitness](https://www.eurachem.org/images/stories/Guides/pdf/valid.pdf) |

第四波保持 `experimental`、`reference_only`、`harness_policy` 和 `verifier`；有机化学与分析化学条目明确是只读研究/证据审查，不能触发真实实验、采购或放行。

## 第五波：动态科学方法

第五波针对前四波留下的“动态、不确定、连续介质和信号归因”空洞，新增六个领域，每个领域 5 个 source 与 1 个 derived Method：

| 母领域 | 可复用动作 | 新增 pack | 主要功能类 | 关键限制 |
| --- | --- | --- | --- | --- |
| 随机过程与概率过程 | 状态转移、鞅不变量、停止时刻、集中界、耦合比较 | `stochastic-processes-probability` | 控制/元认知 | 概率界不等于单次保证，停止规则不能偷看未来 |
| 微分方程与动力系统 | 适定性、相图、Lyapunov、分岔、敏感性 | `differential-equations-dynamical-systems` | 验证/证伪 | 局部稳定不等于全局稳定，单条轨迹不覆盖状态空间 |
| 经典力学与变分方法 | 变分建模、Euler-Lagrange、对称守恒、Hamilton 状态、扰动 | `classical-mechanics-variational-methods` | 表征 | 形式推导不等于真实预测，边界和耗散不能丢失 |
| 流体与连续介质 | 控制体守恒、无量纲相似、主导平衡、边界适定性、降阶测试 | `fluid-dynamics-continuum-mechanics` | 表征 | 简化只在声明尺度域有效，不提供工程放行 |
| 物理化学与化学动力学 | 速率律、机理假设、速率控制、稳态近似、参数敏感性 | `physical-chemistry-chemical-kinetics` | 验证/证伪 | 拟合不等于机理确证，只读分析不授权化学操作 |
| 电化学与传质 | 电池模型、Nernst、界面动力学、扩散极限、电流/电势交叉检查 | `electrochemistry-mass-transport` | 诊断/修正 | 平衡关系不能直接用于极化状态，不驱动设备 |

第五波的来源事实来自 MIT、IUPAC 和 NIST：MIT 随机过程课程覆盖 Markov/鞅/停止时刻/集中不等式；MIT 动力系统课程覆盖适定性、相图、稳定性和分岔；MIT 经典力学和流体课程覆盖变分、守恒、尺度和边界；MIT 化学动力学、IUPAC Gold Book 与 NIST 数据库覆盖速率律、稳态、速率控制和参数溯源；IUPAC Nernst/Cottrell 与 MIT Butler–Volmer 覆盖平衡、界面动力学和扩散响应。详细来源、缺口与反向核验见 [`DOMAIN_EVIDENCE_MATRIX.md`](DOMAIN_EVIDENCE_MATRIX.md)。

这些新增条目仍保持 `experimental`、`reference_only`、`harness_policy` 和 `verifier`。第五波的迁移推断是项目设计，不是来源文献对 Agent 效果的承诺；尤其化学和电化学内容只生成可审查的假设、边界和证据清单。

## 第六波：结构、场、算子与多证据方法

第六波在 50 个既有领域和 396 个条目上先做去重，随后补入六条独立方法链：

| 母领域 | 可复用动作 | 新增 pack | 关键限制 |
| --- | --- | --- | --- |
| 线性代数与谱方法 | 可解性、基选择、投影、谱模式、低秩残差 | `linear-algebra-spectral-methods` | 数值可解和小残差不证明模型语义正确 |
| 拓扑与几何 | 连续性、连通分支、有限见证、同伦不变量、局部整体障碍 | `topology-geometry` | 拓扑抽象不保留全部度量，相同不变量不一定充分 |
| 电磁学与场方法 | 源场边界、对称面、叠加、势边值、能流收支 | `electromagnetism-field-methods` | 对称、线性、边界和尺度必须先固定 |
| 量子力学与算子方法 | 状态/可观测量、对易性、基适配、受界近似、概率归一 | `quantum-mechanics-operator-methods` | 一般 Agent 中只作明确标记的结构类比 |
| 溶液热力学与相平衡 | 相律、化学势、非理想性、相稳定、Gibbs-Duhem | `solution-thermodynamics-phase-equilibria` | 平衡不等于动力学可达，参数不能脱离状态域 |
| 光谱学与结构解析 | 分子式约束、正交证据、片段连接、全谱一致性、参考条件 | `spectroscopy-structure-elucidation` | 数据库匹配不等于身份，非唯一候选必须保留 |

每个领域落成 5 个 source 和 1 个 derived Method；详细权威来源、与旧条目的 crosswalk 和停止理由见 [`DOMAIN_EVIDENCE_MATRIX.md`](DOMAIN_EVIDENCE_MATRIX.md)。全部条目仍是 `experimental` / `reference_only`，没有增加现实执行权限。

## 数学专项：从“数学领域”下钻到 55 个求解动作

本轮没有新增 pack，而是审计用户明确列出的 55 个数学方法：20 项复用当前跨领域条目，35 项补入 `mathematics`，再增加 1 个 derived 数学发现与证明循环。八个数学过程组是研究视图，库内仍统一映射到既有八类 `functional_class`。逐项决策、权威来源和证据边界见 [`MATHEMATICAL_PROBLEM_SOLVING_RESEARCH.md`](MATHEMATICAL_PROBLEM_SOLVING_RESEARCH.md)。

## 重点领域的迁移解释

### 数学：把“会推理”变成可反驳的约束

数学条目不是要求 Agent 输出形式证明，而是强制它先定义对象和假设，再给推导、界、反例或不确定性。新增条目覆盖四个缺口：

- `optimization-relaxation`：精确求解太贵时先放松，但必须保留硬约束、界和恢复检查。
- `sensitivity-analysis`、`limit-case-analysis`、`error-bound`：区分稳定结论、边界失效和最坏误差。
- `bayesian-update`、`hypothesis-test`：看到新证据要更新假设；“不拒绝”不能写成“证明没有效应”。
- `linear-algebra-factorization`、`normalization-and-scaling`：用结构分解和尺度控制减少冗余、病态和比较偏差。

### 物理学：先检查不变量和数量级，再信模型

物理学给 Harness 的核心不是某个公式，而是一组低成本的模型 sanity checks：量纲不对先停；守恒不成立先查边界；极限/数量级不合理先回到假设；摄动只在小参数范围内使用；残差和不确定度必须伴随结果。新增 `physics` pack 用十个 source 条目覆盖这些检查，并以 `model-validation-loop` 组合为“建模—检查—扰动—校准”的可复用路径。

### 化学：平衡、机理和安全边界必须同时存在

化学算子把“能算出一个反应式”拆成物料、电荷、电子、平衡和动力学多层约束；`mechanism-hypothesis`、`spectroscopy-assignment` 和 `retrosynthetic-disconnection` 只产生可审查假设，不代表实验批准。`green-chemistry-screen` 用 ACS 原则检查溶剂、废物、能耗和危害。`safe-synthesis-loop` 明确是**参考/设计审查**，不自动执行合成、采购、放大或危险实验；任何真实化学操作必须由具备资质的流程和独立安全审查接管。

## 库面变化（历史阶段快照）

| 指标 | 上一历史阶段 | 当前快照 |
| --- | ---: | ---: |
| source 条目 | 196 | 226 |
| derived Method | 20 | 26 |
| 总条目 | 216 | 252 |
| domain pack | 20 | 26 |
| reference framework | 63 | 87 |

上表保留前两阶段的历史快照。当前新增 pack 包括第二轮六个社会/人文领域和第三波六个形式/自然/信息领域；三轮均用证据矩阵补充来源、迁移边界和停止理由，详见 [`DOMAIN_EVIDENCE_MATRIX.md`](DOMAIN_EVIDENCE_MATRIX.md)。

第二轮快照：256 个 source、32 个 derived Method、288 个总条目、32 个 domain pack、117 个 reference framework；机器校验摘要为 `source_coverage=256/256 derived_methods=32/32 total=288`。

第三波快照：286 个 source、38 个 derived Method、324 个总条目、38 个 domain pack、155 个 reference framework；机器校验摘要为 `source_coverage=286/286 derived_methods=38/38 total=324`。

第四波快照：316 个 source、44 个 derived Method、360 个总条目、44 个 domain pack、190 个 reference framework；机器校验摘要为 `source_coverage=316/316 derived_methods=44/44 total=360`。

第五波快照：346 个 source、50 个 derived Method、396 个总条目、50 个 domain pack、202 个 reference framework；机器校验摘要为 `source_coverage=346/346 derived_methods=50/50 total=396`。

第六波历史快照：376 个 source、56 个 derived Method、432 个总条目、56 个 domain pack、214 个 reference framework；机器校验摘要为 `source_coverage=376/376 derived_methods=56/56 total=432`。

数学专项当前快照：411 个 source、57 个 derived Method、468 个总条目、56 个 domain pack、216 个 reference framework；机器校验摘要为 `source_coverage=411/411 derived_methods=57/57 total=468`。

## 证据分级与未知项

1. **文献事实**：上表链接直接支持某一成熟方法或标准的存在与基本目的。
2. **本项目迁移**：把方法改写成 Agent 可读的前提、步骤和证据，是本项目设计推断，不是原文声称。
3. **尚未验证**：条目是否提升真实任务成功率、是否被选择器正确路由、预算是否合理、不同模型是否稳定，均需未来 Binding/eval 证明。

当前不声称：任何条目已经生产验证；任何数学/物理/化学条目可以代替专家；任何 `source_refs` 都等同于完整教材；任何模型自报置信度都是真实概率。

## 对 Harness 的实现含义

- **检索层**：按 domain、kind、适用条件、风险和目标检索，不把 468 条全塞进上下文。
- **规划层**：`MethodSpec` 是组合提示和证据要求，不是权限授权；运行时仍需 planner/selector。
- **执行层**：`OperatorSpec` 的 procedure 由具体 Harness adapter 映射到只读检查、工具调用或人工步骤；默认不自动执行高风险动作。
- **验证层**：每个动作都要生成与 `evidence_required` 对应的 artifact，并由外部 verifier 裁决 outcome。
- **治理层**：保持 inventory、catalog、pack 三方精确一致；新增条目优先补来源、负例和评估，再考虑晋升状态。

## 停止条件与后续研究

本报告的领域扩展已在“每个候选有权威来源、可执行程序、组合方法、重复审计和明确边界”处停止；数学专项又完成 55 项逐一闭合。下一步优先转向真实消费方或评估缺口，补 Binding、selector/planner 和留出评估，而不是继续堆来源数量。

后续晋升所需证据：固定任务集、baseline、正负例、重复运行、成本/延迟预算、独立 verifier、失败恢复和跨模型稳定性。没有这些证据，新增内容应保持 `experimental`，不能写成“已具备能力”。
