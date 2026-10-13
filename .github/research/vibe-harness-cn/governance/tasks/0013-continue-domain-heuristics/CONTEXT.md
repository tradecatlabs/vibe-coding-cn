# Repo Evidence
- operators/catalog.json 当前登记 32 个 pack、256 个 source 和 32 个 derived
- operators/source-inventory.json 是当前跨学科 256 条 source 的完整性基线
- operators/taxonomy/problem-solving-methodology.json 已定义母领域与八类功能双轴
- research/DOMAIN_EVIDENCE_MATRIX.md 已记录第二轮六个领域的来源、迁移边界和停止理由
- 公共 Core/Profile 校验入口与治理 strict/health 已存在

# Constraints Matrix
- 只读公开资料和项目文件，不执行上游代码、模型训练或现实操作
- 新增内容只进入 operators、research、docs、governance、README/AGENTS 的明确范围
- 高影响领域只作 reference-only 方法说明，现实操作由具体 Harness policy 与独立审查接管
- 保持现有 source/derived 条目、Core 宽松边界和回滚路径

# Change Boundary
- operators/packs/、operators/source-inventory.json、operators/catalog.json、operators/taxonomy/
- research/HEURISTIC_METACOGNITIVE_RESEARCH.md、research/DOMAIN_EVIDENCE_MATRIX.md、research/AGENTS.md
- docs/、README.md、AGENTS.md、治理上下文/ADR/任务包
- 不修改 research/upstreams.sources.json、research/upstreams.lock.json 或上游 checkout

# Risk Matrix
- 法律与伦理术语可能被误读为专业授权或事实结论
- 教育、语言、历史和社会科学方法容易受语境、样本和解释框架影响
- 来源数量增长会增加索引、引用和文档漂移维护成本
- 来源成熟不等于迁移到 Agent 后真实有效
- 不得把参考方法写成法域意见或法律授权
- 不得替代伦理审查、法律判断或责任主体

# Assumptions and Falsification
- 继续使用母领域来源轴与八类功能轴，不把新增领域直接写入公共 Core
- 每个领域先建立证据矩阵，只有存在清晰问题求解程序才进入 pack
- 若候选与既有条目重复或无法写出证据/失败契约，则记录 gap/crosswalk 而不强行新增

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
- 标题: 六个新增母领域分别深度抓取证据
- 类型: `documentation`
- 目标: 为六个候选领域建立一手来源、反复使用的方法程序、可迁移问题、证据边界和未验证项，并映射到八类功能
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
- Step Key: `research-legal-reasoning`
- 标题: 法律推理研究
- 类型: `documentation`
- 目标: 研究争点识别、权威层级、先例类比/区分、证明标准和规则—事实适用如何支持受限结论
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
- 风险: 不得把参考方法写成法域意见或法律授权
- 备注: 无

### TP-01.02
- Step Key: `research-ethics-public-policy`
- 标题: 伦理与公共政策研究
- 类型: `documentation`
- 目标: 研究利益相关者、比例与不伤害、权利公平、影响评估、监督和责任分配中的问题求解程序
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
- 风险: 不得替代伦理审查、法律判断或责任主体
- 备注: 无

### TP-01.03
- Step Key: `research-education-learning`
- 标题: 教育与学习科学研究
- 类型: `documentation`
- 目标: 研究目标操作化、先备/误解诊断、提取应用、支架淡出和形成性反馈如何支持迁移学习
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
- 风险: 无
- 备注: 无

### TP-01.04
- Step Key: `research-linguistics`
- 标题: 语言学研究
- 类型: `documentation`
- 目标: 研究语料采样、最小对比、句法—语义—语用分层、篇章语境和歧义消解中的证据程序
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
- 风险: 无
- 备注: 无

### TP-01.05
- Step Key: `research-historical-reasoning`
- 标题: 历史推理研究
- 类型: `documentation`
- 目标: 研究来源出处批判、语境分期、交叉印证、史学视角和受约束反事实中的解释程序
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
- 风险: 无
- 备注: 无

### TP-01.06
- Step Key: `research-social-science-methods`
- 标题: 社会科学方法研究
- 类型: `documentation`
- 目标: 研究构念操作化、抽样代表性、质性编码、混合方法和制度情境中的证据边界
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
- 风险: 无
- 备注: 无

## TP-02
- Step Key: `gap-audit`
- 标题: 既有库缺口与重复审计
- 类型: `data`
- 目标: 将新研究与现有 226 条目逐项比对，确定哪些方法是新语义、交叉索引或仅需报告补充
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
- 类型: `feature`
- 目标: 把通过缺口审计的方法写成 MentalModelSpec、OperatorSpec 或 MethodSpec，明确前提、步骤、证据、失败和恢复
- 父节点: `ROOT`
- 子节点: 无
- 依赖步骤 Key: gap-audit
- 依赖节点 ID: TP-02
- 输入: 无
- 输出: operators/packs/；operators/source-inventory.json；operators/taxonomy/problem-solving-methodology.json
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

## TP-04
- Step Key: `materialize-library`
- 标题: 入库并同步目录文档
- 类型: `feature`
- 目标: 更新 pack、catalog、计数、研究报告、README、模块上下文、ADR 和任务证据
- 父节点: `ROOT`
- 子节点: 无
- 依赖步骤 Key: define-operators
- 依赖节点 ID: TP-03
- 输入: 无
- 输出: operators/catalog.json；research/HEURISTIC_METACOGNITIVE_RESEARCH.md；docs/；governance/
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

## TP-05
- Step Key: `verify-and-close`
- 标题: 验证、审查与交付收口
- 类型: `testing`
- 目标: 以全量库校验、项目门禁、治理检查、任务证据和 review 证明扩展可复核、可回滚且未越过运行时边界
- 父节点: `ROOT`
- 子节点: 无
- 依赖步骤 Key: materialize-library
- 依赖节点 ID: TP-04
- 输入: 无
- 输出: governance/tasks/0013-continue-domain-heuristics/REVIEW.md；governance/tasks/0013-continue-domain-heuristics/VERIFICATION_PLAN.json
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无
