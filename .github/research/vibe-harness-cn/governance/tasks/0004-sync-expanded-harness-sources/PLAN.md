# Planning Summary
目标终态是一份静态、可审计、revision 绑定的 official Harness registry，统一驱动 15 个 checkout 与 lock；第三方源码始终只是被忽略、可重建、不执行的研究缓存。本轮复用现有数据驱动同步器，只扩充用户指定来源及其事实，不把项目改造成在线 registry 或镜像服务。

# Lifecycle Gates
- `SPEC -> PLAN -> BUILD -> TEST -> REVIEW -> SHIP` 按序闭合，不得跳过 gate。
- SPEC：11 个 canonical repo、默认分支、许可证、核心路径和限制由实际来源确定。
- PLAN：安全拉取/inspection -> registry/docs/tests -> 15 源真实同步 -> review/ship。
- BUILD：只改 registry、lock、集合回归、研究/治理/目录文档与任务证据。
- TEST：离线状态机回归、真实同步幂等、checkouts/lock inspection、项目/治理门禁。
- REVIEW：correctness/security/reliability/performance/architecture/Ponytail/Future-Optimal/document drift。
- SHIP：当前分支选择性本地 commit；无 remote 不 push。

# Simplest Path
- Existence check：11 项由用户明确指定，且扫描已证明均具有真实 Harness 研究价值；来源条目应存在。
- Selected ladder rung：复用系统 Git、现有 `sync_upstreams.sh`、静态 JSON registry、Python 标准库与既有门禁。
- Why lower rungs failed：一次性 clone 无法让后续 sync/lock/研究重算；只写文档不能证明 revision 与源码边界。
- Skipped scope：不新增并发调度、数据库、镜像、submodule、GitPython、插件系统或额外来源。
- Ceiling / upgrade path：15 源已触发同步规模复核；先测量首次/重复同步耗时和磁盘，只有明确超预算才引入有界并发。
- Do-not-simplify：canonical origin、branch、dirty、ancestry、license、core-path、timeout、atomic clone 与 preview/migration limitation 不能删除。
- Minimal runnable check：真实同步成功；冻结 registry/checkout revision 后连续生成 lock 的 digest 与 `generated_at` 不变，15 个 checkout/lock/registry 一致。
- Target end state：单一 registry 拥有全部受治理官方来源定义，lock 只拥有 revision 事实，文档只解释证据边界。
- Real constraints：用户指定集合、官方迁移、许可证、GitHub 网络、磁盘、无上游执行、现有本地 checkout 安全。
- Inertia constraints：旧“4 源”硬编码文案和测试不得限制终态；实现成本不得迫使一次性 clone。
- Kill list：硬编码 `len == 4`、所有“四个来源”文案、旧 canonical URL、任何双清单。
- Proof point：15 源精确集合、真实 checkouts 与 lock 一致、幂等 digest、全部门禁 PASS。
- Falsifier：任一来源事实无法从当前 checkout 证明，或现有 schema 无法如实表达。
- Migration slice：只向既有 registry 增加 11 条实际核验 spec，并同步测试/文档。
- Rejected short-term patches：手工 clone 后不登记、为大仓库绕过 core path、把旧 URL 当 canonical、另建候选同步脚本。
- Complexity/Future-optimal review owner：`auto-review`。

# Split Strategy
- TP-01 先拉取并冻结外部事实，避免从宣传页猜目录或许可证。
- TP-02 只消费已核验事实，统一更新 registry、集合回归与文档。
- TP-03 对最终状态执行网络、性能、门禁、治理与 Git 交付收口。

# Execution Waves
- Wave 1：TP-01。
- Wave 2：TP-02。
- Wave 3：TP-03。

# Runtime Workflow Contract
- Graph mode：bypass atomic graph；三个串行叶子共享同一 registry/checkout 状态，拆成并行 worker 会增加冲突且本项目禁用原生子代理。
- 允许：公开 GitHub clone/fetch、Git/tree/license inspection、项目内任务范围编辑、Bash/Python 验证、本地 commit。
- 禁止：执行上游、凭据搜寻、原生子代理、reset/clean/stash/强制 checkout、push/部署。
- 停止条件：来源/许可证/路径/非 FF/磁盘/网络/required gate 任一错误立即非零停止；结构性失败更换路径，不重复撞同一命令。

# Next Executable Leaves
- TP-01。

# Dependency Graph
```text
TP-01 -> TP-02 -> TP-03
```

# Rollback Protocol
- 恢复 `INDEX.md` 当前任务行
- 使用反向 commit 移除 11 个登记及关联文档/测试，不改写历史。
- checkout 是 ignored、可重建缓存；不得用 destructive Git 清理任何有本地状态的目录。
- 来源事实变化时保持 BLOCK，核验后更新 registry/lock，而不是保留错误 URL 或路径。
