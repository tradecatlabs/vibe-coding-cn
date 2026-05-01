# Documents 目录 Agent 指南

## 目录用途

`docs/` 存放项目核心知识库文档，包含入门路径、核心概念、操作指南、工具方法与参考清单。

## 目录结构

```text
docs/
├── README.md             # 知识库总索引
├── getting-started/      # 从零开始、学习地图、环境与 AI CLI 配置
├── concepts/             # 核心概念、方法论与底层模型
├── guides/               # 操作型指南
├── playbooks/            # 工具方法与专项实践文档
├── references/           # 清单、约束、常见坑、审查标准
└── faq.md                # 高频问题
```

## 关键入口

- `README.md`：知识库总索引。
- `getting-started/学习地图.md`：按目标选择学习路径。
- `getting-started/Vibe Coding 经验.md`：语言化、门禁、人机分工与 Vibe Coding 工程闭环。
- `getting-started/Codex-CLI配置.md`：默认 AI CLI 路线。
- `concepts/拼好码.md`：复用优先、能力编排、边界治理与工程门禁。
- `guides/仓库维护与质量门禁.md`：仓库维护、迁移检查和质量门禁指南。

## 操作规范

### 允许

- 新增/修改文档内容。
- 修复错误和过时信息。
- 为每个一级目录维护 `README.md` 作为索引入口（如存在）。

### 禁止

- 删除现有文档（除非明确要求）。
- 大规模重命名/移动文件导致链接失效（如必须调整，需同步更新引用）。

## 命名规范

- 文件名使用中文或清晰英文。
- 使用 Markdown 格式。
- 目录名使用简短英文，保证跨平台与链接稳定。
