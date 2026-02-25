# repo/ 目录 Agent 指南

本目录用于收纳**可执行代码与外部依赖镜像**，将“知识库/提示词/技能”与“代码/第三方工具”做物理隔离，便于迁移与审计。

## 目录结构（当前）

```text
repo/
├── AGENTS.md
└── libs/
    ├── external/                  # 第三方工具与外部集成（含 Git submodule）
    └── common/
        └── utils/
            └── backups/           # 历史备份脚本快照（README + 脚本）
```

## 操作规范

- `repo/libs/external/`：尽量原样保留外部项目，优先使用 Git submodule 管理上游。
- `repo/libs/common/utils/backups/`：只做“脚本快照/参考”；常用备份优先使用仓库根目录 `backups/`。
- 若需要更新路径/结构，必须同步更新：根目录 `AGENTS.md`、`README.md` 及本文件，保证“文档即真相源”。
