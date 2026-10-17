# Task-Level Acceptance
- 三个运行时对象通过宽松 Core Schema 和统一验证入口
- 参考 Harness 完成 Select、Bind、Materialize、Verify、Trace 全链路
- 未知绑定、策略不匹配、预算超限和摘要篡改均失败关闭
- 文档和治理清楚区分共享协议、Harness 本地职责与剩余互操作缺口
- approved plan 已成功编译为递归任务树
- 叶子节点数量: 5
- 当前可立即执行叶子节点: TP-01

# Validation Plan
- uv run --locked --script scripts/validate_harness.py --operator-runtime <examples>
- python3 -m unittest tests.test_reference_operator_harness
- python3 scripts/verify_project.py --gate architecture/behavior/contract/test
- 治理 strict、health、principle、task docs、reuse 和任务级 verification
- TP-01 | Verify: 核对验收项: 有效样例通过，缺失稳定字段的反例被拒绝 | Gate: 任务目标与上下文已确认
- TP-02 | Verify: 核对验收项: 正常请求产生可重算摘要和已验证 instruction packet | Gate: 前置步骤已完成: runtime-contract
- TP-03 | Verify: 核对验收项: 错误路径稳定非零或 verdict=rejected，不产生误导性成功 | Gate: 前置步骤已完成: reference-harness
- TP-04 | Verify: 核对验收项: 共享协议与 Harness 本地职责边界一致且可追踪 | Gate: 前置步骤已完成: runtime-negative-tests
- TP-05 | Verify: 核对验收项: 当前输入绑定的确定性证据通过；独立审查状态如实记录 | Gate: 前置步骤已完成: sync-runtime-docs

# Review Gate
- Core Contract 未强制具体算法、领域或业务字段
- 参考 Harness 不拥有中央状态且不执行外部工具
- Verifier 从原始输入独立重算摘要，不信任 Executor 自报
- 所有错误路径非零退出且无伪成功记录

# Runtime Verification Gate
- [x] 每个 tool/action 结果都有可回指证据或明确未执行原因。
- [x] 高风险动作没有由 worker/agent 自我批准；审批状态可追踪。
- [x] compaction / resume 后目标、计划、修改文件、审批状态和验证项未丢失。
- [x] verifier / 自审已检查关键发现是否有证据支持。
- [x] closeout 明确 coverage gaps、failed packets 和 unresolved questions。
- [x] TP-01: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [x] TP-02: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [x] TP-03: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [x] TP-04: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [ ] TP-05: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据

# Ship Readiness
- runtime examples、unit tests、self-test 与 required project gates PASS
- 治理 strict/health/principle、任务 docs、reuse 和 verification 校验通过
- 独立 reviewer 缺失时明确保留 In Progress，不冒充完全完成

# Task Package Acceptance
## TP-01
- 标题: 定义运行时互操作契约
- 验收标准:
  - 有效样例通过，缺失稳定字段的反例被拒绝
- Verify: 核对验收项: 有效样例通过，缺失稳定字段的反例被拒绝
- Gate: 任务目标与上下文已确认
- 输出物: contracts/operator-runtime.schema.json；contracts/examples/；scripts/validate_harness.py

## TP-02
- 标题: 实现参考 Harness 闭环
- 验收标准:
  - 正常请求产生可重算摘要和已验证 instruction packet
- Verify: 核对验收项: 正常请求产生可重算摘要和已验证 instruction packet
- Gate: 前置步骤已完成: runtime-contract
- 输出物: examples/reference-harness/

## TP-03
- 标题: 建立失败关闭证据
- 验收标准:
  - 错误路径稳定非零或 verdict=rejected，不产生误导性成功
- Verify: 核对验收项: 错误路径稳定非零或 verdict=rejected，不产生误导性成功
- Gate: 前置步骤已完成: reference-harness
- 输出物: tests/test_reference_operator_harness.py；tests/fixtures/

## TP-04
- 标题: 同步架构与治理真相
- 验收标准:
  - 共享协议与 Harness 本地职责边界一致且可追踪
- Verify: 核对验收项: 共享协议与 Harness 本地职责边界一致且可追踪
- Gate: 前置步骤已完成: runtime-negative-tests
- 输出物: docs/；README.md；AGENTS.md；governance/

## TP-05
- 标题: 验证、审查与交付
- 验收标准:
  - 当前输入绑定的确定性证据通过；独立审查状态如实记录
- Verify: 核对验收项: 当前输入绑定的确定性证据通过；独立审查状态如实记录
- Gate: 前置步骤已完成: sync-runtime-docs
- 输出物: governance/tasks/0019-reference-operator-runtime-proof/REVIEW.md；governance/tasks/0019-reference-operator-runtime-proof/REUSE_SAMPLING.json

# Anti-Goals
- 不得把参考实现变成中央 Runtime、通用 Planner、服务、数据库或插件框架
- 不得执行模型、工具、网络请求、外部写入或读取凭据
- 不得修改 Operator Library 内容、上游 registry/lock 或 checkout
- 不得虚构证据
- 不得越权补全未确认信息
