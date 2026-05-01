# Codex CLI 参数参考

> 来源: [官方文档](https://developers.openai.com/codex/cli/reference)

## 安装

```bash
npm install -g @openai/codex
```

## 认证

```bash
# 方式 1: 浏览器 OAuth (ChatGPT 账号)
codex login

# 方式 2: API Key
printenv OPENAI_API_KEY | codex login --with-api-key

# 检查登录状态
codex login status
```

## 核心命令

| 命令 | 说明 | 示例 |
|:---|:---|:---|
| `codex` | 启动交互式 TUI | `codex` |
| `codex "prompt"` | 带提示词启动 | `codex "explain this"` |
| `codex exec` / `codex e` | 非交互模式 | `codex exec "fix bugs"` |
| `codex resume` | 恢复会话 | `codex resume --last` |
| `codex apply` / `codex a` | 应用 Cloud 任务的 diff | `codex apply TASK_ID` |
| `codex mcp` | 管理 MCP 服务器 | `codex mcp add server` |
| `codex completion` | 生成 shell 补全 | `codex completion zsh` |

## 全局参数

| 参数 | 说明 | 示例 |
|:---|:---|:---|
| `--model, -m` | 指定模型 | `-m gpt-5.5` |
| `--sandbox, -s` | 沙箱策略: `read-only`/`workspace-write`/`danger-full-access` | `-s workspace-write` |
| `--ask-for-approval, -a` | 审批模式: `untrusted`/`on-failure`/`on-request`/`never` | `-a on-failure` |
| `--full-auto` | 自动化预设 (workspace-write + on-failure) | `--full-auto` |
| `--dangerously-bypass-approvals-and-sandbox` / `--yolo` | 跳过所有审批和沙箱 | `--yolo` |
| `--search` | 启用网页搜索 | `--search` |
| `--add-dir` | 添加额外写入目录 | `--add-dir ./other` |
| `--enable` | 启用功能标志 | `--enable web_search_request` |
| `--disable` | 禁用功能标志 | `--disable feature_name` |
| `--config, -c` | 配置覆盖 | `-c model_reasoning_effort="xhigh"` |
| `--image, -i` | 附加图片 | `-i image.png` |
| `--cd, -C` | 设置工作目录 | `-C /path/to/project` |
| `--profile, -p` | 配置文件 profile | `-p my-profile` |
| `--oss` | 使用本地开源模型 (Ollama) | `--oss` |

## codex exec 专用参数

| 参数 | 说明 | 示例 |
|:---|:---|:---|
| `--json` | 输出 JSONL 格式 | `--json` |
| `--output-last-message, -o` | 保存最终消息到文件 | `-o result.txt` |
| `--output-schema` | JSON Schema 验证输出 | `--output-schema schema.json` |
| `--color` | 颜色输出: `always`/`never`/`auto` | `--color never` |
| `--skip-git-repo-check` | 允许在非 Git 目录运行 | `--skip-git-repo-check` |

## 可用模型

- `gpt-5.5` - 最新推荐模型
- `gpt-5.4` - 上一代兼容模型
- `gpt-5.2` - 旧版兼容模型

## 推理强度配置

```bash
-c model_reasoning_effort="low"    # 快速
-c model_reasoning_effort="medium" # 平衡
-c model_reasoning_effort="high"   # 深度
-c model_reasoning_effort="xhigh"  # 最深
```

## 无头模式用法

```bash
# 非交互执行
codex exec "fix all linting errors"

# 管道输入
echo "explain this error" | codex exec -

# YOLO 模式（跳过所有确认和沙箱）
codex --yolo "Your prompt"

# 或完整写法
codex --dangerously-bypass-approvals-and-sandbox "Your prompt"

# full-auto 模式（推荐的自动化方式）
codex --full-auto "Your prompt"

# 完整 YOLO 配置别名
alias c='codex --enable web_search_request -m gpt-5.5 -c model_reasoning_effort="xhigh" --yolo'

# 恢复最近会话
codex resume --last
codex exec resume --last "continue"
```

## 配置文件

配置存储在 `~/.codex/config.toml`：

```toml
model = "gpt-5.5"
sandbox = "workspace-write"
ask_for_approval = "on-failure"

[features]
web_search_request = true
```

## 常见问题

1. **审批弹窗**: 使用 `--yolo` 或 `--full-auto`
2. **需要联网**: 使用 `--search` 或 `--enable web_search_request`
3. **推理不够深**: 使用 `-c model_reasoning_effort="high"`
4. **非 Git 目录**: 使用 `--skip-git-repo-check`
