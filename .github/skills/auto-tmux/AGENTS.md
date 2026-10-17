# .github/skills/auto-tmux

本目录是 tmux 自动化操控技能：面向 AI 终端巡检、按键注入、蜂群协作与 oh-my-tmux 配置复用。

## 目录结构

```text
.github/skills/auto-tmux/
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
│   ├── verify-report-pack.sh
│   ├── incident-report.sh
│   ├── audit-package.sh
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
    ├── report-pack-review.md
    ├── reading-paths.md
    ├── incident-runbook.md
    ├── script-cheatsheet.md
    ├── swarm-state.md
    ├── prompt-templates.md
    ├── codex-pilot-mode.md
    ├── ai-swarm-collaboration.md
    ├── iteration-roadmap.md
    ├── iteration-closeout.md
    ├── examples.md
    └── troubleshooting.md
```

## 职责边界

- `assets/oh-my-tmux` 只暴露 gpakosz/oh-my-tmux submodule，不在技能目录内复制配置源码。
- `assets/tmux-src` 只暴露 tmux/tmux submodule，供需要查看源码或上游文档时定位。
- `.github/extensions/auto-tmux/auto-tmux.sh` 是技能执行层，封装 topology/capture/send/scan/rescue/record/snapshot/hub/wait。
- `.github/extensions/auto-tmux/swarm-state.sh` 是蜂群协作状态层，管理任务、锁、状态日志和结果报告。
- `.github/extensions/auto-tmux/swarm-brief.sh` 是只读交接层，汇总 doctor/topology/scan/report 形成上下文快照。
- `.github/extensions/auto-tmux/swarm-watch.sh` 是有限轮次巡检层，按间隔采集 pane 输出与 swarm report。
- `.github/extensions/auto-tmux/swarm-archive.sh` 是归档层，打包 brief、snapshot 和 swarm state 供复盘交接。
- `.github/extensions/auto-tmux/swarm-board.sh` 是看板层，将任务、依赖、锁和状态日志渲染为 Markdown。
- `.github/extensions/auto-tmux/swarm-deps-graph.sh` 是依赖可视化层，将 `deps.tsv` 渲染为 Mermaid 图。
- `.github/extensions/auto-tmux/swarm-export.sh` 是机器可读导出层，将任务、依赖和锁导出为 JSONL。
- `.github/extensions/auto-tmux/swarm-timeline.sh` 是状态时间线层，将 `status.log` 渲染为 Markdown。
- `.github/extensions/auto-tmux/swarm-blockers.sh` 是阻塞报告层，聚合 BLOCKED/FAIL、锁和异常状态。
- `.github/extensions/auto-tmux/swarm-results.sh` 是结果收敛层，汇总 DONE/FAIL/BLOCKED worker 结果。
- `.github/extensions/auto-tmux/swarm-report-pack.sh` 是报告包层，聚合多个只读报告与 JSONL 导出。
- `.github/extensions/auto-tmux/swarm-assign.sh` 是分配建议层，将 ready task 轮询映射到 worker pane。
- `.github/extensions/auto-tmux/swarm-health.sh` 是健康检查层，汇总 tmux 和 swarm state 的只读报告包。
- `.github/extensions/auto-tmux/remote-readonly.sh` 是远端只读层，通过 SSH 采集 tmux 拓扑和输出证据。
- `.github/extensions/auto-tmux/record-summary.sh` 是复盘摘要层，将 pane 录制日志整理为 Markdown。
- `.github/extensions/auto-tmux/check-jsonl.sh` 是轻量 JSONL 字段门禁层，不替代完整 JSON parser。
- `.github/extensions/auto-tmux/review-checklist.sh` 是报告包审计层，为 reviewer 生成固定检查清单。
- `.github/extensions/auto-tmux/verify-report-pack.sh` 是报告包统一验证层，组合 manifest、JSONL 和审计清单门禁。
- `.github/extensions/auto-tmux/incident-report.sh` 是事故复盘层，生成误发送、误广播和敏感信息风险模板。
- `.github/extensions/auto-tmux/completion.bash` 是本地补全层，补全 `auto-tmux.sh` 与 `swarm-state.sh`。
- `.github/extensions/auto-tmux/safety-check.sh` 是安全预检层，检查待发送 payload 的危险命令、敏感信息和大小。
- `.github/extensions/auto-tmux/render-swarm-prompt.sh` 是提示词渲染层，生成 commander/worker/reviewer/codex-worker 协议文本。
- `.github/extensions/auto-tmux/swarm-dispatch.sh` 是提示词下发层，默认写文件，显式 `--send` 后才发送到 pane；支持 Codex Pilot Mode 的单 worker 下发。
- `references/codex-pilot-mode.md` 是显式激活协议，定义主 Codex 控制一个人类可旁观、持久化交互式 worker Codex pane 的提示词、边界和验收。
- `.github/extensions/auto-tmux/validate-auto-tmux.sh` 是技能专属质量门禁，覆盖脚本、文档索引和 smoke test。
- 技能文档可以引用软链接入口；更新上游内容必须通过 `.github/extensions/` 下的 submodule 指针完成。
- 不在本目录直接修改 submodule 内容；如需改造，先 fork 上游并更新 submodule 来源。
- SSH/远程 session 的默认边界写在 `references/session-safety.md`；不得把 `remote-readonly.sh` 扩展成远程写操作入口。

## 依赖关系

- 上游来源：`.github/extensions/oh-my-tmux` 与 `.github/extensions/tmux`。
- 下游使用：`SKILL.md` 和 `references/` 中的命令示例。
- 验证入口：`.github/extensions/validate-skill.sh .github/skills/auto-tmux --strict`。
- 脚本验证：`.github/extensions/auto-tmux/validate-auto-tmux.sh`、`bash -n .github/extensions/auto-tmux/auto-tmux.sh`、`bash -n .github/extensions/auto-tmux/swarm-state.sh`、`bash -n .github/extensions/auto-tmux/swarm-brief.sh`、`bash -n .github/extensions/auto-tmux/swarm-watch.sh`、`bash -n .github/extensions/auto-tmux/swarm-archive.sh`、`bash -n .github/extensions/auto-tmux/swarm-board.sh`、`bash -n .github/extensions/auto-tmux/swarm-deps-graph.sh`、`bash -n .github/extensions/auto-tmux/swarm-export.sh`、`bash -n .github/extensions/auto-tmux/swarm-timeline.sh`、`bash -n .github/extensions/auto-tmux/swarm-blockers.sh`、`bash -n .github/extensions/auto-tmux/swarm-results.sh`、`bash -n .github/extensions/auto-tmux/swarm-report-pack.sh`、`bash -n .github/extensions/auto-tmux/swarm-assign.sh`、`bash -n .github/extensions/auto-tmux/swarm-health.sh`、`bash -n .github/extensions/auto-tmux/remote-readonly.sh`、`bash -n .github/extensions/auto-tmux/record-summary.sh`、`bash -n .github/extensions/auto-tmux/check-jsonl.sh`、`bash -n .github/extensions/auto-tmux/review-checklist.sh`、`bash -n .github/extensions/auto-tmux/verify-report-pack.sh`、`bash -n .github/extensions/auto-tmux/completion.bash`、`bash -n .github/extensions/auto-tmux/safety-check.sh`、`bash -n .github/extensions/auto-tmux/render-swarm-prompt.sh`、`bash -n .github/extensions/auto-tmux/swarm-dispatch.sh`、`.github/extensions/auto-tmux/auto-tmux-smoke-test.sh`。
