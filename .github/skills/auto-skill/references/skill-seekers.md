# Skill Seekers（链接工具）使用说明

原Skill Seekers源码只保留在`.github/extensions/Skill_Seekers-development`固定Gitlink；本Skill描述其文档/GitHub/PDF转Skill的现有工作流，不再保留旧scripts别名。下文命令从仓库根运行；抓取、依赖安装与生成仍须具体任务授权。

## 目录约定

- 唯一工具源码：`.github/extensions/Skill_Seekers-development`。
- 运行入口：`.github/extensions/skill-seekers.sh`
- 依赖初始化：`.github/extensions/skill-seekers-bootstrap.sh`
- 导入到本仓库：`.github/extensions/skill-seekers-import.sh`
- 更新源码：作为明确的Gitlink变更单独评审；`skill-seekers-update.sh`拒绝非预览覆盖，不因目标已是实际Git目录而解除保护。其`--dry-run`仍下载并解压临时归档，不是离线或零I/O。

## 推荐工作流（强约束）

1. 用 Skill Seekers 生成初稿到 `output/<name>/`
2. 导入到 `.github/skills/<name>/`
3. 用 `validate-skill.sh --strict` 做质量闸门
4. 回到 `auto-skill` 的规范对 `SKILL.md` 做“可激活性”与“边界”修订

## 最小可执行示例

```bash
# 1) 初始化（只需一次）
./.github/extensions/skill-seekers-bootstrap.sh

# 2) 生成（示例：抓 docs 配置）
./.github/extensions/skill-seekers.sh -- scrape --config ./.github/extensions/Skill_Seekers-development/configs/react.json

# 3) 导入到 .github/skills/
./.github/extensions/skill-seekers-import.sh react

# 4) 严格校验
./.github/extensions/validate-skill.sh .github/skills/react --strict
```

## 设计原则

- `.github/skills/auto-skill/` 负责：规范、模板、闸门、可激活性；不直接承载领域知识。
- Skill Seekers 负责：抓取与初稿生成；最终交付仍以本仓库的 `validate-skill.sh --strict` 为准。
