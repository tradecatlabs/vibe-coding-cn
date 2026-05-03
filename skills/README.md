# AI Skills 技能库

`skills/` 目录只保留当前仓库仍需要维护和展示的 Skill 入口。清理原则是：主仓库只维护元技能与必要入口，领域型/工具型大包优先移出主仓库，避免文档噪音、体积膨胀和重复维护。

## 当前保留

| 技能 | 说明 |
|:---|:---|
| [auto-skill](./auto-skill/SKILL.md) | 生成、重构与校验 Skills 的元技能 |
| [claude-official-skills](./claude-official-skills/) | Claude 官方 skills 仓库的软链接入口，事实来源在 `tools/external/claude-official-skills/` |

## 维护口径

- `auto-skill/` 是本仓库的 Skill 生产与升级入口，继续保留。
- `claude-official-skills/` 是外部官方仓库展示入口，通过 submodule 管理事实来源。
- 领域型/工具型 Skill 如交易、数据库、代理、Telegram、tmux、EPUB 等不在主仓库维护；如需引入，优先使用独立仓库、submodule 或重新生成的方式。

## 外部技能仓库

- 初始化/更新方式：`git submodule update --init --recursive`
- Skills 大全网站：`https://skills.sh/`

## Repo 软链接入口

- `skills/claude-official-skills/`：指向 `tools/external/claude-official-skills/`。
- `skills/auto-skill/scripts/Skill_Seekers-development`：指向 `tools/external/Skill_Seekers-development` submodule，作为 Skill Seekers 工具来源。

## 快速使用

```bash
# 查看元技能
cat skills/auto-skill/SKILL.md

# 初始化外部 skills 仓库
git submodule update --init --recursive
```

## 创建自定义 Skill

使用元技能生成：

1. 准备领域资料（文档、代码、规范）。
2. 将资料和 `auto-skill/SKILL.md` 一起提供给 AI。
3. AI 会生成针对该领域的专用 Skill。

## 相关资源

- [元技能文件](./auto-skill/SKILL.md) - 生成、重构与校验 Skills
- [提示词库](../prompts/) - 更细粒度的提示词集合
- [文档库](../docs/) - 方法论与开发经验
