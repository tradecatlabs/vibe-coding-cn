# References Sources Agent 指南

## 目录职责

`docs/references/sources/` 是 `docs/references/README.md` 的唯一正文来源。

## 修改规则

- 不直接编辑 `docs/references/README.md` 的主体内容。
- 新增或调整参考资料时，先修改本目录中的有序源片段。
- 文件名前缀用于控制总文档顺序，例如 `00-`、`10-`、`20-`。
- 修改后运行 `make sync-reference-readme` 生成总文档。
- 提交前运行 `make test`，确认生成结果、锚点、链接和目录结构全部通过。

## 边界

- 工程经验、质量门禁、模板和常见坑归入 `10-engineering-practice.md`。
- 技术栈选型、组合方案和学习路径归入 `20-technology-stack.md`。
- 新技术、技术栈或优秀 repo 的短篇判断笔记先放入 `docs/research/`，稳定后再沉淀到 references。
