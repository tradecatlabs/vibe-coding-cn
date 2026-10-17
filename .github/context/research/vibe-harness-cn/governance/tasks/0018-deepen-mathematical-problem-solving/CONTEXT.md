# Repo Evidence
- operators/catalog.json 当前登记 56 个 pack、376 个 source、56 个 derived
- operators/source-inventory.json 是来源覆盖单一真相源
- operators/packs/mathematics.json 当前有 20 个 source 与 1 个 derived
- operators/taxonomy/problem-solving-methodology.json 已固定八类功能轴

# Constraints Matrix
- 只读公开资料和项目文件，不执行上游代码或现实实验
- 公共 Core 保持宽松，内容保持 reference_only
- 不修改 upstream registry、lock 或 checkout
- 不读取凭据，不执行破坏性 Git 操作

# Change Boundary
- operators/packs/mathematics.json、operators/source-inventory.json、operators/catalog.json、operators/taxonomy/
- research/、docs/、README.md、AGENTS.md
- governance/tasks/0018-deepen-mathematical-problem-solving/ 与相关 module context
- 不修改 contracts/、research/upstreams.sources.json、research/upstreams.lock.json 或 checkout

# Risk Matrix
- 同义方法重复建模会污染选择器和评测
- 把教学框架误当成唯一官方分类会夸大证据
- 把计算实验、类比或样例当成证明会混淆证据等级
- 多功能方法只选一个主类可能丢失次级语义
- 不把综合八分类写成单一机构的官方分类

# Assumptions and Falsification
- 用户提供的八个数学过程分组作为研究视图保留
- 项目八类 functional_class 继续作为统一运行分类视图
- 新增条目只改变静态参考库，不增加实际执行能力

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
- Step Key: `research-frameworks`
- 标题: 核验数学问题求解框架
- 类型: `action`
- 目标: 核验 Pólya、Schoenfeld、Mason–Burton–Stacey、NCTM 和 MIT 对问题求解、发现、控制与证明的支持边界
- 父节点: `ROOT`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: research/MATHEMATICAL_PROBLEM_SOLVING_RESEARCH.md
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 不把综合八分类写成单一机构的官方分类
- 备注: 无

## TP-02
- Step Key: `crosswalk-55`
- 标题: 逐项审计 55 个方法
- 类型: `action`
- 目标: 与当前 432 个条目逐项去重并形成 20 reuse/35 add 的完整 crosswalk
- 父节点: `ROOT`
- 子节点: 无
- 依赖步骤 Key: research-frameworks
- 依赖节点 ID: TP-01
- 输入: operators/source-inventory.json；operators/packs/；research/MATHEMATICAL_PROBLEM_SOLVING_RESEARCH.md
- 输出: research/MATHEMATICAL_PROBLEM_SOLVING_RESEARCH.md
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

## TP-03
- Step Key: `materialize-mathematics`
- 标题: 沉淀数学算子与组合方法
- 类型: `action`
- 目标: 将 35 个独立缺口和 1 个数学发现与证明循环写入现有 Reference Library
- 父节点: `ROOT`
- 子节点: 无
- 依赖步骤 Key: crosswalk-55
- 依赖节点 ID: TP-02
- 输入: research/MATHEMATICAL_PROBLEM_SOLVING_RESEARCH.md；docs/OPERATOR_SPEC.md
- 输出: operators/packs/mathematics.json；operators/source-inventory.json；operators/catalog.json；operators/taxonomy/problem-solving-methodology.json
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

## TP-04
- Step Key: `sync-docs-governance`
- 标题: 同步文档与治理真相
- 类型: `action`
- 目标: 同步研究索引、目录职责、库快照、领域模型和任务证据
- 父节点: `ROOT`
- 子节点: 无
- 依赖步骤 Key: materialize-mathematics
- 依赖节点 ID: TP-03
- 输入: 无
- 输出: research/；docs/；governance/；README.md；AGENTS.md
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

## TP-05
- Step Key: `verify-review-ship`
- 标题: 验证、审查与交付
- 类型: `action`
- 目标: 运行全量库、自测、项目门禁、治理与任务级验证，记录独立审查状态
- 父节点: `ROOT`
- 子节点: 无
- 依赖步骤 Key: sync-docs-governance
- 依赖节点 ID: TP-04
- 输入: 无
- 输出: governance/tasks/0018-deepen-mathematical-problem-solving/REVIEW.md；governance/tasks/0018-deepen-mathematical-problem-solving/VERIFICATION_PLAN.json
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无
