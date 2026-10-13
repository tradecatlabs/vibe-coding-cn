# Task-Level Acceptance
- `research/upstreams/deepseek-harness` 是官方 `master` 的干净浅 checkout。
- revision lock 有且只有四个来源，并包含 DeepSeek Harness 精确 revision、MIT、核心路径和 preview 限制。
- 同一 source registry 驱动同步与 lock，重复/缺字段/路径漂移会 fail closed。
- 连续两次真实同步成功，第二次不会造成 lock 内容漂移。
- 同步回归、项目 capability、governance strict/health 与任务文档校验通过。

# Validation Plan
| 验证 | 命令/证据 | 失败归因 |
|---|---|---|
| Shell 语法 | `bash -n scripts/sync_upstreams.sh tests/test_sync_upstreams.sh` | 脚本语法/引用错误 |
| 同步回归 | `bash tests/test_sync_upstreams.sh` | clone/FF/锁/登记源行为回归 |
| 真实同步 | `bash scripts/sync_upstreams.sh`，连续运行两次并比较 lock digest | 网络、来源、布局、许可证或幂等错误 |
| Lock 结构 | `python3 -m json.tool research/upstreams.lock.json` 与 checkout inspection | 元数据或 revision 不一致 |
| 项目门禁 | 按 `VERIFICATION_PLAN.json` 逐个执行 `python3 scripts/verify_project.py --gate <capability>` | 对应 capability 失败 |
| 治理 | strict validator、health report、task docs validator | 文档、索引、链接或任务状态漂移 |

# Review Gate
- 正确性：四源清单、origin/branch/HEAD/license/core paths 一致。
- 可读性：source registry 字段直白，脚本继续是薄编排。
- 架构：外部 checkout 仍是可重建缓存，不进入产品 runtime 或 Git 历史。
- 安全：不执行上游内容、不接触凭据、不弱化现有 fail-closed 分支。
- 性能：仍为串行 `O(B + F)` 浅同步；只有实测成为瓶颈后才引入受限并发。

# Runtime Verification Gate
- `VERIFICATION_PLAN.json` 状态必须为 READY。
- architecture、behavior、contract、test 四个 required gate 必须绑定最终输入并 PASS。
- 任何实现或任务状态变更都会使旧证据失效，必须重新运行。

# Ship Readiness
- 本地 commit 必须只包含本任务路径及必要文档同步。
- 当前无 Git remote；本任务不声称 push、PR、CI 或外部独立 review。
- 回滚：反向提交 tracked 变更；checkout 为忽略缓存，可在确认干净后人工移除再重建，脚本不自动删除。

# Task Package Acceptance
- TP-01：官方 URL、master、MIT、核心路径与 preview 限制均有 checkout 证据。
- TP-02：单一登记源、同步脚本、测试和文档一致，三源回归不变。
- TP-03：四源真实同步和幂等成立，门禁通过并形成可追踪本地 commit。

# Anti-Goals
- 不得执行或安装上游代码。
- 不得把 checkout 纳入本项目提交。
- 不得因 preview 状态声称 DeepSeek Harness 已生产就绪。
- 不得用 reset、clean、stash、强制 checkout 或历史改写整理工作区。
