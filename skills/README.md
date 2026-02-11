# 🎯 AI Skills 技能库

`skills/` 目录存放 AI 技能（Skills），这些是比提示词更高级的能力封装，可以让 AI 在特定领域表现出专家级水平。当前包含 **19 个**专业技能。

## 目录结构

```
skills/
├── README.md
│
├── 00-元技能/               # 元技能（生成 Skills 的 Skills）
│   ├── claude-skills/       # ⭐ 元技能核心
│   └── sop-generator/       # SOP 生成与规范化
│
├── 01-AI工具/               # AI CLI 和工具
│   ├── canvas-dev/          # ⭐ Canvas白板驱动开发（AI架构总师）
│   ├── headless-cli/        # 无头模式 AI CLI 调用
│   ├── claude-code-guide/   # Claude Code 使用指南
│   └── claude-cookbooks/    # Claude API 最佳实践
│
├── 02-数据库/               # 数据库技能
│   ├── postgresql/          # ⭐ PostgreSQL 专家（76KB）
│   └── timescaledb/         # 时序数据库扩展
│
├── 03-加密货币/             # 加密货币/量化交易
│   ├── ccxt/                # 交易所统一 API
│   ├── coingecko/           # 行情数据 API
│   ├── cryptofeed/          # 实时数据流
│   ├── hummingbot/          # 量化交易框架
│   └── polymarket/          # 预测市场 API
│
└── 04-开发工具/             # 通用开发工具
    ├── ddd-doc-steward/    # 文档驱动开发文档管家
    ├── telegram-dev/        # Telegram Bot 开发
    ├── twscrape/            # Twitter/X 数据抓取
    ├── snapdom/             # DOM 快照工具
    └── proxychains/         # 代理链配置
```

## Skills 一览表

### 00-元技能

| 技能 | 说明 |
|:---|:---|
| [claude-skills](./00-元技能/claude-skills/SKILL.md) | ⭐ 生成 Skills 的 Skills |
| [sop-generator](./00-元技能/sop-generator/SKILL.md) | SOP 生成与规范化 |

### 01-AI工具

| 技能 | 说明 |
|:---|:---|
| [canvas-dev](./01-AI工具/canvas-dev/SKILL.md) | ⭐ Canvas白板驱动开发（AI架构总师） |
| [headless-cli](./01-AI工具/headless-cli/SKILL.md) | 无头模式 AI CLI 调用（Gemini/Claude/Codex） |
| [claude-code-guide](./01-AI工具/claude-code-guide/SKILL.md) | Claude Code CLI 使用指南 |
| [claude-cookbooks](./01-AI工具/claude-cookbooks/SKILL.md) | Claude API 最佳实践 |

### 02-数据库

| 技能 | 说明 |
|:---|:---|
| [postgresql](./02-数据库/postgresql/SKILL.md) | ⭐ PostgreSQL 完整专家技能（76KB） |
| [timescaledb](./02-数据库/timescaledb/SKILL.md) | PostgreSQL 时序扩展 |

### 03-加密货币

| 技能 | 说明 |
|:---|:---|
| [ccxt](./03-加密货币/ccxt/SKILL.md) | 加密货币交易所统一 API |
| [coingecko](./03-加密货币/coingecko/SKILL.md) | CoinGecko 行情 API |
| [cryptofeed](./03-加密货币/cryptofeed/SKILL.md) | 加密货币实时数据流 |
| [hummingbot](./03-加密货币/hummingbot/SKILL.md) | 量化交易机器人框架 |
| [polymarket](./03-加密货币/polymarket/SKILL.md) | 预测市场 API |

### 04-开发工具

| 技能 | 说明 |
|:---|:---|
| [ddd-doc-steward](./04-开发工具/ddd-doc-steward/SKILL.md) | 文档驱动开发（DDD）文档管家，按证据链生成/更新 docs SSOT |
| [telegram-dev](./04-开发工具/telegram-dev/SKILL.md) | Telegram Bot 开发 |
| [twscrape](./04-开发工具/twscrape/SKILL.md) | Twitter/X 数据抓取 |
| [snapdom](./04-开发工具/snapdom/SKILL.md) | DOM 快照与测试 |
| [proxychains](./04-开发工具/proxychains/SKILL.md) | 代理链配置与使用 |

## 快速使用

```bash
# 查看元技能
cat skills/00-元技能/claude-skills/SKILL.md

# 查看无头 CLI 技能
cat skills/01-AI工具/headless-cli/SKILL.md

# 查看 PostgreSQL 技能
cat skills/02-数据库/postgresql/SKILL.md
```

## 创建自定义 Skill

使用元技能生成：
1. 准备领域资料（文档、代码、规范）
2. 将资料和 `00-元技能/claude-skills/SKILL.md` 一起提供给 AI
3. AI 会生成针对该领域的专用 Skill

## 相关资源

- [元技能文件](./00-元技能/claude-skills/SKILL.md) - 生成 Skills 的 Skills
- [无头 CLI 技能](./01-AI工具/headless-cli/SKILL.md) - 无头模式 AI CLI 调用
- [提示词库](../prompts/) - 更细粒度的提示词集合
- [文档库](../documents/) - 方法论与开发经验
