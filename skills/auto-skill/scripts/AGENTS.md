# skills/auto-skill/scripts/ Agent 指南

本目录维护 `auto-skill` 的执行脚本和外部工具软链接入口。

## 约束

- 不把外部仓库源码复制进脚本目录；需要暴露时使用软链接或 submodule。
- 不在脚本中硬编码本地绝对路径、Token 或账号信息。
- 修改 shell 脚本后检查可执行位和基本语法。
- `Skill_Seekers-development` 相关路径视为外部工具入口，主仓门禁不深入检查其内部链接。
