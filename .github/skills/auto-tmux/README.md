# auto-tmux

`auto-tmux` 是 tmux 自动化操控技能，用于读取 pane 输出、发送按键、批量巡检、救援卡住的终端，以及组织多 AI 终端协作。

## 入口

- [SKILL.md](SKILL.md) - 技能触发条件、命令片段、规则和质量门禁。
- [scripts/](../../extensions/auto-tmux) - 安全封装的 tmux 自动化脚本。
- [references/](references) - tmux / oh-my-tmux 参考、示例和故障排查。
- [assets/](assets) - 指向仓库外部 submodule 的只读软链接入口。

## 资产来源

| 入口 | 指向 | 用途 |
|:---|:---|:---|
| `assets/oh-my-tmux` | `.github/extensions/oh-my-tmux` | gpakosz/oh-my-tmux 配置参考 |
| `assets/tmux-src` | `.github/extensions/tmux` | tmux 上游源码参考 |

## 快速验证

```bash
bash -n .github/extensions/auto-tmux/auto-tmux.sh
bash -n .github/extensions/auto-tmux/swarm-state.sh
bash -n .github/extensions/auto-tmux/swarm-brief.sh
bash -n .github/extensions/auto-tmux/swarm-watch.sh
bash -n .github/extensions/auto-tmux/swarm-archive.sh
bash -n .github/extensions/auto-tmux/swarm-board.sh
bash -n .github/extensions/auto-tmux/swarm-deps-graph.sh
bash -n .github/extensions/auto-tmux/swarm-export.sh
bash -n .github/extensions/auto-tmux/swarm-timeline.sh
bash -n .github/extensions/auto-tmux/swarm-blockers.sh
bash -n .github/extensions/auto-tmux/swarm-results.sh
bash -n .github/extensions/auto-tmux/swarm-report-pack.sh
bash -n .github/extensions/auto-tmux/swarm-assign.sh
bash -n .github/extensions/auto-tmux/swarm-health.sh
bash -n .github/extensions/auto-tmux/remote-readonly.sh
bash -n .github/extensions/auto-tmux/record-summary.sh
bash -n .github/extensions/auto-tmux/check-jsonl.sh
bash -n .github/extensions/auto-tmux/review-checklist.sh
bash -n .github/extensions/auto-tmux/verify-report-pack.sh
bash -n .github/extensions/auto-tmux/completion.bash
bash -n .github/extensions/auto-tmux/safety-check.sh
bash -n .github/extensions/auto-tmux/render-swarm-prompt.sh
bash -n .github/extensions/auto-tmux/swarm-dispatch.sh
bash -n .github/extensions/auto-tmux/validate-auto-tmux.sh
.github/extensions/auto-tmux/auto-tmux.sh help
.github/extensions/auto-tmux/swarm-state.sh help
.github/extensions/auto-tmux/swarm-brief.sh --help
.github/extensions/auto-tmux/safety-check.sh --text "make test"
.github/extensions/auto-tmux/render-swarm-prompt.sh commander --session ai-hub --task "smoke"
.github/extensions/auto-tmux/auto-tmux-smoke-test.sh
.github/extensions/auto-tmux/validate-auto-tmux.sh
.github/extensions/validate-skill.sh .github/skills/auto-tmux --strict
```

## 使用边界

- 优先使用 `.github/extensions/auto-tmux/auto-tmux.sh`，需要低层调试时再直接使用 tmux 原生命令。
- 发送按键前必须先 `capture-pane` 复核目标上下文；脚本会默认打印最近上下文。
- 发送长文本、粘贴文件或下发 prompt 前先运行 `.github/extensions/auto-tmux/safety-check.sh`。
- SSH/远程场景默认只读，先用 `.github/extensions/auto-tmux/remote-readonly.sh` 采集证据，再按 `references/session-safety.md` 判断是否需要人工确认升级。
- 批量操作前必须先列出 session/window/pane 白名单。
- 多 worker 并发前用 `swarm-state.sh` 管理任务、锁和状态，避免重复修改同一资源。
- 不在未知 pane 中发送破坏性命令。
- 不在本目录复制或修改上游 tmux / oh-my-tmux 源码。
