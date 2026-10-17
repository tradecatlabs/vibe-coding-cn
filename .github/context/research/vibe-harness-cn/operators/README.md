# 问题求解算子库

`operators/` 保存 Harness 可装载的问题求解内容。它把用户提供的跨领域思维模型与方法论拆成
`MentalModelSpec`、`OperatorSpec` 和 `MethodSpec`，并用独立清单证明没有漏项。

```text
operators/
├── AGENTS.md                  # 模块职责、依赖和维护规则
├── README.md                  # 人类入口与使用方式
├── catalog.json               # Reference Library Profile、pack 路径、计数和全库不变量
├── source-inventory.json      # 411 个原始条目的独立完整性基线
├── taxonomy/                  # 母领域来源与八类功能的双轴分类视图
└── packs/
    ├── research.json          # 科研方法：7 个原始条目 + 1 个组合方法
    ├── computer-science.json  # 计算机科学：15 + 1
    ├── mathematics.json       # 数学：55 + 2
    ├── software-engineering.json # 软件工程：16 + 1
    ├── programming.json       # 编程：17 + 1
    ├── machine-learning.json  # 机器学习：17 + 1
    ├── deep-learning.json     # 深度学习：19 + 1
    ├── scientific-methodology.json # 科学方法论：6 + 1
    ├── systems-science.json   # 系统科学：7 + 1
    ├── complexity-science.json # 复杂性科学：8 + 1
    ├── algorithms.json        # 算法：6 + 1
    ├── information-theory.json # 信息论：5 + 1
    ├── physics.json           # 物理学：10 + 1
    ├── chemistry.json         # 化学：10 + 1
    ├── problem-solving-methodology.json # 通用问题求解：8 + 1
    ├── statistics.json        # 统计学：5 + 1
    ├── decision-science.json  # 决策科学：5 + 1
    ├── operations-research.json # 运筹学：5 + 1
    ├── design-methods.json    # 设计方法：5 + 1
    ├── engineering.json       # 工程学：5 + 1
    ├── causal-inference.json  # 因果推断：5 + 1
    ├── economics-game-theory.json # 经济学/博弈论：5 + 1
    ├── ecology-biology.json   # 生态/生物学：5 + 1
    ├── cognitive-science.json # 认知科学：5 + 1
    ├── human-factors-reliability.json # 人因与可靠性：5 + 1
    ├── medical-decision.json  # 医学决策：5 + 1
    ├── legal-reasoning.json   # 法律推理：5 + 1
    ├── ethics-public-policy.json # 伦理与公共政策：5 + 1
    ├── education-learning-science.json # 教育与学习科学：5 + 1
    ├── linguistics.json       # 语言学：5 + 1
    ├── historical-reasoning.json # 历史推理：5 + 1
    ├── social-science-methods.json # 社会科学方法：5 + 1
    ├── formal-logic-automated-reasoning.json # 形式逻辑与自动推理：5 + 1
    ├── philosophy-science-epistemology.json # 哲学、科学与认识论：5 + 1
    ├── earth-science-geoscience.json # 地球科学与地学：5 + 1
    ├── astronomy-astrophysics.json # 天文学与天体物理：5 + 1
    ├── materials-science.json # 材料科学：5 + 1
    ├── information-knowledge-science.json # 信息与知识科学：5 + 1
    ├── control-theory-cybernetics.json # 控制论与反馈系统：5 + 1
    ├── numerical-analysis-scientific-computing.json # 数值分析与科学计算：5 + 1
    ├── discrete-combinatorics.json # 离散组合数学：5 + 1
    ├── thermodynamics-statistical-mechanics.json # 热力学与统计物理：5 + 1
    ├── organic-chemistry-reaction-design.json # 有机化学反应设计：5 + 1
    ├── analytical-chemistry-metrology.json # 分析化学与计量学：5 + 1
    ├── stochastic-processes-probability.json # 随机过程与概率过程：5 + 1
    ├── differential-equations-dynamical-systems.json # 微分方程与动力系统：5 + 1
    ├── classical-mechanics-variational-methods.json # 经典力学与变分方法：5 + 1
    ├── fluid-dynamics-continuum-mechanics.json # 流体与连续介质：5 + 1
    ├── physical-chemistry-chemical-kinetics.json # 物理化学与化学动力学：5 + 1
    ├── electrochemistry-mass-transport.json # 电化学与传质：5 + 1
    ├── linear-algebra-spectral-methods.json # 线性代数与谱方法：5 + 1
    ├── topology-geometry.json # 拓扑与几何方法：5 + 1
    ├── electromagnetism-field-methods.json # 电磁学与场方法：5 + 1
    ├── quantum-mechanics-operator-methods.json # 量子力学与算子方法：5 + 1
    ├── solution-thermodynamics-phase-equilibria.json # 溶液热力学与相平衡：5 + 1
    └── spectroscopy-structure-elucidation.json # 光谱学与结构解析：5 + 1
```

分类视图另存于 [`taxonomy/problem-solving-methodology.json`](taxonomy/problem-solving-methodology.json)：
它把“方法来自哪个母领域”和“算子在问题求解中承担什么功能”分成两条轴，避免把出处当能力。

当前库共 468 个条目：411 个来自用户给出的扩展清单，57 个是本项目显式标记为 `derived` 的领域组合
方法。来源领域用于组织首版内容和证明覆盖；未来运行时应按问题、适用性、风险和证据需求选择条目，
不能把整库默认塞入模型上下文。

## 类型

- `MentalModelSpec`：提供观察和解释问题的视角，不声明现实世界副作用。
- `OperatorSpec`：描述一次问题求解动作、前置条件、步骤、状态效果、证据、失败和恢复。
- `MethodSpec`：按有序步骤组合指令或已存在条目，并声明停止、成功、证据与失败条件。

所有条目当前均为 `experimental`。它们是可机检的方法内容，不是已经在生产环境验证有效的声明，
也不授予模型任何权限；权限由具体 Harness policy 决定，结果由 Verifier 裁决。

本目录采用 `vibe-harness-cn/reference-library-v1` Profile，所以继续强制内容字段、411/411 来源覆盖、
57/57 派生方法、引用和计数。该 Profile 是本仓库参考库的发布规则；第三方 pack 只需满足
[`Operator Pack Core Contract`](../docs/OPERATOR_SPEC.md)，可在 `draft` 阶段渐进补全内容。

## 验证

```bash
uv run --locked --script scripts/validate_harness.py --operator-library operators/catalog.json
uv run --locked --script scripts/validate_harness.py --self-test
```

第一条命令检查 Schema、精确覆盖、ID、计数、来源和 Method 引用；第二条还运行 Harness manifest
回归、Core 宽松正例与 Profile 负例。完整库的当前期望摘要是
`source_coverage=411/411 derived_methods=57/57 total=468`。

## 当前边界

本目录不包含 selector、planner、模型调用、tool binding、权限执行、在线 registry、数据库或 UI。
具体 Harness 负责装载本地库存并实现 Binding；Vibe Harness CN 负责共享内容和契约的治理。
