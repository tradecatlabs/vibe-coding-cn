# Claude Code CLI 参数参考

> 来源: [官方文档](https://docs.anthropic.com/en/docs/claude-code/cli-reference)

## 安装

```bash
npm install -g @anthropic-ai/claude-code
```

## 认证

需要 Anthropic API Key 或 Claude Pro/Max 订阅：
```bash
export ANTHROPIC_API_KEY="YOUR_API_KEY"
```

## 核心命令

| 命令 | 说明 | 示例 |
|:---|:---|:---|
| `claude` | 启动交互式 REPL | `claude` |
| `claude "query"` | 带初始提示词启动 | `claude "explain this"` |
| `claude -p "query"` | Print 模式，执行后退出 | `claude -p "review code"` |
| `claude -c` | 继续最近的对话 | `claude -c` |
| `claude -c -p "query"` | 继续对话（Print 模式） | `claude -c -p "run tests"` |
| `claude -r "id" "query"` | 恢复指定会话 | `claude -r "abc123" "continue"` |
| `claude update` | 更新到最新版本 | `claude update` |
| `claude mcp` | 配置 MCP 服务器 | `claude mcp add server` |

## CLI 参数

| 参数 | 说明 | 示例 |
|:---|:---|:---|
| `--model` | 指定模型 | `--model claude-sonnet-4` |
| `--output-format` | 输出格式: `text`/`json`/`stream-json` | `--output-format json` |
| `--max-turns` | 限制对话轮数 | `--max-turns 3` |
| `--dangerously-skip-permissions` | 跳过所有权限确认 (YOLO) | 见下方 |
| `--allowedTools` | 允许的工具列表 | `--allowedTools "Write" "Bash(git *)"` |
| `--disallowedTools` | 禁止的工具列表 | `--disallowedTools "Bash(rm *)"` |
| `--add-dir` | 添加额外工作目录 | `--add-dir ./apps ./lib` |
| `--verbose` | 启用详细日志 | `--verbose` |
| `--continue` | 继续最近对话 | `--continue` |
| `--resume` | 恢复指定会话 | `--resume abc123` |

## 可用模型

- `claude-sonnet-4` - 平衡模型 (默认)
- `claude-opus-4` - 最强模型
- `claude-opus-4.5` - 最新最强

## 无头模式用法

```bash
# Print 模式（非交互，执行后退出）
claude -p "review this code" --output-format text

# 管道输入
cat input.txt | claude -p "explain these errors"

# YOLO 模式（跳过所有权限确认）
claude --dangerously-skip-permissions "Your prompt"

# 别名设置
alias cc='claude --dangerously-skip-permissions'

# 继续对话 + Print 模式（适合脚本）
claude -c -p "show progress"
```

## 交互式命令 (Slash Commands)

| 命令 | 说明 |
|:---|:---|
| `/help` | 显示所有命令 |
| `/config` | 配置设置 |
| `/allowed-tools` | 配置工具权限 |
| `/mcp` | 管理 MCP 服务器 |
| `/vim` | 启用 vim 编辑模式 |

## 配置文件

- 用户设置: `~/.claude/settings.json`
- 项目设置: `.claude/settings.json`
- 本地设置: `.claude/settings.local.json`

```json
{
  "model": "claude-sonnet-4",
  "permissions": {
    "allowedTools": ["Read", "Write", "Bash(git *)"],
    "deny": ["Read(./.env)", "Bash(rm *)"]
  }
}
```

## 上下文文件 (CLAUDE.md)

- 全局: `~/.claude/CLAUDE.md`
- 项目: `./CLAUDE.md`
- 子目录: 组件特定指令

## 深度思考触发词

强度递增：
- `think` - 基础思考
- `think hard` - 深入思考
- `think harder` - 更深入
- `ultrathink` - 最深度思考

## 常见问题

1. **权限弹窗**: 使用 `--dangerously-skip-permissions`
2. **上下文过长**: 使用 `/compact` 或 `/clear`
3. **回退更改**: 使用 `/rewind`
