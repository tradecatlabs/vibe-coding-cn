# auto-tmux Reference Index

## Quick Links

- `getting_started.md`：术语、最小安装、前缀说明
- `api.md`：tmux/oh-my-tmux 常用命令、同步广播、安全写法
- `automation.md`：`scripts/auto-tmux.sh` 子命令、安全模型与 AI 蜂群协作流程
- `swarm-state.md`：蜂群状态、任务、锁和报告协议
- `prompt-templates.md`：commander/worker/reviewer 提示词模板和下发方式
- `ai-swarm-collaboration.md`：tmux 蜂群协作完整说明、架构模式、协议、案例和风险限制
- `examples.md`：蜂群巡检脚本、自动救援脚本、Skill Seeker 抓取示例
- `troubleshooting.md`：常见报错与修复路径

## Notes

- 长文档、脚本细节放这里，`SKILL.md` 只保留可立即执行的片段。
- 脚本入口统一为 `skills/auto-tmux/scripts/auto-tmux.sh`，原生命令作为兜底参考。
- 配置来源：仓库内 `tools/external/.tmux`（gpakosz/oh-my-tmux）。
- 大规模文档抓取/刷新可用 `tools/external/Skill_Seekers-development`，示例见 `examples.md`。
