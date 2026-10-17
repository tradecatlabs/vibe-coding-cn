# auto-tmux Script Cheatsheet

本文件按场景组织脚本入口，适合已经知道目标、只需要快速选命令的人。

## 观察与取证

```bash
.github/extensions/auto-tmux/auto-tmux.sh topology --session ai-hub
.github/extensions/auto-tmux/auto-tmux.sh inspect -t ai-hub:1.0 -n 80
.github/extensions/auto-tmux/auto-tmux.sh snapshot --session ai-hub --dir /tmp/auto-tmux-snapshot
.github/extensions/auto-tmux/remote-readonly.sh --host user@example.com --session ai-hub --out /tmp/auto-tmux-remote
```

## 控制与救援

```bash
.github/extensions/auto-tmux/safety-check.sh --text "make test"
.github/extensions/auto-tmux/auto-tmux.sh send -t ai-hub:1.0 --text "make test" --enter
.github/extensions/auto-tmux/auto-tmux.sh rescue -t ai-hub:1.0 --pattern "(y/n)" --reply y --dry-run
.github/extensions/auto-tmux/swarm-dispatch.sh --role worker --target ai-hub:1.0 --task "run tests" --send --dry-run
```

## 状态与协作

```bash
.github/extensions/auto-tmux/swarm-state.sh init --dir /tmp/ai_swarm
.github/extensions/auto-tmux/swarm-state.sh task-ready --dir /tmp/ai_swarm
.github/extensions/auto-tmux/swarm-assign.sh --swarm-dir /tmp/ai_swarm --session ai-hub --out /tmp/ai-swarm-assign.md
.github/extensions/auto-tmux/swarm-health.sh --session ai-hub --swarm-dir /tmp/ai_swarm --out /tmp/auto-tmux-health
```

## 报告与交付

```bash
.github/extensions/auto-tmux/swarm-board.sh --dir /tmp/ai_swarm --out /tmp/ai-swarm-board.md
.github/extensions/auto-tmux/swarm-results.sh --dir /tmp/ai_swarm --out /tmp/ai-swarm-results.md --jsonl /tmp/ai-swarm-results.jsonl
.github/extensions/auto-tmux/swarm-report-pack.sh --dir /tmp/ai_swarm --session ai-hub --out /tmp/ai-swarm-report-pack --tar
.github/extensions/auto-tmux/verify-report-pack.sh --pack /tmp/ai-swarm-report-pack
```

## 审计与事故

```bash
.github/extensions/auto-tmux/check-jsonl.sh /tmp/ai-swarm-results.jsonl --require-key type --require-key id --require-key status
.github/extensions/auto-tmux/review-checklist.sh --pack /tmp/ai-swarm-report-pack --strict
.github/extensions/auto-tmux/incident-report.sh --type mis-send --out /tmp/auto-tmux-incident.md
```

## 技能门禁

```bash
.github/extensions/auto-tmux/validate-auto-tmux.sh
.github/extensions/validate-skill.sh .github/skills/auto-tmux --strict
make test
```
