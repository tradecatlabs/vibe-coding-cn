# Planning Summary

目标终态是一个独立于研究排名的供应链生命周期：研究目录只提供事实，准入目录持有采用决策，未来 artifact registry 才持有已验证版本。当前迁移切片只建立准入目录，不安装工具。

# Lifecycle Gates

以下 Gate 不得跳过；任一 Gate 失败必须保持非完成状态，并保留可归因错误。

1. SPEC：明确状态机、八个门禁、默认禁用和失效语义。
2. PLAN：按 W0 信任/数据、W1 本地只读、W2 隔离主动、W3 扩面编排。
3. BUILD：建立 JSON 真相源、标准库校验器和生成表。
4. TEST：跨目录覆盖、状态、版本、风险和确定性校验。
5. REVIEW：禁止把候选状态声称为已纳入。
6. SHIP：只交付本地治理资产，不提交、不推送、不安装。

# Simplest Path

- 复用 0001 的 18 项 MVP，不另建第二份工具事实。
- 使用一个 JSON 决策 overlay 和一个 Python 标准库校验器。
- 不创建数据库、插件框架、包管理器封装或运行时适配器。

# Split Strategy

- TP-01 先固定准入语言和安全边界。
- TP-02 将研究 MVP 全量映射到准入波次。
- TP-03 建立机械完整性和 fail-closed 校验。
- TP-04 同步长期项目真相并验证 closeout。

# Execution Waves

```text
Task execution: TP-01 -> TP-02 -> TP-03 -> TP-04
Future admission: W0 -> W1 -> W2 -> W3
```

# Runtime Workflow Contract

- Allowed：读取 0001 JSON、编辑治理/任务 Markdown/JSON/Python、运行本地校验。
- Forbidden：下载、安装、远程 API、扫描、选择或猜测具体版本。
- Evidence：校验命令退出码、生成表摘要、任务和治理 strict 结果。
- Stop：研究目录血缘不一致、active-high 进入候选、候选默认启用或 admitted 缺门禁。

# Next Executable Leaves

无。本任务已完成；下一任务从 W0 选择一个固定 schema/数据快照和 Cosign trust policy 做真实验证。

# Dependency Graph

```text
0001 research catalog
  -> 0002 admission overlay
  -> deterministic candidate view
  -> future artifact pin/verification tasks
```

# Rollback Protocol

删除 0002 准入任务并恢复 README/AGENTS/操作模型中的 0002 入口即可；0001 研究事实不受影响，没有外部资源或运行时状态需要回滚。
