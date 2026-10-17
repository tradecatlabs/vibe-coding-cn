# SWE-agent/mini-SWE-agent 深度研究

## 研究级别

- 当前级别：L2 最小 Agent loop 与评估研究。
- 研究对象：SWE-agent/mini-swe-agent。
- 证据来源：本目录 raw/ 下的 README、src/minisweagent、docs 和 tests。
- 观察日期：2026-09-08。

## L2 结论

DefaultAgent 的核心循环很短：初始化 system/user 消息，查询模型，解析 action，调用环境，追加 observation，直到提交或限制触发；serialize/save 保存消息、模型统计、环境状态和版本。InteractiveAgent 再在同一基础上加入 human、confirm 和 yolo 模式。这个设计说明 Agent 的最小控制面可以很小，但边界和证据不能缺失。

## 关键机制

### Bash-only 工具面

README 强调只依赖 bash action，而不是为每个能力设计专用工具。这降低了 runtime 复杂度，但把安全、命令格式和环境隔离责任放到了执行环境。

### 有界执行

AgentConfig 包含 step_limit、cost_limit、wall_time_limit_seconds 和 max_consecutive_format_errors。限制直接进入运行循环，失败不会无限尝试。

### 线性轨迹

每一步都追加到 messages，trajectory 与传给模型的历史保持一致，便于调试、复现和 fine-tuning 研究。

### 环境可替换

local、docker、singularity、bubblewrap 等环境以适配器方式分开，说明执行隔离应由环境层决定，而不是散落在 Agent prompt 中。

## 可迁移模式

- 为本仓外部拉取和验证脚本设置明确超时。
- 保存 raw sources、退出码和失败信息，禁止把失败吞掉。
- 对不同副作用环境分级，默认读和验证优先。
- 将 benchmark、示例和生产质量明确分层。

## 迁移边界

- 本仓研究脚本不需要实现模型驱动动作循环。
- 不用 subprocess 直接执行来自外部 README 的命令。
- 不能把 bash-only 当作天然安全；本仓仍遵守命令安全红线。

## L3 验证任务

1. 检查 fetch-research-raw.py 是否对所有网络和 Git 动作有足够超时边界。
2. 为研究域保存一次完整失败来源记录并验证 checker 行为。
3. 将“benchmark 不是生产证明”写入相关研究模板。
