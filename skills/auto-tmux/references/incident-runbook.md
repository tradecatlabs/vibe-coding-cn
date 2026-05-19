# auto-tmux Incident Runbook

本文件用于处理 `auto-tmux` 操作事故。原则：先停止继续操作，再保留证据，最后收敛到可复盘结论。

## 误发送到错误 pane

1. 立即停止继续发送。
2. 捕获错误目标 pane 输出：

```bash
skills/auto-tmux/scripts/auto-tmux.sh capture -t <wrong-target> -n 120
```

3. 捕获原本目标 pane 输出：

```bash
skills/auto-tmux/scripts/auto-tmux.sh capture -t <expected-target> -n 120
```

4. 在 swarm state 中标记阻塞或失败：

```bash
skills/auto-tmux/scripts/swarm-state.sh task-block --id <task-id> --owner <owner> --reason "mis-sent to wrong pane" --dir /tmp/ai_swarm
```

## 误广播

1. 关闭同步面板：

```bash
tmux set-window-option synchronize-panes off
```

2. 生成全局快照：

```bash
skills/auto-tmux/scripts/auto-tmux.sh snapshot --session ai-hub --dir /tmp/auto-tmux-incident-snapshot
```

3. 生成阻塞报告：

```bash
skills/auto-tmux/scripts/swarm-blockers.sh --dir /tmp/ai_swarm --out /tmp/auto-tmux-incident-blockers.md
```

## 远程采集失败

1. 先 dry-run 确认 SSH 命令形态：

```bash
skills/auto-tmux/scripts/remote-readonly.sh --host user@example.com --session ai-hub --dry-run
```

2. 确认远端是否安装 tmux、session 是否存在。
3. 不把 `remote-readonly.sh` 改造成远程写操作入口。
4. 失败仍需记录 host、session、错误信息和下一步验证路径。

## 敏感信息泄露风险

1. 停止继续分享原始 pane 输出。
2. 使用脱敏后的 `snapshot`、`remote-readonly.sh` 或 `record-summary.sh` 重新生成证据。
3. 检查附件目录，不提交 `/tmp/auto-tmux-*` 原始证据。
4. 如果 token 已泄露，按项目安全流程轮换凭证。

## 复盘模板

```text
incident:
  time:
  operator:
  target_expected:
  target_actual:
  command_or_payload:
  impact:
  evidence:
  mitigation:
  prevention:
```
