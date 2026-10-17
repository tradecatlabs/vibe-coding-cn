# aaif-goose/goose 深度研究

## 研究级别

- 当前级别：L2 多入口 Agent 与扩展架构研究。
- 研究对象：aaif-goose/goose。
- 证据来源：本目录 raw/ 下的 README、crates、documentation、workflow_recipes 和 evals。
- 观察日期：2026-09-08。

## L2 结论

Goose 的源码按 Rust workspace 拆出 goose-agent、goose-providers、goose-mcp、goose-context-management、goose-sdk、CLI 和 UI 等边界；仓库还把 workflow recipe 和 evals 作为单独资产。这个结构说明可扩展 Agent 的复杂度主要来自“模型适配、工具扩展、上下文、界面和验证”之间的组合，而不只是模型调用本身。

## 关键机制

### Provider 与 Agent 分离

不同模型服务由 provider 层适配，Agent 层负责任务循环和工具协作。这样更换模型不会直接改变任务流程。

### MCP 与扩展面

goose-mcp、documentation/plugins 和 examples/mcp 表明扩展是独立边界。扩展可以增加能力，也会增加信任、网络和数据访问风险。

### 上下文管理

goose-context-management 是独立 crate，说明上下文裁剪、压缩和历史管理在长任务中需要显式所有权。

### Recipe 与评估

workflow_recipes 和 evals 将可复用流程与质量验证分开。流程有了不等于结果可靠，必须有评估。

## 可迁移模式

- 在本仓研究矩阵中单独标注模型层、Harness 层、工具层和扩展层。
- 将长期上下文写入 AGENTS/文档，将短期命令输出作为证据，不混为一谈。
- 对 workflow 资产配套失败和回滚检查。
- 对外部资源保留来源、许可证和观察日期。

## 迁移边界

- 本仓不是通用 Agent 平台，不需要增加 provider 抽象或 MCP runtime。
- 不将 Rust workspace 的模块划分直接映射到本仓 docs 目录。
- 只有当某个扩展被本仓真实使用时，才新增具体配置文档。

## L3 验证任务

1. 为本仓工具与资源索引补“用途/权限/验证/撤销”字段。
2. 选一个外部扩展做只读来源审计，不运行安装器。
3. 对一条长文档研究任务记录上下文输入、输出证据和压缩边界。
