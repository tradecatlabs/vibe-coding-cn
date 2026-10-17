# Acceptance Checklist

# Global Standards

- [x] 未来终态（fork 级授权审计）与当前差距（管线未成型）已明确记录。
- [x] 新增长期对象（COMBAT_READINESS.md）通过存在性检查：就绪度需持续复查。
- [x] 成熟工具优先；本轮零代码、零新依赖。
- [x] 网络副作用为零；无公网目标动作，无 git 远端操作。

# Task Package Checklists

### TP-01

- [x] 现状盘点覆盖任务/工具/靶场/控制面/skills，每项绑定证据。
- Verify: INDEX.md、ADMISSION_TABLE.md、web3-lab/evidence、SKILLS_MANIFEST.json。
- Gate: 证据与 2026-08-14 现场核实一致。

### TP-02

- [x] COMBAT_READINESS.md 含能力域评分、综合得分、P0/P1/P2 差距清单与 M1-M4 路径。
- Verify: `governance/context/COMBAT_READINESS.md`。
- Gate: 每项得分绑定现状证据与权重说明，无虚构数据。

### TP-03

- [x] 拓扑/操作模型/上下文地图/README/任务索引/tasks-AGENTS 六处同步完成。
- Verify: 各文件 diff 与 INDEX.md 任务行。
- Gate: 无死链、无占位符、无重复 ID。

### TP-04

- [x] closeout 校验与 governance strict/health 全绿。
- Verify: validate_task_docs / validate_tasks_tree / strict / health 输出。
- Gate: 无占位、死链或过度声明。
