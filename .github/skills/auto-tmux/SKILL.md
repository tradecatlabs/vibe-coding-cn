---
name: auto-tmux
description: "需要用tmux原生命令列出session/window/pane、capture-pane读取终端、确认目标后send-keys发送输入，或排查tmux/oh-my-tmux配置时使用；不提供已退役的蜂群、报告或自动救援封装。"
---

# auto-tmux

用tmux原生CLI完成明确授权的终端观察与操作。原27个自研封装脚本已退役；不依赖旧命令，不重造包装层。

## When to Use This Skill

- 列出本机tmux会话、窗口和pane，定位用户指定的终端。
- 读取指定pane近期输出，排查等待输入或报错状态。
- 在用户已授权且目标、当前程序与输入含义明确时发送文字或按键。
- 查阅tmux与oh-my-tmux的已有配置和快捷键。

## Not For / Boundaries

- 不自动启动AI worker、不创建蜂群、不提供原锁/任务状态/报告包协议或自动确认机制。
- 不因为旧参考中有命令就运行已退役的脚本；历史封装材料只作记录，当前操作以本文件为准。
- 不安装tmux，不改用户主配置，不接管未知pane，不操作真实密码或凭据输入。
- 远程SSH、录制会话内容、广播、关闭会话、发送中断及破坏性命令需要针对目标与副作用的明确授权。
- 删除封装后没有原程序的自动安全检查、预览和锁保证；下面是操作约束，不声称提供等价自动防护。

## Quick Reference

### 1. 确认本机前置条件

```bash
command -v tmux
tmux -V
```

缺少程序或连接不到指定server时报告实际失败，不自动安装或换到未知server。

### 2. 只读列出目标

```bash
tmux list-sessions
tmux list-windows -a -F '#{session_name}:#{window_index} #{window_name}'
tmux list-panes -a -F '#{pane_id} #{session_name}:#{window_index}.#{pane_index} #{pane_current_command} #{pane_current_path}'
```

只选择用户授权的目标。使用列出的稳定pane_id，不能根据第一个窗口、相似名称或旧截图猜目标。

### 3. 读取当前上下文

先把占位符替换成刚核对的真实pane_id；未替换时不能执行后续发送。

```bash
target='<已核对的pane_id>'
tmux display-message -p -t "$target" '#{session_name}:#{window_index}.#{pane_index} #{pane_current_command} #{pane_current_path}'
tmux capture-pane -p -S -120 -t "$target"
```

输出可能含个人资料或凭据，先脱敏再展示；没有授权不写日志或上传。读取成功不授权继续控制。

### 4. 明确授权后，逐次发送

发送前重新列出并capture，确认pane仍存在、当前程序及其解释输入的方式未变化。
只在已确认的shell里使用下面的无害示例；在模型UI、数据库、安装确认或密码提示中不能套用。

```bash
tmux send-keys -t "$target" -l 'printf "hello\\n"'
tmux send-keys -t "$target" Enter
```

`-l`按字面文字发送，不把文本误识别为tmux按键名称；文字与Enter分开不是事务，发送中途状态变化应停止。
完成后再次capture检查真实结果。不自动发送y、Ctrl-C、Ctrl-D或广播，不通过重试重复不可逆操作。

### 5. 配置与故障定位

- [原生命令参考](references/api.md)、[入门说明](references/getting_started.md)、[故障排查](references/troubleshooting.md)用于按需查阅。
- `assets/tmux-src`和`assets/oh-my-tmux`仍指向固定上游，仅查阅不代表安装或写用户配置。
- 原蜂群、脚本API、自动救援、锁和报告材料属于历史说明，不是当前承诺；不从历史材料恢复实现。

## Examples

### Example 1：只读查看一个报错终端

- 输入：用户指定的session及允许读取的输出范围。
- 操作：列出目标，核对pane_id、当前程序和路径，capture指定范围，脱敏后汇报错误。
- 验收：证据绑定实际pane；没有发送输入、改配置或读取无关会话。

### Example 2：在已确认的测试shell中发送命令

- 输入：明确授权的测试pane和无副作用命令。
- 操作：重新capture确认shell，字面发送命令，再单独发送Enter，capture结果。
- 验收：只影响指定pane，输出符合独立预期；不把发送成功当命令执行成功。

### Example 3：终端停在确认提示

- 输入：用户要判断卡住原因，不等于授权自动确认。
- 操作：只读capture，判断提示对应的程序、动作与后果；目标或权限不清时说明缺口，不发送猜测按键。
- 验收：给出实际等待状态和下一步；没有自动同意安装、删除、提权或密码操作。

## References

- [当前参考导航](references/index.md)
- [tmux原生命令](references/api.md)
- [入门与术语](references/getting_started.md)
- [故障排查](references/troubleshooting.md)
- [参考材料状态](references/README.md)

## Maintenance

只维护操作指令、来源与权限边界，不再维护自动化程序、共享任务锁、日志报告或多Agent执行框架。
原生发现、原生CLI隔离示例及静态审阅分别报告；未做模型压力实测时不得宣称模型会稳定遵守所有边界。
