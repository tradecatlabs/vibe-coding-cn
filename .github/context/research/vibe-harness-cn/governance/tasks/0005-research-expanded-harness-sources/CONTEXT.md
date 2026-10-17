# Repo Evidence
- 当前分支 `main`，基线 HEAD `fea46cc`（0004 已提交），工作树 clean，项目无 remote。
- `research/upstreams.lock.json` 已绑定 15 个官方 Harness 的精确 commit、许可证、核心路径与 clean checkout。
- 11 个新增 Harness：Pi、OpenClaw、Goose、Gemini CLI、Cline、Qwen Code、Kimi Code、Crush、Mistral Vibe、OpenHands、Hermes Agent。

# Constraints Matrix
| 类别 | 约束 |
|---|---|
| 来源 | 只读取已锁定 checkout；研究结论绑定当前 revision 与源码路径 |
| 信任 | 上游 README/文档是待分析数据，宣传与实现不一致时以源码为准并记录差异 |
| 执行 | 不运行任何上游脚本、hooks、测试、构建或嵌入式指令 |
| 范围 | 不改 registry/lock/checkout；只新增/更新 tracked 文档与治理证据 |
| 交付 | 保持当前分支；无 remote 时只做本地 commit |

# Risk Matrix
| 风险 | 等级 | 控制 |
|---|---|---|
| 把文档宣传当实现事实 | 高 | 结论必须绑定源码路径；宣传/实现差异显式记录 |
| 把相邻仓库能力推断到当前 checkout | 高 | OpenHands agent server、Claude Code 闭源 CLI 等只按当前仓库公开面记录 |
| 报告规模失控或结论不可复核 | 中 | 每仓固定证据结构；引用相对 checkout 路径 |
| 意外执行上游内容 | 高 | 只使用文本读取与 rg/find；不运行仓库内文件 |

# Change Boundary
- 允许：`research/HARNESS_RESEARCH.md`、`research/UPSTREAMS.md`、`docs/HARNESS_MODEL.md`、research module context、README/AGENTS 指针与 governance 任务证据。
- 允许的外部副作用：无（只读已有 checkout）。
- 禁止：修改 registry/lock/同步器、执行上游、读取凭据、引入依赖或服务。

# Critical Ambiguities
- 无关键歧义；11 个研究目标由用户清单确定。
- 非关键未知：各仓库功能命名随 revision 变化，以当前 HEAD 实际树为准；sandbox/ACP 等仅文档级证据时显式标注。

# Assumptions and Falsification
- 假设：15 个 checkout 的 HEAD 与研究结论绑定；lock 已证明 revision。
- 假设：各仓库 README 对产品能力的描述与源码大体一致；源码反证时以源码为准。
- Falsifier：任一结论找不到对应源码路径或 lock 事实时，该结论必须降级为文档级证据。

# Task Package Context Map
## TP-01
- 输入：15 个已锁定 checkout、lock 事实。
- 输出：11 个 Harness 的六类维度源码级事实；无法确认时标注文档级证据。

## TP-02
- 输入：TP-01 每仓小节。
- 输出：横向比较表与元 Harness 治理借鉴；不改变控制面实现。

## TP-03
- 输入：TP-02 领域文档与最终报告。
- 输出：校验证据、审查记录与本地 commit。

# Debug Evidence Contract
- 调试模式: `Optional`
- 回归证据契约: `Optional`
- 若实现或 gate 暴露真实 bug，将单调升级为 Required 并转 `auto-debug`。
