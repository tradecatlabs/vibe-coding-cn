# research 目录

`research/` 保存上游 Harness 的来源清单、精确 revision 与源码级比较材料；上游 checkout
本身位于忽略目录，不复制进本项目历史。

```text
research/
├── AGENTS.md                # 本目录职责与依赖边界
├── UPSTREAMS.md             # 官方仓库的研究范围、可见性结论与使用约束
├── HARNESS_RESEARCH.md      # 逐仓源码级研究档案（revision 绑定，随 lock 失效）
├── EXPANDED_OPERATOR_RESEARCH.md # 跨学科方法抽取、证据矩阵与算子扩展边界
├── HEURISTIC_METACOGNITIVE_RESEARCH.md # 八类功能与母领域双轴的深度方法论研究
├── DOMAIN_EVIDENCE_MATRIX.md # 三十六个新增母领域的来源、缺口、迁移和证伪边界
├── MATHEMATICAL_PROBLEM_SOLVING_RESEARCH.md # 55 个数学方法的证据、去重与算子 crosswalk
├── upstreams.sources.json   # 同步与 lock 共同消费的官方来源登记
├── upstreams.lock.json      # 官方 GitHub URL、默认分支、commit 与源码可见性
└── upstreams/               # 被忽略的 15 个官方 Harness 浅克隆
```

依赖方向：`upstreams.sources.json` 定义允许同步的官方来源，`scripts/sync_upstreams.sh` 从 GitHub
同步 checkout 并生成 lock；研究文档只消费 registry、lock 和本地 checkout，不修改上游。
`HARNESS_RESEARCH.md` 是逐仓结论真相源，必须绑定 `upstreams.lock.json` 的 revision 与
`upstreams/<name>/` 相对路径；lock revision 变化后旧结论自动失效。
`EXPANDED_OPERATOR_RESEARCH.md` 是跨学科 Operator 内容的研究与来源矩阵；它描述来源事实、迁移推断和
尚未验证项，不授予任何运行时权限，也不替代 `operators/` 的机器清单。
`HEURISTIC_METACOGNITIVE_RESEARCH.md` 是上位问题求解方法论的研究真相源，按 Representation、Decomposition、
Transformation、Search、Construction、Verification/Falsification、Diagnosis/Revision、Control/Metacognition
八类功能组织用户列出的母领域；它明确区分来源事实、项目迁移推断和未验证项。
`DOMAIN_EVIDENCE_MATRIX.md` 是新增因果推断、经济学/博弈论、生态/生物学、认知科学、人因可靠性、医学决策、法律推理、伦理与公共政策、教育与学习科学、语言学、历史推理、社会科学方法、形式逻辑、科学认识论、地球科学、天文学、材料科学、信息知识科学、控制论、数值分析、离散组合数学、热力学/统计物理、有机化学、分析化学、随机过程、微分方程与动力系统、经典力学、流体与连续介质、化学动力学、电化学、线性代数谱方法、拓扑几何、电磁场、量子算子、溶液相平衡和光谱结构解析的证据缺口与反向证伪矩阵；它不授予现实操作权限，也不替代专业审查。
`MATHEMATICAL_PROBLEM_SOLVING_RESEARCH.md` 是数学专项研究真相源，逐项记录用户点名 55 个方法的 `reuse/add` 决策、目标 ID、过程分组、功能主类、证据等级和未验证项；它不复制 pack 语义，也不把项目八分法冒充外部官方分类。
不得把第三方 fork、教程仓库或本机安装目录冒充官方源码。
若官方仓库只公开插件、文档或分发资产，必须在 lock 中如实标记，不得推断未公开实现。

存在性：15 个官方来源必须由一份机器登记驱动；最低阶梯仍是静态 JSON + Python 标准库，
验证入口为 `bash tests/test_sync_upstreams.sh`。当前保留串行 fail-fast；只有重复测量证明同步延迟
超过明确预算，才升级为受限并发，不能用无界后台任务换取表面速度。
