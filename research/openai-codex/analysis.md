# openai/codex 研究分析

## 本轮结论

`openai/codex` 的核心价值不是“官方 CLI 怎么写”，而是展示了成熟 coding agent 必须有执行控制面。
它把配置、沙箱、执行策略、工具、技能、项目上下文和交互入口拆成显式对象，避免让高风险行为只靠
提示词自觉。

本仓最应该迁移的是治理思想：凡是能执行命令、改文件、访问网络或影响仓库状态的入口，都必须有
owner、风险等级、输入输出、dry-run、CI 状态和审计边界。

## 本地证据

- 研究对象：`openai/codex`
- 当前研究角色：官方 coding agent 工具源码
- 原始仓库：`raw/repository/`
- 原始来源清单：`raw/sources.yml`
- 事实摘要：`domain.yml`
- 深度证据：`deep-dive.md`

## 对标拆解

| 项 | 内容 |
|:---|:---|
| 参考对象 | `openai/codex` |
| 它解决的核心问题 | 让本地 coding agent 的命令执行、文件修改和工具调用进入可配置、可审计、可限制的系统 |
| 核心机制 | `config`、`sandboxing`、`linux-sandbox`、`tools`、`skills`、`docs/exec*`、`AGENTS.md` 分层 |
| 真正带来结果的动作 | 把执行风险做成系统对象，而不是把风险控制写成提示词愿望 |
| 可迁移做法 | 脚本登记表、风险等级、自动执行边界、人工审批边界、dry-run 和审计说明 |
| 不可迁移条件 | 不复制 Rust workspace、Bazel/Nix、CLI runtime 和产品级沙箱实现 |
| 下一步试用动作 | 先为本仓 `scripts/` 建立 `manifest.yml` 或等价登记表 |

## 改良迭代

| 改良目标 | 原模式 | 本仓版本 | 验证指标 |
|:---|:---|:---|:---|
| 脚本控制面 | Codex 将执行策略和沙箱显式化 | `scripts/manifest.yml` 记录脚本 owner、风险、输入、输出、CI 状态 | Agent 能判断哪些脚本可自动执行，哪些必须人工确认 |
| Agent 上下文接口 | Codex 使用 `AGENTS.md` 承载项目规则 | 保持根目录和子目录 `AGENTS.md` 为正式上下文入口 | 新目录或架构变更后索引和 AGENTS 同步 |
| 技能治理 | Codex 将 skills 作为可复用能力对象 | 本仓 skills 必须有触发条件、边界、输入输出和验证 | skill 不再只是 prompt 收藏 |

## 可迁移清单

- 对所有写仓库、网络访问、高风险发布或迁移脚本标注风险等级。
- 对脚本补齐输入、输出、幂等性、dry-run、失败恢复和审计说明。
- 把 Agent 可自动执行与必须人工确认的边界写进 `scripts/AGENTS.md`。
- 把命令执行策略沉淀到 `docs/references/` 或 `docs/workflow/`。

## 不可迁移清单

- 不把本仓改造成 Codex 类 runtime 产品。
- 不为了“看起来企业级”引入复杂沙箱、Bazel、Nix 或多语言构建系统。
- 不把官方产品实现等同于本仓必须采用的唯一标准。

## 验证动作

| 动作 | 成功信号 | 失败信号 |
|:---|:---|:---|
| 抽样 5 个 `scripts/` 文件登记 owner、风险、输入输出 | 维护者能一眼判断脚本能否自动跑 | 仍需要读源码才知道脚本风险 |
| 给写仓库脚本补 dry-run 或说明为何不能 dry-run | 高风险动作有预演或审计路径 | 脚本一运行就产生不可逆副作用 |
| 把脚本风险边界加入 `scripts/AGENTS.md` | Agent 执行前能引用明确规则 | 每次仍靠对话临时判断 |

## 沉淀判断

- 稳定结论应下沉到 `scripts/`、`docs/workflow/` 和 `docs/references/`。
- `deep-dive.md` 保留源码证据；本文件负责把证据转成迁移动作。
