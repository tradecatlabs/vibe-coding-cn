# Execution Checklist
[x] TP-01 | P0 | 核验 DeepSeek Harness 官方来源、分支、许可证、核心路径与 preview 限制 | Verify: checkout Git/tree/license inspection | Gate: 事实可绑定当前 revision | Parallelizable: No
[x] TP-02 | P0 | 接入单一登记源、同步逻辑、lock、回归和文档 | Verify: bash -n 与 bash tests/test_sync_upstreams.sh | Gate: 四源定义一致且拒绝路径不退化 | Parallelizable: No
[x] TP-03 | P0 | 真实拉取四源、验证幂等、项目门禁、治理与本地交付 | Verify: sync twice + verify_project + governance/task validators | Gate: 当前输入无 BLOCK 且本地 commit 可追踪 | Parallelizable: No

说明：
- 每一行绑定一个语义叶子；依赖以 PLAN/STATUS 为准。
- 本任务由主 Codex 串行执行，不使用原生子代理。
