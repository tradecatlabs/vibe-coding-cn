#  telegram Markdown 代码块格式修复记录 2025-12-15

## 问题

排盘完成后发送消息报错：
```
❌ 排盘失败: Can't parse entities: can't find end of the entity starting at byte offset 168
```

## 原因

`bot.py` 中 `header` 消息的 Markdown 代码块格式错误。

原代码使用字符串拼接，在 ``` 后面加了 `\n`，导致 Telegram Markdown 解析器无法正确识别代码块边界：

```python
# 错误写法
header = (
    "```\n"
    f"{filename}\n"
    "```\n"
)
```

## 修复

改用三引号字符串，确保 ``` 单独成行：

```python
# 正确写法
header = f"""报告见附件
```
{filename}
{ai_filename}
```
"""
```

## 修改文件

- `services/telegram-service/src/bot.py` 第 293-308 行
