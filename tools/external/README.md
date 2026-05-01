# 🔌 tools/external：外部仓库与第三方工具

`tools/external/` 用来收纳第三方工具、外部依赖与 Git submodule。核心原则是：

- **尽量原样保留**：避免“魔改后不可升级”
- **隔离依赖与风险**：外部工具的依赖不要污染主仓库
- **可追溯**：来源、许可证、用法要写清楚

## 目录结构

```text
tools/external/
├── AGENTS.md                    # 本目录的 Agent 行为准则
├── README.md                    # 本文件（外部工具索引）
├── .tmux/                       # submodule：oh-my-tmux 配置
├── tmux/                        # submodule：tmux 源码
├── claude-official-skills/      # submodule：Claude 官方 skills 仓库
├── Skill_Seekers-development/   # submodule：Skills 制作器
├── html-tools-main/             # HTML 工具集
├── my-nvim/                     # Neovim 配置
├── MCPlayerTransfer/            # MC 玩家迁移工具
└── XHS-image-to-PDF-conversion/ # 图片合并 PDF 工具
```

## 工具清单

- `Skill_Seekers-development/`：以 submodule 引入的 Skills 抓取/制作器
- `.tmux/`：以 submodule 引入的 oh-my-tmux 配置来源
- `tmux/`：以 submodule 引入的 tmux 上游源码
- `claude-official-skills/`：以 submodule 引入的 Claude 官方 skills 仓库
- `html-tools-main/`：HTML 工具集
- `my-nvim/`：个人 Neovim 配置
- `MCPlayerTransfer/`：MC 玩家迁移工具
- `XHS-image-to-PDF-conversion/`：图片合并 PDF 工具

## 相关迁移

- 提示词转换工具已迁移到 `tools/prompts-library/`。
- AI 聊天记录保存工具已迁移到 `tools/chat-vault/`。
- 备份脚本已迁移到 `scripts/backups/`。
- 技能库入口已迁移到 `skills/`。

## 当前软链接显示

| 事实来源 | 展示入口 | 说明 |
|:---|:---|:---|
| `tools/external/.tmux/` | `skills/tmux-autopilot/assets/oh-my-tmux` | oh-my-tmux 配置来源 |
| `tools/external/tmux/` | `skills/tmux-autopilot/assets/tmux-src` | tmux 上游源码入口 |
| `tools/external/claude-official-skills/` | `skills/claude-official-skills` | Claude 官方 skills 仓库 |
| `tools/external/Skill_Seekers-development/` | `skills/auto-skill/scripts/Skill_Seekers-development` | `auto-skill` 的 Skill Seekers 工具来源 |

## 表达规则

- 完整外部仓库：优先 `git submodule add <url> tools/external/<name>`。
- 跨目录展示入口：使用相对软链接，例如 `skills/<name> -> ../tools/external/<name>`。
- 不允许：软链接到本机绝对路径、复制大型上游源码、提交构建产物/生成物、提交二进制运行时。
- 需要本地改造第三方工具时：优先 fork 后以 submodule 指向 fork；不要在主仓库直接魔改一份不可升级的源码快照。

## 新增外部工具（最小清单）

1. 优先新增 submodule：`git submodule add <url> tools/external/<tool-name>`。
2. 只在没有上游仓库、且体量小/与本项目强耦合时，才创建普通目录：`tools/external/<tool-name>/`。
3. 必备文件：`README.md`（用途/入口/依赖/输入输出）、许可证与来源说明（如 `LICENSE` / `SOURCE.md`）。
4. 依赖约束：尽量使用工具自带的虚拟环境/容器化方式，不影响仓库其他部分。
5. 文档同步：在本 README 增加一行工具说明，保证可发现性。
