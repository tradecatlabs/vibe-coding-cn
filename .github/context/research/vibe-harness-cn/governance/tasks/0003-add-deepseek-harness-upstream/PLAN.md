# Planning Summary
目标终态是一个登记源定义全部官方 Harness 上游，系统 Git 负责安全同步，Python 标准库负责校验与生成 revision lock；研究 checkout 始终只是被忽略、可重建、不可执行的外部输入缓存。本轮只加入 DeepSeek Harness 并消除第四源触发的双清单漂移，不扩展成服务或插件框架。

# Lifecycle Gates
- `SPEC -> PLAN -> BUILD -> TEST -> REVIEW -> SHIP` 必须按序闭合，不得跳过 gate。
- SPEC：官方来源、分支、许可证、核心路径、preview 限制和行为验收确定。
- PLAN：单一登记源 -> 薄同步 -> lock -> 回归 -> 真实拉取 -> 验证/交付。
- BUILD：只修改 registry、同步脚本、测试、研究/治理文档。
- TEST：语法、离线回归、真实四源同步、幂等和项目门禁。
- REVIEW：correctness/security/reliability/performance/architecture/document drift。
- SHIP：选择性本地 commit；无 remote 时明确停止在本地交付。

# Simplest Path
- Existence check：DeepSeek Harness 是用户明确要求且官方确认的真实第四个 Harness，上游条目必须存在。
- Selected ladder rung：复用系统 Git、bash、Python 标准库和现有同步入口；新增一个机器 source registry 作为两处重复定义的单一真相源。
- Why lower rungs failed：继续在 shell/Python 两处复制第四项会形成可复发漂移；一次性 clone 无法生成 revision 与验证证据。
- Skipped scope：不新增数据库、service、plugin、GitPython、并发调度或供应链框架。
- Ceiling / upgrade path：10+ 仓库或 p95 同步超预算后，再基于测量评估受限并发和更强 schema。
- Do-not-simplify：origin/branch/dirty/ancestry/license/core-path/timeout/atomic clone 校验不能删除。
- Minimal runnable check：连续两次 `bash scripts/sync_upstreams.sh` 成功，第二次 lock digest 不变。

# Split Strategy
- TP-01 先固定外部事实，避免从宣传文案猜路径。
- TP-02 在一个变更切片中同步实现、测试与真相源文档，防止中间漂移。
- TP-03 只消费最终实现做真实网络验证和交付，失败时不回写成功状态。

# Execution Waves
- Wave 1：TP-01。
- Wave 2：TP-02。
- Wave 3：TP-03。

# Runtime Workflow Contract
- Graph mode：bypass atomic graph；三个叶子严格串行，副作用边界清楚。
- 允许：官方 GitHub clone/fetch、checkout 只读检查、项目文件编辑、bash/Python 验证、本地 commit。
- 禁止：执行上游代码、原生子代理、凭据搜寻、reset/clean/stash/强制 checkout、push/部署。
- 停止条件：任何来源、布局、许可证、非 FF、测试或 required gate 错误立即非零停止。

# Next Executable Leaves
- TP-01：核验官方 checkout 的实际树、许可证和 revision。

# Dependency Graph
```text
TP-01 -> TP-02 -> TP-03
```

# Rollback Protocol
- tracked 变更使用反向 commit 回滚，不改写已提交历史。
- checkout 是可重建缓存；脚本不得自动删除或 reset 有现场的 checkout。
- 来源或 preview 边界变化时保持 BLOCK，人工核验后再更新 registry/lock。
