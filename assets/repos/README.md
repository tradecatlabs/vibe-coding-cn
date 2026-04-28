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

> 📝 系统提示词已迁移到云端表格，入口见 [`assets/prompt/README.md`](../prompt/README.md)。

## 外部仓库治理分析（2026-04-28）

目标：`assets/repos/` 只保留外部仓库的可追溯入口，不把大型第三方源码、二进制产物或生成物长期塞进主仓库。GitHub 中优先用
Git submodule 表示上游仓库；如需在其它目录暴露入口，则用相对软链接指向 `assets/repos/<repo>/`。

| 目录 | 当前状态 | 建议 | 原因 |
|:---|:---|:---|:---|
| `.tmux/` | submodule | 保持 | 上游清晰，主仓库只记录 commit 指针 |
| `tmux/` | submodule | 保持 | 上游源码体量较大，已正确用 submodule 表示 |
| `claude-official-skills/` | submodule | 保持；`assets/skills/claude-official-skills` 用相对软链暴露 | 官方 skills 应作为外部权威仓库，不复制源码 |
| `Skill_Seekers-development/` | 主仓库直接追踪源码；`auto-skill` 通过软链接引用 | 后续可再评估是否转 submodule | 已消除 `auto-skill` 内重复源码，当前单一来源为 `assets/repos/Skill_Seekers-development/` |
| `my-nvim/` | 主仓库直接追踪源码与二进制 | 高优先级改为 submodule 或清退二进制后只保留索引 | 包含大型 `nvim` 可执行文件，污染主仓库体量 |
| `chat-vault/` | 主仓库直接追踪源码 | 中高优先级拆为独立仓库/submodule，或至少清退内嵌第三方监控源码 | 目录体量大，且含 vendored `monitor-tui`/第三方代码 |
| `prompts-library/` | 主仓库直接追踪工具源码 | 中优先级拆分：工具用 submodule，生成输出不跟踪 | 上游/工具属性明显，`prompt_jsonl/` 属生成输出且已加入忽略规则 |
| `html-tools-main/` | 主仓库直接追踪源码 | 中优先级改为 submodule | README 指向外部 GitHub 仓库，适合用指针表示 |
| `XHS-image-to-PDF-conversion/` | 主仓库直接追踪源码 | 中优先级改为 submodule | README 指向外部 GitHub 仓库，适合用指针表示 |
| `MCPlayerTransfer/` | 主仓库直接追踪源码 | 暂缓；先补来源/许可证，再决定是否独立仓库化 | 当前未发现明确上游 URL，体量小 |
| `backups/` | 主仓库直接追踪备份脚本与存档目录 | 保持；继续禁止删除 `gz/` 存档 | 属本项目历史备份资产，不是外部仓库镜像 |

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
