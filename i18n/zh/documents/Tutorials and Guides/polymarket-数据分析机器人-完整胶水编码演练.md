# Polymarket 数据分析机器人：完整的胶水编码演练

> **场景**：用 Vibe Coding 方法，从零开始，把 Polymarket API、Claude AI、Telegram Bot 三个现成服务"胶水"在一起，构建一个能自动分析预测市场数据的机器人。

---

## 🎯 一句话目标 & 非目标

**目标**：构建一个 Telegram 机器人，能查询 Polymarket 热门市场、分析赔率变化趋势、用 AI 生成简报，每天定时推送。

**非目标**：
- 不做交易执行（只分析，不下单）
- 不做复杂的 ML 预测模型
- 不做 Web 前端界面

---

## 🧠 元思考：为什么这是"胶水编码"

```
Polymarket API  ──┐
                  ├──► 胶水层 (Python) ──► Claude AI ──► Telegram Bot
定时调度器      ──┘
```

三个外部服务都有现成 API，我们的工作只是：
1. **拉数据**（Polymarket CLOB API）
2. **处理数据**（清洗、格式化）
3. **喂给 AI**（Claude 生成分析）
4. **推送结果**（Telegram 发消息）

这就是胶水编码的本质：**能抄不写，不重复造轮子**。

---

## 📋 项目结构

```
polymarket-bot/
├── README.md
├── requirements.txt
├── .env                    # 不提交 Git
├── .env.example
├── .gitignore
├── CLAUDE.md               # Claude 持久上下文
│
├── src/
│   ├── main.py             # 程序入口 + 定时调度
│   ├── config.py           # 配置管理
│   │
│   ├── data/
│   │   └── polymarket.py   # Polymarket API 客户端
│   │
│   ├── core/
│   │   └── analyzer.py     # Claude AI 分析逻辑
│   │
│   └── external/
│       └── telegram.py     # Telegram Bot 推送
│
└── logs/
    └── bot.log
```

---

## 🚀 完整演练过程

### 第一步：明确需求，逆向构建

在开始写任何代码之前，先问 AI：

> **提示词**：
> "我想构建一个 Polymarket 数据分析 Telegram 机器人。请帮我：
> 1. 列出 Polymarket 有哪些公开 API 端点
> 2. 分析获取热门市场数据需要哪些字段
> 3. 给出最小可行的数据结构设计"

AI 会告诉你 Polymarket 有 CLOB API（`https://clob.polymarket.com`），核心端点是 `/markets`。

---

### 第二步：搭骨架，接口先行

先定义各模块的接口，不写实现：

```python
# src/data/polymarket.py - 接口定义
class PolymarketClient:
    def get_markets(self, limit: int = 20) -> list[dict]:
        """获取热门市场列表"""
        ...

    def get_market_detail(self, condition_id: str) -> dict:
        """获取单个市场详情"""
        ...
```

```python
# src/core/analyzer.py - 接口定义
class MarketAnalyzer:
    def analyze(self, markets: list[dict]) -> str:
        """用 Claude 分析市场数据，返回简报文本"""
        ...
```

```python
# src/external/telegram.py - 接口定义
class TelegramBot:
    def send_report(self, text: str) -> bool:
        """发送分析报告到频道"""
        ...
```

> **核心原则**：接口先行，实现后补。先把数据流打通，再填充细节。

---

### 第三步：实现数据层

```python
# src/data/polymarket.py
import requests
from loguru import logger

CLOB_BASE = "https://clob.polymarket.com"

class PolymarketClient:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})

    def get_markets(self, limit: int = 20) -> list[dict]:
        """获取活跃市场，按成交量排序"""
        try:
            resp = self.session.get(
                f"{CLOB_BASE}/markets",
                params={"limit": limit, "active": "true"},
                timeout=10
            )
            resp.raise_for_status()
            data = resp.json()
            return data.get("data", [])
        except Exception as e:
            logger.error(f"获取市场数据失败: {e}")
            return []

    def get_market_prices(self, token_ids: list[str]) -> dict:
        """批量获取市场当前价格（即概率）"""
        try:
            resp = self.session.get(
                f"{CLOB_BASE}/prices",
                params={"token_ids": ",".join(token_ids)},
                timeout=10
            )
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            logger.error(f"获取价格失败: {e}")
            return {}
```

