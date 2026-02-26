# 🎯 AI Skills 技能库

`skills/` 目录存放 AI 技能（Skills），这些是比提示词更高级的能力封装，可以让 AI 在特定领域表现出专家级水平。当前包含 **20 个**专业技能。

## Skills 一览表

### 🔮 元技能（生成 Skills 的 Skills）

| 技能 | 说明 |
|:---|:---|
| [skills-skills](./skills-skills/SKILL.md) | ⭐ 生成 Skills 的 Skills |
| [sop-generator](./sop-generator/SKILL.md) | SOP 生成与规范化 |

### 🤖 AI 工具

| 技能 | 说明 |
|:---|:---|
| [canvas-dev](./canvas-dev/SKILL.md) | ⭐ Canvas白板驱动开发（AI架构总师） |
| [headless-cli](./headless-cli/SKILL.md) | 无头模式 AI CLI 调用（Gemini/Claude/Codex） |
| [claude-code-guide](./claude-code-guide/SKILL.md) | Claude Code CLI 使用指南 |
| [claude-cookbooks](./claude-cookbooks/SKILL.md) | Claude API 最佳实践 |

### 🗄️ 数据库

| 技能 | 说明 |
|:---|:---|
| [postgresql](./postgresql/SKILL.md) | ⭐ PostgreSQL 完整专家技能 |
| [timescaledb](./timescaledb/SKILL.md) | PostgreSQL 时序扩展 |

### 💰 加密货币 / 量化交易

| 技能 | 说明 |
|:---|:---|
| [ccxt](./ccxt/SKILL.md) | 加密货币交易所统一 API |
| [coingecko](./coingecko/SKILL.md) | CoinGecko 行情 API |
| [cryptofeed](./cryptofeed/SKILL.md) | 加密货币实时数据流 |
| [hummingbot](./hummingbot/SKILL.md) | 量化交易机器人框架 |
| [polymarket](./polymarket/SKILL.md) | 预测市场 API |

### 🛠️ 开发工具

| 技能 | 说明 |
|:---|:---|
| [ddd-doc-steward](./ddd-doc-steward/SKILL.md) | 文档驱动开发（DDD）文档管家 |
| [telegram-dev](./telegram-dev/SKILL.md) | Telegram Bot 开发 |
| [twscrape](./twscrape/SKILL.md) | Twitter/X 数据抓取 |
| [snapdom](./snapdom/SKILL.md) | DOM 快照与测试 |
| [proxychains](./proxychains/SKILL.md) | 代理链配置与使用 |
| [tmux-autopilot](./tmux-autopilot/SKILL.md) | tmux 自动化操控（AI蜂群协作） |

### ⚡ 生产力

| 技能 | 说明 |
|:---|:---|
| [markdown-to-epub](./markdown-to-epub/SKILL.md) | Markdown 转 EPUB 电子书 |

## 外部技能仓库（软链接）

- `skills/claude-official-skills/`：来自 Claude 官方 skills 仓库（Anthropic）。
  本仓库以 Git submodule 的形式落在 `assets/repo/claude-official-skills/`，
  并通过软链接暴露到 `skills/` 下便于浏览与复用。
- 初始化/更新方式：`git submodule update --init --recursive`
- Skills 大全网站：`https://skills.sh/`

## 快速使用

```bash
# 查看元技能
cat skills/skills-skills/SKILL.md

# 查看无头 CLI 技能
cat skills/headless-cli/SKILL.md

# 查看 PostgreSQL 技能
cat skills/postgresql/SKILL.md
```

## 创建自定义 Skill

使用元技能生成：
1. 准备领域资料（文档、代码、规范）
2. 将资料和 `skills-skills/SKILL.md` 一起提供给 AI
3. AI 会生成针对该领域的专用 Skill

## 相关资源

- [元技能文件](./skills-skills/SKILL.md) - 生成 Skills 的 Skills
- [提示词库](../prompts/) - 更细粒度的提示词集合
- [文档库](../assets/documents/) - 方法论与开发经验
- [skills.sh](https://skills.sh/) - Skill 大全网站
