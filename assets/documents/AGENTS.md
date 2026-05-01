# Documents 目录 Agent 指南

## 目录用途

`assets/documents/` 存放项目知识库文档，包含方法论、入门指南、实战案例等。

## 目录结构

```
assets/documents/
├── principles/          # 原则与思想（fundamentals + philosophy）
│   ├── fundamentals/    # 基础原则、问题求解、工程范式与代码质量
│   └── philosophy/      # 原 05-哲学与方法论
├── guides/              # 入门与方法（getting-started + playbook）
│   ├── getting-started/ # 原 01-入门指南
│   └── playbook/        # 原 02-方法论
├── case-studies/        # 原 03-实战
└── workflow/            # 可复用工作流模板
```

## 关键入口

- `guides/getting-started/README.md`：零基础学习路径索引。
- `guides/getting-started/Vibe Coding 校验.md`：语言化、门禁、人机分工与 Vibe Coding 工程闭环。
- `guides/getting-started/Codex-CLI配置.md`：默认 AI CLI 路线。
- `guides/getting-started/OpenCode-CLI配置.md`：Codex CLI 不可用时的备选路线。
- `principles/fundamentals/拼好码.md`：胶水原则与复用优先的工程交付方法。

## 操作规范

### 允许
- 新增/修改文档内容
- 修复错误和过时信息
- 添加新的实战案例
 - 为每个一级目录维护 `README.md` 作为索引入口（如存在）

### 禁止
- 删除现有文档（除非明确要求）
- 大规模重命名/移动文件导致链接失效（如必须调整，需同步更新引用）

## 命名规范

- 文件名使用中文
- 使用 Markdown 格式
- 目录名使用简短英文（便于跨平台与链接稳定）
