# Documents 目录 Agent 指南

## 目录用途

`docs/` 存放项目核心知识库文档，包含入门路径、核心概念与参考清单。

## 目录结构

```text
docs/
├── README.md             # 知识库总索引
├── AGENTS.md             # docs 总操作规则
├── getting-started/      # 从零开始、学习地图、环境与 AI CLI 配置
├── concepts/             # 核心概念、方法论与工程思想
├── philosophy/           # 哲学方法论、思维模型与底层认知模型
├── research/             # 新技术、技术栈、优秀 repo、工程范式和工具趋势研究
└── references/           # 清单、约束、常见坑、模板
```

## 关键入口

- `README.md`：知识库总索引。
- `AGENTS.md`：`docs/` 总操作规则。
- `concepts/README.md`：核心概念索引。
- `concepts/AGENTS.md`：核心概念目录操作规则。
- `getting-started/README.md`：从零开始完整入门，包含学习地图、Vibe Coding 经验、网络配置、CLI 配置与开发环境搭建。
- `getting-started/AGENTS.md`：入门教程目录操作规则。
- `concepts/拼好码.md`：复用优先、能力编排、边界治理与工程门禁。
- `concepts/问题求解.md`：目标、现状、差距、标准与反馈迭代的底层能力。
- `concepts/系统构建方法.md`：自顶向下、自底向上与分而治之的组合方法。
- `concepts/开发范式演进.md`：软件工程组织方式的历史演进。
- `concepts/递归自优化系统.md`：递归自优化生成系统的形式化模型。
- `philosophy/README.md`：哲学方法论工具箱入口。
- `philosophy/AGENTS.md`：哲学方法论目录操作规则。
- `philosophy/思维模型.md`：可复用认知工具入口。
- `philosophy/组合描述模型.md`：对象、状态、快照、序列、过程、变换、同一/差异与关系的组合描述模型。
- `philosophy/编程之道.md`：编程哲学与工程判断入口。
- `references/README.md`：参考资料索引。
- `references/AGENTS.md`：参考资料目录操作规则。
- `research/README.md`：新技术、技术栈、优秀 repo、工程范式和工具趋势研究入口。
- `research/AGENTS.md`：研究笔记目录操作规则。
- `research/Harness工程解析.md`：Harness Engineering 的工程控制、评估器与反馈闭环解析。
- `references/工程实践.md`：项目架构、代码组织、开发经验、质量门禁与常见坑的统一入口。
- `references/技术栈.md`：技术栈选型、组合案例与初学者学习路径。

## 操作规范

### 允许

- 新增/修改文档内容。
- 修复错误和过时信息。
- 为每个目录维护 `README.md` 作为索引入口。
- 为每个目录维护 `AGENTS.md` 作为 Agent 操作规则。

### 禁止

- 删除现有文档（除非明确要求）。
- 大规模重命名/移动文件导致链接失效（如必须调整，需同步更新引用）。
- 新增目录但不补 `README.md` 和 `AGENTS.md`。

## 命名规范

- 文件名使用中文或清晰英文。
- 使用 Markdown 格式。
- 目录名使用简短英文，保证跨平台与链接稳定。
