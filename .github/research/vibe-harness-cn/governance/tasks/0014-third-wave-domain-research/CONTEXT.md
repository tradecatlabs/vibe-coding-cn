# Repo Evidence
- operators/catalog.json 当前登记 32 个 pack、256 个 source 和 32 个 derived
- operators/source-inventory.json 是当前跨学科 256 条 source 的完整性基线
- operators/taxonomy/problem-solving-methodology.json 已定义母领域与八类功能双轴
- research/DOMAIN_EVIDENCE_MATRIX.md 已记录前两轮领域的来源、迁移边界和停止理由
- 公共 Core/Profile 校验入口与治理 strict/health 已存在

# Constraints Matrix
- 只读公开资料和项目文件，不执行上游代码、模型训练或现实操作
- 新增内容只进入 operators、research、docs、governance、README/AGENTS 的明确范围
- 高风险领域只作 reference-only 方法说明，现实操作由具体 Harness policy 与独立审查接管
- 保持现有 source/derived 条目、Core 宽松边界和回滚路径

# Change Boundary
- operators/packs/、operators/source-inventory.json、operators/catalog.json、operators/taxonomy/
- research/HEURISTIC_METACOGNITIVE_RESEARCH.md、research/DOMAIN_EVIDENCE_MATRIX.md、research/AGENTS.md
- docs/、README.md、AGENTS.md、治理上下文/ADR/任务包
- 不修改 research/upstreams.sources.json、research/upstreams.lock.json 或上游 checkout

# Risk Matrix
- 形式证明与科学解释容易被误读为真实世界结论或自动授权
- 地学、天文和材料方法依赖测量误差、校准、尺度和实验条件
- 信息检索方法容易把来源相关性误写成事实正确性
- 来源数量增长会增加索引、引用和文档漂移维护成本
- 来源成熟不等于迁移到 Agent 后真实有效
- 不得把形式证明流程写成现实命题已证实
- 不得把解释偏好写成事实确定性
- 不得把静态方法说明当成地质或环境专业结论
- 不得把观测拟合写成未经校准的天体事实
- 不得自动给出材料制备、采购或安全操作指令
- 不得把检索命中自动当成事实或授权

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
- 类型: `package`
- 目标: 为六个候选领域建立权威来源、反复使用的方法程序、可迁移问题、证据边界和未验证项，并映射到八类功能
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
- Step Key: `research-formal-logic`
- 标题: 形式逻辑与自动推理研究
- 类型: `action`
- 目标: 研究规格化、语法语义分离、可满足性反例、证明状态分解和内核检查如何约束推理
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
- 风险: 不得把形式证明流程写成现实命题已证实
- 备注: 无

### TP-01.02
- Step Key: `research-epistemology`
- 标题: 哲学与科学认识论研究
- 类型: `action`
- 目标: 研究观察与解释分离、最佳解释推断、辅助假设审计、欠定性分支和区分性证据设计
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
- 风险: 不得把解释偏好写成事实确定性
- 备注: 无

### TP-01.03
- Step Key: `research-geoscience`
- 标题: 地球科学与地学研究
- 类型: `action`
- 目标: 研究观测误差、地层相对时序、地图剖面、质量守恒和遥感地面真值如何支持跨尺度推断
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
- 风险: 不得把静态方法说明当成地质或环境专业结论
- 备注: 无

### TP-01.04
- Step Key: `research-astronomy`
- 标题: 天文学与天体物理研究
- 类型: `action`
- 目标: 研究观测模型分离、信号背景区分、尺度检查、光变/光谱拟合和独立观测确认
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
- 风险: 不得把观测拟合写成未经校准的天体事实
- 备注: 无

### TP-01.05
- Step Key: `research-materials`
- 标题: 材料科学研究
- 类型: `action`
- 目标: 研究加工—结构—性能映射、计量溯源、微观结构表征、数据质量和资格校准
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
- 风险: 不得自动给出材料制备、采购或安全操作指令
- 备注: 无

### TP-01.06
- Step Key: `research-information-knowledge`
- 标题: 信息与知识科学研究
- 类型: `action`
- 目标: 研究信息需求表达、查询扩展、来源权威与 provenance、精确率召回率审计和元数据公平性检查
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
- 风险: 不得把检索命中自动当成事实或授权
- 备注: 无

## TP-02
- Step Key: `gap-audit`
- 标题: 既有库缺口与重复审计
- 类型: `action`
- 目标: 将新研究与现有 256 条目逐项比对，确定哪些方法是新语义、交叉索引或仅需报告补充
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
- 目标: 把通过缺口审计的方法写成 MentalModelSpec、OperatorSpec 或 MethodSpec，明确前提、步骤、证据、失败和恢复
- 父节点: `ROOT`
- 子节点: 无
- 依赖步骤 Key: gap-audit
- 依赖节点 ID: TP-02
- 输入: research/DOMAIN_EVIDENCE_MATRIX.md；docs/OPERATOR_SPEC.md
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
- 类型: `action`
- 目标: 更新 pack、inventory、catalog、taxonomy、研究报告、README、模块上下文和 ADR，保持单一真相源一致
- 父节点: `ROOT`
- 子节点: 无
- 依赖步骤 Key: define-operators
- 依赖节点 ID: TP-03
- 输入: operators/packs/；operators/source-inventory.json；operators/catalog.json
- 输出: operators/catalog.json；research/；docs/；governance/；README.md；AGENTS.md
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
- 目标: 运行全量库、Core、自测、项目门禁、治理校验和任务证据检查，绑定 clean HEAD 与未验证项
- 父节点: `ROOT`
- 子节点: 无
- 依赖步骤 Key: materialize-library
- 依赖节点 ID: TP-04
- 输入: 无
- 输出: governance/tasks/0014-third-wave-domain-research/REVIEW.md；governance/tasks/0014-third-wave-domain-research/VERIFICATION_PLAN.json
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无
