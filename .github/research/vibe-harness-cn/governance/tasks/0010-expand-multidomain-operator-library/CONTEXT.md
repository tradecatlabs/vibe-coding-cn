# Repo Evidence
- 本任务起始基线为 75 个 source、7 个 derived 和 7 个 pack；扩展完成后已更新为 163 个 source、14 个 derived、14 个 pack、177 个总条目。
- `operators/source-inventory.json` 是当前 163 个 source 条目的独立清单；`operators/catalog.json` 登记当前 14 个 pack 及其计数。
- scripts/validate_operator_library.py 已支持开放 domain、精确覆盖、引用解析和治理 owner
- contracts/problem-solving-operator-pack.schema.json 的 Core 不封闭 domain，也不强制语义集合数量

# Constraints Matrix
- 只读上游源码与公开资料，不执行上游代码或脚本
- 使用 apply_patch 编辑，选择性 stage，保留其他 AI 的工作树改动
- 新增对象必须有存在性理由、最小验证、天花板和回滚路径
- 化学/物理条目只能作为参考方法，实际副作用仍由 Harness policy 控制

# Change Boundary
- operators/source-inventory.json、operators/catalog.json、operators/packs/*.json
- research/EXPANDED_OPERATOR_RESEARCH.md、docs/、README/AGENTS 与 operators 模块文档
- governance/ 中与任务、ADR、QA、context、索引相关的同步文件
- 不修改 research/upstreams.sources.json、lock 或上游 checkout

# Risk Matrix
- 跨学科术语可能被过度简化，导致算子与真实方法脱节
- 条目规模扩大可能造成重复、索引漂移和维护成本上升
- 化学/物理内容若缺少安全语境，可能被误读为实验授权
- 一手资料覆盖不等于真实 Harness 质量验证，需保留 experimental 状态

# Assumptions and Falsification
- 本轮采用“第一研究波”边界：优先建立每个点名领域的最小高价值覆盖，而非穷尽所有学科
- 新领域使用独立 domain pack；已有领域在原 pack 内追加 source 条目
- 若某个方法只有 mental model 证据而无可执行步骤，登记为 MentalModelSpec

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
- 标题: 建立跨学科证据矩阵
- 类型: `documentation`
- 目标: 从一手资料提炼每个目标领域可执行、可证伪、可记录证据的候选方法
- 父节点: `ROOT`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: research/EXPANDED_OPERATOR_RESEARCH.md；operators/source-inventory.json
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

## TP-02
- Step Key: `define-operators`
- 标题: 定义算子语义与领域边界
- 类型: `feature`
- 目标: 把候选方法写成 MentalModelSpec、OperatorSpec 或 MethodSpec，明确适用、证据、失败和恢复
- 父节点: `ROOT`
- 子节点: 无
- 依赖步骤 Key: research-evidence
- 依赖节点 ID: TP-01
- 输入: 无
- 输出: operators/packs/*.json
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

## TP-03
- Step Key: `materialize-library`
- 标题: 入库并同步目录文档
- 类型: `feature`
- 目标: 更新 pack、catalog、计数、研究报告、README、模块上下文、ADR/QA 与 source-of-truth
- 父节点: `ROOT`
- 子节点: 无
- 依赖步骤 Key: define-operators
- 依赖节点 ID: TP-02
- 输入: 无
- 输出: operators/catalog.json；operators/packs/；docs/；governance/
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
- 目标: 以全量门禁、治理检查、任务证据和 review 证明当前扩展可复核且可回滚
- 父节点: `ROOT`
- 子节点: 无
- 依赖步骤 Key: materialize-library
- 依赖节点 ID: TP-03
- 输入: 无
- 输出: governance/tasks/0010-expand-multidomain-operator-library/REVIEW.md；governance/tasks/0010-expand-multidomain-operator-library/REUSE_SAMPLING.json
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无
