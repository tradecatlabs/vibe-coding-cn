# Task-Level Acceptance
- 三个官方 checkout 的 origin、登记分支与 lock commit 完全一致。
- OpenCode/Codex 被标记为核心源码公开；Claude Code 被标记为官方公开仓库但无 CLI 核心源码。
- 同步脚本可重复运行，普通浅克隆前进通过，脏工作树/错误分支/真实改写明确拒绝。
- 上游源码不进入项目历史、不被执行，lock 和研究边界进入项目真相源。
- 文档、governance、Task Intent、回归证据与 high-risk required capability 均通过当前输入验证。

# Validation Plan
1. `bash tests/test_sync_upstreams.sh`：本地、无网络地验证 Git 状态机。
2. `bash scripts/sync_upstreams.sh`：对三个真实官方仓库执行同步并刷新 lock。
3. 连续重跑同步并比较 `sha256sum research/upstreams.lock.json`：证明 revision 未变时 lock 不漂移。
4. `python3 scripts/verify_project.py --gate <capability>`：执行项目 policy 的 required gates。
5. governance rebuild、strict validate、health 与 task docs/回归 owner validator 收口。

# Review Gate
- Correctness：origin/branch/commit、shallow ancestry 与计数语义正确。
- Security：不执行上游内容、不获取凭据、不覆盖本地修改、第三方源码 gitignored。
- Reliability：真实前进与拒绝路径有本地回归；网络/结构失败非零退出。
- Architecture：checkout/cache、lock、研究文档和治理边界分离；artifact 不绑定历史任务。
- Performance：默认浅克隆，有界 deepen，无无限循环或无界并发。
- Documentation：根/目录 AGENTS、研究基线、操作模型、工具链、topology/context map 同步。

# Runtime Verification Gate
- Task Intent 风险：high；required capability 由项目 policy 编译，不允许手工降级。
- 结果必须绑定当前 Git 输入摘要与 `governance/runtime/verification-artifacts/` 的真实 artifact。
- capability 缺失、BLOCK、artifact digest 不符或输入变更时 closeout 必须 BLOCK。

# Ship Readiness
- 交付形态：本地 commit 与可重跑命令；仓库没有 remote，因此没有 push/PR/CI 事实。
- 回滚：checkout 可重建，跟踪文件通过反向 commit；真实远端改写保持人工门禁。
- 观察项：官方 owner/branch/license/source visibility 变化、max-deepen 触顶、同步 p95 与磁盘占用。

# Task Package Acceptance
## TP-01
- 三个 URL 属于官方 owner，分支和许可证来自实际 checkout；Claude 限制有文件级证据。

## TP-02
- 一条命令完成 clone/update/lock；同 revision 重跑不改变 lock；checkout 被 ignore。

## TP-03
- DEBUG 根因成立；最终测试在 RED、GREEN、counterfactual 三阶段满足 owner 契约。

## TP-04
- governance/task/project gates 对当前输入新鲜；review 无未处理 BLOCK，剩余 unknown 明示。

# Anti-Goals
- 不执行、构建、安装或修改上游代码。
- 不以 fork、README 推断或本机二进制补齐未公开源码。
- 不使用 reset、clean、stash、强制 checkout 或删除重克隆掩盖同步问题。
- 不把本地确定性门禁声称为外部独立审查或生产就绪证明。
