# References 目录 Agent 指南

## 目录职责

`docs/references/` 存放工程实践、技术栈、质量门禁、模板和检查清单。

这里的文档回答：

- 项目应该如何组织。
- AI 编程应该如何设置硬门禁。
- 常见技术栈如何选择和组合。
- 工程经验如何变成可执行清单。

## 文件地图

```text
references/
├── README.md  # 索引入口：参考资料导航
├── project-architecture-template.md
├── python-project-skeleton.md
├── enterprise-architecture-template.md
├── modern-enterprise-architecture-template.md
├── dataset-first-data-service.md
├── code-organization.md
├── development-experience.md
├── quality-gates-and-pitfalls.md
├── low-level-program-logic.md
├── technology-stack.md
├── AGENTS.md  # 本目录操作规则
```

## 修改规则

- 继承 `docs/AGENTS.md` 的 README 结构契约：H1 后直接进入 `## 字多不看`，再按 `快速导航 -> 完整细粒度目录 -> 使用方式 -> 正文` 排列。
- 新增参考资料时，优先写入对应独立主题文档，并同步更新 `README.md` 索引。
- 检查清单、模板、质量门禁和经验类内容优先进入对应独立文档，避免重新塞回 README。
- 技术选型、技术栈组合和学习路径优先维护在 `technology-stack.md`。
- 不在本目录写一次性研究笔记；新技术判断应先放入 `docs/research/`。
- 不在 README 正文中写 `和其他目录的边界` 或 `维护规则`；维护者规则只写本文件。

## 质量要求

- 参考文档必须可执行、可检查、可复用。
- 门禁类内容尽量转成测试、CI、脚本、schema、类型或检查清单。
- 不确定项必须标注 TODO，不能编造成熟结论。
- 提交前必须运行 `make sync-doc-toc` 和 `make test`，确保锚点、链接和目录结构一致。
