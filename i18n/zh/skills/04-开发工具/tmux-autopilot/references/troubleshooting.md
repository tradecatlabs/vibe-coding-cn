# Troubleshooting & Edge Cases

格式：症状 → 可能原因 → 诊断 → 修复

- `no such session` / `no current client`  
  → 会话名写错或未 attach  
  → `tmux list-sessions` 校验；需要时 `tmux new -s <name>`  
  → 重试带绝对目标：`-t <s:w.p>`

- 发送无效、卡在 copy-mode  
  → pane 处于 copy-mode  
  → `tmux display-message -pt <t> '#{pane_in_mode}'`  
  → 先 `tmux send-keys -t <t> Escape` 再发命令

- 状态栏符号混乱、重复一行  
  → 终端宽字符/字体问题或重复加载配置  
  → `tmux -f /dev/null -L test` 检查；确认 `LC_CTYPE` 使用 UTF-8；清理多重 source  
  → 使用仓库版 `.tmux.conf.local` 默认字体设置

- 广播误伤其他 pane  
  → `synchronize-panes` 未关闭  
  → `tmux show-window-options | grep synchronize`  
  → `tmux set-window-option synchronize-panes off`

- Powerline 符号缺失  
  → 字体未带 Powerline codepoints  
  → 切换到带符号字体或安装 `PowerlineSymbols.otf`，再重载 `tmux source-file ~/.tmux.conf.local`

- `prefix` 无反应  
  → 其他程序占用或配置被覆盖  
  → `grep prefix ~/.tmux.conf.local` 确认；可改为 `C-b` 并加 `#!important`

- 长任务输出缺失  
  → 未开启 pipe-pane / buffer 溢出  
  → 提前 `pipe-pane` 到文件；或 `capture-pane -S -100000` 抓历史
