# aaif-goose/goose 研究域

## 字多不看

- 本目录研究 aaif-goose/goose 这个跨模型开源 AI Agent。
- 当前优先级：P1；研究角色：桌面、CLI、API、多提供商和 MCP 扩展。
- 重点观察 Agent 能力如何从代码建议扩展到执行、编辑、测试和一般自动化。

## 快速导航

| 文档 | 定位 |
|:---|:---|
| [domain.yml](domain.yml) | 仓库事实快照、研究方向、优先级和来源证据。 |
| [analysis.md](analysis.md) | 多入口 Agent 的结构化研究结论和迁移边界。 |
| [deep-dive.md](deep-dive.md) | Rust workspace、扩展、配置和权限边界的 L2 研究。 |
| [AGENTS.md](AGENTS.md) | 本研究域维护规则。 |

<details>
<summary><strong>完整细粒度目录（点击展开/收起）</strong></summary>

### 细粒度目录

- [domain.yml](domain.yml) - 仓库事实快照、研究方向、优先级和来源证据。
- [analysis.md](analysis.md) - 多入口 Agent 的结构化研究结论和迁移边界。
- [deep-dive.md](deep-dive.md) - Rust workspace、扩展、配置和权限边界的 L2 研究。
- [AGENTS.md](AGENTS.md) - 本研究域维护规则。

</details>

## 使用方式

- 先读本 README 的判断，再读 analysis.md 和 deep-dive.md。
- 需要安装、扩展或 provider 配置时，优先核验官方文档 https://goose-docs.ai/ 和 raw/ 快照。
- 不把“支持某个模型”当作安全或质量证明；重点检查工具权限、网络访问、凭据来源和恢复路径。

## 正文

### 研究定位

aaif-goose/goose 是一个开源 AI Agent，提供桌面、CLI 和 API 入口，可使用多个模型提供商和 MCP 扩展来执行代码、工作流及其他任务。

### 当前判断

它适合作为“多入口 Agent + 扩展生态”的对标对象。对本仓最有价值的是 provider、extension、工作区和执行边界的分层；不应因为其功能覆盖广，就把平台级能力全部引入教程。

### 观察字段

- GitHub URL：https://github.com/aaif-goose/goose
- 当前研究方向：coding-agent-tooling
- 当前优先级：P1
- 当前归档状态：false
- 主要语言：Rust
- 最新 release：v1.49.0
- 项目主页：https://goose-docs.ai/

### 后续观察

- 多提供商配置、订阅接入和 API key 的边界是否清晰。
- MCP 扩展的发现、授权、失败和卸载流程是否可审计。
- 哪些桌面/CLI/API 分层经验可以补充本仓的工具选择文档。
