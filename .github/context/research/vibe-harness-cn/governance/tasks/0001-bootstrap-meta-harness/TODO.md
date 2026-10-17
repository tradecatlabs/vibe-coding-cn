# Execution Checklist
[x] TP-01 | P0 | 研究并定义 Harness 领域模型与元 harness 终态 | Verify: 检查 docs/HARNESS_MODEL.md 的定义、来源、proof point 与 falsifier | Gate: 领域模型可导出供应商中立契约 | Parallelizable: No
[x] TP-02 | P0 | 落地 manifest Schema、样例和 validator | Verify: uv run --locked --script scripts/validate_harness.py --self-test | Gate: 正例 PASS 且结构/策略负例 BLOCK | Parallelizable: Yes
[x] TP-03 | P0 | 建立项目治理包、ADR、QA 和模块上下文 | Verify: python3 governance/tools/governance_context_bundle.py --project-root . --task-type architecture --code-path contracts | Gate: 架构 context bundle PASS | Parallelizable: Yes
[x] TP-04 | P0 | 执行完整验证与风险审查并收口证据 | Verify: 运行 Task Intent、task docs、manifest、governance 全部门禁 | Gate: 无未处理 BLOCK，unknowns 与剩余风险明确 | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX`
- 不允许出现无归属 TODO
