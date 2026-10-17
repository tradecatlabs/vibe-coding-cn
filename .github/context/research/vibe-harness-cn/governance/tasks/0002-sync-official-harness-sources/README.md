# Task Overview
- Task ID: `0002`
- Slug: `sync-official-harness-sources`
- Objective: `从官方 GitHub 同步 OpenCode、Codex、Claude Code，固定 revision 与源码可见性，并修复浅克隆强制更新恢复路径`
- Status: `Done`

## In Scope
- 核验并同步三个官方 GitHub origin 与登记分支。
- 保存精确 revision、许可证、核心路径、文件计数、源码可见性和限制。
- 为浅克隆前进、脏工作树、错误分支与真实远端改写建立 fail-closed 行为。
- 同步目录自述、研究基线、项目操作模型、工具链、module context 与验证能力。

## Out of Scope
- 执行、安装、构建或修改任何上游仓库代码。
- 把第三方 checkout、Git submodule 或 subtree 纳入本项目历史。
- 从非官方 fork 补齐 Claude Code CLI 核心实现。
- 完成三个 Harness 的全面架构评分或运行时 eval。

## Task Package Tree
```text
ROOT
├── TP-01 核验官方来源与公开范围
├── TP-02 建立同步、revision lock 与研究边界（依赖 TP-01）
├── TP-03 修复浅克隆同步并建立回归证据（依赖 TP-02）
└── TP-04 执行治理、验证与收口审查（依赖 TP-02、TP-03）
```

## Requirement Alignment
- “从 GitHub 上面”由脚本中固定的三个官方 HTTPS origin、登记分支与实际 checkout 证明。
- “这些 Harness 都拉取了没”由被忽略的 `research/upstreams/` 和已跟踪的 revision lock 共同回答。
- Claude Code 官方仓库不含 CLI 核心源码；任务明确报告限制，不用推断冒充源码事实。
- GitHub 同步是可重复工程入口，不保留一次性手工 clone 步骤。

## Task Package Overview
| Node | Objective | Depends On | Deliverables |
|---|---|---|---|
| TP-01 | 确认官方 origin、分支、许可证和公开范围 | - | 来源结论与本地 checkout |
| TP-02 | 建立安全同步和机器 revision 真相源 | TP-01 | `sync_upstreams.sh`、lock、研究文档 |
| TP-03 | 修复 depth=1 前进失败且证明防覆盖边界 | TP-02 | 本地 Git 回归、DEBUG、RED/GREEN/反事实 |
| TP-04 | 同步长期文档并执行 high-risk 门禁 | TP-02, TP-03 | governance、Verification Plan、review/closeout |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
8. DEBUG.md / REGRESSION_EVIDENCE.json
9. TASK_INTENT.json / VERIFICATION_PLAN.json
