# tools/external/ 目录 Agent 指南

本目录用于收纳 **外部工具/第三方项目**（含 Git submodule），保持“主仓库资产”和“外部依赖”边界清晰、可审计、可更新。

## 目录结构（约定）

```text
tools/external/
├── AGENTS.md                         # 本文件（目录级行为准则）
├── README.md                         # 外部工具索引
├── .tmux/                            # submodule：oh-my-tmux 配置
├── tmux/                             # submodule：tmux 源码
├── claude-official-skills/           # submodule：Claude 官方 skills 仓库
├── Skill_Seekers-development/        # submodule：Skill Seekers 工具来源
├── html-tools-main/                  # 普通目录：HTML 工具集
├── my-nvim/                          # 普通目录：Neovim 配置
├── MCPlayerTransfer/                 # 普通目录：MC 玩家迁移工具
└── XHS-image-to-PDF-conversion/      # 普通目录：图片合并 PDF 工具
```

## 当前软链接显示

```text
skills/claude-official-skills -> ../tools/external/claude-official-skills
skills/tmux-autopilot/assets/oh-my-tmux -> ../../../tools/external/.tmux
skills/tmux-autopilot/assets/tmux-src -> ../../../tools/external/tmux
skills/auto-skill/scripts/Skill_Seekers-development -> ../../../tools/external/Skill_Seekers-development
skills/auto-skill/scripts/skill-seekers-configs -> Skill_Seekers-development/configs
skills/auto-skill/scripts/skill-seekers-src -> Skill_Seekers-development/src
```

## 操作规范

### 允许

- 新增外部依赖（优先 Git submodule，确保可复现）
- 更新 submodule 指针（明确记录上游来源与用途）
- 用相对软链接把 `tools/external/` 下的事实来源暴露到其它目录，软链接目标必须仍在仓库内
- 为已复制进主仓库的外部源码建立清退计划：上游 URL、保留理由、迁移方式、验证命令

### 禁止 / 不推荐

- 直接复制粘贴大型第三方仓库内容到主仓库（优先 submodule）
- 将 submodule 替换为本地绝对路径软链接（会导致他人环境不可用）
- 提交第三方仓库的构建产物、生成物、运行时二进制或缓存目录
- 在主仓库直接魔改第三方源码快照；需要改造时先 fork，再以 submodule 指向 fork

## 仓库表达决策

1. **完整外部仓库**：优先使用 `git submodule`，主仓库只记录 commit 指针。
2. **同仓多入口展示**：使用相对软链接，例如 `skills/<name> -> ../tools/external/<name>`。
3. **项目内小工具**：只有在无上游、体量小、与本项目强耦合时才直接追踪源码。
4. **生成输出**：默认不跟踪；若必须保留样例，只提交最小样例和生成说明。
5. **历史备份**：`scripts/backups/` 按项目资产处理，不套用外部仓库清退规则。
