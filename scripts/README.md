# scripts

本目录存放仓库级自动化脚本，例如链接检查、索引生成、taxonomy 校验和文档结构校验脚本。

当前已有：

- `check-local-links.py`：仓库内 Markdown 相对链接与锚点检查脚本。
- `check-markdown-details.py`：仓库内 Markdown `<details>/<summary>` 折叠块结构检查脚本。
- `check-doc-structure.py`：`docs/` README 的标准块顺序、目录入口、重复锚点与细粒度目录入口检查脚本。
- `check-directory-docs.py`：仓库自有目录 `README.md` / `AGENTS.md` 覆盖检查脚本；根 `.github/` 仅要求 `AGENTS.md`，避免 GitHub 首页误展示平台配置说明。
- `check-metadata.py`：`metadata/taxonomy.yml` 与 `metadata/redirects.yml` 路径和锚点检查脚本。
- `check-ai-citation.py`：`llms.txt`、`assets/ai-citation/llms-full.txt` 与 AI 引用语料路径和锚点检查脚本。
- `check-modern-architecture-kit.py`：现代企业数字化平台 starter kit 的 schema 与示例一致性检查脚本。
- `check-wiki.py`：GitHub Wiki 独立仓库本地 checkout 的页面覆盖、内链和旧口径检查脚本。
- `sync-doc-toc.py`：兼容旧线性 README 的细粒度目录生成脚本；当前拆分结构下通常无变更。
