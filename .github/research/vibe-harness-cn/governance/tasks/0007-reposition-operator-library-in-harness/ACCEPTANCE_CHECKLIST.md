# Acceptance Checklist

# Global Standards
- [x] Operator Library 明确属于 Harness。
- [x] 共享规范、中央治理目录、本地库存和 Binding 所有权清楚。
- [x] 权限、验证、证据与业务状态边界未弱化。
- [x] 未新增无消费方的服务、抽象、Schema 或依赖。
- [x] 文档、治理和项目门禁有新鲜证据。

# Task Package Checklists
## TP-01
- [x] 更新 PRD 的定义、全局树、对象所有权、执行流、MVP 和验收。
- [x] 更新 HARNESS_MODEL 的 Harness 组成和算子库小节。
- [x] Verify: 旧边界术语扫描。
- [x] Gate: Operator Library 明确属于 Harness 且既有安全语义未弱化。

## TP-02
- [x] 更新 ADR-0003、README/AGENTS、操作模型、拓扑和 docs module context。
- [x] 重建治理索引。
- [x] Verify: governance strict 和 health report。
- [x] Gate: 全部长期真相源使用一致边界。

## TP-03
- [x] 完成本地自审并写入 REVIEW.md。
- [x] 运行 principle scan 与 architecture/behavior/contract/test gates。
- [x] 完成任务 closeout、复用采样和本地提交后验证。
- [x] Verify: task closeout 与任务级 verification strict。
- [x] Gate: 当前输入绑定证据全部 PASS 且无 scope 漂移。
