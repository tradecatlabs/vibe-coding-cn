# 知识库总索引

> `docs/` 是本仓库的核心知识库入口，承载从零开始、核心概念、哲学模型、研究笔记和工程参考资料。

## 目录地图

| 目录 | 定位 | 首选入口 |
|:---|:---|:---|
| [getting-started](./getting-started/) | 从零开始的线性入门教程 | [Vibe Coding 经验](./getting-started/README.md#1-vibe-coding-经验) / [学习地图](./getting-started/README.md#1-学习地图) |
| [concepts](./concepts/) | 核心概念、问题求解与工程思想 | [核心概念索引](./concepts/README.md) |
| [philosophy](./philosophy/) | 哲学方法论、思维模型与底层认知模型 | [哲学方法论工具箱](philosophy/README.md#philosophy-methodology-toolbox-怎么选) |
| [references](./references/) | 工程实践、技术栈、模板和检查清单 | [参考资料索引](./references/README.md#目录定位) |
| [research](./research/) | 新技术、优秀 repo 与工程范式研究 | [研究笔记索引](./research/README.md) |

## 推荐阅读路径

### 新手路径

1. [从零开始完整入门](./getting-started/README.md#1-学习地图)
2. [Vibe Coding 经验](./getting-started/README.md#1-vibe-coding-经验)
3. [问题求解](concepts/README.md#concept-problem-solving)
4. [拼好码](concepts/README.md#concept-glue-coding)
5. [工程实践](references/README.md#reference-engineering-practice)

### 开发者路径

1. [拼好码](concepts/README.md#concept-glue-coding)
2. [系统构建方法](concepts/README.md#concept-system-building)
3. [技术栈](references/README.md#reference-technology-stack)
4. [工程实践](references/README.md#reference-engineering-practice)

### 思维模型路径

1. [思维模型](philosophy/README.md#philosophy-thinking-models)
2. [组合描述模型](philosophy/README.md#philosophy-compositional-description-model)
3. [编程之道](philosophy/README.md#philosophy-programming-dao)
4. [递归自优化系统](concepts/README.md#concept-recursive-self-optimizing-system)

### AI Agent 读取路径

1. [根目录 AGENTS](../AGENTS.md)
2. [docs 目录 AGENTS](./AGENTS.md)
3. [从零开始完整入门](./getting-started/README.md#1-学习地图)
4. [Vibe Coding 经验](./getting-started/README.md#1-vibe-coding-经验)
5. [工程实践](references/README.md#reference-engineering-practice)
6. [AI 引用语料](../assets/ai-citation/README.md)

<details>
<summary><strong>完整细粒度目录（默认收起）</strong></summary>

### 全部文档索引

### getting-started

- [README](./getting-started/README.md#顶部导航) - 从零开始完整入门，包含学习地图、Vibe Coding 经验、网络配置、CLI 配置与开发环境搭建。
- [Vibe Coding 经验](./getting-started/README.md#1-vibe-coding-经验) - 通用语言能力、人机分工、机器门禁和入门铁律。
- [AGENTS](./getting-started/AGENTS.md) - 入门教程目录操作规则。

### concepts

- [README](./concepts/README.md) - 核心概念索引。
- [AGENTS](./concepts/AGENTS.md) - 核心概念目录操作规则。
- [问题求解](concepts/README.md#concept-problem-solving) - 用目标、现状、差距、标准、约束、对象和路径定义问题。
- [拼好码](concepts/README.md#concept-glue-coding) - 复用成熟能力，用胶水代码连接、编排、适配业务流程。
- [系统构建方法](concepts/README.md#concept-system-building) - 自顶向下、自底向上与分而治之的组合使用。
- [开发范式演进](concepts/README.md#concept-development-paradigms) - 软件工程组织方式的演进。
- [语言层要素](concepts/README.md#concept-language-layers) - 看懂代码需要掌握的语言层要素。
- [递归自优化系统](concepts/README.md#concept-recursive-self-optimizing-system) - 递归自优化生成系统的形式化模型。

### philosophy

- [README](philosophy/README.md#philosophy-methodology-toolbox-怎么选) - 哲学方法论工具箱。
- [AGENTS](./philosophy/AGENTS.md) - 哲学方法论目录操作规则。
- [思维模型](philosophy/README.md#philosophy-thinking-models) - 可复用思维模型索引。
- [组合描述模型](philosophy/README.md#philosophy-compositional-description-model) - 用对象、状态、快照、序列、过程、变换、同一/差异与关系描述复杂系统。
- [编程之道](philosophy/README.md#philosophy-programming-dao) - 编程哲学与工程判断。

### references

- [README](./references/README.md) - 参考资料索引。
- [AGENTS](./references/AGENTS.md) - 参考资料目录操作规则。
- [工程实践](references/README.md#reference-engineering-practice) - 项目架构、代码组织、开发经验、质量门禁与常见坑。
- [技术栈](references/README.md#reference-technology-stack) - 技术栈选型、组合案例与初学者学习路径。

### research

- [README](./research/README.md) - 研究笔记索引。
- [AGENTS](./research/AGENTS.md) - 研究笔记目录操作规则。
- [Harness 工程解析](research/README.md#research-harness-engineering) - Harness Engineering 的工程控制、评估器与反馈闭环解析。

</details>

## 维护规则

- 每个目录必须同时维护 `README.md` 和 `AGENTS.md`。
- 新增、删除、移动、重命名文档时，必须同步更新本索引、所在目录索引和 `metadata/taxonomy.yml`。
- 面向 AI 引用的重要入口变化，必须同步更新 `assets/ai-citation/llms-full.txt` 和相关摘要文件。
- 不确定信息标注 TODO，不用猜测补齐。
