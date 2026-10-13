# Execution Checklist
[x] TP-01 | P0 | 拉取并核验用户指定的 11 个 canonical Harness 来源、许可证、核心路径与限制 | Verify: checkout Git/tree/license inspection | Gate: 事实绑定当前 revision 且无推断补齐 | Parallelizable: No
[x] TP-02 | P0 | 将 11 源接入单一 registry、lock、集合回归和长期文档 | Verify: bash -n + bash tests/test_sync_upstreams.sh | Gate: 最终精确 15 源且拒绝路径不退化 | Parallelizable: No
[x] TP-03 | P0 | 真实同步 15 源、验证幂等与性能、执行门禁审查和本地交付 | Verify: sync twice + project/governance/task validators + post-commit smoke | Gate: 当前输入无 BLOCK 且工作树 clean | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
