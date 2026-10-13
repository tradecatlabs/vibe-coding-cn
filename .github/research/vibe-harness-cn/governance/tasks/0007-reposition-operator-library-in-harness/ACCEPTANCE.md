# Task-Level Acceptance
- PRD 明确 `Operator Library ⊂ Harness`，并解释它如何辅助 LLM/Agent。
- 共享 `OperatorSpec`、本地 `Operator Library`、`OperatorBinding` 和元 Harness 治理目录职责不重叠。
- Harness 组件树、执行流和元 Harness 控制流依赖方向一致。
- 既有权限、证据、失败、预算、验证和 provenance 约束未被削弱。
- 所有项目真相源同步且确定性门禁通过。

# Validation Plan
- Inspection：全仓扫描“独立语义层”“位于 Harness 执行之间”等旧边界残留。
- Structure：检查 PRD、HARNESS_MODEL、ADR、README/AGENTS、操作模型、拓扑和 module context。
- Commands：治理索引重建、strict validator、health report、principle scan 和项目 gates。
- Evidence：命令退出码、生成 artifact 与最终 `REVIEW.md`。

# Review Gate
- Correctness：组件归属与 Agent/Harness 定义一致。
- Architecture：规范治理和运行执行只有一个 owner。
- Security/Reliability：Operator 不扩权，执行者不自证成功，失败语义保留。
- Performance：不把完整算子库默认塞入上下文，检索目标仍为廉价预筛选。
- Ponytail：不新增平行规格、服务、Schema 或空抽象。

# Runtime Verification Gate
- `VERIFICATION_PLAN.json` 为 READY。
- 所有 REQUIRED capability 必须在最终输入上取得新鲜 PASS；NOT_APPLICABLE 只能来自计划条件。
- 本地主 Codex 自审不冒充外部独立 reviewer。

# Ship Readiness
- 文档和任务证据均完成且无占位符。
- 最终 diff 与 scope 一致，无 contracts/scripts/tests 行为变更。
- 选择性本地提交；无 remote 时明确不 push。
- 回滚使用反向提交；无数据或运行时迁移。

# Task Package Acceptance
## TP-01
- PRD 和 HARNESS_MODEL 的树与文字都显示 Operator Library 在 Harness 内。
- 核心对象增加共享规范、本地库存和执行 Binding 的清晰区分。

## TP-02
- ADR-0003 明确记录边界纠正及其原因。
- 根入口、目录说明、操作模型、拓扑和 module context 无冲突描述。

## TP-03
- 任务文档、治理严格校验和 required project gates 全部通过。
- REVIEW 记录 unknowns、性能检查、文档同步和无外部 reviewer 边界。

# Anti-Goals
- 不得把算子库再次建模为 Harness 外部独立执行平面。
- 不得把元 Harness 变成所有算子的业务执行 runtime。
- 不得把 Operator 简化成只有自然语言 prompt 的模板。
- 不得修改 contracts/scripts/tests 行为。
- 不得虚构证据
- 不得越权补全未确认信息
