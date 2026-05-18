# auto-tmux scripts

`scripts/` 存放 `auto-tmux` 的可执行辅助脚本，把常见 tmux 操作封装成安全、可复用、可审计的命令。

## 入口

- [`auto-tmux.sh`](./auto-tmux.sh) - 统一命令入口，支持拓扑、读取、发送、巡检、救援、录制、等待和 AI 工作台初始化。

## 常用命令

```bash
# 查看帮助
skills/auto-tmux/scripts/auto-tmux.sh help

# 查看 tmux 拓扑
skills/auto-tmux/scripts/auto-tmux.sh topology

target="$(tmux list-panes -t ai-hub:worker1 -F '#S:#I.#P' | head -n 1)"

# 读取指定 pane 最近 80 行
skills/auto-tmux/scripts/auto-tmux.sh capture -t "$target" -n 80

# 发送命令并回车
skills/auto-tmux/scripts/auto-tmux.sh send -t "$target" --text "make test" --enter

# 扫描某个 session 的错误
skills/auto-tmux/scripts/auto-tmux.sh scan --session ai-hub --pattern "ERROR|Traceback"
```

## 安全约束

- 默认对捕获输出做密钥脱敏。
- `send` 会先打印目标 pane 最近上下文，再发送按键。
- 危险命令默认拒绝，必须显式 `--force`。
- 批量操作必须使用明确的 session/window/pane 目标。
