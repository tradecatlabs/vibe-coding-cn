# Planning Summary
目标终态是：每个 Harness 内部都可包含 Operator Library，为 LLM 提供可选择、可组合的问题求解方法；
元 Harness 维护共享 Operator 规范、治理目录、分发、conformance、eval 和生命周期，不成为算子执行运行时。

- Target end state：`Agent = LLM + Harness`，Harness 内含 Operator Library 与其 selector/materializer/bindings。
- Real constraints：权限必须由 Harness policy 裁决；业务状态留在具体 Harness；证据必须可独立裁决。
- Inertia constraints：现有“独立语义层”文案和 PSOA 工作名不能决定真实组件边界。
- Wrong boundary：把 Operator Library 画在 Harness 外部，并让 Planner/Verifier 看起来都是外置平台。
- Kill list：外部独立 Operator 执行平面、双运行状态 owner、把本地库存等同中央治理目录。
- Proof point：共享 `OperatorSpec` 可被两个 Harness 以不同 `OperatorBinding` 使用。
- Falsifier：跨 Harness 复用必须共享内部运行时，或规范无法表达本地 Binding 差异。

# Lifecycle Gates
1. SPEC：冻结用户纠正后的归属和所有权。
2. PLAN：列出受影响真相源和不变约束。
3. BUILD：只修订现有文档，不实现新运行时。
4. TEST：执行术语扫描、治理校验和项目 gates。
5. REVIEW：检查架构、正确性、复杂度、安全、性能与文档漂移。
6. SHIP：选择性提交；无 remote 不 push。

任何 gate 不得跳过；未取得对应证据时任务保持 In Progress 或 Blocked。

# Simplest Path
- Existence check：这次纠偏必须存在，否则后续 Schema 会固化错误所有权。
- Selected ladder rung：project-native capability；直接修订现有 PRD、ADR 和上下文，不新增平行规格。
- Skipped scope：Schema、实现、运行时、服务、数据存储和批量算子。
- Ceiling / upgrade path：文档通过后，以首批算子和两个 Harness Binding 验证；失败再修改抽象。
- Do-not-simplify：权限、证据、失败、预算、版本和 provenance 边界。
- Minimal runnable check：治理 strict + architecture/behavior/contract/test gates。

# Split Strategy
- TP-01 先修领域真相，避免导航反向定义架构。
- TP-02 再同步所有长期引用，避免文档漂移。
- TP-03 最后独立检查最终 diff 和验证证据。

# Execution Waves
- Wave 1：TP-01
- Wave 2：TP-02
- Wave 3：TP-03

# Runtime Workflow Contract
- 这是串行文档任务，不创建原子执行图，不调用子代理，不产生外部运行时副作用。
- 每个波次只消费前一波次已稳定的文档结论；失败时只重开受影响文档切面。

# Next Executable Leaves
- 无；全部 task package 已完成。

# Dependency Graph
```text
TP-01 -> TP-02 -> TP-03
```

# Rollback Protocol
- 通过新的反向提交恢复上一版文档，不使用破坏性 Git 操作。
- 若语义修正被真实双 Harness proof 证伪，重新打开 PRD/ADR，而不是增加兼容层。
- 不触碰 contracts、runtime 数据或其他任务目录，因此无需数据迁移回滚。
