# 🔌 assets/repos/：外部集成与第三方工具

`assets/repos/` 用来收纳第三方工具、外部依赖与集成模块（含 Git submodule）。核心原则是：

- **尽量原样保留**：避免“魔改后不可升级”
- **隔离依赖与风险**：外部工具的依赖不要污染主仓库
- **可追溯**：来源、许可证、用法要写清楚

## 目录结构

```
assets/repos/
├── AGENTS.md                    # 本目录的 Agent 行为准则
├── README.md                    # 本文件（外部工具索引）
├── .tmux/                       # submodule：oh-my-tmux 配置
├── tmux/                        # submodule：tmux 源码
├── claude-official-skills/      # submodule：Claude 官方 skills 仓库（Anthropic）
├── prompts-library/             # Excel ↔ Markdown 转换工具
├── chat-vault/                  # AI 聊天记录保存工具
├── Skill_Seekers-development/   # submodule：Skills 制作器
├── html-tools-main/             # HTML 工具集
├── my-nvim/                     # Neovim 配置（含 nvim-config/）
├── MCPlayerTransfer/            # MC 玩家迁移工具
├── XHS-image-to-PDF-conversion/ # 图片合并 PDF 工具
└── backups/                     # 历史备份脚本快照
```

## 工具清单（入口与文档）

- `chat-vault/`：AI 聊天记录保存工具（详见 `chat-vault/README.md`）
- `prompts-library/`：提示词 Excel ↔ Markdown 批量互转与索引生成（详见 `prompts-library/README.md`）
- `Skill_Seekers-development/`：以 submodule 引入的 Skills 抓取/制作器（详见 `Skill_Seekers-development/README.md`）
- `html-tools-main/`：HTML 工具集（详见 `html-tools-main/README.md`）
- `my-nvim/`：个人 Neovim 配置（详见 `my-nvim/README.md`）
- `MCPlayerTransfer/`：MC 玩家迁移工具（详见 `MCPlayerTransfer/README.md`）
- `XHS-image-to-PDF-conversion/`：图片合并 PDF（详见 `XHS-image-to-PDF-conversion/README.md`）
- `.tmux/`、`tmux/`、`claude-official-skills/`、`Skill_Seekers-development/`：以 submodule 形式引入的上游仓库

> 📝 系统提示词已迁移到云端表格，入口见 [`assets/prompt/README.md`](../prompt/README.md)。

## 当前表达状态（2026-04-29）

目标：`assets/repos/` 是外部工具与依赖的事实来源；需要在其它资产目录展示时，才用相对软链接指向这里。当前只对确有跨目录入口需求的仓库做软链接显示。

| 目录 | 当前表示 | 软链接显示 | 备注 |
|:---|:---|:---|:---|
| `.tmux/` | Git submodule | `assets/skills/tmux-autopilot/assets/oh-my-tmux` | oh-my-tmux 配置来源 |
| `tmux/` | Git submodule | `assets/skills/tmux-autopilot/assets/tmux-src` | tmux 上游源码入口 |
| `claude-official-skills/` | Git submodule | `assets/skills/claude-official-skills` | Claude 官方 skills 仓库 |
| `Skill_Seekers-development/` | Git submodule | `assets/skills/auto-skill/scripts/Skill_Seekers-development` | `auto-skill` 的 Skill Seekers 工具来源；`configs` 与 `src` 另有软链接入口 |
| `prompts-library/` | 普通目录 | 无 | 转换工具直接从 `assets/repos/` 使用，不做跨目录软链接显示 |
| `html-tools-main/` | 普通目录 | 无 | 工具目录保持 README 索引 |
| `XHS-image-to-PDF-conversion/` | 普通目录 | 无 | 工具目录保持 README 索引 |
| `chat-vault/` | 普通目录 | 无 | 工具目录保持 README 索引 |
| `MCPlayerTransfer/` | 普通目录 | 无 | 工具目录保持 README 索引 |
| `my-nvim/` | 普通目录 | 无 | Neovim 配置镜像，保持 README 索引 |
| `backups/` | 普通目录 | 无 | 本项目历史备份资产，继续保护 `gz/` 存档 |

## 表达规则

- 外部完整仓库：优先 `git submodule add <url> assets/repos/<name>`。
- 跨目录展示入口：使用相对软链接，例如 `assets/skills/<name> -> ../repos/<name>`。
- 不允许：软链接到本机绝对路径、复制大型上游源码、提交构建产物/生成物、提交二进制运行时。
- 需要本地改造第三方工具时：优先 fork 后以 submodule 指向 fork；不要在主仓库直接魔改一份不可升级的源码快照。

## 新增外部工具（最小清单）

1. 优先新增 submodule：`git submodule add <url> assets/repos/<tool-name>`。
2. 只在没有上游仓库、且体量小/与本项目强耦合时，才创建普通目录：`assets/repos/<tool-name>/`。
3. 必备文件：`README.md`（用途/入口/依赖/输入输出）、许可证与来源说明（如 `LICENSE` / `SOURCE.md`）。
4. 依赖约束：尽量使用工具自带的虚拟环境/容器化方式，不影响仓库其他部分。
5. 文档同步：在本 README 增加一行工具说明，保证可发现性。
