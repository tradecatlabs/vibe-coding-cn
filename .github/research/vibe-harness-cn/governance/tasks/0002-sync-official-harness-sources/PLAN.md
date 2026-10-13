# Planning Summary
正确终态不是把第三方源码变成本项目代码，而是把官方上游当成版本化、可重取、默认不可信的
研究输入：checkout 是缓存，revision lock 是机器事实，研究文档声明证据边界。

- Target end state：登记来源 -> 安全同步 -> revision lock -> revision 绑定研究结论。
- Real constraints：官方 origin、许可证、浅克隆语义、本地研究改动、Claude 核心源码不可见。
- Inertia constraints：首次人工 clone 方式和旧 `0001` artifact 路径不是公共契约。
- Wrong boundary：第三方源码不属于本项目 source tree；项目只拥有同步策略和元数据。
- Kill list：手工 clone 清单、submodule/subtree/vendoring、自动 reset、把插件仓库冒充核心源码。
- Proof point：真实三仓同步成功，lock 可复算，本地 Git 拒绝路径与反事实证据通过。
- Falsifier：同步必须执行上游代码或覆盖本地修改才能维持，说明当前边界错误。
- Migration slice：官方来源核验 -> ignored checkout + lock -> 回归加固 -> 治理/验证。
- Short-term patches rejected：失败时删除重克隆、无条件 reset、无限 deepen、只在聊天报告 commit。

# Lifecycle Gates
`SPEC -> PLAN -> BUILD -> TEST -> REVIEW -> SHIP` 均绑定当前输入，不得跳过任何 gate。
- SPEC：Task Intent READY，来源/可见性边界明确。
- PLAN：四个语义叶子、依赖、回滚与性能上限明确。
- BUILD：同步入口、lock、研究/治理文档和测试。
- TEST：本地 Git 回归、真实上游同步、JSON/Shell/Python、项目六门禁。
- REVIEW：source authenticity、reliability、security、Ponytail、future-optimal、document drift。
- SHIP：本地 commit；当前无 remote，不声称 push/PR/发布。

# Simplest Path
选择“标准 Git + bash 编排 + Python 标准库写 lock”。Git 负责 clone/fetch/ancestry/FF，Python 只连接
元数据输出；不引入 GitPython、供应链框架、数据库、服务或插件系统。

存在性与工程阶梯：
- `research/` 应存在：隔离外部输入及其人类/机器证据，不混入产品源码。
- 同步脚本应存在：三源动作可重复且含防覆盖分支，一次性命令无法保存不变量。
- 回归测试应存在：浅边界、历史改写与脏工作树是非平凡 Git 分支。
- 最低阶梯：系统 Git + bash + Python stdlib；没有成熟依赖引入理由。
- Ceiling：每仓最多有界深化 4096 commits；超过上限人工核验，不自动 unshallow/reset。

# Split Strategy
- TP-01 先固定外部事实，避免从项目名称猜仓库或源码范围。
- TP-02 把一次性动作变为机器可重算输入。
- TP-03 由真实失败驱动，不把 Git shallow 误差变成删除重克隆脚本。
- TP-04 等实现与调试收敛后统一校验文档、策略和交付状态。

# Execution Waves
- Wave 1：TP-01。
- Wave 2：TP-02。
- Wave 3：TP-03。
- Wave 4：TP-04。

# Runtime Workflow Contract
- Graph mode：bypass atomic graph；四个叶子严格串行、输出清晰、无并行生产副作用。
- 允许工具：Git 只读/clone/fetch/FF、本地文件编辑、bash/Python 验证、官方网页检索。
- 禁止动作：执行上游代码、原生子代理、reset/clean/stash/强制 checkout、push、部署、凭据搜寻。
- 失败策略：首个 origin/branch/worktree/ancestry/gate 错误非零退出；不得静默跳过某个仓库。

# Next Executable Leaves
- TP-04：运行真实同步幂等、项目 capability、治理健康与收口 review。

# Dependency Graph
```text
TP-01 -> TP-02 -> TP-03 -> TP-04
                  TP-02 ----^
```

# Efficiency and Optimization
- 复杂度：同步网络/磁盘成本为 `O(B + F)`，`B` 是拉取对象字节数，`F` 是 tracked file 数；额外内存为 lock 元数据规模。
- Hot path：GitHub 网络 fetch 与首次 checkout；不是 Python JSON 生成。
- 立即值得做：depth=1、按需有界深化、网络超时、`flock` 互斥、首次 clone 原子落位、内容不变时不改写 lock。
- 需要数据再做：仓库数量达到 10+ 或 p95 同步超过预算后再考虑受限并发与 manifest 驱动。
- 暂不优化：三个仓库串行同步便于 fail-fast 与清晰审计；并行收益不足以承担输出/失败协调复杂度。
- 验证指标：每次 fetch 数、下载字节/耗时、checkout 磁盘占用、lock digest 和失败原因。

# Rollback Protocol
- checkout 为可重建缓存；删除单个干净 checkout 后可从 lock URL/branch 重新 clone，但脚本不会自动删除。
- 跟踪文件回滚使用反向 commit 或选择性恢复，不执行 reset/checkout/clean。
- 若上游真实历史改写或迁移 owner，保持 BLOCK，人工核验并显式更新登记与 lock。
- 本任务不修改外部仓库、不 push，无远端回滚动作。
