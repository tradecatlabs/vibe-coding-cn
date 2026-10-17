# Repo Evidence
- operators/source-inventory.json 当前登记 163 个 source 条目
- operators/catalog.json 当前登记 14 个 pack、163 个 source 和 14 个 derived
- scripts/validate_operator_library.py 已支持开放 domain、精确覆盖、引用解析和治理 owner
- contracts/problem-solving-operator-pack.schema.json 允许 extensions，Core 不封闭 domain 或语义字段集合

# Constraints Matrix
- 只读公开资料与源码，不执行上游代码或实验
- 使用 apply_patch 编辑，保留其他工作树改动，选择性 stage
- 新对象必须有存在性理由、最小验证、天花板和回滚路径
- 物理/化学及其他高影响方法只作为 reference-only，现实副作用由 Harness policy 裁决

# Change Boundary
- operators/source-inventory.json、operators/catalog.json、operators/packs/*.json、operators/taxonomy/
- research/HEURISTIC_METACOGNITIVE_RESEARCH.md、research/AGENTS.md、docs/ 与 README/AGENTS
- governance/ 中任务、ADR、QA、context、索引和验证证据相关文件
- 不修改 research/upstreams.sources.json、research/upstreams.lock.json 或上游 checkout

# Risk Matrix
- 跨领域同名方法可能被重复登记或语义漂移
- 功能分类是项目综合推断，不应伪装成单一来源的原生分类
- 条目规模扩大将增加索引、引用和文档维护成本
- 方法来源充分不等于在真实 Harness 上有效，必须保持 experimental 与未知项

# Assumptions and Falsification
- 采用‘母领域来源 + 八类功能交叉归类’的双轴模型
- 对已有同名方法优先建立 crosswalk，不新建重复 entry；只有可区分语义才新增
- 八类功能允许一个条目有主类和辅助类，具体执行仍由 Harness policy 决定

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
- 标题: 八类功能分别深度抓取证据
- 类型: `documentation`
- 目标: 为八类功能各自建立权威来源、核心动作、适用边界、失败方向和迁移推断
- 父节点: `ROOT`
- 子节点: TP-01.01, TP-01.02, TP-01.03, TP-01.04, TP-01.05, TP-01.06, TP-01.07, TP-01.08
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: research/HEURISTIC_METACOGNITIVE_RESEARCH.md
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-01.01
- Step Key: `research-representation`
- 标题: Representation 表征研究
- 类型: `documentation`
- 目标: 抓取重述、抽象、图示、模型选择和问题表征变换的权威证据
- 父节点: `TP-01`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: research/HEURISTIC_METACOGNITIVE_RESEARCH.md
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-01.02
- Step Key: `research-decomposition`
- 标题: Decomposition 分解研究
- 类型: `documentation`
- 目标: 抓取子目标、分治、模块化、依赖拆解和 means-ends 方法的权威证据
- 父节点: `TP-01`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: research/HEURISTIC_METACOGNITIVE_RESEARCH.md
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-01.03
- Step Key: `research-transformation`
- 标题: Transformation 变换研究
- 类型: `documentation`
- 目标: 抓取类比、归约、反向工作、松弛、特化/推广和等价变换的权威证据
- 父节点: `TP-01`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: research/HEURISTIC_METACOGNITIVE_RESEARCH.md
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-01.04
- Step Key: `research-search`
- 标题: Search 搜索研究
- 类型: `documentation`
- 目标: 抓取系统枚举、贪心、回溯、分支定界、探索/利用和启发式搜索证据
- 父节点: `TP-01`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: research/HEURISTIC_METACOGNITIVE_RESEARCH.md
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-01.05
- Step Key: `research-construction`
- 标题: Construction 构造研究
- 类型: `documentation`
- 目标: 抓取构造性证明、原型、模拟、生成检验、约束满足和迭代精化证据
- 父节点: `TP-01`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: research/HEURISTIC_METACOGNITIVE_RESEARCH.md
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-01.06
- Step Key: `research-verification`
- 标题: Verification/Falsification 验证证伪研究
- 类型: `documentation`
- 目标: 抓取证明、反例、实验、复现、不变量、独立审查和校准证据
- 父节点: `TP-01`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: research/HEURISTIC_METACOGNITIVE_RESEARCH.md
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-01.07
- Step Key: `research-diagnosis`
- 标题: Diagnosis/Revision 诊断修正研究
- 类型: `documentation`
- 目标: 抓取复现、定位、二分、根因、误差分解、差分比较和反思修正证据
- 父节点: `TP-01`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: research/HEURISTIC_METACOGNITIVE_RESEARCH.md
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

### TP-01.08
- Step Key: `research-control`
- 标题: Control/Metacognition 控制元认知研究
- 类型: `documentation`
- 目标: 抓取策略选择、监控、停止、预算分配、切换、回溯和 look-back 证据
- 父节点: `TP-01`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: research/HEURISTIC_METACOGNITIVE_RESEARCH.md
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

## TP-02
- Step Key: `define-operators`
- 标题: 提炼母领域算子与双轴分类
- 类型: `feature`
- 目标: 从统计学、决策科学、运筹学、设计方法及其他母领域筛出不重复的可执行算子，并建立功能分类交叉索引
- 父节点: `ROOT`
- 子节点: 无
- 依赖步骤 Key: research-evidence
- 依赖节点 ID: TP-01
- 输入: 无
- 输出: operators/packs/；operators/taxonomy/；operators/source-inventory.json
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

## TP-03
- Step Key: `materialize-library`
- 标题: 入库并同步交叉索引与文档
- 类型: `feature`
- 目标: 更新 packs、inventory、catalog、taxonomy、研究报告、README、领域文档、ADR/QA 和模块上下文
- 父节点: `ROOT`
- 子节点: 无
- 依赖步骤 Key: define-operators
- 依赖节点 ID: TP-02
- 输入: 无
- 输出: operators/catalog.json；operators/source-inventory.json；operators/taxonomy/；docs/；governance/
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

## TP-04
- Step Key: `verify-and-close`
- 标题: 验证、审查与交付收口
- 类型: `testing`
- 目标: 用全量门禁、治理检查、任务证据、review 和回滚说明证明本轮扩展可复核
- 父节点: `ROOT`
- 子节点: 无
- 依赖步骤 Key: materialize-library
- 依赖节点 ID: TP-03
- 输入: 无
- 输出: governance/tasks/0011-deepen-heuristic-metacognitive-operator-library/REVIEW.md；governance/tasks/0011-deepen-heuristic-metacognitive-operator-library/REUSE_SAMPLING.json
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无
