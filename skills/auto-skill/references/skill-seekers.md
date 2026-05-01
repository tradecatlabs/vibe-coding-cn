# Skill Seekers（链接工具）使用说明

本目录通过相对软链接暴露 `tools/external/Skill_Seekers-development` submodule，用于把「文档 / GitHub 仓库 / PDF」快速转成一个可落地的 Skill 初稿。`tools/external/` 是源码单一来源，`auto-skill/scripts/` 只保留工具入口。

## 目录约定

- 工具源码入口：`skills/auto-skill/scripts/Skill_Seekers-development -> ../../../tools/external/Skill_Seekers-development`
- 运行入口：`skills/auto-skill/scripts/skill-seekers.sh`
- 依赖初始化：`skills/auto-skill/scripts/skill-seekers-bootstrap.sh`
- 导入到本仓库：`skills/auto-skill/scripts/skill-seekers-import.sh`
- 更新源码：直接更新 `tools/external/Skill_Seekers-development` submodule 指针；`skill-seekers-update.sh` 仅保留为受保护的旧入口。

## 推荐工作流（强约束）

1. 用 Skill Seekers 生成初稿到 `output/<name>/`
2. 导入到 `skills/<name>/`
3. 用 `validate-skill.sh --strict` 做质量闸门
4. 回到 `auto-skill` 的规范对 `SKILL.md` 做“可激活性”与“边界”修订

## 最小可执行示例

```bash
# 1) 初始化（只需一次）
./skills/auto-skill/scripts/skill-seekers-bootstrap.sh

# 2) 生成（示例：抓 docs 配置）
./skills/auto-skill/scripts/skill-seekers.sh -- scrape --config ./skills/auto-skill/scripts/Skill_Seekers-development/configs/react.json

# 3) 导入到 skills/
./skills/auto-skill/scripts/skill-seekers-import.sh react

# 4) 严格校验
./skills/auto-skill/scripts/validate-skill.sh skills/react --strict
```

## 设计原则

- `skills/auto-skill/` 负责：规范、模板、闸门、可激活性；不直接承载领域知识。
- Skill Seekers 负责：抓取与初稿生成；最终交付仍以本仓库的 `validate-skill.sh --strict` 为准。
