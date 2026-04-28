# 数据库结构 (v5)

**位置**: `项目目录/output/chat_history.db`

## sessions 表（主表）

| 字段 | 类型 | 说明 |
|------|------|------|
| file_path | TEXT | 主键，源文件路径 |
| session_id | TEXT | 会话 ID |
| source | TEXT | 来源: codex/kiro/gemini/claude |
| cwd | TEXT | 工作目录 |
| messages | TEXT | JSON 数组 |
| file_mtime | INTEGER | 文件修改时间戳 |
| start_time | TEXT | 会话开始时间 |
| token_count | INTEGER | Token 数量 |

**索引**: `idx_source`, `idx_session_id`, `idx_start_time`

## meta 表（全局统计）

| key | 说明 |
|-----|------|
| schema_version | 数据库版本 (5) |
| total_sessions | 总会话数 |
| total_messages | 总消息数 |
| total_tokens | 总 Token 数 |
| last_sync | 最后同步时间 |

## meta_{cli} 表（各 CLI 统计）

每个 CLI 独立的元信息表：`meta_codex`, `meta_kiro`, `meta_gemini`, `meta_claude`

| key | 说明 |
|-----|------|
| path | 监控路径 |
| sessions | 会话数 |
| messages | 消息数 |
| total_tokens | Token 总数 |
| last_sync | 最后同步时间 |

## 消息格式

```json
[
  {"time": "2025-12-18T10:30:00", "role": "user", "content": "..."},
  {"time": "2025-12-18T10:30:05", "role": "ai", "content": "..."}
]
```
