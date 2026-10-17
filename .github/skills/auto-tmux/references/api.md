# tmux原生CLI参考

先遵守[当前Skill合同](../SKILL.md)：确认server、目标和当前程序，只读定位后再决定是否有发送权限。
原封装不再提供自动安全扫描、预览或锁；不要将这些命令当成同等防护的自动执行器。

## 只读观察

```bash
tmux -V
tmux list-sessions
tmux list-windows -a -F '#{session_name}:#{window_index} #{window_name}'
tmux list-panes -a -F '#{pane_id} #{session_name}:#{window_index}.#{pane_index} #{pane_current_command} #{pane_current_path}'
```

设置刚核对的稳定pane_id后才能继续：

```bash
target='<已核对的pane_id>'
tmux display-message -p -t "$target" '#{pane_current_command} #{pane_current_path} #{pane_in_mode}'
tmux capture-pane -p -S -120 -t "$target"
```

输出先脱敏，不默认写日志或读取无关会话。

## 明确授权后的输入

对已确认shell发送字面文字，再单独发送Enter；示例见父级SKILL.md。
`send-keys`、退出copy-mode、发送中断、确认提示和新建/关闭会话都会改变状态，不属于只读诊断。
不自动发送y、Escape、Ctrl-C或Ctrl-D；不默认开启同步广播，不猜测密码提示的回答。

## 配置来源

上游在`assets/tmux-src`和`assets/oh-my-tmux`的固定引用中可读。
修改用户配置、重载配置或安装字体属于另外的写入操作，本参考不默认执行；版本行为用当前`tmux -V`与本机man手册核对。
