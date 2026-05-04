# Documents 目录 Agent 指南

## 目录用途

`docs/` 存放项目核心知识库文档，包含入门路径、核心概念与参考清单。

## 目录结构

```text
docs/
├── README.md             # 知识库总索引
├── AGENTS.md             # docs 总操作规则
├── getting-started/      # 从零开始、学习地图、环境与 AI CLI 配置
├── concepts/             # 线性总文档：核心概念、问题求解与工程思想
├── philosophy/           # 线性总文档：哲学方法论、思维模型与底层认知模型
├── research/             # 线性总文档：新技术、优秀 repo、工程范式和工具趋势研究
└── references/           # 线性总文档：工程实践、技术栈、清单与质量门禁
```

## 关键入口

- `README.md`：知识库总索引。
- `AGENTS.md`：`docs/` 总操作规则。
- `getting-started/README.md`：从零开始完整入门，包含学习地图、Vibe Coding 经验、网络配置、CLI 配置与开发环境搭建。
- `getting-started/AGENTS.md`：入门教程目录操作规则。
- `concepts/README.md`：线性总文档，包含问题求解、拼好码、系统构建方法、开发范式演进、语言层要素和递归自优化系统。
- `concepts/AGENTS.md`：核心概念目录操作规则。
- `philosophy/README.md`：线性总文档，包含思维模型、组合描述模型、编程之道和方法论工具箱。
- `philosophy/AGENTS.md`：哲学方法论目录操作规则。
- `references/README.md`：线性总文档，包含工程实践和技术栈。
- `references/AGENTS.md`：参考资料目录操作规则。
- `research/README.md`：线性总文档，包含新技术、优秀 repo、工程范式和工具趋势研究笔记。
- `research/AGENTS.md`：研究笔记目录操作规则。

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

## README 结构契约

所有 `docs/**/README.md` 必须面向人类阅读，按以下标准块顺序组织：

1. 顶部标题块：只允许一个 H1，且 H1 后必须直接进入 `## 字多不看`。
2. `## 字多不看`：用 3-7 条说明最短判断和阅读入口。
3. `## 快速导航`：列出主要章节、路线或常用入口。
4. `完整细粒度目录（点击展开/收起）`：使用标准 `<details>/<summary>` 折叠块。
5. `## 使用方式`：说明人类读者如何使用本文档。
6. `## 正文`：承载真正内容；没有正文内容时也保留结构锚点。

禁止在 README 中出现以下结构：

- H1 和 `## 字多不看` 之间的引用块、说明段或任何夹层内容。
- `### 和其他目录的边界`。
- `### 维护规则`。
- “本目录只保留”“不再新增”“同步 metadata”“同步 AI 引用”等维护者口径。

这些维护规则必须写入对应 `AGENTS.md`，不写入面向人类的 README。

## 维护规则

- 每个目录必须同时维护 `README.md` 和 `AGENTS.md`。
- 新增、删除、移动、重命名文档时，必须同步更新 `docs/README.md`、所在目录索引和 `metadata/taxonomy.yml`。
- 面向 AI 引用的重要入口变化，必须同步更新 `assets/ai-citation/llms-full.txt` 和相关摘要文件。
- 不确定信息标注 TODO，不用猜测补齐。
- 修改任意 docs README 后，运行 `make sync-doc-toc` 和 `make test`。
- `make check-doc-structure` 是 README 结构契约硬门禁；失败时必须先修结构，再继续提交。

## 命名规范

- 文件名使用中文或清晰英文。
- 使用 Markdown 格式。
- 目录名使用简短英文，保证跨平台与链接稳定。
