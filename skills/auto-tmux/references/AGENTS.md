# skills/auto-tmux/references Agent 指南

本目录保存 auto-tmux 的参考资料、示例和排障说明。

## 规则

- 参考资料只能引用仓库相对路径，不写个人机器绝对路径。
- 上游来源统一写为 `tools/external/.tmux`、`tools/external/tmux` 或 `tools/external/Skill_Seekers-development`。
- 示例命令必须优先使用可复制的占位符或 `git rev-parse --show-toplevel` 动态定位仓库根目录。
- 脚本类说明优先引用 `skills/auto-tmux/scripts/auto-tmux.sh`，再给原生命令兜底。
- SSH/远程 session 规则写入 `session-safety.md`；远程默认只读，不把只读采集扩展成控制入口。
- 机器可读输出字段约定写入 `jsonl-schema.md`；新增 JSONL/manifest 输出必须同步维护。
- report pack 审查路径写入 `report-pack-review.md`；新增报告文件时同步更新阅读顺序和通过标准。
- 角色化阅读路线写入 `reading-paths.md`；新增关键 reference 时同步判断是否进入某个角色路径。
- 操作事故处理流程写入 `incident-runbook.md`；新增控制类脚本时同步补事故处理路径。
- 不确定的 tmux 行为必须给出验证命令，不编造。
