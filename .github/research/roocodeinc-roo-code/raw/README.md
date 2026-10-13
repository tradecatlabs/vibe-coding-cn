# raw 事实层

本目录保存 `RooCodeInc/Roo-Code` 的本地原始材料快照。

这里不写分析结论，只保存可复查的一手资料：

- `sources.yml`：来源清单、拉取时间、命令和文件状态。
- `repository/`：Git 仓库工作树；本目录由 `.gitignore` 忽略，只作为本地研究材料。
- `github-repo.raw.json`：GitHub 仓库元数据。
- `github-readme.raw.md.txt`：GitHub README 原文快照。
- `github-license.raw.txt`：GitHub license 原文快照；仓库无 license 时可能不存在。
- `github-root-contents.raw.json`：默认分支根目录内容快照。
- `github-languages.raw.json`：GitHub language 统计快照。
- `github-latest-release.raw.json`：最新 release 快照；无 release 时可能不存在。

`repository/` 是外部源码快照，不参与本仓库 Markdown、链接、README/AGENTS 覆盖检查。原始 README 使用 `.txt` 后缀保存，避免其中的外部相对链接被本仓库 Markdown 链接检查误判。
