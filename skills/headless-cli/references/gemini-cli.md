# Gemini CLI 参数参考

> 来源: [官方文档](https://geminicli.com/docs/get-started/configuration/)

## 安装

```bash
npm install -g @anthropic-ai/gemini-cli
```

## 认证

首次运行会引导 Google 账号登录，或设置环境变量：
```bash
export GEMINI_API_KEY="YOUR_API_KEY"
```

## 核心命令行参数

| 参数 | 说明 | 示例 |
|:---|:---|:---|
| `--model <model>` | 指定模型 | `--model gemini-2.5-flash` |
| `--yolo` | YOLO 模式，自动批准所有工具调用 | `gemini --yolo` |
| `--approval-mode <mode>` | 审批模式: `default`/`auto_edit`/`yolo` | `--approval-mode auto_edit` |
| `--allowed-tools <tools>` | 允许的工具列表（逗号分隔） | `--allowed-tools ''` (禁用所有) |
| `--output-format <format>` | 输出格式: `text`/`json`/`stream-json` | `--output-format text` |
| `--sandbox` / `-s` | 启用沙箱模式 | `gemini -s` |
| `--prompt <prompt>` / `-p` | 非交互模式，直接传入提示词 | `gemini -p "query"` |
| `--prompt-interactive <prompt>` / `-i` | 交互模式，带初始提示词 | `gemini -i "explain"` |
| `--debug` / `-d` | 启用调试模式 | `gemini -d` |

## 可用模型

- `gemini-2.5-flash` - 快速模型
- `gemini-2.5-pro` - 高级模型
- `gemini-3-flash-preview` - 最新 Flash
- `gemini-3-pro-preview` - 最新 Pro

## 无头模式用法

```bash
# 基础无头调用（管道输入）
cat input.txt | gemini -p "Your prompt" --output-format text

# 禁用工具调用（纯文本输出）
cat input.txt | gemini -p "Your prompt" --output-format text --allowed-tools ''

# YOLO 模式（跳过所有确认）
gemini --yolo "Your prompt"

# 或使用 approval-mode
gemini --approval-mode yolo "Your prompt"
```

## 配置文件

配置存储在 `~/.gemini/settings.json` 或项目 `.gemini/settings.json`：

```json
{
  "security": {
    "disableYoloMode": false
  },
  "model": {
    "name": "gemini-2.5-flash"
  }
}
```

## 代理配置

```bash
export http_proxy=http://127.0.0.1:9910
export https_proxy=http://127.0.0.1:9910
```

## 常见问题

1. **MCP 初始化慢**: 使用 `--allowed-tools ''` 跳过
2. **超时**: 使用 `timeout` 命令包装
3. **输出包含日志**: 重定向 stderr `2>/dev/null`
