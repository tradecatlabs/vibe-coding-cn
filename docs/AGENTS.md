# Documents 目录 Agent 指南

## 目录用途

`docs/` 是人类知识库：入门教程与功法体系分工。可复用方法论、哲学、思维模型、工程准则和流程的完整正文统一进入 `gongfa/`。
根级 `research/` 维护具体对象、原始事实与验证观察；稳定或待验证的可复用解释/方法正文归功法，保留来源与状态，移动不意味着验证通过。

## 目录结构

```text
docs/
├── README.md          # 知识库总导航
├── AGENTS.md          # docs 总操作规则
├── getting-started/   # 学习路线、环境配置与第一个可验收练习
└── gongfa/            # 思想、准则、模型、方法及配套文集的唯一正文位置
```

## 关键入口

- `getting-started/README.md` 与 `AGENTS.md`：启动教程、环境、学习地图与最小实践的边界。
- `gongfa/README.md`：按问题任务选择功法文集。
- `gongfa/AGENTS.md`：正文、历史来源、登记、生成视图与研究/运行能力的职责分离。
- `../metadata/gongfa/README.md`：功法身份、内容版本、已有初评和生成总表。
- `../research/README.md` 与 `AGENTS.md`：具体对象的观测、原始事实和研究验证。

## 操作规范

- 新增/修改文档、修复过时信息；正文按唯一职责放置，不重建已退役的独立哲学或方法目录。
- 入门区不复制通用方法正文；教程可以保留实例和必要说明，链接至功法。
- 创建目录必须具备 README 和 AGENTS；未经明确要求不删除文档或造成链接失效。
- 文档移动需同步所有当前消费者，保留历史来源和稳定锚点；不保永久转发页或旧可编辑副本。

## README 结构契约

所有 `docs/**/README.md` 面向人类，依次包含：

1. 一个 H1，后面直接进入 `## 字多不看`。
2. `## 字多不看`，3–7 条最短判断与阅读入口。
3. `## 快速导航`。
4. 标准 `<details>/<summary>` 完整细粒度目录。
5. `## 使用方式`。
6. `## 正文`，正文已拆分到独立文档，不在索引承载长正文。

README 不使用“和其他目录的边界”“维护规则”标题或维护者口径；维护规则写 AGENTS。

## 同步与验证

- 正文新增、移动、删除、重命名：同步本级 README、`docs/README.md`、`metadata/taxonomy.yml` 和必要 redirects。
- 面向 AI 的入口变化：同步 `llms.txt`、`assets/ai-citation/llms-full.txt` 和摘要中的当前路径。
- 功法的身份、版本、初评和快照变化遵守 `gongfa/AGENTS.md` 与 `../metadata/gongfa/AGENTS.md`。
- 修改 docs README 后运行 `make sync-doc-toc`；任务末运行 `make test`，结构、链接与目录门禁不能弱化。
- 不确定项标注 TODO，不猜测、不把迁移和语法检查称为原典、许可或效果验证。

## 命名

文件名使用清晰英文，文档使用中文；保留已有稳定 ID 与锚点，路径变化不自动变更内容身份。
