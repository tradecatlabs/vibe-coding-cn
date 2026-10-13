# Acceptance Checklist

# Global Standards
- [x] 目标终态、真实/惯性约束、kill list、proof point、falsifier 和迁移切片已记录。
- [x] 新增对象通过存在性检查；未创建投机服务与基础设施。
- [x] 权限、秘密、停止条件、验证和回滚等不可简化边界被保留。
- [x] 最终新鲜验证和 review 结论完成；生产 runtime 与独立审查边界明确保留为 WARN。

# Task Package Checklists
## TP-01 研究并定义 Harness 领域模型
- [x] 定义 `Agent = LLM + Harness` 的用途和精确运行表达。
- [x] 区分 workflow、agent、harness 与 meta harness。
- [x] 记录一手资料、候选路径、风险和效率判断。
- Verify: `docs/HARNESS_MODEL.md` 结构检查与来源链接检查。
- Gate: 领域模型不绑定单一供应商，且能导出机器契约。

## TP-02 落地 manifest 契约与 validator
- [x] Schema、有效样例、结构负例和策略负例存在。
- [x] validator 使用成熟 jsonschema，并以非零状态拒绝失败输入。
- [x] 工具声明包含 schema、结果上限、超时、重试、幂等和审批绑定。
- Verify: `uv run --locked --script scripts/validate_harness.py --self-test`。
- Gate: 正例 PASS 且结构/策略多类反事实负例均 BLOCK。

## TP-03 建立项目治理与架构记忆
- [x] Operating model、toolchain、topology、架构原则、ADR、QA 和 module context 同步。
- [x] 根及新增目录 `AGENTS.md` 解释文件职责和依赖方向。
- Verify: `python3 governance/tools/governance_context_bundle.py --project-root . --task-type architecture --code-path contracts`。
- Gate: context bundle 和 governance strict validator 均 PASS。

## TP-04 执行验证与风险审查
- [x] 跑完 JSON/Python、manifest、Task Intent、task docs、governance 全部门禁。
- [x] 完成 agent-harness/security/contract/Ponytail/document-drift 自审并记录 unknowns。
- Verify: 任务 `STATUS.md` 中记录所有新鲜命令证据。
- Gate: 无未处理 BLOCK；WARN 有明确边界、owner 和下一验证路径。
