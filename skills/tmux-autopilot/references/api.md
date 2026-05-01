# API / CLI / Config Reference

## 结构化速查（按场景）

### 拓扑与定位
- 列 session：`tmux list-sessions`
- 列窗口（含 flag）：`tmux list-windows -a -F '#S:#I:#W#F'`
- 列 pane：`tmux list-panes -a -F '#S:#I.#P #{pane_current_command} #{pane_title}'`

### 读取输出
- 抓取最近 N 行：`tmux capture-pane -t <s:w.p> -p -S -120`
- 全量抓取到文件：`tmux capture-pane -t <s:w.p> -p -S -100000 > pane.log`
- 实时镜像：`tmux pipe-pane -t <s:w.p> -o 'cat >> /tmp/pane.log'`

### 发送按键/命令
- 发送字符串+回车：`tmux send-keys -t <s:w.p> "command here" Enter`
- 发送单键：`tmux send-keys -t <s:w.p> C-c`、`Escape`、`Space`
- 发送确认：`tmux send-keys -t <s:w.p> "y" Enter`
- 退出 copy-mode 后再发：`tmux send-keys -t <s:w.p> Escape`

### 广播 / 同步
- 开启窗口广播：`tmux set-window-option synchronize-panes on`
- 关闭广播：`tmux set-window-option synchronize-panes off`
- 广播一次性命令（推荐先列出名单）：配合上面 `list-panes` 逐一 send-keys

### session/window 管理
- 新建：`tmux new-session -d -s <name> -n <win> 'cmd'`
- 新窗口：`tmux new-window -t <s> -n <name> 'cmd'`
- 重命名：`tmux rename-window -t <s:w> <new>`
- 分屏：`tmux split-window -t <s:w> -h|-v 'cmd'`

### oh-my-tmux 关键配置
- 前缀：默认 `set -g prefix C-a`；若想回到 `C-b` 在 `~/.tmux.conf.local` 中加 `#!important`。
- 主题/状态栏调整：在 `~/.tmux.conf.local` 修改对应变量（按 README 指引）。
- 升级/重载：`tmux source-file ~/.tmux.conf.local`

## 常见误用与修复

- 错 pane：始终用 `<s:w.p>`，避免仅用 `-t 0`（易撞到当前 pane）。
- 广播遗留未关：操作完立即 `synchronize-panes off`，避免误输入。
- Unicode 宽度导致状态栏错位：优先使用仓库内 `.tmux.conf.local` 默认设置；若仍异常用 `tmux -f /dev/null -L test` 排查终端字体。
