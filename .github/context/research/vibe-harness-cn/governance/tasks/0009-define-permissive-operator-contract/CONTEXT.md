# Repo Evidence
- contracts/problem-solving-operator-pack.schema.json 当前要求完整语义数组并封闭 domain 枚举
- scripts/validate_operator_library.py 当前同时执行 Schema 与本项目 exact-set 策略
- operators/catalog.json 已能作为 Reference Library Profile 的明确入口

# Constraints Matrix
- 保持 v1alpha1 既有 pack 向后兼容，放宽变化不要求迁移已有内容
- 复用 JSON Schema Draft 2020-12、jsonschema 和现有统一 CLI
- 不读取凭据、不联网、不执行上游代码、不部署、不 push、不执行破坏性 Git

# Change Boundary
- 只调整 Operator Pack 契约、校验入口、相应文档与治理资产
- 不修改 Harness manifest、不改 82 个条目语义、不触碰 research 上游

# Risk Matrix
- 过度放宽可能让拼写错误或类型混淆静默进入库
- 过度加严会把当前作者习惯误写成跨 Harness 标准
- Core 与 Profile 边界若不清楚会让第三方误以为必须复制 75+7 目录

# Assumptions and Falsification
- 结构严格包括 JSON 类型、稳定身份、kind 判别、引用形状、显式扩展与安全 owner
- 内容宽松包括领域集合、说明字段、步骤数量、证据数量和自然语言组织

# Critical Ambiguities
- 当前未记录会改变实现路径的关键歧义；若发现此类歧义，必须暂停并回到需求澄清

# Debug Evidence Contract
- 调试模式: Optional
- 回归证据契约: Optional
- 若任务属于 bugfix / regression / flaky / crash / CI-only failure，必须切到 `Required`
- 调试模式为 `Required` 时必须在当前任务目录创建并维护 `DEBUG.md`
- 回归证据契约为 `Required` 时，closeout 必须由 `auto-debug` 校验 `REGRESSION_EVIDENCE.json` 的 RED/GREEN/反事实证据
- 强制调试叶子节点: 无

# Task Package Context Map
## TP-01
- Step Key: `define-spec`
- 标题: 定义宽松核心与 Profile 边界
- 类型: `documentation`
- 目标: 把规范性 MUST 与内容建议 SHOULD 分开
- 父节点: `ROOT`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 用户约束；现有 PSOA PRD、Schema、ADR-0003
- 输出: docs/OPERATOR_SPEC.md；governance/decisions/adr/ADR-0004-问题求解算子采用宽松核心与可选加严-Profile.md
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

## TP-02
- Step Key: `relax-contract`
- 标题: 放宽 Schema 并标注参考库 Profile
- 类型: `feature`
- 目标: 让新领域和渐进式定义可被结构契约表达
- 父节点: `ROOT`
- 子节点: 无
- 依赖步骤 Key: define-spec
- 依赖节点 ID: TP-01
- 输入: docs/OPERATOR_SPEC.md；contracts/problem-solving-operator-pack.schema.json
- 输出: contracts/problem-solving-operator-pack.schema.json；operators/catalog.json
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

## TP-03
- Step Key: `verify-profiles`
- 标题: 实现 Core 与 Reference 验证
- 类型: `testing`
- 目标: 证明宽松不等于失去格式和安全门禁
- 父节点: `ROOT`
- 子节点: 无
- 依赖步骤 Key: relax-contract
- 依赖节点 ID: TP-02
- 输入: 调整后的 Schema 与 catalog
- 输出: scripts/validate_harness.py；scripts/validate_operator_library.py
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

## TP-04
- Step Key: `sync-and-close`
- 标题: 同步文档治理并完成验证
- 类型: `delivery`
- 目标: 让所有长期真相源和任务证据与新分层一致
- 父节点: `ROOT`
- 子节点: 无
- 依赖步骤 Key: verify-profiles
- 依赖节点 ID: TP-03
- 输入: 本任务实现和验证结果
- 输出: README.md；AGENTS.md；docs/；governance/；governance/tasks/0009-define-permissive-operator-contract/
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无
