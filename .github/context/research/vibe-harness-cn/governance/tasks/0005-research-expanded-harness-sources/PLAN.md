# Planning Summary
目标终态是研究/UPSTREAMS.md 之外的一份 revision 绑定、源码可追溯的 Harness 研究报告，把 11 个新增 Harness 的循环、工具、会话、权限、沙箱与扩展机制压缩成可比较事实，并回写领域模型。研究只读 checkout，不执行上游，不改 registry。

# Lifecycle Gates
- SPEC -> PLAN -> BUILD -> TEST -> REVIEW -> SHIP 按序闭合，不得跳过任何 gate。
- SPEC：11 个 Harness 的研究维度与证据契约由本 PLAN 固定。
- BUILD：逐仓提取事实 -> 横向比较 -> 回写领域文档。
- TEST：文档校验、治理 strict/health、registry/lock/checkouts 一致性。
- REVIEW：source evidence、宣传/实现差异、元 Harness 借鉴边界。
- SHIP：选择性本地 commit；无 remote 不 push。

# Simplest Path
- Existence check：研究报告应存在，因为 15 源研究基线需要可复核的逐仓事实；不创建新框架。
- Selected ladder rung：复用现有 Markdown、lock JSON 与治理校验工具；零新依赖。
- Skipped scope：不做适配器、不跑上游、不生成 Per-Harness 数据库。
- Ceiling / upgrade path：当 15 个以上 Harness 或需要机器查询时，再评估结构化 registry 扩展。
- Minimal runnable check：报告中的每个 Harness 小节都可从 `research/upstreams/<name>/` 相对路径复核。
- Target end state：一份研究真相源 + 领域模型借鉴 + 可重跑校验。
- Real constraints：只读 checkout、无凭据、无执行、revision 绑定。
- Kill list：把 README 宣传当事实、把相邻仓库能力算进当前 checkout、无限扩展报告篇幅。
- Proof point：11 个 Harness 各维度结论均可溯源。
- Falsifier：任一结论缺源码或 lock 证据。
- Migration slice：先 Pi/OpenClaw/Goose 三仓深读校准格式，再批量完成其余 8 仓。
- Rejected short-term patches：不建第二份来源登记，不复制 checkout。

# Split Strategy
- TP-01 逐仓调研。
- TP-02 横向比较与治理借鉴。
- TP-03 文档同步、门禁与交付。

# Execution Waves
- Wave 1：TP-01（三仓校准 + 八仓批量）。
- Wave 2：TP-02。
- Wave 3：TP-03。

# Runtime Workflow Contract
- 允许：读取 checkout 文本、rg/find 检索、项目内文档编辑、治理校验、本地 commit。
- 禁止：执行上游、凭据、原生子代理、reset/clean/stash、push/部署。
- 停止条件：发现需要执行上游才能确认的事实，降级为文档级证据并记录。

# Next Executable Leaves
- TP-01。

# Dependency Graph
```text
TP-01 -> TP-02 -> TP-03
```

# Rollback Protocol
- 恢复上一个 commit；新增报告与文档用反向 commit 移除。
- checkout 是 ignored 可重建缓存，不用 destructive Git 清理。
