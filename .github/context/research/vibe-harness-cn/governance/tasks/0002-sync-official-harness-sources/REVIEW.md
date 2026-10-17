# Official Harness Sources Review

## Verdict

- Decision: `WARN`
- Review depth: `deep`
- Target: 本地实现与 deterministic merge gate；不是外部独立 review 或生产供应链认证。
- Provenance: 当前主 Codex 自审；没有仓库外 reviewer、remote、PR 或 CI provenance。

实现级 BLOCK 已收敛：三个来源固定官方 origin/branch，第三方 checkout 被忽略且从不执行；
浅克隆只在工作树干净后有界深化并证明 ancestry，真实改写保持 BLOCK；lock 现场断言许可证、
公开路径和 revision，Claude Code 负面可见性结论绑定 assessment commit。

## Profiles And Audit Cases Consumed

- Profiles: correctness、security、reliability、performance、architecture、repo-hygiene、
  test-quality、ponytail-complexity、future-optimal-drift、document-drift、completion-verification。
- `CASE-0003`：TODO/STATUS/closeout 只能在最终新鲜验证后改为 Done。
- `CASE-0004`：研究白名单为三个官方仓库；禁止 fork、安装目录与未公开实现推断。
- `CASE-0005`：复用 Git/bash/Python stdlib；未自研 clone、Git 图或专业分析器。
- `CASE-0006`：无交互回调、数据库冷查询或在线请求路径，不适用。
- `CASE-0007`：无可选运行依赖；系统 Git/timeout/Python 是显式前置，缺失即 BLOCK。

## Resolved Findings

### RESOLVED-001：depth=1 普通前进被误判为不相关历史

- Severity: `BLOCK -> RESOLVED`
- Evidence: `DEBUG.md` 记录 Codex `781445f -> 990218b` 症状与最小 deepen 实验。
- Fix: 有界指数 deepen 后证明 `HEAD` 是 `FETCH_HEAD` 祖先，才允许 `merge --ff-only`。
- Verification: 最终 RED/GREEN/counterfactual owner contract 与本地 Git 回归。

### RESOLVED-002：同步可能覆盖本地研究现场

- Severity: `BLOCK -> RESOLVED`
- Fix: origin、登记分支、detached HEAD、tracked/untracked/ignored 文件全部预检；不使用 reset。
- Verification: 测试证明拒绝路径不改变本地 HEAD。

### RESOLVED-003：静态来源标签可能在上游变化后继续假装新鲜

- Severity: `BLOCK -> RESOLVED`
- Fix: lock 生成时现场断言许可证 marker 与公开路径；Claude 的负面可见性结论绑定
  `visibility_assessment_commit`，新 revision 自动降级为 `requires-manual-review`。
- Verification: 真实三仓同步、lock JSON 与 checkout origin/branch/HEAD 一致性检查。

### RESOLVED-004：项目 gate artifact 绑定历史任务

- Severity: `WARN -> RESOLVED`
- Fix: capability registry 和 runner 改用被忽略的 `governance/runtime/verification-artifacts/`，
  历史 `0001` 证据保持不变。
- Verification: 六个 gate 均写入项目 runtime 固定路径。

## Remaining Warnings

### WARN-001：没有外部独立 provenance

- Impact: 本地结果可证明命令和 revision 一致，不能证明 reviewer 身份独立或 GitHub 仓库身份经过签名认证。
- Follow-up: 配置 remote/CI/外部 reviewer 后，对固定 review HEAD 生成平台证明。

### WARN-002：Claude Code CLI 核心实现仍不可审计

- Impact: 只能比较官方公开扩展面与行为资料，不能做核心 loop/permission/session 源码等价比较。
- Follow-up: 若官方仓库 revision 变化或公开核心源码，重新做可见性评估；不得从 fork 补齐。

## Performance And Cost

- Complexity: Git 网络/磁盘 `O(B + F)`；`B` 为对象字节，`F` 为 tracked file 数；lock 内存为 `O(1)` 个来源记录。
- Hot path: GitHub clone/fetch，而非 JSON 生成。
- Immediate: depth=1、按需有界 deepen、300 秒网络超时、首次 clone 原子落位、lock 内容不变不重写。
- Concurrency: 同一 checkout 根由系统 `flock` 非阻塞互斥；不使用自研锁、忙等或无界等待。
- Measure later: 仓库数达到 10+ 或同步 p95 超预算时，再评估受限并发；当前串行便于 fail-fast。
- Avoid: 无界并发、无限 deepen、全量 clone、数据库/服务化和自研 Git 图算法。

## Gate Conclusion

- 本地同步、revision lock、研究边界与回归证据：可进入 checkpoint commit。
- 正式供应链认证、外部 merge/release/production readiness：`NOT ESTABLISHED`。
