# Repo Evidence
- 官方 checkout 已位于 `research/upstreams/{opencode,codex,claude-code}`，目录被 Git 忽略。
- OpenCode 的核心入口为 `packages/opencode/src`，Codex 为 `codex-rs/core/src` 等 Rust 路径。
- Claude Code 官方仓库有插件、hooks、示例与发布资料，但没有 CLI 核心项目 manifest 或核心源码入口。
- Codex 在首次复验时从 `781445f` 前进到 `990218b`，暴露 depth=1 ancestry 不可见导致的同步失败。

# Constraints Matrix
| Constraint | Source | Effect |
|---|---|---|
| 只接受官方 origin 与登记分支 | 用户要求 / 来源真实性 | 不接受 fork、镜像或本机安装目录 |
| 上游内容是不可信数据 | 项目信任边界 | 不执行上游脚本、hooks、测试与嵌入式指令 |
| 不覆盖本地研究现场 | Git 安全规则 | 脏工作树、detached HEAD、错误分支与无法证明 FF 均 BLOCK |
| 第三方源码不进入历史 | 许可证与所有权边界 | checkout gitignored，只提交 lock 和研究结论 |
| 单 agent 串行 | 会话规则 | 不创建原生子代理，普通命令可并行但本任务无需 |

# Change Boundary
- 允许：`.gitignore`、根入口、`research/`、同步/验证脚本、回归测试和对应治理/任务文档。
- 禁止：修改上游源码、安装上游依赖、reset/clean/强制 checkout、push、部署和凭据搜寻。
- 创建 `research/` 与测试脚本后，已同步根、`research/`、`scripts/`、`tests/` 的 `AGENTS.md`。

# Risk Matrix
| Risk | Level | Mitigation |
|---|---|---|
| fork 或错误分支被冒充官方输入 | High | origin/分支精确匹配，lock 绑定 commit |
| 本地改动被同步覆盖 | High | 工作树预检与 FF 证明，禁止 reset |
| 浅历史把普通前进误判为改写 | High | 有界指数 deepen 后再做 ancestry 判定 |
| Claude 扩展仓库被误称核心源码 | High | visibility/limitation 字段和公开范围报告 |
| 上游规模拖慢同步 | Medium | 默认 depth=1，只在 ancestry 不足时有界深化 |

# Assumptions and Falsification
- 假设：脚本登记的 URL/分支是本轮官方来源；若 GitHub 官方 owner 或默认分支变化，重新核验并更新登记值。
- Proof point：三个 checkout origin/branch/HEAD 与 lock 一致，连续同步不改变 lock 摘要。
- Falsifier：需要 reset/force 才能完成普通官方分支前进，或 Claude 官方仓库出现可核验的 CLI 核心源码入口。
- 假设被推翻时只更新来源登记与研究结论，不通过 fork、猜测或强制覆盖维持旧结论。

# Critical Ambiguities
- 无阻塞当前同步的歧义。
- 非阻塞未知：官方仓库未来可能迁移 owner、变更默认分支、重写历史或改变许可证。

# Debug Evidence Contract
- 调试模式: Required
- 回归证据契约: Required
- Owner evidence: `DEBUG.md`、`REGRESSION_EVIDENCE.json` 和 `runtime/regression/` 已建立；closeout 前必须机械校验。

# Task Package Context Map
## TP-01 核验官方来源与公开范围
- 输入：官方 GitHub 页面、clone origin、目录树与许可证。
- 输出：OpenCode/Codex 核心源码可见，Claude Code CLI 核心源码不可见的 revision 绑定结论。

## TP-02 建立同步、revision lock 与研究边界
- 输入：TP-01 来源登记。
- 输出：被忽略 checkout、可重跑同步入口、机器 lock 与人类研究基线。

## TP-03 修复浅克隆同步并建立回归证据
- 输入：真实 Codex forced-update 症状。
- 输出：根因、最小永久修复、本地 Git RED/GREEN/反事实与拒绝路径。

## TP-04 执行治理、验证与收口审查
- 输入：全部实现、Task Intent、项目 Verification Policy。
- 输出：新鲜 high-risk capability 结果、governance strict/health、review 与 closeout 状态。