> **调试技巧**：先在 Python REPL 里手动调用 API，确认返回结构，再写代码。
> ```python
> import requests
> r = requests.get("https://clob.polymarket.com/markets?limit=3&active=true")
> print(r.json()["data"][0].keys())
> ```

---

### 第四步：实现 AI 分析层

```python
# src/core/analyzer.py
import anthropic
from loguru import logger

class MarketAnalyzer:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)

    def analyze(self, markets: list[dict]) -> str:
        """将市场数据喂给 Claude，生成中文简报"""
        if not markets:
            return "暂无市场数据"

        # 格式化数据，只保留关键字段，减少 token 消耗
        market_summary = []
        for m in markets[:10]:  # 只取前10个
            tokens = m.get("tokens", [])
            yes_price = next((t["price"] for t in tokens if t.get("outcome") == "Yes"), "N/A")
            market_summary.append(
                f"- {m.get('question', '未知')} | Yes概率: {yes_price} | 成交量: ${m.get('volume', 0):,.0f}"
            )

        market_text = "\n".join(market_summary)

        prompt = f"""你是一个预测市场分析师。以下是 Polymarket 今日热门市场数据：

{market_text}

请用中文生成一份简洁的市场简报（200字以内），包括：
1. 最值得关注的2-3个市场及其含义
2. 整体市场情绪判断
3. 一句话投资者提示

格式要适合 Telegram 消息，使用 emoji 增加可读性。"""

        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text
        except Exception as e:
            logger.error(f"Claude 分析失败: {e}")
            return "AI 分析暂时不可用"
```

---

### 第五步：实现 Telegram 推送层

```python
# src/external/telegram.py
import requests
from loguru import logger

class TelegramBot:
    def __init__(self, token: str, chat_id: str):
        self.token = token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{token}"

    def send_report(self, text: str) -> bool:
        """发送消息，自动处理长文本截断"""
        # Telegram 单条消息上限 4096 字符
        if len(text) > 4000:
            text = text[:4000] + "\n...(已截断)"

        try:
            resp = requests.post(
                f"{self.base_url}/sendMessage",
                json={
                    "chat_id": self.chat_id,
                    "text": text,
                    "parse_mode": "Markdown"
                },
                timeout=10
            )
            resp.raise_for_status()
            logger.info("报告发送成功")
            return True
        except Exception as e:
            logger.error(f"Telegram 发送失败: {e}")
            return False
```

---

### 第六步：配置管理

```python
# src/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
    SCHEDULE_HOUR = int(os.getenv("SCHEDULE_HOUR", "9"))   # 每天9点推送
    MARKET_LIMIT = int(os.getenv("MARKET_LIMIT", "20"))

    @classmethod
    def validate(cls):
        missing = [k for k, v in {
            "ANTHROPIC_API_KEY": cls.ANTHROPIC_API_KEY,
            "TELEGRAM_BOT_TOKEN": cls.TELEGRAM_BOT_TOKEN,
            "TELEGRAM_CHAT_ID": cls.TELEGRAM_CHAT_ID,
        }.items() if not v]
        if missing:
            raise ValueError(f"缺少环境变量: {', '.join(missing)}")
```

```bash
# .env.example
ANTHROPIC_API_KEY=sk-ant-...
TELEGRAM_BOT_TOKEN=123456:ABC-...
TELEGRAM_CHAT_ID=-100123456789
SCHEDULE_HOUR=9
MARKET_LIMIT=20
```

---

### 第七步：主程序 + 定时调度

