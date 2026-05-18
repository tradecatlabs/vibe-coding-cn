# auto-tmux

`auto-tmux` 是 tmux 自动化操控技能，用于读取 pane 输出、发送按键、批量巡检、救援卡住的终端，以及组织多 AI 终端协作。

## 入口

- [SKILL.md](./SKILL.md) - 技能触发条件、命令片段、规则和质量门禁。
- [scripts/](./scripts/) - 安全封装的 tmux 自动化脚本。
- [references/](./references/) - tmux / oh-my-tmux 参考、示例和故障排查。
- [assets/](./assets/) - 指向仓库外部 submodule 的只读软链接入口。

## 资产来源

| 入口 | 指向 | 用途 |
|:---|:---|:---|
| `assets/oh-my-tmux` | `tools/external/.tmux` | gpakosz/oh-my-tmux 配置参考 |
| `assets/tmux-src` | `tools/external/tmux` | tmux 上游源码参考 |

## 快速验证

```bash
bash -n skills/auto-tmux/scripts/auto-tmux.sh
skills/auto-tmux/scripts/auto-tmux.sh help
skills/auto-skill/scripts/validate-skill.sh skills/auto-tmux --strict
```

## 使用边界

- 优先使用 `scripts/auto-tmux.sh`，需要低层调试时再直接使用 tmux 原生命令。
- 发送按键前必须先 `capture-pane` 复核目标上下文；脚本会默认打印最近上下文。
- 批量操作前必须先列出 session/window/pane 白名单。
- 不在未知 pane 中发送破坏性命令。
- 不在本目录复制或修改上游 tmux / oh-my-tmux 源码。
