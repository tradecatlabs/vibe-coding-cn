# 🔌 repo/libs/external：外部集成与第三方工具

`repo/libs/external/` 用来收纳第三方工具、外部依赖与集成模块。核心原则是：

- **尽量原样保留**：避免“魔改后不可升级”
- **隔离依赖与风险**：外部工具的依赖不要污染主仓库
- **可追溯**：来源、许可证、用法要写清楚

## 目录结构

```
repo/libs/external/
├── README.md
├── chat-vault/                                  # AI 聊天记录保存工具
├── prompts-library/                             # 提示词库管理工具（Excel ↔ Markdown）
├── l10n-tool/                                   # 多语言翻译脚本
├── my-nvim/                                     # Neovim 配置（含 nvim-config/）
├── MCPlayerTransfer/                            # MC 玩家迁移工具
├── XHS-image-to-PDF-conversion/                 # 图片合并 PDF 工具
└── .gitkeep
```

## 工具清单（入口与文档）

- `chat-vault/`：AI 聊天记录保存工具，支持 Codex/Kiro/Gemini/Claude CLI（详见 [`chat-vault/README_CN.md`](./chat-vault/README_CN.md)）
- `prompts-library/`：提示词 Excel ↔ Markdown 批量互转与索引生成（详见 [`prompts-library/README.md`](./prompts-library/README.md)）
- `l10n-tool/`：多语言批量翻译脚本
- `my-nvim/`：个人 Neovim 配置（详见 [`my-nvim/README.md`](./my-nvim/README.md)）
- `MCPlayerTransfer/`：MC 玩家迁移工具
- `XHS-image-to-PDF-conversion/`：图片合并 PDF（详见 [`XHS-image-to-PDF-conversion/README.md`](./XHS-image-to-PDF-conversion/README.md)）

> 📝 `system-prompts-and-models-of-ai-tools-main-cn/` 已移至 [`prompts/system_prompts/`](../../prompts/system_prompts/)

## 新增外部工具（最小清单）

1. 创建目录：`repo/libs/external/<tool-name>/`
2. 必备文件：`README.md`（用途/入口/依赖/输入输出）、许可证与来源说明（如 `LICENSE` / `SOURCE.md`）
3. 依赖约束：尽量使用工具自带的虚拟环境/容器化方式，不影响仓库其他部分
4. 文档同步：在本 README 增加一行工具说明，保证可发现性
