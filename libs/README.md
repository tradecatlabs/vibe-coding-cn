# 📦 通用库与外部集成 (libs)

`libs/` 用来放两类东西：

1. **内部可复用的胶水代码**：小而稳、低耦合、可替换（`common/`）
2. **第三方工具与外部集成**：尽量保持原样、只做最薄适配（`external/`）

`database/` 预留未来的数据持久化层（当前仅占位）。

## 目录结构

```text
libs/
├── README.md
├── common/
│   ├── README.md
│   ├── __init__.py
│   ├── models/
│   │   └── __init__.py
│   └── utils/
│       └── backups/
│           ├── README.md
│           ├── 快速备份.py
│           └── 一键备份.sh
├── database/
│   ├── README.md
│   └── .gitkeep
└── external/
    ├── README.md
    ├── chat-vault/
    ├── prompts-library/
    ├── l10n-tool/
    ├── my-nvim/
    ├── MCPlayerTransfer/
    ├── XHS-image-to-PDF-conversion/
    └── .gitkeep
```

## 子目录职责与边界

### `common/`：内部通用模块

- 入口：[`common/README.md`](./common/README.md)
- 只放 **可复用** 的基础能力：模型、工具函数、脚本等
- 不要把业务逻辑、项目临时代码塞进来
- 约定：新增/调整能力时，同步更新 `libs/common/README.md`

### `database/`：数据库适配层（预留）

- 入口：[`database/README.md`](./database/README.md)
- 目标是把“存储细节”关进盒子里：连接、迁移、查询适配、事务边界
- 约定：实现前先写清楚目录结构与边界（见 `libs/database/README.md`）

### `external/`：第三方工具与外部集成

- 入口：[`external/README.md`](./external/README.md)
- 尽量保持第三方代码原样，避免“魔改后不可升级”
- 每个工具目录至少包含：`README.md`（用途/入口/依赖）与许可证/来源说明
- 约定：新增外部工具时，同步更新 `libs/external/README.md`

## 常用入口

- AI 聊天记录保存：
  [`external/chat-vault/`](./external/chat-vault/)（支持 Codex/Kiro/Gemini/Claude CLI）
- 提示词批量管理：
  [`external/prompts-library/`](./external/prompts-library/)（配合 `../prompts/` 使用）
- 备份工具：优先使用仓库根目录的 `backups/`（当前与 `libs/common/utils/backups/` 内容一致）

## 贡献约定（最小要求）

1. 新增模块先定义职责边界，再写代码/文档
2. 新增依赖记录安装方式与最低版本（必要时补充到 `documents/工具集.md`）
3. 目录结构/职责变化时，更新对应 README，保证“文档即真相源”
