# Acceptance Checklist

# Global Standards
- [x] 运行时 Core 结构严格但语义宽松，extensions 可扩展
- [x] Binding 不能扩大 Harness policy，执行层不能自证成功
- [x] Trace 默认最小披露且摘要可重算
- [x] 参考实现不是中央运行时，也不是生产适配器

# Task Package Checklists
## TP-01
- 标题: 定义运行时互操作契约
- 验收项:
  - [x] 有效样例通过，缺失稳定字段的反例被拒绝
- Verify: 核对验收项: 有效样例通过，缺失稳定字段的反例被拒绝
- Gate: 任务目标与上下文已确认
- 输出物:
  - [x] contracts/operator-runtime.schema.json
  - [x] contracts/examples/
  - [x] scripts/validate_harness.py
- 标准清单:
  - [x] Verify: 核对验收项: 有效样例通过，缺失稳定字段的反例被拒绝
  - [x] Gate: 任务目标与上下文已确认
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

## TP-02
- 标题: 实现参考 Harness 闭环
- 验收项:
  - [x] 正常请求产生可重算摘要和已验证 instruction packet
- Verify: 核对验收项: 正常请求产生可重算摘要和已验证 instruction packet
- Gate: 前置步骤已完成: runtime-contract
- 输出物:
  - [x] examples/reference-harness/
- 标准清单:
  - [x] Verify: 核对验收项: 正常请求产生可重算摘要和已验证 instruction packet
  - [x] Gate: 前置步骤已完成: runtime-contract
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

## TP-03
- 标题: 建立失败关闭证据
- 验收项:
  - [x] 错误路径稳定非零或 verdict=rejected，不产生误导性成功
- Verify: 核对验收项: 错误路径稳定非零或 verdict=rejected，不产生误导性成功
- Gate: 前置步骤已完成: reference-harness
- 输出物:
  - [x] tests/test_reference_operator_harness.py
  - [x] tests/fixtures/
- 标准清单:
  - [x] Verify: 核对验收项: 错误路径稳定非零或 verdict=rejected，不产生误导性成功
  - [x] Gate: 前置步骤已完成: reference-harness
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

## TP-04
- 标题: 同步架构与治理真相
- 验收项:
  - [x] 共享协议与 Harness 本地职责边界一致且可追踪
- Verify: 核对验收项: 共享协议与 Harness 本地职责边界一致且可追踪
- Gate: 前置步骤已完成: runtime-negative-tests
- 输出物:
  - [x] docs/
  - [x] README.md
  - [x] AGENTS.md
  - [x] governance/
- 标准清单:
  - [x] Verify: 核对验收项: 共享协议与 Harness 本地职责边界一致且可追踪
  - [x] Gate: 前置步骤已完成: runtime-negative-tests
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

## TP-05
- 标题: 验证、审查与交付
- 验收项:
  - [x] 当前输入绑定的确定性证据通过；独立审查状态如实记录
- Verify: 核对验收项: 当前输入绑定的确定性证据通过；独立审查状态如实记录
- Gate: 前置步骤已完成: sync-runtime-docs
- 输出物:
  - [x] governance/tasks/0019-reference-operator-runtime-proof/REVIEW.md
  - [x] governance/tasks/0019-reference-operator-runtime-proof/REUSE_SAMPLING.json
- 标准清单:
  - [x] Verify: 核对验收项: 当前输入绑定的确定性证据通过；独立审查状态如实记录
  - [x] Gate: 前置步骤已完成: sync-runtime-docs
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检
