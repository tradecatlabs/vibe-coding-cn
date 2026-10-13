# Task-Level Acceptance
- 11 个新增 checkout 均来自 canonical official GitHub origin、实际默认分支，工作树 clean，且 HEAD 与 lock 一致。
- registry 与 lock 最终恰好包含 15 个唯一来源；用户本轮列出的 11 项全部存在且无额外研究样本混入。
- 每个新增条目有实际许可证 marker、核心源码路径、文件计数和必要 limitation；不得从 README 宣传推断未公开实现。
- 网络同步成功；在 registry 与 checkout revision 冻结时连续生成 lock digest 不变。官方 HEAD 在两次网络同步间真实前进时，lock 必须更新而不能伪装幂等；非法 registry、脏树、错误分支/origin 与非 FF 仍被拒绝。
- 项目 capability、governance strict/health、task closeout 与自审无 BLOCK。

# Validation Plan
- Source inspection：逐项比较 registry、origin、branch、HEAD、LICENSE、core paths 与 clean 状态。
- Offline regression：`bash tests/test_sync_upstreams.sh`，覆盖 15 源集合与既有 Git 状态机拒绝路径。
- Real sync：运行 `bash scripts/sync_upstreams.sh`；随后在同一 registry/checkout revision 上连续生成 lock，比较 SHA-256 与 `generated_at`。
- Project gates：architecture、behavior、contract、rollback、security、test 全部执行。
- Governance/task：重建索引，运行 strict/health 与 task docs validators。

# Review Gate
- correctness：11 项与用户清单一一对应，canonical 迁移和来源元数据准确。
- readability：registry 条目字段一致，文档按架构类别解释差异，不堆宣传文案。
- architecture：复用现有 registry/sync/lock；无第二真相源、无逐仓库专用代码。
- security/reliability：不执行上游、无凭据、fail-closed、原子 clone、超时与本地现场保护不退化。
- performance：记录 15 源首次/重复同步耗时、磁盘规模与网络瓶颈；无证据不引入并发复杂度。
- Ponytail/Future-Optimal/document drift：新增对象、终态、天花板、proof/falsifier 与文档归属均复核。

# Runtime Verification Gate
- Task Intent 与 Verification Plan 必须为 READY。
- medium 风险 required capability 缺失、ERROR、非 PASS 或 stale evidence 时 fail closed。
- 外部 reviewer/CI 不存在时只能声明本地确定性 PASS。

# Ship Readiness
- 选择性 stage 当前任务所有文件，确认 checkout 与 runtime 证据继续 ignored。
- 本地 commit 后在新 HEAD 上复跑关键回归与门禁。
- 无 remote 时不 push，并明确远端/CI/PR/独立 reviewer 均不在本次证据内。
- 回滚使用反向 commit；不得 reset/clean 用户现场。

# Task Package Acceptance
## TP-01
- Verify：11 个 checkout 的 `remote get-url`、`branch --show-current`、`rev-parse HEAD`、LICENSE 与 core path inspection。
- Gate：事实均绑定实际 revision；不一致即 BLOCK。

## TP-02
- Verify：JSON parse、registry 集合回归、`bash -n`、`bash tests/test_sync_upstreams.sh`。
- Gate：15 源由同一 registry 驱动同步与 lock，无重复/遗漏。

## TP-03
- Verify：sync twice、lock/checkouts inspection、六 capability、governance/task validators、post-commit smoke。
- Gate：当前输入无 BLOCK，工作树 clean，本地 commit 可追踪。

# Anti-Goals
- 不得修改任务范围以外路径
- 不得虚构证据
- 不得越权补全未确认信息
- 不得执行上游代码或引入用户未列入本轮的额外来源
