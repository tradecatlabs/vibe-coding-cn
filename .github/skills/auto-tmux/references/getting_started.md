# tmux原生操作入门

## 术语

- session：会话；window：会话内窗口；pane：窗口内终端。
- pane_id：server内定位pane的标识，优先使用刚列出的真实值。
- capture-pane：读取终端输出，不代表获得控制权限。
- send-keys：发送输入，会改变目标程序状态。
- copy-mode：终端滚动/复制模式，退出也属于发送操作。
- synchronize-panes：同步输入，会扩大影响范围，当前Skill不默认开启。
- oh-my-tmux：保留的上游配置参考，不是本次安装或用户主配置写入授权。

## 只读最短路径

```bash
command -v tmux
tmux -V
tmux list-sessions
tmux list-panes -a -F '#{pane_id} #{session_name}:#{window_index}.#{pane_index} #{pane_current_command} #{pane_current_path}'
```

确认用户指定目标后，按[当前Skill](../SKILL.md)的capture步骤读取并脱敏。
没有server或程序时报告实际状态，不自动创建会话、安装依赖或覆盖用户配置。

## 下一步

明确授权的输入示例见父级SKILL.md；诊断命令见[API参考](api.md)。
原自动封装、蜂群、锁和报告实现已退役，历史材料不是当前执行手册，不因看到旧步骤自动恢复功能。
