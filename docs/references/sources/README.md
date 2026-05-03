# References Sources

本目录存放 `docs/references/README.md` 的源片段。

生成规则：

- `README.md` 与 `AGENTS.md` 不参与拼接。
- 其他 `*.md` 文件按文件名升序拼接。
- 修改源片段后运行 `make sync-reference-readme`。
- 提交前运行 `make test`，确保总文档与源片段一致。

当前片段：

- `00-intro.md`：参考资料总入口、常用入口、总目录和维护规则。
- `10-engineering-practice.md`：工程实践、项目架构、代码组织、开发经验、质量门禁和常见坑。
- `20-technology-stack.md`：技术栈选型、组合案例和学习路径。
