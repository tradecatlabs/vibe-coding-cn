# auto-tmux Script Cheatsheet

本文件按场景组织脚本入口，适合已经知道目标、只需要快速选命令的人。

## 观察与取证

```bash
.github/skills/auto-tmux/scripts/auto-tmux.sh topology --session ai-hub
.github/skills/auto-tmux/scripts/auto-tmux.sh inspect -t ai-hub:1.0 -n 80
.github/skills/auto-tmux/scripts/auto-tmux.sh snapshot --session ai-hub --dir /tmp/auto-tmux-snapshot
.github/skills/auto-tmux/scripts/remote-readonly.sh --host user@example.com --session ai-hub --out /tmp/auto-tmux-remote
```

## 控制与救援

```bash
.github/skills/auto-tmux/scripts/safety-check.sh --text "make test"
.github/skills/auto-tmux/scripts/auto-tmux.sh send -t ai-hub:1.0 --text "make test" --enter
.github/skills/auto-tmux/scripts/auto-tmux.sh rescue -t ai-hub:1.0 --pattern "(y/n)" --reply y --dry-run
.github/skills/auto-tmux/scripts/swarm-dispatch.sh --role worker --target ai-hub:1.0 --task "run tests" --send --dry-run
```

## 状态与协作

```bash
.github/skills/auto-tmux/scripts/swarm-state.sh init --dir /tmp/ai_swarm
.github/skills/auto-tmux/scripts/swarm-state.sh task-ready --dir /tmp/ai_swarm
.github/skills/auto-tmux/scripts/swarm-assign.sh --swarm-dir /tmp/ai_swarm --session ai-hub --out /tmp/ai-swarm-assign.md
.github/skills/auto-tmux/scripts/swarm-health.sh --session ai-hub --swarm-dir /tmp/ai_swarm --out /tmp/auto-tmux-health
```

## 报告与交付

```bash
.github/skills/auto-tmux/scripts/swarm-board.sh --dir /tmp/ai_swarm --out /tmp/ai-swarm-board.md
.github/skills/auto-tmux/scripts/swarm-results.sh --dir /tmp/ai_swarm --out /tmp/ai-swarm-results.md --jsonl /tmp/ai-swarm-results.jsonl
.github/skills/auto-tmux/scripts/swarm-report-pack.sh --dir /tmp/ai_swarm --session ai-hub --out /tmp/ai-swarm-report-pack --tar
.github/skills/auto-tmux/scripts/verify-report-pack.sh --pack /tmp/ai-swarm-report-pack
```

## 审计与事故

```bash
.github/skills/auto-tmux/scripts/check-jsonl.sh /tmp/ai-swarm-results.jsonl --require-key type --require-key id --require-key status
.github/skills/auto-tmux/scripts/review-checklist.sh --pack /tmp/ai-swarm-report-pack --strict
.github/skills/auto-tmux/scripts/incident-report.sh --type mis-send --out /tmp/auto-tmux-incident.md
```

## 技能门禁

```bash
.github/skills/auto-tmux/scripts/validate-auto-tmux.sh
.github/skills/auto-skill/scripts/validate-skill.sh .github/skills/auto-tmux --strict
make test
```
