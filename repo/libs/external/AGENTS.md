# repo/libs/external/ 目录 Agent 指南

本目录用于收纳 **外部工具/第三方项目**（含 Git submodule），保持“主仓库资产”和“外部依赖”边界清晰、可审计、可更新。

## 目录结构（约定）

```text
repo/libs/external/
├── AGENTS.md                         # 本文件（目录级行为准则）
├── README.md                         # 外部工具索引
├── .tmux/                            # submodule：oh-my-tmux 配置
├── tmux/                             # submodule：tmux 源码
└── claude-official-skills/           # submodule：Claude 官方 skills 仓库（Anthropic）
```

## 操作规范

### 允许

- 新增外部依赖（优先 Git submodule，确保可复现）
- 更新 submodule 指针（明确记录上游来源与用途）

### 禁止 / 不推荐

- 直接复制粘贴大型第三方仓库内容到主仓库（优先 submodule）
- 将 submodule 替换为本地绝对路径软链接（会导致他人环境不可用）
