# Repo Evidence
- operators/catalog.json 是当前 Reference Library 目录入口
- contracts/problem-solving-operator-pack.schema.json 已采用宽松 Core + 可选 Profile
- docs/PROBLEM_SOLVING_OPERATOR_ARCHITECTURE_PRD.md 已定义 FR-015、FR-018、FR-019 和 FR-020
- scripts/validate_harness.py 是统一静态验证入口

# Constraints Matrix
- 只实现本地无副作用 instruction materialization
- Selector 对目录单次线性扫描，不把全文交给模型
- Verifier 独立重算摘要并裁决契约结果
- 不读取凭据、不触碰上游 checkout、不执行破坏性 Git 操作

# Change Boundary
- contracts/、examples/reference-harness/、scripts/、tests/
- docs/、README.md、AGENTS.md、governance/
- 不修改 operators/packs/、research/upstreams.sources.json、research/upstreams.lock.json 或 checkout

# Risk Matrix
- 参考实现若放错边界会被误解为中央运行时
- 执行成功若命名不清会被误解为问题已解决
- Binding 若与 policy 合并不严谨可能形成权限扩大
- Trace 若保存原始上下文可能泄露敏感信息

# Assumptions and Falsification
- 用户的“执行”批准了上一轮明确提出的 Selector 到 Trace 实现顺序
- 第一版以一个参考 Harness 证明协议闭环，后续再用第二个独立 Harness 验证互操作性
- Reference Library Profile 的 468 条静态内容保持不变

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
- Step Key: `runtime-contract`
- 标题: 定义运行时互操作契约
- 类型: `action`
- 目标: 定义三个宽松 envelope、最小例子和静态验证入口
- 父节点: `ROOT`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 无
- 输出: contracts/operator-runtime.schema.json；contracts/examples/；scripts/validate_harness.py
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

## TP-02
- Step Key: `reference-harness`
- 标题: 实现参考 Harness 闭环
- 类型: `action`
- 目标: 实现确定性 Select、Bind、Materialize、Verify 与 Trace
- 父节点: `ROOT`
- 子节点: 无
- 依赖步骤 Key: runtime-contract
- 依赖节点 ID: TP-01
- 输入: operators/catalog.json；operators/packs/；contracts/operator-runtime.schema.json
- 输出: examples/reference-harness/
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

## TP-03
- Step Key: `runtime-negative-tests`
- 标题: 建立失败关闭证据
- 类型: `action`
- 目标: 覆盖未知绑定、策略不匹配、预算超限、循环/未知引用和摘要篡改
- 父节点: `ROOT`
- 子节点: 无
- 依赖步骤 Key: reference-harness
- 依赖节点 ID: TP-02
- 输入: 无
- 输出: tests/test_reference_operator_harness.py；tests/fixtures/
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无

## TP-04
- Step Key: `sync-runtime-docs`
- 标题: 同步架构与治理真相
- 类型: `action`
- 目标: 更新 PRD、Operator Spec、Harness Model、ADR、README、AGENTS 和 module context
- 父节点: `ROOT`
- 子节点: 无
- 依赖步骤 Key: runtime-negative-tests
- 依赖节点 ID: TP-03
- 输入: 无
- 输出: docs/；README.md；AGENTS.md；governance/
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
- 目标: 运行所有 required gates、strict governance、任务 closeout 和本地提交
- 父节点: `ROOT`
- 子节点: 无
- 依赖步骤 Key: sync-runtime-docs
- 依赖节点 ID: TP-04
- 输入: 无
- 输出: governance/tasks/0019-reference-operator-runtime-proof/REVIEW.md；governance/tasks/0019-reference-operator-runtime-proof/REUSE_SAMPLING.json
- 允许工具: 默认遵循当前环境与任务范围
- 禁止动作: 无未声明授权的高风险动作
- 证据要求: 命令输出、文件 diff、日志或审查结论
- 停止条件: 越界、缺审批、验证失败或上下文不足时暂停
- 风险: 无
- 备注: 无
