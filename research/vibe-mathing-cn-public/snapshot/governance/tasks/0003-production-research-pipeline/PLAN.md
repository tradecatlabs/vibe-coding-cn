# Planning Summary
先封闭信任根，再建立单一存储和可恢复状态机；随后用确定性 adapter 证明主链，用 Lean 证明形式化链，最后以攻击性测试、CI、成熟度审计和文档审查收口。
- 编译节点总数: 6
- 叶子执行项: 6
- 执行波次数: 6
- 当前任务必须遵守 `SPEC -> PLAN -> BUILD -> TEST -> REVIEW -> SHIP`

# Lifecycle Gates
- SPEC：TASK_INTENT 和任务树通过 owner validator
- PLAN：APPROVED_PLAN 已编译为六个串行 TP，每个 TP 均有输入、输出、Verify、Gate、预算与停止条件
- BUILD：每个 TP 只实现其声明的所有权面
- TEST：先保留伪造证据 RED，再取得同源 GREEN；所有状态机和恢复分支有负例
- REVIEW：auto-review 按 agent-harness、security、reliability、completion-verification 审查
- SHIP：maturity audit=100/100 且 task closeout 证据齐全；否则保持 In Progress/Blocked
- 禁止跳过任何 gate；前一 gate 的当前输入绑定证据失效时，后继状态必须回退为未验收而不是沿用旧 PASS

# Simplest Path
复用 Python 标准库、JSON Schema、SymPy、官方 Lean/Mathlib 与现有校验器；不引入数据库、队列、Web 服务或多 Agent 框架。

# Split Strategy
按信任与数据依赖串行拆分六个垂直能力包；每个包都有独立命令和 fail-closed gate，后继只消费前驱的已验证契约。

# Execution Waves
- Wave 1: TP-01
- Wave 2: TP-02
- Wave 3: TP-03
- Wave 4: TP-04
- Wave 5: TP-05
- Wave 6: TP-06

# Runtime Workflow Contract
- workflow artifact 必须存入任务目录，而不是只留在聊天上下文。
- worker 只能消费当前 packet 的最小上下文、允许工具、禁止动作、证据要求和停止条件。
- verifier / 自审必须独立挑战关键发现，不能把 worker 自评当作验收。
- integrator / closeout 必须报告 verified、rejected、unresolved、failed、not-covered。
- 全局预算: 单次 deterministic adapter 默认 30 秒
- 全局预算: 单次外部工具输出默认 1 MiB
- 全局预算: 单次 run 默认最多 16 个状态转换、2 次可重试失败
- 全局预算: Lean 安装/构建采用独立长超时，失败后不无限重试
- 全局停止条件: required gate 首次结构性失败且无法在当前范围修复
- 全局停止条件: Lean 官方工具链无法下载或固定版本不可构建
- 全局停止条件: 需要外部独立 reviewer 实际签发才能继续的状态保持 awaiting_review
- 全局停止条件: 成熟度审计未达 100/100 时禁止完成声明
- 需要审批: 提交、推送、部署、外部消息或修改权限
- 需要审批: 使用凭据或付费模型 API
- 需要审批: 破坏性删除、覆盖现有研究事实或修改已发布 Git 历史
- TP-01: tools=Python stdlib;jsonschema;apply_patch;read-only shell; forbidden=信任调用者 independent 布尔值;读取可信根外 artifact; evidence=pre-fix RED;post-fix GREEN;counterfactual; budget=O(E) 校验;单 artifact 有界读取; stop=可信根或 registry owner 无法确定
- TP-02: tools=Python stdlib fcntl/tempfile/os.replace;jsonschema; forbidden=直接 append 绕过锁;引入数据库; evidence=concurrency test;partial failure test;idempotency test; budget=default; stop=default
- TP-03: tools=Python stdlib argparse/subprocess;现有 owner skills; forbidden=模型自报状态;宽 execute-anything 工具; evidence=state transition tests;timeout/output/retry tests;resume tests; budget=默认 16 transitions;默认 2 retries;默认 1 MiB output; stop=状态图不再单调推进且无可恢复错误
- TP-04: tools=SymPy;Python subprocess/tempfile; forbidden=写真实开放问题记录;网络或模型调用; evidence=CLI-level E2E output;record/artifact digests;idempotency proof; budget=default; stop=default
- TP-05: tools=官方 elan/Lean/lake;GitHub public artifacts;Python subprocess; forbidden=使用 sorry/admit/unsafe;伪造 kernel output; evidence=lean --version;lake build output;escape scan;#print axioms output; budget=安装/构建有界超时;失败最多一次换官方安装路径; stop=官方工具链不可访问或固定版本无法构建
- TP-06: tools=项目 validators;auto-review;Git diff/status read-only; forbidden=硬编码 100;用 REVIEW.md 文本替代命令;自动提交推送; evidence=fresh command outputs;maturity JSON/Markdown;document drift audit;rollback path; budget=default; stop=default

# Next Executable Leaves
- 无；六个实现节点均已完成。剩余事项属于 Git 交付、Verification Plan、复用资产和外部 reviewer provenance，不是可由本轮实现节点继续执行的叶子。

# Dependency Graph
TP-01 -> TP-02
TP-02 -> TP-03
TP-03 -> TP-04
TP-04 -> TP-05
TP-05 -> TP-06

# Rollback Protocol
- 代码与文档通过普通 Git revert 回滚，不使用 reset/clean/checkout/stash，不影响用户或 0002 的改动
- 运行中断先由 WAL 与 run checkpoint 恢复；无法证明完整性时 fail-closed，保留 journal 供人工诊断
- Result 失效只追加 invalidation evidence 并重算 Solution View，不覆盖历史证据
- Lean/Mathlib fixture 回滚到上一个固定 toolchain、Mathlib commit 与对应 lake manifest
