# Getting Started & Vocabulary

## 核心术语（10 个）

1. session：tmux 的最外层会话。
2. window：session 下的窗口，编号 `<session>:<window>`。
3. pane：窗口内分屏，编号 `<session>:<window>.<pane>`。
4. prefix：组合键前缀，oh-my-tmux 主前缀为 `Ctrl+a`，备用 `Ctrl+b`。
5. capture-pane：抓取 pane 输出到 stdout。
6. send-keys：向 pane 注入按键/命令。
7. synchronize-panes：窗口级广播开关。
8. pipe-pane：将 pane 输出流向命令/文件。
9. copy-mode：tmux 内置滚动/复制模式，需先退出再发按键。
10. .tmux.conf.local：oh-my-tmux 推荐的用户自定义文件。

## 最短路径：接管本仓库内 oh-my-tmux 并跑通命令

```bash
# 1) 确认 tmux 版本 >= 2.6
tmux -V

# 2) 软链配置（不会覆盖已有 .tmux.conf.local，如需自定义请编辑该文件）
ln -sfn /home/lenovo/zip/vibe-coding-cn/libs/external/.tmux/.tmux.conf ~/.tmux.conf
cp -n  /home/lenovo/zip/vibe-coding-cn/libs/external/.tmux/.tmux.conf.local ~/.tmux.conf.local

# 3) 启动会话并验证前缀
tmux new -s demo -n shell
# 在 tmux 内按 <Ctrl+a> ? 打开快捷键帮助，确认状态栏与主题正常

# 4) 基础自检：列窗、抓取、发送
tmux list-windows
tmux capture-pane -t demo:0.0 -p -S -10
tmux send-keys   -t demo:0.0 "echo ok" Enter
```

## 工作姿势

- 始终用绝对定位 `<session>:<window>.<pane>`；跨 session 操作更安全。
- 批量广播前先名单化：`tmux list-panes -a -F '#S:#I.#P #{pane_current_command}'`。
- 高风险按键（`Ctrl+C`、确认 `y`）先 `capture-pane` 再发送。
- 长任务用 `pipe-pane` 记录；救援/打断后再关。
