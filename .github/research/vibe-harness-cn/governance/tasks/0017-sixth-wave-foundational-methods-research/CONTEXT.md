# Repo Evidence
- operators/catalog.json 当前登记 50 个 pack、346 个 source 和 50 个 derived
- operators/source-inventory.json 是独立完整性基线
- operators/taxonomy/problem-solving-methodology.json 已定义八类功能
- research/DOMAIN_EVIDENCE_MATRIX.md 已记录前五轮来源、缺口和停止理由

# Constraints Matrix
- 只读公开资料和项目文件，不执行上游代码、模型训练或现实操作
- 物理与化学内容只作 reference-only，权限归 Harness policy，结果归 verifier
- 不修改 upstream registry、lock 或 checkout
- 不读取凭据，不执行破坏性 Git 操作

# Change Boundary
- operators/packs/、operators/source-inventory.json、operators/catalog.json、operators/taxonomy/
- research/、docs/、README.md、AGENTS.md
- governance/tasks/0017-sixth-wave-foundational-methods-research/ 与相关 module context
- 不修改 research/upstreams.sources.json、research/upstreams.lock.json 或上游 checkout

# Risk Matrix
- 线性结构依赖模型和数据质量，分解不能替代业务验证
- 拓扑不变量只保留其定义范围内的信息
- 场与量子模型依赖边界、尺度和近似条件
- 热力学平衡不等于动力学可达
- 光谱归属可能非唯一且依赖样品和采集条件
- 不把低秩近似当成语义正确性保证
- 不把拓扑等价当成所有性质等价
- 不提供现实高能电磁系统操作建议
- 不把形式推导当成实验验证
- 不把热力学可行等同于动力学可达
- 不把非唯一谱归属写成确定结论

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
- 标题: 六个基础领域深度抓取证据
- 类型: `package`
- 目标: 为线性代数谱方法、拓扑几何、电磁场方法、量子算子方法、溶液热力学相平衡和光谱结构解析建立权威来源、方法程序、迁移边界和未验证项
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
- Step Key: `research-linear-algebra`
- 标题: 线性代数与谱方法研究
- 类型: `action`
- 目标: 研究秩与零空间、基选择、正交投影、谱分解和低秩残差
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
- 风险: 不把低秩近似当成语义正确性保证
- 备注: 无

### TP-01.02
- Step Key: `research-topology`
- 标题: 拓扑与几何研究
- 类型: `action`
- 目标: 研究连续性、连通性、紧致性、同伦不变量和局部到整体障碍
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
- 风险: 不把拓扑等价当成所有性质等价
- 备注: 无

### TP-01.03
- Step Key: `research-electromagnetism`
- 标题: 电磁场方法研究
- 类型: `action`
- 目标: 研究源场建模、对称面、叠加、势与边值问题和能流守恒
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
- 风险: 不提供现实高能电磁系统操作建议
- 备注: 无

### TP-01.04
- Step Key: `research-quantum`
- 标题: 量子算子方法研究
- 类型: `action`
- 目标: 研究状态与可观测量、对易性、基表示、变分与微扰近似及概率归一
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
- 风险: 不把形式推导当成实验验证
- 备注: 无

### TP-01.05
- Step Key: `research-phase-equilibria`
- 标题: 溶液热力学与相平衡研究
- 类型: `action`
- 目标: 研究相律、化学势、活度逸度、相稳定和 Gibbs-Duhem 一致性
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
- 风险: 不把热力学可行等同于动力学可达
- 备注: 无

### TP-01.06
- Step Key: `research-spectroscopy`
- 标题: 光谱结构解析研究
- 类型: `action`
- 目标: 研究分子式约束、正交谱特征、片段连接、全证据一致性和参考条件审计
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
- 风险: 不把非唯一谱归属写成确定结论
- 备注: 无

## TP-02
- Step Key: `gap-audit`
- 标题: 既有库缺口与重复审计
- 类型: `action`
- 目标: 将六个领域方法与当前 396 个条目逐项比对，确定新增语义和交叉映射
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
- 输出: governance/tasks/0017-sixth-wave-foundational-methods-research/REVIEW.md；governance/tasks/0017-sixth-wave-foundational-methods-research/VERIFICATION_PLAN.json
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无
