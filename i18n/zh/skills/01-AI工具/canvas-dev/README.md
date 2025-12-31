# Canvas-Dev Skill

Canvas白板驱动开发技能，用于 AI 辅助架构设计与代码生成。

## 概述

此技能实现「图形是第一公民，代码是白板的序列化形式」的开发范式。

## 核心能力

1. **架构分析** - 从代码自动生成 Obsidian Canvas 白板
2. **白板驱动编码** - 根据白板生成/修改代码
3. **一致性检查** - 校验白板与代码同步状态

## 文件结构

```
canvas-dev/
├── SKILL.md              # 技能入口（触发条件、模式、示例）
├── references/
│   ├── index.md          # 导航索引
│   ├── canvas-json-spec.md   # Canvas JSON 规范
│   ├── workflow-guide.md     # 工作流指南
│   └── prompts.md            # 提示词集合
├── scripts/              # 自动化脚本（预留）
└── assets/               # 模板资源（预留）
```

## 快速开始

1. 阅读 `SKILL.md` 了解触发条件和使用模式
2. 参考 `references/workflow-guide.md` 了解完整工作流
3. 使用 `references/prompts.md` 中的提示词

## 相关资源

- [Canvas白板驱动开发详解](../../documents/02-方法论/图形化AI协作-Canvas白板驱动开发.md)
- [Canvas开发工作流](../../workflow/canvas-dev/)
- [元技能: claude-skills](../00-元技能/claude-skills/SKILL.md)
