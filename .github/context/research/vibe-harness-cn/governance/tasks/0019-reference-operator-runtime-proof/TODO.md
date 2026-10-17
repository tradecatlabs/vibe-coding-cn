# Execution Checklist
[x] TP-01 | P0 | 定义运行时互操作契约 | Verify: 核对验收项: 有效样例通过，缺失稳定字段的反例被拒绝 | Gate: 任务目标与上下文已确认 | Parallelizable: No
[x] TP-02 | P0 | 实现参考 Harness 闭环 | Verify: 核对验收项: 正常请求产生可重算摘要和已验证 instruction packet | Gate: 前置步骤已完成: runtime-contract | Parallelizable: No
[x] TP-03 | P0 | 建立失败关闭证据 | Verify: 核对验收项: 错误路径稳定非零或 verdict=rejected，不产生误导性成功 | Gate: 前置步骤已完成: reference-harness | Parallelizable: No
[x] TP-04 | P0 | 同步架构与治理真相 | Verify: 核对验收项: 共享协议与 Harness 本地职责边界一致且可追踪 | Gate: 前置步骤已完成: runtime-negative-tests | Parallelizable: No
[ ] TP-05 | P0 | 验证、审查与交付 | Verify: 核对验收项: 当前输入绑定的确定性证据通过；独立审查状态如实记录 | Gate: 前置步骤已完成: sync-runtime-docs | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
