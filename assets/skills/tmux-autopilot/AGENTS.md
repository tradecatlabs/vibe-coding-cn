# assets/skills/tmux-autopilot

本目录是 tmux 自动化操控技能：面向 AI 终端巡检、按键注入、蜂群协作与 oh-my-tmux 配置复用。

## 目录结构

```text
assets/skills/tmux-autopilot/
├── AGENTS.md                 # 本文件：目录职责、结构与边界
├── SKILL.md                  # 技能入口：触发条件、命令片段、规则与质量门
├── assets/                   # 外部 tmux 相关仓库的只读软链接入口
│   ├── oh-my-tmux -> ../../../repos/.tmux
│   └── tmux-src -> ../../../repos/tmux
└── references/               # 长文档、示例与故障排查
    ├── index.md
    ├── getting_started.md
    ├── api.md
    ├── examples.md
    └── troubleshooting.md
```

## 职责边界

- `assets/oh-my-tmux` 只暴露 gpakosz/oh-my-tmux submodule，不在技能目录内复制配置源码。
- `assets/tmux-src` 只暴露 tmux/tmux submodule，供需要查看源码或上游文档时定位。
- 技能文档可以引用软链接入口；更新上游内容必须通过 `assets/repos/` 下的 submodule 指针完成。
- 不在本目录直接修改 submodule 内容；如需改造，先 fork 上游并更新 submodule 来源。

## 依赖关系

- 上游来源：`assets/repos/.tmux` 与 `assets/repos/tmux`。
- 下游使用：`SKILL.md` 和 `references/` 中的命令示例。
- 验证入口：`assets/skills/auto-skill/scripts/validate-skill.sh assets/skills/tmux-autopilot --strict`。
