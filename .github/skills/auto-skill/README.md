# auto-skill

`auto-skill` 是本仓库保留的 Skills 元技能，用于生成、升级、重构和校验 Claude/Codex 风格的 Skill。

## 入口

- `SKILL.md`：技能说明与执行规则。
- `AGENTS.md`：本目录维护规则。
- `references/`：技能设计、校验和迁移参考资料。
- `../../extensions/`：原技能校验、生成及Skill Seekers适配脚本的单一实现；本Skill不再保留旧scripts目录。
- `assets/`：技能内部可复用资产。

## 使用

修改本技能后先运行相关校验；完整`make test`仅在任务最终版本执行：

```bash
.github/extensions/validate-skill.sh .github/skills/auto-skill --strict
make test
```
