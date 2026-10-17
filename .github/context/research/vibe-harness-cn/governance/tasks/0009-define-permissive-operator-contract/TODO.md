# Execution Checklist
[x] TP-01 | P0 | 定义宽松核心与 Profile 边界 | Verify: 检查规范覆盖 Core、Profile、extensions、兼容性和安全边界 | Gate: 任何字段强制项都能由互操作或安全必要性解释 | Parallelizable: No
[x] TP-02 | P0 | 放宽 Schema 并标注参考库 Profile | Verify: 运行 JSON Schema 自校验和既有 7 个 pack 校验 | Gate: 既有内容兼容，最小自定义领域 pack 可通过，未知稳定字段被拒绝 | Parallelizable: No
[x] TP-03 | P0 | 实现 Core 与 Reference 回归 | Verify: 运行 --operator-pack、--operator-library 与 --self-test | Gate: Core 正例通过、结构负例拒绝、Reference 75+7 回归通过 | Parallelizable: No
[ ] TP-04 | P0 | 同步文档治理并完成验证 | Verify: 运行 project gates、governance strict/health、task docs 与 Git 输入检查 | Gate: 没有文档漂移或未解释的长期约束 | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
- TP-04 的产品文档与确定性门禁已完成；仅因 owner 要求的高风险 retrospective 缺少外部受信评审，不能完成 task closeout。
