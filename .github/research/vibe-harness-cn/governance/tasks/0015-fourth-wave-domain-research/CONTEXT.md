# Repo Evidence
- 本轮开始时 operators/catalog.json 登记 38 个 pack、286 个 source 和 38 个 derived；当前登记 44 个 pack、316 个 source 和 44 个 derived
- operators/source-inventory.json 是独立完整性基线
- operators/taxonomy/problem-solving-methodology.json 已定义八类功能
- research/DOMAIN_EVIDENCE_MATRIX.md 已记录前四轮来源、缺口和停止理由，实际来源引用当前为 190 条

# Constraints Matrix
- 只读公开资料和项目文件，不执行上游代码、模型训练或现实操作
- 高风险化学与计量内容只作 reference-only，权限归 Harness policy，结果归 verifier
- 不修改 upstream registry、lock 或 checkout
- 不读取凭据，不执行破坏性 Git 操作

# Change Boundary
- operators/packs/、operators/source-inventory.json、operators/catalog.json、operators/taxonomy/
- research/、docs/、README.md、AGENTS.md
- governance/tasks/0015-fourth-wave-domain-research/ 与相关 module context
- 不修改 research/upstreams.sources.json、research/upstreams.lock.json 或上游 checkout

# Risk Matrix
- 控制反馈可能被误读为稳定保证
- 数值残差可能被误读为真实准确
- 组合搜索未找到不等于不存在
- 热力学可行不等于动力学必然
- 化学路线与计量结果不能替代专业复核
- 不把反馈改善写成稳定保证
- 不把小残差写成高精度保证
- 不把搜索未找到写成不存在
- 不把热力学可行写成动力学必然
- 不提供合成、采购或危险实验授权
- 不把检出限或相关性写成方法充分性

# Assumptions and Falsification
- 继续使用母领域来源轴与八类功能轴
- 每个领域先做来源与重复审计再入库
- 新增条目只改变静态参考库，不增加运行时执行能力

# Critical Ambiguities
- 当前未记录会改变实现路径的关键歧义；若发现此类歧义，必须暂停并回到需求澄清

# Debug Evidence Contract
- 调试模式: Optional
- 回归证据契约: Optional
- 若任务属于 bugfix / regression / flaky / crash / CI-only failure，必须切到 `Required`
- 调试模式为 `Required` 时必须在当前任务目录创建并维护 `DEBUG.md`
- 回归证据契约为 `Required` 时，closeout 必须由 `auto-debug` 校验 `REGRESSION_EVIDENCE.json` 的 RED/GREEN/反事实证据

# Task Package Context Map
## TP-01
- Step Key: `research-evidence`
- 标题: 六个新增母领域深度抓取证据
- 类型: `package`
- 目标: 为控制论、数值分析、离散组合数学、热力学/统计物理、有机化学和分析化学建立权威来源、方法程序、迁移边界和未验证项
- 父节点: `ROOT`
- 子节点: TP-01.01, TP-01.02, TP-01.03, TP-01.04, TP-01.05, TP-01.06
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: research/HEURISTIC_METACOGNITIVE_RESEARCH.md；research/DOMAIN_EVIDENCE_MATRIX.md
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-01.01
- Step Key: `research-control`
- 标题: 控制论与反馈系统研究
- 类型: `action`
- 目标: 研究状态空间、可控/可观测、反馈、稳定裕度和滚动重规划
- 父节点: `TP-01`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: research/DOMAIN_EVIDENCE_MATRIX.md
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 不把反馈改善写成稳定保证
- 备注: 无

### TP-01.02
- Step Key: `research-numerical`
- 标题: 数值分析与科学计算研究
- 类型: `action`
- 目标: 研究条件性/稳定性、收敛、误差控制、残差和复现
- 父节点: `TP-01`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: research/DOMAIN_EVIDENCE_MATRIX.md
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 不把小残差写成高精度保证
- 备注: 无

### TP-01.03
- Step Key: `research-combinatorics`
- 标题: 离散组合数学研究
- 类型: `action`
- 目标: 研究双射、抽屉、容斥、递推/生成函数和极值界
- 父节点: `TP-01`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: research/DOMAIN_EVIDENCE_MATRIX.md
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 不把搜索未找到写成不存在
- 备注: 无

### TP-01.04
- Step Key: `research-thermodynamics`
- 标题: 热力学与统计物理研究
- 类型: `action`
- 目标: 研究系统边界、熵、自由能、扰动响应和系综采样
- 父节点: `TP-01`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: research/DOMAIN_EVIDENCE_MATRIX.md
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 不把热力学可行写成动力学必然
- 备注: 无

### TP-01.05
- Step Key: `research-organic`
- 标题: 有机化学反应设计研究
- 类型: `action`
- 目标: 研究化学/区域/立体选择性、保护基代价、机理和复现审查
- 父节点: `TP-01`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: research/DOMAIN_EVIDENCE_MATRIX.md
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 不提供合成、采购或危险实验授权
- 备注: 无

### TP-01.06
- Step Key: `research-analytical`
- 标题: 分析化学与计量学研究
- 类型: `action`
- 目标: 研究校准、检出限、基质干扰、方法验证和不确定度
- 父节点: `TP-01`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: research/DOMAIN_EVIDENCE_MATRIX.md
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 不把检出限或相关性写成方法充分性
- 备注: 无

## TP-02
- Step Key: `gap-audit`
- 标题: 既有库缺口与重复审计
- 类型: `action`
- 目标: 将六个领域方法与当前 286 条目逐项比对，确定新增语义和交叉映射
- 父节点: `ROOT`
- 子节点: 无
- 依赖步骤 Key: research-evidence
- 依赖节点 ID: TP-01
- 输入: research/DOMAIN_EVIDENCE_MATRIX.md；operators/source-inventory.json；operators/catalog.json
- 输出: research/DOMAIN_EVIDENCE_MATRIX.md；operators/taxonomy/problem-solving-methodology.json
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

## TP-03
- Step Key: `define-operators`
- 标题: 提炼新增算子与组合 Method
- 类型: `action`
- 目标: 把独立语义写成五个 source 与一个 derived Method，保留前提、步骤、证据、失败和恢复
- 父节点: `ROOT`
- 子节点: 无
- 依赖步骤 Key: gap-audit
- 依赖节点 ID: TP-02
- 输入: research/DOMAIN_EVIDENCE_MATRIX.md；docs/OPERATOR_SPEC.md
- 输出: operators/packs/；operators/source-inventory.json；operators/catalog.json；operators/taxonomy/problem-solving-methodology.json
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

## TP-04
- Step Key: `materialize-library`
- 标题: 入库并同步目录文档
- 类型: `action`
- 目标: 同步 pack、inventory、catalog、taxonomy、研究报告、README、AGENTS、module context 和任务证据
- 父节点: `ROOT`
- 子节点: 无
- 依赖步骤 Key: define-operators
- 依赖节点 ID: TP-03
- 输入: operators/；research/；docs/
- 输出: operators/；research/；docs/；governance/；README.md；AGENTS.md
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

## TP-05
- Step Key: `verify-review-ship`
- 标题: 验证、审查与交付收口
- 类型: `action`
- 目标: 运行全量库、Core、自测、项目门禁、治理校验和任务级证据检查
- 父节点: `ROOT`
- 子节点: 无
- 依赖步骤 Key: materialize-library
- 依赖节点 ID: TP-04
- 输入: 无
- 输出: governance/tasks/0015-fourth-wave-domain-research/REVIEW.md；governance/tasks/0015-fourth-wave-domain-research/VERIFICATION_PLAN.json
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无
