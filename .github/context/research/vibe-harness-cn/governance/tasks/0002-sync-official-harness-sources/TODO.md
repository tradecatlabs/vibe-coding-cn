# Execution Checklist
[x] TP-01 | P0 | 核验三个官方 GitHub 来源、许可证与源码可见性 | Verify: 检查 checkout origin/branch/tree/license | Gate: 来源与限制可绑定 revision | Parallelizable: No
[x] TP-02 | P0 | 建立安全同步入口、revision lock 与研究边界 | Verify: bash scripts/sync_upstreams.sh | Gate: 三仓同步且 lock 结构完整 | Parallelizable: No
[x] TP-03 | P0 | 修复浅克隆 ancestry 故障并建立回归证据 | Verify: auto-debug owner validators | Gate: RED/GREEN/counterfactual PASS | Parallelizable: No
[x] TP-04 | P0 | 执行 high-risk 验证、治理健康、review 与任务收口 | Verify: verification/governance/task/review gates | Gate: 当前输入无未处理 BLOCK | Parallelizable: No

说明：
- 每一行绑定一个语义叶子；依赖以 PLAN/STATUS 为准。
- 本任务单 agent 串行执行，不使用原生子代理。
