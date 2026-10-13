# openai/plugins 研究分析

## 本轮结论

`openai/plugins` 是当前 OpenAI 官方公开的 Codex 插件示例仓库。官方 README 明确每个插件位于 `plugins/<name>/`，必须有 `.codex-plugin/plugin.json`，并可组合 skills、MCP、agents、commands、hooks 和 assets；仓库还区分默认 marketplace 与 API key 登录用户 marketplace。它是理解 Codex 能力如何从单个 skill 走向可安装插件包的主要一手对象。

## 本地证据

- `raw/github-readme.raw.md.txt`：插件目录结构、manifest、marketplace 和示例插件说明。
- `raw/github-root-contents.raw.json`：`.agents/` 和 `plugins/` 是核心入口。
- `raw/repository/.agents/plugins/marketplace.json`：默认 marketplace。
- `raw/repository/.agents/plugins/api_marketplace.json`：API key 登录用户的 marketplace。
- `raw/repository/plugins/*/.codex-plugin/plugin.json`：插件 manifest 样本。
- `raw/repository/plugins/build-web-apps/`、`plugins/codex-security/`：带 skills、references、schemas 和 scripts 的复杂插件样本。

## 对标拆解

| 项 | 内容 |
|:---|:---|
| 参考对象 | `openai/plugins` |
| 它解决的核心问题 | 把技能、工具接入和专业工作流打包成可发现、可安装的 Codex 插件 |
| 核心机制 | plugin manifest、marketplace、skills、MCP、agents、commands、hooks 和 assets |
| 真正带来结果的动作 | 用机器可读 manifest 组织能力包，并把不同副作用面拆成独立文件 |
| 可迁移做法 | 能力包结构、来源/权限审查、安装边界、插件级文档和验证资产 |
| 不可迁移条件 | 不把全部官方插件装进本仓，也不把第三方 MCP 默认设为可信 |
| 下一步试用动作 | 为 `.github/skills/auto-tmux` 设计一个仅含元数据的本地能力包审查清单 |

## 改良迭代

| 改良目标 | 本仓版本 | 验证指标 |
|:---|:---|:---|
| 能力发现 | `.github/skills/README.md` 与 `AGENTS.md` 说明 owner 和触发条件 | Agent 能定位能力且不加载无关全文 |
| 包结构 | 用现有 skill 目录承载说明、脚本、资源和测试 | 入口、依赖和验证都能从目录找到 |
| 供应链 | 外部 skill/plugin 登记来源、许可证、版本和权限 | 未登记能力不进入默认路径 |
| 可回滚 | 安装/更新前备份，失败恢复旧版本 | 失败后用户目录和仓库状态可复原 |

## 可迁移清单

- 要求机器可读的 manifest 或等价登记信息。
- 将 skills、MCP、agents、commands、hooks 和 assets 视为不同能力表面。
- 对复杂能力包附带 schema、脚本、references 和测试。
- 把 marketplace 看成发现层，不把发现结果直接等同于信任。

## 不可迁移清单

- 不把官方 marketplace 内容复制为本仓的稳定事实。
- 不在配置示例中写 API key、OAuth token 或真实订阅信息。
- 不把插件的外部权限隐藏在一段自然语言说明中。

## 验证动作

| 动作 | 成功信号 | 失败信号 |
|:---|:---|:---|
| 审查一个插件 manifest | 能定位入口、版本、依赖和副作用 | 只能看到显示名称 |
| 模拟安装前后 diff | 用户文件先备份，失败可恢复 | 安装过程直接覆盖未知配置 |
| 禁用插件后复查 | skills、MCP、commands 和 hooks 不再生效 | 禁用只隐藏 UI，能力仍被调用 |

## 沉淀判断

可将“Agent 能力包最小登记字段”下沉到本仓 `.github/skills/AGENTS.md`；具体 Codex plugin manifest 和官方 marketplace 仍应链接到 OpenAI 官方文档与本研究 raw，不复制成第二套规范。
