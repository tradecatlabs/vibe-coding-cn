# skills/auto-tmux

本目录是 tmux 自动化操控技能：面向 AI 终端巡检、按键注入、蜂群协作与 oh-my-tmux 配置复用。

## 目录结构

```text
skills/auto-tmux/
├── AGENTS.md                 # 本文件：目录职责、结构与边界
├── SKILL.md                  # 技能入口：触发条件、命令片段、规则与质量门
├── assets/                   # 外部 tmux 相关仓库的只读软链接入口
│   ├── oh-my-tmux -> ../../../tools/external/.tmux
│   └── tmux-src -> ../../../tools/external/tmux
├── scripts/                  # 安全封装的 tmux 自动化脚本
│   ├── auto-tmux.sh
│   ├── swarm-state.sh
│   ├── swarm-brief.sh
│   ├── swarm-watch.sh
│   ├── swarm-archive.sh
│   ├── swarm-board.sh
│   ├── swarm-deps-graph.sh
│   ├── swarm-export.sh
│   ├── swarm-timeline.sh
│   ├── swarm-blockers.sh
│   ├── swarm-results.sh
│   ├── swarm-report-pack.sh
│   ├── swarm-assign.sh
│   ├── swarm-health.sh
│   ├── remote-readonly.sh
│   ├── record-summary.sh
│   ├── check-jsonl.sh
│   ├── review-checklist.sh
│   ├── completion.bash
│   ├── safety-check.sh
│   ├── render-swarm-prompt.sh
│   ├── swarm-dispatch.sh
│   ├── auto-tmux-smoke-test.sh
│   ├── validate-auto-tmux.sh
│   ├── README.md
│   └── AGENTS.md
└── references/               # 长文档、示例与故障排查
    ├── index.md
    ├── getting_started.md
    ├── api.md
    ├── automation.md
    ├── safety-policy.md
    ├── session-safety.md
    ├── jsonl-schema.md
    ├── swarm-state.md
    ├── prompt-templates.md
    ├── ai-swarm-collaboration.md
    ├── examples.md
    └── troubleshooting.md
```

## 职责边界

- `assets/oh-my-tmux` 只暴露 gpakosz/oh-my-tmux submodule，不在技能目录内复制配置源码。
- `assets/tmux-src` 只暴露 tmux/tmux submodule，供需要查看源码或上游文档时定位。
- `scripts/auto-tmux.sh` 是技能执行层，封装 topology/capture/send/scan/rescue/record/snapshot/hub/wait。
- `scripts/swarm-state.sh` 是蜂群协作状态层，管理任务、锁、状态日志和结果报告。
- `scripts/swarm-brief.sh` 是只读交接层，汇总 doctor/topology/scan/report 形成上下文快照。
- `scripts/swarm-watch.sh` 是有限轮次巡检层，按间隔采集 pane 输出与 swarm report。
- `scripts/swarm-archive.sh` 是归档层，打包 brief、snapshot 和 swarm state 供复盘交接。
- `scripts/swarm-board.sh` 是看板层，将任务、依赖、锁和状态日志渲染为 Markdown。
- `scripts/swarm-deps-graph.sh` 是依赖可视化层，将 `deps.tsv` 渲染为 Mermaid 图。
- `scripts/swarm-export.sh` 是机器可读导出层，将任务、依赖和锁导出为 JSONL。
- `scripts/swarm-timeline.sh` 是状态时间线层，将 `status.log` 渲染为 Markdown。
- `scripts/swarm-blockers.sh` 是阻塞报告层，聚合 BLOCKED/FAIL、锁和异常状态。
- `scripts/swarm-results.sh` 是结果收敛层，汇总 DONE/FAIL/BLOCKED worker 结果。
- `scripts/swarm-report-pack.sh` 是报告包层，聚合多个只读报告与 JSONL 导出。
- `scripts/swarm-assign.sh` 是分配建议层，将 ready task 轮询映射到 worker pane。
- `scripts/swarm-health.sh` 是健康检查层，汇总 tmux 和 swarm state 的只读报告包。
- `scripts/remote-readonly.sh` 是远端只读层，通过 SSH 采集 tmux 拓扑和输出证据。
- `scripts/record-summary.sh` 是复盘摘要层，将 pane 录制日志整理为 Markdown。
- `scripts/check-jsonl.sh` 是轻量 JSONL 字段门禁层，不替代完整 JSON parser。
- `scripts/review-checklist.sh` 是报告包审计层，为 reviewer 生成固定检查清单。
- `scripts/completion.bash` 是本地补全层，补全 `auto-tmux.sh` 与 `swarm-state.sh`。
- `scripts/safety-check.sh` 是安全预检层，检查待发送 payload 的危险命令、敏感信息和大小。
- `scripts/render-swarm-prompt.sh` 是提示词渲染层，生成 commander/worker/reviewer 协议文本。
- `scripts/swarm-dispatch.sh` 是提示词下发层，默认写文件，显式 `--send` 后才发送到 pane。
- `scripts/validate-auto-tmux.sh` 是技能专属质量门禁，覆盖脚本、文档索引和 smoke test。
- 技能文档可以引用软链接入口；更新上游内容必须通过 `tools/external/` 下的 submodule 指针完成。
- 不在本目录直接修改 submodule 内容；如需改造，先 fork 上游并更新 submodule 来源。
- SSH/远程 session 的默认边界写在 `references/session-safety.md`；不得把 `remote-readonly.sh` 扩展成远程写操作入口。

## 依赖关系

- 上游来源：`tools/external/.tmux` 与 `tools/external/tmux`。
- 下游使用：`SKILL.md` 和 `references/` 中的命令示例。
- 验证入口：`skills/auto-skill/scripts/validate-skill.sh skills/auto-tmux --strict`。
- 脚本验证：`skills/auto-tmux/scripts/validate-auto-tmux.sh`、`bash -n skills/auto-tmux/scripts/auto-tmux.sh`、`bash -n skills/auto-tmux/scripts/swarm-state.sh`、`bash -n skills/auto-tmux/scripts/swarm-brief.sh`、`bash -n skills/auto-tmux/scripts/swarm-watch.sh`、`bash -n skills/auto-tmux/scripts/swarm-archive.sh`、`bash -n skills/auto-tmux/scripts/swarm-board.sh`、`bash -n skills/auto-tmux/scripts/swarm-deps-graph.sh`、`bash -n skills/auto-tmux/scripts/swarm-export.sh`、`bash -n skills/auto-tmux/scripts/swarm-timeline.sh`、`bash -n skills/auto-tmux/scripts/swarm-blockers.sh`、`bash -n skills/auto-tmux/scripts/swarm-results.sh`、`bash -n skills/auto-tmux/scripts/swarm-report-pack.sh`、`bash -n skills/auto-tmux/scripts/swarm-assign.sh`、`bash -n skills/auto-tmux/scripts/swarm-health.sh`、`bash -n skills/auto-tmux/scripts/remote-readonly.sh`、`bash -n skills/auto-tmux/scripts/record-summary.sh`、`bash -n skills/auto-tmux/scripts/check-jsonl.sh`、`bash -n skills/auto-tmux/scripts/review-checklist.sh`、`bash -n skills/auto-tmux/scripts/completion.bash`、`bash -n skills/auto-tmux/scripts/safety-check.sh`、`bash -n skills/auto-tmux/scripts/render-swarm-prompt.sh`、`bash -n skills/auto-tmux/scripts/swarm-dispatch.sh`、`skills/auto-tmux/scripts/auto-tmux-smoke-test.sh`。
