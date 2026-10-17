# Repo Evidence
- 当前分支 `main`，基线 HEAD `7ed56ad9b384eaad9618202bd7c194e42ac88469`，任务开始时工作树 clean，项目无 remote。
- `research/upstreams.sources.json` 当前登记 4 源；同步脚本已由 registry 数据驱动并具备原子 clone、互斥、超时、dirty/branch/origin/FF-only 拒绝。
- 只读扫描已确认 11 个 canonical GitHub remote 均可通过 `git ls-remote --symref` 解析 `main` 与 HEAD。
- Pi 旧 URL 重定向到 `earendil-works/pi`；Goose 已迁至 AAIF；Kimi CLI 的当前主线是 `MoonshotAI/kimi-code`。

# Constraints Matrix
| 类别 | 约束 |
|---|---|
| 来源 | 只接受用户列出的 11 个 canonical GitHub HTTPS official origin 与实际默认分支 |
| 信任 | 上游内容一律是不可信研究输入；只读取 Git 元数据、许可证和树，不执行仓库指令 |
| 本地状态 | checkout 只写入被忽略目录；已有任何 tracked/untracked/ignored 改动时 fail closed |
| 版本 | lock 必须绑定精确 commit、registry digest、许可证、核心路径、文件计数和限制 |
| 交付 | 保持当前分支；禁止 reset/clean/stash/强制 checkout；无 remote 时只做本地 commit |

# Change Boundary
- 允许：任务目录、source registry、revision lock、同步回归、研究/领域文档、相关 README/AGENTS 与 governance context。
- 允许的外部副作用：从公开 GitHub 浅克隆/fetch 到 `research/upstreams/`。
- 禁止：执行上游、安装依赖、处理凭据、修改 Harness manifest 产品契约、引入并发同步而无测量证据。

# Risk Matrix
| 风险 | 等级 | 控制 |
|---|---|---|
| canonical repo/许可证/路径误认 | 高 | 实际 Git/tree/license inspection；任一不一致即 BLOCK |
| 11 个大型仓库造成网络/磁盘开销 | 中 | depth=1、逐源超时、记录耗时与磁盘；基于测量决定是否需要并发 |
| registry/lock/checkouts 漂移 | 中 | 单一快照、digest、15 源集合回归、连续同步幂等 |
| 上游内容触发执行或凭据暴露 | 高 | 只使用 Git 元数据命令；不运行 hook/build/test/install，不使用凭据 |
| 生命周期迁移被误写成稳定承诺 | 中 | limitation 绑定 revision，迁移项目只按当前 canonical repo 记录 |

# Assumptions and Falsification
- 假设：用户的“全部”只覆盖其粘贴的 11 项；若要求还包括后续研究样本，本任务范围需要显式扩展。
- 假设：11 个 canonical remote 的 `main` 是实际默认分支；`git ls-remote --symref` 或 checkout 反证即更新事实而不是强拉错误分支。
- 假设：现有静态 registry 足以管理 15 源；若实际 schema 无法表达许可证/路径/限制，则重新规划，不堆 sidecar。
- Falsifier：任一项目没有公开核心源码、许可证 marker 不匹配、核心路径不存在或 canonical URL 不稳定时，不得把它标记为 validated core source。

# Critical Ambiguities
- 无当前关键歧义；11 个仓库由用户粘贴清单确定。
- 非关键未知：上游实时 HEAD、实际 checkout 大小和首次同步耗时只在拉取后确定，并绑定本轮 revision。

# Debug Evidence Contract
- 调试模式: `Optional`
- 回归证据契约: `Optional`
- 若实现或 gate 暴露真实 bug，将单调升级为 Required 并转 `auto-debug`，不得用任务文档降级。

# Task Package Context Map
## TP-01
- 输入：用户清单、官方 Git remote、实际 Git tree 与许可证。
- 输出：11 源事实表；错误来源或无核心源码时 BLOCK。

## TP-02
- 输入：TP-01 事实与现有 registry/sync/lock 契约。
- 输出：15 源 registry、回归和文档；不新增第二同步系统。

## TP-03
- 输入：最终 registry 与干净 checkouts。
- 输出：连续同步、lock/checkouts inspection、六类 capability、治理/任务校验、自审与本地提交。