```python
# src/main.py
import schedule
import time
from loguru import logger
from config import Config
from data.polymarket import PolymarketClient
from core.analyzer import MarketAnalyzer
from external.telegram import TelegramBot

def run_daily_report():
    """核心流程：拉数据 → AI分析 → 推送"""
    logger.info("开始生成每日市场简报...")

    # 1. 拉数据
    client = PolymarketClient()
    markets = client.get_markets(limit=Config.MARKET_LIMIT)
    logger.info(f"获取到 {len(markets)} 个市场")

    # 2. AI 分析
    analyzer = MarketAnalyzer(Config.ANTHROPIC_API_KEY)
    report = analyzer.analyze(markets)

    # 3. 推送
    bot = TelegramBot(Config.TELEGRAM_BOT_TOKEN, Config.TELEGRAM_CHAT_ID)
    header = f"📊 *Polymarket 每日简报*\n\n"
    bot.send_report(header + report)

def main():
    Config.validate()
    logger.add("logs/bot.log", rotation="1 day", retention="7 days")

    # 立即运行一次
    run_daily_report()

    # 定时每天运行
    schedule.every().day.at(f"{Config.SCHEDULE_HOUR:02d}:00").do(run_daily_report)
    logger.info(f"定时任务已设置，每天 {Config.SCHEDULE_HOUR}:00 运行")

    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()
```

---

### 第八步：依赖与启动

```txt
# requirements.txt
anthropic==0.40.0
requests==2.31.0
python-dotenv==1.0.0
schedule==1.2.1
loguru==0.7.2
```

```bash
# 安装依赖
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 填入你的 key

# 运行
cd src && python main.py
```

---

## 🐛 Debug 实录

### 问题1：Polymarket API 返回空数据

**预期**：`data` 字段有市场列表
**实际**：返回 `{"data": [], "next_cursor": ""}`

**排查过程**：
```python
# 先裸调 API 看原始响应
import requests
r = requests.get("https://clob.polymarket.com/markets?active=true&limit=5")
print(r.status_code, r.json())
```

**原因**：`active=true` 参数需要用布尔值，某些端点用 `"true"` 字符串，某些用 `1`。

**修复**：改用 `params={"active": True}` 让 requests 自动处理。

---

### 问题2：Telegram Markdown 解析报错

**错误**：`Can't parse entities: can't find end of the entity`

**原因**：Claude 返回的文本里有未转义的 `_` 或 `*`。

**修复**：发送时改用 `parse_mode: "HTML"` 或对特殊字符转义：

```python
import re

def escape_markdown(text: str) -> str:
    """转义 Telegram MarkdownV2 特殊字符"""
    special_chars = r'_*[]()~`>#+-=|{}.!'
    return re.sub(f'([{re.escape(special_chars)}])', r'\\\1', text)
```

---

### 问题3：Claude 分析结果不稳定

**现象**：有时返回英文，有时格式乱

**修复**：在 prompt 里加强约束：

```python
prompt = f"""...
【强制要求】：
- 必须用简体中文回复
- 必须使用以下格式，不得偏离：
  🔥 重点市场：...
  📈 市场情绪：...
  💡 提示：...
"""
```

---

## 🔑 胶水编码核心心法

| 原则 | 在本项目的体现 |
|------|--------------|
| 能抄不写 | 直接用 Polymarket 公开 API，不自建数据爬虫 |
| 接口先行 | 先定义三个类的方法签名，再填实现 |
| 一次只改一个模块 | 数据层、分析层、推送层分开调试 |
| 上下文是第一性要素 | prompt 里给 Claude 足够的市场背景 |
| 奥卡姆剃刀 | 不做 Web UI，不做数据库，只做核心流程 |
| Debug 给预期 vs 实际 | 每个问题都先打印原始响应再分析 |

---

## 🔧 扩展方向（按需添加）

- **加命令交互**：用 `python-telegram-bot` 库支持 `/query <关键��>` 查询特定市场
- **加数据持久化**：用 SQLite 存历史价格，分析趋势变化
- **加多市场对比**：同时监控多个预测平台（Manifold、Metaculus）
- **加告警**：某市场概率剧变超过 10% 时立即推送

---

## 📚 参考资源

- [Polymarket CLOB API 文档](https://docs.polymarket.com/)
- [Anthropic Python SDK](https://github.com/anthropics/anthropic-sdk-python)
- [python-telegram-bot 文档](https://python-telegram-bot.org/)
- [schedule 库文档](https://schedule.readthedocs.io/)

---

**版本**: 1.0
**更新日期**: 2026-03-18
**作者**: Vibe Coding 社区
