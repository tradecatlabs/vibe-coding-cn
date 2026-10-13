# Execution Checklist
[x] TP-01 | P0 | 冻结 PSOA 需求、语义边界、对象模型、MVP 与验收 | Verify: 检查 PRD 必需章节和编号需求 | Gate: 需求可供后续契约任务消费且未冒充实现 | Parallelizable: No
[x] TP-02 | P0 | 同步 ADR、docs context、项目入口、操作模型和拓扑 | Verify: 检查所有导航与 owner 边界 | Gate: 长期真相一致且 Harness manifest 未改变 | Parallelizable: No
[x] TP-03 | P0 | 完成 review、严格校验、复用采样和本地交付 | Verify: validators、project gates、Git diff/commit | Gate: 当前输入全部 required gate PASS 且无越界文件 | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
