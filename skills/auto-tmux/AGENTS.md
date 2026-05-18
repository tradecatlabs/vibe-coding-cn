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
- `scripts/render-swarm-prompt.sh` 是提示词渲染层，生成 commander/worker/reviewer 协议文本。
- `scripts/swarm-dispatch.sh` 是提示词下发层，默认写文件，显式 `--send` 后才发送到 pane。
- `scripts/validate-auto-tmux.sh` 是技能专属质量门禁，覆盖脚本、文档索引和 smoke test。
- 技能文档可以引用软链接入口；更新上游内容必须通过 `tools/external/` 下的 submodule 指针完成。
- 不在本目录直接修改 submodule 内容；如需改造，先 fork 上游并更新 submodule 来源。

## 依赖关系

- 上游来源：`tools/external/.tmux` 与 `tools/external/tmux`。
- 下游使用：`SKILL.md` 和 `references/` 中的命令示例。
- 验证入口：`skills/auto-skill/scripts/validate-skill.sh skills/auto-tmux --strict`。
- 脚本验证：`skills/auto-tmux/scripts/validate-auto-tmux.sh`、`bash -n skills/auto-tmux/scripts/auto-tmux.sh`、`bash -n skills/auto-tmux/scripts/swarm-state.sh`、`bash -n skills/auto-tmux/scripts/swarm-brief.sh`、`bash -n skills/auto-tmux/scripts/render-swarm-prompt.sh`、`bash -n skills/auto-tmux/scripts/swarm-dispatch.sh`、`skills/auto-tmux/scripts/auto-tmux-smoke-test.sh`。
