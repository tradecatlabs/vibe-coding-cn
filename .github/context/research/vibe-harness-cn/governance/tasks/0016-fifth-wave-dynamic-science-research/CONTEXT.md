# Repo Evidence
- operators/catalog.json 当前登记 50 个 pack、346 个 source 和 50 个 derived
- operators/source-inventory.json 是独立完整性基线
- operators/taxonomy/problem-solving-methodology.json 已定义八类功能
- research/DOMAIN_EVIDENCE_MATRIX.md 已记录前五轮来源、缺口和停止理由

# Constraints Matrix
- 只读公开资料和项目文件，不执行上游代码、模型训练或现实操作
- 化学动力学与电化学内容只作 reference-only，权限归 Harness policy，结果归 verifier
- 不修改 upstream registry、lock 或 checkout
- 不读取凭据，不执行破坏性 Git 操作

# Change Boundary
- operators/packs/、operators/source-inventory.json、operators/catalog.json、operators/taxonomy/
- research/、docs/、README.md、AGENTS.md
- governance/tasks/0016-fifth-wave-dynamic-science-research/ 与相关 module context
- 不修改 research/upstreams.sources.json、research/upstreams.lock.json 或上游 checkout

# Risk Matrix
- 随机过程的概率界不等于单次结果保证
- 动力系统稳定性依赖模型和参数，不能从局部线性化外推全局
- 变分或守恒形式不等于数值解正确
- 流体尺度分析需要边界与无量纲假设
- 热力学可行不等于动力学必然
- 电化学信号可能受动力学、传质和干扰共同影响
- 不把概率界写成单次保证
- 不把局部稳定外推成全局保证
- 不把形式模型当成真实系统验证
- 不提供现实流体或工程放行意见
- 不提供合成、投料或危险实验授权
- 不提供电化学装置、参数或专业放行

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
- 标题: 六个动态科学领域深度抓取证据
- 类型: `package`
- 目标: 为随机过程、微分方程与动力系统、经典力学、流体与连续介质、化学动力学和电化学建立权威来源、方法程序、迁移边界和未验证项
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
- Step Key: `research-stochastic`
- 标题: 随机过程与概率过程研究
- 类型: `action`
- 目标: 研究状态转移、条件期望/鞅、停止时刻、集中界和耦合对问题求解的启发
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
- 风险: 不把概率界写成单次保证
- 备注: 无

### TP-01.02
- Step Key: `research-dynamical`
- 标题: 微分方程与动力系统研究
- 类型: `action`
- 目标: 研究适定性、初边值条件、相图、Lyapunov 稳定和分岔敏感性
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
- 风险: 不把局部稳定外推成全局保证
- 备注: 无

### TP-01.03
- Step Key: `research-mechanics`
- 标题: 经典力学与变分方法研究
- 类型: `action`
- 目标: 研究作用量、Euler-Lagrange、对称守恒、Hamilton 状态空间和扰动分析
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
- 风险: 不把形式模型当成真实系统验证
- 备注: 无

### TP-01.04
- Step Key: `research-fluids`
- 标题: 流体与连续介质研究
- 类型: `action`
- 目标: 研究控制体守恒、无量纲相似、主导平衡、边界条件和降阶模型验证
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
- 风险: 不提供现实流体或工程放行意见
- 备注: 无

### TP-01.05
- Step Key: `research-kinetics`
- 标题: 化学动力学研究
- 类型: `action`
- 目标: 研究速率律、机理候选、速率控制、稳态近似和参数敏感性
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
- 风险: 不提供合成、投料或危险实验授权
- 备注: 无

### TP-01.06
- Step Key: `research-electrochemistry`
- 标题: 电化学与传质研究
- 类型: `action`
- 目标: 研究平衡电势、Nernst、界面动力学、扩散限制和测量交叉检查
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
- 风险: 不提供电化学装置、参数或专业放行
- 备注: 无

## TP-02
- Step Key: `gap-audit`
- 标题: 既有库缺口与重复审计
- 类型: `action`
- 目标: 将六个领域方法与本轮开始的 316 条目逐项比对，确定新增语义和交叉映射
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
- 目标: 运行全量库、自测、项目门禁、治理校验和任务级证据检查
- 父节点: `ROOT`
- 子节点: 无
- 依赖步骤 Key: materialize-library
- 依赖节点 ID: TP-04
- 输入: 无
- 输出: governance/tasks/0016-fifth-wave-dynamic-science-research/REVIEW.md；governance/tasks/0016-fifth-wave-dynamic-science-research/VERIFICATION_PLAN.json
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无
