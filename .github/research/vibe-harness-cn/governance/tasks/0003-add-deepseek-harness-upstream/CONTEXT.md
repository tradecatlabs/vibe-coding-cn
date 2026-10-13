# Repo Evidence
- 当前分支为 `main`，任务开始时工作树干净；本项目没有配置 Git remote。
- `scripts/sync_upstreams.sh` 当前分别在 shell 与内嵌 Python 中重复登记三个上游。
- `research/upstreams.lock.json` 和 `research/UPSTREAMS.md` 当前只有 OpenCode、Codex、Claude Code。
- `research/upstreams/deepseek-harness` 当前不存在。
- 官方仓库：`https://github.com/deepseek-ai/deepseek-harness.git`，登记分支 `master`，许可证 MIT。
- 官方明确标注 developer preview 和 compatibility-breaking changes；该限制必须写入 revision lock。

# Constraints Matrix
| 约束 | 执行口径 |
|---|---|
| 官方来源 | 只接受 `deepseek-ai/deepseek-harness.git` 与 `master` |
| 不覆盖现场 | 脏树、ignored 文件、detached HEAD、错误分支和非 FF 均 BLOCK |
| 上游不可信 | 只读取 Git 元数据与文件布局，不执行上游脚本、hooks、测试或指令 |
| checkout 隔离 | checkout 继续位于被忽略的 `research/upstreams/` |
| 凭据 | 公开 clone 不需要凭据；不得搜寻、记录或显示 API key/token |
| 交付 | 当前无 remote，只允许本地 commit，不声称 push/PR |

# Change Boundary
- 允许修改：上游 source registry、同步脚本、同步回归、研究文档、受影响 README/AGENTS、任务与治理上下文。
- 只读：四个上游 checkout 的 Git 元数据、许可证与源码目录。
- 禁止修改：上游 checkout 内容、Harness manifest 契约、运行时产品能力和无关模块。

# Risk Matrix
| 风险 | 等级 | 控制 |
|---|---|---|
| GitHub 网络失败或超时 | Medium | 既有 timeout、原子 clone、非零退出 |
| 来源登记与 lock 生成漂移 | Medium | 单一 registry、结构校验、回归测试 |
| 上游破坏性更新 | Medium | 精确 revision lock、FF-only、preview limitation |
| 本地研究现场被覆盖 | High | 脏树/分支/ancestry fail-closed |
| checkout 体积与同步耗时增长 | Low | depth=1、有界深化、串行 fail-fast |

# Assumptions and Falsification
- 假设：官方仓库默认研究分支为 `master`；若 clone/HEAD 证明不一致则 BLOCK 并重新核验官方源。
- 假设：MIT marker 与核心源码目录在当前 revision 存在；任一缺失都使 lock 生成失败。
- 假设：第四源开始使重复登记不再值得保留；若单一 registry 反而需要新依赖或降低可读性，则退回直接实现并用回归绑定两处清单。

# Critical Ambiguities
- 无。URL、分支、目标路径和完成标准都可由官方仓库与现有同步契约确定。

# Debug Evidence Contract
- 调试模式: Required
- 回归证据契约: Required
- architecture gate 暴露原则扫描器对 breaking-change 外部事实的误报；必须用 `DEBUG.md`、RED/GREEN/counterfactual 和回归测试收口。

# Task Package Context Map
- TP-01：消费官方 README、许可证、仓库树和现有 lock；不得执行上游代码。
- TP-02：消费 TP-01 事实与现有同步不变量；输出必须保持三源行为兼容。
- TP-03：消费最终实现；真实同步、幂等、验证与 Git 交付必须绑定最终输入。
