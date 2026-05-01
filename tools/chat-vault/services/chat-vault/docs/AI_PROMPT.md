# AI Chat Converter - AI 助手完全指南

> **把这个文档发给 AI 助手，它就知道怎么帮你用这个工具了**

---

## 🎯 这是什么？

一个把 Codex、Kiro、Gemini、Claude 的聊天记录全部存到一个 SQLite 数据库的工具。

**数据库位置**: `项目目录/output/chat_history.db`

---

## 🚀 怎么启动？

### 方式一：双击启动（推荐）
```bash
./start.sh          # Linux/macOS
start.bat           # Windows（双击）
```

### 方式二：命令行
```bash
cd ai-chat-converter
python src/main.py --watch   # 持续监控（推荐）
python src/main.py           # 同步一次就退出
```

### 方式三：后台运行
```bash
nohup ./start.sh > /dev/null 2>&1 &
```

---

## 📊 数据库长啥样？

### 主表：sessions

| 字段 | 说明 | 例子 |
|------|------|------|
| file_path | 主键，文件路径 | `/home/user/.codex/sessions/xxx.jsonl` |
| session_id | 会话ID | `019b2164-168c-7133-9b1f-5d24fea1d3e1` |
| source | 来源 | `codex` / `kiro` / `gemini` / `claude` |
| cwd | 工作目录 | `/home/user/projects/myapp` |
| messages | 消息内容（JSON） | `[{"time":"...", "role":"user", "content":"..."}]` |
| start_time | 开始时间 | `2025-12-18T10:30:00` |
| token_count | Token 数量 | `1234` |

---

## 🔍 常用查询（直接复制用）

### 1. 看看有多少数据

```sql
SELECT source, COUNT(*) as 会话数, SUM(token_count) as Token总数
FROM sessions 
GROUP BY source;
```

### 2. 最近的 10 个会话

```sql
SELECT session_id, source, cwd, start_time, token_count
FROM sessions
ORDER BY start_time DESC
LIMIT 10;
```

### 3. 搜索包含某个词的对话

```sql
SELECT session_id, source, cwd, start_time
FROM sessions
WHERE messages LIKE '%要搜索的词%'
ORDER BY start_time DESC
LIMIT 20;
```

### 4. 查某个项目的所有对话

```sql
SELECT session_id, source, start_time, token_count
FROM sessions
WHERE cwd LIKE '%项目名%'
ORDER BY start_time;
```

### 5. 看某个会话的完整内容

```sql
SELECT messages FROM sessions WHERE session_id = '会话ID';
```

### 6. 统计每天用了多少 Token

```sql
SELECT 
    date(start_time) as 日期,
    SUM(token_count) as Token数
FROM sessions
GROUP BY 日期
ORDER BY 日期 DESC
LIMIT 7;
```

### 7. 统计每个来源的 Token

```sql
SELECT source, SUM(token_count) as tokens
FROM sessions
GROUP BY source
ORDER BY tokens DESC;
```

---

## 💻 命令行用法

| 命令 | 干啥的 |
|------|--------|
| `python src/main.py` | 同步一次 |
| `python src/main.py -w` | 持续监控（推荐） |
| `python src/main.py --stats` | 看统计信息 |
| `python src/main.py --search "关键词"` | 搜索 |
| `python src/main.py --export json` | 导出 JSON |
| `python src/main.py --export csv` | 导出 CSV |
| `python src/main.py --prune` | 清理已删除文件的记录 |

---

## 🐍 用 Python 查询

```python
import sqlite3
import json

# 连接数据库
db = sqlite3.connect('output/chat_history.db')

# 查所有 Codex 会话
for row in db.execute("SELECT session_id, cwd, token_count FROM sessions WHERE source='codex'"):
    print(f"{row[0]}: {row[2]} tokens - {row[1]}")

# 搜索包含 "python" 的对话
for row in db.execute("SELECT session_id, source FROM sessions WHERE messages LIKE '%python%'"):
    print(f"[{row[1]}] {row[0]}")

# 获取某个会话的消息
row = db.execute("SELECT messages FROM sessions WHERE session_id=?", ('会话ID',)).fetchone()
if row:
    messages = json.loads(row[0])
    for msg in messages:
        print(f"{msg['role']}: {msg['content'][:100]}...")
```

---

## 📁 文件在哪？

```
ai-chat-converter/
├── start.sh              ← 双击这个启动
├── output/
│   ├── chat_history.db   ← 数据库在这
│   └── logs/             ← 日志在这
└── src/
    └── main.py           ← 主程序
```

---

## ❓ AI 助手任务示例

当用户说这些话时，你应该这样做：

| 用户说 | 你做 |
|--------|------|
| "帮我查最近的对话" | 执行最近会话 SQL |
| "搜索关于 Python 的讨论" | 用 `--search` 或 SQL 搜索 |
| "这个月用了多少 Token" | 执行 Token 统计 SQL |
| "导出所有 Codex 记录" | `python src/main.py --export json --source codex` |
| "启动监控" | `./start.sh` 或 `python src/main.py -w` |
| "数据库在哪" | `output/chat_history.db` |

---

## 🔧 出问题了？

### 问题：找不到数据库
```bash
# 先运行一次同步
python src/main.py
```

### 问题：依赖没装
```bash
pip install -r requirements.txt
```

### 问题：权限不够
```bash
chmod +x start.sh
```

---

## 📊 消息格式

数据库里的 `messages` 字段是 JSON 数组：

```json
[
  {
    "time": "2025-12-18T10:30:00",
    "role": "user",
    "content": "帮我写个 Python 脚本"
  },
  {
    "time": "2025-12-18T10:30:05",
    "role": "ai",
    "content": "好的，这是一个简单的脚本..."
  }
]
```

- `role`: `user`（用户）或 `ai`（AI 回复）
- `time`: ISO 格式时间
- `content`: 消息内容
