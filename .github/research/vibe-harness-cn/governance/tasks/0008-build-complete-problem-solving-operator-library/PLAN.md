# Planning Summary
目标终态：共享算子内容以供应商中立 JSON 发布；每个 Harness 可装载同一 Spec 并提供自己的 Binding；本仓库用 source inventory 和 conformance validator 保证内容完整、结构合法、引用可解析。

- Target end state：独立 inventory、catalog、typed packs、Schema、validator、tests 和文档形成单向依赖。
- Real constraints：必须覆盖全部 75 项；复用现有 jsonschema/uv；权限仍归 Harness；不执行外部代码。
- Inertia constraints：现有目录只有 Harness manifest，不能成为把 operator 字段塞回 manifest 的理由。
- Wrong concept：把所有内容做成 prompt 列表，或用 7 个摘要 Method 替代 75 项逐项建模。
- Kill list：手工计数、自由文本无类型对象、中央 runtime、未解析引用、无来源条目。
- Proof point：有效库报告 75/75 + 7/7；四类关键负例全部 BLOCK。
- Falsifier：Schema 不能区分视角/动作/组合，或覆盖只能靠人工解释。
- Migration slice：本轮交付静态库与离线 conformance；运行选择和 Binding 留给后续双 Harness proof。
- Rejected short-term patches：不只写 Markdown 清单；不只生成一个大 JSON 而没有独立 inventory 和 validator。

# Lifecycle Gates
1. SPEC：冻结 75 项清单、7 项派生 Method、字段语义与非目标。
2. PLAN：固定目录、依赖、验证和回滚。
3. BUILD：先 Schema/inventory，再 packs，再 validator/tests。
4. TEST：运行正反例、精确覆盖和项目 gates。
5. REVIEW：检查内容完整性、架构、安全、复杂度、性能与文档漂移。
6. SHIP：选择性本地提交并在 clean HEAD 复验。

任何 gate 不得跳过；缺少新鲜证据时不得声明 Done。

# Simplest Path
- Existence check：机器可读算子库是当前明确需求，且 PRD 已把它列为下一实现切片。
- Selected ladder rung：project-native + one direct implementation；复用 JSON Schema/jsonschema/现有 validator 入口，只新增必要数据、Schema 和薄校验模块。
- Why lower rungs failed：Markdown 或现有 Harness manifest 无法表达逐项类型、覆盖和跨引用。
- Skipped scope：selector、planner、Binding SDK、服务、数据库、UI、模型 eval。
- Ceiling / upgrade path：两个真实 Harness 重复装载/绑定逻辑时再抽 Binding SDK；离线文件无法满足查询时再评估 registry。
- Do-not-simplify：75 项 exact coverage、类型语义、路径安全、ID/reference、权限和证据边界。
- Minimal runnable check：`uv run --locked --script scripts/validate_harness.py --operator-library operators/catalog.json`。
- Complexity review owner：auto-review ponytail-complexity + performance。

# Split Strategy
- TP-01 固定结构后，TP-02 才能批量制作内容，避免先写数据再改语义。
- TP-03 消费稳定内容建立反例；TP-04 只根据真实路径同步文档。
- TP-05 在最终输入上重跑门禁并交付。

# Execution Waves
- Wave 1：TP-01。
- Wave 2：TP-02。
- Wave 3：TP-03。
- Wave 4：TP-04。
- Wave 5：TP-05。

# Runtime Workflow Contract
- 单主 Agent 串行执行，不创建原生 subagent。
- 每一波只消费前一波稳定输出；Schema 或 inventory 改变时，pack 与测试证据全部失效并重跑。
- 允许工具：只读检索、apply_patch、项目脚本、测试和非破坏性 Git。
- 禁止动作：执行上游 Harness、联网安装依赖、读取凭据、破坏性 Git、部署或 push。

# Next Executable Leaves
- 无；产品叶子均已完成，TP-05 等待全局 `auto-retro` registry 恢复可验证状态。

# Dependency Graph
```text
TP-01 -> TP-02 -> TP-03 -> TP-04 -> TP-05
```

# Rollback Protocol
- 使用反向提交撤销本任务，不执行 reset/checkout/clean。
- Schema 和数据尚未成为公共发布版本；无需双轨兼容或数据迁移。
- 若 75 项映射被证伪，修订 inventory 版本并让 validator 强制所有 pack 同步。
