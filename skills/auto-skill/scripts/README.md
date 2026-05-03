# skills/auto-skill/scripts

`auto-skill` 的辅助脚本目录。

## 当前内容

- `create-skill.sh` - 创建 skill 骨架。
- `validate-skill.sh` - 校验 skill 结构。
- `skill-seekers-*.sh` - Skill Seekers 相关适配脚本。
- `Skill_Seekers-development`、`skill-seekers-src`、`skill-seekers-configs` - 指向外部仓库内容的软链接入口。

## 维护规则

- 软链接入口属于外部工具暴露面，不直接修改其目标内容。
- 脚本应保持可重复执行，并在失败时输出明确原因。
- 修改脚本后运行对应 `--help`、dry-run 或最小校验命令。
