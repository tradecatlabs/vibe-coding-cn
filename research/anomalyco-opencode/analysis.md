# anomalyco/opencode 研究分析

## 本轮结论

`anomalyco/opencode` 是当前规范仓库的开源 coding agent，README 展示了终端、桌面、模型提供商、build/plan agent、subagent 和插件能力；仓库的 v2 spec 则进一步把配置、提供商、权限、Agent 和插件生命周期拆成可演进的边界。它是本仓 OpenCode 配置文档的直接对标，且不能继续使用旧的 `sst/opencode` 作为当前仓库名。

## 本地证据

- `raw/github-readme.raw.md.txt`：安装方式、build/plan agent、general subagent 和文档入口。
- `raw/repository/packages/cli/`、`packages/tui/`、`packages/app/`：CLI、终端和桌面入口。
- `raw/repository/packages/core/src/config.ts`、`permission.ts`、`plugin.ts`、`skill.ts`：配置、权限、插件和技能控制面。
- `raw/repository/packages/llm/`、`packages/protocol/`、`packages/server/`：模型、协议和服务边界。
- `raw/repository/specs/v2/config.md`：v2 配置字段、提供商、Agent 和权限重设计。
- `raw/repository/specs/v2/catalog-config-plugin-lifecycle.md`：插件、配置、catalog 和 reload 生命周期方案。

## 对标拆解

| 项 | 内容 |
|:---|:---|
| 参考对象 | `anomalyco/opencode` |
| 它解决的核心问题 | 为不同模型和工具提供开放、可扩展的 coding agent 运行入口 |
| 核心机制 | provider、model、agent、permission、plugin、skill、session、TUI/desktop 多入口 |
| 真正带来结果的动作 | 把“模型接入”“Agent 行为”“工具权限”和“用户界面”拆成独立层 |
| 可迁移做法 | 配置分层、plan/build 双模式、权限策略、插件生命周期和 v2 迁移文档 |
| 不可迁移条件 | 不复制其 TypeScript monorepo、数据库、桌面端或全部 provider 适配 |
| 下一步试用动作 | 对本仓 CLI 配置文档增加 provider、权限、备份和回滚检查清单 |

## 改良迭代

| 改良目标 | 本仓版本 | 验证指标 |
|:---|:---|:---|
| 配置分层 | 用户配置、项目规则和研究事实分开 | 修改一个层不会静默覆盖其他层 |
| 只读规划 | 先计划和检查，再允许写入 | 只读阶段不修改工作区 |
| 权限策略 | 将命令、文件、网络和提交边界写清楚 | 高风险动作有确认或机器门禁 |
| 生命周期 | 配置变化同步更新索引和备份 | 重复执行可回滚、结果可核验 |

## 可迁移清单

- 用只读 plan 阶段理解仓库，再进入 build/execute 阶段。
- 将 provider、model、agent、permission 作为不同配置概念。
- 对插件安装、禁用、更新和卸载设计状态恢复。
- 使用 schema 和 policy 而不是散落布尔开关表达权限。
- 为配置备份、迁移和兼容性保留明确入口。

## 不可迁移清单

- 不把 OpenCode 的默认 agent、模型和订阅策略当作 Codex 默认值。
- 不把 v2 spec 的提议字段写成已经稳定的公开 API。
- 不把插件可安装等同于插件可信。

## 验证动作

| 动作 | 成功信号 | 失败信号 |
|:---|:---|:---|
| 用 plan 模式审查一个配置变更 | 只产生计划和风险，不改文件 | 计划阶段已产生写入副作用 |
| 修改 provider/permission 后重载 | 受影响服务一致更新且有明确事件 | 配置部分生效、部分使用旧值 |
| 安装后禁用一个插件 | 插件贡献的配置和能力完全撤销 | 仍残留 provider、权限或工具 |

## 沉淀判断

稳定结论可下沉到 `docs/getting-started/cli-setup.md` 和 `docs/gongfa/` 的配置/权限部分；v2 spec 的未定设计继续保留在研究域，不能写成教程硬规则。
