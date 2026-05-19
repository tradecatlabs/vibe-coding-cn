# auto-tmux Reading Paths

本文件按角色给出最短阅读路线，避免所有人从头读完整 references。

## Commander

目标：分配任务、巡检状态、回收证据、决定是否交接。

阅读顺序：

1. `getting_started.md`
2. `swarm-state.md`
3. `automation.md`
4. `report-pack-review.md`
5. `troubleshooting.md`

关键命令：

```bash
skills/auto-tmux/scripts/swarm-state.sh task-ready --dir /tmp/ai_swarm
skills/auto-tmux/scripts/swarm-report-pack.sh --dir /tmp/ai_swarm --session ai-hub --out /tmp/ai-swarm-report-pack --tar
skills/auto-tmux/scripts/verify-report-pack.sh --pack /tmp/ai-swarm-report-pack
```

## Worker

目标：领取单个任务、执行、写回结果，不越界改动。

阅读顺序：

1. `prompt-templates.md`
2. `swarm-state.md`
3. `safety-policy.md`
4. `session-safety.md`

关键命令：

```bash
skills/auto-tmux/scripts/swarm-state.sh task-next --owner ai-hub:1.0 --dir /tmp/ai_swarm
skills/auto-tmux/scripts/swarm-state.sh task-done --id task-001 --owner ai-hub:1.0 --result "make test passed" --dir /tmp/ai_swarm
```

## Reviewer

目标：只读审查交付包，判断是否可合并、可交接、可复现。

阅读顺序：

1. `report-pack-review.md`
2. `jsonl-schema.md`
3. `automation.md`
4. `troubleshooting.md`

关键命令：

```bash
skills/auto-tmux/scripts/verify-report-pack.sh --pack /tmp/ai-swarm-report-pack
skills/auto-tmux/scripts/check-jsonl.sh /tmp/ai-swarm-report-pack/results.jsonl --require-key type --require-key id --require-key status
```

## Operator

目标：操作 tmux、远程采集、救援卡住的 pane，并控制误操作风险。

阅读顺序：

1. `api.md`
2. `automation.md`
3. `session-safety.md`
4. `safety-policy.md`
5. `troubleshooting.md`

关键命令：

```bash
skills/auto-tmux/scripts/auto-tmux.sh topology --session ai-hub
skills/auto-tmux/scripts/auto-tmux.sh inspect -t ai-hub:1.0 -n 80
skills/auto-tmux/scripts/remote-readonly.sh --host user@example.com --session ai-hub --out /tmp/auto-tmux-remote --dry-run
```
