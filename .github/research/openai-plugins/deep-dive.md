# openai/plugins 深度研究

## 研究级别

- 当前级别：L2 源码/结构深度研究。
- 研究对象：`openai/plugins`。
- 证据来源：本目录 `raw/` 下的官方 README、marketplace、manifest 和插件工作树。
- 观察日期：2026-09-08。

## L2 结论

OpenAI Plugins 将 Codex 能力包分成三层：marketplace 负责发现，`.codex-plugin/plugin.json` 负责插件身份和入口，插件目录内部再组合 skills、MCP、agents、commands、hooks、assets、references、schemas 和 scripts。这个结构把“我知道有这个能力”“我能安装它”“它具体会做什么”拆开，是比单一 `SKILL.md` 更完整的分发模型。

## 源码证据

- `raw/repository/README.md`：插件最小目录和可选能力表面。
- `raw/repository/.agents/plugins/marketplace.json`：默认市场目录。
- `raw/repository/.agents/plugins/api_marketplace.json`：API key marketplace。
- `raw/repository/plugins/build-web-apps/.codex-plugin/plugin.json`：完整 Web 开发插件入口。
- `raw/repository/plugins/codex-security/.codex-plugin/plugin.json`：安全插件入口。
- `raw/repository/plugins/codex-security/schemas/`、`references/`、`.github/scripts/`：复杂能力包如何附带校验资产。
- `raw/repository/plugins/figma/agents/`、`commands/`、`.github/skills/`：多个能力表面协作的样本。

## 关键机制

### Manifest 是边界索引

强制 manifest 让插件身份和发现入口稳定，减少 Agent 通过扫描任意文件猜测能力的风险。本仓可用同样思想登记 skill owner、触发条件和验证命令。

### Marketplace 与能力本体分离

市场只负责发现和指向插件，不应承担全部运行逻辑。这样插件可以被本地、团队或不同 marketplace 复用，也便于撤销失效入口。

### 能力面可组合

一个插件既可以只提供 skills，也可以增加 MCP、agents、commands、hooks 和静态资源。组合带来效率，也带来叠加权限；安装审查必须按能力面逐个检查。

### 复杂插件自带验证资产

`codex-security` 等目录包含 schema、references 和 scripts，说明专业能力的可信度来自可执行约束和输出契约，而不是名称或 prompt 长度。

## 可迁移模式

- 为本仓的自动化 skill 建立能力登记表，而非只维护目录名。
- 把脚本、schema、reference 和测试放在能力包内部，减少隐式外部依赖。
- 安装前生成权限/文件/网络影响 diff，安装后执行 smoke 和回滚验证。
- 将“当前推荐”“历史对象”“实验对象”分离，避免发现层混淆成熟度。

## 不可迁移条件

- marketplace 不是安全扫描器，来源可信度仍需独立验证。
- plugin manifest 不会自动保证脚本没有恶意或数据泄露。
- 本仓规模不足以复制完整插件 marketplace 服务，目录与 metadata 已足够。

## 验证计划

选一个本仓 skill，模拟三种包：skill-only、带脚本、带外部 MCP。对每种包记录 manifest、权限、网络、文件副作用、测试、禁用和回滚。成功信号是安装前后边界可比较；失败信号是必须阅读所有脚本才能知道插件能做什么且没有禁用路径。
