# skills/auto-tmux/references Agent 指南

本目录保存 auto-tmux 的参考资料、示例和排障说明。

## 规则

- 参考资料只能引用仓库相对路径，不写个人机器绝对路径。
- 上游来源统一写为 `tools/external/.tmux`、`tools/external/tmux` 或 `tools/external/Skill_Seekers-development`。
- 示例命令必须优先使用可复制的占位符或 `git rev-parse --show-toplevel` 动态定位仓库根目录。
- 脚本类说明优先引用 `skills/auto-tmux/scripts/auto-tmux.sh`，再给原生命令兜底。
- SSH/远程 session 规则写入 `session-safety.md`；远程默认只读，不把只读采集扩展成控制入口。
- 不确定的 tmux 行为必须给出验证命令，不编造。
