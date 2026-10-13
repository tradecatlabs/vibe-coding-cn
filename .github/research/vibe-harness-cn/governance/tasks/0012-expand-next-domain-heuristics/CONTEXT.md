# Repo Evidence
- 本任务开始时基线为 20 个 pack、196 个 source、20 个 derived（总计 216）；本轮完成后当前库为 26 个 pack、226 个 source、26 个 derived（总计 252）
- operators/source-inventory.json 是当前跨学科 226 条 source 的完整性基线；本轮新增六个母领域各 5 个 source
- operators/taxonomy/problem-solving-methodology.json 已定义母领域与八类功能双轴
- research/HEURISTIC_METACOGNITIVE_RESEARCH.md 已有八类功能研究、来源矩阵和下一阶段方向
- 公共 Core/Profile 校验和治理 strict/health 已在提交 060c1b2 后通过

# Constraints Matrix
- 只读公开资料和项目文件，不执行上游代码、模型训练或现实实验
- 新增内容只进入 operators、research、docs、governance、README/AGENTS 的明确范围
- 高影响领域只作 reference-only 方法说明，现实操作由具体 Harness policy 与独立审查接管
- 保持任务开始时的 196/20 source/derived 基线、Core 宽松边界和回滚路径；新增条目均可独立移除

# Change Boundary
- operators/packs/、operators/source-inventory.json、operators/catalog.json、operators/taxonomy/
- research/HEURISTIC_METACOGNITIVE_RESEARCH.md、research/AGENTS.md、docs/、README.md、AGENTS.md
- governance/tasks/0012-*、治理 ADR/QA、module context 和必要索引
- 不修改 research/upstreams.sources.json、research/upstreams.lock.json 或上游 checkout

# Risk Matrix
- 因果、医学和人因术语可能被误读为专业授权或事实结论
- 经济/博弈、生态/生物和认知研究可能跨越多个功能类，容易重复或过度泛化
- 来源数量增长会增加索引、引用和文档漂移维护成本
- 来源成熟不等于迁移到 Agent 后真实有效
- 不得把观察关联写成因果证明

# Assumptions and Falsification
- 继续使用母领域来源轴与八类功能轴，不把新增领域直接写入公共 Core
- 每个候选领域先建立证据矩阵，只有存在清晰问题求解程序才进入 pack
- 若某候选领域缺少可审计方法或与已有条目重复，则记录缺口而不强行新增

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
- 目标: 为候选母领域建立一手来源、反复使用的方法程序、可迁移问题、证据边界和未验证项，并映射到八类功能
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
- Step Key: `research-causal-inference`
- 标题: 因果推断研究
- 类型: `documentation`
- 目标: 研究反事实、因果图、干预、识别条件、混杂审计和敏感性分析如何支持受限结论
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
- 风险: 不得把观察关联写成因果证明
- 备注: 无

### TP-01.02
- Step Key: `research-economics-game-theory`
- 标题: 经济与博弈研究
- 类型: `documentation`
- 目标: 研究机会成本、边际分析、激励、均衡、机制设计和鲁棒策略中的问题求解程序
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

### TP-01.03
- Step Key: `research-ecology-biology`
- 标题: 生态与生物研究
- 类型: `documentation`
- 目标: 研究生态系统边界、种群动力学、适应、选择、网络关系、实验对照和多尺度推断
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
- Step Key: `research-cognitive-science`
- 标题: 认知科学研究
- 类型: `documentation`
- 目标: 研究表征、类比、双过程、工作记忆、策略选择、认知负荷和元认知监控中的可迁移程序
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
- Step Key: `research-human-factors`
- 标题: 人因可靠性研究
- 类型: `documentation`
- 目标: 研究情境意识、检查表、错误分类、工作负荷、冗余、恢复和安全关键决策中的方法
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
- Step Key: `research-medical-decision`
- 标题: 医学决策研究
- 类型: `documentation`
- 目标: 研究临床决策中的证据分层、诊断阈值、风险收益、共享决策和不确定性沟通，仅作参考方法
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
- 目标: 将新研究与现有 216 条目逐项比对，确定哪些方法是新语义、交叉索引或仅需报告补充
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
- 目标: 更新 pack、catalog、计数、研究报告、README、模块上下文、ADR/QA 和任务证据
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
- 输出: governance/tasks/0012-expand-next-domain-heuristics/REVIEW.md；governance/tasks/0012-expand-next-domain-heuristics/VERIFICATION_PLAN.json
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无
