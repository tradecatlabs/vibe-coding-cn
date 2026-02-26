# 🔌 assets/repo/：外部集成与第三方工具

`assets/repo/` 用来收纳第三方工具、外部依赖与集成模块（含 Git submodule）。核心原则是：

- **尽量原样保留**：避免“魔改后不可升级”
- **隔离依赖与风险**：外部工具的依赖不要污染主仓库
- **可追溯**：来源、许可证、用法要写清楚

## 目录结构

```
assets/repo/
├── AGENTS.md                    # 本目录的 Agent 行为准则
├── README.md                    # 本文件（外部工具索引）
├── .tmux/                       # submodule：oh-my-tmux 配置
├── tmux/                        # submodule：tmux 源码
├── claude-official-skills/      # submodule：Claude 官方 skills 仓库（Anthropic）
├── prompts-library/             # Excel ↔ Markdown 转换工具
├── chat-vault/                  # AI 聊天记录保存工具
├── Skill_Seekers-development/   # Skills 制作器
├── html-tools-main/             # HTML 工具集
├── my-nvim/                     # Neovim 配置（含 nvim-config/）
├── MCPlayerTransfer/            # MC 玩家迁移工具
├── XHS-image-to-PDF-conversion/ # 图片合并 PDF 工具
└── backups/                     # 历史备份脚本快照
```

## 工具清单（入口与文档）

- `chat-vault/`：AI 聊天记录保存工具（详见 `chat-vault/README.md`）
- `prompts-library/`：提示词 Excel ↔ Markdown 批量互转与索引生成（详见 `prompts-library/README.md`）
- `Skill_Seekers-development/`：Skills 抓取/制作器（详见 `Skill_Seekers-development/README.md`）
- `html-tools-main/`：HTML 工具集（详见 `html-tools-main/README.md`）
- `my-nvim/`：个人 Neovim 配置（详见 `my-nvim/README.md`）
- `MCPlayerTransfer/`：MC 玩家迁移工具（详见 `MCPlayerTransfer/README.md`）
- `XHS-image-to-PDF-conversion/`：图片合并 PDF（详见 `XHS-image-to-PDF-conversion/README.md`）
- `.tmux/`、`tmux/`、`claude-official-skills/`：以 submodule 形式引入的上游仓库

> 📝 系统提示词已迁移到云端表格，入口见 [`prompts/README.md`](../../prompts/README.md)。

## 新增外部工具（最小清单）

1. 创建目录：`assets/repo/<tool-name>/`
2. 必备文件：`README.md`（用途/入口/依赖/输入输出）、许可证与来源说明（如 `LICENSE` / `SOURCE.md`）
3. 依赖约束：尽量使用工具自带的虚拟环境/容器化方式，不影响仓库其他部分
4. 文档同步：在本 README 增加一行工具说明，保证可发现性
