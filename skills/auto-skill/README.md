# auto-skill

`auto-skill` 是本仓库保留的 Skills 元技能，用于生成、升级、重构和校验 Claude/Codex 风格的 Skill。

## 入口

- `SKILL.md`：技能说明与执行规则。
- `AGENTS.md`：本目录维护规则。
- `references/`：技能设计、校验和迁移参考资料。
- `scripts/`：技能校验与辅助脚本。
- `assets/`：技能内部可复用资产。

## 使用

修改本技能后，至少运行：

```bash
skills/auto-skill/scripts/validate-skill.sh skills/auto-skill --strict
make test
```
